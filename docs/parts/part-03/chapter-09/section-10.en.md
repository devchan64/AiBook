# P3-9.10 How Do We Distinguish Delayed Label Confirmation from Incomplete Observation

> Section ID: `P3-9.10`
> Version: `v2026.09.20`

[P3-9.9](section-09.en.md) separated review requests from actual failure outcomes. Even with failure as the target, some rows still have unconfirmed outcomes. “We have not seen a failure record yet” is insufficient to fill a [training label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) with 0. Check separately whether observation has ended and whether the collected records have been verified.

## Input Cutoff and the End of the Outcome Window Differ

A, B, and C here are separate fictional equipment samples, unrelated to the same letters in previous sections. All predictions occur at `2026-09-01 10:00 KST`. As in [P3-9.7](section-07.en.md), inputs use information available by that time; subsequent outcomes are collected separately.

The target is `failure_within_7d`. Its window is **at or after September 1 at 10:00 and before September 8 at 10:00**, including the start and excluding the end. Under `failure-v1`, count an equipment fault that prevented a scheduled operation from completing, with its cause confirmed in maintenance records. Exclude planned stops.

| Boundary to check | Meaning in this example |
| --- | --- |
| Input cutoff `cutoff_at` | September 1, 10:00. Later-confirmed labels do not enter those inputs |
| End of outcome window | September 8, 10:00. Use failure occurrence time to determine membership |
| Current assessment time | Up to what time were records confirmed when the label status was recorded? |
| Actual follow-up coverage | How much of the outcome window was observed, and were there gaps? |

Seven days equal `7 × 24 = 168 hours`. Reaching September 8 at 10:00 on the calendar differs from having verified all records for that period.

## C Is Unconfirmed on September 3 and Positive on September 4

The table records evidence available at each assessment time. `?` denotes an unconfirmed outcome, not a third outcome class for the model to predict. The target here is a confirmed 0 or 1.

| Sample | Current assessment time | Evidence available then | `label_status` | Outcome |
| --- | --- | --- | --- | ---: |
| A | September 3, 10:00 | No failure record so far; the remaining period has not been observed | Observation incomplete | ? |
| B | September 8, 11:00 | All seven days followed without gaps; reports and maintenance records checked; no failure within the window | Confirmed negative | 0 |
| C | September 3, 10:00 | An incident at September 2, 14:00 was reported; whether it meets the failure definition is still being checked | Confirmation pending | ? |
| C | September 4, 15:00 | Maintenance records confirm the September 2, 14:00 incident as a target failure | Confirmed positive | 1 |

A has only 48 hours of observation, insufficient to claim 168 failure-free hours. B's 0 rests on both complete follow-up and completed record verification. Empty records alone do not justify treating another sample like B.

C's failure occurred on September 2 at 14:00 and was confirmed on September 4 at 15:00. Later confirmation does not make a confirmed label available retrospectively on September 3. Preserve that earlier pending state. On September 4, however, one failure within the window has been confirmed, so C can become 1 without waiting for all seven days. This follows from the target being “at least one failure within the window.”

## A Count of Zero Also Needs an Observation Scope

The follow-up aggregation in [P3-5.7](../chapter-05/section-07.en.md) can map one or more failures to 1. But zero failure records collected so far does not establish no failures over the entire window. Reports may not have arrived, or follow-up may contain gaps.

To confirm 0, observation must cover the full defined window without gaps or unresolved reports, and the required failure and maintenance records must establish no target failure in that period. If time has passed but evidence is insufficient, retain `?` and identify the missing records. Even a confirmed 0 means no failure during those seven days, not that the equipment will never fail.

## Checking Outcome Confirmation and Observation Completion Separately {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-10-mermaid-01-en.mmd"
```

First check for a confirmed target failure within the window. If none is confirmed, check whether both full-window observation and record verification are complete. This lets C become 1 before the window ends while preventing A from becoming 0 merely because no failure record is currently available.

| Record to retain | Concrete content |
| --- | --- |
| Sample and outcome definition | Equipment ID and prediction time, `failure-v1`, window start and end, endpoint inclusion |
| Occurrence and confirmation times | C: `failure_occurred_at=2026-09-02 14:00 KST`, `label_observed_at=2026-09-04 15:00 KST` |
| Follow-up scope and evidence | A: followed only through September 3, 10:00. B: full-window follow-up and record checks completed. Preserve source record IDs and gaps |
| Status and pending reason | `label_status`, `pending_reason`; distinguish an unfinished window from pending report verification |
| Evidence for confirmed 0 | `negative_is_complete`: true for B; false for A and unconfirmed C; not applicable to confirmed-positive C |
| Assessment history | Preserve the state at each assessment time and link later confirmation to its reasons and evidence |

Here, `label_observed_at` means when the confirmed label became usable by the system. Leave it empty while unconfirmed. Separating confirmation from occurrence helps prevent later training-table construction from placing outcomes unavailable at the time into inputs.

## Judge Endpoint Cases and Missing Records

Exercise: ① If B's September 6 records are missing and cannot be recovered from other evidence, can it remain 0 at September 8, 11:00? ② Is a failure occurring exactly at September 8, 10:00 positive for this window? ③ If C's failure is only confirmed on September 9, does it become an out-of-window failure?

Answer: ① Keep `?` and the reason for the gap because full-window verification is incomplete. ② No: the endpoint is excluded. That does not automatically establish 0; complete verification of the preceding window is still required. ③ No: occurrence remains September 2, within the window. Confirm 1 on September 9, preserving the earlier pending states.

## Checklist

- Can you explain why C changes from `?` to 1 using occurrence and confirmation times?
- Can you distinguish A's zero failure records from B's confirmed outcome 0?
- Can you apply endpoint rules and follow-up and verification requirements without turning unconfirmed outcomes into 0?

## Sources and References

- NIST/SEMATECH, [Censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm){: target="_blank" rel="noopener noreferrer" }. Used to distinguish a defined test period from failure records within it. The seven-day binary labels and confirmation states here are a teaching application. Accessed: 2026-09-20.
- W3C, [PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. Used for tracing source records, processing, versions, and derivation relationships. Accessed: 2026-07-20.
