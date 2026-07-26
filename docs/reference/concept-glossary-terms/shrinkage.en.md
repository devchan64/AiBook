<a id="shrinkage"></a>

## shrinkage

- Meaning: In gradient boosting, shrinkage scales down each weak learner's correction through the learning rate. Instead of adding the whole correction from a new stage, the model adds only a smaller fraction and moves more slowly.
- Why it matters: Boosting keeps reducing remaining error, so a correction that is too strong can quickly follow noise in the training data. Shrinkage slows the correction and helps reduce excessive fitting and overfitting risk. Because a smaller learning rate often needs more stages, it should be read together with `n_estimators`.
- Related concepts: `gradient boosting`, `learning rate`, `overfitting`
- Core Section: `P4-16.2`
- Appears in: `P4-16.2`
