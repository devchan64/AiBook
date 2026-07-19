# P3-2.1 Why Are Stored Records Not Yet a Dataset

> Section ID: `P3-2.1`
> Version: `v2026.07.20`

When people first hear data modeling, many immediately think of database-table design. In practice, the term is often used in the context of organizing storage structure. Behind that usage also sits the longer flow of data-driven systems such as `DSS/BI/DW/OLAP`, where data was collected and connected to decision making. In other words, data modeling was not originally a word only for AI. It also grew inside the broader flow of regrouping stored data, comparing it again, and connecting it to judgment. But the data modeling needed for AI and data analysis goes one step further. Here, `where should the data be stored?` matters less than `how should the stored records be reread as dataset candidates that answer a specific question?`

This section focuses on separating `stored records` from a `dataset candidate`. A [dataset](/AiBook/reference/concept-glossary/#glossary-dataset) can first be understood as a collection of samples and variables grouped so they can answer the same question for learning or evaluation. Later sections will unfold `sample`, `feature`, `baseline`, and `output structure` together, but here the first task is not to define those terms at length. It is to fix why storage structure alone cannot yet enter that stage directly.

It is also better not to read the terms in the opening with the same weight. `DSS`, `BI`, `DW`, and `OLAP` are background acronyms that show the data-use context. The core concepts of this section are `storage structure`, `dataset candidate`, `sample unit`, and `problem-representation structure`.

| Category | How it should be read here |
| --- | --- |
| `DSS/BI/DW/OLAP` | the background context of collecting data and connecting it to decisions |
| Storage structure | a table designed to preserve records without loss |
| Dataset candidate | a comparable table where samples have been regrouped so they answer the same question |
| Sample unit | the criterion that decides what counts as one case |

In other words, a dataset is not `just a table with many rows`. It is closer to a table where samples grouped to answer the same question are gathered together and the columns describing those samples are organized alongside them. So one row in storage structure does not automatically become one sample in a dataset.

Suppose there is source data for automatically executed actions. Control parameters and sensor values accumulated over time can be stored directly in a storage table. Each row can hold a time point, a sensor name, a measured value, and a control-setting value. This structure is suitable for preserving records and tracing detailed flow when a problem appears.

But from that table alone, it is still hard to answer questions such as `was this action longer than usual?`, `was the late-stage drop unusually slow?`, or `have the most recent 20 cases changed relative to the baseline?` That is because one row in storage structure usually means `one time-point record`, while the comparison unit required by those questions is `one full action` or `a recent segment formed by grouping multiple actions`. So the mere fact that stored records exist does not mean a dataset already exists.

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

These three questions are a quick way to separate `is the record in hand already a dataset, or is it still only a dataset candidate?` The first asks about the meaning of a row, the second asks about comparability, and the third asks when the raw logs must be reopened. Data modeling is the work of rerepresenting stored records so those three questions can be answered.

In storage structure, what matters is preserving everything without omission. In problem-representation structure, by contrast, we have to decide `what should remain` and `what should be discarded`. For example, once we decide to treat one full action as one sample, we can replace hundreds of time-point rows with new columns such as total action time, early-stage mean, late-stage drop rate, or tracking error. This does not damage the storage structure. It designs a new representation to answer a different question.

The small table below immediately shows how the same source data is read differently depending on the purpose.

| Structure | Example columns | What one row means |
| --- | --- | --- |
| Storage structure | `timestamp`, `sensor_name`, `value` | one time-point record |
| Problem-representation structure | `event_id`, `mid_flow_mean`, `late_drop_rate` | a summary of one action |

## A Small Diagram

It becomes clearer that stored records do not immediately become a dataset when the split between `record preservation` and `regrouping for a question` is reread as the flow below.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-1-mermaid-01-en.mmd"
```

Problem situation: confirm that the same source record remains as time-point rows in storage structure, but is regrouped into an action-level summary table in the dataset candidate.

Input: a flow-log table stored as time-point records under each `event_id` and the minimum number of time points required to treat an action as one event, `min_points_per_event`

Expected output: a display in which the same records are separated into two different table roles, `stored time-step records` and `event-level dataset candidate`, and events that do not meet the criterion are excluded from comparison candidates

Concept to check: the fact that stored records exist is not the same as the fact that a dataset candidate able to answer a question has been prepared. If `min_points_per_event` changes, which records are accepted as one action sample also changes.

```python
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

dataset_candidate = (
    storage_table.groupby("event_id")
    .agg(
        point_count=("second", "count"),
        duration_seconds=("second", "max"),
        mean_flow=("flow", "mean"),
        late_drop_rate=("flow", lambda values: values.iloc[-1] - values.iloc[-2]),
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

So when we say that stored records are not yet a dataset, it means less `the format is different` and more `the unit that will answer the question and the derived representation still have not been decided`.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`. Because it explains the example unit and the role of features separately, it supports the core point of this section that a stored row and a comparable sample row may differ. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Oracle, `Introduction to Data Warehousing Concepts`. Because it explains that a data warehouse is designed for business intelligence activities, query and analysis, maintaining historical records, and data analysis, it supports the opening context that `DSS/BI/DW/OLAP` connects stored data to decision making and analysis. [https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html](https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance, derivation, and traceability together, it strengthens the higher-level frame that storage structure preserves raw evidence while problem-representation structure creates derived representations for different questions. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it organizes the relationship among variables, observations, and table structure, it provides the general principle behind the explanation that one row in storage structure and one row in an analysis table may not mean the same thing. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
