# P3-7.1 What Should We Compare the Structure We Kept Against So That Change Becomes Visible

> Section ID: `P3-7.1`
> Version: `v2026.09.20`

A current value alone cannot tell us whether it rose or fell relative to the past. Here a [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) is the reference value paired with it. This section connects recent and baseline tables to create **difference columns and review statements**. The distinction from a baseline model for performance evaluation is discussed in [P3-7.3](section-03.en.md).

## Align Conditions Before Joining Recent and Historical Tables

This is a fictional aggregation example. The recent period is 2026-09-20 from 09:00 inclusive to 09:30 exclusive; the reference period covers the same daily half-hour from September 13 through 19. Include actions completed within each interval. Assume equipment and operating conditions other than process type match, as do sensor location, units, middle-segment definition, and missing-data rules.

First calculate each action's middle-segment mean flow, then average actions equally within each group. Units are **L/min**. This is not a pooled average of all raw measurement points, and the numbers below cannot reconstruct raw logs or their spread.

| Recent table: process_type | recent_mid_flow (L/min) | recent_count (actions) |
| --- | ---: | ---: |
| type-A | 2.10 | 20 |
| type-B | 2.30 | 18 |

| Baseline table: process_type | baseline_mid_flow (L/min) | baseline_count (actions) |
| --- | ---: | ---: |
| type-A | 2.45 | 100 |
| type-B | 2.28 | 90 |

The baseline uses records collected before the recent period starts. This period is chosen to answer a question about earlier actions at the same time of day. Older records or changed operating conditions require checking whether the reference still answers that question.

## Joining by Process Type Creates a Difference Column

Join the tables by `process_type` and calculate `diff = recent_mid_flow − baseline_mid_flow`. Each type has one baseline row here. If type alone does not identify matching conditions in real data, include equipment, operating mode, measurement definitions, or other necessary join conditions.

| process_type | Recent (L/min) | Baseline (L/min) | diff (L/min) | Recent/baseline actions |
| --- | ---: | ---: | ---: | --- |
| type-A | 2.10 | 2.45 | −0.35 | 20 / 100 |
| type-B | 2.30 | 2.28 | +0.02 | 18 / 90 |

For A, `2.10−2.45=−0.35 L/min`, giving “The recent actions' middle-segment mean flow is 0.35 L/min below the selected historical reference.” For B, `2.30−2.28=+0.02 L/min`. This table alone cannot establish whether a difference is acceptable, random variation, or a failure. A small difference and a normal state are different judgments.

If a new type has no reference, do not replace its baseline with zero and subtract. Mark the comparison unavailable and obtain a suitable reference. If several baseline rows match, choose the intended period and conditions rather than accidentally multiplying a recent row through the join.

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-1-mermaid-01-en.mmd"
```

## Changing the Baseline Changes the Comparison Question

Reversing A's subtraction gives `2.45−2.10=+0.35`. That is a column with the opposite definition, not an arithmetic error. Record “recent−baseline” alongside the name `diff`.

Comparing the same recent value 2.10 with a reference of 2.00 L/min from another historical period gives `+0.10 L/min`. Here 2.00 is hypothetical, not calculated from the reference period above. Actual use would require separately reporting its period, conditions, aggregation rule, and count.

Choosing a baseline to obtain a desired sign changes the question about differences from a selected past period while presenting it as the same conclusion. If both references are used, identify their respective populations and report the differences separately. A baseline is not a number selected after seeing which result looks preferable.

Check the arithmetic: adding baseline 2.45 to A's −0.35 recovers the recent value 2.10. For B, `0.02+2.28=2.30`. Values, signs, and units must agree for someone to reproduce the review statement.

The 2.8 L/min baseline in [P3-7.2](section-02.en.md) belongs to a separate fictional example using late-segment means and 200 historical actions. Do not combine it with this middle-segment table as if it were the same dataset.

## Checklist

- Can you explain the periods, inclusion conditions, units, and aggregation units of both tables?
- Did you join recent and reference rows with matching conditions?
- Can you check the sign and L/min units of recent−baseline?
- Can you explain how changing the reference changes the population and question?

## Sources and Further Reading

- U.S. Bureau of Labor Statistics, `Base period`. Because it explains a base period as a reference for comparing other times, it supports the central point of this section that change becomes visible only when the current range and the baseline range are placed together. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute, `baseline`. Because it explains baseline as the standard against which later change is compared after an initial measurement is set, it provides a general basis for reading baseline in Part 3 as `a state-comparison reference`. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
