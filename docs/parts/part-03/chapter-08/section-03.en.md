# P3-8.3 In What Order and With What Wording Should Conservative Interpretation Sentences Be Written

> Section ID: `P3-8.3`
> Version: `v2026.07.25`

A conservative interpretation sentence should separate `what changed`, `how strongly it can be stated`, and `what a person should do next` inside one sentence. The key question here is what order and wording should be used after reading a [comparison table](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) so that you avoid both exaggeration and a sentence so weak that it leaves no information. More important than inventing a new boundary is deciding how to place already confirmed [comparison results](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-result) and [evidence strength](/AiBook/en/reference/concept-glossary-alpha/e/#glossary-evidence-strength) in the sentence.

The safest default order is as follows.

1. State the comparison result first.
2. Then attach the condition that lowers or raises interpretation strength.
3. End with the [next action](/AiBook/en/reference/concept-glossary-alpha/n/#glossary-next-action) that a person should take.
4. Do not write cause confirmation unless separate evidence exists.

Compressed into a shorter rule, this becomes `comparison result -> confidence strength -> next action`.

| Sentence order | Why it should come first |
| --- | --- |
| Comparison result | Because the actually observed difference should be stated first |
| Confidence-strength condition | Because wording strength should be adjusted by sample size and repeatability |
| Next action | Because the operational next step for a person should remain in the sentence |
| Excluding cause confirmation | Because you should not write evidence that is not there yet |

## Safe Sentences and Risky Sentences

Even for the same observation, interpretation strength changes a great deal depending on the wording.

| Observation state | Risky sentence | Safer sentence |
| --- | --- | --- |
| A difference appears in a few recent cases | The state has definitely changed | A difference appears in a small number of recent cases, so more observation is needed |
| A decline pattern appears repeatedly | A sensor abnormality occurred | A repeated decline pattern appears, so the review priority is raised |
| The difference is large but the sample size is small | Confirm the alert immediately | The difference is large, but the warning strength stays conservative because the sample size is small |
| The change from baseline is large and repeated | The cause is obvious | The change signal is strong enough to make human checking more worthwhile |

The point of this table is not `speak weakly`. It is `state only the level directly supported by the evidence with precision`.

## Fix the Sentence Skeleton First

If you try to write a sentence immediately after reading the comparison table, cause claims can easily slip in. At this stage, it is safer to fix the skeleton below first.

The safe default skeleton is as follows. The recent window shows [what kind of difference] from the [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline), and given [the sample-size/repeatability condition], [the review strength or next action] is appropriate.

If you insert actual values into that skeleton, it turns into sentences like these.

- The recent window shows a larger late-stage drop rate than the baseline, and because there are only 4 recent cases, more observation is needed without confirming the cause.
- The recent window shows both a lower average and higher variability than the baseline, and because the same-direction change repeats across 20 recent cases, the review priority is raised.
- The recent window shows only a small difference from the baseline and weak repeatability, so it remains at a record level.

All three sentences first state the comparison result, then attach the strength condition, and end with the next action. By contrast, sentences such as `A sensor abnormality occurred` or `The failure has been confirmed` pull in evidence that is not yet present.

## Sentence Ladder by Interpretation Strength

If the previous section's levels of `record`, `review candidate`, and `strong warning` are moved into actual sentence endings, they can be organized like this.

| Interpretation strength | More natural sentence ending |
| --- | --- |
| Record level | Keep it in the record and continue observing |
| Review-candidate level | It is worth a person reviewing first |
| High review priority | Raise the review priority |
| Not cause confirmation | Defer cause confirmation |

This table does not mean `every state always gets this label`. Its role is to keep the sentence from sliding into excessively strong confirmatory wording by fixing default endings in advance.

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-3-mermaid-01-en.mmd"
```

This diagram shows that the order of sentence construction is itself the key point. If you state the comparison result first, then add the strength condition, and close with the next action, both exaggeration and empty vagueness are reduced. The issue here is not `how to write weak sentences`, but `how to place a sentence in the order directly supported by the evidence`. When that order is fixed, report sentences keep the comparison basis and avoid dragging in a cause judgment that does not yet exist.

## Sources and References

- W3C, `PROV-Overview`. It offers a provenance perspective that separates an observed result from the path of evidence behind it, which supports this section's claim that comparison result, confidence-strength condition, and next action should be written as separate levels within a single sentence. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. It provides a control-chart context in which comparison signals are read without jumping immediately to functional judgment or confirmed cause, which supports the boundary awareness in this section that conservative interpretation sentences should follow the order `comparison result -> strength condition -> next action`. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
