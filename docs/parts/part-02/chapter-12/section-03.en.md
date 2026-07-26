# P2-12.3 Intuition of Preparing a Learning Dataset

> Section ID: `P2-12.3`
> Version: `v2026.07.26`

In P2-12.1, we read a `DataFrame` as a table-shaped data structure. In P2-12.2, we chose the needed columns from that table, filtered rows by condition, and checked summary values. Now the question moves one step further: `what must be prepared to turn this table into a learning dataset that a model can read?`

The important point here is that `handling Pandas well` and `preparing a learning dataset well` are not the same thing. The former is a table-manipulation skill. The latter is the work of deciding what inputs the model receives and what answers it should learn.

This Section explains the basic distinction among dataset, feature, target, validation, and data leakage. The representative explanation of `DataFrame` and table selection stays in P2-12.1, P2-12.2, and the [dataset glossary entry](/AiBook/en/reference/concept-glossary-alpha/d.en/#dataset). Here, the focus is on how to reorganize that table into learning inputs and answers.

If Chapter 11 made a computable array shape, Chapter 12 is now the stage where we decide which columns to keep from the table and which to remove. The input and answer candidates organized here lead into the visualizations of Chapter 13 and the record organization of Chapter 14.

## Core Criteria: the Intuition of Preparing a Learning Dataset

- You can explain learning-dataset preparation as `reorganizing the original table into model inputs and answers`.
- You can read one row as one sample and one column as a candidate feature or target.
- You can explain why `X` and `y` are separated.
- You can explain why train, validation, and test are separated.
- You can explain why data leakage distorts evaluation.
- You can explain that Pandas is used for reading data, selecting, filtering, creating columns, and basic checking, while training splits are often handled together with separate tools.

## One Scene to Hold First

The first scene to hold in this Section is that one row is usually one sample, one column is a candidate feature or target, `X` is a bundle of input columns, and `y` is the answer column to predict.

If we look again at a small student table:

| What You See in the Table | When You Read It Again in Learning-Dataset Language |
| --- | --- |
| one row | one student sample |
| columns `region`, `absences`, `score` | candidate input features |
| column `passed` | candidate answer target |
| `X.shape = (4, 3)` | 4 samples, 3 features |
| `y.shape = (4,)` | a bundle of answers for 4 samples |

If this picture is held first, later expressions such as `train_test_split`, `fit`, and `predict` feel less vague.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| Why the table should not be trained as-is | It helps distinguish table structure from model-input structure. | Understand that question-irrelevant columns, answer columns, and identifier columns may be mixed together. |
| Why `X` and `y` are separated | It makes the boundary between input and answer explicit. | Understand that the learning structure becomes clearer when input and the thing to predict are separated. |
| Why data is split first | It becomes the standard for preventing leakage and inflated evaluation. | Understand that the reason is to prevent information meant for later evaluation from leaking into training early. |

| Term | Meaning to Fix First in This Section |
| --- | --- |
| dataset | A bundle of samples and variables organized for learning or evaluation. |
| feature | A column or value to be used as model input. |
| target | The answer column the model should predict. |
| validation | Intermediate evaluation data used to compare settings and choices. |
| data leakage | The problem where information unavailable at prediction time gets mixed into the learning process in advance. |

## Do Not Train the Table as It Is; Reorganize It for the Question

The original table is often organized so that a person can read it easily, but it is not always in a shape that a model can learn from directly.

For example, consider the following table.

| student_id | name | region | absences | score | passed |
| --- | --- | --- | ---: | ---: | --- |
| S001 | Kim | Seoul | 1 | 82 | yes |
| S002 | Park | Busan | 5 | 45 | no |
| S003 | Lee | Seoul | 0 | 90 | yes |
| S004 | Choi | Busan | 2 | 73 | yes |

A person can ask several questions from this table.

- Do we want to predict the score?
- Do we want to classify pass/fail?
- Do we want to inspect trends by region?

Even with the same table, if the question changes, the structure of the learning dataset changes as well.

| Question | Candidate `y` | Candidate `X` |
| --- | --- | --- |
| Are we predicting pass/fail? | `passed` | `region`, `absences`, `score`, and so on |
| Are we predicting the score? | `score` | reconsider whether to exclude `passed`, along with `region`, `absences` |
| Are we identifying the student? | a separate problem definition is needed | `student_id` and `name` usually play identifier roles |

So dataset preparation is more accurately read not as `organizing a table`, but as `drawing the boundary between inputs and answers again according to the question`.

## Separate `X` and `y`

The scikit-learn documentation typically uses `X` for the input feature matrix and `y` for the target. In the glossary, a feature is described as a quantity that represents a sample with numerical or categorical values, and features are described as columns in a data matrix. A sample is usually described as one feature vector, and a target as the dependent variable in supervised learning.

At this stage, it is enough to remember the following difference.

- `X`: the bundle of input columns the model will look at and use for judgment
- `y`: the answer column the model should predict

A small example helps.

Problem situation: when turning the student table into a classification problem that predicts pass/fail, you first need to divide it into input `X` and answer `y`.
Input: a small `DataFrame` containing region, number of absences, score, and pass status for each student.
Expected output: the input-column bundle `X` and the answer column `y` are separated.
Concept to check: preparing a learning dataset is not using the original table unchanged, but dividing inputs and targets according to the problem definition.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
import pandas as pd

df = pd.DataFrame(
    {
        "student_id": ["S001", "S002", "S003", "S004"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
        "absences": [1, 5, 0, 2],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
    }
)

X = df[["region", "absences", "score"]]
y = df["passed"]
```

This code can be read as a classification problem that predicts `passed`.

- Each row is one student sample.
- `region`, `absences`, and `score` are input features.
- `passed` is the answer target.

Seen as a diagram, it looks like this.

```mermaid
--8<-- "assets/part-02/chapter-12/x-y-split-flow-en.mmd"
```

The core point is that `X` and `y` are not fixed from the beginning. The problem definition comes first, and then the columns are divided.

This also keeps the perspective that connects directly to P2-11.2.

| Expression | How to Read It in This Section |
| --- | --- |
| `X.shape[0]` | number of samples |
| `X.shape[1]` | number of features |
| `y.shape[0]` | number of answers, usually equal to the number of samples |

So dividing `X` and `y` does not only mean splitting column names. It also means deciding the shape of the array the model will read.

You can check the same separation with an input that has a few more rows. The input file is the same [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview } used in P2-12.2. One row is one student's learning record. Here, `passed` is the target, and some of the remaining columns are treated as input candidates.

Problem situation: I want to check the shapes of the input column group `X`, the answer column `y`, and a simple train/test candidate split from the original table.
Input: a 36-row student-progress CSV, `feature_columns`, and `target_column`.
Expected output: the shapes of `X`, `y`, encoded input columns, and train/test split candidates.
Concept to check: Dataset preparation means deciding the boundary between input and answer in the table before model training, and separating rows for later evaluation.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

feature_columns = ["region", "study_hours", "absences", "practice_quizzes", "score"]
target_column = "passed"

X = df[feature_columns]
y = df[target_column]
X_encoded = pd.get_dummies(X, columns=["region"], dtype=int)

test_index = df.sample(frac=0.25, random_state=42).index
train_index = df.index.difference(test_index)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("encoded columns:", list(X_encoded.columns))
print("train/test rows:", len(train_index), len(test_index))
```

The same code can be run as [`p2_12_3_dataset_split_preview.py`](/AiBook/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py). This does not train a scikit-learn model. The goal of Part 2 is first to check, at the Pandas level, which columns are inputs, which column is the answer, and which rows should be held out for later checking.

## You Should Not Put Every Column in as-Is

Not every column in the table is suitable as model input. Usually, the following three groups must be separated.

1. columns that can be used directly for prediction
2. columns that need transformation
3. columns that should be excluded from the input

For example:

| Column | Can It Be Used Immediately? | Reason |
| --- | --- | --- |
| `absences` | relatively yes | because it is a numeric column |
| `region` | transformation needed | because it is a string category |
| `student_id` | usually excluded | because it is an identifier and may not itself represent a general pattern |
| `passed` | excluded from input if it is the target | because putting the answer column into the input greatly increases leakage risk |

Here, categorical columns such as `region` may require a step that converts them into a numeric form depending on the model. Pandas `get_dummies()` is introduced as a function that converts categorical variables into dummy/indicator variables.

For example:

Problem situation: many models cannot read a string category such as `region` directly, so its representation must be changed.
Input: input `X` made of the columns `region`, `absences`, and `score`.
Expected output: `X_encoded`, where `region` has been expanded into multiple 0/1 columns.
Concept to check: categorical columns may need to be re-expressed numerically before learning.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
X = df[["region", "absences", "score"]]
X_encoded = pd.get_dummies(X, columns=["region"])

print(X_encoded)
```

The core of this stage is not `memorizing the encoding method`. The more important question is `can this column be read directly like a number, or must its representation be changed first?`

## If You Do Not Distinguish Identifiers and Answer Columns, You Easily Misread the Table

A common confusion is `feeling that every visible column is a feature`. But identifiers and targets play different roles from features.

For example:

- `student_id` is a marker that distinguishes each row.
- `name` is a human-readable name.
- `passed` may be the answer we want to predict.

If you include them in the input unchanged, two problems can appear.

1. The model may be drawn to accidental identifier information rather than general patterns.
2. Information too close to the answer may enter the input and inflate evaluation.

This intuition remains important later as well. A good dataset is not good because it has many columns. It is closer to `a dataset that keeps only the columns appropriate to the problem definition`.

## Split Into Train, Validation, and Test

The next important step in dataset preparation is splitting. The scikit-learn `train_test_split` documentation describes it as a tool that randomly splits arrays or matrices into train and test subsets.

Here, it is enough to understand it like this.

- train: data the model actually learns from
- validation: data used to inspect settings and compare choices
- test: data used at the end as if it were being seen for the first time

Seen as a diagram:

```mermaid
--8<-- "assets/part-02/chapter-12/train-val-test-flow-en.mmd"
```

Why should we split it? Because performing well on data the model has already seen is not enough. What we want to know is `does it work similarly on data it sees for the first time?`

This perspective leads directly to overfitting, generalization, and evaluation metrics in Part 3.

## Split First, and Learn Training-Time Transformations Only from Train

The scikit-learn common pitfalls documentation strongly warns against two mistakes.

- inconsistent preprocessing: the mistake of applying different preprocessing to train data and test data
- data leakage: the mistake of mixing information into the learning process that should be unavailable at prediction time

In particular, the documentation explains that test data should never be used to make choices about the model, and as a general rule advises not to call `fit` or `fit_transform` on test data.

At this stage, the following order is a good standard.

1. Choose input candidates and answer candidates from the full table.
2. Split them into train, validation, and test first.
3. For transformations that must be learned, such as means, standardization, encoding, or feature selection, establish the rule only from train.
4. Apply the same transformation to validation and test without learning from them.

If this order is broken, it becomes similar to letting the model peek at the answers in advance.

If you place the wrong flow and the safer flow side by side:

| Flow | Problem |
| --- | --- |
| make the rule from the full data and split later | test information may leak in advance |
| split first and make the rule only from train | evaluation becomes fairer |

In this Section, we fix this judgment standard before implementation details.

It becomes clearer again in the following diagram.

```mermaid
--8<-- "assets/part-02/chapter-12/no-leakage-preprocessing-flow-en.mmd"
```

If you rewrite the wrong order and the safer order as questions:

| Question | Safer Answer |
| --- | --- |
| Is it okay to organize the whole table and split afterward? | Split first, because information meant for later evaluation may leak in early. |
| Where do we learn the means, standardization rules, and encoding rules? | Learn them only from train. |
| What do validation and test do? | They only receive the same rules learned from train. |

## View It Through a Case

### Case 1. Predicting Pass/Fail While Accidentally Putting the Answer Column into the Input

Suppose a learner wants to build a model that predicts `passed` from a student table. The table contains `student_id`, `region`, `absences`, `score`, and `passed` together. At that point, it is tempting to put every visible column into `X`.

But that creates a problem. `passed` is the answer to predict, yet it also gets included in the input, and `student_id` may be only a marker that distinguishes students rather than something directly related to a general pattern. The model may end up peeking at the answer or being drawn to accidental identifier information instead of learning a real rule.

So in dataset preparation, you first decide `what do we want to predict?`, then separate `y`, and then choose again which features to keep and which columns to remove. After that, train, validation, and test should be split first, and transformations such as encoding or scaling that must learn a rule during training should be established only on the train side.

This case shows that dataset preparation is not simple table organization. Even with the same table, the boundary between `X` and `y` changes according to the question, and if you choose the split order incorrectly, the evaluation may become inflated. Pandas is the tool used in the front part of this process to choose columns and inspect structure, while fair learning evaluation is established only when the later split and transformation order are also correct.

The sentence the reader should especially hold here is the following.

- `Separate X and y first, split into train / validation / test first, and then create transformation rules to learn only from train.`

## Pandas Handles the Front Part of the Preparation Process

Pandas is usually strong in the front part of dataset preparation.

- It reads raw sources such as CSV, Excel, and JSON.
- It chooses only the needed columns.
- It checks invalid values or strange formats.
- It distinguishes categorical columns from numeric columns.
- It performs basic column creation and transformation.

For example:

Problem situation: before model training, you want to inspect with your eyes what shape the input columns and answer column actually have.
Input: separated `X` and `y`.
Expected output: the first few rows of `X` and the first few values of `y`.
Concept to check: Pandas is strong at inspecting table structure and checking column roles before learning.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
X = df[["region", "absences", "score"]]
y = df["passed"]

print(X.head())
print(y.head())
```

Or:

Problem situation: you need to check whether there are missing values and what type each column was read as.
Input: the original `DataFrame` `df`.
Expected output: the count of missing values for each column and the list of data types for each column.
Concept to check: pre-learning inspection is not only about the values themselves, but also about missing values and type structure.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
print(df.isna().sum())
print(df.dtypes)
```

Code like this is closer to `inspect the table before learning` than to `train the model`.

By contrast, the actual split and learning pipeline is often handled together with tools such as scikit-learn.

For example:

Problem situation: after inspection is complete, you need to split the data into train and test to separate learning from evaluation.
Input: input `X`, answer `y`, a split ratio, and a random seed.
Expected output: `X_train`, `X_test`, `y_train`, and `y_test` split into learning and test sets.
Concept to check: the table-manipulation stage and the learning-data split stage are connected, but they are different tasks with different roles.

```python
# This example separates features X and target y from a DataFrame and prepares a learning dataset.
from sklearn.model_selection import train_test_split

X = df[["region", "absences", "score"]]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)
```

The important point here is not memorizing the full function usage, but understanding that `table manipulation` and `learning split` are different stages that connect to each other.

## in One Sentence, What Is Learning-Dataset Preparation?

If we reduce the core of this Section to one sentence, preparing a learning dataset is `reassigning the roles of sample, feature, and target in the original table, and preserving the split order so that evaluation is not distorted`.

Without this perspective, the longer the Pandas code becomes, the easier it is to lose track of why columns are being changed and divided. With this perspective, even before you know every preprocessing technique, you can still ask `is this code choosing the input, choosing the answer, or preventing leakage?`

## Checklist

- Can you say in one sentence what you are trying to predict from the current table?
- Can you distinguish which column is `y` and which columns are candidates for `X`?
- Can you explain why it is risky to put identifier columns and answer columns directly into the input?
- Can you explain why train / validation / test are separated?
- Can you explain why preprocessing rules should be learned only from train?
- When you see `X.shape = (4, 3)` and `y.shape = (4,)`, can you say what is the number of samples and what is the number of features?
- Can you explain that dataset preparation is not using the table as it is, but dividing it into `X` and `y` according to the problem definition?

## Sources and References

- pandas Developers, [pandas.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html){: target="_blank" rel="noopener noreferrer" }, pandas 3.0.4 documentation, checked on 2026-07-20. Used to confirm examples of converting categorical variables into dummy or indicator variables.
- scikit-learn Developers, [Glossary](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn 1.9.0 documentation, checked on 2026-07-20. Used to confirm background for 1d/2d arrays, array-like inputs, estimator input conventions, and the terms `X` and `y`.
- scikit-learn Developers, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn 1.9.0 documentation, checked on 2026-07-20. Used to confirm the API for splitting arrays and matrices into train/test subsets and examples involving `test_size` and `random_state`.
- scikit-learn Developers, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn 1.9.0 documentation, checked on 2026-07-20. Used to confirm cautions about preprocessing order before and after train/test split and data leakage.
