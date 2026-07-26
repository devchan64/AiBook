<a id="ccp-alpha"></a>

## ccp_alpha

- Meaning: `ccp_alpha` is the complexity parameter used by scikit-learn for Minimal Cost-Complexity Pruning in decision trees. As the value grows, keeping complex branches becomes more costly, so more branches may be pruned.
- Why it matters: `ccp_alpha` controls how much an already grown tree is simplified. If it is too small, leftover branches may overfit; if it is too large, important patterns may be removed and the tree may underfit.
- Related concepts: `pruning`, `decision tree`, `overfitting`, `hyperparameter`
- Core Section: `P4-14.2`
- Appears in: `P4-14.2`
