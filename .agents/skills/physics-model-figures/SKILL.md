---
name: physics-model-figures
description: Generate physics-textbook figures pairing a conceptual model diagram with the governing function curves (e.g. electric field + potential vs. distance). Use when drawing a physics concept illustration that needs a model/scene panel beside one or more function plots.
---

# Physics Model Figures (model diagram + function curves)

A standard two-panel layout for physics teaching figures: a **conceptual model
diagram** on the left (charges, field lines, vectors, test points) beside a
**function-curve plot** on the right (e.g. $E(r)$, $V(r)$). Side-by-side, equal
or near-equal width, shared visual style.

This skill captures the pattern already implemented in this repo
(`src/point_charge_field.py`, `src/magnetic_field_loop.py`). Reuse that shape
rather than reinventing it.

## When to use

- A physics illustration where a model/scene and one or more quantitative
  curves belong together (field + potential, spring + force/energy curve,
  charge distribution + E/V profile, wave + amplitude, orbit + r(t), …).
- Standalone single-panel model diagrams (see "single-panel variant" below).

Do NOT use for pure data plots (no model diagram) — those are plain matplotlib.

## The recipe

1. **Pick an output preset** from `src/_viz/output.py`. Default per `AGENTS.md`:
   transparent PNG. For textbook serif style use `Presets.PNG_TEXTBOOK`
   (transparent PNG + serif) or `Presets.SVG_TEXTBOOK` (vector).
   ```python
   from _viz.output import Presets
   SPEC = Presets.PNG_TEXTBOOK
   ```
2. **Build a horizontal 2-panel figure** — left = model, right = curves:
   ```python
   fig = SPEC.figure()
   ax_model, ax_curves = fig.subplots(1, 2)
   fig.subplots_adjust(left=0.07, right=0.98, top=0.92, bottom=0.10, wspace=0.18)
   ```
3. **Model panel (`set_aspect("equal")`, `set_axis_off()`)** — draw with
   `matplotlib.patches` (Circle, FancyArrowPatch) and `Line2D`. Draw
   field/force vectors as arrowed line segments; mark test points with small
   white-filled circles; add a small `loc="lower right"` legend built from
   `Line2D` handles.
4. **Curve panel** — plot the governing function(s). Multiple curves that
   share compatible units may share **one** y-axis with a combined label
   (e.g. `"E (N/C)   /   V (V)"`); if units/ scales differ a lot, use a
   secondary axis (`ax.twinx()`). Add light grey grid (`color="#dddddd"`).
5. **Annotations**: marked points as white-filled circles with a short label;
   legend `loc="upper right"` (so it won't cover the falling right tail of a
   $1/r$-type curve); sub-title via `ax.set_title(...)`, **no** `suptitle`.
6. **Save** through the spec so format/padding/transparency stay consistent:
   ```python
   path = SPEC.save(fig, OUT_DIR / "my_figure")
   ```

## Conventions (from AGENTS.md)

- Default output is **transparent-background PNG** unless another format is
  explicitly requested.
- Reuse `Presets.*` from `src/_viz/output.py`; do not hard-code
  `figsize`/`dpi`/`facecolor` in each script.
- All annotation text in **English**; serif fonts for textbook style.
- No inter-panel separator lines, no overall title — only per-panel subtitles.
- Legend entries list the **function/expression only** (e.g. `E = kq/r²`), not
  the numeric constants.

## Single-panel variant

If only a model diagram is needed (no function curves), drop the second panel
and use a `Presets.SVG_DOC`-style square or near-square figure; see
`src/magnetic_field_loop.py` for a 3D example (it adds an `Arrow3D` subclass so
`FancyArrowPatch` renders under matplotlib's 3D projection sort).

## Reference implementation

`src/point_charge_field.py` is the canonical example of the two-panel pattern.
Copy it as a starting point and swap in the target physics:

- the constants block (`K`, `Q`, …)
- `draw_model(ax)` — replace the charge/field-line geometry
- `draw_curves(ax)` — replace the function(s) and y-axis label/range

## Gotchas

- **3D arrows**: `FancyArrowPatch` added to a 3D axes raises
  `'FancyArrowPatch' object has no attribute 'do_3d_projection'` on
  matplotlib ≥ 3.11. Use the `Arrow3D` subclass that calls `proj_transform`
  (see `src/magnetic_field_loop.py`).
- **Legend occlusion**: $1/r^n$ curves fall steeply on the right — keep the
  function legend at `upper right`, not `lower right`.
- **Transparent background** requires `transparent=True` (the presets' default);
  passing `facecolor` overrides transparency and lays down an opaque rectangle.
