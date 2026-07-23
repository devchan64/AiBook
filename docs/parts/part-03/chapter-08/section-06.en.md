# P3-8.6 Confirmed Labels Left Only on Some Cases

> Section ID: `P3-8.6`
> Version: `v2026.07.23`

_Subtitle: What should be written with the interpretation when confirmed labels exist only for reviewed cases?_

At the interpretation stage, it can matter not only `how the numbers differ` but also `who received a confirmed label`. In real operations, not every event gets reviewed with the same depth. A person may revisit only some cases that looked abnormal, and only those cases may receive confirmed labels. If that structure is hidden, readers can easily read `the set of cases with labels` as if it were `the set of all events`.

If confirmed labels remain only on reviewed cases, those labels should not immediately be read as representing the whole.

| Visible state | What should also be written in the interpretation |
| --- | --- |
| Confirmed labels exist only for some cases | By what rule were only those cases reviewed? |
| Cases with `review_needed=0` were rarely rechecked | Does no label mean normal, or does it mean unchecked? |
| Labels cluster only in a certain period or on certain equipment | Could the label set itself be biased? |

Consider the table below.

| event_id | review_needed | manually_reviewed | confirmed_root_cause |
| --- | ---: | ---: | --- |
| A | 1 | 1 | sensor_drop |
| B | 1 | 1 | valve_delay |
| C | 0 | 0 | None |
| D | 0 | 0 | None |

If you look only at the two rows with `confirmed_root_cause` and then describe the root-cause distribution of the whole operation, the interpretation can become exaggerated. You need to state why only A and B were reviewed by people, and whether C and D are blank because they were truly normal or because they were simply not reviewed yet.

At the interpretation stage, notes like the following are enough.

| Note to write first | Why it is needed |
| --- | --- |
| The rule for becoming a review target | To expose a structure in which labels remain selectively |
| The meaning of a missing label | To avoid mixing normal with unchecked |
| Range bias in the set with labels | To avoid overstating interpretation strength |

The important point here is that `a selectively attached confirmed label can serve as interpretation evidence, but before reading it as a full answer set that represents all events, you should first write the review path and possible bias`. A confirmed-label table should therefore first be read not as `the answer table for all events`, but as a confirmation result for some events that passed through a review path.

## A Small Diagram

The key point in this section is not to read `confirmed labels that remain only on reviewed cases` as if they were the answer table for all events. Once confirmed labels appear, the `meaning of missing labels`, the `review path`, and possible `bias` should be written beside them so the interpretation is not overstated.

--8<-- "assets/part-03/chapter-08/p3-8-6-mermaid-01-en.mmd"

## Sources and References

- Google for Developers, `Machine Learning Glossary`, `labeled example`. It provides the basic frame that a label is result information attached to an example, which supports this section's explanation that if confirmed labels remain only for some cases, that labeled set may not represent the same range as the set of all events. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Himabindu Lakkaraju, Jon Kleinberg, Jure Leskovec, Jens Ludwig, Sendhil Mullainathan, `The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables`, KDD 2017. It explains that in selectively labeled data, observed outcomes can be consequences of earlier human decisions rather than a random sample of the whole population, which directly supports this section's warning not to read labels left only on reviewed cases as the answer table for all events. [https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. It offers a provenance perspective for recording what review procedure produced a given result, which provides a general basis for this section's claim that the review path and the meaning of missing labels should be written together when interpreting selectively labeled cases. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
