<a id="gradient"></a>

## gradient

- Meaning: A gradient is a vector of partial derivatives that shows how a value, usually loss, changes with respect to multiple parameters. It acts like a direction signal for how parameter changes would affect the loss.
- Why it matters: Gradients are the link between loss and learning. They explain why parameters are not changed randomly, but updated in directions that are expected to reduce loss. Without gradients, gradient descent and backpropagation cannot be read as concrete computation.
- Related concepts: `partial derivative`, `vector`, `training`
- Core Section: `P2-4.3`
- Appears in: `P2-4.4`, `P2-6.3`, `P5-5.1`, `P5-5.2`, `P5-6.1`, `P5-7.1`
