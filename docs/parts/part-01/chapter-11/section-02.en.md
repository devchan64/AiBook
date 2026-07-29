# P1-11.2 RNN, Seq2Seq, and Attention

> Section ID: `P1-11.2`
> Version: `v2026.07.26`

Section 11.1 introduced `language models` and `embeddings`. This section asks how neural networks tried to handle the `order` and `context` of those vectorized tokens.

The central question is:

> once words and tokens have been turned into vectors,  
> how can a model handle their order and context internally?

The important flow is:

> RNNs handled order by passing previous state into the next computation,  
> Seq2Seq built a structure that turns an input sequence into an output sequence,  
> and Attention allowed the model to refer back to relevant input positions at each output step.

Part 1 introduces the basic distinctions among `RNNs`, `hidden states`, `LSTMs`, `GRUs`, `Seq2Seq`, `Encoder-Decoder`, `Attention`, and the `fixed-length vector bottleneck` here. This section focuses on the narrower question:

> after tokens become vectors,  
> how were their sequence and context handled?

Transformers are not yet handled here. They continue in 11.3.

This section does not explain Transformers. These terms can all sound similar at first, so a quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| RNN | a sequence neural network that passes previous state into the next step | the first structure for handling order |
| hidden state | the internal state that accumulates what has been seen so far | the core of RNN-style context handling |
| LSTM/GRU | RNN variants designed to handle longer context more stably | improvements over RNN limits |
| Seq2Seq | a structure that maps an input sequence to an output sequence | the frame for tasks such as translation and summarization |
| Encoder-Decoder | the reader part and the generator part of a Seq2Seq model | the basic Seq2Seq structure |
| Attention | a structure that looks back at relevant input positions while generating output | the key turning point on the way to Transformers |

The minimum distinction to keep is:

- RNNs accumulate order
- Seq2Seq transforms input sequences into output sequences
- Attention looks back again at relevant input positions

This section focuses on three pre-Transformer flows:

| Topic | Question in this section |
| --- | --- |
| RNN | how can a model process ordered input by accumulating it over time? |
| Seq2Seq | how can an input sentence become an output sentence? |
| Attention | how can the model decide which part of the input matters when producing each output word? |

`LSTMs` and `GRUs` were important RNN-family structures for handling `long-range dependency`, but only the motivation matters here.

This section also does not explain `pretraining` or the difference between `BERT` and `GPT`. Those return in 11.3 together with Transformers.

## Handling Order and Context Inside the Model

- Understand RNNs as neural-network structures for sequence data.
- Understand hidden state not as human memory, but as an accumulated internal state of the model.
- See that LSTMs and GRUs were RNN variants for handling longer context.
- Understand Seq2Seq as a structure that turns an input sequence into an output sequence.
- Understand the fixed-length-vector bottleneck in Encoder-Decoder models.
- Understand Attention as a structure that uses weighted reference to relevant input positions at each output step.
- Avoid exaggerating Attention into human-style conscious focus or logical understanding.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| RNNs handle sequence by passing previous state into the next computation | This shows why sequence data needed a special structure. | It is enough to understand that earlier information is carried forward little by little. |
| Seq2Seq means turning an input sequence into an output sequence | This makes clear how tasks such as translation and summarization were modeled. | It is enough to see it as the framework that turns one sentence into another. |
| Attention lets the model look back at relevant input parts while producing output | This prepares the key transition into Transformers. | It is enough to understand it as an attempt to avoid packing everything into one fixed vector. |

## RNNs Pass Previous State into the Next Computation

N-gram language models used only short prior context. But sentences are `sequence data`: what appears earlier can affect what becomes meaningful later.

For example:

> I finished reading the book that I borrowed from the library yesterday.

To interpret `finished reading`, it helps to preserve the fact that `book` appeared earlier rather than looking only at the immediately previous word.

`RNNs` handled this kind of sequence by passing a previous `hidden state` into the next step:

> input 1 -> state 1  
> input 2 + state 1 -> state 2  
> input 3 + state 2 -> state 3

Here, a hidden state is not the same as human conscious memory. It is the model’s internal vector state, built while processing the sequence so far.

> hidden state:  
> an internal state passed forward so earlier inputs can influence the current computation

Because of this, RNNs could be used on sentences, speech, and time series, where order matters.

## RNNs Struggled with Long Context

The basic RNN idea is simple and powerful, but learning long context stably was difficult. To learn relations between far-apart words, the error signal has to travel backward across many time steps. In that process, gradients can become too small or too large.

At the introductory level, the intuition is:

> short context:  
> earlier information reaches later steps relatively easily
>
> long context:  
> important information may weaken or become unstable across many steps

`LSTMs` became a widely used RNN variant for this long-dependency problem. They use cell state and gates to regulate what information should be kept, what should be newly accepted, and what should be exposed to output.

`GRUs` are another RNN variant with a simpler gate structure but a similar purpose. This section does not compare LSTMs and GRUs in detail. The main point is that RNN-family research grew around the question:

> how can a model handle ordered data while preserving useful information across longer spans?

## Seq2Seq Turns Input Order into Output Order

`Seq2Seq` means a structure that takes an input sequence and produces an output sequence. The representative case is machine translation.

> input sequence:  
> I read a book.
>
> output sequence:  
> I read a book. -> Korean sentence

The basic Seq2Seq structure is `Encoder-Decoder`.

| Component | Role |
| --- | --- |
| Encoder | reads the input sequence and builds an internal representation |
| Decoder | generates the output sequence from that representation |

The 2014 paper by Sutskever, Vinyals, and Le proposed a general sequence-learning approach in which one LSTM turns the input sequence into a fixed-dimensional vector and another LSTM generates the output sequence from that vector. Cho and colleagues also proposed an RNN Encoder-Decoder in which one RNN encodes a symbol sequence into a fixed-length vector and another RNN decodes it into another symbol sequence.

At an introductory level, the structure can be pictured like this:

> input sentence  
> -> Encoder  
> -> sentence vector  
> -> Decoder  
> -> output sentence

This connects back to the embeddings of 11.1. The model does not stop at representing words as vectors. It also treats the whole sentence as something that can be compressed into an internal vector representation.

## A Fixed-Length Vector Can Become a Bottleneck

The basic Encoder-Decoder structure had an important weakness. The entire input sentence had to be compressed into one `fixed-length vector`.

For a short sentence, this can look manageable:

```text
I read.
-> [sentence vector]
-> translated sentence
```

But for a long sentence:

```text
translate a sentence that includes budget, schedule, risk, people in charge, and next actions from a meeting
-> [one sentence vector]
-> output sentence
```

When all input information must be compressed into one vector, important details can be weakened or lost. The Attention paper by Bahdanau, Cho, and Bengio described this as a bottleneck in the basic encoder-decoder structure and proposed looking at relevant parts of the input again while generating each output word.

## Attention Looks Again at the Input Positions That Matter

`Attention` is a structure that refers to multiple input positions through weights at each output step.

Suppose we translate:

> source:  
> The cat sat on the mat.
>
> target being generated:  
> the cat ...

When generating the word corresponding to `cat`, the source position `cat` matters. When generating the phrase corresponding to `on the mat`, that later part of the source matters more.

Attention makes the model behave more like this:

> at each output step  
> score the input positions  
> normalize those scores like weights  
> mix the input representations using those weights to form a context vector  
> use that context vector to generate the next output word

Bahdanau and colleagues described this as a form of `soft search`, where the decoder automatically focuses on the relevant parts of the source sentence. `Soft` here does not mean that only one position is chosen exactly. It means the model can distribute weight across multiple positions.

## Attention Is Not the Same as Human Conscious Attention

Because of the word `Attention`, it is easy to imagine the model attending in the same way a person consciously focuses. This section does not use that explanation.

The safer explanation is:

> Attention:  
> a structure that computes weights over input positions for use in the current output calculation

Attention helps the model refer more strongly to relevant parts of the input. In some cases, attention weights can also be visualized, which makes the structure easier to inspect.

But attention weights should not automatically be treated as `the model’s true reason` or as `full human-like understanding`. Here, Attention is kept in its safer role:

> an important structure that reduces the bottleneck of sequence-to-sequence models

## Why This Leads to Transformers

`RNNs`, `Seq2Seq`, and `Attention` are all important parts of the direct lineage of LLMs. But one more step is needed before we can explain the core structure of modern LLMs.

RNN-based models process sequence step by step. Because they pass previous state into the next state, long sequences create a burden of sequential computation.

Attention showed a stronger idea: directly refer to the relevant positions in the input. Transformers then pushed this further by putting Attention at the center and using `self-attention` so tokens inside a sequence can refer to one another without recurrence.

For now, this is enough to keep:

> RNN:  
> handle order by passing forward previous state
>
> Seq2Seq:  
> transform an input sequence into an output sequence
>
> Attention:  
> use weighted reference to relevant input positions at each output step
>
> Transformer:  
> extend Attention into the central structure

The concrete structure of Transformers and pretrained LLMs continues in 11.3.

## Checklist

- I can explain that an RNN passes the previous hidden state into the next computation.
- I can explain hidden state as an internal vector state rather than human memory.
- I can explain LSTMs and GRUs as RNN variants for handling longer dependencies.
- I can explain Seq2Seq as a structure that turns an input sequence into an output sequence.
- I can distinguish the roles of Encoder and Decoder.
- I can explain why a fixed-length vector can become a bottleneck.
- I can explain Attention as a structure that uses weights over input positions to refer to relevant information.
- I can avoid exaggerating Attention into human-style conscious focus or complete interpretability.
- I am ready to continue into why Transformers put Attention at the center in 11.3.
- I can distinguish `the structure that accumulates order`, `the structure that turns an input sequence into an output sequence`, and `the structure that looks back again at relevant input positions while generating output`.
- I can explain Transformers not as an isolated invention, but on top of earlier sequence-modeling problems and solutions.

## Sources and Further Reading

- Sepp Hochreiter, Jürgen Schmidhuber, [Long Short-Term Memory](https://pubmed.ncbi.nlm.nih.gov/9377276/){: target="_blank" rel="noopener noreferrer" }, Neural Computation 9(8), 1735-1780, 1997, accessed 2026-07-19.
- Kyunghyun Cho et al., [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-06-23.
- Graham Neubig, [Neural Machine Translation and Sequence-to-sequence Models: A Tutorial](https://arxiv.org/abs/1703.01619){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, accessed 2026-06-23.
- Sarthak Jain, Byron C. Wallace, [Attention is not Explanation](https://aclanthology.org/N19-1357/){: target="_blank" rel="noopener noreferrer" }, NAACL-HLT 2019, accessed 2026-07-19.
