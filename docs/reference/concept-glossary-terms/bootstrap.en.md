<a id="bootstrap"></a>

### bootstrap

- Meaning: A resampling method that creates new sample sets by drawing from the original data with replacement.
- Why it matters: Bootstrap samples make it possible to see how much a model or estimate changes under slightly different samples from the same data. In random forest, each tree sees a different bootstrap sample, which creates diversity among trees.
- Related concepts: `random forest`, `ensemble`, `OOB score`, `sample`
- Core Section: `P4-15.1`
- Appears in: `P4-15.3`, `P4-15.4`
