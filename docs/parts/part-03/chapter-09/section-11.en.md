# P3-9.11 Candidate Targets and Changing Criteria

> Section ID: `P3-9.11`
> Version: `v2026.09.20`

One sample may contain review need, post-inspection status, and processing priority. These columns answer different questions. Separate choosing the [target](/AiBook/en/reference/concept-glossary-alpha/t/#target) for this learning task from recording the criteria used to assign that target.

## Sharing a Row Does Not Mean Sharing an Answer

A, B, and C are fictional completed operations local to this section. `review_needed` records need under specified review criteria; `final_status` records the final state within an inspection's scope. Its definition is `inspection-status-v1`: after inspection is complete, record `abnormal` if an issue is confirmed, otherwise `normal`. `normal` does not imply that no later failure will occur.

| event_id | `review_needed` | `final_status` | `label_status` |
| --- | ---: | --- | --- |
| A | 1 | ? | pending |
| B | 1 | normal | confirmed |
| C | 0 | normal | confirmed |

This teaching table assumes all three operations were included in inspection. C has `normal` because a separate inspection was completed despite review need being 0, not because 0 was copied into a normal label. A's `pending` is a confirmation state, not an outcome class alongside `normal` and `abnormal`.

When reproducing the review criteria, A and B share answer `review_needed=1`. When predicting later inspection status from information at operation completion, the target is `final_status`, and A has no answer yet. B and C's two normal results do not establish sufficient training data either. Inputs must be limited to pre-inspection information, excluding the inspection outcome.

Here we choose “predict post-inspection status” as the main question, recording `target_name=final_status` and `target_definition_version=inspection-status-v1`. Keep review need and processing rank separately. The representative target specifies the question for this learning and evaluation task. Other questions or designs predicting multiple outcomes are possible; each needs its own definition, observation conditions, and evaluation.

## Apply Two Criteria to the Same Observation

Now consider a separate case X in which only the review-need criteria change. `recent_diff` is recent mean flow minus baseline mean flow under the same conditions, in L/min. X is `-0.25`, with source records, aggregation window, baseline, and calculation version held fixed. These are teaching rules, not actual safety limits.

| Review definition version | Effective from (KST) | Rule producing `review_needed` | Result for the same X=-0.25 |
| --- | --- | --- | ---: |
| `review-rule-v1` | 2026-09-01 00:00 | 1 if `recent_diff <= -0.30`, otherwise 0 | 0 |
| `review-rule-v2` | 2026-09-15 00:00 | 1 if `recent_diff <= -0.20`, otherwise 0 | 1 |

Both rules include equality. X fails `-0.25 <= -0.30` but satisfies `-0.25 <= -0.20`. Its change from 0 to 1 reflects **a changed definition**, not a worsening observation. Because this decision can be calculated directly, reproducing it does not necessarily require a model.

The model-score threshold change in [P3-9.8](section-08.en.md) changed assignment policy under a fixed outcome definition. Here we change the rule that creates `review_needed` itself. If this column supplies training answers, the answer definition changes. The inspection definition of `final_status` does not change along with it.

## Separate Effective Dates from Historical Reassessment

In this example, a version applies to new judgments made after it takes effect. Preserve X's original September 10 judgment as `review-rule-v1`, result 0. Reassessing old X on September 16 under the new criteria creates a new linked record: `review-rule-v2`, result 1. Do not overwrite the historical observation time or original judgment.

| Check before reassessment | What to record here |
| --- | --- |
| Original criteria and assessment time | Original record ID for X, September 10 assessment, `review-rule-v1`, value 0 |
| Scope of new criteria | `review-rule-v2` applies to new judgments from September 15, 00:00; historical reassessments are separate records |
| Evidence enabling reassessment | Can `recent_diff=-0.25` be verified using the same source records, units, aggregation, and baseline? |
| Reassessment and responsible person | September 16, `review-rule-v2`, value 1; record the person and reason in the actual record |
| Choice when combining training data | Use data reassessed under the same definition, or separate versions; identify records that cannot be reassessed and why |

If only the old label 0 remains, without the original `recent_diff` or calculation evidence, the new label cannot be confirmed. Old zeros include both -0.25, which becomes 1, and -0.10, which remains 0. Simply renaming versions does not harmonize their definitions. Nor should two judgments of one observation become two independent samples.

## Organizing Target Candidates and Criteria Versions {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-11-mermaid-01-en.mmd"
```

After specifying each outcome's definition and confirmation state, check version differences. When criteria change, first identify what changed and whether the same evidence supports reassessment. These notes help distinguish observation changes from definition changes when monthly proportions of label 1 shift.

Exercise: ① What labels do `recent_diff=-0.30` and `-0.20` receive under each version? ② If only X's old result 0 was retained, can it be changed to 1 under v2? ③ Can A's `review_needed=1` substitute for its unconfirmed final-status answer?

Answer: ① -0.30 is 1 under both versions; -0.20 is 0 under v1 and 1 under v2. ② Not without the observation and its supporting evidence. The new result 1 can be calculated only if X=-0.25 can be verified as in this example. ③ No: the columns answer different questions. Keep `final_status=?` and `label_status=pending` for A, consistent with [P3-9.10](section-10.en.md).

## Checklist

- Can you explain the choice of target for this task and the questions answered by other candidates?
- Can you calculate why X's 0→1 reflects a definition change rather than an observation change?
- Can you retain effective dates, original judgments, reassessment evidence and history without blindly combining labels from different versions?

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. Used to check the term basis that a label is the answer or result part of a supervised-learning example and that a proxy label approximates labels not directly available in a dataset. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
