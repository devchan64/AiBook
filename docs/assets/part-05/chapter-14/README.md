# Part 5 Chapter 14 Mermaid Assets

- Deployed manuscript pages must reference their own language asset directly through `pymdownx.snippets`.
- Current public references in this chapter use `-ko.mmd` for Korean pages, `-en.mmd` for English pages, and `-zh.mmd` for Simplified Chinese pages.
- The `-en.mmd` files remain the canonical English originals for this chapter.
- When updating a Mermaid asset set, revise the English original first and then sync every deployed language derivative so the conceptual flow stays aligned.
- Current language pairs:
  - `sequential-vs-direct-baseline-en.mmd` / `sequential-vs-direct-baseline-ko.mmd` / `sequential-vs-direct-baseline-zh.mmd`
  - `transformer-representation-update-en.mmd` / `transformer-representation-update-ko.mmd` / `transformer-representation-update-zh.mmd`
  - `transformer-block-flow-en.mmd` / `transformer-block-flow-ko.mmd` / `transformer-block-flow-zh.mmd`
  - `transformer-task-flow-en.mmd` / `transformer-task-flow-ko.mmd`
  - `long-context-direct-reference-en.mmd` / `long-context-direct-reference-ko.mmd` / `long-context-direct-reference-zh.mmd`
  - `long-context-task-flow-en.mmd` / `long-context-task-flow-ko.mmd` / `long-context-task-flow-zh.mmd`
- Current usage note:
  - `transformer-task-flow-en.mmd` / `transformer-task-flow-ko.mmd` are currently kept as reusable chapter assets but are not directly included by the current Part 5 public manuscript pages.
- Matplotlib chart assets:
  - `p5_14_1_transformer_block_charts.py` regenerates `transformer-block-action-stage-trace-ko.png`, `transformer-block-action-stage-trace-en.png`, `transformer-block-action-stage-trace-zh.png`, `transformer-block-action-residual-compare-ko.png`, `transformer-block-action-residual-compare-en.png`, and `transformer-block-action-residual-compare-zh.png` for P5-14.1.
  - `p5_14_2_sequential_vs_direct_reference.py` regenerates `sequential-state-decay-ko.png`, `sequential-state-decay-en.png`, `sequential-state-decay-zh.png`, `direct-reference-match-scores-ko.png`, `direct-reference-match-scores-en.png`, and `direct-reference-match-scores-zh.png` for P5-14.2.
