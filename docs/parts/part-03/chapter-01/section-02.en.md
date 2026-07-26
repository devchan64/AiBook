# P3-1.2 In What Sequence Does Data Modeling Proceed

> Section ID: `P3-1.2`
> Version: `v2026.07.25`

Once we understand what data modeling is trying to achieve, the next question follows immediately: in what sequence should the work actually proceed? Features cannot be built before the sample unit is fixed, and without a comparison reference even the [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) becomes unstable. So data modeling is best read as an order that fixes the structures needed later, one by one, from the front.

In practice, as soon as source data arrives, it is easy to want to choose the learning-problem frame first, with familiar labels such as `prediction problem`, `classification problem`, or `anomaly-detection problem`. But this order often creates trouble, because `what one row means`, `the sample unit`, `the comparison reference`, and `the output structure` have not yet been fixed.

General machine-learning work is often explained as a broad flow of problem definition, data understanding and preparation, modeling, and evaluation. Part 3 focuses on the front part of that larger flow, especially `the front-end stage that builds a problem structure before AI learning begins`. So here we examine the items that should be checked together at the front by grouping them into the following six.

1. Decide the problem question.
2. Decide the sample unit.
3. Rebuild the raw logs into a comparable table.
4. Design features and baselines.
5. Separate the output structure from candidate target labels.
6. Decide the interpretation boundary and conservative phrasing.

What has to be fixed first here is how `samples, tables, features, comparison, and output structure` fit together in sequence. Source-data collection, full exploratory data analysis, formal statistical testing, model training, and evaluation experiments each appear again later, but even those explanations stay less scattered when this front-end structure is already standing.

In official documentation, these six items are usually explained not as one fixed procedure name, but as separate concepts such as `task`, `example`, `feature engineering`, `label/target`, `preprocessing`, and `classification threshold`. In Part 3, we regroup those individual concepts into `a flow for reading problem structure before learning`.

Reduced to one line, the connection among these six items is as follows.

```mermaid
--8<-- "assets/part-03/chapter-01/p3-1-2-mermaid-01-en.mmd"
```

If this grouping still feels abstract, it becomes easier to understand when compared with a `wrong starting order` that people often follow in real work.

| Starting approach | Why it seems plausible at first | The problem that soon appears |
| --- | --- | --- |
| Choose the learning-problem frame before the problem structure | Familiar terms such as prediction, classification, and anomaly detection come to mind first | Because one row has not yet been fixed as one time point or one action, the input `X` itself remains unstable |
| Rush to extract features first | It feels as if progress is being made quickly when averages, maxima, and standard deviations are produced | Without a sample unit, it becomes ambiguous whether the value describes `the whole action` or only `part of a segment` |
| Set a threshold first | In practice, people often want a warning criterion quickly | Without a baseline, it is impossible to distinguish `is this value large` from `is this different from usual` |
| Fix the question and sample first | It looks slower at first | Later tables, features, baselines, and output structures all sit on the same criteria, so instability is reduced |

Part 3 puts this flow first because later explanations often assume these earlier judgments. The most common failure is `choosing the learning-problem frame first and then trying to force the sample unit into it afterward`. In that case, the table often has to be rebuilt, the features re-extracted, and even the output structure redefined. It is usually less unstable to organize the judgment criteria up front.

The role of each stage can be read as follows.

| Stage | Core question | Representative output |
| --- | --- | --- |
| Decide the problem question | What do we want to know? | a comparison question or a prediction question |
| Decide the sample unit | What should count as one case? | action unit, segment unit, entity unit |
| Rebuild the table | How should the raw logs be represented again? | summary table, aggregate table |
| Design features and baselines | Which values should remain, and what should they be compared against? | feature columns, baseline-comparison columns |
| Separate the output structure | How should human review and prediction targets be separated? | warning, review candidate, target-label candidate |
| Decide the interpretation boundary | How far should we speak, and where should we stop? | conservative phrasing, `needs review` markings |

These items must stay grouped because later explanations often assume earlier judgments. If the sample unit is not fixed, the features also drift. If the features drift, baseline comparison drifts as well. If the comparison structure drifts, it becomes hard even to separate `needs review` from a `target label`.

A small example makes this clearer.

- Question: Has recent behavior become more unstable than usual?
- Sample: one execution of the action
- Table: an action-level summary table of mean, slope, and variability
- Features: `mid_flow_mean`, `late_drop_rate`, `flow_std`
- Baseline: compare the most recent 20 cases with the prior 200
- Output: `needs review` or `normal range`

In this example, no specific learning-problem name has appeared yet. Even so, almost all of the important data-modeling decisions are already present. That is because what counts as one case, which values remain, what gets compared, and what result will be emitted have already been decided.

If we map the same example back onto the six stages once more, it becomes even clearer what each stage really decides.

| Stage | The actual decision made in this example |
| --- | --- |
| Decide the problem question | Decide that we first want to know whether recent behavior has become shakier than usual |
| Decide the sample unit | Treat one full action, rather than one sensor time point, as one row |
| Rebuild the table | Turn time-step logs into an action-level table of mean, slope, and variability |
| Design features and baselines | Create `mid_flow_mean`, `late_drop_rate`, `flow_std`, and columns that compare against the usual range |
| Separate the output structure | Separate review-oriented results such as `review` and `normal` from later candidate target labels |
| Decide the interpretation boundary | Use conservative wording such as `needs review` instead of `confirmed anomaly` |

The key to reading this table is that if an earlier judgment is missing, the later judgments are also likely to become vague together. For example, if features are built before the sample unit is fixed, it becomes unclear whether the feature describes `variation at one time point` or `variation across the whole action`.

These six items are not a list that replaces later explanations. They are an order that keeps later explanations from drifting. Because if one stage is empty the next stage also tends to become ambiguous, Part 3 is safer when it first fixes the interlocking order of `question -> sample -> table -> feature and baseline -> output structure -> interpretation boundary`. For the same reason, Part 3 should be read less as `studying data science` and more as `designing a learnable data problem`. Once that viewpoint is in place, the sample design, summary tables, feature design, and baseline comparison that come later start to read not as scattered techniques, but as one procedure for setting up a problem.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`, `feature engineering`, `label`, `label leakage`. Because it explains that the roles of example, feature, and label each have to be fixed separately, it supports the core point of this section that question, sample, table, feature, and output structure should be read as an ordered chain. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because it explains that identifying an object and preserving derivation should both remain visible, it strengthens the higher-level frame that the sample unit, derived tables, and result structure should be explainable in sequence. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, `From Data Mining to Knowledge Discovery in Databases`. Because it explains a broader flow in which data selection, preprocessing, transformation, and interpretation continue together, it provides the general background that Part 3 focuses on `the pre-learning stage that fixes problem structure in order`. [https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
