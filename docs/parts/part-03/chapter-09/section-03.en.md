# P3-9.3 Differences Among Three Operational Tables

> Section ID: `P3-9.3`
> Version: `v2026.07.25`

_Subtitle: How do comparison reports, review-candidate queues, and target-candidate tables organize the same events differently?_

Even the same event list changes into a [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), or a target candidate table depending on the purpose. Some tables foreground comparison sentences and difference values, others foreground review priority, and others foreground the split between input columns and result-candidate columns. Here, a target candidate should be read as a preparatory result column inside a problem structure that separates input columns from result columns, even if it has not yet hardened into a confirmed answer.

The key difference is not `what is being calculated` but `how the same event list is reorganized for different questions`.

| Output | Most direct purpose right now | What appears first in the table |
| --- | --- | --- |
| Comparison report | Show immediately what differs from the usual state | Difference value, comparison sentence, change from baseline |
| Review-candidate queue | Choose in order what a person should inspect first | Priority, review-needed status, repeatability |
| Target-candidate table | Organize candidate result columns inside the problem structure | Feature columns, target candidate, columns to hold back |

Even for the same events, the central columns change when the question changes. If you ask `what differs from the usual state and by how much`, the comparison report is natural. If you ask `what should a person look at first right now`, the review queue is natural. If you ask `what should be used as the result column`, then a target-candidate table is needed.

Suppose a one-event summary table already exists, along with baseline differences, repeatability, and judgment notes. The same data can then be read three different ways as shown below.

## 1. A Comparison Report Is a Change-Reading Table

In a comparison report, `what changed` has to appear first. The goal is still to show the shape of the change rather than to automate judgment.

| event_id | baseline_mean | current_mean | diff | repeatability | report_sentence |
| --- | --- | --- | --- | --- | --- |
| A | 2.6 | 2.2 | -0.4 | high | The late-stage mean is clearly lower than the baseline |
| B | 2.5 | 2.4 | -0.1 | low | There is no large difference from the baseline |
| C | 2.7 | 2.1 | -0.6 | high | Mean decline and increased variability appear together |

The center of this table is `difference explanation`. A reader can immediately read what differs from the usual state. But this table alone may still be insufficient to decide automatically `what should be reviewed first`, and target labels such as `normal/abnormal` may still be unclear.

## 2. A Review-Candidate Queue Is a Priority Table

When it changes into a review-candidate queue, the center of the table changes. Now, not only the existence of change matters, but also `is this worth a person looking at first`.

| event_id | diff | repeatability | review_needed | priority_score | queue_rank |
| --- | --- | --- | --- | --- | --- |
| C | -0.6 | high | 1 | 0.92 | 1 |
| A | -0.4 | high | 1 | 0.81 | 2 |
| B | -0.1 | low | 0 | 0.18 | 3 |

In this table, `priority_score`, `queue_rank`, and `review_needed` stand ahead of `report_sentence`. In other words, if the comparison report says `what change is visible`, the review-candidate queue says `which of those should a person inspect first`.

What matters is that a review-candidate queue is not automatically a target-label table. `review_needed` can be used for follow-up judgment, but that alone may not immediately become a stable cause label or final-state label.

## 3. A Target-Candidate Table Is a Result-Column-Organizing Table

When the table becomes a target-candidate table, its center shifts again. Now the key is not `what should be shown`, but `what should be given as input` and `what should be treated as the result`.

| event_id | feature_1_mean | feature_2_delta | feature_3_variability | review_needed | status_label |
| --- | --- | --- | --- | --- | --- |
| A | 2.2 | -0.4 | 0.21 | 1 | none |
| B | 2.4 | -0.1 | 0.08 | 0 | none |
| C | 2.1 | -0.6 | 0.27 | 1 | none |

Here, feature columns such as `feature_1_mean`, `feature_2_delta`, and `feature_3_variability` appear together with target candidates such as `review_needed`. This table is neither meant for immediately reading sentences like a comparison report nor for assigning priority like a review queue. It is closer to a table that separates input columns from result columns to organize the problem structure.

Even in this example, however, `status_label` is still empty. So having such a table does not mean every prediction problem becomes possible immediately. A judgment-column candidate such as `review_needed` can become the starting point for some prediction problems, but the basis for jumping straight to more detailed state classification may still be too weak.

## The Minimum Procedure by Which the Same Data Splits into Three Tables

The difference above becomes simpler if you read it in the following order.

1. First compare the baseline with the current window and create a comparison report.
2. Add repeatability and judgment criteria to that difference and create a review-candidate queue.
3. Gather again only the columns to be used as result candidates and create a target-candidate table.

This order matters because the three tables are not substitutes for one another. If you create a review-candidate queue without a comparison report, the explanation of why a case rose becomes weak. If you create only a target-candidate table without a review-candidate queue, the current reason the problem mattered can disappear. Conversely, if you keep only the review queue without a target-candidate table, it becomes hard to organize where input columns and result columns should be split.

The diagram below shows how the same event list splits into three outputs.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-01-en.mmd"
```

What should be seen first in this diagram is not `one table is copied three times`, but `one event list is cut again for three questions`. A comparison report keeps change explanation, a review queue keeps review priority, and a target-candidate table keeps the split between input columns and result columns. The three tables should therefore be read not as duplicated copies of the same data, but as reorganizations of the same event list for different purposes.

If you briefly reread only the role of the representative columns, it becomes the following.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-02-en.mmd"
```

This second diagram compresses only `what appears first in each output` after the split shown in the first diagram. A comparison report foregrounds the difference value and the comparison sentence, a review-candidate queue foregrounds review-needed status and priority score, and a target-candidate table foregrounds the split between feature columns and result-candidate columns. So the first diagram should be read as `what does it split into`, and the second as `what is foregrounded after it splits`.

## Where Should You Stop with What

Confusion decreases if you judge it like this at the end.

| What is most needed right now | Output to create first | What is still postponed |
| --- | --- | --- |
| Reading the change itself | Comparison report | Review priority, target-label table |
| Deciding the order a person should inspect first | Review-candidate queue | Stable prediction label |
| Organizing learning inputs and results | Target-candidate table | Replacing the explanation in the comparison report |

The key is that these three outputs are not `wasteful duplication of the same data three times`. They are structures that answer different questions. The comparison report handles change interpretation, the review-candidate queue handles review priority, and the target-candidate table handles the split between input and result columns.

## Sources and References

- U.S. Bureau of Labor Statistics (BLS), *BLS Handbook of Methods: Glossary*, base period. Used to check the idea that a base period or point in time can serve as a reference for comparison. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute (NCI), *NCI Dictionary of Cancer Terms: baseline*, baseline. Used to check the idea that an initial measurement can serve as a comparison point for later change. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Machine Learning Glossary*, `label`, `labeled example`. Used to check how labels and labeled examples separate input features from result columns in supervised learning. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, entity/activity provenance overview. Used to check the provenance view that different outputs from the same event list should preserve their creation context and processing steps. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
