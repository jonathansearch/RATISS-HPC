# 📦 BOM — Bill of Materials RATISS-HPC (cluster 8 noeuds)

Prix estimés FCFA (sourçables Chine/Dubaï/local). Taux indicatif : 1 USD ≈ 600 FCFA.

**Objectif doctrine : le cluster complet < 400 000 FCFA**, contre plusieurs
millions pour un serveur HPC occidental d'occasion (qui en plus consomme 500 W+
et exige une climatisation).

---

## 🧠 Calcul (le cœur)

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 1 | SBC Rockchip RK3588 16 Go | Orange Pi 5 Plus / Rock 5B | 8 | 45 000 | 360 000 | Chine (Alibaba) |
| 2 | Carte microSD 64 Go A2 (boot) | SanDisk / Samsung | 8 | 4 500 | 36 000 | local |
| 3 | SSD NVMe 256 Go (nœud maître + stockage partagé) | WD SN770 ou clone | 2 | 18 000 | 36 000 | Dubaï |
| 4 | Dissipateur + ventilateur 5 V par SBC | kit ventilé ARM | 8 | 3 000 | 24 000 | Chine |

**Sous-total calcul : ~456 000 FCFA** (les SBC dominent — voir optimisation §fin)

---

## 🌐 Réseau

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 5 | Switch Gigabit 8 ports (unmanaged) | TP-Link TL-SG108 | 1 | 18 000 | 18 000 | local |
| 6 | Câbles RJ45 Cat6 0.5 m | sertis local | 8 | 800 | 6 400 | local |

**Sous-total réseau : ~24 400 FCFA**

---

## ⚡ Alimentation DC (directe depuis RATISS-GRID)

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 7 | Convertisseur DC-DC 48 V → 5 V 5 A | module abaisseur isolé | 8 | 4 000 | 32 000 | Chine |
| 8 | Connecteurs USB-C PD / barillet + câblage 1.5 mm² | | 1 | 8 000 | 8 000 | local |
| 9 | Fusibles 5 A par nœud + porte-fusibles | | 8 | 400 | 3 200 | local |

**Sous-total alimentation : ~43 200 FCFA**

> 💡 **Pourquoi du DC-DC direct ?** Chaque conversion AC→DC perd 10-20 %. En
> restant en DC du bus 48 V solaire jusqu'au 5 V des cartes, on économise deux
> conversions — c'est ~25 W de gagnés en permanence, soit ~220 kWh/an.

---

## 🌡️ Refroidissement liquide

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 10 | Plaques waterblock cuivre 40×40 mm | waterblock CPU universel | 8 | 3 500 | 28 000 | Chine |
| 11 | Pompe 12 V brushless | pompe PC watercooling | 1 | 9 000 | 9 000 | Chine/Dubaï |
| 12 | Radiateur automobile + ventilos | recyclé (casse auto) | 1 | 15 000 | 15 000 | local (récup) |
| 13 | Tubes PVC souple 8/10 + raccords + collier | | 1 | 8 000 | 8 000 | local |
| 14 | Liquide : eau distillée + glycol 30 % | antigel auto | 2 L | 3 000 | 6 000 | local |

**Sous-total refroidissement : ~66 000 FCFA**

---

## 🔩 Structure & divers

| # | Composant | Référence | Qté | PU (FCFA) | Total | Source |
|---|-----------|-----------|:---:|:---:|:---:|--------|
| 15 | Profilés aluminium 20×20 (rack) | 2 m | 6 | 4 000 | 24 000 | local |
| 16 | Plaques support SBC (imprimées 3D — Priorité 4 !) | PETG | 8 | 500 | 4 000 | atelier local |
| 17 | Visserie M3/M4, entretoises, écrous | | 1 | 5 000 | 5 000 | local |
| 18 | Ventilos extraction haut de rack 12 V | 120 mm | 2 | 2 500 | 5 000 | local |

**Sous-total structure : ~38 000 FCFA**

---

## 💰 Total projet

| Poste | Coût (FCFA) |
|-------|:---:|
| Calcul (SBC, stockage) | ~456 000 |
| Réseau | ~24 400 |
| Alimentation DC | ~43 200 |
| Refroidissement | ~66 000 |
| Structure | ~38 000 |
| **TOTAL** | **~627 600** |

> ⚠️ Au-delà de l'objectif initial — le poste SBC domine. **Optimisations
> réalistes** : démarrer avec 4 nœuds (~228 000 FCFA de moins, cluster extensible
> à chaud), SBC 8 Go au lieu de 16 Go (~8 000 FCFA/nœud d'économie), ou RK3566
> plus modeste pour les nœuds de stockage. **Version de démarrage 4 nœuds :
> ~400 000 FCFA** — l'extensibilité est un choix de conception, pas une limite.

### Comparaison avec l'alternative importée

| Solution | Coût | Conso | Autonomie solaire |
|----------|:---:|:---:|:---:|
| Serveur HPC occidental d'occasion | 3-10 M FCFA | 500-1000 W | impossible sans gros onduleur |
| **RATISS-HPC 8 nœuds** | **~628 k** | **~72 W** | **✅ 254 h sur batterie** |
| RATISS-HPC 4 nœuds (démarrage) | ~400 k | ~36 W | ✅ ~500 h |

---

*RATIS Labs · Cameroun — Sourçage régional privilégié, récupération encouragée.*
