<a id="context-window"></a>

## context window

- Meaning: A context window is the maximum token range a model can keep available during one input-output computation. It is the size of the working memory for the current response, not unlimited memory.
- Why it matters: Long documents, long conversations, and retrieved passages must be selected or summarized to fit the context window. A larger window helps capacity but does not remove the need to choose what matters most.
- Related concepts: `token`, `tokenization`, `retrieval-augmented generation, RAG`
- Core Section: `P6-4.2`
- Appears in: `P6-2.1`, `P6-4.1`
