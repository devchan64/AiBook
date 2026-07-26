<a id="solver"></a>

## solver

- Meaning: A solver is the calculation procedure that actually searches for model parameters after the learning objective has been defined. In logistic regression, it is the implementation choice that repeatedly reduces the objective built from log loss and regularization.
- Why it matters: Even under the same model name, changing the solver can change convergence behavior, supported penalties, and how well the model handles large data or sparse input. A comparison record therefore needs the solver setting, not only the phrase `logistic regression`.
- Related concepts: `logistic regression`, `regularization`, `optimization`
- Core Section: `P4-11.5`
- Appears in: `P4-11.5`
