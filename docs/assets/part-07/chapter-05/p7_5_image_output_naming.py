"""Stable output names for Part 7 Chapter 5 image-generation candidates."""

from __future__ import annotations

from hashlib import sha256
import json


def candidate_stem(prefix: str, *, seed: int, steps: int, contract: object) -> str:
    """Return a deterministic candidate stem with contract hash, seed, and diffusion steps."""
    encoded = json.dumps(contract, ensure_ascii=False, sort_keys=True, separators=(",", ":"), default=str)
    digest = sha256(encoded.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-hash-{digest}-seed-{seed}-steps-{steps}"
