# P2-12.1 What a Pandas DataFrame Represents

> Section ID: `P2-12.1`
> Version: `v2026.09.15`

## A Table with Rows and Columns

A Pandas DataFrame is a two-dimensional table with labeled rows and columns. In a student score table, one row holds a student's name, score, and pass status, while column names identify what each value means. Within the same table, the score column contains numbers and the name column contains strings.

Using dictionary keys as column names and the value lists as column data creates a table of three students.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee"],
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    }
)

print(df)
```

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

The `0, 1, 2` on the left form the index: the row labels. `name`, `score`, and `passed` are column labels. Excluding the index, the data area has three rows and three columns. Row label 1 contains Park's score of 45 and pass status `no`.

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-en.mmd"
```

## Column Records and Row Records

A list of dictionaries, each containing one student's information, can also become a DataFrame. This code prints the same table as before.

```python
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

The first approach puts `[82, 45, 90]` in the `score` column. The second puts `score: 82` in Kim's record. Although the input is organized differently, the resulting rows and columns are the same.

## Assigning Row Labels

Without an explicit index, the default is a `RangeIndex` of `0, 1, 2, ...`. Specifying names as the index replaces these numbers with Kim, Park, and Lee as row labels.

```python
named = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(named)
```

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

This table has two data columns: `score` and `passed`. Names are in the index, so `named.shape` is `(3, 2)`. The earlier `df` also stores names in a data column, giving `(3, 3)`. A numeric index does not always equal the current row position, and labels can be duplicated.

## Aligning Values by Label

When assigning a Series to a column, Pandas matches index labels rather than simply following value order. Suppose student bonuses are added to the score table indexed by name. The bonuses are ordered Lee, Kim, Park, while the table is ordered Kim, Park, Lee.

```python
bonus = pd.Series([5, 10, 0], index=["Lee", "Kim", "Park"])
adjusted = named.copy()
adjusted["bonus"] = bonus
adjusted["adjusted_score"] = adjusted["score"] + adjusted["bonus"]
print(adjusted[["score", "bonus", "adjusted_score"]])
```

```text
      score  bonus  adjusted_score
Kim      82     10              92
Park     45      0              45
Lee      90      5              95
```

The first value, 5, goes to Lee rather than Kim because labels determine the match. Changing the Lee label in `bonus` to Choi leaves no matching value for Lee in the score table, producing a missing value. Equal lengths do not mean that the same students are paired. In real records where names may repeat, first establish an identifier such as a student ID.

## Column Types and Table Structure

Print the size, column names, index, column types, and first two rows of the earlier `df`. Checking whether `score` has a numeric type helps determine whether calculations such as an average can use it directly.

```python
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

The shape is `(3, 3)`, and `columns` contains `name`, `score`, and `passed`. The index is `RangeIndex(start=0, stop=3, step=1)`, and `head(2)` shows only Kim and Park.

| Check | What it shows in this table |
| --- | --- |
| `shape` | Three students and three data columns |
| `columns` | Names of the name, score, and pass-status columns |
| `index` | Labels attached to rows |
| `dtypes` | Numeric score type and string types for other columns |
| `head(2)` | Actual values for the first two students |

Depending on the Pandas version and settings, string columns may display types such as `str` or `object`. The `yes` and `no` in `passed` are strings here; they do not automatically become Boolean values.

A NumPy array uses one dtype for the entire array, whereas a DataFrame has a dtype for each column. Use a DataFrame to select and organize named columns; numeric columns can then be moved to arrays for vector and matrix calculations.

## A Row and the Unit of Analysis

One row does not always represent one final unit of analysis. These sensor records measure actions A-01 and B-02 at three times each. A row represents one measurement time, and several rows belong to one action.

```python
import pandas as pd

raw = pd.DataFrame(
    [
        ["A-01", 0.0, 0.00, 0.8],
        ["A-01", 1.0, 0.20, 1.4],
        ["A-01", 2.0, 0.40, 1.9],
        ["B-02", 0.0, 0.00, 0.7],
        ["B-02", 1.0, 0.25, 1.3],
        ["B-02", 2.0, 0.50, 1.5],
    ],
    columns=["action_id", "elapsed_seconds", "progress_fraction", "signal_a"],
)

print("rows =", len(raw))
print("actions =", raw["action_id"].nunique())
print(raw.groupby("action_id").size())
```

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

`len(raw)` counts six measurement records. `nunique()` counts two distinct action IDs, and `groupby("action_id").size()` shows three records per action. `elapsed_seconds` is time since the action began, `progress_fraction` is progress as a fraction, and `signal_a` is the measured value.

Adding one measurement row for A-01 increases the total to seven and A-01's count to four, while the number of actions remains two. The result depends on what is being counted. To compare mean signals by action, group measurement rows by `action_id`.

In a customer list, a row may represent one customer; in an order list, the same customer may have several rows. Whether row count can stand for customer count therefore depends on the unit of each record.

## Case: Inspecting a Student CSV

[`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview } contains learning records for 36 students. The first student, S001, is in Seoul and has 8.0 study hours, one absence, nine practice quizzes, a score of 86, and pass status `yes`.

Run this code from the repository root to inspect `(36, 7)`, the seven column names, index, column types, and first three rows.

```python
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

print("shape:", df.shape)
print("columns:", list(df.columns))
print("index:", df.index)
print(df.dtypes)
print(df.head(3))
```

`student_id` is a data column; the left-hand index is a separate sequence from `0` to `35`. `study_hours` includes decimals, while `region` and `passed` are strings. Since some columns are nonnumeric, the entire table cannot be used directly in numeric calculations.

For score prediction, `score` is a target candidate, while study hours, absences, and quiz counts are input candidates. `student_id` identifies the student. Column names and actual values together help determine each column's role.

Changing only S001's score from 86 to 96 in the CSV preserves shape and column names but changes the score shown by `head(3)`. Adding a student row increases the row count to 37. Structure checks and value checks reveal different changes.

To run the same CSV inspection as a file, use this command from the repository root.

[p2_12_1_dataframe_first_check.py](/AiBook/assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_1_dataframe_first_check.py
```

## Types and the Meaning of Values

A numeric score type indicates that calculations are possible, not that the score is correct. A value of 900 in an exam scored out of 100 still has a valid numeric type. Nor does dtype tell you whether 8 in a study-time column means hours or minutes. After reading the structure, check column units, allowed ranges, and recording times.

## Checklist

- Can you explain the roles of rows, columns, and the index?
- Can you explain how a DataFrame holds numeric and string columns together?
- Can you explain how shape differs when names are a data column versus the index?
- Can you explain why measurement count and action count differ?
- Can you explain what changes `shape`, `columns`, `index`, `dtypes`, and `head()` each reveal?
- Can you explain why Series values follow matching student labels even when their order changes?

## Sources and References

- pandas Developers, [pandas.DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-08. DataFrame structure with labeled rows and columns.
- pandas Developers, [Package overview](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-07-20. Background on tabular, time-series, and matrix data.
- pandas Developers, [Migration guide for the new string data type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-08. String dtype displays across versions and settings.
- pandas Developers, [Intro to data structures](https://pandas.pydata.org/docs/user_guide/dsintro.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. label alignment on Series assignment and missing labels.
