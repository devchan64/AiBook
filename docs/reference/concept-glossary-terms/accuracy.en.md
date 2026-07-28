<a id="accuracy"></a>

## accuracy

- Meaning: Accuracy is the fraction of predictions that are correct: correct predictions divided by all predictions. It is one of the most intuitive metrics for classification because it quickly summarizes how often a model chose the right answer.
- Why it matters: Accuracy is useful as a first check, but it can hide important failure patterns. With imbalanced data, a model can look accurate while ignoring rare but important cases. Readers should treat accuracy as a starting point and then ask what kinds of mistakes remain, whether some errors cost more than others, and whether other metrics are needed.
- Related concepts: `loss curve`, `model validation`, `test data`
- Core Section: `P2-13.3`
- Appears in: `P2-13.3`, `P4-4.2`, `P4-5.1`, `P4-6.1`, `P4-6.4`
