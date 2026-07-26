<a id="weak-learner"></a>

## weak learner

- Meaning: A weak learner is a small model that handles a limited role at one stage instead of solving the whole problem strongly by itself. In boosting, it is often explained through a shallow decision tree that reduces the currently remaining error a little.
- Why it matters: Reading weak learner as `a useless model` misses the point of boosting. The key is that each stage has a narrow role, and many stages accumulate into a stronger model. This concept explains why gradient boosting often combines small trees with many correction stages.
- Related concepts: `gradient boosting`, `residual`, `learning rate`
- Core Section: `P4-16.1`
- Appears in: `P4-16.1`, `P4-16.2`
