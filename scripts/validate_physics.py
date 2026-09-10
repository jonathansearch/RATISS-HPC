"""Outil en ligne de validation mathématique & physique — RATISS-HPC.

Recalcule INDÉPENDAMMENT chaque résultat du simulateur par une méthode
analytique différente, et le confronte à des références externes sourcées.
Si un écart dépasse la tolérance, la validation échoue (code de sortie 1).

Croisements :
  - thermique CPU : loi d'Ohm thermique T = T_amb + P·R_th
  - magnitude thermique : T doit rester < T_jonction max (datasheet Rockchip)
  - puissance : interpolation linéaire idle↔load (datasheet)
  - Amdahl : formule de speedup recalculée à la main
  - énergie/autonomie : cohérence E = P·t

Usage : PYTHONPATH=. python scripts/validate_physics.py
"""

from __future__ import annotations

import numpy as np

from ratiss_hpc.cluster import (Cluster, HEATSINK_RTH_ACTIVE, SBCNode,
                                benchmark_relative, solar_autonomy_hours,
                                thermal_safe)


def banner(txt):
    print("\n" + "=" * 68 + "\n" + txt + "\n" + "=" * 68)


def verdict(name, ok, detail):
    print(f"  [{'✅ PASS' if ok else '❌ FAIL'}] {name:<46} {detail}")
    return ok


def validate_thermal_ohms_law() -> bool:
    """Loi d'Ohm thermique : T = T_amb + P·R_th, recalculée à la main."""
    c = Cluster.standard(8)
    t_sim = c.cpu_temp_c(1.0, ambient_c=35.0, rth=HEATSINK_RTH_ACTIVE)
    p_per_node = 2.5 + (9.0 - 2.5) * 1.0          # interpolation indépendante
    t_ana = 35.0 + p_per_node * 2.5                # T_amb + P·R_th
    ok = abs(t_sim - t_ana) < 1e-9
    return verdict("Thermique: loi d'Ohm T = T_amb + P·R_th",
                   ok, f"T_sim={t_sim:.1f} °C vs T_ana={t_ana:.1f} °C")


def validate_thermal_margin() -> bool:
    """Sécurité thermique : pleine charge < T_jonction max (85 °C datasheet Rockchip)
    avec refroidissement actif — sinon la conception est invalide."""
    r = thermal_safe(Cluster.standard(8), 1.0, active_cooling=True)
    ok = r["safe"] and r["margin_c"] > 10.0
    return verdict("Thermique: marge pleine charge (actif)",
                   ok, f"T={r['cpu_temp_c']:.1f} °C, marge {r['margin_c']:.1f} °C")


def validate_passive_insufficient() -> bool:
    """Le refroidissement passif DOIT être insuffisant en climat tropical à pleine
    charge — c'est la justification physique de la boucle liquide. Si le passif
    suffisait, la conception serait surdimensionnée."""
    r = thermal_safe(Cluster.standard(8), 1.0, active_cooling=False)
    t = r["cpu_temp_c"]
    # passif : T = 35 + 9×8 = 107 °C → largement au-delà de 85 °C
    ok = not r["safe"]
    return verdict("Thermique: passif insuffisant (justifie le liquide)",
                   ok, f"T_passif={t:.0f} °C > 85 °C → boucle liquide justifiée")


def validate_power_linearity() -> bool:
    """Puissance : à charge 0 → idle, à charge 1 → load (datasheet RK3588)."""
    node = SBCNode("test")
    ok = (abs(node.power_w(0.0) - 2.5) < 1e-12
          and abs(node.power_w(1.0) - 9.0) < 1e-12)
    return verdict("Puissance: bornes idle/load (datasheet)",
                   ok, f"P(0)={node.power_w(0):.1f} W, P(1)={node.power_w(1):.1f} W")


def validate_amdahl_formula() -> bool:
    """Loi d'Amdahl généralisée : speedup = N/(1 + s(N-1)), recalculée à la main."""
    n, overhead = 8, 0.10
    r = benchmark_relative(Cluster.standard(n))
    expected = n / (1.0 + overhead * (n - 1))
    ok = abs(r["speedup_vs_single"] - expected) < 1e-12
    return verdict("Amdahl: speedup = N/(1+s(N-1))",
                   ok, f"speedup={r['speedup_vs_single']:.3f} (attendu {expected:.3f})")


def validate_amdahl_bounds() -> bool:
    """Loi d'Amdahl avec overhead linéaire : le speedup est strictement
    croissant avec N mais SATURÉ asymptotiquement à 1/s (= 10× pour s=10 %).
    C'est la signature physique de ce modèle : ajouter des nœuds donne des
    gains décroissants qui plafonnent — jamais un speedup ≥ N ni décroissant."""
    overhead = 0.10
    saturation = 1.0 / overhead
    prev = 0.0
    for n in (1, 2, 4, 8, 16, 64):
        s = benchmark_relative(Cluster.standard(n))["speedup_vs_single"]
        if not (prev < s < min(n, saturation) or n == 1):
            return verdict("Amdahl: croissance + saturation", False,
                           f"N={n} → {s:.2f} (prev={prev:.2f}, sat={saturation:.0f})")
        prev = s
    return verdict("Amdahl: croissante, saturée à 1/s = 10×", True,
                   "vérifié pour N = 1..64")


def validate_autonomy_consistency() -> bool:
    """Autonomie : E_batterie / P = heures, cohérence avec E = P·t."""
    c = Cluster.standard(8)
    h = solar_autonomy_hours(c, 14.3, load_frac=0.7)
    p = c.power_w(0.7)
    h_ana = 14.3 * 1000.0 / p
    ok = abs(h - h_ana) < 1e-9 and 100 < h < 400
    return verdict("Énergie: autonomie = E/P cohérente",
                   ok, f"{h:.0f} h à {p:.0f} W sur 14.3 kWh")


def validate_daily_energy() -> bool:
    """Énergie journalière : profil plat 70 % → E = 24 h × P(0.7)."""
    c = Cluster.standard(8)
    e = c.daily_energy_wh(np.full(24, 0.7))
    e_ana = 24.0 * c.power_w(0.7)
    ok = abs(e - e_ana) < 1e-6
    return verdict("Énergie: journalière = 24 h × P(charge)",
                   ok, f"{e:.0f} Wh/jour")


def main() -> int:
    banner("VALIDATION MATHÉMATIQUE & PHYSIQUE — RATISS-HPC\n"
           "Recalcul indépendant + confrontation aux datasheets et à Amdahl")
    checks = [
        validate_thermal_ohms_law,
        validate_thermal_margin,
        validate_passive_insufficient,
        validate_power_linearity,
        validate_amdahl_formula,
        validate_amdahl_bounds,
        validate_autonomy_consistency,
        validate_daily_energy,
    ]
    results = [fn() for fn in checks]
    banner("RÉSUMÉ")
    n_pass = sum(results)
    print(f"  {n_pass}/{len(results)} validations réussies")
    if n_pass == len(results):
        print("  ✅ Le simulateur thermique/énergétique/parallèle est cohérent.")
        return 0
    print("  ❌ Écarts détectés — corriger le simulateur.")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
