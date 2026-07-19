# P2-10.3 Organizing Notebooks as Re-runnable Records

> Section ID: `P2-10.3`
> Version: `v2026.07.19`

In P2-10.1, we viewed a notebook as a computational document containing code, explanation, and output together. In P2-10.2, we distinguished Jupyter, Colab, and local execution from the viewpoint of execution location and file access.

Now we go one step further. A notebook is useful as a learning record, but after cells are run many times, the order visible in the document and the actual execution state can diverge. So a notebook must be organized both as `a readable document` and as `a reproducible record`.

This Section explains the basic distinctions among `reproducible record`, `execution order`, `hidden state`, and `runtime state`. The representative explanation of `notebook` and cell structure is in P2-10.1, execution-location differences are in P2-10.2, and the representative explanation of `reproducibility` is placed in P2-7.5 and the [Concept Glossary](/AiBook/reference/concept-glossary/). Here the focus is on the standard for organizing that record so that it can be trusted again.

Seen in the flow of Part 2, Chapter 7 treated `where execution happens`, Chapters 8 through 9 treated `what is written and in what kind of sentences`, and Chapter 10 treats `how that execution and output are left so that they can be read again`. Only when this standard stands do Chapters 11 through 14 read not as a list of new tool names, but as a preparation flow where arrays are calculated in notebooks, tables are read, graphs are checked, and records are left through Git.

This Section focuses less on notebook decoration tips and more on the standard for organizing execution results into records that can be trusted again. If the previous Sections explained what a notebook is and where it runs, this Section looks at what must be left so that the notebook can be rerun and re-explained later. Read this way, the tools in Chapters 11 through 14 also become easier to read inside a record flow of rechecking computation and interpretation rather than as new features.

| What to capture in this Section now | The question that follows immediately next | Where it appears again later |
| --- | --- | --- |
| The point that a good notebook must be both a readable document and a rerunnable record | It leads to what order should be used to leave calculations, tables, visualizations, and Git records in Chapters 11 through 14 | It repeats later in every practice notebook, Colab sharing, and project record |
| The point that cell order and hidden state can change results | It leads to why the habit of restarting and running from top to bottom is needed | It remains important later in debugging, reproducibility checks, and collaboration sharing |
| The point that notebook-verified code reaches a point where it should be separated into functions and `.py` files | It leads to the criterion for deciding where to separate records and reusable code | It is used again later in utility scripts, project structure, and Git record organization |

| Term | Meaning to capture first in this Section |
| --- | --- |
| reproducible record | A notebook that can reproduce execution and interpretation later through the same flow |
| execution order | The order in which cells were actually run |
| hidden state | Variables, imports, and temporary results that remain inside the runtime but are not directly visible in the document |
| runtime state | Variables, packages, and memory state that live only in the current session |
| setup cell | A cell near the front that gathers package imports, options, and data preparation |

## Scope of This Section

This Section focuses on the standard for making notebooks into rerunnable records: execution order, cell order, hidden state, and the placement of setup and data-preparation cells. Larger experiment-tracking systems are reconnected later in the supplement P3-9.3 and in Part 6 project records.

This Section answers the following questions.

- Why should a notebook be rerun again from top to bottom?
- In what order should code cells, markdown cells, and output be arranged?
- Where should packages, data files, and randomness be written down?
- In what different ways should reproducibility be watched in Colab and local execution?
- When is it good to separate code that began in a notebook into a `.py` file?

This Section connects the dependency and reproducibility ideas of Part 2 Chapter 7 Section 5, the strengths and weaknesses of notebooks in P2-10.1, and the execution-environment differences of P2-10.2 into habits for practice records.

## Goals of This Section

- You can explain why a notebook should be organized as a learning record that can be rerun.
- You can explain that execution order and hidden state can make notebook results confusing.
- You can explain why environment, package, and data-preparation cells should be placed near the front of a notebook.
- You can explain that in Colab sharing, notebook content and runtime state can be different things.
- You can explain the point at which code verified in a notebook should be separated into functions and scripts.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What makes a good notebook different | It makes you see document quality and rerunnability together | The reading flow and the execution flow should be organized together |
| Why cell order must be watched | It connects the hidden-state problem of notebooks to the structure of the document itself | Understand that even if a notebook looks like a document, it is really also an execution record |
| What does it lead to later | It lets you see in advance the boundary between record notebooks and reusable code | A well-organized notebook becomes the starting point of scripts and project code |

## A Notebook Is Both a Document and an Execution Record

Jupyter Notebook files are JSON-based documents with the `.ipynb` extension. The nbformat documentation explains that a notebook contains a list of cells and metadata, and that each cell can have inputs and outputs. Jupyter architecture documentation also explains notebooks as documents that store code, output, and markdown notes together.

Understand this structure here like this.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-structure-flow-en.mmd"
```

What matters here is that the content saved in the file and the state during execution are not the same thing.

Code and some output can remain in the notebook file. But variables, imported packages, temporary files, and memory state live in the runtime. If the runtime is restarted, that state can disappear.

So simply saving a notebook is not enough. You also need to check whether the saved notebook can be rerun later.

## Create a Flow That Runs from Top to Bottom

A good learning notebook should be readable and runnable from top to bottom.

The following flow can be used as a default.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-rerun-flow-en.mmd"
```

This structure is not formality. It is an order of thinking.

First write what you want to check. Then load the needed packages, prepare the data, and run the calculation. After seeing the result, write the interpretation.

If this order collapses, then later when reopening the notebook it becomes easy to lose `why this calculation was done`, `what data was used`, and `what the result means`.

## Write the Purpose in the First Cell

Near the beginning of the notebook, place the purpose before the code.

For example, you can begin with something like `This notebook calculates the mean and variance of a small score dataset and checks how the center and spread of data differ.`

This one sentence becomes very important later. As cells are added, notebooks become long quickly. Without a purpose, experiments scatter and it becomes unclear what the result is explaining.

Write the following briefly in the purpose cell.

| Item | Why it is written |
| --- | --- |
| question to check | prevents the experiment from scattering |
| data to be used | makes the scope of the result clear |
| expected output | defines what should be looked at |
| what is not covered | prevents the notebook from growing too large |

A notebook is similar to a Section. If possible, one notebook should also have one central question.

## Gather Packages and Settings Near the Front

If imports are scattered through the middle of a notebook, it becomes hard later to find which packages are needed when rerunning it.

A good habit is to keep a setup cell near the front.

Problem situation: You want it to become visible at once, near the front of the notebook, which packages are being used.
Input: Import code for `numpy`, `pandas`, and `matplotlib`.
Expected output: There is no output, but the package names needed for later cells are prepared.
Concept to check: See that gathering imports near the front makes notebook rerunning and dependency inspection easier.

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

This cell shows `which tools does this notebook use?`

In Colab, cells that install packages are also placed near the front.

Problem situation: You want a person who received a shared Colab notebook to install the required packages first.
Input: A `%pip` command that installs `numpy`, `pandas`, and `matplotlib`.
Expected output: The required packages are installed into the current kernel.
Concept to check: See that placing package-installation cells near the front makes it easier for someone else to prepare a similar runtime.

```python
%pip install numpy pandas matplotlib
```

You also often see `!pip install ...` in Colab or Jupyter. `!` means that a shell command will be run from a notebook cell. But for Python package installation, an IPython magic command such as `%pip` often matches the currently running kernel better, so here `%pip` is introduced first whenever possible.

At this point, what matters is not the installation method itself, but the fact that package installation and imports need to be near the front so that another person can understand the preparation needed for rerunning the notebook.

## Keep a Clear Data-Preparation Cell

One common reason notebook practice fails is the file path.

On a local PC, the following path may exist.

Problem situation: You want to see with the simplest string example that even the same notebook can have different file paths depending on the execution environment.
Input: A CSV file-path string based on a local project.
Expected output: There is no output, but it becomes visible which file location the code expects.
Concept to check: See that a rerunnable notebook must leave the file path and data location clearly inside the code.

```python
data_path = "data/scores.csv"
```

But in Colab, the same file may not exist. The path changes depending on whether the file was uploaded, whether Google Drive was connected, or whether it was downloaded from GitHub.

So in the data-preparation cell, one of the following should be clear.

| Situation | What to leave in the notebook |
| --- | --- |
| small example data | create it directly in the code |
| local file | write the file location and folder structure |
| Colab upload | write that upload is required |
| Drive file | write the Drive connection and permission condition |
| downloaded web file | write the download source and checked date |

Here it is often better, when possible, to place small example data directly in the code.

Problem situation: To focus on the concept itself without file-path problems, you place a small example dataset directly in the code.
Input: A list containing five scores.
Expected output: There is no output, but the data needed for later cells is prepared immediately.
Concept to check: See that in early learning, small data inside the code is better for rerunnability and understanding than file-based setup.

```python
scores = [82, 75, 45, 90, 61]
```

This may be insufficient for a real project, but it is good for concept learning. It lets you focus on ideas such as mean, variance, sample, and error without file problems.

## Leave Output, but Leave Interpretation Too

A notebook can store output. But if only output remains, the learning record is not sufficient.

For example, suppose the following output exists.

Problem situation: You want to see why a saved output that is only one number becomes hard to interpret later.
Input: A single number `67.3` left as a cell output.
Expected output: Only a context-free number remains, with no clue whether it is a mean or a loss.
Concept to check: See that output should not be left as only a value, but with interpretation placed right below it.

```python
67.3
```

Looking at it later, it becomes hard to know whether this number is a mean, an accuracy, or a loss.

So directly below the output, place a short interpretation such as `The mean is 67.3. But because a low value like 45 is included, the whole distribution is hard to explain through the mean alone.`

This one sentence changes the quality of the learning record. A notebook should not be just a file containing code. It should be a record that interprets computed results.

## Cell Execution Order Can Change the Result

Cells in a notebook can be executed freely. That advantage is also a risk.

Think about the following situation.

Problem situation: In one cell, a hyperparameter value is first defined.
Input: The code `learning_rate = 0.1`.
Expected output: There is no output, but the current learning-rate value is stored in the runtime.
Concept to check: See that variable state in a notebook changes depending on cell execution order.

```python
learning_rate = 0.1
```

Later, the value is changed again in another cell.

Problem situation: In the same notebook, the same variable is overwritten in another cell.
Input: The code `learning_rate = 0.01`.
Expected output: There is no output, but the current runtime value is overwritten with the new value.
Concept to check: Confirm that the visible order of the document and the actual last execution state can differ.

```python
learning_rate = 0.01
```

Two values are visible in the document from top to bottom, but in the actual runtime the value from the most recently executed cell remains. If the lower cell was executed first and the upper cell later, the result can change again.

So an important notebook is checked as follows.

1. Restart the runtime.
2. Run from the first cell to the last cell in order.
3. Check whether there is any cell that raises an error.
4. Check whether the output matches the explanation.
5. Clean up unnecessary temporary cells.

Through this process, the notebook becomes closer not to `a record that happened to run on my computer once`, but to `a record that can be rerun again`.

If this checking sequence is written more briefly again:

| Check step | Why it is needed |
| --- | --- |
| restart runtime | to remove hidden state |
| run top to bottom | to align document order with execution order |
| check errors | to see whether any necessary cell is missing |
| check output and interpretation | to see whether the result matches the explanation |
| clean up unnecessary cells | to keep the rerunnable record from becoming blurry |

## Fix Randomness or Explain It

In AI and statistics practice, random elements appear often. The result can change when sampling, shuffling data, or setting a model's initial values.

Here, even simply explaining that randomness exists is already a starting point.

Problem situation: You want to see an example in which the seed is fixed so that the same random sampling can be checked again.
Input: A random generator with seed `42` and code selecting three values from five.
Expected output: A sampled list is printed in a reproducible way.
Concept to check: See that in random practice, leaving a seed makes it easier to check the same result flow again.

```python
rng = np.random.default_rng(seed=42)
sample = rng.choice([10, 20, 30, 40, 50], size=3, replace=False)
sample
```

Here the `seed` can be viewed as a starting value for recreating the same random flow. Not every practice notebook must fix a seed, but if you want to see the same result again, then leaving the seed is good.

One caution is that a seed does not solve every reproducibility problem. Results can still vary depending on package version, execution environment, hardware, or parallel processing style. This Section does not go deeply into those details.

## In Colab Sharing, Notebook Sharing and Runtime Sharing Are Different

The Colab FAQ explains that when a notebook is shared, notebook contents such as text, code, output, and comments may be shared, but the virtual machine, runtime files, and installed libraries are not shared.

So when sharing a Colab notebook, the following should be checked.

| What to check | Why |
| --- | --- |
| Is there a cell that installs the required packages? | The other person's runtime may not have them installed |
| Is there a way to prepare the data files? | Files in my runtime may not be shared |
| Are Drive file permissions required? | The other person may not be able to access personal Drive files |
| Does it run from top to bottom? | This checks whether it reproduces without hidden state |
| Is the output outdated? | Saved output may differ from the result of the current code |

This also matters when creating example notebooks for the book. When a reader opens a link, it should not only show code, but also make clear what should be run first.

## When to Move from Notebooks to Scripts

Code that began in a notebook grows over time. At some point, it becomes better to move it into a `.py` script.

Consider separation when the following signals appear.

| Signal | Meaning |
| --- | --- |
| The same code is repeated across several cells | It can be bundled into a function |
| Cell order becomes tangled often | Script execution order may be safer |
| The same preprocessing is done every time | It can move into a separate function or module |
| The same code is used in other notebooks too | A common `.py` file may be needed |
| Automatic execution is needed | A script is more natural than a notebook |

The flow can be taken like this.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-to-module-flow-en.mmd"
```

Here it is not demanded that you create a package structure from the beginning. First understand it in a notebook, then when repeated code becomes visible, bundle it into a function, and when reuse becomes necessary, separate it into files.

## A Minimal Template for Learning Notebooks

When making a learning notebook, the following flow can be used as a default template.

| Order | Cell role | Example |
| --- | --- | --- |
| 1 | purpose | the question this notebook will check |
| 2 | environment | package installation, imports, version checks |
| 3 | data | small example data or file path |
| 4 | calculation | run only one concept at a time |
| 5 | output | numbers, tables, charts, error messages |
| 6 | interpretation | what the result means |
| 7 | summary | what was learned and what question comes next |

This template is not formality. It is a checklist. The longer the notebook becomes, the more you should check whether `purpose, environment, data, calculation, output, interpretation` are all present.

Before moving to the next Chapter of Part 2, check only three things. Can the notebook be rerun from top to bottom? Are packages, data, and output interpretation left near the front cells? Is repeated code ready to be moved later into functions and `.py` files? Once this standard stands, the next Chapters 11 through 14 continue not as a zone of learning more tool names, but as a flow of calculating arrays inside organized notebooks, reading tables, checking graphs, and leaving records through Git.

In other words, the goal of P2-10 is not to master notebooks completely. It is to establish a standard for leaving pre-Part-3 computation records in a form that can be rerun.

## Case Study

### Case 1. A notebook that works today but not tomorrow

Suppose a learner did a data-preprocessing practice in Colab and ran cells here and there. A file-upload cell was run in the middle, a variable name was changed in another cell, and at the end a chart appeared correctly. That day, the document can look finished.

But the next day, after reopening the runtime and running from top to bottom, the file may be missing, a later cell may refer to a variable not present in earlier cells, and the saved output may not match the current code. A person feels, `Why did it work yesterday but not now?` But in reality, the notebook has been left only as `a readable document`, not organized as `a rerunnable record`.

To reduce this problem, purpose, package installation, imports, and data preparation should be gathered near the front, calculation and interpretation should be arranged in order, and finally the runtime should be restarted and run again from beginning to end. Only if the same result appears again does the notebook become closer to a reproducible record instead of an experiment that happened to work.

This case shows the core of notebook organization. Reproducibility is not about making `a pretty document`. It is about reducing hidden state and making it possible to verify again through the same flow on another day.

## Checklist

- Can you explain a good notebook as `a rerunnable record`?
- Can you explain why hidden state is a problem?
- Can you explain why a setup cell and a data-preparation cell should be near the front of the notebook?
- Can you explain why the runtime should be restarted and rerun from top to bottom?
- Is there a purpose and scope near the beginning of the notebook?
- Are the necessary import and package-installation cells near the front?
- Is it explained where the data file comes from?
- Is there no error when the cells are rerun from top to bottom?
- Is interpretation left below the output?
- If randomness exists, is the seed or variability explained?
- When sharing in Colab, is it checked whether file, package, and permission issues will arise?
- Is there a need to separate repeated code into functions or `.py` files?


## Sources and References

- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, checked on 2026-07-19. Used to confirm that notebook documents store code, output, and markdown notes together.
- Project Jupyter, [The Jupyter Notebook Format](https://nbformat.readthedocs.io/en/latest/format_description.html){: target="_blank" rel="noopener noreferrer" }, nbformat 5.10 documentation, checked on 2026-07-19. Used to confirm that `.ipynb` files are JSON-based documents containing a list of cells, metadata, cell inputs, and outputs.
- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-07-19. Used as the basis for the caution that shared Colab notebook contents and runtime state are separate.
