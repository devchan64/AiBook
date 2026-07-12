# P1-11.1 Statistical Language Models and Embeddings

> Section ID: `P1-11.1`
> Version: `v2026.07.12`

Chapter 10 showed that when generative AI creates outputs, naturalness, factuality, evidence, and risk all need separate review.

Now the question moves one step earlier:

> where did LLMs come from?

This section does not begin by explaining LLMs directly through Transformers. Instead, it starts with two earlier lines of thought for handling language:

> the line that treated language probabilistically  
> the line that represented language as vectors

When these two lines come together, the following view appears:

> language models handle the order of words and tokens probabilistically,  
> and embeddings turn words and tokens into computable vector representations

Part 1 introduces the basic distinctions among `language models`, `statistical language models`, `n-grams`, `sparsity`, `distributed representations`, `embeddings`, and `word2vec` here. The larger map of `direct lineage` and `language modeling` was introduced in 9.3, and the intuition of `next-output generation` already appeared in 10.2. This section restarts that flow at the level of `pre-LLM language models` and `vector representations`.

## Scope of This Section

This section does not explain the whole history of LLMs. `RNNs`, `LSTMs`, `Seq2Seq`, `Attention`, and `Transformers` are handled in 11.2 and 11.3.

These terms can all sound like similar foundational NLP vocabulary at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| language model | a model that handles the likelihood of the next word or token | the starting point of Chapter 11 |
| n-gram | a short-context model that looks at nearby n units | the representative early statistical approach |
| sparsity | the problem that too many combinations are rare | the core limitation of n-grams |
| distributed representation | a way to represent a word across many numeric dimensions | the perspective that turns symbolic units into vectors |
| embedding | a dense vector representation of a word or token | the input basis for later LLM computation |
| word2vec | a representative method that made embeddings widely familiar | the practical case of distributed representation |

The minimum distinction to keep is:

- language models estimate the probability of the next word
- n-grams use short context
- embeddings are vector representations

This section focuses on three questions:

| Topic | Question in this section |
| --- | --- |
| language models | how do we compute the likelihood of the next word from previous words? |
| n-gram language models | how do we estimate next-word probabilities from short-context counts? |
| embeddings | how do we place words and tokens in vector space? |

The point here is not to fully master the equations. It is to recover the way of thinking that handles language through `probability` and `vectors`, and to see why that line leads toward LLMs.

This section also does not yet explain RNNs, Attention, or Transformers. Their structural flow appears in 11.2 and 11.3. Here the focus stays only on two starting points:

> handling language probabilistically  
> and turning words into vectors

## Goal of This Section

- Understand a language model as a model that handles the probabilities of the next word or next token.
- Understand that n-gram language models use short context and counts.
- Understand that the limits of n-grams connect to sparsity, context length, and weak generalization across similar words.
- Understand distributed representations and embeddings as ways to represent words as vectors.
- Distinguish embeddings from dictionary definitions: embeddings are learned from usage context in data.
- Read LLMs not as suddenly appearing chatbots, but as the accumulation of language modeling and vector representation.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| language models are about the likelihood of the next word or token | This shows the most basic question behind LLMs. | It is enough to understand that the model estimates how plausible the next word is given previous context. |
| n-grams tried to handle language through short-context counts | This shows both the strength and the limitation of early language models. | It is enough to know that they estimated the next word from only a few nearby words. |
| embeddings represent words as vectors | This prepares the path toward later discussion of tokens, representations, vector search, and RAG. | It is enough to understand that words are turned into computable positions rather than kept only as dictionary entries. |

## Language Models Begin with the Problem of Predicting the Next Word

A `language model` is a model that assigns probabilities to sentences or word sequences, or that computes the likelihood of the next word or token given previous context.

For example:

> I drink warm ___ in the morning

A person may think of candidates such as `coffee`, `tea`, `soup`, or `water`. A word such as `courtroom` is not grammatically impossible, but in an ordinary corpus it is less likely to fit the context.

A language model turns that intuition into a computational problem:

> P(coffee | I drink warm ...)  
> P(tea | I drink warm ...)  
> P(courtroom | I drink warm ...)

The important point is that a language model does not begin by declaring that it `understands meaning`. It begins by estimating which sequences are more plausible in observed language data and which next words are more likely.

## N-grams Approximate Probability Through Short Context

An `n-gram` is a sequence of n consecutive units. The units can be characters, words, or tokens. Here it is enough to think in terms of word n-grams.

> unigram: I  
> bigram: I / drink  
> trigram: I / drink / coffee

An `n-gram language model` estimates the next word not from the entire history, but from a short previous context. For example, a bigram model looks only at the immediately previous word.

> full context:  
> I drink warm ___ in the morning
>
> bigram approximation:  
> warm ___

Consider a tiny corpus:

> I drink coffee  
> I drink tea  
> I drink coffee every morning

If we count what follows `drink`, we get:

| Previous word | Next word | Count |
| --- | --- | ---: |
| drink | coffee | 2 |
| drink | tea | 1 |

Then a simple bigram probability can be thought of as:

```text
P(coffee | drink) = 2 / 3
P(tea | drink) = 1 / 3
```

This is a simplified teaching example, but the core idea is clear:

> instead of handling sentences only as lists of rules,  
> estimate the likelihood of the next word from frequencies observed in a corpus

## The Limits of N-grams Were Important Before LLMs

N-grams are intuitive and useful, but they have clear limits.

First, the context is short. A bigram sees only one previous word. A trigram sees only two previous words. Increasing n gives longer context, but the number of possible combinations grows quickly.

Second, `sparsity` appears. Real sentences are extremely varied. A word combination that never occurred in the training corpus can end up looking as if its probability were zero. That is why older language modeling needed tools such as smoothing, backoff, and interpolation.

Third, simple n-grams do not generalize well across similar words.

> the cat drinks milk  
> the dog drinks milk

A person can use the similarity between `cat` and `dog` to imagine related contexts. But a simple n-gram model does not automatically share that similarity. It mainly computes over observed string combinations.

These limits help explain why neural language models and embeddings became necessary.

## Distributed Representations Place Words in Vector Form

A `distributed representation` does not treat a word only as one isolated symbol. It represents the word as a vector made of many numeric values.

The simplest symbolic representation is `one-hot` encoding:

```text
Vocabulary:
[cat, dog, coffee, tea]

cat:
[1, 0, 0, 0]

dog:
[0, 1, 0, 0]
```

One-hot representation is good for distinguishing words, but it does not directly encode that `cat` is closer to `dog` than to `coffee`.

An `embedding` represents a word as a lower-dimensional dense vector:

```text
cat    -> [0.21, -0.08, 0.77, ...]
dog    -> [0.19, -0.05, 0.73, ...]
coffee -> [-0.44, 0.62, 0.10, ...]
```

The exact numbers do not need to be human-readable. The important point is that words used in similar contexts can be learned so that they lie close together in vector space.

> used in similar contexts  
> -> learned to have similar vector representations  
> -> the model can generalize across similar words

## Word2vec Made Embeddings Widely Visible

`word2vec` is one of the representative cases that made word embeddings widely known. Mikolov and colleagues proposed efficient ways to learn continuous vector representations from large corpora.

Two well-known forms are:

| Method | Intuition |
| --- | --- |
| CBOW | predict the center word from surrounding words |
| Skip-gram | predict surrounding words from the current word |

Suppose we have:

> I drink coffee in the morning

CBOW can be understood as using surrounding information such as `I`, `drink`, and `morning` to guess `coffee`. Skip-gram can be understood as using `coffee` to predict the surrounding words.

The important point is that the model is not directly given a dictionary definition of a word. It learns vector representations by looking at the contexts in which words appear together.

So the safer statement is not:

> people define the meaning of each word directly

but:

> the model looks at usage context  
> and learns a useful position for the word in vector space

## This Is Not a Break from Symbolic Units, but a Different Level

The relationship to `symbolic AI` needs to be handled carefully.

Embeddings do not erase symbols. Text is still divided into distinguishable units such as words, subwords, and tokens. These units are still identified in a vocabulary. The difference is that inside the model, the unit is not used only as a one-hot ID. It is transformed into a computable vector representation.

> symbol or token:  
> a distinguishable input unit
>
> embedding:  
> a representation that turns that unit into a computable vector

So the safer explanation is:

> LLMs did not simply replace symbolic AI.  
> They still distinguish symbolic units in text as tokens,  
> then transform those tokens into vector representations  
> and use them in probabilistic language modeling.

This connects back to the earlier discussions of `symbols`, `labels`, `features`, and `representations`. But an embedding is not a human-written meaning table. It is a learned numeric representation.

## The Connection to LLMs

Modern LLMs inherit both lines from this section:

| Earlier line | View that continues into LLMs |
| --- | --- |
| language modeling | compute a probability distribution over next-token candidates |
| the limits of n-grams | longer context and stronger generalization are needed |
| distributed representation | represent tokens as vectors for internal computation |
| embeddings | send input tokens into embedding space and then through many layers of computation |

Modern LLM embeddings, however, are not fully explained by static embeddings like word2vec. In Transformer-family models, `contextual representations` matter, because the representation changes with context. That returns in 11.3 and Part 5.

The connection to remember is:

> n-gram:  
> predict the next word from short-context counts
>
> neural language model:  
> learn word representations and next-word probabilities together
>
> embedding:  
> place words and tokens in vector space to improve generalization
>
> LLM:  
> use large data and neural-network structure  
> to compute next-token distributions over long context and generate outputs

## Checklist

- I can explain a language model as a model that handles probabilities of the next word or next token.
- I can explain that n-grams are based on short-context frequency.
- I can explain the limits of n-grams through sparsity, short context, and weak generalization across similar words.
- I can explain embeddings as a way to represent words and tokens as vectors.
- I can distinguish CBOW and Skip-gram at a very simple intuitive level.
- I can explain that embeddings are learned from data rather than being dictionary definitions.
- I can distinguish symbols and embeddings as representations at different levels rather than as direct replacements.
- I can place LLMs in the accumulated line of language modeling and distributed representation rather than treating them as suddenly appearing chatbots.
- I can explain the flow by separating next-word probability, short-context frequency approximation, and vector representation.

## Sources and Further Reading

- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, Chapter 3: N-gram Language Models](https://web.stanford.edu/~jurafsky/slp3/3.pdf){: target="_blank" rel="noopener noreferrer" }, draft of 2026-01-06, accessed 2026-06-23.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, Chapter 6: Neural Networks and Neural Language Models](https://web.stanford.edu/~jurafsky/slp3/6.pdf){: target="_blank" rel="noopener noreferrer" }, draft of 2026-01-06, accessed 2026-06-23.
- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
