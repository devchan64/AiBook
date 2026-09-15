# Part 2 Chapter 4 Diagram Assets

## Function plots

- `p2_4_2_slope_diagrams.py` generates the `linear-slope-constant-{ko,en,zh}.svg` and `curve-slope-changing-{ko,en,zh}.svg` sets for P2-4.2.
- These original diagrams use calculated coordinates for `y=2x+1` and `y=x²`, with numbered axes, secants, and input/output changes on the intervals [0, 1] and [2, 3].
- Run the script with Python and Matplotlib from the repository environment. SVGs are saved beside the script; PNG review previews and the Matplotlib cache are saved under `.tmp/p2-4-2-diagrams/`.
- Labels and accessible descriptions are localized in Korean, English, and Simplified Chinese.

- `p2_4_3_gradient_diagram.py` generates `gradient-directions-{ko,en,zh}.svg` for P2-4.3. It plots calculated contours of `L=w₁²+w₂²` and unit direction arrows at `[3,4]`, with equal axis scales. Review PNGs are saved under `.tmp/p2-4-3-diagrams/`.

## Mermaid assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `chain-rule-composition-flow-en.mmd` / `chain-rule-composition-flow-ko.mmd`
  - `learning-adjustment-flow-en.mmd` / `learning-adjustment-flow-ko.mmd` / `learning-adjustment-flow-zh.mmd`

- P2-4.4 uses the learning adjustment flow to show one update for `x=1`, `y=3`, `w=2`, and learning rate `0.1`: prediction, loss, gradient calculation, parameter update, and return to prediction. Displayed numbers describe the first pass.

## P2-4.5 direction and field diagrams

- `p2_4_5_direction_field_diagrams.py` regenerates `partial-vs-directional-derivative-{ko,en,zh}.svg`, `vector-calculus-context-{ko,en,zh}.svg`, and `gradient-descent-update-intuition-{ko,en,zh}.svg`.
- The three plots use exact coordinates for `F=3x+4y`, `L=x²+2y²`, and `Q=(w−3)²`. Vector-field arrows share a scale factor of 0.1; the one-variable update separates parameter displacement from loss change.
- PNG review previews and the Matplotlib cache are saved under `.tmp/p2-4-5-diagrams/`.

## P2-4.6 chain rule diagrams

- `chain-rule-composition-flow-{ko,en,zh}.mmd` shows the forward values `x=1 → y=3 → z=9` in three nodes.
- `chain-rule-backward-flow-{ko,en,zh}.mmd` separates forward values (blue solid arrows) from backward derivatives (red dashed arrows) for `ŷ=wa+b`, `L=(ŷ−t)²`, with `a=2`, `t=5`, `w=b=1`.
