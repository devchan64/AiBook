# P3-4.4 What Signals Show That the Sample Unit Was Chosen Wrong

> Section ID: `P3-4.4`
> Version: `v2026.07.17`

If the sample unit is chosen incorrectly, the problem usually reappears later in strange forms. That is why the question `how can I notice that I am currently using the wrong sample unit?` matters. In many cases, people keep building features, labels, and comparison tables on top of the wrong sample unit, and only much later realize that the whole structure has become unstable. So this section gathers in one place the representative warning signs that should make us suspect a wrong decision about the sample unit.

When the sample unit is wrong, the problem usually shows itself again later in strange forms. If the same label repeats across several rows, if one row cannot explain a feature, or if there is a comparison table but we still cannot explain `what counts as one case`, then the sample unit should be suspected again.

## The Most Common Warning Signs

| Strange phenomenon visible now | What to suspect first |
| --- | --- |
| The same label is repeated across several rows of the same `event_id` | The label may actually belong to one full action, while we are reading time-point rows as samples |
| Features such as mean, slope, and variability are hard to explain directly on one row | We may be reading time-point records as if they were samples |
| We want to describe a comparison result, but cannot explain in words what `this one case` is | The sample unit and the comparison unit may be mixed together |
| When training and evaluation are split, nearby rows from the same action enter both sides | The split unit may be misaligned with the sample unit |
| A recent-segment comparison table was built, but individual actions and aggregate segments look mixed together in one table | We may be reading sample and segment levels as if they were the same unit |

The key point of this table is not that `every problem comes from the sample unit`. It means that if such patterns appear at the Part 3 stage, then before adding more features or changing the model, it is usually more efficient to recheck the sample unit first.

## If Features Keep Resisting Explanation, Recheck the Sample Unit

A common scene is the following. Features such as `late_drop_rate`, `flow_std`, or `duration_seconds` have been made, but when we look at one row, it is still hard to explain naturally `what does this value represent?` At that point, the feature definition itself may be poor, but the more frequent reason is that the sample unit is still not right.

| Feature name | Natural sample unit |
| --- | --- |
| `duration_seconds` | one full action |
| `late_drop_rate` | one full action or a segment summary |
| `flow_std` | one full action or a recent segment |
| `current_flow` | one time-point record row |

In other words, the feature name alone already reveals to some degree which sample unit it fits. That is exactly why it feels awkward when we try to explain `duration_seconds` on one time-point row.

## If Labels Repeat, Recheck the Unit

If an operational label such as `review_needed` is a value attached to one full action, then the scene in which the same label is repeated across several time-point rows is one of the strongest signals that the sample unit should be suspected again.

| Visible phenomenon | More natural interpretation |
| --- | --- |
| all three rows of `A` have `review_needed=1` | the label may actually belong to the one full action `A` |
| all time-point rows of `B` carry the same state value | it may not be a new label on each row, but the action-level result stored repeatedly |

The important point here is not that `label repetition is always wrong`. The important point is to ask again `to what unit does the label actually attach?`

## If Comparison Sentences Keep Feeling Awkward, Recheck the Unit

When the sample unit is misaligned, the reporting sentence also becomes strange. For example, if we look at one time-point row and try to write `this action had a larger late-stage drop than usual`, that sentence cannot stand on that one line alone. A late-stage drop can only be discussed after the whole action or segment structure has been seen.

| Sentence we want to write | Sample unit required first |
| --- | --- |
| This action was more unstable than usual | one full action |
| The recent state became lower than usual | recent-segment aggregate |
| The sensor value at this time point is high | one time-point record row |

In other words, if the sentence we keep trying to write is talking about an object larger than `one row`, then the sample unit should be suspected again.

## Small Code Example

Problem situation: when the same label repeats in a time-point table and action-level features appear only after regrouping, check how to read those as warning signs of a wrongly chosen sample unit.

Input: a raw log table in which time-point flow values by `event_id` are stored together with `review_needed`, which actually belongs to the action level

Expected output: output showing repeated labels, repeated row counts, and event-summary features that appear only after regrouping

Concept to check: repeated labels and unexplained event-level features are warning signs that a time-point row may not be the real sample unit

```python
import pandas as pd

raw = pd.DataFrame(
    [
        {"event_id": "A", "second": 0, "flow": 0.5, "review_needed": 1},
        {"event_id": "A", "second": 1, "flow": 1.8, "review_needed": 1},
        {"event_id": "A", "second": 2, "flow": 1.1, "review_needed": 1},
        {"event_id": "B", "second": 0, "flow": 0.4, "review_needed": 0},
        {"event_id": "B", "second": 1, "flow": 1.1, "review_needed": 0},
        {"event_id": "B", "second": 2, "flow": 1.0, "review_needed": 0},
    ]
)

label_repetition = raw.groupby("event_id", as_index=False).agg(
    row_count=("second", "count"),
    review_needed_sum=("review_needed", "sum"),
)

event_summary = raw.groupby("event_id", as_index=False).agg(
    duration_seconds=("second", "max"),
    flow_mean=("flow", "mean"),
    review_needed=("review_needed", "max"),
)

warning_check = pd.DataFrame(
    [
        {
            "warning_sign": "same event repeated across many rows",
            "seen_in_output": "yes" if label_repetition["row_count"].max() > 1 else "no",
        },
        {
            "warning_sign": "same label repeated within one event",
            "seen_in_output": "yes" if label_repetition["review_needed_sum"].max() > 1 else "no",
        },
        {
            "warning_sign": "event-level features appear only after regrouping",
            "seen_in_output": "yes" if "duration_seconds" in event_summary.columns else "no",
        },
    ]
)

print("1) row-level table where labels repeat inside one event")
print(raw)
print()
print("2) repeated rows and repeated labels per event")
print(label_repetition)
print()
print("3) event-level summary that appears only after regrouping")
print(event_summary)
print()
print("4) warning signs that sample unit may be wrong")
print(warning_check)
```

Expected output:

```text
1) row-level table where labels repeat inside one event
  event_id  second  flow  review_needed
0        A       0   0.5              1
1        A       1   1.8              1
2        A       2   1.1              1
3        B       0   0.4              0
4        B       1   1.1              0
5        B       2   1.0              0

2) repeated rows and repeated labels per event
  event_id  row_count  review_needed_sum
0        A          3                  3
1        B          3                  0

3) event-level summary that appears only after regrouping
  event_id  duration_seconds  flow_mean  review_needed
0        A                 2   1.133333              1
1        B                 2   0.833333              0

4) warning signs that sample unit may be wrong
                                  warning_sign seen_in_output
0           same event repeated across many rows            yes
1              same label repeated within one event            yes
2  event-level features appear only after regrouping            yes
```

The key in this example is not the calculation result itself, but `where the warning signs are actually visible`. In step 2, we see the same `event_id` repeated across multiple rows, and the fact that `review_needed` is copied as-is inside one full action. In step 3, we see that action-level features such as `duration_seconds` and `flow_mean` do not exist in the raw rows and appear only after regrouping. So the warning table in step 4 is not creating a new judgment. It is regrouping the signals that were already visible in the earlier outputs.

## Questions That Mean the Sample Unit Should Be Rechecked

In practice, the direction becomes much clearer simply by writing down the following four questions again.

1. Does this label attach to one row, or to one full action?
2. Is this feature read directly from one row, or does it appear only after several rows are grouped?
3. Is the sentence I am trying to write talking about one row, or one full action?
4. Does the training/evaluation split divide the rows of the current table, or divide the sample unit?

If two or three of these four questions already fail to align, it is usually better to recheck the sample unit before adding more features.

## A Small Diagram

The warning signs in this section are not independent checklist items. Repeated labels, features that cannot be explained on one row, awkward comparison sentences, and bad splits all converge on the same direction: recheck the sample unit.

--8<-- "assets/part-03/chapter-04/p3-4-4-mermaid-01-en.mmd"

When these diagnostic signals are collected first, it becomes easier to distinguish earlier between cases where the sample unit must be regrouped and cases where it can safely stay as it is. In other words, what matters here is not previewing the next stage, but noticing the mistaken sample-unit judgment early through repeated labels, unexplained features, and awkward comparison sentences that are already visible in the current table.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`, `label leakage`. Because these entries explain both the unit to which a label attaches and the risk of confusing feature and label roles, they support this section's core point that repeated labels and unexplained features are signals that the sample unit should be rechecked. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it explains that identifying an object and preserving derivation should be kept together, it strengthens the higher-level frame that we must be able to trace whether the current line is a time-point record or a one-action summary in order to catch sample-unit misjudgment earlier. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Hadley Wickham, `Tidy Data`, *Journal of Statistical Software* 59(10), 2014. Because it distinguishes variables, observations, and table structure, it provides the general principle behind why interpretation becomes awkward when action-level features are forced onto time-point rows. [https://www.jstatsoft.org/article/view/v059i10](https://www.jstatsoft.org/article/view/v059i10){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
