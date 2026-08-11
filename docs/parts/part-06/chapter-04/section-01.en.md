# P6-4.1 Transformer Computation Flow Inside an LLM

> Section ID: `P6-4.1`
> Version: `v2026.07.26`

_Subtitle: How does a Transformer carry token representations into next-candidate scores?_

We now need to bring the Transformer structure from Part 5 back into the main flow of generative language models in Part 6.

If Part 5 explained the Transformer block structure itself, Part 6 must reread the same structure inside the computation flow of a generative language model. The core is that `token -> embedding -> attention block -> next-token score` connects as one generation flow.

When we reread the Transformer from the LLM view, what is truly central? In an LLM, the Transformer is the basic structure that turns tokens into embeddings, reads their relationships through self-attention, refines representations through feed-forward and repeated blocks, and finally predicts the next token.

## What the Transformer Does in Generation Computation

When rereading the generation computation engine, the core questions are these three.

- What changes when we reread the Transformer we already saw from the LLM view?
- How do tokens, embeddings, self-attention, and next-token prediction connect?
- Why did the Transformer become the basic structure of generative language models?

Once we hold the large structure of Transformer blocks, supplementary topics such as multi-head attention and positional representations, KV cache, sparse attention, and long context can also be placed on the same flow. Latency and cost constraints from the service-operation view also eventually connect to how much, how long, and how quickly this computation flow is repeated.

What matters more than unfolding Transformer formulas again is the `LLM-oriented structure map` that supports all later explanations of GPT, pretraining, next-token prediction, RAG, and agents in Part 6. The standard more important than detailed block names is `through what computation flow input tokens lead to next-token scores`.

| What we are reading now | Question that broadens later |
| --- | --- |
| Whether tokens, embeddings, attention blocks, and next-token scores form one flow | How far the context window can hold input |
| That the Transformer is the basic computation engine of LLMs | What GPT-family branching, pretraining, and operating-cost constraints each change |

This section's role in the main request flow of Part 6 is to show through what computation engine input tokens pass before becoming next-candidate scores. This flow must be fixed so P6-5.1's GPT family, P6-7.1's next-token prediction, and later explanations of context windows, prompts, and RAG can be read on the same structure.

The result to check here is whether you can read the Transformer not as `a device that guesses the next token once`, but as the central engine that reflects the whole context and updates the next-candidate distribution. This distinction lets the deep-learning structure explanation of Part 5 connect naturally to the generative-model structure of Part 6.

## Why Reread the Same Transformer?

In Part 5, we explained the Transformer as a deep learning structure. In other words, the focus was on block elements such as:

- self-attention
- feed-forward
- residual connection
- layer normalization

In Part 6, we look at the same structure, but the questions change.

- How does this structure read text?
- Why does this structure fit next-token prediction well?
- Why did this structure become the basic computation unit of LLM services?

In other words, the structure is the same, but `the reading view` changes.

Reading P5-14 does not automatically make P6-4.1 clear. P5-14 is the section that closes `what is inside a Transformer block`, while P6-4.1 must newly connect how that block `receives an LLM request and closes as next-token candidate scores`.

So when moving directly from Part 5, first fill the following blanks.

| What was already established in P5-14 | What P6-4.1 must newly connect | Why simply moving on is insufficient |
| --- | --- | --- |
| Self-attention reads relationships among tokens | How the current generation position pulls clues from the preceding context to change next candidates | Because relationship reading itself has not yet been connected to generation-candidate change |
| Feed-forward and repeated blocks process representations | The final-position representation after several layers becomes a next-token score table | Because saying the representation became better does not show the actual output form |
| Residual connection and layer normalization stably connect blocks | Even in a long generation flow, the same block computation is repeated to keep updating the candidate distribution | Because block stabilization and the generation loop are different levels |
| Transformer is better than RNN for parallel computation and long-context reference | In LLMs, that strength becomes the foundation for prompt, context window, GPT, and RAG explanations | Because the strength of the computation structure and the service/generation questions of Part 6 have not yet been connected |

The result to check in this table is not `can you explain P5-14 again`. Use the block explanation of P5-14 as a stepping stone, but now you must be able to explain `how representations reflecting context become a next-token candidate distribution`. Without this bridge, the cases and examples in P6-4.1 read as if they suddenly jump to a `next-token score table`.

## LLM Tokens as Starting Point

An LLM does not compute a sentence whole. It first reads it as a token sequence.

For example, you can think of it like this.

```text
raw text
-> tokens
-> token ids
-> embeddings
-> Transformer blocks
-> next-token scores
```

Here, the Transformer is the computation structure after tokens have already been split. In other words, the Transformer is not the first stage that directly interprets text, but is closer to `the central engine that repeatedly processes token representations`.

## Embeddings Make Computable Starting Representations

As we saw in P6-2, token IDs are only numbers. The Transformer does not directly handle these numbers. It first turns them into embedding vectors.

These embedding vectors become the starting point for all later computation.

You can understand it as follows.

`An embedding is the step that turns a token into numerical coordinates the Transformer can compute with.`

In other words, the Transformer does not read text as strings. It operates on embedded token representations.

## Why Was Self-Attention Especially Important for LLMs?

A generative language model must predict the next token at the current position. At that point, all previous tokens that have appeared so far can become clues.

For example, information such as:

- the subject that appeared earlier
- a function name in a code block
- a key condition near the beginning of a document

can affect later generation.

Self-attention lets each token compute relevance with other tokens. So the current token representation can reflect information from both nearby and distant previous tokens.

`In an LLM, self-attention is the structure that computes which tokens that have appeared so far matter more for the current generation.`

## Why Are Feed-Forward and Repeated Blocks Needed?

Self-attention can mix relationships among tokens, but that information does not immediately become a good enough representation.

The feed-forward network processes the representation again at each position. As this block repeats through several layers, the representation can become richer.

In other words:

- attention reads relationships
- feed-forward refines each position representation again
- repeated layers gradually refine representations further

This flow connects directly to the representation learning explanation in Part 5.

## Why Do Next-Token Scores Come Out at the End?

The important difference in LLM explanations is the interpretation of the final output.

Classification models often output class scores at the end. But generative language models usually output scores for `token candidates that can come next`.

In other words, after passing through Transformer blocks, the final question is roughly this.

- Which token is likely to come at the next position?

These scores then lead to actual output-token selection through procedures such as softmax and sampling.

So the structure explanation from Part 5 is reread in Part 6 as follows.

> Representation learning structure
> -> next-token distribution computation structure

If we compress this difference again with one small input, it becomes the following.

| Input fragment | First reading in P5-14 style | What P6-4.1 must additionally see |
| --- | --- | --- |
| `The client meeting today will proceed at 2 p.m.` | Token representations are updated through self-attention and feed-forward | The final-position representation leads to score differences among next candidates such as `as planned`, `today`, and `tomorrow` |
| `This is an internal team memo. Today's meeting will proceed at 2 p.m.` | The same Transformer block computes token relationships again | Because the preceding context gives tone clues, the candidate score table shifts toward conversational expressions rather than announcement style |

So the goal is not memorizing Transformer part names again. It is holding onto the fact that the same parts form the generation flow `context reflection -> representation update -> next-candidate score` inside an LLM.

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-04/p6-c04-s01-transformer-flow-en.mmd"
```

This diagram is the minimum structure you should most often recall when reading the Transformer in Part 6.

## Cases and Examples

The diagram below groups the three cases in this section again under the shared question `how does the whole preceding context change the next-candidate distribution`, rather than `choosing just one next token`.

```mermaid
--8<-- "assets/part-06/chapter-04/p6-c04-s01-use-cases-en.mmd"
```

What you should check in this diagram is that even if tasks differ, the final stage is similar. In all cases, rather than `picking one next token`, first see `what candidate distribution is now made by reflecting the whole context that came in earlier`.

### Case 1. Sentence Autocomplete

Imagine an operator writing a messenger draft and entering only `Today's meeting is at`. It is easy to look only after the last word and try to guess the next phrase, such as `2` or `3`. But actual autocomplete is not a problem of seeing only the last word. The Transformer computes the next-candidate distribution from previous tokens and chooses the next expression while reflecting earlier clues such as `meeting` and `afternoon`.
For example, even for the same sentence, if `with the client` appears earlier, a polite announcement-style expression can become more natural, while if `internal team` appears earlier, a short collaboration-style expression can come up more naturally. The changed point here is moving from the standard of `do we guess after the last word` to the standard of `how does the whole preceding context change the next candidates`.

Even the same ending, `Today's meeting is at`, has different next candidates if the preceding context differs.

| Preceding context | What is easy to recall from only the last word | Candidate that can become more natural in practice |
| --- | --- | --- |
| `with the client` | Time candidates such as simply `2` or `3` | Announcement-style expression such as `2 p.m. as scheduled` |
| `internal team` | It is easy to see it as enough to match the time number | Short collaboration-style expression such as `2, let's meet then` |
| `This is a notice email` | It feels as if filling only the time is enough | Time plus guide-sentence structure is decided together |

The misunderstanding this table corrects is the expectation that `if the last word is the same, the next candidate is almost the same`. The autocomplete case breaks exactly this misunderstanding and most easily shows that the Transformer is a structure that sees the whole preceding context.

### Case 2. Code Generation

When a function definition and variable declarations appear earlier and implementation continues later, looking only at the immediately preceding line makes it easy to miss variable names. If `user_id` was declared earlier but generation later drifts to `userId` or `account_id`, the syntax may look right, but implementation consistency breaks. If the function name is `calculate_total` but the discount step or tax-application order is missing, the purpose set earlier and the later implementation diverge.

Even in the same code generation, the point that shakes differs depending on how much preceding context is held.

| What was already opened in the preceding context | Problem likely when only the immediately preceding line is seen | What is better maintained when preceding context continues to be seen |
| --- | --- | --- |
| Variable declarations such as `user_id` | Drifting to a similar different name | Variable-name consistency |
| Function purpose such as `calculate_total` | Missing discount/tax steps | Maintaining implementation purpose and processing order |
| Conditional/repeated block structure | Indentation and return position diverge | Consistency of block structure and return flow |

The result to check in this case is not `does it match near the current line`, but `are the names and purpose declared earlier still reflected in the next candidates of the later implementation`. The Transformer structure matters in code generation because it changes the next-candidate distribution based not only on the immediate context, but also on already opened names, purposes, and block structures.

### Case 3. Long-Document Summarization

Even when summarizing a long document, the next sentence candidate is not decided only by one visible conclusion line. A definition in the early part can limit the scope of a later conclusion, or an exception condition near the end can narrow an earlier general explanation. For example, if a conclusion sentence is short but the scope where that conclusion holds is tied to an earlier paragraph, the next candidate for the summary sentence should also reflect that scope to be natural.

The result to check in this case is not `do we hold only one visible front or back part`, but `are the earlier conditions and later exceptions reflected together in the next summary candidate`. How long the whole long document can be maintained will be handled more directly in P6-4.2 and P6-4.5. Here, it is enough to hold onto the fact that the Transformer connects context clues to the next-candidate distribution.

If we group the three cases again from the context-reflection view, it becomes the following.

| Situation | What is easy to miss if only the immediately preceding part is seen | What is better maintained when the whole preceding context is reflected |
| --- | --- | --- |
| Sentence autocomplete | Choosing only candidates after the last word | Tone and follow-up expressions that fit the preceding context |
| Code generation | Choosing only tokens near the current line | Consistency of declared variable names and function purpose |
| Long-document summarization | Choosing only one visible conclusion line | Next summary candidates that reflect earlier conditions and later exceptions |

## Standards Revisited in Failure Scenes

A common mistake when rereading the Transformer in application scenes is reading it only as `a collection of difficult internal structure names` and missing when this view should be brought back in an actual scene. In that case, rather than memorizing formulas or block names again, it is safer to first separate whether the current problem is about `choosing next candidates by reflecting the whole preceding context`.

| Scene that first appears now | First question to ask | Axis to revisit first |
| --- | --- | --- |
| Autocomplete looks as if it mechanically attaches only a number after the last word | `Is the whole preceding context actually changing tone and the next-candidate distribution?` | Transformer's context-reflection structure |
| Code generation looks natural on the immediately preceding line, but variable names and function purpose keep drifting | `Are names and purposes opened earlier continuously reflected in the later implementation?` | Transformer's long-distance context connection |
| Long-document summarization keeps only one conclusion line and misses conditions or exceptions | `Is it reflecting front and back clues together, rather than one visible part?` | Transformer's context-integration structure |

The purpose of this table is not redefining the Transformer. It is to make you branch first, when seeing an actual failure scene, whether it is a problem where `attaching only the immediately preceding piece` is enough, or a problem that must be reread as `a structure that reflects the whole preceding context`.

## Practice and Examples

The goal of this practice is not implementing the whole Transformer. It is to confirm the flow organized above, `context reflection -> representation update -> next-candidate score`, with a small score table and graph. We will read how sentences sharing the same ending change into different candidate distributions depending on preceding context clues.

The core to check is reading next-token prediction as `a process where candidate scores and probability distributions change depending on which clues were activated in context`. The values below are not internal probabilities of an actual LLM. They are simplified examples for explaining how score differences appear as candidate distributions.

The diagram below first compresses the flow this example checks. Even when the same ending exists, preceding context clues change representations inside Transformer blocks, and that difference leads to candidate score tables and gaps between candidates.

```mermaid
--8<-- "assets/part-06/chapter-04/p6-c04-s01-scoring-flow-en.mmd"
```

The inputs in the table below are four context conditions. All four conditions share the same ending, `Today's meeting will proceed at 2 p.m.`, but the context clue attached earlier differs. The `Context change` column shows which clue entered, and `Rank-1 candidate` and `Rank-2 candidate` show the ranking of expression candidates that can come next under that condition. `Rank-1 probability` and `Rank 1-2 gap` are values for reading how stable rank 1 is.

Even when the same ending is shared, if the clue read from preceding context differs, the candidate score table changes.

| Context change | Rank-1 candidate | Rank-1 probability | Rank-2 candidate | Rank 1-2 gap | Point to read |
| --- | --- | ---: | --- | ---: | --- |
| Client notice email | `as scheduled` | 0.733 | `was completed` | 1.24 | Announcement-tone clues strongly raise a polite ending |
| Notice feeling weakens | `as scheduled` | 0.619 | `was completed` | 0.84 | Rank 1 is the same, but confidence is lower |
| Internal team memo | `today` | 0.684 | `was completed` | 1.38 | Internal memo clues raise a shorter expression |
| Internal team memo with polite tone mixed in | `as scheduled` | 0.372 | `today` | 0.09 | Rank 1 changes, but the gap is small, so the choice looks unstable |

![Candidate distribution by context clue change](/AiBook/assets/part-06/chapter-04/context-candidate-distribution-en.png)

When reading the table, first look at the `Context change` column, then what the rank-1 candidate is, and finally whether the gap between rank 1 and 2 is large or small. For example, in `Client notice email`, rank 1 is `as scheduled`, and the gap is also large. Conversely, in `Internal team memo with polite tone mixed in`, rank 1 changes to `as scheduled`, but the gap is small at 0.09. This is the point where even the same rank 1 looks different as a stable choice or a shaky choice.

In the graph as well, the point to see is less the height of the bars itself and more the relative distance between candidates. In `Internal team memo with polite tone mixed in`, `as scheduled` is rank 1, but the gap from other candidates is small. It is better to read this state not as the next-token choice having solidified stably into one option, but as context clues pulling the candidate distribution in different directions.

Seen this way, what matters is not `memorizing one correct token`, but `which context clues raise or lower which candidate distribution`.

The core to check in this example is as follows.

- Even with the same candidate set, the score table changes if clues read from preceding context differ.
- The Transformer's final computation is closer to `a score distribution over next candidates` than to the completed sentence itself.
- The actual output token is selected by choosing the highest candidate in that score table or through rules such as sampling.
- In other words, it is more accurate to view generation as `continuously updating the candidate distribution by reflecting context` than as `directly guessing one word`.

## Candidates That Diverge in Next-Token Selection

The previous exercise is a scene that shows in a more practical score-table form that long-context computation ultimately closes as `candidate score comparison` and `next-token selection`. The core to read here is not memorizing all complex internal blocks. It is that the computation eventually makes `a next-token distribution that changes depending on preceding context`. In other words, when reading the Transformer, it is more accurate to look at `how the whole context changes the next-candidate distribution` than at `directly guessing one correct word`.

## Why Did It Become the Central Engine of LLMs?

The Transformer became the central structure of language models not simply because its performance was good.

- It could handle longer contexts better
- It fit parallel processing well
- The same basic structure could be widely reused for many language tasks such as translation, summarization, question answering, and code generation

## Checklist
- Can you explain the Transformer as `an engine that reflects the whole context and updates the next-candidate distribution`?
- Can you distinguish where the structure explanation of Part 5 and the generation explanation of Part 6 diverge?
- Can you continue into the question that Transformer computation also works within input-range constraints?

## Sources and References

- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper_files/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }, NeurIPS 2017, accessed 2026-07-19. Used as basic evidence for self-attention, multi-head attention, positional encoding, and feed-forward blocks in the Transformer for explaining LLM structure.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI 2019, accessed 2026-07-19. Used as background evidence that GPT-2 is a Transformer-based language model that performs multiple language tasks.
- OpenAI, [openai/gpt-2](https://github.com/openai/gpt-2){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as supporting evidence to confirm that the GPT-2 code and model are the public implementation of the paper, and that evaluation is needed when using the model.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv 2020, accessed 2026-07-19. Used as background evidence that GPT-3 is an autoregressive language model and that LLMs perform multiple tasks through few-shot text interaction based on next-token prediction.
- Jay Alammar, [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as supplementary educational material when re-explaining the Transformer computation flow in introductory diagram language.
