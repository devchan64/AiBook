<a id="mean-decrease-in-impurity-mdi"></a>

## mean decrease in impurity(MDI)

- Meaning: MDI assigns each split's impurity decrease to the feature used for that split, then averages those decreases across the forest to produce feature importance.
- Why it matters: It makes `feature_importances_` quick to inspect in a random forest, but it can overestimate high-cardinality features that create many possible training-data splits.
- Related concepts: `feature importance`, `impurity`, `random forest`, `high-cardinality feature`
- Core Section: `P4-15.2`
- Appears in: `P4-15.2`
