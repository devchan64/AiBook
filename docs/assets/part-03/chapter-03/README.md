# Part 3 Chapter 03 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-3-3-mermaid-01-en.mmd` / `p3-3-3-mermaid-01-ko.mmd` / `p3-3-3-mermaid-01-zh.mmd`
  - `p3-3-1-mermaid-01-en.mmd` / `p3-3-1-mermaid-01-ko.mmd` / `p3-3-1-mermaid-01-zh.mmd`
  - `p3-3-2-mermaid-01-en.mmd` / `p3-3-2-mermaid-01-ko.mmd` / `p3-3-2-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_3_1_source_operation_log.csv`: P3-3.1 source-inspection exercise input, created as a fictional log for the book. Contains 36 time-point records across 9 events; no outcome labels. P3-3.1 uses the CSV to distinguish label presence, event linkage, and evidence for labeling criteria. P3-3.2 reuses events A, B, E, F for action means and explicitly assumed baseline/recent groups; no occurrence dates or group labels are present in the source.
