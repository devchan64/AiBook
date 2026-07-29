<a id="output-structure"></a>
<a id="glossary-output-structure"></a>

### modeling output structure

- Meaning: Modeling output structure is the designed result frame that determines how a computation should be delivered, such as a comparison report, review candidate queue, or target label candidates. It asks not only `what is the answer?`, but also `what container should hold the result, and who will use it next?` Choosing between a single number, a human-readable comparison table, or a candidate set for later training is a choice of output structure.
- Why it matters: The same source data leads to different dataset designs depending on whether the result becomes a comparison table, a review workflow, or future training candidates. Output structure must be decided before review procedures and automation steps can be designed. This concept separates `what answer should be produced?` from `what workflow-ready form should carry that answer?`
- Related concepts: `comparison report`, `target`, `sample unit`, `task definition`
- Core Section: `P3-2.2`
- Appears in: `P3-index`, `P3-1.1`, `P3-1.2`, `P3-1.3`, `P3-2.1`, `P3-3.2`, `P3-4.3`, `P3-8.2`, `P3-8.4`, `P3-9.1`, `P3-9.2`, `P3-9.3`, `P3-9.5`, `P3-summary`, `P7-index`, `P7-1.1`, `P7-2.1`, `P7-5.1`, `P7-summary`
