# P2-10.3 Organizing Notebooks as Rerunnable Records

> Section ID: `P2-10.3`
> Version: `v2026.09.15`

## Saved Documents and Execution State

Jupyter Notebook files are JSON-based documents with the `.ipynb` extension. The nbformat documentation describes lists of cells and metadata, with cells that can contain inputs and outputs. Jupyter's architecture documentation likewise describes notebooks as documents storing code, output, and Markdown notes together.

Distinguish code, saved output, and running state.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-structure-flow-en.mmd"
```

Code and some outputs can remain in the notebook file. Variables and imports live in the running kernel's memory, which a kernel restart clears. Disk files and installed packages are separate. Deleting a remote virtual machine can also remove files and installations stored only on that machine.

Saving a notebook is not enough: check whether the saved document can run again later.

## Clearing Outputs and Restarting the Kernel

Clearing the display and resetting memory are different operations. This table assumes the notebook has been saved and the same file system remains available.

| Action | Code and explanations | Displayed output | Variables and imports | Disk files |
| --- | --- | --- | --- | --- |
| Clear outputs only | Retained | Cleared | Retained | Retained |
| Restart kernel only | Retained | May remain | Reset | Retained |
| Restart kernel and run all | Retained | Updated by execution | Created in code order | Code may read or change them |

Restarting a kernel does not create a fresh installation or file system. Deleting a Colab remote VM and obtaining another resets more: files and packages that existed only on the old VM can disappear too.

## From Preparation to Interpretation

A useful learning notebook should read and execute from top to bottom.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-rerun-flow-en.mmd"
```

First write what you want to investigate. Then import packages, prepare data, and run calculations. Interpret the results after inspecting them.

When this order breaks down, reopening the notebook can leave you unsure why a calculation was performed, which data it used, or what the result means.

## Purpose and Data Scope

Put the purpose before the code at the start of the notebook.

For example: “This notebook calculates the mean and variance of a small score dataset to compare its center and spread.”

Notebooks grow quickly as cells are added. Without a purpose, experiments scatter and the meaning of results becomes unclear.

Briefly record these items in the purpose cell:

| Item | Reason |
| --- | --- |
| Question to investigate | Keep experiments focused |
| Data to use | Define the scope of results |
| Expected output | Identify what to inspect |
| Exclusions | Keep the notebook from expanding excessively |

If you add an experiment with a different purpose, give it a distinct title and input conditions.

## Package Preparation

Place installation instructions and imports before calculations. In a Python notebook without NumPy, use `%pip install numpy`. `%pip` is an IPython command targeting the current kernel environment, not ordinary Python script syntax.

This setup cell imports NumPy and prints its version. Record the version actually used, since it depends on the environment.

```python
import numpy as np
print(np.__version__)
```

## Input Data

Files require a source and preparation instructions as well as a path. Saving the string `data/scores.csv` does not save the file itself.

| Input type | What to record |
| --- | --- |
| Small example | Actual values and their meanings |
| Local file | File/folder location and working directory |
| Remote file | Download source and version or check date |
| Private storage file | Connection method and access permissions |

These are five students' scores out of 100. Assignment displays no output and prepares `scores` for the later calculation cell.

```python
scores = [82, 75, 45, 90, 61]
```

## Output and Interpretation

The scores total 353 across five students, giving a mean of 70.6. This cell prints a label alongside the value.

```python
print("mean score:", sum(scores) / len(scores))
```

The output is `mean score: 70.6`. Below it, write “The five students' mean is 70.6 and the lowest score is 45.” Update both output and interpretation if the data changes.

## Configuration Cell Order

When different cells assign the same name, the last executed assignment takes effect. The first cell sets a learning rate of 0.1.

```python
learning_rate = 0.1
```

The second changes it to 0.01.

```python
learning_rate = 0.01
```

The check cell prints the current value.

```python
print(learning_rate)
```

Running first cell → second cell → check gives `0.01`. Running second → first → check gives `0.1`. Keeping final settings in one cell reduces confusion between document order and execution order.

Check important notebooks as follows:

1. Remove unnecessary temporary cells while retaining required preparation.
2. Restart the Python kernel.
3. Run cells from first to last.
4. Check for errors and agreement between outputs and explanations.
5. Save the verified code, outputs, and interpretation.

## Starting State for Randomness

AI and statistics exercises use randomness for sampling and initialization. This code creates a generator with seed 42 and selects three of five values without replacement. The review environment produced `[50 10 40]`.

```python
import numpy as np

rng = np.random.default_rng(seed=42)
sample = rng.choice([10, 20, 30, 40, 50], size=3, replace=False)
print(sample)
```

A seed can be understood as a starting value for recreating the same random sequence. Fixing it is not mandatory in every exercise, but recording it helps when you want to see the same result again.

A seed does not solve all reproducibility problems. Package versions, environment, hardware, and parallel execution can affect results. Repeating only the sampling step advances the same generator's state and may produce different values. Rerun from generator creation to return to the same starting state.

## Preparation for Sharing

The Colab FAQ explains that text, code, output, and comments can be shared with a notebook, while its virtual machine, runtime files, and installed libraries are not shared.

Before sharing a Colab notebook, check:

| Check | Reason |
| --- | --- |
| Required package-installation cells | Recipient's runtime may lack packages |
| Data preparation instructions | Runtime files may not be shared |
| Drive access permissions | Recipient may lack access to private files |
| Top-to-bottom execution | Detect hidden-state dependencies |
| Output freshness | Saved outputs can disagree with current code |

## When to Move Code into Scripts

Code started in notebooks often grows. Eventually a `.py` script may become a better fit.

Consider separation when you see these signs:

| Sign | Meaning |
| --- | --- |
| Same code repeated across cells | Extract a function |
| Cell order often becomes confused | Script execution order may be more dependable |
| Same preprocessing every time | Extract a function or module |
| Code reused in other notebooks | A common `.py` file may help |
| Automatic execution needed | A script may fit better |

The organization can follow this pattern:

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-to-module-flow-en.mmd"
```

Keep common calculations in a module, with inputs and result interpretation in the notebook.

## Case: A Deleted Preparation Cell

Suppose the five-score mean displays correctly, then the cell creating `scores` is deleted. Rerunning only the mean cell in the same kernel still produces 70.6 because the variable remains.

After restarting, that mean cell raises `NameError` because `scores` is absent. Restore preparation and run from top to bottom. Saved output alone cannot establish that the current code can run again.

## A Runnable Record

This notebook contains purpose, inputs and threshold, calculation, output, and interpretation in order. It uses only standard Python features, with no external files or package installation. Download it and open it in Jupyter, or upload it as a notebook in Colab.

[Score and selection-threshold notebook](/AiBook/assets/part-02/chapter-10/score-record-en.ipynb)

The default scores are `[82, 75, 45, 90, 61]` and the threshold is 60. Running all cells produces:

```text
count: 5
mean: 70.6
threshold: 60
selected: [82, 75, 90, 61]
```

Change the input-cell threshold to 80 and rerun through calculation and output: the mean stays 70.6 and selection becomes `[82, 90]`. Changing the final score to 100 makes the mean 78.4. An empty score list deliberately raises `ValueError` in the calculation cell. Output left from a previous run after an error is not the current run's result.

Update the interpretation for the changed conditions, restart the kernel, and run all cells. Save when execution succeeds and output agrees with interpretation. Saved output is a comparison record, not a replacement for a new run.

## Checklist

- Can you explain a useful notebook as a rerunnable record?
- Can you explain why hidden state is a problem?
- Can you explain why setup and data cells belong near the beginning?
- Can you explain why restarting and running from top to bottom matters?
- Does the notebook start with purpose and scope?
- Are required imports and installation steps near the beginning?
- Is the input data source explained?
- Can all cells run in order without errors?
- Is interpretation recorded below outputs?
- Are seeds or possible variation explained when randomness is involved?
- Have files, packages, and permissions been checked for Colab sharing?
- Should repeated code move into functions or `.py` files?
- Can you explain why reproducibility needs the same preparation flow, not just the same file?

## Sources and References

- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation, checked on 2026-09-15. Used to confirm that notebook documents store code, output, and markdown notes together.
- Project Jupyter, [The Jupyter Notebook Format](https://nbformat.readthedocs.io/en/latest/format_description.html){: target="_blank" rel="noopener noreferrer" }, nbformat documentation, checked on 2026-09-15. Used to confirm that `.ipynb` files are JSON-based documents containing a list of cells, metadata, cell inputs, and outputs.
- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-09-15. Used as the basis for the caution that shared Colab notebook contents and runtime state are separate.
- NumPy Developers, [Random Generator](https://numpy.org/doc/stable/reference/random/generator.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Reference for generators, seeds, state, and version compatibility limits.
