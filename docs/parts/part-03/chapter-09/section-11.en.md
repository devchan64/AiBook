# P3-9.11 Target Candidates and Changing Criteria

> Section ID: `P3-9.11`
> Version: `v2026.07.25`

_Subtitle: What should be fixed first when there are multiple target candidates or the criteria keep changing?_

In real data, only one [target candidate](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-candidate) may not be visible. Multiple candidates such as `review_needed`, `final_status`, `status_type`, and `priority_bucket` may appear together, and even a [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target) with the same name may follow different judgment criteria at different times. In that state, the problem itself becomes unstable unless you first fix which one is the representative problem and which version of the current definition is in use. If there are multiple target candidates or the criteria change, you should first write which target is the [representative target](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-representative-target) and what the current [target definition version](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-definition-version) is.

| What should be fixed first | Why it is needed |
| --- | --- |
| [Representative target](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-representative-target) | To make clear which problem is being solved first right now |
| [Target definition version](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-definition-version) | To avoid mixing different criteria under the same name |
| Other target candidates to manage together | To leave a record of which result candidates coexist in the same data |

| Common scene | Note that is needed |
| --- | --- |
| `review_needed` and `final_status` exist together | Which one should be the representative problem first |
| Last month and this month use different judgment criteria | The point of rule change and the version |
| `warning`, `review`, and `failure` exist together | Which level should be treated as the target |

## Why the Representative Target Must Be Fixed First

The most common confusion when several target candidates exist together is the thought that `they all come from the same events anyway, so we can choose one later`. But if the representative target is not fixed first, even the explanation of what problem is currently being solved starts to wobble.

For example, if `review_needed` is taken as the representative target, the question becomes `what should be looked at again first`. By contrast, if `final_status` is taken as the representative target, the question becomes `what state will this eventually close into`. Even when the same event table is used, the objective, evaluation, and error interpretation change. So a state without a fixed representative target is not simply `a state with a lot of data`, but closer to `a state in which the problem itself has not yet been closed into one question`.

## Looking at a Conflicting Scene Once More

| event_id | review_needed | final_status | status_type | priority_bucket |
| --- | --- | --- | --- | --- |
| A | 1 | pending | unstable | high |
| B | 1 | normal | recovered | medium |
| C | 0 | normal | stable | low |

In this table, `A` and `B` both have `review_needed = 1`, but their `final_status` and `status_type` values differ. If the representative target is `review_needed`, then `A` and `B` are grouped as the same result. If the representative target is `final_status`, then `pending` and `normal` become different results. That means the same event can become either the same answer or a different answer depending on which column is fixed as the representative target.

## A Small Diagram

When several candidates coexist, the table alone can make it feel like `we can choose one later`. The actual order is to stabilize the representative target first.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-11-mermaid-01-en.mmd"
```

What this scene shows is that choosing the representative target is not an administrative note added later. It is the act of defining the central question of the current problem, and the target definition version is what fixes the criteria by which that question is being read.

So the real difficulty when there are many target candidates is not `name collision`, but that `the problem itself becomes unstable unless the representative result and the definition version are fixed together`. What is fixed here is the combination of `representative-result definition`, `definition-version management`, and `expansion-candidate management`, so that the central problem remains stable even when several target candidates arise from the same data.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. Used to check the term basis that a label is the answer or result part of a supervised-learning example and that a proxy label approximates labels not directly available in a dataset. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
