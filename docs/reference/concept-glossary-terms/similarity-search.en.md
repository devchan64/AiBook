<a id="similarity-search"></a>

## similarity search

- Meaning: Similarity search finds vectors near the vector representation of a question or document and selects related candidates. Instead of looking only for exact string matches, it searches a representation space for candidates that are semantically close.
- Why it matters: Similarity search is a core step in RAG because it connects embeddings to an actual retrieval flow. It also shows that keyword search and vector search are not simply rivals; some problems need both to retrieve stable evidence. Its strength is finding nearby meaning candidates rather than only exact wording.
- Related concepts: `embedding`, `retrieval-augmented generation, RAG`, `vector`, `similarity`, `top-k`
- Core Section: `P1-13.2`
- Appears in: `P1-13.3`, `P1-13.4`, `P6-3.1`
