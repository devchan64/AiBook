# P3-9.4 How Do Review Results Turn from Review Notes into Target Candidates

> Section ID: `P3-9.4`
> Version: `v2026.07.20`

Even when the [review queue](/AiBook/en/reference/concept-glossary-alpha/v/#glossary-review-queue) and [comparison report](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-report) appear first, a [target candidate](/AiBook/en/reference/concept-glossary-alpha/m/#glossary-target-candidate) is usually not given immediately. What remains at the beginning is often not a neat `correct label`, but varied review results and review notes. A target candidate should therefore be read more accurately not as `an answer given from the start`, but as `the result of turning judgments that repeatedly remained in the review process into more stable columns`.

## Why Do Only Notes Remain at First

At first, what remains is often not organized labels such as `normal`, `abnormal`, `cause A`, or `cause B`, but mixed review notes like these.

| event_id | review_needed | reviewer_note |
| --- | --- | --- |
| A | 1 | Late sharp drop pattern confirmed, check the next case too |
| B | 0 | No large difference from the baseline |
| C | 1 | Repeated decline, further check recommended |

This table is useful for follow-up judgment, but it is still unstable for immediate use as a learning label. Note lengths differ, expression styles differ, and one person may write a cause while another writes only the next action. So `there is a review note` and `a target label is ready` are not the same thing.

## What Else Is Needed Before Notes Become Label Candidates

For review notes to turn into target candidates, the following conditions are usually needed.

| What is additionally needed | Why it is needed |
| --- | --- |
| A shared rule that repeatedly points to the same meaning | Because different expressions from different people must be grouped under the same judgment |
| A recording style that matches the sample unit | Because the note must align with whether the sample is one event or one period summary |
| A rule for handling empty cases | Because it must be decided how to treat cases with no note |
| A basis column that can be checked again later | Because it should remain traceable why the label was attached |

So for review results to become learning labels, it is not enough simply that a value exists. There must first be a rule for leaving the same meaning in the same column.

## Difference Between a Review Queue and a Target-Candidate Table

A review queue centers on `what should be looked at first`, while a target-candidate table centers on `what should later be matched`. Even for the same event list, the center of the table changes.

| Output | Central question | Columns needed first |
| --- | --- | --- |
| Review queue | What should a person look at first? | `priority_score`, `review_needed`, comparison evidence |
| Target-candidate table | What can become a result column? | `target_candidate`, basis note, feature columns |

For example, `review_needed = 1` may be sufficient in a review queue. But in a target-candidate table, what matters more is under what condition `review_needed = 1` was attached and whether it can later be attached again by the same rule.

## The Step-by-Step Change Process

The same event list usually changes in the following order.

1. See the change signal in the comparison report.
2. Create the order in which people should inspect first in the review queue.
3. Repeatedly collect the review results left by people.
4. Organize frequently repeated judgments into common columns.
5. If those columns become relatively stable, raise them to target candidates.

This order matters because it shows that a target candidate does not appear out of nowhere. It comes from `repetition in the review process`.

## Example: Building Label Candidates from Review Notes

At first, the notes may vary like this.

| event_id | diff | repeatability | review_needed | reviewer_note |
| --- | --- | --- | --- | --- |
| A | -0.35 | high | 1 | Repeated late sharp drop, recheck needed |
| B | -0.08 | low | 0 | Leave only a record |
| C | -0.31 | high | 1 | Repeated late sharp drop, inspection recommended |

In this state, it is hard to use `reviewer_note` directly as a target label. Instead, repeated phrases can be reorganized into more stable columns.

| event_id | late_drop_repeated | needs_manual_review | note_source |
| --- | --- | --- | --- |
| A | 1 | 1 | Repeated late sharp drop, recheck needed |
| B | 0 | 0 | Leave only a record |
| C | 1 | 1 | Repeated late sharp drop, inspection recommended |

What makes this second table important is not that the sentences were completely removed, but that repeated judgments were moved into columns with the same meaning. If `note_source` remains, it is also possible to trace again why the label candidate was attached.

## Which Columns Tend to Become Target Candidates First

Not every review note becomes an equally good target candidate.

| What tends to become a candidate first | What is still difficult |
| --- | --- |
| Repeated 0/1 judgments such as `review_needed` | Entire long free-form descriptive notes |
| Judgments such as `late_drop_repeated` that can be attached again with nearly the same meaning | Cause descriptions whose names differ by person |
| Statuses such as `normal/caution` with relatively shared criteria | Cause classification without a detailed cause taxonomy |

So what becomes easier to structure first is usually columns such as `whether review is needed`, `whether a repeated warning exists`, and `simple state categories`. Detailed cause classification tends to stabilize later. In many cases, the target is not something that was originally inside the dataset, but the result of turning judgments accumulated through comparison reports and review queues back into columns. What matters here is deciding whether something should still remain a free-form note, whether it can be raised into a shared judgment column, and whether it repeats enough to become a target candidate.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-4-mermaid-01-en.mmd"
```

This diagram shows that a free-form note does not become a target directly. A middle stage of `grouping the same meaning` must be present. Review results and notes accumulate first, repeated judgments inside those notes are organized into common patterns, and only then do columns such as `late_drop_repeated` and `needs_manual_review` appear. What matters in this section is not string-processing technique, but the conversion structure `note -> shared meaning -> target-candidate column`. A target should therefore be read not as a suddenly given value, but as the result of structuring the review records themselves. A target candidate is often not an answer given from the start, but the result of turning repeated judgments left in the review process into more stable columns.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `labeled example`. Used to check how labels and labeled examples separate input features from result columns in supervised learning. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance, entity, derivation overview. Used to check the provenance view that the path from review notes to shared meanings and target-candidate columns should remain traceable. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
