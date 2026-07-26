# P3-9.7 Under What Conditions Can Inputs and Results Be Read as a Prediction Problem

> Section ID: `P3-9.7`
> Version: `v2026.07.25`

Once you decide to raise the problem into a prediction problem, you now need to close whether its structure satisfies an actual [prediction contract](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-prediction-contract). What matters is not a long theory but four checks: which columns are inputs, which columns are result candidates, whether information from after the prediction time has leaked in, and up to what information you look while predicting a result from what time point.

This section closes four things first: the split between inputs and results, leakage prevention, reproducibility at the operating time point, and the time boundary.

| What should be closed first | If turned into a question |
| --- | --- |
| Split between inputs and results | Which columns are [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) and which are [target candidates](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-candidate)? |
| Preventing future-information leakage | Is there no [data leakage](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-data-leakage) from values still unknown at prediction time? |
| Reproducibility at the operating time point | Can the inputs built during training be rebuilt in operations by the same rule? |
| Cutoff / horizon | Up to what information do you look, and what later result are you trying to predict? |

## One Scene at a Time

Even with the same event table, the structure breaks immediately if `columns knowable before prediction` and `columns created after prediction` are mixed together as below.

| event_id | recent_diff | repeatability | review_result | target_candidate |
| --- | --- | --- | --- | --- |
| A | -0.32 | high | manual_reviewed | review_needed |
| B | -0.06 | low | skipped | normal |

Here, `recent_diff` and `repeatability` are columns that can be built before prediction. By contrast, `review_result` appears only after a person has already completed the review. If that column is placed together with the inputs, the table may still look normal in shape, but in reality it becomes a structure in which `the inputs were built after looking at the answer`. In that case, even if the score is high during training, the model is effectively using information that does not exist at the real prediction time, so it is no longer the same problem.

The next example checks this difference through actual model output. `available_at_cutoff` uses only columns that can be made at prediction time, while `leaky_after_review` uses only `review_result_code`, which is created after prediction. Even if the second model looks better, it breaks the prediction contract because the column is unavailable in operations.

Problem situation: We want to see how model scores look different when we compare inputs available at prediction time with a leaky input created after prediction.

Input: `recent_diff`, `repeatability`, `review_result_code`, and `target`.

Expected output: The columns used by each feature set, test accuracy, and prediction/actual comparison.

Concept to check: If a column created after prediction is put into the inputs, the score may look better, but the structure is not a valid operational prediction problem.

```python
# This example checks the difference between prediction-time inputs and a leaky post-review column.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

records = pd.DataFrame(
    [
        {"event_id": "A", "recent_diff": -0.32, "repeatability": 3, "review_result_code": 1, "target": 1},
        {"event_id": "B", "recent_diff": -0.06, "repeatability": 1, "review_result_code": 0, "target": 0},
        {"event_id": "C", "recent_diff": -0.28, "repeatability": 2, "review_result_code": 1, "target": 1},
        {"event_id": "D", "recent_diff": -0.04, "repeatability": 1, "review_result_code": 0, "target": 0},
        {"event_id": "E", "recent_diff": -0.18, "repeatability": 1, "review_result_code": 1, "target": 1},
        {"event_id": "F", "recent_diff": -0.12, "repeatability": 3, "review_result_code": 0, "target": 0},
    ]
)

train = records.iloc[:4]
test = records.iloc[4:]
feature_sets = {
    "available_at_cutoff": ["recent_diff", "repeatability"],
    "leaky_after_review": ["review_result_code"],
}

for name, columns in feature_sets.items():
    model = DecisionTreeClassifier(random_state=0, max_depth=2)
    model.fit(train[columns], train["target"])
    predicted = model.predict(test[columns])
    comparison = [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predicted, test["target"])
    ]
    print(name, "features:", columns)
    print(name, "accuracy:", accuracy_score(test["target"], predicted))
    print(name, "predictions:", comparison)
```

Expected output:

```text
available_at_cutoff features: ['recent_diff', 'repeatability']
available_at_cutoff accuracy: 0.0
available_at_cutoff predictions: [('E', 0, 1), ('F', 1, 0)]
leaky_after_review features: ['review_result_code']
leaky_after_review accuracy: 1.0
leaky_after_review predictions: [('E', 1, 1), ('F', 0, 0)]
```

`leaky_after_review` has accuracy `1.0`, but this should not be read as a good prediction problem. `review_result_code` is created only after a person has already completed the review. At the real operating prediction time, that value is still unknown. So the point of this example is not to find a high-scoring model, but to close first whether this column can actually be made at prediction time.

## A Small Diagram

The input/result contract does not end with `separate the columns`. It must also close in the order below so that only values available at prediction time remain.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-7-mermaid-01-en.mmd"
```

So closing the input/result contract is not only a matter of `splitting column names`. You must also write down `when each column is created`. For one sample input row to be valid, all values in that row must be values that can actually be produced at the same prediction time.

Even when the same sample boundary is kept, the input representation does not need to stay fixed as only one form. In some cases, a one-row feature vector is more natural. In others, a grouped input that preserves time order is more natural. What matters is that regardless of representation style, the contract `is this an input that can actually be used at prediction time` and `is the result candidate closed together with the time boundary` must be satisfied first. What is being handled here is therefore not `just any table`, but an input structure whose sample boundary and time boundary are closed. The core is not `passing along a table`, but `closing the input/result contract that holds at prediction time`. More broadly, what gets closed here is a prediction contract in which `input definition`, `result definition`, `time-point availability`, and `reproducibility` all match together.

## Sources and References

- Google, *Machine Learning Glossary*, `feature`, `label`, `label leakage`. Used to check the term basis that features are model input variables and that label leakage is a design flaw in which a label proxy is mixed into the features. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Datasets: Dividing the original dataset*. Used to check the view that train/validation/test data should be separated, the same feature transformation should also apply to real-world data, and validation/test data should match the real-world data the model will encounter. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
