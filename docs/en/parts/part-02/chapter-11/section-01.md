# P2-11.1 Building Vectors and Matrices with NumPy Arrays

> Section ID: `P2-11.1`
> Version: `v2026.07.09`

P2-11.1 introduces NumPy as the first practical array tool in Part 2's data-computation workflow. It reconnects vectors, matrices, `shape`, `ndim`, and `dtype` to the small model calculations that appear later in Part 3.

## Scope of This Section

This Section focuses on creating numeric arrays and reading their shapes. It does not cover advanced indexing, memory layout, or GPU execution.

## Central Question

Why does AI practice move from generic Python lists to NumPy arrays when the goal shifts from storing values to calculating with values?

![Python list and NumPy array use the plus sign differently](../../../assets/part-02/chapter-11/list-vs-numpy-array-en.svg)

![Feature matrix times weight vector produces one score per sample](../../../assets/part-02/chapter-11/feature-weight-shape-flow-en.svg)

## Perspective to Keep

- NumPy is a calculation-oriented numeric array library, not just another container.
- `shape`, `ndim`, and `dtype` should be checked before interpreting results.
- A one-dimensional array is often read as a vector, and a two-dimensional array as a matrix.
- Small examples such as `features @ weights` help connect formulas to runnable code.

## Short Check

- Can you explain why `list + list` and `array + array` may mean different operations?
- Can you explain what `shape`, `ndim`, and `dtype` tell you before any deeper analysis?
- Can you explain why a feature matrix and a weight vector are naturally read as arrays?

## Sources and References

- NumPy Developers, [The NumPy ndarray](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- NumPy Developers, [Array objects](https://numpy.org/doc/stable/reference/arrays.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
