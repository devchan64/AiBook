# Part 2 Chapter 12 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `dataframe-structure-flow-en.mmd` / `dataframe-structure-flow-ko.mmd`
  - `no-leakage-preprocessing-flow-en.mmd` / `no-leakage-preprocessing-flow-ko.mmd`
  - `table-processing-flow-en.mmd` / `table-processing-flow-ko.mmd`
  - `table-reading-flow-en.mmd` / `table-reading-flow-ko.mmd`
  - `train-val-test-flow-en.mmd` / `train-val-test-flow-ko.mmd`
  - `x-y-split-flow-en.mmd` / `x-y-split-flow-ko.mmd`
- CSV/Python assets:
  - `student-progress-samples.csv` is shared by P2-12.2 and P2-12.3.
  - `p2_12_1_dataframe_first_check.py` reads the CSV and prints the first DataFrame structure checks.
  - `p2_12_2_filter_aggregate_threshold.py` reads the CSV and compares filtering and grouped summaries.
  - `p2_12_3_dataset_split_preview.py` reads the CSV and previews `X`, `y`, encoding, and train/test shapes.
