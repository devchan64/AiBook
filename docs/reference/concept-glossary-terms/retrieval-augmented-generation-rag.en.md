<a id="retrieval-augmented-generation-rag"></a>

## retrieval-augmented generation, RAG

- Meaning: Retrieval-augmented generation, or RAG, is a structure that first retrieves external material related to a question, attaches that material to the model input context, and then generates an answer. The key point is that retrieval and generation are separate stages, letting the model use both what it learned in its parameters and the evidence just retrieved.
- Why it matters: RAG is a representative way to reduce the limits of answering only from internal model parameters and to ground responses in current material or organization documents. It also shows that answer quality can fail if retrieval quality, chunk design, or source tracking is weak, even when the generation step sounds fluent.
- Related concepts: `embedding`, `similarity search`, `retrieval`, `provenance`, `search index`
- Core Section: `P1-13.3`
- Appears in: `P1-14.1`, `P1-14.2`, `P1-14.3`, `P6-4.2`, `P6-10.3`, `P6-12.1`, `P6-12.2`, `P6-13.1`, `P7-5.1`, `P7-5.2`
