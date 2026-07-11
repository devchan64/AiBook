# Part 2 Chapter 14 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `branch-review-deploy-flow-en.mmd` / `branch-review-deploy-flow-ko.mmd`
  - `git-three-areas-flow-en.mmd` / `git-three-areas-flow-ko.mmd` / `git-three-areas-flow-zh.mmd`
