# Part 2 Chapter 6 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `gradient-descent-loop-flow-en.mmd` / `gradient-descent-loop-flow-ko.mmd`
  - `loss-objective-flow-en.mmd` / `loss-objective-flow-ko.mmd`

## P2-6.1 candidate comparison

- `optimization-search-loop-{ko,en,zh}.mmd` follows the manuscript’s two line candidates through parameter values, predictions, mean squared errors (12.5 and 7.5), and selection.
- The four stages use a vertical layout. The diagram does not claim a global optimum or introduce a third candidate or a constraint absent from the example.
- All language variants share the same values and layout.
- Manuscripts include the Mermaid sources through `pymdownx.snippets`; no pre-rendered SVG copies are maintained.
