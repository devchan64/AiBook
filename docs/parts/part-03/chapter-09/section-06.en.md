# P3-9.6 Checking Label Consistency

> Section ID: `P3-9.6`
> Version: `v2026.09.20`

When the same event receives different labels, which judgments should we revisit? [Label consistency](/AiBook/en/reference/concept-glossary-alpha/l/#label-consistency) asks how well judgments agree for the same subject, information, and criteria. Everyone can give the same wrong answer, so agreement and correctness require separate checks.

## Distinguish 12 Events from 36 Review Records

The [review CSV](/AiBook/assets/part-03/chapter-09/p3_9_6_label_reviews.csv){ .csv-preview } is an educational example for this section. Each row is one reviewer's judgment about one `event_id` in a particular month. A–L identify events within this file; they do not link to comparison windows A–C in earlier sections.

kim and lee each reviewed the 12 events once in April; park reviewed each once in May. There are therefore 12 events and `12 × 3 = 36 review records`. `review_needed` means a judgment that review is needed; `normal` means a judgment classifying the event as normal. Neither is an independently verified failure outcome. R and N below abbreviate these two strings.

| event_id | kim · April | lee · April | park · May |
| --- | --- | --- | --- |
| A | R | N | R |
| B | N | N | N |
| C | R | R | R |
| D | N | N | R |
| E | R | R | R |
| F | N | R | N |
| G | R | N | N |
| H | N | N | N |
| I | R | R | N |
| J | R | R | R |
| K | N | N | N |
| L | R | N | R |

The key columns are `event_id`, `review_month`, `reviewer`, and `review_label`. The CSV's `diff` and `repeatability` are not used in this count. Their values or wording do not establish which label is correct.

## What Is the Denominator?

Six events have at least two different labels: A, D, F, G, I, and L. **The fraction of events with disagreement is `6 / 12 = 50%`.** Each event is counted once, so the denominator is not the 36 review records. This is neither reviewer-pair agreement nor model accuracy.

A's R·N·R counts as one event with disagreement even though two judgments match. Comparing reviewer pairs would require a different calculation, counting kim–lee, kim–park, and lee–park separately. Here, we identify events to revisit instead.

| Month | R records | N records | Total review records | R proportion |
| --- | ---: | ---: | ---: | ---: |
| 2026-04 | 12 | 12 | 24 | 12 / 24 = 50% |
| 2026-05 | 6 | 6 | 12 | 6 / 12 = 50% |

R records fell from 12 to 6, but total review records also halved. Both monthly R proportions are 50%, so it is incorrect to say that the proportion needing review fell. Equal monthly proportions do not imply identical event-level judgments either. D changed from N·N to R, and I from R·R to N.

## Causes of Disagreement and Records to Recheck {#looking-at-the-comparison-table-first}

This file uses the same 12 events in both months, but the reviewers change. It does not record what information each reviewer saw or which criteria version they used. The differences therefore do not establish a time effect or a criteria change. In other datasets, the event mix may change too, so check the event roster as well.

| Record to retrieve first | Question to check | Next action |
| --- | --- | --- |
| Original kim and lee judgments for A | Did they disagree despite seeing the same information in the same month? | Compare the supplied material and recorded reasons |
| April and May judgments for D and I | Which changed: reviewer, information, or criteria? | Reassess the same information package under explicit criteria |
| Label definitions and criteria versions | Did both people use R and N with the same meaning? | Document boundary cases and applicable criteria |
| Separate confirmed inspection records | Was the judgment itself correct? | Independently verify the actual outcome needed |

For reassessment, hold the event ID, supplied information, and criteria version fixed, and consider recording judgments before reviewers see each other's answers. If an adjudicated final label is needed, record the responsible person and rationale too. Preserve original judgments and link new ones to them so the changes remain explainable. A majority vote alone does not establish whether a failure occurred.

## From Disagreement to Reviewing Criteria {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-6-mermaid-01-en.mmd"
```

This process is not about erasing disagreement to raise agreement. It checks the conditions behind differences and gathers outcome evidence appropriate to the task. Events with matching judgments are not automatically exempt from correctness checks.

## Recalculate with a Different Comparison Scope {#a-small-python-example}

Exercise: Hide park's May column and compare April alone. What happens to the event count, review-record count, disagreement list, and disagreement fraction? Does this show that the April criteria were more accurate?

Answer: There are still 12 events, now with 24 review records. kim and lee disagree on A, F, G, and L: four events, giving `4 / 12 ≈ 33.3%`. D and I drop out because their two April judgments match. The decrease from 50% to 33.3% results from changing which judgments are included; it is not evidence of improved accuracy. Only the comparison scope changes, not the original CSV.

## Checklist

- Can you distinguish 12 events, 36 review records, and six events with disagreement, and explain the denominators?
- Can you explain both the monthly R proportion of 50% and the changes in individual event judgments?
- Can you select original judgments to revisit, hold information and criteria fixed, and distinguish agreement from correctness?

## Sources and References

- Google, *Machine Learning Glossary*, `rater`, `inter-rater agreement`, `label`. Used to check the role of a rater who provides labels for examples and the inter-rater agreement view for whether multiple raters agree. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, provenance and activity context overview. Used to check the provenance view that a label candidate should remain traceable to reviewer, time, and activity context. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
