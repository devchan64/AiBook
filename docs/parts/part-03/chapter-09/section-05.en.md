# P3-9.5 By What Is the Same Event Continuously Tracked Across Multiple Outputs

> Section ID: `P3-9.5`
> Version: `v2026.07.25`

Even if a comparison report, a review-candidate queue, and a target-candidate table play different roles, one sample should still be tracked continuously by the same identification rule whenever possible. That is why a column such as `event_id` appears repeatedly across multiple tables. If this link becomes vague, it may still be possible to understand that the three outputs are different tables, but it becomes hard to explain again why a given event was promoted and how a given review result later turned into a target candidate. A [comparison report](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-report), [review queue](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-review-queue), and [target candidate](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-candidate) table can play different roles, but the same sample identity and the minimum evidence link should not be broken if possible.

## Why Must the Same Event Be Tracked Continuously

There are three reasons the same event needs to be traced continuously.

| Why traceability is needed | Why it matters |
| --- | --- |
| Comparison evidence must be checked again | Because you must be able to return to the original comparison report to see why a review candidate was promoted |
| Human review results must be attached continuously | Because judgments in the review queue can later accumulate into target candidates |
| The source of a target candidate must be checked again | Because you must be able to see in what sample and by what path the current label candidate appeared |

The outputs can therefore split into three, but the identity of the sample should not split with them.

## What Becomes the Traceability Criterion

In the simplest case, an identifier column such as `event_id` or `sample_id` becomes the traceability key. In practice, however, two or three elements may be needed together like this.

| Traceability criterion | Why it is used |
| --- | --- |
| Sample identifier | To point to the basic unit such as one event or one recent window |
| Time point or creation time | To distinguish when the same sample was created |
| Version or baseline context | To see again under which comparison condition the output was produced |

For example, even when `event_id` is the same, the baseline definition or review time can differ. So when tracking the same event, it is safer to leave not only `who is it` but also `when was it read` and `under what comparison condition`.

## What Remains and What Shrinks Across the Three Outputs

Even for the same event, the column composition can shrink when the purpose of the output changes. But identification criteria and core evidence columns should not disappear too quickly.

| Output | What usually should remain | What tends to shrink |
| --- | --- | --- |
| Comparison report | `event_id`, baseline values, difference value, comparison sentence | Refined columns meant only for learning inputs |
| Review-candidate queue | `event_id`, basis for priority, `review_needed`, `priority_score` | Parts of long explanatory sentences |
| Target-candidate table | `event_id`, feature columns, target candidate, basis-note reference | Long sentences used for comparison explanation |

The key is to leave trace keys such as `event_id` and the minimum evidence while reducing explanations that do not fit the purpose of each output.

## Example of One Event Moving Through Three Tables

Suppose the same event `A` exists.

### 1. Comparison report

| event_id | baseline_mean | current_mean | diff | report_sentence |
| --- | ---: | ---: | ---: | --- |
| A | 2.6 | 2.2 | -0.4 | The late-stage mean is lower than the baseline |

### 2. Review-candidate queue

| event_id | diff | repeatability | review_needed | priority_score |
| --- | ---: | --- | ---: | ---: |
| A | -0.4 | high | 1 | 0.81 |

### 3. Target-candidate table

| event_id | mid_flow_mean | late_drop_rate | review_needed | note_source |
| --- | ---: | ---: | ---: | --- |
| A | 2.2 | -0.4 | 1 | The late-stage mean is lower than the baseline |

The three tables have different columns, but all point to the same `event_id = A`. Only with this link can you later explain again `why did A become review_needed = 1`.

## Why Are Basis Columns Such as `note_source` Needed

One thing often missed when building a target-candidate table is the `basis`. If only `review_needed = 1` remains and every reason for it is thrown away, it becomes difficult later to recheck label consistency.

| Useful evidence to keep | Role |
| --- | --- |
| Reference to the original comparison sentence | To see again why it became a review candidate |
| Summary of the review note | To see what the person actually saw and judged |
| Baseline-context note | To see under what comparison condition the judgment was attached |

So even before a target-candidate table becomes a completely `clean learning table`, it is safer for it to temporarily keep a structure where minimum evidence can still be traced.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-5-mermaid-01-en.mmd"
```

This diagram shows more directly not just that the same `event_id` repeats across many tables, but why that repetition is needed. Even when the comparison report, review queue, and target-candidate table serve different purposes, it should still be possible in the end to explain `why was A promoted`. So what matters more than merge code is that `the same sample identity + retained evidence` creates the traceability structure.

The same identifier column therefore repeats not `to mechanically join tables`, but `to explain later the source of the result and the grounds for the judgment`. A comparison report, a review queue, and a target-candidate table should keep the same sample-identification rule whenever possible so that evidence and label candidates can later be reconnected. If this identification rule becomes vague, it becomes difficult to reconnect the same event's comparison evidence, review result, and target candidate.

## Sources and References

- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance and entity linkage overview. Used to check the provenance view that the same event's comparison evidence, review result, and target-candidate columns should remain traceable with their creation context. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Machine Learning Glossary*, `labeled example`, `label`. Used to check that a labeled example carries features together with a label, supporting the explanation that the same sample identity should stay connected to result-column candidates. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
