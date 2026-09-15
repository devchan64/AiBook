# Part 2 Chapter 6 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `gradient-descent-loop-flow-en.mmd` / `gradient-descent-loop-flow-ko.mmd` / `gradient-descent-loop-flow-zh.mmd`
  - `loss-objective-flow-en.mmd` / `loss-objective-flow-ko.mmd` / `loss-objective-flow-zh.mmd`

## P2-6.1 candidate comparison

- `optimization-search-loop-{ko,en,zh}.mmd` follows the manuscript’s two line candidates through parameter values, predictions, mean squared errors (12.5 and 7.5), and selection.
- The four stages use a vertical layout. The diagram does not claim a global optimum or introduce a third candidate or a constraint absent from the example.
- All language variants share the same values and layout.
- Manuscripts include the Mermaid sources through `pymdownx.snippets`; no pre-rendered SVG copies are maintained.

## P2-6.2 objective composition

- `loss-objective-flow-{ko,en,zh}.mmd` combines the four students’ mean squared error (12.5) and the slope penalty (λ = 0.2, a = 10, penalty = 20) into the objective value 32.5.
- The two inputs to the objective are separate terms; regularization is not an extra observation or a hard constraint.

## P2-6.3 gradient descent loss history

- `p2_6_3_training_loss.py` generates `gradient-descent-training-loss-{ko,en,zh}.svg` with NumPy and Matplotlib.
- The plot records 20 full-batch updates on x = [1, 2, 3, 4], y = [55, 65, 80, 90], starting from a = 8, b = 45 with learning rate 0.01. Step 0 precedes all updates.
- The horizontal axis counts updates; it does not represent either parameter or a slice through parameter space.
- `gradient-descent-loop-flow-{ko,en,zh}.mmd` shows prediction, loss, both partial derivatives at the same current position, and simultaneous parameter update.
- Review PNGs are saved under `.tmp/p2-6-3-review/`. The former schematic `gradient-descent-loss-curve-*.svg` files were removed.
