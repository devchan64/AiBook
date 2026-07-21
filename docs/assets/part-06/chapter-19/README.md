# Part 6 Chapter 19 Mermaid Assets

- Korean public manuscript pages can include the `-ko.mmd` files through `pymdownx.snippets`.
- The matching `-en.mmd` files remain in this directory as canonical English originals for future translation work.
- When updating a Mermaid diagram pair, revise the English structure first, then sync the Korean derivative so both files keep the same conceptual flow.
- Current language pairs:
  - `p6-c19-s01-diagram-01-en.mmd` / `p6-c19-s01-diagram-01-ko.mmd`
  - `p6-c19-s02-diagram-01-en.mmd` / `p6-c19-s02-diagram-01-ko.mmd`
- Python example result charts:
  - `p6_19_2_understanding_output_chart.py` generates `understanding-output-types-ko.png` and `understanding-output-types-en.png`.
- CSV inputs:
  - `p6-19-understanding-task-cases.csv`: P6-20.2 Python example input. Each row is one understanding-centered task case for classification, pair relation, or ranking output inspection.
