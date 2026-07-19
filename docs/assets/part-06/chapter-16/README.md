# Part 6 Chapter 16 Mermaid Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- Current language pairs:
  - `p6-c16-s01-diagram-01-en.mmd` / `p6-c16-s01-diagram-01-ko.mmd`
  - `p6-c16-s02-diagram-01-en.mmd` / `p6-c16-s02-diagram-01-ko.mmd`
- Python example result charts:
  - `p6_16_1_service_constraint_matrix_chart.py` generates `service-constraint-matrix-ko.png` and `service-constraint-matrix-en.png`.
  - `p6_16_2_failure_recovery_split_chart.py` generates `failure-recovery-routing-ko.png` and `failure-recovery-routing-en.png`.
