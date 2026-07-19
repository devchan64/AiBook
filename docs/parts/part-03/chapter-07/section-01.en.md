# P3-7.1 What Should We Compare the Structure We Kept Against So That Change Becomes Visible

> Section ID: `P3-7.1`
> Version: `v2026.07.20`

When people hear the word baseline, they often think first of model evaluation or performance comparison. That is understandable, because the phrase baseline model also appears often in machine learning. But the baseline discussed in this Part comes earlier than that. Here, a baseline is part of the data-representation structure that decides `what should the current state be compared against` before model-performance comparison begins. If the previous chapter preserved structure through features and intermediate representations, then we now have to decide what that structure should be compared against so that change becomes visible.

To establish a baseline is not to write down one more current value. It is to decide what usual structure the current structure has to meet before change can be seen. Even when the recent value is the same, the interpretation sentence changes according to what we choose as the baseline, so the comparison structure itself has to be designed first. If the previous chapter built a feature table that contains level, change, and stability, we now enter the stage of deciding what usual range that table must meet before it becomes a comparison table.

For example, suppose we want to know whether actions carried out during the most recent 30 minutes differ from usual. In that case, recent actions alone are not enough. Even if a recent value is 2.3, that number by itself does not tell us whether it was always around 2.3, or whether usual behavior used to be 2.8 and only now has become 2.3. In other words, change becomes visible not from one absolute value alone, but only when a comparison reference appears.

| Comparison method | What becomes visible | What is easy to miss |
| --- | --- | --- |
| Look only at the current value | Is the current number large or small? | Has it changed compared with usual? |
| Look only at the recent range | The rough state of the most recent few cases | Is the recent state inside the normal range, or different from usual? |
| Recent range vs baseline | The direction and magnitude of recent change | The cause itself |

As this table shows, a baseline is not a device that immediately fixes whether something is `abnormal or not`. Instead, it lets us read `how different the recent range is from the usual structure`. That is why a baseline is not an appendix to the evaluation stage, but part of data modeling itself, because it helps decide what tables and what columns should exist in the first place.

It is also important here not to mix up `baseline` and `baseline model`.

| Distinction | What it means in this Part | What is not yet covered here |
| --- | --- | --- |
| Baseline | The comparison reference that decides what the recent range should be compared against | Model-performance competition |
| Baseline model | The starting model later used for model-performance comparison | The design of the current comparison table itself |

So the current baseline is closer not to `setting up one model`, but to `preparing together the usual structure against which recent values will be compared`. The moment a baseline is introduced, the dataset stops being a simple record table and becomes `a table where comparison is possible`. The center here is not to define the word baseline at length again, but to decide what comparison structure should be designed now so that change becomes visible.

That comparison structure can be read like this.

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-1-mermaid-01-en.mmd"
```

The recent window and the baseline window first exist separately, and they meet for the first time in the `Comparison table`. What a person actually reads is not one recent value or one baseline value, but the `Difference columns` created when the two meet. The final `Human review sentence` means not a fixed cause, but a comparison sentence that a person should review.

If we place the recent range and the baseline side by side as in the table below, the difference becomes more visible.

| process_type | recent_mid_flow | baseline_mid_flow | diff | recent_count |
| --- | --- | --- | --- | --- |
| type-A | 2.10 | 2.45 | -0.35 | 20 |
| type-B | 2.30 | 2.28 | 0.02 | 18 |

If we look only at `2.10` or `2.30` by themselves, it is hard to say much. But when they are placed next to a baseline under the same conditions, sentences such as `type-A became lower than usual` and `type-B is almost the same` become possible.

What should be read first here is `diff`. But even that difference value can be calculated only when a baseline exists. So the baseline is not extra information added after comparison. It is the premise needed from the beginning in order to build comparison columns.

If we read this comparison table in the order below, it becomes clearer that the baseline is the premise of the comparison columns.

1. First check what is difficult to say when we look at the recent value and the baseline value separately.
2. Then check what comparison sentence becomes possible the moment `diff` appears.
3. At the same time, write down that this table alone still cannot fix the cause.

Once we go through this order, it becomes clearer that the baseline is not just a reference number, but a structure required to make comparable columns and comparison sentences.

The situations where a baseline is especially needed can be summarized more briefly like this.

| What we want to inspect now | Why a baseline is needed |
| --- | --- |
| Has the recent average changed from usual? | Because the current value alone cannot tell us the direction of change |
| Has recent variability grown? | Because we need to distinguish whether fluctuation was always large or only recently became larger |
| Did only one certain process type change? | Because comparing inside the same condition group reduces misreading |

The key point of this table is that the baseline is not `an extra reference number`, but `the premise of comparison needed to speak about whether change exists`.

So this section is more accurately read not as an introduction to the word baseline, but as the problem of `what reference window should be placed alongside the current state in order to read it`. A baseline is not an extra number. It is a reference window that turns the current structure from a standalone value into `a comparable state`.

## Sources and Further Reading

- U.S. Bureau of Labor Statistics, `Base period`. Because it explains a base period as a reference for comparing other times, it supports the central point of this section that change becomes visible only when the current range and the baseline range are placed together. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute, `baseline`. Because it explains baseline as the standard against which later change is compared after an initial measurement is set, it provides a general basis for reading baseline in Part 3 as `a state-comparison reference`. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
