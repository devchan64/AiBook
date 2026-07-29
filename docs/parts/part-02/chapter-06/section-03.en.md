# P2-6.3 Intuition of Gradient Descent

> Section ID: `P2-6.3`
> Version: `v2026.07.26`

In P2-6.1, we looked at optimization as the problem of finding a better value, and in P2-6.2, we looked at how model wrongness is turned into a number called `loss`. Now the question becomes more concrete.

Once we have a number we want to reduce, we have to ask how to change the model's values.

`Gradient descent` is the representative answer to that question. The name sounds difficult, but the core is simple.

Here we reorganize `gradient descent`, `gradient`, `learning rate`, `update`, and `iteration`. If 6.2 was about reading loss and objective function, now we organize how parameters are moved little by little in order to reduce that value.

Rather than deriving the gradient-descent formula rigorously, this Section focuses on reading the repeated method of changing values little by little to reduce loss. If you secure the direction of the gradient, movement in the opposite direction, and the role of the learning rate here, then even when backpropagation and optimizers appear later, you can first understand why such calculations are needed.

## Return to the Shared Scene from 6.1 and 6.2

Keep the data from the previous Section as it is.

| Student | Study time `x` | Actual score `y` |
| --- | ---: | ---: |
| A | 1 | 55 |
| B | 2 | 65 |
| C | 3 | 80 |
| D | 4 | 90 |

And suppose we set the current candidate line as `\(\hat{y} = 8x + 45\)`. This line predicts the scores of students C and D somewhat too low. Now the question of gradient descent is: `if this loss is to decrease, in which direction and by how much should we move a and b?`

So the three Sections of Chapter 6 can be read as the following single flow.

1. 6.1: We have to compare candidate lines.
2. 6.2: The comparison criterion is loss.
3. 6.3: Move the candidate little by little in the direction where the loss decreases.

That is, we look at the direction in which loss increases from the current position, move a little in the opposite direction, look at loss again, and repeat this process.

Seen first on a loss curve, gradient descent is the method of repeating small movements in the direction where loss decreases from the current position.

![Flow of gradient descent moving in small steps toward lower loss on a loss curve](/AiBook/assets/part-02/chapter-06/gradient-descent-loss-curve-en.svg)

If we read this movement as a learning loop, it looks like this.

```mermaid
--8<-- "assets/part-02/chapter-06/gradient-descent-loop-flow-en.mmd"
```

## Core Criteria: the Intuition of Gradient Descent

- You can explain `gradient descent` as a repeated movement method for lowering loss.
- You can explain that the `gradient` is the direction information at the current position.
- You can explain why we move in the direction opposite the gradient.
- You can explain the `learning rate` as the value that determines how much to move at one time.
- You can explain the limitations and cautions of gradient descent at an introductory level.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Gradient descent repeats small movements toward the side where loss decreases | It shows that learning is not one leap to the answer but repeated adjustment. | Understand the structure that it moves little by little repeatedly. |
| We must move in the direction opposite the gradient | Since the gradient is the direction in which loss grows, we must read it opposite to our goal. | It is enough if you can explain why it becomes `descent`. |
| Learning rate determines the width of one movement | Even if the direction is correct, if the stride is wrong, learning can wobble or become slow. | Secure the feel of reading learning rate as the size of one step. |

## Mountain-Descending Metaphor Is Useful, but Not Complete

Gradient descent is often explained with the metaphor of walking down a mountain. You stand on a high place, look at the surrounding slope, and then go little by little in the direction that becomes lower.

This metaphor is good for first understanding. The current position corresponds to the current model parameters, the height corresponds to the loss value, and the direction of descent corresponds to the direction in which loss decreases.

But if we trust this metaphor too much, misunderstanding appears. In actual model learning, we do not see the whole map of the mountain at once. We read the direction near the current position, move a little, and then check again.

So gradient descent is not a method that jumps to the answer at once. It is a repeated method that tries to improve little by little using current information.

The same is true in the study-time and score example. If the current line predicts students C and D generally too low, then instead of pointing to the perfect line at once, we repeatedly check `does the loss go down if we increase slope a a little?` and `does it get better if we adjust intercept b a little?`

## Gradient Tells Us the Uphill Direction

The `gradient` is connected to the direction in which the function value increases fastest at the current position. If we think about the loss function, the gradient direction is the direction in which loss becomes larger.

In AI learning, we usually want to reduce loss. So we do not move exactly in the direction pointed to by the gradient. We move in the opposite direction. The gradient direction is the side where loss increases, and the direction opposite the gradient is the side where loss decreases.

This is the core of the word `descent`. We calculate the `gradient`, but the goal is not to go up. The goal is to go down.

For the reader, the important interpretation is this. If the current line generally predicts the scores too low, then to reduce loss we usually need to move in the direction that raises the predictions. In the actual calculation, the gradient gives that direction information numerically.

## We Must Move Only a Little

Even if we know the direction in which loss decreases, that does not mean we should jump far. The gradient at the current position is information about the neighborhood of the current position. If we move too far, we may overshoot instead of going to a lower place.

That is why gradient descent needs a `learning rate`. The learning rate is the value that decides how much to move at one time. If the learning rate is too small, movement becomes too slow. If it is appropriate, loss can decrease stably. If it is too large, we may pass a good position or make the loss wobble.

Here we understand the learning rate as `the size of one step`. Even if we know the direction, learning becomes difficult when the step is too large or too small.

For example, if we raise slope `a` too much at once, the error around student D may shrink, but around students A and B it may overshoot instead. Conversely, if we change it only a tiny amount, improvement becomes very slow even when we know the direction of reducing loss. The learning rate determines this stride.

## in Work, What Is Changed Little by Little?

If you think of gradient descent only as `a method for changing numbers inside an AI model`, it feels distant. From a work perspective, it means: there is a goal, we produce a result with the current setting, see numerically how bad that result is, change the setting a little in the direction where that number goes down, and then check again.

This structure can be thought through various work examples.

| Work situation | What we want to reduce | What is changed little by little | Gradient-descent perspective |
| --- | --- | --- | --- |
| ad-copy recommendation | how little it gets clicked, how low conversion is | scores of copy candidates, exposure order | repeatedly adjust which expressions create better results |
| product recommendation | how much irrelevant products are recommended | weights by product, representation of user preference | adjust user and product representations by looking at recommendation loss |
| demand forecasting | the gap between actual sales and predicted sales | weights of seasonality, price, event effects | change model values in the direction where prediction error decreases |
| defect detection | how often good products are treated as defective or defects are missed | importance of sensor values, decision boundary | move the criterion little by little so wrong decisions decrease |
| delivery-time prediction | the gap between actual arrival time and predicted arrival time | influence of distance, time slot, traffic variables | adjust the influence of variables in the direction where error decreases |

What matters here is that the person does not complete and insert every work rule one by one. The person sets the goal, the data, and the loss, and the model adjusts its internal values through repeated calculation. Completing rules directly such as `"if it rains, add 10 minutes"` is closer to a rule-based approach, while the model looking at loss and adjusting the influence of rain, distance, time slot, and traffic volume from data is closer to a learning-based approach.

This example does not mean that gradient descent automatically solves every work problem. In work, conditions such as data quality, goal setting, cost, safety, and explainability are also needed together. Gradient descent is the calculation method that answers `how should we change values in order to reduce the given loss?`

## Update Formula Is a Compressed Expression of the Movement Structure

Gradient descent is usually expressed by a formula like the following.

\[
\theta_{\text{new}}
=
\theta_{\text{old}}
-
\eta \nabla J(\theta)
\]

At first glance it looks complicated, but the reading method is simple.

| Symbol | Introductory meaning |
| --- | --- |
| \(\theta\) | the parameter the model adjusts |
| \(J(\theta)\) | the objective function we want to reduce |
| \(\nabla J(\theta)\) | the direction information of where loss increases at the current position |
| \(\eta\) | the learning rate, the size of one movement |
| \(-\eta \nabla J(\theta)\) | the amount of moving a little in the direction where loss decreases |

Here, rather than deriving the formula, we read the structure the formula is describing. In other words, read it as moving a little, by the learning rate, in the direction opposite the gradient from the current parameter.

If we read it through the shared scene, `\(\theta\)` is the line's `a` and `b`, and `\(J(\theta)\)` is the mean loss calculated across all four students. The formula is simply a compressed way of writing: `look at how badly the current line does not fit the data, then move a little toward the line that fits better`.

## Why Repetition Looks Like Learning

Gradient descent repeats the same thing.

1. Predict with the current parameters.
2. Calculate the loss.
3. Calculate the gradient.
4. Change the parameters a little.
5. Predict again.

This repetition looks like the core flow of `training`. Rather than the model understanding a concept by itself, it adjusts internal values in the direction where loss decreases.

The key thing the reader must understand here is the difference between `a human directly writing the correct line` and `adjusting the line little by little by looking at the loss`. The former is closer to directly writing rules, and the latter is closer to learning from data and loss.

What matters here is that the model does not receive the `correct rule` directly. The model predicts with the current parameters, looks at the loss, and changes the parameters using direction information. A way of directly writing the correct rule is closer to a rule-based approach, while adjusting parameters in the direction where loss decreases is closer to the basic flow of a learning-based approach.

## View It Through a Case

### Case 1. A Recommendation System That Does Not Fix Price by Rule, but Adjusts It Little by Little

Suppose an online service is adjusting product recommendation order. A person may first make rules such as `raise the score if it is similar to a product viewed recently` or `show discounted products more`.

But actual clicks and purchases are not that simple. For some users, brand matters more than discounts, and for others, seasonality may matter more than recent behavior. If a person tries to write every combination as a rule, it quickly becomes complex.

From the perspective of gradient descent, the model first produces recommendation scores, calculates the gap with actual responses as loss, and then adjusts internal weights little by little in the direction where that loss decreases. The reason it does not change everything a lot at once is that the direction information we are seeing now is trustworthy only near the current position.

This case lets us read gradient descent not as `a Section for memorizing formulas`, but as `a repeated procedure for looking at reactions and adjusting the criterion little by little`. At the same time, it also shows that if the learning rate is too large, recommendations can wobble, and if it is too small, the speed of improvement can become too slow.

## It Does Not Always Guarantee a Perfect Answer

Gradient descent is powerful, but it is not a method that automatically guarantees a perfect answer.

The result is affected by several conditions.

| Condition | Why it matters |
| --- | --- |
| initialization | the path can change depending on where we start |
| learning rate | if too small it is slow, if too large it can become unstable |
| loss landscape | valleys, flat regions, and multiple low points may exist |
| data | since loss is calculated from data, it is affected by data quality |
| iterations | if too few it learns too little, if too many it may overfit |

This connects to the point from 6.1 that `optimal does not mean perfect`. Gradient descent is a method that moves in a better direction within given criteria and conditions. It does not automatically solve every real-world condition.

## Checklist

- You can explain gradient descent as a repeated movement method for lowering loss.
- You can explain that the gradient is connected to the direction in which loss increases at the current position.
- You can explain that we move in the direction opposite the gradient to reduce loss.
- You can explain the learning rate as the size of one movement.
- You can read the gradient-descent update formula as the structure `move a little from the current value in the direction opposite the gradient`.
- You can explain that gradient descent is affected by initialization, learning rate, loss-function shape, data, and number of iterations.
- You can explain how `reducing loss` is connected to actually changing parameters.
- You can distinguish the gradient direction from movement in the opposite direction, and explain why both are needed.

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to support the deep-learning optimization context of cost functions, parameters, gradient-based movement, gradient descent, and learning rate.
- Stephen Boyd, Lieven Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2004, checked 2026-07-20. Used as supplementary support for optimization problems and gradient-based repeated movement in the mathematical optimization context.
