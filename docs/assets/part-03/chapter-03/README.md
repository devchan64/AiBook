# Part 3 Chapter 03 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-3-3-mermaid-01-en.mmd` / `p3-3-3-mermaid-01-ko.mmd`
  - `p3-3-1-mermaid-01-en.mmd` / `p3-3-1-mermaid-01-ko.mmd` / `p3-3-1-mermaid-01-zh.mmd`
  - `p3-3-2-mermaid-01-en.mmd` / `p3-3-2-mermaid-01-ko.mmd` / `p3-3-2-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_3_1_source_operation_log.csv`: P3-3.1 Python example input. Each row is one time-point sensor record inside an operation event, before a sample unit or label candidate has been fixed.
