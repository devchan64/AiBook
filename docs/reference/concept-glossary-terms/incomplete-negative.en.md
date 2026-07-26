<a id="incomplete-negative"></a>
<a id="glossary-incomplete-negative"></a>

### incomplete negative

- Meaning: An incomplete negative is a case that looks like 0 only because the required follow-up period has not finished yet. A closed negative means the outcome was absent after sufficient observation; an incomplete negative means there is not enough observation to say that yet.
- Why it matters: If incomplete negatives are trained as closed zeros, a model can learn recent cases as safer than they really are. This concept makes the required follow-up period, `pending` state, and label confirmation rule part of the data-modeling contract.
- Related concepts: `delayed label confirmation`, `label`, `target candidate`, `selective labels`
- Core Section: `P3-9.10`
- Appears in: `P3-9.10`
