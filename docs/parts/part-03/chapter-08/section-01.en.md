# P3-8.1 What Adjusts Interpretation Strength?

> Section ID: `P3-8.1`
> Version: `v2026.09.20`

Calculating that a recent mean is below baseline differs from claiming that conditions have persistently worsened. What we can say depends on how many events were observed, under which conditions, and whether one event was counted repeatedly. This is why we examine [evidence strength](/AiBook/en/reference/concept-glossary-alpha/i/#interpretation-boundary).

## What does dividing 17 by 20 tell us?

The following flow-rate example is fictional and constructed for this book. Each window contains distinct completed operations, with all required measurements assumed available. Recent and baseline data use the same equipment, operating conditions, and measurement definitions. We average the per-operation late-period means with equal weights. `diff` subtracts the baseline late-period mean from the recent one.

As in [P3-7.2](../chapter-07/section-02.en.md), `same_direction_count` counts operations for which **late-period mean − early-period mean ≤ −0.30 L/min**. Equality qualifies, and each operation is counted once. `repeat_ratio` divides this count by the total operation count. A difference from baseline and a decline within an operation compare different things: a negative `diff` alone cannot determine this ratio.

| Window | diff (L/min) | event_count | same_direction_count | repeat_ratio |
| --- | ---: | ---: | ---: | ---: |
| W1 | -0.30 | 2 | 1 | 0.50 |
| W2 | -0.30 | 4 | 4 | 1.00 |
| W3 | -0.30 | 20 | 17 | 0.85 |

For W3, `17 ÷ 20 = 0.85`, or 85%. This means **17 of the 20 observed operations met the defined decline condition**. It is neither an 85% failure probability nor 85% certainty that the process state changed. W1 is `1 ÷ 2 = 50%`; W2 is `4 ÷ 4 = 100%`.

W2's 100% does not automatically make its evidence stronger than W3's. Reclassifying one of the same four operations changes W2 to `3 ÷ 4 = 75%`; reclassifying one in W3 changes it to `16 ÷ 20 = 80%`. This calculation shows greater movement with a smaller denominator. It does not establish that 20 observations are sufficient.

## Keep observation coverage and order alongside the ratio

Check whether the four operations came from one day and one material batch or covered multiple days and batches. Even 20 operations may reflect narrow conditions if they came from one batch. Distinct operations can share material or environmental influences, so they need not provide independent evidence. Twenty overlapping windows cut from one operation must not be counted as 20 operations.

Furthermore, `17/20` contains no occurrence order. It does not show whether the 17 qualifying operations came first or were interspersed among the other three. Do not rewrite it as **17 consecutive declines** or **worsening over time**. Those claims require a separate examination of time-ordered records.

| Statement directly supported by the table | Information still needed |
| --- | --- |
| One of W1's two operations met the decline condition | Does the pattern recur in further observations? |
| All four observed operations in W2 met the condition | Which dates, materials, and operating ranges do these four cover? |
| Seventeen of W3's 20 operations met the condition | What are the dependencies, occurrence order, and baseline proportion meeting the same condition? |

Without the baseline proportion meeting the decline condition, the table cannot show that such operations became more frequent than before. Causes and safety status are also absent from this ratio.

## Matching Interpretation Strength to Sample Counts and Repetition {#a-small-diagram}

Write the interpretation and the operational action separately. For W3, one statement is: “Within-operation decline occurred in 17 of 20 observed operations, but coverage and time order need examination before claiming a persistent state change.” Choose the next action using separately established limits, consequences, and response procedures.

For example, assuming valid measurements and no separate limit violation, a fictional team might send W2 and W3 for human review. This is that team's policy example, not a warning grade automatically implied by four operations, 20 operations, or 85%. Conversely, a single observation exceeding an established limit may require immediate checking under the response procedure. Low confidence in persistence does not automatically imply low urgency.

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-1-mermaid-01-en.mmd"
```

Introducing this distinction does not establish that false alarms decrease or review time is saved. Those effects require separate evaluation of actual alarm outcomes, missed cases, and time spent reviewing.

## Check your understanding

Find the unsupported parts of this statement: “W2 is a more certain failure than W3 because it is 100%; W3 deserves a strong warning because it worsened 17 times in a row.”

Explanation: 100% is the proportion of four observed operations meeting a condition, not a failure diagnosis. Evidence strength cannot be ranked without checking coverage and dependence for the four and 20 observations. The fraction 17/20 contains no order, so it cannot establish consecutive worsening. Warning grades require separate operational rules.

## Checklist

- Can you calculate 17/20 and explain its numerator, denominator, and decline condition?
- When comparing 4/4 and 17/20, can you identify missing information about coverage, dependence, and time order?
- Can you write separate statements describing the observations and choosing operational action?

## Sources and references

- [NIST/SEMATECH, What are Variables Control Charts?](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } — Reference for sampling conditions, control versus specification limits, and the relationship between signaling rules and false alarms. The fictional values and review policy above are our own examples, not NIST warning criteria. Accessed: 2026-09-20.
