# P3-3.2 How Should a Dataset Be Redesigned to Match the Question

> Section ID: `P3-3.2`
> Version: `v2026.07.25`

To redesign a dataset means not using an existing file as it is, but reselecting the [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) unit and [column](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-column) structure required by the question. In other words, it means deciding again what should count as one [row](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-row), `which columns should remain`, and `what should be compared against what`. That is also why an action-level table, a [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure), and a candidate prediction-problem table differ from one another: the difference is born inside this redesign.

Even the same source time series can be rebuilt into different [datasets](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-dataset). For example, if we have [source data](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data) from automatically executed actions, the following three tables are all possible, but they do different jobs.

| Type of table | What one row means | Main purpose |
| --- | --- | --- |
| Measurement table | one time-point record during an action | preserving source data and detailed tracing |
| Action-level table | a summary of one automatically executed action | making comparable samples |
| Recent-segment comparison table | the recent state and the baseline obtained by grouping multiple actions | interpreting change and setting review priority |

None of these three tables is automatically `the correct dataset`. The suitable table changes depending on what we are trying to solve. If we want to compare the structure of one action, we need an action-level table. If we want to see whether the recent state differs from the usual state, we need a recent-segment comparison table. So what matters in this section is not memorizing the definition of dataset one more time, but fixing that when the question changes, the table structure must be redesigned along with it.

The place where readers often get stuck here is, `I understand the table types, but which table should I choose for my current question?` So when the question and the table structure are matched directly, the selection criterion becomes much clearer.

| The question we are trying to answer now | The table that should be built first | Why |
| --- | --- | --- |
| Was this one action more unstable than the others? | action-level table | Because the comparison target is `one action`, so time-point logs have to be grouped into one case first |
| Do the most recent 20 cases show a different pattern from the usual 200? | recent-segment comparison table | Because the question itself asks about the difference between `groups of actions`, so aggregate and baseline-comparison columns are needed |
| If an anomaly is visible, at what time point did the cause begin? | measurement table + action-level table | Because we first have to select the anomalous case through the action-level table and then go back down to the raw time-point logs to inspect the detailed cause |
| Can an input table for later supervised learning be built? | action-level feature table or candidate prediction-problem table | Because input columns and target-label candidates must be separated on top of the same sample unit |

In other words, the table that is built first changes depending on whether `the question asks about one action`, `asks about changes in the recent segment`, or `asks about a detailed time-point cause`. Dataset redesign feels difficult not mainly because many tables are made, but because it is easy to miss that `when the question changes, the reference table changes too`.

So when we say a dataset is being built, at least the following judgments are included.

- What is one sample?
- Which values stay as they are, and which values are summarized?
- Is a [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) column needed for comparison?
- Is the [output structure](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) a warning, a review candidate, or a prediction target candidate?

If someone says `there is already a dataset` without these judgments, in many cases they are still only holding source records. This is especially easy to miss with time-series data. When there are many rows and many columns, it looks like a rich dataset already exists. But if the analysis unit is still unfixed, that table still does not express the problem properly.

At this point, the question `but the table already exists, so why is it not a dataset?` naturally appears. Here we have to separate `a file exists` from `a comparable sample table exists`.

| What exists in hand now | What may still not exist |
| --- | --- |
| a source-record file | a sample table regrouped by one action |
| time-point rows and sensor values | [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) columns chosen for comparison |
| all recorded numbers | difference columns compared against a baseline |
| a long log table | an output structure readable directly as review candidates or learning candidates |

So the existence of a file does not mean the dataset is already complete. Only after we decide by what question the source records should be reread can we use the phrase `the dataset for this problem` more accurately.

One important point here is that only one dataset does not exist. Even with the same source data, the dataset for a comparison report, the dataset for review priority, and the dataset later passed into supervised learning may all differ. Unless we admit this difference, we cannot answer the question `why do we rebuild several tables from the same data?`

The example below shows which table becomes necessary first when the question changes over the same source data.

Problem situation: confirm that even with the same source data, the questions `compare one action`, `compare the recent state`, and `prepare later learning candidates` each require a different table.

Input: time-point logs under each `event_id`, plus a column indicating whether each action belongs to the recent segment

Expected output: it becomes visible that, from the same source table, an `action-level table`, a `comparison report table`, and a `learning-candidate table` are built differently according to purpose

Concept to check: a dataset is not the name of one file, but a table structure redesigned to match the question

Even with the same source time series, once the question changes, the draft table that needs to be built first also changes as follows. The earlier map of `question -> table to build first` is now expanded downward into `sample unit`, `columns to keep`, and `immediately readable output`.

| Question | Sample unit fixed first | Columns kept first | Output that becomes directly readable |
| --- | --- | --- | --- |
| Was one action more unstable than the others? | one action per `event_id` | `flow_mean`, `flow_max`, `duration` | action-level comparison table |
| Are the recent 20 cases different from the prior 200? | one recent bundle vs one baseline bundle | `recent_mean`, `baseline_mean`, `diff` | recent-segment comparison report |
| Can later learning candidates be created? | one action per `event_id` | `flow_mean`, `flow_max`, `target_candidate` | a table where input columns and result candidates are separated |

The key point is not that the source data changes three times, but that depending on which question is used to read the same records, `what one row means`, `which columns remain`, and `what output is needed immediately` all change. To compare one action, we first need a table grouped by `event_id`. To compare recent segments, a structure that places the `recent bundle` and the `baseline bundle` side by side is needed earlier than an action-level table. By contrast, once later learning candidates are being considered, a table that separates input columns from result candidates matters more than a comparison-report sentence.

## A Small Diagram

The fact that a changed question also changes the first table to build can be compressed into the redesign flow below.

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-2-mermaid-01-en.mmd"
```

So saying `we rebuild the table several times` does not mean repeating the same work. It means separating the structures required when the question changes. The action-level feature table is the result of summarizing time-point logs so that one action can be compared as one sample. The comparison-report table adds comparison columns so that the recent state and the baseline difference can be read directly. The candidate prediction-problem table goes one step further by separating input columns from candidate target labels.

When rebuilding a table, the current design stage can first be fixed in the following order.

1. Write down what one row means in the source table.
2. Write down what counts as the one sample we are trying to compare.
3. Decide only 2 to 3 summary columns to keep for that one sample.
4. Write down whether the table is for a comparison report or for preparing a prediction problem.

Once these four lines are written, it becomes clear whether what we are doing now is checking storage structure or designing a dataset.

This section can be reread not as a procedure for remaking files, but as the problem of what criteria should guide `question-aligned table redesign`.

So it is more accurate to read dataset redesign not as `making many tables`, but as realigning the meaning of rows and the role of columns whenever the question changes.

## Sources and Further Reading

- W3C, `PROV-Overview`. Because the provenance framework explains that it should support representing processing steps, derivation, and versioning, it provides a general basis for keeping separate records of what transformations produced which tables for which purposes, even from the same source data. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example presupposes a structure of features and label, it strengthens the explanation that when the meaning of one row and the role of the result column change with the question, the table must also be redesigned. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it explains that a base period is a reference used for comparison with another time period, it supports the claim that table structure can change depending on what is chosen as the reference bundle, as in a recent-segment comparison table. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
