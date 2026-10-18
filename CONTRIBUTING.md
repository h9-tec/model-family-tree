# Contributing

Everything except `data/families.yaml` and the code is generated. Do not edit `README.md`, `dist/`, `docs/tables/` or `assets/` by hand; the nightly job overwrites them.

## Fix a family grouping

1. Edit `data/families.yaml`: map a root model id under `roots:` or a series key under `series:` to the family key you want, and add a `display:` name if it is new.
2. `uv run pytest`.
3. Open a PR. CI checks tests and that `dist/` parses; the next nightly build applies your change to the tables.

## Change the pipeline

`modeltree/fetch.py` (dump to tables), `graph.py` (closure), `families.py`, `leaderboard.py`, `export.py` (dist JSON), `render.py` (README and SVG). Run `uv run python scripts/build.py all` to rebuild from the live dump (1.6 GB download, then about 15 seconds).
