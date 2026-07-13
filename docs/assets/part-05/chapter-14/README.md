# Part 5 Chapter 14 Mermaid Assets

- Deployed manuscript pages must reference their own language asset directly through `pymdownx.snippets`.
- Current public references in this chapter use `-ko.mmd` for Korean pages and `-en.mmd` for English pages.
- The `-en.mmd` files remain the canonical English originals for this chapter.
- When updating a Mermaid asset set, revise the English original first and then sync every deployed language derivative so the conceptual flow stays aligned.
- Current language pairs:
  - `sequential-vs-direct-baseline-en.mmd` / `sequential-vs-direct-baseline-ko.mmd`
  - `transformer-representation-update-en.mmd` / `transformer-representation-update-ko.mmd`
  - `transformer-block-flow-en.mmd` / `transformer-block-flow-ko.mmd`
  - `transformer-task-flow-en.mmd` / `transformer-task-flow-ko.mmd`
  - `long-context-direct-reference-en.mmd` / `long-context-direct-reference-ko.mmd`
  - `long-context-task-flow-en.mmd` / `long-context-task-flow-ko.mmd`
- Current usage note:
  - `transformer-task-flow-en.mmd` / `transformer-task-flow-ko.mmd` are currently kept as reusable chapter assets but are not directly included by the current Part 5 public manuscript pages.
- Matplotlib chart assets:
  - `p5_14_2_sequential_vs_direct_reference.py` regenerates `sequential-vs-direct-reference-ko.png` and `sequential-vs-direct-reference-en.png` for P5-14.2.
