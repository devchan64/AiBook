# P3-8.4 Conservative Interpretation and Operational Columns

> Section ID: `P3-8.4`
> Version: `v2026.07.25`

_Subtitle: How do interpretation sentences become warning columns and review-queue criteria?_

After reading a [comparison table](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), you may be left with a conservative interpretation sentence such as `the recent window shows a larger late-stage drop than the baseline, so the review priority should rise`. The next judgment is how that sentence should become structured operational columns such as `warning_level`, `review_needed`, and `priority_score`. A conservative interpretation sentence is not the end. It is the last human-interpretation stage before being turned into an [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) such as a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure). If you convert the comparison table directly into structured output, the reason for the judgment can disappear in the middle. If you leave only free text, it becomes hard to set operational priority or resort cases with the same rule.

| Level | Main form | Role |
| --- | --- | --- |
| [Comparison result](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-result) | Difference value, [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), repeatability | Shows what changed |
| Conservative interpretation sentence | `needs more observation`, `raise review priority` | Organizes judgment strength for human reading |
| Structured operational output | `warning_level`, `review_needed`, `priority_score` | Enables resorting, searching, and follow-up processing in operations |

Separating these three levels creates the flow `numbers -> sentence -> operational columns`.

## Why the Sentence Stage Is Needed First

The reason to go through a sentence stage before creating operational columns is simple.

- Which difference should remain at a `record` level
- Which difference should become a `review candidate`
- Which difference should become a `strong warning`

That judgment usually depends not on one number alone, but on the [evidence strength](/AiBook/en/reference/concept-glossary-alpha/i/#interpretation-boundary) created by sample size, repeatability, and comparison conditions read together. The sentence is therefore not decoration. It is an intermediate stage that translates numbers into operational judgment.

## Looking at One Scene Again in Three Stages

Suppose the recent window was read like this.

1. In the most recent 20 cases, the late-stage drop is larger than the baseline.
2. It also repeats, so it looks closer to a state-change candidate than to a one-off event.
3. Cause confirmation is deferred, and the review priority is raised.

If you convert those three sentences into operational columns, they can become the following.

| What was said at the sentence stage | Example structured column |
| --- | --- |
| The difference is clear, but cause confirmation is deferred | `warning_level = caution` |
| It is worth a person looking again | `review_needed = 1` |
| It should be seen before other cases | `priority_score = 0.82` |

So the sentence does not end as free narrative. It can be compressed into column names that will be reused later.

## Why Conservative Interpretation and Operational Columns Are Not the Same Thing

One thing to be careful about here is that you should not misunderstand the sentence and the columns as being determined automatically in a one-to-one way.

| Conservative sentence | What it does not immediately mean | Reason |
| --- | --- | --- |
| `More observation is needed` | Immediately `review_needed = 1` | Because observation can still stay at record level |
| `Raise the review priority` | Immediately `cause confirmed` | Because review and diagnosis are different levels |
| `Strong change signal` | Immediately `automatic action` | Because operational policy and safety criteria are still needed |

The sentence organizes the strength, but another step of structuring is still needed before it becomes actual operational columns and policy.

## Looking at the Comparison Table First

| event_id | diff | repeatability | conservative_sentence |
| --- | ---: | --- | --- |
| A | -0.35 | high | Raise review priority and defer cause confirmation |
| B | -0.35 | low | A difference appears, but the sample is small, so more observation is needed |

If these sentences are moved into structured operational columns, they can differ like this.

| event_id | warning_level | review_needed | priority_score |
| --- | --- | ---: | ---: |
| A | caution | 1 | 0.82 |
| B | watch | 0 | 0.41 |

These two tables are both needed because the first table records `why that judgment was made`, while the second records `a format that can be reused in operations`.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-4-mermaid-01-en.mmd"
```

This diagram shows that even the same difference value does not move directly into the same operational columns. You first read the comparison result, then adjust the interpretation strength in a human sentence, and only after that compress it into columns such as `warning_level`, `review_needed`, and `priority_score`. A column such as `warning_level` is therefore not a suddenly invented implementation artifact. It is the result of compressing an observed result, through human interpretation, into a format that is easier to reuse in operations. The order that must be fixed first is also this one: read `what changed`, adjust how strongly that difference should be stated in a sentence, and then compress it again into operational columns.

## Sources and References

- Google for Developers, `Thresholds and the confusion matrix`. It explains that a model's raw score is connected to final classification through a threshold, which provides the general basis for separating human interpretation sentences from structured operational columns such as `warning_level`, `review_needed`, and `priority_score`. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. It provides a provenance perspective for tracing how an observed result is derived through intermediate judgments, which is useful for explaining this section's distinction between comparison result, conservative sentence, and structured operational column. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
