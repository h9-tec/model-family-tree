"""Pull the Hub model dump and reduce it to two compact tables: nodes and edges.

Source: the daily `cfahlgren1/hub-stats` dataset (Apache-2.0), a parquet dump of
`/api/models` with the `baseModels` field every model card declares. Reading it with
polars over HTTPS pushes the column projection down to range requests, so a build
never needs the whole 1.6 GB file unless it is cached locally.
"""

from __future__ import annotations

import re
from pathlib import Path

import polars as pl

DUMP_URL = "https://huggingface.co/datasets/cfahlgren1/hub-stats/resolve/main/models.parquet"
RELATIONS = ("finetune", "adapter", "quantized", "merge")
_ID_RE = re.compile(r"^[A-Za-z0-9][\w.-]*/[\w.-]+$")
# A few repos are named after what look like leaked access tokens. GitHub push protection
# rejects any file carrying them, so they are dropped at ingest.
_SECRET_RE = r"(hf_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{30,}|ghp_[A-Za-z0-9]{30,})"

COLUMNS = [
    "id", "author", "createdAt", "lastModified", "downloads", "downloadsAllTime",
    "likes", "pipeline_tag", "library_name", "trendingScore", "baseModels", "tags",
]


def parse_tag(tag: str) -> tuple[str, str] | None:
    """`base_model:finetune:org/name` -> (org/name, finetune); `base_model:org/name` -> (.., unknown)."""
    if not tag.startswith("base_model:"):
        return None
    rest = tag[len("base_model:"):]
    rel = "unknown"
    for r in RELATIONS:
        if rest.startswith(r + ":"):
            rel, rest = r, rest[len(r) + 1:]
            break
    return (rest, rel) if _ID_RE.match(rest) else None


def load_raw(source: str | Path = DUMP_URL) -> pl.DataFrame:
    return pl.scan_parquet(str(source)).select(COLUMNS).collect()


def extract(raw: pl.DataFrame) -> tuple[pl.DataFrame, pl.DataFrame]:
    """Return (nodes, edges). Edges are child -> parent with the declared relation."""
    raw = raw.filter(~pl.col("id").str.contains(_SECRET_RE))
    nodes = raw.select(
        pl.col("id"),
        pl.col("author"),
        pl.col("createdAt").alias("created"),
        pl.col("lastModified").alias("modified"),
        pl.col("downloads").fill_null(0),
        pl.col("downloadsAllTime").fill_null(0).alias("downloads_all"),
        pl.col("likes").fill_null(0),
        pl.col("pipeline_tag").alias("pipeline"),
        pl.col("library_name").alias("library"),
        pl.col("trendingScore").fill_null(0.0).alias("trending"),
    )

    declared = (
        raw.filter(pl.col("baseModels").is_not_null())
        .select(
            child=pl.col("id"),
            relation=pl.col("baseModels").struct.field("relation"),
            parent=pl.col("baseModels").struct.field("models").list.eval(pl.element().struct.field("id")),
        )
        .explode("parent")
        .filter(pl.col("parent").is_not_null())
    )

    # Older cards carry only `base_model:` tags; parse those as a fallback.
    tagged = (
        raw.filter(pl.col("baseModels").is_null())
        .select(child=pl.col("id"), tag=pl.col("tags").list.eval(pl.element().filter(pl.element().str.starts_with("base_model:"))))
        .explode("tag")
        .filter(pl.col("tag").is_not_null())
    )
    parsed = [(c, *p) for c, t in zip(tagged["child"], tagged["tag"]) if (p := parse_tag(t))]
    fallback = pl.DataFrame(parsed, schema=["child", "parent", "relation"], orient="row") if parsed else declared.clear()

    edges = (
        pl.concat([declared.select("child", "parent", "relation"), fallback.select("child", "parent", "relation")])
        .filter(pl.col("child") != pl.col("parent"))
        .filter(~pl.col("parent").str.contains(_SECRET_RE))
        .unique(subset=["child", "parent"], keep="first")
    )
    return nodes, edges


def fetch(source: str | Path = DUMP_URL, cache: Path = Path(".cache")) -> tuple[pl.DataFrame, pl.DataFrame]:
    cache.mkdir(parents=True, exist_ok=True)
    nodes, edges = extract(load_raw(source))
    nodes.write_parquet(cache / "nodes.parquet")
    edges.write_parquet(cache / "edges.parquet")
    return nodes, edges


def load_cached(cache: Path = Path(".cache")) -> tuple[pl.DataFrame, pl.DataFrame]:
    return pl.read_parquet(cache / "nodes.parquet"), pl.read_parquet(cache / "edges.parquet")
