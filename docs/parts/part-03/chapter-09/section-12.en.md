# P3-9.12 How Do False-Alarm and Miss Costs Change Decision Criteria

> Section ID: `P3-9.12`
> Version: `v2026.09.20`

The preferred threshold can change with the costs assigned to misses and false alarms, even when scores stay the same. Here we fix target outcomes and model scores, then calculate [error costs](/AiBook/en/reference/concept-glossary-alpha/e/#glossary-error-cost) for different decision rules. Changing cost assumptions does not change the definition of the actual outcome.

## Define Positive 1 First

A–E are fictional equipment samples local to this section. Each prediction is made at `2026-09-01 10:00 KST`, targeting failure within seven days under `failure-v1` in [P3-9.7](section-07.en.md). The window includes September 1 at 10:00 and excludes September 8 at 10:00. Positive `actual=1` means a confirmed failure within that window; negative `actual=0` means no failure after full-window follow-up without gaps and completed record verification.

Scores are **supplied hypothetical model outputs**, not results of actual model training or validated failure probabilities. Assume they use inputs available at prediction time; `actual` is used only as a subsequently confirmed outcome. This teaching example compares rules against fixed historical outcomes; it does not experiment with the preventive effects of interventions.

The decision is 1 if `score >= threshold`, otherwise 0, including equality. Connect decision 1 to inclusion as a review candidate, initially assuming all candidates can be processed.

| Error | Actual outcome and decision | Meaning here |
| --- | --- | --- |
| Miss: false negative | Actual 1, decision 0 | A sample with a failure is not flagged as a candidate |
| False alarm: false positive | Actual 0, decision 1 | A sample without a failure is flagged as a candidate |

A false alarm is an error relative to this failure target, not proof that reviewing the sample was worthless in every respect. Use hypothetical cost units: 0 for a correct decision, 10 per miss, and 2 per false alarm. These are not estimates of actual money or working time.

## Count Misses and False Alarms in Five Cases

| event_id | score | actual | Decision at 0.3 | Decision at 0.5 | Decision at 0.7 |
| --- | ---: | ---: | --- | --- | --- |
| A | 0.82 | 1 | 1 · correct | 1 · correct | 1 · correct |
| B | 0.64 | 1 | 1 · correct | 1 · correct | 0 · miss |
| C | 0.41 | 0 | 1 · false alarm | 0 · correct | 0 · correct |
| D | 0.36 | 1 | 1 · correct | 0 · miss | 0 · miss |
| E | 0.22 | 0 | 0 · correct | 0 · correct | 0 · correct |

At 0.3, C is the only false alarm and there are no misses. At 0.5, D is missed; at 0.7, B and D are missed. Zero misses at 0.3 is a calculation for these five scores and outcomes, not a guarantee that low thresholds catch every failure.

Calculate **total cost = misses × 10 + false alarms × 2**.

| Threshold | Candidates | Misses | False alarms | Cost calculation |
| --- | ---: | ---: | ---: | --- |
| 0.3 | 4 | 0 | 1 | 0 × 10 + 1 × 2 = 2 |
| 0.5 | 2 | 1 | 0 | 1 × 10 + 0 × 2 = 10 |
| 0.7 | 1 | 2 | 0 | 2 × 10 + 0 × 2 = 20 |

Both 0.3 and 0.5 get four of five decisions correct. Their accuracy is equal, but one false alarm versus one miss yields assumed costs of 2 versus 10. Threshold 0.3 is cheapest among these three candidates, not an operational optimum found by searching every threshold.

## Changing Costs Leaves Targets and Scores Unchanged

Keep miss cost at 10 and raise only false-alarm cost to 12. The three costs become `0×10 + 1×12 = 12`, `1×10 + 0×12 = 10`, and `2×10 + 0×12 = 20`. Threshold 0.5 is now cheapest among the three. The cost assumption changes the policy choice; `actual`, scores, and the failure definition stay fixed.

This differs from [P3-9.11](section-11.en.md), where the rule producing training labels changed. Here we decide how burdensome each error is and compare decisions against the same outcomes. For actual use, retain cost evidence, units, the responsible person, and the policy version.

## Separate Threshold Selection from Ordering Within the Queue

The score order is always A→B→C→D→E. Changing the threshold changes candidate inclusion, not the descending order of fixed scores. Applying capacity as in [P3-9.8](section-08.en.md) requires separating candidate registration from selection for processing today.

Exercise: ① If only false-alarm cost rises to 12, does C automatically leave the candidates at threshold 0.3? ② Keep threshold 0.3 but allow only two reviews today: whom do you select first? Can the table's cost of 2 be attached unchanged to this processing selection?

Answer: ① No. With the same threshold, decisions stay the same and only cost becomes 12. Changing candidates requires changing policy. ② Select A and B by score. C and D qualify but wait because of capacity. If “selected today=1, not selected=0” is evaluated as a separate decision, actual failure D is missed: one miss, zero false alarms, cost 10 under the original costs. This differs from the threshold-only cost of 2. Later processing of waiting candidates can change operational outcomes, so this calculation does not establish actual prevention effects either.

## Reflecting Error Costs in Decision Rules {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-12-mermaid-01-en.mmd"
```

Apply rules to fixed outcomes and scores, count errors, and consider both cost and feasibility. Record `false_negative_cost`, `false_positive_cost`, `review_capacity`, threshold and tie rules, `policy_version`, cost evidence, and the responsible person to make the assumptions traceable. Do not transfer these example numbers directly into operational policy without establishing actual costs and capacity.

## Checklist

- Can you define the positive outcome first and count misses and false alarms for B, C, and D?
- Can you verify costs 2, 10, and 20 and explain the changed choice when false-alarm cost is 12?
- Can you distinguish threshold changes, score ordering, and capacity limits, recalculating cost for the final selection?

## Sources and References

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, `ROC curve`. Used to check the term basis for false negatives and false positives, and the view that real threshold selection can be affected by different costs for different errors. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Thresholds and the confusion matrix*. Used to check that different thresholds change the counts of true/false positives and true/false negatives, and that a simple default threshold can be a poor choice when error costs are asymmetric. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
