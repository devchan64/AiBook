# P2-15.1 A Small Procedure for Translating Formulas into Code

> Section ID: `P2-15.1`
> Version: `v2026.09.15`

## Symbols and Computation Order

Distinguish symbols representing one input value from those representing collections. Separate calculations applied to each value from operations that combine the whole collection.

To summarize errors for three predictions, first pair each prediction with the actual value for the same sample. Compute the difference and square for each pair, then sum and average across samples. Making this compressed procedure explicit in code helps reveal mismatched values or missing operations.

```mermaid
--8<-- "assets/part-02/chapter-15/formula-to-code-flow-en.mmd"
```

## Mean Squared Error

Mean squared error (MSE) averages the squared differences between predicted and actual values.

\[
\mathrm{MSE} = \frac{1}{n}\sum_{i=1}^{n}(y_i - \hat{y}_i)^2
\]

The symbols refer to the following quantities.

| Symbol | Meaning |
| --- | --- |
| \(n\) | Number of data points |
| \(y_i\) | Actual value for sample i |
| \(\hat{y}_i\) | Predicted value for sample i |
| \(y_i - \hat{y}_i\) | Error for sample i |
| \((y_i - \hat{y}_i)^2\) | Squared error |
| \(\sum\) | Sum across all samples |
| \(\frac{1}{n}\) | Divide the sum by the sample count |

Read the formula as “calculate each sample’s error, square it, add the squares, and divide by the count.”

Here each sample has one actual and one predicted value, and every sample has equal weight. \(n\) counts sample pairs, not features, and must be positive. The formula’s first sample, \(i=1\), corresponds to Python index 0. The name `y_hat` spells out the hat over the predicted value \(\hat y\).

## Computing with a Loop

Pair actual values `[3.0, 5.0, 7.0]` with predictions `[2.5, 5.5, 8.0]` at matching positions. Errors are `[0.5, -0.5, -1.0]`, and squared errors are `[0.25, 0.25, 1.0]`. Their sum, 1.5, divided by 3 gives MSE 0.5.

```python
actual = [3.0, 5.0, 7.0]
predicted = [2.5, 5.5, 8.0]

if len(actual) != len(predicted) or not actual:
    raise ValueError("Use equally sized, non-empty lists.")

squared_errors = []

for y, y_hat in zip(actual, predicted):
    error = y - y_hat
    squared_errors.append(error ** 2)

mse = sum(squared_errors) / len(squared_errors)
print(mse)
```

The code follows the parts of the formula directly.

| Part of the Formula | Part of the Code |
| --- | --- |
| \(y_i\), \(\hat{y}_i\) | `y`, `y_hat` |
| \(y_i - \hat{y}_i\) | `error = y - y_hat` |
| \((y_i - \hat{y}_i)^2\) | `error ** 2` |
| \(\sum\) | `sum(squared_errors)` |
| \(\frac{1}{n}\) | `/ len(squared_errors)` |

Both lists must be nonempty and have the same length and sample order. By default, `zip` stops at the shorter list, so a length mismatch can silently omit values.

The `if` check stops computation for unequal lengths or empty lists. Remove 8.0 from the prediction list to trigger `ValueError`. Without the check, only the first two pairs produce MSE 0.25, making missing data look like an improvement. This exercise assumes lists of finite real values.

## Computing with NumPy Arrays

Subtracting, squaring, and averaging the same inputs with NumPy also gives 0.5.

```python
import numpy as np

actual = np.array([3.0, 5.0, 7.0])
predicted = np.array([2.5, 5.5, 8.0])

if actual.ndim != 1 or actual.shape != predicted.shape or actual.size == 0:
    raise ValueError("Use equally shaped, non-empty 1-D arrays.")
if not (np.isfinite(actual).all() and np.isfinite(predicted).all()):
    raise ValueError("Use finite values.")

errors = actual - predicted
squared_errors = errors ** 2
mse = np.mean(squared_errors)

print(mse)
```

Both arrays have shape `(3,)`, so subtraction pairs values at matching positions. Vectorization expresses the same operation across an array.

`ndim` counts axes, `shape` gives each axis length, and `size` counts all elements. `np.isfinite` checks that each value is neither NaN nor infinity; `.all()` checks that every element passes. Whoever constructs the inputs must still verify sample correspondence, which these checks cannot determine.

## Errors and Squared Errors

MSE becomes one number. Print the intermediate values in the same session after executing the NumPy block above.

```python
print(errors)
print(squared_errors)
print(mse)
```

The output is as follows.

```text
[ 0.5 -0.5 -1. ]
[0.25 0.25 1.  ]
0.5
```

Errors have direction: their sign changes with underprediction or overprediction. Squared errors are never negative, allowing MSE to summarize error size without sign cancellation.

MSE is specifically the **mean of squared errors**. If actual values are measured in score points, its unit is points². Taking the square root gives RMSE in the original unit: here, \(\sqrt{0.5}\approx0.707\). Doubling an error multiplies its square by four, increasing the influence of large errors.

`np.mean(errors ** 2)` also differs from `np.mean(errors) ** 2`. The first is 0.5; the second is approximately 0.111. The latter allows opposite signs to cancel before squaring, so it is not MSE.

## Differences by Sample

Compare the vertical distance between actual and predicted values at each sample position. The first two gaps are 0.5; the last is 1.0. Use points and vertical segments without connecting samples to avoid suggesting continuous change between them. This code uses `actual`, `predicted`, and `np` from the NumPy block above.

```python
import matplotlib.pyplot as plt

index = np.arange(len(actual))

fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.scatter(index, actual, marker="o", color="#2563eb", label="actual")
ax.scatter(index, predicted, marker="x", color="#dc2626", label="predicted")
ax.vlines(index, predicted, actual, color="#64748b", linewidth=1.4)
ax.set_xticks(index)
ax.set_xlabel("sample index")
ax.set_ylabel("value")
ax.set_title("Actual and predicted values")
ax.legend()
fig.tight_layout()
plt.show()
```

The image shows the actual–predicted gaps for each sample.

![Actual and predicted values with vertical error gaps for three samples](/AiBook/assets/part-02/chapter-15/actual-predicted-mse-en.svg)

The reference source runs the loop calculation, NumPy calculation, and plot saving together. It localizes the code’s English labels for the published figures while preserving point positions and calculated values.

[MSE calculation and chart-generation code](/AiBook/assets/part-02/chapter-15/p2_15_1_formula_to_code_mse.py)

Run from the repository root in a Python environment with NumPy and Matplotlib installed. Matching the published font requires `Noto Sans CJK JP`; select another font with `--font-family` if needed.

```bash
python docs/assets/part-02/chapter-15/p2_15_1_formula_to_code_mse.py --output-dir .tmp/p2-15-mse
```

The script prints `loop mse`, `errors`, `squared errors`, and `numpy mse`, then saves three language-specific SVGs in the chosen folder. The default final prediction is 8.0. Add `--last-prediction 7` or `--last-prediction 9` to reproduce the numerical and visual changes below.

The graph does not calculate MSE for you. It reveals the differences before they are compressed into a single number.

## Case 1. Changing Only the Final Prediction

Changing the final prediction from 8.0 to the actual value, 7.0, produces squared errors `[0.25, 0.25, 0.0]`. MSE falls to `0.5 / 3`, approximately 0.167, and the final two points overlap.

Changing that prediction to 9.0 instead makes its error −2 and its squared error 4. MSE becomes `(0.25 + 0.25 + 4) / 3 = 1.5`. Doubling this sample’s error magnitude from 1 to 2 quadruples its squared error from 1 to 4.

Changing the inputs in both the loop and NumPy versions should yield the same result. If not, check order, length, shape, and the averaging axis. In particular, changing a `(3,)` array to `(3, 1)` can broadcast subtraction across all combinations instead of computing the original paired-sample MSE.

## Code That Runs but Calculates Something Else

Without the input checks, `actual.reshape(3, 1) - predicted` produces shape `(3, 3)`. Each actual value is compared with all three predictions, creating nine differences. Its first row is `[0.5, -2.5, -5.0]`, mixing in predictions for other samples.

| Calculation | Values Being Averaged | Result |
| --- | --- | ---: |
| Three matching pairs | 3 squared errors | 0.5 |
| Subtracting `(3,)` from `(3, 1)` | 9 squared errors from all combinations | About 7.833 |
| Reversing only prediction order | 3 incorrectly paired squared errors | About 15.167 |

Shape checks prevent the second error but not the third, whose shapes still match. Check sample identifiers such as student IDs as well. Without an axis argument, `np.mean` averages every element, compressing even an incorrectly expanded array into one number.

Predict whether adding 10 to both actual and predicted values changes MSE, then run it. Differences remain unchanged, so MSE stays at 0.5. Multiplying both arrays by 10 multiplies differences by 10 and squared errors by 100, producing MSE 50. Interpreting magnitudes requires matching units, samples, and calculation rules.

## Checklist

- Can you separate symbols, data shape, and calculation steps before writing code?
- Can you explain \(y_i\), \(\hat{y}_i\), \(n\), and \(\sum\) in the MSE formula?
- Can you translate summation into a loop or array calculation?
- Can you write the same calculation with a Python loop and NumPy arrays?
- Can you explain why actual and predicted values need matching order, length, and shape?
- Can you distinguish `errors`, `squared_errors`, and `mse`?
- Can you explain why intermediate values help verify a calculation?
- Can you explain how a plot supports interpretation without replacing calculation?
- Can you distinguish the mean of squares from the square of the mean, and the units of MSE from RMSE?
- Can you explain why incorrect sample order changes results even when shapes match?

## Sources and References

- [Python Software Foundation, Built-in Functions: zip](https://docs.python.org/3/library/functions.html#zip){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Pairing and the default stop at the shorter input.
- [NumPy Developers, numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Averaging all elements when no axis is specified.
- [NumPy Developers, Broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Operations between arrays with different shapes.
- [scikit-learn developers, Regression metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Definitions and interpretation of MSE, RMSE, and MAE.
- [Matplotlib Developers, Axes.scatter](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.scatter.html){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Displaying actual and predicted values by sample.
