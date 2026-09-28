# P3-5.1 How Do We Turn Raw Logs into Comparable Tables

> Section ID: `P3-5.1`
> Version: `v2026.09.19`

Once one action is the [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample), the same records can be represented for different questions. Raw records show detail within an action; summaries compare segment means across actions; aggregates describe groups of actions. **A summary table is one helpful representation, while direct comparison of raw time series or their use as model inputs is also possible.**

## Start with 36 Observations Already Assigned to Segments

The [fictional flow CSV](/AiBook/assets/part-03/chapter-05/p3_5_1_raw_log_segments.csv) contains 36 observations from six actions, A–F. `flow` is measured in L/min. Every action has two observations in each of `early`, `mid`, and `late`; A, B, and C belong to `baseline`, while D, E, and F belong to `recent`.

**Action IDs, progress segments, and comparison groups have already been assigned in this input.** Here we use those assignments to calculate means, rather than calculate new segment boundaries. [P3-5.4](section-04.en.md) discusses segment criteria. The CSV lacks timestamps and original progress values, so it cannot by itself verify the segment assignment or action duration.

First inspect A’s six observations. `(event_id, progress_bin)` groups observations; each combination appears twice, so it is not a unique observation identifier.

| event_id | window | progress_bin | flow |
| --- | --- | --- | ---: |
| A | baseline | early | 0.70 |
| A | baseline | early | 0.90 |
| A | baseline | mid | 2.00 |
| A | baseline | mid | 2.10 |
| A | baseline | late | 1.70 |
| A | baseline | late | 1.80 |

## First Average Observations Within Each Action and Segment

A’s early mean is `(0.70 + 0.90)/2 = 0.80 L/min`. Its middle mean is `(2.00 + 2.10)/2 = 2.05`, and its late mean is `(1.70 + 1.80)/2 = 1.75`. These describe three different parts of A, not three means of the entire action.

Applying the same calculation to the other actions gives this table. One row is one action; `event_id` links back to its observations. Each mean divides by the two observations within that action and segment.

| event_id | window | early_flow_mean | mid_flow_mean | late_flow_mean |
| --- | --- | ---: | ---: | ---: |
| A | baseline | 0.80 | 2.05 | 1.75 |
| B | baseline | 0.80 | 2.15 | 1.65 |
| C | baseline | 0.80 | 2.00 | 1.85 |
| D | recent | 0.95 | 2.45 | 1.85 |
| E | recent | 1.05 | 2.65 | 1.95 |
| F | recent | 1.00 | 2.55 | 1.75 |

For example, this table lets us directly compare A’s and D’s middle means. Equal means do not establish equal within-segment shapes. A’s early observations 0.70 and 0.90 and B’s 0.80 and 0.80 both average 0.80, although their values differ. Inspect raw records for the sequence of changes or brief peaks.

## Average Action Means to Describe a Comparison Group

Now gather the same column from actions in the same `window`. The baseline early mean is `(A’s 0.80 + B’s 0.80 + C’s 0.80)/3 = 0.80`. The recent early mean is `(D’s 0.95 + E’s 1.05 + F’s 1.00)/3 = 1.00`. **The earlier denominator, 2, counts observations; this denominator, 3, counts actions**, giving each action equal weight.

| window | member_events | event_count | early_flow_mean | mid_flow_mean | late_flow_mean |
| --- | --- | ---: | ---: | ---: | ---: |
| baseline | A, B, C | 3 | 0.80 | 2.07 | 1.75 |
| recent | D, E, F | 3 | 1.00 | 2.55 | 1.85 |

Although the mean columns have the same names as before, they now describe three actions rather than one. Preserve the row meaning and calculation rule when passing the table to another file. The baseline middle mean is `(2.05 + 2.15 + 2.00)/3 = 2.0666…`, rounded to 2.07 only for display.

The early recent-minus-baseline difference is `1.00−0.80 = +0.20 L/min`. It is an observed mean difference among these six fictional actions, not immediate evidence of a fault or long-term change. Each group contains three actions and cannot be called “the latest 20 actions.”

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-1-mermaid-01-en.mmd"
```

Transforming 36 observations into six action rows and two aggregate rows does not redefine the action sample. It summarizes the same six actions at different levels. To investigate an aggregate, trace `window → event_id → observations in progress_bin` to locate the changed value.

## Change One Value and Trace Both Stages

Leave the source CSV unchanged and calculate a hypothetical change of A’s early observation from 0.90 to 1.50. What are A’s early mean, the baseline early mean, and the recent-minus-baseline difference?

A becomes `(0.70 + 1.50)/2 = 1.10`; baseline becomes `(1.10 + 0.80 + 0.80)/3 = 0.90`; the difference becomes `1.00−0.90 = +0.10 L/min`. The raw increase of 0.60 contributes 0.30 to the action mean and 0.10 to the three-action aggregate. Recent, middle, and late values remain unchanged. Following affected columns traces the aggregate’s evidence back to a particular observation.

## Choose Equal Weight for Measurement Points or Actions

Every action and segment above has two observations, so pooling observations directly gives the same mean. Unequal counts change this. In a separate fictional case, X has two measurements of 10 and Y has six measurements of 20.

| Question | Calculation | Result | Weight of each action |
| --- | --- | ---: | --- |
| Compare mean levels with equal weight per action | (10+20)/2 | 15 | X:Y = 1:1 |
| Average all eight collected measurements | (2×10+6×20)/8 | 17.5 | X:Y = 2:6 |

In the second calculation Y receives three times X’s weight. This is what weighting means. The point mean is not inherently wrong, nor is the action mean always right: choose the denominator and weights for the question. With irregular measurement intervals, a point mean also cannot automatically be read as a time average.

What if four more observations of 10 are collected for X? The action mean stays 15, while the point mean becomes `(6×10+6×20)/12 = 15` too. Action levels did not change; the balance of measurement counts did. A decline from 17.5 to 15 does not establish an improvement in Y’s condition.

## Checklist

- Can you explain that early/mid/late are assigned input segments, not created by this aggregation?
- Can you trace A’s two early observations through its mean to the baseline mean?
- Can you distinguish what 36 observations, six actions, and two aggregates count?
- Have you calculated which columns and groups change when one observation of A changes?
- Can you choose between 15 and 17.5 for your question and explain each action’s weight?
- Have you recorded what the summary loses and how to return to the original records?

## Sources and Further Reading

- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. General support for recording processing and derivation. The CSV, segment assignments, calculations, and exercises are our fictional example, not a table-transformation procedure prescribed by W3C. / Accessed: 2026-09-19
