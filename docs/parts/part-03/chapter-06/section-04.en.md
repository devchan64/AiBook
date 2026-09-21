# P3-6.4 Why Not Every Column in a Summary Table Is a Feature

> Section ID: `P3-6.4`
> Version: `v2026.09.19`

A summary table can contain comparison values, input candidates, outcomes, and identifiers or context. A column name or numeric format cannot determine whether it belongs in model input. **First specify what is predicted and when, then check whether the value is actually available at that time.** One column can serve both comparison and input roles.

## Predict the Next Seven Days at Action Completion

In this fictional example, immediately after an action ends, predict whether a failure record will appear within the next seven days. Assume sensor summaries are ready at completion and the baseline was computed beforehand using only earlier actions. If current summaries are recalculated later, revisit that availability assumption.

The outcome `failure_within_7d` is 1 if any failure is recorded after completion and within seven days, excluding the completion instant and including the seven-day endpoint. It is 0 only after complete follow-up with no failure record. A and B below form a training table with outcomes attached after follow-up; those outcomes are unknown at prediction time.

| event_id | mid_flow_mean | baseline_mid_flow_mean | delta_from_baseline | failure_within_7d |
| --- | ---: | ---: | ---: | ---: |
| A | 2.40 | 3.05 | −0.65 | 1 |
| B | 2.55 | 2.60 | −0.05 | 0 |

Flow is measured in L/min. A's difference is `2.40−3.05=−0.65 L/min`: 0.65 below its historical baseline. B's is `2.55−2.60=−0.05 L/min`. A negative value is not itself a failure diagnosis, and two rows cannot establish a prediction rule or its performance.

## Mark Comparison and Input Roles Separately

The following decisions apply to this prediction task. A candidate is eligible for consideration, not guaranteed to be adopted or useful. Comparison use means examining values and conditions in reports independently of model training.

| Column or representation | Comparison use | Input candidate | Available at completion |
| --- | --- | --- | --- |
| mid_flow_mean | Inspect current level | Yes | Yes under the completed-summary assumption |
| baseline_mid_flow_mean | Inspect historical reference | Yes | If computed beforehand from past data |
| delta_from_baseline | Inspect difference from baseline | Yes | If both source values are available then |
| event_id | Link source records and check duplicates | Excluded in this example | Yes |
| Time of day derived from completion time | Compare conditions by time of day | Depending on the objective | If the timestamp is recorded immediately |
| failure_within_7d | Compare outcomes after follow-up | Excluded from input for this prediction | No |

The event ID is excluded because it is only an identifier here, not because identifiers are permanently prohibited in every task. A recurring machine ID can carry meaningful context, but deployment on new machines and the possibility of memorizing IDs require separate consideration. A timestamp may be used directly or converted to time of day, so context columns are not categorically excluded from input.

## Identical Differences Can Have Different Availability

Now suppose A's baseline of 3.05 includes measurements from the week after the action ended. Even if the resulting difference is still −0.65, that baseline could not be constructed at completion. The value can support retrospective comparison, but using it as completion-time prediction input introduces future information.

Even a baseline using only past records is unavailable immediately if its calculation finishes the next day. **Check both when source data arose and when the computed value became available.** Training rows should link to baseline versions available at their prediction times, rather than a single baseline recomputed from the entire dataset.

Moving prediction to just before the action starts also makes the current middle-segment mean unavailable. The same table names and values now require different input choices. A historical baseline may remain eligible, while the current middle mean and its difference from baseline must be excluded.

## Record Column Roles and Calculation Sources Together {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-06/p3-6-4-mermaid-01-en.mmd"
```

Mark “comparison use/input candidate/available then” for `delta_from_baseline`. All three are yes in the first case, where a past-only baseline is immediately available. With future records or a delayed calculation, retrospective comparison is possible but input at the specified prediction time is excluded. Being a comparison column does not disqualify it, and being numeric does not qualify it.

Attaching outcomes later to a training table is not itself a problem; input and target columns must be used separately. Can B be labeled 0 merely because no failure is recorded while follow-up remains incomplete? No. Record follow-up completion separately and hold incomplete outcomes.

Retain source event IDs, the period included in the baseline, baseline version, and calculation completion time to reconstruct each difference. Roles are records of purpose and timing, not mutually exclusive labels.

## Checklist

- Can you calculate A's and B's baseline differences with units?
- Can you explain why comparison and input-candidate roles can overlap?
- Can you check both future-data inclusion and calculation completion time?
- Can you identify excluded columns when prediction moves before action start?

Related concepts: [summary table](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling), [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature).

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because it explains a labeled example as the combination of features and label, it provides the basic frame for distinguishing input-description columns from candidate result columns. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Because it explains the design flaw in which a feature becomes a proxy for the label, it provides a basis for not carelessly mixing candidate result columns such as `failure_within_7d` into the feature set. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it provides a standard context for recording and tracing provenance information separately, it can serve as a general basis for leaving identification/context columns such as `event_id` and `captured_at` as information with a role different from features that describe the sample itself. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
