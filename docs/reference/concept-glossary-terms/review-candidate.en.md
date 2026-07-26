<a id="review-candidate"></a>
<a id="glossary-review-candidate"></a>

### review candidate

- Meaning: A case that has a change signal and is also judged worth human rechecking in practice. It is stronger than a simple alert, but it is not yet a prediction problem with a stable target label.
- Why it matters: Treating every alert with the same weight wastes review capacity, while raising every review candidate to label prediction overdefines the problem before label quality is ready. Review candidate is the intermediate stage between a comparison report and human priority judgment.
- Related concepts: `alert`, `review queue`, `comparison report`, `label prediction`
- Core Section: `P3-9.1`
- Appears in: `P3-9.1`, `P3-9.9`
