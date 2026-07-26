<a id="gradient-boosting"></a>

## gradient boosting

- Meaning: Gradient boosting is an ensemble method that builds models sequentially so each new model corrects errors left by the previous ones. In practice, it often adds small decision trees step by step to reduce remaining residuals.
- Why it matters: Gradient boosting is a strong candidate for many tabular-data problems, but it is also sensitive to tuning and overfitting. It shows that ensembles can work by sequential correction, not only by training many independent models and averaging them.
- Related concepts: `ensemble`, `residual`, `hyperparameter`
- Core Section: `P4-16.1`
- Appears in: `P4-3.2`, `P4-16.2`
