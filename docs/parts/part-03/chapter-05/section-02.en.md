# P3-5.2 How Does a Summary Table Preserve Patterns Beyond the Average

> Section ID: `P3-5.2`
> Version: `v2026.07.10`

Two actions with the same average do not always have the same structure. An average is useful for summarizing the overall level at a glance, but it does not show everything about how the values moved over time. So when turning raw logs into a summary table, we should not relax just because `the average is the same`. We also have to think about how to preserve differences in patterns beyond the average.

This section does not explain the summary-table conversion procedure itself again. Instead, it focuses on the point that the summary table built in the previous section should not be a table that leaves only the average. It should also preserve pattern differences that lead into later feature design and baseline comparison.

For example, suppose two automatic actions both recorded an average flow of 2.4. One may have risen quickly in the early phase, stayed stable in the middle phase, and then slowly declined in the late phase. The other may have barely moved at first, then risen sharply in the late phase and dropped right away. If we look only at a single average, the two may appear similar, but their operational meaning can be completely different.

To reveal this difference, values that show structure have to remain together with the average. For example:

- early-phase average
- middle-phase average
- late-phase average
- slope by segment
- time point of the maximum value
- time point when decline begins

| Action | Average flow | Early-phase slope | Late-phase slope | Interpretation |
| --- | --- | --- | --- | --- |
| A | 2.4 | large | gentle decline | relatively stable |
| B | 2.4 | almost none | sharp decline | possible late instability |

There is also an order for reading this table. First check `is the average the same?` Then check `how are the segment averages different?` Finally check `what interpretation becomes possible from slope or time-point information?` Reading in this order makes the sentence `the averages are the same but the structures are different` much clearer.

| Reading level | Value to see first | What becomes knowable |
| --- | --- | --- |
| Overall level | Overall average | Are they roughly on the same scale? |
| Segment structure | Early/mid/late averages | Which segment changed? |
| Shape change | Slope, time of the maximum, time decline starts | What kind of shape difference was there? |

So the average is only a starting point. If the average is the same, we still cannot say the structure is the same. If the average is different, we still do not automatically know in which segment the difference happened. A summary table should be a table that separates these levels and shows them.

At this point it helps to write down separately `what is missed if we only look at the average`, because then it becomes clearer what else the summary table should show.

| What the average alone misses | What should remain together |
| --- | --- |
| Whether the change happened early or late | Segment averages |
| Whether the rise speed and the fall speed differ | Segment-wise slopes |
| When the peak occurred | Time point of the maximum value |
| Whether the action stayed stable or fluctuated sharply | Variability, time decline starts |

One more thing should be added here. The average also easily hides the effect of outliers and skewness. For example, if most actions stay in a similar range but only a few cases spike to very large values, the average rises, yet `what level most actions actually were at` becomes blurred. Conversely, if most values pile up on one side and only a few cases stretch far in the other direction, the average does not show that asymmetric structure well.

| What the average alone does not show well | Why it is easy to miss | What should remain together |
| --- | --- | --- |
| Effect of a few extreme values | A small number of cases can move the average a lot | Minimum, maximum, quantiles |
| A long tail on one side | The average flattens asymmetry into one number | Median, quantiles, frequency by range |
| A structure where most cases are stable but only a few fluctuate greatly | The average cannot separate typical cases from rare cases | Sample count, outlier notes, variability |

The small example below checks in numbers a case where the averages are the same but the patterns differ.

Problem situation: check that even when the overall average looks the same, a different segment-by-segment flow should still be read as a different operating structure.

Input: an action-summary table that retains only `early_flow_mean`, `mid_flow_mean`, and `late_flow_mean`

Expected output: output in which segment differences and `pattern_note` differ even under the same `overall_mean`

Concept to check: one average alone cannot explain all pattern differences, so segment-level differences and an interpretation note should remain together

```python
import pandas as pd

summary = pd.DataFrame(
    [
        {
            "event_id": "A",
            "early_flow_mean": 1.8,
            "mid_flow_mean": 2.8,
            "late_flow_mean": 2.6,
        },
        {
            "event_id": "B",
            "early_flow_mean": 2.4,
            "mid_flow_mean": 2.4,
            "late_flow_mean": 2.4,
        },
    ]
)

summary["overall_mean"] = summary[
    ["early_flow_mean", "mid_flow_mean", "late_flow_mean"]
].mean(axis=1)
summary["mid_minus_early"] = summary["mid_flow_mean"] - summary["early_flow_mean"]
summary["late_minus_mid"] = summary["late_flow_mean"] - summary["mid_flow_mean"]
summary["pattern_note"] = summary.apply(
    lambda row: "mid peak then slight drop"
    if row["mid_minus_early"] > 0 and row["late_minus_mid"] < 0
    else "flat across segments",
    axis=1,
)

print("1) the same overall mean is not enough")
print(summary[["event_id", "overall_mean"]])
print()
print("2) segment-level differences remain")
print(
    summary[
        [
            "event_id",
            "early_flow_mean",
            "mid_flow_mean",
            "late_flow_mean",
            "mid_minus_early",
            "late_minus_mid",
        ]
    ]
)
print()
print("3) one-line pattern interpretation")
print(summary[["event_id", "pattern_note"]])
```

Expected output:

```text
1) the same overall mean is not enough
  event_id  overall_mean
0        A           2.4
1        B           2.4

2) segment-level differences remain
  event_id  early_flow_mean  mid_flow_mean  late_flow_mean  mid_minus_early  late_minus_mid
0        A              1.8            2.8             2.6              1.0            -0.2
1        B              2.4            2.4             2.4              0.0             0.0

3) one-line pattern interpretation
  event_id               pattern_note
0        A  mid peak then slight drop
1        B       flat across segments
```

The `overall_mean` of both actions is 2.4. But in stage 2, A shows `mid_minus_early=1.0` and `late_minus_mid=-0.2`, which means a rise in the middle followed by a decline later. B has 0.0 for both, so its segment structure does not change. The `pattern_note` in stage 3 is the result of folding this difference back into one sentence. So if we look only at the average, the two appear like the same case, but if we look at segment averages and segment differences together, it becomes clear that they are different action structures.

This example should also be read in the same order.

1. Check whether `overall_mean` is the same.
2. Check whether all three segment averages are the same, or only one segment differs.
3. Write one sentence about why a case with the same average but a different structure matters in operational interpretation.

For example, A can be summarized as `an action that is high in the middle and drops a little later`, while B can be summarized as `an action that stays at almost the same level from beginning to end`. Only when this one-sentence summary is possible does the numeric table reach actual structure interpretation. The point here is not that we should discard the average, but that structure interpretation stops if only the average remains. That is why values such as segment averages, segment-wise slopes, time of the maximum value, and time decline starts should remain together even when the averages are the same.

This difference becomes just as important later in baseline comparison. Even if the recent segment average looks the same as usual, the state may already have begun to change if the late-phase decline pattern has become stronger. So the ability to read `same average, different pattern` is not just a trick for looking at one extra feature. It is a preparation step for later reading `has the recent structure changed from the usual one?`

If we lump two actions into the same category just because the average is the same, we may miss cases that actually have a much steeper late decline. That is why the summary table should reveal `even when the average is the same, the structure can differ`. This idea naturally continues into later feature design, segment representation, and baseline comparison.

## Sources and Further Reading

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it provides a way to read signals and patterns inside a time flow, it gives general support for the claim that one average alone cannot explain structural change and that segment-level change and shape differences should remain together. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`: `feature engineering`. Because it explains feature engineering as turning raw data into a more useful input representation, it reinforces the point that a summary table should preserve not just the average but also structural information such as segment averages, slopes, and time points. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because the provenance framework says derivation and processing steps should remain explainable, it reinforces the higher-level frame that beyond the overall average, the segment summaries and derived values that remain should be reconstructable. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
