<a id="margin"></a>

## margin

- Meaning: The safety gap between a classification boundary and the closest data cases to that boundary. In the SVM context, it is read as the minimum distance that should be made large among candidate boundaries.
- Why it matters: When several boundaries can separate the same data, separation alone does not tell the reader which boundary is more stable. Margin helps inspect whether the boundary clings too closely to one class and whether small perturbations near the boundary could flip predictions easily.
- Related concepts: `SVM`, `decision boundary`, `classification`, `hyperparameter`
- Core Section: `P4-13.1`
- Appears in: `P4-13.1`
