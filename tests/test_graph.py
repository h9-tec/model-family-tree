import numpy as np
import polars as pl

from modeltree.families import series_of
from modeltree.fetch import parse_tag
from modeltree.graph import Graph

TODAY = 20_000


def mk(edges, nodes=None):
    ids = sorted({x for e in edges for x in e[:2]} | set(nodes or []))
    nodes_df = pl.DataFrame({"id": ids, "created": [None] * len(ids)}).with_columns(pl.col("created").cast(pl.Datetime("us")))
    edges_df = pl.DataFrame(edges, schema=["child", "parent", "relation"], orient="row")
    g = Graph.build(nodes_df, edges_df)
    g.compute(TODAY)
    return g


def test_chain_counts_unique_descendants():
    g = mk([("b", "a", "finetune"), ("c", "b", "quantized"), ("d", "b", "adapter")])
    a = g.index["a"]
    assert g.desc_total[a] == 3
    assert g.desc_total[g.index["b"]] == 2
    assert g.depth[a] == 2
    assert list(g.desc_by_rel[a][:3]) == [1, 1, 1]


def test_merge_counted_once():
    g = mk([("m", "a", "merge"), ("m", "b", "merge"), ("x", "m", "finetune"), ("b", "a", "finetune")])
    a = g.index["a"]
    assert g.desc_total[a] == 3  # b, m, x — m reached twice, counted once


def test_cycle_does_not_hang():
    g = mk([("b", "a", "finetune"), ("a", "b", "finetune"), ("c", "b", "finetune")])
    assert g.desc_total[g.index["a"]] == 2
    assert g.cyclic


def test_ghost_parent_becomes_root():
    nodes = pl.DataFrame({"id": ["x"], "created": [None]}).with_columns(pl.col("created").cast(pl.Datetime("us")))
    g = Graph.build(nodes, pl.DataFrame([("x", "gone/base", "finetune")], schema=["child", "parent", "relation"], orient="row"))
    g.compute(TODAY)
    v = g.index["gone/base"]
    assert g.is_ghost(v) and g.desc_total[v] == 1 and v in set(g.roots().tolist())


def test_ancestor_chains():
    g = mk([("m", "a", "merge"), ("m", "b", "merge"), ("x", "m", "finetune")])
    chains = g.ancestors(g.index["x"])
    assert sorted(g.ids[c[-1]] for c in chains) == ["a", "b"]


def test_series():
    assert series_of("Qwen/Qwen2.5-7B-Instruct") == "qwen2.5"
    assert series_of("google/gemma-2-9b-it") == "gemma-2"
    assert series_of("google/gemma-2b") == "gemma"
    assert series_of("black-forest-labs/FLUX.1-dev") == "flux.1"
    assert series_of("meta-llama/Llama-3.1-8B") == "llama-3.1"
    assert series_of("stabilityai/stable-diffusion-xl-base-1.0") == "stable-diffusion"
    assert series_of("Qwen/Qwen2.5-Coder-7B") == "qwen2.5-coder"
    assert series_of("openai/whisper-large-v3") == "whisper"
    assert series_of("distilbert/distilbert-base-uncased") == "distilbert"


def test_parse_tag():
    assert parse_tag("base_model:finetune:org/name") == ("org/name", "finetune")
    assert parse_tag("base_model:org/name") == ("org/name", "unknown")
    assert parse_tag("base_model:adapter:D:\\work\\x") is None


def test_token_shaped_ids_dropped():
    from modeltree.fetch import extract
    import datetime as dt
    raw = pl.DataFrame({
        "id": ["ok/model", "leak/hf_" + "a" * 34], "author": ["ok", "leak"],
        "createdAt": [dt.datetime(2026, 1, 1)] * 2, "lastModified": [dt.datetime(2026, 1, 1)] * 2,
        "downloads": [1, 1], "downloadsAllTime": [1, 1], "likes": [0, 0], "pipeline_tag": ["x", "x"],
        "library_name": ["x", "x"], "trendingScore": [0.0, 0.0],
        "baseModels": [None, {"relation": "finetune", "models": [{"_id": "x", "id": "ok/model"}]}], "tags": [["a"], ["a"]],
    }, strict=False)
    nodes, edges = extract(raw)
    assert nodes["id"].to_list() == ["ok/model"] and edges.height == 0
