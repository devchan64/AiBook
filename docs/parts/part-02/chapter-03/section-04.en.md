# P2-3.4 Dot Product, Norm, Distance, and Similarity

> Section ID: `P2-3.4`
> Version: `v2026.07.12`

Once we have read vectors, matrices, and matrix multiplication, the next question remains: `how similar are two vectors`, `how far apart are they`, and `how do we distinguish a large vector from a vector that only points in a similar direction`? Those questions lead directly to dot product, norm, distance, and similarity.

If matrix multiplication is `a calculation that combines vectors to create new values`, then dot product, distance, and similarity are `calculations that compare vectors`. So after building vectors, we also need to hold on to the standard by which those vectors will be read. When you want to recheck the terms quickly, also refer to the [concept glossary](/AiBook/reference/concept-glossary/).

## Scope of This Section

This section handles only the basic intuition of dot product, norm, distance, and similarity. It does not cover the formal proof of cosine similarity, concentration phenomena in high dimensions, or the implementation details of ANN search.

Here we focus on the following questions.

- How does the dot product summarize the relation between two vectors into one number?
- What does vector norm measure?
- Why are distance and similarity not the same thing?
- Why does this intuition lead into k-NN, embedding, and vector retrieval?

## Goals of This Section

- You can explain dot product as the value obtained by multiplying corresponding components of two vectors and adding them.
- You can read norm as a summary value of vector size or strength.
- You can distinguish distance as a standard for separation and similarity as a standard for resemblance.
- You can explain that the comparison standard changes depending on whether shared direction is important or whether absolute size is also important.
- You can gain the minimum comparison language needed to read k-NN, embeddings, and similarity search.

## One Scene to Hold First

The first scene to hold in this section is the comparison of several vectors under the same standard.

| Comparison target | What you notice first | Question to hold now |
| --- | --- | --- |
| `q = [1, 1]`, `a = [2, 2]` | same direction, larger size | does direction matter, or does size also matter? |
| `q = [1, 1]`, `b = [1, 0]` | one axis is missing, so it resembles less | are they close in coordinates, or only partly similar in use? |
| `q = [1, 1]`, `c = [10, 10]` | very far away, but almost the same direction | do distance and cosine similarity give different answers? |

So the core of this section is not simply `calculate a vector`, but first choose `what we are going to count as the same`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Dot product is a summary value that reads `how much two vectors move together` | Because it connects matrix multiplication and similarity calculation. | Read why we multiply matching positions and add them. |
| Norm and direction are not the same information | Because it helps us distinguish a large vector from a vector that only points in a similar direction. | Understand `size` and `direction` as different concepts. |
| Distance and similarity answer different questions | Because it keeps us from mixing k-NN and embedding retrieval into the same problem. | Read `how far apart are they` separately from `how similar are they`. |

## Dot Product Is a Calculation That Folds Two Vectors into One Number

The dot product multiplies matching positions and adds all the results, folding the relation between two vectors into one number.

\[
a \cdot b = a_1b_1 + a_2b_2 + \cdots + a_nb_n
\]

This calculation is useful when we want to summarize quickly `how much two vectors share the same directional components`. That is why it also connects naturally to the explanation of matrix multiplication, because one cell of a matrix product can ultimately be seen as the dot product of one row and one column.

Using the smallest example:

\[
[1,\ 2] \cdot [3,\ 4] = 1 \times 3 + 2 \times 4 = 11
\]

A large dot-product value does not always mean `good`. It is safer to read it as `a summary value that compresses the relation between two vectors into one number`. If many same-direction components overlap, the dot product can become large. If opposite components are strong, the value can become small or even negative.

If we summarize this one more time:

| Question | What dot product sees well |
| --- | --- |
| How much do the same-direction components overlap? | It sees this well |
| How large is the absolute distance difference? | It does not answer that directly |
| Does a longer vector receive a larger score? | That can happen |

## Norm Reads the Size of a Vector

Vector norm is a value that summarizes how far a vector is from the origin, or how large its overall strength is.

For a beginner, it is enough to hold first only the 2-norm that appears most often.

\[
||x|| = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}
\]

When the norm is large, the values are spread farther overall. When the norm is small, the vector lies closer to the origin.

For example:

\[
||[3,\ 4]|| = 5
\]

This can be read immediately through the 3-4-5 triangle. By contrast, `[30, 40]` has almost the same direction but a norm 10 times larger. Because of that difference, we must separate `vectors with similar direction but different size`.

This becomes clearer in a comparison table.

| Vector | Direction | Norm |
| --- | --- | --- |
| `[3, 4]` | reference direction | `5` |
| `[30, 40]` | almost the same direction | `50` |
| `[4, -3]` | different direction | `5` |

## Distance and Similarity Answer Different Questions

Distance and similarity are both comparison standards, but they do not answer the same question.

| Criterion | The first question it asks |
| --- | --- |
| distance | how far apart are they? |
| similarity | how much do they resemble each other? |

In distance-based reasoning, we often first think `the closer they are, the more likely they are similar`. By contrast, similarity asks more directly `do they point in the same direction` or `do they have similar use`.

So later:

- `k-NN` first looks at nearby cases under a distance standard.
- `embedding retrieval` first lifts candidates that are similar under a similarity standard.

Let us look at a small example.

\[
q = [1,\ 1],\quad a = [2,\ 2],\quad b = [1,\ 0]
\]

- `a` has almost the same direction as `q`, and is also longer.
- `b` has similar length but is missing one axis.

If the question is `which vector points in the most similar direction`, then `a` feels more natural. If the question is `which point is closest in coordinates`, the calculation can give another answer. So when reading a comparison problem, we first have to decide `what we are going to count as the same`.

Here is a question-to-criterion table that the reader can use immediately.

| Problem scene | Criterion to recall first |
| --- | --- |
| Choose the nearest sample | distance |
| Find the vector whose direction or meaning is most similar | similarity, cosine similarity |
| Understand why one cell of matrix multiplication is calculated that way | dot product |
| Look at the strength or size of a vector | norm |

## Why Cosine Similarity Needs to Be Separated Out

Cosine similarity is a comparison standard that emphasizes directional similarity more than magnitude. Even when two vectors point the same way, their absolute sizes can differ, so the question `which should matter more` changes with the problem.

For example:

- In a problem like purchase amount, the size itself can matter a lot.
- In a problem like sentence embeddings, directional similarity can matter more than size.

That is why cosine similarity keeps returning in vector retrieval and embedding contexts.

For example, `[1, 1]` and `[10, 10]` differ greatly in size but point in the same direction. Distance reads them as far apart, but cosine similarity judges them to have almost the same direction. By contrast, `[1, 1]` and `[1, -1]` may have similar norm, but their directions are very different. This is why we need to read `distance` and `directional similarity` separately.

If we leave only a very short comparison result:

| Comparison | Distance view | Direction-similarity view |
| --- | --- | --- |
| `[1, 1]` vs `[10, 10]` | far apart | very similar |
| `[1, 1]` vs `[1, -1]` | by length alone they may look similar | direction is very different |

## A Very Short Decision Standard

When you face a vector-comparison problem, it is enough to ask the following three questions first.

1. Does size matter too, or does only direction matter?
2. Are we looking for the nearest neighbor, or the most similar representation?
3. Are the vectors being compared placed in the same space and the same dimension?

Once these three questions are sorted out, it becomes much less confusing which of `distance`, `dot product`, and `cosine similarity` should come first.

## Checklist

- Can you explain dot product as `multiply matching positions and add`?
- Can you explain that norm and direction are different information?
- Can you distinguish distance and similarity in one sentence?
- Can you explain why `[1, 1]` and `[10, 10]` are read differently by distance and cosine similarity?
- Can you explain why k-NN and embedding retrieval are not the same comparison question?
- Can you ask first `does size matter too, or is direction more important?` when you face a vector-comparison problem?

## Scenes Where This Comparison Standard Reappears

| Scene encountered again later | Intuition to leave here first |
| --- | --- |
| k-NN in Part 4 | Saying “find nearby cases” means choosing a distance standard. |
| Embeddings in Part 6 | Saying “place meaning into vectors” means a vector-comparison standard is needed too. |
| Vector retrieval in Part 6 | Saying “rank relevant candidates first” means building a similarity order. |

So what matters here is not stopping at `make vectors`, but reading together `how those vectors will be compared`.

## Sources and References

- NumPy Developers, `numpy.dot`. Because it directly explains that for 1D arrays it is read as the inner product and for 2D arrays as matrix multiplication, it supports the dot-product intuition in this section. [https://numpy.org/doc/stable/reference/generated/numpy.dot.html](https://numpy.org/doc/stable/reference/generated/numpy.dot.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-08
- NumPy Developers, `numpy.linalg.norm`. Because it lets us directly check the basic meaning of vector norm and matrix norm, it supports the explanation in this section that reads norm as a summary value of size. [https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-08
- scikit-learn developers, `cosine_similarity`. Because it directly explains cosine similarity as a normalized dot product, it strengthens the explanation in this section that connects similarity and directional comparison. [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-08
