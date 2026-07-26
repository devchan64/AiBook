<a id="additive-model"></a>

## additive model

- Meaning: An additive model builds the final prediction as the sum of several components. In gradient boosting, the final prediction is made by adding each stage's small correction to the base prediction in sequence.
- Why it matters: The additive-model view lets readers understand gradient boosting as `an accumulation of corrections`, not as `a vote among many trees`. That distinction separates boosting from methods such as random forest, where independent predictions are gathered at the end.
- Related concepts: `gradient boosting`, `residual`, `ensemble`
- Core Section: `P4-16.1`
- Appears in: `P4-16.1`
