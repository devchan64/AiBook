# P2-6.2 Loss Functions and Objective Functions

> Section ID: `P2-6.2`
> Version: `v2026.09.15`

A loss function converts differences between predictions and actual values into numbers used for learning. The objective function is the overall criterion training minimizes or maximizes; it may add a penalty representing additional conditions to the mean loss.

## Line Predictions and Actual Scores

Consider a line model that predicts scores from study time.

| Student | Study time `x` | Actual score `y` |
| --- | ---: | ---: |
| A | 1 | 55 |
| B | 2 | 65 |
| C | 3 | 80 |
| D | 4 | 90 |

For the candidate line \(\hat{y} = 10x + 45\), the predictions are `55, 65, 75, 85`. The loss function quantifies how poorly this line fits.

That is, the model predicts, compares with the actual values, turns the degree of wrongness into a number, and then learns in the direction that reduces that number.

## Error and Squared Error

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

## Cancellation of Opposite-Sign Errors

You may think, `if the prediction is wrong by 2, can't we just use the error 2?` But `error` has direction. For example, for an actual value of 10, prediction 8 creates error 2, while prediction 12 creates error -2.

Both predictions are 2 away from the actual value. But the signs differ. If we simply add the errors of many samples, they can cancel each other out.

```text
2 + (-2) = 0
```

There were two wrong predictions, but the total becomes 0. That does not mean the model fit well. So the loss function turns error into a number usable for learning.

| Method | Calculation | Intuition |
| --- | --- | --- |
| absolute error | \(\lvert y - \hat{y}\rvert\) | looks at how far it is |
| squared error | \((y - \hat{y})^2\) | punishes large errors more strongly |
| log loss | negative logarithm of the correct-class probability | punishes confident wrong probability predictions strongly |

## Probability Assigned to the Correct Class and Log Loss

A classifier predicts probabilities for possible classes. Compare assigning spam probability 0.9 versus 0.1 to an email whose correct class is spam. For classification with one correct class, the individual log loss is `−ln(predicted probability of the correct class)`. Here `ln` is the natural logarithm. The logarithm of a probability strictly between 0 and 1 is negative, so we place a minus sign in front.

| Probability assigned to the correct class, spam | Individual log loss | Interpretation |
| --- | --- | --- |
| 0.9 | `−ln(0.9) ≈ 0.105` | High probability for the correct class |
| 0.5 | `−ln(0.5) ≈ 0.693` | Equal probabilities for the two classes |
| 0.1 | `−ln(0.1) ≈ 2.303` | Low probability for the correct class |

As the probability assigned to the correct class approaches 1, loss approaches 0; as it approaches 0, loss becomes very large. Unlike accuracy, which counts correct and incorrect decisions, log loss also reflects the probability assigned to the correct class. For example, with a spam threshold of 0.5, both 0.6 and 0.9 give correct decisions, but their log losses differ.

## Mean Squared Error

Training data usually does not contain only one sample. We predict for many samples and calculate the loss of each sample.

The predictions and losses for the four students are:

| Student | Actual score | Predicted score | Actual − predicted | Squared error |
| --- | --- | --- | --- | --- |
| A | 55 | 55 | 0 | 0 |
| B | 65 | 65 | 0 | 0 |
| C | 80 | 75 | 5 | 25 |
| D | 90 | 85 | 5 | 25 |

The individual losses are `0, 0, 25, 25`, and the mean squared error (MSE) is `(0 + 0 + 25 + 25) / 4 = 12.5`. This mean allows comparison with other candidate lines on the same data.

Written a little more generally, it becomes the following.

\[
\mathrm{MSE}(y, \hat{y}) =
\frac{1}{n}
\sum_{i=1}^{n}
(y_i - \hat{y}_i)^2
\]

Sigma compresses the calculation of summing squared errors across samples. Here n is the sample count and i identifies a sample. Summing the squared errors and dividing by n gives the mean loss per sample. MSE itself is also called a loss function, so use the formula and context to distinguish individual from mean loss.

## Mean Loss and Regularization Penalties

`Loss function` and `objective function` are often used together. Here we distinguish them as follows: the loss function is the function that calculates how wrong a prediction is, while the objective function is the overall criterion training actually tries to reduce or increase.

In many cases, the objective function is the mean loss.

```text
objective = average loss
```

But it is not always that simple. For example, we may add a penalty so that the model does not become too complex.

```text
objective = average loss + regularization penalty
```

Suppose we add `0.2a²` to the mean loss to discourage an excessively large slope `a`. In this example, the intercept `b` is not penalized.

| Candidate line | Mean loss | Penalty 0.2a² | Objective value |
| --- | --- | --- | --- |
| a = 10, b = 45 | 12.5 | 20 | 32.5 |
| a = 12, b = 40 | 7.5 | 28.8 | 36.3 |

The second candidate has lower mean loss, but the first has the better objective value when the penalty is included. To understand what training minimizes, inspect the regularization term as well as the loss.

Writing the penalty strength as `λ` (lambda), the objective is `mean loss + λa²`. The setting `λ≥0` controls the relative weight of the two terms. With `λ=0`, only mean loss matters; increasing λ assigns more cost to a large slope. In this example, λ is specified separately from the learned parameters `a, b`.

| λ | Candidate 1: a=10, b=45 | Candidate 2: a=12, b=40 | Smaller objective among the two |
| --- | --- | --- | --- |
| 0 | 12.5 | 7.5 | Candidate 2 |
| 0.1 | 22.5 | 21.9 | Candidate 2 |
| 0.2 | 32.5 | 36.3 | Candidate 1 |

A penalty differs from a constraint that forbids a from exceeding a limit. It charges a cost for a large a rather than prohibiting it. A larger λ does not guarantee better performance on new data. An excessively strong penalty may prevent the model from following variation in the data, so its effect should be checked on validation data.

The mean loss and penalty in the diagram are separate terms. Their sum is the objective minimized in this example.

```mermaid
--8<-- "assets/part-02/chapter-06/loss-objective-flow-en.mmd"
```

## Training Loss and Performance on New Data

When the loss decreases, that is usually a good signal. It means the model's predictions fit better under the training data criterion.

But we should not conclude from low loss alone that the model is also good in reality. The loss may be low only on the training data, it may not fit new data well, the service goal and the loss function may differ, and constraints such as safety, fairness, and cost may not be fully expressed by a single loss.

Training loss is calculated on the data we have. It does not fully guarantee performance in the real world.

Training usually separates training, validation, and test data.

## Loss Functions and Evaluation Metrics

The `loss function` is used to adjust model values during the learning process. A `metric` is used so that humans can interpret and compare model results.

In some cases, the two are the same. For example, both training and evaluation may use MSE.

But they can also be different. For example, training may reduce `log loss`, while the report looks at `accuracy`, `precision`, and `recall`, and the real service may additionally look at cost, latency, and risk.

This difference is important in practice. If the number the model reduces during learning and the number humans actually care about are different, the model can improve in the wrong direction.

The same distinction is possible even in the study-time and score example. Learning may find the line with the lower mean loss, but a person may separately ask interpretive questions such as `does it miss high-scoring students especially often?` or `does it generally predict scores too low?` Loss is the compass of learning, and evaluation is the place where humans read the result.

## Mean Loss and Maximum Delivery Error

Suppose the actual delivery time for each of three orders is 60 minutes.

| Model | Predicted delivery times | Squared errors | MSE | Maximum absolute error |
| --- | --- | --- | --- | --- |
| A | 55, 55, 55 minutes | 25, 25, 25 | 25 | 5 minutes |
| B | 60, 60, 52 minutes | 0, 0, 64 | About 21.33 | 8 minutes |

B has lower MSE, but A has a smaller error on its worst prediction. If the service separately counts `orders with prediction errors exceeding 6 minutes`, A has none and B has one. Improving training loss does not necessarily improve other operational metrics.

## Recalculating Penalties and Evaluation Criteria

1. Calculate the objective for both candidate lines with `λ=0.05` and choose the smaller one.
2. What is the log loss when a spam email is assigned spam probability 0.6? How does it compare with probability 0.9, even though both yield the same accuracy outcome? Use a spam threshold of 0.5.
3. In the delivery example, how many orders have absolute errors exceeding 4 minutes for A and B? Does the choice change from the 6-minute criterion?

**Answers:** ① Candidate 1 gives `12.5+0.05×100=17.5`; candidate 2 gives `7.5+0.05×144=14.7`, so candidate 2 is smaller. ② `−ln(0.6)≈0.511`. Both probabilities give correct spam decisions, but the loss at 0.9, approximately 0.105, is smaller. ③ A has 3 orders and B has 1, so minimizing this count favors B. At 6 minutes, A has none and B has 1, favoring A. The threshold as well as the name of an evaluation criterion affects the choice.

## Checklist

- You can explain the `loss function` as a function that turns prediction wrongness into a number.
- You can calculate squared error using the difference between actual value \(y\) and prediction \(\hat{y}\).
- You can explain that mean squared error is the average of the losses of several samples.
- You can explain the `objective function` as the criterion training actually tries to optimize.
- You can explain that loss function and `metric` are not always the same.
- You can explain that low loss is a good signal but does not automatically guarantee real-world performance.
- You can distinguish individual error, mean loss across several samples, and the objective function of the whole learning process.

- You can distinguish low loss from the judgment that a model is good for actual operations.

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to confirm that deep learning training reduces a cost function written as an average of per-example losses over training data.
- scikit-learn developers, [3.4. Metrics and scoring: quantifying the quality of predictions](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, checked 2026-07-20. Used to confirm scoring/metric choices for evaluating prediction quality and the point that a loss function and evaluation metric may be the same or different.
- scikit-learn developers, [mean_squared_error](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.mean_squared_error.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, checked 2026-07-20. Used to confirm mean squared error as a regression loss between `y_true` and `y_pred`, where the best value is 0.
- scikit-learn developers, [log_loss](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, checked 2026-09-15. Used to confirm that log loss is also called logistic loss or cross-entropy loss and is applied to predicted probabilities.
