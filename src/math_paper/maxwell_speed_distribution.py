"""Maxwell speed distribution at three temperatures.

Single-panel SVG showing F(v) for T1 < T2 = 2T1 < T3 = 4T1.
The velocity axis is in units of v_p1 (most probable speed at T1),
so the three curves have different peak positions and heights.

The normalised distribution is
  f(x; alpha) = (x/alpha)^2 exp(1 - (x/alpha)^2)
where x = v/v_p1 and alpha = v_p(T)/v_p1 = sqrt(T/T1).

Run with: uv run python src/math_paper/maxwell_speed_distribution.py
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
ORG = "#e67e22"
GRN = "#2ca02c"
GRY = "#999999"
AXC = "#333333"


def maxwell_f(x, alpha):
    """Normalised Maxwell speed distribution.

    f(x; alpha) = (x/alpha)^2 * exp(1 - (x/alpha)^2)
    Peak value = 1 at x = alpha.
    """
    u = x / alpha
    return u ** 2 * np.exp(1.0 - u ** 2)


def build_figure():
    fig = SPEC.figure()
    ax = fig.add_subplot(111)

    x = np.linspace(0.001, 3.0, 500)

    # alpha = sqrt(T/T1);  T2 = 2T1, T3 = 4T1
    alpha1, alpha2, alpha3 = 1.0, np.sqrt(2.0), 2.0

    f1 = maxwell_f(x, alpha1)
    f2 = maxwell_f(x, alpha2)
    f3 = maxwell_f(x, alpha3)

    # -- three curves ---------------------------------------------------- #
    ax.plot(x, f1, color=BLU, lw=2.2, label=r"$T_1$", zorder=3)
    ax.plot(x, f2, color=ORG, lw=2.0, ls="--",
            label=r"$T_2 = 2T_1$", zorder=3)
    ax.plot(x, f3, color=GRN, lw=2.0, ls="-.",
            label=r"$T_3 = 4T_1$", zorder=3)

    # -- characteristic points on T1 curve --------------------------------
    vp = 1.0                       # v_p / v_p1
    vbar = 2.0 / np.sqrt(np.pi)   # mean speed / v_p1  ~ 1.128
    vrms = np.sqrt(1.5)           # v_rms / v_p = sqrt(3/2) ~ 1.225

    f_vp = maxwell_f(np.array([vp]), alpha1)[0]
    f_vbar = maxwell_f(np.array([vbar]), alpha1)[0]
    f_vrms = maxwell_f(np.array([vrms]), alpha1)[0]

    # gray dashed vertical lines from x-axis
    for xv in (vp, vbar, vrms):
        ax.axvline(xv, color=GRY, lw=0.7, ls="--", zorder=1)

    # solid circle at v_p
    ax.plot(vp, f_vp, "o", color=BLU, ms=7, zorder=5)
    ax.text(vp + 0.03, f_vp + 0.04, r"$v_p$",
            fontsize=10, color=BLU, ha="left")

    # open circle at v_bar
    ax.plot(vbar, f_vbar, "o", color="white", markeredgecolor=BLU,
            markeredgewidth=1.5, ms=7, zorder=5)
    ax.text(vbar + 0.03, f_vbar + 0.04, r"$\bar{v}$",
            fontsize=10, color=BLU, ha="left")

    # solid square at v_rms
    ax.plot(vrms, f_vrms, "s", color=BLU, ms=6, zorder=5)
    ax.text(vrms + 0.03, f_vrms + 0.04, r"$v_{\mathrm{rms}}$",
            fontsize=10, color=BLU, ha="left")

    # -- legend ---------------------------------------------------------- #
    ax.legend(fontsize=10, frameon=False, loc="upper right",
              title=r"$T_1 < T_2 < T_3$", title_fontsize=10)

    # -- axes ------------------------------------------------------------ #
    ax.set_xlim(0, 3.0)
    ax.set_ylim(0, 1.12)
    ax.set_xlabel(r"$v \,/\, v_p$", fontsize=12)
    ax.set_ylabel(r"$F(v)$  (normalised)", fontsize=12)

    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for spine in ax.spines.values():
        spine.set_color(AXC)
        spine.set_linewidth(0.8)
    ax.tick_params(colors=AXC, labelsize=9)

    fig.subplots_adjust(left=0.12, right=0.95, bottom=0.12, top=0.95)
    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "maxwell-speed-distribution")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
