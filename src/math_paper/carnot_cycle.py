"""Carnot cycle on a p-V diagram for an ideal gas.

Four reversible steps (nR = 1, gamma = 5/3):
  a -> b  isothermal expansion at T_h = 4
  b -> c  adiabatic expansion
  c -> d  isothermal compression at T_c = 2
  d -> a  adiabatic compression

Run with: uv run python src/math_paper/carnot_cycle.py
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _viz.output import Presets

SPEC = replace(Presets.SVG_MATH, transparent=False)
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

BLU = "#2196F3"
RED = "#E53935"
GRY = "#999999"
AXC = "#333333"
FILL = "#2196F3"

GAMMA = 5.0 / 3.0
TH = 4.0
TC = 2.0


def build_figure():
    fig = SPEC.figure()
    ax = fig.add_subplot(111)

    # -- cycle vertices -------------------------------------------------- #
    Va, Vb = 1.0, 2.0
    Vc = Vb * (TH / TC) ** 1.5        # ~ 5.657
    Vd = Va * (TH / TC) ** 1.5        # ~ 1.414

    pa = TH / Va    # 4.0
    pb = TH / Vb    # 2.0
    pc = TC / Vc    # ~ 0.354
    pd = TC / Vd    # ~ 1.414

    # -- parametric curves for each leg ---------------------------------- #
    V_iso_h = np.linspace(Va, Vb, 100)
    V_adi_bc = np.linspace(Vb, Vc, 150)
    V_iso_c = np.linspace(Vc, Vd, 100)
    V_adi_da = np.linspace(Vd, Va, 150)

    p_iso_h = TH / V_iso_h
    K_bc = pb * Vb ** GAMMA
    p_adi_bc = K_bc / V_adi_bc ** GAMMA
    p_iso_c = TC / V_iso_c
    K_da = pd * Vd ** GAMMA
    p_adi_da = K_da / V_adi_da ** GAMMA

    # -- fill cycle interior (net work W) -------------------------------- #
    V_all = np.concatenate([V_iso_h, V_adi_bc, V_iso_c, V_adi_da])
    p_all = np.concatenate([p_iso_h, p_adi_bc, p_iso_c, p_adi_da])
    ax.fill(V_all, p_all, color=FILL, alpha=0.25, zorder=0)

    # -- grey dashed isotherm extensions --------------------------------- #
    V_ext = np.linspace(0.5, 5.0, 300)
    ax.plot(V_ext, TH / V_ext, color=GRY, lw=0.7, ls="--",
            alpha=0.5, zorder=1)
    ax.plot(V_ext, TC / V_ext, color=GRY, lw=0.7, ls="--",
            alpha=0.5, zorder=1)

    # -- four legs (blue solid) ------------------------------------------ #
    ax.plot(V_iso_h, p_iso_h, color=BLU, lw=2.0, zorder=3)
    ax.plot(V_adi_bc, p_adi_bc, color=BLU, lw=2.0, zorder=3)
    ax.plot(V_iso_c, p_iso_c, color=BLU, lw=2.0, zorder=3)
    ax.plot(V_adi_da, p_adi_da, color=BLU, lw=2.0, zorder=3)

    # -- direction arrows on each leg ------------------------------------ #
    akw = dict(arrowstyle="-|>", mutation_scale=15, zorder=4)

    # a->b  (isothermal expansion, mid)
    ax.annotate("", xy=(1.65, TH / 1.65), xytext=(1.35, TH / 1.35),
                arrowprops=dict(akw, color=BLU))

    # b->c  (adiabatic expansion, mid)
    Vm_bc = 0.5 * (Vb + Vc)
    ax.annotate("",
                xy=(Vm_bc + 0.3, K_bc / (Vm_bc + 0.3) ** GAMMA),
                xytext=(Vm_bc - 0.3, K_bc / (Vm_bc - 0.3) ** GAMMA),
                arrowprops=dict(akw, color=BLU))

    # c->d  (isothermal compression, mid)
    ax.annotate("", xy=(3.2, TC / 3.2), xytext=(3.6, TC / 3.6),
                arrowprops=dict(akw, color=BLU))

    # d->a  (adiabatic compression, mid)
    Vm_da = 0.5 * (Vd + Va)
    ax.annotate("",
                xy=(Vm_da - 0.15, K_da / (Vm_da - 0.15) ** GAMMA),
                xytext=(Vm_da + 0.15, K_da / (Vm_da + 0.15) ** GAMMA),
                arrowprops=dict(akw, color=BLU))

    # -- state points & labels ------------------------------------------- #
    for name, (vx, vy) in [("a", (Va, pa)), ("b", (Vb, pb)),
                            ("c", (Vc, pc)), ("d", (Vd, pd))]:
        ax.plot(vx, vy, "ko", ms=6, zorder=5)
        ax.text(vx, vy + 0.18, name, fontsize=13, fontweight="bold",
                color=AXC, ha="center")

    # -- heat labels ----------------------------------------------------- #
    ax.text(1.25, 3.35, r"$Q_h$ in", fontsize=10, color=RED,
            fontweight="bold")
    ax.text(3.4, 0.55, r"$Q_c$ out", fontsize=10, color=BLU,
            fontweight="bold")

    # -- isotherm labels ------------------------------------------------- #
    ax.text(4.6, TH / 4.6 + 0.15, r"$T_h$", fontsize=10, color=GRY)
    ax.text(4.6, TC / 4.6 + 0.15, r"$T_c$", fontsize=10, color=GRY)

    # -- W label inside cycle -------------------------------------------- #
    ax.text(2.6, 1.4, r"$W$", fontsize=14, color=BLU,
            ha="center", va="center", fontweight="bold", alpha=0.6)

    # -- axes ------------------------------------------------------------ #
    ax.set_xlim(0.5, 5.0)
    ax.set_ylim(0, 5.0)
    ax.set_xlabel(r"$V$", fontsize=13)
    ax.set_ylabel(r"$p$", fontsize=13)

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(AXC)
        spine.set_linewidth(0.8)
    ax.tick_params(colors=AXC, labelsize=9)

    fig.subplots_adjust(left=0.10, right=0.96, bottom=0.10, top=0.96)
    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "carnot-cycle")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
