# P2-4.4 Why Learning Needs Differentiation

> Section ID: `P2-4.4`
> Version: `v2026.07.20`

In P2-4.3, we looked at derivative, partial derivative, and gradient as `the language for reading how values change`. Now we connect why that language becomes necessary in AI training.

The conclusion of this Section is simple.

1. Loss tells us how wrong the current model is.
2. Differentiation and gradients tell us in which direction to change values so that loss decreases.

What matters in learning is not writing the correct answer all at once. It is seeing the current model result, adjusting parameters a little at a time, and reducing the loss. The tool that tells us `if we change it a little, how does the result change?` is differentiation.

This Section reorganizes training, loss, parameter, update direction, and backpropagation. If P2-4.3 read the gradient, now we organize why that information about change becomes necessary for an actual learning procedure.

Here, rather than unfolding optimization formulas in detail, the focus is on connecting why differentiation and gradients are needed in learning. If we hold onto the relationship among loss, parameters, and update direction, then later, when reading gradient descent, backpropagation, and optimizer, we read the purpose before the calculation procedure.

## Goals of This Section

- You can explain training as the process of reducing loss by adjusting parameters.
- You can explain that the loss value alone makes it hard to know in which direction to change things.
- You can explain that derivatives and gradients give directional information about how loss changes.
- You can preview backpropagation as `the procedure that computes gradients efficiently`.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| Learning is the process of adjusting parameters | The model improves by looking at the current result and changing internal numbers a little at a time. | Understand learning as the repetition of `prediction -> loss calculation -> parameter adjustment`. |
| Loss alone does not tell the direction | It shows how wrong things are, but not where to move. | Understand that loss tells only size, while update direction is a separate need. |
| Derivatives and gradients give directional information | We must judge in which direction to change parameters so that loss decreases. | Understand that a derivative gives information for one parameter and a gradient gives directional information for many parameters. |

## Learning Is the Process of Adjusting Values

An AI model receives an input and makes an output. Before learning, the model may not yet produce good outputs. So we use training data to adjust the parameters inside the model.

1. Input data enters.
2. The model makes a prediction.
3. We calculate the loss.
4. We adjust the parameters.
5. We predict again.

Here, a parameter is not a rule that a person manually sets every time. It is a number that the model adjusts through learning. Learning can be read as the process of changing these numbers and finding the direction that reduces loss.

If we rewrite this structure in practical language, it means repeatedly looking at the current result, scoring how bad it is, judging what to change and in which direction, changing it a little, and checking again.

In this repetition, differentiation enters in judging `what should be changed and in which direction`.

## Loss Tells the Size of Badness

Loss is a value that expresses numerically how different the model's prediction is from the target.

For example, in a model that predicts house prices, if the real house price is 500 million won but the model predicts 400 million won, the error is 100 million won.

If we score that error in some way, it becomes loss. If the loss is large, we can say the model's prediction is not good. If the loss is small, we can say the prediction is better by the current standard.

But the loss value alone is not enough.

If the loss is large, we know the current result is not good. But we still do not know what should be changed or how.

Learning needs questions such as: which parameter makes the loss decrease, should that parameter be increased or decreased, and how sensitively does the loss change when we adjust it a little?

Derivative and gradient are the language for answering these questions.

## Differentiation Lets Us Read the Update Direction

As a very simple example, suppose the loss changes with one parameter \(w\) like this.

\[
L(w) = (w - 3)^2
\]

This function has loss 0 when \(w = 3\). In real learning, we do not know such an answer in advance, but here we use it as an intuition-building example.

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

This explanation leads to the intuition of gradient descent. But here, we do not memorize the update formula. We only hold onto the point that `differentiation lets us read the direction that reduces loss`.

## If There Are Many Parameters, a Gradient Is Needed

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

## We Cannot Test Every Possible Value

The reason differentiation is needed also connects to the question `could we not just try all possible values?`

In a small problem, we can substitute several values directly. For example, we can try `w = 0, 1, 2, 3, 4, 5` and choose the value with the smallest loss.

But once the number of model parameters grows, the number of possible combinations increases extremely quickly. Testing every value becomes unrealistic.

Instead of checking every possibility, the gradient tells us which direction from the current position may reduce loss.

Trying every road is too expensive. So in real learning, we need the gradient to read the descending direction from the current position.

Of course, that does not mean the gradient always guarantees the globally best answer. A gradient gives information about change near the current position. So in real learning, the initial value, learning rate, data, model structure, and optimizer all matter together.

## Why Does Backpropagation Appear?

A deep-learning model is a structure in which calculations across many layers are connected. The input passes through many calculations, becomes an output, and from that output we calculate loss.

We can read it as a flow such as `input -> layer 1 calculation -> layer 2 calculation -> layer 3 calculation -> output -> loss`.

To learn, we must know how the loss changes with respect to the parameters of each layer. In other words, we need gradients for many parameters.

Backpropagation can be understood as the procedure for computing those gradients efficiently. Because of its name, it can feel like `learning itself`, but here we separate it as follows.

Training is the whole process of adjusting parameters so that loss decreases, while backpropagation is the procedure that computes and passes along the gradients needed for that adjustment.

The detailed calculation of backpropagation is treated in the deep-learning part. Here, only remember `why differentiation continues into backpropagation`.

## Read It in Sentences Heard in Practice

In practice, we may hear the following expressions more often than the word differentiation itself.

| Practical Expression | How to Read It by Connecting It to Differentiation |
| --- | --- |
| loss does not decrease | the current adjustment direction or size may not be good |
| the learning rate is too large | moving too far at once may make loss unstable |
| the gradient is small | the change signal may be weak at the current position |
| the gradient explodes | the change signal may be too large, making learning unstable |
| backpropagation is needed | we must calculate the rates of change with respect to parameters across many layers |

All of these expressions are treated in more detail later. For now, only remember that practical terms eventually connect to `information about change for reducing loss`.

## View It Through a Case

### Case 1. A House-Price Prediction Model Is Not Fixed Just by Knowing It Was Wrong

Suppose we operate a house-price prediction model. In a validation result, the real price of a house is 500 million won, but the model predicted 400 million won. A person can immediately confirm the fact that `it was wrong by 100 million won`.

But that number alone does not tell us how to fix the model. We still do not know whether area should be reflected more strongly, whether location information should be read more sensitively, or whether some parameter should be increased or decreased. Loss tells us `how wrong it is`, but it does not tell us `where to move`.

At that point, derivative and gradient take the role. If we inspect whether loss decreases or increases when parameters are changed a little, we can judge in which direction the model should adjust in the next step. In other words, learning is not the process of finding the answer at once, but the repetition of looking at how wrong it is, reading directional information, and correcting a little at a time.

A checkable result is to compare whether the loss really decreases when a specific parameter is adjusted slightly on the same validation sample. If the loss falls from 0.82 to 0.76, that adjustment was a direction of improvement. If it rises to 0.90 instead, we read that the direction was wrong.

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

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }. It supports the relation between derivative and instantaneous rate of change. Checked: 2026-07-20.
- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }. It supports the relation between the gradient and the direction of maximum increase. Checked: 2026-07-20.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8. Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }. It treats deep learning training as cost-function and parameter optimization, and gives the context for gradient-based optimization in training. Checked: 2026-07-20.
