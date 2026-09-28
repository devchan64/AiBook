# P3-3.3 Which Columns Should Be Sketched First to Move a Question into the First Table Draft

> Section ID: `P3-3.3`
> Version: `v2026.09.19`

A first table draft selects columns that answer the question and makes each value’s origin visible. Rather than memorizing column names, distinguish identifiers for a [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample), original observations, calculated [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), comparison references, and result statements. These roles are not mandatory columns in every dataset. Retain only what the current question needs.

## Choose the Question and Calculation Window First

The question is “Is a completed action’s late mean flow lower than the historical reference under the same operating conditions?” The records below are fictional examples created for this section, separate from the preceding section’s CSV. One sample is one action. For this exercise, ‘late’ means observations at seconds 8, 9, and 10 within the action. The mean is the arithmetic mean of those three measurements.

| event_id | operating_mode | flow at 8s | flow at 9s | flow at 10s |
| --- | --- | ---: | ---: | ---: |
| A | standard | 2.2 | 2.4 | 2.6 |
| B | fast | 2.0 | 2.2 | 2.4 |

All flow values are in L/min. Assume a reference of 2.8 L/min is supplied, summarizing the same 8-, 9-, and 10-second means from past actions under `standard` conditions. Its identifier in this exercise is `standard_8_10_v1`. No reference for `fast` conditions is supplied. With real data, check the source, selection conditions, and calculation method behind this identifier.

## Fill A’s Row from a Blank Template

Fill the blanks below first. `mean` denotes an average; `delta` is the current value minus the reference value.

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | --- | --- | --- | --- | --- |
| A | ___ | ___ | ___ | ___ | ___ | ___ |

Separate the roles and evidence for the cells as follows.

| Role | Records or columns used | Application to A |
| --- | --- | --- |
| Identification | `event_id`, `operating_mode` | Take action A and its operating condition from the original record |
| Observation | `flow` at seconds 8, 9, and 10 | Link 2.2, 2.4, and 2.6 as calculation evidence |
| Derived feature | `late_flow_mean` | `(2.2+2.4+2.6)/3 = 2.4` |
| Comparison | `baseline_id`, reference value, `delta_from_baseline` | Find the matching-condition and matching-window reference 2.8; calculate `2.4−2.8 = −0.4` |
| Result | `report_sentence` | State only the difference established by the comparison |

The three observations differ from their mean. The mean 2.4 is calculated from original measurements; its coincidental equality to the 9-second value does not make it a raw measurement. A draft may retain only the mean, but A’s original 8–10-second records and the calculation rule must remain traceable.

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | ---: | --- | ---: | ---: | --- |
| A | standard | 2.4 | standard_8_10_v1 | 2.8 | -0.4 | Late mean is 0.4 L/min below the reference under matching conditions |

The mean, reference, and difference all have units of L/min. This is a comparison statement about lower flow, not a fault label. Repeatability scores across multiple actions and review priorities are unnecessary for this question, so they do not belong in its first draft.

## What to Retain When B Has No Reference

Fill B’s row yourself. Decide whether to copy A’s reference 2.8, enter zero, or leave it unknown, and explain why.

B’s mean can be calculated: `(2.0+2.2+2.4)/3 = 2.2`. Its operating condition is `fast`, however, so there is no basis for reusing the `standard` reference. Leave the reference and difference unknown.

| event_id | operating_mode | late_flow_mean | baseline_id | baseline_late_flow_mean | delta_from_baseline | report_sentence |
| --- | --- | ---: | --- | --- | --- | --- |
| B | fast | 2.2 | unknown | unknown | unknown | Obtain an 8–10-second reference for fast conditions |

`unknown` does not mean zero. An actual file may store a missing-value marker separately from a reason column. Arbitrarily setting the reference to zero creates the unsupported difference `2.2−0 = +2.2`. If a suitable reference is later confirmed to be 2.2, the difference is genuinely **0**, which differs from being unable to calculate the difference.

## Turning a Question into Identification, Description, and Result Columns {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-3-mermaid-01-en.mmd"
```

If the question changes to “Which action has the highest late mean?”, comparing A’s 2.4 with B’s 2.2 answers A without a baseline. Different conditions mean that this does not explain why A is higher. Identifiers, conditions, and means suffice for this first draft, whereas “Is it below usual?” additionally requires a matching reference. Including the evidence needed for the question matters more than adding columns.

## Checklist

- Did you calculate A’s mean 2.4 and reference difference −0.4 from its three observations?
- Can you distinguish original identifiers and observations from derived means, comparison values, and report statements?
- Can you explain why B should receive neither A’s reference nor an arbitrary zero?
- Can you distinguish a calculated difference of zero from an unknown, uncomputable difference?
- Can you identify unnecessary columns when the question changes to comparing mean levels?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label`, `labeled example`, `unlabeled example`. Supports the input/outcome distinction in supervised learning and the distinction from unlabeled examples. [Source](https://developers.google.com/machine-learning/glossary#labeled-example){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- W3C, `PROV-Overview` (2013). Supports tracing entities, activities, people, processing steps, and versions involved in producing data. [Source](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
