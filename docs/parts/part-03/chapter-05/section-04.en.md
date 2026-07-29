# P3-5.4 Where Do We Cut the Input Window and How Do We Align Its Length

> Section ID: `P3-5.4`
> Version: `v2026.07.25`

If a [source time series](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-source-data) is not yet a learning [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input) by itself, one more concrete question immediately remains. `Then where should the real input begin and end?` `If actions have different lengths, how can we treat them like the same kind of input?` The [input window](/AiBook/en/reference/concept-glossary-alpha/m/#model-input-window) is the data-modeling decision that answers exactly these questions.

An input window should not be cut by first choosing `a length that is convenient for the model`. It should be cut only after deciding `what should count as one input in this problem`.

Up to the previous section, the flow asked what should remain in a `one-row feature table`. From this section onward, we check whether the same source time series can also be read as an input structure that preserves time order. In other words, the key point here is that only after we decide where to cut and how to align do we branch into whether to fold it into a summary input or keep the order.

## Why an Input Window Is Needed

Raw time series usually have different lengths, and the meanings of the start point and end point can also differ. One action may last 40 seconds while another lasts 75 seconds. One sensor may change sharply in the early phase, while another may differ only in the late phase. In this state, saying `let's feed it in as-is` really means handling different lengths and different semantic ranges as if they were one uniform bundle.

| Problem if we leave it as-is | Why immediate comparison becomes hard |
| --- | --- |
| Actions have different lengths | It is hard to say one input contains the same amount of information as another |
| The meanings of the start and end points differ | It is hard to say values at the same position belong to the same stage |
| Important changes appear only in certain ranges | If we feed the whole thing in at once, the key range can be blurred |

So an input window is not just a cutting technique. It is the act of deciding `what range should count as one comparison unit`.

## Four Things That Must Be Fixed First

When deciding the input window, at least the following four things should be closed first.

| What to decide first | Turned into a question |
| --- | --- |
| Start point | Where does the meaning of one action begin? |
| End point | Up to where should the same input include data? |
| Length criterion | By what common rule will samples with different lengths be aligned? |
| Alignment criterion | Will they be aligned by time itself, or by progress? |

These four things are not needed only for sequence models. The same judgment is already hidden even when we build a [summary table](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-summary-table). Dividing into early, middle, and late ranges also means that we already decided the input window and the alignment criterion first.

## Several Possible Window Designs from the Same Source Data

Suppose we have a time series for one full action. Even with the same data, there can be many ways of cutting the window.

| Window design | When it is more natural | Limitation that remains |
| --- | --- | --- |
| Keep the whole range from start to end as one input | When the full shape of one action matters | Large length differences are hard to align |
| Divide again into the same number of ranges by progress | When comparing early/mid/late structure matters | Some absolute time difference can disappear |
| Cut only the most recent N seconds | When the final range matters, such as signs right before termination | Early context can drop out |
| Keep only the range around a reference event | When patterns near a specific trigger matter | The whole action structure becomes less visible |

So the input window is not `one correct answer`. It is a structural choice that changes with the problem question.

## What Is Kept and What Is Lost When We Align Length

Aligning lengths is not just the job of making the number of values match. The moment we align lengths, some information is kept and some remains less directly visible.

| Length-alignment method | What mainly remains | What remains less directly |
| --- | --- | --- |
| Progress-based segmentation | Relative structure by action stage | Differences in actual elapsed time |
| Regular-interval resampling | Shape along the time axis | Fine momentary changes |
| Fixed-length clipping | Comparison of same-length inputs | Information outside the clipped range |
| Collapsing into summary [features](/AiBook/en/reference/concept-glossary-alpha/f/#glossary-feature) | Overall tendency and comparable numbers | Detailed time-series shape |

So the length-alignment method should not be chosen only for model convenience. For example, if differences in actual time are important, keeping only a progress-based view may discard important information. Conversely, even if total time varies, progress-based segmentation may be better if the key question is `does the action collapse in the late phase?`

## Looking Again Through One Scene

Suppose action A lasts 40 seconds and action B lasts 80 seconds. Both show a structure of early stability and late decline, but under absolute time, the location of the decline can appear different.

| Action | How it looks by absolute time | How it looks when read again by progress |
| --- | --- | --- |
| A | Sharp drop after 30 seconds | Decline in the last 25% range |
| B | Sharp drop after 65 seconds | Decline in the last 25% range |

If the question is `at what second does the sharp drop happen?`, absolute-time alignment matters more. If the question is `does collapse appear in the final stage of the action?`, progress-based alignment is more natural. In other words, the window and alignment criteria are determined by the question, not by the data itself.

Once the input window is decided, the same judgment can continue in two directions.

| Direction after the input-window decision | What remains |
| --- | --- |
| Build summary features | One-row summary input |
| Preserve segment order | A grouped input that keeps time order |

For example, if one action is aligned again into 10 progress ranges, then two choices appear next.

1. We can turn the 10 range averages and difference values into summary features and fold them into a one-row input.
2. We can preserve the order of the 10 ranges themselves and keep them as a candidate input structure with time order remaining.

So deciding the input window explains, on one side, where the summary features came from, and on the other side, by what criteria an input structure with preserved order was made. Only after the window is fixed can we also speak consistently about whether the next branch is a `summary input` or an `order-preserving input`.

The small diagram below makes it clearer why the same window decision creates two candidate input structures.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-4-mermaid-01-en.mmd"
```

The boundary should also be kept clear here. This section answers `why was the input window cut this way?` It is not the place that explains what learning structure fits best on top of that input.

| Question | Answered in this section? | Postponed from here? |
| --- | --- | --- |
| Where does one input start and end? | Yes | No |
| By what criterion will [samples](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample) of different length be aligned? | Yes | No |
| How will this input structure be used for learning? | No | Yes |
| How should we implement padding, masking, or architecture details? | No | Yes |

The input window is not a format created because the model demanded it. It is the result of data modeling that decides what should count as one comparable input. Once written this way, even when we later read a longer input structure, we still look first at `why was the input window cut this way?` It also becomes clear that summary features are already results built on a particular window and alignment criterion.

## Sources and Further Reading

- Google for Developers, `Machine Learning Glossary`: `labeled example`. Because an example is the unit where features and labels are defined together, it supports the central point of this section that before calling a raw time series an input, we should first fix the start point, end point, and length criterion of one input. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- W3C, `PROV-Overview`. Because the provenance framework says identifying an object, derivation, and reproducibility should be supported, it reinforces the higher-level frame that the rules behind the input window and the alignment criterion should remain reproducible. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general idea of a reference period for comparison, it supports the judgment in this section that the question must first decide whether absolute time or progress will serve as the comparison criterion. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
