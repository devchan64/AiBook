# P5-14.1 The Basic Structure Of The Transformer

Section ID: `P5-14.1`
Version: `v2026.07.17`

In P5-13.2, we explained that self-attention is a method in which tokens inside the same sequence refer directly to one another, and that this idea leads to the core intuition of the Transformer. The next question appears here.

Then is the Transformer a structure that contains only self-attention, or are there other basic components around it that come together with it?

The Transformer can be understood as a structure that reads contextual relationships through self-attention, refines each position's representation again through a feed-forward network, and keeps that computational block from collapsing through residual connections and layer normalization.

When the names of block components become mixed up again, it helps to reread together the glossary entries on [Transformer](/AiBook/reference/concept-glossary/#transformer), [feed-forward network](/AiBook/reference/concept-glossary/#feed-forward-network), [residual connection](/AiBook/reference/concept-glossary/#residual-connection), and [layer normalization](/AiBook/reference/concept-glossary/#layer-normalization).

## Scope Of This Section

- What components make up the core block of the Transformer?
- What role does each of self-attention, feed-forward network, residual connection, and layer normalization play?
- Why did this structure look like a major turning point after RNNs?
- Before the details of encoder and decoder, what big picture should be held first?

The core point that this section needs to hold first is that `the Transformer is not one idea called self-attention, but a structure that has contextual reading, representation refinement, and block-maintenance devices as one bundle`. The handle of this chapter moves from `how should we refer to the needed position` to `through what block structure can that reference computation be repeated stably`. So here, rather than learning procedures such as optimizers or regularization, we first read how each component divides roles inside the Transformer block.

| What is read in this section now | What is passed to the next section |
| --- | --- |
| how self-attention, feed-forward, residual connection, and normalization divide their roles inside one block | what repeating that block changes in parallel processing, long-context cost, and compute scale |
| relationship reading and representation refinement inside the block | large-scale training procedure and long-context optimization |

An introductory explanation of multi-head attention and query, key, and value is revisited in supplementary reading P5-13.3. Meanwhile, the advantages in parallel processing and long context are continued in P5-14.2, and the detailed split among encoder-only, decoder-only, and encoder-decoder is compared again from the LLM viewpoint in P6-3.1. That is, here we first close `how each component divides roles inside the Transformer block`.

Here, rather than following the entire Transformer paper, we first hold what is combined at the block level.

## Goals Of This Section

- You can explain the Transformer not as self-attention alone, but as a combination of several core components.
- You can say which components play the roles of contextual reading, representation refinement, and training stabilization.
- Even when looking later at other model families, you can recall the Transformer’s basic block.
- Through an executable Python example, you can intuitively confirm the flow in which token representations change through several stages.

## The Transformer In A Very Large Picture

It is enough if we first firmly hold only the following four elements.

1. self-attention
2. feed-forward network
3. residual connection
4. layer normalization

If we say these four very simply:

- self-attention: decides which tokens should refer to which other tokens
- feed-forward: refines each position representation again
- residual connection: keeps the original information flow alongside the new computation
- layer normalization: handles value scale and helps keep learning stable

That is, the Transformer is a repeated structure of `a block that reads contextual relationships -> refines representations -> keeps the information flow stable`.

The division of roles can be organized through the following table.

| Component | Role to hold first |
| --- | --- |
| self-attention | reads the relationships with other tokens |
| feed-forward | refines each position representation again |
| residual connection | keeps the original information flow alongside the new one |
| layer normalization | organizes the value range so learning shakes less |

If we immediately split the two most frequently mixed questions here, the boundary with the next section becomes clearer.

| Question answered in this section now | Question passed to the next section |
| --- | --- |
| `inside one block, how do attention, feed-forward, residual, and normalization divide their roles?` | `when that block is repeated many times, why does it become advantageous in GPU parallel processing and long-context computation?` |
| `in what order is the representation read and refined?` | `how do compute cost, processing speed, and long-context cost change?` |

If we follow just one current token representation, the difference in the role of each component becomes more direct.

| The same scene | Component that should be looked at first | What that component immediately does |
| --- | --- | --- |
| deciding where the current token should refer more strongly inside the sentence | self-attention | gathers the needed context by reading relationships with other positions |
| refining the current representation after the gathered context has been mixed in | feed-forward | processes the current position representation once more to make the features richer |
| preventing the new computation from overwriting the original input flow too strongly | residual connection | keeps the previous representation alongside and carries the information flow forward |
| organizing the value range before sending the result to the next computation | layer normalization | organizes the size and distribution of the representation so the next computation shakes less |

If P5-13.2 was read as a section about `the computation in which tokens refer to one another`, this section is the one that shows `with what surrounding supporting components that computation forms one block inside the real model`.

What the reader especially needs to hold here is that it is not `a structure where components are scattered separately`. The Transformer is usually easiest to understand if one block is read in the following order of questions.

1. Among the other tokens, where should the current token refer more strongly?
2. Once that context is gathered, how should it be reflected again in the current position representation?
3. Should that representation be processed once more at each position?
4. In this process, how are the original information and stability maintained?

That is, it is more natural to read the Transformer block as `relationship reading -> position-wise processing -> stable transfer`.

## What Does Self-Attention Handle

As seen in Chapter P5-13, self-attention plays the role of letting each token reread the other tokens and recalculating contextual representations.

`Self-attention is the device that decides which part of the sentence should be looked at more in order to understand this token right now.`

The core is `reading relationships`.

## Why Is A Feed-Forward Network Needed

Self-attention alone can read relationships among tokens, but we also need a process that refines each position representation more nonlinearly. This is where the feed-forward network appears.

The core point is that after attention mixes in contextual relationships, feed-forward refines each position representation more nonlinearly at that position.

`If attention mixes context by reflecting relationships with other tokens, feed-forward can be seen as a small MLP that refines each position representation into something richer again.`

This difference can also be read by looking at just one token. The self-attention stage asks `what should this token receive from the other tokens?`, while the feed-forward stage asks `how should the current representation, now mixed with the received context, be refined again at this position?` That is, attention is closer to `the relationship with the outside`, while feed-forward is closer to `the processing inside the current position`.

## Why Is Residual Connection Needed

As depth increases in deep learning, information can change too much or learning can become unstable. A residual connection can be seen as a device that lets the previous representation continue flowing together into the next stage.

The core is that instead of trusting only the completely new computation, the model also leaves the original input representation in place and sends it forward together so the learning shakes less.

`Do not trust only the completely new computation; also leave the original input representation and send it together to the next stage as a safety device.`

Residual connections reduce information loss and make learning more stable.

## Why Does Layer Normalization Appear

When many layers and large matrix operations are repeated, the scale and distribution of values can affect training stability. Layer normalization is a device that organizes each position representation into a range that is easier to handle and helps the learning process.

The core is that it organizes the size and distribution of the representation values so the next computation can continue more stably.

`Layer normalization is a device that organizes the size and distribution of representation values so the next computation shakes less.`

That is, the Transformer has not only `strong attention`, but also `stabilization devices that help it endure deep learning`.

## If We Draw This Very Simply

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-flow-en.mmd"
```

This diagram compresses one Transformer block at the introductory level.

If we reread this flow line by line, it becomes the following.

- `self-attention`: reflects the relationships with other tokens
- `add + norm`: organizes the result so the original information flow is not lost too much
- `feed-forward`: refines each position representation once more
- `add + norm`: again sends the representation stably to the next block

That is, the Transformer block is not `a structure that ends after mixing context`, but `a structure that, after mixing context, refines that representation again and then passes it onward stably`.

If we focus only on how one current representation changes inside the block, it can be read as follows.

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-representation-update-en.mmd"
```

The first points to fix from this diagram are the following.

- self-attention decides `what should be referred to` and mixes context into the current representation
- feed-forward processes the current representation with mixed context into a clearer meaning at that position
- residual and layer normalization do not leave only the new representation, but let it pass stably to the next block without losing the original axis

## Why Was This Structure Important

The Transformer looked like a major turning point not because it simply added one new layer. The core point that should be seen first within the scope of this section is that the following components were combined into `one repeatable block`.

- attention-centered contextual reference
- a feed-forward stage that refines each position representation again
- residual and normalization that preserve the original flow and the value range

That is, the Transformer was an architecture that rebound `the core computation of sequence modeling` into a new block unit.

If we pause once here and briefly fix `when should we first read from the viewpoint of Transformer block structure rather than only the attention idea itself`, the baseline shakes less when moving into the next section on parallel processing.

| Question to recall first | Why the basic-structure viewpoint of the Transformer is needed first | What continues in the very next section |
| --- | --- | --- |
| why does the model not end with self-attention alone? | because, besides contextual reading, position-wise processing and stable transfer devices are also needed for a repeatable block to exist | why does the computational feel change when this block is repeated |
| why are residual connection and layer normalization mentioned together? | because, beyond strong contextual computation, a stabilization axis is needed so deep block repetition can be endured | what block repetition means in parallel learning and scale expansion |
| how is feed-forward different from attention? | because we need to separate relationship reading from position-wise processing so the roles inside the block do not mix | how the full block works in long context and GPU computation |

## Cases And Examples

Before entering the cases, in this section we need to look first not at `does it reread long context`, but at `how does the current representation change inside one block`. That is, even when reading the case, we should not end only with `what was referred to again`, but also look together at `how the current position representation is refined after that`, `how the original information remains`, and `how it is passed stably to the next block`.

| Situation | Change in the current representation that should be looked at first | How the Transformer block helps |
| --- | --- | --- |
| work-permit sentence | the current action expression must split into `simple restart` versus `conditional hold` | self-attention connects the condition and the action, and feed-forward processes the current representation into a clearer action state |
| one line of incident summary | the current summary expression must split into `vague anomaly` versus `anomaly with causal evidence` | after gathering the related cues, the current position representation is refined more sharply toward `causal summary` |
| one line of an operation memo | the current memo must split into `general approval` versus `approval with a blocking condition attached` | the original input meaning is preserved through the residual path, and after normalization the condition remains stable even in the next block |

### Representative Case. Interpreting One Work-Permit Sentence

Let us think about a work-permit sentence such as `Restart is held while the pressure remains unreleased.` If a person reads this sentence in a hurry, it is easy to separate `restart` and `held`, or to grab only the action word `restart` strongly first. But in reality, the current action expression must be read not as `approval`, but as `conditional hold` for safety. Here, self-attention first connects what relationship `pressure unreleased`, `restart`, and `hold` have inside the same sentence. Then feed-forward, based on this gathered relationship, processes the current action expression more clearly not toward `just a work instruction`, but toward `a blocking instruction with a condition attached`. The residual connection leaves behind the basic meaning that the original action expression already had so that it is not lost completely, and layer normalization organizes the changed representation so the value distribution does not shake too much when it is passed to the next block.
So the result to confirm in this case is whether the current action expression avoids following only the word `restart`, and is instead read as a conditional blocking expression that also reflects `pressure unreleased` and `hold`.

The same viewpoint extends directly to refining an incident-summary sentence and rewriting an operation memo. But the core point to hold in this section is not the domain name, but `how the current position representation is processed again into a clearer meaning and then preserved stably inside one block`.

| Standard that is easy for a person to see first | Standard to reread from the Transformer-block viewpoint |
| --- | --- |
| it is easy to feel that the Transformer is fully explained once attention is present | only when we also see the components that refine the representation again after reading the relationship, and preserve the original information and stability, does the block close |
| it can feel that the final judgment comes immediately once the context is mixed once | only when `context reading -> position-wise processing -> residual -> normalization` continue in order can the change in the current representation be interpreted |
| it is easy to feel that the model structure must change greatly when the task changes | even if the tasks are work-permit sentences, incident-summary sentences, or operation memos, it is more accurate to see the same block repeated while only changing `how the current representation is refined again` |

If we split the same three cases again by the responsibility of each block component, it becomes more direct why it is not enough to close the section with `attention alone`.

| Case | What self-attention handles first | What feed-forward handles next | What residual + normalization preserve |
| --- | --- | --- | --- |
| work-permit sentence | connects `pressure unreleased`, `restart`, and `hold` with the current action expression | processes the current representation more clearly into `conditional blocking instruction` rather than `simple instruction` | lets the block condition continue stably into the next block without losing the original action meaning |
| incident-summary sentence | connects cues such as `right after deployment`, `pressure fluctuation`, and `no anomaly` to the current summary position | refines the current sentence into `a summary with a causal basis` rather than `a vague anomaly` | keeps the balance between the whole situation feel and the specific basis from collapsing during block repetition |
| one line of an operation memo | connects `interlock`, `not released`, `restart`, and `hold` to the current memo expression | processes the current position representation not into `a sentence about restart`, but into `a hold sentence with a blocking condition attached` | lets the restart-action axis remain while the blocking meaning is also kept stable |

## Practice And Example

The goal of this example is to place onto a practical operations sentence the two core stages that make up a Transformer block, namely `the stage that mixes context` and `the stage that refines each position representation again`.

Before reading the code, if we look in order at the following four values, the structural axis of this section spreads less.

| Value to look at first | Why it should be looked at first |
| --- | --- |
| `contextual tokens` | because it immediately shows how self-attention first mixes the different cues in an incident-response log |
| `feed-forward output` | because it lets us then see how the attention-mixed representation is processed again at each position |
| `after residual` | because it lets us confirm that not only the new computation result is used, but the original input representation is also left in place |
| `after simple layer norm` | because at the end it lets us hold the feel of organizing the value range again before passing it to the next block |

Input:

- initial representations of three tokens
- attention weights for two different operational scenes
- feed-forward weights

Output:

- token representations before and after attention
- the representation after feed-forward
- the representation after adding the residual path
- the representation after simple layer normalization
- how the action-token representation changes in the `rollback confirmed` versus `rollback not confirmed` scenes

Problem situation:

- in incident-response operations, even when `incident symptom`, `deployment clue`, and `action confirmation` are written far apart, they still need to be read together, so we need to see step by step how a Transformer block updates the representation in such a scene

Concepts to confirm:

- a Transformer block repeats attention and feed-forward as one bundle
- only when residual and normalization are also seen can we understand how the representation is updated stably
- in an operations-sentence scene, if we ask `how does the action-token representation change when an action-confirmation cue comes in`, the division of roles inside the block becomes clearer

Before reading the code, it helps to predict first which stage will change before the others in the two operational scenes.

| Comparison point | Change to predict first in `rollback confirmed` | Change to predict first in `rollback not confirmed` |
| --- | --- | --- |
| `contextual tokens` | the action token will mix in the action-confirmation cue more strongly | the action token will keep more of the symptom/deployment-cue side |
| `feed-forward output` | the mixed action context will be reflected more in each position representation | the context of lacking confirmation will remain, so the action representation will move less toward recovery |
| `action token after residual` | the recovery axis will remain more strongly | the symptom/cause axis will remain relatively more strongly |

Input:

We use the three tokens `symptom`, `deploy clue`, and `action status`, and compare the scenes `rollback confirmed` and `rollback not confirmed`.

```python
import numpy as np

tokens = np.array([
    [1.0, 0.2],   # symptom token: urgency high
    [0.8, 0.5],   # deploy clue token: cause evidence medium
    [0.3, 1.0],   # action token: recovery status important
])

attention_cases = {
    "rollback_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.2, 0.5, 0.3],
        [0.1, 0.3, 0.6],
    ]),
    "rollback_not_confirmed": np.array([
        [0.6, 0.3, 0.1],
        [0.3, 0.5, 0.2],
        [0.3, 0.5, 0.2],
    ]),
}

ff_weights = np.array([
    [1.1, 0.4],
    [0.2, 1.0],
])

def simple_layer_norm(row):
    mean = np.mean(row)
    std = np.std(row)
    return (row - mean) / (std + 1e-6)

for name, attention_weights in attention_cases.items():
    contextual = attention_weights @ tokens
    ff_output = contextual @ ff_weights
    delta_from_input = ff_output - tokens
    residual_added = ff_output + tokens
    normalized = np.vstack([simple_layer_norm(row) for row in residual_added])

    print(f"[{name}]")
    print("contextual tokens =")
    print(np.round(contextual, 3))
    print("feed-forward output =")
    print(np.round(ff_output, 3))
    print("change from input =")
    print(np.round(delta_from_input, 3))
    print("after residual =")
    print(np.round(residual_added, 3))
    print("after simple layer norm =")
    print(np.round(normalized, 3))
    print("action token after residual =", np.round(residual_added[2], 3))
    print("---")
```

In the output, in both scenes, compare `action token after residual` first, and then trace back how that difference was already created at the `contextual tokens` stage.

```text
[rollback_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.69 0.59]
 [0.52 0.77]]
feed-forward output =
[[1.031 0.718]
 [0.877 0.866]
 [0.726 0.978]]
change from input =
[[ 0.031  0.518]
 [ 0.077  0.366]
 [ 0.426 -0.022]]
after residual =
[[2.031 0.918]
 [1.677 1.366]
 [1.026 1.978]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.026 1.978]
---
[rollback_not_confirmed]
contextual tokens =
[[0.87 0.37]
 [0.76 0.51]
 [0.76 0.51]]
feed-forward output =
[[1.031 0.718]
 [0.938 0.814]
 [0.938 0.814]]
change from input =
[[ 0.031  0.518]
 [ 0.138  0.314]
 [ 0.638 -0.186]]
after residual =
[[2.031 0.918]
 [1.738 1.314]
 [1.238 1.814]]
after simple layer norm =
[[ 1. -1.]
 [ 1. -1.]
 [-1.  1.]]
action token after residual = [1.238 1.814]
---
```

The first result to look at in this example is where the action token moves across the stages of the block. `rollback confirmed` and `rollback not confirmed` start from the same input, but from the stage of mixing context through attention they already separate into different paths, and after feed-forward and residual they remain as different action representations.

![Stage-by-stage movement of the action token](/AiBook/assets/part-05/chapter-14/transformer-block-action-stage-trace-en.png)

The second result is a comparison that isolates only the action token after the residual path. In the rollback-confirmed scene, the recovery-status axis remains more strongly, while in the not-confirmed scene the urgency/cause axis remains relatively more strongly. This makes clearer why the Transformer block should be read not as attention alone, but as a combination of `context mixing -> position-wise processing -> preservation of original information`.

![Comparison of the action token after the residual path](/AiBook/assets/part-05/chapter-14/transformer-block-action-residual-compare-en.png)

| Comparison point | rollback confirmed | rollback not confirmed | Why it matters |
| --- | --- | --- | --- |
| context referred to by the action token | the action-confirmation token keeps itself and the cause cue more strongly | as action confirmation weakens, the symptom/deployment-cue side stays relatively larger | because even with the same block, `which cues are tied together more strongly` changes depending on the operational scene |
| action token after residual | `[1.026, 1.978]` | `[1.238, 1.814]` | because it reveals that whether the action is confirmed actually moves the current position representation in different directions |
| reading style | `because the action was confirmed, it reflects the recovery-status side more strongly` | `because confirmation is still weak, it suspects the alert and deployment cues more strongly` | because it shows that even when reading operations sentences, the Transformer block works through relationship rereflection rather than simple sequence order |

| Block stage | Misunderstanding that can easily arise if this stage is looked at alone | Point that must be corrected when reading the full block |
| --- | --- | --- |
| self-attention (`contextual tokens`) | it can feel that the final judgment is already complete because the context was mixed once | this stage is where `what should be reread` is decided; the current position representation still has to be processed and passed stably |
| feed-forward (`feed-forward output`) | because it transforms only numbers again, it can feel like a secondary post-processing step | in reality it refines the context gathered through attention inside each position representation, so even the same context can separate into different position-wise interpretations |
| residual (`after residual`) | it can look like just adding the previous value back in | by not trusting only the new computation and leaving the original input representation in place together, it prevents the recovery-status information that the action token originally had from disappearing |
| layer normalization (`after simple layer norm`) | it can feel like a secondary step that only organizes number size | it realigns the range of representations sent to the next block so the computation shakes less even when block repetition becomes deep |

- at the attention stage, each token changes its original representation by receiving information from the other tokens
- at the feed-forward stage, the representation with mixed context is transformed again position by position
- `after residual` shows that, instead of using only the new computation result, the original token representation is also kept
- `after simple layer norm` shows that before each position representation moves to the next stage, the value range can be reorganized again
- in an operations-sentence scene, the key question is whether a distant cue such as `rollback confirmed` is actually reflected in the action-token representation

That is, what separates `rollback confirmed` from `rollback not confirmed` begins at the attention stage, but what passes that difference onward into a stable block output is the full combination including feed-forward, residual, and normalization. If we read the Transformer only as `a model with strong attention`, this division of responsibility disappears.

This example shows that, even under the same incident-response log, the current action representation can change depending on whether the phrase `rollback confirmed` is present. The Transformer block matters not because it merely mixes tokens, but because it makes it possible for `a distant cue needed for an operational judgment` to be reflected again inside the current representation.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| `action token after residual` differs by scene | raise or lower the attention weight on the action-confirmation token and compare how the operational-judgment representation changes | do not conclude that one attention number alone fully determines the real operational priority |
| `contextual tokens` mix differently by scene | change the weights of the symptom token and the deployment-cue token and see what context enters the action token more strongly | do not conclude that larger numeric change always means better representation learning |
| `after simple layer norm` is organized into a similar range | make one axis excessively large and compare how much the difference grows before and after normalization | do not use this one simple normalization comparison as a replacement for all real layer-normalization implementation details |

Real Transformers use residual connection, layer normalization, and multi-head attention together, but the broad flow is best read as this kind of block repetition.

## If We Reread This Example From The Viewpoint Of Block Combination

The numbers above do not implement the whole Transformer, but the role of each component appears clearly.

- `contextual tokens` is the stage where self-attention first mixes in information from other positions
- `feed-forward output` is the result of processing that mixed representation once more at each position
- `after residual` shows the role of a safety device that does not trust only the new computation, but also carries forward the original representation
- `after simple layer norm` gives the feel of organizing the value range again before passing to the next block

That is, the Transformer block is not `attention alone`, but a structure in which `context mixing + position-wise processing + preservation of original information + stabilization` are repeated as one bundle. Only when this feel is fixed does it become easier in the next section, P5-14.2, to read more naturally why this block could be repeated at large scale.

The Transformer is a case where attention was promoted from an auxiliary device to the central block. And this block design was reused as a common basic unit across many later large-scale language and multimodal models.

## Checklist

- Can you explain the Transformer block through self-attention, feed-forward, residual connection, and layer normalization?
- Can you say that the Transformer is not one idea, but a structure made of a bundle of components?
- When reading the Transformer, can you distinguish it as a block combination where self-attention gathers contextual relationships, feed-forward processes the representation, and residual plus normalization stabilize deep computation?
- Can you explain the Transformer not merely as `a model with attention`, but as `a block structure that repeats relationship reading, position-wise processing, and stable transfer`?
- Can you separate the roles of self-attention and feed-forward into `reading relationships with the outside` and `processing the current position representation`?
- Can you explain that residual and normalization stabilize deep learning?
- When attention alone is not enough to explain the Transformer, can you recall the block-structure viewpoint first?
- When reading the next section on parallel processing, are you ready first to ask `if this block is repeated many times, why does the computational flow change`?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`, checked on 2026-06-29. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
