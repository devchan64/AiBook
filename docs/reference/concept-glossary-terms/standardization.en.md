<a id="standardization"></a>

## standardization

- Meaning: Standardization transforms each feature by subtracting its mean and dividing by its standard deviation so different units and spreads become more comparable. In distance-based models, it can be read as preprocessing that rebalances how much each feature influences distance.
- Why it matters: Without standardization, a large-range feature can dominate distance calculation. After standardization, smaller-range features can affect neighbor selection again, so the before-and-after neighbor composition needs to be inspected.
- Related concepts: `feature scale`, `distance`, `preprocessing`
- Core Section: `P4-12.2`
- Appears in: `P4-12.2`
