## pooling

- Meaning: Pooling is an operation that summarizes local responses in a feature map and passes them forward in a smaller, compressed form. It may keep the maximum value in a small region or average values to reduce detailed position information while preserving key responses.
- Why it matters: Pooling reduces spatial size while retaining important local signals, helping CNNs read larger visual cues step by step. It explains the tradeoff between reducing resolution and preserving useful patterns.
- Related concepts: `convolution`, `feature map`, `CNN, convolutional neural network`
- Core Section: `P5-11.2`
