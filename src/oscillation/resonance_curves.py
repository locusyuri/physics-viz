"""Resonance curves for a driven damped harmonic oscillator.

Two-panel physics-textbook illustration (serif, line-art style), side by side:
  * Left:  model schematic — spring-mass-damper driven by a crank mechanism.
  * Right: amplitude A(ω) vs. driving frequency ω for three damping ratios,
           with resonance-frequency markers, FWHM annotation, and the
           undamped asymptotic reference.

Run with:    uv run python src/oscillation/resonance_curves.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle

from _viz.output import Presets

# --------------------------------------------------------------------------- #
# Physical parameters
# --------------------------------------------------------------------------- #
OMEGA0 = 1.0                         # natural frequency (normalized)
ZETA_UNDER = 0.05                    # weak damping   β/ω₀
ZETA_MEDIUM = 0.10                   # medium damping  β/ω₀
ZETA_HEAVY = 0.30                    # heavy damping   β/ω₀

# Palette (consistent with damped_oscillation.py).
BLU = "#1f4e9b"
GRN = "#2e8b57"
ORG = "#d4740e"
GREY = "#888888"
RED = "#cc3333"
MASS_COL = "#2e6fb5"

SPEC = Presets.PNG_TEXTBOOK
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"


# --------------------------------------------------------------------------- #
# Drawing primitives (reused from damped_oscillation.py)
# --------------------------------------------------------------------------- #
def _bracket(ax, x, y, w=0.9, h=0.12):
    """A fixed support: hatched grey rectangle (ceiling / floor)."""
    ax.add_patch(Rectangle(
        (x - w / 2, y - h / 2), w, h,
        facecolor="#d5d8dc", edgecolor=GREY, linewidth=1.0,
        hatch="////", zorder=2,
    ))


def _spring(ax, x, y_top, y_bot, coils=7, width=0.18, lw=1.6):
    """A vertical zig-zag spring from (x, y_top) down to (x, y_bot)."""
    n = coils * 2
    ys = np.linspace(y_top, y_bot, n + 3)
    xs = np.full_like(ys, x)
    xs[1:-1] = x + np.array(
        [width if i % 2 else -width for i in range(n + 1)]
    )
    ax.plot(xs, ys, color=GREY, lw=lw, zorder=2, solid_joinstyle="round")


def _damper(ax, x, y_top, y_bot, width=0.26, lw=1.6):
    """A vertical dashpot: piston rod + cylinder + piston head."""
    mid = (y_top + y_bot) / 2.0
    # piston rod from top attachment to the piston head
    ax.plot([x, x], [y_top, mid + 0.02], color=GREY, lw=lw, zorder=2)
    # cylinder (open-top box) housing the piston head
    cyl_top = mid + 0.06
    ax.plot([x - width, x + width], [cyl_top, cyl_top], color=GREY, lw=lw,
            zorder=2)
    ax.plot([x - width, x - width], [cyl_top, y_bot], color=GREY, lw=lw,
            zorder=2)
    ax.plot([x + width, x + width], [cyl_top, y_bot], color=GREY, lw=lw,
            zorder=2)
    ax.plot([x - width, x + width], [y_bot, y_bot], color=GREY, lw=lw,
            zorder=2)
    # piston head inside the cylinder
    ax.plot([x - width + 0.04, x + width - 0.04], [mid, mid],
            color=GREY, lw=lw + 0.6, zorder=3)


def _mass_block(ax, x, y, w=0.42, h=0.30, label=r"$m$"):
    """A blue mass block centred at (x, y)."""
    ax.add_patch(Rectangle(
        (x - w / 2, y - h / 2), w, h,
        facecolor=MASS_COL, edgecolor="black", linewidth=1.1, zorder=3,
    ))
    ax.text(x, y, label, ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=4)


# --------------------------------------------------------------------------- #
# Panel (a) — model schematic
# --------------------------------------------------------------------------- #
def draw_model(ax):
    """Draw the driven damped harmonic oscillator model.

    Left side: vertical spring-mass-damper assembly.
    Right side: rotating crank mechanism delivering the driving force.
    """
    ax.set_axis_off()
    ax.set_xlim(-0.5, 5.8)
    ax.set_ylim(-2.8, 2.8)
    ax.set_aspect("equal")

    ax.set_title("(a) Driven Damped Harmonic Oscillator",
                 fontsize=11, pad=8)

    # --- Mass-spring-damper assembly (vertical) ---
    cx = 1.5          # centre x of the mass
    cy = 0.0          # equilibrium y of the mass
    mass_h = 0.30
    mass_w = 0.42
    block_top = cy + mass_h / 2
    block_bot = cy - mass_h / 2

    # Ceiling bracket
    ceil_y = cy + 1.6
    _bracket(ax, cx, ceil_y)

    # Spring from ceiling to mass top
    _spring(ax, cx, ceil_y - 0.06, block_top)

    # Floor bracket + damper from mass bottom to floor
    floor_y = cy - 1.6
    _damper(ax, cx, block_bot, floor_y + 0.06)
    _bracket(ax, cx, floor_y)

    # Mass block
    _mass_block(ax, cx, cy)

    # Equilibrium dashed line through the mass
    ax.plot([cx - 0.75, cx + 0.75], [cy, cy],
            color=GREY, ls="--", lw=0.9, zorder=1)

    # --- Force arrows on spring and damper ---
    # Spring restoring force (upward, toward ceiling)
    arrow_y_s = cy + 0.55
    ax.annotate("", xy=(cx + 0.38, arrow_y_s + 0.28),
                xytext=(cx + 0.38, arrow_y_s - 0.28),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.text(cx + 0.58, arrow_y_s, r"$F_s = -kx$",
            fontsize=8.5, color=RED, va="center")

    # Damper force (opposing velocity, shown downward for positive velocity)
    arrow_y_d = cy - 0.55
    ax.annotate("", xy=(cx + 0.38, arrow_y_d - 0.28),
                xytext=(cx + 0.38, arrow_y_d + 0.28),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))
    ax.text(cx + 0.58, arrow_y_d, r"$F_d = -b\dot{x}$",
            fontsize=8.5, color=RED, va="center")

    # --- Crank mechanism (right side) ---
    wheel_cx = 4.0
    wheel_cy = cy
    wheel_r = 0.55
    crank_angle = np.deg2rad(30)  # 30° for a dynamic look

    # Wheel circle
    ax.add_patch(Circle((wheel_cx, wheel_cy), wheel_r,
                        facecolor="none", edgecolor=GREY, lw=1.8, zorder=3))
    # Wheel centre dot
    ax.scatter([wheel_cx], [wheel_cy], s=18, color=GREY, zorder=4)

    # Crank arm (radius line from centre to pin)
    pin_x = wheel_cx + wheel_r * np.cos(crank_angle)
    pin_y = wheel_cy + wheel_r * np.sin(crank_angle)
    ax.plot([wheel_cx, pin_x], [wheel_cy, pin_y],
            color=GREY, lw=2.0, zorder=3)
    # Pin dot
    ax.scatter([pin_x], [pin_y], s=28, facecolor="white",
               edgecolor=GREY, lw=1.2, zorder=4)

    # Connecting rod from mass right edge to pin
    mass_right = cx + mass_w / 2
    ax.plot([mass_right, pin_x], [cy, pin_y],
            color=GREY, lw=2.0, zorder=3, solid_joinstyle="round")

    # Rotation arrow (curved, counterclockwise around the wheel)
    ax.annotate("", xy=(wheel_cx + 0.38, wheel_cy + 0.35),
                xytext=(wheel_cx - 0.38, wheel_cy + 0.45),
                arrowprops=dict(
                    arrowstyle="->,head_length=4,head_width=3",
                    color=RED, lw=1.4,
                    connectionstyle="arc3,rad=0.45",
                ),
                zorder=5)

    # Driving force arrow along the connecting rod direction
    ax.annotate("", xy=(mass_right + 0.12, cy + 0.04),
                xytext=(pin_x - 0.25, pin_y - 0.04),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))

    # --- Labels ---
    # k label (spring stiffness)
    ax.text(cx + 0.75, cy + 0.85, r"$k$", fontsize=10, color=GREY,
            ha="center")
    # b label (damping coefficient)
    ax.text(cx + 0.75, cy - 0.85, r"$b$", fontsize=10, color=GREY,
            ha="center")
    # ω label near rotation arrow
    ax.text(wheel_cx + 0.92, wheel_cy + 0.35, r"$\omega$",
            fontsize=10, color=RED, ha="center")
    # F₀ label near the pin
    ax.text(pin_x + 0.18, pin_y + 0.22, r"$F_0$",
            fontsize=10, color=RED, ha="center")
    # Driving force expression
    ax.text(wheel_cx + 0.05, wheel_cy - 0.95,
            r"$F_0\cos(\omega t)$", fontsize=9.5, color=RED,
            ha="center", va="top")

    # --- Legend ---
    handles = [
        Line2D([0], [0], color=GREY, lw=1.8, label="Spring ($k$)"),
        Line2D([0], [0], color=GREY, lw=1.8, label="Damper ($b$)"),
        Line2D([0], [0], color=MASS_COL, lw=6.0, label="Mass ($m$)"),
        Line2D([0], [0], color=RED, lw=1.4,
               label=r"Driving force $F_0\cos(\omega t)$"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=7.5,
              frameon=True, edgecolor="#cccccc", facecolor="white",
              framealpha=0.9, bbox_to_anchor=(0.0, 0.05))


# --------------------------------------------------------------------------- #
# Amplitude function
# --------------------------------------------------------------------------- #
def amplitude(x, zeta):
    """Normalised amplitude A(x) / A_static for a driven damped oscillator.

    Parameters
    ----------
    x : array_like
        Normalised driving frequency ω/ω₀.
    zeta : float
        Damping ratio β/ω₀.

    Returns
    -------
    array_like
        A(x) / A_static = 1 / √((1−x²)² + (2ζx)²).
    """
    denom = np.sqrt((1 - x ** 2) ** 2 + (2 * zeta * x) ** 2)
    with np.errstate(divide="ignore"):
        result = 1.0 / denom
    return result


def resonance_x(zeta):
    """Resonance frequency (normalised): ω_res / ω₀ = √(1 − 2ζ²).

    Returns 0 when ζ ≥ 1/√2 (no resonance peak).
    """
    disc = 1 - 2 * zeta ** 2
    if disc <= 0:
        return 0.0
    return np.sqrt(disc)


# --------------------------------------------------------------------------- #
# Panel (b) — resonance curves
# --------------------------------------------------------------------------- #
def draw_curves(ax):
    """Draw amplitude A(ω) vs. driving frequency for three damping ratios.

    Includes resonance-frequency markers, a FWHM annotation, and the
    undamped asymptotic reference.
    """
    ax.set_title(
        r"(b) Resonance Curves — Amplitude vs. Driving Frequency",
        fontsize=11, pad=8,
    )

    x = np.linspace(0.001, 2.5, 2000)  # avoid x = 0 exactly

    # Compute amplitudes for each damping ratio
    a_under = amplitude(x, ZETA_UNDER)    # β/ω₀ = 0.05
    a_medium = amplitude(x, ZETA_MEDIUM)  # β/ω₀ = 0.10
    a_heavy = amplitude(x, ZETA_HEAVY)    # β/ω₀ = 0.30

    # Global maximum — the peak of the weakest-damping curve
    a_max = np.max(a_under)

    # Normalise all curves to the global maximum
    a_under_n = a_under / a_max
    a_medium_n = a_medium / a_max
    a_heavy_n = a_heavy / a_max

    # Resonance frequencies (normalised) and amplitudes at resonance
    x_res_u = resonance_x(ZETA_UNDER)
    x_res_m = resonance_x(ZETA_MEDIUM)
    x_res_h = resonance_x(ZETA_HEAVY)

    a_res_u = amplitude(x_res_u, ZETA_UNDER) / a_max
    a_res_m = amplitude(x_res_m, ZETA_MEDIUM) / a_max
    a_res_h = amplitude(x_res_h, ZETA_HEAVY) / a_max

    # --- Plot curves ---
    ax.plot(x, a_under_n, color=BLU, lw=2.6,
            label=r"$\beta/\omega_0 = 0.05$", zorder=4)
    ax.plot(x, a_medium_n, color=GRN, lw=2.6,
            label=r"$\beta/\omega_0 = 0.10$", zorder=4)
    ax.plot(x, a_heavy_n, color=ORG, lw=2.6,
            label=r"$\beta/\omega_0 = 0.30$", zorder=4)

    # --- Undamped reference: vertical dashed line at x = 1 ---
    ax.axvline(1.0, color=GREY, ls="--", lw=1.4, alpha=0.8, zorder=2)
    # "∞" symbol near the top to indicate divergence
    ax.text(1.0, 1.15, r"$\to\infty$", ha="center", va="bottom",
            fontsize=9, color=GREY, fontstyle="italic")

    # --- Natural frequency marker (red dashed vertical) ---
    ax.axvline(1.0, color=RED, ls=":", lw=1.0, alpha=0.7, zorder=2)
    ax.annotate(r"Natural frequency $\omega_0$",
                xy=(1.0, 1.08), xytext=(1.28, 1.08),
                fontsize=8.5, color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=0.8))

    # --- Resonance frequency markers (hollow circles at each peak) ---
    ax.scatter([x_res_u], [a_res_u], s=50, facecolor="white",
               edgecolor=BLU, lw=1.5, zorder=6)
    ax.scatter([x_res_m], [a_res_m], s=50, facecolor="white",
               edgecolor=GRN, lw=1.5, zorder=6)
    ax.scatter([x_res_h], [a_res_h], s=50, facecolor="white",
               edgecolor=ORG, lw=1.5, zorder=6)

    # Resonance frequency formula (once, near the blue peak)
    ax.annotate(
        r"$\omega_{\rm res} = \omega_0\sqrt{1 - 2\beta^2/\omega_0^2}$",
        xy=(x_res_u, a_res_u),
        xytext=(x_res_u + 0.50, a_res_u - 0.02),
        fontsize=9, color=BLU,
        arrowprops=dict(arrowstyle="->", color=BLU, lw=0.8),
        bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#cccccc",
                  lw=0.5),
    )

    # --- FWHM annotation on the green curve (ζ = 0.1) ---
    half_max = a_res_m / 2.0
    x_left = 1.0 - ZETA_MEDIUM
    x_right = 1.0 + ZETA_MEDIUM

    # Horizontal double-headed arrow at half-maximum
    ax.annotate("", xy=(x_left, half_max), xytext=(x_right, half_max),
                arrowprops=dict(arrowstyle="<->", color=GRN, lw=1.2))
    # Vertical dashed guides from half-max points down to the x-axis
    ax.plot([x_left, x_left], [0, half_max], color=GRN, ls=":",
            lw=0.7, alpha=0.6, zorder=2)
    ax.plot([x_right, x_right], [0, half_max], color=GRN, ls=":",
            lw=0.7, alpha=0.6, zorder=2)
    # FWHM label
    ax.text(1.0, half_max + 0.025,
            r"FWHM $\Delta\omega = 2\beta$",
            ha="center", va="bottom", fontsize=8.5, color=GRN,
            bbox=dict(boxstyle="round,pad=0.20", fc="white", ec=GRN,
                      lw=0.5, alpha=0.85))

    # --- Axes ---
    ax.set_xlim(0, 2.5)
    ax.set_xlabel(r"Driving frequency $\omega/\omega_0$", fontsize=10)
    ax.set_xticks(np.arange(0, 2.6, 0.5))

    ax.set_ylim(0, 1.2)
    ax.set_ylabel(r"Amplitude $A(\omega)/A_{\rm max}$", fontsize=10)
    ax.set_yticks(np.arange(0, 1.3, 0.2))
    ax.tick_params(labelsize=8)

    # --- Light grey dashed grid ---
    ax.grid(True, which="both", color="#dddddd", lw=0.6, ls="--", zorder=0)
    ax.axhline(0, color=GREY, lw=0.7, zorder=1)

    # --- Legend ---
    handles = [
        Line2D([0], [0], color=BLU, lw=2.6,
               label=r"$\beta/\omega_0 = 0.05$"),
        Line2D([0], [0], color=GRN, lw=2.6,
               label=r"$\beta/\omega_0 = 0.10$"),
        Line2D([0], [0], color=ORG, lw=2.6,
               label=r"$\beta/\omega_0 = 0.30$"),
        Line2D([0], [0], color=GREY, ls="--", lw=1.4,
               label=r"Undamped ($\beta \to 0$)"),
    ]
    ax.legend(handles=handles, loc="center right", fontsize=8.5,
              frameon=True, edgecolor="#cccccc", facecolor="white",
              framealpha=0.9, bbox_to_anchor=(1.0, 0.55))


# --------------------------------------------------------------------------- #
# Build the figure
# --------------------------------------------------------------------------- #
def build_figure():
    fig = SPEC.figure()
    ax_model = fig.add_subplot(121)
    ax_curve = fig.add_subplot(122)

    fig.subplots_adjust(left=0.06, right=0.97, top=0.91, bottom=0.10,
                        wspace=0.22)

    draw_model(ax_model)
    draw_curves(ax_curve)

    return fig


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    fig = build_figure()
    path = SPEC.save(fig, OUT_DIR / "resonance_curves")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()