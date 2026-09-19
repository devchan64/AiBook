# P3-7.2 How Should We Read a Comparison Table as a Human Review Sentence

> Section ID: `P3-7.2`
> Version: `v2026.09.20`

Choosing only the largest difference in a comparison table can hide what was compared and how many observations support it. A review statement should distinguish **conditions, counts, mean change, between-action spread, and rule-matching counts**. These are not substitutes for one another, nor do they automatically establish a cause or action.

## Define the Decline Rule and the Object of Standard Deviation

This fictional summary is separate from P3-7.1. Each type has a baseline of 200 earlier actions, with 20 recent completed actions for A and three for B. Assume matching operating conditions within each type, sensors, units, and early/late segment definitions. These are illustrative summary values, not results calculated from actual raw logs.

Calculate early and late mean flow for each action in L/min. The example's **decline rule is `late mean−early mean ≤ −0.30 L/min`**. Exactly −0.30 qualifies; −0.29 does not. Count an action at most once. This does not mean every instantaneous slope is negative or that a failure occurred.

Table means average the late-segment means of individual actions equally. Standard deviations measure **spread between those per-action late means**, not sensor fluctuations within an action. Assume the same sample-standard-deviation convention throughout. This example includes only actions with all observations needed for the summaries and decline classification.

| Type | Baseline count | Recent count | Baseline mean (L/min) | Recent mean (L/min) | Baseline SD (L/min) | Recent SD (L/min) | Recent declines |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| type-A | 200 | 20 | 2.8 | 2.2 | 0.2 | 0.4 | 14 |
| type-B | 200 | 3 | 2.8 | 1.9 | 0.2 | 0.5 | 1 |

## One Row for Type-A Answers Four Questions

| Question | Calculation | Supported statement |
| --- | --- | --- |
| How much did late flow level change? | 2.2−2.8=−0.6 L/min | 0.6 below the selected baseline |
| How large is the change relative to baseline? | (−0.6/2.8)×100≈−21.4% | Decrease of about 21.4% of the baseline mean |
| Did between-action spread change? | 0.4−0.2=+0.2 L/min | SD of late means increased from 0.2 to 0.4 |
| How many actions met the decline rule? | 14/20=70% | Fourteen of twenty recent actions qualified |

Relative change uses baseline mean 2.8 as its denominator; the decline proportion uses 20 recent actions. Although both are dimensionless percentages, 21.4% and 70% mean different things. A zero baseline mean makes this relative-change formula undefined.

A lower mean does not imply every action declined: actions starting at a lower level can also lower the late mean. A larger SD cannot establish repeated declines either. Fourteen qualifying actions show multiple rule matches, but determining whether they were consecutive or worsened over time requires occurrence order. With no baseline decline count, this table also cannot establish an increase in decline proportion from the past.

## Separate Limited Counts from Action Decisions

B has `1.9−2.8=−0.9 L/min`, about −32.1% relative change, and a decline proportion of `1/3≈33.3%`. Changing one action's classification moves that proportion to 0/3=0% or 2/3≈66.7%. For A, one classification changes the proportion by five percentage points, so counts also affect sensitivity of the reported proportion.

B's three actions provide limited support for generalizing to a wider population. They do not justify “only three cases, so take no action.” Check measurement errors, actual limit violations, impact, and existing response rules separately. Sample count describes an interpretive limitation, not a rule for delaying action. A's twenty actions do not by themselves guarantee independence or sufficient representativeness either.

## Include Numbers, Limits, and Follow-Up Checks in the Statement

For A: “Compared with 200 historical actions under matching conditions, the recent twenty had a late mean 0.6 L/min lower, about −21.4%. SD across per-action late means rose from 0.2 to 0.4 L/min, and 14/20 met the within-action decline rule. Review occurrence order and source records; this table alone does not establish the cause.”

For B: “The recent three actions had a late mean 0.9 L/min below baseline, with 1/3 meeting the decline rule. Record the limitation of the small count while promptly checking actual values and response criteria.” Differences in this table alone do not universally determine which type must be reviewed first.

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-2-mermaid-01-en.mmd"
```

Correct “The mean fell by 21.4%, so 70% of actions failed.” The answer is: “The late mean fell by about 21.4%, while 70% met a separately defined decline rule. Neither figure directly measures the failure proportion.”

## Checklist

- Can you explain inclusion of −0.30 and counting once per action?
- Can you distinguish the denominators and meanings of −0.6 L/min, −21.4%, and 70%?
- Can you explain that SD describes spread between per-action late means?
- Can you separate small-sample interpretation limits from action decisions?

## Sources and Further Reading

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains both the structure of comparing current performance with past performance and the distinction that a comparison signal is not immediately the same as a confirmed functional judgment, it reinforces the point that a comparison table should be read not as a cause-confirmation table but as a review-signal table. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it provides a general framework of provenance information for keeping the context of the conditions and procedures through which data was produced, it can help generalize the explanation that a comparison table should be read with comparison context such as baseline condition and recent_count rather than diff alone. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
