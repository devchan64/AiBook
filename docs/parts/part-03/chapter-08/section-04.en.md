# P3-8.4 Conservative Interpretation and Operational Columns

> Section ID: `P3-8.4`
> Version: `v2026.09.20`

“Review is needed” does not calculate a priority score. To produce the same [operational output](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) from the same observations, specify inputs, applicability conditions, and decision rules. Sentences explain observations and limitations; operational columns store the results of an explicit policy.

| Layer | Information retained | Role in this example |
| --- | --- | --- |
| Comparison result | Difference, counts, rule-satisfaction proportion | Preserve observations |
| Interpretation statement | Observation, uncertainty, checking action | Explain meaning and limitations to people |
| Operational output | Warning label, review flag, priority band | Support retrieval, grouping, and follow-up under a defined policy |

## Fix input conditions and calculations

The following is a separate fictional aggregate for practicing operational outputs. A, B, and C identify comparison windows. `diff` subtracts the baseline average of per-operation late-period means from the recent average, in L/min. `event_count` counts recent completed operations. As in [P3-7.2](../chapter-07/section-02.en.md), the decline condition is `late-period mean−early-period mean ≤ −0.30 L/min`, counting each operation once.

| window_id | diff (L/min) | event_count | decline_count | decline_ratio |
| --- | ---: | ---: | ---: | ---: |
| A | -0.35 | 20 | 14 | 14/20=0.70 |
| B | -0.35 | 3 | 1 | 1/3≈0.333 |
| C | -0.10 | 10 | 2 | 2/10=0.20 |

`decline_ratio=decline_count/event_count`. A's 70% is the proportion meeting the defined decline condition, not a failure probability or confidence score. The baseline difference and the within-operation decline proportion also compare different things.

Assume all required measurements are available and baseline and recent data match in type, operating conditions, units, and segment definitions. Total counts are positive integers, and decline counts range from zero to the total. Also assume a separate allowable-limit check found no violation. Rows with missing measurements, mismatched conditions, limit violations, or unknown violation status are outside this policy's scope. Route them to data checks or existing response procedures; do not use the last policy row to treat them as normal.

## A policy connecting numbers to operational decisions

Suppose a fictional team defines the following review-assignment policy, `review-v1`. For rows satisfying the applicability conditions, apply **the first matching rule from top to bottom**. The values 0.30 and 0.60 are choices for this exercise, not statistically validated boundaries or actual equipment safety limits.

| Rule | Input condition | warning_level | review_needed | priority_band |
| --- | --- | --- | ---: | --- |
| R1 | diff ≤ −0.30 and decline_ratio ≥ 0.60 | caution | 1 | first |
| R2 | R1 does not match and diff ≤ −0.30 | caution | 1 | standard |
| R3 | Neither rule above matches | watch | 0 | none |

`caution` is this policy's review label, not a failure diagnosis. `first` means review before `standard` within this policy, not greater certainty about the cause. `watch` and `review_needed=0` mean **not placed in the review queue by this rule**, not guaranteed safety or cancellation of all follow-up. Both boundaries include equality. Use the original fraction for decisions, not its rounded display value.

## Comparing the Roles of Interpretation Statements and Operational Columns {#looking-at-the-comparison-table-first}

Follow A through the policy: `−0.35 ≤ −0.30` and `14/20=0.70 ≥ 0.60`, so R1 matches. Store `warning_level=caution`, `review_needed=1`, and `priority_band=first`. An explanation can say: “The late-period mean for 20 recent operations was 0.35 L/min below baseline, and 14 operations met the decline condition. The cause is unverified. Rule R1 of review-v1 assigns this window to first-priority review.”

| window_id | warning_level | review_needed | priority_band | rule_id |
| --- | --- | ---: | --- | --- |
| A | caution | 1 | first | R1 |
| B | caution | 1 | standard | R2 |
| C | watch | 0 | none | R3 |

B meets the difference condition but has `1/3 < 0.60`, so R2 applies. It is not excluded from review because it has only three recent operations. C has `−0.10 > −0.30`, so R3 applies. Store `policy_version=review-v1` on every output row and use `window_id` to locate its original comparison row. Preserve the baseline version and input values as well, so the policy application can be checked again.

If another policy set R1's proportion boundary to 0.80, the same A would match R2 instead of R1. Observations and causal uncertainty would remain unchanged; only the assigned band would change. Record a new version when the policy changes rather than inventing a band from the phrase “review needed.”

## From Interpretation Statements to Warning Columns and Review Queues {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-4-mermaid-01-en.mmd"
```

Writing a sentence explains the reasoning to readers. A real system does not have to generate natural language first and then interpret it again. It can apply the policy directly to validated inputs, produce operational columns, and generate an explanation from the same inputs, policy, and outputs. Either implementation must distinguish and trace observations and policy-selected actions.

## Apply the policy yourself

D satisfies all applicability conditions and has `diff=−0.30`, `event_count=5`, and `decline_count=3`. What does review-v1 output? What changes if only the decline count becomes two?

Explanation: Initially `3/5=0.60`, and equality is included at both boundaries, so R1 outputs `caution·1·first`. With two declines, `2/5=0.40`, so R2 outputs `caution·1·standard`. These are policy assignments, not certifications of representativeness or failure from five observations. If missing measurements prevent calculating the proportion, revisit applicability instead of routing the row to R3.

## Checklist

- Can you apply the same policy to A, B, C, and boundary case D and reproduce their operational columns?
- Can you distinguish an observed proportion, a policy band, and a failure probability, and explain why rule IDs and policy versions are retained?
- Can you avoid treating inapplicable rows as normal and explain why natural-language generation is not a required calculation step?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for retaining provenance connecting inputs, processing activities, and derived results. Values, rules, and bands are this book's fictional policy, not W3C warning criteria. Accessed: 2026-09-20.
