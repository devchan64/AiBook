# Part 2 Summary. Rebuilding the Foundations

> Section ID: `P2-summary`
> Version: `v2026.09.15`

Mathematics compresses calculations. The rules expressed in formulas can be executed in Python, while NumPy arrays and Pandas tables represent the structure of the values involved. Graphs show changes and distributions in the results, and execution environments and Git history help track the conditions needed to reproduce them.

## Connecting calculations and tools

| Topic | Perspective to remember |
| --- | --- |
| Formulas and code | Formulas express computational intent; code translates that calculation into executable steps. |
| Logarithms and exponentials | A logarithm reverses exponentiation and reappears in the language of probability scores and losses. |
| Variables and data | Variables in formulas can appear in code as values, arrays, tables, or datasets. |
| Vectors and matrices | Vectors and matrices group multiple values using positions, directions, axes, and shapes for calculation. |
| Dot products and distances | A dot product reduces a relationship between vectors to one number; distance and similarity address different comparison questions. |
| Derivatives and gradients | Derivatives describe rates of change, while gradients describe changes along multiple directions together. |
| Composite functions and the chain rule | They show how rates of change propagate through connected calculation steps. |
| Loss and optimization | Loss quantifies how poor the current result is; optimization searches for better values. |
| Probability and statistics | Probability expresses uncertainty numerically; statistics produces summaries that support judgments about collections of data. |
| Python and execution environments | The same code has different execution contexts in Colab, on a local PC, in a terminal, in a notebook, or in a virtual environment. |
| NumPy and Pandas | NumPy supports array calculations; Pandas supports reading and organizing tabular data. |
| Matplotlib and visualization | Graphs reveal numerical patterns, distributions, relationships, and training progress. |
| Git and reproducibility | Git tracks how manuscripts, code, images, and evidence notes change over time. |

In probability, we distinguished long-run frequencies of repeated observations from degrees of belief in uncertain propositions. Bayes' rule updates conditional probabilities in light of new evidence. Derivatives and gradients describe how outputs change when inputs or parameters change; loss and optimization describe which criterion to reduce when adjusting values.

## Concepts to distinguish

| Easily confused concepts | Distinction |
| --- | --- |
| Python lists and NumPy arrays | `+` concatenates lists, while array `+` performs elementwise addition when shapes are compatible. |
| Table rows and samples | One row in a student list may represent one student, but multiple sensor-record rows may together represent one action. |
| Mean and distribution | Values with the same mean can have different spreads and changes over time. |
| Training loss and evaluation results | Even when loss decreases on training data, performance on new data must be checked separately. |
| Correlation and causation | A trend in a scatter plot alone does not establish that one variable causes another. |
| Saving files and committing | Saving updates the current file; a commit records staged file states in the history. |

## Distinguishing a calculation criterion from a direction of change

Answer each question before comparing it with the explanation on the right. Check both the calculated value and what it lets you conclude.

| Question to check | Calculation and interpretation |
| --- | --- |
| What is the dot product of `[1, 2]` and `[3, 4]`? | Multiply corresponding values and add: `1×3 + 2×4 = 11`. A dot product is one number and differs from the distance between the vectors. |
| For the loss `L(w) = (w − 3)²`, what are the loss and derivative at `w = 1`? | The loss is `4`, and the derivative is `2(w − 3) = −4`. Loss measures the current error; the derivative helps identify a direction for changing the value at this position. |
| What happens after one gradient descent step with a learning rate of `0.1` under these conditions? | `w = 1 − 0.1×(−4) = 1.4`, and the loss decreases to `2.56`. This single decrease does not guarantee a decrease for every learning rate and function. |
| Do `[1, 3]` and `[2, 2]` have the same mean? Is their spread also the same? | Both means are `2`. Averaging the squared distances from the mean gives `1` and `0`, respectively, so their spreads differ. |
| If the observed pass rate is `1/3`, must the next student's probability of passing also be `1/3`? | The observed proportion among three students alone cannot determine the next student's probability. Check the conditions of both the sample and the prediction target. |

## Checking with a small table

Suppose we predict whether students pass using their study hours and the number of questions solved before the exam. The first two columns are input features; the last column contains the correct answers observed after the exam.

| study_hours | solved_questions | passed |
| ---: | ---: | ---: |
| 1 | 5 | 0 |
| 2 | 9 | 0 |
| 4 | 16 | 1 |

`predicted` contains example values assigned directly to check the accuracy calculation. The code below does not train a model or generate predictions from `X`. Change the predictions to see which changes: the observed pass rate or accuracy.

```python
import numpy as np

X = np.array([[1, 5], [2, 9], [4, 16]])
y = np.array([0, 0, 1])
predicted = np.array([0, 1, 1])

print(X.shape, y.shape)
print("pass rate:", y.mean())
print("correct:", predicted == y)
print("accuracy:", (predicted == y).mean())
```

```text
(3, 2) (3,)
pass rate: 0.3333333333333333
correct: [ True False  True]
accuracy: 0.6666666666666666
```

`X` contains three samples with two features, and `y` contains three correct answers in the same order. The mean of the pass indicators is the observed pass rate, 1/3. Only the second student's prediction is wrong, so accuracy is 2/3. Pass rate and prediction accuracy answer different questions.

Changing the predictions to `[0, 0, 1]` makes accuracy 1 while the observed pass rate remains 1/3. Removing the number of solved questions from the inputs gives `X` a shape of `(3, 1)`, while the three correct answers remain unchanged. To compare how input changes affect model results, use the same data split and evaluation criteria and record the changes.

## Related sections

| What to check | Location |
| --- | --- |
| Inputs, targets, and data leakage | [P2-12.3](chapter-12/section-03.en.md) |
| Array shapes and axes | [P2-11.2](chapter-11/section-02.en.md) |
| Mean and variance | [P2-5.2](chapter-05/section-02.en.md) |
| Dot products and distances | [P2-3.4](chapter-03/section-04.en.md) |
| Derivatives and gradients | [P2-4.3](chapter-04/section-03.en.md) |
| Gradient descent | [P2-6.3](chapter-06/section-03.en.md) |
| Calculating loss | [P2-15.1](chapter-15/section-01.en.md) |
| Execution location and environment | [P2-7.6](chapter-07/section-06.en.md), [P2-7.7](chapter-07/section-07.en.md) |
| Rerunning notebooks | [P2-10.3](chapter-10/section-03.en.md) |
| Methods and objects | [P2-8.6](chapter-08/section-06.en.md) |
| Comparing data structures | [P2-9.4](chapter-09/section-04.en.md) |
| Comparing and saving graphs | [P2-13.3](chapter-13/section-03.en.md) |
| Change history | [P2-14.1](chapter-14/section-01.en.md) |

## Remaining questions

With small calculations and data structures as a foundation, machine learning learns rules from data and evaluates those rules on new data. Which model to choose, how to divide training, validation, and test data, and which metrics to compare are questions for the model-training material that follows.

Advanced mathematical proofs, large-scale data processing, and collaboration automation cover broader conditions than the small examples in this Part. Do not assume that the code run here will have the same memory cost and performance on large datasets.

## Checklist

- Can you distinguish a dot product calculation from a vector distance calculation?
- Can you explain one parameter update using the loss, derivative, and learning rate?
- Can you explain how equal means can conceal different spreads, and distinguish an observed proportion from a predicted probability?

- Can you explain the inputs, targets, and array shapes in the table above?
- Can you calculate and distinguish the observed pass rate and prediction accuracy?
- Can you check what changes when you alter input features or predictions?
- Can you state the graph axes, what each table row represents, and the code's execution environment?
- Can you record changed conditions and code and data versions alongside the results?

## Sources and further reading

This is an original summary based on the Part 2 chapters. The sources supporting each concept are listed in the related sections.
