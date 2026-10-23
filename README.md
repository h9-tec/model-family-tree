<div align="center">

<a href="https://h9-tec.github.io/model-family-tree/galaxy.html"><img src="assets/galaxy.jpg" alt="The Model Galaxy: every Hugging Face model with an ancestor or a descendant, as one zoomable map. Families are clusters, base models are stars, derivatives are the dots around them." width="100%"/></a>

**[Fly through the Model Galaxy →](https://h9-tec.github.io/model-family-tree/galaxy.html)** · 948,476 models in one zoomable WebGL map · **[Explorer →](https://h9-tec.github.io/model-family-tree/)** · search any model, walk its pedigree, share a link.

# Open Model Family Tree

**Every model on the Hugging Face Hub, its ancestry, and a leaderboard of the base models the ecosystem actually builds on. Rebuilt nightly.**

![Models](https://img.shields.io/badge/models-3177k-0A7E8C)
![Links](https://img.shields.io/badge/parent%20links-936k-0A7E8C)
![Updated](https://img.shields.io/badge/updated-2026--10--23-555)
[![Stars](https://img.shields.io/github/stars/h9-tec/model-family-tree?style=flat)](https://github.com/h9-tec/model-family-tree/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

**3,177,706** models · **903,174** declare a base model (28%) · **936,128** parent links · **88,890** models have descendants · **45,263** roots in **24,154** families

The most built-on model on the Hub is **[black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)** with **43,706** descendants. In the last 90 days it is **[Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)** with **4,779** new ones. The biggest family is **Qwen1.5** (71,023).

## Install into your agent

```bash
claude plugin marketplace add h9-tec/model-family-tree
claude plugin install model-family-tree@model-family-tree
```

Requires [uv](https://docs.astral.sh/uv/) on PATH. Then ask Claude: *what is unsloth/Qwen2.5-7B-Instruct based on, and which Qwen base has the most finetunes?* It answers from the `lineage` and `leaderboard` MCP tools.

<details>
<summary>Any MCP client</summary>

```json
{"mcpServers": {"model-family-tree": {"command": "uv", "args": ["run", "--frozen", "--no-dev", "--directory", "/path/to/model-family-tree", "python", "mcp/server.py"]}}}
```

Tools: `lineage(id)`, `children(id)`, `leaderboard(kind)`, `family(name)`, `search(query)`.

</details>

## See it

| | |
|---|---|
| **[Galaxy](https://h9-tec.github.io/model-family-tree/galaxy.html)** | Every model that has an ancestor or a descendant (948,476 points) in one WebGL map. Families are circle-packed clusters, base models are stars, each derivative is a dot colored by relation and sized by downloads. Scroll to zoom from the whole Hub down to one model, click any dot. |
| **[Explorer](https://h9-tec.github.io/model-family-tree/)** | Type any model id. Its pedigree is drawn as a radial tree: every ancestor path fans out to the left (merges show all parents), the most downloaded descendants to the right, unfoldable level by level, live from the Hub. |
| **[Leaderboard](https://h9-tec.github.io/model-family-tree/#board:all)** | All 88,890 models with descendants, sortable and filterable, plus the curated views below. |

<a href="assets/families.svg"><img src="assets/families.svg" alt="Cumulative descendants per model family over the last 24 months" width="100%"/></a>

## Most-descended base models

Unique descendants of every kind: finetunes, adapters (LoRA), quantizations and merges, each counted once however many paths reach it. † marks a base that was deleted or made private but is still referenced. [Full top 500 →](docs/tables/models_all_time.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | 43,706 | 43,432 | 226 | 680 / 42,881 / 129 / 16 | FLUX.1 |
| 2 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) | 32,564 | 32,534 | 0 | 41 / 32,475 / 46 / 2 | Qwen1.5 |
| 3 | [Qwen/Qwen1.5-1.8B](https://huggingface.co/Qwen/Qwen1.5-1.8B) | 30,657 | 30,627 | 1 | 35 / 30,591 / 29 / 2 | Qwen1.5 |
| 4 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) | 24,115 | 24,035 | 10 | 309 / 23,706 / 89 / 11 | Gemma 1 |
| 5 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 22,814 | 2,087 | 2,721 | 11,840 / 6,873 / 3,508 / 593 | Qwen2.5 |
| 6 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,559 | 3,264 | 2,356 | 9,555 / 6,064 / 5,096 / 844 | Llama 3.1 |
| 7 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,152 | 7,297 | 1,640 | 6,856 / 3,998 / 3,585 / 713 | Llama 3.1 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,406 | 6,636 | 2,014 | 8,351 / 3,860 / 1,786 / 409 | Qwen2.5 |
| 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,644 | 13,263 | 802 | 13,096 / 397 / 150 / 1 | DistilBERT |
| 10 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) | 11,603 | 4,013 | 68 | 2,974 / 5,189 / 2,060 / 1,365 | Mistral |
| 11 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | 11,506 | 11,028 | 177 | 1,413 / 9,990 / 50 / 53 | Stable Diffusion |
| 12 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,088 | 8,850 | 1,467 | 3,417 / 6,514 / 1,064 / 93 | Qwen3 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 10,868 | 1,027 | 1,675 | 4,950 / 4,067 / 1,694 / 157 | Qwen2.5 |
| 14 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,276 | 1,728 | 119 | 4,206 / 2,071 / 3,013 / 986 | Llama 3 |
| 15 | [google/gemma-7b](https://huggingface.co/google/gemma-7b) | 9,853 | 9,586 | 4 | 454 / 9,294 / 97 / 8 | Gemma 1 |
| 16 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,813 | 193 | 1,770 | 8,846 / 611 / 351 / 5 | SmolLM2 |
| 17 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,556 | 1,371 | 936 | 5,979 / 2,217 / 1,304 / 56 | Qwen2.5 |
| 18 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,484 | 849 | 1,816 | 4,730 / 2,897 / 1,784 / 72 | Qwen3 |
| 19 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,354 | 383 | 1,726 | 8,691 / 380 / 278 / 5 | SmolLM2 |
| 20 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,670 | 92 | 1,626 | 8,456 / 148 / 66 / 0 | SmolLM2 |
| 21 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,569 | 128 | 1,606 | 8,422 / 117 / 30 / 0 | SmolLM2 |
| 22 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,563 | 1,135 | 1,340 | 3,864 / 3,105 / 1,509 / 85 | Qwen2.5 |
| 23 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,437 | 8,390 | 1,588 | 8,331 / 100 / 6 / 0 | SmolLM2 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 7,909 | 5,113 | 1,441 | 3,691 / 2,680 / 1,469 / 68 | Qwen3 |
| 25 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,518 | 3,473 | 664 | 3,926 / 1,589 / 1,851 / 152 | Llama 3.2 |

## Hot right now: new descendants in the last 90 days

[Full top 500 →](docs/tables/models_90d.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 4,782 | 2,483 | 4,779 | 966 / 379 / 3,380 / 57 | Qwen3.8 |
| 2 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) | 6,189 | 765 | 3,206 | 2,432 / 1,422 / 2,229 / 106 | Qwen3.5 |
| 3 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 22,814 | 2,087 | 2,721 | 11,840 / 6,873 / 3,508 / 593 | Qwen2.5 |
| 4 | [Qwen/Qwen3.5-4B-Base](https://huggingface.co/Qwen/Qwen3.5-4B-Base) | 4,743 | 375 | 2,599 | 1,872 / 1,280 / 1,550 / 41 | Qwen3.5 |
| 5 | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | 5,074 | 2,747 | 2,527 | 1,648 / 1,322 / 2,001 / 103 | Qwen3.5 |
| 6 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,559 | 3,264 | 2,356 | 9,555 / 6,064 / 5,096 / 844 | Llama 3.1 |
| 7 | [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | 4,177 | 2,463 | 2,234 | 1,576 / 1,141 / 1,424 / 36 | Qwen3.5 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,406 | 6,636 | 2,014 | 8,351 / 3,860 / 1,786 / 409 | Qwen2.5 |
| 9 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,484 | 849 | 1,816 | 4,730 / 2,897 / 1,784 / 72 | Qwen3 |
| 10 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,813 | 193 | 1,770 | 8,846 / 611 / 351 / 5 | SmolLM2 |
| 11 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,354 | 383 | 1,726 | 8,691 / 380 / 278 / 5 | SmolLM2 |
| 12 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 10,868 | 1,027 | 1,675 | 4,950 / 4,067 / 1,694 / 157 | Qwen2.5 |
| 13 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,152 | 7,297 | 1,640 | 6,856 / 3,998 / 3,585 / 713 | Llama 3.1 |
| 14 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,670 | 92 | 1,626 | 8,456 / 148 / 66 / 0 | SmolLM2 |
| 15 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,547 | 926 | 1,613 | 3,791 / 998 / 1,733 / 25 | Qwen3 |
| 16 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,569 | 128 | 1,606 | 8,422 / 117 / 30 / 0 | SmolLM2 |
| 17 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,437 | 8,390 | 1,588 | 8,331 / 100 / 6 / 0 | SmolLM2 |
| 18 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,088 | 8,850 | 1,467 | 3,417 / 6,514 / 1,064 / 93 | Qwen3 |
| 19 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 7,909 | 5,113 | 1,441 | 3,691 / 2,680 / 1,469 / 68 | Qwen3 |
| 20 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,563 | 1,135 | 1,340 | 3,864 / 3,105 / 1,509 / 85 | Qwen2.5 |
| 21 | [Qwen/Qwen3.5-0.8B-Base](https://huggingface.co/Qwen/Qwen3.5-0.8B-Base) | 2,569 | 258 | 1,326 | 974 / 700 / 886 / 9 | Qwen3.5 |
| 22 | [krea/Krea-2-Raw](https://huggingface.co/krea/Krea-2-Raw) | 2,962 | 1,101 | 1,229 | 116 / 2,775 / 68 / 3 | krea-2-raw |
| 23 | [Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | 6,770 | 703 | 1,198 | 3,429 / 1,650 / 1,598 / 93 | Qwen3 |
| 24 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | 2,891 | 1,695 | 1,186 | 499 / 488 / 1,856 / 47 | Qwen3.6 |
| 25 | [Qwen/Qwen3-1.7B-Base](https://huggingface.co/Qwen/Qwen3-1.7B-Base) | 4,878 | 602 | 1,142 | 2,725 / 1,004 / 1,129 / 20 | Qwen3 |

## Finetunes only

Adapters and quantizations inflate the all-time table (tens of thousands of auto-generated LoRAs sit on a few small bases). This view counts descendants whose own relation to their parent is `finetune`. [Full top 500 →](docs/tables/models_finetune.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,644 | 13,263 | 802 | 13,096 / 397 / 150 / 1 | DistilBERT |
| 2 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 22,814 | 2,087 | 2,721 | 11,840 / 6,873 / 3,508 / 593 | Qwen2.5 |
| 3 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,559 | 3,264 | 2,356 | 9,555 / 6,064 / 5,096 / 844 | Llama 3.1 |
| 4 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,813 | 193 | 1,770 | 8,846 / 611 / 351 / 5 | SmolLM2 |
| 5 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,354 | 383 | 1,726 | 8,691 / 380 / 278 / 5 | SmolLM2 |
| 6 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,670 | 92 | 1,626 | 8,456 / 148 / 66 / 0 | SmolLM2 |
| 7 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,569 | 128 | 1,606 | 8,422 / 117 / 30 / 0 | SmolLM2 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,406 | 6,636 | 2,014 | 8,351 / 3,860 / 1,786 / 409 | Qwen2.5 |
| 9 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,437 | 8,390 | 1,588 | 8,331 / 100 / 6 / 0 | SmolLM2 |
| 10 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) | 7,458 | 7,218 | 263 | 7,230 / 147 / 74 / 7 | BERT |
| 11 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,152 | 7,297 | 1,640 | 6,856 / 3,998 / 3,585 / 713 | Llama 3.1 |
| 12 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,556 | 1,371 | 936 | 5,979 / 2,217 / 1,304 / 56 | Qwen2.5 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 10,868 | 1,027 | 1,675 | 4,950 / 4,067 / 1,694 / 157 | Qwen2.5 |
| 14 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,484 | 849 | 1,816 | 4,730 / 2,897 / 1,784 / 72 | Qwen3 |
| 15 | [unsloth/Qwen2.5-7B-Instruct](https://huggingface.co/unsloth/Qwen2.5-7B-Instruct) | 5,349 | 5,307 | 674 | 4,546 / 772 / 29 / 2 | Qwen2.5 |
| 16 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) | 4,738 | 4,375 | 198 | 4,543 / 79 / 115 / 0 | XLM-RoBERTa |
| 17 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) | 6,683 | 395 | 543 | 4,522 / 944 / 1,201 / 16 | Gemma 3 |
| 18 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,276 | 1,728 | 119 | 4,206 / 2,071 / 3,013 / 986 | Llama 3 |
| 19 | [aubmindlab/bert-base-arabertv02](https://huggingface.co/aubmindlab/bert-base-arabertv02) | 4,115 | 4,058 | 16 | 4,106 / 5 / 4 / 0 | BERT |
| 20 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) | 4,737 | 4,410 | 362 | 4,070 / 349 / 318 / 0 | Whisper |
| 21 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,518 | 3,473 | 664 | 3,926 / 1,589 / 1,851 / 152 | Llama 3.2 |
| 22 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,563 | 1,135 | 1,340 | 3,864 / 3,105 / 1,509 / 85 | Qwen2.5 |
| 23 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,547 | 926 | 1,613 | 3,791 / 998 / 1,733 / 25 | Qwen3 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 7,909 | 5,113 | 1,441 | 3,691 / 2,680 / 1,469 / 68 | Qwen3 |
| 25 | [Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | 6,770 | 703 | 1,198 | 3,429 / 1,650 / 1,598 / 93 | Qwen3 |

## Families

Roots grouped by series name across organizations (so `unsloth/Llama-3.1-8B` re-uploads count toward Llama 3.1). Grouping is a heuristic with hand overrides in [`data/families.yaml`](data/families.yaml); PRs welcome. [Full table →](docs/tables/families.md)

<a href="assets/monthly.svg"><img src="assets/monthly.svg" alt="New derivatives per month for the top families" width="100%"/></a>

| # | Family | Descendants | Last 90d | Roots | Finetune / adapter / quantized / merge | Biggest root |
|---:|---|---:|---:|---:|---|---|
| 1 | **Qwen1.5** | 71,023 | 7 | 44 | 224 / 70,434 / 349 / 16 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 2 | **Qwen2.5** | 69,905 | 7,879 | 689 | 33,800 / 19,899 / 14,584 / 1,622 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) |
| 3 | **Qwen3** | 54,413 | 10,379 | 642 | 24,125 / 17,032 / 12,818 / 436 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) |
| 4 | **FLUX.1** | 44,166 | 256 | 16 | 772 / 43,186 / 191 / 17 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | **Gemma 1** | 37,057 | 52 | 184 | 1,753 / 34,349 / 887 / 68 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 6 | **Mistral** | 36,474 | 994 | 582 | 10,618 / 11,239 / 11,669 / 2,932 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 7 | **Llama 3.1** | 28,146 | 2,565 | 222 | 11,082 / 6,950 / 8,174 / 1,940 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 8 | **Llama 3** | 24,170 | 414 | 544 | 8,075 / 5,861 / 7,773 / 2,461 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) |
| 9 | **BERT** | 23,205 | 610 | 305 | 22,430 / 508 / 259 / 8 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 10 | **Llama 3.2** | 21,075 | 1,466 | 478 | 9,682 / 5,712 / 5,087 / 594 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) |
| 11 | **Qwen3.5** | 19,385 | 9,011 | 144 | 7,338 / 4,314 / 7,521 / 211 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) |
| 12 | **Gemma 3** | 18,185 | 1,327 | 140 | 10,593 / 2,987 / 4,386 / 219 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) |
| 13 | **Stable Diffusion** | 17,884 | 336 | 29 | 3,413 / 14,302 / 98 / 71 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 14 | **Whisper** | 15,501 | 1,460 | 201 | 11,473 / 2,339 / 1,681 / 8 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 15 | **DistilBERT** | 15,224 | 868 | 81 | 14,447 / 497 / 279 / 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 16 | **SmolLM2** | 13,672 | 2,103 | 59 | 10,932 / 1,602 / 1,118 / 20 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 17 | **Gemma 2** | 12,327 | 461 | 226 | 5,076 / 3,172 / 3,138 / 941 | [google/gemma-2-9b](https://huggingface.co/google/gemma-2-9b) |
| 18 | **Llama 2** | 11,631 | 280 | 413 | 2,984 / 7,067 / 1,367 / 213 | [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) |
| 19 | **Gemma 4** | 11,102 | 3,895 | 132 | 3,279 / 2,011 / 5,655 / 157 | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) |
| 20 | **Qwen2** | 10,772 | 197 | 161 | 3,170 / 6,024 / 1,490 / 88 | [Qwen/Qwen2-0.5B](https://huggingface.co/Qwen/Qwen2-0.5B) |
| 21 | **DeepSeek-R1** | 8,894 | 415 | 131 | 2,713 / 1,512 / 3,777 / 892 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 22 | **XLM-RoBERTa** | 6,330 | 316 | 49 | 6,018 / 138 / 173 / 0 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |
| 23 | **ViT** | 6,082 | 182 | 66 | 5,197 / 752 / 133 / 0 | [google/vit-base-patch16-224-in21k](https://huggingface.co/google/vit-base-patch16-224-in21k) |
| 24 | **Qwen3.8** | 5,976 | 5,972 | 59 | 1,135 / 390 / 4,380 / 71 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) |
| 25 | **Qwen3.6** | 5,932 | 2,141 | 52 | 1,105 / 1,126 / 3,603 / 91 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) |

## Organizations

Descendants of every root owned by the organization, deduplicated. [Full table →](docs/tables/orgs.md)

| # | Organization | Descendants of its roots | Last 90d | Roots | Biggest root |
|---:|---|---:|---:|---:|---|
| 1 | [Qwen](https://huggingface.co/Qwen) | 235,234 | 36,293 | 148 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 2 | [google](https://huggingface.co/google) | 91,907 | 7,450 | 326 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 3 | [meta-llama](https://huggingface.co/meta-llama) | 68,748 | 4,548 | 50 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 4 | [black-forest-labs](https://huggingface.co/black-forest-labs) | 46,136 | 737 | 20 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | [mistralai](https://huggingface.co/mistralai) | 32,751 | 1,343 | 32 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 6 | [unsloth](https://huggingface.co/unsloth) | 24,202 | 378 | 269 | [unsloth/llama-3-8b-Instruct-bnb-4bit](https://huggingface.co/unsloth/llama-3-8b-Instruct-bnb-4bit) |
| 7 | [microsoft](https://huggingface.co/microsoft) | 22,320 | 1,271 | 255 | [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) |
| 8 | [openai](https://huggingface.co/openai) | 19,201 | 1,803 | 21 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 9 | [facebook](https://huggingface.co/facebook) | 17,709 | 1,334 | 495 | [facebook/wav2vec2-base](https://huggingface.co/facebook/wav2vec2-base) |
| 10 | [distilbert](https://huggingface.co/distilbert) | 17,549 | 977 | 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 11 | [HuggingFaceTB](https://huggingface.co/HuggingFaceTB) | 16,265 | 2,256 | 29 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 12 | [stabilityai](https://huggingface.co/stabilityai) | 15,226 | 267 | 73 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 13 | [google-bert](https://huggingface.co/google-bert) | 14,691 | 371 | 12 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 14 | [deepseek-ai](https://huggingface.co/deepseek-ai) | 14,208 | 1,486 | 77 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 15 | [FacebookAI](https://huggingface.co/FacebookAI) | 9,924 | 473 | 19 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |

## How it works

1. **Source.** The daily [`cfahlgren1/hub-stats`](https://huggingface.co/datasets/cfahlgren1/hub-stats) dump of the Hub's `/api/models` (Apache-2.0), which carries the `base_model` metadata model authors declare in their cards, plus the legacy `base_model:` tags as a fallback.
2. **Graph.** Child → parent edges with the declared relation (`finetune`, `adapter`, `quantized`, `merge`). Merges give a DAG, mis-tagged cards give the occasional cycle (78 nodes today); both are handled.
3. **Counts.** Descendant sets are built children-first and unioned, so every model is counted once per ancestor. `direct` is declared children; `total` is the whole subtree.
4. **Families.** Roots (models that declare no parent) are grouped by a series heuristic over the model name, with overrides in `data/families.yaml`.
5. **Galaxy layout.** Each root's subtree is a radial tree (depth rings sized by population, wedges by subtree size); roots are circle-packed inside their family and families into the galaxy, with a port of d3's front-chain packing. Positions ship as a 10 MB binary, ids load lazily in chunks.
6. **Refresh.** A GitHub Action rebuilds everything nightly, commits `dist/` and `README.md`, and attaches the full node and edge tables plus the galaxy data to the [`data-latest`](https://github.com/h9-tec/model-family-tree/releases/tag/data-latest) release, which the site reads.

### Caveats

- **Declared ancestry only.** 28% of models declare a base. Untagged re-uploads and GGUF conversions without metadata are invisible, so every number is a floor.
- **Activity, not quality.** A base with 30,000 adapters was mostly a tutorial default. Read the finetune-only and 90-day tables alongside the all-time one.
- **Ghost parents.** 4,025 referenced bases are no longer public. They stay in the tree, marked †.
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

*Generated 2026-10-23.*
