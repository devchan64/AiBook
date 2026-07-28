# P3-9.10 Delayed Label Confirmation and Incomplete Negatives

> Section ID: `P3-9.10`
> Version: `v2026.07.25`

_Subtitle: How should delayed labels be distinguished from 0 labels that have not yet closed?_

When choosing a [target candidate](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target-candidate), you need to distinguish `when a result becomes confirmed` from `whether it has been observed enough to attach a 0 label`. If these are mixed, recent events can look too easily like zeros, or values still in a temporary state can be read like confirmed [supervised learning labels](/AiBook/en/reference/concept-glossary-alpha/l/#glossary-label). [Delayed label confirmation](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-delayed-label-confirmation) and [incomplete negatives](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-incomplete-negative) are different problems, so they need to be separated first.

| Category | Central question |
| --- | --- |
| [Delayed label confirmation](/AiBook/en/reference/concept-glossary-alpha/d/#glossary-delayed-label-confirmation) | The result existed, but when does it close as the final answer? |
| [Incomplete negative](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-incomplete-negative) | Has it been observed long enough to say that no result occurred? |

For example, if the target is `failure within the next 7 days`, then the following two lines need to be written together.

- The horizon of looking for the result within 7 days
- Whether the full 7 days were observed before attaching 0

| Note to write first | Why it is needed |
| --- | --- |
| When is the target label usually confirmed? | To know the delay in collecting the answer |
| Is there a temporary state before confirmation? | To separate `pending` from confirmed |
| What is the minimum follow-up period for attaching 0? | To avoid mixing closed negatives with incomplete observation |

## A Small Diagram

If the tables still leave `not yet confirmed` and `0 after sufficient follow-up` feeling too close together, read the flow below once more.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-10-mermaid-01-en.mmd"
```

So what matters here is not `a technique for splitting 0 and 1 more finely`, but a distinction in observation completeness that keeps not-yet-closed labels from being mixed with sufficiently observed negatives under the same value. This section treats `delay in result confirmation`, `incomplete observation period`, and `state note` separately, so that whether a label is closed becomes a data-modeling condition in itself.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `proxy labels`. Used to check the term basis that a label is the answer or result part of an example and that a proxy label approximates labels not directly available in a dataset. In this section, the interpretation of `incompletely observed negatives` extends the proxy-label idea into an operational observation-completeness context. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for preserving processing steps, reproducibility, versioning, and derivation. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Corbin, Baiocchi, Chen, *Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection*, 2023. Used as evidence for distinguishing `closed 0` from `not yet observed`, because class labels may remain unobserved when enough follow-up records after prediction time are missing. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
