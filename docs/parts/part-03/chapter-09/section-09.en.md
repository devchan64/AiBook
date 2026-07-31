# P3-9.9 How Should the Actual Target and a Proxy Target Be Distinguished

> Section ID: `P3-9.9`
> Version: `v2026.07.31`

If you decide to use a proxy target, keep notes such as `business_goal`, `proxy_target`, `proxy_reason`, `proxy_gap`, and `review_owner` in the table. These fields keep the target name from hardening into the real goal and help you later separate what you directly predict from what you predict as a substitute when the problem type moves toward prediction.

In real data, the result you truly want to predict is often not directly visible. So it becomes tempting to use an intermediate operational judgment or a substitute column as a temporary [target](/AiBook/en/reference/concept-glossary-alpha/t/#target). The distinction needed here is between an [actual target](/AiBook/en/reference/concept-glossary-alpha/a/#glossary-actual-target) and a [proxy target](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-proxy-target). You should first write whether the target currently in use is the result you truly want to know, or a substitute column used in its place.

| Target type | Meaning |
| --- | --- |
| [Actual target](/AiBook/en/reference/concept-glossary-alpha/a/#glossary-actual-target) | The result you truly want to know and ultimately want to reduce |
| [Proxy target](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-proxy-target) | A substitute column used because the actual target cannot be seen directly or is seen too late |

For example, if `actual state confirmation` cannot be observed directly, `review needed` may be used first as a target candidate. But the two do not mean the same thing. A proxy target can become a starting point, but it does not automatically become the same thing as the actual target.

| Note to write first | Why it is needed |
| --- | --- |
| What is the result you really want to know? | To avoid hiding the original purpose of the problem |
| Why is the current column a proxy target? | To leave the distance and limitation relative to the actual target |
| How is it connected to the actual target, and at what distance? | To preserve the limitation of the proxy target and its distance from the actual target |

## Why This Distinction Changes the Problem Type Itself

The difference between an actual target and a proxy target does not end as a naming difference. Once what you are really predicting changes, the decision about whether the current problem should remain a [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure), become a [review-candidate](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) selection problem, or be raised into a [prediction](/AiBook/en/reference/concept-glossary-alpha/p/#prediction) problem also changes with it.

| What can actually be seen now | More natural problem type | Why |
| --- | --- | --- |
| The actual target is directly visible | Predict the actual target | Because inputs and results can be tied directly to the same question |
| The actual target appears late and only a proxy column is visible first | Predict the proxy target or treat it as a review-candidate problem | Because the value being predicted now is different from the value you truly want to know |
| Both the actual target and the proxy column are weak | Keep it as a comparison report or a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) | Because even the choice of which result column to use is not yet sufficiently settled |

In other words, the moment you use a proxy target, you must distinguish between `this problem is solvable` and `this problem is directly solving the original goal`. Even if it looks like a prediction problem, it may actually be predicting `a proxy judgment` rather than `the actual target`. If that difference is not written down, it becomes unclear later what the score is really measuring.

## One Scene at a Time

Suppose the result you truly want to know is `final state confirmation`, but the only thing observable right now is `review_needed`.

| event_id | recent_diff | repeatability | review_needed | final_status |
| --- | --- | --- | --- | --- |
| A | -0.31 | high | 1 | not yet available |
| B | -0.05 | low | 0 | not yet available |
| C | -0.28 | high | 1 | not yet available |

In this table, the prediction problem you can build right now may be `review_needed`. But that is not the same thing as directly predicting `final state confirmation`. The problem defined here is `does this need review`, not `what will the final state be`. Keeping the proxy-target label makes it explicit whether the current problem type is `actual-target prediction` or `proxy-column prediction`.

## A Small Diagram

The moment a proxy target is used, it becomes clearer to reread where `what can be observed now` diverges from `what is truly wanted`.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-9-mermaid-01-en.mmd"
```

A proxy target is therefore not a temporary convenient name, but a device that explicitly states that a different observable is being used in place of the original goal. The core here is to leave together `the result you truly want to know`, `the proxy column you can observe now`, and `a record of the distance between them`, so that the limitation of the proxy goal stays preserved inside the structure.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `derived label`, `proxy labels`. Used to check the term basis that a supervised-learning label is the answer or result part of an example, and that proxy labels should be chosen carefully when an actual label is absent. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
