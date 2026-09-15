# P2-12.3 Intuition for Preparing a Learning Dataset

> Section ID: `P2-12.3`
> Version: `v2026.09.15`

## Prediction Time and Input Columns

A learning dataset pairs the inputs a model uses with the answers it should predict. Even in the same student table, usable columns differ between predicting pass status before an exam and calculating it from scores after the exam.

| Column | Role in predicting pass status before the exam |
| --- | --- |
| `student_id` | Identifier distinguishing students |
| `region` | Categorical input candidate known at prediction time |
| `absences` | Input candidate counted up to prediction time |
| `score` | Excluded: the result of an exam not yet taken |
| `passed` | Answer to predict |

The final score is unavailable before the exam. Including it merely because historical records contain it supplies training with information unavailable at prediction time. This is data leakage. If final pass status follows a score rule, determining it from the score can instead be handled by directly applying that rule.

## Inputs X and Targets y

`X` is the table of input features, and `y` is the target collection: the answers. In this table, select pre-exam region and absence count as input candidates and separate pass status as the target.

```python
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

X = df[["region", "absences"]]
y = df["passed"]

print(X)
print(y)
print(X.shape, y.shape)
```

`X` contains region and absence count for four students, while `y` contains `["yes", "no", "yes", "yes"]`. Their shapes are `(4, 2)` and `(4,)`: four students with two features each, and their four answers. Handle `X` and `y` together so that changes in row order do not pair a student with someone else's answer.

```mermaid
--8<-- "assets/part-02/chapter-12/x-y-split-flow-en.mmd"
```

`student_id` identifies records when linking them. Exclude it as an input unless there is a reason to believe the number itself explains achievement. Including `passed` in the inputs lets a model read the answer directly, preventing meaningful evaluation of predictive ability.

## Separating Training, Validation, and Test Data

Training data teaches the model its rules. Validation data compares model types or settings, and test data is reserved for the final evaluation after selection. Using the same records for training and evaluation makes it difficult to distinguish memorization from predictive ability on new records.

```mermaid
--8<-- "assets/part-02/chapter-12/train-val-test-flow-en.mmd"
```

`train_test_split` can randomly separate independent records from different students. Repeated records from a student or data with temporal order require attention to student groups or time order. Randomly splitting rows does not prevent every form of leakage.

## Case: Splitting 36 Students into 27 and 9

Prepare data for predicting pass status before the exam using the 36 students in [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }. Assume study hours, absences, and quiz counts were all available by prediction time. Exclude final `score` and the answer `passed` from the inputs.

Run from the repository root. Input shape is `(36, 3)` and target shape is `(36,)`. Set aside 25% of rows, or nine students, for testing and leave 27 for training.

```python
from pathlib import Path
from sklearn.model_selection import train_test_split

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

feature_columns = ["study_hours", "absences", "practice_quizzes"]
X = df[feature_columns]
y = df["passed"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print("X shape:", X.shape)
print("y shape:", y.shape)
print("train/test shapes:", X_train.shape, X_test.shape, y_train.shape, y_test.shape)
```

```text
X shape: (36, 3)
y shape: (36,)
train/test shapes: (27, 3) (9, 3) (27,) (9,)
```

Changing `test_size` to `0.5` gives 18 training and 18 test students. Changing `random_state` may select different students, but the counts stay the same at a fixed ratio. This code creates training and test sets without a separate validation set. To compare model settings, split validation data from the training side or use cross-validation.

`stratify=y` keeps pass/fail proportions as similar as possible in both sets. Whole-student counts may prevent exact equality. Stratified splitting can fail when a class has too few records or a resulting set is too small. A fixed `random_state` reproduces a split under the same input and execution conditions; a single split does not guarantee representativeness.

## Checking Input–Target Pairs and Student Overlap

Student order in `X` and `y` must already match before splitting. `train_test_split` does not look up student IDs to repair mismatched pairs; it preserves the current positional pairing of the arrays supplied together. Returned indices can be used to check alignment and overlap between sets.

```python
print(X_train.index.equals(y_train.index))
print(X_test.index.equals(y_test.index))
print(set(X_train.index).isdisjoint(X_test.index))

train_ids = set(df.loc[X_train.index, "student_id"])
test_ids = set(df.loc[X_test.index, "student_id"])
print(train_ids.isdisjoint(test_ids))
```

```text
True
True
True
True
```

The first two results mean input and target labels have the same order; the third means rows do not overlap. The fourth confirms that student IDs do not overlap either. This CSV has one row per student, but repeated records can put the same student in different rows. To evaluate predictions for new students in that situation, split by student.

## Reserving Nine Students for Validation

Taking nine validation students from the 27 training candidates leaves 18 training, nine validation, and nine test students. The test set does not participate in this second split.

```python
X_fit, X_val, y_fit, y_val = train_test_split(
    X_train, y_train, test_size=9, random_state=42, stratify=y_train
)
print(len(X_fit), len(X_val), len(X_test))
```

```text
18 9 9
```

`test_size=9` means nine rows, whereas `test_size=0.25` means 25% of the input rows. When comparing models with these three sets, learn preprocessing criteria and train models using `X_fit`, select settings using validation results, and use the test set for final evaluation. These 36 students illustrate the splitting procedure; they are not a basis for a stable performance estimate.

The same splitting and overlap checks can be run from a file.

[p2_12_3_dataset_split_preview.py](/AiBook/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_3_dataset_split_preview.py
```

## Learning Preprocessing Criteria from Training Data

Filling missing values with a mean or standardizing values requires criteria such as means and standard deviations calculated from data. Learn these only from training data, then apply the same criteria to validation and test data. Computing a mean that includes test data mixes evaluation information into training.

```mermaid
--8<-- "assets/part-02/chapter-12/no-leakage-preprocessing-flow-en.mmd"
```

Suppose training study hours are `[2.0, 4.0, missing]` and test hours are `[10.0, missing]`. The observed training mean is 3, so fill missing values in both sets with 3.

```python
train_hours = pd.Series([2.0, 4.0, None])
test_hours = pd.Series([10.0, None])

fill_value = train_hours.mean()
print(train_hours.fillna(fill_value).tolist())
print(test_hours.fillna(fill_value).tolist())
```

```text
[2.0, 4.0, 3.0]
[10.0, 3.0]
```

Using all observed values would give `(2 + 4 + 10) / 3`, about 5.33, injecting test information into the filled training value. Even if the test value changes from 10 to 100, the training-derived fill value must remain 3.

In scikit-learn, `fit` learns criteria and `transform` applies learned criteria. Do not call preprocessing `fit` or `fit_transform` on test data.

## Representing Categories as Numeric Columns

String categories such as region may need numeric representations, depending on the model. `get_dummies` creates an indicator column per region, with 1 for that region and 0 otherwise. This small table produces Busan and Seoul columns.

```python
regions = pd.DataFrame({"region": ["Seoul", "Busan", "Seoul"]})
encoded = pd.get_dummies(regions, columns=["region"], dtype=int)
print(encoded)
```

```text
   region_Busan  region_Seoul
0             0             1
1             1             0
2             0             1
```

This standalone example only demonstrates category representation. Calling `get_dummies` separately on training and test data can produce different columns depending on the regions present. In actual training, learn the categories and column layout from training data, apply that layout to test data, and define how to handle unseen categories.

## Checking Missing Values and Types

Checking missing counts and types by column reveals values that need filling or columns that need numeric conversion. In this student CSV, the code reports zero missing values in every column. That means no values are missing; it does not establish that recording times or answers are correct.

```python
print(df.isna().sum())
print(df.dtypes)
```

For a numeric field containing the string `"unknown"`, `isna()` alone will not detect the unentered value. This code converts values that cannot be interpreted as numbers into missing values.

```python
hours_text = pd.Series(["8.0", "unknown", "6.5"])
hours = pd.to_numeric(hours_text, errors="coerce")
print(hours.isna().tolist())
print(hours.dropna().tolist())
```

```text
[False, True, False]
[8.0, 6.5]
```

`errors="coerce"` turns invalid strings into missing values without interpreting what they mean. If the missing count increases after conversion, inspect the original notation and input errors before deciding how to handle them. Even successfully parsed numbers can be outside allowed ranges, such as negative study hours.

## Checklist

- Can you define prediction time and the target in one sentence?
- Can you explain why final scores are excluded from pre-exam inputs?
- Can you align rows of `X` and `y` for the same students?
- Can you distinguish training, validation, and test roles?
- Can you explain why changing test values must not change preprocessing criteria learned from training?
- Can you explain why category encoding must use matching training and test columns?
- Can you distinguish row overlap from student overlap and reserve validation data from the training candidates?

## Sources and References

- pandas Developers, [pandas.get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-07-20. Indicator columns for categorical variables.
- scikit-learn Developers, [Glossary](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, accessed: 2026-07-20. Array shapes, estimator input conventions, and X/y terminology.
- scikit-learn Developers, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, accessed: 2026-09-15. Joint splitting of inputs and targets, test_size, random_state, and stratify.
- scikit-learn Developers, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn documentation, accessed: 2026-09-15. Training-only preprocessing and leakage prevention.
- pandas Developers, [pandas.to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. numeric conversion failures with errors="coerce".
