# P2-12.2 Selection, Filtering, and Aggregation

> Section ID: `P2-12.2`
> Version: `v2026.09.15`

## A Student Score Table

Create a table of four students with names, scores, pass status, and regions. Each student occupies one row; scores and regions can be used to select rows or calculate averages.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "name": ["Kim", "Park", "Lee", "Choi"],
        "score": [82, 45, 90, 73],
        "passed": ["yes", "no", "yes", "yes"],
        "region": ["Seoul", "Busan", "Seoul", "Busan"],
    }
)

print(df)
```

The output is:

```text
   name  score passed region
0   Kim     82    yes  Seoul
1  Park     45     no  Busan
2   Lee     90    yes  Seoul
3  Choi     73    yes  Busan
```

```mermaid
--8<-- "assets/part-02/chapter-12/table-reading-flow-en.mmd"
```

## Series and DataFrame

`df["score"]` returns the score column as a `Series`, a one-dimensional collection of values with an index.

```python
print(df["score"])
```

The output looks like this:

```text
0    82
1    45
2    90
3    73
Name: score, dtype: int64
```

The result is a `Series`, rather than a `DataFrame`. Read a Series as a one-dimensional column of indexed values, not as a table containing one row.

```python
print(df[["name", "score"]])
```

The result is a four-row, two-column DataFrame containing names and scores. Passing a list with one column name, as in `df[["score"]]`, preserves a four-row, one-column DataFrame.

```text
   name  score
0   Kim     82
1  Park     45
2   Lee     90
3  Choi     73
```

```python
print(type(df["score"]).__name__)
print(type(df[["name", "score"]]).__name__)
```

The output is:

```text
Series
DataFrame
```

## Labels and Positions

The Pandas documentation describes `.loc` as label-based selection and `.iloc` as integer-position-based selection.

```python
print(df.loc[1])
print(df.iloc[1])
```

Both statements print Park's row because label 1 and the second position currently identify the same row.

Changing the index to names makes the distinction clearer.

```python
named = df.set_index("name")

print(named.loc["Lee"])
print(named.iloc[2])
```

Here:

- `named.loc["Lee"]` looks up the label `Lee`.
- `named.iloc[2]` selects the third row by position.

## Slice Endpoints and Row Order

Label slices with `.loc` include the end label, whereas position slices with `.iloc` exclude the end position. Comparing the two on the current default index reveals the difference.

```python
print(df.loc[1:2, "name"].tolist())
print(df.iloc[1:2]["name"].tolist())

ranked = df.sort_values("score", ascending=False)
print(ranked.index.tolist())
print(ranked.loc[0, "name"])
print(ranked.iloc[0]["name"])
```

```text
['Park', 'Lee']
['Park']
[2, 0, 3, 1]
Kim
Lee
```

Sorting changes row positions while preserving existing labels. The first position is therefore Lee, while label 0 still identifies Kim. `reset_index(drop=True)` replaces labels with new position numbers; preserve student identifiers in a separate column when they are needed.

## Selecting Rows by Condition

Selecting students with scores of at least 80 leaves Kim and Lee. The original scores do not change.

```python
print(df[df["score"] >= 80])
```

The output looks like this:

```text
  name  score passed region
0  Kim     82    yes  Seoul
2  Lee     90    yes  Seoul
```

Read the expression in two steps:

1. `df["score"] >= 80` produces `True` or `False` for each row.
2. Only rows marked `True` remain.

Inspect the intermediate result directly:

```python
mask = df["score"] >= 80
print(mask)
```

```text
0     True
1    False
2     True
3    False
Name: score, dtype: bool
```

Such a Boolean result is often called a mask. Filtering asks a question of each row and keeps those that answer True.

Combining a score of at least 70 with region Busan using `&` leaves only Choi. Enclose each condition in parentheses.

```python
print(df[(df["score"] >= 70) & (df["region"] == "Busan")])
```

This selects rows whose scores are at least 70 and whose region is Busan. Use `&` (and) or `|` (or) to combine conditions row by row. Python's `and` and `or` try to evaluate a whole Series as one Boolean value and cannot be used for this purpose.

## Updating Values by Condition

Filtering selects rows; assignment changes values at selected positions. To preserve the original table and add five points to students below 60, copy the table and assign through `.loc[row condition, column]`.

```python
adjusted = df.copy()
low = adjusted["score"] < 60
adjusted.loc[low, "score"] = adjusted.loc[low, "score"] + 5
print(df["score"].tolist())
print(adjusted["score"].tolist())
```

```text
[82, 45, 90, 73]
[82, 50, 90, 73]
```

Do not use chained assignment such as `df[condition]["score"] = ...` to update the original. In particular, pandas 3 Copy-on-Write prevents this from changing the original table. Specify the table and positions in one `.loc` assignment. Distinguish assignment from the earlier read-only expression `df.iloc[1:2]["name"]`.

## Mean, Maximum, and Count

Aggregation reduces multiple values to summaries. The scores `[82, 45, 90, 73]` have mean 72.5, maximum 90, and count 4.

```python
print(df["score"].mean())
print(df["score"].max())
print(df["score"].count())
```

Pass a list of aggregation names to `agg` to collect all three results. `count` excludes missing values.

```python
print(df["score"].agg(["mean", "max", "count"]))
```

The output looks like this:

```text
mean     72.5
max      90.0
count     4.0
Name: score, dtype: float64
```

Read this result as a small summary of the single `score` column in several ways.

## Mean Scores by Region

The Pandas documentation describes `groupby` as splitting data by a criterion, applying a function to each group, and combining the results. For regional mean scores, rows with the same `region` value belong together.

Busan has mean 59 from Park's 45 and Choi's 73. Seoul has mean 86 from Kim's 82 and Lee's 90.

```python
print(df.groupby("region")["score"].mean())
```

The output looks like this:

```text
region
Busan    59.0
Seoul    86.0
Name: score, dtype: float64
```

Read the calculation as follows:

1. Group rows sharing the same `region` value.
2. Select `score` within each group.
3. Calculate each group's mean.

## Missing Values and Aggregation Denominators

If Park's score has not been entered, Busan still has two students but only one observed score: Choi's 73. `size` counts rows, while `count` counts nonmissing values. The mean also excludes missing values by default. `Float64` is a Pandas floating-point type that can hold the missing value `pd.NA`. The conversion distinguishes numbers from unentered values in one column.

```python
missing = df.copy()
missing["score"] = missing["score"].astype("Float64")
missing.loc[1, "score"] = pd.NA
print(missing.groupby("region")["score"].agg(["size", "count", "mean"]))
```

```text
        size  count  mean
region
Busan      2      1  73.0
Seoul      2      2  86.0
```

The Busan mean of 73 does not summarize observed scores for both students. Filling the missing value with zero changes the mean to `(0 + 73) / 2 = 36.5`, interpreting an unentered score as zero points. Reporting total rows and observed-value counts alongside summaries shows what data underlies the calculation.

## Summarizing Sensor Records by Action

Actions A-01 and B-02 were each measured at three times. Grouping by action can place the last recorded time, mean signal, and last observed signal in one row per action.

| action_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

| action_id | last_recorded_seconds | signal_a_mean | last_recorded_signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 2.0 | 1.37 | 1.9 |
| B-02 | 2.0 | 1.17 | 1.5 |

```python
log_df = pd.DataFrame(
    {
        "action_id": ["A-01", "A-01", "A-01", "B-02", "B-02", "B-02"],
        "elapsed_seconds": [0.0, 1.0, 2.0, 0.0, 1.0, 2.0],
        "progress_fraction": [0.00, 0.20, 0.40, 0.00, 0.25, 0.50],
        "signal_a": [0.8, 1.4, 1.9, 0.7, 1.3, 1.5],
    }
)

summary = (
    log_df.sort_values(["action_id", "elapsed_seconds"]).groupby("action_id")
    .agg(
        last_recorded_seconds=("elapsed_seconds", "max"),
        signal_a_mean=("signal_a", "mean"),
        last_recorded_signal_a=("signal_a", "last"),
    )
    .reset_index()
)

print(summary.round(2).to_string(index=False))
```

The output is:

```text
action_id  last_recorded_seconds  signal_a_mean  last_recorded_signal_a
    A-01                    2.0           1.37                     1.9
    B-02                    2.0           1.17                     1.5
```

After sorting by elapsed time, `last` returns the latest signal in this example. By default, `last` skips missing values, so a missing signal at the final time can cause an earlier value to be returned. Without sorting, it selects the last observed value in current row order, not necessarily the latest in time. Both actions have their last record at two seconds, but progress is 0.40 and 0.50 respectively. This is the last observed time, not the completion time of the whole action.

## Case: Changing Threshold and Region

The input is [`student-progress-samples.csv`](/AiBook/assets/part-02/chapter-12/student-progress-samples.csv){ .csv-preview }. Each row is one student's learning record; key columns are `region`, `study_hours`, `absences`, `practice_quizzes`, `score`, and `passed`. Applying a threshold of 75 and region Busan selects S010, S013, S016, and S018.

```python
from pathlib import Path
import pandas as pd

csv_path = Path("docs/assets/part-02/chapter-12/student-progress-samples.csv")
df = pd.read_csv(csv_path)

pass_threshold = 75
focus_region = "Busan"

selected = df.loc[
    (df["score"] >= pass_threshold) & (df["region"] == focus_region),
    ["student_id", "region", "score", "passed"],
]

summary = (
    df.assign(over_threshold=df["score"] >= pass_threshold)
    .groupby("region")
    .agg(
        sample_count=("student_id", "count"),
        mean_score=("score", "mean"),
        over_threshold_count=("over_threshold", "sum"),
        mean_absences=("absences", "mean"),
    )
    .round(2)
)

print(selected)
print(summary)
```

The same calculation can be run from a file.

[p2_12_2_filter_aggregate_threshold.py](/AiBook/assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py)

```bash
python docs/assets/part-02/chapter-12/p2_12_2_filter_aggregate_threshold.py
```

Changing `pass_threshold` among `70`, `75`, and `80` changes the count meeting the threshold; changing `focus_region` changes the selected row list.

```mermaid
--8<-- "assets/part-02/chapter-12/table-processing-flow-en.mmd"
```

Raising the threshold to 80 removes S016, whose score is 77, from the Busan selection, leaving three students. Regional summaries use the full `df`, not `selected`, so mean scores and student counts remain unchanged while counts meeting the threshold change. Changing only `focus_region` to Seoul changes the selected students but does not change regional summaries at all.

The CSV's `passed` column is stored pass status. Changing `pass_threshold` does not recalculate this column, so it must not be treated as equivalent to meeting the current threshold.

## Checklist

- Can you explain the difference between selecting one column and several columns?
- Can you explain what `loc` and `iloc` select by?
- Can you explain how Boolean conditions keep or discard rows?
- Can you explain why mean, count, and maximum are useful summaries?
- Can you explain `groupby` as grouping before summarizing?
- Can you explain which selection results and full regional summaries change when threshold or region changes?
- Can you explain slice endpoint differences and the difference between size and count?

## Sources and References

- pandas Developers, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. Column selection, loc/iloc, inclusive label slices, and Boolean filtering.
- pandas Developers, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. Split-apply-combine, group sizes, nonmissing counts, and means.
- pandas Developers, [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-07-20. DataFrame creation, selection, summary statistics, and table operations.
- pandas Developers, [Copy-on-Write (CoW)](https://pandas.pydata.org/docs/user_guide/copy_on_write.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. chained assignment versus a single loc assignment.
- pandas Developers, [DataFrameGroupBy.last](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.api.typing.DataFrameGroupBy.last.html){: target="_blank" rel="noopener noreferrer" }, pandas documentation, accessed: 2026-09-15. last skipping missing values by default.
