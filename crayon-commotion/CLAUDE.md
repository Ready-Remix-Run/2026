# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Crayon Commotion is a classroom activity generator, not a typical application: the deliverable teachers care about is the printed PDF/CSV output, and the code exists to compute those. `src/commotion/` is the package; `generate_materials.ipynb` is a thin Colab wrapper around it for non-technical users. Per the README, the package is written to be readable and browsable, not just runnable — teachers may read the source (see [[feedback_code_readability]] in memory: favor clarity over cleverness or premature abstraction here).

## Commands

Install dependencies (no lockfile; `pyproject.toml` only declares build metadata):
```
pip install -r requirements.txt
```

Run the full pipeline end-to-end (loads a sample image, quantizes it, encodes it, writes every artifact to `output/`):
```
PYTHONPATH=src python src/commotion/cli.py
```
`cli.py` is a manual walkthrough script (each `test_*` function exercises one pipeline stage and prints its result), not an argparse CLI despite the module name. `oldcli.py` is an earlier, simpler version of the same walkthrough kept alongside it — prefer `cli.py`.

Run tests (`pyproject.toml` sets `pythonpath = ["src"]` for pytest, so no env var needed):
```
pytest
```
`tests/` currently only contains `__init__.py` — there are no test modules yet. Add `test_*.py` files there; pytest will pick them up automatically given the configured pythonpath.

## Architecture

The package is a linear pipeline, and each stage lives in its own subpackage. `models.py` defines every dataclass used across stages (`Palette`/`PaletteColor`, `ClassroomPlan`/`DimensionOption`, `GridCell`, `EncodedCell`, `Worksheet`, `StudentSheet`) — read it first when tracing how data flows between stages, since most functions just transform one of these into another.

1. **`palettes/loader.py`** — reads a `palettes/*.csv` file (`id,name,r,g,b`) into a `Palette`.
2. **`planning/dimensions.py`** and **`planning/sheets.py`** — given a `ClassroomPlan` (students × sheets × cells), suggest near-square grid dimensions by factoring the total cell count. `dimensions.py` sizes the whole worksheet; `sheets.py` sizes each student's individual mini-page. These two don't know about each other, so a suggested sheet size isn't guaranteed to evenly tile the chosen worksheet size — `cli.py`'s `pick_compatible_sheet_size` shows the pattern for reconciling the two (try each suggestion and its transpose until one divides evenly).
3. **`imaging/resize.py`** — loads a source image and resizes it to the target grid, returning a 2D list of RGB tuples.
4. **`imaging/quantize.py`** — maps every pixel to its nearest `PaletteColor`, using CIE L\*a\*b\* distance (not raw RGB distance) so perceptually similar colors are matched, not just similarly bright ones. Produces the `GridCell` grid.
5. **`imaging/variety.py`** — optional pass that nudges a few cells in any monochrome block to their second-nearest palette color, so no student gets a mini-page of all-identical cells. Opt-in (`ensure_block_variety`); only matters for flat/vector-style source images.
6. **`encoders/`** — `Encoder` (in `encoder.py`) is the abstract base, with one `.encode(cell) -> str` per cell; `decimal.py`, `binary.py`, `rgb_binary.py`, `hexadecimal.py`, `rgb_decimal.py` are the concrete per-cell strategies matching five of the six modes described in the README. `grid.py`'s `encode_grid` applies one `Encoder` across a `GridCell` grid to produce an `EncodedCell` grid. Binary/RGB-based encoders don't use palette ids the same way Decimal does — see `rgb_binary.py`'s docstring and `cli.py`'s `reference_label_fn` for how the reference-chart label changes accordingly. `rgb_decimal.py` inverts the RGB Binary/Hex direction: it gives students decimal and has them produce binary, so its reference-chart label shows each color's binary triple instead of decimal. `run_length.py` is the odd one out: Run Length isn't a per-cell `Encoder` at all (a single cell has no "run length" on its own), so it's a standalone `run_length_encode(cells) -> list[Run]` function that groups one block's cells (already split into a `StudentSheet`, already in reading order) into runs of consecutive identical colors — it runs *after* splitting, not through `encode_grid` like the others. `cli.py`/the notebook route "Run Length" through `DecimalEncoder` as a placeholder just to keep `EncodedCell.value` populated with something; nothing renders that value for this encoding.
7. **`worksheets/builder.py`** — wraps an encoded grid into a `Worksheet` (adds title/palette/encoder metadata). **`worksheets/splitter.py`** then cuts a `Worksheet` into per-student `StudentSheet` blocks of a given size.
8. **`renderers/`** — terminal output stage. `csv_renderer.py` writes a plain encoded grid to CSV. `pdf.py` (reportlab-based) renders the printable artifacts: blank student sheet, per-block encoding instructions (`render_encoding_sheets` for the grid-style encodings, `render_run_length_encoding_sheets` for Run Length's text-list style — the latter takes pre-computed `list[Run]` per sheet rather than calling `run_length_encode` itself, keeping renderers decoupled from encoder logic like every other `render_*` function), the wall-sized color reference chart, and the teacher's cheat sheet (fully colored, tiled across pages with block-boundary labels like "C7").

`export/__init__.py` is currently empty — no code lives there yet.

Sample data used by the pipeline: `images/` (source images), `palettes/crayola24.csv` and `palettes/crayola16.csv` (the two supported palettes).
