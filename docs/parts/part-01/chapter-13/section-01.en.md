# P1-13.1 What It Means to Represent Text as Vectors

> Section ID: `P1-13.1`
> Version: `v2026.07.12`

Chapter 12 explained how prompts give task conditions to an LLM and why prompts alone cannot guarantee `factuality`, `evidence`, or `recency`. That leads to the next question:

> how can an LLM find external material to refer to?

To move toward that question, we first need to understand how text is turned into a computable form. The starting point is the `embedding`.

> an embedding is a way of turning text into a vector representation that the model can compute over

The key caution is that an embedding is not `meaning itself`. It is a numeric representation produced from how text was used in data and from the learning objective of the model.

Part 1 introduces the basic distinctions among `embeddings`, `vectors`, `vector space`, `sentence/paragraph/document embeddings`, and `embedding versus prompt` here. Section 11.1 already covered the historical background of embeddings in the line of language modeling, and Chapter 12 organized how prompts specify input conditions. This section connects those two flows from a service perspective and explains:

> why do we first turn text into vectors before trying to retrieve external material?

## Scope of This Section

Section 11.1 already covered language models, n-grams, distributed representations, and word2vec as part of the historical flow. This section does not repeat that history.

`Embeddings`, `vectors`, `vector space`, `sentence embeddings`, and `document embeddings` belong to different levels of representation. Their roles can first be separated like this:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| embedding | a way of turning text into a computable vector | the starting point of Chapter 13 |
| vector | a representation made of many numbers | the basic unit for understanding embedding output |
| vector space | the comparison space in which vectors are placed | the frame for reading closeness and distance |
| sentence/paragraph/document embedding | vector representations of longer text units | the practical units used for retrieval and RAG |
| embedding vs prompt | the distinction between search representation and task-specification input | a core boundary in the service flow later in Part 1 |

The baseline distinctions here are:

- embeddings are vector representations
- vector space is a comparison space
- prompts and embeddings have different roles

This section focuses on the role of embeddings in modern AI service flow:

| Topic | Question in this section |
| --- | --- |
| text representation | why turn sentences and documents into numeric vectors? |
| vector space | what does it mean to place text like coordinates? |
| limits of embeddings | why is it risky to treat vectors as if they were meaning itself? |

How similarity is actually calculated, and how close vectors are retrieved, is covered in P1-13.2. How retrieved results are connected back into LLM input through `RAG` is covered in P1-13.3. This section focuses only on the stage before search:

> representation transformation

## Goal of This Section

- Understand embeddings as a way of turning text into vector representations.
- Understand vectors as computable representations made of many numbers.
- Understand vector space as a space where text can be placed for comparison.
- Distinguish the level of math and probability needed for a first understanding of embeddings.
- Distinguish embeddings as learned representations rather than as meaning itself.
- Prepare to move into similarity search in P1-13.2.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| embeddings are representations that turn text into computable vectors | This is the basic premise for later vector search and RAG. | It is enough to understand them as expressions that turn sentences into something like numeric coordinates. |
| nearby positions can reflect similar usage context | This gives the first intuition of vector space. | It is enough to understand that vectors encode similarity of use, not meaning itself as a perfect object. |
| embeddings are not meaning itself, but numeric representations for computation | This reduces the mistake of equating vectors directly with human meaning. | It is enough to understand them as learned numeric tools for handling meaning-related tasks. |

## Computers Do Not Compare Sentences the Way People Do

A person may feel that these two sentences are similar:

> AI helps automate repetitive work.  
> Artificial intelligence can be used to reduce repeated tasks.

The wording is not identical. `AI` and `artificial intelligence`, `repetitive work` and `repeated tasks`, `helps automate` and `can be used to reduce` are different expressions, but the overall meaning is close.

Simple string comparison does not capture this relation well.

> string comparison:  
> how many characters or exact words match?
>
> embedding-based comparison:  
> how close are the texts inside the learned representation space?

Embeddings make the second question possible. Once text is turned into numeric vectors, a model or search system can compute distance between those vectors.

## A Vector Is a Representation Made of Many Numbers

A `vector` is a value made up of many numbers. Here it is enough to understand it as something like a coordinate representation.

```text
Sentence A -> [0.12, -0.44, 0.87, ...]
Sentence B -> [0.10, -0.40, 0.81, ...]
Sentence C -> [-0.72, 0.15, 0.03, ...]
```

Real embedding vectors may contain hundreds or even thousands of numbers. People do not need to interpret each number directly. The important point is:

> text:  
> the human-readable expression
>
> vector:  
> the representation used by the model or search system for computation

Once text is converted this way, different texts can be compared computationally. A system can estimate which document is close to a question or which sentences discuss similar topics.

This can sound mathematically intimidating, but understanding P1-13.1 does not require prior mastery of linear algebra or probability formulas.

| Knowledge | Level needed here |
| --- | --- |
| vector | the intuition that it is a representation made of many numbers |
| dimension | the intuition that the representation has many numeric slots |
| distance | the intuition that two representations can be near or far |
| probability | the intuition that models learn patterns from data |

The actual math becomes more important later when similarity measures such as dot products or cosine similarity are introduced. For now, the key flow is simpler:

> turn text into a multi-number position  
> then use those positions to find nearby text

## Embeddings Place Text in Vector Space

`Vector space` is the space in which vectors are placed. It is not easy to draw in the way we draw a 2D map, but the intuition is similar.

> nearby positions:  
> texts the model represents similarly
>
> distant positions:  
> texts the model represents differently

Consider:

| Sentence | Intuitive topic |
| --- | --- |
| AI can help summarize documents. | AI use |
| LLMs can shorten long documents into summaries. | AI use |
| The taste of coffee beans changes with roast level. | coffee |

If the embedding model is well suited to the task, the first two sentences are more likely to be placed closer together than either is to the coffee sentence.

The wording `more likely` matters. An embedding is not an absolute map of meaning. Its quality depends on the data, the training objective, the language, and the domain in which it is used.

## Words, Sentences, and Documents Can All Become Vectors

Section 11.1 focused mainly on `word embeddings`. But in real services, sentences, paragraphs, and documents can also be represented as vectors.

| Unit | Example | Use |
| --- | --- | --- |
| word | `artificial intelligence` | word relations, language-model input |
| token | a subword or token fragment | the internal input unit of an LLM |
| sentence | `AI can help summarize documents.` | semantic search, duplicate detection |
| paragraph | a multi-sentence explanation | document retrieval, question answering |
| document | a long article or file | classification, candidate generation for retrieval |

A long document can be embedded as one vector, but retrieval systems often split documents into smaller `chunks`. That helps them retrieve the part that is directly related to the user’s question.

> long document  
> -> split into smaller chunks  
> -> convert each chunk into an embedding vector  
> -> compare the question vector against those chunk vectors

How to chunk a document is not trivial. If chunks are too small, context becomes thin. If chunks are too large, unrelated content gets mixed together. That issue returns in P1-13.3 and again in later sections dealing with retrieval and generation.

## An Embedding Is Not Meaning Itself

One of the most important cautions about embeddings is this:

> misunderstanding:  
> an embedding stores the true meaning of a sentence perfectly in numbers
>
> safer explanation:  
> an embedding is a learned vector representation of text,  
> produced according to the model’s training criteria

Embeddings are useful, but they have limits.

| Limit | Explanation |
| --- | --- |
| context loss | one short vector cannot always contain the full meaning of a long document |
| polysemy | the same word can shift meaning across contexts |
| domain mismatch | a general-purpose embedding may be weak in a specialized field |
| language differences | quality may change across Korean, English, or mixed-language cases |
| recency | the embedding itself does not guarantee current factual validity |

So embeddings are better treated not as `meaning understood completely`, but as `representations useful for search and comparison`.

## Prompts and Embeddings Have Different Roles

`Prompts` deliver the current task conditions to the LLM. `Embeddings` turn text into vectors so that comparison and retrieval become possible.

| Item | Role |
| --- | --- |
| prompt | gives the model instructions, context, examples, and constraints |
| embedding | turns text into vectors for search and comparison |

Suppose a user asks:

> what are the limits of prompts?

If only the prompt is used, the LLM answers from its training and the current conversation context. But if the answer should rely on a specific part of this book, the relevant document first has to be found. That is where embeddings can be used.

> question text  
> -> question embedding  
> -> compare against document-chunk embeddings  
> -> select nearby chunks as candidates  
> -> place those selected chunks into LLM input

That is the flow that leads into P1-13.2 and P1-13.3.

## Checklist

- I can explain embeddings as a way of turning text into vector representations.
- I can explain vectors as computable representations made of many numbers.
- I can explain vector space as a comparison space for text.
- I can explain that words, tokens, sentences, paragraphs, and documents can all be embedding targets.
- I can explain that embeddings are learned representations rather than meaning itself.
- I can explain the role difference between prompts and embeddings.
- I can describe the flow that leads into similarity search in P1-13.2.
- I can explain why questions and documents should be compared through computable representations rather than raw strings.
- I can distinguish `turn text into vectors`, `compare those vectors`, and `keep prompts for task conditions`.

## Sources and Further Reading

- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, Chapter 6: Neural Networks and Neural Language Models](https://web.stanford.edu/~jurafsky/slp3/6.pdf){: target="_blank" rel="noopener noreferrer" }, draft of 2026-01-06, accessed 2026-06-23.
- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
