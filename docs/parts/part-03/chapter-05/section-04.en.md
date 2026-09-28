# P3-5.4 Where Do We Cut the Input Window and How Do We Align Its Length

> Section ID: `P3-5.4`
> Version: `v2026.09.19`

The previous section represented the same records as a summary vector or sequence input. Either way, an [input window](/AiBook/en/reference/concept-glossary-alpha/m/#model-input) specifies which observations form one input. **Different lengths are not inherently an error.** Choose length handling to suit the time or phase being compared and the model’s input format.

## Specify Whether Boundaries Are Included

Suppose fictional action A starts at 0 seconds and ends at 40, while B starts at 0 and ends at 80. These are elapsed times relative to each action’s start, not simultaneous clock times. We first compare completed records.

Observations arrive once per second, with **the start included and the end excluded**. `[0, 40)` includes 0 but excludes 40. A has 40 observations at seconds 0–39; B has 80 at seconds 0–79. Completion time is a separate record in this example, not the final sensor-observation time.

| Item | A | B |
| --- | --- | --- |
| Start and end | 0 s, 40 s | 0 s, 80 s |
| Full observation window | [0, 40) | [0, 80) |
| Final 10 seconds | [30, 40): 10 points | [70, 80): 10 points |
| Final 25% | [30, 40): 10 points | [60, 80): 20 points |

B’s final 25% lasts `80×0.25 = 20 seconds` and starts at `80−20 = 60 seconds`. Include the observation at 60 and exclude 80. For A, the final ten seconds and final 25% coincide; for B they differ. Using the terms interchangeably changes which records are included.

## Time Alignment and Progress Alignment Answer Different Questions

Define completed-action progress as `elapsed time ÷ actual total duration`. Time alignment matches seconds since the start; progress alignment matches relative positions within total duration.

| Comparison criterion | A’s position | B’s position | What is aligned |
| --- | --- | --- | --- |
| 30 seconds after start | 30/40 = 75% | 30/80 = 37.5% | Equal elapsed time |
| 75% progress | 0.75×40 = 30 s | 0.75×80 = 60 s | Equal relative position |

“What is the value 30 seconds after start?” differs from “What is the shape in the final 25%?” Progress alignment matches relative positions but does not guarantee that equal percentages represent the same physical process phase. Check actual transition events or state records when phase meaning must align.

The names `early/mid/late` in [P3-5.1](section-01.en.md) do not define their own boundaries. As a new illustrative rule, take `early=[0,25%)`, `mid=[25%,75%)`, and `late=[75%,100%)`. A becomes [0,10), [10,30), [30,40); B becomes [0,20), [20,60), [60,80). This is a rule for this example, not an inference about the original P3-5.1 CSV assignment.

Assign A’s observations at 10 and 30 seconds and B’s at 20 and 60 seconds. The answers are middle and late for both. Boundary observations enter the interval on their right, avoiding duplicate inclusion. Since widths are 25%, 50%, and 25%, their time means must not be combined with equal weights to obtain the overall time mean.

## Equal Spacing Does Not Mean Equal Point Counts

Resampling represents values at new intervals or positions. Even with one-second spacing for both actions, these boundary rules give 40 points for A and 80 for B. Standardizing spacing does not create fixed-count inputs.

| Length-handling choice | Input in this example | Information and limitation to retain |
| --- | --- | --- |
| Keep variable lengths | A: 40, B: 80 points | Compatible model/input format and actual lengths |
| Crop to common [0,40) | 40 points each | B’s final 40 seconds are excluded |
| Average four equal progress bins | Four means each | Each bin covers 10 s for A and 20 s for B; detail is summarized |
| Pad A to 80 positions | A: 40 observations + 40 fillers; B: 80 observations | An indicator distinguishing filled positions from observations |

Four-bin averaging is aggregation by relative position, unlike representing data at one-second spacing. Padding also creates no new observations. If actual flow can be zero, distinguish zero padding from a measured zero. A design supporting variable lengths may require neither cropping nor padding.

## Before Completion, Actual Final Duration Is Not Yet Known

Now predict for B at 30 seconds. Assume observations arrive immediately upon measurement and define the input as the latest ten seconds `[20,30)`, namely observations at seconds 20–29. Including the 30-second observation would be a separate boundary choice; this rule excludes it.

After completion we know B lasted 80 seconds, making its final 25% [60,80). At the 30-second prediction time, however, the actual final duration has not yet been established, and those observations do not exist yet. Using retrospectively calculated final progress as if known then exceeds the available-information boundary.

If an expected duration of 80 seconds was already in the operating plan, progress relative to that planned duration could be a separate input candidate. It is not the eventual actual progress; retain the plan version available at prediction time. This distinguishes completed-record analysis from prediction during an action.

## Choose the Representation After Defining the Window

The same window can yield summary features or an ordered input. The diagram shows the boundary decisions shared by both choices.

```mermaid
--8<-- "assets/part-03/chapter-05/p3-5-4-mermaid-01-en.mmd"
```

Record start/end events, boundary inclusion, alignment, observation spacing, length/missingness/padding handling, prediction time, and available information. When aligning by progress, preserve original duration too, so similar relative shapes can still be distinguished by elapsed time.

## Checklist

- Can you state why [0,40) contains 40 observations under these sampling and boundary assumptions?
- Can you distinguish B’s final ten seconds [70,80) from its final 25% [60,80)?
- Have you calculated how equal 30-second positions differ from equal 75% progress?
- Can you distinguish one-second spacing, fixed point counts, and bin averages?
- Can you explain why eventual actual duration is unavailable before completion?
- Have you retained original lengths and padding indicators to identify actual observations?

## Sources and Further Reading

- TensorFlow, [Time series forecasting](https://www.tensorflow.org/tutorials/structured_data/time_series){: target="_blank" rel="noopener noreferrer" }. Provides general examples specifying input-window widths and target positions. The 40/80-second durations, progress bins, and boundary convention here are our fictional design, not universal segmentation standards. / Accessed: 2026-09-19
