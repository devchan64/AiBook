# P3-9.12 Target Names and Error Costs

> Section ID: `P3-9.12`
> Version: `v2026.07.25`

_Subtitle: Why must you first write whether missed cases or false alarms hurt more, even for the same target?_

Even under the same [target](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-target) name, which mistake hurts more can vary from problem to problem. Even in a problem that predicts `review_needed`, it depends on the operating context whether missing a risky case is more dangerous or whether unnecessarily sending a case to review is more burdensome. Even with the same target, the cost of a missed case and the cost of an unnecessary catch can differ, so this [error cost](/AiBook/en/reference/concept-glossary-alpha/e/#glossary-error-cost) difference should be written down first in order to make clear which judgment you are trying harder to reduce.

| Error type | What can happen in operations |
| --- | --- |
| [False negative](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-false-negative) | A risky case can be missed and spread into a larger abnormality |
| [False positive](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-false-positive) | People can spend time unnecessarily, increasing review burden |

| Note to write first | Why it is needed |
| --- | --- |
| Which mistake hurts more? | To fix which kind of judgment should be reduced first |
| In what form does that cost appear in real operations? | To explain it as an action burden rather than only a number |
| What are you trying harder to reduce right now? | To fix the interpretation direction even under the same target |

## Why Error Cost Changes the Interpretation of the Target

Even with the same `review_needed` target, not every prediction score is read in the same way. In some problems, false negatives hurt more, so it is better to miss fewer risky cases even if that means sending somewhat more items into the [review queue](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-review-queue). In other problems, false positives hurt more, so it is better to keep the review queue narrower. What changes here is not just a single [threshold](/AiBook/en/reference/concept-glossary-alpha/t/#glossary-threshold) number, but `the judgment structure through which this target is interpreted`.

Suppose the model scores look like this.

| event_id | score | Reading 1: miss cost is high | Reading 2: over-detection cost is high |
| --- | --- | --- | --- |
| A | 0.82 | Move directly to the top of the review queue | Move to the top of the review queue |
| B | 0.64 | Include in the review queue | Hold for now |
| C | 0.41 | Keep as a secondary review candidate | Exclude |

If the cost of missing a case is high, then including `B` in the review queue is more natural. If the cost of over-detection is high, then it may be more natural to hold `B` and look only at `A`. So even under the same [score](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-score) and the same target name, a different error-cost structure changes both review-queue priority and threshold interpretation.

The next example applies several thresholds to the same scores and calculates false-negative and false-positive costs separately. Here, the miss cost is 10 and the false-alarm cost is 2.

Problem situation: We want to see how total cost changes under the same `review_needed` scores when thresholds and error costs change.

Input: Each event's `score`, the actual result `actual`, threshold candidates, and error costs.

Expected output: Review-queue size, false-negative count, false-positive count, and total cost by threshold.

Concept to check: Threshold selection should be read together with which error cost matters more, not with accuracy alone.

```python
# This example checks how judgment cost changes with threshold and error-cost settings.
import pandas as pd
from sklearn.metrics import confusion_matrix

scores = pd.DataFrame(
    [
        {"event_id": "A", "score": 0.82, "actual": 1},
        {"event_id": "B", "score": 0.64, "actual": 1},
        {"event_id": "C", "score": 0.41, "actual": 0},
        {"event_id": "D", "score": 0.36, "actual": 1},
        {"event_id": "E", "score": 0.22, "actual": 0},
    ]
)

thresholds = [0.3, 0.5, 0.7]
miss_cost = 10
false_alarm_cost = 2

for threshold in thresholds:
    predicted = scores["score"].ge(threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(scores["actual"], predicted, labels=[0, 1]).ravel()
    total_cost = fn * miss_cost + fp * false_alarm_cost
    print(
        {
            "threshold": threshold,
            "queued": int(predicted.sum()),
            "false_negative": int(fn),
            "false_positive": int(fp),
            "total_cost": int(total_cost),
        }
    )
```

Expected output:

```text
{'threshold': 0.3, 'queued': 4, 'false_negative': 0, 'false_positive': 1, 'total_cost': 2}
{'threshold': 0.5, 'queued': 2, 'false_negative': 1, 'false_positive': 0, 'total_cost': 10}
{'threshold': 0.7, 'queued': 1, 'false_negative': 2, 'false_positive': 0, 'total_cost': 20}
```

A lower threshold makes the review queue larger, but it does not miss risky cases. A higher threshold makes the review queue smaller, but missed cases increase and total cost rises. The values to change in this example are `miss_cost`, `false_alarm_cost`, and `thresholds`. If the false-alarm cost is set higher, another threshold may become more natural. So even with the same target name, the error cost has to be written first so that score and threshold are interpreted in the same direction.

## A Small Diagram

Even with the same score, the review-queue flow changes depending on which kind of error you are trying harder to reduce.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-12-mermaid-01-en.mmd"
```

This section is therefore not only a section that defines `false negative` and `false positive`. It is a section that makes you reread the current problem as `what kind of mistake are we trying harder to reduce`. Once the target name has been fixed, the next thing to write is which kind of error hurts more under that target, so that scores, thresholds, and review-queue priority are all read in the same direction.

So rather than closing the problem with accuracy alone, you should first ask why the intention to reduce one kind of error more than the other has to be written down first. This section groups together `miss cost`, `over-detection cost`, and `judgment-rule adjustment`, so that the error-cost structure is fixed first before it changes how the target is interpreted.

## Sources and References

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, `ROC curve`. Used to check the term basis for false negatives and false positives, and the view that real threshold selection can be affected by different costs for different errors. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Google, *Thresholds and the confusion matrix*. Used to check that different thresholds change the counts of true/false positives and true/false negatives, and that a simple default threshold can be a poor choice when error costs are asymmetric. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
