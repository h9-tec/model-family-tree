"""Group root models into families ("Qwen2.5", "Llama-3.1", "FLUX.1") by naming heuristics.

The heuristic is deliberately simple and is overridden by `data/families.yaml`, the one
hand-edited file in the repo: map a root id or a series key to the family you want.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

_SIZE = re.compile(r"^(\d+(\.\d+)?[bm]|\d+x\d+(\.\d+)?[bm]|a\d+(\.\d+)?b|\d+(\.\d+)?[bm]-a\d+(\.\d+)?b)$", re.I)
_VERSION_STOP = re.compile(r"^v\d", re.I)
_STOP = {
    "base", "instruct", "it", "chat", "dev", "schnell", "preview", "hf", "gguf", "awq", "gptq", "exl2",
    "sft", "dpo", "rl", "uncensored", "small", "medium", "large", "xl", "xxl", "mini", "tiny", "nano",
    "micro", "turbo", "lite", "pro", "max", "plus", "ultra", "flash", "thinking", "reasoning", "code",
    "uncased", "cased", "multilingual", "en", "zh", "ja", "ko", "ar", "fr", "de", "es", "bf16", "fp16",
    "fp8", "int4", "int8", "4bit", "8bit", "bnb", "quant", "lora", "adapter", "merged", "full", "ckpt",
    "checkpoint", "step", "epoch", "final", "test", "demo", "model", "weights", "safetensors",
}


def series_of(model_id: str) -> str:
    """`Qwen/Qwen2.5-7B-Instruct` -> `qwen2.5`; `google/gemma-2-9b-it` -> `gemma-2`."""
    name = model_id.split("/", 1)[-1]
    tokens = re.split(r"[-_ ]+", name)
    kept: list[str] = []
    for i, tok in enumerate(tokens):
        low = tok.lower()
        if not tok:
            continue
        if i == 0:
            kept.append(low)
            continue
        if _SIZE.match(low) or _VERSION_STOP.match(low) or low in _STOP or re.fullmatch(r"\d{6,}", low):
            break
        if re.fullmatch(r"\d+(\.\d+)*", low) or low.isalpha() or re.fullmatch(r"[a-z]+\d+(\.\d+)*", low):
            kept.append(low)
            continue
        break
    return "-".join(kept) or name.lower()


def load_overrides(path: Path = Path("data/families.yaml")) -> dict:
    if not path.exists():
        return {"roots": {}, "series": {}, "display": {}}
    doc = yaml.safe_load(path.read_text()) or {}
    return {"roots": doc.get("roots") or {}, "series": doc.get("series") or {}, "display": doc.get("display") or {}}


def family_of(model_id: str, overrides: dict | None = None) -> str:
    ov = overrides or {"roots": {}, "series": {}}
    if model_id in ov["roots"]:
        return ov["roots"][model_id]
    s = series_of(model_id)
    return ov["series"].get(s, s)
