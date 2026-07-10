# P3-4.1 How Do We Decide One Comparable Sample

> Section ID: `P3-4.1`
> Version: `v2026.07.10`

The first thing to confirm when reading data is not the size of the values, but `what does one row mean?` If this question is not settled first, then the criteria drift later when features are built, when labels are attached, and even when evaluation results are read. In the end, this question leads to `what should count as one comparable sample?`

Suppose that in an automatically executed action, both control-parameter time series and sensor time series remain recorded. In one table, one row may mean `the pressure and flow measurement at the 1-second time point`. In another table, one row may mean `the summary of one full action`. In yet another table, one row may mean `the aggregate result of several actions executed during the most recent 30 minutes`. All three come from the same source data, but the object that one row means is completely different.

| Category | What one row means | The question it mainly answers |
| --- | --- | --- |
| Measurement table | one sensor or control value at one time point during the action | What is the value at this time point? |
| Action-level table | one full automatically executed action | What was the overall structure of this action? |
| Recent-segment table | a recent aggregate formed by grouping several actions | Is the recent change repeating? |
| Baseline table | a comparison aggregate that represents the usual state | How different is the current state from the usual one? |

This table shows that even with the same data, `the meaning of one row` changes according to what question we are trying to answer. A measurement table is strong for reading the current state, but it cannot immediately show the structure of the full action. By contrast, an action-level table is useful for comparing one action, but it does not preserve moment-by-moment changes as they were. A recent-segment table and a baseline table go one step further and mean not `one case`, but `a comparison structure made by grouping several cases`. So the fact that rows are visible in front of us does not mean we can treat that row as one sample. If what the model must learn is `the pattern of the full action`, then several time-point measurement rows must be regrouped into a new sample called `one action`.

To call something a `comparable sample` here, at least three things must be satisfied together.

1. The boundary of one case has to be clear.
2. The same kinds of features must be attachable to all cases in the same way.
3. The labels or comparison criteria attached later must connect naturally to that unit.

Using those three criteria, a per-time-point measurement row usually satisfies only the first, while the second and third are weak. By contrast, an action-level summary table often satisfies all three. A recent-segment table is strong in the third sense of comparison criteria, but it is closer to an interpretation structure formed by regrouping several samples than to an individual sample comparison. So what this section must decide is which of `one time point`, `one full action`, and `one recent segment` should count as one comparable sample.

When a table first arrives in front of us, the role distinction becomes clearer if we read it in the following order.

1. Check whether one row in the current table means `one time point`, `one full action`, or `an aggregate of several actions`.
2. Check what question that row was created to answer.
3. Confirm whether that question matches the problem we are currently trying to solve.

Once we go through this order, we can delay the automatic assumption that `if there are rows, then there must already be samples`. That is what keeps us from mixing raw logs, summary tables, and recent-segment tables together as if they were the same kind of table.

The small table below makes this difference clearer.

| event_id | elapsed_seconds | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |
| B | 0 | 1.1 | 0.0 |
| B | 1 | 1.7 | 1.1 |
| B | 2 | 2.0 | 1.2 |

In this table, one row is not `one full action`, but `one time point during the action`. So if we want one sample to mean one full action, then several rows with the same `event_id` must be grouped together. And if we look one step more closely here, even with the same source data, choosing whether to read `one time point`, `one full action`, or `one recent segment` as one case changes not only the number of samples, but also which columns make sense only at that unit.

If we reread the same example now with the three criteria above, it becomes clearer why `one full action` is closer to a comparable sample.

| Candidate unit | Is the boundary clear? | Is it easy to attach the same features? | Is it natural to attach labels / comparison criteria? |
| --- | --- | --- | --- |
| one measurement row | Yes | Weak | Weak |
| one full action | Yes | Yes | Yes |
| one recent-segment bundle | Yes | Only partly | Strong for comparison criteria, weak for individual-sample labels |

In other words, if we take `one full action` as one sample, then features such as `pressure_mean`, `pressure_rise`, and `flow_mean` can be attached to all cases in the same way, and later results such as `needs review`, `normal`, or `anomalous` also connect naturally at that unit. By contrast, one measurement row is good for holding an instant observation value, but it is difficult to place features and labels on it stably when the goal is to compare the structure of the whole action. A recent-segment bundle is closer not to an individual action-comparison sample, but to an interpretation unit formed by regrouping several actions.

So in practice, `which unit should be chosen first as the sample?` can be decided as follows.

| The question we are trying to answer now | Sample unit to choose first | Why |
| --- | --- | --- |
| Was this action more anomalous than other actions? | one full action | Because the comparison target is `action versus action` |
| At what time point did the pressure rise sharply? | measurement time point | Because the question itself asks about the time point of the momentary change |
| Has the recent operating state changed from the usual one? | one recent-segment bundle | Because the comparison target is not an individual action, but a recent bundle and a baseline bundle |
| Can we build an input table that will later predict `needs review`? | one full action | Because the result is usually attached at the action level, and features are also computed stably there |

So what should count as one sample is not decided from the shape of the table alone. It has to be decided first according to whether the current question is `time-point comparison`, `action comparison`, or `segment comparison`. In the example of this section, the question is `comparing the pattern of the whole action`, so one full action becomes the most natural sample unit.

Problem situation: confirm that even with the same source log, the comparable table changes depending on whether `one time point`, `one full action`, or `one recent segment` is read as one sample.

Input: a raw log table containing time-point records by `event_id`, together with a flag showing whether each record belongs to the recent segment

Expected output: the units `measurement_row`, `event`, and `window` produce different sample counts and different possibilities for features

Concept to check: one comparable sample is determined not by the number of visible rows, but by the analysis unit that matches the question

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "pressure": 1.0, "flow": 0.0, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 1, "pressure": 2.0, "flow": 1.4, "is_recent": 1, "review_needed": 1},
        {"event_id": "A", "elapsed_seconds": 2, "pressure": 2.4, "flow": 1.6, "is_recent": 1, "review_needed": 1},
        {"event_id": "B", "elapsed_seconds": 0, "pressure": 1.1, "flow": 0.0, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 1, "pressure": 1.7, "flow": 1.1, "is_recent": 0, "review_needed": 0},
        {"event_id": "B", "elapsed_seconds": 2, "pressure": 2.0, "flow": 1.2, "is_recent": 0, "review_needed": 0},
        {"event_id": "C", "elapsed_seconds": 0, "pressure": 1.2, "flow": 0.1, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 1, "pressure": 2.3, "flow": 1.5, "is_recent": 1, "review_needed": 1},
        {"event_id": "C", "elapsed_seconds": 2, "pressure": 2.7, "flow": 1.8, "is_recent": 1, "review_needed": 1},
    ]
)

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        pressure_mean=("pressure", "mean"),
        pressure_rise=("pressure", lambda s: s.iloc[-1] - s.iloc[0]),
        flow_mean=("flow", "mean"),
        is_recent=("is_recent", "max"),
        review_needed=("review_needed", "max"),
    )
)

window_summary = (
    event_summary.groupby("is_recent", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        pressure_mean=("pressure_mean", "mean"),
        flow_mean=("flow_mean", "mean"),
    )
    .assign(window_name=lambda df: df["is_recent"].map({0: "baseline", 1: "recent"}))
    [["window_name", "event_count", "pressure_mean", "flow_mean"]]
)

unit_check = pd.DataFrame(
    [
        {
            "unit_name": "measurement_row",
            "sample_count": len(raw),
            "can_use_pressure_rise": "no",
            "label_attaches_naturally": "weak",
        },
        {
            "unit_name": "event",
            "sample_count": len(event_summary),
            "can_use_pressure_rise": "yes",
            "label_attaches_naturally": "yes",
        },
        {
            "unit_name": "window",
            "sample_count": len(window_summary),
            "can_use_pressure_rise": "partial",
            "label_attaches_naturally": "weak",
        },
    ]
)

print("1) count rows under each candidate unit")
print("measurement rows:", len(raw))
print("event samples:", len(event_summary))
print("window aggregates:", len(window_summary))
print()
print("2) raw rows still mean per-time-step records")
print(raw.groupby("event_id").size().reset_index(name="measurement_rows"))
print()
print("3) event-level summaries can hold comparison features and labels")
print(
    event_summary[
        [
            "event_id",
            "total_duration_seconds",
            "pressure_mean",
            "pressure_rise",
            "flow_mean",
            "review_needed",
        ]
    ]
)
print()
print("4) window-level aggregates are for broader comparison, not single-sample judgment")
print(window_summary)
print()
print("5) unit check for comparable-sample suitability")
print(unit_check)
```

Expected output:

```text
1) count rows under each candidate unit
measurement rows: 9
event samples: 3
window aggregates: 2

2) raw rows still mean per-time-step records
  event_id  measurement_rows
0        A                 3
1        B                 3
2        C                 3

3) event-level summaries can hold comparison features and labels
  event_id  total_duration_seconds  pressure_mean  pressure_rise  flow_mean  review_needed
0        A                       2       1.800000            1.4   1.000000              1
1        B                       2       1.600000            0.9   0.766667              0
2        C                       2       2.066667            1.5   1.133333              1

4) window-level aggregates are for broader comparison, not single-sample judgment
  window_name  event_count  pressure_mean  flow_mean
0    baseline            1       1.600000   0.766667
1      recent            2       1.933333   1.066667

5) unit check for comparable-sample suitability
         unit_name  sample_count can_use_pressure_rise label_attaches_naturally
0  measurement_row             9                    no                      weak
1            event             3                   yes                       yes
2           window             2               partial                      weak
```

What we should see first in this output is `how many cases are being counted`. In the raw table, there are 9 measurement time points; when grouped by `event_id`, there are 3 action-level samples; and when grouped again into recent versus baseline segments, there are 2 aggregates for comparison. But the next thing to see is `which values become meaningful only at which unit`. A column such as `pressure_rise`, which looks at the difference between the starting point and the ending point, cannot be created from one time-point row. It becomes meaningful only after the data is grouped into one full action. By contrast, `window_summary` is not a table for comparing individual actions, but a comparison-interpretation table built by grouping several actions together. So even with the same source data, depending on whether `one time point`, `one full action`, or `one recent segment` is read as one sample, the row count, the meaning of the table, and the role of the columns that can sit on top of it all change together.

Here the `unit check` output shows the judgment of this section even more directly. `measurement_row` has the largest sample count, but it cannot hold `pressure_rise` directly, and it is also hard for a result such as `review_needed` to attach naturally. `window` can be used to interpret the recent state, but it is weak as an individual action-comparison sample. By contrast, `event` places the sample count, summary features, and result column on the same unit, so it best fits this section's question of `one comparable sample`.

This example does not merely show how to count sample units.

| Value visible here | At which unit it is natural | Why |
| --- | --- | --- |
| one-time-point values such as `pressure`, `flow` | measurement time point | because they are observation values at that instant |
| `pressure_mean`, `pressure_rise` | one full action | because they are summary values that only exist after several time points are grouped |
| `event_count`, recent averages | recent segment or baseline segment | because they are comparison aggregates made by regrouping several actions |

Seen this way, `deciding one sample` is not just about reducing the row count. It is also about deciding which columns read naturally at the current unit.

When a table first arrives, a very quick diagnosis can also be done as follows. This quick diagnosis also reveals the stage in the data lifecycle. A measurement table is closer to observation and recording, an action-level table is closer to a comparable-sample representation, and a recent-segment table and baseline table are closer to interpretation and decision preparation.

| If the current table looks like this | The row meaning to suspect first |
| --- | --- |
| it has a time column and the same `event_id` repeats several times | it is likely a one-time-point record |
| there is only one line per `event_id`, with summary columns such as mean, max, and slope | it is likely a one-full-action sample |
| there are comparison columns such as recent-20 mean and prior-200 mean | it is likely an aggregate over several actions |

The purpose of this diagnosis table is not to memorize table names. It is to quickly separate whether the rows in hand are `samples that can be compared immediately` or `records that still need to be regrouped into samples`.

Only after an action-level summary table exists can features such as means, slopes, and variability be built stably, and only then can recent-segment and baseline comparison be read on the same unit. So the question `what does one row mean?` does not stop at deciding one sample unit. It becomes a floor rule that supports the later structures of all of Part 3.

A comparable sample is not determined first by the data itself. It is determined together by the comparison unit required by the question and the feature and label structure that will sit on top of it. So when we say `decide one sample`, it does not mean recounting rows. It means deciding which object, between observation unit and aggregate unit, will be treated as the comparable analytical unit.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it provides a general basis for keeping explainable which object was chosen as the analytical unit among different units such as time-point records, one full action, and recent segments. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example should be the unit on which features and label attach naturally, it strengthens the point that the sample should be a unit such as one full action, rather than a time-point row. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains that a base period is a reference for comparison with another period, it provides a general basis for the claim that before comparing with a baseline segment, we must first decide what the comparison unit itself is. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
