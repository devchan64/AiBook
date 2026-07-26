<a id="subsampling"></a>

## subsampling

- Meaning: Subsampling uses only part of the available samples for a learning or correction step. In gradient boosting, it can train each stage's base learner on a subset of the training data so every stage does not fit the full dataset exactly.
- Why it matters: If every stage reacts too tightly to the full training data, the model can keep following accidental patterns. Subsampling injects randomness into stage-wise correction and helps soften variance and overfitting risk.
- Related concepts: `gradient boosting`, `overfitting`, `variance`
- Core Section: `P4-16.2`
- Appears in: `P4-16.2`
