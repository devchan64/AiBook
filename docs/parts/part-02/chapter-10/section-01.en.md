# P2-10.1 Why Are Notebooks Useful for Learning?

> Section ID: `P2-10.1`
> Version: `v2026.09.15`

A notebook is a computational document that stores code, results, and explanations together. In Jupyter Notebook or Google Colab, you can run code cell by cell and write interpretations beside the numbers, tables, and charts it produces.

## Code and Markdown Cells

A cell is a small document block. Code cells execute calculations; Markdown cells record headings, explanations, equations, and links. Output belongs to the code cell that produced it; it is not a separate cell type.

| Component | Role | Example |
| --- | --- | --- |
| Markdown cell | Record questions and interpretations | Check both the average and the low score among three students |
| Code cell | Execute a calculation | `sum(scores) / len(scores)` |
| Code-cell output | Display the result | `67.33333333333333` |

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-cell-learning-flow-en.mmd"
```

The mean of `[82, 75, 45]` is approximately 67.33. A Python script can display it with `print()`.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
print(average)
```

A Python notebook cell also displays the value of its final expression. This cell stores the result in `average`, then displays it on the last line. The output matches the previous code.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
average
```

A Markdown cell after the calculation could say, “The mean is about 67.33, but one student scored 45.” This records both the representative value and an individual value. Editing the code does not automatically update this interpretation.

## Experiments Across Cells

Separating data preparation, calculation, and condition changes makes each stage's results easier to identify.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-experiment-flow-en.mmd"
```

The first code cell prepares five students' scores. Assignment alone displays no output, but creates `scores` in the running Python kernel. A kernel is the process that executes code and maintains state such as variables.

```python
scores = [82, 75, 45, 90, 61]
```

The second cell calculates the mean of those scores and displays `70.6`.

```python
mean_score = sum(scores) / len(scores)
mean_score
```

The third cell selects scores at or above the threshold `60`, displaying `[82, 75, 90, 61]`.

```python
threshold = 60
passed = [score for score in scores if score >= threshold]
passed
```

Change `threshold` to `80` in the third cell and rerun only that cell: it displays `[82, 90]`. The scores and mean remain unchanged; only the selection criterion and result change.

## Input Changes and Dependent Cells

`mean_score` stores the number calculated at that moment, not a formula continuously linked to `scores`. With the threshold set to 60, run the three cells above, then change the last score in the data cell from `61` to `100` and compare the results.

| Action | Last score in kernel | Stored `mean_score` | `passed` with threshold 60 |
| --- | --- | --- | --- |
| Edit code without running it | 61 | 70.6 | `[82, 75, 90, 61]` |
| Rerun only the data cell | 100 | 70.6 | `[82, 75, 90, 61]` |
| Rerun data → mean → selection cells | 100 | 78.4 | `[82, 75, 90, 100]` |

After changing the cell that creates an input, rerun calculations and outputs that use it. Execution numbers beside cells give clues about execution order, but do not guarantee that current code, inputs, and outputs agree. Code can be edited after execution, or another cell can change a variable.

## Execution Order and Retained State

Cell order on the page can differ from execution order. Running this first cell stores `x = 10` in the kernel.

```python
x = 10
```

Running the next cell displays `15`.

```python
x + 5
```

If you edit the first cell to `x = 100` without running it, rerunning the second still displays `15`: the kernel retains `10`. Run the first and then the second cell to obtain `105`.

Restarting the kernel clears previous variable state. Running only the second cell then raises `NameError` because `x` is undefined. Restarting and running all cells from top to bottom checks whether the code remaining in the document can recreate its results.

| What to check | Why |
| --- | --- |
| Import and data-preparation cells | Confirm required inputs and packages |
| Restart kernel and run all | Detect reliance on values left from previous runs |
| Agreement between code and output | Check whether edited code actually ran |
| Agreement between output and interpretation | Check whether explanations reflect changed results |

## Case: Equal Means, Different Spread

Both score lists below have a mean of 12. Averages alone hide the difference, so we also calculate distance from the mean. We use descriptive variance: the sum of squared deviations divided by the number of items.

```python
sample_a = [10, 12, 13, 11, 14]
sample_b = [8, 16, 9, 15, 12]

mean_a = sum(sample_a) / len(sample_a)
mean_b = sum(sample_b) / len(sample_b)
variance_a = sum((value - mean_a) ** 2 for value in sample_a) / len(sample_a)
variance_b = sum((value - mean_b) ** 2 for value in sample_b) / len(sample_b)

print("means:", mean_a, mean_b)
print("variances:", variance_a, variance_b)
```

```text
means: 12.0 12.0
variances: 2.0 10.0
```

The interpretation could say, “The means are equal, but B's variance is five times as large.” Replace B with `[10, 14, 11, 13, 12]` and rerun: its mean remains 12 and its variance becomes 2. Both lists now have equal means and variances, so the old interpretation must change.

Notebooks can retain inputs, calculations, outputs, and interpretations together. Rerunning calculations and editing interpretations after changing inputs are still separate actions.

## Uses of Notebooks and Scripts

Notebooks suit exploration that examines intermediate results alongside explanations. Repeated tasks and functions reused across projects can move into `.py` scripts or modules.

| Task | Example organization |
| --- | --- |
| Interpret data and charts | Keep code, output, and interpretation in the notebook |
| Compare experimental conditions | Record each condition's results and explanation |
| Reuse processing across experiments | Extract common functions into a Python module |
| Repeat a defined task | Use a script with clear inputs and execution order |

For example, a module can contain score-statistics functions while the notebook calls them to compare two inputs and interpret their results.

## Checklist

- Explain notebooks as computational documents combining code, explanation, and output.
- Distinguish code cells from Markdown cells.
- Explain why notebooks help record AI mathematics and Python practice.
- Explain how cell execution order can affect results.
- Explain why notebooks do not completely replace scripts.
- Record questions, code, output, and interpretation together.
- Explain notebooks as both execution tools and learning records.

## Sources and References

- Project Jupyter, [Project Jupyter Documentation](https://docs.jupyter.org/en/latest/){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation, checked on 2026-07-20. Used to confirm that notebooks are documents combining code, explanation, data, visualization, and interaction.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation, checked on 2026-09-15. Used as background for distinguishing notebook documents, user interfaces, kernels, and related components.
- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-07-20. Used to confirm examples of running and recording code with explanations in a browser-based notebook environment.
- IPython, [Execution semantics](https://ipython.readthedocs.io/en/stable/interactive/reference.html#execution-semantics){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Reference for final-expression display and code execution.
