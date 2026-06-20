"""Three damping regimes of a mass-spring system.

Two-panel physics-textbook illustration (serif, line-art style), side by side:
  * Left:  three vertically stacked mass-spring-damper models
           (underdamped, critically damped, overdamped).
  * Right: normalized displacement x(t)/A for the three regimes vs. time,
           with the underdamped envelope, time-constant marker, and
           first zero-crossing annotated.

All three curves use the release-from-rest initial condition x(0)=A,
dx/dt(0)=0, so the critical and overdamped solutions take the standard
textbook form.

Run with:    uv run python src/oscillation/damped_oscillation.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch, Rectangle

from _viz.output import Presets

# --------------------------------------------------------------------------- #
# Physical parameters & scene
# --------------------------------------------------------------------------- #
# Choose omega0 = 2*pi so that the natural period T0 = 2*pi/omega0 = 1 s,
# giving clean integer ticks on the time axis over [0, 6*T0].
OMEGA0 = 2.0 * np.pi          # natural angular frequency, rad/s
T0 = 2.0 * np.pi / OMEGA0      # natural period (= 1 s)
A = 1.0                        # initial (normalized) amplitude

# Damping ratios: underdamped, critically damped, overdamped.
BETA_U = 0.2 * OMEGA0          # underdamped  (beta < omega0)
BETA_C = 1.0 * OMEGA0          # critical     (beta = omega0)
BETA_O = 2.0 * OMEGA0          # overdamped   (beta > omega0)

# Palette (consistent with the rest of the repo).
BLU = "#1f4e9b"
GRN = "#2e8b57"
ORG = "#d4740e"
GREY = "#888888"
MASS_COL = "#2e6fb5"           # mass block fill (blue)

SPEC = Presets.PNG_TEXTBOOK
OUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"


# --------------------------------------------------------------------------- #
# Panel (a) — model schematic (pure 2D line art)
# --------------------------------------------------------------------------- #
def _bracket(ax, x, y, w=0.9, h=0.12):
    """A fixed support: hatched grey rectangle (ceiling/floor)."""
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
    # zig-zag the interior points left/right of the centerline
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
            zorder=2)  # open top (two short tabs)
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
    """A blue mass block centered at (x, y)."""
    ax.add_patch(Rectangle(
        (x - w / 2, y - h / 2), w, h,
        facecolor=MASS_COL, edgecolor="black", linewidth=1.1, zorder=3,
    ))
    ax.text(x, y, label, ha="center", va="center",
            fontsize=11, color="white", fontweight="bold", zorder=4)


def _draw_one_system(ax, cx, cy_block, show_damper=True, motion_amp=0.22):
    """Draw one ceiling-spring-mass-(damper)-floor assembly.

    The mass block sits at ``cy_block`` (the equilibrium height). Returns
    the y of the mass center for the equilibrium line.
    """
    mass_h = 0.30
    block_top = cy_block + mass_h / 2
    block_bot = cy_block - mass_h / 2

    # ceiling bracket
    ceil_y = cy_block + 1.15
    _bracket(ax, cx, ceil_y)
    # spring from ceiling to mass top
    _spring(ax, cx, ceil_y - 0.06, block_top)

    # floor bracket
    floor_y = cy_block - 1.15
    if show_damper:
        # damper from mass bottom to floor
        _damper(ax, cx, block_bot, floor_y + 0.06)
    else:
        # no damper shown — draw a thin rigid connector so the mass is
        # still visually "above" the floor bracket.
        ax.plot([cx, cx], [block_bot, floor_y + 0.06],
                color=GREY, lw=1.4, ls=":", zorder=2)
    _bracket(ax, cx, floor_y)

    # equilibrium dashed line through the mass
    ax.plot([cx - 0.75, cx + 0.75], [cy_block, cy_block],
            color=GREY, ls="--", lw=0.9, zorder=1)

    # double-headed motion arrow to the right of the mass
    ax.add_patch(FancyArrowPatch(
        (cx + 0.62, cy_block - motion_amp),
        (cx + 0.62, cy_block + motion_amp),
        arrowstyle="<->", mutation_scale=10,
        color="black", lw=1.2, zorder=4,
    ))


def draw_model(ax):
    ax.set_axis_off()
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-4.6, 1.6)
    ax.set_aspect("equal")

    ax.set_title("(a) Three Damping Regimes of a Mass-Spring System",
                 fontsize=11, pad=8)

    # y centers for the three systems (top -> bottom).
    ys = [0.35, -1.55, -3.45]
    regimes = [
        (BETA_U, "Underdamped", r"$\beta < \omega_0$", True),
        (BETA_C, "Critically damped", r"$\beta = \omega_0$", True),
        (BETA_O, "Overdamped", r"$\beta > \omega_0$", False),
    ]
    cx = 1.4

    for i, (beta, name, cond, show_d) in enumerate(regimes):
        cy = ys[i]
        _draw_one_system(ax, cx, cy, show_damper=show_d)

        # regime label to the right of each model
        ax.text(cx + 1.05, cy + 0.08, name,
                fontsize=11, fontweight="bold", va="center")
        ax.text(cx + 1.05, cy - 0.16, cond,
                fontsize=10, color=GREY, va="center")

        # separator between systems (dashed), except after the last
        if i < len(regimes) - 1:
            sep_y = (ys[i] + ys[i + 1]) / 2.0 - 0.55
            ax.plot([-0.35, 4.0], [sep_y, sep_y],
                    color="#cccccc", ls="--", lw=0.7, zorder=0)

    # legend at the bottom of the panel
    handles = [
        Line2D([0], [0], color=GREY, lw=1.8, label="Spring ($k$)"),
        Line2D([0], [0], color=GREY, lw=1.8, label="Damper ($b$)"),
        Line2D([0], [0], color=MASS_COL, lw=6.0, label="Mass ($m$)"),
        Line2D([0], [0], color=GREY, ls="--", lw=1.0, label="Equilibrium"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=8,
              frameon=True, edgecolor="#cccccc", facecolor="white",
              framealpha=0.9, bbox_to_anchor=(0.0, 0.135))


# --------------------------------------------------------------------------- #
# Solutions
# --------------------------------------------------------------------------- #
def x_underdamped(t, beta):
    w1 = np.sqrt(OMEGA0**2 - beta**2)
    return A * np.exp(-beta * t) * np.cos(w1 * t)


def x_critical(t):
    return A * (1.0 + OMEGA0 * t) * np.exp(-OMEGA0 * t)


def x_overdamped(t, beta):
    disc = np.sqrt(beta**2 - OMEGA0**2)
    r1 = beta - disc
    r2 = beta + disc
    return A * 0.5 * (np.exp(-r1 * t) + np.exp(-r2 * t))


# --------------------------------------------------------------------------- #
# Panel (b) — displacement curves
# --------------------------------------------------------------------------- #
def draw_curves(ax):
    ax.set_title(
        r"(b) Displacement vs. Time for Three Damping Regimes",
        fontsize=11, pad=8,
    )

    t = np.linspace(0, 6 * T0, 2000)
    w1 = np.sqrt(OMEGA0**2 - BETA_U**2)

    xu = x_underdamped(t, BETA_U)
    xc = x_critical(t)
    xo = x_overdamped(t, BETA_O)
    env_p = A * np.exp(-BETA_U * t)   # positive envelope
    env_n = -env_p                     # negative envelope

    # --- curves ---
    ax.plot(t, xu, color=BLU, lw=2.6, label="Underdamped", zorder=4)
    ax.plot(t, xc, color=GRN, lw=2.6, label="Critically damped", zorder=4)
    ax.plot(t, xo, color=ORG, lw=2.6, label="Overdamped", zorder=4)

    # --- underdamped envelope (dashed blue) ---
    ax.plot(t, env_p, color=BLU, ls="--", lw=1.4, alpha=0.9, zorder=3)
    ax.plot(t, env_n, color=BLU, ls="--", lw=1.4, alpha=0.9, zorder=3)

    # --- axes ---
    ax.set_xlim(0, 6 * T0)
    ax.set_xticks(np.arange(0, 6 * T0 + 1e-9, T0))
    ax.set_xticklabels([r"$0$", r"$T_0$", r"$2T_0$", r"$3T_0$",
                        r"$4T_0$", r"$5T_0$", r"$6T_0$"])
    ax.set_xlabel(r"Time $t$ (s)", fontsize=10)

    ax.set_ylim(-0.45, 1.18)
    ax.set_yticks([1.0, 0.5, 0.0, -0.5])
    ax.set_ylabel(r"Displacement $x(t)/A$", fontsize=10)
    ax.tick_params(labelsize=8)

    # --- light grey dashed grid ---
    ax.grid(True, which="both", color="#dddddd", lw=0.6, ls="--", zorder=0)
    ax.axhline(0, color=GREY, lw=0.7, zorder=1)

    # --- common start point at (0, A) ---
    ax.scatter([0], [A], s=30, facecolor="white",
               edgecolor="black", zorder=6)

    # --- time-constant marker: envelope = A/e at t = tau = 1/beta ---
    inv_e = A / np.e
    tau = 1.0 / BETA_U
    ax.axhline(inv_e, color=BLU, ls=":", lw=1.0, alpha=0.8, zorder=2)
    ax.plot([tau, tau], [0, inv_e], color=BLU, ls=":", lw=1.0,
            alpha=0.8, zorder=2)
    ax.scatter([tau], [inv_e], s=26, facecolor="white",
               edgecolor=BLU, zorder=6)
    ax.annotate(r"$\tau = 1/\beta$", xy=(tau, inv_e),
                xytext=(tau + 0.25, inv_e + 0.13),
                fontsize=9, color=BLU,
                arrowprops=dict(arrowstyle="->", color=BLU, lw=0.8))
    ax.text(6 * T0 - 0.05, inv_e + 0.015, r"$A/e$",
            ha="right", va="bottom", fontsize=8, color=BLU)

    # --- underdamped first zero-crossing ---
    # cos(w1 t) = 0  ->  t = pi/(2 w1)
    t_zero1 = np.pi / (2 * w1)
    ax.scatter([t_zero1], [0], s=26, facecolor="white",
               edgecolor=BLU, zorder=6)
    ax.annotate("first zero", xy=(t_zero1, 0),
                xytext=(t_zero1 + 0.2, -0.22),
                fontsize=8, color=BLU,
                arrowprops=dict(arrowstyle="->", color=BLU, lw=0.8))

    # --- formula labels (bold, color-matched, rounded boxes) ---
    ax.text(
        0.985, 0.94,
        r"$\mathbf{x(t) = A\,e^{-\beta t}\cos(\omega_1 t)}$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10.5, color=BLU, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.30", fc="white",
                  ec="#cccccc", lw=0.6),
    )
    ax.text(
        0.985, 0.80,
        r"$\mathbf{x(t) = A(1+\omega_0 t)\,e^{-\omega_0 t}}$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10.5, color=GRN, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.30", fc="white",
                  ec="#cccccc", lw=0.6),
    )
    ax.text(
        0.985, 0.66,
        r"$\mathbf{x(t) = \dfrac{A}{2}(e^{-r_1 t}+e^{-r_2 t})}$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=10.5, color=ORG, fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.30", fc="white",
                  ec="#cccccc", lw=0.6),
    )
    # omega1 definition (small, near the underdamped formula)
    ax.text(
        0.985, 0.585,
        r"$\omega_1 = \sqrt{\omega_0^2 - \beta^2}$",
        transform=ax.transAxes, ha="right", va="top",
        fontsize=9, color=BLU, style="italic",
    )

    # --- legend ---
    handles = [
        Line2D([0], [0], color=BLU, lw=2.6, label="Underdamped"),
        Line2D([0], [0], color=GRN, lw=2.6, label="Critically damped"),
        Line2D([0], [0], color=ORG, lw=2.6, label="Overdamped"),
        Line2D([0], [0], color=BLU, ls="--", lw=1.4,
               label=r"Envelope $\pm A e^{-\beta t}$"),
    ]
    # Legend in the lower-right where all three curves have decayed to ~0.
    ax.legend(handles=handles, loc="lower right", fontsize=8.5,
              frameon=True, edgecolor="#cccccc", facecolor="white",
              framealpha=0.9)


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
    path = SPEC.save(fig, OUT_DIR / "damped_oscillation")
    plt.close(fig)
    print(f"Saved: {path}")


if __name__ == "__main__":
    main()
