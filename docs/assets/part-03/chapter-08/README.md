# Part 3 Chapter 08 Assets

- Korean public manuscript pages include the `-ko.mmd` files through `pymdownx.snippets`.
- English translation pages include the matching `-en.mmd` files.
- Simplified Chinese translation pages use `-zh.mmd` only when a diagram needs localized labels. Diagrams that remain English are shared from the `-en.mmd` original.
- Each Mermaid set uses a flat filename pattern so language variants stay grouped by basename.
- When updating a Mermaid diagram set, revise the English original first. Sync the Korean derivative, and add or refresh a Simplified Chinese derivative only when the diagram itself needs localized labels.
- Current language sets:
  - `p3-8-1-mermaid-01-en.mmd` / `p3-8-1-mermaid-01-ko.mmd`
  - `p3-8-2-mermaid-01-en.mmd` / `p3-8-2-mermaid-01-ko.mmd`
  - `p3-8-3-mermaid-01-en.mmd` / `p3-8-3-mermaid-01-ko.mmd`
  - `p3-8-4-mermaid-01-en.mmd` / `p3-8-4-mermaid-01-ko.mmd`
  - `p3-8-5-mermaid-01-en.mmd` / `p3-8-5-mermaid-01-ko.mmd`
  - `p3-8-6-mermaid-01-en.mmd` / `p3-8-6-mermaid-01-ko.mmd` / `p3-8-6-mermaid-01-zh.mmd`
  - `p3-8-7-mermaid-01-en.mmd` / `p3-8-7-mermaid-01-ko.mmd` / `p3-8-7-mermaid-01-zh.mmd`

## P3-8.2 box plot

- `p3-8-2-boxplot.svg` is a shared figure with English group/axis labels explained in each manuscript.
- `p3_8_2_boxplot.py` reads the existing `../chapter-04/p3_4_1_measurement_log.csv`; no dataset copy is maintained. It selects one flow value per operation at `elapsed_seconds=2` and groups by `is_recent`.
- Quartiles are medians of the sorted lower/upper halves. Whiskers show min/max; dots show all six observations per group. This fictional grouping does not establish matched conditions or a normal baseline.
- Regenerate from repository root: `.venv/bin/python docs/assets/part-03/chapter-08/p3_8_2_boxplot.py`. A PNG preview is written to `/tmp/p3-8-2-boxplot.png` for visual inspection only.
- The chart is original; NIST references in the manuscript support concepts, not the fictional data or cause hypotheses.
