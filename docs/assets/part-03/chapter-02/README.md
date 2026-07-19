# Part 3 Chapter 02 Mermaid Assets

- Korean manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages include the matching `-zh.mmd` files.
- When updating a Mermaid set, keep the node structure aligned across languages and localize only the visible labels and minimal layout wording.
- Current language sets:
  - `p3-2-1-mermaid-01-en.mmd` / `p3-2-1-mermaid-01-ko.mmd` / `p3-2-1-mermaid-01-zh.mmd`
  - `p3-2-2-mermaid-01-en.mmd` / `p3-2-2-mermaid-01-ko.mmd` / `p3-2-2-mermaid-01-zh.mmd`
  - `p3-2-3-mermaid-01-en.mmd` / `p3-2-3-mermaid-01-ko.mmd` / `p3-2-3-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_2_2_event_flow_log.csv`: P3-2.2 Python example input. Each row is one second-level flow measurement for a baseline or recent sample.
- `p3_2_3_first_table_log.csv`: P3-2.3 Python example input. Each row is one time-point record inside an event log that must be grouped before event-level comparison.
