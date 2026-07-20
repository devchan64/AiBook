# P3-5.1 How Do We Turn Raw Logs into Comparable Tables

> Section ID: `P3-5.1`
> Version: `v2026.07.20`

At first glance, raw logs look very rich. They contain many values in time order, often from several sensors, sometimes together with control parameters. But that richness does not automatically mean we already have a comparable dataset. After the [sample](/AiBook/reference/concept-glossary/#glossary-sample) unit has been fixed, we still need a procedure that turns raw logs into a summary table and an aggregate table. Raw logs, summary tables, and aggregate tables play different roles, and one row means something different in each of them.

`raw log -> summary table -> aggregate table` is the order in which the same time series is rewritten into tables that answer different questions. Once that order is visible, it also becomes clearer at what level [baseline](/AiBook/reference/concept-glossary/#glossary-baseline) comparison and [intermediate representation](/AiBook/reference/concept-glossary/#glossary-intermediate-representation) design attach.

Take an automatically executed action as an example. In the raw log, one row is left behind at every time point during the action, with sensor values and control values. In the summary table, one full automatically executed action becomes one row. In the aggregate table, one row can instead mean the result of grouping several actions again, such as the average of the most recent 20 cases or the average of a usual operating range.

| Type of table | What one row means | The question it mainly answers |
| --- | --- | --- |
| Raw log | One time-point record during an action | What was measured right now? |
| Summary table | A sample summarizing one full action | What structure did this action have? |
| Aggregate table | A recent or baseline summary built from many actions | Is the recent change different from the usual state? |

This is not just a matter of different table names. A raw log is strong at preserving fine detail, but it is hard to compare whole actions there. A summary table makes comparison across actions easier, but most moment-to-moment fluctuations are compressed away. An aggregate table lets us read recent state quickly, but the special shape of an individual action can disappear.

So in this section, table conversion is closer to `turning the data into a structure where numeric values and categorical states can be explored together` than to merely `making a table`. Numerical exploration can begin only when the summary table lets us compare level, change, and variability. Categorical exploration can begin only when status ranges, missingness, overlap, and reasons why comparison is impossible are also organized together.

| Exploration angle | What should be left in the table first | What later sections read more deeply |
| --- | --- | --- |
| Numerical exploration | Range averages, rates of change, variability | Patterns beyond the average, recent-vs-baseline differences |
| Categorical exploration | State labels, missingness flags, overlap / non-comparable flags | Sample-collapse distinctions, judgments about comparability |

That is why it is misleading to read `summary` as simple shrinking. One action-summary row is the result of turning many raw time-series rows into one row that people can compare and models can handle more easily. The important point is not redefining the sample unit again, but building a comparable table on top of the sample unit that has already been fixed. It makes comparison easier, but it does not replace every context in the raw time series.

So when reading a table, the first question should not be `what are the columns?` but `what is one row?` One row in a raw log is usually not yet one full sample. Only when it becomes one row in the summary table can one action finally be read as a comparable sample. The aggregate table goes one step further and builds a comparison structure by grouping several samples again.

Moving from the raw log to the summary table is not only about reducing the number of rows. At this stage, we also have to decide `which ranges will be separated`, `what rates of change will be computed`, and `which sensor values will remain as representative values`. For example, a one-action summary table may include columns such as total action time, average pressure in the early phase, average flow in the middle phase, decline rate in the late phase, and control-tracking error. These are not values that originally appeared as one line in the raw log. They are the result of rewriting many time-point values into a form that is easier for people to compare.

The diagram below compresses this transformation into its shortest form.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-1-mermaid-01-en.mmd"
```

In this flow, the `Segment by progress` stage is especially important. We do not simply average the raw log as-is. First we divide the action into comparable ranges such as early, middle, and late, and only then do summary values appear. `Aggregate across events` comes after that. Summarizing one action and aggregating a recent operating range are not the same job. The second one groups once more.

At this point, the first thing to check is `which of the three tables is the starting point for my current work`, because that keeps different tables from being mixed together.

| The table currently in hand | What should be done first | What is still hard with only this table |
| --- | --- | --- |
| Raw log | Decide action boundaries and segment criteria | Direct comparison across actions |
| Summary table | Compare one action against another | Read repeated recent changes |
| Aggregate table | Compare recent state against the baseline | Inspect the detailed shape of one action |

The aggregate table changes role one more time. Here the focus is not the shape of one action, but grouped flows such as `average of the most recent 20 cases`, `variability of the most recent 20 cases`, `difference from the baseline`, or `the number of repeated changes in the same direction`. If the summary table is closer to `reading cases`, the aggregate table is closer to `reading state`.

The next example shows how a raw log leads first to an action-level summary table and then all the way to a recent/baseline aggregate table. Here we assume that the action is divided into three progress segments, and that 3 `baseline` events and 3 `recent` events are compared.

Problem situation: check in one view how a raw log becomes an `action-level summary table` and then a `recent/baseline aggregate table`.

Input: the [`p3_5_1_raw_log_segments.csv`](/AiBook/assets/part-03/chapter-05/p3_5_1_raw_log_segments.csv){: target="_blank" rel="noopener noreferrer" } file. One row is a `flow` record measured in one progress segment of one action, and `window` marks whether the event belongs to the baseline or recent range.

Expected output: an output in which the three tables `raw`, `summary`, and `aggregate` have different row meanings and different comparison roles

Concept to check: turning raw logs into comparable tables means rewriting the same records step by step into a summary table and an aggregate table

```python
# This example turns raw log rows into per-event summary and per-window aggregate tables.
import csv
from collections import defaultdict
from pathlib import Path

data_path = Path("docs/assets/part-03/chapter-05/p3_5_1_raw_log_segments.csv")

with data_path.open(newline="", encoding="utf-8") as file:
    raw = [
        {**row, "flow": float(row["flow"])}
        for row in csv.DictReader(file)
    ]

event_segments = defaultdict(lambda: {"window": None, "segments": defaultdict(list)})
for row in raw:
    event = event_segments[row["event_id"]]
    event["window"] = row["window"]
    event["segments"][row["progress_bin"]].append(row["flow"])

summary = []
for event_id in sorted(event_segments):
    event = event_segments[event_id]
    summary.append(
        {
            "event_id": event_id,
            "window": event["window"],
            "early_flow_mean": sum(event["segments"]["early"]) / len(event["segments"]["early"]),
            "mid_flow_mean": sum(event["segments"]["mid"]) / len(event["segments"]["mid"]),
            "late_flow_mean": sum(event["segments"]["late"]) / len(event["segments"]["late"]),
        }
    )

window_groups = defaultdict(list)
for row in summary:
    window_groups[row["window"]].append(row)

aggregate = []
for window in sorted(window_groups):
    rows = window_groups[window]
    aggregate.append(
        {
            "window": window,
            "event_count": len(rows),
            "early_flow_mean": sum(row["early_flow_mean"] for row in rows) / len(rows),
            "mid_flow_mean": sum(row["mid_flow_mean"] for row in rows) / len(rows),
            "late_flow_mean": sum(row["late_flow_mean"] for row in rows) / len(rows),
        }
    )

print("1) raw log rows before comparison")
for row in raw[:6]:
    print(
        f'{row["event_id"]} {row["window"]:<8} '
        f'{row["progress_bin"]:<5} flow={row["flow"]:.2f}'
    )
print(f"... {len(raw) - 6} more raw log rows")
print()
print("2) per-event summary table for direct comparison")
for row in summary:
    print(
        f'{row["event_id"]} {row["window"]:<8} '
        f'early={row["early_flow_mean"]:.2f} '
        f'mid={row["mid_flow_mean"]:.2f} '
        f'late={row["late_flow_mean"]:.2f}'
    )
print()
print("3) recent-vs-baseline aggregate table built from event summaries")
for row in aggregate:
    print(
        f'{row["window"]:<8} events={row["event_count"]} '
        f'early={row["early_flow_mean"]:.2f} '
        f'mid={row["mid_flow_mean"]:.2f} '
        f'late={row["late_flow_mean"]:.2f}'
    )
```

Expected output:

```text
1) raw log rows before comparison
A baseline early flow=0.70
A baseline early flow=0.90
A baseline mid   flow=2.00
A baseline mid   flow=2.10
A baseline late  flow=1.70
A baseline late  flow=1.80
... 30 more raw log rows

2) per-event summary table for direct comparison
A baseline early=0.80 mid=2.05 late=1.75
B baseline early=0.80 mid=2.15 late=1.65
C baseline early=0.80 mid=2.00 late=1.85
D recent   early=0.95 mid=2.45 late=1.85
E recent   early=1.05 mid=2.65 late=1.95
F recent   early=1.00 mid=2.55 late=1.75

3) recent-vs-baseline aggregate table built from event summaries
baseline events=3 early=0.80 mid=2.07 late=1.75
recent   events=3 early=1.00 mid=2.55 late=1.85
```

In this output, the raw log contains 36 time-point records. Only at stage 2 do the 6 full actions become one row each. At stage 3, those samples are grouped again into `baseline` and `recent` aggregates. What matters is not only that the number of rows decreased, but that comparison units such as `early`, `mid`, and `late` entered the column structure of the summary table, and that this summary table then became the material for a recent-state comparison table. If the values in the CSV are changed, both the per-event summaries and recent/baseline aggregates change, so the reader can check directly at which representation level the judgment changes.

After seeing this example, the following questions help check whether what just happened was simple shrinking or a change of representation.

1. Did we merely reduce the row count, or did we also redefine the sample-level representation?
2. Were `early`, `mid`, and `late` columns that already existed in the raw log, or were they new segments created for comparison?
3. If we want to make an average of the most recent 20 cases in the next step, which is the more direct starting point now: this table or the raw log?

If these questions can be answered, `raw log -> summary table -> aggregate table` becomes clearer as not a simple compression order but a series of representation shifts for different judgment questions.

The same flow can be judged more briefly like this.

| The judgment needed right now | The more direct starting point |
| --- | --- |
| Comparing the structure of individual actions | Summary table |
| Comparing recent state with usual state | Aggregate table |
| Checking the detailed time point of an unusual change | Raw log |

The importance of this table does not mean `once we make one good table, we are done`. It means that depending on the question, the table we have to move down to or up to changes.

Another important point is that the three tables are not in competition. Making a summary table does not make the raw log unnecessary. Making an aggregate table does not make the action-level table useless. On the contrary, if an unusual change appears in the aggregate table, we have to move back down to the summary table and the raw log to check it. The more comparison-oriented representations we add, the more important it becomes to re-check the raw time series too.

So `raw log -> summary table -> aggregate table` is not a simple order of shrinking. It is a continuous design that rewrites the same time series at the record level, the sample level, and the state level. The key point is not just that more tables appear one by one, but that for some questions raw records are the more direct evidence, for other questions sample summaries are, and for still other questions state aggregates are.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because the provenance framework explains that processing steps, reproducibility, versioning, and derivation should be representable, it provides a general basis for keeping separate records of how raw logs were transformed into summary tables and aggregate tables. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `example` and `labeled example`. Because an example assumes a sample-level structure where features and labels attach, it reinforces the need to distinguish raw rows from event-summary rows and build a sample-level table. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains a reference period as the basis for comparing other periods, it offers a general basis for needing a separate representation level such as an aggregate table when comparing recent state against baseline state. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
