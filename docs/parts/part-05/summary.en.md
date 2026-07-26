# Part 5 Wrap-up. Deep Learning Review

> Section ID: `P5-summary`
> Version: `v2026.07.26`

Part 5 was the section that actually explained how the larger family of functions called neural networks was built on top of the common questions of machine learning. If Part 4 established the standard for reading models around data splitting, generalization, and evaluation, Part 5 had to recover `the structure that learns deeper representations` and `the procedure that actually trains that structure`, while keeping that same standard.

The core of this Part is not to memorize deep learning merely as `a model with many layers`, but to read it as a repeated structure in which inputs are transformed into progressively different representations through weights and activation functions, and those representations are adjusted through loss and backpropagation.

In other words, Part 5 was the first main-text Part that had to actually explain the perceptron, representation learning, loss functions, backpropagation, optimizers, CNNs, and Transformers that Part 1 through Part 4 had left behind with `this will be explained later`.

That core can be regrouped into the following three lines.

| The reading order to leave behind first | Why this order matters |
| --- | --- |
| Look at the structure first | You need to know what kind of input-structure problem it is solving so that model names become less confusing. |
| Move from loss to gradients | The loss number must become a correction signal for each parameter before learning becomes visible. |
| Look at optimizers and regularization last | This lets you separate whether the performance gap came from structure or learning stabilization. |

At this point, an important principle is not to end Part 5 as a `preview for the next Part`. CNNs, RNNs, Attention, and Transformers all connect to the later explanation of LLMs, but that connection must follow the order `close the current structure first, then expand it into a different problem in the next Part`, not `we will look at it later`.

When reviewing, it is more stable not to stop after rereading this summary alone, but to go back at the point where a term becomes blurry and read the corresponding entry in the [Concept Glossary](/AiBook/en/reference/concept-glossary/) together with its `Core Section`.

## Review Flow That Regroups Part 5

This document holds its flow best if read in the following order.

1. First, recover what large flow structured all of Part 5.
2. Next, organize together the concepts that must be remembered and the points that are easy to misunderstand.
3. Then, check what questions Part 5 intentionally did not close.
4. Finally, connect how those questions reopen in the next Part.

## Core Flow Covered in This Part

The flow of Part 5 can be organized as follows.

1. It begins with perceptrons and multilayer neural networks.
2. It connects activation functions, output layers, and loss.
3. It examines backpropagation and automatic differentiation, which move from loss to gradients.
4. It distinguishes learning from model execution.
5. It examines optimizers, regularization, and dropout.
6. It examines GPU, batch, and tensor computation.
7. It reads representation learning as the entrance to structural branching.
8. It examines CNNs, RNNs, LSTMs, and GRUs.
9. It examines Attention and self-attention.
10. It examines Transformers.
11. It examines generative models and sampling.
12. It organizes the structure that leads into the next Part on LLMs and generative AI.

If this flow is reduced into one sentence, it becomes the following.

`Deep learning is not a technique for memorizing one large function, but a learning system that progressively turns data into more appropriate representations and sends the error of that process backward again for adjustment.`

In Part 5, this structure immediately connects to the following questions.

| Structural intuition fixed in Part 5 | The question reread in the next Part |
| --- | --- |
| Inputs are turned into representations | Into what token units is a sentence split? |
| Loss is turned into gradients for adjustment | Why does next-token prediction lead into a learnable generation problem? |
| Attention and Transformers handle context | Why did long context and generative services become possible? |
| Generation and sampling change the result | Why must response quality and service quality be examined together? |

If this entire flow is regrouped again as briefly as possible like a review map, it becomes the following.

```mermaid
--8<-- "assets/part-05/part5-recap-flow-en.mmd"
```

In other words, to say you have finished Part 5 means that `the structure that changes representations`, `the procedure that adjusts error`, `branching by data structure`, and `selection of generated output` are connected in one line.

Under the current table-of-contents structure, this flow is more naturally reread as `basic computational structure of neural networks -> outputs and loss signals -> training loops and stabilization -> computational scaling -> representation learning and structural branching -> generative models and sampling`.

At this point, it is also helpful to regroup the latter half once more, more slowly. Chapters 12 through 15 begin from `how can sequential state be carried forward`, then move to `can the needed positions be revisited now`, then to `why is that reference computation repeated as parallel blocks`, and finally to `how do we choose an actual output among the resulting candidates`. Only with that handle in place can `RNN -> attention -> Transformer -> generation` be read not as a quick swap of model names, but as a staged change in structural thinking.

If only the latter-half transition is compressed again, it becomes the following.

| Latter-half structural flow | The key question to hold onto |
| --- | --- |
| Sequential state | Can earlier state be carried stably into the current judgment? |
| Direct reference | Can the needed earlier position be revisited now? |
| Parallel blocks | Why must this reference computation be bundled into a repeatable block structure? |
| Generation-candidate selection | By what standard is the actual output chosen from the computed distribution? |

In this wrap-up, an especially important point is not to finish Part 5 as `the Part where many structure names appeared`, but to regroup it again as one flow from `representation learning -> structural branching -> the basis of generation`. Only then can you explain, not merely that `you already know Transformers`, but `why this structure became the basis of generative language models`.

If the latter-half structural chapters are regrouped once more in the shortest possible form, they become the following.

| Structural chapter | The problem to read before the name |
| --- | --- |
| CNN | Why do local patterns become important first in images? |
| RNN / LSTM / GRU | Why do order and accumulated state change the current judgment? |
| Attention / self-attention | Why must distant clues be referenced again now? |
| Transformer | Why did relationship computation need to be bundled into parallel blocks? |
| Generation / sampling | Why must actual output candidates be selected separately after the distribution is produced? |

## Concepts That Must Be Remembered

The concepts that should remain the longest after Part 5 are the following.

| Distinction | Perspective to remember |
| --- | --- |
| Perceptron | It is the smallest starting point that places a decision structure on top of a linear combination of inputs and weights. |
| Hidden layer | The intermediate layer is not merely a computation step, but the place where inputs are turned into different representations. |
| Activation function | Without nonlinearity, stacking deeper layers still gives limited growth in expressiveness. |
| Output layer and loss | Output interpretation and the loss function must be chosen together to match the problem type. |
| Backpropagation and automatic differentiation | Backpropagation is the procedure that calculates gradients backward from loss, and automatic differentiation is the technique that automatically organizes that computation from the forward-pass record. |
| Optimizer | Even if the direction is always to reduce loss, the actual update rule can differ. |
| Regularization | Good learning is not merely fitting longer, but making the model less likely to collapse on unseen data. |
| GPU and batches | The spread of deep learning happened not only with good ideas, but together with a parallel computation environment. |
| Representation learning | The key shift of deep learning is that the model learns features directly instead of humans writing them. |
| CNN / RNN / Attention | Favorable model designs changed depending on data type and dependency structure. |
| Transformer | Self-attention and parallel structure became the basis of the LLM era. |
| Generation and sampling | Generative AI creates the output itself, and the actual result is affected by sampling strategy. |

These concepts also become less confusing if they are regrouped again into two axes.

| Axis to separate first | What goes here | Why it must be read separately |
| --- | --- | --- |
| Structure | Perceptrons, hidden layers, CNNs, RNNs, Attention, Transformers, generative structures | This explains what form the input is turned into and what dependencies are handled. |
| Learning procedure | Loss, gradient computation, backpropagation, automatic differentiation, optimizers, regularization, dropout, batches | This shows that even with the same structure, learning stability, generalization, and computation cost can differ. |

In other words, in Part 5 it is important to build the habit of reading `what structure was used` separately from `how that structure was trained`.

## Points That Are Easy to Misunderstand

The misunderstandings that especially require caution in Part 5 are the following.

- Deep learning is not `something completely different from machine learning`, but a branch of machine learning extended into a larger representation-learning structure.
- Simply having more layers does not automatically make a model better.
- You cannot conclude that actual quality improved immediately just because the loss went down.
- Backpropagation is not the name of the whole learning process, but the procedure for computing gradients; automatic differentiation automates that procedure through the code execution record.
- GPUs are not merely speed-up devices, but a computational environment that changed the direction of deep learning research itself.
- The appearance of Attention does not mean RNN-family models became entirely meaningless. It means the mainstream structure for large language models changed.
- Understanding Transformers does not mean you understand the entirety of LLMs. In the next Part, you still have to examine tokens, pretraining, alignment, and tool connection together.
- If a generated result looks strange, it is not enough to interpret that only as `the model does not know`. Sampling method, context length, and input structure must also be examined.
- If Part 5 merely introduces structural names and moves on, the next Part's explanation of LLMs can weaken again into surface-level term introduction.

## Questions This Part Does Not Close

Part 5 focused on explaining the structures and learning procedures of deep learning. Therefore, the following questions are intentionally passed to the next Part.

- Into what token units is an input sentence actually split in a real service?
- Why does the Transformer lead into user experiences such as long conversation, summarization, and code generation?
- How are the quality and grounding of generated results supplemented at the service level?

In other words, Part 5 is the Part that closes `the structural foundation`, not the Part that finishes the whole service experience of LLMs here.

In other words, the final question of Part 5 does not stop at `what structures exist`, but must move to `how those structures lead into the actual experience of generative AI services`.

If this transition is reduced as briefly as possible, it becomes the following.

- Part 5 explains `why these computational structures are needed`.
- The next Part explains `why those structures lead into the actual understanding and use of generative AI`.

## Questions to Check Before Moving to the Next Part

Before moving to Part 6, you should be able to answer the following questions.

- Can you explain the relationship among perceptrons, multilayer neural networks, and hidden layers?
- Can you explain why activation functions are needed?
- Can you explain that output layers and loss functions connect to problem type?
- Can you explain how loss becomes parameter-wise gradient signals, and what roles backpropagation and automatic differentiation each play?
- Can you explain how optimizers and learning rate affect learning stability?
- Can you explain how regularization and dropout relate to overfitting?
- Can you explain why GPU, batch, and tensor computation are connected to the spread of deep learning?
- Can you explain what kinds of data structure or problems brought forth CNNs, RNNs, Attention, and Transformers?
- Can you explain the difference between generative models and classification models?
- Can you explain that sampling affects quality and diversity in generation?

## Closing Part 5

Once you pass through Part 5, you should no longer see deep learning only as `a complicated black box with many weights`. The large flow should begin to appear in which inputs turn into representations, loss is computed, error is sent back again, parallel computation resources support the whole process, and Attention and Transformers open the problems of long context and generation.

Only when that flow is in place can you explain in the next Part not merely that LLMs are famous product names or API targets, but on what input units and computational structures they operate.

That was exactly the purpose of Part 5.

One final point must be fixed again here: to say you have finished Part 5 does not mean `you have seen many deep-learning terms`, but `you can say what computational answer appeared for what structural problem`.

| What should remain when Part 5 is finished | What is still passed to the next Part |
| --- | --- |
| You can explain why the structures branch from perceptrons to Transformers | Tokenization, pretraining, retrieval integration, tool connection, operational details |
| You can explain loss, gradient computation, backpropagation, automatic differentiation, optimizers, and regularization separately from structure | Service settings, inference cost, long-context operational optimization |
| You can explain generative models and sampling as `distribution learning` and `output selection` | LLM product experience and service-design judgment |

## Checklist

- After Part 5, have you developed the habit of reading `structure` and `learning procedure` separately?
- Can you explain Transformers not just as a famous structure, but as `a structure that bundles relationship computation into parallel blocks`?
- Can you explain generation and sampling not as `topics that newly appear in the next Part`, but as `topics whose structural starting point is already closed here`?

## Sources and References

This document is an internal summary of all of Part 5. It does not directly cite external sources.
