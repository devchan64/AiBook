# P2-13.3 Comparing and Saving Multiple Plots

> Section ID: `P2-13.3`
> Version: `v2026.07.08`

P2-13.3 extends basic plotting into comparison and record-keeping. The key move is to place related questions side by side and save the result as a reusable artifact.

## Scope of This Section

This Section introduces subplots, comparison reading, legends, and `savefig()` as part of reproducible learning records.

## Central Question

How do multiple plots and saved image files help turn visual inspection into a reusable record?

![Subplots comparing loss and accuracy](../../../assets/part-02/chapter-13/subplot-loss-accuracy.png)

![Train and validation loss diverging](../../../assets/part-02/chapter-13/train-validation-loss-diverge.png)

## Perspective to Keep

- Multiple plots are useful when they sharpen a comparison question.
- Separate `Axes` help when values should be compared side by side but not forced onto one scale.
- `savefig()` preserves a chart as a file, but reproducibility still requires code and data context.
- A saved plot is stronger when the surrounding experiment conditions are also recorded.

## Short Check

- Can you explain why one `Figure` may contain several `Axes`?
- Can you explain when to compare flows in separate panels and when to compare them on one axis?
- Can you explain why an image file alone is not a complete reproducible record?

## Sources and References

- Matplotlib, [Creating multiple subplots](https://matplotlib.org/stable/gallery/subplots_axes_and_figures/subplots_demo.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- Matplotlib, [savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.savefig.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
