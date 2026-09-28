# P3-9.1 How Far Should the Current Problem Be Taken?

> Section ID: `P3-9.1`
> Version: `v2026.09.20`

First decide whether you need to explain a change, order human review, or predict an unknown outcome. Choose the [output](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) for that purpose. Prediction does not require first building alerts and then a review queue. A question with established outcome labels and evaluation conditions can proceed directly to prediction design; if explaining change is the purpose, a comparison report can itself be a complete deliverable.

## Choose among three questions in parallel

| Question to answer now | Suitable output | Evidence to check first |
| --- | --- | --- |
| What differs from a reference under matching conditions? | Comparison report, with an alert if needed | Comparison populations, units, aggregation, baseline, and alert conditions |
| Which cases should people inspect first today? | Review candidates in an ordered queue | Inclusion criteria, sorting and tie-break rules, and capacity |
| Can inputs available at a defined time predict an unknown outcome? | Target-outcome prediction | Target definition, input availability time, outcome labels, and evaluation data separate from training |

These are not levels of completion. A report communicates observed differences, a queue assigns checking work, and prediction estimates a defined outcome. One workflow may use more than one, but each output retains its own purpose and supporting evidence.

## Different purposes yield different answers from operational records

The following three requests are fictional. For the first, assume late-period means of 2.8 and 2.2 L/min from 200 past and 20 recent operations under matching conditions. Their difference is `2.2−2.8=−0.6 L/min`. This is an observed comparison, not a prediction of future failure or its cause.

| Request | Output choice and reason | Checks still needed |
| --- | --- | --- |
| “Report how recent flow differs from baseline” | Comparison report containing the −0.6 L/min mean difference and counts | Baseline suitability and coverage; issuance rules if an alert is also requested |
| “We have candidates A, B, and C, but can inspect only two today” | First two entries of a queue produced by a sorting policy | Candidate inclusion, ordering, tie-breaks, and handling of remaining cases |
| “At operation completion, predict whether failure will occur within seven days” | Prediction design targeting that outcome | Inputs at completion, seven-day outcome definition and complete labels, and data for evaluating new cases |

Applying `queue-v1` from [P3-8.5](../chapter-08/section-05.en.md) to the second request gives A→C→B, so A and C are assigned first. B is left out of this allocation, not diagnosed as normal. Explicit operational rules can create this queue without failure-cause labels. A previously issued alert is not a prerequisite either.

For the third request, outcome labels belong to historical training and evaluation cases. A new operation's seven-day outcome is still unknown when making its prediction. Having past labels differs from already knowing the answer for a new event. If only selected reviewed events have labels, check the selection problem in [P3-8.6](../chapter-08/section-06.en.md).

## Alerts also require a policy

Separate a calculated difference from issuing an alert. A difference of −0.6 L/min alone does not automatically imply `warning=1`. Define issuance conditions, recipients, and handling of missing measurements and duplicate alerts. If alerts trigger action, also check the consequences of false and missed alerts and the responsibilities and procedures for responding.

Alerts are not invariably lightweight, nor predictions invariably heavyweight. An alert that stops equipment may require stringent operational rules, while another task may provide predictions for reference only. Match validation to purpose and error consequences rather than the output's name. [P3-8.4](../chapter-08/section-04.en.md) illustrates reproducible policies.

## Prediction targets extend beyond cause classification

A prediction [target](/AiBook/en/reference/concept-glossary-alpha/t/#target) is the outcome to estimate. It may be a category, such as failure within seven days, or a number, such as the next operation's duration. Predicting categories is classification; predicting continuous numeric values is regression. Classifying a failure's cause is one possible target, not a requirement for every prediction task.

For example, if historical inputs available at operation start are linked to durations confirmed after completion and evaluation data are ready, duration prediction need not begin with an alert system. Check the input–outcome linkage, outcome definition, and evaluation on cases not used for training. Labels alone do not establish predictive performance or deployment readiness.

## Boundaries Between Comparison Reports, Review Queues, and Prediction Problems {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-1-mermaid-01-en.mmd"
```

If prediction is the purpose but the outcome window or label definition is unclear, document those gaps and improve outcome definition and collection. A report or queue may be useful as a separate deliverable, but it does not thereby answer the original prediction question. Conversely, a report that fulfills its purpose is not incomplete merely because it was not converted into prediction.

## Choose an output for the purpose

① You want the next operation's duration in advance and have historical input–outcome pairs plus separate evaluation data. ② You want only the difference between recent and baseline means under matching conditions. ③ You need to inspect two of three candidates first and have no cause labels. Choose an output for each and name something that is not a mandatory prerequisite.

Explanation: ① Can proceed to duration-prediction design without first building an alert system. ② Calls for a comparison report, not mandatory future-outcome prediction. ③ Calls for a review queue with explicit inclusion and sorting rules; confirmed cause labels are not mandatory. However, its label-free queue rank cannot be called an actual failure probability.

## Checklist

- Can you justify your choice among explaining change, ordering review, and predicting an outcome?
- Have you identified the required evidence and specific gaps for the chosen output?
- Have you avoided treating prediction as a mandatory final stage or alerts as requiring no validation?

## Sources and references

- [Google, Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } — Reference for label, classification model, and regression model definitions. The output-choice table and requests are this book's educational examples, not a standard prescribing mandatory development stages. Accessed: 2026-09-20.
