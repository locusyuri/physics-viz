"""Right-hand rule for the cross product a x b = c in 3D.

Single-panel isometric projection (elevation 30 deg, azimuth 45 deg):
- black coordinate axes x, y, z from the origin to 2.5;
- vector a = (1.8, 0.4, 0) in blue, b = (0.4, 1.8, 0) in green,
  a x b = (0, 0, 1.8) in red;
- a light-grey curl arrow from a to b plus a stylised right hand
  (thumb pointing along +z) illustrating the rule;
- white background, SVG output.

Run with: uv run python src/math_paper/right_hand_rule.py
"""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch, FancyArrowPatch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _viz.output import Presets

SPEC = replace(Presets.SVG_TEXTBOOK, figsize=(8.6, 8.6), transparent=False)
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# -- colors ------------------------------------------------------------
AXIS = "#000000"
BLUE = "#2563EB"
GREEN = "#16A34A"
RED = "#DC2626"
GREY = "#9CA3AF"

# -- vectors (spec data) ------------------------------------------------
A = np.array([1.8, 0.4, 0.0])
B = np.array([0.4, 1.8, 0.0])
C = np.array([0.0, 0.0, 1.8])
AXIS_LEN = 2.5

# geometry self-check: c must be parallel to a x b (same direction, len 1.8)
_cross = np.cross(A, B)
assert np.allclose(_cross / np.linalg.norm(_cross) * np.linalg.norm(C), C)

# -- isometric projection: elevation 30 deg, azimuth 45 deg -------------
AZ = math.radians(45.0)
EL = math.radians(30.0)
SA, CA = math.sin(AZ), math.cos(AZ)
SE, CE = math.sin(EL), math.cos(EL)


def proj(p):
    """Orthographic projection of a 3-D point onto the screen."""
    x, y, z = p
    return (-x * SA + y * CA, -x * CA * SE - y * SA * SE + z * CE)


def arrow3(ax, p0, p1, color, lw, zorder=4, ms=16):
    ax.add_patch(
        FancyArrowPatch(proj(p0), proj(p1), arrowstyle="-|>", color=color,
                        lw=lw, mutation_scale=ms, zorder=zorder,
                        shrinkA=0, shrinkB=0)
    )


def panel(ax):
    ax.set_xlim(-1.85, 2.05)
    ax.set_ylim(-1.35, 2.62)
    ax.set_aspect("equal")
    ax.axis("off")

    # -- coordinate axes -------------------------------------------------
    for vec, label, ha, va, dx, dy in (
        ((AXIS_LEN, 0, 0), "$x$", "right", "top", 0.20, -0.10),
        ((0, AXIS_LEN, 0), "$y$", "left", "top", 0.20, -0.10),
        ((0, 0, AXIS_LEN), "$z$", "center", "bottom", 0.0, 0.20),
    ):
        arrow3(ax, (0, 0, 0), vec, AXIS, lw=1.3, zorder=3, ms=13)
        tip = np.array(vec, dtype=float)
        u = tip / np.linalg.norm(tip)
        sp = proj(tip + u * 0.10)
        ax.text(sp[0] + dx, sp[1] + dy, label, ha=ha, va=va,
                fontsize=14, color=AXIS, zorder=5)

    # -- the three vectors ------------------------------------------------
    arrow3(ax, (0, 0, 0), A, BLUE, lw=2.6)
    arrow3(ax, (0, 0, 0), B, GREEN, lw=2.6)
    arrow3(ax, (0, 0, 0), C, RED, lw=2.6)

    for vec, label, ha, dx, dy in (
        (A, r"$\mathbf{a}$", "right", -0.12, -0.05),
        (B, r"$\mathbf{b}$", "left", 0.12, -0.05),
        (C, r"$\mathbf{a}\times\mathbf{b}$", "left", 0.10, 0.02),
    ):
        sp = proj(vec)
        ax.text(sp[0] + dx, sp[1] + dy, label, ha=ha, va="center",
                fontsize=13, color="black", zorder=6)

    # -- curl arrow from a to b (in the xy-plane) --------------------------
    th0, th1 = math.atan2(A[1], A[0]), math.atan2(B[1], B[0])
    r = 0.85
    th = np.linspace(th0, th1, 60)
    arc3d = np.stack([r * np.cos(th), r * np.sin(th), 0.06 * np.ones_like(th)],
                     axis=1)
    arc2d = np.array([proj(p) for p in arc3d])
    ax.plot(arc2d[:-2, 0], arc2d[:-2, 1], color=GREY, lw=1.7, zorder=2)
    ax.add_patch(FancyArrowPatch(arc2d[-3], arc2d[-1], arrowstyle="-|>",
                                 color=GREY, lw=1.7, mutation_scale=13,
                                 zorder=2, shrinkA=0, shrinkB=0))

    # -- stylised right hand, thumb along +z -------------------------------
    hand(ax, ox=1.18, oy=0.78, s=0.85)
    ax.text(1.20, 0.52, "right-hand rule", ha="center", va="top",
            fontsize=10, color=GREY, style="italic", zorder=6)


def hand(ax, ox, oy, s):
    """Stylised fist with thumb pointing up (local units, scaled by s)."""
    color = GREY
    verts = [
        (-0.30, 0.00),                                    # wrist left
        (-0.40, 0.18), (-0.44, 0.30), (-0.42, 0.44),      # palm left edge
        (-0.40, 0.54), (-0.40, 0.60), (-0.38, 0.66),      # thumb root
        (-0.34, 1.06), (-0.32, 1.20), (-0.20, 1.22),      # thumb left -> tip
        (-0.12, 1.23), (-0.10, 1.10), (-0.10, 0.94),      # thumb tip -> right
        (-0.10, 0.78), (-0.11, 0.68), (-0.06, 0.70),      # thumb right edge
        (0.04, 0.74), (0.18, 0.72), (0.30, 0.66),         # web / knuckles
        (0.42, 0.58), (0.50, 0.44), (0.50, 0.30),         # fingers curl right
        (0.49, 0.12), (0.40, 0.01), (0.28, -0.02),        # curl to bottom
        (0.16, -0.04), (0.04, -0.02), (-0.30, 0.00),      # wrist right
    ]
    codes = [MplPath.MOVETO] + [MplPath.CURVE4] * (len(verts) - 1)
    path = MplPath([(ox + x * s, oy + y * s) for x, y in verts], codes)
    ax.add_patch(PathPatch(path, facecolor="none", edgecolor=color,
                           lw=1.6, zorder=5, joinstyle="round"))

    # finger creases
    for v0, v1, v2, v3 in (
        ((0.16, 0.62), (0.30, 0.50), (0.34, 0.32), (0.30, 0.14)),
        ((0.02, 0.68), (0.12, 0.52), (0.13, 0.32), (0.09, 0.14)),
    ):
        cp = [(ox + x * s, oy + y * s) for x, y in (v0, v1, v2, v3)]
        ax.add_patch(PathPatch(MplPath(cp, [MplPath.MOVETO]
                                           + [MplPath.CURVE3] * 3),
                               facecolor="none", edgecolor=color,
                               lw=1.1, zorder=5))
    # thumb tip arrow
    ax.add_patch(FancyArrowPatch((ox - 0.10 * s, oy + 0.98 * s),
                                 (ox - 0.18 * s, oy + 1.26 * s),
                                 arrowstyle="-|>", color=color, lw=1.6,
                                 mutation_scale=12, zorder=6,
                                 shrinkA=0, shrinkB=0))


def build_figure():
    fig = SPEC.figure()
    panel(fig.add_axes([0.02, 0.02, 0.96, 0.96]))
    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "right-hand-rule")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()