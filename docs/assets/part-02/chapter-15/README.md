# Part 2 Chapter 15 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `formula-to-code-flow-en.mmd` / `formula-to-code-flow-ko.mmd` / `formula-to-code-flow-zh.mmd`
  - `ml-reading-flow-en.mmd` / `ml-reading-flow-ko.mmd`
  - `part2-learning-map-flow-en.mmd` / `part2-learning-map-flow-ko.mmd` / `part2-learning-map-flow-zh.mmd`
- Python/Matplotlib assets:
  - `p2_15_1_formula_to_code_mse.py` regenerates `actual-predicted-mse.png`.
