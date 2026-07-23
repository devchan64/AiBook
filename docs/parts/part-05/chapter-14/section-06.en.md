# P5-14.6 Supplementary Learning: Position-Wise Representation Processing

> Section ID: `P5-14.6`
> Version: `v2026.07.23`

_Subtitle: How does the feed-forward network process each position representation again after attention?_

In P5-14.2, we saw that the feed-forward network does a different job from self-attention inside the Transformer block. But the question remains: `if attention already mixed context, why is feed-forward needed again?`

In a Transformer block, the feed-forward network is not a device that chooses a new token to refer to. It is a device that reprocesses each position representation whose context has already been mixed by attention.

When the terms scatter again, it is useful to reread the [feed-forward network](/AiBook/reference/concept-glossary/#feed-forward-network) glossary entry together with the four-component role division in P5-14.2.

## Why Process Once More After Attention?

Self-attention decides what information the current position should bring from other positions. But `what was referred to` and `how that referenced result should become the next representation of the current position` are not the same question.

For example, suppose the `restart` position in `hold restart while pressure remains unreleased` has looked at `pressure unreleased` and `hold` together through attention. Attention mixes the relation, but a separate transformation is needed to process that result more clearly toward one of `simple action`, `conditional action`, or `action to be blocked`. In the Transformer block, the feed-forward network takes that role.

In short, the division is as follows.

| Question | Component that handles it more directly | Why |
| --- | --- | --- |
| Which other position should the current position refer to? | self-attention | because it reads relationships among tokens |
| How should the current representation, now mixed with referenced context, change? | feed-forward network | because it nonlinearly reprocesses the representation inside the same position |

## What It Means To Apply The Same FFN To Several Positions

The feed-forward network in a Transformer usually applies the same weights to each position. Here, `same` does not mean every position becomes the same output. If the input representation differs by position, the output differs even after passing through the same transformation.

```mermaid
--8<-- "assets/part-05/chapter-14/feed-forward-position-update-en.mmd"
```

In this diagram, the dotted lines mean that the same weights are shared across several positions, and the solid lines mean that each position representation is processed separately inside its own position. So the feed-forward network is neither a device that passes state along in order nor a device that chooses a new position to refer to. It is a device that transforms each already context-mixed position representation again by the same rule.

Using the same FFN does not make every token have the same meaning. It should be read as `passing different input representations through the same processing criterion`.

## Why Nonlinear Processing Is Needed

If we read the feed-forward network as simple numeric post-processing, half of the Transformer block disappears. Even after attention mixes context, the representation is still a state where several cues have entered together. The feed-forward network further separates and compresses that mixed representation into the next representation of the current position.

| State remaining after attention | What feed-forward helps with |
| --- | --- |
| several cues are mixed, but the current position meaning is still blurry | process meaning axes more clearly inside the current position |
| differences such as condition, negation, and exception can remain weak under only simple linear combination | make differences in cue combinations stand out better through nonlinear transformation |
| each position received a different mixed context | apply the same FFN while producing different output representations for each position |

Here, the word `nonlinear` does not mean memorizing formulas immediately. At the introductory level, it is enough to read it as `a process that changes a merely added or averaged representation into a more separated representation that the next block can use`. In the example below, `relu` should be read only with this feel. When axes below 0 are folded to 0 after a linear computation, the output direction can bend differently from simple addition.

## Cases And Examples

### Case. Processing An Action Representation In A Work-Permit Sentence

If a person sees only the word `restart` in a work-permit sentence, the first thought is usually the action `turn the line on again`. But if `pressure unreleased` and `hold` are also in the sentence, the representation at the current position should change from a simple action name toward `an action that must be blocked because a condition is attached`.

Self-attention makes `restart` look together at `pressure unreleased` and `hold`. The feed-forward network then processes that mixed representation again inside the current position, helping the `restart` representation remain closer to a conditionally blocked action than to a simple execution request.

| Expression a person may first see | Context mixed after attention | Representation that should become clearer after feed-forward |
| --- | --- | --- |
| `restart` is an execution action | `pressure unreleased` and `hold` are mixed together | `an action to be blocked because a condition is attached` |
| `approval` is an allow signal | `verification incomplete` and `no exception` are mixed together | `not yet final approval` |
| `deployment` is work progress | `rollback not confirmed` and `symptom continues` are mixed together | `risky work before recovery is confirmed` |

The result to confirm in this case is that the feed-forward network does not find a new evidence position. It processes evidence that already entered through attention into a more separated meaning inside the current position representation.

## Practice And Example

### Example. Check Whether Outputs Differ By Position Even Through The Same FFN

This example is not an implementation of an actual Transformer. It is a small experiment for checking the position-wise processing feel of a feed-forward network. Assume that three position representations already have context mixed after attention, and that the same FFN weights are applied identically to each position.

| Value to Manipulate | Output to Observe | Question to Check |
| --- | --- | --- |
| each row of `positions` | `hidden`, `output` | do outputs differ by position even after passing through the same FFN? |
| input value of the `restart` position | `restart before/after` | if the current position representation changes, does the same FFN process it in a different direction? |
| change only `changed[1]` | `other positions unchanged` | does one position's FFN computation avoid newly referring to other positions? |

```python
# This example checks how each position's hidden and output are processed differently even when the same feed-forward network is shared across position-wise representations.
import numpy as np

output_axes = ["action_axis", "block_axis"]

positions = np.array([
    [0.2, 0.1, 0.9, 0.1],  # pressure_state: condition signal high
    [0.8, 0.2, 0.2, 0.1],  # restart: action signal high
    [0.3, 0.9, 0.2, 0.7],  # hold: block/negation signal high
])

position_names = ["pressure_state", "restart", "hold"]

w1 = np.array([
    [1.0, -0.2, 0.8],
    [0.3, 1.2, -0.6],
    [0.8, 0.1, 0.5],
    [-0.4, 0.7, 1.0],
])
b1 = np.array([-0.2, -0.1, 0.0])
w2 = np.array([
    [0.9, 0.2],
    [-0.3, 1.0],
    [0.4, 0.8],
])

def relu(x):
    return np.maximum(x, 0.0)

def ffn(x):
    hidden = relu(x @ w1 + b1)
    output = hidden @ w2
    return hidden, output

hidden, output = ffn(positions)

print("[same FFN, different positions]")
print("output axes =", output_axes)
for name, before, h, after in zip(position_names, positions, hidden, output):
    print(f"{name:15s} input={np.round(before, 2)} hidden={np.round(h, 2)} output={np.round(after, 2)}")

changed = positions.copy()
changed[1] += np.array([0.0, 0.5, 0.0, 0.4])
_, changed_output = ffn(changed)

print("
[change only restart position]")
print("restart before/after =", np.round(output[1], 2), "->", np.round(changed_output[1], 2))
print("other positions unchanged =", np.allclose(output[[0, 2]], changed_output[[0, 2]]))
```

Read the example output as follows.

```text
[same FFN, different positions]
output axes = ['action_axis', 'block_axis']
pressure_state  input=[0.2 0.1 0.9 0.1] hidden=[0.71 0.14 0.65] output=[0.86 0.8 ]
restart         input=[0.8 0.2 0.2 0.1] hidden=[0.78 0.07 0.72] output=[0.97 0.8 ]
hold            input=[0.3 0.9 0.2 0.7] hidden=[0.25 1.43 0.5 ] output=[-0.    1.88]

[change only restart position]
restart before/after = [0.97 0.8 ] -> [0.74 1.76]
other positions unchanged = True
```

The first output shows that even when the same FFN is applied, hidden and output differ if the input representation differs by position. Here, the first `output` value is read as `action_axis`, and the second as `block_axis`. For example, the `hold` position leaves a larger `block_axis`, and when hold-related cues are mixed more into the `restart` position, the second output shows `block_axis` growing from `0.8` to `1.76`. The second output also shows that changing only the input at the `restart` position changes only that position's output, while the outputs of other positions remain the same.

Explanation: The result to read in this example is that the feed-forward network is not a device for choosing a new token. Referring to other positions already happened at the attention stage, and the FFN passes each position's incoming representation through the same processing criterion. That is why outputs can differ by position even when the same FFN is shared.

### Practice. Turn The Current Position Representation Into Words

Assume that context has been mixed after attention in the scenes below. Write in words which direction the current position representation should be processed toward after feed-forward.

| Current Position | Cues Mixed By Attention | Representation Direction After Feed-Forward | Explanation |
| --- | --- | --- | --- |
| `restart` | `pressure unreleased`, `hold` | conditionally blocked action | it should be read as an action blocked by a safety condition, not only as the action itself |
| `approval` | `verification incomplete`, `no exception` | hold state before final approval | the incomplete condition should be reflected inside the current representation, not only the word approval |
| `deployment` | `rollback not confirmed`, `symptom continues` | risky work before recovery is confirmed | deployment should be processed as work that still leaves risk, not simple progress |

Explanation: A good answer is not a fancy term, but a clear statement of `which direction the current position representation should change`. First, write the basic meaning that comes to mind when the current-position word is seen by itself. Then add which cues entered together after attention. Finally, write which direction the current position representation should become clearer because those cues entered.

For example, if we see only `restart`, the basic meaning is `an execution action that turns the line on again`. But after attention, the cues `pressure unreleased` and `hold` have entered together. Then the representation direction after feed-forward is not a simple execution action, but `an action blocked by a safety condition`. So an answer can be written as: `restart looks like an execution action, but because pressure is still unreleased and a hold cue is present, the current position representation should be processed toward a conditionally blocked action`.

Writing it this way prevents `feed-forward output` in the representation-movement example integrated into P5-14.2 from being read as a mere intermediate number. The output numbers are not unlabeled calculation leftovers; they should be read as traces showing which meaning direction the current position representation has been organized toward.

## Checklist

- Can you explain the feed-forward network not as simple post-processing after attention, but as position-wise representation processing?
- Can you explain that even when the same FFN is applied to several positions, different input representations produce different output representations?
- Can you distinguish self-attention's `relationship reading` from the feed-forward network's `within-position transformation`?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
