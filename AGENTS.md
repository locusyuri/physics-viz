# AGENTS.md

Conventions for this repository. Follow these unless explicitly told otherwise.

## Image output

- When generating physics model figures, default to **transparent-background PNG**.
  Other formats (SVG/PDF) only when explicitly requested.
- Reuse the shared output presets in `src/_viz/output.py` (`Presets.*`) rather
  than hard-coding `figsize` / `dpi` / `facecolor` in each model script.
- Annotations use English text. Default to serif fonts for textbook-style figures.
