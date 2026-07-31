# Part 5. Deep Learning

> Section ID: `P5-index`
> Version: `v2026.07.31`

The first plan for this opening page is to read `representation transformation`, `loss`, `gradient`, `training stabilization`, `structure branching`, and `generation connection` in order. For each structure, first check which data-structure problem it answers rather than its name, and keep the connection to Part 6 brief where it is needed.

Part 5 is the Part that explains neural networks and deep learning in earnest. In Part 1, Part 2, and Part 4, topics such as perceptrons, representation learning, backpropagation, optimizers, convolutional neural networks (CNNs), recurrent neural networks (RNNs), Attention, and Transformers were previewed several times, but their role there was to sketch the terrain and restore the foundations. Part 5 no longer postpones those explanations. From here on, it must actually recover `why these structures are needed`, `how they are trained`, and `what differences cause model structures to branch`.

The core purpose of this Part is to make deep learning explainable not as the name of a black box, but as a computational structure and a learning structure. Many readers have already heard names such as neural networks, CNNs, and Transformers many times, yet still cannot describe in one flow `how inputs become representations`, `how error is sent back`, `why GPUs and batches matter`, and `why Attention became a structural turning point`.

So Part 5 recovers the real explanation along the following six axes.

1. Basic computational structure of neural networks
2. Outputs and loss signals
3. Training loops and stabilization
4. Computational scaling
5. Representation learning and structural branching
6. Generative models and sampling

If this order is compressed at once like a learning map, it becomes the following.

```mermaid
--8<-- "assets/part-05/part5-learning-map-en.mmd"
```

In other words, Part 5 is the Part that gradually moves its handle from `basic computational structure -> outputs and loss -> training loops -> computational scaling -> structural branching -> generation`.

In other words, Part 5 is the first Part that actually explains the core deep learning concepts that Part 1 through Part 4 left behind with the phrase `this will be explained later`. If the explanation here is weak, the LLM and generative AI material in the next Part will also collapse back into surface-level term introduction.

Part 5 must not be read as a `deep learning trailer`. Therefore, the default principle is that CNNs, RNNs, Attention, and Transformers each settle `why this design appeared for this kind of data-structure problem` inside this Part first, while the bridge to Part 6 remains only as a short pointer to the next layer.

If the baseline for a core term becomes blurry again while reading this Part, the default reference point is to review through the [Concept Glossary](/AiBook/en/reference/concept-glossary/) by checking each entry's `Core Section` and `Appears In` list together.

If this standard is reassembled into one line for the current Part 5 table of contents, it becomes the following.

| What is settled first in Part 5 | What is passed to Part 6 |
| --- | --- |
| The basic structure and role of perceptrons, loss, backpropagation, optimizers, regularization, CNNs, RNNs, Attention, Transformers, generation, and sampling | Tokenization, pretraining, instruction tuning, retrieval-augmented generation (RAG), tool use, agents, service operations |

This Part also prepares the interpretation targets that will reappear in Part 6 and later Parts.

- Representation learning later leads to how tokens, context windows, and embeddings are interpreted.
- Generation and sampling later lead to comparing generated results and making decoding judgments.
- Attention and Transformers later lead to retrieval integration, evidence selection, and interpretation of evaluation structure.
- Learning procedures and stabilization later lead to quality judgment, failure analysis, and the reading of operational evaluation.

At the same time, it is important not to rush through this connection in a single sentence too early. The latter half of Part 5 is not the section for memorizing the order `RNN, then attention, then Transformer`. It is the section where the handle changes from `a structure that passes sequential state`, to `a structure that looks back at needed positions`, to `a structure that bundles those reference computations into repeatable parallel blocks`, and then to `the problem of selecting an actual output among the resulting candidates`. This slow sense of transition must be in place for the latter half to remain a flow of structural change rather than a list of model names.

If only the latter-half transition is fixed again in the shortest possible form, it becomes the following.

| The handle that changes first in the latter half | The question to hold onto at this stage |
| --- | --- |
| Sequential state | How is previous state carried into the current decision? |
| Direct reference | Can the necessary earlier position be revisited right now? |
| Parallel blocks | Why bundle this reference computation into a repeatable block structure? |
| Generation-candidate selection | How is the actual output chosen from the computed distribution? |

## Purpose of This Part

This Part is the section for understanding deep learning again across three levels: `representation-learning structures`, `training procedures`, and `model-structure branching`.

Earlier Parts repeatedly previewed that representation learning, backpropagation and optimizers, and CNN/RNN/Transformer structures would be revisited later.

Part 5 is responsible for keeping that promise. So this Part must not stop at something like `neural networks are also an important technology`; at minimum, it must provide real explanation for the following questions.

- What is different between a single perceptron and a multilayer neural network?
- Why does depth lose its meaning if there is no activation function?
- What do loss and backpropagation compute?
- What is different between SGD and Adam?
- What are regularization and dropout trying to prevent?
- What kinds of data-structure problems are CNNs, RNNs, Attention, and Transformers trying to solve?
- Why do generative models and sampling lead into the next Part on generative AI?

### Current Reading Principles

Part 5 is most stable when it is read by the following principles.

| Principle | Meaning |
| --- | --- |
| Settle the structure first | Each chapter should finish `what the problem was and what computational structure answered it` inside the current chapter. |
| Separate the learning procedure | Loss, gradients, optimizers, and regularization are read on the learning-procedure axis rather than mixed into structure names. |
| Keep the Part 6 bridge short | Explain `why the next Part is needed`, but do not postpone the current chapter's key explanation. |

Here it is important not to mix the following two axes.

| Axis being read now | Representative question | Representative items in this Part |
| --- | --- | --- |
| Structural problem | How should this input structure be represented? | Perceptrons, CNNs, RNNs, Attention, Transformers, generative structures |
| Learning-procedure problem | How can that structure be trained stably? | Loss, gradient computation, backpropagation, automatic differentiation, optimizers, regularization, dropout, batches |

In the early part of Part 5, the following connection standard is fixed first.

| Structural axis read first | The question attached immediately after it | The learning-procedure axis passed to next |
| --- | --- | --- |
| Perceptrons and multilayer structure | How do inputs turn into intermediate representations? | How do loss, backpropagation, and optimizers correct that structure? |
| Activation functions | Why does depth become meaningful representational expansion rather than simple repeated linearity? | Learning stabilization, initialization, and regularization |
| CNN / RNN / Attention / Transformer | What data-structure problem caused the design to branch? | The procedure that actually trains each structure stably |

Only when this distinction is in place can you separately read whether `performance improved because CNN was better` or `performance improved because the optimizer change stabilized learning`.

This distinction can first be fixed in the following three lines.

| The minimum order for reading deep learning | Why this order comes first |
| --- | --- |
| Look at the structure first | You need to know what input-structure problem it is trying to solve before model names become less confusing. |
| Move from loss to gradients | Learning can actually continue only when a loss number becomes a correction signal for each parameter. |
| Look at optimizers and regularization last | This lets you separate whether the performance difference came from structure or learning stabilization. |

## What This Part Explains and Does Not Explain

Part 5 is the Part that actually performs the main explanation of deep learning. Therefore, the following content is explained within the main text.

- The connection among perceptrons, multilayer structures, activation functions, output layers, loss, gradient computation, backpropagation, and automatic differentiation
- Learning procedures and stabilization such as optimizers, regularization, dropout, and training/eval mode
- Why GPUs, batches, and tensor computation should be read together with the spread of deep learning
- Why representation learning becomes the entrance to structural branches such as CNNs, RNNs, Attention, and Transformers
- The structural position of CNNs, RNNs, LSTMs, GRUs, Attention, Transformers, generation, and sampling

Part 5 is responsible for connecting and explaining `why these structures and procedures are needed`. Therefore, this Part opening page first shows the main recovery axes of `structure`, `loss and gradients`, `learning stabilization`, `computational scaling`, `representation learning and structural branching`, and `generation and sampling`. Each chapter then settles the structural explanation and the learning-procedure explanation again at the Section level.

## Goals of This Part

After reading Part 5, the goal is to reach roughly the following level of understanding.

- You can explain the relationship among perceptrons, multilayer neural networks, and hidden layers.
- You can connect and explain the roles of activation functions, output layers, and loss functions.
- You can explain how backpropagation and automatic differentiation turn loss into parameter-wise gradient signals.
- You can describe the difference between learning and model execution by separating the computation stage from the update stage.
- You can explain why optimizers such as SGD and Adam have different update behavior.
- You can explain the relationship among regularization, dropout, and generalization.
- You can describe why GPU, batch, and tensor computation are directly connected to the spread of deep learning.
- You can explain what kind of input-structure and dependency problems led to the appearance of CNNs, RNNs, LSTMs, GRUs, Attention, and Transformers.
- You can explain the basic intuition of generative models and sampling.

From the viewpoint of preparing for the rest of Part 5, these goals can be read again through the following questions.

| Structure to understand in Part 5 | The question reread in the next Part |
| --- | --- |
| Representation learning | Why is the input read again as tokens and embedding representations? |
| Generation and sampling | Why do next-token prediction and decoding become important? |
| Attention and Transformers | Why do they become the basis of long context and generative services? |
| Learning stabilization and generalization | Why must evaluation and operational judgment be carried separately? |

## What Earlier Previews This Part Must Actually Recover

Part 5 must actually fill in the explanations that earlier Parts postponed. In particular, the following items must have real main-text explanation here, not merely `their names mentioned again`.

| Topic postponed in earlier Parts | What this Part must actually explain |
| --- | --- |
| Representation learning | The difference between humans writing features and models learning representations directly |
| Loss functions and optimization | Why loss is needed, and how gradients and optimizers connect |
| Backpropagation and automatic differentiation | The process by which gradients starting from loss are organized into parameter-wise signals by following the computation record |
| CNNs, RNNs, and Transformers | Why model design branches according to data structure and dependency structure |
| GPUs and parallel processing | Why the spread of deep learning cannot be separated from computational resources |
| Generation and sampling | The difference between classification-style outputs and generative outputs, and the starting point that leads into the next Part |

If this standard is missing, Part 5 weakens back into a `list of deep learning keywords`.

## Reading Standards for Entry-Level Readers

This Part is the first section where explanations of computational structure become dense. Rather than trying to hold every formula and implementation detail at once, it is more stable to read it first by the following three questions.

| Question to hold onto first | Why this question is needed | What is enough to hold in this Part |
| --- | --- | --- |
| Is what is being explained now `a structure that changes representations`, or `a procedure that adjusts learning`? | Hidden layers, activation functions, and CNNs are structures, while loss, gradients, and optimizers are learning procedures. | Read structures and learning procedures as separate things. |
| What is this model designed to `connect or remember`? | CNNs, RNNs, Attention, and Transformers emerged from different input-structure problems. | Distinguish whether each structure is strong on images, order, or long context. |
| Is the current improvement due to `deeper representation`, or due to `more stable learning`? | In deep learning explanations, structural improvement and learning-stabilization techniques are often mixed. | Separate the model-structure axis from the optimizer/regularization axis. |

This flow can be summarized simply as follows.

Deep learning stacks structures that turn inputs into better representations. Loss and backpropagation tell the structure how to correct itself, and optimizers and regularization make learning more stable. CNNs, RNNs, Attention, and Transformers emerged to answer different data-structure problems.

## What It Explains

Part 5 can largely be read in three bundles: `basic neural-network computation`, `learning procedures and stabilization`, and `major deep-learning structures`.

First, the early part treats perceptrons, multilayer structure, activation functions, output layers, loss functions, and gradient computation together. This section explains that a neural network is not merely `a function with many layers`, but a structure that gradually turns inputs into different representations and turns loss back into parameter-wise gradient signals.

The middle part treats the learning loop, the difference between model execution and training, optimizers, regularization, GPU, batch, and tensor computation. This section explains not only model structure, but also `how learning becomes possible in practice and scales to large computation`.

Then representation learning is established again as the entrance to structural branching. Only after distinguishing between humans making features directly and models learning representations can CNNs, RNNs, Attention, and Transformers be read as designs answering different data-structure problems rather than as mere model names.

The latter part treats CNNs, RNNs, LSTMs, GRUs, Attention, Transformers, generation, and sampling. This section exists to show `why this structural transition was needed before LLMs`, before moving into the next Part.

In particular, Chapters 11 through 15 are more accurately read not as `introductions to model names`, but as `what kind of data-structure problem caused this design to appear`.

| Chapter | The data-structure problem to hold first | The core that must be confirmed in the current Part |
| --- | --- | --- |
| Chapter 11 CNNs | The problem that nearby positions in an image create meaning together | A structure that repeatedly reads and summarizes local patterns |
| Chapter 12 RNN / LSTM / GRU | The problem that earlier state in sequential data must remain in later judgment | A structure that inherits state and preserves long memory more effectively |
| Chapter 13 Attention / self-attention | The problem that distant clues must be referenced again in the current computation | A transition where relationship re-reference becomes more important than state passing |
| Chapter 14 Transformer | The problem that parallel computation and long-context re-reference must be pushed together | A repeated block structure bundling self-attention, feed-forward layers, and stabilization |
| Chapter 15 generation/sampling | The problem that we must move beyond label selection and create new outputs, then choose actual candidates | The point that generative distribution and sampling choice jointly shape quality |

## Why It Is Needed

When relearning deep learning, the most common confusion is that `model structure`, `learning procedure`, and `computational environment` get mixed together in a single sentence.

For example, if you cannot distinguish whether a performance improvement happened because:

- a deeper structure was used
- the activation or loss design changed
- the optimizer or regularization was more stable
- a larger experiment was possible because of GPUs and parallel processing

then instead of understanding deep learning, you end up only listing terms.

Part 5 builds a common structure for reducing this confusion. Only when computational structure and learning structure are seen separately here can you more clearly read in the next Part `why this structure leads into generation` when Transformers and LLMs appear again.

At the same time, once you understand this structure, later Parts also become clearer about what is a problem of input representation, what is a problem of comparing generated results, and what is a problem of interpreting evidence and evaluation.

## Understanding That Should Remain After This Part

After this Part, you should see deep learning as a structure in which input transformation, error computation, learning adjustment, structural branching, and the link to generation continue in one line.

The process that turns inputs by linear combinations and nonlinear transformations, the process that turns loss into a numerical error, the process that backpropagation and automatic differentiation turn that loss into parameter-wise gradient signals, the process that optimizers and regularization adjust learning, the process that CNNs, RNNs, Attention, and Transformers answer different structural problems, and the process that generation and sampling lead into the next Part on generative AI should all become visible in one flow.

Once this understanding forms, you can move beyond the superficial explanation that `deep learning is a technology that stacks neural networks deeply`, and also reduce the misunderstanding that `only Transformers matter`. Part 5 is the Part that actually performs the main explanation of deep learning and supports the later Parts.

## Completion Criteria

- You can explain the relationship among perceptrons, multilayer neural networks, and hidden layers.
- You can explain why activation functions, output layers, and loss functions must be read together.
- You can say how loss becomes parameter-wise gradient signals, and how backpropagation and automatic differentiation handle that computation.
- You can explain the difference between learning and model execution.
- You can explain what problems optimizers and regularization are trying to solve.
- You can say what structural problems led to the appearance of CNNs, RNNs, Attention, and Transformers.
- You can explain the basic intuition of generative models and sampling.

## Checklist

- Are you reading this Part not as `an introduction to deep-learning names`, but as the Part that settles `structural problems, learning procedures, and the link to generation`?
- Can you explain CNNs, RNNs, Attention, and Transformers all as answers to `what kind of data-structure problem produced them`?
- Can you distinguish that what is passed to Part 6 is not `the part left unexplained in the current Part`, but `the next layer that is built on top of these structures`?

## Sources and References

This overview page is an internal overview that organizes the purpose and learning path of Part 5. It does not directly cite external sources.
