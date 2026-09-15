# P2-4.5 Gradient Supplement: from School Differentiation to Multivariable Differentiation

> Section ID: `P2-4.5`
> Version: `v2026.09.15`

For a function of one variable, differentiation measures change along a single input axis. For several variables, the rate depends on the proportions in which the inputs change together. Traveling the same distance may increase or decrease the function value, and the effects of two inputs may cancel.

## Rates Along Axes and Diagonals

The following function calculates one number from two inputs.

\[
F(x,y)=3x+4y,\qquad \nabla F=[3,4]
\]

Changing `x` with `y` fixed gives rate 3; changing `y` with `x` fixed gives rate 4. These partial derivatives refer to the positive coordinate-axis directions. When both inputs change, we combine these components according to the direction of travel.

At the current position `[1,1]`, the function value is 7. Normalize direction vector `u=[u₁,u₂]` to length 1. Traveling distance `h` then changes the inputs by `[hu₁,hu₂]`. A unit vector prevents the distance from changing while we compare directions.

For a differentiable function, the instantaneous rate in direction `u` is the dot product of the gradient and `u`, called the **directional derivative**.

\[
D_{\mathbf u}F=\nabla F\cdot\mathbf u=3u_1+4u_2
\]

| Unit direction u | Position after traveling 0.1 | New value | Change | Directional derivative |
| --- | --- | --- | --- | --- |
| `[1,0]` | `[1.1,1]` | 7.3 | +0.3 | 3 |
| `[0,1]` | `[1,1.1]` | 7.4 | +0.4 | 4 |
| `[0.6,0.8]` | `[1.06,1.08]` | 7.5 | +0.5 | 5 |
| `[-0.6,-0.8]` | `[0.94,0.92]` | 6.5 | −0.5 | −5 |
| `[0.8,-0.6]` | `[1.08,0.94]` | 7 | 0 | 0 |

Because this function is linear, `change = directional derivative × distance` holds exactly even for a finite displacement. For a general curved function, it is an approximation for small displacements.

## When Two Input Changes Cancel

Direction `[0.8,-0.6]` has length `√(0.8²+(-0.6)²)=1`. In this direction, increasing `x` contributes `3×0.8=2.4`, while decreasing `y` contributes `4×(-0.6)=−2.4`, canceling each other. Neither partial derivative is zero, but the rate in this direction is zero.

![Contours of F=3x+4y with directions of increase, decrease, and no change at the current position.](/AiBook/assets/part-02/chapter-04/partial-vs-directional-derivative-en.svg)

A contour connects points with the same function value. Here, the straight line `3x+4y=7` passes through the current point. The green zero-rate direction follows this line, while the gradient direction crosses contours perpendicularly toward larger values.

Gradient `[3,4]` has length 5, so its unit direction is `[0.6,0.8]`. Among unit directions, this one has the largest instantaneous rate, 5. This comparison measures coordinate distance as `√(Δx²+Δy²)`.

## A Vector at One Point and a Vector Field

The gradient of `F=3x+4y` is `[3,4]` everywhere. For another function, however, it may vary by position. The following function lets us calculate this directly.

\[
L(x,y)=x^2+2y^2,\qquad \nabla L(x,y)=[2x,4y]
\]

| Position | Function value L | Gradient |
| --- | --- | --- |
| `[1,0]` | 1 | `[2,0]` |
| `[0,1]` | 2 | `[0,4]` |
| `[1,1]` | 3 | `[2,4]` |
| `[-1,1]` | 3 | `[-2,4]` |
| `[0,0]` | 0 | `[0,0]` |

A function assigning one number to each position in space is a **scalar field**. Placing the gradient of this scalar field `L` at each position produces a **vector field**. One gradient describes one position; a gradient vector field shows information at many positions together.

![Contours of L=x²+2y² and gradients at different positions. All arrows use the same scale factor.](/AiBook/assets/part-02/chapter-04/vector-calculus-context-en.svg)

Each arrow points in the direction of increasing function value at its point. All are shortened by the same factor, preserving lengths proportional to gradient magnitude; these are not the unit vectors used to compare directions. At the origin, the gradient is zero and has no direction arrow. The origin is this function’s minimum, but a zero gradient does not always mean a minimum in other functions.

## Zero Rate Versus Constant Value

At `[1,1]` in this function, the gradient is `[2,4]`. Direction `[2/√5,-1/√5]` has length 1 and dot product zero with the gradient. Its instantaneous rate is zero, but traveling straight in this direction does not preserve the function value exactly.

\[
L\left(1+\frac{2h}{\sqrt5},1-\frac{h}{\sqrt5}\right)
=3+\frac65h^2
\]

Traveling distance `h=0.1` raises the function value from 3 to 3.012. The quadratic term vanishes in the instantaneous rate but remains in a finite displacement. For the earlier linear function, contours were straight, so continuing straight in the canceling direction preserved the value. Here the contours are curved, so maintaining the same value requires following them while changing direction.

## Parameter Displacement and Loss Change

In a learning update, `−η∇L` is a **displacement in parameter space**. Reading it as the same thing as a diagonal arrow on a loss graph can confuse the axes. The one-variable loss `Q(w)=(w−3)²` makes the distinction clear.

At `w=4`, the derivative is 2. With learning rate 0.1, the update is `Δw=−0.1×2=−0.2`, giving new parameter 3.8. Loss falls from 1 to 0.64, so loss change `ΔQ=−0.36` differs from parameter change `Δw=−0.2`.

![Parameter w moves from 4 to 3.8 along its axis, while loss decreases from 1 to 0.64.](/AiBook/assets/part-02/chapter-04/gradient-descent-update-intuition-en.svg)

The horizontal arrow below shows the actual parameter displacement; the two points on the curve show loss before and after the update. The slope changes at the new position, so it must be recalculated before the next move. Repeated updates and learning-rate choices connect to the preceding section’s calculations.

## Exercise: Calculate Directions and Displacements

First, find the rate in direction `[-0.8,0.6]` for `F=3x+4y`. Second, start at `[-1,1]` in `L=x²+2y²` and calculate the position and loss after one update with learning rate 0.1. Third, check whether both parameters decreased in the second calculation.

??? note "Calculation and Explanation"
    The first rate is `3×(-0.8)+4×0.6=0`. In the second calculation the gradient is `[-2,4]`, giving `[-1,1]−0.1×[-2,4]=[-0.8,0.6]`. Loss falls from 3 to `0.8²+2×0.6²=1.36`. Since x increases and y decreases, descent does not mean making every coordinate numerically smaller.

## Checklist

- Can you connect coordinate-axis partial derivatives to a directional derivative in an arbitrary direction?
- Can you compare directions using equal travel distances?
- Can you use a dot product to identify a direction where input effects cancel?
- Can you distinguish a gradient at one point from a vector field across positions?
- Can you explain why zero instantaneous rate need not preserve a value over a finite displacement?
- Can you distinguish parameter change from loss change?

## Sources and References

- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }. Partial derivatives, directional derivatives, gradients, and contours. Checked: 2026-09-15. Function examples and coordinate-based diagrams are original constructions.
