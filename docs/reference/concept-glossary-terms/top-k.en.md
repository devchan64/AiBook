<a id="top-k"></a>

## top-k

- Meaning: top-k means retrieving not only the single nearest candidate, but the k closest candidates in order. It is closer to making a candidate set to review first than to choosing one final answer.
- Why it matters: Search systems must decide how many related candidates to retrieve. Too few candidates can miss useful evidence, while too many can add noise, review cost, and RAG context-length pressure. Understanding top-k helps readers see retrieval as a design choice about candidate width.
- Related concepts: `nearest neighbor`, `ranking`, `similarity search`, `context window`
- Core Section: `P1-13.2`
- Appears in: `P5-15.3`, `P6-3.2`, `P6-12.2`, `P6-17.1`
