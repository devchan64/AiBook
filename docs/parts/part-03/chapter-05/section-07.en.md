# P3-5.7 How Should We Fold Multiple Follow-Up Events After the Same Sample into a Table Structure

> Section ID: `P3-5.7`
> Version: `v2026.07.20`

Even after the sample unit and the input window are fixed, one more point often blocks the table structure. It is the case where several follow-up events attach after the same sample. For example, after one action, we may record `review`, `warning`, `failure`, and `revisit` in sequence. If we do not decide how to fold them into one result column, the same sample can easily change meaning from table to table.

If there are several follow-up events, we should first write down by what rule they were folded into one table structure.

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

So even when we are looking at the same source event, the table structure changes according to `what we choose as the representative result`. This is a data-modeling problem in which we must first decide by what rule the representative result will be folded and left in the table.

Leaving the notes below first reduces later confusion.

| Note to write down first | Why it is needed |
| --- | --- |
| Which follow-up events are treated as one bundle | To fix the result range handled by the table |
| Which of `any`, `first`, `worst`, `count` was used | To explain again what the result column means |
| Whether the folded result is for reporting or a prediction candidate | To avoid mixing comparison reports with target candidates |

Small example:

Problem situation: check that when several follow-up events exist after the same sample, different folding rules such as `first`, `worst`, `count`, and `any` create different result columns.

Input: the sample roster [p3_5_7_sample_roster.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_sample_roster.csv), the follow-up event log [p3_5_7_follow_up_events.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv), the event severity table [p3_5_7_event_severity.csv](/AiBook/assets/part-03/chapter-05/p3_5_7_event_severity.csv), and candidate severity thresholds for failure, `failure_severity_cutoffs`

The first CSV has one row for each sample that must remain in the final result table. The second CSV has one row for each follow-up event that actually occurred after a sample. The third CSV turns event names into severity numbers so that the `worst` and `any_failure` rules can be calculated.

Expected output: output showing that even for the same source event, `first_event`, `worst_event`, `event_count`, `event_sequence`, and `any_failure` are created differently. If `failure_severity_cutoffs` changes, the number and list of failure-candidate samples also change.

Concept to check: when folding several follow-up events into one result column, we should first specify by what rule they were folded, so the meaning of the table structure does not drift

```python
# This example folds multiple follow-up events after the same sample into a table structure and chooses a representative label.
import csv
from collections import defaultdict
from pathlib import Path

sample_roster_path = Path("docs/assets/part-03/chapter-05/p3_5_7_sample_roster.csv")
follow_up_events_path = Path("docs/assets/part-03/chapter-05/p3_5_7_follow_up_events.csv")
event_severity_path = Path("docs/assets/part-03/chapter-05/p3_5_7_event_severity.csv")

selected_failure_severity_cutoff = 4
failure_severity_cutoffs = [4, 3, 2]
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

ordered_events = sorted(follow_ups, key=lambda row: (row["sample_id"], row["days_after_sample"]))
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
            "any_failure": int(worst_severity >= selected_failure_severity_cutoff),
        }
    )

cutoff_results = []
for cutoff in failure_severity_cutoffs:
    failed = [row for row in folded if row["worst_severity"] >= cutoff]
    cutoff_results.append(
        {
            "failure_severity_cutoff": cutoff,
            "failure_sample_count": len(failed),
            "failure_samples": ",".join(row["sample_id"] for row in failed) or "none",
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
print("3) folded result when failure_severity_cutoff = 4")
print(
    "sample_id      first_event      worst_event  worst_severity  event_count"
    "             event_sequence  any_failure"
)
for row in folded[:preview_row_count]:
    print(
        f"{row['sample_id']:>9} {row['first_event']:>16} {row['worst_event']:>16} "
        f"{row['worst_severity']:>15} {row['event_count']:>12} "
        f"{row['event_sequence']:>26} {row['any_failure']:>12}"
    )
print(f"... {len(folded) - preview_row_count} more folded samples")
print()
print("4) sensitivity by failure_severity_cutoff")
print(
    " failure_severity_cutoff  failure_sample_count"
    "                                                                     failure_samples"
)
for row in cutoff_results:
    print(
        f"{row['failure_severity_cutoff']:>24} {row['failure_sample_count']:>21} "
        f"{row['failure_samples']:>83}"
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

3) folded result when failure_severity_cutoff = 4
sample_id      first_event      worst_event  worst_severity  event_count             event_sequence  any_failure
      S01           review          failure               4            3 review > warning > failure            1
      S02           review          warning               3            2           review > warning            0
      S03          revisit          revisit               1            1                    revisit            0
      S04          warning          warning               3            1                    warning            0
      S05          revisit           review               2            2           revisit > review            0
      S06 minor_adjustment minor_adjustment               1            1           minor_adjustment            0
      S07          warning          failure               4            2          warning > failure            1
      S08           review           review               2            1                     review            0
      S09          revisit          revisit               1            1                    revisit            0
      S10          warning          warning               3            1                    warning            0
      S11       inspection       inspection               2            1                 inspection            0
      S12           review          warning               3            2           review > warning            0
... 24 more folded samples

4) sensitivity by failure_severity_cutoff
 failure_severity_cutoff  failure_sample_count                                                                     failure_samples
                       4                     5                                                                 S01,S07,S13,S19,S25
                       3                    12                                     S01,S02,S04,S07,S10,S12,S13,S16,S19,S22,S25,S28
                       2                    21 S01,S02,S04,S05,S07,S08,S10,S11,S12,S13,S16,S17,S18,S19,S21,S22,S24,S25,S26,S28,S29
```

The key point in this example is that even while looking at the same source event, `first_event`, `worst_event`, `event_count`, `event_sequence`, and `any_failure` can become different result columns. For S01, the first follow-up event is `review`, but the most severe event is `failure`. For S02, the first event is `review`, but the most severe event is `warning`. Samples like S30 have no follow-up events, but they still exist in the sample roster, so they are folded as `none` and 0 and remain in the final table. The values to manipulate here are `selected_failure_severity_cutoff` and `failure_severity_cutoffs`. With the threshold at 4, only S01, S07, S13, S19, and S25, which have `failure`, become failure candidates. If the threshold is lowered to 3, samples whose worst event is `warning` also enter the failure-candidate set. If it is lowered to 2, samples whose worst event is `review` or `inspection` are included too. In other words, unless the folding rule and threshold are written down, the same follow-up event log can be read with different meanings from table to table.

## A Small Diagram

This section compresses one point: `several follow-up events` do not automatically become one result column. The same event list turns into different representative result columns depending on whether it is folded by `any`, `first`, `worst`, or `count`.

--8<-- "assets/part-03/chapter-05/p3-5-7-mermaid-01-en.mmd"

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label` and `labeled example`. Because result information first has to be fixed to a given example, it supports the judgment in this section that when several follow-up events are folded into one result column, we should first specify which rule among `any`, `first`, `worst`, and `count` was used. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it shows that result columns with unclear construction rules are easy to confuse with prediction candidates, it reinforces the explanation that the folding rule should be written first to fix the meaning of the table structure. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it explains that a provenance framework should leave derivation and activity context traceable, it provides the higher-level frame that we should also be able to trace by what rule several follow-up events were folded into one representative result column. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
