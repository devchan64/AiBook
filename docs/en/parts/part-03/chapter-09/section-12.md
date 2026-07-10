# P3-9.12 Even Under the Same Target Name, Why Must You First Write Which Error Hurts More

> Section ID: `P3-9.12`
> Version: `v2026.07.10`

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

So rather than closing the problem with accuracy alone, you should first ask why the intention to reduce one kind of error more than the other has to be written down first. This section groups together `miss cost`, `over-detection cost`, and `judgment-rule adjustment`, so that the error-cost structure is fixed first before it changes how the target is interpreted.

## Sources and References

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, accessed 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Thresholds and the Confusion Matrix*, threshold choice under asymmetric costs. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" }

