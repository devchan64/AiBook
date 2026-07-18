# Part 3 Chapter 06 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Pyplot-generated chart assets keep the generating script next to the output images and use language-suffixed filenames when visible labels differ by manuscript language.
- The P3-6.2 pyplot chart keeps only graph-reading labels inside the image, such as axes, segment labels, and token labels. Title, description, and summary text stay in the manuscript body instead of being rendered into the PNG.
- Current language sets:
  - `p3-6-1-mermaid-01-en.mmd` / `p3-6-1-mermaid-01-ko.mmd` / `p3-6-1-mermaid-01-zh.mmd`
  - `p3-6-2-mermaid-01-en.mmd` / `p3-6-2-mermaid-01-ko.mmd` / `p3-6-2-mermaid-01-zh.mmd`
  - `p3-6-3-mermaid-01-en.mmd` / `p3-6-3-mermaid-01-ko.mmd` / `p3-6-3-mermaid-01-zh.mmd`
  - `p3-6-4-mermaid-01-en.mmd` / `p3-6-4-mermaid-01-ko.mmd` / `p3-6-4-mermaid-01-zh.mmd`
  - `p3-6-5-mermaid-01-en.mmd` / `p3-6-5-mermaid-01-ko.mmd` / `p3-6-5-mermaid-01-zh.mmd`
  - `p3-6-6-mermaid-01-en.mmd` / `p3-6-6-mermaid-01-ko.mmd`
  - `p3_6_2_segment_tokenization_curve.py`
  - `segment-tokenization-curve-en.png` / `segment-tokenization-curve-ko.png` / `segment-tokenization-curve-zh.png`
