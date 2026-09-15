# P2-13.2 Basic Charts and Function Shapes

> Section ID: `P2-13.2`
> Version: `v2026.09.15`

## Line Plots: Function Shapes

Line plots are useful when x-axis order matters, such as time, iterations, training epochs, or continuous changes in an input value.

For \(y=x^2\), inputs −3, 0, and 3 give 9, 0, and 9. This code evaluates 121 points from −3 to 3 and connects them into a U-shaped curve.

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3, 3, 121)
y = x**2

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Function shape: y = x^2")
plt.show()
```

The output is:

![Function y = x squared](/AiBook/assets/part-02/chapter-13/basic-line-function-shape-en.svg)

This script saves SVG plots in all three languages using the same input conditions as the manuscript.

[p2_13_2_basic_chart_shapes.py](/AiBook/assets/part-02/chapter-13/p2_13_2_basic_chart_shapes.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_2_basic_chart_shapes.py
```

The curve shows these features:

- The minimum is 0 at \(x=0\).
- As \(x\) moves away from zero on either side, \(y\) grows.
- The slope varies with position.

Changing `y = x**2` to `y = (x - 1)**2` moves the lowest point from `(0, 0)` to `(1, 0)`. The equation change shifts the curve.

`np.linspace(-3, 3, 121)` includes both endpoints and produces 121 inputs spaced by 0.05. The plot joins computed points with line segments; it does not evaluate every real input. Reducing the count to three connects only `(-3, 9)`, `(0, 0)`, and `(3, 9)`, producing a V-like shape. Even with the same equation, too few sample points may fail to represent its curvature.

## Scatter Plots: Relationships and Spread

A scatter plot draws each sample as a point, putting different variables on the x- and y-axes to inspect how they vary together.

This artificial dataset evaluates `2.5 * x` for 24 inputs and adds normal random noise with mean 0 and standard deviation 2.2. The points scatter around a straight line.

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(42)
x = np.linspace(1, 10, 24)
y = 2.5 * x + rng.normal(0, 2.2, size=x.shape)

fig, ax = plt.subplots()
ax.scatter(x, y)
ax.set_xlabel("input value")
ax.set_ylabel("observed value")
ax.set_title("Scatter plot: relationship with variation")
plt.show()
```

The output is:

![A relationship with variation](/AiBook/assets/part-02/chapter-13/basic-scatter-relationship-en.svg)

The points do not lie exactly on one line, but they generally rise toward the right.

In this artificial dataset:

- Each point is one sample.
- Points generally follow an increasing trend.
- Departures from the line reflect added noise.
- A scatter plot alone does not establish causation.

## Histograms: Counts by Interval

A histogram divides values into bins and shows how many fall into each. This example draws 240 values from a normal distribution with mean 0 and standard deviation 1, then uses 18 bins. Bar height is the count in each bin.

```python
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(7)
values = rng.normal(loc=0, scale=1, size=240)

fig, ax = plt.subplots()
ax.hist(values, bins=18)
ax.set_xlabel("value")
ax.set_ylabel("count")
ax.set_title("Histogram: where values gather")
plt.show()
```

The output is:

![Values grouped into intervals](/AiBook/assets/part-02/chapter-13/basic-hist-distribution-en.svg)

When inspecting a histogram, ask:

- Where do most values cluster?
- Is the distribution skewed to one side?
- Are rare values present at the ends?
- What shape would a mean alone hide?

Changing `bins=18` to `bins=6` groups the same 240 values into wider intervals. The number and height of bars change, but their counts still sum to 240.

## Bin Edges and Excluded Values

For scores `[45, 62, 71, 73, 82, 88, 90]` and edges `[40, 60, 80, 100]`, the three bar heights are shown below. An edge list contains one more element than the number of bins.

| Interval | Scores | Count |
| --- | --- | ---: |
| 40 ≤ score < 60 | 45 | 1 |
| 60 ≤ score < 80 | 62, 71, 73 | 3 |
| 80 ≤ score ≤ 100 | 82, 88, 90 | 3 |

Matplotlib histogram bins include the left edge and exclude the right edge, except that the final bin includes both. Thus 80 belongs in the final bin and 100 is included too. Setting `bins=3, range=(60, 100)` excludes 45, reducing the total count to six. Changing the visible axis range differs from changing which values participate in binning.

Use the same bin edges when comparing two groups. Calling `bins=5` separately can produce different edges if their minima and maxima differ. The y-axis here is count. With `density=True`, heights become probability densities: the sum of bar areas, rather than heights, is one.

## Bar Charts: Comparing Categories

Suppose fictional models A, B, and C have losses `[0.42, 0.39, 0.47]` on the same validation data with the same loss function. Model names are categories, not numeric intervals, so compare them with `bar`.

```python
models = ["A", "B", "C"]
validation_loss = [0.42, 0.39, 0.47]
fig, ax = plt.subplots()
ax.bar(models, validation_loss)
ax.set_ylim(0, 0.55)
ax.set_xlabel("model")
ax.set_ylabel("validation loss")
ax.set_title("Model comparison on the same validation set")
plt.show()
```

![Model losses on the same validation set](/AiBook/assets/part-02/chapter-13/basic-bar-model-comparison-en.svg)

B has the lowest loss here, 0.03 below A. Since bar length encodes magnitude, the y-axis begins at zero. Changing B to 0.49 makes A the lowest. A bar chart displays values already assigned to categories; a histogram computes counts by placing raw observations into numeric intervals.

## Loss Curves: Decrease and Oscillation

Compare two fictional training records. The first decreases at every step from 2.4 to 0.57. The second ends at 1.46 after starting at 2.4, but rises relative to the preceding value at iterations 4, 6, 8, and 10.

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 11)
decreasing_loss = [2.4, 1.8, 1.35, 1.08, 0.91, 0.79, 0.70, 0.64, 0.60, 0.57]
unstable_loss = [2.4, 1.9, 1.75, 1.82, 1.55, 1.62, 1.45, 1.52, 1.40, 1.46]

fig, ax = plt.subplots()
ax.plot(epochs, decreasing_loss, marker="o", label="steady decrease")
ax.plot(epochs, unstable_loss, marker="o", label="unstable")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Loss curves can reveal training behavior")
ax.legend()
plt.show()
```

The resulting plot compares the two patterns.

![Decreasing and oscillating loss](/AiBook/assets/part-02/chapter-13/basic-loss-curve-comparison-en.svg)

This plot does not immediately establish that a model is good. It supports questions such as:

- Does loss generally decrease?
- Does it fluctuate strongly?
- When does the decline slow down?
- Should training and validation loss be inspected separately?

These are separate fictional records, not a training/validation pair. Even when training loss is lower, performance on new data must be checked separately using validation data.

## Axes and Titles

The function plot uses equation inputs on x and computed values on y; the loss plot uses iterations on x and loss on y. Similar shapes can mean different things when axes differ. Use `set_xlabel`, `set_ylabel`, and `set_title` to identify variables and subject, and `label` with `legend()` to distinguish multiple lines.

## Case: Reversing a Loss Record

Compare `[2.4, 1.8, 1.2, 0.6]` with its reverse `[0.6, 1.2, 1.8, 2.4]`. Both contain the same values with mean 1.5, but one decreases and the other increases.

Histograms using the same bin edges are identical because they count occurrences without retaining order. Line plots against iteration number move in opposite directions.

A histogram can answer a question about the distribution of loss values. To ask whether loss fell during training, use an ordered line plot. Choose a chart that retains the information your question needs.

## Checklist

- Can you choose a chart according to change, relationship, or distribution?
- Can you explain when a line plot is appropriate?
- Can you interpret one scatter point and the pattern of spread?
- Can you explain what distribution information a histogram adds beyond the mean?
- Can you formulate questions about training from loss curves?
- Can you choose a chart for checking a function or distribution shape?
- Can you explain why axes, titles, and labels are part of interpretation?

## Sources and References

- Matplotlib Developers, [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. Axes methods, labels, and titles.
- Matplotlib Developers, [Plot types](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. Lines, scatter plots, bars, and histograms.
- Matplotlib Developers, [matplotlib.pyplot](https://matplotlib.org/stable/api/pyplot_summary.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. The pyplot interface for basic plotting.
- Matplotlib Developers, [Axes.hist](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html){: target="_blank" rel="noopener noreferrer" }, accessed: 2026-09-15. bin edges, range, and density behavior.
- NumPy Developers, [numpy.linspace](https://numpy.org/doc/stable/reference/generated/numpy.linspace.html){: target="_blank" rel="noopener noreferrer" }, accessed: 2026-09-15. endpoint inclusion and sampling point count.
