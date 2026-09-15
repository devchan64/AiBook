# P2-15.2 Checks Before Moving to Part 3

> Section ID: `P2-15.2`
> Version: `v2026.09.15`

## Connecting Data and Computation

Formulas express calculation rules; Python expresses executable procedures. NumPy handles arrays, Pandas selects and aggregates tables, and Matplotlib reveals changes and distributions. Git records why the code and explanation changed.

```mermaid
--8<-- "assets/part-02/chapter-15/part2-learning-map-flow-en.mmd"
```

## Case 1. Inputs and Targets for Four Students

Suppose we want to predict scores before an exam. This fictional table illustrates how inputs relate to targets. Study hours, absences, and practice quizzes are recorded by prediction time; the exam score is the target observed later.

| Student | Study Hours | Absences | Quizzes | Exam Score |
| --- | ---: | ---: | ---: | ---: |
| A | 2 | 5 | 3 | 50 |
| B | 4 | 3 | 5 | 65 |
| C | 6 | 1 | 7 | 80 |
| D | 8 | 0 | 9 | 90 |

Input `X` contains the three columns for study hours, absences, and quizzes; target `y` contains exam scores. Students are rows and features are columns, so `X.shape` is `(4, 3)` and `y.shape` is `(4,)`. The first input `[2, 5, 3]` pairs with target 50.

Including exam scores in `X` would produce `(4, 4)` but expose answers unavailable before the exam. Correct column counts and executable code do not establish that the inputs are appropriate.

Removing quizzes from the inputs changes `X.shape` to `(4, 2)` without changing `y.shape`. Removing student D requires removing the same student from both `X` and `y`.

Student names identify corresponding rows and are not predictive features in this example. If only `X` is sorted by decreasing study hours, D’s input `[8, 0, 9]` pairs incorrectly with A’s score 50. Equal sample counts do not guarantee valid training data.

Even with the same three features, changing column order at prediction time is a problem. If the first training column is study hours, a new student’s first column must also be study hours. Shape `(1, 3)` identifies one student and three features but does not guarantee column meanings.

## Reading Training and Prediction Calls

In scikit-learn, objects that learn from data are called estimators. In supervised learning, `fit(X_train, y_train)` trains a model from training inputs and targets. `predict(X_test)` obtains predictions from the trained model using test inputs.

| Expression | Meaning |
| --- | --- |
| sample | One data instance; here, one student |
| feature | An input attribute; here, hours, absences, or quizzes |
| target, `y` | The answer to predict; here, the exam score |
| train data | Data used to train the model |
| test data | Data reserved for final evaluation, unused for training or model selection |
| `fit` | Learn model rules from data |
| `predict` | Obtain outputs for inputs using the trained model |

```mermaid
--8<-- "assets/part-02/chapter-15/ml-reading-flow-en.mmd"
```

Test targets are not inputs to `predict`. They are used afterward to compare predictions with actual answers.

## Roles of Training, Validation, and Test Data

Splitting data means keeping sample pairs together, not shuffling `X` and `y` independently. Assigning A, B, and C to training and D to testing gives these shapes. This four-row example illustrates the flow; it is insufficient for judging real predictive performance.

| Dataset | Students | Input Shape | Target Shape |
| --- | --- | --- | --- |
| Training | A, B, C | `(3, 3)` | `(3,)` |
| Test | D | `(1, 3)` | `(1,)` |

`fit` sees inputs and targets for A, B, and C. `predict` receives only D’s input. Its one prediction is compared with D’s actual score of 90. The feature matrix must retain two axes even when passing one new sample.

In real model comparisons, reserve validation data within the training data or use cross-validation. Validation results guide the choice of features, model, and settings; test data remain for final evaluation after selection. Repeatedly changing features in response to test scores uses test information for selection, removing its role as an independent final evaluation.

Learn preprocessing parameters from training data as well. To subtract mean study hours, use the A–B–C mean `(2+4+6)/3 = 4`. Apply that same value to D’s 8 hours to obtain `8-4 = 4`. Computing the all-student mean of 5 first would use test-input information before training.

## Case 2. Distinguishing Errors, Loss, and Metrics

As a separate calculation exercise, let actual scores be `[50, 65, 80, 90]` and predictions `[55, 60, 80, 85]`. These predictions are chosen for metric comparison, not obtained from a trained-model experiment. Subtracting predictions from actual values gives `[-5, 5, 0, 5]`. Their mean is 1.25, but opposite signs cancel, so this does not directly represent error magnitude.

Squared errors are `[25, 25, 0, 25]`, giving MSE `75 / 4 = 18.75`. Mean absolute error, MAE, averages absolute errors: `15 / 4 = 3.75`. The same predictions yield different values and meanings under different summaries.

| Summary | Value | Interpretation |
| --- | ---: | --- |
| Mean error | 1.25 points | Signed errors after cancellation |
| MAE | 3.75 points | Mean absolute error |
| MSE | 18.75 points² | Mean squared error |
| RMSE | About 4.330 points | Square root of MSE |

A numerically larger MSE than MAE does not mean worse performance. They summarize the same predictions using different units and rules. Compare models using the same evaluation samples and metric.

Loss is the quantity training seeks to reduce; a metric is a criterion for evaluating results. The same calculation, such as MSE, can serve both roles. Specify which data produced it and what decision it supports.

Changing predictions to `[50, 65, 80, 90]` makes all errors, MSE, and MAE zero. This is a small case for checking the calculation.

Now calculate how MAE and MSE change if only the last prediction moves from 85 to 75. The absolute-error sum rises to 25, giving MAE 6.25. The squared-error sum rises to 275, giving MSE 68.75. Squaring gives a larger influence to one sample’s large error.

## Recording Changed Conditions

Record changes to features or splitting conditions alongside the results. “Improved results” alone does not identify the comparison.

| Record | Concrete Example |
| --- | --- |
| Input change | Remove quizzes, reducing three features to two |
| Fixed conditions | Same training and validation students, same model settings |
| Comparison | Record validation MSE and prediction tables before and after; test after selection |
| Generation record | Code and data versions, execution command |

Changing many conditions together makes it harder to identify which caused the difference. Choose and record changes that match the comparison’s purpose.

## Checking Result Interpretations

Decide whether each situation can immediately be read as a performance improvement.

| Situation | Judgment and Reason |
| --- | --- |
| Adding exam scores to the inputs produces zero error | This leaks an answer unavailable at prediction time and is not evidence of improvement |
| One student is removed from `X` but `y` is unchanged | Fix sample counts and correspondence first |
| Model A’s training MSE is below model B’s test MSE | Different evaluation data prevent a direct comparison of generalization performance |
| Removing a feature lowers the same metric on the same validation data | This improves the result under those validation conditions; separate testing is still needed after selection |

Executable code and a smaller number are not enough. Inputs must be available at prediction time, samples must correspond, and evaluation conditions must match.

## Where to Review Each Concept

| Topic | Related Section |
| --- | --- |
| Variables and functions | [P2-2.1](../chapter-02/section-01.en.md) |
| Vectors and matrices | [P2-3.1](../chapter-03/section-01.en.md) |
| Mean and variance | [P2-5.2](../chapter-05/section-02.en.md) |
| Loss functions | [P2-6.1](../chapter-06/section-01.en.md) |
| Gradient descent | [P2-6.3](../chapter-06/section-03.en.md) |
| Array shapes and axes | [P2-11.2](../chapter-11/section-02.en.md) |
| Inputs, targets, and splitting data | [P2-12.3](../chapter-12/section-03.en.md) |
| Reading plots | [P2-13.1](../chapter-13/section-01.en.md) |
| Calculating MSE | [P2-15.1](section-01.en.md) |

## Checklist

- Can you distinguish input and target columns in the student table?
- Can you explain changes to `X` and `y` shapes when removing a feature or student?
- Can you distinguish the data passed to `fit` and `predict`?
- Can you calculate mean error, MSE, and MAE from the predictions above?
- Can you distinguish training loss from a test evaluation value?
- Can you record fixed conditions and results when changing inputs or splits?
- Can you explain why incorrect row correspondence or feature order is a problem despite matching shapes?
- Can you distinguish validation-based selection from final testing?
- Can you use the numbers to explain why preprocessing parameters come only from training data?

## Sources and References

- [scikit-learn developers, Getting Started](https://scikit-learn.org/stable/getting_started.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Basic structure of X, y, fit, and predict.
- [scikit-learn developers, Glossary](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Sample, feature, target, and estimator terminology.
- [scikit-learn developers, Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Avoiding leakage and learning preprocessing from training data.
- [scikit-learn developers, Cross-validation: evaluating estimator performance](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Validation-based selection versus testing.
- [scikit-learn developers, Regression metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Summarizing the same predictions with MSE, MAE, and RMSE.
