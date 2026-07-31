# P5-14.1 Why Attention Alone Does Not Settle the Transformer

> Section ID: `P5-14.1`
> Version: `v2026.07.31`

The starting point for this chapter is not a single `attention_score`, but how `token_representation` moves into the next representation as it passes through a block. From P5-14.1 onward, read `relation_reading`, `position_update`, `stable_passage`, and `next_block_input` as one flow.

_Subtitle: Why should the Transformer be read as a block structure, not just as self-attention?_

In P5-13.2, we saw that self-attention is a method in which tokens inside the same sequence reread one another and update their representations. The immediate next question is this.

Is it enough to say that the Transformer is a model that uses self-attention?

It is not enough. The Transformer is a block structure that reads relationships through self-attention, reprocesses each position representation through a feed-forward network, and stabilizes deep repeated computation through residual connections and layer normalization. We need to hold this difference so that, later, when reading about parallel processing, long context, and LLM structure, we do not end the explanation with only `it has attention`.

## Question Handled by the Basic Transformer Problem

- If self-attention is central to the Transformer, why does the explanation not end there?
- As what bundle of roles should a Transformer block be read?
- What should Part 5 settle about the Transformer, and what should be passed to the next section?

The question to settle first here is not `what parts does the Transformer have`, but `why did self-attention and feed-forward need to be bundled into a repeatable block`.

| What this section reads now | What is passed to later sections |
| --- | --- |
| the standard for reading the Transformer as a block structure, not as self-attention alone | the detailed role of each component and the representation update process |
| the feel that relationship reading, position-wise processing, and stable transfer are all needed together | parallel processing, direct rereference in long context, and the connection to generative models |

## What Is Missing with Self-Attention Alone?

Self-attention is strong at deciding which other tokens the current token should refer to more. But once the model becomes deep, the next questions immediately follow.

- How should the gathered context information be processed again at the current position?
- How can the new computation avoid overwriting the original information too strongly?
- When many layers repeat, how can value scale and distribution avoid shaking too much?

If these questions are left open, the Transformer is understood only as `a model with attention`. A safer standard is the following.

`The Transformer is a structure that bundles self-attention's relationship reading, feed-forward's position-wise representation processing, and stable transfer into one repeatable block.`

## First Seeing the Basic Block as a Big Picture

At an introductory level, it is enough to distinguish four elements first.

| Component | Role to hold first |
| --- | --- |
| self-attention | reads relationships with other tokens |
| feed-forward network | reprocesses each position representation |
| residual connection | leaves the original information flow together |
| layer normalization | organizes the value range so the computation shakes less |

These four are not a scattered list of parts. They are usually bundled as a repeating unit that `reads contextual relationships -> processes the current position representation -> preserves original information and stability -> passes the result to the next block`.

```mermaid
--8<-- "assets/part-05/chapter-14/transformer-block-repeat-en.mmd"
```

What matters in this diagram is not one attention computation, but the fact that the same bundle repeats again in the next block. So in P5-14.1, before the detailed calculation, we first hold the standard that `relationship reading`, `representation processing`, and `stable transfer` are bundled into one repeating unit.

## Cases and Examples

### Case. When Attention Alone Cannot Settle An Action Judgment

Consider a work-permit sentence such as `Restart is held while the pressure remains unreleased.` Self-attention is important for reading that `pressure unreleased`, `restart`, and `held` are related. But if the explanation ends here, it remains unclear how the current action expression becomes clearer as `conditional hold` rather than `simple restart`, and how that meaning is preserved into the next layer.

The standard a person may first use is `did the word restart refer to pressure unreleased and held?` This is enough to explain the role of attention. But to explain the whole Transformer, one more question remains.

After reading that relationship, in what state should the current action representation move to the next block?

Once this question remains, the attention-only explanation breaks. The fact that the `restart` token referred to the earlier condition does not explain how the current representation is processed from `an approvable action` into `a conditionally blocked action`, or how it is organized into a range that the next computation can handle without losing the original action meaning.

If we read the same sentence in two ways, the difference becomes clearer.

| Reading method | What it can explain | Where the explanation breaks |
| --- | --- | --- |
| attention-only explanation | that `restart` is related to `pressure unreleased` and `held` | what action state the current representation changes into after reading the relationship |
| Transformer block explanation | the flow that reads the relationship, processes the current position representation, keeps the original action meaning and stability, and passes it to the next block | the detailed role split and representation movement are handled together in P5-14.2 |

The result of this case settles as follows.

| Question for reading the current representation | Can attention alone answer it? | Supplement needed from the block viewpoint |
| --- | --- | --- |
| What condition is this action connected to? | yes | relationship reading handled by self-attention |
| How does that connected condition change the action representation? | not enough | feed-forward reprocesses the current position representation |
| Does the new representation move to the next computation without losing the original action meaning? | not enough | residual connection and layer normalization help stable transfer |

The result to confirm in this case is not `attention is important`. A more precise result is: `attention is central for reading relationships, but a Transformer explanation settles only when it also includes the structure in which that relationship changes the current representation and moves stably to the next block`.

## Practice and Example

### Practice. Rewrite An Attention-Only Explanation As A Block Explanation

Look at the input sentence below and first choose which of the three explanations best settles the central question of P5-14.1.

Input sentence:

`Restart is held while the pressure remains unreleased.`

| Candidate explanation | Judgment |
| --- | --- |
| A. `Restart` refers to `pressure unreleased` and `held`, so the Transformer explanation is complete. | not enough |
| B. `Restart` refers to `pressure unreleased` and `held`, and because of that relationship, the current action representation should be processed toward `conditional hold`. | middle |
| C. `Restart` refers to the relevant condition, that relationship changes the current action representation, and the result should move to the next block while keeping the original action meaning and stability. | more appropriate |

Explanation: A only says `relationship reading`, which self-attention handles. It answers `what was referred to`, but not `how the current representation changes after the reference`. B comes more similar to why a feed-forward network is needed. But in deep block repetition, the changed representation also needs stability so that it does not completely lose the original action meaning when it moves to the next computation. C is most similar to the center of this section. What P5-14.1 must settle is not `attention is important`, but `attention + position-wise processing + stable transfer must be bundled into one block for the Transformer explanation to settle`.

Now directly rewrite the short explanations below.

| Before rewriting | Example rewritten explanation | Why rewrite it this way |
| --- | --- | --- |
| The Transformer refers to needed words through self-attention. | The Transformer reads needed word relationships through self-attention, reprocesses the current representation mixed with that relationship, and passes it stably to the next block. | If it stops at `refers`, it is an attention explanation; it becomes a block explanation only when it reaches `processes the representation and passes it stably`. |
| Because `restart` referred to `pressure unreleased`, a hold judgment is possible. | After `restart` refers to `pressure unreleased`, the current action representation must move toward `conditional hold`, and that meaning must remain in the next computation. | Relationship checking alone does not explain representation change and transfer. |

Explanation: A good answer is not a sentence that memorizes many component names. If it includes `relationship reading`, `current representation processing`, and `stable transfer to the next block`, it passes the standard of P5-14.1. The detailed roles of self-attention, feed-forward, residual connection, and layer normalization are separated further in P5-14.2.

## Checklist

- Can you say what is missing if the Transformer is explained only as self-attention?
- Can you explain that self-attention's relationship reading and feed-forward's position-wise processing are both needed inside a repeated block?
- Are you ready to read the next section as a closer look at how each component divides roles?

## Sources and References

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, checked on 2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Jay Alammar, `The Illustrated Transformer`, checked on 2026-06-29. [https://jalammar.github.io/illustrated-transformer/](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }
