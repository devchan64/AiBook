<a id="bias-term"></a>

## bias term

- Meaning: A bias term is a model parameter that adjusts the default position of an output even when input signals are weak or zero. Like the intercept in a line, it moves the starting level of the output separately from the input weights.
- Why it matters: Weights explain how inputs affect the output, but they do not by themselves set the output's default starting point. The bias term helps readers see that training adjusts both input effects and baseline output position, which matters in linear models and neural-network layers.
- Related concepts: `weight`, `parameter`, `training`
- Core Section: `P1-5.1`
