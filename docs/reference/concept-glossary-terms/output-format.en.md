## output format

- Meaning: Output format is the condition that specifies the shape of the returned answer, such as a table, list, JSON object, paragraph, or step-by-step explanation. It is an interface condition that is separate from the core content itself. It decides the wrapper in which the result should be delivered.
- Why it matters: The same content can be much easier or harder to post-process, review, and reuse depending on its output format. This concept separates `what should be answered?` from `in what structure should it be returned?` It also explains why a useful answer can still break an automation pipeline or review process if the format is wrong.
- Related concepts: `prompt`, `constraint`, `instruction`
- Core Section: `P1-12.1`
