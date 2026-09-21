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
  - `p3_6_2_segment_slopes.csv`
  - `segment-tokenization-curve-en.png` / `segment-tokenization-curve-ko.png` / `segment-tokenization-curve-zh.png`

- P3-6.2 curve: illustrative cumulative reconstruction of CSV event A slopes, starting at zero; horizontal units are segment-boundary indices, vertical values are arbitrary units. It is not a measured raw trace. The original CSV remains unchanged. The generator registers an available Noto CJK font for Korean and Chinese labels.

- P3-6.3 diagrams show two example paths from shared input boundaries: summary features and ordered measurements. Handcrafted features, tokens, and representation learning are not mandatory serial stages; combined designs are also possible.

- P3-6.4 diagrams start from the prediction objective and time, then check column roles and availability. Comparison and input-candidate roles can overlap.

- P3-6.6 diagrams separate unit conversion, measurement/calibration/aggregation checks, and operational-rule versions. Matching metadata strings alone does not establish comparability.
