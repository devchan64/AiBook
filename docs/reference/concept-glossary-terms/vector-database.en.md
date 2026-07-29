<a id="vector-database"></a>

## vector database

- Meaning: A vector database is a retrieval system that stores embedding vectors and manages search indexes, metadata, filtering, and updates together. It is an infrastructure layer for actual search service behavior, not just a place to keep a few vectors.
- Why it matters: RAG implementation depends not only on a vector comparison algorithm, but also on storage, metadata filtering, permissions, updates, and operations. This concept helps readers connect the mathematical problem of finding nearby vectors with the service problem of retrieving safe, fast, current documents.
- Related concepts: `search index`, `ANN, approximate nearest neighbor`, `metadata`
- Core Section: `P6-12.1`
- Appears in: `P1-13.4`, `P6-3.2`, `P6-12.2`
