# P3-8.2 How Far Should You Describe a Change Signal, and Where Should You Stop on Cause

> Section ID: `P3-8.2`
> Version: `v2026.07.25`

Once you have a [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), you can read the difference between a recent window and the usual state. But it is still very risky to think, `if a difference appears, the cause must be obvious too`. A visible change signal and a confirmed cause are completely different stages. After adjusting interpretation strength, you next need to define the [interpretation boundary](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-interpretation-boundary) more clearly.

Another perspective that needs to be recovered in this chapter is `visual interpretation`. Overinterpretation can happen when comparison tables are read numerically, but the risk becomes even larger in graphs that draw the eye quickly, such as line charts, bar charts, and distribution plots. A split line or a taller bar can help you spot a change signal quickly, but that alone does not mean the cause is confirmed or that a strong conclusion is justified. The first boundary to hold here is that `a difference is visible` and `the cause has been confirmed` should not be merged into the same sentence.

Suppose the late-stage drop rate became larger than usual in the most recent 20 cases. That may be an important change signal. But the table alone still cannot tell you whether the reason is a sensor problem, a change in input conditions, a shift in control settings, or a temporary environmental factor. What the comparison table shows is that `a structure different from the usual state exists`, not that a finished diagnosis of `why` already exists.

The same judgment applies when reading a figure. A recent line may sit below the baseline line, or a recent box plot may look wider than the usual range. Such figures help you catch `what looks different` quickly, but the figure alone cannot confirm whether the difference comes from too few samples, from a few outliers, or from a sustained structural shift.

| What appears first in the figure | Risky sentence if spoken from the figure alone | Safer interpretation |
| --- | --- | --- |
| The recent line is below the baseline | The state has definitely worsened | The recent window appears lower than the baseline, so further checking is needed |
| The recent bar is larger | The cause is already clear | A difference appears in the comparison value, so it should be reviewed without cause confirmation |
| The box-plot range is wider | The system has become unstable | The recent spread looks larger, so repeatability and sample size should be checked together |

| Expression | Meaning | Can you say it at this stage? |
| --- | --- | --- |
| Change signal | A structure different from the usual state has been observed | Yes |
| Warning candidate | It is worth human review | Yes |
| Review needed | Additional checking is needed | Yes |
| Cause confirmed | The reason has already been determined | Usually not yet |

As this table shows, the comparison structure directly supports statements mostly up to the level of `change signal`, `warning candidate`, and `review needed`. By contrast, `cause confirmed` requires more evidence. You may need raw log rechecks, operational context, extra sensors, downstream outcomes, and human judgment.

So saying that [comparison tables](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-table) are powerful is not the same as saying they can say everything on their own. They are strong at showing `what looks different from the usual state`, but they are not standalone tools for deciding `why`. Keeping this boundary clear prevents warnings and diagnoses, [review queues](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-review-queue) and automatic classification, from being mixed together.

Statistical conservatism matters exactly here. If the sample size is small or repeatability is weak, the wording should stay softer even when a difference is visible. The default stance is therefore `a change is observed, but the cause is not yet confirmed`.

This is not needed because AI is weak. It is needed because the structure of the problem is originally like this. Comparison tables are strong at showing `what changed`, but often do not provide enough basis to explain `why it changed` on their own. At the modeling stage, that is why it can be more honest to design the [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) around `warning candidate`, `review needed`, and `comparison report` rather than `automatic diagnosis`.

This boundary matters especially when reading correlation. Even if two values move together, you cannot immediately say that one caused the other. For example, if a certain input condition often appears together with late-stage decline, hidden operating conditions, seasonality, or changes in measurement procedure may still lie between them. In Part 3, it is therefore important to build the habit of not putting `moved together` and `is the cause` into the same sentence.

This becomes even more sensitive in areas such as financial modeling, where the cost of misinterpretation is high. Values such as price movement, trading volume, risk score, and delinquency probability can look highly correlated on the surface, but linking them directly to action can lead to losses or unfair decisions. At the Part 3 stage, it is safer to separate `prediction score` from `actual decision`, and to talk about cause confirmation or automatic action only when stronger evidence exists.

Visualization is especially double-edged here. A well-made chart can show more structure than a single average, but it can also make a visible pattern feel like a larger signal than it really is. A figure is therefore strong as a tool for `finding whether a difference exists`, but it should not be used immediately as a tool for `deciding whether the cause is confirmed`.

Compare the two sentences below.

| Expression | Why it is safer or riskier |
| --- | --- |
| The recent window shows a larger late-stage drop than the baseline | It reports the comparison result |
| The recent window shows a larger late-stage drop because of sensor abnormality | It has already fixed the cause |

Operational sentences are usually built in the following order.

1. State the comparison result first.
2. Adjust the wording strength to the sample size and repeatability.
3. Attach the next action a person should take.
4. Mention cause confirmation only when separate evidence exists.

For example, a sentence like `The recent window shows a larger late-stage drop than the baseline, and because the recent count is 6, the review priority is raised without cause confirmation` reflects both the comparison structure and the interpretation boundary. By contrast, a sentence like `A sensor abnormality occurred` brings in evidence that is not there yet. The warning needs to stay a signal that narrows what a person should look at first, not an automatic diagnosis.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-2-mermaid-01-en.mmd"
```

This diagram shows that a comparison result does not go directly to confirmed cause. You first describe the change signal, then you can move as far as the level of review needed, but a causal claim should move to the next stage only when separate evidence exists. The issue here is not the calculation itself but the interpretation boundary of `how far you speak` and `where you stop`.

This section is not about the stylistic preference to `write operational sentences conservatively`. It is about separating the levels of `observation`, `review`, and `causal claim`. Visual interpretation belongs to the same frame. A figure can make the `observed signal` easier to see, but it does not let you jump directly to the `cause claim` stage by itself.

Comparison tables support the observation and review stages well, but they do not automatically complete a causal claim.

The same boundary can be compressed like this.

| Sentence being spoken now | The closer level |
| --- | --- |
| A structure different from the usual state is visible | Change signal |
| It is worth a person looking first | Review candidate |
| Sensor abnormality is the cause | Cause confirmed |

The key point of this table is not to mix the level directly supported by the comparison structure with the level that still needs additional evidence.

## Sources and References

- W3C, `PROV-Overview`. It offers a provenance perspective that separates an observed result from the procedure and evidence through which that result was produced, which helps generalize this section's claim that comparison tables directly support change observation and review candidates, but not cause confirmation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. It explains signal structures that compare current performance with past performance and distinguishes control limits from specification limits, which reinforces this section's boundary that change signals and cause confirmation or functional judgment should not be treated as the same level. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
