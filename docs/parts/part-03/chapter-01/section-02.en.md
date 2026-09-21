# P3-1.2 In What Sequence Does Data Modeling Proceed

> Section ID: `P3-1.2`
> Version: `v2026.09.20`

[P3-1.1](section-01.en.md) grouped flow readings over time into one row per operation and retained metrics and review results suited to the question. Building that table involved connected decisions: the question determines which interval is needed, while the sample unit determines what means and slopes describe. Here we examine the order of these decisions and where to return when the records differ from expectations.

## What to Retain from the Question to the Review Result

Reuse A-101 from the previous section. Flow at 0, 1, and 2 seconds was 24.8, 25.1, and 23.9 L/min. Seeing a decline in the final interval leads to “Did flow fall faster in the final interval than in usual operations under the same conditions?” This specifies an observable difference without first assuming failure.

Six decisions turn that question into one result row. The formulas are the same as in the previous section.

| Decision | What to check for A-101 | Small output to retain |
| --- | --- | --- |
| 1. Define the question | Are we comparing overall level or late decline with usual operations? | Compare final-interval slopes under the same conditions |
| 2. Define the sample | Which records form one case? | One operation, ID `A-101` |
| 3. Group and check records | Do times and flows correspond, with the required interval present? | Per-operation records at 0, 1, and 2 seconds |
| 4. Choose features and baseline | Which interval is calculated, how, and against what reference? | 1–2-second slope −1.2 L/min/s, assumed baseline 0.0 L/min/s, difference −1.2 L/min/s |
| 5. Define the output structure | How will a person receive the comparison? | Rule: `review` if the difference is below −0.5 L/min/s, and its result |
| 6. State interpretation limits | What does the result support? | Steeper decline than the assumed reference warrants review; failure cause remains unknown |

The [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) is the form a person can read next: identifiers, comparison values, and review results. `review` is a rule-based flag, distinct from a learning label assigned after confirming an actual failure. Baseline 0.0 and threshold −0.5 remain illustrative assumptions, not validated equipment limits.

This question selects the final-interval slope. Being able to calculate means and standard deviations does not require including them in every result table. Add questions and calculation scopes if overall flow level or spread also needs examination.

The diagram summarizes connections in this per-operation summary example. These six items organize the book's explanation, rather than prescribing identical summaries and baselines for all data.

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-2-mermaid-01-en.mmd"
```

## Which Decision Should We Revisit If the Last Record Is Missing?

Unlike the previous section, suppose the supplied A-101 data lacks the 2-second record. Only 24.8 at 0 seconds and 25.1 L/min at 1 second remain. They give `(25.1−24.8)/(1−0) = +0.3 L/min/s`, but this is the **0–1-second slope**. It does not answer the original question about **the 1–2-second decline**.

Always taking the last two available rows changes the interval while retaining the name `late_drop_rate`. Missing required information becomes a supposed upward result. Return to grouping and checking records before completing the calculation.

| What rechecking reveals | Decision to revisit and action | Current result |
| --- | --- | --- |
| The 2-second value exists in source logs but was omitted during extraction | Correct the extraction range, restore the value, and calculate the same interval | Produce the comparison using restored data |
| The sensor did not record the 2-second value | Check collection status and mark the 1–2-second slope uncomputable | Leave slope and baseline difference uncomputed; report insufficient information |
| The purpose is deliberately changed to checking the initial rise | Change the question and interval to 0–1 seconds and define a matching baseline | Treat it as a new question, not a late-decline result |

“Insufficient information” is not a third failure grade. It means missing comparison records prevent applying the existing review rule. Filling an empty slope with 0 or `no_flag` misrepresents something unobserved as no change.

Even complete values can require revisiting comparison conditions. Suppose A-101 was configured to lower flow before completion, while baseline operations were configured to maintain it. First seek historical runs with matching settings and redefine the reference. If none exist, report that the current baseline cannot support a same-condition comparison. Discovering a settings difference alone does not prove the decline's cause.

## Why Exploration Changes Earlier Decisions

Exploring and organizing records are not one-time activities after the table is finished. Here, a missing value discovered during slope calculation sends us back to record coverage; inspecting conditions changes the baseline choice. Changing the question also changes the required interval and output meaning.

The initial expectation “let us inspect the late decline” proposes a question to check. Actual records help decide whether to keep it, change it, or state that the data cannot answer it. Expectations are not guaranteed to be right or reduce the number of work steps.

Recording decisions does not mean they can never change. It distinguishes restoring missing records under the same question from changing intervals to answer a different question. Retain operation IDs, intervals, calculation rules, baseline conditions, review rules, and unresolved items to trace what needs rechecking.

## Checklist

- For A-101, write one line each for question → sample → grouped records → features and baseline → output → interpretation.
- Can you explain why +0.3 for 0–1 seconds cannot answer the original question when the 2-second value is absent?
- What should be checked when extraction omitted a value versus when the sensor never recorded it?
- If ending settings differ, which decision must be revisited? What should the result say if matching records are unavailable?
- If the question changes to an initial rise, what must change in both the interval and baseline?

The second question separates being able to calculate a number from answering the intended question: a changed interval changes meaning. The last question requires redefining both the interval and its matching baseline. Keep “insufficient information” when required evidence is unavailable.

## Sources and References

- [Google, Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Sample, input and label terminology; not a prescription of these six steps. / 2026-07-20
- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. Identifying objects and derivations supports tracing samples and derived outputs. / 2026-07-20
- [Fayyad, Piatetsky-Shapiro and Smyth, From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }. Background linking selection, preprocessing, transformation and interpretation. / 2026-07-20
- [NIST/SEMATECH, What is EDA?](https://www.itl.nist.gov/div898/handbook/eda/section1/eda11.htm){: target="_blank" rel="noopener noreferrer" }. Exploring structure, assumptions and unexpected information. The missing-data and settings scenes are fictional, not evidence of fewer work steps. / 2026-09-19
