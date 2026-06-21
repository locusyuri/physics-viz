"""Normal modes of a vibrating string fixed at both ends.

Three-panel physics-textbook illustration (serif, vertical stack):
  * Panel (a): n = 1 — Fundamental mode
  * Panel (b): n = 2 — Second harmonic
  * Panel (c): n = 3 — Third harmonic

Each panel shows the standing-wave mode shape u_n(x) = A_n sin(nπx/L)
with nodes (red dots) and antinodes (red dashed lines) marked.

Run with:    uv run python src/oscillation/string_normal_modes.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

from _viz.output import OutputSpec

# --------------------------------------------------------------------------- #
# Output configuration
# --------------------------------------------------------------------------- #
SPEC = OutputSpec(
    figsize=(10.0, 13.0),
    fmt="png",
    dpi=300,
    pad_inches=0.05,
    rc_overrides={
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman", "serif"],
        "mathtext.fontset": "dejavuserif",
    },
)
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# Palette
BLU = "#1f4e9b"
GRN = "#2e8b57"
ORG = "#d4740e"
RED = "#cc3333"
GREY = "#888888"


# --------------------------------------------------------------------------- #
# Single panel drawing
# --------------------------------------------------------------------------- #
def draw_mode_panel(
    ax,
    n: int,
    color: str,
    nodes: list[float],
    antinodes: list[float],
    wavelength_label: str,
    freq_label: str,
    title: str,
):
    """Draw one normal-mode panel with nodes, antinodes, and annotations.

    Parameters
    ----------
    ax : Axes
    n : int
        Mode number (1, 2, 3, …).
    color : str
        Line colour for the displacement curve.
    nodes : list of float
        Normalised x positions where u = 0 (nodes).
    antinodes : list of float
        Normalised x positions where |u| is maximum (antinodes).
    wavelength_label : str
        LaTeX label for the wavelength.
    freq_label : str
        LaTeX label for the frequency.
    title : str
        Sub-panel title.
    """
    x = np.linspace(0, 1, 500)
    y = np.sin(n * np.pi * x)

    # --- Displacement curve ---
    ax.plot(x, y, color=color, lw=2.4, zorder=4)

    # --- Nodes (red dots on the x-axis) ---
    for xn in nodes:
        ax.scatter([xn], [0], s=40, color=RED, zorder=6, clip_on=False)

    # --- Antinodes (red dashed vertical lines, full height) ---
    for xa in antinodes:
        ax.axvline(xa, color=RED, ls="--", lw=1.0, alpha=0.7, zorder=2)

    # Label one antinode with "Antinode"
    if antinodes:
        xa0 = antinodes[0]
        ya0 = np.sin(n * np.pi * xa0)
        ax.text(xa0 + 0.02, ya0 + 0.12, "Antinode", fontsize=8, color=RED,
                va="bottom", ha="left",
                bbox=dict(boxstyle="round,pad=0.15", fc="white",
                          ec="#ffcccc", lw=0.4, alpha=0.85))

    # --- Amplitude double-headed arrow at the first antinode ---
    if antinodes:
        xa0 = antinodes[0]
        ya0 = np.sin(n * np.pi * xa0)
        ax.annotate("", xy=(xa0, 0), xytext=(xa0, ya0),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.2))
        ax.text(xa0 + 0.04, ya0 / 2, f"$A_{n}$", fontsize=9, color=color,
                va="center")

    # --- Wavelength and frequency labels ---
    ax.text(0.98, 0.92, wavelength_label, transform=ax.transAxes,
            ha="right", va="top", fontsize=10, color=color,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc",
                      lw=0.5))
    ax.text(0.98, 0.78, freq_label, transform=ax.transAxes,
            ha="right", va="top", fontsize=10, color=color,
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc",
                      lw=0.5))

    # --- Axes ---
    ax.set_xlim(0, 1)
    ax.set_xlabel(r"Position $x/L$", fontsize=10)
    ax.set_xticks(np.arange(0, 1.01, 0.25))

    ax.set_ylim(-1.25, 1.25)
    ax.set_ylabel(rf"Displacement $u(x)/A_{n}$", fontsize=10)
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.tick_params(labelsize=8)

    # --- Grid ---
    ax.grid(True, which="both", color="#dddddd", lw=0.6, ls="--", zorder=0)
    ax.axhline(0, color=GREY, lw=0.7, zorder=1)

    # --- Title ---
    ax.set_title(title, fontsize=11, pad=6)


# --------------------------------------------------------------------------- #
# Build the figure
# --------------------------------------------------------------------------- #
def build_figure():
    fig = SPEC.figure()

    ax_a = fig.add_subplot(311)
    ax_b = fig.add_subplot(312)
    ax_c = fig.add_subplot(313)

    fig.subplots_adjust(left=0.10, right=0.96, top=0.96, bottom=0.07,
                        hspace=0.30)

    # Panel (a): n = 1
    draw_mode_panel(
        ax_a, n=1, color=BLU,
        nodes=[0, 1],
        antinodes=[0.5],
        wavelength_label=r"$\lambda_1 = 2L$",
        freq_label=r"$f_1 = v/(2L)$",
        title=r"(a) $n = 1$ — Fundamental Mode ($f_1$)",
    )

    # Panel (b): n = 2
    draw_mode_panel(
        ax_b, n=2, color=GRN,
        nodes=[0, 0.5, 1],
        antinodes=[0.25, 0.75],
        wavelength_label=r"$\lambda_2 = L$",
        freq_label=r"$f_2 = 2f_1$",
        title=r"(b) $n = 2$ — Second Harmonic ($f_2 = 2f_1$)",
    )

    # Panel (c): n = 3
    draw_mode_panel(
        ax_c, n=3, color=ORG,
        nodes=[0, 1 / 3, 2 / 3, 1],
        antinodes=[1 / 6, 0.5, 5 / 6],
        wavelength_label=r"$\lambda_3 = 2L/3$",
        freq_label=r"$f_3 = 3f_1$",
        title=r"(c) $n = 3$ — Third Harmonic ($f_3 = 3f_1$)",
    )

    # Shared legend below the panels
    handles = [
        Line2D([0], [0], color=BLU, lw=2.4,
               label=r"Displacement $u_n(x)$"),
        Line2D([0], [0], color=RED, marker="o", lw=0, markersize=6,
               label=r"Node ($u = 0$)"),
        Line2D([0], [0], color=RED, ls="--", lw=1.0,
               label="Antinode"),
    ]
    fig.legend(handles=handles, loc="lower center", fontsize=9,
               frameon=True, edgecolor="#cccccc", facecolor="white",
               framealpha=0.9, ncol=3, bbox_to_anchor=(0.5, 0.01))

    return fig


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "string_normal_modes")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()