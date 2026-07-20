# P5-14.9 Supplementary Learning: Why Does Layer Normalization Align the Value Baseline?

> Section ID: `P5-14.9`
> Version: `v2026.07.19`

In P5-14.2, we saw that layer normalization organizes the value range inside a Transformer block. But the word `normalization` is easily confused with input preprocessing, batch normalization, and regularization.

In a Transformer block, layer normalization is not a device that chooses new meaning. It adjusts the mean and spread of the values inside one position representation so that they lie on a baseline that is easier for the next computation to handle.

When the terminology begins to scatter again, revisit the layer normalization entry in the concept glossary together with the four-part role split from P5-14.2.

## What It Means for the Value Baseline to Shake

A representation inside a Transformer block is not one number. It is a vector with several axes. One axis may carry the action meaning `restart`, while other axes may carry contextual cues such as `held`, `risk`, or `condition`.

When self-attention and the feed-forward network change the representation, and the residual connection adds the original representation back in, the size and spread of the values can keep changing. In one block, some axes may become too large. In another block, the values may gather too narrowly. If this continues, the next attention or feed-forward computation receives inputs on a different baseline each time.

At the introductory level, this is enough:

| Shaken State | Why It Becomes a Problem |
| --- | --- |
| One representation axis is too large. | The next computation can be pulled too strongly toward that axis. |
| Values are gathered too narrowly. | Differences between axes can become too weak to read. |
| The value range changes greatly from block to block. | The next component has difficulty continuing computation from a similar baseline. |

Layer normalization does not solve this by deciding `which meaning matters`. It reorganizes the value range inside one position representation and creates an input state that the next computation can handle more easily.

## Matching Mean and Spread Inside One Position

The core of layer normalization is that it organizes values `inside one position representation`. It does not mix all tokens in a sentence to choose meaning. It uses the values in the current position’s representation vector as the basis for matching the mean and spread.

```mermaid
--8<-- "assets/part-05/chapter-14/layer-normalization-value-scale-en.mmd"
```

In this diagram, the earlier representation has already passed through attention, feed-forward, and residual connection, so its value range has shaken. Layer normalization reorganizes those values inside one position and passes them onward as a baseline from which the next computation can start.

The important boundary is this:

| Question | Component That More Directly Handles It |
| --- | --- |
| Which other token should this position refer to? | self-attention |
| How should the context-mixed current representation be changed? | feed-forward network |
| Should the original representation be prevented from being covered by new computation? | residual connection |
| Are the values in a range that the next computation can handle? | layer normalization |

Layer normalization answers the fourth question. So `organizing values` does not mean `erasing meaning` or `leaving only important meaning`. It means aligning the baseline so the next computation can handle the same kind of input more stably.

## How Is It Different from Batch Normalization?

The most common beginner confusion is to read layer normalization and batch normalization as the same thing. Both use the name normalization, but they use different statistics as their basis.

| Distinction | What Is Used as the Basis | How to Read It in the Transformer Context |
| --- | --- | --- |
| batch normalization | statistics across a batch of samples | batch composition and train/eval mode need to be considered together |
| layer normalization | values inside one sample, one position representation | the current position representation is aligned to the next computation baseline |

When reading batch normalization earlier in Part 5, the learning batch with several samples mattered. In contrast, inside a Transformer, it is more direct at the introductory level to read layer normalization as organizing the values inside one position representation.

This difference matters in real use as well. Language models can face varying sentence lengths, batch compositions, and generation-time states. Layer normalization uses the current position representation itself as the basis for organizing values, so it is a useful stabilization device inside repeated Transformer blocks.

## Why It Often Appears After Residual Connection

In Transformer explanations, residual connection and layer normalization often appear together. But they do not appear together because they do the same job.

The residual connection leaves the original input representation and the new computed result together. This addition helps preserve information flow, but it can also make the size and spread of values shake more. Layer normalization then aligns the combined representation into a range that the next computation can handle more easily.

| Stage | Central Question | Result |
| --- | --- | --- |
| new computation | How should the current representation be changed? | A new representation reflecting context appears. |
| residual connection | Should the original representation be kept together? | The original axis and the new representation remain together. |
| layer normalization | Is the result in a range the next computation can handle? | The value baseline is organized. |

So it is not enough to memorize `residual + normalization` as one bundle. Residual connection deals with information flow, and layer normalization deals with value range.

## Cases and Examples

### Case. When the Value Baseline Shakes in an Operations Sentence

Consider the `restart` position in `If pressure remains unresolved, restart is held`. Attention makes it refer to `pressure remains unresolved` and `held`, and feed-forward refines the current representation toward `a conditionally blocked action`. The residual connection leaves the original `restart` action axis together with that new representation.

Now the representation passed to the later block contains several cues together. Axes such as `restart`, `pressure unresolved`, `held`, `risk`, and `condition` can remain with different sizes. If some axes become too large, later computation can be pulled too strongly toward them. If values become too small or too narrowly gathered, differences between cues may not be read well enough.

Layer normalization does not newly decide whether `restart` or `held` is more important. It organizes the value range of the already-created current position representation so that the next block can start relationship reading and representation refinement again from a similar baseline.

| Cues Remaining Together in the Representation | What Layer Normalization Directly Does | What It Does Not Directly Do |
| --- | --- | --- |
| Values for `restart`, `held`, and `risk` axes differ greatly. | Aligns mean and spread to organize the next computation baseline. | Judges which cue is legally more important. |
| The original action axis and new risk axis remain together through residual. | Stabilizes the value range of the combined representation. | Creates a new path for preserving the original action axis. |
| The next attention will use this position again. | Creates an input state the next computation can handle more easily. | Chooses which token to look at again. |

The result to confirm in this case is that layer normalization is not a meaning judge. It is a computation-baseline organizer.

### Example. Passing Value-Range Shaking into an Experiment

Even if two representations both carry the direction `restart should be held`, the next computation can feel different if their value ranges differ greatly. If one axis is too large, if all values gather too narrowly, or if the value range changes greatly from block to block, the next attention and feed-forward computation receive inputs on a different baseline each time.

This difference is easy to blur if it is only described in words. So in the next example, we directly pass in three representations: `risk_axis_spike`, `too_narrow`, and `mixed_after_residual`. Then we inspect how the mean, spread, and next computation score change before and after normalization. The baseline to hold first is that `representation meaning` and `value scale` are not the same problem.

## Practice and Examples

### Example. Check the Baseline Before and After Layer Normalization

This example is not code for memorizing the layer normalization formula. It is an experiment for seeing how the input feel of the next computation changes when the value range inside one position representation shakes and then the mean and spread are aligned.

| Value to Manipulate | Output to Observe | Question to Confirm |
| --- | --- | --- |
| the large value in `risk_axis_spike` | `raw mean/std`, `norm mean/std` | How is the baseline organized when one axis is too large? |
| the value differences in `too_narrow` | `normalized values` | Do values gathered too narrowly regain a readable spread? |
| `probe` | `next score before/after` | How strongly was the next computation score pulled by the original value scale? |

```python
# This example compares mean, standard deviation, and next-score values before and after layer normalization to see how one position representation is rescaled.
import numpy as np

representations = {
    "risk_axis_spike": np.array([0.6, 8.0, 0.4, 0.5]),
    "too_narrow": np.array([0.48, 0.51, 0.49, 0.50]),
    "mixed_after_residual": np.array([2.0, 4.5, 1.0, 3.5]),
}

probe = np.array([0.2, 1.0, 0.3, 0.7])

def layer_norm(x, eps=1e-6):
    return (x - x.mean()) / (x.std() + eps)

for name, values in representations.items():
    normalized = layer_norm(values)
    raw_score = float(values @ probe)
    normalized_score = float(normalized @ probe)

    print(f"[{name}]")
    print("raw mean/std =", round(values.mean(), 3), round(values.std(), 3))
    print("norm mean/std =", round(normalized.mean(), 3), round(normalized.std(), 3))
    print("next score before/after =", round(raw_score, 3), round(normalized_score, 3))
    print("normalized values =", np.round(normalized, 3).tolist())
    print("---")
```

Read the output like this.

```text
[risk_axis_spike]
raw mean/std = 2.375 3.248
norm mean/std = -0.0 1.0
next score before/after = 8.59 1.036
normalized values = [-0.546, 1.732, -0.608, -0.577]
---
[too_narrow]
raw mean/std = 0.495 0.011
norm mean/std = 0.0 1.0
next score before/after = 1.103 1.252
normalized values = [-1.342, 1.342, -0.447, 0.447]
---
[mixed_after_residual]
raw mean/std = 2.75 1.346
norm mean/std = 0.0 1.0
next score before/after = 7.65 1.188
normalized values = [-0.557, 1.3, -1.3, 0.557]
```

The first case is a representation where one risk axis is too large. After layer normalization, the mean is nearly 0 and the standard deviation is close to 1, so the degree to which the next computation is pulled by the original value size is reduced. The second case is a representation where the values are gathered too narrowly. After normalization, differences between axes are spread back into a readable range.

Explanation: The important point in this example is not memorizing each normalized value as an answer. Layer normalization does not choose new meaning. It aligns the value baseline inside one position representation into a state that the next computation can handle more easily. So the change in `next score before/after` does not mean that the meaning judgment changed. It means the same probe was computed from a more organized input baseline.

### Practice. Diagnose the Value-Range Problem in Words

Write one sentence explaining why layer normalization is needed in each situation below.

| Situation | Possible Answer | Explanation |
| --- | --- | --- |
| After residual, one axis value became too large. | The value baseline should be organized so the next computation is not pulled too strongly by one axis. | This is the view of reducing value-size imbalance. |
| Across several blocks, the representation value range keeps changing. | The value range should be aligned so repeated blocks can continue computation from a similar input baseline. | This is the view of stabilizing deep repetition. |
| Values inside one position representation are gathered too narrowly. | The spread should be adjusted so differences between axes can be read in the next computation. | Values that are too large are not the only problem; values that are too narrow can also be a problem. |

Explanation: This practice is not a formula calculation. It checks in words that layer normalization is not `a stage that chooses the answer`, but `condition organization that lets the next computation read the representation`.

## Checklist

- Can you explain layer normalization as matching the mean and spread of values inside one position representation?
- Can you explain the basis difference between layer normalization and batch normalization?
- Can you distinguish residual connection and layer normalization as `information-flow preservation` and `value-baseline organization`?
- Can you explain that layer normalization does not directly choose meaning or token relationships?

## Sources and References

- Jimmy Lei Ba, Jamie Ryan Kiros, Geoffrey E. Hinton, `Layer Normalization`, arXiv, 2016, checked on 2026-07-19. [https://arxiv.org/abs/1607.06450](https://arxiv.org/abs/1607.06450){: target="_blank" rel="noopener noreferrer" }
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-06-29.
