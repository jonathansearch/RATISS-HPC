# 🔬 PHYSICS — Références RATISS-HPC

## Thermique des processeurs
- Température de jonction max RK3588 : **85 °C** (fiche technique Rockchip).
- Résistance thermique radiateur : passif ~8 °C/W, actif (ventilé) ~2.5 °C/W.
  Source : *Incropera et al., Fundamentals of Heat and Mass Transfer (2011)*.
- Modèle : T_cpu = T_ambiante + P × R_th (loi d'Ohm thermique).

## Montée en charge parallèle
- **Loi d'Amdahl** : speedup sous-linéaire avec overhead de communication.
  Source : *Amdahl, "Validity of the single processor approach...", AFIPS (1967)*.

## Consommation
- RK3588 : ~2.5 W idle, ~9 W pleine charge (benchmarks publiés, datasheets).
- Kendryte K210 (RISC-V) : ~1 W (fiche Kendryte/Canaan).

*RATIS Labs · Cameroun — constantes vérifiables.*
