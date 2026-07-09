# P2-12.2 Selection, Filtering, and Aggregation

> Section ID: `P2-12.2`
> Version: `v2026.07.09`

P2-12.2 organizes three common table-reading actions: choose columns or rows, keep rows that satisfy a condition, and summarize many values into fewer numbers.

## Scope of This Section

This Section introduces basic selection, filtering, aggregation, and `groupby` at an entry level.

## Central Question

Why are “what to keep,” “what to remove,” and “what to summarize” different table actions even when they are all done on the same DataFrame?

## Perspective to Keep

- Selection chooses visible parts of the table.
- Filtering keeps or drops rows by condition.
- Aggregation compresses many rows into a smaller summary.
- `groupby` is useful when the summary question depends on categories.

## Short Check

- Can you explain the difference between selecting a column and filtering rows?
- Can you explain why aggregation answers a different question from selection?
- Can you explain why `groupby` often appears before model inspection or reporting?

## Sources and References

- pandas, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- pandas, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
