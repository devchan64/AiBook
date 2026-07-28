# P3-3.1 Why Source Data Should Not Be Read as a Learning Problem Right Away

> Section ID: `P3-3.1`
> Version: `v2026.07.25`

When source data first arrives, many people almost reflexively think, `what can we predict with this?` first. Because there is a table, many values, and records measured over time, it feels as if the data could be turned immediately into some learning problem. But that reaction is usually too fast. The table in front of us is more likely not yet `a training dataset`, but merely [recorded source data](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data), or at best a [dataset candidate](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-dataset-candidate).

Here the first point to fix is that [problem-representation structure](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-problem-representation-structure) comes before `the learning-problem frame`. We have to make clear the warning that this is not yet the stage for choosing a learning-problem frame such as a prediction problem, a classification problem, or an anomaly-detection problem.

At the entry to this Chapter, the `dataset candidate` viewpoint built in Chapter 2 is narrowed one step further.

| What the previous Chapter left behind | What this Chapter adds | The structure passed to the next Chapter |
| --- | --- | --- |
| the difference between storage structure and a dataset candidate, and the first checks for a new table | the reason source data should not yet be promoted into a learning problem | the judgment that actually fixes the sample unit and table structure |

Consider a situation where, for each automatically executed action, a control-parameter time series and a sensor time series are recorded. When seeing such a table, thoughts like the following arise first.

- Since there are sensor values, this could be turned into an anomaly-detection problem.
- Since action results differ slightly, it could be turned into a classification problem.
- If the time series is long, maybe it can be sent directly into a time-series prediction problem.

These thoughts are not themselves wrong. The problem is that the learning-problem frame appears first while `what counts as one case`, `what we are trying to predict`, and whether a [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/l/#glossary-label) actually exists have not yet been fixed. In that state, the data problem has not been defined yet. The learning-problem frame has merely been imagined before the data itself.

The reason this happens so often is clear. First, when a table is visible, people often accept it immediately as `already organized data`. Second, if prior AI-learning experience has been remembered mostly through learning-problem types, prediction style appears before problem representation. Third, the longer and more complex the raw time series is, the more likely the expectation comes first that `maybe this can be passed directly into a learning problem as it is`.

But if source data is read immediately as if it were already a dataset, important questions are skipped.

| The question that easily comes to mind first | The question that is actually needed first |
| --- | --- |
| Into what learning problem should this be read? | What should count as one [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample)? |
| What should the label be? | Does a stable label truly exist right now? |
| How should accuracy be improved? | Into what table must this be regrouped so comparison becomes possible? |

This difference is not merely about order. What is needed when source data is first seen is not choosing a learning problem, but `asking again what kind of table this really is`. Depending on whether what we are looking at is time-point measurement records, a summary of one action, or an aggregate of a recent segment, every later explanation of [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), and [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target) changes.

For example, even after seeing only part of the source data below, the learning-problem frame may jump out too early.

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

Looking only at this table, it is easy to think of words such as `classification problem`, `prediction problem`, or `time-series learning problem`. But we still have not decided whether this table is `a time-point record` or `a one-action table`. So if we choose a learning-problem frame here right away, the format of the problem gets ahead of the problem itself.

## A Small Diagram

It becomes clearer which questions stay empty when source data is escalated too early into a learning problem if the flow is reread as `source records -> empty questions -> sample/label candidate cleanup`.

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-1-mermaid-01-en.mmd"
```

Problem situation: when a time-point log table arrives, check which core questions remain empty if we read it immediately as a learning problem.

Input: the raw log table [p3_3_1_source_operation_log.csv](/AiBook/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv), where multiple time-point measurements are mixed under each `event_id`, and `label_column_to_try`, the column name to inspect as a label candidate

One row in the input file is a sensor record measured at a specific second (`second`) inside one action (`event_id`). The table also contains `batch_id`, `recipe`, `pressure`, `flow`, `vibration`, and `temperature`, but at this point we have not yet decided which column is the sample identifier and which column is the label.

Expected output: it becomes visible that `read it as a classification problem right now` and `fill in the missing questions first` produce different results. Changing `label_column_to_try` also shows that column existence and label-candidate usability are not the same thing.

Concept to check: before source data is read as a learning problem, we first have to decide what `one sample`, `a label candidate`, and `a comparison table` are. Learning-problem judgment is not a fixed sentence; it has to be checked against the current table's columns and grouping criteria.

```python
# This example avoids reading a raw log as a learning problem too early and rebuilds it as an event-level summary table.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 160)

raw_log_path = "docs/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv"
label_column_to_try = "review_label"

column_unit = {
    "batch_id": "operation_context",
    "recipe": "operation_context",
    "pressure": "time_point_sensor_value",
    "flow": "time_point_sensor_value",
    "vibration": "time_point_sensor_value",
    "temperature": "time_point_sensor_value",
    "review_label": "event_label",
}

raw = pd.read_csv(raw_log_path)

print("1) raw input shape and first rows")
print("shape:", raw.shape)
print(raw.head())
print()

print("2) too-early reading")
print("- maybe this is a classification problem")
print("- label column:", "found" if label_column_to_try in raw.columns else "not found yet")
print("- one training sample: not decided yet")
print()

column_exists = label_column_to_try in raw.columns
candidate_unit = column_unit.get(label_column_to_try, "unknown")
same_unit_as_sample = column_exists and candidate_unit == "event_label"
stable_label_meaning_known = same_unit_as_sample
usable_label_candidate = column_exists and same_unit_as_sample and stable_label_meaning_known

print("3) label candidate check")
print("- column to try:", label_column_to_try)
print("- column exists:", column_exists)
print("- candidate unit:", candidate_unit)
print("- same unit as one event:", same_unit_as_sample)
print("- stable label meaning known:", stable_label_meaning_known)
print("- usable label candidate:", usable_label_candidate)
print()

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        batch_id=("batch_id", "first"),
        recipe=("recipe", "first"),
        row_count=("second", "count"),
        duration_seconds=("second", "max"),
        max_pressure=("pressure", "max"),
        mean_flow=("flow", "mean"),
        max_vibration=("vibration", "max"),
        end_temperature=("temperature", "last"),
    )
)
print("4) questions that must be settled first")
print("- one sample: one event")
print("- candidate comparison table: one row per event")
print("- label candidate:", "usable" if usable_label_candidate else "still not decided")
print()

print("5) event-level table after defining the sample")
print(event_summary.round(2))
```

Expected output:

```text
1) raw input shape and first rows
shape: (36, 8)
  event_id batch_id    recipe  second  pressure  flow  vibration  temperature
0        A     B-17  standard       0       1.0   0.0       0.02         24.1
1        A     B-17  standard       1       2.0   1.4       0.04         24.4
2        A     B-17  standard       2       2.4   1.6       0.07         24.8
3        A     B-17  standard       3       2.2   1.2       0.08         25.0
4        B     B-17  standard       0       1.1   0.1       0.03         24.0

2) too-early reading
- maybe this is a classification problem
- label column: not found yet
- one training sample: not decided yet

3) label candidate check
- column to try: review_label
- column exists: False
- candidate unit: event_label
- same unit as one event: False
- stable label meaning known: False
- usable label candidate: False

4) questions that must be settled first
- one sample: one event
- candidate comparison table: one row per event
- label candidate: still not decided

5) event-level table after defining the sample
  event_id batch_id     recipe  row_count  duration_seconds  max_pressure  mean_flow  max_vibration  end_temperature
0        A     B-17   standard          4                 3           2.4       1.05           0.08             25.0
1        B     B-17   standard          4                 3           1.9       0.78           0.06             24.7
2        C     B-18       fast          4                 3           2.8       1.05           0.22             26.8
3        D     B-18       fast          4                 3           2.6       1.02           0.16             26.2
4        E     B-19   standard          4                 3           2.1       0.90           0.07             24.8
5        F     B-19   standard          4                 3           2.5       1.12           0.09             25.3
6        G     B-20  high-load          4                 3           3.1       1.35           0.28             27.5
7        H     B-20  high-load          4                 3           2.9       1.30           0.24             27.0
8        I     B-21   standard          4                 3           2.3       0.98           0.08             25.1
```

The core of this example is the difference between steps 2 and 3. In step 2, only the sentence `maybe this is a classification problem` appears first, but in reality the `review_label` column specified by `label_column_to_try` does not exist, and even one sample has not yet been decided. The value to manipulate here is `label_column_to_try`. If it is changed to `"flow"`, `column exists` becomes `True`, but `candidate unit` is `time_point_sensor_value` and `usable label candidate` remains `False`. That is because `flow` is not a stable label attached to one action; it is a time-point sensor value. By contrast, step 4 first fixes the structure `one sample is one action` and `the comparison table is one row per action`. Only after that does an event-level comparison table with `row_count`, `duration_seconds`, `max_pressure`, `mean_flow`, `max_vibration`, and `end_temperature` appear, as in step 5. In other words, if source data is read too quickly as a learning problem, the problem format is fixed first while the still-empty questions remain covered over.

If we place side by side the empty questions left behind when the learning-problem frame jumps out first, the issue becomes clearer.

| The phrase that jumps out first | The question that is still empty |
| --- | --- |
| `anomaly-detection problem` | What exactly will count as an anomaly? |
| `classification problem` | Does a stable label truly exist? |
| `time-series learning problem` | Is one sample one time-point bundle, or one full action? |

The core of this table is not that the name of the learning problem is wrong. The problem is that the questions that have to be answered before that frame are still empty. Data modeling is the front-end design that fills those blanks.

So the most common mistake when source data first arrives is to mistake `record structure` for `learning structure`. The mere existence of time-point logs does not mean a prediction problem has already been defined. Only after we decide how to group those logs, what to keep, and what to compare them against can we accurately use the word dataset. Once the learning-problem frame appears first, that front-end design is easily skipped, and later the sample unit and table structure have to be taken apart and rebuilt. If this section is reread as a problem of managing the moment of `problem escalation`, it becomes even clearer that the key is not `let model names come to mind later`, but the judgment not to escalate prematurely into a learning problem before the sample unit and label candidate are organized.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because it explains that a labeled example consists of features and a label, it supports the claim that source data where neither one sample nor a label has yet been fixed should not be read immediately as a learning problem. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains a design flaw where a feature becomes a proxy for the label, it strengthens the warning that choosing the problem frame first risks reading not-yet-organized source columns into a bad learning structure. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it strengthens the higher-level frame that we must first decide what counts as one object and through what transformation a dataset candidate was made. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
