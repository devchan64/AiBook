# Part 3 Chapter 04 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-4-1-mermaid-01-en.mmd` / `p3-4-1-mermaid-01-ko.mmd` / `p3-4-1-mermaid-01-zh.mmd`
  - `p3-4-2-mermaid-01-en.mmd` / `p3-4-2-mermaid-01-ko.mmd` / `p3-4-2-mermaid-01-zh.mmd`
  - `p3-4-3-mermaid-01-en.mmd` / `p3-4-3-mermaid-01-ko.mmd` / `p3-4-3-mermaid-01-zh.mmd`
  - `p3-4-4-mermaid-01-en.mmd` / `p3-4-4-mermaid-01-ko.mmd` / `p3-4-4-mermaid-01-zh.mmd`
  - `p3-4-5-mermaid-01-en.mmd` / `p3-4-5-mermaid-01-ko.mmd`

## CSV Inputs

- `p3_4_1_measurement_log.csv`: P3-4.1 Python example input. Each row is one time-step measurement inside an event.
- `p3_4_1_review_decisions.csv`: P3-4.1 Python example input. Each row is an event-level review decision that should be joined after event-level samples are built.
- `p3_4_4_sample_unit_warning_log.csv`: P3-4.4 Python example input. Each row is one time-point record where an event-level review label is repeated across rows.
- `p3_4_5_sample_coverage.csv`: P3-4.5 Python example input. Each row is one event-level sample with operating-condition columns used to inspect coverage.
