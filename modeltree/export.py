"""Write dist/*: the JSON the site, the MCP server and other agents read."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .graph import Graph
from .leaderboard import Meta


def _dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_dist(lb: dict, g: Graph, out: Path, date: str, source_date: str) -> None:
    out.mkdir(parents=True, exist_ok=True)
    stats = {"generated_at": date, "source_date": source_date, **lb["stats"]}
    _dump(out / "stats.json", stats)
    _dump(out / "leaderboard.json", {
        "generated_at": date,
        "models_all_time": lb["models_all_time"],
        "models_90d": lb["models_90d"],
        "models_finetune": lb["models_finetune"],
        "families": lb["families"],
        "orgs": lb["orgs"],
    })
    _dump(out / "timeseries.json", {"generated_at": date, **lb["timeseries"]})

    # Every model that has at least one declared child: compact columnar table.
    idx = np.flatnonzero(g.desc_total > 0)
    order = idx[np.argsort(-g.desc_total[idx], kind="stable")]
    rf = lb["root_family"]
    _dump(out / "parents.json", {
        "generated_at": date,
        "columns": ["id", "direct", "total", "d90", "finetune", "adapter", "quantized", "merge", "family"],
        "rows": [
            [g.ids[v], len(g.children[v]), int(g.desc_total[v]), int(g.desc_90d[v]),
             int(g.desc_by_rel[v][0]), int(g.desc_by_rel[v][1]), int(g.desc_by_rel[v][2]), int(g.desc_by_rel[v][3]),
             rf.get(int(v), "")]
            for v in order
        ],
    })

    # Top children (by downloads) for the most-descended parents: offline fallback for the explorer and MCP.
    meta: Meta = lb["meta"]
    children = {}
    for v in order[:3000]:
        kids = [c for c in g.children[v] if not g.is_ghost(c)]
        kids.sort(key=lambda c: -int(meta.downloads[c]))
        children[g.ids[int(v)]] = [[g.ids[c], int(meta.downloads[c]), int(g.desc_total[c])] for c in kids[:25]]
    _dump(out / "children_top.json", {"generated_at": date, "children": children})

    (out / "llms.txt").write_text(_llms_txt(lb, stats))


def _llms_txt(lb: dict, stats: dict) -> str:
    lines = [
        "# Open Model Family Tree",
        "",
        f"> The ancestry of every model on the Hugging Face Hub, rebuilt nightly from declared base_model metadata. Generated {stats['generated_at']} from the {stats['source_date']} Hub dump.",
        "",
        f"- {stats['models']:,} models tracked, {stats['with_ancestry']:,} declare a base model, {stats['edges']:,} parent links, {stats['parents']:,} models have descendants.",
        "- Counts are unique descendants (finetunes, adapters, quantizations, merges), each counted once.",
        "",
        "## Most-descended base models (all time)",
    ]
    for i, m in enumerate(lb["models_all_time"][:25], 1):
        lines.append(f"{i}. {m['id']}: {m['total']:,} descendants ({m['d90']:,} in the last 90 days)")
    lines += ["", "## Families"]
    for i, f in enumerate(lb["families"][:15], 1):
        lines.append(f"{i}. {f['display']}: {f['total']:,} descendants across {f['n_roots']} roots")
    lines += ["", "## Files", "- dist/leaderboard.json: top 500 models (all time, 90 days, finetune-only), families, orgs",
              "- dist/parents.json: every model with descendants, compact columns", "- dist/timeseries.json: monthly new descendants, top families and models", ""]
    return "\n".join(lines)
