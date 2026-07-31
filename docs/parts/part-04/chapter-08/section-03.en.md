# P4-8.3 Supplementary Learning: How To First Set A Baseline By Problem Type

> Section ID: `P4-8.3`
> Version: `v2026.07.31`

When setting the first baseline, first write `problem_type`, `simple_rule`, `metric`, `known_easy_case`, and `known_hard_case`. Classification, regression, and time series have different baseline candidates, but the shared purpose is to place an easy standard and representative failure scene in the same table before looking at complex models.

If P4-8.2 showed why a [baseline is needed](/AiBook/en/reference/concept-glossary-alpha/b/#baseline-model), then the next question immediately appears.

So how is a baseline actually set?

This supplementary learning answers that question. Its goal is not to memorize many baseline names, but to enable the reader to look at the problem type and directly choose `the simplest standard that still carries comparison meaning`.

## Problem Types That Split Baseline Choices

This Section handles how to first set representative baselines in [classification](/AiBook/en/reference/concept-glossary-alpha/c/#classification), [regression](/AiBook/en/reference/concept-glossary-alpha/r/#regression), and time-series problems.

- What should be fixed first before setting a baseline?
- What baseline can be brought to mind first depending on problem type?
- After setting a baseline, with what cases and exercises should comparison begin?
- After seeing the baseline score, what should be checked next?

This Section first settles `how to set the simplest baseline that still carries comparison meaning by problem type`. Cross-validation, model-comparison procedures, and more complex tuning methods continue after P4-9.

## Judgments To Keep From Baselines By Problem Type

- You can distinguish representative baseline candidates in classification, regression, and time series.
- You can explain the baseline-setting procedure in the order `fix the problem type -> choose the simplest rule -> measure with the same metric -> inspect errors -> decide the next comparison`.
- You can explain why cases and exercises should be attached immediately after the baseline explanation.
- You can say to what next question the reader should proceed after seeing the baseline score.

## First Fix The Baseline-Setting Procedure

It is safer to set a baseline not as a temporary rule chosen by intuition, but as a procedure for choosing `the simplest standard in the current problem that still carries comparison meaning`.

The shortest procedure can be fixed in the following order.

1. Fix the problem type first.
2. Choose the simplest rule that uses features very little.
3. Measure the baseline on the same metric as the candidate model.
4. Look not only at the score, but also at representative error scenes.
5. Only after interpreting how much better it is than the baseline should the reader move to tuning or changing candidates.

If this order is grouped again in a table, it becomes the following.

| Baseline design order | Question to ask now | Why it is needed |
| --- | --- | --- |
| 1. fix the problem type | is it classification, regression, or time series | because the form of the baseline itself changes here |
| 2. choose the simplest rule | is it majority class, mean/median, or previous value | because the reader must first set the minimum standard that uses features very little |
| 3. measure with the same metric | should it be judged by accuracy, recall, MAE, or MAPE | because the baseline and candidate model must be compared with the same [metric](/AiBook/en/reference/concept-glossary-alpha/m/#metric) |
| 4. inspect error scenes | what is it especially missing or getting badly wrong | because it is hard to read the direction of improvement from score difference alone |
| 5. decide the next step after interpretation | should the reader tune, change candidates, or revisit features | so that a candidate that cannot beat the baseline is not held onto for too long |

In other words, the core of baseline methodology is not `make the easiest rule`, but `place the easiest rule inside the same comparison frame`.

## Representative Baseline Map By Problem Type

Representative baselines begin from different starting points depending on problem type.

| Problem type | Baseline to bring to mind first | Why it is often used first |
| --- | --- | --- |
| classification | majority-class prediction | because it reveals high-accuracy illusions the fastest |
| classification | dummy prediction based on class proportions | because it distinguishes simple distribution-following from actual learning |
| regression | mean prediction | because it shows the default error that appears even without input features |
| regression | median prediction | because it can become a more stable standard when there are many extreme values |
| time series | naive prediction | because it is the simplest time-order standard that reuses the previous value directly |
| time series | seasonal naive prediction | because when seasonality is strong, the previous value from the same season can be used as the standard |

This table is not an answer list of baselines, but a map that quickly organizes `what should be set as the comparison line first`. On the time-series side, methods such as naive and seasonal naive are directly explained in public teaching material such as Hyndman et al. as representative `simple forecasting methods`.

## How Is A Baseline Set In Classification?

In classification, readers can first think of baselines such as the following.

| Baseline form | Meaning | Scene where it is good to use first |
| --- | --- | --- |
| always predict the most common class | majority-class standard | problems with strong class imbalance |
| random prediction according to class proportions | distribution-level standard | when readers want to distinguish following the distribution from actual learning |
| always predict the same class | the absolute minimum floor line | when readers are first fixing how to interpret the metric itself |

Consider a case where churn is rare in customer-churn prediction. A baseline that says `always non-churn` can produce high accuracy. But churn recall can become 0. That is why the first role of a classification baseline is not to answer `is the score high`, but to reveal first `what illusion is being created`.

## Cases And Examples

### Case 1. Why A Majority-Class Baseline Is Set First In Customer-Churn Prediction

A subscription-service team is trying to predict customer churn next month. Suppose the data contain 90% non-churn customers and 10% churn customers.

If the baseline predicts `always non-churn`, accuracy can become 90%. But what matters is that it catches no churn customers at all. So if the reader looks only at the actual model's accuracy of 91% without the baseline, the reader ends up saying `it improved by 1 percentage point`. But once the baseline is placed beside it, the first question becomes `is it still catching almost none of the important customers`.

| Item | Content |
| --- | --- |
| problem | predict whether a customer will churn next month |
| class distribution | non-churn 90%, churn 10% |
| baseline | always predict `non-churn` |
| metric to look at first | accuracy, [recall](/AiBook/en/reference/concept-glossary-alpha/r/#recall), F1 |
| error to check immediately | cases where actual churn customers were missed |

```mermaid
--8<-- "assets/part-04/chapter-08/p4-8-3-mermaid-01-en.mmd"
```

The key point of this case is that the baseline matters not because it is a low model, but because it is `the standard that immediately reveals the accuracy illusion`.

### Small Example: Reading A Classification Baseline Numerically

If the baseline and actual model are placed side by side on the same data as follows, the role of the baseline becomes clearer.

| Model | accuracy | recall | F1 | Reading |
| --- | ---: | ---: | ---: | --- |
| baseline: always non-churn | 0.90 | 0.00 | 0.00 | Even if accuracy looks high, it catches none of the important customers. |
| candidate model | 0.94 | 0.50 | 0.63 | The reader can see whether it has actually started catching real churn better than the baseline. |

The questions for reading this table are simple.

- Is the difference in accuracy actually meaningful?
- How much did recall and F1 change from the baseline?
- What kinds of churn customers are still being missed?

## How Is A Baseline Set In Regression?

In regression, the following baselines can be placed first.

| Baseline form | Meaning | Scene where it is good to use first |
| --- | --- | --- |
| predict the mean for every sample | most basic central-value standard | when the reader first checks whether input features really help |
| predict the median for every sample | a standard less sensitive to extreme values | when there are many outliers |
| predict a specific constant value | a domain-fixed standard | when there is already a standard line used in the field |

The core of a regression baseline is to first create the starting point that says `this much error appears even when there is no input`.

### Case 2. Why A Mean Baseline Comes First In Delivery-Time Prediction

A logistics team wants to predict delivery time. Before building a model that uses region, distance, volume, and weather information, it first places `a baseline that predicts only the average delivery time`.

The purpose of this baseline is not that average prediction is excellent. It is to check how much the model using input features actually reduces error compared with the average standard.

| Item | Content |
| --- | --- |
| problem | delivery-time prediction |
| baseline | predict the average delivery time for every order |
| metric to look at first | MAE, RMSE |
| error to check immediately | large-error regions such as long-distance delivery and bad-weather delivery |

For example, if the MAE of the mean baseline is 18 minutes and the MAE of the candidate model is 15 minutes, the next question becomes `is a reduction of 3 minutes operationally meaningful`. To answer that, the reader should look not only at the overall average but also at in what order groups the error actually decreased.

### Small Example: Reading A Regression Baseline Numerically

| Model | MAE | RMSE | Reading |
| --- | ---: | ---: | --- |
| baseline: average delivery time | 18.0 | 24.5 | This is the starting point without looking at the input. |
| candidate model | 15.0 | 20.8 | It reduced error over the baseline, but the reader still needs to inspect in what order groups the reduction happened. |

When reading this table, it is safer to also write down the following together.

- Which order groups saw large errors reduced?
- Did it improve not only on average, but also in important regions?
- Does the reduced error over the baseline lead to operational cost reduction?

## How Is A Baseline Set In Time Series?

In time-series problems, rather than erasing time order completely, it is often more natural to set a simple standard that reflects time structure at least minimally.

| Baseline form | Meaning | Scene where it is good to use first |
| --- | --- | --- |
| naive | predict the next value by the previous value | time series where change is slow |
| seasonal naive | use the value from the same weekday of the previous week, or the same month of the previous year | time series with seasonality or periodicity |
| mean method | use the overall mean as the standard for the next value | when a simple comparison start is needed and time structure is weak |

### Case 3. Why Seasonal Naive Comes First In Daily Visitor Forecasting

An e-commerce team wants to forecast daily visitors. If the pattern difference between Mondays and weekends is large, it is more natural to use `the value from the same weekday last week` as the next standard than to use a simple mean.

| Item | Content |
| --- | --- |
| problem | predict tomorrow's visitor count |
| baseline candidates | naive, seasonal naive |
| metric to look at first | MAE, MAPE |
| error to check immediately | holidays, event days, promotion periods |

For example, if seasonal naive, which uses the value from the same weekday last week, produces lower error than a naive baseline that simply uses yesterday's visitor count, that means the `weekday cycle` must be part of the minimum standard in that time series.

### Small Example: Comparing Time-Series Baselines

| Model | MAE | Reading |
| --- | ---: | --- |
| naive | 320 | This is the standard that follows only the immediately previous value. |
| seasonal naive | 180 | The minimum standard that reflects the weekday pattern is better. |
| candidate model | 150 | The reader can see whether there is additional improvement beyond the seasonal standard. |

In this scene, the baseline itself may not be only one. In time series, it is more natural to first compare whether `the previous-value standard` or `the cycle standard` is the better floor line, and then place a complex model above that.

## Practice And Examples

### Comparing A Classification Baseline And Candidate Model Through A Python Example

The example below is a tiny exercise that compares scikit-learn's `DummyClassifier` and a simple classification model.

Problem situation:

- to see whether a new model is really helpful, it must be placed beside a minimum standard and compared

Input:

- imbalanced classification data made with `make_classification`
- `DummyClassifier`
- `LogisticRegression`

Expected output:

- accuracy, recall, and F1 of the baseline and actual model

Concepts to check:

- the baseline is the comparison standard that a complex model must at least beat
- in imbalanced data, not only accuracy but also recall and F1 should be viewed together

Values to change:

- If the positive-class ratio in `weights=[0.9, 0.1]` is changed to `0.2` or `0.05`, the interpretation of baseline accuracy, recall, and F1 changes.
- If `DummyClassifier(strategy="most_frequent")` is changed to `DummyClassifier(strategy="stratified")`, the reader can compare a majority-class-only standard with a standard that predicts randomly according to the class distribution.

```python
# This example sets baselines by problem type and compares candidate model performance against them.
from sklearn.datasets import make_classification
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

X, y = make_classification(
    n_samples=400,
    n_features=6,
    n_informative=3,
    n_redundant=0,
    weights=[0.9, 0.1],
    random_state=42,
)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, stratify=y, random_state=42
)

baseline = DummyClassifier(strategy="most_frequent")
baseline.fit(X_train, y_train)
baseline_pred = baseline.predict(X_test)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)
model_pred = model.predict(X_test)

print("baseline accuracy :", round(accuracy_score(y_test, baseline_pred), 3))
print("baseline recall   :", round(recall_score(y_test, baseline_pred), 3))
print("baseline f1       :", round(f1_score(y_test, baseline_pred), 3))
print()
print("model accuracy    :", round(accuracy_score(y_test, model_pred), 3))
print("model recall      :", round(recall_score(y_test, model_pred), 3))
print("model f1          :", round(f1_score(y_test, model_pred), 3))
```

An example of the execution result is as follows.

```text
baseline accuracy : 0.9
baseline recall   : 0.0
baseline f1       : 0.0

model accuracy    : 0.942
model recall      : 0.5
model f1          : 0.632
```

What must be read in this example is not one number.

- accuracy can already be high even for the baseline
- recall and F1 can show better whether important minority classes are actually being caught
- that is why baseline comparison makes the reader look together at `on what metric improvement happened` and `what kind of error remains`

### Actually Comparing Regression Baselines Through A Python Example

The example below uses a very small target-value array to compare the mean baseline and median baseline directly.

Problem situation:

- in delivery-time prediction, the reader wants to see whether the mean baseline or median baseline is the more natural starting point

Input:

- simple training target values and evaluation target values
- mean baseline, median baseline

Expected output:

- the predicted values and MAE of the mean baseline and the median baseline

Concept to check:

- even for a baseline, the more natural starting point can change depending on the actual data scene

Values to change:

- If the large value `120` in `y_train` is changed to `60` or `200`, the mean baseline moves strongly while the median baseline moves less.
- If one more large delay value is added to `y_test`, the reader can compare again which baseline has the more stable MAE.

```python
# This example sets baselines by problem type and compares candidate model performance against them.
y_train = [32, 35, 31, 120, 33]
y_test = [34, 36, 30, 90]

mean_value = sum(y_train) / len(y_train)
median_value = sorted(y_train)[len(y_train) // 2]

mean_pred = [mean_value] * len(y_test)
median_pred = [median_value] * len(y_test)

def mae(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

print("mean baseline")
print("  prediction :", [round(v, 1) for v in mean_pred])
print("  MAE        :", round(mae(y_test, mean_pred), 2))
print()
print("median baseline")
print("  prediction :", [round(v, 1) for v in median_pred])
print("  MAE        :", round(mae(y_test, median_pred), 2))
```

An example of the execution result is as follows.

```text
mean baseline
  prediction : [50.2, 50.2, 50.2, 50.2]
  MAE        : 22.6

median baseline
  prediction : [33, 33, 33, 33]
  MAE        : 16.0
```

This example shows why both the mean baseline and the median baseline should be brought to mind. If the training target values include one very large value, `120`, the mean gets dragged strongly, while the median stays more stable. In a scene like this, it is safer to first check numerically whether `the mean is the default baseline` or `the median is the more natural baseline`.

## Checklist

- Have you written down at least one representative baseline candidate that fits the current problem type?
- Are you comparing the baseline and the candidate model with the same metric?
- Are you looking together not only at score difference, but also at representative error scenes?
- Are you avoiding dragging a candidate that cannot beat the baseline into long tuning?
- Can you explain that a baseline is not `the model that loses first`, but `the standard that must be compared first`?
- Can you explain that representative baseline methods must be set differently depending on problem type?
- Can you explain that it is safer to move to tuning only after confirming that a candidate better than the baseline exists?

## Sources And References

- scikit-learn developers, [`DummyClassifier`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyClassifier.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, accessed 2026-07-26.
- scikit-learn developers, [`DummyRegressor`](https://scikit-learn.org/stable/modules/generated/sklearn.dummy.DummyRegressor.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn API Reference, accessed 2026-07-26.
- scikit-learn developers, [`Cross-validation: evaluating estimator performance`](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, accessed 2026-07-26.
- Rob J Hyndman, George Athanasopoulos, [`Forecasting: Principles and Practice (3rd ed), 5.2 Some simple forecasting methods`](https://otexts.com/fpp3/simple-methods.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
- Trevor Hastie, Robert Tibshirani, Jerome Friedman, [*The Elements of Statistical Learning*](https://hastie.su.domains/ElemStatLearn/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-26.
- Sebastian Raschka, [`Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning`](https://arxiv.org/abs/1811.12808){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-26.
