"""Conformal mapping illustration: z-plane → w-plane.

Two-panel mathematical textbook figure showing a conformal mapping
w = f(z) that transforms a circular domain D in the z-plane into a
deformed domain f(D) in the w-plane.

Run with: uv run python src/math_paper/conformal_mapping.py
"""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _viz.output import Presets

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
SPEC = Presets.PNG_MATH_PANEL
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# Conformal mapping: f(z) = z + 0.4*z^2
# This is analytic and conformal inside the unit disk (critical point at z=-1.25)
def f(z):
    return z + 0.4 * z**2

# Generate boundary curves
theta = np.linspace(0, 2 * np.pi, 500)
z_circle = np.exp(1j * theta)
w_curve = f(z_circle)

# Points in D
z_points = np.array([0.3 + 0.2j, -0.4 + 0.3j, 0.1 - 0.5j])
w_points = f(z_points)


# --------------------------------------------------------------------------- #
# Build the figure
# --------------------------------------------------------------------------- #
def build_figure():
    fig = SPEC.figure()

    # Left panel: z-plane
    ax_z = fig.add_subplot(121)
    ax_z.set_title("z-plane", fontsize=14, pad=10, fontweight="bold")
    ax_z.set_aspect("equal")
    ax_z.grid(True, color="#dddddd", lw=0.6, zorder=0)
    ax_z.axhline(0, color="k", lw=1.0, zorder=1)
    ax_z.axvline(0, color="k", lw=1.0, zorder=1)
    ax_z.set_xlim(-2.5, 2.5)
    ax_z.set_ylim(-2.5, 2.5)
    ax_z.set_xlabel("Re z", fontsize=11, loc="right")
    ax_z.set_ylabel("Im z", fontsize=11, rotation=0, loc="top")
    ax_z.text(0, -0.15, "O", fontsize=10, ha="right", va="top")

    # Domain D (unit disk)
    ax_z.fill(z_circle.real, z_circle.imag, "#4a90d9", alpha=0.3, zorder=2)
    ax_z.plot(z_circle.real, z_circle.imag, "#4a90d9", lw=1.5, zorder=3)
    ax_z.text(0, 0, "D", fontsize=13, ha="center", va="center",
              fontweight="bold", zorder=4)

    # Points in D
    for i, z in enumerate(z_points, 1):
        ax_z.scatter([z.real], [z.imag], s=30, color="k", zorder=5)
        ax_z.text(z.real + 0.1, z.imag + 0.1, f"z{i}", fontsize=10, zorder=6)

    # Right panel: w-plane
    ax_w = fig.add_subplot(122)
    ax_w.set_title("w-plane", fontsize=14, pad=10, fontweight="bold")
    ax_w.set_aspect("equal")
    ax_w.grid(True, color="#dddddd", lw=0.6, zorder=0)
    ax_w.axhline(0, color="k", lw=1.0, zorder=1)
    ax_w.axvline(0, color="k", lw=1.0, zorder=1)
    ax_w.set_xlim(-2.5, 2.5)
    ax_w.set_ylim(-2.5, 2.5)
    ax_w.set_xlabel("Re w", fontsize=11, loc="right")
    ax_w.set_ylabel("Im w", fontsize=11, rotation=0, loc="top")
    ax_w.text(0, -0.15, "O", fontsize=10, ha="right", va="top")

    # Mapped domain f(D)
    ax_w.fill(w_curve.real, w_curve.imag, "#4a90d9", alpha=0.3, zorder=2)
    ax_w.plot(w_curve.real, w_curve.imag, "#4a90d9", lw=1.5, zorder=3)
    ax_w.text(0.3, 0, "f(D)", fontsize=13, ha="center", va="center",
              fontweight="bold", zorder=4)

    # Mapped points
    for i, w in enumerate(w_points, 1):
        ax_w.scatter([w.real], [w.imag], s=30, color="k", zorder=5)
        ax_w.text(w.real + 0.1, w.imag + 0.1, f"w{i}", fontsize=10, zorder=6)

    # Curved arrow between panels (figure-relative coordinates)
    ax_z.annotate(
        "",
        xy=(0.66, 0.50), xycoords="figure fraction",
        xytext=(0.36, 0.50), textcoords="figure fraction",
        arrowprops=dict(
            arrowstyle="-|>",
            connectionstyle="arc3,rad=-0.3",
            color="#c0392b",
            lw=2.5,
            mutation_scale=30,
        ),
    )

    # Label for the mapping
    fig.text(0.50, 0.72, r"$w = f(z)$", fontsize=13, ha="center", va="center",
             fontweight="bold")

    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "conformal_mapping")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
