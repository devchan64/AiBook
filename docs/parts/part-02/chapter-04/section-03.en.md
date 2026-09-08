# P2-4.3 Derivative and Gradient

> Section ID: `P2-4.3`
> Version: `v2026.09.08`

The derivative function of one variable gives the instantaneous rate of change with respect to its input. For a function of several variables, we take partial derivatives with respect to one variable while holding the others fixed, then gather them into the gradient.

## Derivatives, Partial Derivatives, and Gradients

| Criterion | Why It Matters |
| --- | --- |
| A derivative is the instantaneous rate of change of one input | It is the starting point for reading slope and instantaneous rate of change in a one-variable problem. |
| A partial derivative looks at several inputs one by one | In a multivariable function, we must inspect separately how each input changes the result. |
| A gradient is a vector that gathers several partial derivatives | In learning, we must read changes across many parameter directions at once. |

## Derivative of a One-Variable Function

Suppose a function receives one input.

\[
y = f(x)
\]

Then the derivative shows how much \(y\) changes when \(x\) changes by a very small amount. It is the instantaneous rate of change at a specific point.

For example, consider the following function.

\[
f(x) = x^2
\]

The derivative function of this function is the following.

\[
f'(x) = 2x
\]

This expression tells the slope at each position.

| \(x\) | \(f(x) = x^2\) | \(f'(x) = 2x\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 2 |
| 2 | 4 | 4 |
| 3 | 9 | 6 |

At \(x = 1\), the slope is 2, and at \(x = 3\), the slope is 6. Even in the same function, the rate of change differs by position.

```text
f(x) = x^2      -> a function that turns input into output
f'(x) = 2x      -> a function that tells how quickly the output changes at each position
```

## Derivative Values and Derivative Functions

When learning differentiation in Korean, we meet the expressions for `derivative at a point` and `derivative function`.

| Expression | Introductory Meaning |
| --- | --- |
| derivative at a point | the instantaneous rate of change at a specific point |
| derivative function | the function that tells the instantaneous rate of change at each point |

For example, in \(f(x) = x^2\), the derivative at a point at \(x = 2\) is the following.

\[
f'(2) = 4
\]

By contrast, the derivative function is this whole function.

\[
f'(x) = 2x
\]

1. A derivative at a point is the value at one point.
2. A derivative function is the function that tells the derivative at a point at each point.

## Multiple Variables and Partial Derivatives

In AI models, it is rare that there is only one input or one parameter. Usually several values exist together.

For example, suppose a loss function depends on two parameters \(w_1\) and \(w_2\).

\[
L(w_1, w_2)
\]

Then there is not only one question.

1. If we change `w_1` a little, how does the loss `L` change?
2. If we change `w_2` a little, how does the loss `L` change?

Calculating the rate of change while looking at each input one by one is the partial derivative.

\[
\frac{\partial L}{\partial w_1}
\]

\[
\frac{\partial L}{\partial w_2}
\]

The symbol \(\partial\) is used when finding the rate of change with respect to one variable while keeping the other variables fixed.

1. An ordinary derivative is the rate of change when there is one input.
2. A partial derivative is the rate of change viewed one input at a time when there are several inputs.

## Partial-Derivative Vectors and Nabla

Gradient is a vector that gathers several partial derivatives.

If the loss function depends on \(w_1\) and \(w_2\), the gradient can be written as follows.

\[
\nabla L =
\left[
\frac{\partial L}{\partial w_1},
\frac{\partial L}{\partial w_2}
\right]
\]

The symbol \(\nabla\) is read as nabla.

1. We inspect how the loss changes when each parameter is changed a little.
2. We gather those rates of change into one bundle.
3. That bundle is the gradient.

The order of gradient components matches the parameter order. In the expression above, the first component is the rate of change with respect to `w_1`, and the second is with respect to `w_2`.

## Gradients and the Direction of Increase

The reason gradient matters is that it has meaning beyond being a bundle of numbers. In a function made of several variables, the gradient connects to the direction in which the value increases most rapidly.

For a differentiable function with a nonzero gradient, comparing directions over the same small distance gives the following.

1. The gradient direction is the direction in which the function value increases most rapidly.
2. Moving a sufficiently small distance opposite the gradient reduces the function value.

In AI learning, we usually want to reduce loss. So, rather than the gradient itself, the direction opposite the gradient often becomes important.

## Sum of Two Squares and Its Gradient

Let us think about the following loss function.

\[
L(w_1, w_2) = w_1^2 + w_2^2
\]

This function grows as \(w_1\) and \(w_2\) move farther from 0.

The partial derivatives with respect to each parameter are the following.

\[
\frac{\partial L}{\partial w_1} = 2w_1
\]

\[
\frac{\partial L}{\partial w_2} = 2w_2
\]

So the gradient becomes:

\[
\nabla L = [2w_1,\ 2w_2]
\]

If the current values are \(w_1 = 3\), \(w_2 = 4\), then the gradient is:

\[
\nabla L = [6,\ 8]
\]

This means that, at the current position, the loss increases in the \(w_1\) direction and also in the \(w_2\) direction. If we want to reduce the loss, we naturally think of the opposite side.

```text
current position: [3, 4]
gradient: [6, 8]
intuitive direction for reducing loss: toward [-6, -8]
```

The current loss is `3² + 4² = 25`. Moving by `0.01 × [6, 8]` opposite the gradient gives the new position `[2.94, 3.92]`, where the loss decreases to `2.94² + 3.92² = 24.01`.

## Two Weights in a Recommendation Score

Suppose one item has interest similarity `0.8` and freshness `0.4`. Multiply these two features by weights `w_1` and `w_2` to calculate its recommendation score `S`.

\[
S(w_1,w_2)=0.8w_1+0.4w_2
\]

With `w_1 = 1` and `w_2 = 1`, the score is `1.2`. Increase one weight by `0.05` while keeping the other fixed.

| Changed weight | New score | Score increase | Increase / 0.05 |
| --- | --- | --- | --- |
| `w_1`: 1 → 1.05 | `1.24` | `0.04` | `0.8` |
| `w_2`: 1 → 1.05 | `1.22` | `0.02` | `0.4` |

This expression is linear in each weight, so these rates equal the partial derivatives. The gradient is `[0.8, 0.4]`. For equal increases in the weights, this item’s score is twice as sensitive to `w_1`.

This calculation describes the score change for one item. To determine changes in ranking, we must also compare other items’ scores. A higher score does not guarantee a higher click-through rate or greater user satisfaction.

## Checklist

- You can explain a derivative as the instantaneous rate of change with respect to one input.
- You can distinguish a derivative at a point from a derivative function.
- You can explain a partial derivative as the rate of change viewed separately for one among several inputs.
- You can explain a gradient as a vector that gathers several partial derivatives.
- You can explain that a gradient connects to the direction in which the function value increases rapidly.
- You can explain a gradient in practice as `the information used to see in which direction to change one among several control values`.
- You can connect the partial derivative with respect to each recommendation-score weight to the score increase.
- You can explain the broad flow in which, in AI learning, a gradient is used to find the direction that reduces loss.
- You can distinguish what `derivative`, `partial derivative`, and `gradient` each point to.

- You can read a gradient as a vector of rates of change along different directions, beyond a bundle of numbers.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }. It supports the relation between derivative and instantaneous rate of change. Checked: 2026-07-20.
- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }. It supports partial derivatives, the gradient vector, nabla notation, and the relation between the gradient and the direction of maximum increase. Checked: 2026-07-20.
