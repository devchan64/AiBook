# P1-11.3 Transformers and Pretrained LLMs

> Section ID: `P1-11.3`
> Version: `v2026.07.26`

Section 11.1 introduced language models and embeddings. Section 11.2 covered the flow of RNNs, Seq2Seq, and Attention for handling order and context.

This section examines two turning points that created the direct lineage of modern `LLMs`:

> Transformers, which placed Attention at the center of the structure  
> and pretraining, which taught models on large-scale text before task-specific use

The central question is:

> if Attention became important,  
> how did modern LLMs grow on top of Transformers and pretraining?

The important flow is:

> Transformers placed self-attention at the center so tokens inside a sequence could refer directly to one another,  
> and pretrained LLMs learned language patterns from large text corpora first, then connected to many tasks through fine-tuning, prompting, or in-context learning.

Part 1 introduces the basic distinctions among `Transformers`, `self-attention`, `positional encoding`, `Encoders`, `Decoders`, `pretraining`, `fine-tuning`, `BERT`, `GPT`, and `in-context learning` here. Section 11.2 first explained why RNNs, Seq2Seq, and Attention emerged. This section continues on top of that flow and organizes the question:

> on what structure and training procedure did modern LLMs grow?

This section does not explain Transformer equations, the inner computation of multi-head attention, or large-scale training infrastructure in detail. Transformer blocks and self-attention structure return in Part 5, and modern LLM service structure returns later in P1-14.1 through P1-14.6.

These terms can all sound like similar names from modern LLM discussions at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| Transformer | a sequence-model structure centered on self-attention | the core structural family of modern LLMs |
| self-attention | a structure that computes relevance among tokens in the same sequence | the central mechanism of Transformers |
| positional encoding | a way to add token-position information | the supplement for handling order without recurrence |
| Encoder | a structure that builds contextual representations of the full input | the basis for understanding the BERT family |
| Decoder | a structure that generates the next token from previous tokens | the basis for understanding the GPT family |
| pretraining | the stage of first learning from large text | the key to broad language-pattern learning |
| fine-tuning | additional adjustment for a specific task | a major post-pretraining usage pattern |
| in-context learning | changing behavior through prompt context without weight updates | the key shift in GPT-3 style user experience |

The minimum distinction to keep is: Transformers are centered on self-attention, BERT is encoder-centered, GPT is decoder-centered, and pretraining comes first.

This section focuses only on four questions:

| Topic | Question in this section |
| --- | --- |
| Transformer | why did Attention become the central model structure? |
| Encoder and Decoder | why are the BERT and GPT families used differently? |
| pretraining | why is the model first trained on large text corpora? |
| in-context learning | why can examples inside a prompt change the model’s behavior? |

Prompt-writing practice returns in P1-12.1 through P1-12.3. Vector search and RAG return in P1-13.1 through P1-13.4 and P1-14.2. AI service architecture returns in P1-14.1 through P1-14.6. Here, the only goal is to keep one big line clear: modern LLMs did not appear suddenly, but grew out of language modeling, embeddings, sequence modeling, Attention, and pretraining. This section separates only `structure`, `training procedure`, and `changes in user experience`.

## Connecting Transformers with Pretraining

- Understand Transformers as structures centered on self-attention.
- Understand self-attention not as human attention, but as a way to compute relevance among tokens.
- Understand intuitively why positional encoding is needed.
- Distinguish the roles of Encoder, Decoder, and Encoder-Decoder structures.
- Understand that BERT and GPT both belong to the Transformer family but differ in training goals and usage direction.
- Distinguish pretraining from fine-tuning.
- Understand how GPT-2 and GPT-3 led into zero-shot, few-shot, and in-context-learning experience.
- Avoid identifying LLMs with all of AI.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Transformers raised Attention into the central structure | This shows why Transformer explanations are unavoidable in modern LLM discussion. | It is enough to understand them as structures where tokens refer directly to one another. |
| pretraining means learning from large text first | This explains why LLMs develop broad language behavior before task-specific use. | It is enough to know that the model first trains on a large corpus before being adapted to particular tasks. |
| BERT and GPT are both Transformer-family models but serve different roles | This prevents Transformers from being mistaken for one single product. | It is enough to understand that models in the same family can still have different training goals and usage directions. |

## Transformers Put Attention at the Center

In 11.2, RNNs processed sequences by passing forward hidden states. That fits ordered data naturally, but long inputs create a burden of step-by-step computation.

Attention suggested another possibility. If the model can refer directly to relevant positions in the input, it no longer needs to pack everything into a single fixed-length vector.

Transformers raised that idea from a supporting device to the main structure. The 2017 paper by Vaswani and colleagues proposed a sequence-transduction architecture that uses attention without recurrence or convolution. The title *Attention Is All You Need* captures that turning point.

The core intuition is:

> each token in a sentence  
> looks at other tokens in the same sentence  
> and updates its own representation accordingly

Consider:

> the model predicts the next token from earlier context

When handling `predicts`, the tokens `model`, `earlier context`, and `next token` may all matter. `Self-attention` computes weights so tokens in the same sequence can refer to one another.

Here, `self` does not mean a token looks only at itself. It means that tokens refer to other tokens within the same input sequence.

## Positional Encoding Restores Order Information

RNNs naturally include order because they process inputs sequentially. Transformers, however, use self-attention without recurrence. That means a separate device is needed to supply order information.

This is why Transformers use `positional encoding`.

> token embedding:  
> information about what the token is
>
> positional encoding:  
> information about where the token is

At the introductory level:

> "I read books"
>
> I: token meaning + first position  
> read: token meaning + second position  
> books: token meaning + third position

This does not mean Transformers are blind to order. It means they do not pass hidden states sequentially the way RNNs do. Instead, they incorporate position information into self-attention-based computation.

## Encoder and Decoder Have Different Roles

The original Transformer paper used an `Encoder-Decoder` structure. The Encoder builds representations of the input sequence, and the Decoder generates the output sequence.

| Structure | Representative line | Intuition |
| --- | --- | --- |
| Encoder | BERT family | builds contextual representations by looking at the full input |
| Decoder | GPT family | generates the next token from left context |
| Encoder-Decoder | original Transformer translation setup | reads an input sequence and transforms it into an output sequence |

This distinction becomes important for understanding BERT and GPT.

`BERT` uses the Transformer encoder. The BERT paper by Devlin and colleagues describes pretraining deep bidirectional representations using masked language modeling and next sentence prediction, then fine-tuning those representations for many tasks.

`GPT` belongs to the Transformer-decoder line. The 2018 GPT paper by Radford and colleagues proposed generative pretraining followed by task-specific fine-tuning. The GPT family is close to the autoregressive language-model line that predicts the next token from previous context.

This distinction should not be oversimplified into:

> BERT understands, GPT thinks

That phrasing creates confusion. The safer version is:

> the BERT family is encoder-centered and strong at building contextual input representations  
> the GPT family is decoder-centered and strong at generating the next token from earlier context

## Pretraining Lets the Model Learn Language Patterns First

`Pretraining` means that instead of going directly into one specific task, the model first learns general language patterns from large text corpora.

> pretraining:  
> first learn from a large text corpus
>
> fine-tuning:  
> later adjust the model for a specific task

This flow did not begin only with Transformers. `ELMo` introduced deep contextualized word representations that reflect the fact that word meaning changes with context. `ULMFiT` showed a systematic procedure of pretraining a language model and then fine-tuning it for a target task.

The Transformer family scaled this much further. GPT combined generative pretraining with supervised fine-tuning. BERT used masked language modeling to pretrain bidirectional representations.

The important caution is:

> pretraining does not mean the model stores facts as verified truth  
> it means the model learns language patterns and representations  
> through training goals such as next-word prediction, masked-word recovery, and context relations over large text corpora

That is also why a pretrained LLM can still generate plausible but unsupported content. The model learned patterns of language, not guaranteed truth.

## Contextual Representations Went Beyond Static Embeddings

The earlier embeddings from 11.1 can be understood as relatively fixed vectors for each word. But in real language, meaning changes with context.

> I deposited money in the bank.  
> I saw trees near the river bank.

The surface form `bank` is the same, but the context changes the meaning. `ELMo` addressed this by producing word representations that change with context. `BERT` also uses a Transformer encoder to build representations that reflect the full input context.

This matters for understanding LLMs. LLMs do not treat words only as fixed dictionary entries. They compute the role of a token within surrounding context.

## GPT-2 and GPT-3 Expanded Prompt-Based Use

`GPT-2` emphasized that a language model could display many task behaviors through natural-language instruction and examples. The paper showed that a model trained on WebText could perform multiple downstream tasks in a zero-shot setting without separate task-specific fine-tuning.

`GPT-3` expanded this line much further. Brown and colleagues compared zero-shot, one-shot, and few-shot settings with a 175B-parameter model. The key point is that `few-shot` here does not mean retraining model weights.

> fine-tuning:  
> update the model weights using training data
>
> in-context learning:  
> change the output behavior by including instructions and examples inside the prompt  
> while leaving the base weights unchanged

That flow led directly into today’s experience of describing tasks to an LLM in natural language and supplying examples in the prompt.

This section does not go into prompt-writing technique. The structure and limits of prompts return in 12.1 through 12.3. Here the narrower point is enough:

> GPT-2 and GPT-3 widened the experience that natural-language input itself can function as the way a task is specified

The GPT-3 paper also notes a limitation. Even if few-shot performance improves, that does not automatically prove that the model learns new tasks the same way people do. The paper points out that it is hard to separate actual task learning from recognition of patterns already seen in training data.

## Shortcuts to Avoid in This Section

The following shortcuts are risky:

| Risky shortcut | Safer phrasing |
| --- | --- |
| Transformer is the same thing as an LLM | Transformers are a core structure widely used in modern LLMs, but do not mean the whole of LLMs |
| pretraining is just memorizing facts | pretraining is learning language patterns and representations from large text |
| BERT understands and GPT thinks | BERT and GPT are different lines within the Transformer family, with different structures and training goals |
| prompt examples retrain the model | in-context learning usually changes behavior through input context without updating weights |
| AI is basically the same thing as LLMs | LLMs are a major stream of modern AI, but not the whole of AI |

The last shortcut matters especially. Today, AI is often immediately equated with LLMs. But AI also includes rule-based systems, search, machine learning, reinforcement learning, computer vision, speech recognition, robotics, and recommender systems. The safer position is:

> LLMs are one major line that created a large change in language and generative interfaces,  
> but they are not identical to all of AI

## Checklist

- I can explain Transformers as self-attention-centered structures.
- I can explain self-attention as relevance computation among tokens rather than human conscious attention.
- I can explain why positional encoding is needed.
- I can distinguish Encoder, Decoder, and Encoder-Decoder roles.
- I can explain that BERT and GPT both belong to the Transformer family but differ in structure and training goals.
- I can distinguish pretraining from fine-tuning.
- I can describe ELMo and ULMFiT as important signs before large pretrained Transformers.
- I can explain in-context learning as behavior change through input context without weight updates.
- I do not identify LLMs with all of AI.
- I can explain Transformers, pretraining, BERT, and GPT not as one lump of trendy terms but by separating `structure`, `training procedure`, and `changes in user experience`.
- I can explain modern LLMs not as a single product name but as a family that grew on top of self-attention structure and large-scale pretraining.

## Sources and Further Reading

- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, accessed 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2018, accessed 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2019, accessed 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
