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
