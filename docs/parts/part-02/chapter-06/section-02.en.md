# P2-6.2 Loss Functions and Objective Functions

> Section ID: `P2-6.2`
> Version: `v2026.07.23`

In P2-6.1, we looked at optimization as `placing candidates, comparing them by a criterion, and finding a better value within constraints`. Now we look at what name that criterion takes inside model learning.

The model does not know from the beginning `how wrong it is`. So a person first has to decide on a criterion that turns wrongness into a number. That criterion is the `loss function`.

Here we reorganize `loss function`, `objective function`, `error`, `mean loss`, and `metric`. If 6.1 was about reading the problem of finding a better value, now we organize what criterion learning actually moves by.

Rather than memorizing many loss-function formulas, this Section focuses on reading what criterion learning actually moves by. If you secure the difference among loss function, mean loss, and objective function here, then even when gradient descent and backpropagation appear later, you can keep following `what is being reduced`.

## Return to the Shared Scene from 6.1

We bring back the data from the previous Section as it is.

| Student | Study time `x` | Actual score `y` |
| --- | ---: | ---: |
| A | 1 | 55 |
| B | 2 | 65 |
| C | 3 | 80 |
| D | 4 | 90 |

If we place one candidate line as `\(\hat{y} = 10x + 45\)`, the predicted values become `55, 65, 75, 85`. In this scene, the role of the loss function is to turn `how badly this line does not fit` into a number. In other words, the `candidate comparison` of 6.1 becomes concrete here as `loss calculation`.

That is, the model predicts, compares with the actual values, turns the degree of wrongness into a number, and then learns in the direction that reduces that number.

```mermaid
--8<-- "assets/part-02/chapter-06/loss-objective-flow-en.mmd"
```

## Core Criteria: Loss Function and Objective Function

- You can explain the `loss function` as a function that turns prediction wrongness into a number.
- You can explain the `objective function` as the overall criterion training tries to reduce or increase.
- You can distinguish the loss of an individual sample from the mean loss across many samples.
- You can calculate the intuition of mean squared error (MSE) with small numbers.
- You can explain that loss function and metric are not always the same.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Loss is the value that turns how wrong the model is into a number | It shows that learning moves not by intuitive judgment but on top of a computable criterion. | Understand the role of turning wrongness into a number. |
| The losses of many samples are combined to see the whole tendency | We need to see performance across data overall, not only one accidental prediction. | It is enough if you can explain why mean loss is needed. |
| Loss function and metric may be the same or different | If we confuse the learning criterion and the real operational judgment criterion, interpretation goes wrong. | Secure the feel of separating training numbers from reporting numbers. |

## Loss Turns Wrongness into a Number

Saying that a model's prediction is wrong feels natural to a person, but it is not a statement the computer can directly use. If the computer is to adjust values, wrongness must be expressed as a number.

For example, suppose the actual value is 10 and the model's prediction is 8.

```text
actual value: 10
prediction: 8
error: 10 - 8 = 2
```

The `error` is 2. But in learning, we do not use the raw error as it is. We change it in a way that fits the problem, such as squaring it, taking its absolute value, or applying a logarithm to a probability. The function used at that time is the `loss function`.

The easiest example is `squared error`.

\[
\mathrm{loss} = (y - \hat{y})^2
\]

Here, \(y\) is the actual value and \(\hat{y}\) is the model's predicted value.

```text
actual y = 10
prediction y_hat = 8
loss = (10 - 8)^2 = 4
```

This number 4 is the result of turning `how wrong it is` into a computable value. Now the model can adjust its values in the direction that reduces this number.

If we reread it through the common scene, then for each student we calculate `actual score - predicted score` and turn that error into a loss such as squared error. The loss function is ultimately the device that turns `how badly the candidate line does not fit the data` into a comparable number.

## Why Not Just Use the Error Directly?

You may think, `if the prediction is wrong by 2, can't we just use the error 2?` But `error` has direction. For example, for an actual value of 10, prediction 8 creates error 2, while prediction 12 creates error -2.

Both predictions are 2 away from the actual value. But the signs differ. If we simply add the errors of many samples, they can cancel each other out.

```text
2 + (-2) = 0
```

There were two wrong predictions, but the total becomes 0. That does not mean the model fit well. So the loss function turns error into a number usable for learning.

| Method | Calculation | Intuition |
| --- | --- | --- |
| absolute error | \(|y - \hat{y}|\) | looks at how far it is |
| squared error | \((y - \hat{y})^2\) | punishes large errors more strongly |
| log loss | apply a logarithm to probability prediction | punishes confident wrong probability predictions strongly |

Here we calculate only squared error. Why loss functions differ in classification and regression is revisited in P4-4.1 and P4-4.2, and an introductory reading of log loss itself connects again in the supplementary learning of P3-6.4.

## Combine the Losses of Many Samples into One

Training data usually does not contain only one sample. We predict for many samples and calculate the loss of each sample.

For example, suppose there are three samples.

| Sample | Actual value \(y\) | Prediction \(\hat{y}\) | Squared error |
| --- | ---: | ---: | ---: |
| 1 | 10 | 8 | 4 |
| 2 | 5 | 6 | 1 |
| 3 | 7 | 4 | 9 |

The loss differs by sample. In learning, we have to combine these losses into one criterion. The simplest method is to take the mean.

\[
\mathrm{MSE} = \frac{4 + 1 + 9}{3} = \frac{14}{3} \approx 4.67
\]

This `mean squared error` summarizes the wrongness of several predictions into one number.

In the earlier line example too, if we average the losses from student A through D, we can produce one overall score for the line `\(\hat{y} = 10x + 45\)`. Now we can directly compare mean loss with another candidate line, and this comparability connects optimization and learning.

Written a little more generally, it becomes the following.

\[
\mathrm{MSE}(y, \hat{y}) =
\frac{1}{n}
\sum_{i=1}^{n}
(y_i - \hat{y}_i)^2
\]

Here the sigma means, as we saw in P2-2.2, that we repeat the same calculation across several samples and add the results. When the loss function meets sigma, it becomes a number that means `how wrong it is across the whole dataset`.

## The Objective Function Is the Criterion Learning Actually Moves By

`Loss function` and `objective function` are often used together. Here we distinguish them as follows: the loss function is the function that calculates how wrong a prediction is, while the objective function is the overall criterion training actually tries to reduce or increase.

In many cases, the objective function is the mean loss.

```text
objective = average loss
```

But it is not always that simple. For example, we may add a penalty so that the model does not become too complex.

```text
objective = average loss + regularization penalty
```

You do not need to understand this formula in detail now. What matters is that the objective function is `the criterion the learning process actually tries to optimize`. The loss function often becomes the main ingredient of that criterion.

For the reader, it is important to separate `how wrong is it for one student` from `how badly does this candidate line fit across all four students`. The former is individual loss, and the latter continues toward mean loss or the objective function.

## Low Loss Is a Good Signal, but Not a Sufficient Conclusion

When the loss decreases, that is usually a good signal. It means the model's predictions fit better under the training data criterion.

But we should not conclude from low loss alone that the model is also good in reality. The loss may be low only on the training data, it may not fit new data well, the service goal and the loss function may differ, and constraints such as safety, fairness, and cost may not be fully expressed by a single loss.

The perspective of sample and error that we saw in P2-5.3 returns here. The loss of training data is a value calculated from the data we have. It does not fully guarantee performance in the whole real world.

So in learning, we usually divide training data, validation data, and test data. This data split is handled in more detail later in the machine-learning Part.

## Loss Function and Metric May Be the Same or Different

The `loss function` is used to adjust model values during the learning process. A `metric` is used so that humans can interpret and compare model results.

In some cases, the two are the same. For example, both training and evaluation may use MSE.

But they can also be different. For example, training may reduce `log loss`, while the report looks at `accuracy`, `precision`, and `recall`, and the real service may additionally look at cost, latency, and risk.

This difference is important in practice. If the number the model reduces during learning and the number humans actually care about are different, the model can improve in the wrong direction.

The same distinction is possible even in the study-time and score example. Learning may find the line with the lower mean loss, but a person may separately ask interpretive questions such as `does it miss high-scoring students especially often?` or `does it generally predict scores too low?` Loss is the compass of learning, and evaluation is the place where humans read the result.

## View It Through a Case

### Case 1. What Loss Does in Delivery-Time Prediction

Suppose a delivery service predicts arrival time for each order. A person can explain that conditions such as `downtown Seoul`, `rush hour`, `rainy day`, and `logistics-center congestion` are related to delay, but it is hard to set by hand how many minutes each condition affects every time.

So the model first predicts arrival time for each order and then compares it with the actual arrival time. For example, if the actual arrival is 60 minutes and the prediction is 50 minutes, there is a 10-minute gap. The loss function turns this gap into a number usable for learning.

What matters here is that `how wrong the model is` is examined not for one order alone but across many orders together. One specific order can miss badly by chance, but if the overall loss goes down, that is a signal that the model is being adjusted in a better direction across the data as a whole.

Also, the criterion the service operations team actually cares about may not end with one mean error. Separate metrics such as VIP-customer delay, overnight-delivery failure, or regional deviation may be more important. This case shows why loss function and metric can be the same or different.

## Checklist

- You can explain the `loss function` as a function that turns prediction wrongness into a number.
- You can calculate squared error using the difference between actual value \(y\) and prediction \(\hat{y}\).
- You can explain that mean squared error is the average of the losses of several samples.
- You can explain the `objective function` as the criterion training actually tries to optimize.
- You can explain that loss function and `metric` are not always the same.
- You can explain that low loss is a good signal but does not automatically guarantee real-world performance.
- You can distinguish individual error, mean loss across several samples, and the objective function of the whole learning process.

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to confirm that deep learning training reduces a cost function written as an average of per-example losses over training data.
- scikit-learn developers, [3.4. Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, checked 2026-07-20. Used to confirm scoring/metric choices for evaluating prediction quality and the point that a loss function and evaluation metric may be the same or different.
- scikit-learn developers, [mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, checked 2026-07-20. Used to confirm mean squared error as a regression loss between `y_true` and `y_pred`, where the best value is 0.
- scikit-learn developers, [log_loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, checked 2026-07-20. Used to confirm that log loss is also called logistic loss or cross-entropy loss and is applied to predicted probabilities.
