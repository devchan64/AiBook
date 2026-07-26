# P3-9.2 Why Should Some Problems Remain Comparison Reports All the Way Through

> Section ID: `P3-9.2`
> Version: `v2026.07.25`

Pushing every real problem into a [label prediction](/AiBook/en/reference/concept-glossary-alpha/l/#glossary-label-prediction) problem is not good data modeling. In some cases, a [comparison report](/AiBook/en/reference/concept-glossary-alpha/c/#glossary-comparison-report) is more honest and fits the current data state better. This is especially true when cause labels are weak, or when what the decision-maker actually wants is not `correct classification` but `choosing what to inspect first right now`. Here, you also need to organize the possibility that some problems are more correctly left as comparison reports all the way through instead of being raised upward.

At this point, the structure `input -> correct label -> automatic decision` comes to mind first, so real problems can start to feel as if they must all fit that frame. But in real data, `what should be shown first` is often more important than `what should be matched correctly`. If such a problem is forced into a classification problem, it becomes easy to create exaggerated automation while label quality is still weak.

Situations where a comparison report is more appropriate usually look like the following.

- It is important to show the recent change direction relative to the usual state first.
- Review priority is more practical than confirmed labels.
- The cause of the change cannot yet be automatically fixed.
- Human follow-up checking is part of the judgment procedure.

For example, it can already be quite useful to organize recent-window mean, variability, pattern difference, difference from baseline, and whether review is needed. In this case, what matters is not `what was matched`, but `what was shown first`. A good comparison report is therefore not just an intermediate artifact. It becomes one form of actual follow-up judgment.

By contrast, moving to a prediction problem requires at least the following conditions.

- The [target label](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target) is defined relatively stably.
- The sample unit and label unit match each other.
- The sample structure is organized enough to design train/evaluation splits and evaluation.

The difference between the two approaches can be summarized like this.

| Category | Comparison report | Prediction problem |
| --- | --- | --- |
| Central question | What should be reviewed first? | What should be automatically matched? |
| Labels needed | Can start even when weak | Must be relatively stable |
| Output | Priority table, comparison sentence, [review queue](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-review-queue) | Target label, predicted value, evaluation result |
| Human role | Central in follow-up checking | Central in evaluation and exception handling |

This table shows that a comparison report is not `a temporary artifact used only because prediction is not possible`. It is a different problem setup from the start. A comparison report helps the reader read the state and decide the next action. A prediction problem is a structure for automatically matching a relatively stable target label.

In practice, it is safer to judge first whether `it is more honest to leave this as a comparison report`, as in the following table.

| Current state | More natural output | Reason |
| --- | --- | --- |
| There are almost no cause labels, and only change comparison is possible | Comparison report | You can say what changed, but it is still hard to fix the cause |
| Review priority can be set, but confirmed labels are weak | Comparison report or review queue | The decision-maker wants to know what to look at first, while classification answers are still weak |
| Target label and evaluation structure are relatively stable | Prediction problem | There is a basis for defining what should be automatically matched |

The difference between comparison reports and prediction problems becomes clearer in the small table below.

| event_id | diff | repeatability | review_needed | cause_label |
| --- | --- | --- | --- | --- |
| A | -0.35 | high | 1 | none |
| B | -0.08 | low | 0 | none |
| C | -0.31 | high | 1 | none |

## A Small Diagram

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-2-mermaid-01-en.mmd"
```

This diagram shows that a comparison report is not just a stopover used because prediction is not yet possible. For some questions, it can remain the better output all the way through. If what is needed first is to show `what changed`, then a comparison report is natural, and only when stable target labels exist does it make sense to move to a prediction problem. Good data modeling is not the act of defining the most complex problem from the start. It is the act of honestly choosing the output form that matches the current data state. If change explanation and review priority matter more, and stable target labels are still weak, then keeping a comparison report through to the end can be more accurate.

A comparison report is therefore not a temporary alternative before prediction. For some questions, it can itself be the most correct output structure.

## Sources and References

- U.S. Bureau of Labor Statistics (BLS), *BLS Handbook of Methods: Glossary*, base period. Used to check the idea that a base period or point in time can serve as a reference for comparison. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute (NCI), *NCI Dictionary of Cancer Terms: baseline*, baseline. Used to check the idea that an initial measurement can serve as a comparison point for later change. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Machine Learning Glossary*, `proxy labels`, `label`. Used to check what labels and proxy labels mean and why proxy labels need care. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Lakkaraju, Kleinberg, Leskovec, Ludwig, Mullainathan, *The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables*, KDD 2017. Used to check why evaluation and problem framing can be distorted when observed outcomes are selected by prior human decisions. [https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres](https://www.kdd.org/kdd2017/papers/view/the-selective-labels-problem-evaluating-algorithmic-predictions-in-the-pres){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
