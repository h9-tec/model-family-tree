"""MCP server for the Open Model Family Tree: lineage / children / leaderboard / family / search.

Counts come from dist/ (rebuilt nightly). Ancestors and children of arbitrary models come
live from the Hugging Face API, with dist/children_top.json as the offline fallback.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # append: the SDK `mcp` package must win over this repo's mcp/ dir

import requests  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402

DIST = Path(os.environ.get("MODELTREE_DIST") or ROOT / "dist")
HF = "https://huggingface.co/api"
UA = {"user-agent": "model-family-tree-mcp (https://github.com/h9-tec/model-family-tree)"}


def _load(name: str) -> dict:
    return json.loads((DIST / name).read_text())


STATS = _load("stats.json")
LB = _load("leaderboard.json")
PARENTS = _load("parents.json")
CHILDREN = _load("children_top.json")["children"]
COLS = PARENTS["columns"]
ROWS = {r[0]: dict(zip(COLS, r)) for r in PARENTS["rows"]}
ROWS_LOWER = {k.lower(): k for k in ROWS}
FAMILIES = {f["family"]: f for f in LB["families"]}
FAMILIES_BY_DISPLAY = {f["display"].lower(): f for f in LB["families"]}

server = MCPServer("model-family-tree")


def _hf_get(url: str, **params) -> dict | list | None:
    try:
        r = requests.get(url, params=params, headers=UA, timeout=15)
        return r.json() if r.ok else None
    except requests.RequestException:
        return None


def _counts(model_id: str) -> dict:
    row = ROWS.get(model_id) or ROWS.get(ROWS_LOWER.get(model_id.lower(), ""))
    if not row:
        return {"direct": 0, "total": 0, "d90": 0, "note": "no declared descendants in the last dump"}
    return {k: row[k] for k in ("direct", "total", "d90", "finetune", "adapter", "quantized", "merge", "family")}


def _base_models(model_id: str) -> tuple[list[str], str | None]:
    info = _hf_get(f"{HF}/models/{model_id}")
    if not isinstance(info, dict):
        return [], None
    tags = info.get("tags") or []
    rel = next((t.split(":")[1] for t in tags if t.startswith("base_model:") and t.count(":") == 2), None)
    bases = [t.split(":", 2)[-1] for t in tags if t.startswith("base_model:") and t.count(":") == 2]
    if not bases:
        bases = [t.split(":", 1)[1] for t in tags if t.startswith("base_model:") and t.count(":") == 1]
    return list(dict.fromkeys(bases)), rel


@server.tool()
def lineage(id: str, max_depth: int = 12) -> dict:
    """Ancestry of one Hugging Face model: the chain of declared base models up to the root,
    plus how many descendants the model itself has.

    Walks `base_model` metadata live from the Hub (first parent at each step; merges list all
    parents in `parents`). Each hop carries the relation (finetune, adapter, quantized, merge)
    and the parent's descendant counts from the nightly build.

    Example: lineage(id="unsloth/Qwen2.5-7B-Instruct")
    """
    chain, seen, cur = [], set(), id
    for _ in range(max_depth):
        parents, rel = _base_models(cur)
        node = {"id": cur, "relation_to_parent": rel, "parents": parents, **_counts(cur)}
        chain.append(node)
        if not parents or parents[0] in seen:
            break
        seen.add(cur)
        cur = parents[0]
    root = chain[-1]["id"]
    return {"model": id, "root": root, "root_family": _counts(root).get("family"), "chain": chain, "generated_at": STATS["generated_at"]}


@server.tool()
def children(id: str, relation: str | None = None, limit: int = 20, sort: str = "downloads") -> dict:
    """Direct descendants of a model, most downloaded first (or `sort="likes"`).

    `relation` filters to finetune, adapter, quantized or merge. Live from the Hub API;
    falls back to the nightly top-25 list when offline. Example: children(id="Qwen/Qwen3-8B", relation="finetune")
    """
    flt = f"base_model:{relation}:{id}" if relation else f"base_model:{id}"
    live = _hf_get(f"{HF}/models", filter=flt, sort=sort, direction=-1, limit=min(limit, 100))
    if isinstance(live, list):
        rows = [{"id": m["id"], "downloads": m.get("downloads", 0), "likes": m.get("likes", 0), "pipeline": m.get("pipeline_tag"), **{k: v for k, v in _counts(m["id"]).items() if k in ("total", "direct")}} for m in live]
        source = "huggingface api"
    else:
        rows = [{"id": c[0], "downloads": c[1], "total": c[2]} for c in CHILDREN.get(id, [])[:limit]]
        source = "nightly fallback (top 25 by downloads)"
    return {"model": id, **_counts(id), "children": rows, "source": source}


@server.tool()
def leaderboard(kind: str = "all_time", limit: int = 20, offset: int = 0) -> list[dict]:
    """Most-descended base models on the Hub.

    kind: all_time (unique descendants of every kind), 90d (new descendants in the last 90
    days), finetune (finetune descendants only; filters out LoRA and quantization noise),
    families (roots grouped by series across orgs), orgs (by organization owning the roots).
    """
    key = {"all_time": "models_all_time", "90d": "models_90d", "finetune": "models_finetune", "families": "families", "orgs": "orgs"}.get(kind)
    if not key:
        return [{"error": "kind must be one of all_time, 90d, finetune, families, orgs"}]
    rows = LB[key][offset: offset + limit]
    return [{k: v for k, v in r.items() if k not in ("parents",)} for r in rows]


@server.tool()
def family(name: str) -> dict:
    """One model family (e.g. "Qwen2.5", "Llama 3.1", "FLUX.1"): totals, relation breakdown,
    roots, organizations and the top models in it by descendants."""
    f = FAMILIES.get(name) or FAMILIES.get(name.lower()) or FAMILIES_BY_DISPLAY.get(name.lower())
    if not f:
        cands = [x["display"] for x in LB["families"] if name.lower() in x["display"].lower() or name.lower() in x["family"]][:10]
        return {"error": f"unknown family {name!r}", "did_you_mean": cands}
    members = [r for r in LB["models_all_time"] if r.get("family") == f["family"]][:15]
    return {**f, "top_models": [{"id": m["id"], "total": m["total"], "d90": m["d90"]} for m in members]}


@server.tool()
def search(query: str, limit: int = 15) -> list[dict]:
    """Find models with descendants whose id contains the query (case-insensitive), most
    descended first. Covers the 88k models that have at least one declared child."""
    q = query.lower()
    out = []
    for r in PARENTS["rows"]:
        if q in r[0].lower():
            out.append(dict(zip(COLS, r)))
            if len(out) >= limit:
                break
    return out


@server.tool()
def stats() -> dict:
    """Headline numbers for the current build: models tracked, links, parents, roots, families, dates."""
    return STATS


if __name__ == "__main__":
    server.run()
