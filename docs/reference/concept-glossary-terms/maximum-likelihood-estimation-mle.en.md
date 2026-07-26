<a id="maximum-likelihood-estimation-mle"></a>

### maximum likelihood estimation (MLE)

- Meaning: Maximum likelihood estimation is a way to choose parameters so the observed data are as plausible as possible under the model. For logistic regression, it can first be read as choosing parameters that assign high probability to the correct class.
- Why it matters: It lets classification training be read not only as `how many labels were correct`, but as `how much probability was assigned to the correct answers`. MLE also connects maximizing log-likelihood and minimizing log loss as two directions of the same learning objective.
- Related concepts: `logistic regression`, `log loss`, `likelihood`
- Core Section: `P4-11.3`
- Appears in: `P4-11.4`
