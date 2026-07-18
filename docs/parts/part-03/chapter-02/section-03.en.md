# P3-2.3 What Should Be Written Down First When a New Table Arrives

> Section ID: `P3-2.3`
> Version: `v2026.07.17`

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

Input: a raw log table in which multiple time-point records are mixed under each `event_id`

Expected output: even for the same table, checking `row meaning`, `grouping criterion`, and `time/order column` first reveals that it is not yet a table that can be compared directly

Concept to check: when reading a table for the first time, before calculation we must check whether `this row is one full sample` or `only part of a sample record`

```python
import pandas as pd

table = pd.DataFrame(
    [
        {"event_id": "A", "elapsed_seconds": 0, "flow": 0.8, "pressure": 1.0},
        {"event_id": "A", "elapsed_seconds": 1, "flow": 1.5, "pressure": 2.0},
        {"event_id": "A", "elapsed_seconds": 2, "flow": 0.9, "pressure": 1.4},
        {"event_id": "B", "elapsed_seconds": 0, "flow": 0.7, "pressure": 1.1},
        {"event_id": "B", "elapsed_seconds": 1, "flow": 0.8, "pressure": 1.2},
    ]
)

print("1) raw table")
print(table)
print()

row_check = pd.DataFrame(
    [
        {"check_item": "row_count", "value": len(table)},
        {"check_item": "event_id_count", "value": table["event_id"].nunique()},
        {"check_item": "has_time_order", "value": "yes"},
    ]
)
print("2) quick structural check")
print(row_check)
print()

rows_per_event = table.groupby("event_id", as_index=False).size().rename(columns={"size": "row_count"})
print("3) repeated rows per event")
print(rows_per_event)
print()

wrong_reading = table[["event_id", "elapsed_seconds", "flow"]]
print("4) if we compare rows as if each row were a sample")
print(wrong_reading)
print()

event_summary = (
    table.groupby("event_id", as_index=False)
    .agg(
        duration_seconds=("elapsed_seconds", "max"),
        mean_flow=("flow", "mean"),
        peak_pressure=("pressure", "max"),
    )
)
print("5) after regrouping into one row per event")
print(event_summary)
```

Expected output:

```text
1) raw table
  event_id  elapsed_seconds  flow  pressure
0        A                0   0.8       1.0
1        A                1   1.5       2.0
2        A                2   0.9       1.4
3        B                0   0.7       1.1
4        B                1   0.8       1.2

2) quick structural check
      check_item  value
0      row_count      5
1  event_id_count      2
2  has_time_order    yes

3) repeated rows per event
  event_id  row_count
0        A          3
1        B          2

4) if we compare rows as if each row were a sample
  event_id  elapsed_seconds  flow
0        A                0   0.8
1        A                1   1.5
2        A                2   0.9
3        B                0   0.7
4        B                1   0.8

5) after regrouping into one row per event
  event_id  duration_seconds  mean_flow  peak_pressure
0        A                 2   1.066667            2.0
1        B                 1   0.750000            1.2
```

What this example shows is not simply that the columns are named `event_id` and `elapsed_seconds`. In steps 2 and 3, what must be seen first is that `the number of rows, 5` is larger than `the number of event_id values, 2`, and that the same `event_id` repeats across multiple lines. Only after reading that signal can we reach the interpretation that `the current row is not one full sample, but only part of a sample record`. So if we compare each row immediately as in step 4, we still do not have a table that compares `the full A action` and `the full B action`. By contrast, only after regrouping by `event_id` as in step 5 does one action become one row, and only then can comparable columns such as mean flow or peak pressure be created on top of it.

The same result becomes clearer when read again from the perspectives of format and quality. The repetition of `event_id` means, in terms of format consistency, that `a key exists that can group one sample`. The fact that `rows per event` differ means, in terms of the first quality check, that `the record length differs by sample`. This distinction has to be written down early so that when averages are compared later, we can also read `why some samples stand on less evidence than others`.

Format consistency and the first quality check are written down first so that, instead of attaching averages or model names the moment a new table arrives, we first see `what kind of row is in hand now` and `what is still blocking comparison`. Only when key format, time order, repetition length, missing values, and orphan rows are organized early can the same table be read later with stable criteria when regrouping samples and building comparable columns.

## Sources and Further Reading

- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it distinguishes variables, observations, and table structure, it supports this section's starting point that `what one row means` should be written down first. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- E. Wang, D. L. Cook, R. J. Hyndman, and R. Wickham, `A Grammar of Spatiotemporal Data Transformation`, *Journal of Computational and Graphical Statistics* 27(2), 2018. Because it provides the principle for reading time data by separating key and index, it strengthens the judgment that `what can be grouped` and `is there a time/order column` should be checked first. [https://doi.org/10.1080/10618600.2017.1371377](https://doi.org/10.1080/10618600.2017.1371377){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it treats provenance and traceability together, it supports the last check item in this section: when a strange case appears, the raw evidence to return to should have been written down early. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
