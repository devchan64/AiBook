# Part 5 Chapter 15 Mermaid Assets

- Public manuscript pages must include their own language asset through `pymdownx.snippets`.
- Current deployment references:
  - Korean pages reference `-ko.mmd`.
  - English pages reference `-en.mmd`.
- The matching `-en.mmd` files remain in this directory as canonical English originals.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow and node relationships.
- Current language pairs:
  - `generative-model-flow-en.mmd` / `generative-model-flow-ko.mmd`
  - `generative-task-flow-en.mmd` / `generative-task-flow-ko.mmd`
  - `sampling-selection-flow-en.mmd` / `sampling-selection-flow-ko.mmd`
  - `sampling-task-flow-en.mmd` / `sampling-task-flow-ko.mmd`
- SVG chart assets:
  - `sampling-distribution-choice-en.svg` / `sampling-distribution-choice-ko.svg`
  - `sampling-candidate-weights-en.svg` / `sampling-candidate-weights-ko.svg`
  - `sampling-choice-counts-en.svg` / `sampling-choice-counts-ko.svg`
- Python chart source:
  - `p5_15_sampling_chart.py`
