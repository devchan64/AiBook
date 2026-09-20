# P3-9.5 How Is the Same Event Tracked Across Outputs?

> Section ID: `P3-9.5`
> Version: `v2026.09.20`

A common ID identifies a subject, but not which calculation about it was used. If window A was compared against two baselines, `window_id=A` alone cannot identify the queue's evidence. Linking [outputs](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) requires the subject ID together with the report, policy, and outcome evidence actually used.

## Window A and its member operations use different identifiers

Continue with comparison window A from [P3-9.3](section-03.en.md). A groups 20 recent completed operations; it is not a single operation's event_id. Assign those operations the following fictional IDs to illustrate linkage. The two display rows group the list for readability; the underlying relationship consists of 20 `window_id`–`event_id` pairs.

| window_id | Member event_id list |
| --- | --- |
| A | E001, E002, E003, E004, E005, E006, E007, E008, E009, E010 |
| A | E011, E012, E013, E014, E015, E016, E017, E018, E019, E020 |

Twenty operations link to one window. Overlapping windows may also contain the same operation, so record each membership. Changes to membership require a new window ID or a separate membership version. A's membership is fixed here. Do not copy its inspection outcome to every operation E001–E020.

## Why A's two reports are not interchangeable

Retain A's −0.35 L/min difference from the preceding section and add fictional recent and baseline means of 2.20 and 2.55 L/min to expose its calculation. All times below share one time zone on 2026-09-20. The second report changes only the baseline; a newer version is not automatically more appropriate.

| report_id | window_id | Created at | baseline_version | Baseline mean | Recent mean | diff_mean |
| --- | --- | --- | --- | ---: | ---: | ---: |
| REP-A-1 | A | 10:00 | base-v1 | 2.55 | 2.20 | -0.35 |
| REP-A-2 | A | 11:00 | base-v2 | 2.30 | 2.20 | -0.10 |

Means and differences use L/min, with equal weights for per-operation late-period means. `2.20−2.55=−0.35` and `2.20−2.30=−0.10`. A's recent observations and membership did not change. The difference shifted by 0.25 L/min because the baseline changed, not as evidence of recovery.

`base-v1` and `base-v2` must resolve to baseline records specifying reference periods, equipment and operating conditions, included operations, and aggregation definitions. Names without retained definitions cannot reproduce calculations. These summaries illustrate differences; they do not establish which baseline better fits the task.

## The queue identifies the report actually used

Allocation Q-01, created at 10:30, uses `queue-v1` from [P3-8.5](../chapter-08/section-05.en.md) and capacity two. B retains difference −0.35 and safety category no; C retains −0.18 and yes. A is yes and uses REP-A-1's −0.35, yielding A→C→B and selected entries A and C.

| queue_id | Allocated at | window_id | queue_rank | source_report_id | policy_version |
| --- | --- | --- | ---: | --- | --- |
| Q-01 | 10:30 | A | 1 | REP-A-1 | queue-v1 |

This is an excerpt containing only A's selected queue row. Preserve C's queue row and original candidate B separately. Without `source_report_id`, A's two reports are ambiguous. Attaching the latest report would insert REP-A-2, created at 11:00, into a decision made at 10:30.

A new allocation using REP-A-2 would rank C's 0.18 before A's 0.10 within the yes group, giving C→A→B. Record a new allocation ID and time rather than overwriting Q-01's historical evidence. Times help cross-check chronology, but reports may share timestamps, so they cannot replace report IDs and explicit references.

## Trace an outcome candidate back to its inspection note

Link A's inspection outcome one from [P3-9.3](section-03.en.md) in the same way. The identifiers and times below are fictional additions for this tracing exercise. The note reference illustrates source identity; it is not an actual file.

| note_id | window_id | inspection_id | reviewer_id | Written at | Original note |
| --- | --- | --- | --- | --- | --- |
| NOTE-A-1 | A | check-A | RV1 | 12:00 | Completed the inspection-v1 scope and confirmed the defined issue. |

| window_id | source_queue_id | source_report_id | source_note_id | label_definition_version | confirmed_issue |
| --- | --- | --- | --- | --- | ---: |
| A | Q-01 | REP-A-1 | NOTE-A-1 | inspection-v1 | 1 |

The candidate outcome one comes from the inspection note, the difference from REP-A-1, and the rank from Q-01's policy application. Their sources differ. `inspection-v1` must resolve to the definition of the issue and inspection scope. Do not use a result note written at 12:00 as information already available for allocation at 10:30.

## Tracking Events Across Outputs with Shared Identifiers {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-5-mermaid-01-en.mmd"
```

For a queue row, follow Q-01→REP-A-1→base-v1 for comparison evidence, and the outcome candidate's NOTE-A-1→check-A for inspection evidence. Resolve member operations separately through A→E001–E020. Collapsing everything into one event_id loses the distinct units of window, calculation version, allocation, and inspection.

## Repair the wrong report link

Someone attaches REP-A-2's −0.10 to A in Q-01 because it is “the latest value,” then copies confirmed_issue=1 to all E001–E020. Identify both errors and restore the correct links.

Explanation: Q-01 specifies `source_report_id=REP-A-1`, so its historical difference is −0.35 and its baseline is base-v1. Preserve REP-A-2 separately and create a new allocation if needed. Outcome one belongs to the inspection associated with A, not automatically to each operation. Individual-operation labels require evidence at that unit.

## Checklist

- Can you trace a queue row beyond the subject ID to its actual report and baseline version?
- Can you link an outcome candidate to its inspection note, reviewer, and definition version without mixing in information unavailable at the time?
- Can you record window and operation IDs separately without automatically propagating outcomes across units?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for tracing entities, processing activities, derivations, and versions. Numbers, IDs, and times are fictional examples constructed for this book. Accessed: 2026-09-20.
