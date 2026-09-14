# Part 2 Chapter 4 Diagram Assets

## Function plots

- `p2_4_2_slope_diagrams.py` generates the `linear-slope-constant-{ko,en,zh}.svg` and `curve-slope-changing-{ko,en,zh}.svg` sets for P2-4.2.
- These original diagrams use calculated coordinates for `y=2x+1` and `y=x²`, with numbered axes, secants, and input/output changes on the intervals [0, 1] and [2, 3].
- Run the script with Python and Matplotlib from the repository environment. SVGs are saved beside the script; PNG review previews and the Matplotlib cache are saved under `.tmp/p2-4-2-diagrams/`.
- Labels and accessible descriptions are localized in Korean, English, and Simplified Chinese.

## Mermaid assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `chain-rule-composition-flow-en.mmd` / `chain-rule-composition-flow-ko.mmd`
  - `learning-adjustment-flow-en.mmd` / `learning-adjustment-flow-ko.mmd`
