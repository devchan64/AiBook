# P2-4.3 Derivative and Gradient

> Section ID: `P2-4.3`
> Version: `v2026.07.09`

P2-4.2 treated rate of change and slope as the bridge. This Section carries that bridge into two later terms that appear constantly in AI writing: `derivative` and `gradient`.

## Scope of This Section

This Section distinguishes derivative, derivative function, partial derivative, gradient, and nabla at an entry level.

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| derivative | instantaneous rate of change for one input | starting point |
| derivative function | function that gives derivative values by point | must be separated from one-point derivative |
| partial derivative | change rate with respect to one chosen input | basic tool for multivariable functions |
| gradient | vector collecting several partial derivatives | central concept for learning |
| nabla | notation often used for gradients | makes formulas less unfamiliar |

## One Input, One Local Change Question

For a one-variable function, the derivative reads how much output changes when the input changes a little near one point.

## Several Inputs Need Partial Derivatives

If a function depends on several inputs, one question is not enough. We ask how the output changes when we vary one input while holding the others fixed.

That is why partial derivatives appear.

## A Gradient Collects Several Partial Derivatives

When several partial derivatives are arranged in order, they form a gradient vector.

This is useful because model learning usually has many parameters. We do not need only one local change signal. We need many of them at once.

## Why Gradient Feels New

The school-memory version of differentiation is often “one function, one input, one slope.” AI learning expands the same idea into many input directions.

## One Practical Reading

When you see a gradient in AI writing, a helpful first reading is:

“This vector summarizes how the loss changes along several parameter directions.”

## Perspective to Keep

- Derivative is one-input local change.
- Partial derivative isolates one input inside a multivariable function.
- Gradient gathers those directional change rates into one vector.

## Short Check

- Can you explain derivative as one-input local change?
- Can you explain why partial derivatives are needed for several inputs?
- Can you explain a gradient as an ordered collection of partial derivatives?
- Can you explain why gradients appear repeatedly in model learning?

## Sources and References

- OpenStax, [Calculus Volume 3](https://openstax.org/details/books/calculus-volume-3){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- NumPy Developers, [Gradient and array routines overview](https://numpy.org/doc/stable/reference/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
