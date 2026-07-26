# P5-14.3 Two Devices That Stabilize Deep Repetition

> Section ID: `P5-14.3`
> Version: `v2026.07.26`

_Subtitle: How do residual and normalization divide stabilization between information flow and value range?_

In P5-14.2, we saw how the current representation moves through attention, feed-forward, and residual addition. But a Transformer block does not only keep stacking new computation. It also has stabilization devices that leave the original representation and organize the value range.

Why are residual connection and layer normalization not secondary decoration in the Transformer block?

The core is not `stronger attention`, but `information flow that can endure deep repetition`.

## Questions Handled by Stabilization Devices

- What can go wrong if only new computation is repeated?
- Why does residual connection leave the original representation together?
- Why does layer normalization organize the value range before handing the representation to the next computation?

## What Shakes If We Trust Only New Computation?

When deep blocks repeat, representations keep changing. At that time, if new computation overwrites the original input axis too strongly, important cues can disappear. If the size and distribution of values shake, the next computation can also become unstable.

So a Transformer block usually keeps the following two intuitions together.

| Device | Problem it tries to prevent | First intuition to keep |
| --- | --- | --- |
| residual connection | new computation covers the original information too much | leave the original representation together |
| layer normalization | the value range shakes and makes the next computation unstable | organize the representation range |

## Cases and Examples

### Case. When the Action Token Must Not Lose Its Original Meaning

In an incident-response sentence, the action token has an original axis called `recovery state`. Even if attention and feed-forward reflect new context, if that original axis completely disappears, the current representation becomes unstable. The representation should differ depending on whether rollback was confirmed, but the basic meaning that the action token points to an action state should be preserved.

Here, residual connection preserves the action axis by leaving the new computation and the original representation together. Layer normalization organizes the result into a range that the next block can handle easily.

The criterion a person may quickly use is `a representation becomes better if it reflects new context more strongly`. But in deep block repetition, leaving only strong new context is not always safe. If the original action axis disappears, the next block can easily lose what the current representation changed from.

If we divide this scene into three stages, the roles of residual and normalization become clearer.

| Stage | Question used to read the current representation | Problem if it is missing |
| --- | --- | --- |
| only new computation remains | How did the new context change the current action representation? | the action axis of the original action token can weaken |
| after residual | Do the new context and the original action axis remain together? | value axes can be added together and make size and distribution shake |
| after normalization | Is this a value range that the next block can handle easily? | the next attention and feed-forward can receive unstable input |

![Action token comparison after residual](/AiBook/assets/part-05/chapter-14/transformer-block-action-residual-compare-en.png)

| Comparison point | rollback confirmed | rollback not confirmed | Why it matters |
| --- | --- | --- | --- |
| action token after residual | `[1.026, 1.978]` | `[1.238, 1.814]` | whether the action was confirmed moves the current position representation in different directions |
| interpretation | recovery-state axis is stronger | symptom/cause axis remains relatively more | new-context reflection and original-information preservation must be read together |

This graph does not show new values after normalization. First check whether the original action axis and the new context axis remain together after residual, then read normalization as the step that aligns those combined values to a baseline the next block can handle.

When reading the numbers, first see that both axes remain together, rather than asking which value is absolutely correct. In `rollback confirmed`, the recovery-state axis is stronger, but the original action axis of the action token should not disappear. In `rollback not confirmed`, the symptom/cause axis remains relatively more, but it should still be traceable as a meaning attached to some action. Residual leaves this trace path, and normalization aligns the combined values into a range the next block can handle easily.

The result to confirm in this case is that residual and normalization are not `components that newly create the answer`, but devices that protect the action token's basic axis and the stability of the next computation even after new computation enters.

## Practice and Example

### Practice. What Is Missing if We Remove Residual and Normalization?

Answer the questions below by separating the roles of residual and normalization.

| Question | Answer | Explanation |
| --- | --- | --- |
| What risk appears if we leave only the attention and feed-forward result and discard the original input representation? | new computation can cover important starting cues | residual connection leaves the original representation together, so the basic information flow is not cut off even when new context enters |
| If values become too large or too small after residual, what problem can appear in the next block? | the next computation can become unstable | layer normalization organizes the value range and distribution, then hands over a representation that the next block can handle easily |
| Are residual and normalization devices that make the answer smarter, or devices that help deep repeated computation endure? | they are closer to devices that help deep repeated computation endure | rather than being the main actors that create new meaning, they are stabilization axes that help repeated blocks keep information flow and value range |

Explanation: The core of this practice is not reading residual and normalization as `decorations that improve performance`. Because a deep Transformer block keeps stacking new computations, it needs both a path where original information remains and a value range that the next computation can handle.

### Practice. Diagnose the Action Token Axis

Choose which stabilization device is needed more directly in each situation below.

| Situation | More directly needed device | Explanation |
| --- | --- | --- |
| after new computation, only meanings like `block` and `risk` remain strongly, and what should be blocked has weakened | residual connection | the action axis of the original action token must remain together so later blocks do not lose the target |
| after residual adds the original axis and new context, only one axis value becomes too large | layer normalization | the value range should be organized so the next computation is not pulled too strongly by one axis |
| rollback confirmed and not confirmed move in different directions, but both must keep the action-state axis | residual connection | scene-specific new meanings may differ, but the basic axis that the current position is an action token should remain |
| the size of representation values changes greatly every time several blocks pass | layer normalization | repeated blocks should continue computation from a similar baseline |

Explanation: This practice is for avoiding memorizing residual and normalization as one bundle. If `what was lost` is original information, first think of residual. If `what range the computation uses` is shaking, first think of normalization.

## Checklist

- Can you say why residual connection preserves the original information flow?
- Can you explain that layer normalization organizes the value range and stabilizes the next computation?
- Can you explain the Transformer block as a combination of `context mixing + position-wise processing + original-information preservation + stabilization`?

## Sources and References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
