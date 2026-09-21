# Part 3. Data Modeling

> Section ID: `P3-index`
> Version: `v2026.09.20`

Part 2 rebuilt the foundations for reading mathematics, Python, arrays, tables, and graphs. Part 3 uses those tools to learn **how to understand and handle data before choosing a model**. When we say “give data to AI,” we first ask what was recorded, what was grouped into one case, and which information was retained. These choices explain what a model sees and what it is meant to predict.

In this book, `data modeling` means organizing records into samples, tables, features, and targets for a question. A sample is one case considered in analysis or learning; features are input information describing that case. This educational scope is broader than database storage design, but does not replace the definition of data science as a whole. Part 3 also covers meaning, quality, representation, and interpretation of comparisons.

## What Can the Same Sensor Records Tell Us?

Imagine equipment repeatedly performing an operation that lets water flow. Each run records sensor flow readings, measurement times, and equipment settings. If flow appears to fall near the end of recent records, check the following before calling it a failure.

| Question | What to inspect in this example |
| --- | --- |
| What was recorded? | Is it water volume or volume per unit time? When and under which settings was it measured? |
| How is it grouped? | Group records from start to finish into one case to inspect change within an operation. |
| What is retained? | To inspect the late decline, retain time order and changes in that interval. Check what disappears when an entire operation becomes one number. |
| What can be known? | Compare with past operations using the same settings and measurement method. Distinguish an observed difference from an explanation of failure causes. |

If the final sensor records are missing, judging the decline is difficult. If equipment settings differ between past and recent runs, examine that difference too. This is why data quality and observation conditions matter. Comparing observations consistently requires numbers, so later sections select and calculate **metrics** suited to the question. A metric quantifies a particular aspect of a phenomenon; beyond its name, explain what was counted and how.

Predicting later failures also requires outcomes for learning. For example, define the outcome as “Did a failure occur within seven days after the operation, and was it subsequently confirmed?” A **label** is the outcome supplied as the answer during learning. A record of human review and a confirmed failure record differ, so choosing between them changes the learning target.

This is a fictional teaching example, not an established failure cause or operating criterion. [P3-1.1](chapter-01/section-01.en.md) examines concrete metrics and calculations alongside the records.

## Six Connected Questions for Working with Data

Part 3's nine chapters connect the following questions. Follow how earlier choices enable later inputs and interpretations.

| Question | What you will learn | Chapters |
| --- | --- | --- |
| What part of reality was recorded? | Read record meanings, measurement conditions, timing, and units. | Chapters 1–3 |
| What counts as one case? | Choose samples and organize rows, columns, and time windows around the question. | Chapters 2–5 |
| How far can the records be trusted and used? | Check missing values, duplicate records, insufficient conditions, and measurement differences. | Chapters 4–6 |
| Which information is kept or lost? | Compare what summaries and time-ordered representations preserve. | Chapters 5–6 |
| What is compared, and how far can it be interpreted? | Choose metrics and references; distinguish observations from causal judgments. | Chapters 7–8 |
| What will AI see and predict? | Separate inputs, targets, labels, availability times, and evaluation subjects. | Chapter 9 |

This is the book's learning sequence, not a mandatory one-pass procedure for every analysis. Missing records discovered during comparison may require revisiting the question or sample construction.

## Raw Records Are Datasets; Summarization Is a Choice

Raw logs are datasets too. Having a collection of data differs from being ready to use it for the current question. Even time-ordered sensor records need checks of their operation and interval, missingness, and links to outcomes.

The book follows an example that turns sensor records into per-operation summaries and compares operations against a historical reference, or baseline. We inspect how a row's meaning changes and how to trace it back to original records. A summary table is one representation for explaining comparisons.

Depending on the question and model, inputs can also be raw time series, images, or documents. Not everything must become manually calculated summaries. Ask what one image contains, or whether a document or a portion of it is one case. Chapter 6 examines the relationship between human-designed features and representations learned by models.

## Inputs and Targets to Hand Off to Part 4

Part 3 reads and organizes data, then checks what can be said from it. The result may remain a human-readable comparison report or a list of cases to review first. If prediction is needed, specify the input information and the outcome to predict.

Part 4 builds on these inputs and targets to study machine learning and evaluation. Part 3 separates information known at prediction time from outcomes confirmed later, and specifies the subjects on which performance should be assessed. Detailed learning algorithms and evaluation-data splitting continue in Part 4.

## Checklist

- Can you explain what is recorded, grouped into a case, and retained in the sensor example?
- Can you state what metrics compare, which judgment limits quality checks reveal, and which learning target labels support?
- Can you distinguish raw records being a dataset from readiness for the current question?
- Can you suggest a boundary or piece of context to check when applying the same questions to an image or document?

## Sources and References

- [National Academies, Data Science for Undergraduates: Opportunities and Options (2018)](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" }. Background for connecting collection, preparation, representation, modeling and interpretation; the six-question arrangement is editorial. / 2026-07-20
- [Google, Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Definitions of examples, features and labels. / 2026-09-19
- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }. Provenance and derivation for tracing transformed tables to source records. / 2026-09-19
- [Fayyad, Piatetsky-Shapiro and Smyth, Knowledge Discovery and Data Mining: Towards a Unifying Framework (1996)](https://www.microsoft.com/en-us/research/publication/knowledge-discovery-and-data-mining-towards-a-unifying-framework/){: target="_blank" rel="noopener noreferrer" }. Background on data preparation and subsequent discovery. / 2026-07-20
- [U.S. Bureau of Labor Statistics, Consumer Price Index: Concepts](https://www.bls.gov/opub/hom/cpi/concepts.htm){: target="_blank" rel="noopener noreferrer" }. Reference for comparing current values against a defined base period. / 2026-07-20
