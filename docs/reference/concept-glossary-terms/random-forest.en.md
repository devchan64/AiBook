<a id="random-forest"></a>

## random forest

- Meaning: A random forest is an ensemble model that trains many decision trees with small differences and combines their predictions to produce a more stable result. Each tree sees a somewhat different sample bundle and feature candidates, so the final prediction does not depend too heavily on one tree.
- Why it matters: Random forest is a representative way to reduce the instability of a single decision tree through agreement across many trees. It helps readers understand why a model can trade some direct interpretability for more stable prediction, and how it differs from gradient boosting, which corrects errors sequentially rather than averaging many independently varied trees.
- Related concepts: `decision tree`, `ensemble`, `bootstrap`
- Core Section: `P4-15.1`
- Appears in: `P4-index`, `P4-3.2`, `P4-15.1`, `P4-15.2`, `P4-15.3`
