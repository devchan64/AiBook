<a id="hessian"></a>

## hessian

- Meaning: A hessian collects second-order derivative information for a multivariable function. In this book's boosting context, it can be read as second-order information about how sensitively the loss bends around the current prediction.
- Why it matters: If the gradient says `which direction should the model move?`, the hessian adds information about how carefully to move in that direction. Some boosting implementations use second-order information when computing splits and leaf values, so this term helps readers understand why hessian appears in implementation comparisons.
- Related concepts: `gradient`, `loss function`, `gradient boosting`
- Core Section: `P4-16.3`
- Appears in: `P4-16.3`
