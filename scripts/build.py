#!/usr/bin/env python3
"""Build pipeline: fetch the Hub dump, compute the tree, write dist/, README and charts.

  python scripts/build.py fetch [--source URL|PATH]   # dump -> .cache/nodes.parquet + edges.parquet
  python scripts/build.py build [--date YYYY-MM-DD]   # cache -> dist/, README.md, assets/, docs/tables/
  python scripts/build.py all   [--source ...]        # both
  python scripts/build.py check                       # dist/ parses and README is in sync with dist/stats.json
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from modeltree import export, fetch, render  # noqa: E402
from modeltree.graph import Graph  # noqa: E402
from modeltree.leaderboard import build_leaderboards  # noqa: E402

CACHE = ROOT / ".cache"


def _today(date: str | None) -> tuple[str, int]:
    d = dt.date.fromisoformat(date) if date else dt.date.today()
    return d.isoformat(), int(np.datetime64(d.isoformat()).astype("datetime64[D]").astype(int))


def cmd_fetch(source: str) -> int:
    t = time.time()
    nodes, edges = fetch.fetch(source, CACHE)
    (CACHE / "source_date.txt").write_text(dt.date.today().isoformat())
    print(f"fetched {nodes.height:,} models, {edges.height:,} edges in {time.time() - t:.0f}s")
    return 0


def cmd_build(date: str | None) -> int:
    date_s, today = _today(date)
    t = time.time()
    nodes, edges = fetch.load_cached(CACHE)
    source_date = (CACHE / "source_date.txt").read_text().strip() if (CACHE / "source_date.txt").exists() else date_s
    g = Graph.build(nodes, edges)
    g.compute(today, keep_sets_for=set(g.roots().tolist()))
    lb = build_leaderboards(g, nodes, today)
    export.write_dist(lb, g, ROOT / "dist", date_s, source_date)
    stats = json.loads((ROOT / "dist" / "stats.json").read_text())
    (ROOT / "assets").mkdir(exist_ok=True)
    (ROOT / "assets" / "families.svg").write_text(render.cumulative_chart(lb["timeseries"], lb["families"]))
    (ROOT / "assets" / "monthly.svg").write_text(render.monthly_chart(lb["timeseries"], lb["families"]))
    render.write_tables(lb, ROOT / "docs" / "tables")
    (ROOT / "README.md").write_text(render.readme(lb, stats, date_s))
    print(f"built: {stats['models']:,} models, {stats['edges']:,} edges, {stats['parents']:,} parents, {stats['families']:,} families in {time.time() - t:.0f}s")
    return 0


def cmd_check() -> int:
    errors = []
    for f in ("stats.json", "leaderboard.json", "timeseries.json", "parents.json", "children_top.json"):
        p = ROOT / "dist" / f
        if not p.exists():
            errors.append(f"missing dist/{f}")
            continue
        try:
            json.loads(p.read_text())
        except json.JSONDecodeError as e:
            errors.append(f"dist/{f}: {e}")
    stats = json.loads((ROOT / "dist" / "stats.json").read_text()) if not errors else {}
    readme = (ROOT / "README.md").read_text() if (ROOT / "README.md").exists() else ""
    if stats and f"*Generated {stats['generated_at']}.*" not in readme:
        errors.append("README.md generated date does not match dist/stats.json")
    for e in errors:
        print("error:", e)
    print("ok" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["fetch", "build", "all", "check"])
    ap.add_argument("--source", default=fetch.DUMP_URL)
    ap.add_argument("--date")
    a = ap.parse_args(argv)
    if a.cmd == "fetch":
        return cmd_fetch(a.source)
    if a.cmd == "build":
        return cmd_build(a.date)
    if a.cmd == "all":
        return cmd_fetch(a.source) or cmd_build(a.date)
    return cmd_check()


if __name__ == "__main__":
    raise SystemExit(main())
