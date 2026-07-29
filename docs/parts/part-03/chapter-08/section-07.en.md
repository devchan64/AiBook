# P3-8.7 Data Interpretation Changed by Operational Intervention

> Section ID: `P3-8.7`
> Version: `v2026.07.25`

_Subtitle: Why should later data not be read as a natural course when review rules and actions change it?_

The last point to watch at the [interpretation boundary](/AiBook/en/reference/concept-glossary-alpha/i/#interpretation-boundary) is the current [intervention feedback](/AiBook/en/reference/concept-glossary-alpha/i/#glossary-intervention-feedback). If a person quickly acted on cases where `review_needed=1`, the data left afterward may differ from the original natural progression. If you hide that, it becomes too easy to write a sentence such as `the later data looks safer`.

If current review rules or actions can change later data and [selective labels](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-selective-labels), the later data should not be read as if it means the same thing as the natural progression before intervention.

| Current rule or action | What can change in later data |
| --- | --- |
| Immediate review | Action may be taken before a large abnormality spreads, reducing later events |
| Early stop | Log length and later patterns may become shorter |
| Stronger inspection cycle | More detailed records may remain under certain conditions |

Consider the table below.

| event_id | review_needed | intervention | failure_within_7d |
| --- | ---: | --- | ---: |
| A | 1 | immediate_check | 0 |
| B | 1 | immediate_check | 0 |
| C | 0 | none | 1 |

On the surface, `review_needed=1` may look safer. In practice, however, A and B may not have been safer by nature. They may simply have received intervention first, which reduced failure. The interpretation sentence should therefore also state whether the result is `after intervention` or part of `natural progression`.

| Note to write first | Why it is needed |
| --- | --- |
| Which output triggered real action | To know when intervention began |
| Can that action change later logs or labels? | To avoid reading the target of interpretation incorrectly |
| Are you trying to see the pre-intervention signal, or the post-intervention operational result? | To avoid mixing meanings inside the same result column |

The important point is that `if current operational rules are already changing future data, the difference that appears later may contain both an original pattern difference and an intervention effect`. This section can be read not as a special case from one team, but as the problem of whether `the observation target can already be changed by policy and intervention`, which is feedback from intervention. Later data should therefore be read with the possibility that it is not simply an extension of natural progression, but a result already shaped by current rules and actions.

## A Small Diagram

The key point in this section is that current rules and actions may not leave later data untouched. If the review rule triggers intervention and the intervention changes later data, the later difference has to be read by separating `the original pattern` from `the intervention effect`.

--8<-- "assets/part-03/chapter-08/p3-8-7-mermaid-01-en.mmd"

## Sources and References

- W3C, `PROV-Overview`. It provides a provenance perspective for tracing what activities generated particular data and results, which supports this section's explanation that if review rules or actions can change later logs and labels, the later data should be read together with the intervention context. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`. It explains that training and evaluation data can differ from the data encountered in real operation and that the same transformations must be reproduced on real-world data, which is useful for generalizing this section's warning that current operational intervention can change the later data distribution and its meaning. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Conor K. Corbin, Michael Baiocchi, Jonathan H. Chen, `Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection`, 2023. It explains that deployed clinical prediction models can create feedback loops that affect prospectively collected data and label selection, and that performance estimates based only on observed labels can diverge from the deployment population. This directly supports this section's warning that current review rules and actions can change the meaning of later data. [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
