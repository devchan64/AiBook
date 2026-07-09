# P2-11.2 Indexing, Slicing, and Axis

> Section ID: `P2-11.2`
> Version: `v2026.07.09`

P2-11.1 created arrays and checked `shape`. This Section moves to reading inside the array: choosing one position, keeping a range, and deciding the direction of a calculation.

## Scope of This Section

This Section introduces basic indexing, slicing, and `axis` reading in one- and two-dimensional arrays.

## Central Question

How do indexing, slicing, and axis answer different questions about the same array?

![Slice notation selects a range from start to stop before the stop position](../../../assets/part-02/chapter-11/slice-start-stop-step-en.svg)

![Indexing, slicing, and axis read different parts of the same array](../../../assets/part-02/chapter-11/index-slice-axis-map-en.svg)

![Axis controls the direction of reduction](../../../assets/part-02/chapter-11/axis-reduction-en.svg)

![Rows often represent samples and columns often represent features](../../../assets/part-02/chapter-11/dataset-row-column-selection-en.svg)

## Perspective to Keep

- Indexing chooses one precise position.
- Slicing keeps a range instead of a single value.
- `axis=0` and `axis=1` describe the direction of reduction, not just screen direction.
- In dataset-style reading, rows often mean samples and columns often mean features.

## Short Check

- Can you explain the difference between `x[1, 2]`, `x[1, :]`, and `x[:, 2]`?
- Can you explain why `sum(axis=0)` and `sum(axis=1)` leave different result shapes?
- Can you explain why row/column reading becomes important before model training examples?

## Sources and References

- NumPy Developers, [Indexing on ndarrays](https://numpy.org/doc/stable/user/basics.indexing.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
