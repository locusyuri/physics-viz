"""Electric field and potential of a point charge.

Three-panel physics-textbook illustration (serif, line-art style):
  * Figure 1 (top, full width):   point charge +q with radial field lines.
  * Figure 2 (bottom-left):       E = kq/r^2  vs. distance.
  * Figure 3 (bottom-right):      V = kq/r    vs. distance, with V -> 0 asymptote.

Run with:    uv run python src/point_charge_field.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, FancyArrowPatch

from _viz.output import Presets

# --------------------------------------------------------------------------- #
# Physical constants
# --------------------------------------------------------------------------- #
K = 9.0e9          # Coulomb constant, N·m^2/C^2
Q = 1.0e-9         # charge, C  ->  E(r)=9/r^2 N/C,  V(r)=9/r V

RED = "#c0392b"
BLU = "#1f4e9b"
GRN = "#2e8b57"
GREY = "#888888"

SPEC = Presets.SVG_TEXTBOOK
OUT_DIR = Path(__file__).resolve().parent.parent / "output"


# --------------------------------------------------------------------------- #
# Figure 1 — point charge and field lines
# --------------------------------------------------------------------------- #
def draw_model(ax):
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)

    ax.set_title(
        "Figure 1: Point Charge +q and its Electric Field Lines",
        fontsize=12, pad=8,
    )

    cx = cy = 0.0

    # 12 radial field lines with directional arrows.
    n_lines = 12
    r_max = 1.25
    for i in range(n_lines):
        a = 2 * np.pi * i / n_lines
        dx, dy = np.cos(a), np.sin(a)
        # line itself
        ax.plot(
            [cx, cx + r_max * dx], [cy, cy + r_max * dy],
            color=RED, lw=1.2, zorder=2,
        )
        # a small arrow at ~60% along the line
        t = 0.6
        ax.add_patch(
            FancyArrowPatch(
                (cx + (t - 0.07) * r_max * dx, cy + (t - 0.07) * r_max * dy),
                (cx + t * r_max * dx, cy + t * r_max * dy),
                arrowstyle="-|>", mutation_scale=9,
                color=RED, lw=1.2, zorder=3,
            )
        )

    # The charge itself.
    ax.add_patch(Circle((cx, cy), 0.07, color=RED, zorder=5))
    ax.text(cx, cy - 0.22, "+q", ha="center", va="top",
            fontsize=13, color=RED, fontweight="bold", zorder=5)

    # Test points P1 (1/3) and P2 (2/3) along +x.
    pts = [("P1", 1 / 3), ("P2", 2 / 3)]
    for name, frac in pts:
        px = cx + frac * r_max * np.cos(0.0)
        py = cy + frac * r_max * np.sin(0.0)
        ax.scatter([px], [py], s=22, facecolor="white",
                   edgecolor="k", zorder=6)
        ax.text(px, py - 0.16, name, ha="center", va="top",
                fontsize=9, zorder=6)
        # thicker blue E arrow, radial outward
        ax.add_patch(
            FancyArrowPatch(
                (px + 0.04, py), (px + 0.34, py),
                arrowstyle="-|>", mutation_scale=14,
                color=BLU, lw=2.4, zorder=7,
            )
        )
        ax.text(px + 0.20, py + 0.10, "E", ha="center", va="bottom",
                fontsize=12, color=BLU, fontweight="bold", zorder=7)

    # "r" distance axis indicator at the bottom.
    ax.annotate(
        "", xy=(0.95, -1.25), xytext=(0.05, -1.25),
        arrowprops=dict(arrowstyle="-|>", color="k", lw=1.0),
    )
    ax.text(0.5, -1.38, "r", ha="center", va="top",
            fontsize=12, style="italic")

    # Legend (bottom-right).
    legend_handles = [
        Line2D([0], [0], marker="o", color="none", markerfacecolor=RED,
               markersize=9, label="+q (Positive Point Charge)"),
        Line2D([0], [0], color=RED, lw=1.4, label="Electric Field Lines"),
        Line2D([0], [0], color=BLU, lw=2.4, label="Electric Field E"),
    ]
    ax.legend(handles=legend_handles, loc="lower right",
              fontsize=8, frameon=True, edgecolor="#cccccc",
              facecolor="white", framealpha=0.9)


# --------------------------------------------------------------------------- #
# Figure 2 — E vs. r
# --------------------------------------------------------------------------- #
def draw_e_field(ax):
    ax.set_title("Figure 2: Electric Field vs. Distance",
                 fontsize=12, pad=8)

    r = np.linspace(0.1, 3.0, 400)
    E = K * Q / r ** 2

    ax.plot(r, E, color=BLU, lw=1.8)
    ax.set_xlim(0.1, 3.0)
    ax.set_ylim(0, 20)
    ax.set_xlabel("Distance r (m)", fontsize=10)
    ax.set_ylabel("E (N/C)", fontsize=10)
    ax.set_xticks(np.arange(0.1, 3.01, 0.5))
    ax.set_yticks(np.arange(0, 21, 5))
    ax.grid(True, which="both", color="#dddddd", lw=0.6)
    ax.tick_params(labelsize=8)

    # Marked points r = 1.0 (E=9.0) and r = 2.0 (E=2.25).
    for rr, val in ((1.0, 9.0), (2.0, 2.25)):
        ee = K * Q / rr ** 2
        ax.scatter([rr], [ee], s=24, facecolor="white",
                   edgecolor=BLU, zorder=5)
        ax.annotate(
            f"E = {val:g}",
            xy=(rr, ee), xytext=(8, 10), textcoords="offset points",
            fontsize=9, color=BLU,
        )

    # Formula box (upper-right).
    ax.text(
        0.97, 0.95,
        r"$\mathbf{E = kq\,/\,r^2}$" "\n"
        r"$(k = 9.0\times10^{9},\ q = 1.0\times10^{-9})$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10, color=BLU, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", fc="white",
                  ec="#cccccc", lw=0.6),
    )

    # Legend (bottom-right).
    ax.legend(
        handles=[Line2D([0], [0], color=BLU, lw=1.8,
                        label=r"Blue solid line: $E = kq\,/\,r^2$")],
        loc="lower right", fontsize=8, frameon=True,
        edgecolor="#cccccc", facecolor="white",
    )


# --------------------------------------------------------------------------- #
# Figure 3 — V vs. r
# --------------------------------------------------------------------------- #
def draw_v_field(ax):
    ax.set_title("Figure 3: Electric Potential vs. Distance",
                 fontsize=12, pad=8)

    r = np.linspace(0.1, 3.0, 400)
    V = K * Q / r

    ax.plot(r, V, color=GRN, lw=1.8)
    ax.set_xlim(0.1, 3.0)
    ax.set_ylim(0, 10)
    ax.set_xlabel("Distance r (m)", fontsize=10)
    ax.set_ylabel("V (V)", fontsize=10)
    ax.set_xticks(np.arange(0.1, 3.01, 0.5))
    ax.set_yticks(np.arange(0, 11, 2))
    ax.grid(True, which="both", color="#dddddd", lw=0.6)
    ax.tick_params(labelsize=8)

    # Horizontal dashed asymptote V -> 0.
    ax.axhline(0.0, xmin=0.0, xmax=1.0, color=GREY, ls="--", lw=1.0)
    ax.text(2.95, 0.25, r"$V \rightarrow 0$", ha="right", va="bottom",
            fontsize=9, color=GREY, style="italic")

    # Marked points r = 1.0 (V=9.0) and r = 2.0 (V=4.5).
    for rr, val in ((1.0, 9.0), (2.0, 4.5)):
        vv = K * Q / rr
        ax.scatter([rr], [vv], s=24, facecolor="white",
                   edgecolor=GRN, zorder=5)
        ax.annotate(
            f"V = {val:g}",
            xy=(rr, vv), xytext=(8, 10), textcoords="offset points",
            fontsize=9, color=GRN,
        )

    # Formula box (upper-right).
    ax.text(
        0.97, 0.95,
        r"$\mathbf{V = kq\,/\,r}$" "\n"
        r"$(k = 9.0\times10^{9},\ q = 1.0\times10^{-9})$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10, color=GRN, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", fc="white",
                  ec="#cccccc", lw=0.6),
    )

    # Legend (bottom-right).
    ax.legend(
        handles=[Line2D([0], [0], color=GRN, lw=1.8,
                        label=r"Green solid line: $V = kq\,/\,r$")],
        loc="lower right", fontsize=8, frameon=True,
        edgecolor="#cccccc", facecolor="white",
    )


# --------------------------------------------------------------------------- #
# Build the whole figure
# --------------------------------------------------------------------------- #
def build_figure():
    fig = SPEC.figure()
    gs = GridSpec(
        3, 2, figure=fig,
        height_ratios=[2, 1, 1],   # top 50%, bottom rows 25% each
        hspace=0.45, wspace=0.18,
        left=0.08, right=0.97, top=0.92, bottom=0.06,
    )

    ax1 = fig.add_subplot(gs[0, :])      # top: full width
    ax2 = fig.add_subplot(gs[1, 0])      # bottom-left
    ax3 = fig.add_subplot(gs[1, 1])      # bottom-right

    draw_model(ax1)
    draw_e_field(ax2)
    draw_v_field(ax3)

    fig.suptitle(
        "Electric Field and Potential of a Point Charge",
        fontsize=15, fontweight="bold", y=0.975,
    )

    # Thin separator lines between panels.
    fig.add_artist(
        plt.Line2D([0.08, 0.97], [0.50, 0.50], transform=fig.transFigure,
                   color="k", lw=0.6)
    )
    fig.add_artist(
        plt.Line2D([0.505, 0.505], [0.06, 0.50], transform=fig.transFigure,
                   color="k", lw=0.6)
    )

    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "point_charge_field")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
