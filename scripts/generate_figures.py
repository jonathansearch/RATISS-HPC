"""Génère les figures RATISS-HPC : plans de conception, appareil, perfs, logo."""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle

OUT = os.path.join(os.path.dirname(__file__), "..", "docs", "images")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"figure.dpi": 110, "font.size": 11,
                     "axes.grid": True, "grid.alpha": 0.3})

RATIS_DARK = "#0b1f3a"; RATIS_GREEN = "#1f9d55"; RATIS_GOLD = "#e0a800"
RATIS_RED = "#c0392b"; RATIS_BLUE = "#4aa3df"


def save(fig, name, facecolor="white"):
    fig.savefig(os.path.join(OUT, name), bbox_inches="tight", facecolor=facecolor)
    plt.close(fig)
    print("généré :", name)


def _box(ax, x, y, w, h, text, fc, fs=8):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                facecolor=fc, edgecolor=RATIS_DARK, linewidth=1.5, zorder=2))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, zorder=3,
            fontweight="bold")


# 1. PLAN ARCHITECTURE RÉSEAU
def fig_plan_architecture():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    ax.set_title("PLAN DE CONCEPTION — Cluster HPC RATISS (8× RK3588, solaire)\n"
                 "Topologie réseau + alimentation DC depuis RATISS-GRID",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Switch central
    _box(ax, 5.0, 3.2, 2.0, 1.2, "Switch\nGigabit\n(local)", "#cfe0ff", 10)
    # 8 noeuds
    positions = [(0.7, 5.2), (3.0, 5.4), (8.0, 5.4), (10.3, 5.2),
                 (0.7, 0.9), (3.0, 0.7), (8.0, 0.7), (10.3, 0.9)]
    for i, (x, y) in enumerate(positions):
        _box(ax, x, y, 1.3, 0.9, f"RK3588\n#{i}\n8 cœurs", "#bfe6bf", 7)
        ax.annotate("", xy=(6.0, 3.8), xytext=(x+0.65, y+0.45),
                    arrowprops=dict(arrowstyle="-", color=RATIS_BLUE, lw=1.2))
    # Alim DC depuis GRID
    _box(ax, 5.0, 0.4, 2.0, 0.9, "RATISS-GRID\nbus DC 48 V\n(solaire)", "#ffd9b3", 8)
    ax.annotate("", xy=(6.0, 3.2), xytext=(6.0, 1.3),
                arrowprops=dict(arrowstyle="->", color=RATIS_RED, lw=2))
    ax.text(6.2, 2.2, "48 V DC", fontsize=8, color=RATIS_RED)

    ax.text(0.5, 6.6,
            "CONCEPTION : 8 SBC RK3588 (64 cœurs ARM) + switch local. Alimentation 100 % DC\n"
            "depuis le micro-réseau solaire (pas de conversion AC/DC = pas de pertes). Linux\n"
            "minimaliste compilé pour les algorithmes RATISS. Zéro dépendance cloud.",
            fontsize=8.5, style="italic",
            bbox=dict(boxstyle="round", facecolor="#fffbe6", edgecolor=RATIS_GOLD))
    save(fig, "01_plan_architecture.png")


# 2. PLAN THERMIQUE (rack + refroidissement)
def fig_plan_thermique():
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis("off")
    ax.set_title("PLAN DE CONCEPTION THERMIQUE — Rack + refroidissement liquide custom\n"
                 "Dissipation vers radiateur automobile recyclé (climat 35 °C)",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    # Rack
    ax.add_patch(Rectangle((1.0, 1.0), 4.5, 5.0, facecolor="#22303f",
                           edgecolor=RATIS_DARK, linewidth=2.5, zorder=1))
    for i in range(4):
        ax.add_patch(Rectangle((1.3, 1.4+i*1.2), 3.9, 0.9, facecolor="#0a1526",
                               edgecolor="#4a6a8a", zorder=2))
        ax.text(3.2, 1.85+i*1.2, f"Étage {i+1} : 2× RK3588", ha="center",
                va="center", color="#9ad", fontsize=8, zorder=3)
    ax.text(3.2, 6.3, "Rack serveur (soudé localement)", ha="center", fontsize=9,
            style="italic", color=RATIS_DARK)

    # Boucle de refroidissement
    _box(ax, 7.0, 4.5, 2.0, 1.0, "Bloc eau\n( plaques\nfroides CPU)", "#bfe6bf", 8)
    _box(ax, 7.0, 1.2, 2.0, 1.0, "Pompe\n12 V\n(faible conso)", "#e0b3ff", 8)
    _box(ax, 9.8, 2.8, 1.8, 1.4, "Radiateur\nautomobile\nrecyclé", "#ffb3b3", 8)
    ax.annotate("", xy=(7.0, 5.0), xytext=(5.5, 5.0),
                arrowprops=dict(arrowstyle="->", color=RATIS_BLUE, lw=2))
    ax.annotate("", xy=(9.8, 3.5), xytext=(9.0, 5.0),
                arrowprops=dict(arrowstyle="->", color=RATIS_RED, lw=2))
    ax.annotate("", xy=(9.0, 1.7), xytext=(9.8, 3.2),
                arrowprops=dict(arrowstyle="->", color=RATIS_BLUE, lw=2))
    ax.annotate("", xy=(7.0, 1.7), xytext=(5.5, 1.5),
                arrowprops=dict(arrowstyle="->", color=RATIS_BLUE, lw=2))
    ax.text(8.5, 5.8, "eau + glycol (chaude)", fontsize=7, color=RATIS_RED)
    ax.text(8.5, 0.8, "eau (froide)", fontsize=7, color=RATIS_BLUE)

    ax.text(0.5, 6.6,
            "RÈGLES : boucle d'eau fermée, pompe 12 V (alimentée par le même bus DC solaire),\n"
            "radiateur automobile recyclé à l'extérieur. Le refroidissement liquide permet la\n"
            "pleine charge en climat tropical sans dépasser 85 °C de jonction.",
            fontsize=8.5, style="italic",
            bbox=dict(boxstyle="round", facecolor="#fffbe6", edgecolor=RATIS_GOLD))
    save(fig, "02_plan_thermique.png")


# 3. APPAREIL MONTÉ (le rack)
def fig_appareil_monte():
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.set_title("RATISS-HPC — Le cluster une fois monté",
                 fontsize=13, fontweight="bold", color=RATIS_DARK)

    ax.add_patch(FancyBboxPatch((2.5, 0.8), 5, 8.4, boxstyle="round,pad=0.05",
                                facecolor="#1a2530", edgecolor="black", linewidth=3))
    ax.text(5.0, 8.9, "RACK HPC SOUVERAIN", ha="center", fontsize=10,
            fontweight="bold", color=RATIS_GOLD)
    # 8 tiroirs SBC avec LED
    for i in range(8):
        y = 1.2 + i*0.9
        ax.add_patch(Rectangle((2.9, y), 4.2, 0.7, facecolor="#0d1b2a",
                               edgecolor="#3a5a80", zorder=2))
        ax.text(4.0, y+0.35, f"RK3588-{i}", va="center", color="#9ad",
                fontsize=7, family="monospace", zorder=3)
        # LEDs activité
        for j, c in enumerate(["lime", RATIS_GOLD]):
            ax.add_patch(Circle((6.5+j*0.3, y+0.35), 0.07, facecolor=c, zorder=3))
        ax.text(5.5, y+0.35, "OK", va="center", color="lime", fontsize=6,
                family="monospace", zorder=3)
    # bandeau d'état
    ax.add_patch(Rectangle((2.9, 8.0), 4.2, 0.5, facecolor="#001a00",
                           edgecolor="lime", zorder=3))
    ax.text(5.0, 8.25, "64 cœurs · 72 W · 58 °C · 100% SOLAIRE", ha="center",
            va="center", color="lime", fontsize=7.5, family="monospace", zorder=4)
    ax.text(5.0, 0.35, "Refroidissement liquide · Alimentation DC 48 V solaire",
            ha="center", fontsize=9, style="italic", color=RATIS_DARK)
    save(fig, "03_appareil_monte.png")


# 4. PERFORMANCES & ÉNERGIE
def fig_performances():
    from ratiss_hpc.cluster import Cluster, benchmark_relative, solar_autonomy_hours
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle("RATISS-HPC — Performances et autonomie énergétique (simulateur)",
                 fontsize=13, fontweight="bold", color=RATIS_DARK)

    # Speedup vs nb noeuds (Amdahl)
    ns = np.arange(1, 17)
    sp = [benchmark_relative(Cluster.standard(int(n)))["speedup_vs_single"] for n in ns]
    axs[0].plot(ns, sp, "o-", color=RATIS_GREEN, lw=2, label="speedup réel")
    axs[0].plot(ns, ns, "--", color="#888", label="linéaire idéal")
    axs[0].set_xlabel("nombre de noeuds"); axs[0].set_ylabel("speedup")
    axs[0].set_title("Montée en charge (Amdahl, overhead 10 %)"); axs[0].legend(fontsize=8)

    # Puissance vs charge
    c = Cluster.standard(8)
    loads = np.linspace(0, 1, 50)
    pw = [c.power_w(l) for l in loads]
    axs[1].plot(loads*100, pw, color=RATIS_RED, lw=2)
    axs[1].set_xlabel("charge (%)"); axs[1].set_ylabel("puissance (W)")
    axs[1].set_title("Consommation du cluster (8 noeuds)")
    axs[1].axhline(72, color=RATIS_GOLD, linestyle=":", label="~72 W pleine charge")
    axs[1].legend(fontsize=8)

    # Autonomie sur batterie GRID (14.3 kWh)
    batts = [7.2, 14.3, 28.7]
    x = np.arange(len(batts))
    aut = [solar_autonomy_hours(c, b) for b in batts]
    axs[2].bar(x, aut, color=[RATIS_GOLD, RATIS_GREEN, RATIS_BLUE])
    axs[2].set_xticks(x, [f"{b} kWh" for b in batts])
    axs[2].set_ylabel("autonomie (heures)")
    axs[2].set_title("Autonomie sur batterie RATISS-GRID (charge 70 %)")
    for i, v in enumerate(aut):
        axs[2].text(i, v+3, f"{v:.0f} h", ha="center", fontweight="bold")

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    save(fig, "04_performances.png")


# 5. COUPLAGE ÉNERGÉTIQUE AVEC RATISS-GRID (24 h)
def fig_energie_journaliere():
    from ratiss_hpc.cluster import Cluster
    fig, ax = plt.subplots(figsize=(12, 6))
    fig.suptitle("RATISS-HPC × RATISS-GRID — une journée d'autonomie solaire (simulation)",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    t = np.linspace(0, 24, 289)  # pas de 5 min
    # irradiance typique tropique (bell curve 6h-18h, pic 1000 W/m² à midi)
    irradiance = 1000 * np.maximum(0, np.sin(np.pi * (t - 6) / 12)) ** 1.5
    # PV 2 kWc → production DC (rendement 85 %)
    pv_w = 2000 * 0.85 * irradiance / 1000
    # cluster à charge variable : pleine charge le jour (calcul), idle la nuit
    c = Cluster.standard(8)
    load = np.where((t >= 7) & (t <= 22), 0.9, 0.15)
    cluster_w = np.array([c.power_w(l) for l in load])
    # batterie 14.3 kWh, SOC dynamique
    dt_h = t[1] - t[0]
    net = pv_w - cluster_w
    soc = np.empty_like(t); soc[0] = 60.0
    cap_wh = 14300.0
    for i in range(1, len(t)):
        soc[i] = np.clip(soc[i-1] + net[i] * dt_h / cap_wh * 100, 0, 100)

    ax2 = ax.twinx()
    ax.fill_between(t, 0, pv_w, color=RATIS_GOLD, alpha=0.4, label="production PV (2 kWc)")
    ax.plot(t, cluster_w, color=RATIS_RED, lw=2, label="consommation cluster")
    ax2.plot(t, soc, color=RATIS_GREEN, lw=2.5, label="batterie LiFePO4 (%)")
    ax.axvspan(0, 6, color="#0b1f3a", alpha=0.08)
    ax.axvspan(18, 24, color="#0b1f3a", alpha=0.08)
    ax.set_xlabel("heure"); ax.set_ylabel("puissance (W)")
    ax2.set_ylabel("état de charge (%)", color=RATIS_GREEN)
    ax.set_xlim(0, 24); ax.set_ylim(0, 1900); ax2.set_ylim(0, 105)
    lines = ax.get_legend_handles_labels()
    l2 = ax2.get_legend_handles_labels()
    ax.legend(lines[0] + l2[0], lines[1] + l2[1], loc="upper left", fontsize=9)
    ax.set_title("Le soleil couvre la pleine charge le jour ; la batterie tient la nuit",
                 fontsize=10)
    save(fig, "06_energie_journaliere.png")


# 6. CARTE THERMIQUE (passif vs actif)
def fig_carte_thermique():
    from ratiss_hpc.cluster import (Cluster, CPU_TJ_MAX_C, HEATSINK_RTH_ACTIVE,
                                    HEATSINK_RTH_PASSIVE)
    fig, ax = plt.subplots(figsize=(11, 6))
    fig.suptitle("RATISS-HPC — température CPU : passif vs refroidissement liquide",
                 fontsize=12.5, fontweight="bold", color=RATIS_DARK)

    c = Cluster.standard(8)
    loads = np.linspace(0, 1, 100)
    for amb, ls in [(25, "-"), (35, "--"), (42, ":")]:
        t_act = [c.cpu_temp_c(l, amb, HEATSINK_RTH_ACTIVE) for l in loads]
        t_pas = [c.cpu_temp_c(l, amb, HEATSINK_RTH_PASSIVE) for l in loads]
        ax.plot(loads * 100, t_pas, ls, color=RATIS_RED, alpha=0.75,
                label=f"passif, {amb} °C ambiant")
        ax.plot(loads * 100, t_act, ls, color=RATIS_BLUE,
                label=f"liquide, {amb} °C ambiant")
    ax.axhline(CPU_TJ_MAX_C, color="black", lw=2, label="T jonction max (85 °C)")
    ax.axhline(70, color=RATIS_GREEN, lw=1.5, linestyle="-.",
               label="cible exploitation (70 °C)")
    ax.fill_between([60, 100], 0, 120, color=RATIS_RED, alpha=0.05)
    ax.set_xlabel("charge (%)"); ax.set_ylabel("température CPU (°C)")
    ax.set_ylim(20, 120)
    ax.legend(fontsize=8, ncol=2, loc="upper left")
    ax.set_title("Le passif dépasse la limite dès ~60 % de charge en climat tropical ; "
                 "le liquide garde 27 °C de marge", fontsize=10)
    save(fig, "07_carte_thermique.png")


# 7. LOGO
def fig_logo():
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    fig.patch.set_facecolor(RATIS_DARK); ax.set_facecolor(RATIS_DARK)
    for angle, col in [(0, RATIS_GREEN), (60, RATIS_GOLD), (120, RATIS_BLUE)]:
        th = np.linspace(0, 2*np.pi, 200)
        x = 3.2*np.cos(th); y = 1.2*np.sin(th); a = np.radians(angle)
        xr = x*np.cos(a) - y*np.sin(a); yr = x*np.sin(a) + y*np.cos(a)
        ax.plot(5+xr, 5.6+yr, color=col, lw=3, alpha=0.9)
    ax.add_patch(Circle((5, 5.6), 0.7, facecolor=RATIS_GOLD, edgecolor="white",
                        linewidth=2, zorder=5))
    ax.text(5, 3.4, "RATIS LABS", ha="center", va="center", fontsize=34,
            fontweight="bold", color="white", family="sans-serif")
    ax.text(5, 2.7, "Souveraineté technologique · Cameroun", ha="center",
            va="center", fontsize=12, color=RATIS_GOLD, style="italic")
    save(fig, "05_logo_ratis_labs.png", facecolor=RATIS_DARK)


if __name__ == "__main__":
    fig_plan_architecture(); fig_plan_thermique(); fig_appareil_monte()
    fig_performances(); fig_energie_journaliere(); fig_carte_thermique()
    fig_logo()
    print("Figures RATISS-HPC dans docs/images/")
