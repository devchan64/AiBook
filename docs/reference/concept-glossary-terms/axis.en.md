<a id="axis"></a>

## axis

- Meaning: An axis is the direction along which an array operation reads, groups, reduces, or selects values. It is not just a number; it defines the direction of interpretation inside an array.
- Why it matters: The same calculation can produce different shapes and meanings depending on which axis is reduced or preserved. Axis awareness prevents readers from mixing rows with columns, batches with features, or samples with channels. It turns array operations from memorized syntax into questions about direction and structure.
- Related concepts: `indexing`, `slicing`, `shape`
- Core Section: `P2-11.2`
- Appears in: `P2-11.3`, `P2-12.1`, `P2-13.1`, `P2-13.2`, `P2-13.3`
