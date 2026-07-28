# P3-4.2 What Else Starts to Drift When the Sample Unit Drifts

> Section ID: `P3-4.2`
> Version: `v2026.07.25`

The [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) unit is the reference point for almost every concept that appears later. So if measurements and samples are confused, the problem does not end with using one term incorrectly. The meaning of a [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) drifts, the meaning of a [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) drifts, and even what [evaluation](/AiBook/en/reference/concept-glossary-alpha/e/#glossary-evaluation) is evaluating drifts along with them. If the previous section decided what should count as one sample, then this section must show what that decision fixes together and what starts to drift together.

This section does not redefine the sample unit itself. Instead, it focuses on following why the sample unit fixed in the previous section also affects later features, labels, splits, and evaluation.

Let us begin from the most common confusion. Suppose there is a time-series table measured at 1-second intervals during an action. In many cases, one row of this table is accepted as `one sample` as it is. Then current values such as pressure, flow, and temperature begin to be attached immediately as if they were features. But if what we actually want to know is `did this action have a different structure from the usual one?`, then one time-point row is not the sample that answers that question.

The problem can be organized point by point.

## 1. The Meaning of Features Drifts

If one full action is taken as the sample, then values such as total action time, early-stage mean, late-stage drop rate, and variability can become features. But if one time-point row is taken as the sample, then the same columns either cannot yet be calculated, or even if they are calculated, their meaning remains incomplete on that single row.

## 2. The Meaning of Labels Drifts

If an operational label is `needs review`, that label usually attaches not to one measurement point, but to one full action or a recent segment. But once one time-point row is read as the sample, even the question of which row the label should attach to becomes ambiguous.

## 3. The Evaluation Unit Drifts

If one full action is the sample, then learning and evaluation should also happen at the action level. But if one time-point row is treated as if it were the sample, then nearby rows from the same action can easily be mixed into both training and evaluation.

## 4. Operational Interpretation Drifts

Operators usually want to know not `what was the number at one time point`, but `what was the whole action like`. But if measurements and samples are confused, the operational question and the data structure stop matching.

When these four problems are seen together, it becomes clearer why the sample unit is not just a vocabulary issue.

A short operating scene makes this even clearer. Suppose an automatic cleaning action on a production line is repeated hundreds of times a day. The question that operators actually ask is usually not `was the flow normal at 12:03:01?`, but something closer to `was the cleaning cycle that just ended more unstable than usual?` or `has the same anomaly repeated during the most recent 30 minutes?` But once one time-point row is taken as the sample, the operational question points to one full action while the [dataset](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-dataset) points to second-by-second records. From that moment on, features become sliced too finely, labels are copied repeatedly, and evaluation starts to diverge from the real operational judgment unit.

| What drifts | Why it drifts together |
| --- | --- |
| Feature | Because what has to be summarized depends on the sample unit |
| Label | Because what result attaches to one case depends on the sample unit |
| Split and evaluation | Because what gets divided into training and evaluation depends on the sample unit |
| Operational sentence | Because what a person reads as one case depends on the sample unit |

Here the mismatch of the sample unit becomes clearer if we divide the `misattached questions` from the `questions that should be attached again`.

| Misattached question | Why it is misaligned | The question that should be attached again |
| --- | --- | --- |
| Is this one row normal? | One row is only a time-point record and may not represent the whole action | Does this one full action have a different structure from the usual one? |
| Can I attach the label to this row? | Labels usually attach to one action or one recent segment | Does the label attach to one time point or one full action? |
| Can this row be used as one training case? | Nearby rows from the same action can be mixed into training and evaluation | Is the split target a time-point row, or an action-level sample? |

So the sample unit is not a decision needed only in one section of Part 3. It is the floor structure on which feature engineering, [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) comparison, the [review queue](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-review-queue), and even the interpretation of the prediction input structure all depend.

## A Small Diagram

The core point of the previous discussion is simple. When the sample unit drifts, feature, label, split, evaluation, and operational interpretation do not drift separately. They all lose the same reference point together.

--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-en.mmd"

The example below shows how feature, label, and split interpretation change when the same [source data](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data) is read as a `time-point table` and as an `action-level table`.

Problem situation: check how feature, label, and train/test split all drift together when the same log is read as a `time-point table` versus as an `action-level table`.

Input: a raw log table containing time-point flow values by `event_id` together with `review_needed`

Expected output: a comparison in which `row` and `event` units produce different sample counts, repeated labels, and split stability

Concept to check: when the sample unit changes, the interpretation of feature, label, and split must all be realigned on top of the same unit

```python
# This example checks whether features, labels, and baselines drift together when the sample unit drifts.
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
        {"event_id": "C", "second": 0, "flow": 0.6, "review_needed": 1},
        {"event_id": "C", "second": 1, "flow": 1.9, "review_needed": 1},
        {"event_id": "C", "second": 2, "flow": 1.3, "review_needed": 1},
    ]
)

per_row = raw[["event_id", "second", "flow", "review_needed"]]
per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
        late_drop=("flow", lambda s: s.iloc[-2] - s.iloc[-1]),
        review_needed=("review_needed", "max"),
    )
)

row_split = raw.assign(split=lambda df: df["second"].map({0: "train", 1: "train", 2: "test"}))
event_split = per_event.assign(split=lambda df: df["event_id"].map({"A": "train", "B": "train", "C": "test"}))

unit_summary = pd.DataFrame(
    [
        {
            "unit": "row",
            "sample_count": len(per_row),
            "feature_example": "flow at one second",
            "label_rows": per_row["review_needed"].sum(),
            "train_events": ",".join(sorted(row_split.loc[row_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(row_split.loc[row_split["split"] == "test", "event_id"].unique())),
        },
        {
            "unit": "event",
            "sample_count": len(per_event),
            "feature_example": "flow_mean / flow_max / late_drop",
            "label_rows": per_event["review_needed"].sum(),
            "train_events": ",".join(sorted(event_split.loc[event_split["split"] == "train", "event_id"].unique())),
            "test_events": ",".join(sorted(event_split.loc[event_split["split"] == "test", "event_id"].unique())),
        },
    ]
)

print("1) sample counts change with the chosen unit")
print("row-level samples:", len(per_row))
print("event-level samples:", len(per_event))
print()
print("2) row-level labels are repeated because the label belongs to the whole event")
print(per_row.groupby("event_id", as_index=False)["review_needed"].sum())
print()
print("3) event-level features and labels line up on the same unit")
print(per_event)
print()
print("4) split stability differs by unit")
print(unit_summary)
```

Expected output:

```text
1) sample counts change with the chosen unit
row-level samples: 9
event-level samples: 3

2) row-level labels are repeated because the label belongs to the whole event
  event_id  review_needed
0        A              3
1        B              0
2        C              3

3) event-level features and labels line up on the same unit
  event_id  flow_mean  flow_max  late_drop  review_needed
0        A   1.133333       1.8        0.7              1
1        B   0.833333       1.1        0.1              0
2        C   1.266667       1.9        0.6              1

4) split stability differs by unit
    unit  sample_count                    feature_example  label_rows train_events test_events
0    row             9                 flow at one second           6        A,B,C       A,B,C
1  event             3  flow_mean / flow_max / late_drop           2          A,B           C
```

This output shows three things at once. First, `review_needed` is a label attached to one full action, but in the time-point table it is repeated three times each for A and C. Second, a feature such as `late_drop` is computed only after the data is grouped into one full action. Third, if we look at `unit summary`, then in the time-point split the same `event_id` can appear on both the training and evaluation sides, while in the action-level split the whole of `C` can be held out as test. This difference is exactly why the units of feature, label, split, and evaluation drift together.

This example becomes clearer if we first check the following three questions rather than the output values themselves.

1. Does `review_needed` attach to one time-point number, or to one full action?
2. Are `flow_mean` and `flow_max` values read directly from one row, or values created by grouping several rows?
3. If we divide into training and evaluation, do we divide `per_row`, or do we divide `per_event`?

Once those three questions are answered, it becomes clearer why the sentence `even with the same source data, the sample unit has to be fixed first` keeps being repeated.

We can also reduce the same problem into an actual model evaluation. The code below is not meant to teach how to use `DecisionTreeClassifier` well. It checks that when rows from the same action enter both training and evaluation, the evaluation score can look better than it should, and that this illusion shrinks when we hold out whole actions.

Problem situation: We want to confirm that evaluating the same raw log with a row-level split and with an action-level split can produce different scores.

Input: A small action log with `event_id`, `second`, `flow`, and `review_needed`.

Expected output: The `event_id` values that entered both training and evaluation in the row-level split, the row-level evaluation score, and the action-level evaluation score.

Concept to check: If nearby rows from the same action are mixed into training and evaluation, the model may look as if it predicted a new action, while it is closer to matching nearby values from an action it already saw.

```python
# This example checks how the split unit changes the evaluation score on the same raw log.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

raw_rows = []
labels = {"A": 1, "B": 0, "C": 1, "D": 0, "E": 1, "F": 0, "G": 0, "H": 1}
base_flow = {"A": 10, "B": 30, "C": 50, "D": 70, "E": 90, "F": 110, "G": 130, "H": 150}

for event_id, label in labels.items():
    for second, offset in enumerate([0.0, 0.2, -0.1]):
        raw_rows.append(
            {
                "event_id": event_id,
                "second": second,
                "flow": base_flow[event_id] + offset,
                "review_needed": label,
            }
        )

raw = pd.DataFrame(raw_rows)

# Row-level split: some rows from every event_id enter both train and test.
row_train = raw[raw["second"].isin([0, 1])]
row_test = raw[raw["second"].eq(2)]

# Action-level split: test event_id values are fully excluded from training.
event_train = raw[raw["event_id"].isin(["A", "B", "C", "D"])]
event_test = raw[raw["event_id"].isin(["E", "F", "G", "H"])]


def evaluate(train, test):
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[["flow"]], train["review_needed"])
    predictions = model.predict(test[["flow"]])
    return accuracy_score(test["review_needed"], predictions), [
        (event_id, int(prediction), int(actual))
        for event_id, prediction, actual in zip(test["event_id"], predictions, test["review_needed"])
    ]


row_accuracy, _ = evaluate(row_train, row_test)
event_accuracy, event_predictions = evaluate(event_train, event_test)
leaked_events = sorted(set(row_train["event_id"]) & set(row_test["event_id"]))

print("leaked events in row split:", leaked_events)
print("row split accuracy:", row_accuracy)
print("event split accuracy:", event_accuracy)
print("event split predictions:", event_predictions)
```

Expected output:

```text
leaked events in row split: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row split accuracy: 1.0
event split accuracy: 0.5
event split predictions: [('E', 0, 1), ('E', 0, 1), ('E', 0, 1), ('F', 0, 0), ('F', 0, 0), ('F', 0, 0), ('G', 0, 0), ('G', 0, 0), ('G', 0, 0), ('H', 0, 1), ('H', 0, 1), ('H', 0, 1)]
```

In the row-level split, every `event_id` enters training and evaluation at the same time. So the score looks good at `1.0`. But that is closer to matching nearby rows from the same action again than to predicting a new action well. This illusion should also be checked through the lens of [data leakage](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-data-leakage). In the action-level split, the whole of `E`, `F`, `G`, and `H` is excluded from training, so the score drops to `0.5`. This difference shows through model output that the sample unit must also fix the evaluation unit.

There are two values worth changing in this code. If we change the `event_id` groups in `event_train` and `event_test`, the action-level evaluation changes. If we add a column such as `second` to the features, the basis used by the model may also change. The important point is not the score itself, but that `what we divided as one sample` changes the meaning of the evaluation result.

One more short layer can be added here to read the direction of the drift immediately.

- If `review_needed` is an action-level label, then a `per_row` split carries a high risk of cutting the label unit incorrectly.
- If `flow_mean` and `flow_max` are features created by grouping several rows, then the moment we read one time-point row as the sample, the meaning of the feature changes too.
- So when the sample unit drifts, feature, label, and split do not drift independently. They become misaligned together.

The same content can be summarized more briefly as follows.

| If one time-point row is taken as the sample | If one full action is taken as the sample |
| --- | --- |
| the label is repeatedly copied across several rows | the label attaches once to one action |
| it is hard to build whole-action features directly | summary features can be attached in the same way |
| the same action can be mixed into both training and evaluation | splitting can happen at the action level |
| the operational question and the data unit diverge | the operational question and the data unit align |

So when the sample unit drifts, the problem should not be read as a simple notation confusion. It should be read as a collapse of consistency in which feature, label, split, and evaluation begin pointing at different units.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example requires features and label to be aligned on the same unit, it provides the basis for the claim that if the sample unit drifts, the meaning of both feature and label drifts together. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains a design flaw in which a feature becomes a proxy for the label, it strengthens the warning that structural errors can arise when row-level features and event-level labels are mixed on the wrong unit. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- scikit-learn developers, `Cross-validation: evaluating estimator performance`. Because it explains that, for grouped data, dependent samples from the same group should not appear in both the training and validation folds, it directly strengthens this section's split/evaluation warning that nearby rows from the same action can be mixed into training and evaluation if time-point rows are treated as samples. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because the provenance framework explains that it should support reproducibility and derivation, it strengthens the higher-level frame that split and evaluation can keep the same criterion only when the unit at which features and labels were made is recorded reproducibly. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
