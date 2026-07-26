<a id="underfitting"></a>

## underfitting

- Meaning: Underfitting is a state where a model has not learned enough of the relationships in the data, so performance is weak on both training data and new data. The model may be too simple, or training may not have progressed far enough to capture the important pattern.
- Why it matters: Underfitting helps separate `not learned enough` from `learned the training data too tightly`. Without this distinction, a low score may be misread as overfitting even when the model actually needs more capacity, better features, or more effective training. Underfitting is not a desirable form of generality; it is a failure to capture even the basic pattern needed for the task.
- Related concepts: `generalization`, `overfitting`, `model complexity`
- Core Section: `P1-3.2`
- Appears in: `P4-4.1`, `P4-5.1`, `P4-5.2`
