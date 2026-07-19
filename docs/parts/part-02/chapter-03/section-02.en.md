# P2-3.2 Vector Space and the Intuition of Position

> Section ID: `P2-3.2`
> Version: `v2026.07.19`

In P2-3.1, we looked at scalar, vector, and matrix from the perspective of data shape. Now we extend the vector a little beyond a simple list of values. In AI documents, a vector is often explained as if it were `a position inside some space`.

1. A vector is a list of values.
2. That list can be read as an expression like coordinates.
3. So it can also be seen as a position whose nearness and farness can be compared.

Here the focus is on understanding why vectors appear in the language of `position` and `distance` in explanations of embedding, feature, similarity, and search.

Here we reorganize `vector space`, `dimension`, `position`, `distance`, and `similarity`. If 3.1 read a vector as a list of values, now we reorganize how that vector is compared inside the same space.

If we continue the flow from P2-3.1, it becomes the following.

1. A scalar expresses one value.
2. A vector expresses one object through several values.
3. A matrix gathers the vectors of several objects.
4. A vector space lets us place and compare those vectors under the same standard.

So the core of P2-3.2 is not stopping at `we made a vector`, but thinking about `where those vectors are placed and how close they are to one another`.

Here we focus less on the full formal mathematical definition of vector space and more on reading vectors as positions in AI documents. Once the intuition of position, dimension, and nearness is stable, we can reread `why we search for nearby vectors` as calculation language when we later meet embedding retrieval or RAG.

## A Shared Comparison Scene to Hold First

In Chapter 3, we repeatedly use the following three small vectors.

\[
\mathbf{a} = [2,\ 3]
\]

\[
\mathbf{b} = [2.2,\ 3.1]
\]

\[
\mathbf{c} = [8,\ 1]
\]

These three vectors form a shared scene that continues into later sections.

- `a` and `b` are candidates for positions that are close to each other.
- `a` and `c` are candidates for positions that are farther apart.
- In `P2-3.4`, this example can be brought back again to compare distance, similarity, and dot product.
- In `P2-3.6`, the same vectors can be turned into code arrays to check shape and calculation.

So the goal of this section is to stop treating a vector as only `a list of numbers` and to make it readable as `a position compared inside the same space`.

If we place them on a coordinate plot like the one below, it becomes immediately visible why `a` and `b` are read as the first nearby candidates while `c` is read as farther away. At this point in the section, that level of positional intuition is enough.

![Coordinate plot where a and b are close in vector space and c is farther away](/AiBook/assets/part-02/chapter-03/vector-space-near-far-en.svg)

| What to fix in this section now | Question that follows immediately | Where it reappears later |
| --- | --- | --- |
| Why vectors are read like positions | In P2-3.3, we examine how matrix multiplication creates a new representation. | It becomes a foundation when rereading embedding, similarity search, and RAG from Part 1. |
| The intuition that comparison works only inside the same space | In P2-3.6, we check shape and calculation rules in code. | It returns when reading feature space, clustering, and distance-based intuition in Part 3. |
| The interpretation that nearness is a candidate for similarity | It continues into later sections through NumPy and data examples. | It reappears in Part 6 `P6-11.1` on vector databases and `P6-11.2` on indexes and retrieval quality. |

## Goals of This Section

- You can explain a vector as both a list of values and an expression that can be read like coordinates.
- You can explain vector space as the intuition of a calculable space in which vectors are placed.
- You can understand dimension as the number of values in a vector or the number of coordinate axes.
- You can explain the intuition that nearby vectors can represent similar data or meaning.
- You can understand that an embedding is a representation that turns text or items into positions in vector space.
- You can explain why this intuition returns in similarity search, RAG, recommendation, and classification.
- You can lightly explain the meaning of vector addition and scalar multiplication as the basic operations of vector space.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Read a vector like a position | Because explanations of embedding and representation learning frequently use the language of coordinates, positions, and space. | Understand that each component can play the role of a coordinate, so a vector can be compared like one point. |
| Nearness is a candidate for similarity | Because it explains why similarity search and recommendation look for nearby vectors. | Understand that nearby vectors can have similar features or similar meaning. |
| Compare only inside the same space | Because if dimension and shape differ, distance or similarity cannot be calculated directly. | Understand that only vectors with the same length and the same rules are compared together. |

## Read a Vector Like a Position

In P2-3.1, we treated a vector as an ordered list of values.

\[
\mathbf{x} = [2,\ 3]
\]

This vector is a list with two values. At the same time, it can also be read like the coordinates of one point in a two-dimensional plane. In that case, the first value can be read as horizontal position and the second as vertical position.

So \([2,\ 3]\) can be read like `the position reached by moving 2 horizontally and 3 vertically`. This explanation does not capture the full meaning of every vector mathematically, but in an introduction to AI it gives the basic intuition of reading a vector like a position.

Let us place the vectors from the shared scene again.

\[
\mathbf{a} = [2,\ 3]
\]

\[
\mathbf{b} = [2.2,\ 3.1]
\]

\[
\mathbf{c} = [8,\ 1]
\]

\(\mathbf{a}\) and \(\mathbf{b}\) have similar numbers. So if we place them in the same space, we can expect them to lie near each other. By contrast, \(\mathbf{c}\) has a very different pattern of numbers from \(\mathbf{a}\), so it may lie farther away.

This is the first intuition for reading a vector like a position.

If the numbers of vectors are similar, they may be close in space, and that nearness can be interpreted as the possibility that the data’s features or meanings are similar.

The important point here is not yet to prove fully `why` they are close, but to notice that `a comparison question appears`. That question leads into distance and similarity calculations in later sections.

Of course, this does not mean `if the numbers are similar, the meaning is always similar`. It depends on how the values were made to carry meaning, how they were learned, and what distance or similarity standard is being used.

## Vector Space Is a Calculable Place Where Vectors Are Placed

Strictly defined, a vector space is a mathematical structure that satisfies several conditions. Here it is enough to read it as a place where vectors are arranged under the same rules, can be compared with each other, and support calculations such as addition or scaling.

For example, the following vectors all have two values.

\[
[1,\ 2],\quad [3,\ 4],\quad [0,\ -1]
\]

They can be placed in the same two-dimensional space. By contrast, a vector with three values can be seen as an expression in three-dimensional space.

\[
[1,\ 2,\ 3]
\]

The important point is that comparison must happen inside the same space. A vector with two values and a vector with three values are difficult to compare directly in the same way.

[1, 2] and [1, 2, 3] have different lengths, so it is hard to apply the same position comparison or distance calculation directly.

This also connects to the shape problem in code. The intuition of vector space ultimately gives the sense that `comparison happens inside the same rules and the same shape`.

## The Minimum Mathematical Rules of Vector Space

To define vector space strictly, we would need to handle several axioms. We do not prove the full set here. Instead, there are two calculations a beginner should know first.

- vectors can be added to each other
- a number can be multiplied into a vector

The first is vector addition.

\[
[1,\ 2] + [3,\ 4] = [4,\ 6]
\]

The second is scalar multiplication. Here, scalar means one number.

\[
2[1,\ 2] = [2,\ 4]
\]

These two calculations matter because they let us create new vectors. For example, we can add two vectors or make one vector a little larger or smaller.

\[
0.5[2,\ 4] = [1,\ 2]
\]

The way of creating a new vector by multiplying vectors by numbers and then adding them is called a linear combination.

\[
2\mathbf{a} + 3\mathbf{b}
\]

This expression means doubling vector \(\mathbf{a}\), tripling vector \(\mathbf{b}\), and then adding them. There is no need to memorize the formula deeply right now. What matters is that a vector space is not only `a place where vectors sit`, but also a calculation structure where vectors can be added, rescaled, and used to create new representations.

This perspective becomes important later in AI contexts.

For example, calculations that multiply an input vector by weights, add several values to form a new representation, and adjust that vector representation little by little are all explained on top of this perspective.

Still, we do not calculate linear combinations and matrix multiplication in detail here. It is enough to remember vector space as `a space of representations where addition and scalar multiplication are possible`.

Returning to the shared scene, we can do more than compare `a` and `b`. We can also create a new representation such as `a + b`, or change the size as in `2a`. So a vector space is both a place of comparison and a place of calculation for constructing new vectors.

## Read Dimension First as the Number of Axes or the Number of Values

Here, dimension is read as the number of values a vector has.

\[
[2,\ 3]
\]

This vector has two values, so it can be read as a two-dimensional vector.

\[
[0.1,\ 0.7,\ -0.2,\ 1.5]
\]

This vector has four values, so it can be read as a four-dimensional vector.

In everyday life, it is easy to imagine two or three dimensions as drawings. But in AI, vectors with hundreds or thousands of dimensions appear often. For example, a text embedding can represent one sentence or one word as a vector made of many numbers.

One sentence can pass through an embedding model and be represented as a vector with hundreds or thousands of numbers.

It is hard for a person to visualize that many dimensions directly. Even so, the basic intuition stays the same: each dimension can be used like one coordinate of the representation, the whole vector can be compared like one position, and nearness or farness can serve as a clue for reading the relation between pieces of data.

Still, we should not conclude that every dimension has a meaning a person can interpret directly. In a learned embedding, each number may not have a clear name attached by humans.

## Nearness Becomes a Candidate for Similarity

In vector space, vectors that lie near each other can correspond to similar data. This is the core intuition of embedding and vector search.

For a simple example, imagine product vectors with only two features.

Here we treat the first value as price level and the second value as weight.

\[
\mathbf{p}_1 = [3,\ 2]
\]

\[
\mathbf{p}_2 = [3.1,\ 2.2]
\]

\[
\mathbf{p}_3 = [9,\ 8]
\]

\(\mathbf{p}_1\) and \(\mathbf{p}_2\) have similar price level and weight. So there is a strong chance that these two are nearby vectors. \(\mathbf{p}_3\) may lie farther away from both.

This kind of intuition is used often in recommendation, search, and classification. In the end, it leads to questions about finding similar users, similar documents, similar images, or similar products.

But nearness is a candidate, not the final answer. We still have to verify what standard defines nearness, how the vectors were learned from the data, and whether nearness is actually useful for the real problem.

This matters because in `P2-3.4`, even with the same vectors, we ask different questions through `distance`, `norm`, `direction`, and `cosine similarity`. For now, `close` is only the starting question, and in later sections we narrow down `what it means to be close and in what way`.

## Position and Topology Are Not the Same Word

The position discussed here is an introductory expression that places a vector like coordinates and lets us think about nearness and farness. By contrast, topology is a broader and more abstract concept in mathematics. Rather than simply talking about the coordinates of one point, topology is related to how points are close to one another, how structures are connected, and how properties such as continuity are viewed.

Even in AI documents, phrases such as `the topology of the space`, `data manifold`, or `the structure of representation space` may appear. These expressions do not mean that we are only looking at one vector’s coordinates. They are closer to asking about the overall connected structure and relations formed by all the data representations together.

Still, we do not study topology here. For now, distinguish them only at the following level: position is where one vector sits in the space, distance is a value that tells how close two vectors are, and topology is a more abstract perspective for looking at structure, closeness, connection, and continuity in a space.

So in P2-3.2, we first fix the intuition of position and nearness, and remember topology only as `an expression that may appear when talking about deeper mathematical structure`.

Here we first fix the intuition of position and nearness, without going into proofs of vector-space axioms or the full development of distance formulas and cosine similarity calculations. Shape and array calculation return in P2-3.6, and more concrete retrieval use returns in Part 6.

## Embedding Is a Way of Placing Data in Vector Space

An embedding is a representation that turns objects such as text, images, products, or users into vectors. In Part 1, we saw the big picture of embedding. Here we reread it as a mathematical expression.

An object passes through an embedding model, changes into a vector, and the result is handled like one position inside vector space.

For example, suppose one sentence is represented by the following vector.

\[
\mathbf{e} = [0.12,\ -0.03,\ 0.88,\ 0.41]
\]

It is hard to say that each number of this vector has a word meaning that a person can read directly. But the whole vector can still be used as a representation of that sentence.

Once this representation is placed in vector space, it can be compared with other sentence vectors.

If the vectors of sentence A, sentence B, and sentence C are placed in the same space, we can compare which sentence lies closer to which.

This intuition leads into similarity search and RAG. But we do not implement a retrieval system here. We only fix the point that `embedding creates comparable vector representations`.

## Connection Seen Through Related Academic Sources

The explanation in this section is not only a simple metaphor. In research on representation learning and word vectors, the relationship between data representation and vector space is treated as an important theme.

The review on representation learning by Bengio, Courville, and Vincent explains that the success of machine learning algorithms depends heavily on data representation. It also presents the geometric connection among representation learning, density estimation, and manifold learning as an important question. This supports the perspective that `a vector representation is not only a list of numbers, but can be a representation that reveals data structure`.

The word2vec paper by Mikolov, Chen, Corrado, and Dean learned continuous vector representations of words from large text data and evaluated their quality through word similarity tasks. This shows an important flow in modern NLP: even symbolic objects such as words can be turned into representations in vector space, and the closeness among those vectors can be compared.

We do not explain the detailed models of those two sources here. We only use them as grounding for the connection from scalar, vector, matrix, and position thinking into embedding and representation learning.

## Reading Order When You See the Phrase Vector Space

When the expression vector space appears, read it in the following order.

1. What has been represented as a vector?
2. How many dimensions does the vector have?
3. Are we comparing only vectors inside the same space?
4. By what standard is nearness being calculated?
5. What meaning does that nearness have in the actual problem?

For example, the phrase `search the document embedding vectors` can be unpacked as follows: documents are turned into vectors by an embedding model, those document vectors are stored in the same space, the query is also turned into a vector, nearby document vectors are found relative to the query vector, and those nearby documents are used as candidates.

This explanation connects to the RAG discussion in Part 1. In Part 2, we restore the intuition of vector space that lies underneath it.

## Why Vector Space Feels Difficult

Vector space feels difficult because two or three dimensions can be imagined as drawings, but high dimensions are hard to picture, and the number in each dimension does not always correspond one-to-one with a human-assigned meaning.

So here we do not try to imagine high-dimensional space as an exact picture. Instead, we keep the intuition that vectors are numeric representations made under the same rules, vectors in the same space can be compared, nearby vectors can be candidates for similarity, and that similarity must still be verified.

This intuition continues directly into embedding, vector search, recommendation, and clustering.

## Looking Through a Case

### Case 1. Why Similar Sentences Are Explained as Vectors in Nearby Positions

When a learner first hears the phrase `sentences are close in vector space`, it can be hard to imagine how a sentence becomes a position. People read sentences through words and meaning, but an embedding model changes a sentence into several numbers and represents it like one position in the same space.

For example, `The delivery is late` and `When will it arrive?` can describe similar situations even though the words are not exactly the same. If such sentences are placed as nearby vectors in embedding space, the system can find candidates with similar meaning more easily.

This case shows why we need to see vectors as more than simple lists of numbers. Even if a person cannot explain the individual meaning of each coordinate directly, the positional relation of the whole vector can become a clue for similarity and difference.

So the intuition of vector space lies less in `there are many numbers` and more in `the representations are comparable inside the same space`. With that intuition, explanations of embedding, similarity search, recommendation, and RAG are all read on the same map.

## Checklist

- Can you explain a vector as both a list of values and an expression that can be read like coordinates?
- Can you explain vector space as a calculable place where vectors are placed and compared?
- Can you explain dimension as the number of values in a vector or the number of coordinate axes?
- Can you explain that nearby vectors can be candidates for similarity, but are not automatically the answer?
- Can you distinguish position, distance, and topology instead of mixing them as the same word?
- Can you explain that embedding is a way of turning objects into representations inside vector space?
- Can you explain why the intuition of vector space returns in similarity search, RAG, recommendation, and clustering?
- Can you lightly explain vector addition, scalar multiplication, and linear combination as the basic calculations of vector space?
- Can you explain that embedding and similarity search require the condition of the same space and the same dimension?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012, checked 2026-07-19.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, checked 2026-07-19.
- Google for Developers, [Embeddings: Embedding space and static embeddings](https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, checked on 2026-07-19. This official educational reference explains embeddings as vector representations and nearby positions in embedding space.
- Google for Developers, [Measuring similarity from embeddings](https://developers.google.com/machine-learning/clustering/dnn-clustering/supervised-similarity){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, checked on 2026-07-19. This reference supports the connection between embedding-vector similarity and distance, cosine, or dot-product measures.
