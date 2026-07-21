# Part 6 Chapter 18 Mermaid Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- P6-18 request flow language pairs:
  - `p6-c18-s01-request-flow-en.mmd` / `p6-c18-s01-request-flow-ko.mmd`
  - `p6-c18-s01-request-routing-en.mmd` / `p6-c18-s01-request-routing-ko.mmd`
  - `p6_18_1_request_structure_matrix_chart.py` generates `request-structure-matrix-ko.png` and `request-structure-matrix-en.png`.
  - `p6_18_2_run_record_status_chart.py` generates `run-record-status-summary-ko.png` and `run-record-status-summary-en.png`.
- Legacy P6-19 history and lineage copies kept here only for compatibility cleanup:
  - `p6-c18-s01-diagram-01-en.mmd` / `p6-c18-s01-diagram-01-ko.mmd`
  - `p6-c18-s02-diagram-01-en.mmd` / `p6-c18-s02-diagram-01-ko.mmd`
  - `p6_18_1_history_computation_gain_chart.py` generates `history-computation-search-gain-ko.png` and `history-computation-search-gain-en.png`.
  - `p6_18_2_lineage_rule_check_chart.py` generates `lineage-rule-check-matrix-ko.png` and `lineage-rule-check-matrix-en.png`.
- CSV example data:
  - `p6-18-lineage-items.csv`
