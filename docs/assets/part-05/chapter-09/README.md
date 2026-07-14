# Part 5 Chapter 9 Mermaid Assets

- Public manuscript pages must include their own language asset through `pymdownx.snippets`.
- Current deployment references:
  - Korean pages reference `-ko.mmd`.
  - English pages reference `-en.mmd`.
- The matching `-en.mmd` files remain in this directory as canonical English originals.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow and node relationships.
- Current language pairs:
  - `batch-shape-modality-compare-en.mmd` / `batch-shape-modality-compare-ko.mmd`
  - `batch-tensor-flow-en.mmd` / `batch-tensor-flow-ko.mmd`
  - `cpu-gpu-parallel-flow-en.mmd` / `cpu-gpu-parallel-flow-ko.mmd`
- PNG chart assets:
  - `gpu-batch-score-comparison-en.png` / `gpu-batch-score-comparison-ko.png`
  - `gpu-scalar-multiply-scaling-en.png` / `gpu-scalar-multiply-scaling-ko.png`
- Python chart source:
  - `p5_9_1_gpu_parallel_charts.py`
