# Part 5 Chapter 12 Mermaid Assets

- Public manuscript pages should include their own language asset files through `pymdownx.snippets`.
- Current deployment uses the Korean pages with `-ko.mmd` assets and the English pages with `-en.mmd` assets.
- The matching `-en.mmd` files remain in this directory as the canonical English originals.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow and node relationships.
- Current language pairs:
  - `rnn-state-flow-en.mmd` / `rnn-state-flow-ko.mmd`
  - `long-term-dependency-flow-en.mmd` / `long-term-dependency-flow-ko.mmd`
  - `state-vs-direct-reference-flow-en.mmd` / `state-vs-direct-reference-flow-ko.mmd`
- Matplotlib chart assets:
  - `p5_12_1_sequence_state_accumulation.py`
  - `sequence-state-accumulation-en.png` / `sequence-state-accumulation-ko.png`
