# physics-viz

Physics textbook illustrations — matplotlib scripts that generate vector/raster figures for classical electromagnetism topics.

## Quick start

```bash
# Install dependencies (matplotlib)
uv sync

# Generate a figure (transparent PNG to output/)
uv run python src/point_charge_field.py
uv run python src/magnetic_field_loop.py
```

Output goes to `output/`.

## Project structure

```
src/
├── _viz/
│   ├── __init__.py
│   └── output.py          # OutputSpec + Presets (shared render config)
├── magnetic_field_loop.py  # 3D: B-field on the axis of a circular current loop
└── point_charge_field.py   # 2-panel: point charge model + E(r)/V(r) curves
.agents/skills/
└── physics-model-figures/  # Skill: "model diagram + function curves" pattern
output/                      # Generated figures (git-ignored)
```

## Output presets

`src/_viz/output.py` defines reusable render profiles so each model script doesn't hard-code figure size, DPI, or format:

| Preset | Format | Size | Font | Use |
|---|---|---|---|---|
| `PNG_TEXTBOOK` | PNG (transparent) | 14×7 | Serif | Default for textbook figures |
| `SVG_TEXTBOOK` | SVG (transparent) | 12×12 | Serif | Vector for documents |
| `SVG_DOC` | SVG (transparent) | 9.5×9 | Default | General-purpose vector |
| `PNG_PRINT` | PNG | 9.5×9 | Default | 300 dpi print |
| `PNG_WEB` | PNG | 8×8 | Default | 150 dpi web |

Usage in a model script:

```python
from _viz.output import Presets

SPEC = Presets.PNG_TEXTBOOK
fig = SPEC.figure()
# ... draw ...
SPEC.save(fig, "output/my_figure")
```

## Figures

### Magnetic Field on the Axis of a Circular Loop

3D illustration of a current-carrying loop in the xy-plane with the magnetic field **B** at point P on the z-axis. Field-line rings drawn around the wire; hidden portions rendered dashed.

```
uv run python src/magnetic_field_loop.py
```

### Electric Field and Potential of a Point Charge

Two-panel figure: left panel shows +q with 12 radial field lines and test points P1, P2; right panel plots E = kq/r² (blue) and V = kq/r (green) on a shared axis.

```
uv run python src/point_charge_field.py
```

## Conventions

See [`AGENTS.md`](./AGENTS.md) for the full list. Key points:

- **Transparent PNG** by default; SVG/PDF only on request.
- Reuse `Presets.*` — don't hard-code render settings per script.
- English annotations; serif fonts for textbook style.
- No inter-panel separator lines; per-panel subtitles only, no overall title.
