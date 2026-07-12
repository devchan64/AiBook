# Part 5 Chapter 13 Mermaid Assets

- Public manuscript pages should include their own language asset files through `pymdownx.snippets`.
- Current deployment uses the Korean pages with `-ko.mmd` assets and the English pages with `-en.mmd` assets.
- The matching `-en.mmd` files remain in this directory as the canonical English originals.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow and node relationships.
- Current language pairs:
  - `attention-direct-reference-bridge-en.mmd` / `attention-direct-reference-bridge-ko.mmd`
  - `attention-focus-flow-en.mmd` / `attention-focus-flow-ko.mmd`
  - `attention-to-self-attention-bridge-en.mmd` / `attention-to-self-attention-bridge-ko.mmd`
  - `self-attention-token-graph-en.mmd` / `self-attention-token-graph-ko.mmd`
  - `qkv-flow-en.mmd` / `qkv-flow-ko.mmd`
  - `multihead-flow-en.mmd` / `multihead-flow-ko.mmd`
