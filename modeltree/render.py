"""Render README.md, docs/tables/*.md and the SVG charts from the leaderboard dict."""

from __future__ import annotations

from pathlib import Path

REPO = "h9-tec/model-family-tree"
SITE = "https://h9-tec.github.io/model-family-tree/"
PALETTE = ["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2", "#FF9DA6", "#9D755D"]


def hf(mid: str) -> str:
    return f"[{mid}](https://huggingface.co/{mid})"


def n(x: int) -> str:
    return f"{x:,}"


def _rel_cell(by_rel: dict) -> str:
    return " / ".join(n(by_rel.get(k, 0)) for k in ("finetune", "adapter", "quantized", "merge"))


def models_table(rows: list[dict], score_key: str = "total", limit: int | None = None, start: int = 1) -> str:
    head = "| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |\n|---:|---|---:|---:|---:|---|---|\n"
    body = []
    for i, m in enumerate(rows[:limit] if limit else rows, start):
        name = hf(m["id"]) + (" †" if m["ghost"] else "")
        fam = m.get("family_display", m.get("family", ""))
        body.append(f"| {i} | {name} | {n(m['total'])} | {n(m['direct'])} | {n(m['d90'])} | {_rel_cell(m['by_rel'])} | {fam} |")
    return head + "\n".join(body) + "\n"


def families_table(rows: list[dict], limit: int | None = None) -> str:
    head = "| # | Family | Descendants | Last 90d | Roots | Finetune / adapter / quantized / merge | Biggest root |\n|---:|---|---:|---:|---:|---|---|\n"
    body = []
    for i, f in enumerate(rows[:limit] if limit else rows, 1):
        top = f["roots"][0]["id"] if f["roots"] else ""
        body.append(f"| {i} | **{f['display']}** | {n(f['total'])} | {n(f['d90'])} | {n(f['n_roots'])} | {_rel_cell(f['by_rel'])} | {hf(top) if top else ''} |")
    return head + "\n".join(body) + "\n"


def orgs_table(rows: list[dict], limit: int | None = None) -> str:
    head = "| # | Organization | Descendants of its roots | Last 90d | Roots | Biggest root |\n|---:|---|---:|---:|---:|---|\n"
    body = []
    for i, o in enumerate(rows[:limit] if limit else rows, 1):
        top = o["roots"][0]["id"] if o["roots"] else ""
        body.append(f"| {i} | [{o['org']}](https://huggingface.co/{o['org']}) | {n(o['total'])} | {n(o['d90'])} | {n(o['n_roots'])} | {hf(top) if top else ''} |")
    return head + "\n".join(body) + "\n"


# ---- charts -----------------------------------------------------------------------------
def _nice(v: float) -> int:
    """Round an axis maximum up to 1, 2, 2.5 or 5 x 10^k."""
    import math
    if v <= 0:
        return 1
    mag = 10 ** math.floor(math.log10(v))
    for m in (1, 2, 2.5, 5, 10):
        if v <= m * mag:
            return int(m * mag)
    return int(10 * mag)


def _esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def cumulative_chart(ts: dict, families: list[dict], months_back: int = 24, top: int = 8) -> str:
    months = ts["months"][-months_back:]
    fams = [f for f in families if f["family"] in ts["families"]][:top]
    series = []
    for f in fams:
        full = ts["families"][f["family"]]
        before = f["total"] - sum(full)
        window = full[-months_back:]
        before += sum(full[:-months_back]) if len(full) > months_back else 0
        cum, acc = [], before
        for v in window:
            acc += v
            cum.append(acc)
        series.append((f["display"], cum))
    W, H, L, R, T, B = 1200, 520, 90, 230, 50, 60
    ymax = _nice(max(max(c) for _, c in series) if series else 1)
    xs = lambda i: L + i * (W - L - R) / max(len(months) - 1, 1)
    ys = lambda v: T + (H - T - B) * (1 - v / ymax)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif" font-size="14">',
           '<style>text{fill:#444}.grid{stroke:#999;stroke-opacity:.25}.axis{stroke:#888}.lbl{font-size:13px}.title{font-size:20px;font-weight:600}.sub{fill:#777;font-size:13px}@media (prefers-color-scheme: dark){text{fill:#ddd}.sub{fill:#aaa}}</style>',
           f'<text class="title" x="{L}" y="28">Descendants per model family, cumulative</text>',
           f'<text class="sub" x="{L}" y="46">Finetunes, adapters, quantizations and merges on the Hugging Face Hub, by month the derivative was created. Last {months_back} months.</text>']
    for k in range(6):
        v = ymax * k / 5
        y = ys(v)
        out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text class="lbl" x="{L - 8}" y="{y + 5:.1f}" text-anchor="end">{int(v):,}</text>')
    for i, mo in enumerate(months):
        if i % 3 == 0 or i == len(months) - 1:
            out.append(f'<text class="lbl" x="{xs(i):.1f}" y="{H - B + 22}" text-anchor="middle">{mo}</text>')
    out.append(f'<line class="axis" x1="{L}" x2="{W - R}" y1="{H - B}" y2="{H - B}"/>')
    for j, (name, cum) in enumerate(series):
        col = PALETTE[j % len(PALETTE)]
        pts = " ".join(f"{xs(i):.1f},{ys(v):.1f}" for i, v in enumerate(cum))
        out.append(f'<polyline fill="none" stroke="{col}" stroke-width="2.5" stroke-linejoin="round" points="{pts}"/>')
        out.append(f'<circle cx="{xs(len(cum) - 1):.1f}" cy="{ys(cum[-1]):.1f}" r="4" fill="{col}"/>')
        ly = T + 18 + j * 24
        out.append(f'<rect x="{W - R + 14}" y="{ly - 11}" width="14" height="14" rx="3" fill="{col}"/>')
        out.append(f'<text class="lbl" x="{W - R + 34}" y="{ly}">{_esc(name)} · {cum[-1]:,}</text>')
    out.append("</svg>\n")
    return "\n".join(out)


def monthly_chart(ts: dict, families: list[dict], months_back: int = 18, top: int = 6) -> str:
    months = ts["months"][-months_back:]
    fams = [f for f in families if f["family"] in ts["families"]][:top]
    W, H, L, R, T, B = 1200, 440, 80, 200, 50, 60
    ymax = _nice(max(max(ts["families"][f["family"]][-months_back:]) for f in fams) if fams else 1)
    gw = (W - L - R) / len(months)
    bw = gw / (len(fams) + 1)
    ys = lambda v: T + (H - T - B) * (1 - v / ymax)
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-sans-serif, system-ui, sans-serif" font-size="14">',
           '<style>text{fill:#444}.grid{stroke:#999;stroke-opacity:.25}.lbl{font-size:12px}.title{font-size:20px;font-weight:600}.sub{fill:#777;font-size:13px}@media (prefers-color-scheme: dark){text{fill:#ddd}.sub{fill:#aaa}}</style>',
           f'<text class="title" x="{L}" y="28">New derivatives per month</text>',
           f'<text class="sub" x="{L}" y="46">Models created each month that declare a base in the family. Last {months_back} months.</text>']
    for k in range(6):
        v = ymax * k / 5
        out.append(f'<line class="grid" x1="{L}" x2="{W - R}" y1="{ys(v):.1f}" y2="{ys(v):.1f}"/>')
        out.append(f'<text class="lbl" x="{L - 8}" y="{ys(v) + 4:.1f}" text-anchor="end">{int(v):,}</text>')
    for i, mo in enumerate(months):
        out.append(f'<text class="lbl" x="{L + gw * (i + .5):.1f}" y="{H - B + 20}" text-anchor="middle">{mo[2:]}</text>')
        for j, f in enumerate(fams):
            v = ts["families"][f["family"]][-months_back:][i]
            x = L + gw * i + bw * (j + .5)
            out.append(f'<rect x="{x:.1f}" y="{ys(v):.1f}" width="{bw:.1f}" height="{H - B - ys(v):.1f}" fill="{PALETTE[j % len(PALETTE)]}"/>')
    for j, f in enumerate(fams):
        ly = T + 18 + j * 24
        out.append(f'<rect x="{W - R + 14}" y="{ly - 11}" width="14" height="14" rx="3" fill="{PALETTE[j % len(PALETTE)]}"/>')
        out.append(f'<text class="lbl" x="{W - R + 34}" y="{ly}">{_esc(f["display"])}</text>')
    out.append("</svg>\n")
    return "\n".join(out)


# ---- README -------------------------------------------------------------------------------
def readme(lb: dict, stats: dict, date: str) -> str:
    s = stats
    top = lb["models_all_time"][0]
    fam = lb["families"]
    hot = lb["models_90d"][0]
    pct = 100 * s["with_ancestry"] / s["models"]
    return f"""<div align="center">

<a href="{SITE}galaxy.html"><img src="assets/galaxy.png" alt="The Model Galaxy: every Hugging Face model with an ancestor or a descendant, as one zoomable map. Families are clusters, base models are stars, derivatives are the dots around them." width="100%"/></a>

**[Fly through the Model Galaxy →]({SITE}galaxy.html)** · {n(s['parents'] + s['with_ancestry'])}+ models in one zoomable WebGL map · **[Explorer →]({SITE})** · search any model, walk its pedigree, share a link.

# Open Model Family Tree

**Every model on the Hugging Face Hub, its ancestry, and a leaderboard of the base models the ecosystem actually builds on. Rebuilt nightly.**

![Models](https://img.shields.io/badge/models-{s['models'] // 1000}k-0A7E8C)
![Links](https://img.shields.io/badge/parent%20links-{s['edges'] // 1000}k-0A7E8C)
![Updated](https://img.shields.io/badge/updated-{date.replace('-', '--')}-555)
[![Stars](https://img.shields.io/github/stars/{REPO}?style=flat)](https://github.com/{REPO}/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

**{n(s['models'])}** models · **{n(s['with_ancestry'])}** declare a base model ({pct:.0f}%) · **{n(s['edges'])}** parent links · **{n(s['parents'])}** models have descendants · **{n(s['roots'])}** roots in **{n(s['families'])}** families

The most built-on model on the Hub is **{hf(top['id'])}** with **{n(top['total'])}** descendants. In the last 90 days it is **{hf(hot['id'])}** with **{n(hot['d90'])}** new ones. The biggest family is **{fam[0]['display']}** ({n(fam[0]['total'])}).

## Install into your agent

```bash
claude plugin marketplace add {REPO}
claude plugin install model-family-tree@model-family-tree
```

Requires [uv](https://docs.astral.sh/uv/) on PATH. Then ask Claude: *what is unsloth/Qwen2.5-7B-Instruct based on, and which Qwen base has the most finetunes?* It answers from the `lineage` and `leaderboard` MCP tools.

<details>
<summary>Any MCP client</summary>

```json
{{"mcpServers": {{"model-family-tree": {{"command": "uv", "args": ["run", "--frozen", "--no-dev", "--directory", "/path/to/model-family-tree", "python", "mcp/server.py"]}}}}}}
```

Tools: `lineage(id)`, `children(id)`, `leaderboard(kind)`, `family(name)`, `search(query)`.

</details>

## See it

| | |
|---|---|
| **[Galaxy]({SITE}galaxy.html)** | Every model that has an ancestor or a descendant ({n(s['with_ancestry'] + s['parents'])}+ points) in one WebGL map. Families are circle-packed clusters, base models are stars, each derivative is a dot colored by relation and sized by downloads. Scroll to zoom from the whole Hub down to one model, click any dot. |
| **[Explorer]({SITE})** | Type any model id. Its pedigree is drawn as a radial tree: every ancestor path fans out to the left (merges show all parents), the most downloaded descendants to the right, unfoldable level by level, live from the Hub. |
| **[Leaderboard]({SITE}#board:all)** | All {n(s['parents'])} models with descendants, sortable and filterable, plus the curated views below. |

<a href="assets/families.svg"><img src="assets/families.svg" alt="Cumulative descendants per model family over the last 24 months" width="100%"/></a>

## Most-descended base models

Unique descendants of every kind: finetunes, adapters (LoRA), quantizations and merges, each counted once however many paths reach it. † marks a base that was deleted or made private but is still referenced. [Full top 500 →](docs/tables/models_all_time.md)

{models_table(lb['models_all_time'], limit=25)}
## Hot right now: new descendants in the last 90 days

[Full top 500 →](docs/tables/models_90d.md)

{models_table(lb['models_90d'], limit=25)}
## Finetunes only

Adapters and quantizations inflate the all-time table (tens of thousands of auto-generated LoRAs sit on a few small bases). This view counts descendants whose own relation to their parent is `finetune`. [Full top 500 →](docs/tables/models_finetune.md)

{models_table(lb['models_finetune'], limit=25)}
## Families

Roots grouped by series name across organizations (so `unsloth/Llama-3.1-8B` re-uploads count toward Llama 3.1). Grouping is a heuristic with hand overrides in [`data/families.yaml`](data/families.yaml); PRs welcome. [Full table →](docs/tables/families.md)

<a href="assets/monthly.svg"><img src="assets/monthly.svg" alt="New derivatives per month for the top families" width="100%"/></a>

{families_table(fam, limit=25)}
## Organizations

Descendants of every root owned by the organization, deduplicated. [Full table →](docs/tables/orgs.md)

{orgs_table(lb['orgs'], limit=15)}
## How it works

1. **Source.** The daily [`cfahlgren1/hub-stats`](https://huggingface.co/datasets/cfahlgren1/hub-stats) dump of the Hub's `/api/models` (Apache-2.0), which carries the `base_model` metadata model authors declare in their cards, plus the legacy `base_model:` tags as a fallback.
2. **Graph.** Child → parent edges with the declared relation (`finetune`, `adapter`, `quantized`, `merge`). Merges give a DAG, mis-tagged cards give the occasional cycle ({n(s['cyclic_nodes'])} nodes today); both are handled.
3. **Counts.** Descendant sets are built children-first and unioned, so every model is counted once per ancestor. `direct` is declared children; `total` is the whole subtree.
4. **Families.** Roots (models that declare no parent) are grouped by a series heuristic over the model name, with overrides in `data/families.yaml`.
5. **Galaxy layout.** Each root's subtree is a radial tree (depth rings sized by population, wedges by subtree size); roots are circle-packed inside their family and families into the galaxy, with a port of d3's front-chain packing. Positions ship as a 10 MB binary, ids load lazily in chunks.
6. **Refresh.** A GitHub Action rebuilds everything nightly, commits `dist/` and `README.md`, and attaches the full node and edge tables plus the galaxy data to the [`data-latest`](https://github.com/{REPO}/releases/tag/data-latest) release, which the site reads.

### Caveats

- **Declared ancestry only.** {pct:.0f}% of models declare a base. Untagged re-uploads and GGUF conversions without metadata are invisible, so every number is a floor.
- **Activity, not quality.** A base with 30,000 adapters was mostly a tutorial default. Read the finetune-only and 90-day tables alongside the all-time one.
- **Ghost parents.** {n(s['ghost_parents'])} referenced bases are no longer public. They stay in the tree, marked †.
- **Families are heuristic.** Series detection is a regex over names. Fix a wrong grouping by editing `data/families.yaml`.

## Data files

| File | What |
|---|---|
| [`dist/leaderboard.json`](dist/leaderboard.json) | Top 500 models (all time, 90 days, finetune-only), families, organizations |
| [`dist/parents.json`](dist/parents.json) | Every model with descendants, compact columns |
| [`dist/timeseries.json`](dist/timeseries.json) | Monthly new descendants for the top families and models |
| [`dist/children_top.json`](dist/children_top.json) | Top 25 children by downloads for the 3,000 most-descended parents |
| [`dist/llms.txt`](dist/llms.txt) | Plain-text summary for LLMs |
| `data-latest` release | `nodes.parquet` and `edges.parquet`, the full graph |

## Build it yourself

```bash
uv sync
uv run python scripts/build.py all        # downloads the dump (~1.6 GB), builds in about 15 seconds
uv run python scripts/build.py build      # rebuild from the cached dump
uv run pytest
```

## Related

- [Arabic AI Atlas](https://github.com/h9-tec/arabic-ai-atlas): the same idea for one language's ecosystem, with a map.
- Hugging Face shows the tree for one model on its page; this repo aggregates the whole Hub.

## License

Code MIT. Generated data CC BY 4.0, derived from Hub metadata via `cfahlgren1/hub-stats` (Apache-2.0).

*Generated {date}.*
"""


def write_tables(lb: dict, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    (out / "models_all_time.md").write_text("# Most-descended base models, all time (top 500)\n\n" + models_table(lb["models_all_time"]))
    (out / "models_90d.md").write_text("# Most new descendants in the last 90 days (top 500)\n\n" + models_table(lb["models_90d"]))
    (out / "models_finetune.md").write_text("# Most finetune descendants (top 500)\n\n" + models_table(lb["models_finetune"]))
    (out / "families.md").write_text("# Families (top 300)\n\n" + families_table(lb["families"]))
    (out / "orgs.md").write_text("# Organizations (top 150)\n\n" + orgs_table(lb["orgs"]))
