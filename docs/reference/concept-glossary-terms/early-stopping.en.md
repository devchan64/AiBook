<a id="early-stopping"></a>

## early stopping

- Meaning: Early stopping stops training when validation performance no longer improves, even if the training process could continue. In gradient boosting, training performance can keep improving as more stages are added, so validation performance is used to choose where to stop.
- Why it matters: Training score alone can make a model look better and better, while performance on new data has already stopped improving or begun to worsen. Early stopping makes readers ask not `can training continue?`, but `does generalization still improve if training continues?`
- Related concepts: `validation data`, `overfitting`, `gradient boosting`
- Core Section: `P4-16.2`
- Appears in: `P4-16.2`
