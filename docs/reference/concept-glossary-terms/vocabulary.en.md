<a id="vocabulary"></a>

## vocabulary

- Meaning: A tokenizer vocabulary is the internal list of token pieces that a tokenizer can produce and the IDs assigned to those pieces. In this context, vocabulary is not a human dictionary; it is a computational lookup table for model input pieces.
- Why it matters: The same source string can become different token pieces, token counts, and token IDs depending on the vocabulary and splitting rules. This concept helps readers treat token IDs as vocabulary item numbers, not definitions, and explains why tokenizer choice affects cost and context length.
- Related concepts: `token`, `tokenization`, `token ID`, `embedding`
- Core Section: `P6-2.2`
- Appears in: `P6-2.2`, `P6-2.5`, `P7-4.1`
