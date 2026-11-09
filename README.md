<div align="center">

<a href="https://h9-tec.github.io/model-family-tree/galaxy.html"><img src="assets/galaxy.jpg" alt="The Model Galaxy: every Hugging Face model with an ancestor or a descendant, as one zoomable map. Families are clusters, base models are stars, derivatives are the dots around them." width="100%"/></a>

**[Fly through the Model Galaxy →](https://h9-tec.github.io/model-family-tree/galaxy.html)** · 970,111 models in one zoomable WebGL map · **[Explorer →](https://h9-tec.github.io/model-family-tree/)** · search any model, walk its pedigree, share a link.

# Open Model Family Tree

**Every model on the Hugging Face Hub, its ancestry, and a leaderboard of the base models the ecosystem actually builds on. Rebuilt nightly.**

![Models](https://img.shields.io/badge/models-3223k-0A7E8C)
![Links](https://img.shields.io/badge/parent%20links-957k-0A7E8C)
![Updated](https://img.shields.io/badge/updated-2026--11--09-555)
[![Stars](https://img.shields.io/github/stars/h9-tec/model-family-tree?style=flat)](https://github.com/h9-tec/model-family-tree/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

</div>

**3,223,298** models · **923,838** declare a base model (29%) · **957,119** parent links · **91,492** models have descendants · **46,235** roots in **24,724** families

The most built-on model on the Hub is **[black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev)** with **43,710** descendants. In the last 90 days it is **[Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B)** with **5,685** new ones. The biggest family is **Qwen2.5** (71,360).

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
| **[Galaxy](https://h9-tec.github.io/model-family-tree/galaxy.html)** | Every model that has an ancestor or a descendant (970,111 points) in one WebGL map. Families are circle-packed clusters, base models are stars, each derivative is a dot colored by relation and sized by downloads. Scroll to zoom from the whole Hub down to one model, click any dot. |
| **[Explorer](https://h9-tec.github.io/model-family-tree/)** | Type any model id. Its pedigree is drawn as a radial tree: every ancestor path fans out to the left (merges show all parents), the most downloaded descendants to the right, unfoldable level by level, live from the Hub. |
| **[Leaderboard](https://h9-tec.github.io/model-family-tree/#board:all)** | All 91,492 models with descendants, sortable and filterable, plus the curated views below. |

<a href="assets/families.svg"><img src="assets/families.svg" alt="Cumulative descendants per model family over the last 24 months" width="100%"/></a>

## Most-descended base models

Unique descendants of every kind: finetunes, adapters (LoRA), quantizations and merges, each counted once however many paths reach it. † marks a base that was deleted or made private but is still referenced. [Full top 500 →](docs/tables/models_all_time.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) | 43,710 | 43,433 | 227 | 693 / 42,865 / 136 / 16 | FLUX.1 |
| 2 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) | 32,564 | 32,534 | 0 | 41 / 32,475 / 46 / 2 | Qwen1.5 |
| 3 | [Qwen/Qwen1.5-1.8B](https://huggingface.co/Qwen/Qwen1.5-1.8B) | 30,658 | 30,628 | 2 | 36 / 30,591 / 29 / 2 | Qwen1.5 |
| 4 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) | 24,117 | 24,037 | 8 | 311 / 23,706 / 89 / 11 | Gemma 1 |
| 5 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,206 | 2,090 | 2,403 | 12,072 / 6,996 / 3,547 / 591 | Qwen2.5 |
| 6 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,786 | 3,277 | 2,103 | 9,624 / 6,163 / 5,151 / 848 | Llama 3.1 |
| 7 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,340 | 7,405 | 1,502 | 6,919 / 4,088 / 3,617 / 716 | Llama 3.1 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,727 | 6,780 | 1,799 | 8,545 / 3,967 / 1,806 / 409 | Qwen2.5 |
| 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,720 | 13,338 | 739 | 13,168 / 398 / 153 / 1 | DistilBERT |
| 10 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) | 11,620 | 4,014 | 73 | 2,985 / 5,188 / 2,067 / 1,365 | Mistral |
| 11 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) | 11,568 | 11,083 | 219 | 1,423 / 10,037 / 54 / 54 | Stable Diffusion |
| 12 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,366 | 9,029 | 1,689 | 3,595 / 6,557 / 1,123 / 91 | Qwen3 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,309 | 1,078 | 1,815 | 5,121 / 4,247 / 1,778 / 163 | Qwen2.5 |
| 14 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,312 | 1,730 | 96 | 4,241 / 2,072 / 3,011 / 988 | Llama 3 |
| 15 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 10,001 | 205 | 1,634 | 9,003 / 631 / 362 / 5 | SmolLM2 |
| 16 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,918 | 887 | 2,063 | 4,953 / 3,028 / 1,864 / 72 | Qwen3 |
| 17 | [google/gemma-7b](https://huggingface.co/google/gemma-7b) | 9,857 | 9,587 | 6 | 456 / 9,296 / 97 / 8 | Gemma 1 |
| 18 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,852 | 1,391 | 1,121 | 6,087 / 2,337 / 1,368 / 60 | Qwen2.5 |
| 19 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,530 | 411 | 1,592 | 8,839 / 398 / 288 / 5 | SmolLM2 |
| 20 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,814 | 93 | 1,464 | 8,590 / 158 / 66 / 0 | SmolLM2 |
| 21 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,741 | 1,138 | 1,271 | 3,912 / 3,185 / 1,559 / 85 | Qwen2.5 |
| 22 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,712 | 132 | 1,445 | 8,555 / 127 / 30 / 0 | SmolLM2 |
| 23 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,576 | 8,513 | 1,425 | 8,461 / 109 / 6 / 0 | SmolLM2 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,201 | 5,314 | 1,604 | 3,787 / 2,804 / 1,541 / 68 | Qwen3 |
| 25 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,570 | 3,509 | 505 | 3,948 / 1,603 / 1,867 / 152 | Llama 3.2 |

## Hot right now: new descendants in the last 90 days

[Full top 500 →](docs/tables/models_90d.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) | 5,694 | 2,881 | 5,685 | 1,274 / 471 / 3,886 / 63 | Qwen3.8 |
| 2 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) | 6,809 | 799 | 3,507 | 2,689 / 1,535 / 2,478 / 107 | Qwen3.5 |
| 3 | [Qwen/Qwen3.5-4B-Base](https://huggingface.co/Qwen/Qwen3.5-4B-Base) | 5,665 | 462 | 3,305 | 2,194 / 1,593 / 1,827 / 51 | Qwen3.5 |
| 4 | [Qwen/Qwen3.5-4B](https://huggingface.co/Qwen/Qwen3.5-4B) | 5,015 | 2,998 | 2,868 | 1,857 / 1,423 / 1,689 / 46 | Qwen3.5 |
| 5 | [Qwen/Qwen3.5-9B](https://huggingface.co/Qwen/Qwen3.5-9B) | 5,646 | 3,069 | 2,821 | 1,877 / 1,426 / 2,239 / 104 | Qwen3.5 |
| 6 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,206 | 2,090 | 2,403 | 12,072 / 6,996 / 3,547 / 591 | Qwen2.5 |
| 7 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,786 | 3,277 | 2,103 | 9,624 / 6,163 / 5,151 / 848 | Llama 3.1 |
| 8 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,918 | 887 | 2,063 | 4,953 / 3,028 / 1,864 / 72 | Qwen3 |
| 9 | [Qwen/Qwen3.5-0.8B-Base](https://huggingface.co/Qwen/Qwen3.5-0.8B-Base) | 3,276 | 292 | 1,920 | 1,228 / 1,004 / 1,034 / 10 | Qwen3.5 |
| 10 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,309 | 1,078 | 1,815 | 5,121 / 4,247 / 1,778 / 163 | Qwen2.5 |
| 11 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,727 | 6,780 | 1,799 | 8,545 / 3,967 / 1,806 / 409 | Qwen2.5 |
| 12 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,366 | 9,029 | 1,689 | 3,595 / 6,557 / 1,123 / 91 | Qwen3 |
| 13 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,861 | 959 | 1,683 | 3,961 / 1,062 / 1,813 / 25 | Qwen3 |
| 14 | [Qwen/Qwen3.5-0.8B](https://huggingface.co/Qwen/Qwen3.5-0.8B) | 2,830 | 1,878 | 1,650 | 1,036 / 916 / 870 / 8 | Qwen3.5 |
| 15 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 10,001 | 205 | 1,634 | 9,003 / 631 / 362 / 5 | SmolLM2 |
| 16 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,201 | 5,314 | 1,604 | 3,787 / 2,804 / 1,541 / 68 | Qwen3 |
| 17 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,530 | 411 | 1,592 | 8,839 / 398 / 288 / 5 | SmolLM2 |
| 18 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,340 | 7,405 | 1,502 | 6,919 / 4,088 / 3,617 / 716 | Llama 3.1 |
| 19 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,814 | 93 | 1,464 | 8,590 / 158 / 66 / 0 | SmolLM2 |
| 20 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,712 | 132 | 1,445 | 8,555 / 127 / 30 / 0 | SmolLM2 |
| 21 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,576 | 8,513 | 1,425 | 8,461 / 109 / 6 / 0 | SmolLM2 |
| 22 | [Qwen/Qwen3-1.7B-Base](https://huggingface.co/Qwen/Qwen3-1.7B-Base) | 5,218 | 655 | 1,334 | 2,884 / 1,099 / 1,215 / 20 | Qwen3 |
| 23 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,741 | 1,138 | 1,271 | 3,912 / 3,185 / 1,559 / 85 | Qwen2.5 |
| 24 | [Qwen/Qwen3-4B-Base](https://huggingface.co/Qwen/Qwen3-4B-Base) | 6,949 | 736 | 1,269 | 3,510 / 1,696 / 1,650 / 93 | Qwen3 |
| 25 | [Qwen/Qwen3.5-2B-Base](https://huggingface.co/Qwen/Qwen3.5-2B-Base) | 2,489 | 209 | 1,269 | 1,139 / 526 / 818 / 6 | Qwen3.5 |

## Finetunes only

Adapters and quantizations inflate the all-time table (tens of thousands of auto-generated LoRAs sit on a few small bases). This view counts descendants whose own relation to their parent is `finetune`. [Full top 500 →](docs/tables/models_finetune.md)

| # | Model | Descendants | Direct | Last 90d | Finetune / adapter / quantized / merge | Family |
|---:|---|---:|---:|---:|---|---|
| 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) | 13,720 | 13,338 | 739 | 13,168 / 398 / 153 / 1 | DistilBERT |
| 2 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) | 23,206 | 2,090 | 2,403 | 12,072 / 6,996 / 3,547 / 591 | Qwen2.5 |
| 3 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) | 21,786 | 3,277 | 2,103 | 9,624 / 6,163 / 5,151 / 848 | Llama 3.1 |
| 4 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) | 10,001 | 205 | 1,634 | 9,003 / 631 / 362 / 5 | SmolLM2 |
| 5 | [HuggingFaceTB/SmolLM2-360M-Instruct](https://huggingface.co/HuggingFaceTB/SmolLM2-360M-Instruct) | 9,530 | 411 | 1,592 | 8,839 / 398 / 288 / 5 | SmolLM2 |
| 6 | [HuggingFaceTB/SmolVLM-500M-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM-500M-Instruct) | 8,814 | 93 | 1,464 | 8,590 / 158 / 66 / 0 | SmolLM2 |
| 7 | [HuggingFaceTB/SmolVLM2-500M-Video-Instruct](https://huggingface.co/HuggingFaceTB/SmolVLM2-500M-Video-Instruct) | 8,712 | 132 | 1,445 | 8,555 / 127 / 30 / 0 | SmolLM2 |
| 8 | [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) | 14,727 | 6,780 | 1,799 | 8,545 / 3,967 / 1,806 / 409 | Qwen2.5 |
| 9 | [lerobot/smolvla_base](https://huggingface.co/lerobot/smolvla_base) | 8,576 | 8,513 | 1,425 | 8,461 / 109 / 6 / 0 | SmolLM2 |
| 10 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) | 7,513 | 7,268 | 288 | 7,277 / 147 / 82 / 7 | BERT |
| 11 | [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) | 15,340 | 7,405 | 1,502 | 6,919 / 4,088 / 3,617 / 716 | Llama 3.1 |
| 12 | [Qwen/Qwen2.5-0.5B](https://huggingface.co/Qwen/Qwen2.5-0.5B) | 9,852 | 1,391 | 1,121 | 6,087 / 2,337 / 1,368 / 60 | Qwen2.5 |
| 13 | [Qwen/Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | 11,309 | 1,078 | 1,815 | 5,121 / 4,247 / 1,778 / 163 | Qwen2.5 |
| 14 | [Qwen/Qwen3-8B-Base](https://huggingface.co/Qwen/Qwen3-8B-Base) | 9,918 | 887 | 2,063 | 4,953 / 3,028 / 1,864 / 72 | Qwen3 |
| 15 | [unsloth/Qwen2.5-7B-Instruct](https://huggingface.co/unsloth/Qwen2.5-7B-Instruct) | 5,468 | 5,426 | 617 | 4,664 / 772 / 30 / 2 | Qwen2.5 |
| 16 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) | 4,792 | 4,429 | 213 | 4,590 / 79 / 122 / 0 | XLM-RoBERTa |
| 17 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) | 6,756 | 397 | 493 | 4,556 / 974 / 1,210 / 16 | Gemma 3 |
| 18 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) | 10,312 | 1,730 | 96 | 4,241 / 2,072 / 3,011 / 988 | Llama 3 |
| 19 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) | 4,801 | 4,453 | 348 | 4,110 / 354 / 337 / 0 | Whisper |
| 20 | [aubmindlab/bert-base-arabertv02](https://huggingface.co/aubmindlab/bert-base-arabertv02) | 4,115 | 4,059 | 13 | 4,105 / 5 / 5 / 0 | BERT |
| 21 | [Qwen/Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | 6,861 | 959 | 1,683 | 3,961 / 1,062 / 1,813 / 25 | Qwen3 |
| 22 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) | 7,570 | 3,509 | 505 | 3,948 / 1,603 / 1,867 / 152 | Llama 3.2 |
| 23 | [Qwen/Qwen2.5-3B](https://huggingface.co/Qwen/Qwen2.5-3B) | 8,741 | 1,138 | 1,271 | 3,912 / 3,185 / 1,559 / 85 | Qwen2.5 |
| 24 | [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B) | 8,201 | 5,314 | 1,604 | 3,787 / 2,804 / 1,541 / 68 | Qwen3 |
| 25 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) | 11,366 | 9,029 | 1,689 | 3,595 / 6,557 / 1,123 / 91 | Qwen3 |

## Families

Roots grouped by series name across organizations (so `unsloth/Llama-3.1-8B` re-uploads count toward Llama 3.1). Grouping is a heuristic with hand overrides in [`data/families.yaml`](data/families.yaml); PRs welcome. [Full table →](docs/tables/families.md)

<a href="assets/monthly.svg"><img src="assets/monthly.svg" alt="New derivatives per month for the top families" width="100%"/></a>

| # | Family | Descendants | Last 90d | Roots | Finetune / adapter / quantized / merge | Biggest root |
|---:|---|---:|---:|---:|---|---|
| 1 | **Qwen2.5** | 71,360 | 7,752 | 690 | 34,427 / 20,450 / 14,847 / 1,636 | [Qwen/Qwen2.5-7B](https://huggingface.co/Qwen/Qwen2.5-7B) |
| 2 | **Qwen1.5** | 71,026 | 10 | 44 | 225 / 70,436 / 349 / 16 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 3 | **Qwen3** | 56,403 | 10,443 | 652 | 25,192 / 17,483 / 13,295 / 431 | [Qwen/Qwen3-4B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507) |
| 4 | **FLUX.1** | 44,174 | 255 | 16 | 787 / 43,170 / 200 / 17 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | **Gemma 1** | 37,081 | 59 | 184 | 1,758 / 34,366 / 889 / 68 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 6 | **Mistral** | 36,615 | 974 | 584 | 10,680 / 11,256 / 11,730 / 2,933 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 7 | **Llama 3.1** | 28,399 | 2,277 | 222 | 11,156 / 7,056 / 8,243 / 1,944 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 8 | **Llama 3** | 24,268 | 432 | 545 | 8,145 / 5,868 / 7,793 / 2,462 | [meta-llama/Meta-Llama-3-8B](https://huggingface.co/meta-llama/Meta-Llama-3-8B) |
| 9 | **BERT** | 23,351 | 677 | 306 | 22,545 / 508 / 290 / 8 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 10 | **Qwen3.5** | 22,086 | 10,807 | 156 | 8,372 / 5,126 / 8,343 / 244 | [Qwen/Qwen3.5-9B-Base](https://huggingface.co/Qwen/Qwen3.5-9B-Base) |
| 11 | **Llama 3.2** | 21,144 | 1,160 | 477 | 9,746 / 5,670 / 5,132 / 596 | [meta-llama/Llama-3.2-3B-Instruct](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) |
| 12 | **Gemma 3** | 18,323 | 1,247 | 141 | 10,651 / 3,038 / 4,415 / 219 | [google/gemma-3-4b-pt](https://huggingface.co/google/gemma-3-4b-pt) |
| 13 | **Stable Diffusion** | 18,025 | 447 | 30 | 3,433 / 14,409 / 109 / 74 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 14 | **Whisper** | 15,888 | 1,645 | 205 | 11,746 / 2,356 / 1,779 / 7 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 15 | **DistilBERT** | 15,306 | 797 | 81 | 14,523 / 498 / 284 / 1 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 16 | **SmolLM2** | 13,985 | 2,029 | 60 | 11,147 / 1,654 / 1,164 / 20 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 17 | **Gemma 2** | 12,376 | 357 | 226 | 5,098 / 3,187 / 3,149 / 942 | [google/gemma-2-9b](https://huggingface.co/google/gemma-2-9b) |
| 18 | **Gemma 4** | 12,076 | 4,203 | 136 | 3,616 / 2,184 / 6,096 / 180 | [google/gemma-4-E4B](https://huggingface.co/google/gemma-4-E4B) |
| 19 | **Llama 2** | 11,633 | 260 | 412 | 2,971 / 7,075 / 1,374 / 213 | [meta-llama/Llama-2-7b-hf](https://huggingface.co/meta-llama/Llama-2-7b-hf) |
| 20 | **Qwen2** | 10,805 | 173 | 161 | 3,184 / 6,045 / 1,488 / 88 | [Qwen/Qwen2-0.5B](https://huggingface.co/Qwen/Qwen2-0.5B) |
| 21 | **DeepSeek-R1** | 9,113 | 577 | 130 | 2,876 / 1,530 / 3,811 / 896 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 22 | **Qwen3.8** | 7,162 | 7,147 | 70 | 1,498 / 484 / 5,099 / 81 | [Qwen/Qwen3.8-27B](https://huggingface.co/Qwen/Qwen3.8-27B) |
| 23 | **XLM-RoBERTa** | 6,425 | 357 | 49 | 6,101 / 138 / 185 / 0 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |
| 24 | **Qwen3.6** | 6,221 | 1,850 | 55 | 1,185 / 1,175 / 3,759 / 95 | [Qwen/Qwen3.6-35B-A3B](https://huggingface.co/Qwen/Qwen3.6-35B-A3B) |
| 25 | **ViT** | 6,140 | 179 | 72 | 5,247 / 753 / 140 / 0 | [google/vit-base-patch16-224-in21k](https://huggingface.co/google/vit-base-patch16-224-in21k) |

## Organizations

Descendants of every root owned by the organization, deduplicated. [Full table →](docs/tables/orgs.md)

| # | Organization | Descendants of its roots | Last 90d | Roots | Biggest root |
|---:|---|---:|---:|---:|---|
| 1 | [Qwen](https://huggingface.co/Qwen) | 243,072 | 39,036 | 148 | [Qwen/Qwen1.5-0.5B](https://huggingface.co/Qwen/Qwen1.5-0.5B) |
| 2 | [google](https://huggingface.co/google) | 93,336 | 7,517 | 327 | [google/gemma-2b](https://huggingface.co/google/gemma-2b) |
| 3 | [meta-llama](https://huggingface.co/meta-llama) | 69,177 | 3,956 | 51 | [meta-llama/Llama-3.1-8B](https://huggingface.co/meta-llama/Llama-3.1-8B) |
| 4 | [black-forest-labs](https://huggingface.co/black-forest-labs) | 46,229 | 770 | 20 | [black-forest-labs/FLUX.1-dev](https://huggingface.co/black-forest-labs/FLUX.1-dev) |
| 5 | [mistralai](https://huggingface.co/mistralai) | 32,960 | 1,332 | 33 | [mistralai/Mistral-7B-v0.1](https://huggingface.co/mistralai/Mistral-7B-v0.1) |
| 6 | [unsloth](https://huggingface.co/unsloth) | 24,258 | 319 | 269 | [unsloth/llama-3-8b-Instruct-bnb-4bit](https://huggingface.co/unsloth/llama-3-8b-Instruct-bnb-4bit) |
| 7 | [microsoft](https://huggingface.co/microsoft) | 22,563 | 1,148 | 256 | [microsoft/Phi-3-mini-4k-instruct](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) |
| 8 | [openai](https://huggingface.co/openai) | 19,692 | 2,041 | 21 | [openai/whisper-small](https://huggingface.co/openai/whisper-small) |
| 9 | [facebook](https://huggingface.co/facebook) | 17,970 | 1,279 | 507 | [facebook/wav2vec2-base](https://huggingface.co/facebook/wav2vec2-base) |
| 10 | [distilbert](https://huggingface.co/distilbert) | 17,659 | 922 | 9 | [distilbert/distilbert-base-uncased](https://huggingface.co/distilbert/distilbert-base-uncased) |
| 11 | [HuggingFaceTB](https://huggingface.co/HuggingFaceTB) | 16,657 | 2,237 | 29 | [HuggingFaceTB/SmolLM2-360M](https://huggingface.co/HuggingFaceTB/SmolLM2-360M) |
| 12 | [stabilityai](https://huggingface.co/stabilityai) | 15,321 | 328 | 73 | [stabilityai/stable-diffusion-xl-base-1.0](https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0) |
| 13 | [google-bert](https://huggingface.co/google-bert) | 14,773 | 407 | 12 | [google-bert/bert-base-uncased](https://huggingface.co/google-bert/bert-base-uncased) |
| 14 | [deepseek-ai](https://huggingface.co/deepseek-ai) | 14,658 | 1,600 | 78 | [deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B](https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B) |
| 15 | [FacebookAI](https://huggingface.co/FacebookAI) | 10,036 | 498 | 19 | [FacebookAI/xlm-roberta-base](https://huggingface.co/FacebookAI/xlm-roberta-base) |

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
- **Ghost parents.** 4,209 referenced bases are no longer public. They stay in the tree, marked †.
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

*Generated 2026-11-09.*
