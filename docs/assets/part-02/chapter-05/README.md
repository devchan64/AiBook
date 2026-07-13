# Part 2 Chapter 5 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Pyplot-generated chart assets keep the generating script next to the output images and use language-suffixed filenames when visible labels differ by manuscript language.
- The P2-5.2 distribution and variance charts use the same data and layout for Korean, English, and Simplified Chinese. Only graph-reading labels change by language.
- Current language sets:
  - `p2_5_2_distribution_mean_variance.py`
  - `distribution-mean-variance-summary-en.png` / `distribution-mean-variance-summary-ko.png` / `distribution-mean-variance-summary-zh.png`
  - `same-mean-different-variance-en.png` / `same-mean-different-variance-ko.png` / `same-mean-different-variance-zh.png`
  - `belief-update-flow-en.mmd` / `belief-update-flow-ko.mmd`
  - `dataset-train-test-flow-en.mmd` / `dataset-train-test-flow-ko.mmd`
  - `population-sample-dataset-flow-en.mmd` / `population-sample-dataset-flow-ko.mmd`
