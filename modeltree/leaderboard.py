"""Turn a computed Graph into leaderboard records: models, families, organizations, time series."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import numpy as np
import polars as pl

from .families import family_of, load_overrides, series_of
from .fetch import RELATIONS
from .graph import Graph, N_REL

REL_NAMES = list(RELATIONS) + ["unknown"]
DISPLAY: dict[str, str] = {}


@dataclass
class Meta:
    """Column arrays for real nodes, indexed by graph index."""
    author: list[str]
    downloads: np.ndarray
    downloads_all: np.ndarray
    likes: np.ndarray
    created: list[str | None]
    pipeline: list[str | None]
    library: list[str | None]

    @classmethod
    def from_nodes(cls, nodes: pl.DataFrame) -> "Meta":
        return cls(
            author=nodes["author"].to_list(),
            downloads=nodes["downloads"].to_numpy(),
            downloads_all=nodes["downloads_all"].to_numpy(),
            likes=nodes["likes"].to_numpy(),
            created=nodes["created"].dt.strftime("%Y-%m-%d").to_list(),
            pipeline=nodes["pipeline"].to_list(),
            library=nodes["library"].to_list(),
        )


def _by_rel(row: np.ndarray) -> dict[str, int]:
    return {name: int(row[i]) for i, name in enumerate(REL_NAMES) if name != "unknown" or row[i]}


def model_record(g: Graph, meta: Meta, v: int, fam: dict[int, str] | None = None) -> dict:
    real = not g.is_ghost(v)
    rec = {
        "id": g.ids[v],
        "author": g.ids[v].split("/")[0],
        "ghost": not real,
        "root": not g.parents[v],
        "direct": len(g.children[v]),
        "total": int(g.desc_total[v]),
        "by_rel": _by_rel(g.desc_by_rel[v]),
        "d30": int(g.desc_30d[v]),
        "d90": int(g.desc_90d[v]),
        "depth": int(g.depth[v]),
        "parents": [g.ids[p] for p in g.parents[v][:4]],
    }
    if real:
        rec.update(
            downloads=int(meta.downloads[v]),
            downloads_all=int(meta.downloads_all[v]),
            likes=int(meta.likes[v]),
            created=meta.created[v],
            pipeline=meta.pipeline[v],
            library=meta.library[v],
        )
    if fam is not None and v in fam:
        rec["family"] = fam[v]
        rec["family_display"] = DISPLAY.get(fam[v], fam[v])
    return rec


def assign_families(g: Graph, overrides: dict) -> tuple[dict[int, str], dict[str, list[int]]]:
    """node index -> family key (for every node with descendants), and family key -> root indices.

    A root's family comes from its own name; any other parent inherits the family of the
    root reached by following first parents, so `Llama-3.1-8B-Instruct` sits under Llama 3.1.
    """
    node_fam: dict[int, str] = {}
    fam_roots: dict[str, list[int]] = {}
    for r in g.roots().tolist():
        f = family_of(g.ids[r], overrides)
        node_fam[r] = f
        fam_roots.setdefault(f, []).append(r)
    for v in np.flatnonzero(g.desc_total > 0).tolist():
        if v in node_fam:
            continue
        chain, x = [v], v
        while g.parents[x] and x not in node_fam and len(chain) < 64:
            x = g.parents[x][0]
            if x in chain:
                break
            chain.append(x)
        f = node_fam.get(x, family_of(g.ids[x], overrides))
        for c in chain:
            node_fam[c] = f
    return node_fam, fam_roots


def _union(g: Graph, roots: list[int]) -> np.ndarray:
    parts = [g.descendants(r) for r in roots]
    parts = [p for p in parts if len(p)]
    if not parts:
        return np.zeros(0, dtype=np.int64)
    return np.unique(np.concatenate(parts)) if len(parts) > 1 else parts[0]


def _group_stats(g: Graph, members: np.ndarray, today: int) -> dict:
    cd = g.created_day[members]
    return {
        "total": int(len(members)),
        "by_rel": _by_rel(np.bincount(g.node_rel[members], minlength=N_REL)) if len(members) else {},
        "d30": int((cd >= today - 30).sum()),
        "d90": int((cd >= today - 90).sum()),
    }


def family_records(g: Graph, meta: Meta, fam_roots: dict[str, list[int]], overrides: dict, today: int, top: int = 300) -> list[dict]:
    display = overrides.get("display", {})
    # cheap upper bound first, exact union only for candidates
    cand = sorted(fam_roots.items(), key=lambda kv: -sum(int(g.desc_total[r]) for r in kv[1]))[: top * 3]
    out = []
    for key, roots in cand:
        members = _union(g, roots)
        if not len(members):
            continue
        st = _group_stats(g, members, today)
        roots_sorted = sorted(roots, key=lambda r: -int(g.desc_total[r]))
        orgs = Counter()
        for r in roots:
            orgs[g.ids[r].split("/")[0]] += int(g.desc_total[r])
        out.append({
            "family": key,
            "display": display.get(key, key),
            **st,
            "n_roots": len(roots),
            "roots": [{"id": g.ids[r], "total": int(g.desc_total[r])} for r in roots_sorted[:5]],
            "orgs": [o for o, _ in orgs.most_common(3)],
            "_members": members,
        })
    out.sort(key=lambda x: -x["total"])
    return out[:top]


def org_records(g: Graph, today: int, top: int = 150) -> list[dict]:
    by_org: dict[str, list[int]] = {}
    for r in g.roots().tolist():
        by_org.setdefault(g.ids[r].split("/")[0], []).append(r)
    cand = sorted(by_org.items(), key=lambda kv: -sum(int(g.desc_total[r]) for r in kv[1]))[: top * 3]
    out = []
    for org, roots in cand:
        members = _union(g, roots)
        if not len(members):
            continue
        st = _group_stats(g, members, today)
        roots_sorted = sorted(roots, key=lambda r: -int(g.desc_total[r]))
        out.append({"org": org, **st, "n_roots": len(roots), "roots": [{"id": g.ids[r], "total": int(g.desc_total[r])} for r in roots_sorted[:5]]})
    out.sort(key=lambda x: -x["total"])
    return out[:top]


def monthly_series(g: Graph, members: np.ndarray, months: list[str]) -> list[int]:
    cd = g.created_day[members]
    cd = cd[cd >= 0]
    m = cd.astype("datetime64[D]").astype("datetime64[M]").astype(str)
    c = Counter(m.tolist())
    return [c.get(mo, 0) for mo in months]


def month_axis(today: int, n: int = 36) -> list[str]:
    last = np.datetime64(int(today), "D").astype("datetime64[M]")
    return [str(last - np.timedelta64(i, "M")) for i in range(n - 1, -1, -1)]


def build_leaderboards(g: Graph, nodes: pl.DataFrame, today: int, top_models: int = 500) -> dict:
    meta = Meta.from_nodes(nodes)
    overrides = load_overrides()
    DISPLAY.clear()
    DISPLAY.update(overrides.get("display", {}))
    root_fam, fam_roots = assign_families(g, overrides)
    months = month_axis(today)

    def top_by(score: np.ndarray, n: int) -> list[dict]:
        idx = np.argsort(-score, kind="stable")[:n]
        return [model_record(g, meta, int(v), root_fam) for v in idx if score[v] > 0]

    fams = family_records(g, meta, fam_roots, overrides, today)
    series = {
        "months": months,
        "families": {f["family"]: monthly_series(g, f["_members"], months) for f in fams[:12]},
    }
    top_models_all = top_by(g.desc_total, top_models)
    series["models"] = {rec["id"]: monthly_series(g, g.descendants(g.index[rec["id"]]), months) for rec in top_models_all[:20]}
    for f in fams:
        f.pop("_members", None)

    n_parents = int((g.desc_total > 0).sum())
    rel_counts = Counter(g.node_rel[g.node_rel < N_REL - 1].tolist())
    stats = {
        "models": g.n_real,
        "with_ancestry": int((g.node_rel < N_REL - 1).sum()),
        "edges": sum(len(c) for c in g.children),
        "parents": n_parents,
        "connected": int(sum(1 for v in range(len(g.ids)) if g.parents[v] or g.children[v])),
        "roots": int(len(g.roots())),
        "ghost_parents": len(g.ids) - g.n_real,
        "cyclic_nodes": len(g.cyclic),
        "families": len(fam_roots),
        "by_rel": {REL_NAMES[k]: v for k, v in sorted(rel_counts.items())},
    }
    return {
        "stats": stats,
        "models_all_time": top_models_all,
        "models_90d": top_by(g.desc_90d, top_models),
        "models_finetune": top_by(g.desc_by_rel[:, 0], top_models),
        "families": fams,
        "orgs": org_records(g, today),
        "timeseries": series,
        "meta": meta,
        "root_family": root_fam,
    }
