# P2-3.4 Dot Product, Norm, Distance, and Similarity

> Section ID: `P2-3.4`
> Version: `v2026.09.14`

Suppose we want to find a similar buyer for someone who bought one cup of coffee and one cup of tea. Someone who bought two cups of each has the same purchase ratio, while someone who bought only one cup of coffee differs less in quantity. The choice depends on what we mean by similar.

Dot product, norm, distance, and similarity express these judgments numerically. Even with the same data, changing the comparison criterion can change the ranking of candidates.

## Purchase Quantities and Ratios

The first component of each vector is the number of cups of coffee purchased; the second is the number of cups of tea. All counts cover the same period.

| Buyer | Vector | Difference from the reference buyer |
| --- | --- | --- |
| Reference `q` | `[1, 1]` | One cup each of coffee and tea |
| `a` | `[2, 2]` | Twice as much of each drink |
| `b` | `[1, 0]` | The same amount of coffee, but no tea |
| `c` | `[10, 10]` | Ten times as much of each drink |

Both `a` and `c` have the same purchase ratio as `q`. On a coordinate plane, they lie in the same direction from the origin. The second component of `b` is zero, so its direction differs, but its purchase quantities differ from `q` by only one cup of tea.

## Dot Product: Multiply Components and Add

The dot product multiplies corresponding components of two vectors and adds the results. For real vectors with \(n\) components each, it is calculated as follows.

\[
x\cdot y=x_1y_1+x_2y_2+\cdots+x_ny_n
\]

For the purchase vectors, we multiply the coffee counts together, multiply the tea counts together, and add the two products.

\[
q\cdot a=1\times2+1\times2=4
\]

Likewise, `q·b = 1` and `q·c = 20`. Both `a` and `c` have the same purchase ratio as the reference buyer, but `c`, with larger quantities, has a larger dot product. **The dot product reflects magnitude as well as direction.** A larger dot product alone does not mean a more similar purchase ratio.

With negative components, the products can cancel each other out. For example, `[1, 1]·[1, -1] = 1−1 = 0`. Dot products also appear in matrix multiplication. Each entry of the result matrix in the previous section is the dot product of a row of the left matrix and a column of the right matrix.

## Norm: Distance from the Origin

A norm measures the length of a vector. The **2-norm** used here is the straight-line distance from the origin to the vector's endpoint. For two components, treating them as horizontal and vertical lengths lets us apply the Pythagorean theorem.

\[
\|x\|_2=\sqrt{x_1^2+x_2^2+\cdots+x_n^2}
\]

\[
\|q\|_2=\sqrt{1^2+1^2}=\sqrt2,\qquad
\|a\|_2=\sqrt{2^2+2^2}=2\sqrt2
\]

Since each component of `a` is twice the corresponding component of `q`, its length is also twice as large. The length of `c` is `10√2`, ten times that of `q`. Their directions match, but their lengths differ.

Do not confuse the 2-norm with the total number of cups purchased. The total for `q` is `1+1=2` cups, but its 2-norm is `√2`. A norm measures vector magnitude according to the chosen calculation rule.

## Distance: The Difference Between Two Points

Euclidean distance is the straight-line distance between the endpoints of two vectors. **Subtract corresponding components, then calculate the length of the difference vector.**

\[
d(q,a)=\|a-q\|_2
=\sqrt{(2-1)^2+(2-1)^2}=\sqrt2\approx1.414
\]

\[
d(q,b)=\sqrt{(1-1)^2+(0-1)^2}=1
\]

![Vectors q, a, and b drawn from the origin, with separate distance markers between endpoints. q and a share a direction, but b is closer to q.](/AiBook/assets/part-02/chapter-03/vector-distance-en.png)

Arrows from the origin show each buyer's vector. Red distance markers compare the endpoints. From `q` to `a`, the horizontal and vertical changes are both 1; from `q` to `b`, only the vertical coordinate changes by 1. Thus, **when purchase quantities are compared using this distance, `b` is closer.**

Measuring from the origin to an endpoint gives a vector's length. Measuring from one endpoint to another gives the distance between two vectors. The length calculation is the same; the positions being compared differ.

## Cosine Similarity: Divide Out Magnitude and Compare Direction

Cosine similarity is the dot product divided by the product of the two vector lengths. Both vectors must have nonzero length.

\[
\operatorname{cos\_sim}(q,a)
=\frac{q\cdot a}{\|q\|_2\|a\|_2}
=\frac{4}{\sqrt2\times2\sqrt2}=1
\]

Dividing each component by the vector's length preserves its direction and makes its length 1. This is called **normalizing to a unit vector**. Normalizing `q`, `a`, and `c` gives approximately `[0.707, 0.707]` in each case. Cosine similarity equals the dot product of these vectors after their magnitudes have been removed in this way.

\[
\frac{q}{\|q\|_2}=\left[\frac1{\sqrt2},\frac1{\sqrt2}\right]\approx[0.707,\ 0.707]
\]

![After normalization to length 1, q, a, and c coincide, while b lies on the horizontal axis. The angle between the directions is 45 degrees.](/AiBook/assets/part-02/chapter-03/vector-normalization-en.png)

Every point on the dashed circle is at distance 1 from the origin. The normalized vectors `q`, `a`, and `c` coincide and make an angle of 45 degrees with `b`. The cosine similarity of `q` and `b` is `1/(√2×1) ≈ 0.707`.

Cosine similarity is the cosine of the angle between two vectors. As the angle increases from 0° to 180°, the value decreases from `1` to `−1`. It is `1` for the same direction, `0` for perpendicular directions, and `−1` for opposite directions. For example, `[1, 1]` and `[1, -1]` are perpendicular, giving `0`; `[1, 1]` and `[-1, -1]` point in opposite directions, giving `−1`. Negative components do not represent purchase counts, but can occur in vectors representing other data.

The vector `[0, 0]` has zero length, so we cannot divide by its length or assign it a direction. Its cosine similarity is undefined under the formula above.

## How the Criterion Changes the Choice

| Compared with `q = [1, 1]` | Dot product | Euclidean distance | Cosine similarity |
| --- | --- | --- | --- |
| `a = [2, 2]` | `4` | About `1.414` | `1` |
| `b = [1, 0]` | `1` | `1` | About `0.707` |
| `c = [10, 10]` | `20` | About `12.728` | `1` |

Choosing the buyer with the closest quantities by distance gives `b`. Choosing the same purchase ratio by cosine similarity gives a tie between `a` and `c`. Choosing the largest dot product gives `c`, who purchased more. The three calculations answer different questions.

Here, the coordinates have defined meanings and units, so direction can be interpreted as a purchase ratio. To connect sentence-embedding directions with meaning, we need to check how the embedding model was trained and which comparison criterion it uses. Cosine similarity itself does not determine what a sentence means. With k-NN and vector search, too, we need to check both the vector representation and the comparison criterion.

Distance also depends on the units and scales of the components. If one component is a cup count and another is money spent, the larger monetary numbers may have a greater influence on distance. Making the entire vector's length 1 does not automatically resolve differences in component units.

## Exercise: Doubling the Quantities

Change `a = [2, 2]` to `a′ = [4, 4]`, keeping `q = [1, 1]` fixed. Before calculating, predict whether the dot product, distance to `q`, and cosine similarity increase or stay the same.

??? note "Calculation and explanation"
    The dot product increases from `4` to `8`. Distance increases from `√2` to `√(3²+3²)=3√2`. Cosine similarity remains `8/(√2×4√2)=1`. The purchase quantities increased, but their ratio did not change.

## Checklist

- Can you use the calculations for `a` and `c` to explain how magnitude affects the dot product?
- Can you distinguish where a vector's length and the distance between two vectors are measured from?
- Can you calculate Euclidean distance from component differences?
- Can you explain why quantity comparison selects `b`, while ratio comparison selects `a` and `c`?
- Can you see in the diagram that normalization makes the length 1 while preserving direction?
- Can you explain why the cosine similarity formula cannot be applied to a zero-length vector?

## Sources and References

- NumPy Developers, `numpy.dot`. The documentation explicitly describes the inner product for one-dimensional arrays and matrix multiplication for two-dimensional arrays, supporting the dot-product explanation here. [numpy.dot](https://numpy.org/doc/stable/reference/generated/numpy.dot.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-19
- NumPy Developers, `numpy.linalg.norm`. The documentation explains vector and matrix norms, supporting the interpretation of a norm as a measure of magnitude. [numpy.linalg.norm](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-19
- scikit-learn developers, `cosine_similarity`. The documentation defines cosine similarity as a normalized dot product, supporting its connection to direction comparison. [cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-09-08