# P3-4.3 How Are One Row, One Sample, and One Recent Segment Different

> Section ID: `P3-4.3`
> Version: `v2026.07.20`

`One row`, `one sample`, and `one recent segment` all come to mind while looking at a data table, but they are not the same level. In a source-data table, the row is seen first. In the comparison of one full action, the sample becomes central. In baseline comparison, the recent segment appears as yet another comparison unit.

The reason all three units must be separated at once is that features, baseline comparison, and review sentences attach at different levels. The moment a row is mistaken for a sample, or a segment is read as if it were one sample, the later table structure and comparison structure also begin to drift.

If we divide the three levels again, they become the following.

- `One row` is one visible line in the current table.
- `One sample` is the basic unit for comparison or learning.
- `One recent segment` is a comparison unit made by regrouping several samples.

These three can contain one another, but they do not mean the same thing.

| What we are looking at now | The most natural question | The level in this section |
| --- | --- | --- |
| one line of a time-point log | What was measured at this time point? | row |
| one full action | Did this action have a different structure from the usual one? | sample |
| a bundle of the most recent 20 cases | Has the recent state changed from the usual segment? | segment |

This table shows that `there is one line`, `there is one sample`, and `there is one recent segment to compare` each answer a different question. The reason Part 3 keeps becoming confusing is not that these three belong to the same level, but that all three questions begin while looking at data tables.

## Rereading One Scene at Three Levels

Let us look again at automatically executed action data.

| event_id | second | flow |
| --- | ---: | ---: |
| A | 0 | 0.8 |
| A | 1 | 1.5 |
| A | 2 | 1.1 |
| B | 0 | 0.7 |
| B | 1 | 1.2 |
| B | 2 | 1.0 |

At first glance, this table shows six lines. But those six lines may not yet be six samples. If one full action such as `A` is the sample here, then the three lines above are time-point records that together compose one sample.

Then, if several actions are grouped again to create `the mean of the most recent 20 cases`, individual samples such as `A` and `B` move one level downward again. That is because the recent segment is an aggregate unit made by regrouping several samples.

Placed at the three levels, the same scene can be read as follows.

| Level | What counts as one case | Example |
| --- | --- | --- |
| Row | one time-point record line | `A, second=1, flow=1.5` |
| Sample | one full action | the whole of `event_id=A` |
| Segment | a bundle of several samples | the mean and variability of the most recent 20 cases |

In other words, `A, second=1` may be not a sample, but one piece that composes a sample, while `the most recent 20 cases` may be a larger comparison unit made by regrouping 20 samples again.

The same scene becomes even clearer when rewritten as sentences.

- If the operator is asking `what was the flow at the 1-second time point?`, then what they want to see is the row.
- If the operator is asking `was action A more unstable than usual?`, then what they want to see is the sample.
- If the operator is asking `have the most recent 20 cases become worse than last week's baseline?`, then what they want to see is the segment.

The key point is that every time the question changes, the same source data is reread at a different level. Confusion usually arises not because the data is complex, but because we begin looking at the table without writing down which question we are attaching to it right now.

## Why This Distinction Is Needed

This distinction is needed because later concepts attach at different levels.

| Concept | The level where it mainly attaches | Why |
| --- | --- | --- |
| raw measurement value | row | because it is the actual observation value at one time point |
| feature | sample | because it is a value that describes the structure of one full action |
| baseline comparison | segment or sample-vs-segment | because the recent state has to be compared with the usual state |
| review sentence | segment or sample | because it is a judgment unit that a person reads |

For example, a feature such as `late_drop_rate` does not attach directly to one time-point row. It can only be calculated after one full action has been constructed as the sample. By contrast, a value such as `recent_count=20` is closer not to an individual-sample feature, but to a recent-segment aggregate. That is why, once these levels are mixed together, features, baselines, and output structure all begin to feel abstract.

## Small Code Example for Seeing the Comparison at a Glance

Problem situation: check, through row count and output structure, that `one row`, `one sample`, and `one recent segment` are different levels in the same source log.

Input: time-point flow records by `event_id`, plus a column indicating recent versus baseline segment

Expected output: `row count`, `sample count`, and `window count` differ, and the meaning of one case differs at each level

Concept to check: row, sample, and segment are different representation levels of the same data, and should not be read as the same unit

```python
# This example compares one row, one sample, and one recent segment as different analysis units.
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.8},
        {"event_id": "A", "second": 1, "flow": 1.5},
        {"event_id": "A", "second": 2, "flow": 1.1},
        {"event_id": "B", "second": 0, "flow": 0.7},
        {"event_id": "B", "second": 1, "flow": 1.2},
        {"event_id": "B", "second": 2, "flow": 1.0},
        {"event_id": "C", "second": 0, "flow": 0.9},
        {"event_id": "C", "second": 1, "flow": 1.6},
        {"event_id": "C", "second": 2, "flow": 1.2},
    ]
)

per_event = (
    raw.groupby("event_id", as_index=False)
    .agg(
        flow_mean=("flow", "mean"),
        flow_max=("flow", "max"),
    )
    .assign(window=lambda df: df["event_id"].map({"A": "recent", "B": "baseline", "C": "recent"}))
)

per_window = (
    per_event.groupby("window", as_index=False)
    .agg(
        event_count=("event_id", "count"),
        flow_mean=("flow_mean", "mean"),
    )
)

print("1) counts change by level")
print("row count:", len(raw))
print("sample count:", len(per_event))
print("window count:", len(per_window))
print()
print("2) one row still means one time-step record")
print(raw.loc[[1], ["event_id", "second", "flow"]])
print()
print("3) one sample means one whole event")
print(per_event.loc[per_event["event_id"] == "A", ["event_id", "flow_mean", "flow_max"]])
print()
print("4) one window means multiple samples regrouped")
print(per_window)
```

Expected output:

```text
1) counts change by level
row count: 9
sample count: 3
window count: 2

2) one row still means one time-step record
  event_id  second  flow
1        A       1   1.5

3) one sample means one whole event
  event_id  flow_mean  flow_max
0        A   1.133333       1.5

4) one window means multiple samples regrouped
     window  event_count  flow_mean
0  baseline            1   0.966667
1    recent            2   1.183333
```

What matters here is not the numbers themselves, but `what is being counted`.

- `row count: 9` means nine time-point records.
- `sample count: 3` means three actions.
- `window count: 2` means two segments, `recent` and `baseline`.

And the three outputs right below show the representative shape of each level.

- `one row example` is one time-point line such as `A, second=1, flow=1.5`.
- `one sample example` is one sample, like the mean and max values of action `A`.
- `window summary` is a segment aggregate made by regrouping the sample table into `recent` and `baseline`.

The row count decreases not because of simple compression, but because `what counts as one case` has changed.

Summarized in one sentence, the example says the following: `A, second=1` shows what happened at that moment, `event_id=A` shows what one action was like as a whole, and `recent` shows a state comparison made by regrouping several such samples again. Even with the same data, once the question changes, we move back and forth among exactly these three levels.

## Quick Questions to Ask When a Table Arrives

In practice, confusion is already reduced a great deal if the following three questions are written down first.

1. Does one line of the current table mean a time-point record, one full action, or a recent-segment aggregate?
2. Am I trying to read one line, one action, or the whole recent state right now?
3. Is the value I am about to attach a feature, a comparison column, or a candidate review sentence?

These three questions each play the role of separating `row`, `sample`, and `segment` again.

This section is not a terminology table, but something that can be reread as the problem of reading `levels of representation` at the same time.

## A Small Diagram

Reduced to the shortest form, the earlier explanation says that `one row -> one sample -> one segment` is a shift across levels where the same data is reread into larger comparison units. Each level answers a different question, so they should not be mixed as if they were the same unit.

--8<-- "assets/part-03/chapter-04/p3-4-3-mermaid-01-en.mmd"

So `one row`, `one sample`, and `one recent segment` should not be read as three similarly named objects. They should be read as the result of reexpressing the same source data at different levels in order to answer different questions.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because the provenance framework explains that it should support identifying an object and representing derivation, it provides a general basis for recording row-level records, event-level samples, and window-level aggregates as distinct representation levels. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains that a base period is a reference used for comparison with another period, it strengthens the point that aggregate-level representations such as a recent segment and a baseline segment live at a comparison level different from a sample-level representation. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example presupposes sample-level structure, it supports the point that row-level records and window-level aggregates should not be read as if they were sample-level examples. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
