# P2-3.3 What Does Matrix Multiplication Reuse?

> Section ID: `P2-3.3`
> Version: `v2026.07.09`

Matrix multiplication often looks like a mysterious advanced operation. In AI reading, a more useful entry point is this: matrix multiplication reuses the same weighted-sum pattern many times.

## Scope of This Section

This Section introduces `matrix multiplication`, `weighted sum`, `weight matrix`, `linear transformation`, and `input/output dimension`. It does not aim for full symbolic mastery.

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| matrix multiplication | combining rows and columns to create new values | core computation here |
| weighted sum | inputs multiplied by weights and then added | smallest unit behind one output |
| weight matrix | table of weights for several outputs | changes one representation into another |
| linear transformation | vector-to-vector change by a matrix | interpretation frame for matrix multiplication |
| input/output dimension | lengths of input and output | explains why shape matters |

## Element-wise Multiplication Is Different

Matrix multiplication is not the same thing as multiplying values position by position.

- element-wise multiplication: same positions multiply each other
- matrix multiplication: one output combines several inputs through multiply-and-add structure

That difference becomes important when you later read neural-network layers or linear classifiers.

## One Output Comes from a Weighted Sum

Suppose input is:

\[
x = [x_1, x_2, x_3]
\]

One output can be made as:

\[
y_1 = w_{11}x_1 + w_{12}x_2 + w_{13}x_3
\]

That is a weighted sum. Matrix multiplication becomes useful because the same pattern is reused for many outputs.

## A Matrix Reuses the Same Pattern for Many Outputs

Instead of writing each weighted sum separately, a weight matrix stores them together. Then one multiplication can produce several outputs at once.

![Matrix multiplication changes a vector's position](../../../assets/part-02/chapter-03/matrix-multiplication-position-change-en.svg)

This is why a matrix can be read as a rule that transforms one vector into another representation.

## Shape Decides Whether the Calculation Is Allowed

The inside dimensions must match. Otherwise we do not know which input values should pair with which weights.

That is why matrix multiplication questions often become shape questions first.

## Matrix Multiplication Also Handles Many Inputs Together

If one vector is one sample, then many samples can be stacked into a matrix. The same weight matrix can then be applied to all of them in batch form.

That is one of the reasons matrix notation is so common in AI explanations and code.

## Perspective to Keep

- Matrix multiplication is reused weighted-sum computation.
- It is not the same as element-wise multiplication.
- A weight matrix changes an input representation into a new one.
- Shape tells us whether the computation is even possible.

## Short Check

- Can you explain why matrix multiplication is not position-by-position multiplication?
- Can you explain a weighted sum as the smallest unit behind one output?
- Can you explain why matrix multiplication is described as representation change?
- Can you explain why shape matters before the exact numbers?

## Sources and References

- NumPy Developers, [Array objects](https://numpy.org/doc/stable/reference/arrays.ndarray.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- Gilbert Strang, *Introduction to Linear Algebra*, Wellesley-Cambridge Press.
