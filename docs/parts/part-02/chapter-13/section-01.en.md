# P2-13.1 What Does a Plot Reveal?

> Section ID: `P2-13.1`
> Version: `v2026.09.15`

## Changes in Loss

These fictional records illustrate changes in loss over training iterations. The table gives the third value precisely as 1.12; a line plot reveals that the size of each decrease becomes smaller.

| epoch | loss |
| ---: | ---: |
| 1 | 2.40 |
| 2 | 1.65 |
| 3 | 1.12 |
| 4 | 0.86 |
| 5 | 0.79 |

The first decrease is `2.40 - 1.65 = 0.75`, while the last is `0.86 - 0.79 = 0.07`. This code plots the five ordered values as points and connects them.

```python
import matplotlib.pyplot as plt

epochs = [1, 2, 3, 4, 5]
loss = [2.40, 1.65, 1.12, 0.86, 0.79]

fig, ax = plt.subplots()
ax.plot(epochs, loss, marker="o")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Loss decreases over epochs")
plt.show()
```

The resulting line falls as epoch increases.

![Loss decreasing over epochs](/AiBook/assets/part-02/chapter-13/pyplot-loss-line-en.svg)

All three language versions are generated from the same data. This script recreates the SVG assets for this section. The manuscript code uses `plt.show()` for screen display; the script saves files and closes each figure.

[p2_13_1_plot_questions.py](/AiBook/assets/part-02/chapter-13/p2_13_1_plot_questions.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_1_plot_questions.py
```

## Same Mean, Different Changes

Action A has segment values `[1.0, 2.0, 2.0, 1.0]`, while action B has `[1.5, 1.5, 1.5, 1.5]`. Both means are 1.5, but A rises in the middle and B stays constant. Plotting only the mean hides this difference, so compare values by segment.

```python
import matplotlib.pyplot as plt

steps = [1, 2, 3, 4]
action_a = [1.0, 2.0, 2.0, 1.0]
action_b = [1.5, 1.5, 1.5, 1.5]

fig, ax = plt.subplots()
ax.plot(steps, action_a, marker="o", label="action A")
ax.plot(steps, action_b, marker="o", label="action B")
ax.set_xlabel("segment")
ax.set_ylabel("signal level")
ax.set_title("Same mean, different pattern")
ax.legend()
plt.show()
```

![Two signals with the same mean and different patterns](/AiBook/assets/part-02/chapter-13/same-mean-pattern-en.svg)

## Trends, Relationships, Distributions, and Outliers

Plots reveal changes in values, relationships between variables, intervals where values cluster, and observations far from the others.

| Question | What a plot helps reveal | Example |
| --- | --- | --- |
| Trend | Movement over time or sequence | Loss by training epoch |
| Relationship | Whether two values move together | Study hours and score |
| Distribution | Where values cluster | Scores or errors |
| Outlier | Unusually distant values | Sensor readings far from others |

## Study Hours and Scores

Consider these four student records.

| name | study_hours | score |
| --- | ---: | ---: |
| Kim | 2 | 62 |
| Park | 4 | 71 |
| Lee | 6 | 82 |
| Choi | 8 | 88 |

The table provides exact values. A scatter plot is more natural for asking whether students with more study hours also tend to have higher scores.

```python
import matplotlib.pyplot as plt

study_hours = [2, 4, 6, 8]
scores = [62, 71, 82, 88]

fig, ax = plt.subplots()
ax.scatter(study_hours, scores)
ax.set_xlabel("study hours")
ax.set_ylabel("score")
ax.set_title("Study hours and score")
plt.show()
```

Each point is one student: Kim is at `(2, 62)` and Choi at `(8, 88)`. Among these four records, students with longer study times have higher scores.

![Study hours and scores](/AiBook/assets/part-02/chapter-13/pyplot-study-scatter-en.svg)

The plot does not prove causation. It makes the pattern of joint variation easier to inspect.

## Figure and Axes

Matplotlib describes plotting data on a `Figure`. A Figure is the entire image and can contain one or more `Axes`. An Axes is the coordinate region where data is drawn.

| Term | Intuition |
| --- | --- |
| `Figure` | The entire sheet |
| `Axes` | A panel containing coordinates and data |
| `plot`, `scatter`, `hist` | Methods choosing how to draw data on an Axes |

Create a figure and coordinate region with `plt.subplots()`, then connect `(1, 2)`, `(2, 4)`, and `(3, 3)`.

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [2, 4, 3])
plt.show()
```

`plt.subplots()` returns a Figure and one Axes here. Draw on that Axes using methods such as `ax.plot(...)`.

`ax.set_xlabel(...)` names the x-axis and `ax.set_title(...)` sets the panel title. Multiple Axes in one Figure let you compare plots on the same screen.

## Choosing a Plot for the Question

Matplotlib offers plot types including line plots (`plot`), scatter plots (`scatter`), bar charts (`bar`), and histograms (`hist`).

Choose according to whether you need change over a sequence or comparisons between categories.

| Question | Often suitable |
| --- | --- |
| Change over a sequence? | Line plot |
| Relationship between two values? | Scatter plot |
| Magnitudes by category? | Bar chart |
| Where values cluster? | Histogram |

This table is a starting point rather than a fixed rule. The actual choice depends on data shape, the reader's question, and the intended message.

## Axis Ranges and Interpretation

A plot compresses many numbers into one view. Axis ranges and presentation can change the impression of the same data.

For example:

- Changing axis ranges can make changes look larger or smaller.
- Connecting a few points may suggest more continuity than was observed.
- Excessive color or area can exaggerate unimportant differences.
- Plotting means alone can hide distributions or outliers.

When reading a plot, ask:

1. What do the x- and y-axes represent?
2. What does one point or line mean?
3. Are values missing or ranges hidden?
4. Does the plot show an observation or an interpretation?

## Same Values, Different Axis Ranges

The scores `[80, 82, 81, 83]` span three points from minimum to maximum. With a y-axis of 0–100, the change looks small; narrowing it to 79–84 makes the same change look large.

```python
attempts = [1, 2, 3, 4]
scores = [80, 82, 81, 83]
fig, axes = plt.subplots(1, 2, figsize=(8, 3.6), sharex=True)
for ax in axes:
    ax.plot(attempts, scores, marker="o")
    ax.set_xlabel("attempt")
    ax.set_ylabel("score")
axes[0].set_ylim(0, 100)
axes[0].set_title("Full range: 0 to 100")
axes[1].set_ylim(79, 84)
axes[1].set_title("Zoomed range: 79 to 84")
fig.tight_layout()
plt.show()
```

![The same scores on full and zoomed axes](/AiBook/assets/part-02/chapter-13/axis-range-comparison-en.svg)

The right panel is useful for inspecting small changes, but reading its steep line as a large score difference would be wrong. The actual span remains three points. To compare changes between experiments, use the same axis ranges or clearly mark their differences.

## Score Distribution

Divide `[45, 62, 71, 73, 82, 88, 90]` into five bins and count the values. A histogram reveals concentration and spread that a mean alone cannot show.

```python
import matplotlib.pyplot as plt

scores = [45, 62, 71, 73, 82, 88, 90]

fig, ax = plt.subplots()
ax.hist(scores, bins=5)
ax.set_xlabel("score")
ax.set_ylabel("count")
ax.set_title("Score distribution")
plt.show()
```

The result shows which score intervals contain more values.

![Score distribution](/AiBook/assets/part-02/chapter-13/pyplot-score-hist-en.svg)

This code does not calculate the mean; it shows where the scores cluster.

## Case: Finding a Spike in Loss

In the first loss list `[2.40, 1.65, 1.12, 0.86, 0.79]`, change only the third value to `2.10` and plot again. The endpoints stay the same, but loss rises by 0.45 from the second to third point and then drops by 1.24. The third point becomes a peak.

Recording only the overall decrease `2.40 - 0.79 = 1.61` misses that rise. The plot identifies a segment worth investigating, but cannot determine whether the cause was a data batch, training setting, or logging error. Check the inputs and settings for that iteration.

If this is training loss, its downward trend alone cannot establish performance on new data. Inspect validation loss or evaluation metrics separately.

## Checklist

- Can you explain how plots reveal shapes, trends, relationships, and distributions?
- Can you distinguish exact-value reading in tables from pattern reading in plots?
- Can you distinguish a Figure from an Axes?
- Can you choose a question before choosing a chart type?
- Can you explain typical uses of lines, scatter plots, bars, and histograms?
- Can you inspect axes, point meanings, hidden ranges, and excessive interpretation?
- Can you explain why a plot does not automatically prove causes or conclusions?

## Sources and References

- Matplotlib Developers, [Quick start guide](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. Figure/Axes structure and subplots.
- Matplotlib Developers, [Plot types](https://matplotlib.org/stable/plot_types/index.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. Choosing basic plots for different questions.
- Matplotlib Developers, [matplotlib.pyplot](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.html){: target="_blank" rel="noopener noreferrer" }, Matplotlib documentation, accessed: 2026-07-20. The pyplot interface used by the examples.
