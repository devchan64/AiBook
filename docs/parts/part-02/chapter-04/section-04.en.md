# P2-4.4 Why Learning Needs Differentiation

> Section ID: `P2-4.4`
> Version: `v2026.09.14`

A large loss alone does not tell us whether to increase or decrease a parameter. Differentiation tells us how sensitively, and in which direction, the loss changes when we slightly change the current parameter. **Gradient-based learning repeatedly uses this rate to choose an adjustment direction and a learning rate to set its size.**

## From Prediction to Loss

Consider a small model that predicts an output by multiplying its input by a fixed factor. The input is `x`, the factor to learn is parameter `w`, and the prediction is `ŷ`. The hat `^` distinguishes the prediction from the target.

\[
\hat y=wx
\]

Suppose one training example has `input x=1, target y=3`. If the current value is `w=2`, the prediction is `2×1=2`. The target stays fixed in the data; learning changes `w`.

Subtracting the target from the prediction gives the error `2−3=−1`. Defining the loss as the squared error assigns a positive value to both overprediction and underprediction.

\[
L(w)=(\hat y-y)^2=(w\times1-3)^2=(w-3)^2
\]

The current loss is therefore 1. This loss function is not a separate expression introduced without context: it **combines the model’s prediction rule, the target, and the rule for scoring errors**. Actual training usually averages losses over multiple examples; here we check the calculation with one example.

## Same Loss, Opposite Adjustments

At `w=2` and `w=4`, predictions lie on opposite sides of the target 3, and both losses are 1. Loss summarizes the size of the error without distinguishing the adjustment direction. The derivative `L′(w)=2(w−3)` reveals that difference.

| Current w | Prediction | Loss | Derivative | Small adjustment that reduces loss |
| --- | --- | --- | --- | --- |
| 2 | 2 | 1 | −2 | Increase w |
| 4 | 4 | 1 | 2 | Decrease w |
| 3 | 3 | 0 | 0 | Minimum in this example |

Moving from `w=2` to `2.1`, or from `w=4` to `3.9`, gives loss `0.81` in either case. Moving the other way to `1.9` or `4.1` raises the loss to `1.21`. Even with the same starting loss, the derivative’s sign changes the adjustment direction.

## Setting the Update Size with a Learning Rate

Basic gradient descent subtracts the derivative multiplied by a positive learning rate from the current value. The learning rate controls how much of the rate of change enters each update. Below it is written with the Greek letter eta, `η`.

\[
w_{\mathrm{new}}=w-\eta L'(w)
\]

With `w=2` and learning rate `η=0.1`, the update is `w_new=2−0.1×(−2)=2.2`. Subtracting a negative number increases the parameter. The new prediction is 2.2 and the new loss is `(2.2−3)²=0.64`. Starting at `w=4` instead gives `4−0.1×2=3.8`, with the same loss of 0.64.

On repeated updates, **recalculate the derivative at the changed parameter**. Do not keep using the initial value `−2`. Three updates starting at `w=2` give the following results.

| Updates completed | Current w = prediction | Current loss | Current derivative | Next update `−0.1×derivative` |
| --- | --- | --- | --- | --- |
| 0 | 2 | 1 | −2 | +0.2 |
| 1 | 2.2 | 0.64 | −1.6 | +0.16 |
| 2 | 2.36 | 0.4096 | −1.28 | +0.128 |
| 3 | 2.488 | 0.262144 | −1.024 | +0.1024 |

Row 0 is the state before training; the last row’s update would be used for the fourth step. The prediction approaches target 3, while the loss and the derivative’s absolute value decrease. Here `0.1` is not the travel distance itself. Its product with the derivative determines the actual parameter change.

## A Large Update Can Fail Despite the Right Direction

Keep the starting point `w=2` fixed and change only the learning rate.

| Learning rate η | New w | New loss | Result |
| --- | --- | --- | --- |
| 0.01 | 2.02 | 0.9604 | Small decrease |
| 0.1 | 2.2 | 0.64 | Decrease |
| 0.5 | 3 | 0 | Reaches this function’s minimum in one step |
| 1 | 4 | 1 | Crosses to the other side with unchanged loss |
| 1.1 | 4.2 | 1.44 | Overshoots and increases loss |

Differentiation gives information about changes near the current position. Even in a descent direction, moving too far can pass the minimum and increase loss. The good result with 0.5 above depends on this function’s shape; it does not make the same learning rate suitable for other models.

## Computing Gradients and Updating Parameters

With several parameters, use the gradient from the preceding section in place of the single derivative. The vector form of basic gradient descent is:

\[
\mathbf w_{\mathrm{new}}=\mathbf w-\eta\nabla L(\mathbf w)
\]

Each gradient component updates its corresponding parameter. In deep learning, loss is produced through computations across several layers, so we need an efficient way to obtain rates linking the loss to every parameter. **Backpropagation computes these gradients using the chain rule.** The chain rule connects rates of change through composed computations.

**An optimizer uses the computed gradients to update parameters.** The equation above is the simplest method; other optimizers may also use information from previous updates. Do not confuse gradient computation by backpropagation with parameter updates by the optimizer.

The diagram shows the first update of the same example. Learning repeats by predicting with the updated parameter and calculating the loss and gradient again.

```mermaid
--8<-- "assets/part-02/chapter-04/learning-adjustment-flow-en.mmd"
```

## Using Rates Instead of Trying Every Value

With one parameter, we could try every value in `w=0,1,2,3,4,5` and compare losses. Trying these six values for each parameter produces `6²=36` combinations for two parameters and `6¹⁰=60,466,176` for ten. Combinations grow rapidly even with just six discrete candidates per parameter.

Gradients use information at the current position instead of enumerating every combination. Backpropagation reuses intermediate computation results to calculate gradients efficiently for many parameters. Information at the current position alone, however, cannot guarantee a global minimum.

This discussion concerns learning methods that use differentiation. Not all AI learning requires derivatives; other methods search values or select rules without them.

## Training Loss and Performance on New Data

The example’s loss decreased steadily for one training case. Real training often computes gradients on a group of examples called a minibatch. Since the examples can change between updates, we should not expect the loss to decrease steadily at every step.

A lower training loss also does not guarantee better predictions on unseen data. The model may have fitted only the examples used for training. We must also check performance on validation data that do not enter parameter updates. Differentiation supplies information for reducing the chosen loss; whether that loss and those data represent the real goal requires a separate judgment.

## Exercise: Continue the Updates

Starting at `w=4` with `η=0.1`, calculate the parameter and loss after two updates. Compare this with reusing the initial derivative 2 in the second update.

??? note "Calculation and Explanation"
    The first update is `4−0.1×2=3.8`. The derivative is now `2×(3.8−3)=1.6`, so the second update gives `3.8−0.1×1.6=3.64`, with loss `0.64²=0.4096`. Reusing the old derivative 2 gives 3.6, which differs from gradient descent evaluated at the current position.

## Checklist

- Can you construct a loss function from a prediction rule and a target?
- Can you explain why equal losses can have derivatives of opposite signs?
- Can you calculate a new parameter using a learning rate and derivative?
- Can you explain why gradients are recalculated at the updated position?
- Can you distinguish backpropagation’s computation role from the optimizer’s update role?
- Can you distinguish lower training loss from better performance on new data?

## Sources and References

- Goodfellow, Bengio, Courville, [Deep Learning, Chapter 8](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }. Loss optimization, minibatches, and generalization.
- PyTorch, [Optimizing Model Parameters](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html){: target="_blank" rel="noopener noreferrer" }. Gradient computation and optimizer updates.

Checked: 2026-09-14. The numerical examples and diagram are original constructions.
