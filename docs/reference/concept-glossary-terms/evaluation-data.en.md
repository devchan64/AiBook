<a id="evaluation-data"></a>

## evaluation data

- Meaning: Evaluation data is data kept out of direct model training and used to check how the trained model behaves. In this entry, the term is used broadly before separating validation data and test data more finely.
- Why it matters: To check whether a model only fits data it has already seen, or whether it can generalize to unseen cases, the check must use data not used for training. The term helps readers avoid mixing the training score with an estimate of new-data performance.
- Related concepts: `training data`, `validation data`, `test data`, `generalization`, `metric`
- Core Section: `P4-4.1`
- Appears in: `P4-4.1`, `P4-4.2`
