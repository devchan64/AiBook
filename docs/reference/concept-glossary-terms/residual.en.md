<a id="residual"></a>

## residual

- Meaning: A residual is the remaining difference between the actual value and the current prediction. In a regression context, it is often read as `actual value - current prediction`. In sequential correction models, it is the remaining error signal that the next stage tries to reduce.
- Why it matters: Residuals show both the direction and size of what the model has not explained yet. Sequential correction ensembles reduce that remaining part by adding small learners in order, so residual is the key handle for understanding why the method is described as `the next stage correcting the previous stage`.
- Related concepts: `additive model`, `error`, `ensemble`
- Core Section: `P4-16.1`
- Appears in: `P4-16.1`, `P4-16.2`
