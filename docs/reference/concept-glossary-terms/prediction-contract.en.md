<a id="prediction-contract"></a>
<a id="glossary-prediction-contract"></a>

### prediction contract

- Meaning: An explicit agreement in a prediction problem about which values count as inputs, which result is being predicted, and what information is available up to the prediction time. It includes not only column names, but also when each column is created and whether it can be rebuilt the same way in operations.
- Why it matters: If a value created after prediction time leaks into the inputs, the score may look better while the operational prediction problem is broken. A prediction contract keeps features, target candidates, time boundaries, leakage prevention, and reproducibility checked together.
- Related concepts: `feature`, `target candidate`, `data leakage`, `reproducibility`
- Core Section: `P3-9.7`
- Appears in: `P3-9.7`
