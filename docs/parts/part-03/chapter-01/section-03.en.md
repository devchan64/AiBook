# P3-1.3 How Should a Data Question Be Written So the Problem Structure Appears Before the Model

> Section ID: `P3-1.3`
> Version: `v2026.09.20`

“Is the equipment abnormal?” does not identify which records to seek. It may mean a lower flow level or a rapid decline near the end of an operation. Making a [data question](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) concrete turns a broad concern into a sentence stating **what to check, for which subject, and when**.

[P3-1.2](section-02.en.md) stopped calculation and revisited earlier decisions when the required interval was missing. Now put the subject, time, required records, and desired output into the question itself to distinguish what available data can answer. Not every question needs a historical baseline: comparing with usual behavior needs comparable conditions, while classifying a document needs categories and their criteria.

## Turn “Abnormal” into an Observable Difference

Assume the same fictional equipment runs from 0 to 2 seconds. Instead of attaching every condition at once, fill in what is missing one step at a time.

| Revision of the question | What becomes explicit | What remains to decide |
| --- | --- | --- |
| Is the equipment abnormal? | Interest in equipment condition | Which operation and which difference? |
| Did flow decline near the end of one completed operation? | One operation and a late decline | Which interval is the end? |
| After completion, can we check the flow slope from 1 to 2 seconds after operation start? | Assessment time and calculation interval | Is the question about decline itself or deviation from usual behavior? |
| After completion, can we compare the 1–2-second decline with past operations under matching conditions and flag review? | Subject, timing, interval, comparison conditions, and output form | Are matching historical records and a review rule actually available? |

In the third question, “after completion” is when the answer is assessed; “1–2 seconds” is the interval read relative to operation start. Separate them to identify when information is used and which records it covers.

A-101 in [P3-1.1](section-01.en.md) had a 1–2-second slope of −1.2 L/min/s, steeper than the assumed baseline of 0.0 L/min/s. But that baseline and review threshold were illustrative assumptions. Without matching historical records, state “decline observed; difference from usual behavior not yet established.” A concrete question does not create the data needed to answer it.

We say “declined faster in a specified interval,” not “fluctuated more,” to identify the difference being observed. Dispersion around a mean calls for a separate question comparing standard deviations. Choose the metric for the question.

## Questions About Current Differences and Future Outcomes

Comparing a current state and predicting later failure require different outcome records, even when they begin with the same operations. Compare these questions.

| Element | Observation and comparison | Future prediction |
| --- | --- | --- |
| Question | Did 1–2-second flow in a completed operation fall faster than usual under matching conditions? | From records available at completion, can we predict failure of that equipment within the next seven days? |
| One case and assessment time | One operation, inspected after completion | One completed operation as the reference point, with prediction at completion |
| Required inputs | Interval times and flows, operating conditions, comparison history | Sensor values and operating conditions available by completion |
| Output | Slope difference, rule-based review decision, or insufficient information | Prediction of failure during the next seven days |
| Additional evidence to check the answer | Matching baseline and explicit review rule | Failure definition, equipment ID, later failure times, and observation-completion records |

Collecting operations for people to inspect first produces a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure). Inclusion is not an answer about future failure. Learning and evaluating prediction require linking actual subsequent outcomes.

The previous example's six sensor rows allow slope calculation but not knowledge of the following seven days. If follow-up covers only two days after completion, the remaining five are still unknown. Keep observation incomplete rather than fill in no failure. Chapter 9 develops label and timing boundaries; here we mark records required by the question but currently absent.

## Making the Question Concrete with Samples, Comparisons, and Outputs {#a-small-diagram}

Changing the question changes the meaning of a result row and its required columns. The same source records can produce these different outputs.

| What we want to know | One result-table row | Information to retain |
| --- | --- | --- |
| Is this operation's late decline unusual? | One operation | Operation ID, conditions, interval, slope, baseline difference |
| Do mean late slopes differ between the latest 20 and previous 200 operations? | One comparison of two operation groups | Each group's period, conditions, valid count, interval definition, means and difference |
| Can daily operation be summarized with specified items? | One day | Aggregation start and end, operation count, missing count, chosen summaries |
| Can failure within seven days of completion be learned? | One case anchored at operation completion | Historical inputs, equipment ID, later outcome, observation completeness |

The counts 20 and 200 are illustrative group sizes, not guarantees of sufficient data. Check for shared operations between groups and matching conditions and record coverage.

The diagram summarizes question-to-table relationships. Choosing a table form does not establish that the necessary records actually exist.

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-3-mermaid-01-en.mmd"
```

Rewrite “Is the equipment abnormal?” as a per-operation comparison, then as “Summarize the day's overall operation at the end of each day.” A row in the first table is an operation; in the second, a day. If operating conditions vary within a day, decide whether to separate or combine them. Write the changed row unit and columns, not just revised wording.

Comparing summarized versus raw time-series inputs for the same operation instead holds the operation ID, question, and observation interval fixed while changing representation. That differs from changing a per-operation question into a daily question.

## Apply the Same Questions to One Document

“Classify documents with AI” can become the following fictional question.

> At receipt of a customer inquiry, can we read one document's title and body, assign `delivery`, `payment`, or `other` according to its main request, and route it to the responsible review list?

The subject is one document, the time is receipt, inputs are title and body, and output is one of three categories. No historical flow mean or slope baseline is needed. Instead, specify how to classify a document containing both delivery and payment requests. A title-only record lacks the body this question requires; a reply added later by an agent is not an input available at receipt.

Revise this document example yourself. If multiple categories are allowed per document, what changes in the output? It must hold multiple categories instead of one, and labeling criteria must change. More important than having a baseline is aligning the subject, timing, inputs, and outcomes with the current question.

## Checklist

- Have you replaced “abnormal” or “fluctuating” with a measurable difference and stated the subject, time, interval, and output form?
- Can you separate what is knowable from what remains unknown without matching historical records?
- Have you separated records needed for current comparison and seven-day failure prediction, marking absent information?
- When changing per-operation to daily questions, did you change the row unit and required columns too?
- Have you specified information available at document receipt and classification criteria, identifying unresolved choices?

## Sources and References

- [Google, Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Terminology for inputs, labels and leakage; the question-writing format is this book's construction. / 2026-07-20
- [U.S. Bureau of Labor Statistics, Base period](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" }. Reference periods support comparisons with usual behavior; not every data question needs a historical baseline. / 2026-07-20
- [Fayyad, Piatetsky-Shapiro and Smyth, From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }. Background connecting problem definition, data preparation and subsequent structures. / 2026-07-20
- [Google, Framing an ML problem](https://developers.google.com/machine-learning/problem-framing/ml-framing){: target="_blank" rel="noopener noreferrer" }. Distinguishes desired outcomes and model outputs, classes and proxy labels. The sensor and document questions are fictional examples. / 2026-09-19
