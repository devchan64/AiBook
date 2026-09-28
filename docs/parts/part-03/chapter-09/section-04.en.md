# P3-9.4 How Do Review Notes Become Target Candidates?

> Section ID: `P3-9.4`
> Version: `v2026.09.20`

Before converting notes into columns, decide what is being extracted. “Repeated late decline; recheck needed; sensor issue suspected” combines an observation report, a review request, and a causal hypothesis. Reducing all of it to `failure=1` invents a conclusion. A [target candidate](/AiBook/en/reference/concept-glossary-alpha/t/#target) can be structured from notes, but structuring is neither factual validation nor readiness for training.

## Preserve the source and separate sentence roles

These notes are fictional. A–D identify comparison windows local to this section, not the same letters in other sections. Notes concern their windows and must not be copied automatically into individual-operation labels. R1 and R2 are fictional note-author IDs.

| note_id | window_id | reviewer_id | Original note |
| --- | --- | --- | --- |
| N1 | A | R1 | Repeated late decline observed. Recheck needed. Sensor issue suspected. |
| N2 | B | R1 | Record only. |
| N3 | C | R2 | A downward late-period pattern was observed across several operations. Additional checking recommended. |
| N4 | D | R2 | Template example: “Recheck needed.” No additional review requested for the current case. |

N1's first sentence is **what the author reports observing**. It does not mean raw sensor records were independently verified here. “Sensor issue suspected” proposes a cause rather than confirming it. N4 quotes a template, not a request about D.

## A short annotation guide: note-v1

This exercise records **what the current note explicitly states**, not actual failure status. `?` means a value cannot be assigned because information is absent, unclear, or contradictory. When statements conflict, retain the case for source checking instead of arbitrarily choosing one.

| Candidate column | Rule for assigning 1 or a value | Zero or unknown treatment |
| --- | --- | --- |
| reported_repeated_drop | Explicitly reports late decline across multiple operations in the current window | 0 if it explicitly reports not observing that repetition; ? if unmentioned |
| note_requests_review | Requests checking of the current target, such as “Recheck needed” or “Additional checking recommended” | 0 for explicit no additional request or this guide's “Record only”; ? if target or intent is unclear |
| suspected_cause | Preserve a hypothesized cause stated for the current target | ? if unmentioned; never convert into a confirmed cause |

`note_requests_review=0` means this note contains no additional request, not that review is unnecessary or that no other channel requested it. Mapping “Record only” to zero is an explicit document-interpretation convention in note-v1. If the source note itself is missing, leave all three columns unknown.

## Different wording with shared meaning; identical wording in different contexts

N1's “Repeated late decline observed” and N3's “A downward late-period pattern was observed across several operations” are the same kind of observation report under this guide. N1's “Recheck needed” and N3's “Additional checking recommended” both request further checking of the current target. Different wording can map to the same value after checking role and subject.

Conversely, “Recheck needed” appears identically in N1 and N4 but has different roles: an actual request in N1 and a template quotation in N4. Setting N4's request flag to one merely because the words appear would discard context.

| note_id | window_id | reported_repeated_drop | note_requests_review | suspected_cause |
| --- | --- | --- | --- | --- |
| N1 | A | 1 | 1 | Sensor issue |
| N2 | B | ? | 0 | ? |
| N3 | C | 1 | 1 | ? |
| N4 | D | ? | 0 | ? |

B's “Record only” does not state that repeated decline was absent, so its repetition report remains `?`. Ones for N1 and N3 also differ from repetition independently verified in measurements. If a quantitative decline rule defines the target, check the window's raw measurements and consistent calculation criteria, not just note wording.

## Check label evidence after structuring

Link every structured row to `note_id` for its source, `window_id` for its target, `reviewer_id` for the author, `annotator_id` for the person extracting values, and `annotation_version` for the guide used. For example, retain `reviewer_id=R1`, `annotator_id=AN1`, and `annotation_version=note-v1` for N1. Author and annotator need not be the same person. Preserve the original text, creation time, and evidence location; distinguish revisions without overwriting the source.

A phrase appearing ten times may reflect ten copies of a template. Frequency alone establishes neither consistent meaning nor truth. If independent annotators assign different values to the same target's note, compare scope, negation, quotation, and evidence to refine the guide. Agreement still does not verify the underlying failure fact.

If the goal is classifying additional-review requests, `note_requests_review` may be a candidate for that judgment. If the goal is actual failure, separate outcome confirmation is needed. Decide whether the target concerns requests, observation reports, or causal hypotheses, then check label provenance, input timing, and evaluation scope.

## Organizing Review Notes Around Shared Label Criteria {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-4-mermaid-01-en.mmd"
```

This is one route from notes to candidate columns. Not every label must originate in repeated review notes. Existing independent inspection outcomes can be used with their definitions and supporting evidence.

## Annotate a short note yourself

A new note says: “Checked several operations in this window but did not observe repeated late decline. Recheck needed.” Fill the three note-v1 columns and explain whether actual failure status is also established.

Explanation: `reported_repeated_drop=0`, `note_requests_review=1`, and `suspected_cause=?`. Extract the explicit report of no observed repetition separately from the additional request. Distinguish this from B's `?`, where repetition is never mentioned. The note alone does not establish actual failure status. Retain a new note_id, original text, author, annotator, and guide version.

## Checklist

- Can you separate observation reports, review requests, and causal hypotheses without converting unmentioned information to zero?
- Can you distinguish different expressions with the same meaning from identical phrases used in different contexts?
- Can you trace a candidate value to the source, author, annotator, and guide version, and distinguish frequency from factual verification?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for linking derived results to sources, activities, and responsible agents. Note-v1, notes, and annotations are fictional teaching examples, not validated failure ground truth. Accessed: 2026-09-20.
