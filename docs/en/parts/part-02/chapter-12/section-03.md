# P2-12.3 The Intuition of Preparing a Learning Dataset

> Section ID: `P2-12.3`
> Version: `v2026.07.09`

P2-12.3 turns table reading into model-preparation language. It brings together `X`, `y`, samples, features, train/validation/test splits, and the rule that learned transformations should come from train data only.

## Scope of This Section

This Section focuses on introductory dataset preparation logic rather than a full preprocessing pipeline.

## Central Question

How do we reorganize a table into `X` and `y` without mixing identifiers, answers, and training-time rules?

## Perspective to Keep

- A table is not fed to a model unchanged; it is reorganized for a learning question.
- `X` and `y` must be separated clearly.
- Identifier columns and answer columns should not be treated as ordinary features.
- Splitting comes first, and train-only learning rules protect evaluation from leakage.

## Short Check

- Can you explain why `X` and `y` are separated before model training?
- Can you explain why IDs and labels should not simply be left among feature columns?
- Can you explain why train/validation/test order matters for trustworthy evaluation?

## Sources and References

- scikit-learn, [Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- scikit-learn, [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
