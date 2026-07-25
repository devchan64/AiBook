<a id="backpropagation"></a>

## backpropagation

- Meaning: Backpropagation is the procedure that computes how much the loss at the output depends on each parameter by working backward through the network. More precisely, it applies the chain rule along the computation graph to distribute the final error signal across intermediate activations and weights.
- Why it matters: A neural network cannot reduce loss unless it knows which direction each weight should move. Backpropagation provides that gradient signal efficiently, so learning becomes a concrete calculation rather than a vague idea that the network adjusts itself. It also explains why deep layers can be trained by tracing each connection's contribution to the final error.
- Related concepts: `gradient`, `loss function`, `chain rule`
- Core Section: `P5-5.1`
- Appears in: `P5-5.2`, `P5-6.1`, `P5-7.1`
