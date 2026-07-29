<a id="token"></a>

## token

- Meaning: A token is the basic computational unit into which a model splits text for processing. It is not always the same as a word: one word can split into several tokens, and several short expressions can sometimes be handled as one piece. A sentence that looks continuous to a person becomes a sequence of tokens inside the model.
- Why it matters: Readers need this distinction because the units people read and the units a model computes over can differ. Cost, context-window limits, and token coverage all begin from this computational unit. Understanding tokens also explains why prompt design and context limits must be judged by token count rather than by character count alone.
- Related concepts: `next-token prediction`, `language modeling`, `embedding`, `tokenization`, `context window`
- Core Section: `P6-2.1`
- Appears in: `P1-10.2`, `P5-13.1`, `P5-13.2`, `P6-2.1`, `P6-2.2`, `P6-2.3`, `P6-2.4`, `P6-2.5`, `P7-4.1`, `P7-4.2`
