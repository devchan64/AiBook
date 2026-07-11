# P3-5.1 How Do We Turn Raw Logs into Comparable Tables

> Section ID: `P3-5.1`
> Version: `v2026.07.11`

At first glance, raw logs look very rich. They contain many values in time order, often from several sensors, sometimes together with control parameters. But that richness does not automatically mean we already have a comparable dataset. After the [sample](../../../reference/concept-glossary.md#glossary-sample) unit has been fixed, we still need a procedure that turns raw logs into a summary table and an aggregate table. Raw logs, summary tables, and aggregate tables play different roles, and one row means something different in each of them.

`raw log -> summary table -> aggregate table` is the order in which the same time series is rewritten into tables that answer different questions. Once that order is visible, it also becomes clearer at what level [baseline](../../../reference/concept-glossary.md#glossary-baseline) comparison and [intermediate representation](../../../reference/concept-glossary.md#glossary-intermediate-representation) design attach.

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

The next example shows how a raw log leads first to an action-level summary table and then all the way to a recent/baseline aggregate table. Here we assume that the action is divided into three progress segments to build segment averages.

Problem situation: check in one view how a raw log becomes an `action-level summary table` and then a `recent/baseline aggregate table`.

Input: a raw log table made of `event_id`, `progress_bin`, and `flow`

Expected output: an output in which the three tables `raw`, `summary`, and `aggregate` have different row meanings and different comparison roles

Concept to check: turning raw logs into comparable tables means rewriting the same records step by step into a summary table and an aggregate table

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "progress_bin": "early", "flow": 0.8},
        {"event_id": "A", "progress_bin": "early", "flow": 1.0},
        {"event_id": "A", "progress_bin": "mid", "flow": 2.4},
        {"event_id": "A", "progress_bin": "mid", "flow": 2.5},
        {"event_id": "A", "progress_bin": "late", "flow": 1.9},
        {"event_id": "A", "progress_bin": "late", "flow": 1.6},
        {"event_id": "B", "progress_bin": "early", "flow": 0.7},
        {"event_id": "B", "progress_bin": "early", "flow": 0.9},
        {"event_id": "B", "progress_bin": "mid", "flow": 2.1},
        {"event_id": "B", "progress_bin": "mid", "flow": 2.0},
        {"event_id": "B", "progress_bin": "late", "flow": 1.8},
        {"event_id": "B", "progress_bin": "late", "flow": 1.7},
        {"event_id": "C", "progress_bin": "early", "flow": 0.9},
        {"event_id": "C", "progress_bin": "early", "flow": 1.1},
        {"event_id": "C", "progress_bin": "mid", "flow": 2.6},
        {"event_id": "C", "progress_bin": "mid", "flow": 2.7},
        {"event_id": "C", "progress_bin": "late", "flow": 2.0},
        {"event_id": "C", "progress_bin": "late", "flow": 1.8},
    ]
)

summary = (
    raw.pivot_table(
        index="event_id",
        columns="progress_bin",
        values="flow",
        aggfunc="mean",
    )
    .rename(
        columns={
            "early": "early_flow_mean",
            "mid": "mid_flow_mean",
            "late": "late_flow_mean",
        }
    )
    .reset_index()
    .assign(window=lambda df: df["event_id"].map({"A": "recent", "B": "baseline", "C": "recent"}))
)

aggregate = (
    summary.groupby("window", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        early_flow_mean=("early_flow_mean", "mean"),
        mid_flow_mean=("mid_flow_mean", "mean"),
        late_flow_mean=("late_flow_mean", "mean"),
    )
)

print("1) raw log rows before comparison")
print(raw.head(6))
print()
print("2) per-event summary table for direct comparison")
print(summary)
print()
print("3) recent-vs-baseline aggregate table built from event summaries")
print(aggregate)
```

Expected output:

```text
1) raw log rows before comparison
  event_id progress_bin  flow
0        A        early   0.8
1        A        early   1.0
2        A          mid   2.4
3        A          mid   2.5
4        A         late   1.9
5        A         late   1.6

2) per-event summary table for direct comparison
  event_id  early_flow_mean  late_flow_mean  mid_flow_mean    window
0        A              0.9            1.75           2.45    recent
1        B              0.8            1.75           2.05  baseline
2        C              1.0            1.90           2.65    recent

3) recent-vs-baseline aggregate table built from event summaries
     window  event_count  early_flow_mean  mid_flow_mean  late_flow_mean
0  baseline            1             0.80           2.05           1.750
1    recent            2             0.95           2.55           1.825
```

In this output, the raw log is a record of time points. Only at stage 2 does one full action become one row. At stage 3, several such samples are grouped again into recent/baseline aggregates. What matters is not only that the number of rows decreased, but that comparison units such as `early`, `mid`, and `late` entered the column structure of the summary table, and that this summary table then became the material for a recent-state comparison table.

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

- W3C, `PROV-Overview`. Because the provenance framework explains that processing steps, derivation, and versioning should be representable, it provides a general basis for keeping separate records of how raw logs were transformed into summary tables and aggregate tables. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example assumes a sample-level structure where features and labels attach, it reinforces the need to distinguish raw rows from event-summary rows and build a sample-level table. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains a reference period as the basis for comparing other periods, it offers a general basis for needing a separate representation level such as an aggregate table when comparing recent state against baseline state. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
