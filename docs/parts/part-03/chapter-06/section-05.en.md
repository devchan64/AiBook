# P3-6.5 How Should We Read and Keep Features Together When Their Units and Scales Differ

> Section ID: `P3-6.5`
> Version: `v2026.07.25`

Once we build a few [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), another confusion easily returns. `Is the column with the larger value more important?` `Can seconds and pressure units stay in the same table?` `Can a column with an average of 200 and another with 0.2 simply be compared side by side?` What is needed first here is the sense to distinguish unit, range, size of variation, and change relative to the [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) before looking at the size of the numbers.

The fact that they appear together in one table and the judgment that they should be read by the same magnitude standard are not the same thing. Features can have different units, ranges, and widths of variation, and if we look only at raw magnitude without knowing that difference, we can easily misread the structure.

For example, suppose the following columns appear together in a one-action summary table.

| Column name | Example value | Meaning |
| --- | ---: | --- |
| `duration_seconds` | 48 | Duration of the action |
| `pressure_mean` | 101.2 | Average pressure |
| `flow_std` | 0.18 | Flow variability |
| `late_drop_rate` | -0.42 | Late-phase decline rate |

All four values are numerical, but they do not describe the same kind of magnitude.

- `duration_seconds` is a time length.
- `pressure_mean` is a pressure level.
- `flow_std` is the size of the fluctuation.
- `late_drop_rate` is the direction and speed of change.

So we should not look only at the common property that they are numbers and read something like `101.2 is more important than 48`.

## Why Is This Distinction Needed

This sense is needed in the feature-design stage for three reasons.

| What we should know first | Why it is necessary |
| --- | --- |
| The units differ | Because the same magnitude can still mean completely different things |
| The ranges differ | Because one column may naturally move near 0 while another may move near 100 |
| The variation widths differ | Because if we look at small-change and large-change columns with the same visual scale, we can miss important differences |

This does not yet mean we must enter normalization formulas for model calculation. In Part 3, the point is first to build the sense that `what the number measures matters more than whether the number itself is large`.

## Putting Them in the Same Table and Reading Them in the Same Way Are Different

Several features can certainly be placed in the same sample table. But the reading method can still differ by column.

| Feature column | How it should be read first |
| --- | --- |
| `duration_seconds` | Check whether it became longer than usual |
| `pressure_mean` | Check the level difference from the baseline |
| `flow_std` | Check whether the fluctuation increased |
| `late_drop_rate` | Check whether the late-phase structure collapsed more steeply |

So comparison should happen not `between numbers`, but `between the same column playing the same role`. Rather than directly comparing `duration_seconds` and `pressure_mean`, we should compare `this duration_seconds` with the usual duration_seconds, and `this pressure_mean` with the usual pressure_mean.

## Common Misunderstandings

| Misunderstanding | What actually needs to be checked again |
| --- | --- |
| A larger-valued column is more important | Are we comparing numbers of different units and roles by magnitude alone? |
| A small value such as 0.2 must have little impact | Is that column originally a feature that only moves within a small range? |
| All features can be read in the same way | Are we distinguishing level, change, variability, and duration? |

For example, `flow_std = 0.18` may look small if we look only at the number, but if the usual value was `0.03`, it can actually mean a large increase in fluctuation. Conversely, `pressure_mean = 101.2` may look large, but if the usual value was `101.0`, the relative change can be small.

## So What Should Be Written Down First

At the Part 3 stage, it becomes much safer if we can write the following three things briefly next to each feature column.

| What to write down | Example |
| --- | --- |
| The unit or meaning of this column | seconds, pressure, rate of change, variability |
| The structure this column shows | level, direction, fluctuation, duration |
| The comparison basis | the absolute value itself, or difference from baseline |

For example, it can be written like this.

| Column name | Unit / meaning | Structural role | Comparison method |
| --- | --- | --- | --- |
| `duration_seconds` | seconds | duration | Has it become longer than usual? |
| `pressure_mean` | pressure level | average level | Is the difference from the baseline large? |
| `flow_std` | variability | fluctuation | Has fluctuation increased compared with usual? |
| `late_drop_rate` | rate of change | late-stage collapse speed | Has the late-phase slope become steeper? |

If we have this table, then `what kind of number this is` and `how it should be read` become fixed together.

## Small Check Table

In this section, it is more appropriate to fix how to read numerical columns in a table than to print two fixed rows with Python. For example, consider the working table below.

| event_id | `duration_seconds` | `pressure_mean` | `flow_std` | `late_drop_rate` |
| --- | ---: | ---: | ---: | ---: |
| A | 48 | 101.2 | 0.18 | -0.42 |
| B | 44 | 100.9 | 0.05 | -0.10 |
| baseline | 45 | 101.0 | 0.03 | -0.12 |

If we look only at absolute values, `pressure_mean` appears largest. But when we read the values as changes from the baseline, a different picture appears.

| event_id | `duration_delta` | `pressure_delta` | `flow_std_delta` | `late_drop_delta` |
| --- | ---: | ---: | ---: | ---: |
| A | 3 | 0.2 | 0.15 | -0.30 |
| B | -1 | -0.1 | 0.02 | 0.02 |

What matters in this table is not the absolute size of the numbers, but the role of each column and the change inside the same column. If we look only at the first table, `101.2` may look large and `0.18` may look small. But once we read them as changes from the baseline, `flow_std_delta=0.15` may actually mean a large increase in fluctuation, while `pressure_delta=0.2` may mean only a small level difference.

| Column name | Role | How to compare first |
| --- | --- | --- |
| `duration_seconds` | duration | difference from baseline |
| `pressure_mean` | level | difference from baseline |
| `flow_std` | variability | difference from baseline |
| `late_drop_rate` | change | difference from baseline |

So the first thing to read is not `larger number`, but `how do we compare the same column playing the same role?`

So Part 3's responsibility reaches this far.

1. Know that numbers with different meanings can sit together in the same table.
2. Be able to write whether each feature means level, change, variability, or duration.
3. Know that the raw size of the number itself can matter less than `the difference from baseline inside the same column`.

Because the numbers in a feature table do not all describe the same kind of magnitude, we should first write down the unit and role, and then read them through the baseline-relative change of the same column. This section can be read not as an introduction to scaling formulas, but as the problem of role-aware reading across different measurement scales inside one working table.


The same issue appears in model input. The next example uses the same [k-NN model](/AiBook/en/reference/concept-glossary-alpha/k/#glossary-k-nn), but compares reading the features without scaling and reading them after `StandardScaler` puts each column onto a comparable scale.

Problem situation: We want to confirm that if features with different units and ranges are passed directly into k-NN, the column with the large numeric range can pull the neighbor decision more strongly.

Input: A small feature table containing duration, pressure change, flow-variability change, and a new sample to check.

Expected output: The nearest `event_id` and prediction before and after scaling.

Concept to check: Even if features sit in the same table, when a model compares them by distance, scaling can change both the neighbor and the prediction.

```python
# This example checks how a distance-based model reads features with different units and ranges.
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

features = pd.DataFrame(
    [
        {"event_id": "A", "duration_seconds": 44, "pressure_delta": 0.10, "flow_std_delta": 0.02, "review_needed": 0},
        {"event_id": "B", "duration_seconds": 48, "pressure_delta": 0.20, "flow_std_delta": 0.15, "review_needed": 1},
        {"event_id": "C", "duration_seconds": 43, "pressure_delta": -0.10, "flow_std_delta": 0.01, "review_needed": 0},
        {"event_id": "D", "duration_seconds": 49, "pressure_delta": 0.00, "flow_std_delta": 0.16, "review_needed": 1},
    ]
)
query = pd.DataFrame(
    [{"duration_seconds": 44, "pressure_delta": 0.15, "flow_std_delta": 0.14}]
)
columns = ["duration_seconds", "pressure_delta", "flow_std_delta"]

plain = KNeighborsClassifier(n_neighbors=1).fit(features[columns], features["review_needed"])
scaled = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=1))
scaled.fit(features[columns], features["review_needed"])

plain_neighbor = plain.kneighbors(query, return_distance=False)[0][0]
scaled_query = scaled.named_steps["standardscaler"].transform(query)
scaled_neighbor = scaled.named_steps["kneighborsclassifier"].kneighbors(
    scaled_query, return_distance=False
)[0][0]

print("without scaling nearest_event:", features.iloc[plain_neighbor]["event_id"])
print("without scaling prediction:", int(plain.predict(query)[0]))
print("with scaling nearest_event:", features.iloc[scaled_neighbor]["event_id"])
print("with scaling prediction:", int(scaled.predict(query)[0]))
```

Expected output:

```text
without scaling nearest_event: A
without scaling prediction: 0
with scaling nearest_event: B
with scaling prediction: 1
```

Before scaling, A is chosen as the nearest case because it has the same `duration_seconds=44`. But when pressure change and flow-variability change are put onto a comparable scale, B becomes the nearer case. This output does not mean that `the larger number is more important`; it shows that in distance-based models, a column with a larger range can dominate the calculation. So even before studying model formulas in detail, Part 3 should record each feature's unit, range, and comparison method.

So a feature table should be understood not as a competition chart of raw magnitudes, but as a structure where different measurement axes are placed side by side and read according to their roles.

## A Small Diagram

The sequence in this section is that even when different units and scales sit in one table, we should read them by column role and compare each one against its own baseline. Before raw magnitude, the first question is `what does this column measure?`

--8<-- "assets/part-03/chapter-06/p3-6-5-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `feature`. Because it explains a feature as an input variable used for prediction, it supports the point that what a number measures as an input variable matters before the size of the number itself. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains the process of turning raw data into a more useful form for learning, it reinforces this section's explanation that features with different roles such as duration, level, variability, and rate of change should be read separately. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general idea that comparison works by placing the same item next to a reference point, it can support the explanation that instead of directly comparing different features with one another, we should read each column through its change from the baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
