<a id="computation-graph"></a>

## computation graph

- Meaning: A computation graph represents operations and value dependencies as connected nodes, making forward and backward calculation paths visible. It breaks a large formula into smaller calculation blocks and their connections.
- Why it matters: Computation graphs make backpropagation and automatic differentiation easier to understand. They show which intermediate values depend on which earlier operations and how gradient signals can flow backward through the graph.
- Related concepts: `backpropagation`, `gradient`, `automatic differentiation`
- Core Section: `P5-5.2`
- Appears in: `P5-6.1`

