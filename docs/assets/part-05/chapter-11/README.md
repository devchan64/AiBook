# Part 5 Chapter 11 Diagram Assets

- Deployed manuscript pages must reference their own language asset directly.
- The current Korean public manuscript page in `docs/parts/part-05/chapter-11/section-01.md` references the `-ko.svg` files.
- This chapter currently deploys only the Korean SVG assets, while the Mermaid source set keeps the English originals and Korean derivatives together.
- When revising a diagram, update the English Mermaid original first and then sync the Korean derivative and any exported Korean SVG asset that the manuscript actually includes.
- Current language pairs:
  - `cnn-local-window-baseline-en.mmd` / `cnn-local-window-baseline-ko.mmd`
  - `cnn-object-detection-flow-en.mmd` / `cnn-object-detection-flow-ko.mmd`
  - `cnn-vit-common-input-compare-en.mmd` / `cnn-vit-common-input-compare-ko.mmd`
  - `convolution-pooling-flow-en.mmd` / `convolution-pooling-flow-ko.mmd`
  - `filter-reading-options-en.mmd` / `filter-reading-options-ko.mmd`
  - `vit-patch-flow-en.mmd` / `vit-patch-flow-ko.mmd`
