# P2-6.3 The Intuition of Gradient Descent

> Section ID: `P2-6.3`
> Version: `v2026.09.08`

Gradient descent calculates the objective function’s gradient at the current parameters and changes the parameters in the opposite direction. The learning rate multiplies the gradient to control the amount of movement.

## Current Loss of the Line Model

We use data for predicting scores from study time.

| Student | Study time `x` | Actual score `y` |
| --- | ---: | ---: |
| A | 1 | 55 |
| B | 2 | 65 |
| C | 3 | 80 |
| D | 4 | 90 |

For the current line \(\hat{y} = 8x + 45\), the predictions are `53, 61, 69, 77`, below the actual scores by `2, 4, 11, 13`. The mean squared error is `(4 + 16 + 121 + 169) / 4 = 77.5`.

The objective is to reduce this loss by changing slope `a` and intercept `b`.

![Gradient descent takes small steps toward lower loss on a loss curve](../../../assets/part-02/chapter-06/gradient-descent-loss-curve-en.svg)

The movement can be represented as a learning loop:

```mermaid
--8<-- "assets/part-02/chapter-06/gradient-descent-loop-flow-en.mmd"
```

## Direction, Step Size, and Repetition

| Criterion | Why it matters |
| --- | --- |
| Gradient descent repeats small steps that reduce loss | Learning involves repeated adjustments rather than one jump to the answer. |
| Move opposite to the gradient | The gradient points toward increasing loss, opposite to the objective. |
| The learning rate controls each step | Even with the right direction, an unsuitable step size can make learning unstable or slow. |

## The Slope at the Current Position

Gradient descent is often compared to descending a mountain: inspect the nearby slope and take small steps downhill.

The current position represents the model parameters, height represents loss, and downhill represents the direction in which loss decreases.

The analogy has limits. In actual model training, we do not see the entire map at once. We read the direction near the current position, move a little, and check again.

Gradient descent is therefore an iterative method that seeks gradual improvement using current information, rather than jumping directly to the answer.

In the study-time example, if the current line underpredicts students C and D, we repeatedly check whether slightly increasing `a` or adjusting `b` reduces loss instead of guessing a perfect line at once.

## Opposite to the Gradient

The gradient is associated with the direction of the fastest local increase in the function value. For a loss function, it points toward increasing loss.

AI training usually seeks to reduce loss, so it moves opposite to the gradient. The gradient points toward increasing loss, and the opposite direction points toward decreasing loss.

This is the meaning of `descent`: we calculate a gradient in order to go down.

For a differentiable objective with a nonzero gradient, a sufficiently small step opposite to the gradient reduces the objective value. A large step in that same direction can increase loss.

## Learning Rate and Movement Size

Knowing a direction of decreasing loss does not justify a large jump. The current gradient describes the local neighborhood. Too large a step may overshoot a lower point.

The learning rate controls how much to move. Too small a rate produces slow progress; an appropriate rate can steadily reduce loss; too large a rate can overshoot a good position or make loss fluctuate.

The actual movement is the learning rate multiplied by the gradient. Even at the same learning rate, movement distance changes when gradient magnitude changes.

For example, increasing `a` too much at once might reduce student D’s error while overshooting for students A and B. Too small a change makes improvement slow even when the direction reduces loss. The learning rate controls this step size.

## The Gradient Descent Update

Gradient descent is commonly written as:

\[
\theta_{\text{new}}
=
\theta_{\text{old}}
-
\eta \nabla J(\theta)
\]

The symbols denote the following values.

| Symbol | Introductory meaning |
| --- | --- |
| \(\theta\) | Parameters adjusted by the model |
| \(J(\theta)\) | The objective function to reduce |
| \(\nabla J(\theta)\) | Direction of increasing loss at the current position |
| \(\eta\) | Learning rate, a movement coefficient multiplying the gradient |
| \(-\eta \nabla J(\theta)\) | A small movement toward decreasing loss |

Here, \(\theta\) is `[a, b]`, and \(J\) is the mean squared error across the four students. The formula compresses the calculation `current parameters − learning rate × gradient`.

## One Update of Slope and Intercept

Writing each student’s `predicted − actual` value as \(r_i\), the current errors are `−2, −4, −11, −13`. Differentiating MSE with respect to each parameter gives:

\[
\frac{\partial J}{\partial a}=\frac{2}{4}\sum_{i=1}^{4}r_i x_i
=\frac{2}{4}(-2-8-33-52)=-47.5
\]

\[
\frac{\partial J}{\partial b}=\frac{2}{4}\sum_{i=1}^{4}r_i
=\frac{2}{4}(-2-4-11-13)=-15
\]

Changing `a` affects predictions more for students with greater study time `x`, so the first expression multiplies by `x_i`. Changing `b` shifts every prediction by the same amount.

At learning rate `0.01`, the update is:

- `a_new = 8 − 0.01 × (−47.5) = 8.475`
- `b_new = 45 − 0.01 × (−15) = 45.15`

Predicting with the new line reduces MSE from `77.5` to about `54.76`. For the next update, recalculate the gradient at `[8.475, 45.15]`.

## From Prediction to Update

Gradient descent repeats the same steps.

1. Predict with the current parameters.
2. Calculate loss.
3. Calculate the gradient.
4. Adjust the parameters slightly.
5. Predict again.

## Comparing Loss Across Learning Rates

Starting from `[8, 45]` with gradient `[-47.5, -15]`, change only the learning rate and take one step.

| Learning rate | New a | New b | MSE after the step |
| --- | --- | --- | --- |
| 0.001 | 8.0475 | 45.015 | About 75.04 |
| 0.01 | 8.475 | 45.15 | About 54.76 |
| 0.2 | 17.5 | 48 | About 409.63 |

All three steps move opposite to the gradient, but a learning rate of `0.2` greatly increases loss. At `0.001`, the decrease is small. Both the direction and the amount of movement need to be chosen appropriately.

## Conditions Affecting Convergence

Gradient descent is powerful, but it does not automatically guarantee a perfect answer.

Several conditions affect the result.

| Condition | Why it matters |
| --- | --- |
| Initialization | The path may depend on the starting position. |
| Learning rate | Too small can be slow; too large can be unstable. |
| Loss landscape | There may be valleys, flat regions, and multiple low points. |
| Data | Loss is calculated from data and is affected by its quality. |
| Iterations | Too few may leave the model undertrained; too many may lead to overfitting. |

Gradient descent moves toward improvement under given criteria and conditions. It does not automatically resolve every real-world condition.

## Checklist

- You can explain gradient descent as repeated movement to reduce loss.
- You can connect the gradient to increasing loss at the current position.
- You can explain why reducing loss requires moving opposite to the gradient.
- You can explain the learning rate in terms of movement size.
- You can read the update as taking a small step opposite to the gradient from the current values.
- You can explain the influence of initialization, learning rate, loss landscape, data, and iteration count.
- You can connect reducing loss to actual changes in parameters.
- You can distinguish the gradient direction from the opposite direction used for descent.

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to support the deep-learning optimization context of cost functions, parameters, gradient-based movement, gradient descent, and learning rate.
- Stephen Boyd, Lieven Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2004, checked 2026-07-20. Used as supplementary support for optimization problems and gradient-based repeated movement in the mathematical optimization context.
