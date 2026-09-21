# Part 3 Chapter 05 Mermaid Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-5-1-mermaid-01-en.mmd` / `p3-5-1-mermaid-01-ko.mmd` / `p3-5-1-mermaid-01-zh.mmd`
  - `p3-5-3-mermaid-01-en.mmd` / `p3-5-3-mermaid-01-ko.mmd` / `p3-5-3-mermaid-01-zh.mmd`
  - `p3-5-4-mermaid-01-en.mmd` / `p3-5-4-mermaid-01-ko.mmd` / `p3-5-4-mermaid-01-zh.mmd`
  - `p3-5-5-mermaid-01-en.mmd` / `p3-5-5-mermaid-01-ko.mmd` / `p3-5-5-mermaid-01-zh.mmd`
  - `p3-5-6-mermaid-01-en.mmd` / `p3-5-6-mermaid-01-ko.mmd` / `p3-5-6-mermaid-01-zh.mmd`
  - `p3-5-7-mermaid-01-en.mmd` / `p3-5-7-mermaid-01-ko.mmd` / `p3-5-7-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_5_7_sample_roster.csv`: P3-5.7 Python example input. Each row is one sample that must remain in the folded output, even when it has no follow-up event.
- `p3_5_7_follow_up_events.csv`: P3-5.7 Python example input. Each row is one follow-up event observed after a sample. P3-5.7 filters days 1–7 inclusive; completion and no duplicates are explicit assumptions because the CSV lacks completion flags and individual follow-up IDs.
- `p3_5_7_event_severity.csv`: P3-5.7 Python example input. Each row maps a follow-up event type to a fictional ordinal severity rank. Threshold selection is separate from recorded failure types; the ranks do not measure severity ratios.
- `p3_5_6_source_events.csv`: P3-5.6 Python example input. Each row is one source event with source and window lengths in observation points (not seconds). The stride experiment yields 453/237/129 windows at strides 5/10/20 while the source-event count stays 36. The CSV is unchanged.
- `p3_5_1_raw_log_segments.csv`: P3-5.1 fictional hand-calculation input, unchanged: 36 observations across six events, with two observations in each preassigned early/mid/late segment. A/B/C are baseline; D/E/F recent. Each row is a flow measurement in L/min; segment and window assignment is already complete. No timestamps or raw progress values are supplied.
- `p3_5_2_segment_patterns.csv`: P3-5.2 fictional source input, unchanged: 36 action summaries with early/middle/late flow means (L/min). `pattern_family` is a generation category, not an operational label. Observation counts and segment durations are not supplied.
- `p3_5_5_missing_segments.csv`: P3-5.5 table and policy exercise input (36 event summaries; unchanged CSV). Distinguishes available means, missing late means with confirmed ends, and unconfirmed ends. Retained events change from 24 to 12, while late-mean comparisons use 12 under either policy. Missing summary values alone do not prove missing raw segments or broken boundaries; operating-condition effects require additional metadata.

## P3-5.1 Aggregation Trace

- The three `p3-5-1-mermaid-01-{en,ko,zh}.mmd` sources show 36 preassigned observations → six action summaries → two aggregates. English is the source; Korean and Chinese preserve its structure.
- The manuscript replaces fixed aggregation code with source-linked tables and two hand-calculation exercises: changing one observation and changing measurement counts. The original CSV remains unchanged; X/Y weighting examples are separate fictional cases.

## P3-5.2 Segment Pattern Charts

- `p3_5_2_plot_patterns.py` reads E01–E03 from the existing CSV and generates `p3-5-2-patterns-{en,ko,zh}.png`. Requires Matplotlib and `/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc`; run from any directory. English is the language source; Korean and Chinese preserve the same plotted values.
- Replaces the three generic Mermaid flowcharts with coordinate plots: category order on x, segment mean flow in L/min on y. Connecting lines are visual guides, not sampled trajectories or elapsed-time axes. Series differ by color, marker and line style.
- Removed fixed pattern-count code in favor of E01–E03 calculations and threshold exercises. Observation-count weights (2/2/6), durations (10/10/40 seconds), and five-action median examples are explicitly separate assumptions, not CSV fields.

## P3-5.3 Alternative Input Representations

- `p3-5-3-mermaid-01-{en,ko,zh}.mmd`: English source and matching Korean/Chinese branches show summaries and ordered sequences as alternatives from the same fictional four observations. A and B have equal mean/max vectors but different sequence order.
- No external data asset or executable example is needed: all observations and calculations are in the manuscript. Completion at 3 seconds and immediate availability are explicit case assumptions; the 1-second prediction and missing-value cases are separate exercises.

## P3-5.4 Window Boundaries

- `p3-5-4-mermaid-01-{en,ko,zh}.mmd`: English source and synchronized Korean/Chinese decision flow specify available information, boundary inclusion, alignment and length handling before selecting summary or sequence representation.
- The 40/80-second cases use integer-second observations and start-inclusive/end-exclusive windows. The early/mid/late rule of 25%/50%/25% is a new illustrative rule, not reconstructed metadata for P3-5.1. All numerical exercises are fully specified in the manuscripts.
