# P2-4.6 Composite Functions and the Chain Rule

> Section ID: `P2-4.6`
> Version: `v2026.07.09`

After derivatives, gradients, and gradient descent, one sentence keeps appearing: backpropagation uses the chain rule. This Section gives the minimum intuition needed to read that sentence properly.

## Scope of This Section

This Section introduces composite functions and the chain rule at an intuitive level. It does not derive full matrix-form chain rules or full backpropagation formulas.

## One Scene to Hold

| Step | Expression | Question to read now |
| --- | --- | --- |
| stage 1 | `y = 2x + 1` | if `x` changes a little, how much does `y` change? |
| stage 2 | `z = y^2` | if `y` changes, how much more does `z` change? |
| whole pipeline | `z = (2x + 1)^2` | how does change in `x` reach final result `z`? |

## Composite Functions Are Calculation Pipelines

A composite function can be read as several function stages connected in order. One stage's output becomes the next stage's input.

## The Chain Rule Is a Change-Transfer Rule

If change travels through several stages, we need a rule for following that change from earlier stages to the final result.

That is the entry-level role of the chain rule.

| Question | Reading |
| --- | --- |
| how sensitive is `x -> y`? | `dy/dx` |
| how sensitive is `y -> z`? | `dz/dy` |
| how sensitive is `x -> z` overall? | connect those stagewise changes |

## Why This Matters for Backpropagation

Neural networks are multi-stage calculation pipelines. Loss is produced at the end, but parameters live in earlier layers.

So when later explanations say:

- `loss -> layer -> parameter`
- backpropagation
- gradient flow

they are relying on this idea of stage-by-stage change transfer.

## Perspective to Keep

- Composite functions are staged computation structures.
- The chain rule connects local change across stages.
- Backpropagation is not the chain rule itself; it is a computation procedure that uses it.

## Short Check

- Can you explain a composite function as several stages joined together?
- Can you explain the chain rule as a way to follow change through those stages?
- Can you explain why this becomes necessary for backpropagation?

## Sources and References

- OpenStax, [Calculus Volume 1](https://openstax.org/details/books/calculus-volume-1){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
