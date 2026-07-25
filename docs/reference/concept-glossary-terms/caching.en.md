<a id="caching"></a>

## caching

- Meaning: Caching stores intermediate inputs, lookup results, or computed outputs so they can be reused later instead of recomputed from scratch. It is an operational choice between calculating again and reusing a result that is already available.
- Why it matters: Caching can reduce both cost and latency when the same prompt fragments, retrieval results, or computations recur. It also creates a freshness risk, so it must be read as a balance between performance and recency rather than as a simple speed trick.
- Related concepts: `cost`, `latency`, `batch`
- Core Section: `P1-14.6`
