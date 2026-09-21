# P3-4.2 What Else Starts to Drift When the Sample Unit Drifts

> Section ID: `P3-4.2`
> Version: `v2026.09.19`

If a [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) is one action, its observations, features, and outcome must refer to that action. But **splitting training and evaluation by event** and **scoring once per event** are separate decisions. A fictional experiment predicting action review outcomes illustrates the distinction.

## Observation Rows, Analysis Objects, Split Groups, and Scoring Units

| Distinction | Meaning in this experiment |
| --- | --- |
| Observation row | Flow recorded at one time within an action |
| Analysis object | One action bearing a review outcome |
| One model input | The `flow` value at one time point |
| Split group | An `event_id` kept together in training or evaluation |
| Scoring unit | One time-point row whose prediction is compared with its target |

The model predicts at each time point, while the target `review_needed` repeats the action’s 0 or 1 across its rows. This is an experiment in input/target design, not confirmed fault data. Repeating 1 across an action’s 18 rows still represents one action flagged for review, not 18 actions.

Specify feature calculation ranges too. In the CSV below, A’s flow is 10.2 at second 16 and 9.9 at second 17. `late_drop = earlier−later = 0.3 L/min` is the drop amount over this interval. The slope is `(9.9−10.2)/(17−16) = −0.3 L/min/s`. Their signs and units differ, and neither can be calculated from a single time-point value. Interval features may be attached to time-point inputs, provided their observation range is specified.

## Read the Accuracy Denominator First

Here, **accuracy is correct evaluation rows divided by all evaluation rows**. Six correct rows out of twelve give `6/12 = 0.5`, or 50%. An event with multiple rows is scored multiple times in this calculation.

| Split | Training records | Evaluation records | Events on both sides? |
| --- | --- | --- | --- |
| Row split | Seconds 0–11 of every event A–H | Seconds 12–17 of every event A–H | Yes: A–H |
| Event split | All times of A–D | All times of E–H | No |

The first evaluates other time points from already-seen events; the second evaluates rows from unseen events. Neither automatically scores once per event. If the question concerns performance on new events, the first split’s high score alone cannot answer it.

## Change the Split and Inspect Model Outputs

The input is a [fictional log CSV](/AiBook/assets/part-03/chapter-04/p3_4_2_split_log.csv): eight events A–H, each with 18 observations, totaling 144 rows. Read flow in L/min. Small changes `0.0, +0.2, −0.1` repeat around event centers 10, 30, …, 150. Values within an event are very similar; repeated observations do not add independent events. The [generator](/AiBook/assets/part-03/chapter-04/p3_4_2_make_split_log.py) reproduces the file.

`DecisionTreeClassifier` predicts 0 or 1 by splitting on input values. The focus here is how the evaluation target changes when the same model runs under two splits, rather than how to maximize performance. `features` specifies input columns; `train_event_ids` specifies training events for the event split. Change them and inspect overlapping events, correct rows, and denominators.

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

raw = pd.read_csv("docs/assets/part-03/chapter-04/p3_4_2_split_log.csv")
# Change input columns and training events; inspect correct rows together with evaluation rows.
features = ["flow"]
train_event_ids = ["A", "B", "C", "D"]
row_train_end = 12

row_train = raw[raw["second"] < row_train_end]
row_test = raw[raw["second"] >= row_train_end]
event_train = raw[raw["event_id"].isin(train_event_ids)]
event_test = raw[~raw["event_id"].isin(train_event_ids)]


def evaluate(name, train, test):
    if train.empty or test.empty:
        raise ValueError("Both training and evaluation need records.")
    model = DecisionTreeClassifier(random_state=0)
    model.fit(train[features], train["review_needed"])
    result = test[["event_id", "review_needed"]].copy()
    result["prediction"] = model.predict(test[features])
    result["correct"] = result["prediction"].eq(result["review_needed"])
    overlap = sorted(set(train["event_id"]) & set(test["event_id"]))
    correct = int(result["correct"].sum())
    total = len(result)
    print(f"{name}: train_rows={len(train)}, test_rows={total}, overlap={overlap}")
    print(f"row_accuracy: {correct}/{total} = {correct / total:.3f}")
    print(result.groupby("event_id").agg(
        test_rows=("correct", "size"), correct_rows=("correct", "sum")
    ).to_string())
    return result


row_result = evaluate("row_split", row_train, row_test)
print()
event_result = evaluate("event_split", event_train, event_test)
```

```text
row_split: train_rows=96, test_rows=48, overlap=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
row_accuracy: 48/48 = 1.000
          test_rows  correct_rows
event_id
A                 6             6
B                 6             6
C                 6             6
D                 6             6
E                 6             6
F                 6             6
G                 6             6
H                 6             6

event_split: train_rows=72, test_rows=72, overlap=[]
row_accuracy: 36/72 = 0.500
          test_rows  correct_rows
event_id
E                18             0
F                18            18
G                18            18
H                18             0
```

The default row split gives **48/48 = 1.0**; the event split gives **36/72 = 0.5**. The latter gets E and H’s 36 rows wrong and F and G’s 36 rows right. The denominator 72 counts time-point rows from four events, not the four events themselves.

In the row split, similar values from each event recur on both sides, making separated event-specific ranges easy to learn. Under the event split, evaluation flows of 90 and above lie outside the training range around 10–70, and the model predicts 0 throughout. Training/evaluation sizes and value distributions also differ, so **this is not an experiment isolating event overlap as the sole cause of the score gap**. Group separation does not always lower scores.

Change `train_event_ids` to `['A', 'B', 'C', 'E']`. Evaluation then uses D, F, G, and H; with these data and this model, only H’s 18 rows are correct, giving `18/72 = 0.25`. Also try `features = ['flow', 'second']`. With the default event split, accuracy remains 0.5. Adding a column need not change or improve the score. These are exploratory checks; do not select the highest-scoring evaluation split and report it as performance.

## Event-Level Scoring Needs a Separate Rule {#a-small-diagram}

To score once per event, specify how time-point predictions become one event outcome. For example, use a majority vote over the 18 predictions, withholding a decision on ties. In the default event split, every prediction within each event is 0, so only F and G are correct: `2/4 = 0.5`. The number matches row accuracy, but the denominator differs. Unequal event lengths or mixed predictions can make the two scores differ.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-2-mermaid-01-en.mmd"
```

Rewrite “event split accuracy is 0.5” precisely. The answer is “After training on A–D, the model correctly predicts 36 of 72 time-point rows from new events E–H.” If scoring once per event, state the combining rule, such as majority vote, and report `2/4` separately.

## Checklist

- Can you identify the observation row, analysis object, split group, and scoring unit?
- Do you avoid counting repeated event labels as new independent events?
- Can you distinguish a 0.3 L/min drop from a −0.3 L/min/s slope?
- Did you expand 1.0 and 0.5 into correct rows divided by evaluation rows?
- Can you distinguish holding out new events from scoring once per event?

## Sources and Further Reading

These sources support grouped splitting and the definition of accuracy.

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, grouped data. [Official documentation](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- scikit-learn developers, `accuracy_score`. [Official documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
