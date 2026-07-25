<a id="brute-force-search"></a>

## brute-force search

- Meaning: Brute-force search compares a query vector directly with every stored vector to find the nearest candidates. It uses no shortcut; it checks the whole candidate set.
- Why it matters: For small data, brute-force search is simple and exact. As the vector collection grows, it shows why search indexes and approximate nearest-neighbor methods become necessary: the number of comparisons grows with the number of stored candidates.
- Related concepts: `search index`, `ANN, approximate nearest neighbor`, `similarity search`
- Core Section: `P1-13.4`
- Appears in: `P1-13.2`
