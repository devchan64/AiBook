# P3-5.7 Rules for Folding Multiple Follow-Up Events

> Section ID: `P3-5.7`
> Version: `v2026.09.19`

_Subtitle: By what rule should multiple events after the same sample be folded into one table structure?_

Even after the [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) unit and the input window are fixed, one more point often blocks the table structure. It is the case where several follow-up events attach after the same sample. For example, after one action, we may record `review`, `warning`, `failure`, and `revisit` in sequence. If we do not decide how to fold them into one result column, the same sample can easily change meaning from table to table.

If there are several follow-up events, we should first write down by what [folding rule](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) they were folded into one table structure.

Common folding rules look like this.

| Folding rule | Meaning |
| --- | --- |
| `any` | If at least one occurred, write 1 |
| `first` | Keep the earliest follow-up event as the representative |
| `worst` | Keep the most severe state as the representative |
| `count` | Keep the number of occurrences itself |

For example, suppose the following follow-up events remained after the same samples.

| event_id | follow_up_events |
| --- | --- |
| A | review, failure |
| B | review |
| C | none |

Depending on how we fold this into a table, the meaning of the result column changes.

| event_id | any_failure | first_event | event_count |
| --- | ---: | --- | ---: |
| A | 1 | review | 2 |
| B | 0 | review | 1 |
| C | 0 | none | 0 |

So even when we are looking at the same [source event](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data), the table structure changes according to `what we choose as the representative result`. This is a data-modeling problem in which we must first decide by what rule the representative result will be folded and left in the table.

Leaving the notes below first reduces later confusion.

| Note to write down first | Why it is needed |
| --- | --- |
| Which follow-up events are treated as one bundle | To fix the result range handled by the table |
| Which of `any`, `first`, `worst`, `count` was used | To explain again what the result column means |
| Whether the folded result is for reporting or a prediction candidate | To avoid mixing comparison reports with target candidates |

The final table should also keep the folding rule traceable. For example, if you leave `folding_rule`, `severity_cutoff`, `follow_up_window_days`, `source_event_count`, and `target_candidate_name` in a memo, you can explain again what event range and threshold produced `any_selected_event=1`. Even from the same follow-up event log, `first_event` and `worst_event` are different columns, so do not freeze one column name as if it were the actual target label.

Before folding events into a result, define the observation period and deduplication rules. For `failure within 7 days`, a failure on day 9 is excluded. If a transmission retry stores the same event twice, compare event identifiers so that `count` does not count it twice. Define `first` using occurrence-time order, and establish tie-breaking rules for events at the same time or with the same severity.

The example below assumes follow-up is complete for the entire sample roster, the event log is already restricted to the analysis period, and there are no duplicates. Only under those assumptions can S30, which has no events, be assigned 0. A sample still under observation must remain `pending` even if no event has occurred.

Small example:

Problem situation: check that when several follow-up events exist after the same sample, different folding rules such as `first`, `worst`, `count`, and `any` create different result columns.

Input: the sample roster [p3_5_7_sample_roster.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_sample_roster.csv){ .csv-preview }, the follow-up event log [p3_5_7_follow_up_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv){ .csv-preview }, the event severity table [p3_5_7_event_severity.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_event_severity.csv){ .csv-preview }, and candidate severity thresholds for selection, `severity_cutoffs`

The first CSV has one row for each sample that must remain in the final result table. The second CSV has one row for each follow-up event that actually occurred after a sample. The third CSV turns event names into severity numbers so that the `worst` and `any_selected_event` rules can be calculated.

Expected output: output showing that even for the same source event, `first_event`, `worst_event`, `event_count`, `event_sequence`, `any_failure`, and `any_selected_event` are created differently. If `severity_cutoffs` changes, the number and list of selected samples also change.

Concept to check: when folding several follow-up events into one result column, we should first specify by what folding rule and [threshold](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-threshold) they were folded, so the meaning of the table structure does not drift

## Fold S01, S02, and S30 by Hand

The CSV files below are fictional data created for this example. The observation period is days 1–7 after each sample, inclusive, and follow-up is assumed complete for all 36 roster entries. `days_after_sample` gives a day index, not a precise occurrence time. The CSV has neither completion flags nor individual follow-up event IDs, so completeness and absence of duplicates cannot be verified from these files alone.

| sample_id | Records within the period | first_event | worst_event | event_count | any_failure |
| --- | --- | --- | --- | ---: | ---: |
| S01 | day 1 review → day 3 warning → day 5 failure | review | failure | 3 | 1 |
| S02 | day 2 review → day 4 warning | review | warning | 2 | 0 |
| S30 | none; follow-up assumed complete | none | none | 0 | 0 |

`any_failure` indicates whether any record has event type `failure` or `critical_failure`. This is the example's type mapping and does not change with the severity threshold. `count` counts all follow-up events in the period, not just failures. `first` hides later failures, while `worst` hides the earlier sequence of warnings and reviews; retain `event_sequence` when that order matters.

Severity is an ordinal ranking defined for this example. review=2, warning=3, and failure=4 specify an order; they do not mean failure is twice as severe as review. `any_selected_event` asks **whether an event reaches the selected severity threshold**, a different question from `any_failure`. S02 changes from 0 at threshold 4 to 1 at threshold 3, yet still has no failure record.

The example includes only days 1–7 and orders `first` by day index. Same-day ties use CSV row order, which does not establish actual chronological order. `worst` uses descending severity, ascending day index, then original row order. Operational data needs more precise occurrence times and event IDs to define tie handling and deduplication.

```python
# This example folds multiple follow-up events after the same sample into a table structure and chooses a representative label.
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_severity_cutoff = 4
severity_cutoffs = [4, 3, 2]
follow_up_window_days = 7
failure_types = {"failure", "critical_failure"}
preview_row_count = 12

def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

sample_roster = read_csv(sample_roster_path)
follow_ups = read_csv(follow_up_events_path)
severity_table = read_csv(event_severity_path)
severity_by_type = {row["event_type"]: int(row["severity"]) for row in severity_table}

for row in follow_ups:
    row["days_after_sample"] = int(row["days_after_sample"])
    row["severity"] = severity_by_type[row["event_type"]]

period_events = [row for row in follow_ups if 1 <= row["days_after_sample"] <= follow_up_window_days]
ordered_events = sorted(period_events, key=lambda row: (row["sample_id"], row["days_after_sample"]))
events_by_sample = defaultdict(list)
for row in ordered_events:
    events_by_sample[row["sample_id"]].append(row)

folded = []
for sample in sample_roster:
    sample_id = sample["sample_id"]
    events = events_by_sample.get(sample_id, [])
    if events:
        first_event = events[0]["event_type"]
        worst = sorted(events, key=lambda row: (-row["severity"], row["days_after_sample"]))[0]
        worst_event = worst["event_type"]
        worst_severity = worst["severity"]
        event_sequence = " > ".join(row["event_type"] for row in events)
    else:
        first_event = "none"
        worst_event = "none"
        worst_severity = 0
        event_sequence = "none"
    folded.append(
        {
            "sample_id": sample_id,
            "first_event": first_event,
            "worst_event": worst_event,
            "worst_severity": worst_severity,
            "event_count": len(events),
            "event_sequence": event_sequence,
            "any_failure": int(any(row["event_type"] in failure_types for row in events)),
            "any_selected_event": int(any(row["severity"] >= selected_severity_cutoff for row in events)),
        }
    )

cutoff_results = []
for cutoff in severity_cutoffs:
    selected = [row for row in folded if row["event_count"] > 0 and row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "severity_cutoff": cutoff,
            "selected_sample_count": len(selected),
            "selected_samples": ",".join(row["sample_id"] for row in selected) or "none",
        }
    )

print("1) raw follow-up events")
print("sample_id  days_after_sample       event_type source_system")
for row in follow_ups[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['days_after_sample']:>18} "
        f"{row['event_type']:>16} {row['source_system']:>13}"
    )
print(f"... {len(follow_ups) - preview_row_count} more follow-up events")
print()
print("2) severity rule table")
print("      event_type  severity")
for row in severity_table[:preview_row_count]:
    print(f"{row['event_type']:>16} {int(row['severity']):>9}")
print(f"... {len(severity_table) - preview_row_count} more severity rules")
print()
print(f"3) folded result when severity_cutoff = {selected_severity_cutoff}")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure  any_selected_event"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12} {row['any_selected_event']:>19}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by severity_cutoff")
print(
    " severity_cutoff  selected_sample_count"
    "                                                                     selected_samples"
)
for row in cutoff_results:
    print(
        f"{row['severity_cutoff']:>24} {row['selected_sample_count']:>21} "
        f"{row['selected_samples']:>83}"
    )
```

Expected output:

```text
1) raw follow-up events
sample_id  days_after_sample       event_type source_system
      S01                  1           review   human_queue
      S01                  3          warning       monitor
      S01                  5          failure   maintenance
      S02                  2           review   human_queue
      S02                  4          warning       monitor
      S03                  1          revisit       service
      S04                  1          warning       monitor
      S05                  1          revisit       service
      S05                  2           review   human_queue
      S06                  3 minor_adjustment      operator
      S07                  1          warning       monitor
      S07                  6          failure   maintenance
... 24 more follow-up events

2) severity rule table
      event_type  severity
            none         0
         revisit         1
minor_adjustment         1
      inspection         2
          review         2
         warning         3
         failure         4
critical_failure         5
    sensor_noise         0
   operator_note         1
     calibration         1
   slow_recovery         2
... 24 more severity rules

3) folded result when severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure  any_selected_event
      S01           review          failure               4            3 review > warning > failure            1                   1
      S02           review          warning               3            2           review > warning            0                   0
      S03          revisit          revisit               1            1                    revisit            0                   0
      S04          warning          warning               3            1                    warning            0                   0
      S05          revisit           review               2            2           revisit > review            0                   0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0                   0
      S07          warning          failure               4            2          warning > failure            1                   1
      S08           review           review               2            1                     review            0                   0
      S09          revisit          revisit               1            1                    revisit            0                   0
      S10          warning          warning               3            1                    warning            0                   0
      S11       inspection       inspection               2            1                 inspection            0                   0
      S12           review          warning               3            2           review > warning            0                   0
... 24 more folded samples

4) sensitivity by severity_cutoff
 severity_cutoff  selected_sample_count                                                                     selected_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

The selected-sample counts are 5 at threshold 4, 12 at threshold 3, and 21 at threshold 2. Lowering 4 to 3 adds **S02, S04, S10, S12, S16, S22, S28**, seven samples whose worst recorded event is warning. No new failures occurred: the selection scope widened. The number of samples with recorded failure types stays five.

Before running the code, predict the two indicators for S02 when `selected_severity_cutoff` becomes 3. The answer is `any_selected_event=1` and `any_failure=0`. Next, suppose S01's failure occurred on day 9 instead of day 5. Its seven-day results become first=review, worst=warning, count=2, any_failure=0. The event falls outside the observation period; it has not been deleted from the source history.

If S30's follow-up is still incomplete, its results cannot be finalized as none and zero. This code assumes a completed fictional roster; real incomplete data needs completion status and separate `pending` handling. Do not mix these future outcomes into prediction inputs at the sample time. Decide whether a result column is a [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) only after defining the prediction time and target.


## Combining Follow-Up Events into Sample-Level Outcomes {#a-small-diagram}

This section compresses one point: `several follow-up events` do not automatically become one result column. The same event list turns into different representative result columns depending on whether it is folded by `any`, `first`, `worst`, or `count`.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-en.mmd"
```

## Checklist

- Can you explain why lowering 4 to 3 for S02 changes selection rather than creating a failure?

- Did you specify the observation period, deduplication, and representative-label selection rules for follow-up events?
- Did you distinguish zero follow-up events from incomplete observation?

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary#label){: target="_blank" rel="noopener noreferrer" }. Used for the definitions of label and labeled example. The any/first/worst/count rules, severity rankings, and failure-type mapping are designed for this example. / 2026-09-19
- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. Provides the general basis for tracking data generation and derivation; it does not prescribe the aggregation rules in this section. / 2026-09-19
