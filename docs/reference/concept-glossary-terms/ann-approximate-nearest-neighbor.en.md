<a id="ann-approximate-nearest-neighbor"></a>

## ANN, approximate nearest neighbor

- Meaning: Approximate nearest neighbor search finds sufficiently close vector candidates quickly instead of always guaranteeing the exact closest item. It intentionally trades perfect optimality for speed at scale.
- Why it matters: Large vector collections make exact comparison expensive. ANN methods explain why real search systems often prefer fast, good-enough candidates over exact answers that arrive too slowly. This concept connects vector search quality with latency, memory use, and service constraints.
- Related concepts: `nearest neighbor`, `search index`, `vector database`
- Core Section: `P1-13.4`
- Appears in: `P6-3.4`
