# Part 2 Chapter 10 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `notebook-cell-learning-flow-en.mmd` / `notebook-cell-learning-flow-ko.mmd`
  - `notebook-experiment-flow-en.mmd` / `notebook-experiment-flow-ko.mmd`
  - `notebook-rerun-flow-en.mmd` / `notebook-rerun-flow-ko.mmd`
  - `notebook-structure-flow-en.mmd` / `notebook-structure-flow-ko.mmd`
  - `notebook-to-module-flow-en.mmd` / `notebook-to-module-flow-ko.mmd`
