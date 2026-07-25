<a id="data-leakage"></a>
<a id="glossary-baseline-model"></a>

## data leakage

- Meaning: Data leakage occurs when information unavailable at prediction time enters training or evaluation and makes performance look unfairly good.
- Why it matters: Leakage breaks the boundary of a fair experiment. A high score may reflect hidden future information or target-like hints rather than real generalization, so data splitting and preprocessing order must be inspected.
- Related concepts: `dataset`, `validation`, `target`
- Core Section: `P2-12.3`
- Appears in: `P4-7.1`

