# Part 2 Chapter 10 Learning Assets

- Mermaid files use matching `-ko`, `-en`, and `-zh` variants. Each manuscript includes its own language through `pymdownx.snippets`, using `assets/...` paths.
- `notebook-cell-learning-flow` connects code, output, and interpretation.
- `notebook-experiment-flow` follows the score experiment in P2-10.1.
- `notebook-structure-flow` separates saved document content from kernel memory.
- `notebook-rerun-flow` includes restart, execution, comparison, and correction before saving.
- `notebook-to-module-flow` shows reusable functions imported by both notebooks and scripts.
- `score-record-{ko,en,zh}.ipynb` are self-contained P2-10.3 examples with identical code and localized explanations. They require Python 3 and a notebook interface; no additional calculation packages or external data are needed.
- The notebook scores are original synthetic examples. Change the input/threshold cell, rerun calculation and output, update interpretation, then restart and run all. Empty input deliberately raises `ValueError`.
- Stored outputs are verified examples, not serialized kernel state. Keep the three notebooks synchronized when changing code or baseline data.
