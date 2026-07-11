# P2-13.3 Comparing and Saving Multiple Plots

> Section ID: `P2-13.3`
> Version: `v2026.07.09`

In P2-13.2, we looked at what questions basic charts such as line plots, scatter plots, and histograms are used for. Now we go one step further and organize the flow of looking at several plots together and leaving the result as a file.

In AI learning, you often do not stop after looking at one plot. You may need to look at loss and accuracy together, or compare the flow of train data and validation data side by side. At that point, it helps to be a little more conscious of Matplotlib's `Figure` and `Axes` structure.

This section explains the basic distinctions in the compare-and-save flow, including `savefig`, `legend`, and `accuracy`. The representative explanation of `plot`, `Figure`, and `Axes` stays in P2-13.1, and the standards for choosing basic chart types stay in P2-13.2 and the [Concept Glossary](../../../reference/concept-glossary.md). Here, we focus on how to compare several plots together and leave the results as files.

## Scope of This Section

This section covers only the introductory flow of arranging and saving multiple plots with Matplotlib. It does not cover complex dashboards, interactive visualization, paper-style polishing, or color-palette design.

This section answers the following questions.

- Why place several plots on one screen?
- How does `plt.subplots()` create multiple `Axes`?
- What should you watch out for when comparing learning curves?
- What does it mean to save a plot with `savefig()`?
- When you keep a plot file as a learning record, what information should be left with it?

## Goals of This Section

- You can explain that one `Figure` can contain multiple `Axes`.
- You can make a plot that compares loss and accuracy side by side.
- You can compare train loss and validation loss on one axis.
- You can save a plot with `savefig()` and reuse it in a document or learning record.
- You can explain that a saved plot becomes a reproducible record only when the code and data conditions are kept together with it.

## Three Criteria

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| Why draw several plots together? | It clarifies that the number of plots is not the point; the comparison question is. | Understand that the purpose is to make the comparison question clearer. |
| When do you separate axes and when do you not? | It helps you distinguish values that can be compared directly from values that should be separated. | Understand that you keep them together when direct comparison matters, and separate them when interpretation would get mixed. |
| Why is saving important? | It helps you distinguish between screen output and a reusable record. | Understand that the purpose is to leave a record that can be explained again later, not only a result on screen. |

| Term | Meaning to Hold First in This Section |
| --- | --- |
| `savefig` | A function call that saves the current plot as an image file. |
| legend | A marker that distinguishes what each line or point means. |
| accuracy | A basic performance metric that shows the ratio of correct predictions among all predictions. |
| comparison plot | A plot made to compare two or more flows or values side by side. |
| reproducible record | A plot result left in a way that can be recreated with the same code and conditions. |

## Multiple Plots Create Comparison Questions

The reason to arrange several plots is not to fill the screen. It is to place related questions side by side.

For example, during learning, you may want to see whether loss decreases and accuracy rises. Because the two values use different units, it is often easier to read them if you split them into two small plots instead of forcing them onto one y-axis.

Problem situation: you want to compare on one screen how loss and accuracy each change as learning proceeds.
Input: epoch numbers, a list of loss values, and a list of accuracy values.
Expected output: a 1-by-2 plot layout with the loss curve on the left and the accuracy curve on the right.
Concept to check: if one `Figure` contains multiple `Axes`, you can compare related questions side by side.

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 13)
loss = [2.02, 1.68, 1.42, 1.18, 1.03, 0.91, 0.82, 0.75, 0.70, 0.66, 0.63, 0.60]
accuracy = [0.55, 0.61, 0.66, 0.70, 0.74, 0.78, 0.81, 0.83, 0.85, 0.86, 0.87, 0.88]

fig, axes = plt.subplots(1, 2)

axes[0].plot(epochs, loss, marker="o")
axes[0].set_title("Loss over epochs")
axes[0].set_xlabel("epoch")
axes[0].set_ylabel("loss")

axes[1].plot(epochs, accuracy, marker="o")
axes[1].set_title("Accuracy over epochs")
axes[1].set_xlabel("epoch")
axes[1].set_ylabel("accuracy")

fig.tight_layout()
plt.show()
```

The output separates two related questions inside one `Figure` as follows.

![Two subplots comparing loss and accuracy](/AiBook/assets/part-02/chapter-13/subplot-loss-accuracy.png)

This picture asks two things at once.

- Does loss generally decrease as repeated learning proceeds?
- Does accuracy generally rise over the same period?

If you place the two plots side by side, you can also create questions such as, "Does one improve while the other becomes stagnant?"

This comparison method is not used only for learning curves. For example, one `Axes` can show the raw curve of two action records, while another `Axes` can show a small comparison chart that summarizes those actions by segment mean or final value. Then the left side shows the `difference in shape itself`, and the right side shows the `difference that remains in a summary value`.

In other words, placing several plots together does not mean increasing the number of pictures. It means clarifying `what question lets us read the original shape and the summarized result together`.

## Reading Figure and Axes Again

In P2-13.1, we treated `Figure` as the whole picture and `Axes` as the coordinate area where data are drawn. When you draw several plots, this distinction becomes more important.

Problem situation: when you make a multi-panel plot, you need to grasp first what `fig` and `axes` each point to.
Input: one call line, `plt.subplots(1, 2)`.
Expected output: a variable structure that points to one whole picture and two plot panels inside it.
Concept to check: `Figure` is the whole picture, and `Axes` are the individual coordinate areas where actual data are drawn.

```python
fig, axes = plt.subplots(1, 2)
```

This code creates two `Axes` side by side inside one `Figure`.

Read it as follows.

| Code | Intuition |
| --- | --- |
| `fig` | the whole picture |
| `axes[0]` | the left plot panel |
| `axes[1]` | the right plot panel |
| `plt.subplots(1, 2)` | make plot panels in one row and two columns |

Once there are multiple `Axes`, the style changes from using one `ax.plot(...)` to specifying "which panel to draw on," such as `axes[0].plot(...)` and `axes[1].plot(...)`.

## Sometimes You Should Compare on the Same Axis

It is not always better to split plots apart. When you compare values with the same unit, it is more direct to put two lines on the same `Axes`.

A representative example is comparing train loss and validation loss. Both values are losses, so you can compare them on the same y-axis.

Problem situation: train loss and validation loss use the same unit, so you want to compare them directly on one axis.
Input: epoch numbers, plus the lists `train_loss` and `validation_loss`.
Expected output: one line plot where the two loss curves are drawn together on the same coordinate axes.
Concept to check: values with the same unit should go on the same `Axes`, so that the gap and crossing between the two flows are easy to read directly.

```python
import matplotlib.pyplot as plt
import numpy as np

epochs = np.arange(1, 16)
train_loss = [1.82, 1.45, 1.19, 1.00, 0.86, 0.76, 0.68, 0.62, 0.57, 0.53, 0.49, 0.46, 0.43, 0.41, 0.39]
validation_loss = [1.88, 1.53, 1.31, 1.14, 1.02, 0.94, 0.90, 0.88, 0.89, 0.92, 0.97, 1.03, 1.10, 1.17, 1.25]

fig, ax = plt.subplots()
ax.plot(epochs, train_loss, marker="o", label="train loss")
ax.plot(epochs, validation_loss, marker="o", label="validation loss")
ax.axvline(8, color="gray", linestyle="--")
ax.text(8.25, 1.38, "validation starts rising")
ax.set_xlabel("epoch")
ax.set_ylabel("loss")
ax.set_title("Training and validation loss can diverge")
ax.legend()
plt.show()
```

The output lets you compare the two loss curves on one axis as follows.

![Comparison plot showing train and validation loss diverging](/AiBook/assets/part-02/chapter-13/train-validation-loss-diverge.png)

This example connects to the intuition for overfitting that you will meet again in Part 3. If the training loss keeps falling but the validation loss rises again, you may suspect that the model is fitting the training data better while fitting new data worse.

Still, do not fix the conclusion here. This graph does not mean "overfitting is confirmed." It means "we should check the performance flow on validation data more closely."

## Saving a Plot Means Leaving a Record

In Colab or Jupyter Notebook, you can see a plot immediately with `plt.show()`. But if you want to use it in a book, report, or experiment log, you need to save it as an image file.

In Matplotlib, you use `savefig()`.

Problem situation: you need to leave the plot you saw on screen as a file so it can be reused in documents and records.
Input: an already created `fig` object and the file name to save.
Expected output: the current plot is saved as an image file such as PNG.
Concept to check: `plt.show()` is screen display, while `savefig()` stores a reusable result file.

```python
fig.savefig("train-validation-loss-diverge.png")
```

Understand it as follows.

| Code | Meaning |
| --- | --- |
| `plt.show()` | view the plot on the current execution screen |
| `fig.savefig(...)` | save the plot as an image file |
| `fig.tight_layout()` | adjust spacing so the title, axis labels, and plot area do not overlap |

In document projects, output images are often generated in this way. You run code to make an image, and then link that image inside a Markdown document.

## A Saved Image Alone Is Not Reproducible Enough

A plot file shows the result, but by itself it is not a reproducible record. To make the same plot again, you need the following information.

- the code that created the plot
- the data used, or the conditions that generated the data
- the libraries and versions used
- the random seed when random values are included
- the question the plot is answering

That is why a document project should not leave only the image file. When possible, it should also keep the Python script that generated the image. For example, if one plot will be revised several times, it is easier to recreate the result when the generation script sits near the image.

This approach is closer to "the picture can be recreated" than merely "the picture was attached."

## Points to Watch When Making Comparison Plots

When comparing several plots, watch the following points.

| Caution | Why |
| --- | --- |
| Do not force values with different units onto the same axis | The change can look distorted |
| Values with the same unit can be compared on the same axis | Direct comparison is possible, as with train loss and validation loss |
| Add a legend | You need to know what each line means |
| Check the axis range | Small differences can be exaggerated, or large ones can be hidden |
| Use descriptive file names when saving | You need to know later what the plot was |

Plots do not replace conclusions. But a good plot helps the next question become more precise.

## Perspective to Remember from This Section

- The reason to arrange several plots is to compare related questions.
- One `Figure` can contain multiple `Axes`.
- Values with different units should be separated, while values with the same unit can be compared on one axis.
- `savefig()` is the method for saving a plot as an image file.
- For a saved plot to become a reproducible record, the code and data conditions must also remain with it.

## Case Study

### Case 1. When You Need to Leave Loss and Accuracy in One Figure

Suppose a learner wants to organize model-training results and put them into a team document. Looking at the loss plot alone can show whether learning is stable, but looking at it together with accuracy can make a comparison question such as "does loss fall while accuracy stagnates?" much clearer.

The first human standard may be, "Wouldn't one plot be enough?" But in actual experiment records, interpretation becomes easier when related values are placed side by side, or when values of the same unit are compared together on one axis. That is why the structure with multiple `Axes`, legends, and axis labels matters.

Also, if you look at it once on screen and stop there, it becomes hard to explain again later. You should save the plot with `savefig()` and keep together the code and data conditions that created that plot, so the same result can be produced again.

The checkable result appears in the saved file and in re-executability. If a figure comparing `train loss`, `validation loss`, and `accuracy` remains as a file and can be generated again with the same script, then that plot functions not as a simple capture but as an experiment record.

## Short Check

- Can you explain that `plt.subplots(1, 2)` creates two Axes inside one Figure?
- Can you explain why loss and accuracy should be compared side by side?
- Can you explain why train loss and validation loss can be compared on the same axis?
- Can you explain the difference between `plt.show()` and `fig.savefig()`?
- Can you explain why a graph file alone is not sufficient for reproducibility?

## When Should You Recall This Perspective First?

- Recall the Figure and Axes layout first when several plots need to be placed side by side on one screen for comparison.
- Return to this section when you need to explain why metrics of the same kind, such as train and validation curves, should be compared on one axis.
- This section becomes the standard again when you need to recheck the difference between screen display and file saving, and why a plot image alone is not enough for reproducibility.

## Sources and References

- Matplotlib Developers, `Quick start guide`, Matplotlib documentation, checked on 2026-06-25. [https://matplotlib.org/stable/users/explain/quick_start.html](https://matplotlib.org/stable/users/explain/quick_start.html){: target="_blank" rel="noopener noreferrer" }
- Matplotlib Developers, `Introduction to Axes (or Subplots)`, Matplotlib documentation, checked on 2026-06-25. [https://matplotlib.org/stable/users/explain/axes/axes_intro.html](https://matplotlib.org/stable/users/explain/axes/axes_intro.html){: target="_blank" rel="noopener noreferrer" }
- Matplotlib Developers, `matplotlib.figure.Figure.savefig`, Matplotlib API reference, checked on 2026-06-25. [https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html){: target="_blank" rel="noopener noreferrer" }
