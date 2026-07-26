<a id="folding-rule"></a>
<a id="glossary-folding-rule"></a>

### folding rule

- Meaning: A folding rule is an explicit rule for reducing several rows, events, or values into one representative result column. For example, it decides whether multiple follow-up events should be kept as `any`, `first`, `worst`, or `count`.
- Why it matters: The same source event and the same follow-up events can produce different result-column meanings when the folding rule changes. The concept helps readers see that a result column is not just a value found in data, but an interpretation structure made by applying a representative rule and often a threshold. Writing the folding rule down also reduces the risk of mixing reporting results with target candidates.
- Related concepts: `source event`, `sample`, `label`, `target candidate`, `threshold`
- Core Section: `P3-5.7`
- Appears in: `P3-5.7`
