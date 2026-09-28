# P3-3.2 How Should a Dataset Be Redesigned to Match the Question

> Section ID: `P3-3.2`
> Version: `v2026.09.19`

To redesign a dataset means reviewing the [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) unit and [column](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) structure required by the question. In other words, it means deciding again what should count as one [row](/AiBook/en/reference/concept-glossary-alpha/s/#sample-unit), `which columns should remain`, and `what should be compared against what`. That is also why an action-level table, a [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure), and a candidate prediction-problem table differ from one another: the difference is born inside this redesign.

Raw logs are also datasets. Redesign is not a procedure for granting them that status; it means choosing what a row represents and what information to retain for the current question. Keeping the original sequence is also an option.

## Build an Action-Level Table from the Same Records

Use only A, B, E, and F from the preceding section’s fictional [source log](/AiBook/assets/part-03/chapter-03/p3_3_1_source_operation_log.csv). Each row records one time point within an action; `second` is elapsed time in seconds within that action. Read flow below in L/min. All four actions have `recipe=standard`, but the file does not establish that all other operating conditions match.

Question 1 is “What is the observed mean flow for each action?” Use one action per row, group original records by `event_id`, and take the arithmetic mean of the four measurements. This is a mean over observation points, not a guaranteed time-weighted mean over the complete action.

| event_id | batch_id | flow at seconds 0, 1, 2, 3 | mean_flow | max_flow |
| --- | --- | --- | ---: | ---: |
| A | B-17 | 0.0, 1.4, 1.6, 1.2 | 1.050 | 1.6 |
| B | B-17 | 0.1, 1.0, 1.1, 0.9 | 0.775 | 1.1 |
| E | B-19 | 0.0, 1.2, 1.4, 1.0 | 0.900 | 1.4 |
| F | B-19 | 0.1, 1.5, 1.6, 1.3 | 1.125 | 1.6 |

For A, `mean_flow` is `(0.0+1.4+1.6+1.2)/4 = 1.050`. `event_id` and `batch_id` are original identifiers; `mean_flow` and `max_flow` are derived from `flow`. The four time-point values are shown to expose the calculation evidence. If an actual summary omits this sequence, it loses the order of rises and falls, so retain a link to the original file, version, and event identifier.

## Compare Two Groups from the Same Action Table

Question 2 is “How does mean flow in the recent group differ from the baseline group?” For this exercise, **assign by assumption** A and B to `baseline`, and E and F to `recent`. The original file has neither occurrence dates nor this grouping column; we are not inferring recency from event names or batch numbers. Real use requires checking dates and selection conditions.

| group | included event_id | event_count | mean_of_event_means |
| --- | --- | ---: | ---: |
| baseline | A, B | 2 | 0.9125 |
| recent | E, F | 2 | 1.0125 |

The baseline mean is `(1.050+0.775)/2 = 0.9125`; the recent mean is `(0.900+1.125)/2 = 1.0125`. Each action receives equal weight, and the unit is L/min. A result row comparing the two groups is:

| recent_members | baseline_members | recent_mean | baseline_mean | diff |
| --- | --- | ---: | ---: | ---: |
| E, F | A, B | 1.0125 | 0.9125 | +0.1000 |

Because `diff = recent_mean−baseline_mean`, the recent group’s mean is 0.1000 L/min higher in this exercise. This is not a fault or instability judgment. The groups belong to different batches and other operating conditions remain unverified, so this table alone does not establish the cause of the difference.

## Different Questions Need Different Columns Even with the Same Row Unit

Compare two questions about the same four actions: “Which action has the highest mean flow?” and “Which action has the steepest flow decline in its final observed interval?” Before reading the table, choose the columns needed for each question from `event_id`, `mean_flow`, `max_flow`, `second`, and `flow`.

Both questions use one action per row, but the mean question needs `mean_flow`, while the final-decline question needs a slope calculated from the final two times and flow values. Here the final interval is always seconds 2–3, so `last_slope = (flow_3−flow_2)/(3−2)`. Its unit is L/min/s; **a more negative slope** means a steeper decline.

| event_id | mean_flow (L/min) | flow_2 (L/min) | flow_3 (L/min) | last_slope (L/min/s) |
| --- | ---: | ---: | ---: | ---: |
| A | 1.050 | 1.6 | 1.2 | -0.4 |
| B | 0.775 | 1.1 | 0.9 | -0.2 |
| E | 0.900 | 1.4 | 1.0 | -0.4 |
| F | 1.125 | 1.6 | 1.3 | -0.3 |

F has the highest mean, but A and E have the steepest final decline. For A, `(1.2−1.6)/1 = −0.4`, compared with `−0.3` for F. `max_flow` does not identify the final two values and their order, so it cannot replace the final slope. This compares declines over one selected interval; it does not classify whole-action instability or faults.

## What Summaries Retain and Lose

| Structure | Meaning of one row | Retained information | What the summary alone cannot establish |
| --- | --- | --- | --- |
| Raw time-point table | A time point within an action | Time and individual measurements | Outcome labels and causes require separate evidence |
| Action summary | One action | Action means, maxima, and source-link keys | Value order and change-onset time |
| Group summary | A selected group of actions | Members, action count, and group mean | Differences between actions and their individual sequences |

Mean and maximum alone cannot answer “Was it unstable?” Change A’s sequence from `0.0, 1.4, 1.6, 1.2` to `0.0, 1.6, 1.2, 1.4`. The mean stays 1.050 and the maximum stays 1.6, but the peak moves from second 2 to second 1. If the question concerns fluctuation patterns or change onset, retain the sequence or return to the raw log. Finding a change time does not establish its cause either.

Not every question requires baseline columns or a summary table. To compare time-point patterns, time and measurements can be retained as they are. For supervised learning, the preceding section’s checks on inputs, targets, and label evidence still apply.

## How Questions Change Samples and Tables {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-03/p3-3-2-mermaid-01-en.mmd"
```

The new question is “Which is the first interval in A with an observed decrease?” Write down these three decisions before comparing them with the explanation.

1. Choose whether one row represents the whole action or an interval between adjacent observations.
2. Select the columns needed as original evidence from `mean_flow`, `max_flow`, `event_id`, `second`, and `flow`.
3. State the interval you would report and what that result cannot establish.

One answer uses `an interval between adjacent observations within an action` as one row. Retain `event_id`, starting and ending `second`, and starting and ending `flow`; calculate `ending flow−starting flow`. A’s differences over seconds 0–1, 1–2, and 2–3 are +1.4, +0.2, and −0.4, so the first observed decrease is over **seconds 2–3**. This does not identify the exact onset within that interval or its cause.

For the earlier reordered sequence, `0.0, 1.6, 1.2, 1.4`, the differences become +1.6, −0.4, and +0.2, moving the answer to **seconds 1–2**. A table retaining only mean and maximum cannot distinguish these answers. Keeping the full sequence in one row is also valid, provided the correspondence between times and flow values is preserved.

## Checklist

- Can you choose and justify the columns and row unit needed for a mean, final slope, or adjacent-interval question?
- Can you explain one row in the action-level and group-level tables made from the same log?
- Did you reproduce A’s mean and the group-mean difference of 0.1000 from the original records?
- Did you distinguish original identifiers, calculated values, and assumed exercise groups?
- Can you explain how time patterns can differ despite identical means and maxima?
- Did you preserve source links for omitted information and note unverified comparison conditions?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label`, `labeled example`, `unlabeled example`. Supports the input/outcome distinction in supervised learning and the distinction from unlabeled examples. [Source](https://developers.google.com/machine-learning/glossary#labeled-example){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- W3C, `PROV-Overview` (2013). Supports tracing entities, activities, people, processing steps, and versions involved in producing data. [Source](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
