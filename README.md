<div align="center">

<a href="https://h9-tec.github.io/model-family-tree/galaxy.html"><img src="assets/galaxy.jpg" alt="The Model Galaxy: every Hugging Face model with an ancestor or a descendant, as one zoomable map. Families are clusters, base models are stars, derivatives are the dots around them." width="100%"/></a>

**[Fly through the Model Galaxy →](https://h9-tec.github.io/model-family-tree/galaxy.html)** · 960,208 models in one zoomable WebGL map · **[Explorer →](https://h9-tec.github.io/model-family-tree/)** · search any model, walk its pedigree, share a link.

# Open Model Family Tree

**Every model on the Hugging Face Hub, its ancestry, and a leaderboard of the base models the ecosystem actually builds on. Rebuilt nightly.**

![Models](https://img.shields.io/badge/models-3200k-0A7E8C)
![Links](https://img.shields.io/badge/parent%20links-947k-0A7E8C)
![Updated](https://img.shields.io/badge/updated-2026--11--01-555)
[![Stars](https://img.shields.io/github/stars/h9-tec/model-family-tree?style=flat)](https://github.com/h9-tec/model-family-tree/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

**3,200,472** models · **914,332** declare a base model (29%) · **947,528** parent links · **90,295** models have descendants · **45,838** roots in **24,475** families

The most built-on model on the Hub is **[black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)** with **43,708** descendants. In the last 90 days it is **[Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)** with **5,250** new ones. The biggest family is **Qwen1.5** (71,025).

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
| **[Galaxy](https://h9-tec.github.io/model-family-tree/galaxy.html)** | Every model that has an ancestor or a descendant (960,208 points) in one WebGL map. Families are circle-packed clusters, base models are stars, each derivative is a dot colored by relation and sized by downloads. Scroll to zoom from the whole Hub down to one model, click any dot. |
| **[Explorer](https://h9-tec.github.io/model-family-tree/)** | Type any model id. Its pedigree is drawn as a radial tree: every ancestor path fans out to the left (merges show all parents), the most downloaded descendants to the right, unfoldable level by level, live from the Hub. |
| **[Leaderboard](https://h9-tec.github.io/model-family-tree/#board:all)** | All 90,295 models with descendants, sortable and filterable, plus the curated views below. |

<a href="assets/families.svg"><img src="assets/families.svg" alt="Cumulative descendants per model family over the last 24 months" width="100%"/></a>

## Most-descended base models

Unique descendants of every kind: finetunes, adapters (LoRA), quantizations and merges, each counted once however many paths reach it. † marks a base that was deleted or made private but is still referenced. [Full top 500 →](docs/tables/models_all_time.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | 43,708 | 43,432 | 229 | 681 / 42,876 / 135 / 16 | FLUX.1 |
| 2 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) | 32,564 | 32,534 | 0 | 41 / 32,475 / 46 / 2 | Qwen1.5 |
| 3 | [Qwen/Qwen1.5-1.8B](https://huggingface.co/Qwen/Qwen1.5-1.8B) | 30,658 | 30,628 | 2 | 36 / 30,591 / 29 / 2 | Qwen1.5 |
| 4 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) | 24,117 | 24,037 | 10 | 311 / 23,706 / 89 / 11 | Gemma 1 |
| 5 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,047 | 2,088 | 2,586 | 11,998 / 6,934 / 3,520 / 595 | Qwen2.5 |
| 6 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,677 | 3,271 | 2,101 | 9,569 / 6,129 / 5,134 / 845 | Llama 3.1 |
| 7 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,247 | 7,366 | 1,501 | 6,874 / 4,057 / 3,603 / 713 | Llama 3.1 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,614 | 6,737 | 2,001 | 8,489 / 3,922 / 1,792 / 411 | Qwen2.5 |
| 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,693 | 13,311 | 793 | 13,143 / 397 / 152 / 1 | DistilBERT |
| 10 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) | 11,605 | 4,013 | 68 | 2,973 / 5,189 / 2,063 / 1,365 | Mistral |
| 11 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | 11,547 | 11,068 | 206 | 1,419 / 10,024 / 50 / 54 | Stable Diffusion |
| 12 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,333 | 9,016 | 1,648 | 3,585 / 6,559 / 1,096 / 93 | Qwen3 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,180 | 1,075 | 1,796 | 5,078 / 4,190 / 1,751 / 161 | Qwen2.5 |
| 14 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,277 | 1,727 | 85 | 4,208 / 2,072 / 3,011 / 986 | Llama 3 |
| 15 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,902 | 202 | 1,711 | 8,919 / 621 / 357 / 5 | SmolLM2 |
| 16 | [google/gemma-7b](https://huggingface.co/google/gemma-7b) | 9,854 | 9,586 | 3 | 455 / 9,294 / 97 / 8 | Gemma 1 |
| 17 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,761 | 1,383 | 1,076 | 6,058 / 2,302 / 1,344 / 57 | Qwen2.5 |
| 18 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,616 | 873 | 1,865 | 4,769 / 2,964 / 1,810 / 72 | Qwen3 |
| 19 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,434 | 401 | 1,670 | 8,756 / 390 / 283 / 5 | SmolLM2 |
| 20 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,729 | 92 | 1,552 | 8,512 / 152 / 65 / 0 | SmolLM2 |
| 21 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,657 | 1,136 | 1,281 | 3,877 / 3,157 / 1,538 / 85 | Qwen2.5 |
| 22 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,628 | 130 | 1,533 | 8,477 / 121 / 30 / 0 | SmolLM2 |
| 23 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,494 | 8,440 | 1,514 | 8,385 / 103 / 6 / 0 | SmolLM2 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,006 | 5,181 | 1,488 | 3,702 / 2,746 / 1,489 / 68 | Qwen3 |
| 25 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,559 | 3,496 | 575 | 3,943 / 1,600 / 1,864 / 152 | Llama 3.2 |

## Hot right now: new descendants in the last 90 days

[Full top 500 →](docs/tables/models_90d.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 5,253 | 2,715 | 5,250 | 1,151 / 432 / 3,611 / 59 | Qwen3.8 |
| 2 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) | 6,516 | 789 | 3,346 | 2,562 / 1,485 / 2,367 / 102 | Qwen3.5 |
| 3 | [Qwen/Qwen3.5-4B-Base](https://huggingface.co/Qwen/Qwen3.5-4B-Base) | 5,207 | 438 | 2,934 | 2,009 / 1,459 / 1,695 / 44 | Qwen3.5 |
| 4 | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | 5,371 | 2,907 | 2,663 | 1,760 / 1,378 / 2,134 / 99 | Qwen3.5 |
| 5 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,047 | 2,088 | 2,586 | 11,998 / 6,934 / 3,520 / 595 | Qwen2.5 |
| 6 | [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | 4,589 | 2,753 | 2,523 | 1,684 / 1,302 / 1,564 / 39 | Qwen3.5 |
| 7 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,677 | 3,271 | 2,101 | 9,569 / 6,129 / 5,134 / 845 | Llama 3.1 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,614 | 6,737 | 2,001 | 8,489 / 3,922 / 1,792 / 411 | Qwen2.5 |
| 9 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,616 | 873 | 1,865 | 4,769 / 2,964 / 1,810 / 72 | Qwen3 |
| 10 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,180 | 1,075 | 1,796 | 5,078 / 4,190 / 1,751 / 161 | Qwen2.5 |
| 11 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,902 | 202 | 1,711 | 8,919 / 621 / 357 / 5 | SmolLM2 |
| 12 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,434 | 401 | 1,670 | 8,756 / 390 / 283 / 5 | SmolLM2 |
| 13 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,721 | 941 | 1,660 | 3,888 / 1,038 / 1,770 / 25 | Qwen3 |
| 14 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,333 | 9,016 | 1,648 | 3,585 / 6,559 / 1,096 / 93 | Qwen3 |
| 15 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,729 | 92 | 1,552 | 8,512 / 152 / 65 / 0 | SmolLM2 |
| 16 | [Qwen/Qwen3.5-0.8B-Base](https://huggingface.co/Qwen/Qwen3.5-0.8B-Base) | 2,850 | 277 | 1,546 | 1,037 / 853 / 951 / 9 | Qwen3.5 |
| 17 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,628 | 130 | 1,533 | 8,477 / 121 / 30 / 0 | SmolLM2 |
| 18 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,494 | 8,440 | 1,514 | 8,385 / 103 / 6 / 0 | SmolLM2 |
| 19 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,247 | 7,366 | 1,501 | 6,874 / 4,057 / 3,603 / 713 | Llama 3.1 |
| 20 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,006 | 5,181 | 1,488 | 3,702 / 2,746 / 1,489 / 68 | Qwen3 |
| 21 | [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | 2,435 | 1,595 | 1,299 | 858 / 770 / 800 / 7 | Qwen3.5 |
| 22 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,657 | 1,136 | 1,281 | 3,877 / 3,157 / 1,538 / 85 | Qwen2.5 |
| 23 | [Qwen/Qwen3-1.7B-Base](https://huggingface.co/Qwen/Qwen3-1.7B-Base) | 5,057 | 624 | 1,272 | 2,812 / 1,064 / 1,161 / 20 | Qwen3 |
| 24 | [Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | 6,866 | 717 | 1,266 | 3,465 / 1,680 / 1,628 / 93 | Qwen3 |
| 25 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) | 3,026 | 1,757 | 1,247 | 538 / 495 / 1,944 / 48 | Qwen3.6 |

## Finetunes only

Adapters and quantizations inflate the all-time table (tens of thousands of auto-generated LoRAs sit on a few small bases). This view counts descendants whose own relation to their parent is `finetune`. [Full top 500 →](docs/tables/models_finetune.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,693 | 13,311 | 793 | 13,143 / 397 / 152 / 1 | DistilBERT |
| 2 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,047 | 2,088 | 2,586 | 11,998 / 6,934 / 3,520 / 595 | Qwen2.5 |
| 3 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,677 | 3,271 | 2,101 | 9,569 / 6,129 / 5,134 / 845 | Llama 3.1 |
| 4 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 9,902 | 202 | 1,711 | 8,919 / 621 / 357 / 5 | SmolLM2 |
| 5 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,434 | 401 | 1,670 | 8,756 / 390 / 283 / 5 | SmolLM2 |
| 6 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,729 | 92 | 1,552 | 8,512 / 152 / 65 / 0 | SmolLM2 |
| 7 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,614 | 6,737 | 2,001 | 8,489 / 3,922 / 1,792 / 411 | Qwen2.5 |
| 8 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,628 | 130 | 1,533 | 8,477 / 121 / 30 / 0 | SmolLM2 |
| 9 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,494 | 8,440 | 1,514 | 8,385 / 103 / 6 / 0 | SmolLM2 |
| 10 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) | 7,490 | 7,246 | 278 | 7,257 / 147 / 79 / 7 | BERT |
| 11 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,247 | 7,366 | 1,501 | 6,874 / 4,057 / 3,603 / 713 | Llama 3.1 |
| 12 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,761 | 1,383 | 1,076 | 6,058 / 2,302 / 1,344 / 57 | Qwen2.5 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,180 | 1,075 | 1,796 | 5,078 / 4,190 / 1,751 / 161 | Qwen2.5 |
| 14 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,616 | 873 | 1,865 | 4,769 / 2,964 / 1,810 / 72 | Qwen3 |
| 15 | [unsloth/Qwen2.5-7B-Instruct](https://huggingface.co/unsloth/Qwen2.5-7B-Instruct) | 5,437 | 5,395 | 703 | 4,634 / 772 / 29 / 2 | Qwen2.5 |
| 16 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) | 4,760 | 4,397 | 211 | 4,562 / 79 / 118 / 0 | XLM-RoBERTa |
| 17 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) | 6,716 | 396 | 517 | 4,545 / 950 / 1,205 / 16 | Gemma 3 |
| 18 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,277 | 1,727 | 85 | 4,208 / 2,072 / 3,011 / 986 | Llama 3 |
| 19 | [aubmindlab/bert-base-arabertv02](https://huggingface.co/aubmindlab/bert-base-arabertv02) | 4,115 | 4,058 | 15 | 4,106 / 5 / 4 / 0 | BERT |
| 20 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) | 4,770 | 4,426 | 355 | 4,088 / 352 / 330 / 0 | Whisper |
| 21 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,559 | 3,496 | 575 | 3,943 / 1,600 / 1,864 / 152 | Llama 3.2 |
| 22 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,721 | 941 | 1,660 | 3,888 / 1,038 / 1,770 / 25 | Qwen3 |
| 23 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,657 | 1,136 | 1,281 | 3,877 / 3,157 / 1,538 / 85 | Qwen2.5 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,006 | 5,181 | 1,488 | 3,702 / 2,746 / 1,489 / 68 | Qwen3 |
| 25 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,333 | 9,016 | 1,648 | 3,585 / 6,559 / 1,096 / 93 | Qwen3 |

## Families

Roots grouped by series name across organizations (so `unsloth/Llama-3.1-8B` re-uploads count toward Llama 3.1). Grouping is a heuristic with hand overrides in [`data/families.yaml`](data/families.yaml); PRs welcome. [Full table →](docs/tables/families.md)

<a href="assets/monthly.svg"><img src="assets/monthly.svg" alt="New derivatives per month for the top families" width="100%"/></a>

| # | Family | Descendants | Last 90d | Roots | Finetune / adapter / quantized / merge | Biggest root |
|---:|---|---:|---:|---:|---|---|
| 1 | **Qwen1.5** | 71,025 | 9 | 44 | 225 / 70,435 / 349 / 16 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 2 | **Qwen2.5** | 70,797 | 7,887 | 687 | 34,203 / 20,240 / 14,723 / 1,631 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) |
| 3 | **Qwen3** | 55,413 | 10,422 | 649 | 24,645 / 17,304 / 13,029 / 433 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) |
| 4 | **FLUX.1** | 44,169 | 260 | 16 | 772 / 43,181 / 199 / 17 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | **Gemma 1** | 37,068 | 58 | 184 | 1,757 / 34,357 / 886 / 68 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 6 | **Mistral** | 36,534 | 976 | 583 | 10,633 / 11,254 / 11,699 / 2,932 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 7 | **Llama 3.1** | 28,283 | 2,316 | 223 | 11,101 / 7,023 / 8,219 / 1,940 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 8 | **Llama 3** | 24,206 | 408 | 544 | 8,095 / 5,866 / 7,785 / 2,460 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) |
| 9 | **BERT** | 23,276 | 632 | 304 | 22,486 / 508 / 274 / 8 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 10 | **Llama 3.2** | 21,179 | 1,240 | 478 | 9,731 / 5,730 / 5,123 / 595 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) |
| 11 | **Qwen3.5** | 20,719 | 9,787 | 153 | 7,783 / 4,752 / 7,952 / 231 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) |
| 12 | **Gemma 3** | 18,259 | 1,289 | 140 | 10,630 / 3,005 / 4,405 / 219 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) |
| 13 | **Stable Diffusion** | 17,968 | 405 | 30 | 3,420 / 14,371 / 103 / 74 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 14 | **Whisper** | 15,683 | 1,548 | 204 | 11,599 / 2,353 / 1,724 / 7 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 15 | **DistilBERT** | 15,275 | 856 | 81 | 14,495 / 497 / 282 / 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 16 | **SmolLM2** | 13,828 | 2,063 | 59 | 11,034 / 1,633 / 1,141 / 20 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 17 | **Gemma 2** | 12,357 | 402 | 226 | 5,085 / 3,182 / 3,148 / 942 | [google/gemma-2-9b](https://huggingface.co/google/gemma-2-9b) |
| 18 | **Gemma 4** | 11,714 | 4,243 | 132 | 3,463 / 2,133 / 5,948 / 170 | [google/gemma-4-31B](https://huggingface.co/google/gemma-4-31B) |
| 19 | **Llama 2** | 11,662 | 297 | 413 | 3,012 / 7,068 / 1,369 / 213 | [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) |
| 20 | **Qwen2** | 10,796 | 183 | 161 | 3,185 / 6,034 / 1,489 / 88 | [Qwen/Qwen2-0.5B](https://huggingface.co/Qwen/Qwen2-0.5B) |
| 21 | **DeepSeek-R1** | 9,064 | 546 | 130 | 2,863 / 1,523 / 3,783 / 895 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 22 | **Qwen3.8** | 6,614 | 6,610 | 67 | 1,357 / 443 / 4,737 / 77 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) |
| 23 | **XLM-RoBERTa** | 6,384 | 354 | 49 | 6,066 / 138 / 179 / 0 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |
| 24 | **ViT** | 6,122 | 187 | 69 | 5,233 / 752 / 137 / 0 | [google/vit-base-patch16-224-in21k](https://huggingface.co/google/vit-base-patch16-224-in21k) |
| 25 | **Qwen3.6** | 6,110 | 2,013 | 53 | 1,158 / 1,152 / 3,701 / 92 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) |

## Organizations

Descendants of every root owned by the organization, deduplicated. [Full table →](docs/tables/orgs.md)

| # | Organization | Descendants of its roots | Last 90d | Roots | Biggest root |
|---:|---|---:|---:|---:|---|
| 1 | [Qwen](https://huggingface.co/Qwen) | 239,407 | 37,710 | 148 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 2 | [google](https://huggingface.co/google) | 92,674 | 7,565 | 327 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 3 | [meta-llama](https://huggingface.co/meta-llama) | 69,069 | 4,107 | 50 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 4 | [black-forest-labs](https://huggingface.co/black-forest-labs) | 46,192 | 781 | 20 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | [mistralai](https://huggingface.co/mistralai) | 32,885 | 1,374 | 33 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 6 | [unsloth](https://huggingface.co/unsloth) | 24,191 | 329 | 269 | [unsloth/llama-3-8b-Instruct-bnb-4bit](https://huggingface.co/unsloth/llama-3-8b-Instruct-bnb-4bit) |
| 7 | [microsoft](https://huggingface.co/microsoft) | 22,468 | 1,234 | 256 | [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) |
| 8 | [openai](https://huggingface.co/openai) | 19,426 | 1,926 | 21 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 9 | [facebook](https://huggingface.co/facebook) | 17,860 | 1,296 | 502 | [facebook/wav2vec2-base](https://huggingface.co/facebook/wav2vec2-base) |
| 10 | [distilbert](https://huggingface.co/distilbert) | 17,624 | 982 | 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 11 | [HuggingFaceTB](https://huggingface.co/HuggingFaceTB) | 16,446 | 2,220 | 29 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 12 | [stabilityai](https://huggingface.co/stabilityai) | 15,288 | 311 | 73 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 13 | [google-bert](https://huggingface.co/google-bert) | 14,729 | 381 | 12 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 14 | [deepseek-ai](https://huggingface.co/deepseek-ai) | 14,525 | 1,646 | 77 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 15 | [FacebookAI](https://huggingface.co/FacebookAI) | 9,988 | 512 | 19 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |

## How it works

1. **Source.** The daily [`cfahlgren1/hub-stats`](https://huggingface.co/datasets/cfahlgren1/hub-stats) dump of the Hub's `/api/models` (Apache-2.0), which carries the `base_model` metadata model authors declare in their cards, plus the legacy `base_model:` tags as a fallback.
2. **Graph.** Child → parent edges with the declared relation (`finetune`, `adapter`, `quantized`, `merge`). Merges give a DAG, mis-tagged cards give the occasional cycle (78 nodes today); both are handled.
3. **Counts.** Descendant sets are built children-first and unioned, so every model is counted once per ancestor. `direct` is declared children; `total` is the whole subtree.
4. **Families.** Roots (models that declare no parent) are grouped by a series heuristic over the model name, with overrides in `data/families.yaml`.
5. **Galaxy layout.** Each root's subtree is a radial tree (depth rings sized by population, wedges by subtree size); roots are circle-packed inside their family and families into the galaxy, with a port of d3's front-chain packing. Positions ship as a 10 MB binary, ids load lazily in chunks.
6. **Refresh.** A GitHub Action rebuilds everything nightly, commits `dist/` and `README.md`, and attaches the full node and edge tables plus the galaxy data to the [`data-latest`](https://github.com/h9-tec/model-family-tree/releases/tag/data-latest) release, which the site reads.

### Caveats

- **Declared ancestry only.** 29% of models declare a base. Untagged re-uploads and GGUF conversions without metadata are invisible, so every number is a floor.
- **Activity, not quality.** A base with 30,000 adapters was mostly a tutorial default. Read the finetune-only and 90-day tables alongside the all-time one.
- **Ghost parents.** 4,144 referenced bases are no longer public. They stay in the tree, marked †.
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

*Generated 2026-11-01.*
