# P3-4.4 What Signals Show That the Sample Unit Was Chosen Wrong

> Section ID: `P3-4.4`
> Version: `v2026.09.19`

Seeing the same label on several rows does not by itself mean the [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) unit is wrong. The table may attach an action’s outcome to each time-point record. **A warning asks you to inspect the original target and calculation scope; it does not establish a data error or an equipment fault.**

The previous section traced the same data through time-point, action, and period tables. Here we distinguish evidence of misreading a table’s unit from what needs correcting after inspection.

## What to Inspect After Finding a Signal

| Signal | Inspect first | Possible conclusion |
| --- | --- | --- |
| The same label repeats within an event | Does the label describe a time point or the whole action? | Storage may be intentional; counting its rows as events may be an aggregation error |
| A mean or slope cannot be explained from one row | Event, observation interval, and units used in calculation | A feature computed from several observations may legitimately be attached to a row |
| “This one case” is ambiguous | Does the statement refer to a time point, action, or period? | Check alignment between the comparison target and table unit |
| An event appears in both training and evaluation | Is the target a new event or another time point of a known event? | Evaluating new-event performance requires separating events |

The name `flow_mean` alone does not reveal whether it averages an action or a recent period. State its calculation scope. Likewise, interpreting `duration_seconds` as action duration requires start and end boundaries. A’s last observation below is at 17 seconds, but there is no end marker, so it does not establish the completed action’s duration.

Storing a value computed from several observations on a time-point row is not inherently an error. Its observation interval and availability must suit the question. For example, a full-action mean available only after completion cannot be used as an input to a prediction made during that action.

## Eighteen Positive Rows Represent One Positive Action {#small-code-example}

The [fictional source CSV](/AiBook/assets/part-03/chapter-04/p3_4_4_sample_unit_warning_log.csv) contains 36 time-point records. `event_id` identifies an action, `second` is elapsed seconds since it began, and `flow` is measured in L/min. In this exercise, `review_needed` is a fictional label assigned to the whole action: 1 means marked for review and 0 means not marked for review. It is neither a verified fault label nor a fault decision for each time point.

After checking that labels agree within each event, compare row counts and label sums:

| event_id | Time-point rows | Repeated label | Sum of row labels | Review actions counted once |
| --- | ---: | ---: | ---: | ---: |
| A | 18 | 1 | 18 | 1 |
| B | 9 | 0 | 0 | 0 |
| C | 6 | 1 | 6 | 1 |
| D | 3 | 0 | 0 | 0 |
| Total | 36 | — | 24 | 2 |

Adding the eighteen 1s for A gives 18. They all copy the same action label, so **A is one action marked for review**. Across the table, `18 + 6 = 24` positive rows represent two actions, A and C. Reporting “24 actions need review” would misread the aggregation unit.

Read the denominators too. The positive-row share is `24/36 ≈ 66.7%`; the share of actions marked for review is `2/4 = 50%`. They answer different questions. In the row share, A contributes six times as many rows as D. Neither share is model accuracy or a fault probability here.

B and D have label sums of 0, yet 0 repeats on nine and three rows respectively. A label sum alone would miss this repetition. Inspect both the number of rows and label consistency within each event.

## Which Events Remain When the Warning Threshold Changes?

Open the data, count the rows of each event, and vary `repeat_warning_threshold`. The exercise rule is: **for an event with consistent labels, flag it for a unit check when `row count > threshold`**. This fictional rule selects repeated storage to inspect; it is not a fault threshold or a standard quality criterion. The count includes the first row.

| repeat_warning_threshold | event_id selected for inspection | Selected actions |
| ---: | --- | ---: |
| 1 | A, B, C, D | 4 |
| 3 | A, B, C | 3 |
| 9 | A | 1 |
| 18 | None | 0 |

Raising the threshold from 1 to 3 removes D. Its three rows do not satisfy `3 > 3`. At 9, B also drops out at equality and only A remains. A single “Are any events selected?” indicator would be `yes` at 1, 3, and 9, so read event lists and counts together to see the change.

At 18 the warnings disappear, but the source table and labels remain unchanged. A and C are still the two actions marked for review. **The number selected for a unit check differs from the number marked for review by the label.** Reducing warnings also does not prove that a data error has been fixed.

## Inspect Conflicting Labels Before Combining Them

Now suppose one of A’s eighteen rows changes to `review_needed=0`. The row-label sum becomes 17, but A contains conflicting labels 0 and 1. Under the current one-label-per-action definition, inspect this conflict first. Raising the repetition threshold cannot resolve it.

Taking `max()` to choose 1, or keeping only the first row, would hide the disagreement. Check the original label record and linkage rule: were old and revised labels mixed, or were time-point decisions mistaken for an action label? Leave A’s action label unresolved until this is checked. If labels actually describe individual time points, different values within an action may instead be valid.

## From a Signal Back to Aggregation Rules {#a-small-diagram}

The diagram shows the decision sequence after finding repeated storage. Identify the label’s target and consistency, then align counting with the unit being reported.

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-4-mermaid-01-en.mmd"
```

Finally, correct “At threshold 3 there are three warnings, so three actions have faults.” A suitable answer is: “A, B, and C were selected for inspection of repeated storage and units. The original review label is 1 for two actions, A and C; this data alone does not establish faults.”

## Checklist

- Can you explain why A’s eighteen positive rows represent one action marked for review?
- Can you identify the numerators and denominators of 24/36 and 2/4?
- Can you explain why D drops out at 1→3 and what remains unchanged when warnings disappear at 18?
- Have you checked that B and D also contain repeated labels despite their zero sums?
- Do you inspect the original target and records instead of arbitrarily combining conflicting labels?
- Can you distinguish unit-check candidates, review labels, and equipment faults?

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary: label](https://developers.google.com/machine-learning/glossary#label){: target="_blank" rel="noopener noreferrer" }. Supports the general meaning of label. The meaning of `review_needed` and the repetition rule are defined for our fictional example. / Accessed: 2026-09-19
- scikit-learn developers, [Cross-validation for grouped data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" }. Supports separating groups when evaluating groups absent from training. It does not classify repeated storage itself as an error. / Accessed: 2026-09-19
