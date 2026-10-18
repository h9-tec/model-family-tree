# LinkedIn post (draft)

Image: `galaxy-square-1600.jpg` (1:1 renders largest in the feed). Alternative: `galaxy-wide-2400x1350.jpg`.

---

This is every open model on Hugging Face that was built from another model. 942,270 of them, in one picture.

Each cluster is a family. Each gold star is a base model. Every dot around it is something someone built on top: a finetune (blue), a LoRA (orange), a quantization (green), a merge (pink).

I built it because the Hub shows you the tree for one model, but nobody shows the whole forest. So I took the daily Hub dump (3.16M models), followed every declared base_model link, and laid the graph out as a galaxy.

Some things you see immediately:

- Qwen2.5 is about to overtake Qwen1.5 as the biggest family. Qwen1.5's lead was never real: 70,000 of its "descendants" are auto-generated LoRAs from 2024.
- FLUX.1-dev is the single most built-on model on the Hub (43,699 descendants), almost all of them LoRAs.
- Count only real finetunes and the picture flips: DistilBERT, Qwen2.5-7B and Llama 3.1-8B lead.
- 3,938 base models that thousands of repos point to are no longer public. They stay in the map as ghosts.

It rebuilds itself every night. There is a leaderboard of the most-descended base models, an explorer that draws any model's pedigree, and an MCP server so your coding agent can ask "what is this model based on?"

Zoom in here: https://h9-tec.github.io/model-family-tree/galaxy.html
Code and data: https://github.com/h9-tec/model-family-tree

#opensource #huggingface #llm #machinelearning #dataviz
