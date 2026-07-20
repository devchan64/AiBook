# P1-9.3 Distinguishing the Direct Lineage of LLMs from Surrounding Evidence

> Section ID: `P1-9.3`
> Version: `v2026.07.20`

Section 9.1 looked at image recognition and representation learning. Section 9.2 looked at object detection and speech generation.

Now the task is to connect those cases to the history of `LLMs` in a careful way.

The central question is:

> are cases such as AlexNet, YOLO, and WaveNet direct ancestors of LLMs,  
> or are they better treated as surrounding evidence that the deep-learning paradigm became broadly persuasive?

> the direct lineage of LLMs should be explained through language modeling, sequence modeling, Seq2Seq, Attention, and Transformers; image, object-detection, and speech-generation cases are better treated as surrounding evidence that deep learning spread across many fields

This section distinguishes `direct lineage`, `surrounding evidence`, `language modeling`, `Seq2Seq`, `Attention`, and `Transformer` from the viewpoint of LLM history. The image, detection, and speech cases from 9.1 and 9.2 are organized not as `direct ancestors of LLMs`, but as part of the background that shows how the deep-learning paradigm spread. The direct flow is handed off from Chapter 11 to Chapter 14 and then into Part 6.

These historical terms can sound similar at first. A quick separation helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| direct lineage | the line that leads directly into the core structure of LLMs | the standard for deciding what is essential to LLM explanation |
| surrounding evidence | cases that form the background of the spread of deep learning | important background, but not direct ancestors |
| language modeling | the problem of modeling next-word or next-token probabilities | the starting point of the direct LLM flow |
| Seq2Seq | a structure that maps an input sequence to an output sequence | an important pre-stage in the direct lineage |
| Attention | a structure that refers more strongly to the input positions that matter | the key shift before Transformers |
| Transformer | a sequence-model structure centered on Attention | the core structural family of modern LLMs |

The minimum distinction to keep is:

- the direct lineage of LLMs belongs to language modeling
- AlexNet, YOLO, and WaveNet are surrounding evidence
- Transformers are central, but not the whole story

One more intention also matters here. Today people often hear `AI` and immediately think of LLMs or chatbots. This section is deliberately cautious about that shortcut. LLMs are extremely important for understanding modern AI, but if all of AI is reduced to LLMs, other lines such as rule-based AI, search, probabilistic models, computer vision, speech, reinforcement learning, recommendation, and robotics disappear from view.

This section does not write the full detailed history of LLMs. Statistical language models, word embeddings, RNNs, LSTMs, Seq2Seq, Attention, Transformers, pretraining, instruction tuning, and RLHF are only positioned here at a map level. Their detailed explanation starts in Part 1 Chapter 11 through Chapter 14, continues into Part 5 for the structural basis of Transformers, and then into Part 6 for the main line of LLM pretraining and generation.

So this section takes on only two roles as the conclusion of P1-9:

- place the `direct lineage` of LLMs on the side of language modeling and sequence modeling
- keep `AI as a whole` from collapsing into `LLMs only`

This section also does not fully explain `tokenization`, `embedding`, or `pretraining`. The key point is not the details of one structure, but building a map that separates:

> what is direct lineage  
> and what is surrounding evidence

The scope can be summarized like this:

> direct lineage:  
> model structures and training flows for language and sequence data
>
> surrounding evidence:  
> cases where deep learning reduced hand-built rules and features  
> and showed strong results in image, location, speech, and generation problems

This separation is needed for a simple reason. If every successful deep-learning case is connected in a straight line to LLMs, the history looks easy to tell, but causes and background become mixed together.

## Separating Direct Lineage from Surrounding Evidence

- Distinguish direct lineage from surrounding evidence.
- Place the direct flow of LLMs on the side of language modeling and sequence modeling.
- Avoid exaggerating AlexNet, YOLO, and WaveNet into direct ancestors of LLMs.
- Place LLMs as one major stream inside the larger AI landscape rather than reducing all of AI to LLMs.
- Treat Transformers as an important turning point without pretending that they alone explain the whole history of LLMs.
- Build a map that leads from Part 1 Chapter 11 through Chapter 14 into Part 5 and Part 6.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| the direct lineage of LLMs belongs to language modeling and sequence modeling | This prevents image and speech cases from being attached too directly to LLM history. | It is enough to understand that the direct line belongs to models for words, tokens, and sequential language data. |
| AlexNet, YOLO, and WaveNet are surrounding evidence | This preserves the meaning of deep-learning spread without overstating causal lineage. | It is enough to understand them as evidence that deep learning gained force in many fields. |
| reducing all of AI to LLMs hides other major streams | This keeps the overall map of Part 1 intact. | It is enough to understand that LLMs are a major stream inside AI, not the whole of AI itself. |

## First Distinction: Direct Lineage and Surrounding Evidence

`Direct lineage` means a technical flow that is directly required to explain the core problem and structure of LLMs. Generative LLMs usually treat language as a sequence of `tokens`, estimate a probability distribution over candidate next tokens given prior `context`, and then generate output using learned `parameters`.

Here, a `token` is not always the same as a human-readable `word`. In LLMs, it means a basic unit into which text is divided so the model can process it. Tokenization and embedding are introduced at a map level in P1-11 through P1-13 and then revisited in Part 6 as actual computational units and learned representations in LLMs.

> text  
> -> token  
> -> next-token probability distribution

This flow is not completely disconnected from earlier concepts. The earlier perspective of a `symbol` as a distinguishable sign helps with the intuition of tokens, and the earlier discussion of `features` and `representations` helps prepare for tokenization and embedding. But 9.3 is not centered on tokenization itself. The center is the distinction between direct lineage and surrounding evidence.

So the direct lineage connects to questions such as:

> how should words and sentences be represented numerically?  
> how should the next word be predicted from previous words?  
> in long contexts, what information should be referred to?  
> how should such structures be trained with large data and large compute?

`Surrounding evidence`, by contrast, means cases that do not directly determine the core structure of LLMs but did help deep learning become a persuasive research direction.

| Distinction | Central question | Examples |
| --- | --- | --- |
| direct lineage | how should language and sequence data be modeled? | neural language models, Seq2Seq, Attention, Transformers |
| surrounding evidence | why did deep learning become persuasive across fields? | AlexNet, YOLO, WaveNet |

The important point is not that surrounding evidence is less important. It matters because it shows the background in which the deep-learning paradigm gained strength.

This boundary also matters in the opposite direction:

> AI as a whole  
> -> LLM

That shortcut may fit current tool experience, but it narrows the history too much. The purpose of 9.3 is not to make LLMs look smaller. It is to see more clearly what direct line they stand on and what larger background helped that line grow.

## Where the Closer Materials to LLMs Belong

Many materials may look like ancestors of LLMs, but they are not all ancestors in the same sense.

| Material or line | Why it is close to LLMs | Position in this section |
| --- | --- | --- |
| neural language models | they show a line where word-sequence probabilities and word representations are learned with neural networks | starting point of the direct lineage |
| word2vec | it strongly established the idea of learning vector representations of words | an important earlier stage in representation learning and word embedding |
| Seq2Seq | it showed a language-processing structure that maps input sequences to output sequences | direct lineage |
| Attention | it showed a structure that refers to relevant input positions at each output step | direct lineage |
| Transformer | it connected Attention-centered structure strongly to large-scale sequence modeling | the core structural family of modern LLMs |
| ELMo | it introduced contextualized word representations | an earlier stage in contextual language representation |
| ULMFiT | it showed how a pretrained language model could be fine-tuned for downstream tasks | an important earlier stage in NLP transfer learning |
| BERT | it strongly demonstrated Transformer-based pretraining and fine-tuning | direct background for modern language-representation models |
| GPT series | it directly showed the line of Transformer decoders, language modeling, pretraining, generation, scaling, and in-context learning | the closest direct lineage to modern generative LLMs |

This table does not try to tell the entire history of LLMs. It only sets the boundary that language modeling, representation learning, pretraining, and Transformer-family research are more direct to LLM explanation than image recognition or object detection cases.

## Direct Lineage 1: Language Modeling

`Language modeling` is the problem of handling word or token sequences probabilistically. Bengio and colleagues described the goal of statistical language modeling as learning the joint probability of word sequences in language. The same paper also proposed learning distributed word representations to reduce the curse of dimensionality.

The introductory baseline is:

> a language model does not begin by declaring that it `understands a sentence`  
> it begins by estimating how plausible a sequence of words or tokens is  
> and what is likely to come next

Here, `probability` does not mean always guessing the one correct answer. It means assigning scores to uncertain candidates. That connects back to the explanation of `probability`, `uncertainty`, and `stochastic process` in Chapter 6.

## Direct Lineage 2: Seq2Seq

`Seq2Seq` means a structure that takes an input sequence and produces an output sequence. A representative example is machine translation. This does not mean every modern LLM is itself a Seq2Seq structure, but Seq2Seq is an important earlier stage for understanding language as a learning problem over sequential inputs and outputs.

The Seq2Seq paper by Sutskever, Vinyals, and Le showed that LSTMs could solve general sequence-to-sequence problems and demonstrated English-to-French translation with a large deep LSTM.

At the introductory level, the core intuition is:

> read the whole input sentence  
> transform it into an internal representation  
> generate the output sentence step by step from that representation

This is not the same thing as an LLM itself, and it is not the direct final structure of all LLMs. But it showed a move away from processing language only through fixed rule lists and toward learning the correspondence between input sentences and output sentences through neural networks.

## Direct Lineage 3: Attention

Early encoder-decoder structures had a problem. If a long sentence had to be compressed into one fixed-length vector, information could bottleneck.

The Attention paper by Bahdanau, Cho, and Bengio proposed reducing that problem by letting the model refer to relevant parts of the input sentence at each step of generation. The paper explains that the decoder learns to decide which parts of the source sentence to pay attention to.

The safe intuition is:

> when generating each output word,  
> the model does not rely only on one lumped memory of the whole input;  
> it refers more strongly to the input positions that matter right now

Here, `Attention` is not the same as a human psychological explanation of conscious focus. It is safer to read it as a mechanical structure inside the model that computes weights over positions and uses relevant information more strongly.

## Direct Lineage 4: Transformer

`Transformer` is a major turning point in the Attention line. Vaswani and colleagues explained that strong sequence-transduction models had usually been based on recurrent or convolutional neural networks with encoders and decoders, and then proposed a Transformer based on Attention mechanisms while removing recurrence and convolution.

Two points matter most:

| View | Meaning |
| --- | --- |
| self-attention | positions inside one sequence refer to one another when forming representations |
| parallelization | the burden of processing strictly step by step, as in RNNs, is reduced, which helps large-scale training |

The Transformer paper showed that sequence transduction could be performed with Attention alone, without recurrence or convolution, and that this structure was easier to parallelize.

But exaggeration should still be avoided:

> Transformer -> immediately modern LLM

That is too short. Modern generative LLMs should be understood as the result of Transformer-family structures combined with large-scale data, pretraining, tokenization, scaling, training stabilization, and depending on the research or product line, alignment methods such as instruction tuning and RLHF.

## Surrounding Evidence Made Deep Learning More Persuasive

The cases in 9.1 and 9.2 are safer to place as surrounding evidence that deep learning spread widely across fields rather than as direct lineage of LLMs.

| Case | Direct lineage? | Role in this chapter |
| --- | --- | --- |
| AlexNet | no | turning point that showed the combination of large data, deep CNNs, GPUs, and training techniques in image recognition |
| YOLO | no | a case that reframed object detection as a single neural-network prediction problem |
| WaveNet | no | a case that treated raw audio as a probabilistic sequence-generation problem |

This lets us write a safer sentence:

> LLMs were not born directly out of image recognition or object detection.  
> But the repeated deep-learning successes of the 2010s strengthened belief in large data, compute, representation learning, and end-to-end training.  
> Against that background, research in language modeling and Transformer-family structures grew much more strongly.

## Shortcuts to Avoid

The following shortcuts are especially risky:

| Shortcut to avoid | Problem | Safer phrasing |
| --- | --- | --- |
| AI is the same thing as LLMs | other research lines and application areas disappear | LLMs are a major stream in modern AI, but not the whole of AI |
| AlexNet created LLMs | direct lineage between image classification and language modeling gets mixed | AlexNet is a representative turning point in the spread of deep learning |
| YOLO drove the development of LLMs | an object-detection model starts to look like a direct ancestor | YOLO is a case of end-to-end reframing in object detection |
| WaveNet is an ancestor of LLMs | audio-waveform generation gets confused with language modeling | WaveNet is a surrounding case of probabilistic sequence generation |
| knowing only Transformers explains the whole history of LLMs | pretraining, data, scaling, and alignment disappear | Transformers are central, but the full history is broader |

The explanation this chapter wants is not:

> everything connects to LLMs in one straight line

The better explanation is:

> deep learning spread across many fields by learning representations and predicting or generating outputs  
> LLMs grew on top of the direct lineage of language modeling and sequence modeling

## Checklist

- I can distinguish direct lineage from surrounding evidence.
- I can explain the direct flow of LLMs through language modeling, Seq2Seq, Attention, and Transformers.
- I do not write AlexNet, YOLO, or WaveNet as direct ancestors of LLMs.
- I can treat Transformers as a major turning point without reducing the whole history of LLMs to Transformers alone.
- I can explain both the spread of the deep-learning paradigm and the direct development line of LLMs without mixing them together.
- I do not use `AI` and `LLM` as if they meant the same thing.
- I can judge how far cases such as AlexNet, YOLO, and WaveNet should be connected by separating direct lineage from surrounding evidence.
- I can explain the importance of LLMs without reducing the whole AI map to LLMs alone.
- when re-establishing the direct flow of LLMs on the side of language modeling, Seq2Seq, Attention, and Transformers
- when preserving the importance of LLMs without reducing all of AI to LLMs

In those moments, separate:

> direct lineage  
> surrounding evidence  
> the larger AI landscape

That makes it easier to place image and speech cases as background while placing language modeling and Transformer-family work on the direct line that leads into later chapters.

## Sources and Further Reading

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-06-23.
- Ashish Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, accessed 2026-06-23.
- Matthew E. Peters et al., [Deep contextualized word representations](https://arxiv.org/abs/1802.05365){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Jeremy Howard, Sebastian Ruder, [Universal Language Model Fine-tuning for Text Classification](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2018, accessed 2026-06-23.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-06-23.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI, 2019, accessed 2026-06-23.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-06-23.
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, [Deep learning](https://www.nature.com/articles/nature14539){: target="_blank" rel="noopener noreferrer" }, Nature 521, 436-444, 2015-05-27, accessed 2026-06-23.
