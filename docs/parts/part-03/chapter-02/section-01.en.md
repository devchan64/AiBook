# P3-2.1 Why Must Stored Records Be Reorganized for the Analysis Purpose

> Section ID: `P3-2.1`
> Version: `v2026.09.19`

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

In storage structure, what matters is preserving everything without omission. In problem-representation structure, by contrast, we have to decide `what should remain` and `what should be discarded`. For example, once we decide to treat one full action as one sample, we can preserve the raw records and separately create columns such as the observed time span, mean flow, and slope of the last observed interval. This does not damage the storage structure. It designs a new representation to answer a different question.

The small table below immediately shows how the same source data is read differently depending on the purpose.

| Structure | Example columns | What one row means |
| --- | --- | --- |
| Storage structure | `timestamp`, `sensor_name`, `value` | one time-point record |
| Problem-representation structure | `event_id`, `mean_flow`, `last_interval_slope` | a summary of one action |

## From Preserving Records to Restructuring for a Question {#a-small-diagram}

The possible need to reorganize stored records for a question becomes clearer when we separate `preserving records` from `regrouping them for the question`, as below.

<div class="aibook-diagram-scroll" role="region" tabindex="0" aria-label="Diagram: scroll horizontally to read" markdown="1">
<div class="aibook-diagram-canvas" markdown="1">

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-1-mermaid-01-en.mmd"
```

</div>
</div>

## Tracing a summary row back to the original records

The following fictional records A, B, and C are separate from A-101 in the previous chapter. `event_id` identifies the action, `second` is elapsed time since its start, and `flow` is flow in L/min. First, look at A's three records.

| event_id | second | flow (L/min) |
| --- | ---: | ---: |
| A | 0 | 0.8 |
| A | 1 | 1.4 |
| A | 2 | 1.2 |

Grouping A into one row gives 3 records, an observed time span of `2−0 = 2 seconds`, and mean flow `(0.8+1.4+1.2)/3 ≈ 1.13 L/min`. The slope of the last observed interval is `(1.2−1.4)/(2−1) = −0.2 L/min/s`. The meaning of these calculations is the same as in [P3-1.1](../chapter-01/section-01.en.md).

| What the summary retains | What this summary cannot reconstruct | Evidence to revisit |
| --- | --- | --- |
| Identifier A, 3 points, 2-second observed span | All individual measurements and their times | Rows with `event_id=A` in the raw table |
| Mean 1.13 L/min, final-interval slope −0.2 L/min/s | The full sequence, including the rise to 1.4 at 1 second | A's time and flow records in order |
| Whether the stored point count passes a condition | Whether the actual end was observed or intermediate records are missing | Action-end records and checks of sampling intervals and missing records |

Keeping the identifier allows a return from the summary to the raw records. If action IDs repeat across equipment, include the equipment ID as well. Here, assume A, B, and C uniquely identify distinct actions.

## Changing the point-count condition changes the candidate set

Problem: A and B have 3 observations, while C has 2. Apply the same aggregation code, then change the point-count condition from 3 to 2 to see which actions pass.

Input: Time-point records grouped by `event_id`, and the minimum observation count `min_points_per_event`.

Expected output: The raw table, an action-summary table, and rows passing the point-count condition. Passing does not establish that an action is complete or that actions are comparable.

Concept to inspect: Separate having values that can be calculated, passing a count condition, and observing the entire action. Two points suffice to calculate the last observed interval's slope. The default 3 is a candidate-selection condition for this experiment, not the mathematical minimum for every metric.

There are no missing values or duplicate timestamps in this input, and all observed intervals are 1 second. The slope calculation below assumes this fixed interval. If you change the timestamps, also change the calculation to divide by the actual time difference. `observed_span_seconds` is the difference between the last and first stored timestamps; it is not necessarily the actual duration of an action with a confirmed end.

```python
# Regroup stored time-point records into event-level dataset candidates.
import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 120)

min_points_per_event = 3  # Lower to 2 to check C; this is not a completion check.

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
        observed_span_seconds=("second", lambda values: values.max() - values.min()),
        mean_flow=("flow", "mean"),
        last_interval_slope=("flow", lambda values: values.iloc[-1] - values.iloc[-2] if len(values) >= 2 else float("nan")),
    )
    .reset_index()
)
dataset_candidate["passes_point_count"] = (
    dataset_candidate["point_count"] >= min_points_per_event
)
count_filtered_candidate = dataset_candidate[dataset_candidate["passes_point_count"]]

print("1) stored time-step records")
print(storage_table)
print()
print(f"2) event-level dataset candidate when min_points_per_event = {min_points_per_event}")
print(dataset_candidate.round(2))
print()
print("3) rows passing the point-count condition")
print(count_filtered_candidate.round(2))
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
  event_id  point_count  observed_span_seconds  mean_flow  last_interval_slope  passes_point_count
0        A            3                      2       1.13                 -0.2                True
1        B            3                      2       0.80                 -0.5                True
2        C            2                      1       0.95                  0.1               False

3) rows passing the point-count condition
  event_id  point_count  observed_span_seconds  mean_flow  last_interval_slope  passes_point_count
0        A            3                      2       1.13                 -0.2                True
1        B            3                      2       0.80                 -0.5                True
```

In the first table, each row is a time-point record; in the second, it summarizes the records associated with one action identifier. True in `passes_point_count` means **only that the count condition was met**. At the default 3, only A and B pass. Lowering it to 2 also admits C, but C's slope of +0.1 describes 0–1 seconds, while A and B describe 1–2 seconds. Identically named columns refer to different intervals, so these values alone cannot compare the ends of the actions.

The following chart aligns the three actions on identical axes. Dots are observations; thick segments mark each action's last observed interval. Connecting lines indicate measurement order and do not establish the path between observations.

<div class="aibook-diagram-scroll" role="region" tabindex="0" aria-label="Chart: scroll horizontally to read" markdown="1">
<div class="aibook-diagram-canvas" style="min-width: 700px" markdown="1">

![A and B have a last interval of 1–2 seconds, while C has only 0–1 seconds](/AiBook/assets/part-03/chapter-02/p3-2-1-observed-intervals-en.png)

</div>
</div>

The gray region after C's 1-second observation means there are no later records. It does not mean flow is zero or that the action ended. No line is extended into that region.

In particular, C's `observed_span_seconds=1` does not establish that the action ended after 1 second. It may actually have ended then, or continued without further records. Nor do A and B's three points prove that their ends were observed. This input has no confirmation of action completion.

Point count and measurement spacing are also separate. If only A's timestamps change to 0, 1, and 4 seconds, the count remains 3 and mean flow is unchanged. But the observed span becomes 4 seconds, and the last slope is `(1.2−1.4)/(4−1) ≈ −0.067 L/min/s`. Code that assumes 1-second spacing still returns −0.2, leading to an incorrect interpretation. Thus, **counting enough points does not replace checking the time axis**.

The two panels below use the same axis ranges and flow values. Only the time of the last observation changes from 2 to 4 seconds.

<div class="aibook-diagram-scroll" role="region" tabindex="0" aria-label="Chart: scroll horizontally to read" markdown="1">
<div class="aibook-diagram-canvas" style="min-width: 700px" markdown="1">

![The same three flow values give different slopes when the last interval changes from 1 to 3 seconds](/AiBook/assets/part-03/chapter-02/p3-2-1-time-spacing-en.png)

</div>
</div>

The flow difference is −0.2 L/min in both panels, but it spans 1 second above and 3 seconds below. The shallower slope is caused by the changed time denominator, not a different point count or flow difference. The connecting segments do not confirm constant change throughout either interval.

It is also useful to check briefly where we get stuck if we keep the same data in storage structure without changing it.

| Question we immediately want to ask | The problem when storage structure is used as-is |
| --- | --- |
| Was this one action longer than usual? | Time-point records alone do not confirm completion; start and end records are also needed |
| Can we select only the actions with a slow late-stage drop? | Unless the late segment is grouped and summarized first, there is no comparison column |
| Can we directly compare the most recent 20 cases with the prior 200? | Even with action identifiers, the periods and conditions for recent and past groups must be defined separately |

So storage structure shows `what was recorded`, but it does not automatically decide `what should be compared as one case`. Rebuilding a dataset candidate means filling in exactly that blank.

One warning is necessary here. Problem-representation structure does not replace storage structure. Creating a summary table does not make raw logs unnecessary. On the contrary, if the summary table shows a strange change, we need to return to storage structure and inspect the detailed time points again. Storage structure preserves evidence, while problem-representation structure makes comparison possible. They are not competing structures, but linked structures with different roles.

This relationship can be summarized more briefly as follows.

| Question | Is storage structure strong here? | Is problem-representation structure strong here? |
| --- | --- | --- |
| What values were actually recorded? | Yes | only partially |
| What was the structure of this one action? | Difficult | Yes |
| Has the recent segment changed from the usual one? | Difficult | Yes |

This table shows that the difference between storage structure and problem-representation structure is not merely `a difference in table shape`, but `a difference in the questions that can be answered`. How a table was stored and which questions it can answer are not the same problem. That is why the first task at the front of Part 3 is not to look at records and imagine model names, but to ask into what dataset candidate those records should be reread.

More broadly, this section separates `preserving source records`, `resetting the analysis unit`, and `creating derived representations` as work at different levels, and determines what regrouping and additional checks the current question requires.

The first thing to check is therefore not what the material is called, but whether the unit and derived representation needed to answer the current question have been defined.

## Checklist

- Can you trace A's summary row back to its three original records and reproduce its mean and last-interval slope?
- Can you name one piece of information retained in the summary and one that requires reopening the raw table?
- Why does C passing after `min_points_per_event` is lowered to 2 not mean its slope describes the same interval as A and B?
- What action-end information and sampling intervals must you check before claiming that three points cover the entire action?
- Can you verify in the output that C's raw records and summary candidate remain even when C fails the count condition?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `example`, `labeled example`, `feature`. Because it explains the example unit and the role of features separately, it supports the core point of this section that a stored row and a comparable sample row may differ. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Oracle, `Introduction to Data Warehousing Concepts`. Because it explains that a data warehouse is designed for business intelligence activities, query and analysis, maintaining historical records, and data analysis, it provides background on storage structures designed for analysis. This does not mean stored tables are always unsuitable for analysis. [https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html](https://docs.oracle.com/en/database/oracle/oracle-database/26/dwhsg/introduction-data-warehouse-concepts.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance, derivation, and traceability together, it strengthens the higher-level frame that storage structure preserves raw evidence while problem-representation structure creates derived representations for different questions. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it organizes the relationship among variables, observations, and table structure, it provides the general principle behind the explanation that one row in storage structure and one row in an analysis table may not mean the same thing. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20

- [Google Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Checked the distinction among datasets, labeled examples, and unlabeled examples. Checked: 2026-09-15.
