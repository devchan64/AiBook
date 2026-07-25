<a id="broadcasting"></a>

## broadcasting

- Meaning: Broadcasting is an array computation rule that lets a compatible smaller array or scalar be applied across a larger array. It is better understood as a shape interpretation rule than as manually copying values into a huge array.
- Why it matters: Broadcasting explains how short array expressions can apply values along particular axes without explicit loops. It helps readers debug cases where an operation works syntactically but spreads values along a different axis than expected.
- Related concepts: `vectorization`, `shape`, `scalar`
- Core Section: `P2-11.3`
- Appears in: `P2-11.4`, `P2-12.1`
