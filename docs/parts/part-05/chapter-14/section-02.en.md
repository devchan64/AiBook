# P5-14.2 What Does Each Of The Four Transformer Block Components Do?

> Section ID: `P5-14.2`
> Version: `v2026.07.20`

In P5-14.1, we saw that explaining the Transformer only with self-attention is not enough. Now we need to separate the roles inside the block more directly.

Inside a Transformer block, what does each of self-attention, feed-forward network, residual connection, and layer normalization do?

The core is not memorizing component names, but dividing roles. To read the path that the same token representation follows inside the block, we need to distinguish `relationship reading`, `position-wise processing`, `preserving original information`, and `stabilizing the value range`.

## Questions Handled By Block Role Division

- What does self-attention handle?
- How is the feed-forward network different from attention?
- Why do residual connection and layer normalization appear together?

| What this section reads now | What is passed to later sections |
| --- | --- |
| the role each component plays inside the block | how representations actually move in numeric examples |
| the difference between relationship reading and position-wise processing | the computational feel of parallel processing and long context |

## Self-Attention Reads Relationships

As we saw in Chapter 13, self-attention is a method in which each token refers to other tokens in the same sequence and recalculates its own representation.

`Self-attention is the device that decides where inside the sentence this token should look more strongly in order to be understood now.`

The core is `relationship reading`. It makes the current token bring in the context it needs from other positions in the sentence.

## Feed-Forward Network Processes The Current Position Representation

Self-attention mixes token relationships, but that result is not automatically a sufficiently good representation. The feed-forward network reprocesses the current position representation, after context has been mixed in, in a nonlinear way.

`If attention mixes context by reflecting relationships with other tokens, feed-forward reprocesses each position representation into something richer.`

Here the phrase `each position` is important. Self-attention is closer to deciding what information the current position should bring from other positions. The feed-forward network changes that mixed representation inside the same position. The same feed-forward network is applied to each token position, but because the input representation is different, the meaning refined at each position is also different.

```mermaid
--8<-- "assets/part-05/chapter-14/feed-forward-position-update-en.mmd"
```

In this diagram, each row means a different token position. The dotted lines mean that the same feed-forward network weights are shared across positions, and the solid lines mean that each position representation is processed separately inside its own position. So the feed-forward network is not a device that chooses a new token to refer to, but a device that changes an already context-mixed representation into the next representation for that position.

In a work-permit sentence, for example, attention makes the `restart` position look together at `pressure unreleased` and `hold`. The feed-forward network then processes that result inside the current position, so that the `restart` representation is read not as a simple action name, but as `an action that must be blocked because a condition is attached`.

The difference is clearer if we focus on one token.

| Stage | First question asked | Role |
| --- | --- | --- |
| self-attention | Which other tokens should this token refer to? | reading outside relationships |
| feed-forward | How should the current representation, now mixed with referenced context, change at this position? | processing the representation inside the current position |

So the feed-forward network should not be read as simple post-processing. If attention opens `what should be seen together`, feed-forward handles `how the mixed representation should become the next representation of the current position`. This distinction is needed to read the Transformer block not as attention alone, but as a repeating unit with divided roles.

Why a feed-forward network can apply the same weights to several positions while still producing different representations at each position is separated into [P5-14.6 Supplementary Reading: Why Does The Feed-Forward Network Handle Position-Wise Representation Processing?](section-06.md).

## Residual Connection Leaves The Original Information Flow

In a deep neural network, repeated new computations can overwrite the original information too strongly or make learning unstable. A residual connection passes the previous representation together with the new computation result, preserving the original information flow.

`A safety device that does not trust only the completely new computation, but also leaves the original input representation and sends it to the next stage together.`

The important point is that residual connection does not remove the new computation. The new representations made by self-attention or feed-forward are still needed. But if only that new representation is passed to the next stage, the basic meaning that the original token had can be covered too easily. So residual connection should be read as a path that leaves `new computation result + original input representation` together.

```mermaid
--8<-- "assets/part-05/chapter-14/residual-connection-skip-path-en.mmd"
```

In this diagram, the solid path is the representation made by the new computation, and the dotted path is the bypass route where the original input representation is added. The core of residual connection is not blocking the new computation, but letting the new computation and the original representation move together to the next stage.

If feed-forward handles `how should the current representation change`, residual connection handles `how can the changed representation avoid completely losing its original starting point`. If layer normalization organizes the value range, residual connection is closer to leaving a bypass path through which information can travel.

| Distinction | First question asked | Role |
| --- | --- | --- |
| feed-forward network | How should the current context-mixed representation change? | makes a new representation |
| residual connection | Can the new representation avoid completely covering the original representation? | leaves the original information flow together |
| layer normalization | Is this in a range the next computation can handle easily? | organizes the value range |

This distinction prevents residual connection from being reduced to mere addition. A more accurate intuition is `a device that leaves a path for original information even when new computation enters, so deep block repetition can endure`.

Why residual connection is not just a skip, but a path that passes original representation and new computation together, is separated into [P5-14.7 Supplementary Reading: Why Does Residual Connection Leave A Path For The Original Representation?](section-07.md).

## Layer Normalization Organizes The Value Range

When many layers and large matrix operations repeat, the size and distribution of representation values can shake. Layer normalization organizes each position representation into a range that is easier to handle, helping the next computation shake less.

`Layer normalization is a device that organizes the size and distribution of representation values so the next computation can continue stably.`

Here, organizing does not mean judging meaning anew. Representations made by self-attention and feed-forward consist of several numeric axes, and once residual connection is added, some axes can become too large while others become relatively small. If the value scale keeps spreading, the next attention or feed-forward step has to compute from a difficult range even when it receives a similar kind of input.

Layer normalization resets the mean and spread of values inside one position representation, so the next component can start from a similar baseline. At the introductory level, it is enough to read it as follows instead of memorizing formulas.

```mermaid
--8<-- "assets/part-05/chapter-14/layer-normalization-value-scale-en.mmd"
```

The important point in this diagram is that layer normalization does not choose new relationships among tokens or add a path for preserving the original information. It adjusts the value range inside one position representation so the next self-attention or feed-forward step does not receive an overly shaky input.

| Easy misunderstanding | Better reading |
| --- | --- |
| layer normalization chooses meaning | attention and feed-forward handle meaning selection more directly |
| it leaves original information like residual connection | residual connection leaves the path for original information |
| it simply makes values smaller | it organizes value distribution into a baseline the next computation can handle |

So residual connection and layer normalization often appear together inside the Transformer block, but they do not do the same job. If residual connection leaves `a path for information`, layer normalization aligns `the computational baseline` so the representation that passed through that path does not shake too much in the next computation.

Why layer normalization is a value-baseline adjustment inside one position representation, not meaning selection, and how it differs from batch normalization, is separated into [P5-14.8 Supplementary Reading: Why Does Layer Normalization Align The Value Baseline?](section-08.md).

If we bundle the four components at once, the questions asked about the same token representation are different.

| Component | What it looks at first in the representation | What it does not directly handle |
| --- | --- | --- |
| self-attention | which other position the current position should refer to | reprocessing the referenced representation inside the current position |
| feed-forward network | how the context-mixed current position representation should change | choosing a new token position to refer to |
| residual connection | whether new computation completely covers the original representation | directly creating new meaning |
| layer normalization | whether the value range is easy for the next computation to handle | choosing meaning or preserving original information |

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-flow-en.mmd"
```

This diagram compresses one Transformer block at an introductory level. Read the flow as `relationship reading -> add and organize the original representation -> process the current position representation -> pass it onward stably again`.

## Cases And Examples

### Case. Reading The `Restart` Position Representation Through The Four Components

Consider the work-permit sentence `Restart is held while the pressure remains unreleased.` The current position of interest is `restart`. If a person reads only the word quickly, it is easy to read `restart` as a simple execution action. But the sentence also contains the condition `pressure unreleased` and the judgment `held`.

The judgment that is too easy to make is `the word restart appeared, so this is an execution request`. If we read through the Transformer block by role, this judgment does not change all at once. The same position representation answers different questions as it passes through several components.

If we first split the input by token position, it can be read as follows.

| Position | Token | Cue used when understanding `restart` |
| --- | --- | --- |
| 1 | `pressure` | the target that says what condition is being discussed |
| 2 | `unreleased` | the state that the condition is not yet resolved |
| 3 | `while` | the link that makes the earlier state a condition for the later action |
| 4 | `restart` | the action currently being interpreted |
| 5 | `held` | the judgment that the action is not execution but hold |

If we isolate only the `restart` position in this table, it looks like an execution action. But the central axis of this section is not what `restart` finally means; it is how that position representation changes while passing through Transformer block components.

| Reading stage | Question asked at the current `restart` position | Misunderstanding if read too quickly |
| --- | --- | --- |
| starting representation | What is the basic word at this position? | only seeing the action name `restart` |
| self-attention | Which positions in the sentence should this position see together? | thinking attention already makes the final judgment |
| feed-forward network | How should the mixed context change inside this position representation? | thinking feed-forward chooses related tokens again |
| residual connection | Does the new computation completely cover the original action axis? | thinking residual skips the new computation |
| layer normalization | Is the value range easy for the next computation to handle? | thinking normalization leaves only the important meaning |

At the self-attention stage, the `restart` position refers together to `pressure unreleased` and `held`. The result to confirm here is that `restart` no longer stays as an isolated execution word, but sees the earlier condition and the later judgment together. But at this point the current position representation has not yet been fully organized as `a conditionally blocked action`.

At the feed-forward network stage, the context mixed by attention is processed again inside the current position. The `restart` representation becomes clearer as an action that should be held because of the pressure condition, rather than as a simple action name. The core of this stage is not choosing a new word to refer to, but changing the already imported context into the current position representation.

At the residual connection stage, only the newly processed blocking meaning is not left behind. The original action axis of `restart` must also remain so that later blocks do not lose what is being held. So residual connection is not a path that skips new computation, but a path that passes the new computation result and the original input representation together.

At the layer normalization stage, meaning is not selected again. The current representation, whose several numeric axes have been mixed after attention, feed-forward, and residual, is organized into a baseline the next block can handle. Aligning the value range and judging meaning are not the same job.

If we narrow the flow to only the change in the `restart` position representation, it becomes the following.

| Point inside the block | `restart` position representation in words | Role distinction to learn here |
| --- | --- | --- |
| input representation | the action name `restart` | the earlier condition and later judgment are not yet reflected enough |
| after self-attention | an action that has seen `pressure unreleased` and `held` together | relationship cues were brought in, but the current position representation has not been finally refined |
| after feed-forward | an action read toward hold rather than execution because of the pressure condition | the context-mixed representation was processed again inside the current position |
| after residual | a representation where the hold-side meaning and original `restart` action axis remain together | new computation does not completely cover the original action information |
| after layer normalization | a representation organized into a range the next block can handle | the computational baseline was aligned, not meaning selected |

So the output of this case is not just the conclusion `restart is held`. The more important output is the distinction that `relationship reading`, `position-wise processing`, `preserving original information`, and `stabilizing value range` are jobs of different components. Once this distinction is fixed, the Transformer block can be read not as `a device where attention gives the answer`, but as a representation-update unit where several roles repeat.

If we close the same case from the output viewpoint, it becomes the following.

| Component | Change directly made in this case | What it does not directly handle |
| --- | --- | --- |
| self-attention | makes the `restart` position see `pressure unreleased` and `held` together | processing the current position representation into final meaning |
| feed-forward network | processes the context-mixed `restart` toward `conditional blocked action` | choosing a new token position to refer to |
| residual connection | leaves the `conditional block` meaning and the original `restart` action axis together | selecting important meaning anew |
| layer normalization | organizes the combined representation's value range into the next computational baseline | preserving the original action axis or choosing a relationship anew |

The result to confirm in this case is that the `restart` representation does not change all at once as if by magic. Self-attention reads relationships, feed-forward processes the current position representation, residual connection leaves the original information flow, and layer normalization aligns the value baseline for the next computation. Only when these four questions are separated can the Transformer block be read not as attention alone, but as a repeating unit with divided roles.

## Practice And Example

### Practice. Naming The Role

Judge which component the description below is most directly connected to.

| Description | More directly connected component | Explanation |
| --- | --- | --- |
| decides which other tokens in the sentence the current token should look at more | self-attention | relationship reading |
| changes the context-mixed `restart` representation toward `conditional block` inside the current position | feed-forward network | reprocesses the relationship brought by attention into the current position representation |
| the same processing device is applied to each token position, but because each position has a different input representation, it is refined into different meanings | feed-forward network | feed-forward transforms each position representation rather than choosing token relationships again |
| leaves the processed `conditional block` meaning together with the original `restart` action axis | residual connection | passes new computation and original representation together to preserve information flow |
| does not create a new representation, but leaves a path for the original representation to pass through | residual connection | this is where it differs from feed-forward |
| after the new computation and original representation are added, realigns the value baseline | layer normalization | organizes value distribution so the next computation continues stably |
| organizes the value range before passing to the next computation | layer normalization | stabilization role |

Explanation: The core of this practice is not memorizing component names, but distinguishing that even inside the same block, `what to refer to`, `how to change the current representation`, `how to leave the original information`, and `how to stabilize computation` are different questions.

### Practice. Fix Misleading Sentences

The sentences below are only partly right or mix roles. Rewrite them more accurately.

| Misleading sentence | More accurate explanation | Explanation |
| --- | --- | --- |
| The feed-forward network chooses related tokens again. | Self-attention makes the model refer to related tokens; the feed-forward network reprocesses the current position representation after context has been mixed in. | We need to separate `what should be seen` from `how should this position representation change`. |
| Residual connection makes the model skip new computation. | Residual connection passes the new computation result and the original input representation together. | It does not remove new computation; it leaves a path for original information. |
| Layer normalization leaves only the important meaning. | Layer normalization aligns the value range of one position representation into a baseline the next computation can handle. | The focus is value-distribution stabilization, not meaning selection. |
| Understanding self-attention is enough to explain the Transformer block. | Self-attention handles relationship reading, while feed-forward, residual connection, and layer normalization divide representation processing and stabilization. | The block is a repeated unit with separated roles, not attention alone. |

Explanation: The reason for correcting these sentences is to create a sense of boundaries, not to memorize terms. All four components are inside the same representation flow, but if `relationship selection`, `within-position transformation`, `information preservation`, and `value stabilization` are mixed together, the computational flow becomes blurry when reading the Transformer structure later.

## Checklist

- Can you explain the role difference between self-attention and feed-forward?
- Can you explain residual connection as a device that leaves the original information flow?
- Can you explain layer normalization as a stabilization device for deep block repetition?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
