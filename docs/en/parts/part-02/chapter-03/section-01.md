# P2-3.1 Scalars, Vectors, and Matrices

> Section ID: `P2-3.1`
> Version: `v2026.07.07`

Chapter 2 reread mathematical notation as a language for calculation. Now the question changes: when AI data is arranged into a calculable form, what shape are we looking at?

This Section fixes three basic shapes first.

1. A single number
2. An ordered list of values
3. A table with rows and columns

Those three become the basic language of linear algebra: scalar, vector, and matrix. The goal here is not full theory. The goal is to recognize what an AI document means when it writes one value, one list, or one table.

## Scope of This Section

This Section introduces `scalar`, `vector`, `matrix`, `shape`, and `array` at an entry level. It does not cover proofs, determinants, eigenvalues, or the full formal definition of vector spaces.

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| scalar | one number | single values such as loss, probability, or learning rate |
| vector | ordered list of values | one object described by several features |
| matrix | table of numbers with rows and columns | many samples or many vectors handled together |
| shape | size information of an array | first clue about which calculations are allowed |
| array | structure that stores numbers in order | meeting point of formulas and code |

## What to Keep

- A scalar reads one value.
- A vector reads one object through several values.
- A matrix gathers several vectors into one table.
- `shape` often matters before the exact values do.

## Why This Comes First

Later Sections keep asking questions such as:

- What is the shape of input `X`?
- How many rows are samples?
- How many columns are features?
- Why does one multiplication work but another fail?

Those questions become much easier once scalar, vector, matrix, and shape are stable in your head.

## Scalar: One Number

A scalar is the simplest case. It is one number.

- A probability score like `0.92`
- A loss value like `0.31`
- A learning rate like `0.001`

All of these are scalar values. They may have different meanings, but their shape is the same: one number.

## Vector: An Ordered List

A vector is an ordered list of values. Order matters.

For example, one customer might be described by:

\[
[age,\ clicks,\ purchases]
\]

That list is not just several unrelated numbers. It is one object described through several coordinates or features.

## Matrix: A Table of Several Vectors

If one customer becomes one vector, then many customers can be stacked into a matrix.

\[
\begin{bmatrix}
25 & 3 & 1 \\
31 & 7 & 0 \\
22 & 2 & 4
\end{bmatrix}
\]

Rows and columns do not carry meaning by themselves. The problem decides the meaning. In many AI examples, rows are samples and columns are features.

## Shape Decides the Calculation Conditions

`shape` tells us how long a vector is, or how many rows and columns a matrix has. That is why shape is often the first thing to inspect in code.

- scalar: one value
- vector: length `n`
- matrix: `rows x columns`

The same numbers rearranged into another shape can change which operation is valid.

## One Short Scene

If one customer is a vector, many customers are a matrix. If one prediction score is a scalar, several prediction scores form a vector. This is why linear algebra is not separate from AI data handling. It is the language that tells us how data is arranged before a model computes with it.

## Perspective to Keep

- Scalars, vectors, and matrices are not decorative vocabulary. They describe data shape.
- A vector is one object with several values.
- A matrix is several vectors placed together.
- Shape is a calculation rule, not a cosmetic label.

## Short Check

- Can you explain a scalar as one number?
- Can you explain a vector as an ordered list of values?
- Can you explain a matrix as several vectors placed in one table?
- Can you explain why `shape` matters before running a calculation?

## Sources and References

- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
