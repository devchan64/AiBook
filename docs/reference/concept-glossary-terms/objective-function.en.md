<a id="objective-function"></a>

## objective function

- Meaning: An objective function is the overall criterion that a learning or optimization process tries to decrease or increase. It can combine sample-level loss, average loss over many samples, regularization penalties, and constraints into one rule for deciding what counts as better. A loss function can be a central component inside an objective function, but the objective function is the broader scoring rule.
- Why it matters: A model does not move toward being vaguely `better`; it is adjusted in the direction defined by the objective function. This concept connects loss functions, regularization, and constraints into the actual learning target. It also separates evaluation statements such as `the accuracy is high` from the quantity that training directly optimized.
- Related concepts: `loss function`, `optimization`, `metric`
- Core Section: `P2-6.2`
- Appears in: `P2-6.3`, `P2-15.2`
