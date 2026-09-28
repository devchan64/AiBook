# P3-4.1 How Do We Decide One Comparable Sample

> Section ID: `P3-4.1`
> Version: `v2026.09.19`

A [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) is one object to compare or predict for the current question. One file [row](/AiBook/en/reference/concept-glossary-alpha/s/#sample-unit) is not necessarily that object. The same log can be read by time point for instantaneous values, by action for action outcomes, or by groups of actions for operating periods.

## Align the Question, Boundary, Features, and Outcome for One Event

The question here is “Which actions were recorded as needing review, and what flow was observed during them?” The [measurement log](/AiBook/assets/part-03/chapter-04/p3_4_1_measurement_log.csv) and [review decisions](/AiBook/assets/part-03/chapter-04/p3_4_1_review_decisions.csv) are fictional data for this book. A measurement row is one time point within an action; an outcome row is one action’s review decision.

Start with E01. Read flow as L/min in this exercise.

| event_id | elapsed_seconds | flow |
| --- | ---: | ---: |
| E01 | 0 | 0.0 |
| E01 | 1 | 1.4 |
| E01 | 2 | 1.6 |

| Decision | Application to E01 |
| --- | --- |
| Object of the question | One action, E01 |
| Group boundary | Group records with the same `event_id`; observed times are 0, 1, and 2 seconds |
| Candidate feature | Observed mean flow `(0.0+1.4+1.6)/3 = 1.0 L/min` |
| Outcome to link | `review_needed=1` in E01’s outcome row |
| Still unknown | Actual end time, full-action coverage, and review criteria |

In these fictional data, `review_needed` is 1 for recorded review needed and 0 for recorded review not needed. It is not a confirmed fault label. Being able to link an outcome to an event differs from having verified the criteria behind it.

For this question, the three measurements provide evidence for one action. Keeping the whole sequence instead of its mean can still use one action as one sample; summarization is not mandatory. Likewise, copying E01’s outcome 1 onto its three measurement rows does not create three actions flagged for review.

## What Changes When the Unit Changes

| Question | Unit of one sample or aggregate row | Count in these data | Evidence needed |
| --- | --- | ---: | --- |
| What is the value at each observed time? | Measurement time point | 36 rows | Event identifier, observation time, measurement |
| What observations and review outcome belong to each action? | One action | 12 events | Grouped event records and the same event’s outcome |
| Does the recent group differ from the baseline group? | A selected group of actions | 2 aggregate rows | Membership, selection conditions, aggregation method |

E01–E12 each have three measurement rows. Grouping the six actions with `is_recent=1` and the six with `is_recent=0` produces recent and baseline aggregate rows. This flag is supplied by the fictional data; the file does not establish actual dates or period lengths. Producing two aggregates does not mean two new independent actions were observed.

The review file has 36 rows, E01–E36, but only E01–E12 have measurements in this input. Thus 12 outcomes can be linked to the current measurement log. Keep E13–E36 separately as outcomes without matching measurements in this input scope. Do not use the outcome-file row count as the current action-sample count.

These correspondences are design choices for the question, not optimal units automatically recommended by data. Reconsider the unit when the question changes. In particular, “Over which interval did the value change?” needs the relationship between adjacent times and measurements, not a single instantaneous value.

## Check Observation Counts and Outcome Linkage Separately

Record `at least three observations` separately from `a linked review outcome`. The first condition is an exercise threshold of at least three observations; it does not verify the action’s end boundary. All 12 original events pass both checks.

Without changing the original files, consider three scenarios: ① exclude only E01’s 2-second measurement; ② exclude only E02’s review outcome; ③ apply both exclusions. Write down event counts, point-count passes, and linked outcomes before checking the table.

| Scenario | Measurement rows | Events | Point-count passes | Linked outcomes | Both conditions met |
| --- | ---: | ---: | ---: | ---: | ---: |
| Original | 36 | 12 | 12 | 12 | 12 |
| ① Exclude E01’s 2-second measurement | 35 | 12 | 11 | 12 | 11 |
| ② Exclude E02’s review outcome | 36 | 12 | 12 | 11 | 11 |
| ③ Apply both exclusions | 35 | 12 | 11 | 11 | 10 |

In ①, E01’s 0- and 1-second records remain, so there are still 12 events. E01 has too few observations but has an outcome. In ②, E02 has three observations but its outcome is unknown. Filling it with `review_needed=0` would change ‘no outcome’ into ‘review not needed’. In ③, two different events each fail one condition, leaving 10 that meet both.

Excluding E01’s 2-second record also changes its observed mean to `(0.0+1.4)/2 = 0.7`. That is a change in the records used, not evidence that the action’s state changed. Raising the threshold to four makes every original event fail the count check; changing the criterion does not damage the original data or make the actions incomplete.

Even enough points require separate checks for duplicate timestamps and actual coverage of the start and end. This CSV has no completion marker, so full-action coverage remains unknown.

## Defining Sample Boundaries for the Question {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-04/p3-4-1-mermaid-01-en.mmd"
```

For your question, write: “One case is ___; its grouping key is ___; its observed range is ___; the required outcome or reference is ___; the unverified boundary is ___.” Here those are one action, `event_id`, the available time-point records, its review outcome, and the actual end boundary. Identifying an event does not by itself verify the meaning of its features or outcome.

## Checklist

- Can you explain what the 36 measurement rows, 12 events, and 2 aggregate rows count?
- Did you connect E01’s observations and outcome as one event and mark its unverified boundary?
- Did you separate E13–E36, which lack measurements here, from the current action-sample count?
- Did you distinguish insufficient observations from an unknown outcome and reproduce the 10 cases in ③?
- Can you distinguish passing a point-count threshold from full-action coverage?

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `label`, `labeled example`, `unlabeled example`. Supports the input/outcome distinction in supervised learning and the distinction from unlabeled examples. [Source](https://developers.google.com/machine-learning/glossary#labeled-example){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
- W3C, `PROV-Overview` (2013). Supports tracing entities, activities, people, processing steps, and versions involved in producing data. [Source](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-19
