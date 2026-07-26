<a id="time-split"></a>
<a id="glossary-time-split"></a>

### time split

- Meaning: A time split is a data split that keeps earlier observations on the training side and later observations on the validation or test side when time order matters. It avoids randomly mixing records that would not have been available together at prediction time.
- Why it matters: Randomly splitting time-ordered data can make performance look better by letting future patterns influence training. A time split asks whether only information available before the later case was used, which helps expose leakage and evaluation-design mistakes.
- Related concepts: `data leakage`, `evaluation design`, `prediction contract`
- Core Section: `P3-9.13`
- Appears in: `P3-9.13`, `P4-4.1`
