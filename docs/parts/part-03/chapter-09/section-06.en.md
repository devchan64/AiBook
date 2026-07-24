# P3-9.6 Checking Label Consistency

> Section ID: `P3-9.6`
> Version: `v2026.07.23`

_Subtitle: What should be checked first when the same event receives different labels by person or time?_

Just because a label-candidate column exists does not mean you can immediately call it a stable learning problem. In real data, two reviewers can describe the same event differently, and something treated as `caution` last month can be recorded as `normal` this month. So when reading a [target candidate](/AiBook/reference/concept-glossary-parts/05-mieum/#glossary-target-candidate), you need to check not only `does a column exist`, but also `does the same meaning repeat for the same event and similar conditions`.

## Why Should Label Consistency Be Checked Together

This question is needed to judge whether the current label candidate can be placed directly as a target label. Even if the sample boundary and result column are already set, it is hard to read it as a stable learning problem when the meaning of the judgment does not repeat.

| Structure already set | Why it still needs to be checked here |
| --- | --- |
| Sample unit | Because labels can still fluctuate even under the same sample rule |
| Target-candidate column | Because even if the column exists, it is hard to use it directly when the attachment rule differs by person |
| Comparison report and review queue | Because judgment consistency also needs to be checked when the review process accumulates into label candidates |

So what should be checked here is not `does a label-candidate column exist`, but `does that candidate really repeat with the same meaning`.

## Why Can Different Labels Attach to the Same Event

The reasons label candidates wobble usually gather into the following few categories.

| Reason for wobbling | What actually happens |
| --- | --- |
| Reviewers use different criteria | One person sees the same pattern as `review_needed`, another as `normal` |
| Operating criteria change over time | A pattern once treated as a warning is now treated as normal under a new policy |
| Basis sentences are weak | It becomes hard to match judgments again later because the reason was not left clearly |
| There are many boundary cases | Cases very close to the baseline are easier to label differently by person |

So the problem with a label candidate is not only `wrong/right`, but also `is the same rule repeating`.

## Looking at the Comparison Table First

| event_id | diff | repeatability | reviewer | review_label |
| --- | ---: | --- | --- | --- |
| A | -0.34 | high | kim | review_needed |
| A | -0.34 | high | lee | normal |
| B | -0.08 | low | kim | normal |
| B | -0.08 | low | lee | normal |
| C | -0.29 | medium | kim | review_needed |
| C | -0.29 | medium | lee | review_needed |

In this table, `A` is the same event, but `kim` wrote `review_needed` while `lee` wrote `normal`. `B` and `C` agree. Seeing this, people are often tempted to think, `there is still a label column, so we can immediately raise it to a learning problem`. In practice, however, the first thing to ask is how many events like `A` exist.

What matters is not that a label-candidate column exists, but `how often the same judgment repeats under the same condition`.

## What Is Worth Writing Down First at This Stage

At this stage, it is enough to leave the following notes before using more complex statistical indicators.

| Note to write first | Why it is needed |
| --- | --- |
| Are there labels that frequently diverge in repeated reviews of the same event? | To see the low-consistency region first |
| Is there a point where the rule changed? | To leave the possibility that label meaning changed by period |
| Should the current label candidate be used directly as the target, or should more weight remain on comparison reports? | To leave a reason for postponing the current problem-type decision |

These notes are not a perfect quality certificate. They are the act of leaving in the current judgment record, without hiding it, the fact that `labels can wobble`.

## When Should It Be Viewed as Hard to Raise Directly to a Target

If scenes like the following repeat, it is safer to refine the target candidate one more step before using it directly as the result column.

| Visible signal | More natural next action |
| --- | --- |
| Reviewer-specific labels for the same event often differ | Keep the comparison report and review queue longer |
| Label criteria change suddenly after a certain date | Read by period or leave a rule-change note |
| Free-form notes exist, but common judgment columns are weak | First strengthen the rule for organizing review notes |
| Boundary cases diverge often | Keep `review needed` as the target before `confirmed label` |

So instead of forcing unstable cause classification straight into a prediction problem, it fits the current problem-type decision better to take simpler and more repeatable judgment columns as target candidates first.

Leaving these notes makes it possible to check not only `is there a column`, but also `does that column repeat with the same meaning`. At the current stage, therefore, the more important judgment is not raising the problem type more heavily, but not leaving a label candidate whose meaning still wobbles as it is.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-6-mermaid-01-en.mmd"
```

## A Small Python Example

Problem situation: when different reviewers label the same event differently, having a label-candidate column still does not immediately make it easy to read as a stable target label.

Input: repeated review records [p3_9_6_label_reviews.csv](/AiBook/assets/part-03/chapter-09/p3_9_6_label_reviews.csv). One row in this table is a label record left by a particular reviewer for a particular event in a particular month. The key columns are `event_id`, `review_month`, `reviewer`, and `review_label`.

Expected output: output that shows the review count by event, the number of label types, the actual disagreement-event list, and the monthly label distribution side by side

Concept to check: what matters more than the existence of a candidate column is whether the same meaning repeats for the same event and similar conditions

```python
# This example checks disagreements among multiple review labels for the same event and their monthly distribution.
import pandas as pd

label_variety_threshold = 1
preview_row_count = 8

reviews_path = "docs/assets/part-03/chapter-09/p3_9_6_label_reviews.csv"
reviews = pd.read_csv(reviews_path)

label_variety = reviews.groupby("event_id")["review_label"].nunique()
disagreed_events = label_variety[label_variety > label_variety_threshold]

review_summary = pd.DataFrame(
    {
        "review_count": reviews.groupby("event_id").size(),
        "label_variety": label_variety,
    }
)

monthly_labels = (
    reviews.groupby(["review_month", "review_label"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)

disagreement_detail = (
    reviews[reviews["event_id"].isin(disagreed_events.index)]
    .sort_values(["event_id", "review_month", "reviewer"])
    [["event_id", "review_month", "reviewer", "review_label"]]
)

print("1) review record preview:")
print(reviews.head(preview_row_count).to_string(index=False))
print(f"... {len(reviews) - preview_row_count} more review records")
print()
print("2) reviews per event:")
print(review_summary)
print()
print("3) label variety by event:")
print(label_variety)
print()
print("4) events with disagreement:")
print(disagreed_events.index.tolist())
print()
print("5) disagreement detail:")
print(disagreement_detail.head(12).to_string(index=False))
print(f"... {len(disagreement_detail) - 12} more disagreement records")
print()
print("6) labels by review month:")
print(monthly_labels.to_string(index=False))
```

Expected output:

```text
1) review record preview:
event_id review_month reviewer  diff repeatability  review_label
       A      2026-04      kim -0.34          high review_needed
       A      2026-04      lee -0.34          high        normal
       A      2026-05     park -0.34          high review_needed
       B      2026-04      kim -0.08           low        normal
       B      2026-04      lee -0.08           low        normal
       B      2026-05     park -0.08           low        normal
       C      2026-04      kim -0.29        medium review_needed
       C      2026-04      lee -0.29        medium review_needed
... 28 more review records

2) reviews per event:
          review_count  label_variety
event_id
A                    3              2
B                    3              1
C                    3              1
D                    3              2
E                    3              1
F                    3              2
G                    3              2
H                    3              1
I                    3              2
J                    3              1
K                    3              1
L                    3              2

3) label variety by event:
event_id
A    2
B    1
C    1
D    2
E    1
F    2
G    2
H    1
I    2
J    1
K    1
L    2
Name: review_label, dtype: int64

4) events with disagreement:
['A', 'D', 'F', 'G', 'I', 'L']

5) disagreement detail:
event_id review_month reviewer  review_label
       A      2026-04      kim review_needed
       A      2026-04      lee        normal
       A      2026-05     park review_needed
       D      2026-04      kim        normal
       D      2026-04      lee        normal
       D      2026-05     park review_needed
       F      2026-04      kim        normal
       F      2026-04      lee review_needed
       F      2026-05     park        normal
       G      2026-04      kim review_needed
       G      2026-04      lee        normal
       G      2026-05     park        normal
... 6 more disagreement records

6) labels by review month:
review_month  normal  review_needed
     2026-04      12             12
     2026-05       6              6
```

The purpose of this example is not to build model inputs, but to check first `how many reviews were performed for the same event, and where did the labels diverge`. When you first look at the review count by event, then count the number of label types, and finally check the actual disagreement-event list and detailed records, it becomes clearer why this section asks you to look at `does label meaning repeat` before `is there a label column`. In the output, events such as `A`, `D`, `F`, `G`, `I`, and `L` appear separately because their label variety is 2 among the 12 events. Looking at the monthly label distribution together also lets you note the possibility of rule changes by period. What matters here is not one team's memo habit, but checking `label meaning stability`. When reading a target candidate, you need to ask together whether the current label candidate repeats with relatively the same meaning, whether a point of rule change can be noted, and whether unstable labels are being kept from being used directly as the result column. Only with that check does a target-candidate table become more than a list of columns. It becomes a structure that includes `the stability of label meaning`.

## Sources and References

- Google, *Machine Learning Glossary*, `rater`, `inter-rater agreement`, `label`. Used to check the role of a rater who provides labels for examples and the inter-rater agreement view for whether multiple raters agree. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance and activity context overview. Used to check the provenance view that a label candidate should remain traceable to reviewer, time, and activity context. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
