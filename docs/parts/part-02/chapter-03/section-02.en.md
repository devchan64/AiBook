# P2-3.2 Vector Space and the Intuition of Position

> Section ID: `P2-3.2`
> Version: `v2026.09.08`

Using each component as a coordinate lets us place a vector as a point in space. Vectors expressed using the same coordinate system can be compared by position and distance.

## Positions of Three Vectors

Place the following three vectors on a two-dimensional plane.

\[
\mathbf{a} = [2,\ 3]
\]

\[
\mathbf{b} = [2.2,\ 3.1]
\]

\[
\mathbf{c} = [8,\ 1]
\]

Moving from `a` to `b` changes the first coordinate by `0.2` and the second by `0.1`. Moving from `a` to `c` changes them by `6` and `−2`, respectively. The coordinate plot also shows that `a` and `b` are close, while `c` is farther away.

![Coordinate plot where a and b are close in vector space and c is farther away](/AiBook/assets/part-02/chapter-03/vector-space-near-far-en.svg)

## Conditions for Comparing Positions

| Criterion | Why it matters |
| --- | --- |
| Read a vector like a position | Because explanations of embedding and representation learning frequently use the language of coordinates, positions, and space. |
| Nearness is a candidate for similarity | Because it explains why similarity search and recommendation look for nearby vectors. |
| Compare only inside the same space | Because if dimension and shape differ, distance or similarity cannot be calculated directly. |

## Vectors and Coordinates

A vector with two values can be read as two coordinates.

\[
\mathbf{x} = [2,\ 3]
\]

This vector is a list with two values. At the same time, it can also be read like the coordinates of one point in a two-dimensional plane. In that case, the first value can be read as horizontal position and the second as vertical position.

So \([2,\ 3]\) can be read as the position reached by moving 2 horizontally and 3 vertically.

Of course, this does not mean `if the numbers are similar, the meaning is always similar`. It depends on how the values were made to carry meaning, how they were learned, and what distance or similarity standard is being used.

## The Same Space and Dimensions

In a vector space, vector addition and scalar multiplication follow defined rules. To compare coordinate vectors, their component counts and the basis for each coordinate must also match.

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

## Addition, Scalar Multiplication, and Linear Combinations

The basic operations of a vector space are addition and scalar multiplication.

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

This expression means doubling vector \(\mathbf{a}\), tripling vector \(\mathbf{b}\), and adding the results.

For example, calculations that multiply an input vector by weights, add several values to form a new representation, and adjust that vector representation little by little are all explained on top of this perspective.

Returning to the shared scene, we can do more than compare `a` and `b`. We can also create a new representation such as `a + b`, or change the size as in `2a`. So a vector space is both a place of comparison and a place of calculation for constructing new vectors.

## Coordinate Count and Higher Dimensions

For the coordinate vectors below, the number of components corresponds to the dimension of the space.

\[
[2,\ 3]
\]

This vector has two values, so it can be read as a two-dimensional vector.

\[
[0.1,\ 0.7,\ -0.2,\ 1.5]
\]

This vector has four values, so it can be read as a four-dimensional vector.

In everyday life, it is easy to imagine two or three dimensions as drawings. But in AI, vectors with hundreds or thousands of dimensions appear often. For example, a text embedding can represent one sentence or one word as a vector made of many numbers.

It is hard for a person to visualize that many dimensions directly. Even so, the basic intuition stays the same: each dimension can be used like one coordinate of the representation, the whole vector can be compared like one position, and nearness or farness can serve as a clue for reading the relation between pieces of data.

Still, we should not conclude that every dimension has a meaning a person can interpret directly. In a learned embedding, each number may not have a clear name attached by humans.

## Nearness and Similarity

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

## Position and Topology

The position discussed here is an introductory expression that places a vector like coordinates and lets us think about nearness and farness. By contrast, topology is a broader and more abstract concept in mathematics. Rather than simply talking about the coordinates of one point, topology is related to how points are close to one another, how structures are connected, and how properties such as continuity are viewed.

Even in AI documents, phrases such as `the topology of the space`, `data manifold`, or `the structure of representation space` may appear. These expressions do not mean that we are only looking at one vector’s coordinates. They are closer to asking about the overall connected structure and relations formed by all the data representations together.

## Embeddings and Document Retrieval

An embedding is a representation that turns objects such as text, images, products, or users into vectors.

An object passes through an embedding model, changes into a vector, and the result is handled like one position inside vector space.

For example, suppose one sentence is represented by the following vector.

\[
\mathbf{e} = [0.12,\ -0.03,\ 0.88,\ 0.41]
\]

It is hard to say that each number of this vector has a word meaning that a person can read directly. But the whole vector can still be used as a representation of that sentence.

Once this representation is placed in vector space, it can be compared with other sentence vectors.

If the vectors of sentence A, sentence B, and sentence C are placed in the same space, we can compare which sentence lies closer to which.

In document retrieval, queries and documents are vectorized with the same embedding model. Document vectors close to the query vector are retrieved, and the resulting documents serve as candidate sources for answering the query.

## Research on Representation Learning and Word Vectors

Research on representation learning and word vectors also treats the relationship between data representation and vector space as an important topic.

The review on representation learning by Bengio, Courville, and Vincent explains that the success of machine learning algorithms depends heavily on data representation. It also presents the geometric connection among representation learning, density estimation, and manifold learning as an important question. This supports the perspective that `a vector representation is not only a list of numbers, but can be a representation that reveals data structure`.

The word2vec paper by Mikolov, Chen, Corrado, and Dean learned continuous vector representations of words from large text data and evaluated their quality through word similarity tasks. This shows an important flow in modern NLP: even symbolic objects such as words can be turned into representations in vector space, and the closeness among those vectors can be compared.

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
- Can you connect a vector as a list of values to the perspective of position and nearness?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012, checked 2026-07-19.
- Tomas Mikolov, Kai Chen, Greg Corrado, Jeffrey Dean, [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, checked 2026-07-19.
- Google for Developers, [Embeddings: Embedding space and static embeddings](https://developers.google.com/machine-learning/crash-course/embeddings/embedding-space){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, checked on 2026-07-19. This official educational reference explains embeddings as vector representations and nearby positions in embedding space.
- Google for Developers, [Measuring similarity from embeddings](https://developers.google.com/machine-learning/clustering/dnn-clustering/supervised-similarity){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, checked on 2026-07-19. This reference supports the connection between embedding-vector similarity and distance, cosine, or dot-product measures.
