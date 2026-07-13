# Part 3 Chapter 06 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- SVG assets follow the same language-suffixed basename rule when the visible labels differ by manuscript language.
- Current language sets:
  - `p3-6-6-mermaid-01-en.mmd` / `p3-6-6-mermaid-01-ko.mmd`
  - `segment-tokenization-curve-en.svg` / `segment-tokenization-curve-ko.svg` / `segment-tokenization-curve-zh.svg`
