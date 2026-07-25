<a id="kv-cache"></a>

## KV cache

- Meaning: A KV cache stores previously computed key and value representations for earlier tokens so they can be reused during later token generation instead of recomputed from scratch.
- Why it matters: Long-context generation can become slow if every step recalculates the whole past context. KV cache connects generation speed and cost to how a system reuses previous computation.
- Related concepts: `query-key-value, QKV`, `context window`, `long-context`
- Core Section: `P6-4.3`
- Appears in: `P5-14.2`
