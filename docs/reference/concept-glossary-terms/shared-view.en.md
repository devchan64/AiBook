<a id="shared-view"></a>

## shared view

- Meaning: A shared view is a selected result that still refers to the same underlying data as the original array. Changing one side can therefore affect the other.
- Why it matters: A new variable name does not always mean new data. This concept helps readers distinguish memory-efficient views from independent copies, especially when preprocessing code modifies selected array parts.
- Related concepts: `slicing`, `copy`, `boolean mask`
- Core Section: `P2-11.4`
- Appears in: `P2-8.7`
