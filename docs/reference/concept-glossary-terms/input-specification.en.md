<a id="input-specification"></a>
<a id="glossary-input-specification"></a>

### input specification

- Meaning: A description of what unit, columns, order, and structure will be passed to a model or later learning stage as input. It is not just the act of handing over a file. It decides what counts as a case, which features remain, and how order or segment information will be represented.
- Why it matters: A clear input specification helps separate human-designed features from representations learned later by the model. In Part 3, feature design first answers `what should the model receive as input`; representation learning then happens inside that input during later model training. Without this boundary, feature design can be mistaken for outdated preprocessing, or the model can be imagined as deciding the whole problem structure by itself.
- Related concepts: `feature`, `intermediate representation`, `representation learning`
- Core Section: `P3-6.3`
- Appears in: `P3-6.3`
