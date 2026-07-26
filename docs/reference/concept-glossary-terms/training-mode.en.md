## training mode

- Meaning: Training mode is the execution state in which a model uses calculation rules prepared for learning and parameter updates. In this state, regularization such as dropout is active, batch normalization uses current-batch statistics, and intermediate information needed for backpropagation is kept.
- Why it matters: Some layers behave differently during training and evaluation even when the model structure is the same. Understanding training mode helps distinguish output fluctuation that belongs to the learning procedure from errors that should be read as deployment behavior.
- Related concepts: `evaluation`, `dropout`, `validation`
- Core Section: `P5-6.4`
- Appears in: `P5-6.1`, `P5-7.1`, `P5-8.2`, `P5-8.3`
