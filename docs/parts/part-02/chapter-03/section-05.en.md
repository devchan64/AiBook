# P2-3.5 Python Runtime Environments: Colab and Local PC

> Section ID: `P2-3.5`
> Version: `v2026.09.08`

Python code can run in a Colab notebook code cell or in a Python interpreter on a local PC. Use installation commands appropriate to the environment, then load installed packages in Python code with `import`.

This document was written based on the official Google Colab guide and FAQ, the IPython `%pip` documentation, and the pip user guide checked on July 19, 2026. Colab is an external service, so its UI, usage conditions, free tier, runtime policy, or even service availability may change later. If, when you read this section, Colab is unavailable or looks different from this guide, you should separately check the current Google Colab documentation and service status.

## Installing, Importing, and Running

| What you want to do | Colab code cell | Local PC terminal | Python code |
| --- | --- | --- | --- |
| Install NumPy | `%pip install numpy` | `python -m pip install numpy` | not used |
| Import NumPy | `import numpy as np` | not used | `import numpy as np` |
| Run a simple calculation | `print(np.array([1, 2]))` | can run as `python example.py` | `print(np.array([1, 2]))` |

## Where Commands Run {#_2}

The statement `run Python code` does not have only one meaning. Even for the same example, the form of the command changes depending on where it is run.

| Execution place | English | What it means | Example command |
| --- | --- | --- | --- |
| Colab code cell | Colab code cell | Run it in a code cell inside a browser notebook. | `%pip install numpy` |
| Local PC terminal | local terminal | Run it in the terminal app of your own computer. | `python -m pip install numpy` |
| Python code | Python code | Run it as a Python statement inside a `.py` file or a code cell. | `import numpy as np` |

If we miss this distinction, it becomes easy to mistake `%pip`, `python -m pip`, and `import` for the same thing. All three can relate to NumPy, but their execution place and role are different.

1. Packages are installed in a Colab code cell or a local PC terminal.
2. Installed packages are loaded inside Python code with `import`.

Running a command in the wrong place can cause the following problems.

| Confusing scene | Why it blocks progress | How to fix it |
| --- | --- | --- |
| Writing `%pip install numpy` inside a `.py` file | Because installation commands and Python code were mixed together | Run it in a code cell, or use `python -m pip` in a terminal. |
| Trying to run `import numpy as np` directly as a terminal command | Because a Python statement was treated like a shell command | Run it in a Python interpreter or a `.py` file. |
| Copying a Colab example directly into a local environment | Because the execution place changed but the syntax was not changed | Distinguish notebook installation commands from local terminal commands. |

## Colab Notebooks

Google Colab is a hosted service that lets you run Python code in the form of a Jupyter Notebook inside the browser. Even without installing Python on your own PC, you can create and run code cells.

- [Google Colab](https://colab.research.google.com/){: target="_blank" rel="noopener noreferrer" }
- [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }
- [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }

Open the `Welcome to Colab` guide first and check how a code cell is run. The examples in this section are very small, so GPU or TPU is not needed. Still, Colab can have Google-account requirements, runtime limits, and resource limits.

## Running on a Local PC

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

## Python Statements in Code Cells

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

## Notebook Installation Command `%pip`

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

Installation and importing take place as shown below.

```mermaid
--8<-- "assets/part-02/chapter-03/execution-location-flow-en.mmd"
```

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
