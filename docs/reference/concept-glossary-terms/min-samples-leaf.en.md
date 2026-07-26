<a id="min-samples-leaf"></a>

## min_samples_leaf

- Meaning: `min_samples_leaf` is a hyperparameter that sets the minimum number of training samples that must remain in a decision-tree leaf. Larger values make it harder for a leaf to represent only one or two exceptional cases.
- Why it matters: Very small leaves can make a tree speak about training exceptions as if they were stable rules. `min_samples_leaf` reduces that risk by requiring each final decision to be supported by more samples.
- Related concepts: `leaf`, `decision tree`, `overfitting`, `hyperparameter`
- Core Section: `P4-14.2`
- Appears in: `P4-14.2`
