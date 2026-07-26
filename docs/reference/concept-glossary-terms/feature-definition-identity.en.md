<a id="feature-definition-identity"></a>
<a id="glossary-feature-definition-identity"></a>

### feature-definition identity

- Meaning: A criterion for checking whether two feature columns or rows share the same definition, not only the same name. It asks whether the unit, generation rule, collection version, and operational definition stayed the same. If the measurement method or calculation rule changed, the same column name may no longer mean the same feature definition.
- Why it matters: Baseline comparison and model input both assume that features with the same role still mean the same thing. Without checking feature-definition identity, a difference caused by a sensor change, unit change, or segment-rule change can be mistaken for a real process change or a model problem. This concept helps readers inspect whether different definitions have been mixed under one column name.
- Related concepts: `feature`, `baseline`, `comparability`, `data quality check`
- Core Section: `P3-6.6`
- Appears in: `P3-6.6`
