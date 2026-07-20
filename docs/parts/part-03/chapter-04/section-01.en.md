# P3-4.1 How Do We Decide One Comparable Sample

> Section ID: `P3-4.1`
> Version: `v2026.07.20`

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

## A Small Diagram

Compressed into one line, the earlier judgment says that we must choose `the question to answer now` first and then choose the unit that matches that question as the sample. In this section, the question is `was this action unusual?`, so `one full action` leads most naturally to the comparable sample.

--8<-- "assets/part-03/chapter-04/p3-4-1-mermaid-01-en.mmd"

Problem situation: confirm that even with the same source log, the comparable table changes depending on whether `one time point`, `one full action`, or `one recent segment` is read as one sample.

Input: time-point records by `event_id` in [p3_4_1_measurement_log.csv](/AiBook/assets/part-03/chapter-04/p3_4_1_measurement_log.csv), event-level review results in [p3_4_1_review_decisions.csv](/AiBook/assets/part-03/chapter-04/p3_4_1_review_decisions.csv), and `question_focus_options`, the candidate questions we are currently trying to answer

One row in the first CSV is a measurement taken at one time point during an action. One row in the second CSV is a review result attached after one full action has ended. Some events may have too few time-point rows or no review result yet, so the code must first rebuild the sample unit and separately check completeness and whether labels can be joined.

Expected output: the units `measurement_row`, `event`, and `window` produce different sample counts and different possibilities for features. When the question focus and the event-completeness threshold change, the recommended unit and valid sample count change with them.

Concept to check: one comparable sample is determined not by the number of visible rows, but by the analysis unit that matches the question. The sample unit is not a fixed answer; it is chosen according to the question and the connectivity of features and labels.

```python
# This example regroupes raw measurement logs into the sample unit that matches the question and checks comparability.
import pandas as pd

measurement_log_path = "docs/assets/part-03/chapter-04/p3_4_1_measurement_log.csv"
review_decisions_path = "docs/assets/part-03/chapter-04/p3_4_1_review_decisions.csv"

question_focus_options = ["instant_value", "event_comparison", "recent_vs_baseline"]
selected_question_focus = "event_comparison"
expected_rows_per_event = 3

raw = pd.read_csv(measurement_log_path)
review_decisions = pd.read_csv(review_decisions_path)

row_counts = raw.groupby("event_id", as_index=False).size().rename(columns={"size": "measurement_rows"})

event_summary = (
    raw.groupby("event_id", as_index=False)
    .agg(
        total_duration_seconds=("elapsed_seconds", "max"),
        pressure_mean=("pressure", "mean"),
        pressure_rise=("pressure", lambda s: s.iloc[-1] - s.iloc[0]),
        flow_mean=("flow", "mean"),
        is_recent=("is_recent", "max"),
    )
    .merge(row_counts, on="event_id")
    .merge(review_decisions, on="event_id", how="left")
)
matched_review_decisions = review_decisions[
    review_decisions["event_id"].isin(event_summary["event_id"])
].reset_index(drop=True)
event_summary["is_complete_event_sample"] = (
    event_summary["measurement_rows"] >= expected_rows_per_event
)
event_summary["has_review_label"] = event_summary["review_needed"].notna()
event_summary["window_name"] = event_summary["is_recent"].map({0: "baseline", 1: "recent"})
event_summary["pressure_mean_for_complete"] = event_summary["pressure_mean"].where(
    event_summary["is_complete_event_sample"]
)
event_summary["flow_mean_for_complete"] = event_summary["flow_mean"].where(
    event_summary["is_complete_event_sample"]
)

window_summary = (
    event_summary.groupby("window_name", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        complete_event_count=("is_complete_event_sample", "sum"),
        labeled_event_count=("has_review_label", "sum"),
        pressure_mean_complete=("pressure_mean_for_complete", "mean"),
        flow_mean_complete=("flow_mean_for_complete", "mean"),
    )
)

unit_check = pd.DataFrame(
    [
        {
            "unit_name": "measurement_row",
            "sample_count": len(raw),
            "valid_sample_count": len(raw),
            "can_use_pressure_rise": "no",
            "label_attaches_naturally": "weak",
            "feature_score": 1,
            "label_score": 0,
        },
        {
            "unit_name": "event",
            "sample_count": len(event_summary),
            "valid_sample_count": int(event_summary["is_complete_event_sample"].sum()),
            "can_use_pressure_rise": "yes",
            "label_attaches_naturally": "yes",
            "feature_score": 3,
            "label_score": 2,
        },
        {
            "unit_name": "window",
            "sample_count": len(window_summary),
            "valid_sample_count": len(window_summary),
            "can_use_pressure_rise": "partial",
            "label_attaches_naturally": "weak",
            "feature_score": 2,
            "label_score": 1,
        },
    ]
)
recommended_unit = {
    "instant_value": "measurement_row",
    "event_comparison": "event",
    "recent_vs_baseline": "window",
}[selected_question_focus]
unit_check["selected_for_question"] = unit_check["unit_name"] == recommended_unit
unit_check["question_match_score"] = unit_check["selected_for_question"].map({True: 2, False: 0})
unit_check["total_score"] = (
    unit_check["feature_score"] + unit_check["label_score"] + unit_check["question_match_score"]
)

focus_result = pd.DataFrame(
    [
        {
            "question_focus": focus,
            "recommended_unit": {
                "instant_value": "measurement_row",
                "event_comparison": "event",
                "recent_vs_baseline": "window",
            }[focus],
        }
        for focus in question_focus_options
    ]
)

print("1) raw input files")
print("measurement_log shape:", raw.shape)
print("review_decisions shape:", review_decisions.shape)
print()
print("2) first raw measurement rows")
print(raw.head(8).to_string(index=False))
print()
print("3) count rows under each candidate unit")
print("measurement rows:", len(raw))
print("event samples:", len(event_summary))
print("window aggregates:", len(window_summary))
print()
print("4) raw rows still mean per-time-step records")
print(row_counts.to_string(index=False))
print()
print("5) review labels arrive at event_id level")
print(matched_review_decisions.to_string(index=False))
print()
print("6) event-level summaries check completeness and labels")
print(
    event_summary[
        [
            "event_id",
            "total_duration_seconds",
            "measurement_rows",
            "is_complete_event_sample",
            "pressure_mean",
            "pressure_rise",
            "flow_mean",
            "review_needed",
            "has_review_label",
        ]
    ].round(3).to_string(index=False)
)
print()
print("7) window-level aggregates are for broader comparison, not single-sample judgment")
print(window_summary.round(3).to_string(index=False))
print()
print("8) question focus changes the recommended unit")
print(focus_result.to_string(index=False))
print()
print("9) unit check for selected_question_focus = event_comparison")
print(unit_check.to_string(index=False))
```

Expected output:

```text
1) raw input files
measurement_log shape: (36, 5)
review_decisions shape: (36, 2)

2) first raw measurement rows
event_id  elapsed_seconds  pressure  flow  is_recent
     E01                0       1.0   0.0          1
     E01                1       2.0   1.4          1
     E01                2       2.4   1.6          1
     E02                0       1.1   0.0          0
     E02                1       1.7   1.1          0
     E02                2       2.0   1.2          0
     E03                0       1.2   0.1          1
     E03                1       2.3   1.5          1

3) count rows under each candidate unit
measurement rows: 36
event samples: 12
window aggregates: 2

4) raw rows still mean per-time-step records
event_id  measurement_rows
     E01                 3
     E02                 3
     E03                 3
     E04                 3
     E05                 3
     E06                 3
     E07                 3
     E08                 3
     E09                 3
     E10                 3
     E11                 3
     E12                 3

5) review labels arrive at event_id level
event_id  review_needed
     E01              1
     E02              0
     E03              1
     E04              0
     E05              0
     E06              0
     E07              1
     E08              0
     E09              1
     E10              0
     E11              1
     E12              0

6) event-level summaries check completeness and labels
event_id  total_duration_seconds  measurement_rows  is_complete_event_sample  pressure_mean  pressure_rise  flow_mean  review_needed  has_review_label
     E01                       2                 3                      True          1.800            1.4      1.000              1              True
     E02                       2                 3                      True          1.600            0.9      0.767              0              True
     E03                       2                 3                      True          2.067            1.5      1.133              1              True
     E04                       2                 3                      True          1.233            0.6      0.633              0              True
     E05                       2                 3                      True          1.667            1.2      0.767              0              True
     E06                       2                 3                      True          1.733            0.9      0.800              0              True
     E07                       2                 3                      True          1.900            1.4      0.933              1              True
     E08                       2                 3                      True          1.467            0.8      0.700              0              True
     E09                       2                 3                      True          2.200            1.6      1.200              1              True
     E10                       2                 3                      True          1.633            0.9      0.700              0              True
     E11                       2                 3                      True          2.000            1.4      1.067              1              True
     E12                       2                 3                      True          1.267            0.8      0.567              0              True

7) window-level aggregates are for broader comparison, not single-sample judgment
window_name  event_count  complete_event_count  labeled_event_count  pressure_mean_complete  flow_mean_complete
   baseline            6                     6                    6                   1.489               0.694
     recent            6                     6                    6                   1.939               1.017

8) question focus changes the recommended unit
    question_focus recommended_unit
     instant_value  measurement_row
  event_comparison            event
recent_vs_baseline           window

9) unit check for selected_question_focus = event_comparison
      unit_name  sample_count  valid_sample_count can_use_pressure_rise label_attaches_naturally  feature_score  label_score  selected_for_question  question_match_score  total_score
measurement_row            36                  36                    no                     weak              1            0                  False                     0            1
          event            12                  12                   yes                      yes              3            2                   True                     2            7
         window             2                   2               partial                     weak              2            1                  False                     0            3
```

What we should see first in this output is `how many cases are being counted`. In the raw table, there are 36 measurement time points; when grouped by `event_id`, there are 12 candidate action-level samples; and when grouped again into recent versus baseline segments, there are 2 aggregates for comparison. But the next thing to see is `which values become meaningful only at which unit`. The review results are not repeatedly injected into raw time-point rows. They arrive separately at the `event_id` level and are then joined to the one-action summary table. The values to manipulate here are `selected_question_focus`, `question_focus_options`, and `expected_rows_per_event`. With `"event_comparison"`, one full action becomes the recommended unit. If it is changed to `"instant_value"`, a measurement time-point row is more natural. If it is changed to `"recent_vs_baseline"`, the recent/baseline segment aggregate is more natural. If `expected_rows_per_event` is raised to `4`, all 12 current events fall out of the complete event-sample set. In other words, even with the same source data, choosing whether to read `one time point`, `one full action`, or `one recent segment` as one sample changes the row count, the meaning of the table, the role of the columns that can sit on top of it, and the valid sample count together.

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

- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it provides a general basis for keeping explainable which object was chosen as the analytical unit among different units such as time-point records, one full action, and recent segments. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example should be the unit on which features and label attach naturally, it strengthens the point that the sample should be a unit such as one full action, rather than a time-point row. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains that a base period is a reference for comparison with another period, it provides a general basis for the claim that before comparing with a baseline segment, we must first decide what the comparison unit itself is. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
