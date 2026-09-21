# P3-9.3 Three Different Operational Tables

> Section ID: `P3-9.3`
> Version: `v2026.09.20`

The same roster plays different roles in a [comparison report, review queue, and target-candidate table](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure). A report explains observations, a queue assigns checking work, and a target-candidate table distinguishes confirmed outcomes from unknowns. Deleting rows absent from the queue or labeling them normal mixes these roles.

## Original roster and comparison report: include A, B, and C

Reuse the fictional comparison windows A, B, and C from [P3-8.5](../chapter-08/section-05.en.md). A row is a window grouping completed operations, not an individual operation; its key is `window_id`. A's difference and decline count also match [P3-9.2](section-02.en.md). Retain the assumptions of available measurements and safety classification, matching baseline/recent conditions and definitions, and comparable differences in the same unit.

| window_id | diff_mean (L/min) | recent_count | decline_count | safety_related |
| --- | ---: | ---: | ---: | --- |
| A | -0.35 | 20 | 14 | yes |
| B | -0.35 | 3 | 1 | no |
| C | -0.18 | 18 | 12 | yes |

`diff_mean` subtracts the baseline average of per-operation late-period means from the recent average. `decline_count` counts operations satisfying `late-period mean−early-period mean ≤ −0.30 L/min`, including equality and counting once per operation. All three roster windows are candidates for this allocation. `safety_related` is a predefined process category, not an incident outcome.

Read A's report as: “The late-period mean for 20 recent operations was 0.35 L/min below baseline; 14/20=70% met the decline condition.” B has the same difference but 1/3≈33.3%; C has a −0.18 difference and 12/18≈66.7%. These values do not establish causes or failures. Keep all three report rows so B's observations remain accessible.

## Selected review queue: only A and C for today

Use `queue-v1`: **safety-related yes first → absolute difference descending within category → ID ascending for ties**. The order is A→C→B. With capacity for two windows today, select the first two. `queue_rank` below is rank within the selected queue.

| queue_rank | window_id | Selection reason | policy_version |
| ---: | --- | --- | --- |
| 1 | A | Within yes, magnitude 0.35 exceeds 0.18 | queue-v1 |
| 2 | C | The yes group precedes B's no group | queue-v1 |

Decline proportions and recent counts are not sorting keys here. B is omitted because it ranks third and capacity is two, not because its difference is small or it has no failure. Preserve B in the roster; record `selected_for_review=0` and `selection_reason=capacity_limit` in allocation records. A and C's `selected_for_review=1` does not mean completed review or confirmed failure.

To reproduce selection, retain the candidate roster, capacity two, and allocation time alongside the policy version. With the same policy but capacity three, B would enter. This does not recalculate the warning labels of [P3-8.4](../chapter-08/section-04.en.md); ordering eligible candidates and allocating them is a separate task.

## Outcome-confirmation table: include A, B, and C again

Now assume reviews of A and C have actually finished. In this exercise, `confirmed_issue` asks **whether an equipment inspection linked to the window confirmed a problem defined by the common inspection-v1 criteria**. One means confirmed, zero means the specified scope was completed without finding that problem, and `?` means unknown. This is neither future seven-day failure nor a root-cause label.

| window_id | selected_for_review | review_status | confirmed_issue candidate | Evidence |
| --- | ---: | --- | --- | --- |
| A | 1 | completed | 1 | Fictional check-A inspection record, inspection-v1 |
| B | 0 | not_reviewed | ? | None |
| C | 1 | completed | 0 | Fictional check-C inspection record, inspection-v1 |

Record names are illustrative identifiers, not actual files. A and C's outcomes are assumed to come from separate inspections, not calculations on the comparison values. C's zero refers to the specified inspection scope, not absence of every risk. B was not inspected and cannot be assigned zero. Building the outcome table solely from the selected queue would erase this unknown row.

If considering this outcome as a supervised target, input candidates are `diff_mean`, counts, and proportions available before allocation; the outcome candidate is post-inspection `confirmed_issue`. Separate `selected_for_review`, review status, and criteria version as metadata describing selection and label provenance. Do not substitute review selection for failure truth or use post-inspection outcomes as pre-allocation inputs. Actual training requires further checks of timing, label definitions, selection bias, and evaluation conditions.

## Follow the same ID across three tables

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-01-en.mmd"
```

A points to **observed evidence −0.35 and 14/20** in the report, **policy-assigned rank 1** in the queue, and **inspection-confirmed outcome 1** in the outcome table. A common ID links them, but their sources differ. B appears in the report, is absent from the selected queue, and remains `?` in the outcome table.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-3-mermaid-02-en.mmd"
```

These tables are not a mandatory sequence. Outcomes collected through independent inspections can populate a target-candidate table without passing through a queue. Whatever the pathway, retain original identifiers and outcome evidence, and do not copy a window label onto every individual operation within it.

## Find the missing B

Capacity rises to three, and B is assigned, but its review has not started. What changes in B's queue membership, selection flag, and outcome candidate?

Explanation: The queue becomes A→C→B; B has rank 3 and `selected_for_review=1`. Its status remains `not_reviewed`, and its outcome remains `?`. Allocation and outcome confirmation are different activities. Confirming A and C does not justify deleting unreviewed B or assigning it zero.

## Checklist

- Can you locate A in all three tables and explain each value's source and role?
- Can you distinguish the three-row roster, two-row selected queue, and three-row outcome table?
- Can you avoid converting queue exclusion or lack of review into deletion or a normal label?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for tracing derived results through common identifiers and processing activities. The roster, allocation, and inspection outcomes are fictional examples constructed for this book. Accessed: 2026-09-20.
