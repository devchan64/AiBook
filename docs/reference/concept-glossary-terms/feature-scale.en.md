<a id="feature-scale"></a>

## feature scale

- Meaning: Feature scale is the unit, range, and spread of values in one feature. In distance-based models such as k-NN, a feature with a large scale can dominate the calculation of nearness.
- Why it matters: Numeric features are not automatically read with equal weight. If a large-range feature such as income hides a small-range feature such as late-payment count, the model may follow the large numeric axis more strongly than the actual meaning of the data warrants.
- Related concepts: `distance`, `standardization`, `preprocessing`
- Core Section: `P4-12.2`
- Appears in: `P4-12.2`, `P4-12.3`
