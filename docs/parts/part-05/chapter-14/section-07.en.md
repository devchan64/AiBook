# P5-14.7 Supplementary Learning: A Path That Preserves the Original Representation

> Section ID: `P5-14.7`
> Version: `v2026.07.26`

_Subtitle: How does a residual connection pass the new computation result and the original input representation together?_

In P5-14.2, we saw that a residual connection leaves the original information flow inside a Transformer block. But if we only hear that it “adds the original input,” it is easy to mistake a residual connection for a simple addition trick or for a shortcut that skips computation.

In a Transformer block, a residual connection does not remove the new computation. It creates a path where the new computed result and the original input representation move on to the next stage together.

When the terminology begins to scatter again, it helps to revisit the [residual connection](/AiBook/en/reference/concept-glossary-alpha/t/#transformer) entry in the concept glossary together with the four-part role split from P5-14.2.

## What Goes Wrong If Only the New Computation Is Passed On?

Self-attention and the feed-forward network keep changing the current representation. This change is necessary. The problem is that, as blocks become deeper, the new computation can too easily cover the basic meaning of the original token.

For example, consider the `restart` position in the sentence `If pressure remains unresolved, restart is held.` Attention and the feed-forward network should refine the `restart` representation toward `a conditionally blocked action`. But if the original action axis of `restart` disappears completely during that process, later blocks have a harder time tracking what exactly is being blocked.

So a residual connection answers the following questions.

| Question | Answer from a residual connection |
| --- | --- |
| Is the new computation needed? | Yes. Attention and feed-forward create a new representation. |
| Is it enough to pass only the new computation onward? | Not always. The original representation axis can be covered. |
| What is passed onward together? | The original input representation and the new computed result. |

## A Path Added Together, Not Computation Skipped

A residual connection is often also called a skip connection. Here, `skip` does not mean that the new computation is not performed. It is closer to saying that the original input representation has an extra path that bypasses the new computation path and is added back in.

```mermaid
--8<-- "assets/part-05/chapter-14/residual-connection-skip-path-en.mmd"
```

In this diagram, the solid line is the representation created by the new computation, and the dotted line is the path through which the original input representation is added back. The key is not choosing one of the two. The key is that `original representation + new computed result` becomes the starting point of the next-stage representation.

The difference can be summarized as follows.

| Easy Misreading | Better Reading |
| --- | --- |
| A residual connection skips the computation. | The new computation is still performed, and a path is left for the original input representation to be added back. |
| Because the original representation is preserved, the new representation matters less. | The new representation is needed, and the original representation is needed as well. |
| Since it is addition, it is only a simple post-processing step. | It is a structural device that keeps information flow from disappearing in deep repetition. |

## Why It Matters More in Deep Block Repetition

A Transformer does not end with one block. The same kind of block is repeated several times, gradually changing the representation. If only the new computation passes through each time, information that mattered in earlier stages can become weaker in later stages.

A residual connection leaves a path for the original representation in each block, so that deep repetition does not become `continuous overwriting by new computation`. At the introductory level, this is enough:

| Problem That Can Appear in Deep Repetition | How a Residual Connection Helps |
| --- | --- |
| The original token meaning is covered by new computation. | The original input representation is added into the next stage. |
| Later blocks lose the starting point of earlier blocks. | Each block has a direct path from its input toward its output. |
| During learning, signals have difficulty passing through deep layers. | The bypass path helps the signal flow continue more stably. |

Here, `signal` carries two senses at once. One is the flow of representation information from earlier blocks to later blocks when an input is given. The other is the flow of correction direction back toward earlier parameters during learning, based on the output error.

At the introductory level, it is better not to prove these flows with equations yet. Instead, read it this way: if a deep structure has only one path, information can weaken while passing through many computations. A residual connection leaves a path for the original representation to pass alongside the new computation path. That is why, even when blocks are stacked deeply, both `the force that keeps changing the representation through new computation` and `the force that keeps the original starting point from being lost` remain together.

## Do Not Confuse It with Layer Normalization

In P5-14.2, residual connection and layer normalization appeared together. But they are not the same stabilization device.

| Distinction | Problem Seen First | What It Does |
| --- | --- | --- |
| residual connection | Is the original information being covered by new computation? | Passes the original input representation and new computed result onward together. |
| layer normalization | Are the values in a range that the next computation can handle? | Organizes the value baseline inside one position representation. |

A residual connection leaves `a path for information to pass through`. Layer normalization makes the value range of the representation produced through that path easier for the next computation to handle. If the two are collapsed into one sentence, the meaning becomes blurred.

## Cases and Examples

### Case. When an Operations Sentence Must Not Lose the Action Axis

In `If pressure remains unresolved, restart is held`, the `restart` position uses attention to look at `pressure remains unresolved` and `held`. The feed-forward network refines this context inside the current position and makes the meaning closer to `a conditionally blocked action`.

Without a residual connection, later blocks might strongly receive new meanings such as `blocked`, `risk`, or `condition`, but lose clarity about which original action those meanings were attached to. The residual connection passes along the original `restart` action axis, helping later blocks continue to track `what must be blocked`.

| Current Position | If Only the New Computation Remains Strong | When Residual Keeps It Together |
| --- | --- | --- |
| `restart` | `blocked` and `risky` are visible, but which action they target can become blurry | the `blocked` meaning remains attached to the original action axis `restart` |
| `approval` | `not finalized` and `held` are visible, but which action is not finalized can weaken | the `not finalized` meaning remains attached to the original action axis `approval` |
| `deployment` | `risky` and `stopped` are visible, but which work is stopped can get mixed | the `risky` meaning remains attached to the original task axis `deployment` |

The result to confirm in this case is that a residual connection does not judge a new meaning by itself. It helps the original representation axis needed for the new judgment remain available to later stages.

So residual addition is not simply a matter of making numbers larger. It should be read as placing `original axis + new meaning` together at the starting point of the next block, so the meaning created by the new computation does not detach from its original target.

## Practice and Examples

### Practice. Find What Must Be Kept and Explain Why

In the scenes below, write the original representation axis that should remain together with the meaning strengthened by the new computation. Do not stop with one word. Also explain why the later block needs to reuse that axis.

| Sentence | Current Position | Meaning Strengthened by New Computation | Original Representation Axis to Keep | Why Later Blocks Need It |
| --- | --- | --- | --- | --- |
| `If pressure remains unresolved, restart is held` | `restart` | conditional blocking | the action name restart | Later blocks need to know not only that something is blocked, but also what is blocked. |
| `If validation is incomplete, approval is not finalized` | `approval` | held or not finalized | the approval action | The target of the not-finalized meaning must remain approval. |
| `Before rollback is confirmed, deployment is stopped and the previous version is kept` | `deployment` | risky progress or stop target | the deployment task | When compared with `keeping the previous version`, the risk judgment must remain attached to the deployment task. |
| `If the incident cause is unclear, expand the alert and stop automatic recovery` | `automatic recovery` | stop target under unclear cause | the automatic recovery action | To avoid mixing it with `alert expansion`, the model must keep which action the stop meaning attaches to. |

Explanation: A good answer does not stop at `keep the original word`. When the meaning created by the new computation is reused in later blocks, the original target or action that the meaning attaches to must remain traceable.

For example, at the `restart` position, the new computation can strongly create meanings such as `blocked` or `risky`. But if only those meanings remain and the original action axis of `restart` weakens, later blocks can read unclearly what is being blocked. A residual connection helps pass along both the new meaning `should be blocked` and the original action `restart`, so later blocks can keep hold of the target of the judgment.

This is why a residual connection should be read not as simple addition, but as a device that leaves information flow in deep repetition.

## Checklist

- Can you explain a residual connection not as skipping new computation, but as a path that passes the original input representation and new computed result onward together?
- Can you explain with a case why the original representation axis becomes necessary in deep Transformer block repetition?
- Can you distinguish residual connection and layer normalization as `information flow` and `value range stabilization`?

## Sources and References

- Kaiming He et al., `Deep Residual Learning for Image Recognition`, CVPR 2016, checked on 2026-07-19. [https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html](https://openaccess.thecvf.com/content_cvpr_2016/html/He_Deep_Residual_Learning_CVPR_2016_paper.html){: target="_blank" rel="noopener noreferrer" }
- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
