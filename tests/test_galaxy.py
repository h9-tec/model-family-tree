import numpy as np
import polars as pl

from modeltree.galaxy import layout, pack_siblings
from modeltree.graph import Graph


def test_pack_siblings_no_overlap():
    rng = np.random.default_rng(0)
    r = np.sort(rng.uniform(1, 20, 300))[::-1]
    x, y, R = pack_siblings(r)
    d = np.hypot(x[:, None] - x[None, :], y[:, None] - y[None, :])
    rs = r[:, None] + r[None, :]
    np.fill_diagonal(d, np.inf)
    assert (d >= rs - 1e-6).all()
    assert (np.hypot(x, y) + r <= R + 1e-6).all()


def test_layout_covers_every_connected_node():
    edges = [("b", "a", "finetune"), ("c", "a", "adapter"), ("d", "b", "quantized"), ("y", "x", "finetune"), ("m", "a", "merge"), ("m", "x", "merge")]
    ids = sorted({e for ed in edges for e in ed[:2]} | {"lonely"})
    nodes = pl.DataFrame({"id": ids, "created": [None] * len(ids)}).with_columns(pl.col("created").cast(pl.Datetime("us")))
    g = Graph.build(nodes, pl.DataFrame(edges, schema=["child", "parent", "relation"], orient="row"))
    g.compute(20_000, keep_sets_for=set(g.roots().tolist()))
    lay = layout(g, {g.index["a"]: "fam-a", g.index["x"]: "fam-x"}, {}, np.ones(len(ids)))
    seen = {g.ids[i] for i in lay["idx"].tolist()}
    assert seen == set(ids) - {"lonely"}
    assert len(lay["x"]) == len(seen) == 7  # m counted once, under its first root
    assert {f["k"] for f in lay["families"]} == {"fam-a", "fam-x"}
