# Part 2 Chapter 12 Assets

- Each manuscript uses its matching `-ko.mmd`, `-en.mmd`, or `-zh.mmd` Mermaid files through `pymdownx.snippets`.
- Update all three language variants together, preserving the data and graph structure.
- The filtering/aggregation diagram separates the selected student list from aggregation over the full table.
- The splitting diagram shows 36 students becoming 27 training candidates and 9 test students, then 18 training and 9 validation students.
- Rendered previews are temporary validation files and are not committed.

## CSV and Python examples

- `student-progress-samples.csv`: shared 36-student input for P2-12.1, P2-12.2, and P2-12.3.
- `p2_12_1_dataframe_first_check.py`: CSV shape, columns, index, types, and first rows.
- `p2_12_2_filter_aggregate_threshold.py`: threshold/region selection and summaries of the full table, in the same region order as the manuscript.
- `p2_12_3_dataset_split_preview.py`: stratified train/test split, input–target alignment, row/student overlap, validation split, and target counts.

Run the scripts with Python. They locate the shared CSV next to their source file. Pandas is required; the splitting example also requires scikit-learn.
