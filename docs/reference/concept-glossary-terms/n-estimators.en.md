<a id="n-estimators"></a>

## n_estimators

- Meaning: `n_estimators` is a hyperparameter that sets how many estimators are built in an ensemble. In random forest, it is usually read as the number of trees in the forest. In gradient boosting, it is closer to the number of sequential correction stages or weak learners.
- Why it matters: In random forest, more trees can make the average judgment more stable, but they also increase computation cost. In gradient boosting, more stages give the model more chances to reduce remaining error, but too many stages can increase overfitting risk. `n_estimators` is therefore a handle for model size, correction opportunity, and runtime cost.
- Related concepts: `random forest`, `gradient boosting`, `learning rate`, `ensemble`
- Core Section: `P4-15.1`
- Appears in: `P4-15.1`, `P4-16.1`
