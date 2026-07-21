# Part 6 Chapter 19 Mermaid Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- P6-19 history and lineage language pairs:
  - `p6-c19-s01-history-flow-en.mmd` / `p6-c19-s01-history-flow-ko.mmd`
  - `p6-c19-s02-lineage-boundary-en.mmd` / `p6-c19-s02-lineage-boundary-ko.mmd`
  - `p6_19_1_history_computation_gain_chart.py` generates `history-computation-search-gain-ko.png` and `history-computation-search-gain-en.png`.
  - `p6_19_2_lineage_rule_check_chart.py` generates `lineage-rule-check-matrix-ko.png` and `lineage-rule-check-matrix-en.png`.
- Legacy P6-20 understanding copies kept here only for compatibility cleanup:
  - `p6-c19-s01-diagram-01-en.mmd` / `p6-c19-s01-diagram-01-ko.mmd`
  - `p6-c19-s02-diagram-01-en.mmd` / `p6-c19-s02-diagram-01-ko.mmd`
  - `p6_19_1_contextual_label_shift_chart.py` generates `contextual-label-shift-ko.png` and `contextual-label-shift-en.png`.
  - `p6_19_2_understanding_output_chart.py` generates `understanding-output-types-ko.png` and `understanding-output-types-en.png`.
- CSV inputs:
  - `p6-19-lineage-items.csv`: P6-19.2 Python example input. Each row is one lineage candidate for direct-lineage and surrounding-evidence classification.
  - `p6-19-understanding-task-cases.csv`: P6-20.2 Python example input. Each row is one understanding-centered task case for classification, pair relation, or ranking output inspection.
