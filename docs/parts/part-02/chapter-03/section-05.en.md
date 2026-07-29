# P2-3.5 Python Runtime Environments: Colab and Local PC

> Section ID: `P2-3.5`
> Version: `v2026.07.26`

From P2-3.1 through P2-3.4, we looked at linear algebra mainly through formulas and comparison standards. In the next section, we will directly check vectors, matrices, and matrix multiplication with NumPy. Before that, we first need to separate where Python code is being run.

The early practice in this Part is explained with two runtime environments.

1. Google Colab runs directly in the browser.
2. A local PC runs in your own terminal and Python installation environment.

So here, rather than studying Colab itself deeply or covering the local installation procedure in detail, we focus on distinguishing `commands run in a code cell`, `commands run in your own PC terminal`, and `statements written inside Python code`, so that the later Python/NumPy practice can be followed correctly.

Here we reorganize `Colab`, `local PC`, `code cell`, `terminal`, and the difference between `import` and installation commands. If 3.1 through 3.4 were about reading formulas and linear-algebra structure, now we first organize the execution place that will carry those structures into real code.

How to install Python on your own PC and manage virtual environments returns in `P2-7.1`, `P2-7.6`, `P2-7.7`, and `P2-7.8`. Here we first fix the difference in execution location between Colab and a local PC. When you want to recheck the terms quickly, return to the notebook explanation in P2-10.1.

This document was written based on the official Google Colab guide and FAQ, the IPython `%pip` documentation, and the pip user guide checked on July 19, 2026. Colab is an external service, so its UI, usage conditions, free tier, runtime policy, or even service availability may change later. If, when you read this section, Colab is unavailable or looks different from this guide, you should separately check the current Google Colab documentation and service status.

## Core Criteria: Python Runtime Environments: Colab and Local PC

- You can understand Google Colab as a browser-based execution environment that requires no installation.
- You can understand local-PC execution as running inside your own computer’s terminal and Python installation environment.
- You can open the `Welcome to Colab` guide and try running a code cell.
- You can explain that `%pip` in Colab/Jupyter is not ordinary Python syntax but a magic command.
- You can distinguish Colab code-cell commands from personal-PC terminal commands.
- You can get ready to run the NumPy examples of the next section in Colab.

## One Scene to Hold First

The first scene to hold in this section is `where to type what if you want to use NumPy`.

| What you want to do | Colab code cell | Local PC terminal | Python code |
| --- | --- | --- | --- |
| Install NumPy | `%pip install numpy` | `python -m pip install numpy` | not used |
| Import NumPy | `import numpy as np` | not used | `import numpy as np` |
| Run a simple calculation | `print(np.array([1, 2]))` | can run as `python example.py` | `print(np.array([1, 2]))` |

So the first distinction the reader needs is not `what kind of command is this`, but `what kind of sentence is written in what place`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Colab is a browser-based practice space | Because it lets you run examples right away even before local Python installation. | Understand that it is a place where Python and notebook-style installation commands run inside code cells. |
| A local PC uses a terminal and an installation environment | Because even the same NumPy preparation changes its command form when the execution place changes. | Understand that `python -m pip` is used in the terminal, while `import` is used inside Python code. |
| Installation commands and Python code belong in different places | Because if the execution place is confused, syntax errors and environment errors repeat. | Understand the three places: Colab cell, local terminal, and Python code. |

## First Separate the Runtime Environment

The statement `run Python code` does not have only one meaning. Even for the same example, the form of the command changes depending on where it is run.

| Execution place | English | What it means | Example command |
| --- | --- | --- | --- |
| Colab code cell | Colab code cell | Run it in a code cell inside a browser notebook. | `%pip install numpy` |
| Local PC terminal | local terminal | Run it in the terminal app of your own computer. | `python -m pip install numpy` |
| Python code | Python code | Run it as a Python statement inside a `.py` file or a code cell. | `import numpy as np` |

If we miss this distinction, it becomes easy to mistake `%pip`, `python -m pip`, and `import` for the same thing. All three can relate to NumPy, but their execution place and role are different.

1. Packages are installed in a Colab code cell or a local PC terminal.
2. Installed packages are loaded inside Python code with `import`.

If we write the most frequent confusion one more time in a shorter form:

| Confusing scene | Why it blocks progress | Question to fix first |
| --- | --- | --- |
| Writing `%pip install numpy` inside a `.py` file | Because installation commands and Python code were mixed together | Am I writing in a code cell now, or in a Python file? |
| Trying to run `import numpy as np` directly as a terminal command | Because a Python statement was treated like a shell command | Am I writing in a terminal, or in a Python interpreter? |
| Copying a Colab example directly into a local environment | Because the execution place changed but the syntax was not changed | Is this environment a browser notebook, or my own PC? |

## Colab Is a Notebook Environment Opened in the Browser

Google Colab is a hosted service that lets you run Python code in the form of a Jupyter Notebook inside the browser. Even without installing Python on your own PC, you can create and run code cells.

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

Open the `Welcome to Colab` guide first and check how a code cell is run. The examples in this section are very small, so GPU or TPU is not needed. Still, Colab can have Google-account requirements, runtime limits, and resource limits.

## A Local PC Means Running on Your Own Computer

Running on a local PC means using the Python installed on your own computer and its terminal. Commands are run in programs such as Terminal on macOS, Windows Terminal, PowerShell, or a Linux shell.

For example, in a local PC terminal, NumPy can be installed like this.

```bash
python -m pip install numpy
```

And inside a Python file, NumPy is imported like this.

```python
# This line imports NumPy inside Python code.
import numpy as np
```

We do not cover the local installation process in detail here. Installation itself returns in the P2-7.7 supplementary learning section, and the syntax of terminals and environment variables returns in P2-7.6 and P2-7.8. What matters now is the distinction that `a Colab code-cell command and a local PC terminal command are different`.

## Put Python Code into a Code Cell

A Colab notebook has cells for writing text and cells for running code. Python code is run inside a code cell.

For example, the following code can be put into a code cell and run.

```python
# This is the smallest output check that confirms a Colab code cell is running.
print("hello, colab")
```

The result appears like this.

```text
hello, colab
```

Here, `print(...)` is Python code. By contrast, a package-installation command is slightly different in character from ordinary Python code.

## in Colab, You Can Use `%pip`

In many cases, NumPy is already available in the Colab environment. But because the environment can change, if needed we run the following command in a code cell.

```python
# %pip is an install command used inside a Colab/Jupyter code cell.
%pip install numpy
```

Here, `%pip` is not ordinary Python syntax. It is a magic command used in Jupyter Notebook style environments. It means “install a package into the current notebook kernel.”

In Colab or Jupyter documentation, you may also see examples that use an exclamation mark (`!`) to run shell commands, like this:

```python
# exclamation-mark form calls a terminal command from a code cell.
!pip install numpy
```

Here we prefer `%pip install numpy`, because it makes more explicit that the installation targets the notebook environment.

If we rewrite that difference again as a flow, it becomes:

```mermaid
--8<-- "assets/part-02/chapter-03/execution-location-flow-en.mmd"
```

## Do Not Mix It with Personal-PC Terminal Commands

On a personal PC terminal, you do not use `%pip` or `!pip`. Those forms belong to Colab/Jupyter code cells.

On a personal PC terminal, the usual form is:

```bash
python -m pip install numpy
```

So we first separate the execution places.

1. In a Colab code cell, use `%pip install numpy`.
2. In a personal PC terminal, use `python -m pip install numpy`.
3. Inside Python code, use `import numpy as np`.

In the next section, we check NumPy code on top of this distinction.

The minimum sentence the reader should keep from here is the following.

- `Install in a code cell or terminal, and use import and calculations inside Python code.`

## Checklist

- Can you explain the difference between Colab execution and local-PC execution in one sentence?
- Can you explain why `%pip install numpy` and `python -m pip install numpy` are not written in the same place?
- Can you explain that `import numpy as np` is not an installation command but Python code?
- Can you distinguish whether the sentence in front of you is for a code cell, a terminal, or Python code?
- Can you explain why you should distinguish the execution location before memorizing the syntax?

## Sources and References

- Google, `Google Colab`. It lets us directly check that Colab is a browser-based notebook environment and see the basic usage flow. [https://colab.research.google.com/](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-19
- Google, `Welcome to Colab`. It lets us directly confirm how code cells are run and how the basic notebook flow works. [https://colab.research.google.com/notebooks/intro.ipynb](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-19
- Google, `Google Colab FAQ`. It confirms that Colab is a hosted Jupyter Notebook service that requires no setup, and that runtime and usage limits can change. [https://research.google.com/colaboratory/faq.html](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-19
- IPython Development Team, `Built-in magic commands - %pip`. It confirms that `%pip install` runs the pip package manager within the current kernel. [https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-19
- Python Packaging Authority, `pip User Guide`. It provides official examples of installing packages from a local terminal with `python -m pip install ...`. [https://pip.pypa.io/en/stable/user_guide/](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-19
