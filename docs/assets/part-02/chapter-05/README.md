# Part 2 Chapter 5 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Pyplot-generated chart assets keep the generating script next to the output images and use language-suffixed filenames when visible labels differ by manuscript language.
- The P2-5.2 distribution and variance charts use the same data and layout for Korean, English, and Simplified Chinese. Only graph-reading labels change by language.
- The P2-5.2 histogram uses boundaries 35, 45, 55, 65, 75, 85, 95 with counts 1, 4, 4, 0, 0, 1 and mean 56. It contains no shaded spread interval; variance is compared in the separate A/B chart.
- Current language sets:
  - `p2_5_2_distribution_mean_variance.py`
  - `distribution-mean-variance-summary-en.png` / `distribution-mean-variance-summary-ko.png` / `distribution-mean-variance-summary-zh.png`
  - `same-mean-different-variance-en.png` / `same-mean-different-variance-ko.png` / `same-mean-different-variance-zh.png`
  - `belief-update-flow-en.mmd` / `belief-update-flow-ko.mmd`
  - `dataset-train-test-flow-en.mmd` / `dataset-train-test-flow-ko.mmd`
  - `population-sample-dataset-flow-en.mmd` / `population-sample-dataset-flow-ko.mmd`

## P2-5.5 uncertainty diagrams

- `p2_5_5_uncertainty_diagrams.py` uses NumPy, SciPy and Matplotlib to generate `sd-se-comparison-{ko,en,zh}.svg` and `repeated-confidence-intervals-{ko,en,zh}.svg`.
- The distribution comparison uses exact normal densities with population mean 50, population SD 10, and sample size 100. Shading denotes one SD of each distribution.
- The interval diagram uses 20 independently simulated samples of size 100, seed `20260915`, and 95% t intervals with 99 degrees of freedom. This run covers the true mean in 18 of 20 intervals; no coverage outcome is forced.
- PNG review previews and the plotting cache are saved under `.tmp/p2-5-5-diagrams/`.

## P2-5.3 signed estimation error

- `p2_5_3_estimation_error.py` generates `estimate-error-gap-{ko,en,zh}.svg` on a shared numerical scale in minutes.
- The true mean is 50; estimates 47 and 53 produce signed errors −3 and +3. Arrows run from the true value to each estimate.
- Review PNGs are saved under `.tmp/p2-5-3-review/`.

## P2-5.5 linear and curved correlation

- `p2_5_5_correlation_diagram.py` generates `linear-vs-curved-correlation-{ko,en,zh}.svg` using NumPy and Matplotlib.
- Each panel shows three observations at x = −1, 0, 1. Pearson correlation is 1 for y = 2x + 4 and 0 for y = x².
- Dashed lines show the given analytic relationships, not additional observations or fitted population relationships.
- Review PNGs and the plotting cache are saved under `.tmp/p2-5-5-correlation/`.
