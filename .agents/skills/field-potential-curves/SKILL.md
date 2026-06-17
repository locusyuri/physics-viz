---
name: field-potential-curves
description: Generate E(r) and V(r) curve panels (electric field + potential vs. distance) for charge distributions — point charge, spherical shell, solid sphere, concentric shells, line charge, cylindrical shell. Specialized companion to physics-model-figures for figures whose right panel is a piecewise E/V vs. distance plot. Use when the task is specifically about electric field and potential curves.
---

# Field & Potential Curves (E(r), V(r) vs. distance)

Specialized skill for the **curve panel** of electrostatics figures: plotting
electric field $E(r)$ and potential $V(r)$ as functions of distance $r$ (or
$\rho$) for a charge distribution. This is the right-hand panel that pairs
with a model diagram (see the general `physics-model-figures` skill for layout,
presets, and conventions — this skill narrows in on the E/V specifics).

The general skill covers *any* model+curves figure. Reach for **this** skill
when the curves are specifically $E$ and $V$ vs. distance — i.e. when you need
the piecewise functions, the dual-y-axis recipe, the ρ₀ reference, or the
canonical formula set below.

## When to use

- Right panel shows $E(r)$ and/or $V(r)$ vs. distance for any charge geometry:
  point charge, spherical shell, solid sphere, concentric shells, infinite line
  charge, cylindrical shell, …
- You need the **standard piecewise forms** for any of these geometries.
- You need the **dual-y-axis** E/V layout (blue E on left, green V on right).

Do NOT use for: pure model diagrams with no curves (use `physics-model-figures`
single-panel variant), or non-electrostatics curves.

## The canonical charge geometries

All forms use $k = 1/(4\pi\varepsilon_0)$. For line/cylindrical geometries the
grouping constant is $\dfrac{\lambda}{2\pi\varepsilon_0}$.

| Geometry | $E(r)$ | $V(r)$ |
|---|---|---|
| **Point charge $q$** | $kq/r^2$ | $kq/r$ |
| **Spherical shell (radius $R$, charge $Q$)** | $\begin{cases}0 & r<R \\ kQ/r^2 & r\geq R\end{cases}$ | $\begin{cases}kQ/R & r\leq R \\ kQ/r & r>R\end{cases}$ |
| **Solid sphere (radius $R$, charge $Q$)** | $\begin{cases}kQr/R^3 & r<R \\ kQ/r^2 & r\geq R\end{cases}$ | $\begin{cases}\dfrac{kQ}{2R}(3-r^2/R^2) & r\leq R \\ kQ/r & r>R\end{cases}$ |
| **Concentric shells ($Q_a$@$a$, $Q_b$@$b$)** | $\begin{cases}0 & r<a \\ kQ_a/r^2 & a\leq r<b \\ k(Q_a+Q_b)/r^2 & r\geq b\end{cases}$ | $\begin{cases}kQ_a/a+kQ_b/b & r<a \\ kQ_a/r+kQ_b/b & a\leq r<b \\ k(Q_a+Q_b)/r & r\geq b\end{cases}$ |
| **Infinite line charge $\lambda$** | $\lambda/(2\pi\varepsilon_0\rho)$ | $\dfrac{\lambda}{2\pi\varepsilon_0}\ln(\rho_0/\rho)$ |
| **Cylindrical shell (radius $R$, $\lambda$)** | $\begin{cases}0 & \rho<R \\ \lambda/(2\pi\varepsilon_0\rho) & \rho\geq R\end{cases}$ | $\begin{cases}\dfrac{\lambda}{2\pi\varepsilon_0}\ln(\rho_0/R) & \rho<R \\ \dfrac{\lambda}{2\pi\varepsilon_0}\ln(\rho_0/\rho) & \rho\geq R\end{cases}$ |

### Continuity rules (sanity-check your plot)

- $E(r)$: **discontinuous** at a **surface** charge (shell, cylindrical shell)
  — jumps by $\sigma/\varepsilon_0$. **Continuous** for a **volume** charge
  (solid sphere) and at the inner edge of a shell (no surface there).
- $V(r)$: **always continuous** everywhere (potential can't jump).
- $E(R^+) \neq E(R^-)$ is *expected* for shells — don't "fix" it by forcing a
  join. If your plotted E looks continuous at a shell surface, the function is
  wrong.

### The ρ₀ reference

$V$ for line/cylindrical geometries needs a **reference distance** $\rho_0$
where $V(\rho_0)=0$ (potential is only defined up to a constant). Pick
$\rho_0$ inside the plotted range and draw a vertical dashed line at it. A
common choice: $\rho_0 = 2R$ or $\rho_0$ at the right edge of the plot.

## The dual-y-axis recipe

$E$ (N/C) and $V$ (V) have different units and scales → **twin axes**, not a
shared one. Single shared axis only when one curve dominates or units match
(e.g. `src/point_charge_field.py` puts both on one axis because values
coincide at small scales).

```python
ax_e = fig.add_subplot(...)
ax_v = ax_e.twinx()

ax_e.set_ylabel("E (N/C)", color=BLU)
ax_e.tick_params(axis="y", labelcolor=BLU)
ax_e.spines["left"].set_color(BLU)

ax_v.set_ylabel("V (V)", color=GRN)
ax_v.tick_params(axis="y", labelcolor=GRN)
ax_v.spines["right"].set_color(GRN)
```

Colour convention (used across all repo figures): **E = blue `#1f4e9b`**,
**V = green `#2e8b57`**. Stick to it for visual consistency.

### Choosing y-axis ranges

$E$ and $V$ ranges differ per geometry — set them per figure, not via a preset:

- **Shells/solid sphere**: $E$ peaks at the surface then falls; set $E$ range
  to comfortably clear $E(R)$. $V$ is positive, peaks at centre; range clears
  $V(0)$. e.g. solid sphere $V(0)=3kQ/(2R)$ needs a taller V axis than a shell.
- **Line/cylindrical**: $E\to\infty$ near $\rho\to0$ — start the x-axis at a
  small positive value (e.g. $0.1\rho_0$), not 0. $V$ goes **negative** for
  $\rho>\rho_0$ → the V y-axis must include a negative range (e.g.
  `set_ylim(-30, 20)`).

### Plotting piecewise functions

Build separate arrays per region and `plot` each segment. Don't use a single
array with `np.where` — it hides the discontinuities and can draw spurious
vertical lines at boundaries.

```python
r1 = np.linspace(0, R, 200)       # inside
r2 = np.linspace(R, 4 * R, 400)   # outside
ax_e.plot(r1, np.zeros_like(r1), color=BLU, lw=2.8)   # E=0 inside
ax_e.plot(r2, K * Q / r2**2, color=BLU, lw=2.8)        # E=kQ/r² outside
```

## Required annotations

Every E/V curve panel in this repo includes these — see existing scripts for
exact code:

1. **Vertical dashed line(s)** at each region boundary ($r=R$, $r=a$, $r=b$,
   $\rho=\rho_0$) in grey (`#888888`), with a small label.
2. **Marked points** at key values: white-filled circle (`facecolor="white"`,
   `edgecolor=<curve color>`) + `annotate` with the numeric value. For the
   central maximum $V(0)$ use a fraction form
   (`$V_0 = \frac{3kQ}{2R}$`) alongside the number.
3. **Asymptotes**: `axhline(0, ls="--")` with a label. Line-charge figures add
   $V\to -\infty$. Mark these near the right edge with
   `ha="right", style="italic"`.
4. **Formula boxes** (upper area of each axis): the **full piecewise
   expression**, one line per region, stacked with `\n`. See gotcha below for
   the mathtext limitation. **No numeric constants** (no `k=9e9, Q=...`) — per
   repo convention.
5. **Legend** (`loc="upper right"` or `"center right"`): one entry per curve,
   label = `$E(r)$` / `$V(r)$` (function name only, not the formula).
6. **Light grid**: `ax_e.grid(True, color="#dddddd", lw=0.6)`.
7. **Subtitle** via `ax.set_title(...)`, **no** `suptitle`.

### Marked-point label placement (avoid overlaps)

When $E$ and $V$ curves cross or sit close (common near $r=R$), their marked
labels collide. Offset them on **opposite sides** of the point:
```python
ax_e.annotate(f"E = {e:g}", xy=(r, e), xytext=(8, +14), textcoords="offset points", ...)
ax_v.annotate(f"V = {v:g}", xy=(r, v), xytext=(8, -14), textcoords="offset points", ...)
```

## Gotchas (hard-won from 6 figures in this repo)

- **`matplotlib` mathtext has NO `\begin{cases}` / `\dfrac` array layout.**
  Those are LaTeX-only. Stack piecewise lines manually with `\n` and
  `linespacing`. When a line contains a tall fraction (`\dfrac`), add an extra
  blank line (`"\n\n"`) and bump `linespacing` to ~2.0, or the fraction
  collides with the line below. See `src/charged_cylindrical_shell.py` for the
  workaround.
- **mathtext unsupported LaTeX commands** (raise `ParseSyntaxException`):
  `\!` (negative thin space), `\tfrac`, `\textstyle`, `\substack`. Use `\frac`
  (not `\tfrac`), drop `\!`, and `\dfrac` *is* OK in mathtext. If a formula
  throws a parse error, suspect these first.
- **Piecewise at a surface → E jumps.** If your shell/cylinder E curve looks
  smooth across $r=R$, you've silently joined the segments — that's
  physically wrong. Plot inside and outside as separate arrays.
- **Line-charge $V$ goes negative** for $\rho>\rho_0$. Set the V y-axis to
  include negatives, and draw a $V=0$ reference line. Don't clip it to
  $\geq 0$.
- **`twinx()` colour binding**: the left spine stays the left axis's colour,
  the right spine the right axis's. Set both explicitly or the axes look
  uncoloured.
- **3D model panel beside an E/V curve panel**: if the left model panel needs
  3D (e.g. line charge, where E is perpendicular to the wire in 3D), use
  `projection="3d"` and the `Arrow3D` subclass (see `src/infinite_line_charge.py`,
  `src/magnetic_field_loop.py`). The right E/V panel stays 2D.

## Model-panel hints specific to E/V geometries

These are the model-panel conventions that recur across E/V figures (the
general skill covers the rest):

- **2D cross-section** is correct for spherical shell, solid sphere,
  concentric shells, cylindrical shell — E lies in the plane of the section.
- **3D** is needed when E is perpendicular to a line (infinite line charge):
  the wire runs along $z$, E arrows radiate horizontally. A 2D side-view would
  misrepresent the field as parallel to the wire.
- **Arrow length encodes field magnitude**: radial arrows get shorter with
  distance ($\propto 1/r^n$). Inside a conductor/shell interior, draw **no**
  arrows ($E=0$) — optionally mark a few `×` or an "E=0" label.
- **Reference circle**: dashed circle at the reference radius, labelled `ρ` or
  `R`, to anchor the distance variable visually.
- **Inset cylinder** (cylindrical shell only): a small 3D cylinder in the
  corner with an arrow to the main circle clarifies "this is a cross-section".
  See `src/charged_cylindrical_shell.py` lines ~98–126; the arrow direction is
  controlled by an `ANGLE` constant there.

## Reference implementations

Closest match per geometry — copy as a starting point:

| Target geometry | Copy from |
|---|---|
| Point charge | `src/point_charge_field.py` (single shared axis, no twin) |
| Spherical shell | `src/charged_sphere.py` |
| Solid sphere | `src/charged_solid_sphere.py` (note V(0)=3kQ/2R peak) |
| Concentric shells | `src/concentric_shells.py` (3-piece piecewise) |
| Infinite line charge | `src/infinite_line_charge.py` (3D model, V<0 region) |
| Cylindrical shell | `src/charged_cylindrical_shell.py` (2D + cylinder inset) |

To adapt one: swap the **constants block**, the **piecewise arrays in
`draw_curves`**, and the **region boundaries** (vertical lines + labels). The
dual-axis scaffolding, annotation style, and formula-box layout stay the same.
