<p align="center">
  <img src="docs/assets/logo.png" alt="RATISS Labs logo" width="180"/>
</p>

[![RATISS Labs](https://img.shields.io/badge/RATISS_Labs-Deep_Tech_Sovereign-06b6d4)](https://github.com/jonathansearch)

<div align="center">

<img src="docs/images/05_logo_ratis_labs.png" alt="RATIS Labs" width="260"/>

# 🖥️ RATISS-HPC — Le Cluster de Calcul Local Souverain

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Citation](https://img.shields.io/badge/citation-CITATION.cff-blueviolet)](CITATION.cff)
[![Tests](https://img.shields.io/badge/tests-15%2F15-success)](tests/)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--4092--5313-a6ce39)](https://orcid.org/0009-0000-4092-5313)

> Propriété intellectuelle : **JOHNKING0 & Jonathan Evina** · RATIS Labs (Cameroun)
> ORCID [0009-0000-4092-5313](https://orcid.org/0009-0000-4092-5313)

**[📘 Document de conception complet → DESIGN.md](DESIGN.md)** ·
**[🔧 Guide de montage → docs/ASSEMBLY.md](docs/ASSEMBLY.md)** ·
**[📦 Liste de matériel → docs/BOM.md](docs/BOM.md)** ·
**[🔬 Références → docs/PHYSICS.md](docs/PHYSICS.md)** ·
**[🧮 Validation math/physique → scripts/validate_physics.py](scripts/validate_physics.py)**

</div>

> **Priorité 3** de la doctrine de souveraineté technologique. Un cluster de
> calcul de **64 cœurs ARM (8× RK3588)**, alimenté à 100 % par le micro-réseau
> solaire RATISS-GRID, refroidi par liquide, administré sous Linux minimaliste.
> **Si internet coupe ou si les sanctions tombent, la recherche continue.**

---

> 🇨🇲 **Un mot au Gouvernement de la République du Cameroun**
>
> La science camerounaise loue sa puissance de calcul à l'étranger — Colab,
> cloud IBM, API occidentales. Une coupure internet, une sanction, une
> facture en devises, et la recherche nationale s'arrête. RATISS-HPC brise
> cette dépendance : un cerveau de calcul **physique, local et autonome
> énergétiquement**, assemblé à partir de cartes low-cost, sans licence
> logicielle occidentale, tournant sur notre propre soleil. Ce dépôt en donne
> les plans et le simulateur. **La souveraineté numérique n'attend pas :
> elle se calcule ici.**

---

## 🖼️ Le projet en images

### 🌐 Plan de conception — architecture réseau + alimentation DC
![Plan architecture](docs/images/01_plan_architecture.png)

### 🌡️ Plan de conception thermique — refroidissement liquide custom
![Plan thermique](docs/images/02_plan_thermique.png)

### 🏭 Le cluster une fois monté (64 cœurs · 72 W · 100 % solaire)
![Appareil monté](docs/images/03_appareil_monte.png)

### 📈 Performances et autonomie énergétique
![Performances](docs/images/04_performances.png)

### ☀️ Couplage avec RATISS-GRID — une journée d'autonomie solaire
![Énergie journalière](docs/images/06_energie_journaliere.png)

### 🌡️ Carte thermique — pourquoi le refroidissement liquide n'est pas optionnel
![Carte thermique](docs/images/07_carte_thermique.png)

---

## 🎯 Pourquoi c'est une rupture

Dépendre de Colab, IBM Cloud ou AlphaFold API, c'est accepter que la recherche
camerounaise s'arrête à la première coupure internet ou sanction. Les serveurs
HPC classiques coûtent des millions, consomment une énergie qu'Eneo ne garantit
pas, et sont soumis aux licences logicielles occidentales.

**La réponse RATISS** : des Single Board Computers low-power (Rockchip RK3588,
RISC-V Kendryte K210) offrant un rapport performance/watt imbattable, alimentés
en DC direct par le solaire (Priorité 0), sans conversion AC/DC, sous Linux
minimaliste compilé pour les algorithmes RATISS (topologie, MD, docking).

## 🔧 Caractéristiques (config Standard)

| Caractéristique | Valeur |
|-----------------|--------|
| Noeuds | 8× Rockchip RK3588 |
| Cœurs totaux | **64 cœurs ARM** |
| RAM totale | 128 Go |
| Puissance pleine charge | ~72 W |
| Autonomie sur batterie 14.3 kWh | **~254 h** |
| Refroidissement | liquide (radiateur auto recyclé) |
| OS | Linux minimaliste (Yocto/Buildroot) |

## 🚀 Quick start

```bash
pip install numpy matplotlib pytest
cd ratiss-hpc

# Simuler le cluster
PYTHONPATH=. python -c "
from ratiss_hpc.cluster import Cluster, thermal_safe, solar_autonomy_hours
c = Cluster.standard(8)
print(f'{c.total_cores()} cœurs, {c.power_w(1.0):.0f} W pleine charge')
print('thermique 100% charge:', thermal_safe(c, 1.0))
print(f'autonomie 14.3 kWh: {solar_autonomy_hours(c, 14.3):.0f} h')
"

# Figures
PYTHONPATH=. python scripts/generate_figures.py

# VALIDATION MATH & PHYSIQUE (recalcul indépendant : thermique, Amdahl, énergie)
PYTHONPATH=. python scripts/validate_physics.py

# Tests
PYTHONPATH=. pytest tests/ -q
```

## 🧮 Validation mathématique & physique

`scripts/validate_physics.py` recalcule **indépendamment** chaque résultat du
simulateur et le confronte aux datasheets (Rockchip RK3588) et à la théorie
(loi d'Amdahl) — **8/8 validations** : loi d'Ohm thermique, marge pleine charge,
saturation du speedup à 1/s, cohérence énergie/autonomie.

## 💰 Coût et montage

- **[📦 BOM détaillée](docs/BOM.md)** : ~628 k FCFA pour 8 nœuds, **~400 k pour
  la version de démarrage 4 nœuds** (extensible à chaud) — contre 3-10 M FCFA
  pour un serveur HPC importé qui consomme 10× plus.
- **[🔧 Guide de montage](docs/ASSEMBLY.md)** : rack alu, alimentation DC 48 V
  directe, boucle liquide avec test d'étanchéité 24 h, Slurm + NFS, benchmark
  de réception.

## ⚠️ Transparence ingénierie

Ce dépôt produit des **prédictions de simulation** (consommation, thermique,
montée en charge par loi d'Amdahl). La validation finale exige le cluster
physique assemblé et benchmarké. **Toujours itérer, jamais figé.**

---

## 📄 Licence & citation

- **Licence** : [MIT](LICENSE) — © JOHNKING0 & Jonathan Evina, RATIS Labs (Cameroun).
- **Citation** : voir [CITATION.cff](CITATION.cff) — ORCID
  [0009-0000-4092-5313](https://orcid.org/0009-0000-4092-5313).

---

*Doctrine matérielle souveraine du Cameroun — Priorité 3 sur 5.*
