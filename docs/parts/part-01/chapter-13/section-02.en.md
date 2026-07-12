# P1-13.2 The Intuition of Similarity Search

> Section ID: `P1-13.2`
> Version: `v2026.07.12`

Section P1-13.1 explained what it means to represent text as `vectors`. Once text is turned into vectors, sentences, paragraphs, and documents can be placed as computable positions.

The next question is:

> among those vectorized texts, what are we trying to find?

`Similarity search` is one answer to that question.

> similarity search is the process of finding document vectors that are close to a query vector,  
> then selecting them as candidates that are likely to be relevant

The key point is not `finding the answer`, but `finding candidate passages that may be relevant`.

Part 1 introduces the basic distinctions among `similarity search`, `similarity`, `distance`, `cosine similarity`, `nearest neighbor`, and `top-k` here. Section 13.1 explained why text is first turned into vectors. This section explains:

> how are those vectors compared to choose candidates?

The connection to `RAG` continues in 13.3.

## Scope of This Section

This section explains the intuition of similarity search. Implementation structures such as `vector databases`, `indexes`, and `approximate nearest neighbor` methods are not discussed in detail here. They return in P1-13.4 as the intuition for why separate fast-retrieval structures become necessary.

These terms belong to different comparison criteria and result-selection methods. Their roles can first be separated like this:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| similarity search | the process of finding vector candidates close to a query | the second stage of Chapter 13 |
| similarity | the criterion of how alike two vectors are | one axis of comparison |
| distance | the criterion of how far apart two vectors are | the other axis of comparison |
| cosine similarity | a measure of how similar vector directions are | a common intuition in text retrieval |
| nearest neighbor | the closest candidate | the basic idea for selecting search results |
| top-k | returning several nearby candidates rather than only one | the method used to choose multiple candidates for later input |

The baseline distinctions are simple: similarity means likeness, distance means closeness or separation, and top-k means multiple candidates.

This section does not require prior knowledge of graphs. Graphs return later in the implementation section. For now, the focus stays on comparing vectors, choosing nearby candidates, and remembering that candidates are not yet guaranteed answers. It also does not explain how search results are inserted into prompts. That belongs to the next section on RAG. The emphasis here is that candidate retrieval is different from answer verification.

| Topic | Question in this section |
| --- | --- |
| similarity | how do we judge that two vectors are similar? |
| distance | how do we judge that two vectors are far apart? |
| nearest neighbor | how do we choose the closest candidate? |
| limit | why is a nearby vector not always a good answer? |

## Goal of This Section

- Understand similarity search as the process of finding nearby vector candidates.
- Understand similarity and distance as comparison criteria.
- Understand cosine similarity as a question of directional similarity rather than as a formula to memorize.
- Distinguish retrieved results as candidates rather than final answers.
- Prepare to move into the RAG flow in P1-13.3.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| similarity asks not whether two expressions are identical, but how close they are | This shows the difference between keyword matching and vector retrieval. | It is enough to understand it as a way of finding nearby expressions even when wording differs. |
| distance and direction can both matter in vector comparison | This makes it clear that vector comparison is not just string matching. | It is enough to understand that vector spaces can be compared by closeness and by directional alignment. |
| high similarity does not automatically mean the correct answer | This prevents overtrust in retrieval results. | It is enough to know that retrieved passages are related candidates, not guaranteed verified answers. |

## Search Means Finding Candidates Close to the Question

Recall the flow from P1-13.1:

> question text  
> -> question embedding  
> -> compare with document-chunk embeddings  
> -> select nearby chunks as candidates

Suppose a user asks:

> why can prompts not guarantee factuality?

A document store may contain chunks such as:

| Document chunk | Topic |
| --- | --- |
| P1-12.1 What does a prompt specify? | the role of prompts |
| P1-12.3 The limits and evaluation of prompts | factuality, evidence, evaluation |
| P1-13.1 What it means to represent text as vectors | embeddings |
| P1-9.1 Image recognition and representation learning | the spread of deep learning |

Similarity search turns the question and each document chunk into vectors, then finds which chunk is closest to the question vector. In this case, it is natural that the chunk from P1-12.3 would rank near the top.

But this is not `answer verification`. Search is only the stage of choosing candidate passages that are likely to be relevant.

## Similarity and Distance Are Comparison Criteria

`Similarity` is a way of judging how alike two vectors are. `Distance` is a way of judging how far apart they are.

At this level, the intuition is:

> high similarity:  
> the vectors are positioned or oriented in similar ways
>
> short distance:  
> the vectors are close
>
> low similarity or long distance:  
> the vectors are less related

These are often two ways of looking at the same comparison task.

| Expression | Intuition |
| --- | --- |
| high similarity | similar |
| short distance | close |
| nearest neighbor | the closest candidate |

Without any formulas, the key idea is still understandable:

> the system compares the question vector with document vectors  
> then orders candidates from closer to farther

## Cosine Similarity Looks at Directional Similarity

One term that often appears in text-embedding retrieval is `cosine similarity`. The formula does not need to come first here.

The useful intuition is:

> cosine similarity measures how much two vectors point in a similar direction

If vectors are imagined as arrows:

> similar direction:  
> the question and the document may be talking about related themes
>
> different direction:  
> the question and the document may be about different themes

Word2vec-style research also used cosine-style notions to inspect nearby words in vector space. Here the only intuition needed is:

> in vector space, we can look for expressions whose directions are close

Cosine similarity is useful, but it is not an absolute standard. Results still depend on which embedding model is used, how text was chunked, and what domain the data belongs to.

## Top-k Means Choosing Several Candidates

Retrieval systems usually do not choose only one result. They often return multiple nearby candidates. This can be described as `top-k` retrieval.

> top-1:  
> return the single closest candidate
>
> top-3:  
> return the three closest candidates
>
> top-k:  
> return the k closest candidates

Suppose the question is:

> do I need a lot of math to understand embeddings?

The candidate list may look like:

| Rank | Candidate | Why it may appear |
| ---: | --- | --- |
| 1 | P1-13.1 What it means to represent text as vectors | directly discusses embeddings and the level of math needed |
| 2 | P1-11.1 Statistical language models and embeddings | gives the historical background of embeddings |
| 3 | P1-13.2 The intuition of similarity search | explains vectors and comparison |

A larger top-k may reduce the chance of missing useful supporting material, but it can also bring in more irrelevant passages.

> top-k too small:  
> useful evidence may be missed
>
> top-k too large:  
> noise and irrelevant passages may enter

## A Nearby Vector Is Not Always a Good Answer

The most important limit of similarity search is this:

> a nearby vector is only a related candidate;  
> it does not guarantee answer quality or evidence quality

The following problems are possible:

| Problem | Explanation |
| --- | --- |
| similar wording but wrong answer | the same words may appear, but the actual intent can differ |
| outdated information | a nearby chunk may still be old |
| wrong document | the retrieved document itself may contain mistakes |
| chunking problem | the necessary context may be spread across neighboring chunks |
| domain mismatch | a general embedding model may be weak on a specialized domain |

For example, a question about `prompt evaluation` might retrieve passages about `model evaluation`, `test evaluation`, or `education evaluation` because of overlapping words. But the required context here is specifically the limits and review criteria of LLM prompts.

That is why retrieval results still need review:

> does the retrieved result actually fit the question?  
> is the source reliable?  
> is the source current?  
> does the chunk contain enough context?

## Retrieval Quality Depends on Input Preparation

Similarity search is not only about the embedding model. It also depends on how the searchable documents are prepared.

| Preparation factor | Effect |
| --- | --- |
| chunk size | too small leads to lost context, too large adds noise |
| title and metadata | can reveal the topic of the chunk more clearly |
| duplicate documents | similar candidates may repeat unnecessarily |
| outdated documents | can still be retrieved even when no longer appropriate |
| mixed languages | Korean-English variation can affect retrieval quality |

Documents organized by one central question per section can actually help retrieval. Each chunk tends to answer a relatively clear question. By contrast, if many chapters are mixed in one long file, it becomes harder to isolate the relevant part.

## Similarity Search Is Different from Keyword Search

`Similarity search` is not the same thing as `keyword search`.

| Search type | What it looks at |
| --- | --- |
| keyword search | whether the same word or phrase appears |
| similarity search | whether the vector representations are close |

Even if a document never contains the word `hallucination`, it may still describe `unsupported generation`, `plausible error`, or `confabulation`. Similarity search can still retrieve it as a candidate. The reverse is also possible: the exact same keyword may appear in a passage that is not actually relevant to the user’s intent.

Real systems sometimes combine keyword and similarity search, but this section does not go into that comparison. The key point is simpler:

> vector retrieval finds candidates by a different criterion from literal string matching

## Checklist

- I can explain similarity search as the process of finding nearby vector candidates.
- I can explain similarity and distance as comparison criteria.
- I can explain cosine similarity as directional similarity.
- I can explain top-k retrieval as returning several nearby candidates.
- I can explain that nearby vectors do not guarantee answer quality or evidence quality.
- I can explain that chunk size and metadata can affect retrieval quality.
- I can explain the difference between keyword search and similarity search.
- I can explain what it means for a question and a document to be `close` when they are compared.
- I can explain that a retrieved document is only a relevant candidate and does not guarantee the correct answer.

## Sources and Further Reading

- Yoshua Bengio, Rejean Ducharme, Pascal Vincent, Christian Jauvin, [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-06-23.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
- Tomas Mikolov, Ilya Sutskever, Kai Chen, Greg Corrado, Jeffrey Dean, [Distributed Representations of Words and Phrases and their Compositionality](https://arxiv.org/abs/1310.4546){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-06-23.
