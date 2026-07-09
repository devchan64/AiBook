# P2-11.3 Broadcasting and Vectorization

> Section ID: `P2-11.3`
> Version: `v2026.07.09`

P2-11.3 explains why array-wide computation often works without explicit `for` loops. The entry point is small: a scalar added to an array, then a row-shaped vector applied across a matrix.

## Scope of This Section

This Section introduces the basic intuition of broadcasting and vectorized array computation. It does not go deep into `reshape`, `np.newaxis`, or performance benchmarking.

## Central Question

How can one small value or one small vector be applied across a larger array, and what does that have to do with `shape` compatibility?

![A scalar is applied across an array by broadcasting](../../../assets/part-02/chapter-11/broadcast-scalar-array-en.svg)

![A row-shaped vector is broadcast across each row of a feature matrix](../../../assets/part-02/chapter-11/broadcast-row-vector-en.svg)

## Perspective to Keep

- Broadcasting is about compatible shapes, not visual similarity.
- Vectorization means expressing repeated work as an array operation.
- `shape` should be checked before assuming a broadcast will work.
- Feature-wise normalization and repeated offset application are common AI examples of this pattern.

## Short Check

- Can you explain why `scores + 10` changes every element even without a visible loop?
- Can you explain why `(4, 3) + (3,)` is easier to read than `(4, 3) + (4,)`?
- Can you explain why broadcasting is convenient but still needs shape discipline?

## Sources and References

- NumPy Developers, [Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
