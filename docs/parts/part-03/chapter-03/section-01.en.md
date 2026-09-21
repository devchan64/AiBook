# P3-3.1 Why Source Data Should Not Be Read as a Learning Problem Right Away

> Section ID: `P3-3.1`
> Version: `v2026.09.19`

A table of source data with time records does not establish the inputs and outcomes required by the current supervised-learning question. [Recorded source data](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data) is also a dataset. The question is not whether a dataset exists, but how to organize it as a [dataset candidate](/AiBook/en/reference/concept-glossary-alpha/d/#dataset) for a particular question.

Here, [problem-representation structure](/AiBook/en/reference/concept-glossary-alpha/t/#task-definition) means the design connecting samples, inputs, and targets. A classification or prediction idea may come first, but its name alone does not establish that the available data is ready.

Consider a situation where, for each automatically executed action, a control-parameter time series and a sensor time series are recorded. When seeing such a table, thoughts like the following arise first.

- Since there are sensor values, this could be turned into an anomaly-detection problem.
- Since action results differ slightly, it could be turned into a classification problem.
- If the time series is long, maybe it can be sent directly into a time-series prediction problem.

These thoughts are not themselves wrong. The problem is that the learning-problem frame appears first while `what counts as one case`, `what we are trying to predict`, and whether a [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) actually exists have not yet been fixed. In that state, the data problem has not been defined yet. The learning-problem frame has merely been imagined before the data itself.

But if source data is treated as already ready for the current supervised-learning question, important questions are skipped.

| The question that easily comes to mind first | The question that is actually needed first |
| --- | --- |
| Into what learning problem should this be read? | What should count as one [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample)? |
| What should the label be? | Does a stable label truly exist right now? |
| How should accuracy be improved? | Into what table must this be regrouped so comparison becomes possible? |

This difference is not merely about order. What is needed when source data is first seen is not choosing a learning problem, but `asking again what kind of table this really is`. Depending on whether what we are looking at is time-point measurement records, a summary of one action, or an aggregate of a recent segment, every later explanation of [feature](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature), [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), and [target](/AiBook/en/reference/concept-glossary-alpha/t/#target) changes.

For example, even after seeing only part of the source data below, the learning-problem frame may jump out too early.

| event_id | second | pressure | flow |
| --- | --- | --- | --- |
| A | 0 | 1.0 | 0.0 |
| A | 1 | 2.0 | 1.4 |
| A | 2 | 2.4 | 1.6 |

This table can quickly suggest phrases such as `classification problem`, `prediction problem`, or `time-series learning problem`. One row is a record at one time point. What remains undecided is whether to use that row as a sample or group rows by action, and which outcome to predict. Choosing a learning formulation immediately would therefore put the form of the problem ahead of the problem itself.

This example considers **classifying an action’s outcome with one action as one sample**. This requires linking input records to event-level outcome labels and checking how those labels were assigned. It does not mean that unlabeled datasets or analyses outside supervised learning are impossible.

| Separate check | Evidence to examine | Current CSV status |
| --- | --- | --- |
| Label column exists | Is `review_label` actually present? | Absent |
| Event-level linkage | Does each event have one outcome without missing or conflicting values? | Unknown because the column is absent |
| Label criteria | Who assigned the outcome, under which criteria and version? | Unknown because supporting evidence is absent |

Repeating one label throughout each event can pass the linkage check. Whether it came from a real inspection or an arbitrary rule, and whether the criteria were consistent across events, still requires separate checks.

## Decisions Between Source Records and a Learning Problem {#a-small-diagram}

It becomes clearer which questions stay empty when source data is escalated too early into a learning problem if the flow is reread as `source records -> empty questions -> sample/label candidate cleanup`.

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-1-mermaid-01-en.mmd"
```

## Check the Label Column, Linkage, and Criteria Separately

[p3_3_1_source_operation_log.csv](/AiBook/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv) is a fictional action log created for this book. Each row is a sensor record at a particular second within an action. There are nine actions, A–I, with four records each. `event_id` identifies the action and `second` gives the observation time. The file contains `flow` but no `review_label`.

Decide whether these records support action-outcome classification. For each situation, mark **label-column existence, event-level linkage, and label criteria** as `confirmed / condition not met / unknown`. Situations ③ and ④ describe hypothetical additions, not data in the original CSV.

| Situation | Available evidence |
| --- | --- |
| ① Select the original file’s `review_label` as the outcome | The column is absent |
| ② Select the original file’s `flow` as the action outcome | A’s values at seconds 0, 1, and 2 are 0.0, 1.4, and 1.6: time-point measurements |
| ③ Receive a separate outcome table | Each event links to one `pass` or `fail`, but no labeling document is provided |
| ④ Add labeling documentation and inspection history to ③ | For this exercise, assume the responsible person, criteria version, and application history are checked and the same criteria were used for every event |

In ①, the label-column condition is not met. Linkage and criteria are unknown because the necessary evidence is absent. In ②, column existence is confirmed, but the measurements are not event-level outcome labels for this question. Criteria remain unknown because no basis for converting sensor values into outcome categories has been provided.

In ③, column existence and event-level linkage are confirmed, but criteria remain unknown. The word `pass` alone does not tell us what was passed. In ④, the three checks in this exercise are confirmed. That does not establish the input scope or evaluation method, so it does not establish complete training readiness.

Now change the question to “predict flow at second 3 from records at seconds 0–2.” A’s inputs are its records at seconds 0, 1, and 2; its target is `flow=1.2` at second 3. Do not mix that flow value or later records into the inputs. The same `flow` column can supply targets once the question and timing are defined.

Finally, write a judgment note: “Event-level labels and their criteria are missing for the current classification question. Sensor records can be compared and explored; label evidence needs a separate check.” Record the original file’s version and the sources of any added outcome table and labeling document so the judgment can be revisited.

Being able to compare or summarize sensor records differs from having evidence to learn the intended outcome. Record the correspondence between samples, inputs, and targets for the current question, and leave unsupported items unknown.

## Checklist

- Can you distinguish source data being a dataset from readiness for the current supervised-learning question?
- Can you assess label-column existence, event-level linkage, and criteria separately in situations ①–④?
- Can you explain why one outcome per event does not establish its meaning?
- Can you separate input records from the target when predicting A’s flow at second 3?
- Did you write one sentence stating what can be explored now and what label evidence still needs checking?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label`, `labeled example`, `unlabeled example`. Supports the input/outcome distinction in supervised learning and the distinction from unlabeled examples. [Source](https://developers.google.com/machine-learning/glossary#labeled-example){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- Google for Developers, `Machine Learning Glossary`: `label leakage`. Supports checking for inputs that reveal the outcome to be predicted. [Source](https://developers.google.com/machine-learning/glossary#label-leakage){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- W3C, `PROV-Overview` (2013). Supports tracing entities, activities, people, processing steps, and versions involved in producing data. [Source](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
