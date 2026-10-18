---
name: model-lineage
description: Use when the user asks what a Hugging Face model is based on, what was built on top of a model, which base model to fine-tune from, or how popular a model family is — answers from the Open Model Family Tree MCP tools.
---

# Model lineage

Answers ancestry and popularity questions about open models from the Open Model Family Tree, a nightly build of the whole Hugging Face Hub's declared `base_model` graph.

## When to use

- "What is X based on?" / "Is X a finetune of Llama or Qwen?"
- "What has been built on X?" / "Show me quantizations of X."
- "Which base model should I fine-tune?" / "Which Qwen3 size has the most finetunes?"
- "How big is the Gemma 3 family?" / "Is Llama still the most built-on model?"

## Procedure

1. Ancestry: call `lineage(id="org/name")`. Report the chain root-ward with each hop's relation, and the root's family.
2. Descendants: call `children(id=..., relation=...)`; use `relation="finetune"` when the user cares about real finetunes rather than LoRAs or GGUFs.
3. Popularity: call `leaderboard(kind=...)`. Default to `kind="finetune"` for "which base should I pick" questions (adapter and quantization counts are noisy), `kind="90d"` for "what is hot", `kind="families"` for family comparisons.
4. Families: call `family(name="Qwen2.5")` for one family's totals and top models.
5. If the MCP tools are unavailable, read `${CLAUDE_PLUGIN_ROOT}/dist/leaderboard.json` and `dist/parents.json`.

## Answer format

Lead with the direct answer (the root, or the top 3 bases). Give counts with their kind (total descendants vs finetunes vs last 90 days). Always state that counts cover declared ancestry only and name the build date from `stats()`.
