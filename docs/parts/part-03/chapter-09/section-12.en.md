# P3-9.12 Even Under the Same Target Name, Why Must You First Write Which Error Hurts More

> Section ID: `P3-9.12`
> Version: `v2026.07.11`

Even under the same target name, which mistake hurts more can vary from problem to problem. Even in a problem that predicts `review_needed`, it depends on the operating context whether missing a risky case is more dangerous or whether unnecessarily sending a case to review is more burdensome. Even with the same target, the cost of a missed case and the cost of an unnecessary catch can differ, so this difference should be written down first in order to make clear which judgment you are trying harder to reduce.

| Error type | What can happen in operations |
| --- | --- |
| False negative | A risky case can be missed and spread into a larger abnormality |
| False positive | People can spend time unnecessarily, increasing review burden |

| Note to write first | Why it is needed |
| --- | --- |
| Which mistake hurts more? | To fix which kind of judgment should be reduced first |
| In what form does that cost appear in real operations? | To explain it as an action burden rather than only a number |
| What are you trying harder to reduce right now? | To fix the interpretation direction even under the same target |

## Why Error Cost Changes the Interpretation of the Target

Even with the same `review_needed` target, not every prediction score is read in the same way. In some problems, `false negatives` hurt more, so it is better to miss fewer risky cases even if that means sending somewhat more items into the review queue. In other problems, `false positives` hurt more, so it is better to keep the review queue narrower. What changes here is not just a single threshold number, but `the judgment structure through which this target is interpreted`.

Suppose the model scores look like this.

| event_id | score | Reading 1: miss cost is high | Reading 2: over-detection cost is high |
| --- | --- | --- | --- |
| A | 0.82 | Move directly to the top of the review queue | Move to the top of the review queue |
| B | 0.64 | Include in the review queue | Hold for now |
| C | 0.41 | Keep as a secondary review candidate | Exclude |

If the cost of missing a case is high, then including `B` in the review queue is more natural. If the cost of over-detection is high, then it may be more natural to hold `B` and look only at `A`. So even under the same score and the same target name, a different error-cost structure changes both review-queue priority and threshold interpretation.

This section is therefore not only a section that defines `false negative` and `false positive`. It is a section that makes you reread the current problem as `what kind of mistake are we trying harder to reduce`. Once the target name has been fixed, the next thing to write is which kind of error hurts more under that target, so that scores, thresholds, and review-queue priority are all read in the same direction.

So rather than closing the problem with accuracy alone, you should first ask why the intention to reduce one kind of error more than the other has to be written down first. This section groups together `miss cost`, `over-detection cost`, and `judgment-rule adjustment`, so that the error-cost structure is fixed first before it changes how the target is interpreted.

## Sources and References

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, accessed 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Thresholds and the Confusion Matrix*, threshold choice under asymmetric costs. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" }
