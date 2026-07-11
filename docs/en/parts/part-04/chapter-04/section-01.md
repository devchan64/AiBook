# P4-4.1 Training Data And Evaluation Data

> Section ID: `P4-4.1`
> Version: `v2026.07.11`

Chapter P4-3 showed how heuristics can narrow the model candidates to try first. That immediately raises an important question. How can you check whether that choice is actually acceptable?

In machine learning, it is not enough for a model to fit the data it has already seen. What we want is a model that makes usable judgments even on new data that will arrive later. So not all data are used only for learning. Some are left aside separately for evaluation.

Training data are the data used for learning. Evaluation data are the data used to check what the model learned. The most important first perspective is simple. `If you take a test using only the worksheet you already studied, you can easily mistake your level of skill.`

## Scope Of This Section

This Section explains why data are split. The detailed distinction between validation data and test data is handled in P4-4.2. Here the goal is first to fix the difference between the data used for learning and the data left aside for evaluation.

Overfitting and generalization are treated in detail in P4-5. Metrics such as accuracy, precision, and recall are handled in P4-6. The focus here is the reason `you must separate them before checking`.

- Why should all data not be used only for training?
- What roles do training data and evaluation data play?
- Why is it risky when a model fits only data it has already seen?
- What kinds of misunderstandings does data splitting prevent?
- What should be treated carefully when the dataset is small?

## Goals Of This Section

- You can distinguish the roles of training data and evaluation data.
- You can explain that training and evaluating on the same data can overestimate performance.
- You can understand that evaluation data are `a proxy scene for estimating how the model may act on new data`.
- You can explain why data splitting leads into model selection, overfitting, and generalization.
- You can keep a clear boundary that the detailed distinction between validation and test is handled in the next Section.

## Learning Background

### Understanding It First Through One Scene

Suppose a student memorized 100 math problems. If you give the same 100 problems again, the student can get a high score. But that alone does not prove the student can solve new problems.

A machine learning model is similar. The model looks for patterns in the training data. But if evaluation is also done on the same data, it becomes hard to tell whether the model learned a pattern or merely memorized particular examples.

| Situation | Surface result | What must actually be treated carefully |
| --- | --- | --- |
| Evaluate again on data used for training | The score can come out high. | The model may simply have memorized them. |
| Evaluate on data kept aside separately | The score can become lower. | It is closer to realistic performance on new data. |
| Fail on new data | This is easy to miss if only the training score is trusted. | Data splitting and a check of generalization are needed. |

This analogy is not perfect, but it shows the core point of data splitting. The purpose of the model is not to match examples it already saw again. It is to respond to examples it has not seen yet.

In practice, you first need to judge `which split perspective should be used first in the current problem`.

| Current problem state | Split perspective to hold first | Why |
| --- | --- | --- |
| Predicting new cases is central in tabular data | Split into training data and evaluation data | Because cases already seen and cases not yet seen must be separated. |
| Time order is central in the data | Train on earlier data and evaluate on later points | Because if future information leaks into past learning, the evaluation becomes distorted. |
| Rare labels are few | Check the label ratio after splitting first | Because if one side becomes too skewed, the evaluation itself can become unstable. |

## Main Learning Content

### Data Are Split By Role

The most basic split is between the part used for learning and the part used for evaluation.

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-1-mermaid-01-en.mmd"
```

In this diagram, evaluation data are the data not used directly during learning. The model is built from training data, then evaluation data are used to check whether the model also works on other examples.

Here the phrase `evaluation data` is used in a broad sense. In a real project, validation data and test data are often separated further. That distinction is handled in P4-4.2.

The same idea becomes more intuitive in a very small table.

| Customer ID | Recent purchase count | Inquiry count | Churn status | Where it is used |
| --- | --- | --- | --- | --- |
| C01 | 8 | 0 | stay | training data |
| C02 | 2 | 3 | churn | training data |
| C03 | 6 | 1 | stay | training data |
| C04 | 1 | 4 | churn | evaluation data |
| C05 | 7 | 0 | stay | evaluation data |

In this example, the rule is learned from C01, C02, and C03, then checked on C04 and C05. If C04 and C05 are also used for training, the model has already seen them, so the meaning of evaluation becomes weak.

The same idea looks like the following when moved into code.

Problem situation:

- Once the whole dataset is split into a learning part and an evaluation part, it is helpful to check directly which samples and labels enter each side.

Input:

- customer feature list `X`
- churn label list `y`

Expected output:

- training inputs and labels, and evaluation inputs and labels
- sample count and churn ratio for each side

Concept to check:

- `train_test_split` splits inputs and labels together using the same criterion
- after splitting, it is important to first check the counts and the label ratio

```python
from sklearn.model_selection import train_test_split

X = [
    [8, 0],  # recent purchases, support tickets
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
]
y = ["stay", "churn", "stay", "churn", "stay"]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
)

print("training inputs:", X_train)
print("evaluation inputs:", X_eval)
print("training labels:", y_train)
print("evaluation labels:", y_eval)
print("training sample count:", len(X_train))
print("evaluation sample count:", len(X_eval))
print("training churn ratio:", y_train.count("churn") / len(y_train))
print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
```

An example output can be read like the following.

```text
training inputs: [[6, 1], [8, 0], [1, 4]]
evaluation inputs: [[2, 3], [7, 0]]
training labels: ['stay', 'stay', 'churn']
evaluation labels: ['churn', 'stay']
training sample count: 3
evaluation sample count: 2
training churn ratio: 0.3333333333333333
evaluation churn ratio: 0.5
```

This code shows the most basic shape of not feeding the whole dataset into the model at once, but first splitting it into a training part and an evaluation part. `X_train` and `y_train` are used for learning, while `X_eval` and `y_eval` are left aside for checking the result.

The values printed together here are not model-performance metrics yet. They are instead the most basic inspection values that should be checked immediately after splitting the data.

- how the training sample count and evaluation sample count were divided
- whether the churn label ratio is skewed heavily to one side

Even these outputs alone help you understand more concretely `what kind of environment the model is about to learn in`.

In a more practical style, people often split inputs and targets from a DataFrame first, then split the data.

Problem situation:

- In practical work, it is common to split a DataFrame into input columns and a target column first, then divide them into learning and evaluation parts.

Input:

- feature-column list `feature_columns`
- target column `target_column`
- tabular dataset `df`

Expected output:

- the shape of `X_train` and `X_eval`
- the label ratio for the training and evaluation sides

Concept to check:

- a practical split should be read in the order `first separate input bundle X and target y`
- shape and label ratio are the basic outputs for checking a split result

```python
from sklearn.model_selection import train_test_split

feature_columns = ["recent_purchases", "support_tickets", "days_since_login"]
target_column = "churned"

X = df[feature_columns]
y = df[target_column]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("X_train shape:", X_train.shape)
print("X_eval shape:", X_eval.shape)
print("training label ratio:")
print(y_train.value_counts(normalize=True))
print("evaluation label ratio:")
print(y_eval.value_counts(normalize=True))
```

The output usually looks like the following.

```text
X_train shape: (4, 3)
X_eval shape: (1, 3)
training label ratio:
stay     0.75
churn    0.25
Name: churned, dtype: float64
evaluation label ratio:
stay    1.0
Name: churned, dtype: float64
```

Here what matters is not the syntax itself, but the separation of roles. As long as you can read the order `first separate X as input and y as answer, then separate them again into training and evaluation parts`, that is enough. The shape and label-ratio outputs are the fastest checks for whether the split result became too skewed.

### Data Splitting Must Also Fit The Problem

The phrase `split the data` does not always mean a random half-and-half split in the same way. The criterion for splitting also changes according to the nature of the problem.

| Situation | Split method to think of first | Why |
| --- | --- | --- |
| Tabular data such as churn prediction or score prediction | random split | Often the goal is to keep training and evaluation close in distribution. |
| Data where time order matters, such as monthly sales, sensor logs, or stock prices | time-based split | If future information is mixed into past learning, the real deployment situation can be distorted. |
| Data with very rare labels, such as defect detection or rare disease | stratified split | If the rare label gathers only on one side, the evaluation can become unstable. |

For example, suppose shopping-mall data were collected from January to June.

| Month | Number of customers | Number of churned customers | Where it is used |
| --- | --- | --- | --- |
| January | 100 | 8 | training data |
| February | 110 | 9 | training data |
| March | 120 | 11 | training data |
| April | 115 | 12 | training data |
| May | 125 | 15 | evaluation data |
| June | 130 | 18 | evaluation data |

In this case, learning from January through April and evaluating on May and June is closer to the real operational flow. By contrast, if part of the June data is cut out and mixed randomly into February and March for training, patterns that appeared only in the future can leak into past learning.

## Detailed Learning Content

### What Misunderstandings Appear If The Split Is Wrong

Even if the data are split, if the method does not match the problem, the result can still create false reassurance.

| Split method | Why it can look acceptable on the surface | Actual risk |
| --- | --- | --- |
| Split the whole dataset randomly | It is fast and simple. | In problems where time order matters, future information can be mixed in. |
| Split without checking the label ratio | The code stays simple. | If a particular label is almost absent in evaluation data, the score can be distorted. |
| The same customer, device, or document fragment appears on both sides | The dataset can look large. | Evaluation can become easier because the model has effectively already seen very similar cases. |

A very small churn example makes this problem clearer.

| Split result | Labels in training data | Labels in evaluation data | Problem that can appear |
| --- | --- | --- | --- |
| Good example | `stay, stay, churn, stay` | `stay, churn` | Both sides can check the basic pattern. |
| Bad example | `stay, stay, stay, stay` | `churn, churn` | There is no churn example in training, so the model cannot really learn churn. |

In such a case, even if the evaluation score is low, it becomes hard to tell whether the model is poor or whether the split itself was poor from the start. So after splitting, you must check not only the sample count but also the label distribution.

### Why It Is Risky To Learn And Evaluate On The Same Data

The model looks for patterns in the data. But if the model is very flexible or the dataset is small, it can follow not only the general pattern but also accidental traces of the training data.

For example, suppose a churn dataset happened to contain many customers from a certain event period who churned. If the model trusts that trace too strongly, it may judge new customers incorrectly even when they are unrelated to that event.

If evaluation is done on the same data, that problem is hidden. The model receives a high score because it is matching traces it already saw. But if evaluation is done on data kept aside separately, it becomes more realistic to check whether the same judgment still works on other examples.

### Training Score And Evaluation Score Are Read Differently

The score on training data and the score on evaluation data do not mean the same thing.

| Score | What it is checking | Can you feel safe just because it is high? |
| --- | --- | --- |
| training score | How well the model fits the training data | No. It may simply have memorized them. |
| evaluation score | How well it still works on held-out data | It estimates new-data performance more closely than the training score does. |

If the training score is high and the evaluation score is also high, that can be a relatively good signal. If the training score is high but the evaluation score is low, the model may have fit the training data too strongly. That problem is called overfitting and is treated in detail in P4-5.

By contrast, if both the training score and the evaluation score are low, the model may not have learned enough. That connects to underfitting, which is also handled in P4-5.

A short practical-style example can be read like the following.

| Model | training score | evaluation score | Signal that can be interpreted first |
| --- | --- | --- | --- |
| A | 0.98 | 0.62 | It may have fit the training data too strongly. |
| B | 0.81 | 0.79 | It may be relatively stable even on new data. |
| C | 0.58 | 0.55 | It may not have learned enough yet. |

This table does not imply a universal threshold. It is an example that shows `how to read the gap between training score and evaluation score`, rather than what the numbers must be.

### Evaluation Data Are Not A Perfect Substitute For The Future

Evaluation data are a device for imitating data the model has not seen yet. But evaluation data do not guarantee perfect representation of the future.

For example, suppose shopping-mall data were collected from January to June, and part of them was left aside as evaluation data. That evaluation set shows customer behavior from the same broad period. But it may not perfectly represent a November discount season or customer behavior in the following year.

So data splitting is a necessary starting point, but not the whole story. Time change, sampling bias, the data-collection method, and service-policy changes must also be considered. The basic sense of sample and bias was already seen in the earlier probability-and-statistics recovery part, and in machine learning it reconnects again in P4-5 and P4-6.

### Be More Careful When The Dataset Is Small

If the dataset is large enough, leaving some aside for evaluation still leaves a reasonable amount for learning. But when the dataset is small, the act of splitting itself becomes difficult.

When the dataset is small, the following problems appear.

- The training data shrink too much, so the model may not learn properly.
- The evaluation data become too small, so the score can swing.
- A single split result can be influenced heavily by chance.
- A specific category or rare case can gather only on one side.

Because of this, methods such as cross-validation are sometimes used. But this Section does not explain the full procedure of cross-validation. At this stage, it is enough to fix the point that `the smaller the data, the more unstable the evaluation score can become`. Cross-validation appears again in P4-4.2 and P4-8 as needed.

## Cases And Examples

### Case 1. When The Coupon-Response Score Looks Too Good

Suppose a marketing team wants to predict whether sending a coupon to a customer will lead to an actual purchase. The first human signals were things like `was there a recent purchase`, `does the user visit the app frequently`, and `has the user used coupons before`.

The problem is that because the team does not have much data, it wants to use the whole table together for both model learning and model evaluation. If this is done, the score can look high, but it becomes hard to know whether the model will still work well on new customers. It may simply have become good at matching order records it already saw.

Here data splitting changes the way judgment is made. If part of the customer records are left for learning and another part is left for evaluation, you can check whether the model behaves similarly even on customer records it sees for the first time. It also becomes easier to distinguish whether the criteria people considered important are truly repeated signals or merely traces that looked strong only in this particular table.

The checkable result is clear as well. If you compare the score from evaluation on the whole dataset with the score from separately held-out evaluation data, you can see whether a gap appears. If only the training score is high while the evaluation score falls a lot, that should be read as a signal that the interpretation without data splitting was too optimistic.

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-1-mermaid-02-en.mmd"
```

## Cases And Examples

### Misunderstandings That Data Splitting Prevents

Data splitting reduces the following misunderstandings.

| Misunderstanding | Why it appears | Help provided by data splitting |
| --- | --- | --- |
| The model got a high score, so it learned well. | Only the training-data score was checked. | It is checked again on held-out data. |
| A more complex model is always better. | It can fit training data more strongly. | Held-out data show whether the improvement is real. |
| One good score is enough. | It may be a lucky split result. | It leads you to think about multiple splits or cross-validation. |
| Having more data is all that matters. | Representativeness or collection bias can be missed. | The composition of the evaluation data is also checked. |

Data splitting is not a device for lowering model performance. It is a device for reading performance more honestly.

## Practice And Examples

### Small Python Exercise

This Section does not yet need to train a model. The goal is to learn by hand what values should be checked first after splitting the data.

### Exercise 1. Change `test_size`

The code below splits the same data using two different ratios.

Problem situation:

- You need to check directly how the sample counts for the training and evaluation sides change when the evaluation-data ratio changes.

Input:

- customer feature list `X`
- churn label list `y`
- two different `test_size` values

Expected output:

- training and evaluation sample counts for each `test_size`
- churn ratio on the training side and the evaluation side

Concept to check:

- as `test_size` grows, the evaluation side grows and the training side shrinks
- the change in sample count and the change in label ratio must be viewed together

```python
from sklearn.model_selection import train_test_split

X = [
    [8, 0],
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
    [3, 2],
    [9, 0],
    [2, 5],
]
y = ["stay", "churn", "stay", "churn", "stay", "churn", "stay", "churn"]

for ratio in [0.25, 0.5]:
    X_train, X_eval, y_train, y_eval = train_test_split(
        X,
        y,
        test_size=ratio,
        random_state=42,
    )

    print("test_size =", ratio)
    print("training sample count:", len(X_train))
    print("evaluation sample count:", len(X_eval))
    print("training churn ratio:", y_train.count("churn") / len(y_train))
    print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
    print("-" * 30)
```

An example output can look like the following.

```text
test_size = 0.25
training sample count: 6
evaluation sample count: 2
training churn ratio: 0.5
evaluation churn ratio: 0.5
------------------------------
test_size = 0.5
training sample count: 4
evaluation sample count: 4
training churn ratio: 0.5
evaluation churn ratio: 0.5
------------------------------
```

In this exercise, what matters is the split result, not a score. As `test_size` grows, the evaluation data increase and the training data decrease. When the dataset is very small, this difference feels even larger.

### Exercise 2. Change `random_state`

Even with the same data, the split result can change if the shuffle criterion changes.

Problem situation:

- Even with the same data and same split ratio, the label composition on the evaluation side can change if the shuffle criterion changes.

Input:

- the same `X` and `y`
- different `random_state` values

Expected output:

- the list of evaluation labels for each `random_state`
- the churn ratio in the evaluation data

Concept to check:

- `random_state` is the reference value used to reproduce a split result
- with small data, the evaluation composition can swing a lot even when only the seed changes

```python
from sklearn.model_selection import train_test_split

X = [
    [8, 0],
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
    [3, 2],
    [9, 0],
    [2, 5],
]
y = ["stay", "churn", "stay", "churn", "stay", "churn", "stay", "churn"]

for seed in [0, 7, 42]:
    X_train, X_eval, y_train, y_eval = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=seed,
    )

    print("random_state =", seed)
    print("evaluation labels:", y_eval)
    print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
    print("-" * 30)
```

An example output can differ like this.

```text
random_state = 0
evaluation labels: ['stay', 'stay']
evaluation churn ratio: 0.0
------------------------------
random_state = 7
evaluation labels: ['churn', 'stay']
evaluation churn ratio: 0.5
------------------------------
random_state = 42
evaluation labels: ['churn', 'churn']
evaluation churn ratio: 1.0
------------------------------
```

This exercise shows why `random_state` should be written down. If you want to reproduce the same split result when the same code is run again, the reference value must be fixed.

### Exercise 3. See What Problem Appears When The Data Are Skewed

The next example shows how easily the split result can swing when churn cases are few.

Problem situation:

- In data where positive labels are very rare, even a single split can skew the evaluation composition heavily

Input:

- `X` and `y` with a sparse `churn` label

Expected output:

- the list of training labels
- the list of evaluation labels
- the churn ratio in each bundle

Concept to check:

- in class-imbalanced data, label distribution can shake easily even with an ordinary random split
- this is why label composition should be printed right after the split

```python
from sklearn.model_selection import train_test_split

X = [[i] for i in range(10)]
y = ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "churn"]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
)

print("training labels:", y_train)
print("evaluation labels:", y_eval)
print("training churn count:", y_train.count("churn"))
print("evaluation churn count:", y_eval.count("churn"))
```

An example output can be read like this.

```text
training labels: ['stay', 'stay', 'stay', 'stay', 'stay', 'stay', 'stay']
evaluation labels: ['stay', 'stay', 'churn']
training churn count: 0
evaluation churn count: 1
```

In this exercise, one side can end up with almost no `churn`, or even none at all. In that state, it becomes very hard for the model to learn churn patterns or to evaluate them properly. That is why the next Section returns to stratified split.

## Perspective To Remember In This Section

- Training data are the data used by the model to learn.
- Evaluation data are the data kept aside to check what the model learned.
- If the same data are used for both learning and evaluation, performance can be overestimated.
- Evaluation data are a proxy scene for estimating behavior on new data.
- Training score and evaluation score do not mean the same thing.
- If the dataset is small, even evaluation scores can swing, so they must be read more carefully.

## Checklist

- Can you explain why using the same data for both learning and evaluation easily overestimates performance?
- Can you explain why the split method should differ in time-ordered data and rare-label data?
- Can you distinguish what training score and evaluation score each show?

## When This Perspective Should Come To Mind First

- When you are tempted to think casually that learning and evaluation can share the same data, recall the role distinction between training data and evaluation data first.
- Return to this Section when you need to explain again what the gap between training score and evaluation score means, and why it is not the same thing as new-data performance.
- This Section is the reference point when evaluation scores must be read more carefully because the dataset is small or time order matters.

## Sources And References

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, accessed 2026-06-25. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `train_test_split`, scikit-learn API Reference, accessed 2026-06-25. [https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, official website accessed 2026-06-25. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
