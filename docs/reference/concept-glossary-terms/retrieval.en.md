<a id="retrieval"></a>

### RAG retrieval

- Meaning: RAG retrieval is the stage that brings in external documents or chunks likely to be relevant to the user's question. It should be read more narrowly than general search or a person's web browsing: it prepares candidate evidence to be placed into the generation input.
- Why it matters: The word retrieval can point to state-space search, document search, web search, or retrieval in RAG. In RAG, retrieval does not directly create the answer; it selects outside material that the generative model may use as additional input context. This distinction makes clear that retrieved results are not automatically the answer.
- Related concepts: `retrieval-augmented generation, RAG`, `information retrieval`, `generation`
- Core Section: `P1-13.3`
- Appears in:
