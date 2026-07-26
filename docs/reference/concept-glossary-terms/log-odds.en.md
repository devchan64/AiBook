<a id="log-odds"></a>

### log-odds

- Meaning: Log-odds is the logarithm of the odds \(p/(1-p)\) for probability \(p\). In logistic regression, log-odds connects directly to the linear score \(z\).
- Why it matters: Probability is bounded between 0 and 1, while log-odds can move across negative and positive values, making it easier to connect probability interpretation to a linear formula. It also explains why `probability 0.5`, `odds 1`, `log-odds 0`, and `linear score z = 0` point to the same decision midpoint.
- Related concepts: `logistic regression`, `log loss`, `decision boundary`
- Core Section: `P4-11.3`
- Appears in: `P4-11.4`
