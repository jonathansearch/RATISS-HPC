# 🔧 ASSEMBLY — Guide de montage RATISS-HPC

Document exécutable par un informaticien systèmes ou un technicien (ENSPY,
Polytech, diaspora). Chaque étape est vérifiable. Deux phases : **hardware**
(le rack physique) puis **logiciel** (le cluster qui calcule).

---

## ⚠️ Consignes de sécurité

- Le bus DC 48 V de RATISS-GRID peut débiter des courants élevés — **fusible
  5 A sur chaque nœud**, jamais de connexion directe sans protection.
- La boucle liquide : **tester l'étanchéité à vide** (sans électronique sous
  tension) pendant 24 h avant le premier démarrage.
- Vérifier la polarité de chaque convertisseur DC-DC **deux fois** avant de
  brancher une carte — une inversion grille le SBC instantanément.

---

## 🔩 A. Structure du rack

1. Assembler le cadre en profilés aluminium 20×20 : 4 étages, 2 SBC par étage.
2. Fixer les plaques support (imprimées 3D en PETG — produites par
   RATISS-ATELIER, Priorité 4) à chaque étage.
3. Installer les 2 ventilos 120 mm d'extraction en haut du rack.
4. **Vérification** : le rack ne doit pas vibrer au toucher ; les flux d'air
   vont bas → haut sans obstruction.

## ⚡ B. Alimentation DC

1. Relier le bus 48 V de RATISS-GRID à un bornier de distribution.
2. Pour chaque nœud : bornier → **fusible 5 A** → convertisseur DC-DC 48→5 V →
   connecteur SBC.
3. Régler chaque convertisseur à **5.1 V à vide** au multimètre AVANT de brancher
   la carte (les RK3588 tolèrent 5 V ±5 %).
4. **Vérification** : mesurer 5.0–5.2 V sous charge (une LED 5 W par exemple)
   sur chaque sortie.

## 🌡️ C. Refroidissement liquide

1. Fixer les waterblocks cuivre sur chaque RK3588 (pâte thermique fine, serrage
   en croix progressif).
2. Monter la boucle : waterblocks (série ou 2 branches de 4) → radiateur auto →
   pompe → retour.
3. Remplir eau distillée + glycol 30 %, purger l'air (incliner la boucle).
4. **Test d'étanchéité 24 h** : pompe seule en marche, papier absorbant sous
   chaque raccord. Aucune trace d'humidité tolérée.
5. **Vérification thermique** : sous stress (voir §E), chaque CPU < 70 °C avec
   la boucle active (le simulateur prédit ~58 °C — mesurer l'écart réel).

## 🌐 D. Réseau

1. Relier les 8 SBC au switch Gigabit (Cat6).
2. Le nœud 0 (`ratiss-master`) porte le SSD NVMe partagé (NFS) et le scheduler.
3. Attribuer des IP fixes : 10.0.0.10 → 10.0.0.17 (nœuds), 10.0.0.1 (master).

## 💻 E. Logiciel (le cluster qui calcule)

1. **OS** : flasher une image Linux ARM64 minimaliste (Armbian/Debian netinstall
   ou Yocto custom) sur chaque microSD. Pas d'environnement graphique.
2. **Master** : installer `slurm` (ordonnanceur) + `nfs-server` (stockage
   partagé) + `python3` + `numpy/scipy` compilés ARM64.
3. **Nœuds** : `slurmd` + montage NFS. Clés SSH du master vers tous les nœuds.
4. **Test de fumée** : `srun -N8 hostname` doit retourner les 8 noms de nœuds.
5. **Benchmark de réception** : lancer une multiplication de matrices MPI ou un
   job embarrassingly parallel ; mesurer le speedup réel et le comparer à la
   prédiction du simulateur (`benchmark_relative`). Écart documenté → recalibrer
   l'overhead du modèle.

## 🔄 Procédure d'itération (boucle RATISS)

```
Simuler → Assembler → Mesurer → Comparer → Recalibrer → Re-simuler
```

Les paramètres à recalibrer sur le rack réel : puissance mesurée en charge
(wattmètre sur le bus DC), température CPU réelle (→ R_th effective de la boucle),
overhead réseau mesuré (→ modèle d'Amdahl). **Documenter chaque écart.**

---

*RATIS Labs · Cameroun — Le DC ne pardonne pas : fusibles, polarité, étanchéité.*
