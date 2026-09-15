# Part 2 Chapter 15 Assets

- Each manuscript includes its own `-ko.mmd`, `-en.mmd`, or `-zh.mmd` variant.
- `formula-to-code-flow` shows symbol mapping, sample checks, per-sample operations, aggregation, and verification.
- `part2-learning-map-flow` connects calculations, data inspection, visualization, and change records.
- `ml-reading-flow` separates training inputs/targets, test inputs, and test targets. Only test targets and predictions enter final evaluation; validation-based selection is explained in the text.
- `p2_15_1_formula_to_code_mse.py` reproduces the loop/NumPy MSE calculation and the three localized `actual-predicted-mse-*.svg` charts.
- The chart uses sample coordinates and error distances, so it is generated with Matplotlib. Points have different shapes, and vertical segments show paired errors without connecting separate samples.
- The script requires NumPy and Matplotlib. The default font is `Noto Sans CJK JP`; use `--font-family` to select another installed font.
- `--last-prediction` defaults to 8.0. Values 7 and 9 produce MSE 1/6 and 1.5 instead of 0.5.
- `--output-dir .tmp/p2-15-mse` saves previews without replacing published assets. The default destination is this asset directory.
- `--language all|ko|en|zh` selects output languages; the default is all three.
- Each language uses an independent figure. SVG timestamps are omitted and IDs use a fixed salt; byte reproducibility requires the same rendering environment.
- The old shared English PNG is replaced by localized SVGs. Temporary previews are not committed.
- Verified with NumPy 2.0.2 and Matplotlib 3.9.4. All three SVGs reproduce byte-for-byte with both all-language and single-language runs in this environment.
