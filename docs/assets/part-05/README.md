# Part 5 Shared Mermaid Assets

- Public manuscript pages must reference their own language asset directly through `pymdownx.snippets`.
- Current deployment rule:
  - Korean pages reference `-ko.mmd`.
  - English pages reference `-en.mmd`.
  - Simplified Chinese pages reference `-zh.mmd`.
- The `-en.mmd` files remain the canonical English originals, but the deployed page still references its own language asset.
- When updating a shared Mermaid set, revise the English original first and then sync the Korean and Simplified Chinese derivatives so every file keeps the same conceptual flow and the same node relationships.
- Current language sets:
  - `part5-learning-map-en.mmd` / `part5-learning-map-ko.mmd` / `part5-learning-map-zh.mmd`
  - `part5-recap-flow-en.mmd` / `part5-recap-flow-ko.mmd` / `part5-recap-flow-zh.mmd`
