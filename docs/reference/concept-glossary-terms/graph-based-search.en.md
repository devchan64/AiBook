<a id="graph-based-search"></a>

## graph-based search

- Meaning: Graph-based search stores nearby vectors or candidates as connected nodes and follows those connections to narrow the search. Instead of comparing everything every time, it moves through promising neighborhoods.
- Why it matters: This is a core intuition behind scalable approximate nearest-neighbor search. A search index is not just storage; it is a structure for reaching likely candidates faster than brute-force comparison.
- Related concepts: `graph`, `ANN, approximate nearest neighbor`, `search index`, `brute-force search`
- Core Section: `P1-13.4`
- Appears in: `P1-13.3`, `P6-3.4`, `P6-12.2`
