# P2-4.6 Composite Functions and the Chain Rule

> Section ID: `P2-4.6`
> Version: `v2026.09.08`

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

## Checking a Small Input Change

Changing `x` from `1` to `1.01` changes `y` from `3` to `3.02` and `z` from `9` to `9.1204`.

- Change approximated using the chain rule: `12 × 0.01 = 0.12`
- Actual change: `9.1204 − 9 = 0.1204`

A derivative is the instantaneous rate at a point, so the approximation may differ slightly from the change over a finite interval. Reducing the input increment to `0.001` gives an actual change of `0.012004` and a derivative-based approximation of `0.012`.

## Computing Rates in Backpropagation

Backpropagation works backward to calculate how parameter changes in each layer affect the final loss. It uses the chain rule to combine the rate from a later stage with the rate from an earlier stage.

If `z` is treated as the final loss in this example, calculate the later-stage rate `dz/dy = 6`, then multiply by `dy/dx = 2` to obtain `dz/dx = 12`. Values are calculated in the order `x → y → z`; rates with respect to the final value are calculated from the later stage toward the earlier stage.

The chain rule is a differentiation rule for composite functions. Backpropagation uses it to efficiently compute gradients for many parameters. An optimization method then uses those gradients to change the parameters.

## Checklist

- You can explain a composite function as one function’s output becoming the next function’s input.
- For `y = 2x + 1` and `z = y²`, you can calculate the overall rate of 12 at `x = 1`.
- You can distinguish a change approximated using an instantaneous rate from the actual change over a finite interval.
- You can distinguish the roles of the chain rule and backpropagation.
- You can explain that backpropagation calculates how parameter changes affect loss.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.6 The Chain Rule](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule){: target="_blank" rel="noopener noreferrer" }. Covers differentiation of composite functions and applying the chain rule across two or more stages. Checked: 2026-09-08.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }. Definitions of backpropagation and gradient provide context for connecting the chain rule with backpropagation. Checked: 2026-07-20.
- Related sections in this Part: [P2-4.3 Derivatives and Gradients](section-03.en.md), [P2-4.5 Gradient Supplement: from School Differentiation to Multivariable Differentiation](section-05.en.md).
