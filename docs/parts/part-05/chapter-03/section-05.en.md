# P5-3.5 Formula Comparison Of Representative Activation Functions

> Section ID: `P5-3.5`
> Version: `v2026.07.19`

From P5-3.2 through P5-3.4, we looked separately at the sigmoid, tanh, and ReLU. Now the three functions are compared in one place. The purpose here is not to memorize names, but to check how the same score \(z\) changes according to different formulas and output ranges.

If the comparison among representative activation functions becomes blurry again, return to the [activation function](/AiBook/reference/concept-glossary/#activation-function) entry in the concept glossary as the baseline.

## Scope Of This Section

- Compare the formulas of the sigmoid, tanh, and ReLU in one table.
- Compare their output ranges and whether they saturate.
- Check how the same input value changes across the functions.
- Connect the comparison result to the next section on the output layer.

This section does not repeat at length the history and detailed usage context of each function. The individual intuition has already been handled in P5-3.2, P5-3.3, and P5-3.4, and the question of what should be used in the output layer continues in P5-3.6.

## Goals Of This Section

- You can compare the formulas of the three representative activation functions side by side.
- You can explain the differences among them through output range and saturation.
- You can confirm numerically that even for the same \(z\), the value passed to the next layer changes.
- You can connect the function comparison to output-layer interpretation and loss functions.

## Formula Comparison

| Function | Formula | Output range | Core response |
| --- | --- | --- | --- |
| sigmoid | \(\sigma(z)=\frac{1}{1+e^{-z}}\) | \(0 < \sigma(z) < 1\) | Compressed between 0 and 1 |
| tanh | \(\tanh(z)=\frac{e^z-e^{-z}}{e^z+e^{-z}}\) | \(-1 < \tanh(z) < 1\) | Negative and positive values compressed around 0 |
| ReLU | \(f(z)=\max(0,z)\) | \(0 \le f(z)\) | Negative values cut, positive values passed through |

The first axes to read in this table are the following three.

1. Into what range is the output confined?
2. Does a negative input remain for the next layer?
3. Can a large positive input keep growing?

## Comparing Them Through Graphs

If you look at the curve shapes before the names, the difference becomes clear more quickly.

![Sigmoid function curve](/AiBook/assets/part-05/chapter-03/sigmoid-curve-en.svg)

![Tanh function curve](/AiBook/assets/part-05/chapter-03/tanh-curve-en.svg)

![ReLU function curve](/AiBook/assets/part-05/chapter-03/relu-curve-en.svg)

If these three graphs are placed side by side, the sigmoid and tanh saturate at both ends. Even if the input grows further, the output no longer changes much near 1 or -1. By contrast, ReLU cuts the negative range to 0, but keeps increasing linearly in the positive range.

## Comparing By Feeding In The Same Score

Suppose that a hidden node in an equipment-warning model created the following five scores.

| Scene | \(z\) | sigmoid | tanh | ReLU |
| --- | --- | --- | --- | --- |
| Quiet scene | \(-2\) | 0.119 | -0.964 | 0 |
| Stable recovery scene | \(-0.5\) | 0.378 | -0.462 | 0 |
| Borderline alarm scene | \(0.1\) | 0.525 | 0.100 | 0.1 |
| Confirmed warning scene | \(0.5\) | 0.622 | 0.462 | 0.5 |
| Review-immediate-shutdown scene | \(3\) | 0.953 | 0.995 | 3 |

There is no need to memorize the numbers. The results that should be read are the following.

- The sigmoid always compresses the value into the range between 0 and 1, creating something easy to read like a risk score.
- Tanh keeps both the negative and positive sign while compressing the value between -1 and 1.
- ReLU turns all negative values into 0 and keeps the positive differences as they are.

## How Is This Comparison Used

| Computation feel needed first | Function to think of first | Reason |
| --- | --- | --- |
| I want to read the value as something between 0 and 1 | sigmoid | The output range is 0 to 1, so it connects naturally to the feel of binary classification. |
| I want to keep both negative and positive direction | tanh | Both signs are preserved around 0. |
| I want to cut negatives and keep only positive signals alive | ReLU | The difference in the positive range stays alive. |

Once this comparison is finished, the next question becomes `what activation should be used in the final output layer?` Hidden-layer activation is a problem of creating internal representation, while output-layer activation is a problem of deciding how to read the final number. This distinction continues in P5-3.6.

## Practice And Exercise

The goal of this exercise is not to choose a function name, but to check directly how the same linear score \(z\) changes into different output ranges and signal forms after passing through the three activation functions.

Before looking at the code, first predict the following three values.

| Value to look at first | Why it should be looked at first |
| --- | --- |
| `z = -3.0` | Because it shows how a negative input remains or disappears differently across the three functions. |
| `z = 0.0` | Because it is the reference point where the sigmoid goes to 0.5 while tanh and ReLU go to 0. |
| `z = 2.5` | Because it shows the difference that the sigmoid and tanh are compressed near 1 while ReLU keeps 2.5 unchanged. |

Input:

- linear scores \(z\) that came from several scenes
- the sigmoid, tanh, and ReLU functions

Output:

- the outputs of all three functions for the same \(z\)
- the differences in negative-input handling, near-zero response, and large-positive handling

Problem situation:

- even if the same score \(z\) is created in the hidden layer, the meaning of the signal that goes to the next layer changes depending on which activation function it passes through

Concepts to confirm:

- the sigmoid compresses into the range between 0 and 1
- tanh keeps both negative and positive direction
- ReLU cuts negative signals to 0 and leaves positive differences unchanged

Input:

```python
import math

z_values = [-3.0, -1.0, 0.0, 0.5, 2.5]

def sigmoid(z):
    return 1 / (1 + math.exp(-z))

def relu(z):
    return max(0, z)

print("z | sigmoid | tanh | relu")
for z in z_values:
    print(
        f"{z:>4.1f} | "
        f"{sigmoid(z):>7.3f} | "
        f"{math.tanh(z):>5.3f} | "
        f"{relu(z):>4.1f}"
    )
```

In the output, each row has to be read horizontally. The row for `z=-3.0` shows how a negative signal is handled, while the row for `z=2.5` shows how a large positive signal remains.

```text
z | sigmoid | tanh | relu
-3.0 |   0.047 | -0.995 |  0.0
-1.0 |   0.269 | -0.762 |  0.0
 0.0 |   0.500 | 0.000 |  0.0
 0.5 |   0.622 | 0.462 |  0.5
 2.5 |   0.924 | 0.987 |  2.5
```

| Row to compare | Difference seen first | Meaning that should be read now |
| --- | --- | --- |
| `z=-3.0` | The sigmoid becomes close to 0, tanh becomes close to -1, and ReLU becomes 0. | It differs by function whether a negative signal is left weakly, left together with its sign, or cut off entirely. |
| `z=0.0` | Only the sigmoid is 0.5, while tanh and ReLU are 0. | Even the same reference point has a different meaning of neutrality depending on the function. |
| `z=2.5` | The sigmoid and tanh are compressed near 1, while ReLU keeps 2.5. | It differs whether a large positive difference continues to remain or is compressed into a limited range. |

The value to change directly in this example is `z_values`. If a larger positive value such as `5.0` is added, the sigmoid and tanh change more slowly near 1, while ReLU keeps enlarging the value difference as it is. If a smaller negative value such as `-5.0` is added, tanh goes near -1 while ReLU is still cut to 0.

| Change to try right now | Difference that becomes clearer | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| Add `5.0` to `z_values` | The difference between the saturation of sigmoid/tanh and the positive pass-through of ReLU | Do not conclude that ReLU is always better for large positive values. |
| Add `-5.0` to `z_values` | The difference between tanh preserving the negative sign and ReLU cutting negatives | Do not conclude that cutting negative signals is always safer. |
| Narrow `z_values` to something like `[-0.2, 0.0, 0.2]` | How differently the three functions move near the reference point | Do not judge the whole character of a function only from values near 0. |

When you summarize the answer, the three axes `output range`, `negative-input handling`, and `large-positive handling` must be explained before the function names. You need to be able to explain through those three axes before the next section can separate hidden-layer activation from output-layer activation.

## Checklist

- Can you compare the formulas of the sigmoid, tanh, and ReLU side by side?
- Can you distinguish the output ranges of the three functions?
- Can you explain that at large positive values, the sigmoid and tanh saturate while ReLU keeps increasing?
- Can you say that the sigmoid, tanh, and ReLU each react differently to negative input?
- Can you distinguish hidden-layer activation comparison from the question of output-layer choice?

## Sources And References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, date checked: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Yann LeCun, Yoshua Bengio, Geoffrey Hinton, `Deep learning`, Nature, 2015, date checked: 2026-06-29. [https://www.nature.com/articles/nature14539](https://www.nature.com/articles/nature14539){: target="_blank" rel="noopener noreferrer" }
- Xavier Glorot, Antoine Bordes, Yoshua Bengio, `Deep Sparse Rectifier Neural Networks`, AISTATS, 2011, date checked: 2026-07-19. [https://proceedings.mlr.press/v15/glorot11a.html](https://proceedings.mlr.press/v15/glorot11a.html){: target="_blank" rel="noopener noreferrer" }
