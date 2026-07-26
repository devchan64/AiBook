<a id="query"></a>

## query

- Meaning: A query is the new input currently being compared or predicted. In k-NN, it is compared with stored training examples to find nearby neighbors; in search, it is the reference expression used to retrieve candidates.
- Why it matters: The query separates `the new case being judged` from `the stored reference cases`. With the same training data, changing the query position or representation can change which neighbors are selected and therefore change the result.
- Related concepts: `nearest neighbor`, `distance`, `search`
- Core Section: `P4-12.1`
- Appears in: `P4-12.1`
