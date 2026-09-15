# P3-7.2 How Should We Read a Comparison Table as a Human Review Sentence

> Section ID: `P3-7.2`
> Version: `v2026.09.15`

Once the [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) [comparison table](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) is built, many numbers start appearing at once. Columns such as recent average, baseline average, difference value, ratio difference, recent variability, and baseline variability can all appear together. At this point, people often look at the single most noticeable difference value and jump straight to a conclusion. But the order in which a comparison table is read matters. In Part 3, this table should be read not as an automatic diagnosis result table, but as `a table for building a human review sentence`.

When we read a comparison table, the important thing is not to recreate the baseline structure again, but to decide in what order an already built comparison structure should be read so that over-interpretation becomes less likely. Even the same difference value can be turned safely into a sentence for human review only when case count, baseline condition, variability, and pattern columns are read together.

The safe order for reading a comparison table is usually this. First check how many recent cases the recent range is built from. Then confirm what the comparison baseline actually is. After that, read the difference value together with the ratio difference instead of reading only the absolute value. Then inspect variability and pattern columns together with the average. Only then summarize it as an operational sentence. This order matters because a comparison table is not `a table showing only one number`. It is `a table that also contains the conditions of the comparison`. If we read the difference value first without checking recent-case count and baseline definition, we lose both how trustworthy the comparison is and what is being compared against what. In other words, a comparison table is a table whose comparison context should be read before its calculation result.

| Column | The question to ask when reading it first |
| --- | --- |
| Recent-range case count | Are there enough cases to say this number out loud? |
| Baseline period or condition | What exactly is being compared against what? |
| Average difference | Did the overall level change? |
| Variability difference | Did the size of the fluctuation also change? |
| Pattern or segment summary | Is there a structural difference that the average hides? |

If we turn this table into shorter operational questions, it becomes the following.

- How many cases support this difference?
- What is being compared against what right now?
- Did only the average change, or did fluctuation change too?
- If we turn the numerical difference into a human review sentence, how should it be written?

Once we go through these questions, we stop reading the comparison table as a bundle of numbers and start reading it as `a draft report sentence for state comparison`.

For example, suppose the recent-range average is lower than the baseline. We should not immediately say `performance got worse`. First we check whether the recent-range case count is large enough. Then we check whether variability also increased. Finally we inspect whether the pattern summary also shows repeated late-stage decline. Once we go through this order, even the same numerical difference can be read differently as `a one-off spike`, `a gradual change`, or `a repeated state shift`.

The following is a separate fictional example using 200 past actions under the same operating conditions as a baseline. Flow is in L/min, and we compare each action's late-segment mean. The decline count records how many actions met the defined within-action decline rule. This is a different observation set from the preceding section's table.

| Type | Recent count | Baseline mean | Recent mean | Baseline standard deviation | Recent standard deviation | Recent decline count |
| --- | --- | --- | --- | --- | --- | --- |
| type-A | 20 | 2.8 | 2.2 | 0.2 | 0.4 | 14 |
| type-B | 3 | 2.8 | 1.9 | 0.2 | 0.5 | 1 |

The table can be expressed in sentences as follows.

- Across the latest 20 type-A actions, the late-segment mean was 0.6 L/min below baseline.
- The type-A decline rule was met in 14/20 cases. Repetition is checked using that count and occurrence order, not the mean or standard deviation alone.
- Raise review priority while withholding a confirmed cause.

These sentences are safer because they do not use the comparison table immediately as if it were an automatic diagnosis result. The warning is closer not to an automatic confirmed diagnosis, but to a signal that narrows what a human should look at first. The reason we place the recent range and the baseline side by side is also exactly to narrow that review target more honestly.

The same reading order can also be shown directly through a simple diagram.

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-2-mermaid-01-en.mmd"
```

This diagram shows the order in which we should not jump directly to the most visible `diff`, but should first check sample count and baseline conditions. In other words, it is less about numerical examples themselves and more about fixing `in what order the comparison table should be read so that it can be safely translated into a human review sentence`.

Turning the two rows into operational statements makes the contrast clearer. Because 14 of the latest 20 `type-A` actions meet the decline rule, they can be treated as a candidate repeated change. A lower mean and higher variability alone cannot establish repetition. For `type-B`, the difference is larger but comes from only three recent actions, so a more qualified statement such as `few samples; further observation needed` is appropriate. That is why reading comparison tables and writing operational statements belong together here. Differences narrow possible explanations, but one comparison table does not automatically identify a cause.

This table defines not `which number catches the eye first`, but `what context must be checked first so that over-interpretation is reduced`.

This section can be read not as a trick for reading tables, but as the problem of `signal-to-review translation order`.

So the comparison table should be read not as an automatic conclusion table, but as an intermediate stage where a human checks the context first and then turns the signal into a sentence.

## Checklist

- Did you calculate type-A's mean difference and decline ratio and express them in a review statement?
- Did you describe type-B's sample count and repetition evidence separately from A's?

## Sources and Further Reading

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains both the structure of comparing current performance with past performance and the distinction that a comparison signal is not immediately the same as a confirmed functional judgment, it reinforces the point that a comparison table should be read not as a cause-confirmation table but as a review-signal table. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it provides a general framework of provenance information for keeping the context of the conditions and procedures through which data was produced, it can help generalize the explanation that a comparison table should be read with comparison context such as baseline condition and recent_count rather than diff alone. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
