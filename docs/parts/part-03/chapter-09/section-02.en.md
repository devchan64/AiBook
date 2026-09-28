# P3-9.2 Why Should Some Problems Remain Comparison Reports?

> Section ID: `P3-9.2`
> Version: `v2026.09.20`

“How does current flow differ from its reference?” requires observations and comparison evidence, not necessarily a future-failure prediction. A [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) communicates observed differences and their limitations. If it answers that question, it is complete without becoming a prediction system and can remain useful as long as the purpose remains.

## What one report row can establish

Reuse fictional row A from [P3-8.4](../chapter-08/section-04.en.md). One row is a comparison window containing 20 recent completed operations. Retain its applicability assumptions: required measurements are available; baseline and recent data match in type, operating conditions, units, and segment definitions; and no separate allowable-limit violation exists.

| Field | Value for A | Meaning |
| --- | --- | --- |
| window_id | A | Comparison-window identifier |
| diff | −0.35 L/min | Recent average of per-operation late-period means minus the corresponding baseline average |
| event_count | 20 | Distinct recent completed operations |
| decline_count | 14 | Operations with late-period mean−early-period mean ≤ −0.30 L/min |
| decline_ratio | 14/20=0.70 | Proportion meeting that decline condition |
| cause_label | Unknown | Confirmed cause record not yet available |

The decline rule includes equality and counts each operation once. The −0.35 baseline difference and −0.30 within-operation decline boundary compare different things. An unknown `cause_label` means neither that no cause exists nor that the case is normal.

The observation statement is: “The late-period mean for 20 recent operations was 0.35 L/min below baseline, and 14/20 operations met the within-operation decline condition.” Add the limitation that occurrence order and cause are unverified. Do not turn 70% into a failure probability or describe 14 consecutive declines.

## Include the policy when adding operational decisions

For this row, `review-v1` matches R1 because `−0.35 ≤ −0.30` and `0.70 ≥ 0.60`. Record `warning_level=caution`, `review_needed=1`, and `priority_band=first`. These come from the fictional assignment policy in P3-8.4, not from calculating a cause label or failure probability.

| Report component | Content for A |
| --- | --- |
| Observed evidence | diff=−0.35 L/min; decline condition met in 14/20 operations |
| Interpretive limits | Time order and cause unverified |
| Policy application | First-priority review under R1 of review-v1 |
| Next check | Compare time-ordered raw records for the 20 operations with per-operation setting histories |

The report can thus explain a current difference and support a specific checking action. Automatically adding “high review priority because the difference is large” without a policy would mix observations with assignment decisions. An ordered review queue may use the report's evidence but is a separate policy output.

## Unknown causes differ from unknown future outcomes

Without `cause_label`, these data alone are insufficient for **learning confirmed cause classification**. That does not block every prediction question. If each historical operation's inputs available at completion are consistently linked to failure outcomes over the following seven days, supervised prediction of “failure within seven days” can be considered without cause names.

The label requirement here concerns **supervised prediction**. It does not mean every analysis or machine-learning approach requires confirmed outcome labels. Also, `review_needed` is an operational policy result; using it as the ground truth for failure changes what is being learned.

| Aspect | Current comparison report | Supervised prediction of seven-day failure |
| --- | --- | --- |
| Question | How does an observed recent window differ from baseline? | Can the next seven-day outcome be estimated at operation completion? |
| Case unit | Comparison window A grouping multiple operations | Individual operation linked to an outcome label |
| Required records | Measurement definitions, baseline, recent aggregates, applicable policy | Operation ID, inputs at completion, outcome window, confirmed result, observation completion |
| Quality to check | Calculations, comparability, explanation, and policy application | Target definition, label coverage and reliability, evaluation on cases not used for training |

The current A row has no seven-day outcomes linked to individual operations. Copying its `decline_ratio=0.70` cannot create future-failure labels for those operations. Check separately whether the individual records exist. Define inclusion of outcome-window endpoints and tracking gaps, and do not fill incomplete follow-up with non-failure zero.

## Choosing Outputs That Match the Comparison Evidence {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-2-mermaid-01-en.mmd"
```

If future prediction is the purpose, do not claim the report answers that question instead. Conversely, a comparison question already answered need not be called a failed prediction task because labels are missing. Keep the report while collecting outcome records to prepare a separate prediction problem.

## Answer two requests separately

You receive two requests about A: ① “Summarize recent change and what to check today”; ② “Predict whether each operation in A will fail within the following seven days.” Separate the answer supported by current data from additional records needed.

Explanation: For ①, report −0.35 L/min, 14/20 operations, and the unverified cause, then connect R1 of review-v1 to checking raw records and setting histories. For ②, the window summary is insufficient: check individual operation IDs, inputs at prediction time, consistently defined seven-day outcomes and completion status, and evaluation data separate from training. Missing cause names alone do not make ② impossible.

## Checklist

- Can you separate A's observations, interpretive limits, and policy outputs?
- Can you identify the unit difference between a comparison window and individual operations, and the record differences between current comparison and future prediction?
- Can you distinguish cause labels from failure-outcome labels and explain label requirements in the supervised-learning context?

## Sources and references

- [Google, Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } — Reference for label and supervised machine learning concepts. The comparison example and review-v1 are fictional constructions for this book. Accessed: 2026-09-20.
