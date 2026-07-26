<a id="token-id"></a>

## token ID

- Meaning: A token ID is the number that points to a tokenizer-created token piece inside a model's vocabulary. It is an identifier for looking up the piece in the internal vocabulary, not the meaning of the visible string.
- Why it matters: An LLM does not compute the source string directly. It receives a sequence of token IDs, turns those IDs into embedding vectors, and then computes with those vectors. This concept prevents token pieces, token count, and token IDs from being mixed together, and keeps readers from treating a larger ID number as a stronger or more important meaning.
- Related concepts: `token`, `tokenization`, `vocabulary`, `embedding`
- Core Section: `P6-2.2`
- Appears in:
