# P2-12.1 What Does a Pandas DataFrame Represent?

> Section ID: `P2-12.1`
> Version: `v2026.07.12`

Part 2 Chapter 11 worked with NumPy arrays for vectors, matrices, axes, and broadcasting. That workflow is strong for numeric computation, but the question changes when we start reading a dataset that looks like a table.

Real data often arrives in a shape like this.

| name | score | passed |
| --- | ---: | --- |
| Kim | 82 | yes |
| Park | 45 | no |
| Lee | 90 | yes |

When we look at this table, we usually read `who`, `which column`, and `which value` before we read position. A Pandas DataFrame is the central structure for exactly this kind of tabular data.

This Section introduces the basic distinction among `DataFrame`, `row`, `column`, and `index`. If the previous NumPy chapter focused on how values appear as vectors and matrices for actual computation, this chapter asks how the same bundle of values should be read as a table of cases and variables. The next chapter will move from this table to plots that reveal patterns not immediately visible in the table. As we continue into selection, aggregation, and dataset preparation, the [concept glossary](../../../reference/concept-glossary.md) remains a useful anchor.

## Scope of This Section

This Section does not cover deep DataFrame manipulation. `loc`, `iloc`, filtering, sorting, aggregation, and missing-value handling are deferred to the next Section.

Here we answer the following questions.

- How is a DataFrame different from a NumPy array?
- What do the row, column, and index of a DataFrame each point to?
- Why is it often more natural to read tabular data through a DataFrame than through an array?
- In a learning dataset, how should we interpret one row and one column?
- What should we check first when we receive a DataFrame?

## Goals of This Section

- You can explain a DataFrame as a labeled two-dimensional tabular data structure.
- You can explain what rows, columns, and the index each identify.
- You can explain that a DataFrame can hold different types, such as numbers and strings, in the same table.
- You can explain why, in machine learning datasets, one row is often read as one case or sample, and one column as one variable or feature.
- You can explain why `shape`, `columns`, `index`, `dtypes`, and `head()` are worth checking first.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| What a DataFrame is | It keeps Pandas from feeling like a mere storage tool and frames it as a structure that reveals tabular meaning. | Understand it as a labeled two-dimensional table. |
| How it differs from an array | It prevents the roles of NumPy arrays and DataFrames from getting mixed together. | Notice row and column names and the ability to hold different column types together. |
| How to begin reading one | It creates the starting point for later selection, aggregation, and dataset preparation. | Begin with the idea that one row is one case and one column is one variable. |

| Term | Working meaning in this Section |
| --- | --- |
| DataFrame | A two-dimensional tabular data structure with row and column labels. |
| row | A horizontal line in the table that often represents one case or observation. |
| column | A vertical line in the table that often represents one variable or attribute. |
| index | A label used to identify each row. |
| label | A name tag attached to a row or column instead of just a position number. |

## A DataFrame Is a Labeled Two-Dimensional Table

The Pandas documentation describes a `DataFrame` as two-dimensional, size-mutable, potentially heterogeneous tabular data. It also explains that rows and columns carry labels and that operations can align by those labels.

Here we read a DataFrame as `a table with named rows and columns, where each column may carry a different meaning and data type`.

If a NumPy array is strong at position-based computation, a DataFrame is strong at revealing `the meaning of the table`.

| Structure | What you look at first | Question it fits naturally |
| --- | --- | --- |
| NumPy array | position, shape, axis | Which value is at which position? Which direction is the calculation moving? |
| Pandas DataFrame | row labels, column labels, column meaning | Which case is this? Which variable is this? Which columns should be compared? |

If NumPy handled computable numeric shapes, this Section rereads the same bundle as a table: what does one row mean, and what variable does one column represent? That perspective connects directly to the next Section on selection and aggregation, the following chapter on visualization, and later sections on keeping records. The first task here is to build a tabular intuition: one row as one case, and one column as one variable.

The simplest construction example uses a `dict` of columns.

Problem situation: you want to build the smallest labeled table and inspect its basic shape.
Input: a `dict` containing the three columns `name`, `score`, and `passed`.
Expected output: a 3-by-3 table containing three students.
Concept to confirm: a DataFrame is a two-dimensional tabular structure with column names.

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

But real raw data often comes in a row-centered form as well. For example, JSON responses or log records frequently arrive as a list of dictionaries.

Problem situation: the same table may arrive not as column groups but as row groups.
Input: a list where each student is stored as one `dict`.
Expected output: the same DataFrame structure as the previous example.
Concept to confirm: a DataFrame can turn both column-centered and row-centered input into the same table structure.

```python
rows = [
    {"name": "Kim", "score": 82, "passed": "yes"},
    {"name": "Park", "score": 45, "passed": "no"},
    {"name": "Lee", "score": 90, "passed": "yes"},
]

df = pd.DataFrame(rows)
print(df)
```

Both approaches can build the same table. We use the following distinction.

- Column-centered input: think first about which values belong to each column.
- Row-centered input: think first about which attributes belong to each case.

Whether the input format is column-centered or row-centered, it does not automatically decide what counts as one sample.

One more warning matters here. In a DataFrame, we should not always assume that `one row = one complete case`. In raw time-series tables, one row may mean `one recorded moment in an action`, not the full action itself.

One row in raw time series may be just one measurement point, while the real comparison target may be the full action formed by many such rows.

| action_id | elapsed_seconds | progress_fraction | signal_a |
| --- | ---: | ---: | ---: |
| A-01 | 0.0 | 0.00 | 0.8 |
| A-01 | 1.0 | 0.20 | 1.4 |
| A-01 | 2.0 | 0.40 | 1.9 |
| B-02 | 0.0 | 0.00 | 0.7 |
| B-02 | 1.0 | 0.25 | 1.3 |
| B-02 | 2.0 | 0.50 | 1.5 |

In a table like this, one row means one moment in time, and an identifier column such as `action_id` becomes the rule that binds several rows into one action. In other words, when reading a DataFrame, we should first separate the question `is one row already one final case?` from the question `do several rows together form one case?`

The next table makes the difference clearer.

| Reading unit | What it means in this table |
| --- | --- |
| one row | one recorded moment from a sensor |
| one `action_id` | one action instance |
| several `action_id` groups | a dataset made of several actions |

This distinction matters because the reading unit changes with the question, even if the DataFrame stays the same. When reading raw time series directly, one row matters. When comparing whole actions, we may need to aggregate multiple rows into one summary row per action.

So a DataFrame provides table structure, but it does not decide the analysis unit for us. First we inspect how rows and columns look, and then we separately judge what the real unit of comparison should be.

For example, simply counting rows per `action_id` already changes the reading unit from `one row` to `one action`.

Problem situation: you want the shortest code that shows how many actions are hidden behind several raw log rows.
Input: a small raw time-series table with `action_id`, `elapsed_seconds`, `progress_fraction`, and `signal_a`.
Expected output: total row count, number of unique `action_id` values, and row counts per `action_id`.
Concept to confirm: in a DataFrame, one row may be one moment in time, and `groupby` can help reread several rows as one action unit.

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

The output can be read roughly like this.

```text
rows = 6
actions = 2
action_id
A-01    3
B-02    3
dtype: int64
```

The key point is the perspective, not the calculation.

- The full DataFrame has 6 rows.
- But the real actions are only 2.
- So a DataFrame can naturally represent situations where several rows together form one case.

This table only shows the structure of the source data. It does not yet tell us anything about quality judgments or causal explanations.

That perspective returns not only in the next Section on filtering and aggregation, but later when we build features or summary tables.

## Read Rows, Columns, and the Index Separately

When people first see a DataFrame, they often focus on the whole table. In practice, we need to read three layers together.

1. row: case, sample, observation
2. column: variable, feature, attribute
3. index: the label that identifies rows

Look at the small example again.

Problem situation: before explaining rows, columns, and the index, we need to look at the simplest table again.
Input: a small `DataFrame` containing name, score, and pass/fail.
Expected output: a table with the default numeric index on the left.
Concept to confirm: one row is one case, and column labels and the index together create the table structure.

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

The output can be read like this.

```text
   name  score passed
0   Kim     82    yes
1  Park     45     no
2   Lee     90    yes
```

Here:

- the `0, 1, 2` on the left are the index,
- `name`, `score`, and `passed` are the column labels,
- and each horizontal line is one row about one person.

The diagram makes that more explicit.

```mermaid
--8<-- "assets/part-02/chapter-12/dataframe-structure-flow-en.mmd"
```

The key point is that the index is not itself a data value. It is the rule for pointing at rows.

## The Index May Be a Simple Number or a Meaningful Label

The Pandas documentation explains that, unless we provide an index separately, a `RangeIndex` is used by default. That is why we often see `0, 1, 2, ...` when a DataFrame is first created.

But the index does not have to be numeric.

Problem situation: you want to confirm that the left side of the table can use meaningful labels instead of plain numbers.
Input: a `DataFrame` with `score` and `passed`, and a list of names passed as the index.
Expected output: a table where `Kim`, `Park`, and `Lee` appear as row labels on the left.
Concept to confirm: the index is a separate structure for identifying rows, not just a default number decoration.

```python
df = pd.DataFrame(
    {
        "score": [82, 45, 90],
        "passed": ["yes", "no", "yes"],
    },
    index=["Kim", "Park", "Lee"],
)

print(df)
```

The output changes like this.

```text
      score passed
Kim      82    yes
Park     45     no
Lee      90    yes
```

Now `Kim`, `Park`, and `Lee` are row labels. We remember the distinction like this.

- Numeric index: points to the default order.
- Label index: points to row identity or row names.

This difference becomes important in the next Section, when we learn selection and filtering.

A tiny experiment makes the distinction even clearer.

Problem situation: you want to inspect the current index structure directly as a Python object.
Input: the `df` built above.
Expected output: index information shaped like `RangeIndex(...)` or `Index([...])`.
Concept to confirm: the index is not visual decoration; it is the structure Pandas uses to manage rows.

```python
print(df.index)
```

With a default numeric index, the output reads like this.

```text
RangeIndex(start=0, stop=3, step=1)
```

If identifier labels are used instead, it can read like this.

```text
Index(['Kim', 'Park', 'Lee'], dtype='object')
```

So the index is not just the left edge of the table. It is another structural layer for identifying rows.

## A DataFrame Can Hold Columns of Different Types Together

NumPy arrays are usually strongest when many values share one common numeric `dtype`. Real tabular data, however, often has one numeric column, one text column, one categorical column, and more.

Even in the simple example above:

- `name` is string-like text,
- `score` is numeric,
- and `passed` can be read as a categorical value stored in text form.

So a DataFrame is more natural for real data because `each column can carry a different meaning`.

This matters when preparing a machine learning dataset. Real data often mixes numbers, dates, text, category-like fields, and missing values.

We can check the types like this.

Problem situation: before making later decisions about selection and preprocessing, you need to know whether each column is numeric or textual.
Input: the `df` containing names, scores, and pass/fail values.
Expected output: type information such as `object` and `int64` for each column.
Concept to confirm: in a DataFrame, types belong to columns individually rather than to the table as one uniform whole.

```python
print(df.dtypes)
```

The output can look roughly like this.

```text
name      object
score      int64
passed    object
dtype: object
```

The key point is not `one type for the whole DataFrame`, but rather `a separate type per column`.

- `score` is a column that can be used directly in numeric work.
- `name` and `passed` are closer to identification and grouping than to direct numeric computation.

We need that intuition later when deciding which columns become model inputs and which need conversion first.

## First Try Reading One Row as One Case and One Column as One Variable

The most important first habit when reading a learning-oriented table is to begin with the assumption that `one row is one case and one column is one variable`.

Suppose we have customer data like this.

| customer_id | age | region | purchased |
| --- | ---: | --- | --- |
| C001 | 29 | Seoul | yes |
| C002 | 41 | Busan | no |
| C003 | 35 | Seoul | yes |

We can read it as follows.

- each row: one customer
- `age`, `region`: candidate input variables or features
- `purchased`: a candidate prediction target

Even before training a model, we need this reading habit so that words like `feature`, `label`, `target`, and `split` do not feel disconnected later.

That sentence is not a universal law, but rather `the default reading pattern we should test first`.

| Table type | Is one row immediately one full sample? |
| --- | --- |
| case tables such as customer lists, order lists, student rosters | often yes |
| raw time-series tables stacked by time | not always |
| already aggregated summary tables | the aggregation unit itself may be the sample |

Of course, not every table follows exactly the same pattern. Some tables are time-ordered logs, and some are already summarized results. Even so, beginning with `row = case, column = variable` is usually helpful.

## A DataFrame Does Not Compete with an Array; They Serve Different Roles

We do not need to think of a DataFrame and a NumPy array as competitors where only one should survive.

They are often used together.

| Task | More natural structure |
| --- | --- |
| reading tabular data, seeing column names, organizing a dataset | DataFrame |
| numeric array computation, vectorization, linear algebra | NumPy array |
| converting just before model input | move from DataFrame to array |

In practice, a common workflow looks like this.

1. Read a CSV into a DataFrame and inspect it.
2. Select the needed columns.
3. Clean missing values and data types.
4. Move to a NumPy array or a model-input shape when numeric computation is required.

So a DataFrame is strong when data should remain an `explainable table`, while NumPy is strong when data should become `an array for computation`.

## What Should You Check First When You Receive a DataFrame?

When a new DataFrame arrives, we do not need to start with complicated manipulation. We should inspect the structure first.

Problem situation: before operating on a new table, you want to quickly inspect its size, column names, index, types, and first rows.
Input: `df`.
Expected output: the results of `shape`, `columns`, `index`, `dtypes`, and `head()`.
Concept to confirm: the first check of a DataFrame is a quick structural sweep.

```python
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head())
```

Each item answers a different question.

| Check | Question |
| --- | --- |
| `shape` | How many rows and columns are there? |
| `columns` | Which columns exist? |
| `index` | How are rows identified? |
| `dtypes` | What type is each column being read as? |
| `head()` | What do the first few rows actually look like? |

These five items form a `first-impression checklist` for a DataFrame.

`dtypes` is especially important. A column may look numeric to the eye but still be stored as text. That becomes important immediately in the next Section on filtering and aggregation.

Here is the same check all at once.

Problem situation: you want to see what the five structural checks look like when executed together.
Input: `df`.
Expected output: table size, column list, index structure, column types, and the first two rows printed in order.
Concept to confirm: a very short block of output can summarize the full outline of a table.

```python
print(df.shape)
print(df.columns)
print(df.index)
print(df.dtypes)
print(df.head(2))
```

The output can be read roughly like this.

```text
(3, 3)
Index(['name', 'score', 'passed'], dtype='object')
RangeIndex(start=0, stop=3, step=1)
name      object
score      int64
passed    object
dtype: object
   name  score passed
0   Kim     82    yes
1  Park     45     no
```

Those five lines already provide a fast structural overview.

- `shape`: table size
- `columns`: list of column names
- `index`: row-label structure
- `dtypes`: column types
- `head(2)`: the actual look of the first rows

Even before we start manipulating the table, these checks tell us much more quickly what kind of data it is.

## Example Case

### Case 1. Where Should You Start When You First Receive an Attendance Table?

Suppose a learner receives a classroom score table. It includes names, regions, absence counts, scores, and whether each student passed. A person can immediately read `who got which score`, but from a model-reading perspective we need to reorganize the view: what does one row represent, and what does each column mean?

At that moment, a DataFrame is not merely a box of numbers. It is a table with labels like `name`, `score`, and `passed`. One row becomes one student case, and one column becomes one variable slot with a different meaning, such as score or absence count. The index also becomes visible as the rule for pointing to rows rather than as a data value.

This case matters because later selection, filtering, and learning-dataset preparation all start from this reading habit. That is why, when a table first arrives, it is often better to check `shape`, `columns`, `dtypes`, and `head()` before writing formulas or model code.

So the beginning of DataFrame reading is closer to a shift in perspective than to memorizing syntax. We need to start reading `a table that looks like a spreadsheet` as `a data structure whose rows and columns already carry roles`. That makes later Pandas operations and machine learning preparation feel far more natural.

## Checklist

- Can you explain a DataFrame as `a table with row and column names`?
- Can you explain the role of row, column, and index separately?
- Can you explain that a DataFrame can hold numeric and text-like columns together?
- Can you explain how one row and one column are often read in a machine learning dataset?
- Can you explain why `shape`, `columns`, `index`, `dtypes`, and `head()` should be checked first?
- Can you explain a DataFrame as a labeled two-dimensional tabular data structure?

## Sources and References

- pandas Developers, `pandas.DataFrame`, pandas API reference, checked 2026-06-25. [https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }
- pandas Developers, `Package overview`, pandas documentation, checked 2026-06-25. [https://pandas.pydata.org/docs/getting_started/overview.html](https://pandas.pydata.org/docs/getting_started/overview.html){: target="_blank" rel="noopener noreferrer" }
