"""End-to-end on a synthetic dump: extract -> graph -> leaderboards -> dist -> README."""

import datetime as dt
import json

import numpy as np
import polars as pl

from modeltree import export, fetch, render
from modeltree.graph import Graph
from modeltree.leaderboard import build_leaderboards

ROWS = [
    # id, author, created, baseModels(relation, [parents]), tags
    ("Qwen/Qwen2.5-7B", "Qwen", "2024-09-15", None, []),
    ("Qwen/Qwen2.5-7B-Instruct", "Qwen", "2024-09-16", ("finetune", ["Qwen/Qwen2.5-7B"]), []),
    ("unsloth/Qwen2.5-7B-Instruct", "unsloth", "2024-09-20", ("finetune", ["Qwen/Qwen2.5-7B-Instruct"]), []),
    ("someone/qwen-lora", "someone", "2026-10-01", ("adapter", ["Qwen/Qwen2.5-7B-Instruct"]), []),
    ("someone/qwen-q4", "someone", "2026-09-01", ("quantized", ["unsloth/Qwen2.5-7B-Instruct"]), []),
    ("meta-llama/Llama-3.1-8B", "meta-llama", "2024-07-23", None, []),
    ("merger/qwen-llama-merge", "merger", "2025-01-01", ("merge", ["Qwen/Qwen2.5-7B", "meta-llama/Llama-3.1-8B"]), []),
    ("legacy/old-finetune", "legacy", "2023-05-05", None, ["base_model:gone/base-model", "other"]),
    ("loner/no-parents", "loner", "2026-01-01", None, []),
]


def raw_df() -> pl.DataFrame:
    def bm(x):
        return None if x is None else {"relation": x[0], "models": [{"_id": "x", "id": p} for p in x[1]]}
    df = pl.DataFrame({
        "id": [r[0] for r in ROWS], "author": [r[1] for r in ROWS],
        "createdAt": [dt.datetime.fromisoformat(r[2]) for r in ROWS], "lastModified": [dt.datetime(2026, 10, 1)] * len(ROWS),
        "downloads": list(range(len(ROWS))), "downloadsAllTime": list(range(len(ROWS))), "likes": [1] * len(ROWS),
        "pipeline_tag": ["text-generation"] * len(ROWS), "library_name": ["transformers"] * len(ROWS), "trendingScore": [0.0] * len(ROWS),
        "baseModels": [bm(r[3]) for r in ROWS], "tags": [r[4] for r in ROWS],
    }, strict=False)
    return df.with_columns(pl.col("baseModels").cast(pl.Struct({"relation": pl.String, "models": pl.List(pl.Struct({"_id": pl.String, "id": pl.String}))})))


def test_pipeline(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # families.yaml absent -> no overrides
    nodes, edges = fetch.extract(raw_df())
    assert edges.height == 7  # 5 declared + 2 merge parents... : instruct, unsloth, lora, q4, merge x2, legacy tag
    g = Graph.build(nodes, edges)
    today = int(np.datetime64("2026-10-18").astype("datetime64[D]").astype(int))
    g.compute(today, keep_sets_for=set(g.roots().tolist()))
    lb = build_leaderboards(g, nodes, today)
    top = lb["models_all_time"][0]
    assert top["id"] == "Qwen/Qwen2.5-7B" and top["total"] == 5  # instruct, unsloth, lora, q4, merge
    assert top["by_rel"] == {"finetune": 2, "adapter": 1, "quantized": 1, "merge": 1}
    assert top["d90"] == 2  # lora (Oct 1) and q4 (Sep 1) are within 90 days of Oct 18
    assert lb["models_90d"][0]["id"] in ("Qwen/Qwen2.5-7B", "Qwen/Qwen2.5-7B-Instruct")
    fams = {f["family"]: f for f in lb["families"]}
    assert fams["qwen2.5"]["total"] == 5 and fams["llama-3.1"]["total"] == 1
    ghost = next(m for m in lb["models_all_time"] if m["id"] == "gone/base-model")
    assert ghost["ghost"] and ghost["total"] == 1
    assert lb["stats"]["roots"] == 3 and lb["stats"]["ghost_parents"] == 1
    # family inherited by a non-root parent
    inst = next(m for m in lb["models_all_time"] if m["id"] == "Qwen/Qwen2.5-7B-Instruct")
    assert inst["family"] == "qwen2.5"

    out = tmp_path / "dist"
    export.write_dist(lb, g, out, "2026-10-18", "2026-10-17")
    stats = json.loads((out / "stats.json").read_text())
    parents = json.loads((out / "parents.json").read_text())
    assert parents["rows"][0][0] == "Qwen/Qwen2.5-7B" and len(parents["rows"]) == stats["parents"] == 5
    kids = json.loads((out / "children_top.json").read_text())["children"]
    assert [k[0] for k in kids["Qwen/Qwen2.5-7B"]] == ["merger/qwen-llama-merge", "Qwen/Qwen2.5-7B-Instruct"]  # by downloads desc
    md = render.readme(lb, stats, "2026-10-18")
    assert "Qwen/Qwen2.5-7B" in md and "*Generated 2026-10-18.*" in md
    svg = render.cumulative_chart(lb["timeseries"], lb["families"])
    assert svg.startswith("<svg") and "polyline" in svg
