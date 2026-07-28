<a id="group-split"></a>
<a id="glossary-group-split"></a>

### group split

- Meaning: A group split separates data by dependent groups, such as the same person, device, store, patient, or account, so that records from the same group do not appear on both the training side and the validation or test side.
- Why it matters: If similar records from the same entity appear on both sides, the model may look strong because it recognizes a familiar entity rather than generalizing to a new one. A group split closes the question of what should count as an independent new case.
- Related concepts: `evaluation design`, `data leakage`, `sample unit`
- Core Section: `P3-9.13`
- Appears in: `P3-9.13`
