# P3-2.3 What Should Be Written Down First When a New Table Arrives

> Section ID: `P3-2.3`
> Version: `v2026.09.19`

When a new table first arrives, it is easy in many cases to think first of averages, distributions, or model candidates. But what should be written down before that is `what does one row of this table mean?`, `what can be grouped together?`, and `what is still missing?` Only after these three are organized can we distinguish whether what is in hand is already a sample table that can be compared directly, or still raw records that must be regrouped. Rather than deciding immediately whether a new table is `a training dataset`, it helps interpretation more to write down these three points first. Once they are written down, later sample design and dataset redesign also become much less abstract.

The viewpoint that must be held first here is [format consistency](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) and the first [data quality check](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling). Format consistency means checking first whether keys that refer to the same object are written in the same format, whether time columns are in a form that really allows order to be read, and whether values with the same meaning are mixed across columns with different units or string rules. The first quality check is the next stage after that. It means checking early whether there are problems that immediately break comparison structure, such as missing values, broken order, duplicate rows, or orphan rows that do not group cleanly.

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
| [Comparability](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparability) | Because we must decide whether samples can already be compared directly, or whether a summary table is needed first |
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

## Checking Row Meaning and Comparability {#a-small-diagram}

When a new table is read for the first time, it is safer to close it in the order `row meaning -> grouping criterion -> format/quality checks -> decide on restructuring or source checks`.

```mermaid
--8<-- "assets/part-03/chapter-02/p3-2-3-mermaid-01-en.mmd"
```

## A very short table-reading memo

If the following five lines are written down first, the table's identity and comparability can be separated quickly.

- One row means `_____`.
- The key that groups the same object is `_____`.
- The column showing time or process order is `_____`.
- The comparison question is `_____`; the required restructuring and conditions still to verify are `_____`.
- The raw evidence to revisit strange cases is `_____`.

For example, to compare mean flow across actions using the CSV below, write:

- One row means `a measured value at one time point during the action`.
- The key that groups the same object is `event_id`.
- The time column is `elapsed_seconds`.
- Comparing action-level means requires grouping by `event_id`; full action coverage and matching operating conditions remain unverified.
- The raw evidence to revisit strange cases is the raw log by `event_id`.

Once this five-line memo exists, even the sentence `redesign the dataset to match the question` in Chapter 3 reads far less abstractly.

Going just one step further, format consistency and the first quality check can be written separately.

- Format consistency: first check whether `event_id` groups the same action in a consistent format, and whether `elapsed_seconds` allows time order to be read.
- First quality check: check whether some `event_id` values have abnormally few or many rows, whether time goes backward or has missing segments, and whether there are missing values that should be marked before comparison.

## Order Errors and Cases That Need Source Checks

The contrasts below copy and modify A’s first three records from the CSV used later. The original `(time, flow)` pairs are `(0, 0.80), (1, 0.92), (2, 1.05)`, in seconds and L/min. We assume a 1-second sampling interval for this small segment. The original CSV stays unchanged.

| Change to the copy | What changed | Next action |
| --- | --- | --- |
| None: 0→1→2 seconds | Order and spacing match this segment’s assumptions | Continue checking other quality items |
| Reverse only the rows to 2→1→0 seconds | Timestamps and measurements stay the same; storage order changes | Check timestamp meaning, then sort a copy |
| Append an identical 1-second record | The same event, time, and measurements repeat | Check the source for repeated collection before deciding how to handle it |
| Append a 1-second row with flow changed to 9.00 | Values 0.92 and 9.00 conflict at the same event and time | Hold the event summary and check the source |
| Remove the 1-second record: 0→2 seconds | Time increases but leaves a gap in the expected spacing | Check the source for missing records; do not fill with zero arbitrarily |

Repeated `event_id` values are needed to group an event’s time-point records. The suspected duplicate here is a repeated `(event_id, elapsed_seconds)` pair. If a real log contains multiple sensors, first check whether sensor identity must also be part of that key. Sorting changes order; it neither selects the correct conflicting value nor recovers a missing measurement.

Record the file path, version or collection time, original row number, and event identifier in the source note. In the derived table’s processing history, record which rows were sorted, excluded, or held, and why. For A’s conflicting 1-second values, for example, inspect CSV data row 2 (file line 3 including the header) alongside the added conflicting row. Keep the original so that the records before and after processing can be compared.

## Checking Row Counts, Time Order, and Duplicates Separately {#small-code-example}

Problem situation: when a new log table arrives, check whether it can already be read directly as a sample-comparison table.

Input: the raw log table stored in [p3_2_3_first_table_log.csv](/AiBook/assets/part-03/chapter-02/p3_2_3_first_table_log.csv), and `minimum_rows_per_event`, the minimum row count used as an observation-count condition

Expected output: check which events pass the row-count condition, then distinguish sorting from checking the source when order, duplication, values, or missing records change in the same three-record segment.

Concept to check: one row may not be one event. Passing a row-count condition does not certify complete event coverage or comparability; even correctly ordered records need separate checks for duplicates, gaps, and differences in conditions.

```python
# Check row counts and time order, then compare next actions for duplicates, conflicts, and gaps in copies.
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
has_time_order = all(
    all(a["elapsed_seconds"] < b["elapsed_seconds"]
        for a, b in zip(event_rows, event_rows[1:]))
    for event_rows in events.values()
)
print(f"has_time_order: {'yes' if has_time_order else 'no'}")
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
    times = [row["elapsed_seconds"] for row in event_rows]
    observed_span = max(times) - min(times)
    mean_flow = sum(row["flow"] for row in event_rows) / len(event_rows)
    peak_pressure = max(row["pressure"] for row in event_rows)
    enough_rows = len(event_rows) >= minimum_rows_per_event
    print(
        f"{event_id}: observed_span={observed_span}s, mean_flow={mean_flow:.2f}, "
        f"peak_pressure={peak_pressure:.1f}, enough_rows={enough_rows}"
    )

print()
print("5) controlled changes to A's first three records")
base_records = [dict(row) for row in events["A"][:3]]
cases = {
    "original": base_records,
    "reversed": list(reversed(base_records)),
    "duplicate": base_records + [dict(base_records[1])],
    "conflict": base_records + [dict(base_records[1], flow=9.0)],
    "missing": [base_records[0], base_records[2]],
}
for name, records in cases.items():
    times = [row["elapsed_seconds"] for row in records]
    ordered = all(a < b for a, b in zip(times, times[1:]))
    same_time = defaultdict(set)
    for row in records:
        same_time[row["elapsed_seconds"]].add((row["flow"], row["pressure"]))
    duplicate_time = len(times) != len(same_time)
    conflicting_values = any(len(values) > 1 for values in same_time.values())
    unique_times = sorted(same_time)
    gap = any(b - a != 1 for a, b in zip(unique_times, unique_times[1:]))
    if conflicting_values or duplicate_time or gap:
        next_action = "check_source"
    elif not ordered:
        next_action = "sort_copy"
    else:
        next_action = "continue_checks"
    print(
        f"{name}: ordered={ordered}, duplicate_time={duplicate_time}, "
        f"conflict={conflicting_values}, gap={gap}, next={next_action}"
    )
```

Expected output: check which events pass the row-count condition, then distinguish sorting from checking the source when order, duplication, values, or missing records change in the same three-record segment.

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
A: observed_span=17s, mean_flow=1.25, peak_pressure=2.0, enough_rows=True
B: observed_span=11s, mean_flow=0.88, peak_pressure=1.5, enough_rows=True
C: observed_span=5s, mean_flow=0.98, peak_pressure=1.5, enough_rows=False

5) controlled changes to A's first three records
original: ordered=True, duplicate_time=False, conflict=False, gap=False, next=continue_checks
reversed: ordered=False, duplicate_time=False, conflict=False, gap=False, next=sort_copy
duplicate: ordered=False, duplicate_time=True, conflict=False, gap=False, next=check_source
conflict: ordered=False, duplicate_time=True, conflict=True, gap=False, next=check_source
missing: ordered=True, duplicate_time=False, conflict=False, gap=True, next=check_source
```

In steps 1 and 2, `has_time_order` checks only whether **the order read from the file strictly increases within each event**. Repeated timestamps and reversed order both yield `no`, but their causes differ. Missing an intermediate record, as in 0→2 seconds, still passes this increasing-order check.

With `minimum_rows_per_event` at 12, A and B pass the row-count condition; lowering it to 6 lets A, B, and C pass. `enough_rows=True` reports only that condition. Duplicate rows also count, so it does not establish enough unique observations or coverage of the full action. Start and end records, sampling intervals, and operating conditions need separate checks.

In step 4, `observed_span` is the last observed time minus the first observed time. A’s `17s` means that observations span 0–17 seconds, not that the action ended after 17 seconds. Mean flow and peak pressure summarize available records; they do not certify immediate comparability.

Step 5 experiments on copies of only A’s first three records. `reversed` changes only order, so the result is `sort_copy`; duplicates, conflicts, and missing-record cases yield `check_source`. Hold the summary for a conflicting case until its source is checked. `gap` checks this experiment’s 1-second interval assumption, not missing records before or after the segment or missing cell values. `continue_checks` does not mean every quality check has passed.

Try changing the added flow in `conflict` from 9.0 to its original value, 0.92. Although `conflict` becomes False, `duplicate_time` stays True, so checking the source is still necessary. Then restore the 1-second record in `missing`: `gap` becomes False. Even when cases share an order-warning signal, write down their different causes and next actions.

## Checklist

- Did you write five lines identifying row meaning, identifiers, time columns, comparison conditions, and original evidence?
- Can you distinguish repeated event identifiers from duplicate event-and-time pairs?
- Can you explain when reversed order, conflicting values, or missing records call for sorting, holding a summary, or checking the source?
- Do you distinguish passing a row-count condition and measuring an observed span from evidence of full event coverage?
- Did you record the original file and row location and preserve the derived table’s processing history?

## Sources and Further Reading

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it distinguishes variables, observations, and table structure, it supports this section's starting point that `what one row means` should be written down first. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Earo Wang, Dianne Cook, Rob J. Hyndman, `A New Tidy Data Structure to Support Exploration and Modeling of Temporal Data`, *Journal of Computational and Graphical Statistics* 29(3), 2020. Because it provides the principle for reading temporal data by separating key and index, it strengthens the judgment that `what can be grouped` and `is there a time/order column` should be checked first. [https://robjhyndman.com/publications/tsibble/](https://robjhyndman.com/publications/tsibble/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it treats provenance and traceability together, it supports the last check item in this section: when a strange case appears, the raw evidence to return to should have been written down early. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
