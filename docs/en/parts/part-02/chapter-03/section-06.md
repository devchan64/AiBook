# P2-3.6 Checking Linear Algebra with NumPy

> Section ID: `P2-3.6`
> Version: `v2026.07.09`

Now the same linear algebra ideas can be checked in code. The goal is not to memorize NumPy syntax in isolation. The goal is to see how vector and matrix notation appears in arrays, shapes, and outputs.

## Scope of This Section

This Section uses NumPy to check vectors, matrices, `shape`, element-wise multiplication, and matrix multiplication. It is not a full NumPy tutorial.

## Concept Mapping to Keep

| Code scene | Earlier concept being checked | What to inspect first |
| --- | --- | --- |
| creating vectors and matrices | P2-3.1 shapes | does the shape appear as expected? |
| comparing vectors | P2-3.2 position intuition | are the vectors in the same space? |
| `a + b`, `2 * a` | basic vector operations | how do those operations look in code? |
| `*` vs `@` | P2-3.3 multiplication distinction | element-wise or matrix product? |
| batch matrix computation | many vectors handled together | how do input and output shapes change? |

## Why NumPy Helps Here

NumPy gives a direct bridge:

- formula notation
- array notation
- printed output

That makes it easier to see that the math and the code are describing the same structure.

## Three Habits to Keep

- check `.shape` before reading the exact values
- separate `*` from `@`
- read batch calculations as matrix-level operations, not only one-sample operations

## What to Confirm in Practice

- one vector can be created as an array
- several vectors can be stacked into a matrix
- `*` keeps position-by-position multiplication
- `@` performs matrix multiplication
- shape mismatches explain many common beginner errors

The example file for this Section is [p2_3_6_numpy_linear_algebra.py](../../../assets/part-02/chapter-03/p2_3_6_numpy_linear_algebra.py).

## Perspective to Keep

- NumPy makes the array structure visible.
- Shape often explains the calculation before the numbers do.
- `*` and `@` should not be mixed.
- Batch computation is one reason matrices appear everywhere in AI code.

## Short Check

- Can you explain why `.shape` should be checked early?
- Can you explain the difference between `*` and `@`?
- Can you explain why a matrix can represent several samples at once?
- Can you explain why NumPy is useful for recovering linear algebra intuition?

## Sources and References

- NumPy Developers, [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- NumPy Developers, [Array creation routines](https://numpy.org/doc/stable/reference/routines.array-creation.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
