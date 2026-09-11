# P2-4.4 Why Learning Needs Differentiation

> Section ID: `P2-4.4`
> Version: `v2026.09.08`

Loss describes how different the current prediction is from the target. Derivatives and gradients tell us how that loss changes when parameters change slightly. Gradient-based learning uses this information to adjust parameters.

## Loss and Adjustment Direction

| Criterion | Why It Matters |
| --- | --- |
| Learning is the process of adjusting parameters | The model improves by looking at the current result and changing internal numbers a little at a time. |
| Loss alone does not tell the direction | It shows how wrong things are, but not where to move. |
| Derivatives and gradients give directional information | We must judge in which direction to change parameters so that loss decreases. |

## Prediction, Loss Calculation, and Parameter Adjustment

An AI model receives an input and makes an output. Before learning, the model may not yet produce good outputs. So we use training data to adjust the parameters inside the model.

1. Input data enters.
2. The model makes a prediction.
3. We calculate the loss.
4. We adjust the parameters.
5. We predict again.

Here, a parameter is not a rule that a person manually sets every time. It is a number that the model adjusts through learning. Learning can be read as the process of changing these numbers and finding the direction that reduces loss.

## Loss Values and Direction Information

Loss is a value that expresses numerically how different the model's prediction is from the target.

For example, in a model that predicts house prices, if the real house price is 500 million won but the model predicts 400 million won, the error is 100 million won.

If we score that error in some way, it becomes loss. If the loss is large, we can say the model's prediction is not good. If the loss is small, we can say the prediction is better by the current standard.

But the loss value alone is not enough.

If the loss is large, we know the current result is not good. But we still do not know what should be changed or how.

Learning needs questions such as: which parameter makes the loss decrease, should that parameter be increased or decreased, and how sensitively does the loss change when we adjust it a little?

Derivative and gradient are the language for answering these questions.

## Derivative Sign and Adjustment Direction

As a very simple example, suppose the loss changes with one parameter \(w\) like this.

\[
L(w) = (w - 3)^2
\]

This function has loss 0 when \(w = 3\).

The derivative is:

\[
L'(w) = 2(w - 3)
\]

Let us read the values at a few points.

| \(w\) | \(L(w)\) | \(L'(w)\) | How to Read It |
| --- | --- | --- | --- |
| 0 | 9 | -6 | We can think of increasing \(w\). |
| 2 | 1 | -2 | Increasing \(w\) is still the direction that reduces loss. |
| 3 | 0 | 0 | In this example, the loss is smallest here. |
| 5 | 4 | 4 | We can think of decreasing \(w\). |

What matters here is the sign and size of the derivative value.

If the derivative value is negative, increasing \(w\) a little may be the direction that reduces loss. By contrast, if the derivative value is positive, we can think of decreasing \(w\). Also, if the derivative value is large in magnitude, we can read that the loss is changing sensitively at the current position.

## Gradients Across Multiple Parameters

Real models rarely have only one parameter. If there are many parameters such as \(w_1\), \(w_2\), and \(w_3\), the loss changes along many directions.

In other words, we ask together how the loss changes when `w_1` changes, how it changes when `w_2` changes, and how it changes when `w_3` changes.

If we gather the rates of change with respect to all parameters, we get the gradient.

\[
\nabla L =
\left[
\frac{\partial L}{\partial w_1},
\frac{\partial L}{\partial w_2},
\frac{\partial L}{\partial w_3}
\right]
\]

This vector tells us how the loss changes along each parameter direction at the current position. That is why loss functions and gradients appear together in AI learning.

The loss function expresses what we want to reduce, and the gradient tells us which direction we should inspect if we want to reduce that loss.

## Number of Parameter Combinations

The reason differentiation is needed also connects to the question `could we not just try all possible values?`

In a small problem, we can substitute several values directly. For example, we can try `w = 0, 1, 2, 3, 4, 5` and choose the value with the smallest loss.

Trying these six values for each parameter gives `6² = 36` combinations for two parameters and `6¹⁰ = 60,466,176` for ten. The cost of evaluating every combination grows rapidly with the number of parameters.

Instead of checking every possibility, the gradient tells us which direction from the current position may reduce loss.

Of course, that does not mean the gradient always guarantees the globally best answer. A gradient gives information about change near the current position. So in real learning, the initial value, learning rate, data, model structure, and optimizer all matter together.

## The Role of Backpropagation

A deep-learning model is a structure in which calculations across many layers are connected. The input passes through many calculations, becomes an output, and from that output we calculate loss.

We can read it as a flow such as `input -> layer 1 calculation -> layer 2 calculation -> layer 3 calculation -> output -> loss`.

To learn, we must know how the loss changes with respect to the parameters of each layer. In other words, we need gradients for many parameters.

Backpropagation is the procedure for computing these gradients efficiently.

Training is the whole process of adjusting parameters so that loss decreases, while backpropagation is the procedure that computes and passes along the gradients needed for that adjustment.

## Training State and Change Signals

In practice, we may hear the following expressions more often than the word differentiation itself.

| Practical Expression | How to Read It by Connecting It to Differentiation |
| --- | --- |
| loss does not decrease | the current adjustment direction or size may not be good |
| the learning rate is too large | moving too far at once may make loss unstable |
| the gradient is small | the change signal may be weak at the current position |
| the gradient explodes | the change signal may be too large, making learning unstable |
| backpropagation is needed | we must calculate the rates of change with respect to parameters across many layers |

## Equal Loss, Opposite Adjustment Directions

For the loss function `L(w) = (w − 3)²` above, both `w = 2` and `w = 4` have loss `1`. Their derivatives, however, are `−2` and `2`, respectively.

| Current w | Current loss | Derivative | Small adjustment that reduces loss | New loss |
| --- | --- | --- | --- | --- |
| 2 | 1 | −2 | 2 → 2.1 | 0.81 |
| 4 | 1 | 2 | 4 → 3.9 | 0.81 |

Although the losses are equal, the adjustment directions are opposite. Increasing `w` at `w = 2` and decreasing it at `w = 4` reduces loss. Moving `0.1` in the opposite directions raises loss to `1.21` in both cases.

Even with the correct direction, moving too far can increase loss. Moving from `w = 2` to `w = 5` raises loss from `1` to `4`. Both direction and step size must therefore be chosen.

```mermaid
--8<-- "assets/part-02/chapter-04/learning-adjustment-flow-en.mmd"
```

## Checklist

- You can explain training as the process of adjusting parameters to reduce loss.
- You can explain that the loss value alone makes it hard to know what should be changed and in which direction.
- You can explain that a derivative shows how the loss changes when one parameter is changed a little.
- You can explain that a gradient is a vector that gathers change information for many parameters.
- You can explain that it is hard to test every possible value, so directional information at the current position matters.
- You can distinguish backpropagation not as learning itself, but as the procedure that computes gradients efficiently.
- You can separately explain `how wrong is it?` and `in which direction should it be changed?`

- You can explain why derivatives and gradients follow naturally from the loss function.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }. It supports the relation between derivative and instantaneous rate of change. Checked: 2026-07-20.
- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }. It supports the relation between the gradient and the direction of maximum increase. Checked: 2026-07-20.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8. Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }. It treats deep learning training as cost-function and parameter optimization, and gives the context for gradient-based optimization in training. Checked: 2026-07-20.
