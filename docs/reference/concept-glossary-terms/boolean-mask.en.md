<a id="boolean-mask"></a>

## boolean mask

- Meaning: A boolean mask selects values by using a true-or-false array of the same length or compatible shape. Instead of naming positions directly, it first evaluates a condition and then keeps the elements where the condition is true.
- Why it matters: Boolean masks support condition-based selection in preprocessing and array work. They differ from simple slicing because the result shape and copying behavior can change, so readers need to understand them before interpreting filtered samples or conditional array operations.
- Related concepts: `filtering`, `fancy indexing`, `copy`
- Core Section: `P2-11.4`
- Appears in: `P2-12.2`
