<a id="regularization"></a>

## regularization

- Meaning: Regularization is the idea of adding constraints or extra costs during learning so a model does not fit only the training data too aggressively. Instead of rewarding only lower training error, the training criterion also makes overly complex or unstable solutions less attractive.
- Why it matters: A model can score well on training data and still fail on new data. Regularization makes learning about both fitting the data and avoiding unnecessarily complex solutions. For example, discouraging very large weights or overly sensitive patterns may slightly reduce training score while improving generalization. This keeps `best training score` from being treated as the same thing as `best model`.
- Related concepts: `overfitting`, `generalization`, `dropout`
- Core Section: `P5-8.1`
- Appears in: `P4-5.1`, `P4-11.5`, `P5-8.2`
