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
  - `p3-4-5-mermaid-01-en.mmd` / `p3-4-5-mermaid-01-ko.mmd` / `p3-4-5-mermaid-01-zh.mmd`

## CSV Inputs

- `p3_4_1_measurement_log.csv`: P3-4.1 fictional source-inspection exercise input: 36 measurement rows for E01–E12, three per event. Completion boundaries are not supplied.
- `p3_4_1_review_decisions.csv`: P3-4.1 fictional event-level review records for E01–E36. Only E01–E12 match this section’s measurement input; E13–E36 do not create additional measured samples. Missing-record exercises are hypothetical exclusions and do not change these CSVs.
- `p3_4_4_sample_unit_warning_log.csv`: P3-4.4 fictional source-inspection exercise input. There are 36 time-point rows: A=18, B=9, C=6, D=3. Each action’s review label repeats on its rows (A/C=1, B/D=0); these are not verified fault outcomes. The manuscript compares 24 positive rows with two review actions and lists unit-check candidates at thresholds 1, 3, 9, and 18. The existing CSV is unchanged.
- `p3_4_5_sample_coverage.csv`: P3-4.5 Python example input. Each row is one event-level sample with operating-condition columns used to inspect coverage.

## P3-4.2 Split Experiment

- `p3_4_2_split_log.csv`: fictional observations, 144 rows; eight events A–H, each with 18 time points (0–17 seconds). Columns are `event_id`, `second`, `flow` (L/min), and `review_needed` (synthetic binary event label repeated on its rows).
- `p3_4_2_make_split_log.py`: deterministic generator. Event centers are 10, 30, …, 150; offsets 0.0, +0.2, −0.1 repeat six times per event. Labels for A–H are 1, 0, 1, 0, 1, 0, 0, 1. These are teaching inputs, not measurements or model predictions. Repeated rows do not add independent events.
- The manuscript trains the model from this input. Default row split uses seconds 0–11 for training and 12–17 for evaluation; event split uses A–D for training and E–H for evaluation. Both initially score rows, not events.
- The three `p3-4-2-mermaid-01-*.mmd` sources distinguish choosing split groups from choosing the scoring unit. English is the source; Korean and Simplified Chinese preserve the same branches.

## P3-4.3 Representation Levels

- `p3-4-3-mermaid-01-{en,ko,zh}.mmd`: traces nine fictional time-point observations through three action summaries into two period aggregates. English is the source; Korean and Simplified Chinese preserve the same membership edges.
- The manuscript contains all nine input values and the action/period tables. No Python or CSV asset is needed for this hand-calculation exercise. Period assignment (A and C recent, B baseline) is explicitly assumed, not inferred from elapsed seconds or event-name order.

## P3-4.4 Unit Warning Checks

- `p3-4-4-mermaid-01-{en,ko,zh}.mmd`: distinguishes label scope, within-action consistency, and counting/splitting checks. English is the source; Korean and Simplified Chinese preserve its branches.
- The fixed yes/no Python output was replaced with source-based counting and threshold exercises. Thresholds select inspection candidates; they neither determine fault status nor repair data. The single conflicting A label is a hypothetical exercise, not a CSV edit.

## P3-4.5 Coverage and Evaluation

- `p3_4_5_sample_coverage.csv` is unchanged: 36 fictional action rows, 26 day and 10 night; normal/high/low counts are 25/6/5. Target shares 80/20 and `minimum_count=9` are teaching assumptions, not facts inferred from the CSV or sufficiency standards.
- Manuscript tables inspect condition counts and the empty night/M2/high intersection. The model code creates synthetic `needs_review` from high load or after-maintenance; its scores measure agreement with that rule, not fault detection. E01–E24 train; E25–E36 evaluate. Input-column changes are the model exercise.
- Updated all three `p3-4-5-mermaid-01-{en,ko,zh}.mmd` sources and added the existing Chinese source to the asset inventory. The flow follows target definition, counting, zero conditions, combinations, and application limits; outdated one-case labels were removed.
