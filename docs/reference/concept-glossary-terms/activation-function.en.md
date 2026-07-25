<a id="activation-function"></a>

## activation function

- Meaning: An activation function transforms a weighted sum or intermediate score before it is passed to the next layer or output. It introduces a non-linear response instead of passing a simple linear combination forward unchanged.
- Why it matters: Repeating only linear combinations would not give a deep network much more expressive power. Activation functions let layers form more complex decision boundaries and representations, while also affecting gradient flow and training stability. They explain why deep networks need both stacked layers and non-linear response curves.
- Related concepts: `linear combination`, `activation`, `hidden layer`
- Core Section: `P5-1.2`
- Appears in: `P5-3.1`, `P5-3.2`
