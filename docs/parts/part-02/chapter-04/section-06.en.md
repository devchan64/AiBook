# P2-4.6 Composite Functions and the Chain Rule

> Section ID: `P2-4.6`
> Version: `v2026.09.15`

A composite function feeds one function’s output into the next function as input. When each stage is differentiable, the chain rule multiplies their rates of change to obtain the overall rate.

## Two Stages and a Composite Function

\[
y = 2x + 1,\qquad z = y^2
\]

First calculate the intermediate value `y` from `x`, then square `y` to obtain `z`. As one expression, this is `z = (2x + 1)²`.

| Stage | Expression | At x = 1 |
| --- | --- | --- |
| First calculation | `y = 2x + 1` | y = 3 |
| Next calculation | `z = y²` | z = 9 |
| Overall calculation | `z = (2x + 1)²` | z = 9 |

In general, `z = f(g(x))` means calculate `g(x)` and feed its result into `f`. In a neural network, one layer’s output similarly becomes the next layer’s input.

```mermaid
--8<-- "assets/part-02/chapter-04/chain-rule-composition-flow-en.mmd"
```

## Multiplying Rates Across Stages

At `x=1`, we have `y=3`. A small input change `Δx` produces `Δy=2Δx` in the first stage. The next stage gives `Δz≈6Δy`, so substituting the intermediate change yields `Δz≈6×2Δx=12Δx`. **Rates multiply because the change produced by one stage becomes the input change to the next.** The first stage is linear, making its change relation exact; the squaring stage uses an approximation near the current point.

Applying the chain rule to this calculation gives:

\[
\frac{dz}{dx} = \frac{dz}{dy}\cdot\frac{dy}{dx}
\]

The rate for the first stage, `y = 2x + 1`, is `dy/dx = 2`. The next stage, `z = y²`, has rate `dz/dy = 2y`. The overall rate is therefore `2y × 2 = 4y`; substituting `y = 2x + 1` gives `8x + 4`.

At `x = 1`, `y = 3`, giving:

| Change | Rate at this point |
| --- | --- |
| x → y | 2 |
| y → z | 6 |
| x → z | 6 × 2 = 12 |

A very small change in `x` is approximately doubled in the first stage and multiplied by six in the next, so the final change is approximately twelve times the input change.

Evaluate the outer rate `2y` at **the intermediate value `y=3` calculated from the input**, not at the original input `x=1`. Using `2×1=2` would evaluate the rate at the wrong point. The general expression is `f′(g(x))×g′(x)`, which differs from `f′(x)×g′(x)`.

## Checking a Small Input Change

Changing `x` from `1` to `1.01` changes `y` from `3` to `3.02` and `z` from `9` to `9.1204`.

- Change approximated using the chain rule: `12 × 0.01 = 0.12`
- Actual change: `9.1204 − 9 = 0.1204`

A derivative is the instantaneous rate at a point, so the approximation may differ slightly from the change over a finite interval. Reducing the input increment to `0.001` gives an actual change of `0.012004` and a derivative-based approximation of `0.012`.

## From Input Derivatives to Parameter Derivatives

The earlier `dz/dx` measures how sensitively the final output changes with the input. During learning, we hold the data input fixed and change parameters such as weights and biases. Consider a small model with input `a`, prediction `ŷ`, and target `t`.

\[
\hat y=wa+b,\qquad L=(\hat y-t)^2
\]

With `a=2`, `t=5`, and current parameters `w=1`, `b=1`, the prediction is 3 and the loss is 4. We keep the input and target fixed and find the loss rate when changing only `w` or only `b`.

| Calculation | Result | Meaning |
| --- | --- | --- |
| `∂L/∂ŷ=2(ŷ−t)` | −4 | A small prediction increase reduces the current loss |
| `∂ŷ/∂w=a` | 2 | Rate at which a weight change affects the prediction |
| `∂ŷ/∂b=1` | 1 | Rate at which a bias change affects the prediction |

The loss derivative with respect to the prediction, `−4`, is shared by both parameter calculations. Multiply it by the prediction derivative with respect to each parameter.

\[
\frac{\partial L}{\partial w}
=\frac{\partial L}{\partial\hat y}\frac{\partial\hat y}{\partial w}
=(-4)\times2=-8,\qquad
\frac{\partial L}{\partial b}
=\frac{\partial L}{\partial\hat y}\frac{\partial\hat y}{\partial b}
=(-4)\times1=-4
\]

The gradient in `[w,b]` order is therefore `[-8,-4]`. Increasing only the weight by 0.01 changes the prediction to 3.02 and the loss to 3.9204. The actual loss change, `−0.0796`, is close to the derivative approximation `−8×0.01=−0.08`.

## Forward Values and Backward Derivatives

The forward pass calculates prediction and loss from the input and current parameters. Backpropagation calculates derivatives of the final loss backward through the computations, combining them with each operation’s derivative. In this example, we reuse the forward prediction 3 to calculate `∂L/∂ŷ=−4`, then reuse that derivative for the earlier parameters.

```mermaid
--8<-- "assets/part-02/chapter-04/chain-rule-backward-flow-en.mmd"
```

The blue flow shows the order of value calculations; the dashed flow shows derivative calculations. Backpropagation does not turn the prediction back into the input or immediately modify the parameters. It starts with the derivative of the final loss with respect to itself, `∂L/∂L=1`, and calculates the required rates backward.

The chain rule differentiates composite functions; backpropagation follows a computation graph backward while reusing intermediate results. When several paths lead to the same parameter, their contributions are added. This small example illustrates multiplication along each path. The optimizer uses the resulting gradients to update parameters.

## Exercise: Recalculate the Intermediate Value

First, find `y`, `z`, and `dz/dx` at `x=0` for `y=2x+1`, `z=y²`. Second, change the first expression to `y=3x+1` and find the overall rate at `x=1`. Third, increase only the bias by 0.01 in the learning example and compare the actual loss change with the derivative approximation.

??? note "Calculation and Explanation"
    First, `y=1`, `z=1`, and `dz/dx=(2×1)×2=4`. Second, the intermediate value is `y=4`, so the overall rate is `(2×4)×3=24`. Third, the prediction becomes 3.01 and the loss is `(-1.99)²=3.9601`, giving actual change `−0.0399`. The derivative approximation is `−4×0.01=−0.04`.

## Checklist

- You can explain a composite function as one function’s output becoming the next function’s input.
- For `y = 2x + 1` and `z = y²`, you can calculate the overall rate of 12 at `x = 1`.
- You can distinguish a change approximated using an instantaneous rate from the actual change over a finite interval.
- You can distinguish the roles of the chain rule and backpropagation.
- You can explain that backpropagation calculates how parameter changes affect loss.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.6 The Chain Rule](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule){: target="_blank" rel="noopener noreferrer" }. Covers differentiation of composite functions and applying the chain rule across two or more stages. Checked: 2026-09-15.
- Related sections in this Part: [P2-4.3 Derivatives and Gradients](section-03.en.md), [P2-4.5 Gradient Supplement: from School Differentiation to Multivariable Differentiation](section-05.en.md).

- PyTorch, [Automatic Differentiation with torch.autograd](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html){: target="_blank" rel="noopener noreferrer" }. Forward computation graphs and application of the chain rule in backpropagation. Checked: 2026-09-15.
