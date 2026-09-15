# Part 2 Chapter 3 Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- SVG assets follow the same language-suffixed basename rule when the visible labels differ by manuscript language.
- Python examples:
  - `p2_3_6_numpy_linear_algebra.py`: compares dot product, norm, distance and cosine similarity; demonstrates a (3, 2) @ (2, 4) batch, a shape error and its repair. Includes purchase-vector and sample-count experiments.
- Current language sets:
  - `execution-location-flow-en.mmd` / `execution-location-flow-ko.mmd`
  - `vector-space-near-far-en.svg` / `vector-space-near-far-ko.svg` / `vector-space-near-far-zh.svg`

- P2-3.4 coordinate diagrams (self-authored purchase-count example):
  - `vector-distance-ko.png`: distances from q to a and b.
  - `vector-normalization-ko.png`: unit-length vectors and their angular difference.
  - Regenerate all language variants with `python docs/assets/part-02/chapter-03/p2_3_4_vector_comparison_diagrams.py` (Matplotlib and a Korean font required). The script is chart production tooling, not a reader exercise.
  - Matching `-en.png` and `-zh.png` variants are synchronized with the English and Simplified Chinese manuscripts. The same script regenerates all six images.
