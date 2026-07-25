<a id="groupby"></a>

## groupby

- Meaning: In Pandas, `groupby` first groups rows that share a category value and then calculates summaries such as counts or averages for each group. It changes table reading from row-by-row reading to group-by-group reading.
- Why it matters: Many patterns appear only after rows are grouped by customer, region, month, status, or another category. `groupby` is not just syntax for computing a mean; it is a choice about which groups should be compared and what question the table should answer.
- Related concepts: `aggregation`, `filtering`, `column`
- Core Section: `P2-12.2`
- Appears in: `P2-12.3`
