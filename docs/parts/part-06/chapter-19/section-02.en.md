# P6-19.2 A Criterion for Separating Direct Lineage from Surrounding Evidence

> Section ID: `P6-19.2`
> Version: `v2026.07.26`

If P6-19.1 held the large development flow, this section needs a sharper criterion for separating direct structural lineage from surrounding evidence of spread. Not every event in deep learning history is immediately part of the direct lineage of LLMs.

Direct lineage is the flow that leads directly to the structure and learning methods of current LLMs. Surrounding evidence explains the spread of deep learning and shifts in computational paradigms, but it is harder to assert as an ancestor of the LLM structure itself.

## Direct Lineage Criterion

The first questions to split are:

- What can be called the direct lineage of LLMs?
- What is an important example of deep learning spread, but hard to call direct lineage?
- Why is this distinction important for learners?

If `direct structural lineage` and `surrounding evidence of spread` are not separated first, it is easy to misunderstand all of deep learning history as one straight lineage. The previous section drew a large historical map. Here, inside that map, the question narrows to where we should divide `flows that directly lead to current LLM structure` from `flows that should remain as the background of deep learning spread`.

So the criterion here is not `do we know many famous events?`, but `what directly connects to current LLM structure?`

The core of this distinction is to avoid expanding lineage explanation into a `new history list`. Rather than memorizing more names, it is enough to establish a criterion that separates the main explanation into `direct structural ancestors` and `surrounding background`.

## Direct Structural Lineage and Surrounding Evidence of Spread

- You can distinguish direct lineage from surrounding evidence.
- You can explain LLM history without exaggeration.
- You can explain why deep learning spread cases are important but may not be direct ancestors.
- You can reorganize the Transformer explanation from a clearer position.

## Why This Distinction Is Needed

Recently, people often understand AI by immediately connecting it to LLMs. This easily creates confusion such as:

- every famous deep learning event is immediately part of the LLM lineage;
- speech models, object detection models, and reinforcement learning models all sit on the same straight line;
- `they are all neural networks, so they are all the same history`.

This kind of explanation can capture the broad atmosphere, but structural understanding becomes blurry.

A safer explanation is:

- some flows lead directly to the structure and learning objectives of LLMs;
- some flows are background evidence showing the spread of the deep learning paradigm and the importance of compute resources.

## What Is Direct Lineage?

Here, the following flow is treated as direct lineage of LLMs.

1. Language model
2. Embeddings and distributed representations
3. RNN, LSTM, Seq2Seq
4. Attention
5. Transformer
6. Pretraining
7. Transformer-family language models such as GPT and BERT

The commonality in this flow is clear.

- It handles language as input.
- It computes order and context of tokens or words.
- It connects to next-token prediction or language representation learning.
- It connects directly to current LLM structure.

In other words, these can be explained as ancestors of `LLM internal structure and learning method`.

## What Is Surrounding Evidence?

By contrast, the following examples are very important, but caution is needed before calling them direct lineage.

- AlexNet and the image-recognition breakthrough
- Object detection families such as YOLO
- Speech generation families such as WaveNet and Deep Voice
- Representative search and reinforcement learning cases such as AlphaGo and AlphaZero

These cases matter because:

- they socially showed that deep learning could create real performance shifts;
- they strengthened the importance of GPU and large-scale compute resources; and
- they created a flow where learning-based approaches spread to many domains.

But if they are written immediately as `direct ancestors of LLMs`, the boundary becomes blurry.

## Why Deep Voice or YOLO Is Not Direct Lineage

For example, Deep Voice is an important case in speech synthesis. YOLO is a representative turning point in real-time object detection.

Both show the spread of the deep learning paradigm, but they are different from the core language-model lineage that formed the direct structure of current LLMs.

A safer explanation is:

- Deep Voice and YOLO are surrounding evidence that `deep learning became strong across many input and output domains`.
- The direct structural history of Transformer-based LLMs should be found more directly in `language modeling and attention families`.

They are related, but they should not be placed unchanged on the same line.

## Why Surrounding Evidence Still Matters

But removing surrounding evidence creates another problem. LLMs did not appear suddenly from a quiet language-model-only development path.

Surrounding evidence answers questions such as:

- Why did deep learning gain social trust and investment?
- Why did parallel processing and GPUs become important?
- Why did data scale, model scale, and compute scale grow together?

So surrounding evidence is not a `structural ancestor`, but it explains the `historical atmosphere and infrastructure conditions`.

## Boundary Between Direct Lineage and Surrounding Evidence

The distinction to keep first is simple. Once direct lineage and surrounding evidence are separated clearly, BERT, GPT, and RAG explanations are less likely to mix structural explanation and background explanation.

Use these two lines as the starting criterion.

- Language modeling, attention, Transformer, and pretraining are close to direct lineage.
- Major results in vision, speech, and reinforcement learning are important, but usually read as background explanation.

## Drawing Direct Lineage and Surrounding Evidence Separately

```mermaid
--8<-- "assets/part-06/chapter-19/p6-c19-s02-lineage-boundary-en.mmd"
```

The purpose of this diagram is one thing:

`read one-line history and background conditions separately.`

## Cases and Examples

### Case 1. Explaining Transformer

Suppose a lecturer introduces Transformer and writes `AlexNet -> YOLO -> GPU -> Transformer` on the first slide. When famous names are placed in time order, it is easy to accept all of them as the same lineage. But this explanation omits the direct structural problems: `why Seq2Seq alone struggled to carry earlier information through long sentences`, and `why attention was needed`. The old criterion was `know many famous events`, but the more important criterion is `which limitation in the immediately previous structure did the next structure solve?`

So the explanation closes only after first showing the scene where earlier context weakens in long-sentence translation, and then attaching attention and Transformer. The shift here is from asking `do many famous events appear?` to asking `does the bottleneck of the previous structure actually lead to the next structure's solution?` The misunderstanding to correct is the feeling that `if they are grouped on the same slide, their direct lineage is also the same`. The result to confirm in this case is whether the reason for the Transformer shift becomes clearer only after explaining the previous structural bottleneck, and whether vision events remain only as background.

### Case 2. Explaining GPUs

Imagine a presenter answering `Why did LLMs become possible?` by showing only GPU photos and server racks for a long time. If we only hear that compute equipment became larger, it is easy to feel that `GPU eventually created even the model principle`. But GPUs are a condition that let models run larger. They are not themselves the structure that explains `which context attention compares and which tokens it looks at more`. The simple criterion people often use combines `what made it run well` with `the idea of what to compute`, but these are different levels.

For example, even with many GPUs, if the attention structure is not explained, we cannot understand why LLMs read long context. The shift here is from asking `did compute resources grow?` to asking `are background conditions and structural principles actually explained separately?` The misunderstanding to correct is reading `conditions that made it possible` and `direct structural principle` as the same lineage. The result to confirm in this case is whether compute-scale background and model-structure explanation are actually read separately, and whether GPU explanation does not replace understanding of attention structure.

### Case 3. Generative AI Boom

Think of a news article where chatbots, image generators, and speech synthesis services all become popular in the same year. In this case, it is easy to group them first as `technologies that became popular together must share the same history`. But in reality, simultaneity in user experience and direct structural lineage must be separated. For example, customers may call both text generation and image generation `generative AI`, but the internal histories may split more closely into language-model lineage and vision-generation lineage. The simple criterion people use is `did they become famous at the same time?`, but the more important criterion is `which input, learning objective, and structural change connect directly?`

The shift here is from asking `did they become hot at the same time?` to asking `is the directly connected structural lineage the same?` The misunderstanding to correct is the feeling that `if technologies became famous together, their one-line history is also the same`. The result to confirm in this case is whether the simultaneity of a trend and the direct lineage of a structure can actually be explained with different criteria, and whether popular cases from the same period can also be placed as surrounding evidence rather than direct lineage.

The three cases can be tied back to the distinction between direct lineage and surrounding evidence.

| Scene | What is easy to mix | What should actually be separated |
| --- | --- | --- |
| Transformer explanation | Famous event list and structural shift | Previous bottleneck and next-structure solution |
| GPU explanation | Compute resources and model principle | Enabling background condition and direct structure |
| Generative AI boom | Simultaneous popularity and direct lineage | Same-period popularity and actual structural family |

## Scenes Where Lineage and Background Should Be Separated

A common misunderstanding when first reading the distinction between direct lineage and surrounding evidence is to group everything as `if it is famous, it must be the same lineage`. But the first thing to check is not fame. It is `which part of current LLM structure does this directly lead to?` Turned into practical questions, this reads as follows.

| If this suspicion appears | First question to ask |
| --- | --- |
| `Is this famous event also an ancestor of LLMs?` | Does it directly lead to current language-model structure and learning method? |
| `Why does GPU explanation appear so much?` | Should this be read as background-condition explanation rather than structural-principle explanation? |
| `If technologies became popular together, aren't they the same history?` | Did we separate simultaneous popularity from direct lineage? |

The first criterion to learn is simple. Direct lineage is the flow that connects directly through `language input`, `context computation`, `next-token/representation learning`, and `attention-Transformer-pretraining`. Surrounding evidence explains the spread of deep learning and compute conditions, but it is background that is too distant to place immediately as structural ancestry.

## Exercise: Split a One-Line History Explanation Again

The following explanation mixes famous events and conditions in one line.

`AlexNet -> YOLO -> GPU scaling -> Transformer -> GPT`

Read as-is, the famous events of deep learning all look like direct ancestors of LLMs. But the judgment needed in this section is not memorizing names in time order. It is dividing how each item relates to current LLM structure.

First, place the items into the three cells below.

| Category | Items to place | Judgment question |
| --- | --- | --- |
| Direct structural history |  | Does it lead directly to current LLM structure through language input, context computation, and next-token or representation learning? |
| Surrounding spread history |  | Is it background evidence that deep learning became strong across several domains? |
| Infrastructure condition |  | Is it a condition that enabled large-scale training and deployment, rather than the model structure itself? |

The explanation can be organized as follows.

| Item | More appropriate position | Reason |
| --- | --- | --- |
| AlexNet | Surrounding spread history | It shows a performance shift in image recognition, but it is not an item that directly leads to the context-computation structure of language models. |
| YOLO | Surrounding spread history | It is a representative result in object detection, but not a direct ancestor of next-token prediction or attention-based language generation. |
| GPU scaling | Infrastructure condition | It is an important condition that enabled large-scale training, but not a structural principle explaining what the model computes and how. |
| Transformer | Direct structural history | It raises attention into the central structure and directly handles token-to-token relationship computation, so it leads directly to current LLM structure. |
| GPT | Direct structural history | Through decoder-only Transformer, pretraining, and prompt-based use, it directly connects to today's generative LLM experience. |

The result to confirm in this exercise is that `famous`, `important at the same time`, and `contributed to AI progress` do not all mean the same thing. Direct structural history is an item that connects to the input, learning objective, and context-computation method of current LLMs. Surrounding spread history and infrastructure conditions explain the background in which LLMs grew and were accepted.

## Main Flow and Background Split by Lineage Selection

This classification exercise prevents history writing from ending as a `list of famous names`. Later historical explanations become clearer only when we distinguish which items form the direct lineage of the LLM structure and which items are surrounding evidence showing spread and expectations in the same era.

Here, we narrow the large development flow from P6-19.1 through the criterion `what is direct structural history and what is background spread history?` This lets us distinguish the direct lineage that made current LLM structure, instead of collapsing many deep learning achievements into one straight history.

The more important distinction here is:

- `direct structural history`: the core lineage that made current LLMs;
- `surrounding spread history`: cases showing why deep learning became strong and widely accepted.

With this distinction, when recalling BERT, GPT, pretraining, prompts, RAG, and agents from Part 6, structure and atmosphere are less likely to be mixed.

## How Direct Lineage Changes the Main-Flow Interpretation

Once this distinction is established, the main-flow explanation can be reread as a narrower structural question.

- From an LLM viewpoint, what is the core of the Transformer structure?
- Where does it connect to tokens, context windows, and causal generation?

This question makes us reread P6-4.1 Transformer from the LLM viewpoint. The core is not expanding the history explanation. It is avoiding mixing `direct structural ancestor` and `contemporary background cases` when reading Transformer and GPT.

## Checklist

- You should be able to explain direct lineage as `a flow that directly leads to current LLM structure and learning method`, and surrounding evidence as `spread and infrastructure background`.
- You should be able to say that simultaneity or influence of famous events and structural ancestry are different judgment criteria.
- You should hold this section not as a new history list, but as a boundary that lets the main flow be reinterpreted without exaggeration.

## Sources and References

- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2017, accessed 2026-07-19.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2018, accessed 2026-07-19.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-19.
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, [ImageNet Classification with Deep Convolutional Neural Networks](https://papers.nips.cc/paper/4824-imagenet-classification-with-deep-convolutional-neural-networks){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2012, accessed 2026-07-19.
- Joseph Redmon et al., [You Only Look Once: Unified, Real-Time Object Detection](https://arxiv.org/abs/1506.02640){: target="_blank" rel="noopener noreferrer" }, CVPR, 2016, accessed 2026-07-19.
- Sercan O. Arik et al., [Deep Voice: Real-time Neural Text-to-Speech](https://proceedings.mlr.press/v70/arik17a.html){: target="_blank" rel="noopener noreferrer" }, ICML, 2017, accessed 2026-07-19.
