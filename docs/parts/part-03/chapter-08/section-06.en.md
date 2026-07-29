# P3-8.6 Confirmed Labels Left Only on Some Cases

> Section ID: `P3-8.6`
> Version: `v2026.07.25`

_Subtitle: What should be written with the interpretation when confirmed labels exist only for reviewed cases?_

At the interpretation stage, it can matter not only `how the numbers differ` but also who received a confirmed [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label). In real operations, not every event gets reviewed with the same depth. A person may revisit only some cases that looked abnormal, and only those cases may receive confirmed labels. If this [selective labels](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-selective-labels) structure is hidden, readers can easily read `the set of cases with labels` as if it were `the set of all events`.

If confirmed labels remain only on reviewed cases, those labels should not immediately be read as representing the whole.

| Visible state | What should also be written in the interpretation |
| --- | --- |
| Confirmed labels exist only for some cases | By what rule were only those cases reviewed? |
| Cases with `review_needed=0` were rarely rechecked | Does no label mean normal, or does it mean unchecked? |
| Labels cluster only in a certain period or on certain equipment | Could the label set itself have [bias](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-bias)? |

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

The important point here is that `a selectively attached confirmed label can serve as interpretation evidence, but before reading it as a full answer set that represents all events, you should first write the review path and possible bias`. A confirmed-label table should therefore first be read not as `the answer table for all events`, but as a confirmation result for some events that passed through a review path such as a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure).

The next example reduces this problem into a small model evaluation. In real operations, the final result of unreviewed events may be unknown. So `actual_failure_for_demo` in the code is a hidden outcome used only for learning. The goal is not to use this value as an answer table, but to check what kind of illusion can appear when a model is evaluated only with labels left on reviewed cases.

Problem situation: We want to see how a model score can look different depending on the review path when confirmed labels exist only for reviewed cases.

Input: `risk_score`, `manually_reviewed`, and the hidden demo outcome `actual_failure_for_demo`.

Expected output: Label coverage, accuracy on reviewed labels, accuracy when all events are opened for the demo, and error counts by review path.

Concept to check: A model can look good if we only inspect selectively reviewed labels, while errors may be hidden in the unreviewed range.

```python
# This example checks how evaluation can become biased when only selectively reviewed labels are used.
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

events = pd.DataFrame(
    [
        {"event_id": "A", "risk_score": 0.92, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "B", "risk_score": 0.88, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "C", "risk_score": 0.81, "manually_reviewed": 1, "actual_failure_for_demo": 0},
        {"event_id": "D", "risk_score": 0.76, "manually_reviewed": 1, "actual_failure_for_demo": 1},
        {"event_id": "E", "risk_score": 0.69, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "F", "risk_score": 0.62, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "G", "risk_score": 0.55, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "H", "risk_score": 0.48, "manually_reviewed": 0, "actual_failure_for_demo": 0},
        {"event_id": "I", "risk_score": 0.37, "manually_reviewed": 0, "actual_failure_for_demo": 1},
        {"event_id": "J", "risk_score": 0.29, "manually_reviewed": 0, "actual_failure_for_demo": 0},
    ]
)

reviewed = events[events["manually_reviewed"].eq(1)]

model = DecisionTreeClassifier(random_state=0, max_depth=2)
model.fit(reviewed[["risk_score"]], reviewed["actual_failure_for_demo"])
events["predicted_from_reviewed_only"] = model.predict(events[["risk_score"]])
events["error"] = events["predicted_from_reviewed_only"].ne(events["actual_failure_for_demo"])

print("label coverage")
print(events.groupby("manually_reviewed")["event_id"].count().to_dict())
print("failure rate in reviewed labels:", reviewed["actual_failure_for_demo"].mean())
print("failure rate in all events for demo:", events["actual_failure_for_demo"].mean())
print(
    "accuracy on reviewed labels:",
    accuracy_score(reviewed["actual_failure_for_demo"], model.predict(reviewed[["risk_score"]])),
)
print(
    "accuracy on all events for demo:",
    accuracy_score(events["actual_failure_for_demo"], events["predicted_from_reviewed_only"]),
)
print("errors by review path:", events.groupby("manually_reviewed")["error"].sum().to_dict())
print(
    events[
        [
            "event_id",
            "manually_reviewed",
            "actual_failure_for_demo",
            "predicted_from_reviewed_only",
            "error",
        ]
    ].to_string(index=False)
)
```

Expected output:

```text
label coverage
{0: 6, 1: 4}
failure rate in reviewed labels: 0.75
failure rate in all events for demo: 0.6
accuracy on reviewed labels: 1.0
accuracy on all events for demo: 0.7
errors by review path: {0: 3, 1: 0}
event_id  manually_reviewed  actual_failure_for_demo  predicted_from_reviewed_only  error
       A                  1                        1                             1  False
       B                  1                        1                             1  False
       C                  1                        0                             0  False
       D                  1                        1                             1  False
       E                  0                        1                             1  False
       F                  0                        0                             1   True
       G                  0                        1                             1  False
       H                  0                        0                             1   True
       I                  0                        1                             1  False
       J                  0                        0                             1   True
```

If we look only at reviewed labels, the accuracy is `1.0`. But when all events are opened for the demo, accuracy drops to `0.7`, and all three errors are on the `manually_reviewed=0` path. This output shows that cases with confirmed labels may not represent all events. In real operations, we may not know the result of unreviewed events, so it is even more important to write together whether a missing label means normal or unchecked, and by what rule a person reviewed only some events.

## A Small Diagram

The key point in this section is not to read `confirmed labels that remain only on reviewed cases` as if they were the answer table for all events. Once confirmed labels appear, the `meaning of missing labels`, the `review path`, and possible `bias` should be written beside them so the interpretation is not overstated.

--8<-- "assets/part-03/chapter-08/p3-8-6-mermaid-01-en.mmd"

## Sources and References

- Google for Developers, `Machine Learning Glossary`, `labeled example`. It provides the basic frame that a label is result information attached to an example, which supports this section's explanation that if confirmed labels remain only for some cases, that labeled set may not represent the same range as the set of all events. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Himabindu Lakkaraju, Jon Kleinberg, Jure Leskovec, Jens Ludwig, Sendhil Mullainathan, `The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables`, KDD 2017. It explains that in selectively labeled data, observed outcomes can be consequences of earlier human decisions rather than a random sample of the whole population, which directly supports this section's warning not to read labels left only on reviewed cases as the answer table for all events. [https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. It offers a provenance perspective for recording what review procedure produced a given result, which provides a general basis for this section's claim that the review path and the meaning of missing labels should be written together when interpreting selectively labeled cases. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
