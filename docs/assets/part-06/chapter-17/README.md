# Part 6 Chapter 17 Mermaid Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- Current language pairs:
  - `p6-c17-s01-diagram-01-en.mmd` / `p6-c17-s01-diagram-01-ko.mmd`
  - `p6-c17-s01-diagram-02-en.mmd` / `p6-c17-s01-diagram-02-ko.mmd`
- Python-backed chart assets:
  - `p6_17_1_request_structure_matrix_chart.py` generates `request-structure-matrix-ko.png` and `request-structure-matrix-en.png`.
  - `p6_17_2_run_record_status_chart.py` generates `run-record-status-summary-ko.png` and `run-record-status-summary-en.png`.
