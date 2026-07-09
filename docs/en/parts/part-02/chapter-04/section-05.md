# P2-4.5 Gradient Supplement: From School Differentiation to Multivariable Differentiation

> Section ID: `P2-4.5`
> Version: `v2026.07.09`

P2-4.3 connected derivative, partial derivative, and gradient. P2-4.4 connected them to learning. This supplementary Section slows down the transition point that often feels unfamiliar.

## Scope of This Supplement

This Section is not the main representative explanation of gradient or gradient descent. Its purpose is to reduce the gap between one-variable school differentiation and multivariable learning explanations.

## Where the Gap Usually Appears

| School memory | Why it becomes confusing here | Expression to recover now |
| --- | --- | --- |
| `y = f(x)` one-variable function | several inputs create several local questions | multivariable function |
| one slope | loss responds to many parameters at once | collection of partial derivatives |
| tangent slope | axis directions and chosen directions were rarely separated | partial derivative, directional derivative |
| differentiation drill | learning cares more about movement direction | gradient, gradient descent |
| solving one problem | deep learning needs many gradients efficiently | backpropagation |

## Working Definitions

| Term | Working definition |
| --- | --- |
| derivative | change rate when one input changes a little |
| partial derivative | change rate for one chosen input among several |
| directional derivative | change rate along a chosen direction |
| gradient | ordered vector of several partial derivatives |
| vector calculus | larger mathematical language for vectors, functions, and change on spaces |
| gradient descent | repeated method that moves parameters toward lower loss |
| backpropagation | efficient procedure for computing gradients in deep models |

## One Midway Summary

| Stage | One-sentence summary |
| --- | --- |
| derivative | read local change for one input |
| partial derivative | split several inputs and inspect them one by one |
| directional derivative | inspect change along a chosen direction |
| gradient | gather partial derivatives into one vector |
| gradient descent | move using that vector toward lower loss |
| backpropagation | compute that vector efficiently in deep models |

![Flow from one derivative to several partial derivatives and a gradient](../../../assets/part-02/chapter-04/gradient-single-to-multiple-directions-en.svg)

![Partial derivative and directional derivative compared](../../../assets/part-02/chapter-04/partial-vs-directional-derivative-en.svg)

![Where the gradient sits in vector calculus](../../../assets/part-02/chapter-04/vector-calculus-context-en.svg)

![Gradient direction on a loss contour](../../../assets/part-02/chapter-04/gradient-direction-loss-contour-en.svg)

![Gradient descent as repeated small downhill steps](../../../assets/part-02/chapter-04/gradient-descent-steps-en.svg)

![Gradient descent update intuition](../../../assets/part-02/chapter-04/gradient-descent-update-intuition-en.svg)

![Backpropagation sends values forward and gradients backward](../../../assets/part-02/chapter-04/backpropagation-gradient-flow-en.svg)

## Perspective to Keep

- Gradient, gradient descent, and backpropagation are related but not identical.
- The unfamiliar part is often not “new math,” but one-variable intuition extended to several directions.
- It is enough here to separate role, not to master every derivation.

## Short Check

- Can you explain how the one-variable picture expands to several inputs?
- Can you explain the difference among gradient, gradient descent, and backpropagation?
- Can you explain why directional derivative is not the same thing as partial derivative?

## Sources and References

- OpenStax, [Calculus Volume 3](https://openstax.org/details/books/calculus-volume-3){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
