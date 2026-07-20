# P5-13.2 The Flow That Leads To Self-Attention

> Section ID: `P5-13.2`
> Version: `v2026.07.20`

In P5-13.1, we explained attention as `a method that refers more strongly to positions important for the current computation`. The next question follows immediately.

Then if not only encoder-decoder reference, where the input and output are separate, but also each position inside one work-instruction sentence can directly refer to the others, what changes?

The core answer to this question is self-attention.

Self-attention is a method in which each token inside a sequence refers to other tokens in the same sequence and recalculates its current representation.

When you need to briefly confirm again the core mechanism right before the Transformer, return to the glossary entry on [self-attention](../../../reference/concept-glossary.md#self-attention).

## The Question Of How Self-Attention Rereads The Same Sequence

- How is self-attention different from attention?
- Why is the idea `tokens refer to one another inside their own sequence` important?
- In what sense is self-attention computationally different from RNNs?
- Why does it lead to the core of the Transformer?

The core point to hold first in this section is that `instead of tokens receiving a state sequentially, they directly refer again to other tokens in the same sequence and create new representations for themselves`. So here, rather than learning procedures such as optimizers or regularization, we first read the structure in which tokens inside the same sequence refer again to one another and update their representations through recalculated relationships.

The full Transformer structure is continued from P5-14.1 through P5-14.6, and an introductory explanation of query, key, value, and multi-head attention is revisited in supplementary reading P5-13.3.

There is one explanation that must be closed here. Rather than `does the token receive sequential state`, this section needs to make the reader understand the shift in computational feel toward `do the tokens reread one another and update their own representations`.

## Standards For Token Relations And Representation Updates

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

This difference becomes more direct if the attention weights are shown as bars. Even in the same memo, when the current token is `it` and when the current token is `not_put_on`, the distributions of reread cues are not the same.

![Self-attention weights of the current token `it`](../../../assets/part-05/chapter-13/self-attention-weight-it-en.svg)

![Self-attention weights of the current token `not_put_on`](../../../assets/part-05/chapter-13/self-attention-weight-cover-en.svg)

The first points to hold from this comparison are the following.

- even when reading the same sentence, the cues reread by `it` and the cues reread by `not_put_on` are different
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
| it feels as if the important cue is determined once for the whole sentence | the cue that `it` considers important and the cue that `not_put_on` considers important can differ |
| it is easy to understand self-attention only as `it sees the whole sentence` | the core is not seeing the whole sentence equally, but recalculating the relationships again for each token |

If we place the three cases together, the core of self-attention is not `the whole sentence is seen once`, but `what must be reread changes for each current token, and the new representation also changes accordingly`.

## Practice And Example

The goal of this example is to confirm directly, in a safety-inspection memo, which candidates inside the sentence the current token rereads more strongly, and how the current representation changes as a result. This time, instead of putting the tokens and scores only inside the code, we separate candidate tokens from several safety memos into a CSV file and read them from there.

Problem situation:

- the interpretation of the current token can change only when it rereads not just the adjacent word, but multiple positions in the sentence
- even in the same memo, the cue to reread can differ depending on whether the current token is `it` or `not_put_on`

Input:

- [`self-attention-safety-memo-candidates.csv`](../../../assets/part-05/chapter-13/self-attention-safety-memo-candidates.csv){ .csv-preview }
- 3 safety-memo scenarios, 6 current-token conditions, and 36 candidate-token rows
- simple meaning vectors for each candidate token: `evidence_pack`, `evidence_cap`, `evidence_action`
- the current-token-specific relevance score `score`

Output:

- a baseline representation that averages the candidate tokens of the current memo equally
- attention weights calculated at the positions `it` and `not_put_on`
- the new representation of each token after self-attention
- a summary of which token group was reflected most strongly

One CSV row means `how strongly one current token in a specific memo rereads one candidate token`. For example, in the `memo_cap_missing` memo, `it` and `not_put_on` look at the same candidate-token set, but the `score` distribution changes because the target token is different.

First look at part of the CSV.

| document_id | target_token | candidate_token | candidate_role | evidence_pack | evidence_cap | evidence_action | score |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| memo_cap_missing | it | insulating_cap | missing_object | 0.1 | 0.95 | 0.2 | 2.4 |
| memo_cap_missing | it | not_put_on | missing_action | 0.0 | 0.7 | 0.9 | 1.7 |
| memo_cap_missing | not_put_on | separated | prior_action | 0.8 | 0.2 | 0.4 | 1.7 |
| memo_cap_missing | not_put_on | insulating_cap | missing_object | 0.1 | 0.95 | 0.2 | 2.1 |
| memo_pressure_hold | restart | restart | current_decision | 0.5 | 0.1 | 0.6 | 2.4 |
| memo_flow_alarm | release | shortage | risk_state | 0.1 | 0.7 | 0.9 | 2.3 |

Before looking at the code, it helps to predict first where the weight will gather when the current token changes even though the sentence stays the same.

| Current token | Misunderstanding that can easily arise in the baseline | Change to predict first in self-attention |
| --- | --- | --- |
| `it` | if we only look at the whole-memo average, it can feel unnecessary to distinguish which safety cue matters more | more weight should go to the cues around `insulating cap` and `not put on` |
| `not_put_on` | because it is in the same memo, it can feel as if the distribution should look similar to `it` | for the action context, more weight can go to `separated` and `insulating cap` |
| both | it can feel as if each sentence has only one common attention distribution | for each token, the target reread from its own perspective should differ |

Input:

Read the CSV and compare the two current tokens in `memo_cap_missing`.

```python
from pathlib import Path
import csv
import math

DATA_PATH = Path("docs/assets/part-05/chapter-13/self-attention-safety-memo-candidates.csv")
FOCUS_DOCUMENT_ID = "memo_cap_missing"
TARGET_TOKENS = ["그것", "씌우지"]
VECTOR_COLUMNS = ["evidence_pack", "evidence_cap", "evidence_action"]

DISPLAY_TOKEN = {
    "배터리팩": "battery_pack",
    "분리": "separated",
    "절연캡": "insulating_cap",
    "씌우지": "not_put_on",
    "그것": "it",
    "위험": "risk",
}

DISPLAY_TARGET = {
    "그것": "it",
    "씌우지": "not_put_on",
}

with DATA_PATH.open(encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))

focus_rows = [row for row in rows if row["document_id"] == FOCUS_DOCUMENT_ID]

unique_candidates = []
seen = set()
for row in focus_rows:
    token = row["candidate_token"]
    if token not in seen:
        seen.add(token)
        unique_candidates.append(row)

baseline_representation = [
    sum(float(row[column]) for row in unique_candidates) / len(unique_candidates)
    for column in VECTOR_COLUMNS
]

def softmax(scores):
    max_score = max(scores)
    exp_scores = [math.exp(score - max_score) for score in scores]
    total = sum(exp_scores)
    return [score / total for score in exp_scores]

print("csv_rows =", len(rows))
print("focus_document_rows =", len(focus_rows))
print("baseline_representation =", [round(value, 3) for value in baseline_representation])
print()

def run_self_attention(target_token):
    target_rows = [row for row in focus_rows if row["target_token"] == target_token]
    weights = softmax([float(row["score"]) for row in target_rows])
    new_representation = [
        sum(weight * float(row[column]) for weight, row in zip(weights, target_rows))
        for column in VECTOR_COLUMNS
    ]
    top_row, top_weight = max(zip(target_rows, weights), key=lambda item: item[1])
    cap_weight = sum(
        weight
        for row, weight in zip(target_rows, weights)
        if row["candidate_token"] in {"절연캡", "씌우지"}
    )

    print("target_token =", DISPLAY_TARGET[target_token])
    for row, weight in zip(target_rows, weights):
        vector = [float(row[column]) for column in VECTOR_COLUMNS]
        print(
            DISPLAY_TOKEN[row["candidate_token"]],
            "weight =", round(weight, 3),
            "role =", row["candidate_role"],
            "vector =", [round(value, 3) for value in vector],
        )
    print("new_representation =", [round(value, 3) for value in new_representation])
    print(
        "representation_shift =",
        [round(new - base, 3) for new, base in zip(new_representation, baseline_representation)],
    )
    print("top_token =", DISPLAY_TOKEN[top_row["candidate_token"]])
    print("cap_plus_not_applied_weight =", round(cap_weight, 3))
    print()

for target_token in TARGET_TOKENS:
    run_self_attention(target_token)
```

In the output, first distinguish the full CSV range from the current comparison range by looking at `csv_rows` and `focus_document_rows`. Then read each current token's `weight`, `new_representation`, and `representation_shift` in order.

```text
csv_rows = 36
focus_document_rows = 12
baseline_representation = [0.383, 0.475, 0.417]

target_token = it
battery_pack weight = 0.048 role = equipment vector = [0.9, 0.1, 0.0]
separated weight = 0.079 role = prior_action vector = [0.8, 0.2, 0.4]
insulating_cap weight = 0.43 role = missing_object vector = [0.1, 0.95, 0.2]
not_put_on weight = 0.214 role = missing_action vector = [0.0, 0.7, 0.9]
it weight = 0.087 role = current_token vector = [0.3, 0.3, 0.3]
risk weight = 0.143 role = risk_question vector = [0.2, 0.6, 0.7]
new_representation = [0.203, 0.691, 0.436]
representation_shift = [-0.18, 0.216, 0.019]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.644

target_token = not_put_on
battery_pack weight = 0.067 role = equipment vector = [0.9, 0.1, 0.0]
separated weight = 0.246 role = prior_action vector = [0.8, 0.2, 0.4]
insulating_cap weight = 0.367 role = missing_object vector = [0.1, 0.95, 0.2]
not_put_on weight = 0.182 role = current_action vector = [0.0, 0.7, 0.9]
it weight = 0.055 role = other_reference vector = [0.3, 0.3, 0.3]
risk weight = 0.082 role = risk_question vector = [0.2, 0.6, 0.7]
new_representation = [0.327, 0.598, 0.41]
representation_shift = [-0.056, 0.123, -0.007]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.55
```

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| in `weights`, `insulating_cap` is largest and `not_put_on` is also high | the current token `it` does not look at cues in the memo equally, but rereads certain safety cues more strongly | if the CSV `score` values are changed, which cue drives the interpretation of the current token changes immediately |
| the `weights` distributions of `it` and `not_put_on` are not the same | even when reading the same memo, the target reread differs for each current token | if the `target_token` changes, which position becomes the top token also changes immediately |
| `cap_plus_not_applied_weight = 0.644` | not only one word, but a group of related cues pulls the interpretation together | if the score of `insulating_cap` or `not_put_on` is lowered, we can see in which direction the risk-cause interpretation begins to shake |
| the second axis rises strongly in `representation_shift` | after attention, the current token representation actually moved again toward a particular contextual direction | if the token vectors change, we can directly compare which meaning axis is emphasized more |

| Current token | Easy judgment if we read only from the baseline | Judgment that changes after reading the self-attention output |
| --- | --- | --- |
| `it` | because the whole memo is one lump, it becomes easy to treat `separated` and `insulating cap not applied` similarly | because the weight on `insulating_cap` and `not_put_on` is high, the risk cause should be checked first on the side of `insulating cap not applied` |
| `not_put_on` | it becomes easy to read only that `something was not done` by following the current action alone | because it refers strongly again to `separated` and `insulating_cap` together, the work context of `what was not put on to what` must also be reconstructed |

That is, the purpose of reading the numbers is not to memorize `which weight was the largest`. It is to confirm whether, even in the same memo, `what must be checked again` actually separates when the current token changes.

- in the baseline average, `battery_pack`, `separated`, `insulating_cap`, `not_put_on`, `it`, and `risk` are all mixed with the same weight, so there is no emphasis on what the current token `it` refers to
- the current token representation is not determined by itself alone, but is recalculated by rereading other tokens in the memo
- in this example, `it` refers much more strongly to the cues around `insulating_cap` and `not_put_on` than to `separated`, so the risk-cause interpretation leans toward `insulating cap not applied`
- even in the same memo, when `not_put_on` is used as the current token, the weight on `separated` and `insulating_cap` rises again, producing a distribution different from the one used to interpret `it`
- the fact that the combined weight of `insulating_cap` and `not_put_on` is 0.644 for `it` and 0.55 for `not_put_on` shows that self-attention reflects not only one word, but a bundle of related cues together
- the fact that the second axis increases strongly in `representation_shift` gives the intuition that the current token representation was pulled again toward the `insulating_cap/not_put_on` context
- that is, self-attention can be read as a way of quantifying separately for each token `where inside the sentence should I look again to understand this token now`

If we translate this result back into field-memo reading, when reading `it`, the gaze gathers toward checking `what is missing`, while when reading `not_put_on`, the gaze gathers toward restoring `to what that action was not applied`. Self-attention can be understood as making exactly this `token-specific rereading path split` into a computation.

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
- the self-attention result is closer to `a representation recalculated by asking who the current token 'it' should refer to more strongly now`
- so what the reader needs to distinguish in practice is not simply `did it see the whole sentence`, but `was the rereading priority recalculated differently for each current token`

That is, self-attention is not merely a function that sees the whole sentence, but `a computation in which each token rereads the full sentence again from its own standpoint and creates a new representation`. Only when this feel is fixed can the QKV and multi-head attention in P5-13.3 be read not as `a section for memorizing names`, but as `a section that explains this rereference computation more structurally`.

The transition to confirm in self-attention is that attention did not remain only an auxiliary device for translation, but moved to the central computation method of sequence modeling. The conclusion the reader should keep from this section is also simple. Self-attention is not `the whole sentence is seen once`, but `for each current token, the positions to reread are calculated and the token's own representation is rebuilt`. In the next chapter, P5-14.1, we explain how this computation becomes grouped as the basic unit of the Transformer block.

## Checklist

- Can you explain that self-attention is a method in which tokens inside the same sequence refer to one another?
- Can you explain the difference between sequential state transfer and relationship recalculation?
- Can you explain self-attention not merely as `it sees the whole sentence`, but as `each token rereads other tokens in the same sequence and updates its own representation`?
- Can you explain the different advantage from RNNs in that it can rereference distant cues while also allowing token computation to be processed in parallel?
- Can you explain through an example that, even in the same sentence, the cues reread and the priority of judgment change depending on whether the current token is `it` or `not_put_on`?
- When recalculating the relationships among tokens seems more important than sequential transfer, can you recall the self-attention viewpoint first?
- When reading the next chapter on the Transformer, are you ready first to ask `why did self-attention become block-centered computation`?

## Sources And References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, checked on 2026-07-19. [https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
