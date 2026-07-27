<a id="bootstrap"></a>

## bootstrap

- Meaning: Bootstrap sampling draws samples from the original data with replacement. In tree ensembles, it gives each tree a slightly different training sample bundle.
- Why it matters: Bootstrap lets trees start from the same dataset while still having different training experiences. That helps reduce the chance that every tree memorizes the same exception in the same way, and it also creates the basis for out-of-bag checking.
- Related concepts: `sample`, `ensemble`, `validation`
- Core Section: `P4-15.1`
- Appears in: `P4-15.1`, `P4-15.3`
