# P3-2.3 What Should Be Written Down First When a New Table Arrives

> Section ID: `P3-2.3`
> Version: `v2026.07.20`

When a new table first arrives, it is easy in many cases to think first of averages, distributions, or model candidates. But what should be written down before that is `what does one row of this table mean?`, `what can be grouped together?`, and `what is still missing?` Only after these three are organized can we distinguish whether what is in hand is already a sample table that can be compared directly, or still raw records that must be regrouped. Rather than deciding immediately whether a new table is `a training dataset`, it helps interpretation more to write down these three points first. Once they are written down, later sample design and dataset redesign also become much less abstract.

The viewpoint that must be held first here is `format consistency` and `the first quality check`. Format consistency means checking first whether keys that refer to the same object are written in the same format, whether time columns are in a form that really allows order to be read, and whether values with the same meaning are mixed across columns with different units or string rules. The first quality check is the next stage after that. It means checking early whether there are problems that immediately break comparison structure, such as missing values, broken order, duplicate rows, or orphan rows that do not group cleanly.

When a new table is read for the first time, it is safer to write down first `what is one row?`, `what can be grouped?`, and `what is still missing?` The question `what is one row?` connects to checking the `observation` unit in statistics and data organization. `What can be grouped?` connects to the principle that in time data, `key` and `index` should be made visible first. The item about preserving `raw evidence` also connects to the principle that data provenance and traceability must remain available so that quality and reliability can be judged again later.

If the same five-line memo is reread from the perspectives of format and quality, it becomes the following.

| Check perspective | What to check first | Why it has to be caught early |
| --- | --- | --- |
| Format consistency | Are key formats consistent, are time columns sortable, and are units or notation rules unmixed? | Because if the same object is read as different ones or time order is misread, every later comparison will drift |
| First quality check | Are there missing values, duplicates, broken order, or rows that cannot be grouped? | Because cases that are already incomparable should be marked separately before sample reconstruction |

## The first five things to write down

When a new table is read for the first time, it is safer to write down the following five questions first. They are the minimum checks that keep us from missing `row unit`, `grouping criterion`, `time structure`, `comparability`, and `raw evidence`.

1. What does one row mean?
2. What identifier groups the same object together?
3. Is there a column that shows time order or process order?
4. Is the current unit directly comparable, or does it need to be regrouped?
5. If something looks strange, what is the raw evidence to return to?

Condensed into a table, those five become the following.

| Item to write down first | Why it is needed |
| --- | --- |
| Row meaning | Because we must distinguish whether it is a time-point record, one full action, or a recent-segment aggregate |
| Identifier | Because we need to know whether multiple lines belong to the same sample |
| Time/order column | Because we must decide whether it is a time-series structure or a static table |
| Comparability | Because we must decide whether samples can already be compared directly, or whether a summary table is needed first |
| Raw-evidence location | Because strange cases must remain traceable later |

Writing down only these five items already reduces how often storage structure and problem-representation structure are mixed together when read.

The order in which the five items are read also matters. `Row meaning`, `identifier`, and `time/order column` belong to the axis that checks format consistency first. `Comparability` and `raw-evidence location` belong to the axis that moves into the first quality check. Writing them down this way lets us separate, in order, whether `the format is wrong first` or `the format is fine but quality problems still break comparison`, instead of vaguely saying that `the quality looks bad`.

## A wrong start and a better start

| What is easy to do as soon as the table is seen | Why it is too early | A better first action |
| --- | --- | --- |
| Compute averages and maxima first | One row and one sample unit may still differ | Write down the row meaning and identifier first |
| Think of classification or regression | The unit that would receive the label may not yet be visible | Check first whether the unit is directly comparable |
| Think of time-series deep learning | Even if a time column exists, the sample boundary may still be unfixed | Check the time/order column and grouping criterion first |
| Attach meaning immediately to one strange value | That one line may not represent the whole sample | Write down the raw evidence and candidate summary structure together |

So the first stage is closer to `identity checking` than to `calculation`.

## A Small Diagram

When a new table is read for the first time, it is safer to close it in the order `row meaning -> grouping criterion -> format/quality checks -> regrouping decision`.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-en.mmd"
```

## A very short table-reading memo

If the following five lines are written down first, the table's identity and comparability can be separated quickly.

- One row means `_____`.
- The key that groups the same object is `_____`.
- The column showing time or process order is `_____`.
- This table is directly comparable / still needs to be regrouped.
- The raw evidence to revisit strange cases is `_____`.

For example, with an automatic-action log, it can be written like this.

- One row means `a measured value at one time point during the action`.
- The key that groups the same object is `event_id`.
- The time column is `elapsed_seconds`.
- This table is not yet a directly comparable sample table and still has to be regrouped.
- The raw evidence to revisit strange cases is the raw log by `event_id`.

Once this five-line memo exists, even the sentence `redesign the dataset to match the question` in Chapter 3 reads far less abstractly.

Going just one step further, format consistency and the first quality check can be written separately.

- Format consistency: first check whether `event_id` groups the same action in a consistent format, and whether `elapsed_seconds` allows time order to be read.
- First quality check: check whether some `event_id` values have abnormally few or many rows, whether time goes backward or has missing segments, and whether there are missing values that should be marked before comparison.

## Small Code Example

Problem situation: when a new log table arrives, check whether it can already be read directly as a sample-comparison table.

Input: the raw log table stored in [p3_2_3_first_table_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_3_first_table_log.csv), and `minimum_rows_per_event`, the minimum number of rows required to treat an event as a comparable candidate

Expected output: even for the same table, checking `row meaning`, `grouping criterion`, and `time/order column` first reveals that it is not yet a table that can be compared directly. Changing `minimum_rows_per_event` also changes which events have enough records to be considered candidates.

Concept to check: when reading a table for the first time, before calculation we must check whether `this row is one full sample` or `only part of a sample record`. Adding a repeated-row threshold turns structural checking into a judgment about comparability.

```python
# This example first checks column names and value distributions when a new CSV table arrives.
import csv
from collections import defaultdict
from pathlib import Path

minimum_rows_per_event = 12
preview_row_count = 8

input_path = Path("docs/assets/part-03/chapter-02/p3_2_3_first_table_log.csv")

with input_path.open(newline="", encoding="utf-8") as file:
    rows = list(csv.DictReader(file))

for row in rows:
    row["elapsed_seconds"] = int(row["elapsed_seconds"])
    row["flow"] = float(row["flow"])
    row["pressure"] = float(row["pressure"])

events = defaultdict(list)
for row in rows:
    events[row["event_id"]].append(row)

print("1) quick structural check")
print(f"row_count: {len(rows)}")
print(f"event_id_count: {len(events)}")
print("has_time_order: yes")
print()

print("2) repeated rows per event")
for event_id, event_rows in sorted(events.items()):
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(f"{event_id}: row_count={len(event_rows)}, enough_rows={enough_rows}")
print()

print("3) if we compare rows as if each row were a sample")
for row in rows[:preview_row_count]:
    print(
        f"{row['event_id']} at {row['elapsed_seconds']}s: "
        f"flow={row['flow']:.1f}"
    )
print(f"... {len(rows) - preview_row_count} more time-point rows")
print()

print("4) after regrouping into one row per event")
for event_id, event_rows in sorted(events.items()):
    duration = max(row["elapsed_seconds"] for row in event_rows)
    mean_flow = sum(row["flow"] for row in event_rows) / len(event_rows)
    peak_pressure = max(row["pressure"] for row in event_rows)
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(
        f"{event_id}: duration={duration}s, mean_flow={mean_flow:.2f}, "
        f"peak_pressure={peak_pressure:.1f}, enough_rows={enough_rows}"
    )
```

Expected output:

```text
1) quick structural check
row_count: 36
event_id_count: 3
has_time_order: yes

2) repeated rows per event
A: row_count=18, enough_rows=True
B: row_count=12, enough_rows=True
C: row_count=6, enough_rows=False

3) if we compare rows as if each row were a sample
A at 0s: flow=0.8
A at 1s: flow=0.9
A at 2s: flow=1.1
A at 3s: flow=1.2
A at 4s: flow=1.3
A at 5s: flow=1.4
A at 6s: flow=1.5
A at 7s: flow=1.6
... 28 more time-point rows

4) after regrouping into one row per event
A: duration=17s, mean_flow=1.25, peak_pressure=2.0, enough_rows=True
B: duration=11s, mean_flow=0.88, peak_pressure=1.5, enough_rows=True
C: duration=5s, mean_flow=0.98, peak_pressure=1.5, enough_rows=False
```

What this example shows is not simply that the columns are named `event_id` and `elapsed_seconds`. In steps 1 and 2, what must be seen first is that `the number of rows, 36` is larger than `the number of event_id values, 3`, and that the same `event_id` repeats across multiple lines. The value to manipulate here is `minimum_rows_per_event`. If it is set to `12`, A and B become candidates with enough records, but C remains a candidate with too few records. If it is lowered to `6`, C also becomes a candidate, but whether an average made from a shorter record should be compared with the same weight must be reviewed again. Only after reading this signal can we reach the interpretation that `the current row is not one full sample, but only part of a sample record`. So if we compare each row immediately as in step 3, we still do not have a table that compares `the full A action`, `the full B action`, and `the full C action`. By contrast, only after regrouping by `event_id` as in step 4 does one action become one row, and only then can comparable columns such as mean flow or peak pressure be created on top of it.

The same result becomes clearer when read again from the perspectives of format and quality. The repetition of `event_id` means, in terms of format consistency, that `a key exists that can group one sample`. The fact that `rows per event` differ means, in terms of the first quality check, that `the record length differs by sample`. This distinction has to be written down early so that when averages are compared later, we can also read `why some samples stand on less evidence than others`.

Format consistency and the first quality check are written down first so that, instead of attaching averages or model names the moment a new table arrives, we first see `what kind of row is in hand now` and `what is still blocking comparison`. Only when key format, time order, repetition length, missing values, and orphan rows are organized early can the same table be read later with stable criteria when regrouping samples and building comparable columns.

## Sources and Further Reading

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it distinguishes variables, observations, and table structure, it supports this section's starting point that `what one row means` should be written down first. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Earo Wang, Dianne Cook, Rob J. Hyndman, `A New Tidy Data Structure to Support Exploration and Modeling of Temporal Data`, *Journal of Computational and Graphical Statistics* 29(3), 2020. Because it provides the principle for reading temporal data by separating key and index, it strengthens the judgment that `what can be grouped` and `is there a time/order column` should be checked first. [https://robjhyndman.com/publications/tsibble/](https://robjhyndman.com/publications/tsibble/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance and traceability together, it supports the last check item in this section: when a strange case appears, the raw evidence to return to should have been written down early. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
