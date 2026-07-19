# Part 3 Chapter 05 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-5-1-mermaid-01-en.mmd` / `p3-5-1-mermaid-01-ko.mmd` / `p3-5-1-mermaid-01-zh.mmd`
  - `p3-5-2-mermaid-01-en.mmd` / `p3-5-2-mermaid-01-ko.mmd` / `p3-5-2-mermaid-01-zh.mmd`
  - `p3-5-3-mermaid-01-en.mmd` / `p3-5-3-mermaid-01-ko.mmd` / `p3-5-3-mermaid-01-zh.mmd`
  - `p3-5-4-mermaid-01-en.mmd` / `p3-5-4-mermaid-01-ko.mmd`
  - `p3-5-5-mermaid-01-en.mmd` / `p3-5-5-mermaid-01-ko.mmd`
  - `p3-5-6-mermaid-01-en.mmd` / `p3-5-6-mermaid-01-ko.mmd` / `p3-5-6-mermaid-01-zh.mmd`
  - `p3-5-7-mermaid-01-en.mmd` / `p3-5-7-mermaid-01-ko.mmd` / `p3-5-7-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_5_7_sample_roster.csv`: P3-5.7 Python example input. Each row is one sample that must remain in the folded output, even when it has no follow-up event.
- `p3_5_7_follow_up_events.csv`: P3-5.7 Python example input. Each row is one follow-up event observed after a sample.
- `p3_5_7_event_severity.csv`: P3-5.7 Python example input. Each row maps a follow-up event type to a severity score used by the folding rule.
- `p3_5_6_source_events.csv`: P3-5.6 Python example input. Each row is one source event with a duration and window length used to compare source-event counts with derived overlapping-window counts.
- `p3_5_1_raw_log_segments.csv`: P3-5.1 Python example input. Each row is one flow measurement from a progress segment of one event, with a baseline/recent window label.
- `p3_5_2_segment_patterns.csv`: P3-5.2 Python example input. Each row is one event-level summary with early, middle, and late segment means used to compare equal averages with different patterns.
