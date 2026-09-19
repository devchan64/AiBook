# Part 3 Chapter 01 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-1-1-mermaid-01-en.mmd` / `p3-1-1-mermaid-01-ko.mmd`
  - `p3-1-1-mermaid-02-en.mmd` / `p3-1-1-mermaid-02-ko.mmd`
  - `p3-1-2-mermaid-01-en.mmd` / `p3-1-2-mermaid-01-ko.mmd`
  - `p3-1-3-mermaid-01-en.mmd` / `p3-1-3-mermaid-01-ko.mmd`

## P3-1.1 flow chart

- `p3_1_1_charts.py` generates `p3-1-1-flow-mean-{ko,en,zh}.png` from the fictional A-101/A-102 measurements in the manuscript.
- Identical axes show observed flow, arithmetic means, and the last observed interval. Lines connect measurements; they do not assert continuous linear behavior.
- Rebuild from the repository root: `.venv/bin/python docs/assets/part-03/chapter-01/p3_1_1_charts.py`.
- Requires Matplotlib, NumPy, and `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`. No external figure or dataset is copied.
- Each language manuscript references its matching localized PNG. Image containers retain a 700px minimum width with horizontal scrolling.
