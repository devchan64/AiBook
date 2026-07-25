<a id="copy"></a>

## copy

- Meaning: A copy is a new data object separated from the original so later changes do not directly modify the source. The key question is whether a new object was actually made, not whether a new name was assigned.
- Why it matters: In NumPy and data preprocessing, slicing, fancy indexing, and boolean masks can relate to the original data differently. Understanding copies prevents accidental source modification while also making memory cost visible.
- Related concepts: `shared underlying object`, `boolean mask`, `fancy indexing`
- Core Section: `P2-11.4`
- Appears in: `P2-8.7`, `P2-12.1`

