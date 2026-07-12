# P4-4.2 Validation And Test

> Section ID: `P4-4.2`
> Version: `v2026.07.12`

P4-4.1 explained why data are divided into training data and evaluation data. Now the discussion moves one step further. The data used while choosing a model and the data used for the final one-time check do not play the same role.

If this difference is not separated, people start looking at test results repeatedly while choosing the model, and at that moment the test data can no longer play the role of `data seen for the first time`. That is why in practice evaluation data are often split again into `validation data` and `test data`.

This Section explains `validation`, `test`, and `the difference between mid-process model-choice checks and the final check`. Later Sections continue the current context through this handle, and the evaluation procedure after data splitting is connected again through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section explains the difference in role between validation and test. The calculation of metrics themselves is not covered in detail here. Metrics such as accuracy, precision, and recall are handled in P4-6.

This Section also explains the flow `what should be looked at while choosing a model`, but the full procedure of model selection and the discussion of baseline models return in P4-8. The ideas of overfitting and generalization are treated in more detail in P4-5.

- Why should validation data and test data be kept separate?
- When should each of them be used?
- Why is it a problem if you keep looking at test data in the middle?
- When the dataset is small, how should this distinction be read carefully?
- How does cross-validation connect to this structure?

## Goals Of This Section

- You can explain the difference in role between validation and test.
- You can explain that validation data are for selection, while test data are for the final check.
- You can understand why repeated exposure to test data can distort the interpretation of results.
- You can explain that the distinction between validation and test becomes harder when the dataset is small.
- You can understand that cross-validation is not magic that replaces test data, but a method for making validation more stable within the available data.

## Learning Background

### Understanding It First Through One Scene

Think of a student preparing for university entrance exams by solving mock exams.

- practice problems: solved often during learning
- mock exam: used to compare which solution strategy is better
- real exam: used once at the end to check actual ability

Machine learning has a similar flow.

| Data | What they do | When they are seen |
| --- | --- | --- |
| training data | The model learns patterns. | They are seen continuously during learning. |
| validation data | Models and settings are compared. | They are seen repeatedly in the middle of experiments. |
| test data | The final result is checked. | They are seen near the very end. |

The biggest difference between validation data and test data is `how often they are used in decision making`.

## Main Learning Content

### Validation Data Help Selection

Validation data are used while choosing the model. For example, they are used for choices like the following.

- which to try first between logistic regression and decision tree
- whether tree depth should be 3 or 5
- whether changing preprocessing improved the result
- whether adding a feature actually helped

In other words, validation data are used in the middle of experiments to compare `is this choice better than the previous one?`

A very simple example can be read like this.

| Candidate | What changed | Validation accuracy | Judgment at this stage |
| --- | --- | --- | --- |
| Model A | Use logistic regression | 0.78 | Keep it as the reference point |
| Model B | Use decision tree | 0.74 | Lower than A, so hold it back |
| Model C | Logistic regression + one extra feature | 0.81 | Best among the current candidates |

The important point in this table is not the number itself, but `for what selection is this number being used?` This is not yet the stage of publishing final performance. It is the stage of comparing candidates and narrowing them to one.

It becomes even easier if you translate it into a work scene. Suppose you are building an email-spam classifier.

- candidate 1: use word frequency only
- candidate 2: use word frequency + sender features
- candidate 3: candidate 2 + title-length feature

When choosing which of these three is better, you use validation data. This is not yet the stage of announcing the final model to deploy in the service. It is still `the stage of finding the better candidate`.

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-2-mermaid-01-en.mmd"
```

In this diagram, validation data sit before the model is fixed. They appear repeatedly in the cycle `change the experiment, check again, change again, check again`.

### Test Data Are For The Final Check

Test data are closer to a one-time final confirmation after the model has been chosen.

You can think about a flow like the following.

1. Train several models on the training data.
2. Compare them on the validation data and choose the most appropriate candidate.
3. Freeze that choice again.
4. Finally, check final performance on the test data.

The purpose of test data is to ask, `after all of this selection process, how well does the model still work on data it sees for the first time?` That is why test data should be opened as late as possible and should not be looked at repeatedly.

The same scene becomes clearer if you separate validation score and test score.

| Candidate | Validation accuracy | Test accuracy | How it should be read |
| --- | --- | --- | --- |
| Model A | 0.78 | not opened yet | Since this is the validation stage, the test set stays closed |
| Model C | 0.81 | not opened yet | Select it first by the validation criterion |
| Final choice: Model C | 0.81 | 0.76 | Check it once at the end |

Here the difference between `0.81` and `0.76` is not strange. The candidate was chosen using the validation data, while the test data give a new-data check after that choice.

This difference is also where readers often misunderstand. If the validation score was higher and the test score dropped a little, that does not immediately mean something went wrong. It should instead be read as a signal that `data for choosing` and `data for final checking` play different roles.

The distinction between validation data and test data becomes clearer if you first ask `is the current question for candidate selection, or for final confirmation?`

| Question being asked now | Data to inspect first | Why |
| --- | --- | --- |
| Which is better, this model or that model? | validation data | Because this is still the candidate-selection stage |
| Does adding one more feature help? | validation data | Because this is a mid-experiment comparison |
| How much can the final model now be trusted on new data? | test data | Because this is a final-confirmation question |

## Detailed Learning Content

### Why You Should Not Keep Looking At The Test Set

If you keep opening the test data in the middle, you start changing choices to fit that result even without noticing.

| Experiment order | Action that can look reasonable on the surface | Actual problem |
| --- | --- | --- |
| Look at Model A test result | Try another model because the score is disappointing | The test result has already influenced selection |
| Look at Model B test result too | Choose the higher score | The test set is now being used like comparison-oriented validation data |
| Change settings and test again | Repeat until the score improves | It becomes easier to fit the test data itself |

Once this happens, the test data are no longer `unseen data for the final check`. In practice, they have been used like validation data.

The core principle is the following.

- validation data may be seen in the middle of experiments
- test data should usually be opened at the end
- if you keep changing selections after seeing the test set, the test set is also contaminated into a validation-like role

It becomes easier to remember if you compare them like this.

| Question | Is it okay to ask this of validation data? | Is it okay to ask this of test data? |
| --- | --- | --- |
| Which is better, this model or that model? | yes | usually no |
| Does changing preprocessing improve the result? | yes | usually no |
| How much does the final model really work on new data? | It is a reference, but not the final check | yes |

It also helps to look together at a flow that `should not be done`.

| Step | Bad habit | Why it is a problem |
| --- | --- | --- |
| 1 | Look at the test score first | A number meant for final confirmation becomes the starting point of the experiment |
| 2 | Add more features because the score is low | Selection is already being changed to fit the test result |
| 3 | Look at the test score again | The test set is being used almost like validation data |
| 4 | Adopt the combination that produced the highest score | The estimate of performance on new data can become exaggerated |

## Cases And Examples

### Case 1. Opening The Test Set Too Early In A Spam-Classification Experiment

Suppose a team operating a mail service is building a spam-classification model. Until now, people first filtered mail using rules such as `are there many ad phrases`, `is it from a certain sender domain`, or `is the title excessively provocative`.

Now the team wants a model that is better than the rule-based classifier. But if it keeps checking test data during experiments, a problem appears. For example, if Model A's test score looks disappointing, then features are added, the test score is checked again, settings are changed again, and so on. In that moment, the test set is effectively becoming comparison data.

This is exactly why validation data and test data are separated. Validation data are where you ask `which candidate is better?` Test data are where you ask `is it now acceptable to check the chosen model one last time?` Only when these roles are separated can the model-selection process avoid being dragged around by test results.

The checkable result appears in the experiment log. If the final model is chosen by candidate-specific validation scores and the test score is opened only once after that, you can read separately which numbers were used for selection and which number was used for the final check. By contrast, if the test score was recorded several times while changing selections, that test result is no longer a reliable basis for a final-confirmation claim.

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-2-mermaid-02-en.mmd"
```

### Separating The Roles Again With A Small Table

If you rewrite the customer-churn prediction example, it can be split like the following.

| Customer ID | Recent purchase count | Inquiry count | Churn status | Where it is used |
| --- | --- | --- | --- | --- |
| C01 | 8 | 0 | stay | training data |
| C02 | 2 | 3 | churn | training data |
| C03 | 6 | 1 | stay | training data |
| C04 | 3 | 2 | churn | validation data |
| C05 | 7 | 0 | stay | validation data |
| C06 | 1 | 4 | churn | test data |
| C07 | 9 | 0 | stay | test data |

In this case, C04 and C05 may be seen several times in the middle of experiments. For example, when comparing Model A and Model B, both are checked on C04 and C05. But C06 and C07 should be opened once at the end.

It becomes even clearer when rewritten as questions.

- `Should tree depth be 3 or 5?` -> a question for validation data
- `Can this model now be announced?` -> a question for test data

When the question changes, the role of the data being used also changes.

Even with the same customer-churn table, once the question changes, the role of the data changes with it. The following diagram shows why `the candidate-selection stage` and `the final-confirmation stage` should not share the same data fragment.

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-2-mermaid-03-en.mmd"
```

## Practice And Examples

### Looking At The Split Structure Through Python

The following code shows the simplest structure for splitting at once into `training`, `validation`, and `test`.

Problem situation:

- It can be hard to picture immediately how `keeping validation and test separate` appears as an actual two-stage split in code.

Input:

- sample list `X`
- label list `y`

Expected output:

- sample count for training, validation, and test
- label composition for validation and test

Concept to check:

- a three-part split is usually implemented by first separating `train` from temporary evaluation data, then splitting that temporary data again
- validation and test play different roles, so their results should also be checked separately

```python
from sklearn.model_selection import train_test_split

X = [[i] for i in range(12)]
y = ["stay", "churn", "stay", "stay", "churn", "stay", "stay", "churn", "stay", "stay", "churn", "stay"]

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.5,
    random_state=42,
)

print("train size:", len(X_train))
print("validation size:", len(X_val))
print("test size:", len(X_test))
print("validation labels:", y_val)
print("test labels:", y_test)
```

An example output can be read like the following.

```text
train size: 7
validation size: 2
test size: 3
validation labels: ['stay', 'churn']
test labels: ['stay', 'stay', 'churn']
```

This code does not split the data into three blocks at once directly. Instead, it first separates `training` and `temporary evaluation data`, then splits that temporary data again into `validation` and `test`. This two-step split is often easier to read.

### Separating `Selection` And `Final Check` Through A Python Example

This time, read a very small experiment log through code output. The following code shows in what order validation score and test score should be read, even without actually training a model.

Problem situation:

- Validation score and test score both look like performance numbers, but their reading order and roles are different.

Input:

- candidate-specific `validation_score`
- final `test_score`

Output:

- validation score for each candidate
- the result selected by validation
- the final test score

Concept to check:

- model selection is done first by validation score
- test score should be read as a number checked once after selection

```python
candidates = [
    {"name": "model_A", "validation_score": 0.78},
    {"name": "model_B", "validation_score": 0.74},
    {"name": "model_C", "validation_score": 0.81},
]

best = max(candidates, key=lambda item: item["validation_score"])

print("candidate scores on validation:")
for item in candidates:
    print(item["name"], "->", item["validation_score"])

print("chosen by validation:", best["name"])

test_score = 0.76
print("final test score:", test_score)
```

An example output is read like this.

```text
candidate scores on validation:
model_A -> 0.78
model_B -> 0.74
model_C -> 0.81
chosen by validation: model_C
final test score: 0.76
```

The key in this output is the order.

1. Compare the candidates by validation score.
2. Then choose one.
3. Finally, check the test score.

What you need to hold here is the order. `Validation is used for choosing, while test is used for checking after the choice` appears directly even in Python output.

### Looking At A Bad Flow Through Python As Well

The following example is a record meant to show what the problem is. It is not a good experiment procedure. It is an example for reading `why you should not look at the test set repeatedly`.

Problem situation:

- If the test score is opened too early, that number can start contaminating model selection.

Input:

- candidate-specific test scores checked too early

Output:

- a record that the selection changed after test scores were seen

Concept to check:

- the moment test data begin to be used like comparison-oriented validation data, their meaning becomes weaker
- this example is not a good procedure, but a flow that should be avoided

```python
test_scores_seen_too_early = {
    "model_A": 0.74,
    "model_B": 0.77,
}

print("looked at test too early:")
for name, score in test_scores_seen_too_early.items():
    print(name, "->", score)

print("decision changed after seeing test scores")
print("problem: test data has started to influence model choice")
```

An example output is read like the following.

```text
looked at test too early:
model_A -> 0.74
model_B -> 0.77
decision changed after seeing test scores
problem: test data has started to influence model choice
```

This code shows interpretation more than calculation. The moment `you look at the test score first and then change the choice because of it`, the test data have already started to leave their role as data for final confirmation only.

### How Validation And Test Should Be Read

When reading experiment results, separate the role before the number itself.

| Value | Question to ask first |
| --- | --- |
| validation score | Is this a number used to compare several candidates? |
| test score | Is this a number checked once after the final choice? |
| unusually good test score | Was the test set opened many times in the middle? |
| large gap between validation and test | Was the selection process repeated too much, or is the dataset small and unstable? |

This Section does not yet treat metric types in detail. What matters now is that even when the number is the same, for example `0.82`, its meaning changes depending on whether it is a validation score or a test score.

So when reading an experiment record, it becomes clearer to complete sentences like the following.

- Is this number `a validation score used for model choice`?
- Is this number `a test score checked after the final choice`?
- After seeing this number, `was the model changed again`?

If the answer to the third question is `yes`, then that number may no longer be only a number for final confirmation.

### Be More Careful When The Dataset Is Small

If the dataset is not large enough, it becomes difficult to keep training, validation, and test all fully separate.

| Problem | Why it appears |
| --- | --- |
| Training data shrink too much | Once the data are split into three pieces, each piece becomes small. |
| Validation score swings | If validation data are too small, chance has a larger effect. |
| Test score also becomes unstable | The data for final confirmation can also be too few. |

In such cases, cross-validation is sometimes used. Cross-validation is a method for repeating validation several times within the available data so that comparison becomes more stable. But that does not mean test data become unnecessary. In real projects, the validation structure must still be adjusted according to the dataset size and the task.

For example, if there are only 30 customer records, the following problems appear immediately.

| Split method | Feeling that can arise |
| --- | --- |
| train 20 / validation 5 / test 5 | The validation and test counts are so small that one or two cases can swing the score heavily |
| train 24 / evaluation 6 | It is simpler at first, but it becomes hard to keep validation and test separate |
| use cross-validation | It becomes a choice for making repeated validation comparisons somewhat more stable on a small dataset |

The important point in this Section is not `what ratio must be correct`, but rather that the smaller the dataset is, the more carefully validation and test must be interpreted.

## Checklist

- Can you explain why validation data are distinguished as `for selection` and test data as `for final confirmation`?
- Can you explain why repeatedly looking at test scores in the middle contaminates the test set into a validation-like role?
- Can you distinguish which questions should be asked to validation data and which should be left for test data?
- Can you explain that validation data are used to compare models and settings, while test data are used for the last check after the final choice?
- Can you explain that if selections keep changing to fit test results, the test set is also contaminated into a validation-like role?
- Can you explain that when the dataset is small, it becomes harder to secure both validation and test stably?

## Sources And References

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, accessed 2026-06-26. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `train_test_split`, scikit-learn API Reference, accessed 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, official website accessed 2026-06-26. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
