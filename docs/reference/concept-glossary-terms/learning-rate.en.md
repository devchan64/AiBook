<a id="learning-rate"></a>

## learning rate

- Meaning: Learning rate controls how large each update step is when optimization moves in a direction that should reduce loss. In sequential correction models, it controls how strongly each correction stage is reflected.
- Why it matters: Learning rate controls the balance between stable progress and speed. In sequential correction models, a larger learning rate gives each correction stage more influence, while a smaller learning rate may require more stages. It is therefore a core hyperparameter for reading both training stability and correction strength.
- Related concepts: `gradient descent`, `gradient`, `optimization`, `training`
- Core Section: `P2-6.3`
- Appears in: `P4-16.1`, `P5-7.1`, `P5-7.2`, `P5-7.3`
