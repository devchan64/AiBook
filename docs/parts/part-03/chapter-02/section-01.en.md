# P3-2.1 Why Must Stored Records Be Reorganized for the Analysis Purpose

> Section ID: `P3-2.1`
> Version: `v2026.09.15`

In databases, data modeling represents the objects and relationships to be stored. This Part focuses on deciding which questions stored records should answer and organizing samples and columns accordingly. When storage and analysis serve different purposes, the same records need different groupings.

A [dataset](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-dataset) is a collection of data. Raw logs, image collections, and unlabeled records can all be datasets. Having a dataset does not, by itself, mean it is ready for a particular analysis or learning task. In this section, a `dataset candidate` means material whose sample units and columns are still being checked against the current question.

A row in a storage table may or may not be the sample to analyze. For predicting the next measurement, time-point rows can be a starting point. For comparing whole actions, multiple rows must be grouped into one action.

Suppose there is source data for automatically executed actions. Control parameters and sensor values accumulated over time can be stored directly in a storage table. Each row can hold a time point, a sensor name, a measured value, and a control-setting value. This structure is suitable for preserving records and tracing detailed flow when a problem appears.

Yet this table alone does not readily answer questions such as `Was this action longer than usual?`, `Was its late decline unusually slow?`, or `Did the latest 20 actions differ from the baseline?` A row in the storage structure usually represents `one time point`, while these questions require `one action` or `a recent period containing several actions` as the unit of comparison. Stored records therefore do not automatically provide the table needed for action-level comparison.

To see this difference clearly, place storage structure and problem-representation structure side by side.

| Category | What one row means | Main purpose |
| --- | --- | --- |
| Storage structure | one time-point record, sensor measurement, control setting | preserving source data and traceability |
| Problem-representation structure | a summary of one action, a recent-segment comparison, a baseline aggregate | comparison, interpretation, preparation for learning |

Applied to a real table, this distinction can first be checked with the following three questions.

| Question to ask first when the table arrives | Why the question is needed |
| --- | --- |
| Does one row mean one time-point record, or a summary of one action? | Because if the row meaning changes, the sample unit that follows also changes |
| Can this table already be compared directly? | Because storage structure may be strong for record preservation but weak for comparison |
| If a strange value appears, where should we return to? | Because problem-representation structure alone cannot explain every detailed cause |

These three questions quickly distinguish whether the current dataset can answer the current question directly or needs restructuring. The first asks what a row means, the second asks about comparability, and the third asks when the raw logs must be reopened. Data modeling represents stored records in a form that lets us answer all three.

In storage structure, what matters is preserving everything without omission. In problem-representation structure, by contrast, we have to decide `what should remain` and `what should be discarded`. For example, once we decide to treat one full action as one sample, we can replace hundreds of time-point rows with new columns such as total action time, early-stage mean, late-stage drop rate, or tracking error. This does not damage the storage structure. It designs a new representation to answer a different question.

The small table below immediately shows how the same source data is read differently depending on the purpose.

| Structure | Example columns | What one row means |
| --- | --- | --- |
| Storage structure | `timestamp`, `sensor_name`, `value` | one time-point record |
| Problem-representation structure | `event_id`, `mid_flow_mean`, `late_drop_rate` | a summary of one action |

## From Preserving Records to Restructuring for a Question {#a-small-diagram}

The possible need to reorganize stored records for a question becomes clearer when we separate `preserving records` from `regrouping them for the question`, as below.

<div class="aibook-diagram-scroll" role="region" tabindex="0" aria-label="Diagram: scroll horizontally to read" markdown="1">
<div class="aibook-diagram-canvas" markdown="1">

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-1-mermaid-01-en.mmd"
```

</div>
</div>

Problem situation: confirm that the same source record remains as time-point rows in storage structure, but is regrouped into an action-level summary table in the dataset candidate.

Input: a flow-log table stored as time-point records under each `event_id` and the minimum number of time points required to treat an action as one event, `min_points_per_event`

Expected output: a display in which the same records are separated into two different table roles, `stored time-step records` and `event-level dataset candidate`, and events that do not meet the criterion are excluded from comparison candidates

Concept to check: the fact that stored records exist is not the same as the fact that a dataset candidate able to answer a question has been prepared. If `min_points_per_event` changes, which records are accepted as one action sample also changes.

These measurements are one second apart, so the difference between the final two flow values equals the change per second. With a different interval, divide by the elapsed time between them.

```python
# This example regroupes stored time-step records into an event-level dataset candidate.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

min_points_per_event = 3

storage_table = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.8},
        {"event_id": "A", "second": 1, "flow": 1.4},
        {"event_id": "A", "second": 2, "flow": 1.2},
        {"event_id": "B", "second": 0, "flow": 0.7},
        {"event_id": "B", "second": 1, "flow": 1.1},
        {"event_id": "B", "second": 2, "flow": 0.6},
        {"event_id": "C", "second": 0, "flow": 0.9},
        {"event_id": "C", "second": 1, "flow": 1.0},
    ]
)

storage_table = storage_table.sort_values(["event_id", "second"])

dataset_candidate = (
    storage_table.groupby("event_id")
    .agg(
        point_count=("second", "count"),
        duration_seconds=("second", lambda values: values.max() - values.min()),
        mean_flow=("flow", "mean"),
        late_drop_rate=("flow", lambda values: values.iloc[-1] - values.iloc[-2] if len(values) >= 2 else float("nan")),
    )
    .reset_index()
)
dataset_candidate["usable_as_event_sample"] = (
    dataset_candidate["point_count"] >= min_points_per_event
)
usable_candidate = dataset_candidate[dataset_candidate["usable_as_event_sample"]]

print("1) stored time-step records")
print(storage_table)
print()
print(f"2) event-level dataset candidate when min_points_per_event = {min_points_per_event}")
print(dataset_candidate.round(2))
print()
print("3) usable event-level rows for comparison")
print(usable_candidate.round(2))
```

Expected output:

```text
1) stored time-step records
  event_id  second  flow
0        A       0   0.8
1        A       1   1.4
2        A       2   1.2
3        B       0   0.7
4        B       1   1.1
5        B       2   0.6
6        C       0   0.9
7        C       1   1.0

2) event-level dataset candidate when min_points_per_event = 3
  event_id  point_count  duration_seconds  mean_flow  late_drop_rate  usable_as_event_sample
0        A            3                 2       1.13            -0.2                    True
1        B            3                 2       0.80            -0.5                    True
2        C            2                 1       0.95             0.1                   False

3) usable event-level rows for comparison
  event_id  point_count  duration_seconds  mean_flow  late_drop_rate  usable_as_event_sample
0        A            3                 2       1.13            -0.2                    True
1        B            3                 2       0.80            -0.5                    True
```

What must be seen first in this output is the difference between `the table that shows the same records as they are` and `the table remade to match the question`. In the first table, one row is one time-point record, so `the average flow of this action` or `the late-stage drop rate` is not yet visible. Only after regrouping into the second table does one action become one row, and only then do columns appear that can be used directly for comparison. The value to manipulate here is `min_points_per_event`. If the value is `3`, C has stored records but is excluded from the comparable one-action samples. If the value is lowered to `2`, C also becomes a candidate, but we must ask again whether its late-stage drop rate can be compared with the same meaning. The fact that stored records exist is not the same statement as the fact that a dataset candidate able to answer a question has been prepared.

It is also useful to check briefly where we get stuck if we keep the same data in storage structure without changing it.

| Question we immediately want to ask | The problem when storage structure is used as-is |
| --- | --- |
| Was this one action longer than usual? | One row is a time-point record, so `the length of one action` is not directly visible |
| Can we select only the actions with a slow late-stage drop? | Unless the late segment is grouped and summarized first, there is no comparison column |
| Can we directly compare the most recent 20 cases with the prior 200? | Storage structure has no comparison unit that points to `one action` or `the recent segment` |

So storage structure shows `what was recorded`, but it does not automatically decide `what should be compared as one case`. Rebuilding a dataset candidate means filling in exactly that blank.

One warning is necessary here. Problem-representation structure does not replace storage structure. Creating a summary table does not make raw logs unnecessary. On the contrary, if the summary table shows a strange change, we need to return to storage structure and inspect the detailed time points again. Storage structure preserves evidence, while problem-representation structure makes comparison possible. They are not competing structures, but linked structures with different roles.

This relationship can be summarized more briefly as follows.

| Question | Is storage structure strong here? | Is problem-representation structure strong here? |
| --- | --- | --- |
| What values were actually recorded? | Yes | only partially |
| What was the structure of this one action? | Difficult | Yes |
| Has the recent segment changed from the usual one? | Difficult | Yes |

This table shows that the difference between storage structure and problem-representation structure is not merely `a difference in table shape`, but `a difference in the questions that can be answered`. How a table was stored and which questions it can answer are not the same problem. That is why the first task at the front of Part 3 is not to look at records and imagine model names, but to ask into what dataset candidate those records should be reread.

More broadly, this section separates `preserving source records`, `resetting the analysis unit`, and `creating derived representations` as work at different levels, and organizes the starting conditions for lifting record structure into problem-representation structure.

The first thing to check is therefore not what the material is called, but whether the unit and derived representation needed to answer the current question have been defined.

## Checklist

- Can you explain why raw logs can be a dataset yet still be unready for the current question?
- Did you specify the identifier and grouping rule needed to build an action-comparison table?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`. Because it explains the example unit and the role of features separately, it supports the core point of this section that a stored row and a comparable sample row may differ. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Oracle, `Introduction to Data Warehousing Concepts`. Because it explains that a data warehouse is designed for business intelligence activities, query and analysis, maintaining historical records, and data analysis, it supports the opening context that `DSS/BI/DW/OLAP` connects stored data to decision making and analysis. [https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html](https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance, derivation, and traceability together, it strengthens the higher-level frame that storage structure preserves raw evidence while problem-representation structure creates derived representations for different questions. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it organizes the relationship among variables, observations, and table structure, it provides the general principle behind the explanation that one row in storage structure and one row in an analysis table may not mean the same thing. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20

- [Google Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){ target="_blank" rel="noopener noreferrer" }. Checked the distinction among datasets, labeled examples, and unlabeled examples. Checked: 2026-09-15.
