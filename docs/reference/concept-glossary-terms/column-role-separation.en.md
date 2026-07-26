<a id="column-role-separation"></a>
<a id="glossary-column-role-separation"></a>

### column-role separation

- Meaning: The practice of reading columns in a working table by role instead of treating every column as the same kind of input. Columns may be feature columns, comparison columns, candidate result columns, or identification/context columns. The first question is not only the value format, but `why was this column created?`
- Why it matters: A summary table can temporarily hold comparison information for people, candidate model inputs, and candidate outcomes in the same place. Without column-role separation, numerical columns can all be mistaken for features, or candidate outcomes can be mixed into features and cause data leakage. This distinction helps explain which columns should remain or be removed before a Part 3 working table is handed to later modeling steps.
- Related concepts: `summary table`, `feature`, `target candidate`, `data leakage`
- Core Section: `P3-6.4`
- Appears in: `P3-6.4`, `P3-8.5`
