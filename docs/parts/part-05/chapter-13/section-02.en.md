# P5-13.2 The Flow That Leads To Self-Attention

Section ID: `P5-13.2`
Version: `v2026.07.18`

In P5-13.1, we explained attention as `a method that refers more strongly to positions important for the current computation`. The next question follows immediately.

Then if not only encoder-decoder reference, where the input and output are separate, but also each position inside one work-instruction sentence can directly refer to the others, what changes?

The core answer to this question is self-attention.

Self-attention is a method in which each token inside a sequence refers to other tokens in the same sequence and recalculates its current representation.

When you need to briefly confirm again the core mechanism right before the Transformer, return to the glossary entry on [self-attention](/AiBook/reference/concept-glossary/#self-attention).

## Scope Of This Section

- How is self-attention different from attention?
- Why is the idea `tokens refer to one another inside their own sequence` important?
- In what sense is self-attention computationally different from RNNs?
- Why does it lead to the core of the Transformer?

The core point to hold first in this section is that `instead of tokens receiving a state sequentially, they directly refer again to other tokens in the same sequence and create new representations for themselves`. So here, rather than learning procedures such as optimizers or regularization, we first read the structure in which tokens inside the same sequence refer again to one another and update their representations through recalculated relationships.

The full Transformer structure is continued in P5-14.1 and P5-14.2, and an introductory explanation of query, key, value, and multi-head attention is revisited in supplementary reading P5-13.3.

There is one explanation that must be closed here. Rather than `does the token receive sequential state`, this section needs to make the reader understand the shift in computational feel toward `do the tokens reread one another and update their own representations`.

## Goals Of This Section

- You can explain self-attention as `mutual reference among tokens inside a sequence`.
- You can say that self-attention gives a computational feel different from RNN-style sequential transfer.
- You can say what advantages self-attention gives for parallel processing and long-context problems.
- Through an executable Python example, you can confirm the intuition of token-to-token importance reference.

## What Is Different Between Attention And Self-Attention

Broadly speaking, attention is `a method that decides which positions the current computation should refer to more strongly`. In self-attention, the key difference is that those reference targets are inside the same sequence.

For example, inside a sentence:

- each word can refer to other words
- and the representation of the current word can be recalculated by gathering relevant token information again from the whole sentence

That is, self-attention is not `bringing in information from outside the sentence`, but `rereading the internal relationships of the sentence`.

If P5-13.1 was a section asking `which part of the input should the current output refer to more strongly`, here the question changes into `how does the current token reread other tokens in the same sentence`.

If we split the same scene into these two methods, the difference becomes clearer.

| The same scene | Relationship read first in attention | Relationship read first in self-attention |
| --- | --- | --- |
| the moment one line of a multilingual work-instruction phrase is being written | which position in the input procedure should the current output phrase refer to more strongly | how should each token inside the current work-instruction sentence reread the others |
| the moment one handoff-summary sentence is being created | which original sentence should the current summary sentence look at more | how do token representations inside the record reread one another and change again |
| the moment one line of maintenance code is being interpreted | which earlier input position should the current output refer to more strongly | how do names, conditions, and call positions inside the code reconnect to one another again |

That is, if attention is closer to `where should the current output look more`, self-attention is closer to `how should each position inside the sentence reread the others`. The core point here is not only that the reference targets moved inward, but that the reference distribution recalculated for each current token can differ.

If we compress only the transition from attention to self-attention, it can be read as follows.

```mermaid
--8<-- "assets/part-05/chapter-13/attention-to-self-attention-bridge-en.mmd"
```

That is, the reference method `where in the input should the current output look` can be seen as extending inward into `how each token should reread other tokens inside the same sequence`.

## Why Is This Important

RNNs usually give a strong feeling of passing state along the flow of time, whether forward only or bidirectional. Self-attention differs in that the current token can refer comparatively directly to even distant tokens when needed.

The core difference is that RNNs are closer to passing state along, while self-attention is closer to recalculating the needed token relationships.

`RNNs are closer to passing memory along, while self-attention is closer to finding the needed words again.`

That is, for the problem of older information becoming faint, self-attention creates a more direct reference path. The key to reading self-attention in this section lies not in `it sees the whole sentence`, but in `the current token recalculates the relationships it needs`.

This difference can be summarized more briefly in the following table.

| Viewpoint | RNN family | self-attention |
| --- | --- | --- |
| basic feel | passes state to the next step | recalculates relatedness among all tokens |
| access to distant information | passed through many steps | can be referred to more directly |
| computational feel | sequential transfer | relationship computation |

The key point that the reader must hold here is that `self-attention is not a structure that passes memory along, but a structure that recalculates relationships`.

## What Happens Inside A Sentence

For example, in the sentence:

`The animal didn't cross the road because it was tired.`

to understand what `it` refers to, we need to look at the relationships with other words in the sentence. Self-attention matches this kind of introductory intuition extremely well.

Each token:

- does not look only at itself
- calculates relatedness with other tokens
- reflects more strongly the information from the more important tokens
- and creates a new representation

That is, self-attention rewrites token representations again in context.

If we rewrite this through a very short example, it becomes the following.

```text
The battery pack was placed on the workbench, and the insulating cap was on the side tray. It had not yet been put on.
```

When reading `it` here, looking only at the immediately preceding word is not enough to judge stably whether it refers to `the tray` or `the insulating cap`. From the self-attention viewpoint, the position of `it` rereads other words in the sentence again and can place larger weight on the candidate that fits the current context better. That is, the core feel is `to understand one current token, the sentence is mixed and reread again as a whole`.

## Why Did It Become The Core Of The Transformer

Self-attention matters not simply because it `looks smarter`. It changes the computational structure itself.

In particular, the following two differences are important from the reader's point of view.

1. It can refer more directly to distant positions.
2. It no longer has to pass state only sequentially, so it fits well with parallel computation.

That is, self-attention looked like a direction that could satisfy both the long-term dependency problem and the need for parallel processing more effectively. This is one reason it became a core part of the Transformer.

In other words, self-attention moved to the center of the architecture because `it was easier to find distant cues again, and the computation was also easier to handle all at once`. The important point here is not merely `there is attention`, but that `the computation that rewrites each token representation again` became block-centered.

One more point the reader should hold here is that self-attention did not remain just `one good feature`, but became a `block-centered computation`. That is, the Transformer repeats as its basic unit a structure that `first rereads relationships through self-attention, and then passes the result to the next computation`. This connection is exactly the starting point of P5-14.1.

## If We Draw This Very Simply

```mermaid
--8<-- "assets/part-05/chapter-13/self-attention-token-graph-en.mmd"
```

This diagram compresses the intuition that each token can refer to other tokens. The real implementation is more precise, but the point to confirm here first is that the tokens do not only pass information from front to back, but instead calculate relatedness with one another together.

`One token does not only receive from the previous token, but rereads other tokens in the sentence together and rebuilds its own representation.`

If we fix once more, very briefly, that even inside the same input sentence the position reread changes when the current token changes, it can be seen like this.

```mermaid
--8<-- "assets/part-05/chapter-13/self-attention-target-shift-en.mmd"
```

This difference becomes more direct if the attention weights are shown as bars. Even in the same memo, when the current token is `it` and when the current token is `cover`, the distributions of reread cues are not the same.

![Self-attention weights of the current token `it`](/AiBook/assets/part-05/chapter-13/self-attention-weight-it-en.svg)

![Self-attention weights of the current token `cover`](/AiBook/assets/part-05/chapter-13/self-attention-weight-cover-en.svg)

The first points to hold from this comparison are the following.

- even when reading the same sentence, the cues reread by `it` and the cues reread by `cover` are different
- so the core of self-attention is not `the whole sentence is read once`, but `the position to reread changes for each current token`
- only when this feel is fixed does it become easier to read the next QKV and multi-head discussion as computational names for `per-token questions` and `split relationships`

## Why Does Self-Attention Fit Parallel Processing Well

RNNs pass state in temporal order, so the computational flow feels strongly sequential. Self-attention treats each token's relatedness calculation in a more matrix-like way, making it fit GPU parallel processing well.

`Self-attention is closer to calculating the relationships among tokens all at once than to pushing tokens forward only in order.`

This point also connects naturally to the Part 5 discussion of GPU, batch, and tensor computation.

## Cases And Examples

### Representative Case. Interpreting A Referring Expression Inside A Sentence

Suppose a safety-inspection memo says, `The battery pack was separated, but the insulating cap was not put on. Is that the cause of the risk?` When people read it roughly, they often first guess the meaning by looking only at the word right next to `that`. But in reality, whether `that` refers to the insulating cap or to the fact of separation can change the content of the follow-up action. If we follow only the nearby words, it becomes easy to miss this reference relationship. The key change here is that the standard moves from `reading only the immediately previous word` to `reading the full sentence relationship together`. Self-attention gives the intuition that the current token rereads other positions in the sentence and calculates more directly what it refers to.

So the result to confirm in this case is whether the current token `that` becomes clearer not by looking only at the immediately previous word, but by showing which candidate among several positions in the sentence should actually be reread more strongly.

The same viewpoint extends directly to interpreting condition scope inside one sentence and to reading one line of code. But the core point to hold in this section is not the domain name, but `whether the target to reread changes for each current token, and whether the new representation changes accordingly`.

| Case | What the current position needs to reread | Problem if only nearby positions are followed | Result to confirm through self-attention |
| --- | --- | --- | --- |
| pronoun interpretation | the earlier noun that the pronoun refers to | it can connect incorrectly if only the adjacent word is followed | whether a more plausible referent is chosen by reflecting the relationship of the whole sentence |
| interpreting condition scope | the condition expression, the action expression, and the span of negation | it can misread how far the prohibition extends if only the action word is followed | whether the sentence relationship is reread to regroup how far the condition reaches |
| interpreting one line of code | variable names, negation, and logical operators | it can misread the meaning of the condition by following only the most noticeable variable | whether the code-sequence relationships are reread so negation and combination order are understood together |

| Standard that is easy for a person to see first | Standard to reread from the self-attention viewpoint |
| --- | --- |
| it feels as if one common context is enough after reading the whole sentence once | because each token has a different target it needs to reread from its own position, each token should also end up with a different new representation |
| it feels as if the important cue is determined once for the whole sentence | the cue that `it` considers important and the cue that `cover` considers important can differ |
| it is easy to understand self-attention only as `it sees the whole sentence` | the core is not seeing the whole sentence equally, but recalculating the relationships again for each token |

If we place the three cases together, the core of self-attention is not `the whole sentence is seen once`, but `what must be reread changes for each current token, and the new representation also changes accordingly`.

## Practice And Example

The goal of this example is to confirm directly, in a safety-inspection memo, which earlier candidates a current token such as `that` refers to more strongly, and how the current representation changes as a result. That is, we experiment with self-attention not as a plain numeric average, but as `the process by which the current token rereads the relevant cues in the memo`.

Problem situation:

- the interpretation of the current token can change only when it rereads not just the adjacent word, but multiple positions in the sentence

Input:

- a short memo: `The battery pack was separated, but the insulating cap was not put on. Is that the cause of the risk?`
- scores showing how much the current tokens `that` and `cover` refer to each token in the sentence
- simple meaning vectors for each token

Output:

- a baseline representation that averages all tokens equally
- attention weights calculated at the positions `that` and `cover`
- the new representation of each token after self-attention
- a summary of which token group was reflected most strongly

Before reading the code, if we look in order first at the following three values, it becomes easier to catch how self-attention differs from `simply averaging the whole sentence`.

| Value to look at first | Why it should be looked at first |
| --- | --- |
| `baseline_representation` | because it first shows how blurry the interpretation of the current token becomes if everything is mixed without weight differences |
| `weights` | because we can directly compare which cues in the sentence the current token rereads more strongly |
| `representation_shift` | because at the end we can group together in which direction the current token representation actually moved after attention recalculation |

Problem situation:

- it is more intuitive to understand self-attention as how strongly the current token rereads other tokens in the sentence

Concepts to confirm:

- self-attention is a structure in which the current token rereads other tokens in the sentence and changes its own representation
- when distant cues matter, as in pronoun interpretation, position-wise weights are needed more than a simple average
- even in the same sentence, if the current token changes, the reread target also changes
- only by comparing the baseline representation with the new representation does the role of self-attention become visible

Before looking at the code, it helps to predict first where the weight will gather when the current token changes even though the sentence stays the same.

| Current token | Misunderstanding that can easily arise in the baseline | Change to predict first in self-attention |
| --- | --- | --- |
| `that` | if we only look at the whole-memo average, it can feel unnecessary to distinguish which safety cue matters more | more weight should go to the cues around `insulating cap` and `not put on` |
| `cover` | because it is in the same memo, it can feel as if the distribution should look similar to `that` | for the action context, more weight can go to `separated` and `insulating cap` |
| both | it can feel as if each sentence has only one common attention distribution | for each token, the target reread from its own perspective should differ |

The actual difference we want to confirm is exactly what this table states. `That` needs to narrow down again `what is the cause of the risk`, while `cover` needs to narrow down again `what work context is missing`. That is, even in the same memo, if the current token differs, the example works properly only when `the cue that needs to be reread` also differs.

Input:

We use the token list and the vector representation for each token summarized above.

```python
# This example compares how self-attention changes referenced clues and new representations when the current token changes inside the same note.
import math

tokens = ["battery_pack", "separated", "insulating_cap", "not_put_on", "that"]
token_vectors = {
    "battery_pack": [0.8, 0.1, 0.0],
    "separated": [0.9, 0.3, 0.1],
    "insulating_cap": [0.1, 0.9, 0.2],
    "not_put_on": [0.0, 0.6, 0.8],
    "that": [0.3, 0.3, 0.3],
}

# current token-specific raw scores:
# "that" focuses on what the risk refers to,
# while "not_put_on" focuses more on the action context around insulating the pack.
raw_scores_by_target = {
    "that": {
        "battery_pack": 0.2,
        "separated": 0.6,
        "insulating_cap": 2.1,
        "not_put_on": 1.2,
        "that": 0.7,
    },
    "not_put_on": {
        "battery_pack": 0.1,
        "separated": 1.4,
        "insulating_cap": 1.8,
        "not_put_on": 0.9,
        "that": 0.2,
    },
}

baseline_representation = [0.0, 0.0, 0.0]
uniform_weight = 1 / len(tokens)
for token in tokens:
    vector = token_vectors[token]
    for idx in range(len(vector)):
        baseline_representation[idx] += uniform_weight * vector[idx]

print("baseline_representation =", [round(value, 3) for value in baseline_representation])
print()

def run_self_attention(target_token, score_table):
    ordered_scores = [score_table[token] for token in tokens]
    exp_scores = [math.exp(score) for score in ordered_scores]
    total = sum(exp_scores)
    weights = [s / total for s in exp_scores]

    new_representation = [0.0, 0.0, 0.0]
    for weight, token in zip(weights, tokens):
        vector = token_vectors[token]
        for idx in range(len(vector)):
            new_representation[idx] += weight * vector[idx]

    print("target_token =", target_token)
    for token, weight in zip(tokens, weights):
        print(token, "weight =", round(weight, 3), "vector =", token_vectors[token])
    print("weights =", [round(w, 3) for w in weights])
    print("new_representation =", [round(value, 3) for value in new_representation])
    print(
        "representation_shift =",
        [round(new - base, 3) for new, base in zip(new_representation, baseline_representation)],
    )
    top_token = tokens[weights.index(max(weights))]
    print("top_token =", top_token)
    print(
        "cap_plus_not_applied_weight =",
        round(weights[tokens.index("insulating_cap")] + weights[tokens.index("not_put_on")], 3),
    )
    print()

run_self_attention("that", raw_scores_by_target["that"])
run_self_attention("not_put_on", raw_scores_by_target["not_put_on"])
```

In the output, start by comparing the `weight` of each token, and then look at how the distribution changes even in the same sentence when the current token changes. Then continue by looking at how `new_representation` and `representation_shift` separate in direction.

```text
baseline_representation = [0.42, 0.44, 0.28]
 
target_token = that
battery_pack weight = 0.074 vector = [0.8, 0.1, 0.0]
separated weight = 0.11 vector = [0.9, 0.3, 0.1]
insulating_cap weight = 0.494 vector = [0.1, 0.9, 0.2]
not_put_on weight = 0.201 vector = [0.0, 0.6, 0.8]
that weight = 0.122 vector = [0.3, 0.3, 0.3]
weights = [0.074, 0.11, 0.494, 0.201, 0.122]
new_representation = [0.244, 0.642, 0.307]
representation_shift = [-0.176, 0.202, 0.027]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.694

target_token = not_put_on
battery_pack weight = 0.074 vector = [0.8, 0.1, 0.0]
separated weight = 0.272 vector = [0.9, 0.3, 0.1]
insulating_cap weight = 0.406 vector = [0.1, 0.9, 0.2]
not_put_on weight = 0.165 vector = [0.0, 0.6, 0.8]
that weight = 0.082 vector = [0.3, 0.3, 0.3]
weights = [0.074, 0.272, 0.406, 0.165, 0.082]
new_representation = [0.37, 0.578, 0.265]
representation_shift = [-0.05, 0.138, -0.015]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.571
```

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| in `weights`, `insulating_cap` is largest and `not_put_on` is also high | the current token `that` does not look at cues in the memo equally, but rereads certain safety cues more strongly | if the raw scores are changed, which cue drives the interpretation of the current token changes immediately |
| the `weights` distributions of `that` and `not_put_on` are not the same | even when reading the same memo, the target reread differs for each current token | if the target token changes, which position becomes the top token also changes immediately |
| `top_token = insulating_cap` and `cap_plus_not_applied_weight = 0.694` appear together | not only one word, but a group of related cues pulls the interpretation together | if the score of `insulating_cap` or `not_put_on` is lowered, we can see in which direction the risk-cause interpretation begins to shake |
| the second axis rises strongly in `representation_shift` | after attention, the current token representation actually moved again toward a particular contextual direction | if the token vectors change, we can directly compare which meaning axis is emphasized more |

| Current token | Easy judgment if we read only from the baseline | Judgment that changes after reading the self-attention output |
| --- | --- | --- |
| `that` | because the whole memo is one lump, it becomes easy to treat `separated` and `insulating cap not applied` similarly | because the weight on `insulating_cap` and `not_put_on` is high, the risk cause should be checked first on the side of `insulating cap not applied` |
| `not_put_on` | it becomes easy to read only that `something was not done` by following the current action alone | because it refers strongly again to `separated` and `insulating_cap` together, the work context of `what was not put on to what` must also be reconstructed |

That is, the purpose of reading the numbers is not to memorize `which weight was the largest`. It is to confirm whether, even in the same memo, `what must be checked again` actually separates when the current token changes.

- in the baseline average, `battery_pack`, `separated`, `insulating_cap`, and `not_put_on` are all mixed with the same weight, so there is no emphasis on what the current token `that` refers to
- the current token representation is not determined by itself alone, but is recalculated by rereading other tokens in the memo
- in this example, `that` refers much more strongly to the cues around `insulating_cap` and `not_put_on` than to `separated`, so the risk-cause interpretation leans toward `insulating cap not applied`
- even in the same memo, when `not_put_on` is used as the current token, the weight on `separated` and `insulating_cap` rises again, producing a distribution different from the one used to interpret `that`
- the fact that the combined weight of `insulating_cap` and `not_put_on` is 0.694 shows that self-attention reflects not only one word, but a bundle of related cues together
- the fact that the second axis increases strongly in `representation_shift` gives the intuition that the current token representation was pulled again toward the `insulating_cap/not_put_on` context
- that is, self-attention can be read as a way of quantifying separately for each token `where inside the sentence should I look again to understand this token now`

If we translate this result back into field-memo reading, when reading `that`, the gaze gathers toward checking `what is missing`, while when reading `not_put_on`, the gaze gathers toward restoring `to what that action was not applied`. Self-attention can be understood as making exactly this `token-specific rereading path split` into a computation.

Rather than reading the result once and moving on, it is better to continue by checking directly what value changes make the feel of `rereference` clearer.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| the weight on `insulating_cap` is the largest | raise the raw score of `separated` or `battery_pack` and see where the center of risk-cause interpretation moves | do not conclude that a large attention weight immediately guarantees complete semantic understanding |
| `cap_plus_not_applied_weight` is high | lower or raise the score of `not_put_on` and see how the cue bundle moves together | do not conclude that because two cues are both high, the correct answer is always fixed |
| `representation_shift` moves far away from the baseline | change the axes of the token vectors and compare which meaning axis is more sensitive to recalculation | do not substitute this one simple vector comparison for the whole of real multi-head self-attention |

That is, self-attention is `a method that sees context and then recalculates the representation again`.

## If We Reread This Example From The Viewpoint Of Reinterpreting The Current Token

The numbers above do not implement all of large-scale self-attention, but the comparison standard is clear.

- the baseline average is closer to `a representation that just mixes the whole sentence information together`
- the self-attention result is closer to `a representation recalculated by asking who the current token 'that' should refer to more strongly now`
- so what the reader needs to distinguish in practice is not simply `did it see the whole sentence`, but `was the rereading priority recalculated differently for each current token`

That is, self-attention is not merely a function that sees the whole sentence, but `a computation in which each token rereads the full sentence again from its own standpoint and creates a new representation`. Only when this feel is fixed can the QKV and multi-head attention in P5-13.3 be read not as `a section for memorizing names`, but as `a section that explains this rereference computation more structurally`.

The transition to confirm in self-attention is that attention did not remain only an auxiliary device for translation, but moved to the central computation method of sequence modeling. The conclusion the reader should keep from this section is also simple. Self-attention is not `the whole sentence is seen once`, but `for each current token, the positions to reread are calculated and the token's own representation is rebuilt`. In the next chapter, P5-14.1, we explain how this computation becomes grouped as the basic unit of the Transformer block.

## Checklist

- Can you explain that self-attention is a method in which tokens inside the same sequence refer to one another?
- Can you explain the difference between sequential state transfer and relationship recalculation?
- Can you explain self-attention not merely as `it sees the whole sentence`, but as `each token rereads other tokens in the same sequence and updates its own representation`?
- Can you explain the different advantage from RNNs in that it can rereference distant cues while also allowing token computation to be processed in parallel?
- Can you explain through an example that, even in the same sentence, the cues reread and the priority of judgment change depending on whether the current token is `that` or `not_put_on`?
- When recalculating the relationships among tokens seems more important than sequential transfer, can you recall the self-attention viewpoint first?
- When reading the next chapter on the Transformer, are you ready first to ask `why did self-attention become block-centered computation`?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-06-29.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, checked on 2026-06-29.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
