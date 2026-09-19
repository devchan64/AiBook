# P3-5.3 Why Can We Not Immediately Call Raw Time Series a Learning Input

> Section ID: `P3-5.3`
> Version: `v2026.09.19`

Raw time series can be used as [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input). Having records does not, by itself, specify an input’s boundary, order, length, or target. **Handcrafted summaries are a representation choice; defining what information forms one input is necessary for either representation.**

## Build Two Inputs from the Same Four Observations

These are fictional flow records for two actions. Each action is measured once per second from its start at 0 seconds through its end at 3 seconds. Assume all four readings are available when the action ends. Flow is in L/min.

| event_id | 0 s | 1 s | 2 s | 3 s |
| --- | ---: | ---: | ---: | ---: |
| A | 1 | 3 | 3 | 1 |
| B | 3 | 1 | 1 | 3 |

Consider predicting, at action completion, a review outcome finalized later. One action is one [sample](/AiBook/en/reference/concept-glossary-alpha/s/#glossary-sample). Link the outcome label to the same `event_id` without mixing it into input values. The table below shows input candidates only; no actual outcome labels or trained model are supplied.

| Representation | Input for A | Input for B | Meaning of elements |
| --- | --- | --- | --- |
| Summary vector | `[2, 3]` | `[2, 3]` | In order: `[mean flow, maximum flow]` |
| Sequence input | `[[1], [3], [3], [1]]` | `[[3], [1], [1], [3]]` | Outer order: 0→3 seconds; inner entry: one flow value |

A vector is a collection of values in a specified order. A’s mean is `(1+3+3+1)/4 = 2`, and its maximum is 3. B has the same two summaries, so they cannot distinguish the sequences. A model receiving only mean and maximum sees identical inputs for these two cases.

The sequence has **4 time steps × 1 value per step**. It preserves that A’s middle two observations are high, whereas B’s first and last are high. It does not preserve everything that happened between the four measurements. Keeping order also does not guarantee that any model will learn the distinction well.

## The Summary Vector Is Not a Required Intermediate Step {#a-small-diagram}

The two branches below are alternatives derived from the same observations. Constructing sequence input does not require passing through a mean-and-maximum vector.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-3-mermaid-01-en.mmd"
```

For questions answered by mean and maximum, a small summary vector is easy to compare. If the timing of high values matters, a sequence or other order-sensitive features may be needed. You can retain sequence input alongside a summary table for human inspection. The usefulness of a summary for comparison does not make it a mandatory model input.

## Specify What Both Representations Need

| Decision | Choice in this example | Risk if unspecified |
| --- | --- | --- |
| Sample boundary and identifier | Seconds 0–3 of one action, `event_id` | Records from different actions may be merged |
| Values and order | Flow in L/min, increasing time | Feature or time order may be mixed up |
| Input length | Four time steps in this example | Three observations may be treated as an equivalent input |
| Prediction time and available information | Observations received by completion at 3 s | Information from after prediction may enter the input |
| Target and linkage | Later review outcome linked to the same action | Another action’s outcome may be attached, or the outcome included as input |

Four steps are a choice for this case, not a universal requirement. For unequal action lengths, specify a format supporting variable length, cropping, or padding. Filled entries need a way to distinguish them from actual observations. Record what information length handling removes or adds.

Suppose A’s 2-second observation is missing. Keeping only `[1, 3, 1]` pulls the original 3-second value into the third position. Filling with zero gives `[1, 3, 0, 1]` and mean 1.25, but zero was never observed. For this example, we defer that input and record the missing position. A design that fills values must define both the filling rule and the missingness indicator.

## Earlier Prediction Changes Which Values Are Available

Now predict the eventual outcome at 1 second. Available observations are `[1, 3]` for A and `[3, 1]` for B. The 2- and 3-second values are not yet available. A summary of all four observations cannot be computed then either, so it is excluded from the input candidates.

Summarizing just the first two steps gives `[mean 2, maximum 3]` for both actions, while their ordered inputs still differ. Preserving order and deciding how far observations are available are separate decisions. Neither a later outcome label nor observations beyond prediction time belong in that input.

External review labels are not required for every learning task. A separate next-value task from A can be defined as `0–2 s input [1, 3, 3] → 3 s target 1`. For B it is `[3, 1, 1] → 3`. Targets come from the records without human review labels, but the time boundary between input and future target is still necessary.

## Checklist

- Can you calculate the shared `[2, 3]` summary and explain what it loses?
- Can you explain both dimensions of the 4×1 sequence input?
- Have you specified sample boundaries, value order, length, and target even without handcrafted summaries?
- Can you distinguish missingness from a real zero or a shift in time positions?
- Do you exclude 2–3 s observations and summaries derived from them when predicting at 1 s?
- Can you distinguish external review labels from future targets constructed from records?

## Sources and Further Reading

- TensorFlow, [Time series forecasting](https://www.tensorflow.org/tutorials/structured_data/time_series){: target="_blank" rel="noopener noreferrer" }. Provides examples of sequence inputs with specified window widths, target positions, and input features. The A/B observations and summary/missingness exercises here are our fictional cases. / Accessed: 2026-09-19
