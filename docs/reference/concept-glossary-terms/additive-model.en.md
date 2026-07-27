<a id="additive-model"></a>

## additive model

- Meaning: An additive model builds the final prediction as the sum of several components. In boosting-style ensembles, the final prediction is made by adding each stage's small correction to the base prediction in sequence.
- Why it matters: The additive-model view lets readers understand sequential correction as `an accumulation of corrections`, not as `a vote among many trees`. That distinction separates correction-based ensembles from methods where independent predictions are gathered at the end.
- Related concepts: `residual`, `ensemble`, `loss function`
- Core Section: `P4-16.1`
- Appears in: `P4-16.1`
