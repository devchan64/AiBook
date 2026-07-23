# Part 2 Chapter 3 Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- SVG assets follow the same language-suffixed basename rule when the visible labels differ by manuscript language.
- Python examples:
  - `p2_3_6_numpy_linear_algebra.py`: checks vector, matrix, batch matrix multiplication, and a real shape mismatch error.
- Current language sets:
  - `execution-location-flow-en.mmd` / `execution-location-flow-ko.mmd`
  - `vector-space-near-far-en.svg` / `vector-space-near-far-ko.svg` / `vector-space-near-far-zh.svg`
