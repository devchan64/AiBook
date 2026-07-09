# P2-3.4 Dot Product, Norm, Distance, and Similarity

> Section ID: `P2-3.4`
> Version: `v2026.07.09`

After vectors and matrix multiplication, another question appears immediately: how do we compare vectors?

This is where `dot product`, `norm`, `distance`, and `similarity` enter. They are not the same thing, and later AI topics become easier once those questions are kept separate.

## Scope of This Section

This Section introduces comparison intuition only. It does not attempt full proofs of cosine similarity or high-dimensional geometry.

## One Scene to Hold

| Comparison | First thing you notice | Question to keep |
| --- | --- | --- |
| `q = [1, 1]`, `a = [2, 2]` | same direction, larger size | does direction matter, or size too? |
| `q = [1, 1]`, `b = [1, 0]` | one axis is missing | are they close, or just partly aligned? |
| `q = [1, 1]`, `c = [10, 10]` | very far but almost same direction | can distance and cosine similarity disagree? |

## Dot Product Folds Two Vectors into One Number

The dot product multiplies matching coordinates and adds them. It is useful when we want one summary score about how two vectors line up.

It does not directly answer every comparison question. In particular, it can mix together direction and size.

## Norm Reads Vector Size

The norm tells us the size or magnitude of a vector.

Two vectors may point in a similar direction but still have very different norms. That is why “large,” “close,” and “similar” should not be collapsed into one word.

## Distance and Similarity Answer Different Questions

| Criterion | First question it answers |
| --- | --- |
| distance | how far apart are they? |
| similarity | how alike are they? |

In k-NN style reasoning, distance often comes first. In embedding retrieval, similarity often comes first.

## Why Cosine Similarity Is Often Separated Out

Cosine similarity is useful when direction matters more than absolute size. A pair such as `[1, 1]` and `[10, 10]` can be far apart in distance but very similar in direction.

## Perspective to Keep

- Dot product gives one summary number.
- Norm reads size.
- Distance and similarity are different comparison questions.
- Cosine similarity becomes useful when direction matters more than scale.

## Short Check

- Can you explain the dot product as multiply-and-add across matching positions?
- Can you explain why norm is not the same thing as similarity?
- Can you explain why distance and similarity may lead to different answers?
- Can you explain why cosine similarity is useful in embedding comparisons?

## Sources and References

- NumPy Developers, [Linear algebra on n-dimensional arrays](https://numpy.org/doc/stable/reference/routines.linalg.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- scikit-learn Developers, [Pairwise metrics](https://scikit-learn.org/stable/modules/metrics.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
