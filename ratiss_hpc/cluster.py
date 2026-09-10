"""RATISS-HPC — Cluster de calcul local souverain (Priorité 3).

Modélise la consommation énergétique, thermique et les performances d'un
cluster de Single Board Computers (SBC) low-power (Rockchip RK3588, RISC-V)
alimenté exclusivement par le micro-réseau solaire RATISS-GRID (Priorité 0).

Objectif : un cerveau de calcul local autonome — plus de dépendance à Colab,
IBM Cloud ou AlphaFold API. Si internet coupe ou si les sanctions tombent, la
recherche continue.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# --- Constantes mesurées/publiées (docs/PHYSICS.md) ---
# RK3588 : 8 cœurs (4×A76 + 4×A55), ~6-12 W en charge, benchmarkés SPEC
RK3588_CORES = 8
RK3588_POWER_IDLE_W = 2.5
RK3588_POWER_LOAD_W = 9.0
# Kendryte K210 (RISC-V 64 bits dual-core) : ~1 W
K210_CORES = 2
K210_POWER_LOAD_W = 1.0
AMBIENT_TROPICAL_C = 35.0
CPU_TJ_MAX_C = 85.0            # température max jonction RK3588
HEATSINK_RTH_PASSIVE = 8.0     # °C/W radiateur passif
HEATSINK_RTH_ACTIVE = 2.5      # °C/W radiateur + ventilateur


@dataclass
class SBCNode:
    """Un noeud de calcul (Single Board Computer)."""

    name: str
    cores: int = RK3588_CORES
    power_idle_w: float = RK3588_POWER_IDLE_W
    power_load_w: float = RK3588_POWER_LOAD_W
    ram_gb: float = 16.0

    def power_w(self, load_frac: float) -> float:
        """Puissance selon la charge (0 = idle, 1 = pleine charge)."""
        return self.power_idle_w + (self.power_load_w - self.power_idle_w) * load_frac


@dataclass
class Cluster:
    """Cluster de noeuds SBC alimenté par le micro-réseau solaire."""

    nodes: list = field(default_factory=list)

    @classmethod
    def standard(cls, n_nodes: int = 8) -> "Cluster":
        return cls(nodes=[SBCNode(f"rk3588-{i}") for i in range(n_nodes)])

    def total_cores(self) -> int:
        return sum(n.cores for n in self.nodes)

    def total_ram_gb(self) -> float:
        return sum(n.ram_gb for n in self.nodes)

    def power_w(self, load_frac: float) -> float:
        """Puissance totale du cluster à une charge donnée."""
        return sum(n.power_w(load_frac) for n in self.nodes)

    def daily_energy_wh(self, load_profile: np.ndarray, dt_h: float = 1.0) -> float:
        """Énergie journalière (Wh) pour un profil de charge horaire."""
        return float(sum(self.power_w(l) * dt_h for l in load_profile))

    def cpu_temp_c(self, load_frac: float, ambient_c: float = AMBIENT_TROPICAL_C,
                   rth: float = HEATSINK_RTH_ACTIVE) -> float:
        """Température CPU en régime : T = T_amb + P × Rth."""
        p = self.power_w(load_frac) / max(len(self.nodes), 1)
        return ambient_c + p * rth


def thermal_safe(cluster: Cluster, load_frac: float,
                 ambient_c: float = AMBIENT_TROPICAL_C,
                 active_cooling: bool = True) -> dict:
    """Vérifie que le cluster reste sous la température max de jonction."""
    rth = HEATSINK_RTH_ACTIVE if active_cooling else HEATSINK_RTH_PASSIVE
    t = cluster.cpu_temp_c(load_frac, ambient_c, rth)
    return {
        "cpu_temp_c": t,
        "t_max_c": CPU_TJ_MAX_C,
        "safe": bool(t < CPU_TJ_MAX_C),
        "margin_c": CPU_TJ_MAX_C - t,
        "cooling": "actif" if active_cooling else "passif",
    }


def solar_autonomy_hours(cluster: Cluster, battery_kwh: float,
                         load_frac: float = 0.7) -> float:
    """Autonomie du cluster sur batterie (RATISS-GRID) en heures."""
    p = cluster.power_w(load_frac)
    return battery_kwh * 1000.0 / p


def benchmark_relative(cluster: Cluster) -> dict:
    """Performance relative estimée (vs 1 noeud RK3588 = 1.0).

    Le speedup d'un cluster est sous-linéaire (loi d'Amdahl avec overhead de
    communication ~10 % typique pour du calcul embarassingly parallel).
    """
    n = len(cluster.nodes)
    overhead = 0.10
    speedup = n / (1.0 + overhead * (n - 1))  # Amdahl généralisé
    return {
        "n_nodes": n,
        "total_cores": cluster.total_cores(),
        "speedup_vs_single": float(speedup),
        "efficiency": float(speedup / n),
    }
