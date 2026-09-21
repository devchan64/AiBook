# P3-4.3 How Do Time-Point Records, Action Samples, and Period Aggregates Differ

> Section ID: `P3-4.3`
> Version: `v2026.09.19`

A [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) is one case compared for the current question. **A row is a storage format: a time-point record, an action summary, or a period aggregate can each occupy one row.** Having separated splitting from scoring in the previous section, we now examine how the meaning of a row changes when the same records are grouped.

## Nine Time-Point Rows Describe Three Actions

The following flow measurements are a fictional teaching example. `event_id` identifies an action, `second` is elapsed seconds since that action began, and `flow` is measured in L/min. In this small table, `(event_id, second)` identifies one observation. `second=1` in different actions does not mean the same clock time.

| event_id | second | flow |
| --- | ---: | ---: |
| A | 0 | 0.8 |
| A | 1 | 1.5 |
| A | 2 | 1.1 |
| B | 0 | 0.7 |
| B | 1 | 1.2 |
| B | 2 | 1.0 |
| C | 0 | 0.9 |
| C | 1 | 1.6 |
| C | 2 | 1.2 |

The value 1.5 at `A, second=1` is one measurement within A. That row alone cannot give A’s overall mean or maximum. For “What was the mean flow of action A?”, its three rows supply one action sample.

## Average Each Action, Then Group Actions by Period {#small-code-example-for-seeing-the-comparison-at-a-glance}

First gather observations with the same `event_id` and calculate their mean and maximum. A separate assignment places B in the earlier reference period `baseline` and A and C in `recent`. This is a teaching assumption, not a chronology inferred from elapsed seconds or alphabetical order. Real data needs period boundaries or an explicit list of included events.

| event_id | point_count | event_flow_mean | event_flow_max | window |
| --- | ---: | ---: | ---: | --- |
| A | 3 | 1.133333 | 1.5 | recent |
| B | 3 | 0.966667 | 1.2 | baseline |
| C | 3 | 1.233333 | 1.6 | recent |

One row now represents an action, identified by `event_id`. `event_flow_mean` averages **flow observations within that action**. For A, `(0.8 + 1.5 + 1.1) ÷ 3 = 3.4 ÷ 3 ≈ 1.133333 L/min`. Its maximum, 1.5, also comes from those three observations. Such summaries can be [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) for comparing actions, but they do not preserve the full sequence of changes.

Next gather action-summary rows with the same `window`. Average their action means, giving each action equal weight.

| window | member_events | event_count | window_flow_mean |
| --- | --- | ---: | ---: |
| baseline | B | 1 | 0.966667 |
| recent | A, C | 2 | 1.183333 |

One row now represents a period, identified here by `window`. The recent mean is `(mean of A + mean of C) ÷ 2 = (3.4/3 + 3.7/3) ÷ 2 ≈ 1.183333 L/min`. **The first denominator, 3, counts observations; the second, 2, counts actions.** The tables show six decimal places, but calculations use unrounded values.

Each action has three observations here, so directly averaging the six recent observations gives the same result. With unequal observation counts, the two calculations can differ. P3-5.1 addresses that weighting difference; here, distinguish what `event_flow_mean` and `window_flow_mean` each aggregate.

The single baseline action B illustrates the calculation structure. One action is not enough to establish that the reference adequately represents usual conditions. Observing a recent mean about 0.216667 L/min higher also does not by itself establish deterioration or a fault.

## Trace an Aggregate Back to Its Records {#a-small-diagram}

To inspect the recent mean, trace `recent → A and C → seconds 0, 1, 2 of each action`. Arrows in the diagram show the calculation direction. When reviewing the result, follow them backward to its member actions and observations.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-3-mermaid-01-en.mmd"
```

The same data therefore appears as **9 time-point rows, 3 action rows, and 2 period rows**. Fewer rows do not mean the original events have disappeared. However, retaining only means and discarding the records and their links prevents reconstruction of the original shape. A real table accumulating periods needs distinct period IDs and membership boundaries, rather than repeatedly using the role name `recent` alone.

## A Period Can Be a Sample When the Question Changes

For “How does this action differ from others?”, one action is the sample. For “How does mean flow in the latest 20-action period differ from the preceding 20-action period?”, one period can be a comparison sample. `event_count` and `window_flow_mean` then describe that period. Neither samples nor features must be restricted to individual actions and their summaries.

The recent period in this small example actually contains only A and C. Asking about “the latest 20 actions” does not make this table evidence for 20 actions. Even when a period counts as one sample, record its number of constituent events separately.

## Change Period Membership and Inspect What Is Averaged

Suppose C moves from `recent` to `baseline`. First write down the row counts at all three levels and the two period means. Leave the raw observations unchanged.

The answer remains **9 rows, 3 actions, and 2 periods**. Recent now contains only A, with mean 1.133333. Baseline averages B and C: `(2.9/3 + 3.7/3) ÷ 2 = 1.1 L/min`. Individual action means stay unchanged, while period membership and means change. This is why a period mean should be read alongside its member events.

Now exclude all three observations of C from the data. There are **6 rows, 2 actions, and 2 periods**; the recent mean is A’s 1.133333. That recent mean matches the first exercise, but C belongs to baseline there and to neither period here. A mean alone cannot reveal which data was included.

## Checklist

- Can you explain what `(event_id, second)`, `event_id`, and `window` identify in the three tables?
- Can you distinguish dividing by 3 for A from dividing by 2 for the recent period?
- Can you trace the recent value 1.183333 to the six original observations of A and C?
- Can you explain how moving C or excluding it changes row counts, means, and membership?
- Have you formed a question that treats a period as a sample while recording its event count separately?

## Sources and Further Reading

- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. General support for recording production processes and derivation. The three tables and their values are our fictional example, not a three-level classification prescribed by W3C. / Accessed: 2026-09-19
- Google for Developers, [Machine Learning Glossary: example](https://developers.google.com/machine-learning/glossary#example){: target="_blank" rel="noopener noreferrer" }. An example is a case represented by features and may have a label or be unlabeled. Choosing actions or periods here is a case-specific response to the question. / Accessed: 2026-09-19
