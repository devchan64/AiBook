# P3-8.7 How Operational Intervention Changes Data Interpretation

> Section ID: `P3-8.7`
> Version: `v2026.09.20`

If someone acts on a risk signal and no failure follows, was the original signal wrong, or did the action prevent failure? The outcome alone cannot establish either explanation. Reading [intervention feedback](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-intervention-feedback) requires separating the signal time, review and action, and subsequent outcome confirmation.

## Put signal, review, action, and outcome on a timeline

A, B, and C below are fictional events constructed here, separate from identically named events in other sections. All timestamps use the same time zone. `review_needed` records a request at signal time; actual review and intervention have separate records. `none` means no intervention is recorded, not that initial risk was absent.

| event_id | Signal time | review_needed | Review time | Intervention start and content |
| --- | --- | ---: | --- | --- |
| A | 2026-09-01 09:00 | 1 | 09-01 09:05 | 09-01 09:10, valve setting adjustment |
| B | 2026-09-01 10:00 | 1 | 09-01 10:08 | 09-01 10:20, component replacement |
| C | 2026-09-01 11:00 | 0 | No initial review | none |

`failure_within_7d` is 1 if a defined failure is confirmed at least once **from signal time through the following seven days**, and 0 if complete observation finds none. Include the start and exclude the end. Assume separate follow-up covers the full period for all three events using the same failure definition. C has a confirmed follow-up outcome despite having no initial review request.

| event_id | Outcome observation interval | Outcome confirmation time | failure_within_7d |
| --- | --- | --- | ---: |
| A | 09-01 09:00 inclusive to 09-08 09:00 exclusive | 09-08 09:00 | 0 |
| B | 09-01 10:00 inclusive to 09-08 10:00 exclusive | 09-08 10:00 | 0 |
| C | 09-01 11:00 inclusive to 09-08 11:00 exclusive | 09-08 11:00 | 1 |

A's zero means no failure was confirmed during a seven-day interval that includes the intervention start. It does not mean there was no initial risk or that the result would also have been zero without intervention. If observation stopped after three days, this definition would not allow assigning zero; record the unknown outcome and completion status separately.

## Distinguish post-intervention outcomes from intervention effects

Both A and B have outcome zero, so the observed failure proportion among treated cases is `0/2=0%`; for C it is `1/1=100%`. Do not translate this into “100% success at preventing failure.” Treated and untreated groups contain different events, and their initial states and selection reasons may differ.

For A, we observed only **outcome zero along the path with intervention**. We did not observe the same A under the same circumstances for seven days without intervention. The action may have helped, but failure might not have occurred anyway. C's outcome one cannot simply replace A's unobserved no-intervention outcome. The table therefore establishes neither an erroneous initial signal nor an intervention effect.

| Statement | Supported by this table? |
| --- | --- |
| A's setting adjustment began ten minutes after its signal, and its observed outcome was zero | Yes: describes timing, action, and outcome |
| A had no initial risk | No: infers initial risk from outcome zero |
| A's setting adjustment prevented failure | No: A's no-intervention outcome is unknown |
| Retain A's action and outcome-observation interval together | Yes: records needed for later interpretation |

## Separate pre-intervention inputs from later records

To explain the initial signal, link measurements available at signal time with baseline and review-policy versions. Do not treat A's 09:10 setting change or September 8 outcome as inputs already known at 09:00. When reporting subsequent operational outcomes, include the intervention and its timing.

Early shutdown can shorten an operation and remove later sensor segments; intensified inspection can produce more detailed labels for the same situation. Records are therefore needed to distinguish changed conditions from interrupted observation, or more confirmed failures from more thorough checking. The distinction between unavailable labels and confirmed non-failure connects to [P3-8.6](section-06.en.md).

## How Operational Actions Change Later Observations {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-7-mermaid-01-en.mmd"
```

Arrows show the records' time order and where intervention may affect later observation. They do not establish the size of an intervention effect. These records alone do not numerically separate natural progression from intervention effects.

## Record the action and observation interval

Replace “successful action after warning” for A with a record of signal time, intervention start and content, outcome interval, completion status, and outcome. Add one claim that remains unsupported.

Example answer: `signal_at=2026-09-01 09:00`, `intervention_at=2026-09-01 09:10`, `intervention=valve_setting_adjustment`, `followup_start=2026-09-01 09:00`, `followup_end=2026-09-08 09:00`, `followup_complete=1`, `failure_within_7d=0`. Add: “No failure was confirmed during the observation interval following the setting adjustment, but prevention remains unverified because the no-intervention outcome is unknown.” Retain the end-exclusive interval rule and confirmation source in the record definition.

If observation ended at 09-04 09:00, use `followup_complete=0` and leave `failure_within_7d` unknown. Do not extend three failure-free days into a seven-day non-failure outcome.

## Checklist

- Can you distinguish inputs, review, intervention, and outcome-confirmation times around the signal?
- Can you explain why outcome zero establishes neither absent initial risk nor successful prevention?
- Can you record intervention content, timing, observation interval, and completion without treating shorter observation as seven-day non-failure?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for linking results to the activities and records involved in their production. The timeline, outcomes, and recording exercise are fictional examples, not evidence validating any particular intervention's effect. Accessed: 2026-09-20.
