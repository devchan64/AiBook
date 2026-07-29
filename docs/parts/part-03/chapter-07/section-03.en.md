# P3-7.3 What Is a Baseline the Reference For

> Section ID: `P3-7.3`
> Version: `v2026.07.25`

A [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) is the reference that decides `what should the current state be compared against`. The reason a baseline is needed in Part 3 is that the state of a recent range, a particular action, or a particular entity should not be read only as an absolute value. It has to be read side by side with the usual structure.

For example, even if the average flow of the most recent 20 cases is 2.1, that value alone is not enough. We also need to see whether the average of the usual range was 2.45, whether recent variability has grown compared with usual, and whether the late-stage decline pattern has become stronger than usual. Only then can we finally say `what changed`. So a baseline is not `a model-evaluation reference`, but `a state-comparison reference`.

## Why a Baseline Is Needed First

Part 3 is not yet evaluating models. What is first needed here is to compare the recent range and the usual range in the same unit, and read whether change exists or not. That is why the baseline appears as the comparison premise for building columns such as recent average, variability, pattern, and segment difference.

For example, if the average flow of the recent 20 cases is 2.1 and the [baseline window](/AiBook/en/reference/concept-glossary-alpha/b/#baseline) average is 2.45, then what we first read is `a difference of -0.35`. This difference is not yet model performance. It is the result of state comparison.

| What becomes readable when a baseline exists | What becomes blurred without a baseline |
| --- | --- |
| The difference between recent range and usual range | We only see whether the current value is large or small |
| Difference values, variability differences, pattern differences | It becomes hard to explain what is different from usual |
| Signals that need review | The reason for raising a warning candidate becomes weak |

Only after passing through this stage can we decide `what can become a prediction problem` and what should remain a [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure). The meaning of baseline that Part 3 should hold on to also reaches only this far. In other words, the baseline of the current section is `the reference that lets us read the difference of the current state side by side with the usual structure`.

## Two Common Misunderstandings

The two most common misunderstandings are these.

First, some people feel that once a baseline exists, interpretation is already finished automatically. But a baseline is only a comparison reference. Interpretation sentences and review judgment still have to be built in the next stage.

Second, some people think absolute values are enough and pass lightly over the baseline. But then the basis for deciding what was actually a change, and what could have become a prediction problem, becomes weak from the start.

| Misunderstanding | More accurate statement |
| --- | --- |
| If a baseline exists, the conclusion is also automatically fixed | A baseline is a state-comparison reference, and interpretation and judgment come after it |
| Looking only at absolute values is enough for judging change | To see what differs from usual, we first need a comparison reference |

This section is more accurate when read not through the dictionary definition of baseline, but as the problem of `what reference measurement should be placed in order to read change`. So a baseline should be read as `a reference measurement for state comparison`, separated from model-evaluation terminology.

## A Small Diagram

The core point of this section is that `the usual structure` and `the current state` should not be viewed in isolation. Once a `baseline` connects them, the difference becomes readable. A baseline does not replace the absolute value; it acts as the reference line for reading state change.

--8<-- "assets/part-03/chapter-07/p3-7-3-mermaid-01-en.mmd"

## Sources and Further Reading

- National Cancer Institute, `baseline`. Because it explains baseline as the standard against which later change is compared after an initial measurement is set, it provides a general basis for reading baseline in this section as `a state-comparison reference`. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the definition of a reference period used to compare other times, it reinforces the explanation in this section that the current range and the usual range should be placed side by side so the direction of change can be read. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
