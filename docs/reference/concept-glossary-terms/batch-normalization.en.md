<a id="batch-normalization"></a>
<a id="glossary-batch-normalization"></a>

## batch normalization

- Meaning: Batch normalization normalizes activation distributions by using the mean and variance of a batch so the next layer receives values in a more manageable range. It is an internal stabilization step, not only input preprocessing.
- Why it matters: In deep networks, shifting activation distributions can make training unstable. Batch normalization helps stabilize computation and also explains why some layers behave differently in training mode and evaluation mode, where current batch statistics and accumulated statistics are handled differently.
- Related concepts: `training mode`, `evaluation mode`, `numerical stability`
- Core Section: `P5-8.3`
- Appears in: `P5-6.3`, `P5-6.4`, `P5-8.4`
