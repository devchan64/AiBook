# P2-4.5 Gradient Supplement: from School Differentiation to Multivariable Differentiation

> Section ID: `P2-4.5`
> Version: `v2026.09.08`

In a one-variable function, we find the slope with respect to one input. With several inputs, the rate of change depends on which input changes or in what proportions inputs change together. Partial derivatives describe rates along coordinate axes; a directional derivative describes the rate along a chosen direction.

## The Slope of a One-Variable Function

When we think of school-level differentiation, we usually remember `y = f(x)`, the slope of a tangent line, instantaneous rate of change, derivative at a point, derivative function, and speed and acceleration.

Most of this flow starts from a function with one input.

\[
y = f(x)
\]

Then the question is relatively simple. It asks `if x changes a little, how much does y change?`

So the rate of change is also easy to understand as one direction. It is like seeing how much the height changes when we move a little forward on a line.

In other words, one input \(x\) corresponds to one output \(y\), and the intuition of reading the slope at one point of that relationship was the starting point of school-level differentiation.

The chart below shows the flow by which one-direction differentiation expands into partial derivatives in many directions and then into a gradient.

![Flow that expands one-variable differentiation into partial derivatives and a gradient in many directions](/AiBook/assets/part-02/chapter-04/gradient-single-to-multiple-directions-en.svg)

## Multiple Inputs and a Vector of Rates

A multivariable function takes several inputs.

\[
z = f(x, y)
\]

Now the questions increase to more than one, such as `if x changes a little, how does z change?` and `if y changes a little, how does z change?`

If we look together at the rate of change in the \(x\)-direction and the rate of change in the \(y\)-direction, it becomes a vector that bundles the two values.

## Partial Derivatives Along Coordinate Axes

Let us look at one multivariable function.

\[
L(w_1, w_2)
\]

In the AI context, we may think of \(L\) as loss and of \(w_1\) and \(w_2\) as parameters.

Looking at how \(L\) changes when only \(w_1\) is changed a little is the partial derivative with respect to \(w_1\).

\[
\frac{\partial L}{\partial w_1}
\]

Looking at how \(L\) changes when only \(w_2\) is changed a little is the partial derivative with respect to \(w_2\).

\[
\frac{\partial L}{\partial w_2}
\]

When calculating a partial derivative, hold the other inputs fixed. For the partial derivative with respect to `w_1`, keep `w_2` unchanged, and vice versa.

## Rate of Change Along a Chosen Direction

Partial derivatives usually look at axis directions one by one. The reference directions are fixed, such as the \(w_1\)-direction and the \(w_2\)-direction.

A directional derivative asks a slightly more general question.

It asks how much the function value changes per unit distance along any chosen direction, including a coordinate-axis direction.

Partial derivatives and directional derivatives both deal with rates of change, but they look in different directions. In the chart below, the partial derivative is distinguished as the rate of change that looks at axis directions one by one, while the directional derivative is the rate of change that follows an arbitrary direction.

![Chart comparing the directions observed by partial derivatives and directional derivatives](/AiBook/assets/part-02/chapter-04/partial-vs-directional-derivative-en.svg)

For `F(x, y) = 3x + 4y`, the partial derivatives are `3` and `4`. The direction `[0.6, 0.8]`, which changes both coordinates, has length `√(0.6² + 0.8²) = 1`. Moving distance `h` in this direction increases x by `0.6h` and y by `0.8h`.

The function increases by `3 × 0.6h + 4 × 0.8h = 5h`, so the directional derivative is `5`. Use unit direction vectors to compare directions at the same travel distance.

## Gradients and Vector Fields

Gradient is a vector that gathers several partial derivatives in order.

\[
\nabla L =
\left[
\frac{\partial L}{\partial w_1},
\frac{\partial L}{\partial w_2}
\right]
\]

This expression contains in one bundle the answers to the two questions: `if we change w_1, how does the loss change?` and `if we change w_2, how does the loss change?`

If there is only one control knob, one slope is enough. But if there are many knobs, we must look at the rate of change for each knob together. That bundle of rates of change is the gradient.

The point that a gradient is a vector also becomes natural here. A vector is an expression that gathers several numbers in order. Among such vectors, a gradient is the vector that gathers `the rate of change of each direction`.

A function assigning one number to each position can be viewed as a scalar field—for example, assigning a height to each point on a plane. Placing the gradient vector at each point of a differentiable scalar field gives a vector field. Vector calculus studies such functions and rates of change in space.

![Chart showing where scalar fields, gradients, and vector fields connect in vector calculus](/AiBook/assets/part-02/chapter-04/vector-calculus-context-en.svg)

## Ascent and Descent Directions

A gradient connects to the direction in which the value increases most rapidly in a multivariable function. In AI learning, we usually want to reduce loss. So, rather than the gradient itself, the direction opposite the gradient often becomes more important.

For a differentiable function with a nonzero gradient, the instantaneous rate of increase is greatest in the gradient direction. A sufficiently small step in the opposite direction decreases the function value.

The chart below shows how, at one point of a loss function, the gradient direction and the direction that reduces loss become opposites.

![Chart comparing the gradient direction and the descending direction on contours of a loss function](/AiBook/assets/part-02/chapter-04/gradient-direction-loss-contour-en.svg)

What matters here is that a gradient does not tell us the whole map. It tells us direction information near the current position. It tells us which side from the current position is likely to increase the value and which side is likely to decrease it.

## Repeating Gradient Descent

Gradient descent is an optimization method that moves opposite to the gradient.

| Expression | Introductory Meaning |
| --- | --- |
| gradient | the direction in which the value increases most rapidly at the current position |
| descent | going down, moving toward the lower side |
| gradient descent | a repeated method that uses the gradient as a clue and moves toward the side where the value becomes lower |

Written in a definition-like way, gradient descent is an optimization method that repeatedly calculates the gradient of the loss function at the current parameter position and moves the parameters a little in the direction in which the loss decreases.

That is why gradient descent is often explained with the analogy of coming down from a mountain. From the current position, we look at the surrounding slope and move a little in the direction that becomes lower. We do not teleport to the correct place at once. We move a little and then check the slope again, repeating this process.

Like the chart below, gradient descent is not a method that moves to the center in one jump. It moves a little in the direction where loss decreases from the current position, then reads the direction again from the new position.

![Chart showing gradient descent as repeated small movement toward lower loss](/AiBook/assets/part-02/chapter-04/gradient-descent-steps-en.svg)

## Learning Rate and Movement

Gradient descent is usually explained with an update expression like the following.

\[
w_{\text{next}} = w - \eta \nabla L
\]

The symbols mean the following.

| Symbol | Introductory Meaning |
| --- | --- |
| \(w\) | the current parameter value |
| \(w_{\text{next}}\) | the next parameter value |
| \(\nabla L\) | the directional information about how loss changes at the current position |
| \(\eta\) | the learning rate that decides how far to move at one time |
| \(-\eta \nabla L\) | the small amount of movement toward the side where loss decreases |

The phrase `a little` matters: too large a step can overshoot a lower point, while too small a step can take a long time.

![Chart showing that the gradient-descent update means moving a little from the current value in the direction opposite the gradient](/AiBook/assets/part-02/chapter-04/gradient-descent-update-intuition-en.svg)

Gradient descent uses the slope at the current position and does not always reach a global minimum. Results can depend on initialization, the loss function’s shape, step size, and iteration count.

## Backpropagation and Parameter Adjustment

Backpropagation is connected to gradient descent, but it is not the same thing.

Gradient descent is an optimization method that uses the gradient to adjust values, while backpropagation is the procedure that efficiently computes the gradients of many parameters inside a deep-learning model.

We can read it as a structure such as `input -> layer 1 calculation -> layer 2 calculation -> output -> loss`.

To learn, we must know how the loss changes with respect to the parameters of each layer. Backpropagation is the procedure that computes this information efficiently by passing it from the back toward the front.

As in the chart below, the forward pass calculates values from input to output and loss, while the backward pass calculates from the loss backward how much each layer's parameters affect the loss.

![Chart comparing the direction of computation in the forward pass and the direction in which gradients are sent back in backpropagation](/AiBook/assets/part-02/chapter-04/backpropagation-gradient-flow-en.svg)

## The Scope of High School AI Mathematics

In the 2022 revised Korean high school curriculum, `AI Mathematics` includes loss functions and gradient descent. So it may be inaccurate to say that `there is nothing in the high school curriculum that connects to gradient at all`.

However, `AI Mathematics` may be an unfamiliar course title to readers who learned school mathematics long ago. It is natural for these readers not to associate loss functions or gradient descent with high school mathematics.

The reviewed Korean high school curriculum text did not contain the terms `그래디언트`, `gradient`, `편미분`, or `방향도함수`. Gradient descent in `AI Mathematics` is closer to an intuitive treatment of a loss function defined using one variable and its derivative at a point.

Even after learning loss functions and gradient descent in high school, readers may encounter partial and directional derivatives of multivariable functions separately.

## Axis-Aligned and Simultaneous Movement

For `F(x, y) = 3x + 4y`, the value at `[1, 1]` is `7`. Move the same distance, `0.1`, in each direction.

| Direction | New position | New function value | Increase |
| --- | --- | --- | --- |
| x-axis `[1, 0]` | `[1.1, 1]` | 7.3 | 0.3 |
| y-axis `[0, 1]` | `[1, 1.1]` | 7.4 | 0.4 |
| `[0.6, 0.8]` | `[1.06, 1.08]` | 7.5 | 0.5 |

The gradient `[3, 4]` has length `5`; dividing by that length gives `[0.6, 0.8]`. Changing both inputs along this direction increases the function more than moving the same distance along either axis. Moving `0.1` in direction `[-0.6, -0.8]` instead gives position `[0.94, 0.92]` and function value `6.5`.

Term definition: [gradient in the glossary](/AiBook/en/reference/concept-glossary-alpha/g/#gradient).

## Checklist

- You can explain that school-level differentiation memory mainly starts from the rate of change of a one-variable function.
- You can explain that the gradient naturally appears in a function with several inputs.
- You can explain a partial derivative as `the rate of change viewed one input at a time among several inputs`.
- You can explain a directional derivative as `the rate of change viewed in a chosen direction`.
- You can explain a gradient as `a vector that gathers partial derivatives`.
- You can explain gradient descent as `the repeated method that reduces loss using the gradient`.
- You can explain backpropagation as `the procedure that efficiently computes the gradients of many parameters`.
- You can explain that, even in the high school `AI Mathematics` curriculum, gradient descent appears, but the systems of gradient and partial derivatives may still need separate supplementary explanation.
- You can distinguish what partial derivative, directional derivative, and gradient each inspect differently.
- You can explain why a gap arises between memories of school differentiation and AI learning documents.

## Sources and References

- Ministry of Education, `[Ministry of Education Notice No. 2022-33] General and Subject-Specific Elementary and Secondary School Curriculum Notice`. It provides the official notice and appendix-material location for the 2022 revised Korean high school curriculum. [https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=141&boardSeq=93458&lev=0&page=1&searchType=null&statusYN=W](https://www.moe.go.kr/boardCnts/viewRenew.do?boardID=141&boardSeq=93458&lev=0&page=1&searchType=null&statusYN=W){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-20
- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }. It supports partial derivatives, directional derivatives, gradient vectors, and the relation between the gradient and direction of maximum increase. Checked: 2026-09-08.
- KOCW, `Calculus 2 - Hanyang University`. It confirms that this open course covers multivariable functions, partial derivatives, vector functions, and related calculus topics. [https://www.kocw.or.kr/home/search/kemView.do?kemId=330031](https://www.kocw.or.kr/home/search/kemView.do?kemId=330031){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-20
