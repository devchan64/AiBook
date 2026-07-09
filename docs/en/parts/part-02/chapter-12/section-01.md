# P2-12.1 What Does a Pandas DataFrame Represent?

> Section ID: `P2-12.1`
> Version: `v2026.07.07`

P2-12.1 shifts from NumPy arrays to labeled tables. The point is not that DataFrame replaces arrays, but that rows, columns, and labels help us read cases and variables more directly.

## Scope of This Section

This Section introduces the DataFrame as a labeled two-dimensional table and separates rows, columns, and index reading.

## Central Question

Why is a DataFrame often the natural first structure for reading a dataset before turning it into model input arrays?

## Perspective to Keep

- A DataFrame is a labeled table, not just a raw numeric matrix.
- One row is often read as one case, and one column as one variable.
- The index may be a simple position or a meaningful label.
- Arrays and DataFrames are not competitors; they answer different questions.

## Short Check

- Can you explain why labels matter when reading real datasets?
- Can you explain the difference among row, column, and index?
- Can you explain why mixed column types fit naturally in a DataFrame?

## Sources and References

- pandas, [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
