# Part 1 Python Example Audit

- Date: 2026-07-19
- Scope: `docs/parts/part-01/`, `docs/assets/part-01/`
- Guideline: `management/guidelines/python-example-guidelines.md`

## Summary

Part 1 Korean Section body does not currently contain reader-facing fenced `python` code blocks. The Python files in Part 1 are Matplotlib chart-generation assets in `docs/assets/part-01/chapter-07/`.

The audit therefore treated the two asset scripts as Python examples only insofar as they generate learning visuals used by Part 1. The main guideline risk was whether score/candidate examples merely hard-code labels and print or draw them, rather than deriving an observable result from input values and thresholds.

## Inventory

| Item | Location | Use | Judgment |
| --- | --- | --- | --- |
| Search-space growth chart | `docs/assets/part-01/chapter-07/p1_7_1_search_space_growth.py` | Generates the P1-7.1 chart showing candidate combinations as stages increase | Acceptable as an experiment-style visual asset: candidate counts are computed from stage count and branch factor, not copied as labels only |
| Threshold/action-region chart | `docs/assets/part-01/chapter-07/p1_7_3_threshold_action_regions.py` | Generates the P1-7.3 chart showing candidate scores against operating thresholds | Revised: changed from fixed candidate scores/labels to score derivation from signal components and threshold-region classification |

## Findings

1. No reader-facing Python code blocks were found in Part 1 Korean Section files.
2. Text code blocks in P1-11.1, P1-11.2, and P1-13.1 are conceptual notation examples, not Python examples.
3. The P1-7.1 chart script already satisfies the relevant experimental criterion because changing the stage list or branch factor changes candidate counts and the curve.
4. The P1-7.3 chart script previously encoded final candidate scores directly, so the script mainly rendered an already labeled score example. It has been revised so scores are derived from signal components before being placed against the thresholds.
5. CJK labels in regenerated PNGs depend on a CJK-capable font. Both Part 1 Chapter 7 chart scripts now include `Noto Sans CJK` candidates, and the Korean PNGs were visually checked after regeneration.

## Changes Made

- Updated `p1_7_3_threshold_action_regions.py`:
  - added `POLICY_THRESHOLDS`
  - added signal components for each candidate
  - added `candidate_score()` and `action_region()` functions
  - kept the public graph meaning the same while making the code derive the score placement
- Updated both Part 1 Chapter 7 chart scripts to prefer `Noto Sans CJK KR` and `Noto Sans CJK SC/TC` for Korean and Chinese labels.
- Regenerated:
  - `search-space-growth-en.png`
  - `search-space-growth-ko.png`
  - `search-space-growth-zh.png`
  - `threshold-action-regions-en.png`
  - `threshold-action-regions-ko.png`
  - `threshold-action-regions-zh.png`
- Updated `docs/assets/part-01/chapter-07/README.md`.
- Updated release notes for `P1-7.1` and `P1-7.3`.

## Verification

- `find docs/assets/part-01 docs/parts/part-01 -type f | rg '\\.py$|\\.csv$|\\.json$|\\.ipynb$'`
  - Found only the two Chapter 7 Python chart scripts.
- `rg -n '^```(python|py)' docs/parts/part-01 -g 'section-[0-9][0-9].md'`
  - No reader-facing Python code blocks found.
- `.venv/bin/python docs/assets/part-01/chapter-07/p1_7_1_search_space_growth.py`
  - Completed without warnings after font-candidate update.
- `.venv/bin/python docs/assets/part-01/chapter-07/p1_7_3_threshold_action_regions.py`
  - Completed. A later local rerun emitted CJK font fallback warnings in this environment, so the generated images should be visually checked when the available font set changes.
- Visual check:
  - `threshold-action-regions-ko.png` renders Korean labels correctly.
  - `search-space-growth-ko.png` renders Korean labels correctly.

## Residual Risk

The Part 1 body still contains many conceptual examples with candidate labels, scores, or output snippets, but they are not Python examples. They should be reviewed under manuscript/example quality criteria if the goal later expands from Python examples to all score/candidate examples.
