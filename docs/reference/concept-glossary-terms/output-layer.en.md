## output layer

- Meaning: The output layer is the final layer of a neural network, where the model produces its prediction. Depending on the task, it may emit a continuous value, a class score, or a probability-like value.
- Why it matters: Hidden layers mainly create internal representations, but the output layer determines how the final number should be interpreted. Its activation therefore needs to be read together with the task type, target format, and loss function.
- Related concepts: `output`, `activation function`, `loss function`, `softmax`
- Core Section: `P5-3.6`
