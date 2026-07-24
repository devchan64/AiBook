# Part 6 Chapter 20 Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- P6-20 encoder and understanding-task language pairs:
  - `p6-c20-s01-encoder-representation-flow-en.mmd` / `p6-c20-s01-encoder-representation-flow-ko.mmd`
  - `p6-c20-s02-understanding-output-flow-en.mmd` / `p6-c20-s02-understanding-output-flow-ko.mmd`
  - `p6_20_1_contextual_label_shift_chart.py` generates `contextual-label-shift-ko.png` and `contextual-label-shift-en.png`.
  - `p6_20_2_understanding_output_chart.py` generates `understanding-output-types-ko.png` and `understanding-output-types-en.png`.
- CSV inputs:
  - `p6-20-understanding-task-cases.csv`: P6-20.2 Python example input. Each row is one understanding-centered task case for classification, pair relation, or ranking output inspection.
  - `p6-20-understanding-task-cases-en.csv`: English companion input for the P6-20.2 translated manuscript and English chart.
