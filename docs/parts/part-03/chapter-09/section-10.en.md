# P3-9.10 How Should Delayed Labels and Not-Yet-Closed Negative Labels Be Distinguished

> Section ID: `P3-9.10`
> Version: `v2026.07.17`

When choosing a [target candidate](/AiBook/reference/concept-glossary/#glossary-target-candidate), you need to distinguish `when a result becomes confirmed` from `whether it has been observed enough to attach a 0 label`. If these are mixed, recent events can look too easily like zeros, or values still in a temporary state can be read like confirmed labels. Delayed label confirmation and incompletely observed negatives are different problems, so they need to be separated first.

| Category | Central question |
| --- | --- |
| Delayed label confirmation | The result existed, but when does it close as the final answer? |
| Incompletely observed negative | Has it been observed long enough to say that no result occurred? |

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

- Google, *Machine Learning Glossary*, `label`, `proxy labels`, accessed 2026-07-08. In this section, the interpretation of `incompletely observed negatives` extends the glossary's proxy-label idea into an operational observation-completeness context. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned state overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
