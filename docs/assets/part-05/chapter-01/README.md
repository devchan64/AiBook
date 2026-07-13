# Part 5 Chapter 1 Mermaid Assets

- Public manuscript pages should include their own language asset files through `pymdownx.snippets`.
- Current deployment uses the Korean pages with `-ko.mmd` assets and the English pages with `-en.mmd` assets.
- The matching `-en.mmd` files remain in this directory as the canonical English originals.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow and node relationships.
- Current language pairs:
  - `perceptron-flow-en.mmd` / `perceptron-flow-ko.mmd`
  - `restart-approval-case-flow-en.mmd` / `restart-approval-case-flow-ko.mmd`
  - `linear-boundary-flow-en.mmd` / `linear-boundary-flow-ko.mmd`
  - `activation-threshold-flow-en.mmd` / `activation-threshold-flow-ko.mmd`
  - `xor-limit-flow-en.mmd` / `xor-limit-flow-ko.mmd`
- SVG chart assets:
  - `linear-boundary-xor-en.svg` / `linear-boundary-xor-ko.svg`
