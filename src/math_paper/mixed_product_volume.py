"""Volume of a parallelepiped spanned by a, b, c: V = |(a, b, c)|.

Single-panel isometric projection (elevation 30 deg, azimuth 30 deg):
- vectors a = (2, 0, 0) blue, b = (0.6, 1.8, 0) green, c = (0.3, 0.3, 1.8)
  orange, all from the origin;
- base parallelogram (0,0,0), (2,0,0), (2.6,1.8,0), (0.6,1.8,0) filled
  light blue; the visible faces of the solid tinted pale grey, hidden
  edges dashed;
- dashed height line h from the base centre to the top centre;
- volume label V = |(a, b, c)| at the right;
- white background, SVG output.

Run with: uv run python src/math_paper/mixed_product_volume.py
"""

from __future__ import annotations

import math
from dataclasses import replace
from pathlib import Path
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, Polygon

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from _viz.output import Presets

SPEC = replace(Presets.SVG_TEXTBOOK, figsize=(8.6, 8.6), transparent=False)
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"

# -- colors -------------------------------------------------------------
BLUE = "#2563EB"
GREEN = "#16A34A"
ORANGE = "#EA580C"
BASE_FILL = "#DBEAFE"
SOLID_FILL = "#F3F4F6"
DASH = "#6B7280"
INK = "#333333"

# -- spec data ----------------------------------------------------------
A = np.array([2.0, 0.0, 0.0])
B = np.array([0.6, 1.8, 0.0])
C = np.array([0.3, 0.3, 1.8])
BASE = [np.array(p, float) for p in
        ((0, 0, 0), (2, 0, 0), (2.6, 1.8, 0), (0.6, 1.8, 0))]

# geometry self-check: base = |a x b|, h = mixed product / base area
_det = abs(np.linalg.det(np.stack([A, B, C], axis=1)))
_area = np.linalg.norm(np.cross(A, B))
_h = np.dot(C, np.cross(A, B) / _area)
assert abs(_det - _area * _h) < 1e-9

# -- isometric projection: elevation 30 deg, azimuth 30 deg --------------
AZ = math.radians(30.0)
EL = math.radians(30.0)
SA, CA = math.sin(AZ), math.cos(AZ)
SE, CE = math.sin(EL), math.cos(EL)
CAM = np.array([CE * CA, CE * SA, SE])          # towards the viewer


def proj(p):
    x, y, z = p
    return (-x * SA + y * CA, -x * CA * SE - y * SA * SE + z * CE)


# -- faces of the solid ---------------------------------------------------
O = np.zeros(3)
SOLID_C = (sum(BASE, np.zeros(3)) / 4.0) + C / 2.0   # solid centre
FACES = [
    ("bottom", [O, BASE[1], BASE[2], BASE[3]]),           # z = 0
    ("top", [p + C for p in BASE]),                        # z = 1.8
    ("side a", [O, BASE[3], BASE[3] + C, C]),              # b-c face at origin
    ("side A", [BASE[1], BASE[2], BASE[2] + C, BASE[1] + C]),   # +a face
    ("side c", [O, BASE[1], BASE[1] + C, C]),              # a-c face at origin
    ("side b", [BASE[3], BASE[2], BASE[2] + C, BASE[3] + C]),   # +b face
]


def outward_normal(quad):
    n = np.cross(quad[1] - quad[0], quad[3] - quad[0])
    ctr = sum(quad, np.zeros(3)) / 4.0
    return n if np.dot(n, ctr - SOLID_C) > 0 else -n


VIS = {name: np.dot(outward_normal(quad), CAM) > 0 for name, quad in FACES}

# an edge is hidden iff no face that contains it is visible
edge_vis = {}
for name, quad in FACES:
    for i in range(4):
        key = tuple(sorted((tuple(quad[i]), tuple(quad[(i + 1) % 4]))))
        edge_vis[key] = edge_vis.get(key, False) or VIS[name]

assert sum(1 for v in edge_vis.values() if not v) == 3   # 3 hidden edges


def arrow3(ax, p0, p1, color, lw, zorder=4, ms=16):
    ax.add_patch(
        FancyArrowPatch(proj(p0), proj(p1), arrowstyle="-|>", color=color,
                        lw=lw, mutation_scale=ms, zorder=zorder,
                        shrinkA=0, shrinkB=0)
    )


def panel(ax):
    ax.set_xlim(-1.62, 2.78)
    ax.set_ylim(-1.88, 1.82)
    ax.set_aspect("equal")
    ax.axis("off")

    # -- hidden edges first (dashed) --------------------------------------
    for (p0, p1), visible in edge_vis.items():
        if not visible:
            (x0, y0), (x1, y1) = proj(p0), proj(p1)
            ax.plot([x0, x1], [y0, y1], ls=(0, (4, 3)), color=DASH,
                    lw=1.0, zorder=2)

    # -- base parallelogram, highlighted ----------------------------------
    ax.add_patch(Polygon([proj(p) for p in BASE], closed=True,
                         facecolor=BASE_FILL, edgecolor=BLUE, lw=1.0,
                         zorder=1))

    # -- visible faces of the solid, pale grey ----------------------------
    for name, quad in FACES:
        if VIS[name]:
            ax.add_patch(Polygon([proj(p) for p in quad], closed=True,
                                 facecolor=SOLID_FILL, edgecolor=INK,
                                 lw=1.0, alpha=0.85, zorder=2))

    # -- height line h: base centre -> top centre --------------------------
    base_c = sum(BASE, np.zeros(3)) / 4.0
    top_c = base_c + C
    (x0, y0), (x1, y1) = proj(base_c), proj(top_c)
    ax.plot([x0, x1], [y0, y1], ls=(0, (5, 4)), color=DASH, lw=1.2,
            zorder=3)
    ax.text(x0 + 0.10, (y0 + y1) / 2, "$h$", fontsize=13, color=DASH,
            ha="left", va="center", zorder=6)

    # -- the three vectors --------------------------------------------------
    arrow3(ax, (0, 0, 0), A, BLUE, lw=2.6)
    arrow3(ax, (0, 0, 0), B, GREEN, lw=2.6)
    arrow3(ax, (0, 0, 0), C, ORANGE, lw=2.6)

    for vec, label, ha, dx, dy in (
        (A, r"$\mathbf{a}$", "right", -0.14, -0.02),
        (B, r"$\mathbf{b}$", "left", 0.14, -0.06),
        (C, r"$\mathbf{c}$", "left", 0.10, 0.04),
    ):
        sp = proj(vec)
        ax.text(sp[0] + dx, sp[1] + dy, label, ha=ha, va="center",
                fontsize=13, color="black", zorder=6)

    # -- volume label --------------------------------------------------------
    ax.text(1.55, 0.92, r"$V = |(\mathbf{a},\mathbf{b},\mathbf{c})|$",
            fontsize=14, color="black", ha="left", va="center", zorder=6)
    ax.text(1.55, 0.52, r"$= |\mathbf{a}\times\mathbf{b}|\; h$",
            fontsize=13, color=INK, ha="left", va="center", zorder=6)


def build_figure():
    fig = SPEC.figure()
    panel(fig.add_axes([0.02, 0.02, 0.96, 0.96]))
    return fig


def main():
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "mixed-product-volume")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()