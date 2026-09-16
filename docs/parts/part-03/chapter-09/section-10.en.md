# P3-9.10 How Do We Distinguish Delayed Label Confirmation from Incomplete Observation

> Section ID: `P3-9.10`
> Version: `v2026.09.15`

In an operational table, keep `label_observed_at`, `observation_cutoff`, `label_status`, `negative_is_complete`, and `pending_reason` separately. Then a value of 0 is separated from the target-candidate stage as either a value assigned after sufficient observation or a temporary state that is still waiting.

_Subtitle: How should delayed labels be distinguished from 0 labels that have not yet confirmed?_

When choosing a target candidate, you need to distinguish `when a result becomes confirmed` from `whether it has been observed enough to attach a 0 label`. If these are mixed, recent events can look too easily like zeros, or values still in a temporary state can be read like confirmed [supervised learning labels](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label). [Delayed label confirmation](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) and [incomplete negatives](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) are different problems, so they need to be separated first.

| Category | Central question |
| --- | --- |
| [Delayed label confirmation](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) | The result existed, but when does it settle as the final answer? |
| [Incomplete negative](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label) | Has it been observed long enough to say that no result occurred? |

For example, if the target is `failure within the next 7 days`, then the following two lines need to be written together.

- The horizon of looking for the result within 7 days
- Whether the full 7 days were observed before attaching 0

| Note to write first | Why it is needed |
| --- | --- |
| When is the target label usually confirmed? | To know the delay in collecting the answer |
| Is there a temporary state before confirmation? | To separate `pending` from confirmed |
| What is the minimum follow-up period for attaching 0? | To avoid mixing confirmed negatives with incomplete observation |

### No Failure Before Seven Days Have Passed Is Not Yet a Zero

Assume fictional events A, B, and C all start at 10:00 on September 1 and the target is failure within the following 7 days.

| Sample | Evidence currently available | Label status | Outcome value |
| --- | --- | --- | --- |
| A | Followed through September 3; no failure recorded | Follow-up incomplete | Empty |
| B | Followed without gaps through 10:00 on September 8; no failure | Confirmed negative | 0 |
| C | Failure occurred September 2; confirmation completed September 4 | Confirmed positive | 1 |

Once a failure within the period is confirmed, C can be assigned 1 without waiting the full seven days. A has not been observed long enough to conclude that no failure occurred. B is 0 only with evidence of complete follow-up, not simply because the date has passed. Record the failure's occurrence date and the date of system confirmation separately.

## Checking Outcome Confirmation and Observation Completion Separately {#a-small-diagram}

If the tables still leave `not yet confirmed` and `0 after sufficient follow-up` feeling too settle together, read the flow below once more.

<div class="aibook-diagram-scroll" role="region" tabindex="0" aria-label="Diagram: scroll horizontally to read" markdown="1">
<div class="aibook-diagram-canvas" markdown="1">

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-10-mermaid-01-en.mmd"
```

</div>
</div>

So what matters here is not `a technique for splitting 0 and 1 more finely`, but a distinction in observation completeness that keeps not-yet-confirmed labels from being mixed with sufficiently observed negatives under the same value. This section treats `delay in result confirmation`, `incomplete observation period`, and `state note` separately, so that whether a label is confirmed becomes a data-modeling condition in itself.

## Checklist

- Did you use A, B, and C's observation end dates and outcome arrival dates to determine confirmation status?
- Can you explain why incomplete observations must not be filled with negative labels?

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. Used to check the term basis that a label is the answer or result part of an example and that a proxy label approximates labels not directly available in a dataset. In this section, the interpretation of `incompletely observed negatives` extends the proxy-label idea into an operational observation-completeness context. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Corbin, Baiocchi, Chen, *Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection*, 2023. Used as evidence for distinguishing `confirmed 0` from `not yet observed`, because class labels may remain unobserved when enough follow-up records after prediction time are missing. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20

- [NIST Censoring](https://www.itl.nist.gov/div898/handbook/apr/section1/apr131.htm){ target="_blank" rel="noopener noreferrer" }. Checked the distinction between records with no event observed by observation end and final negative outcomes. Checked: 2026-09-15.
