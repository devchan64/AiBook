# P2-3.5 Python Runtime Environments: Colab and Local PC

> Section ID: `P2-3.5`
> Version: `v2026.07.09`

Before checking linear algebra in NumPy, we need to separate where code is being run.

This early practice uses two environments:

1. Google Colab in the browser
2. A local PC with a terminal and Python installation

The main goal here is not a deep installation guide. The goal is to separate notebook-cell commands, terminal commands, and Python code.

## Scope of This Section

This Section distinguishes execution locations and the basic command forms used in each one. Detailed installation workflows return in Part 2 Module 3.

## One Table to Hold

| What you want to do | Colab code cell | Local PC terminal | Python code |
| --- | --- | --- | --- |
| install NumPy | `%pip install numpy` | `python -m pip install numpy` | not used here |
| import NumPy | `import numpy as np` | not used here | `import numpy as np` |
| run a quick calculation | `print(np.array([1, 2]))` | `python example.py` | `print(np.array([1, 2]))` |

## Why Confusion Happens

Many beginner errors come from putting the right text in the wrong place.

- `%pip install numpy` inside a `.py` file
- `import numpy as np` treated like a shell command
- a Colab example copied into a local terminal without changing the syntax

## Colab Is a Browser Notebook Environment

Colab lets you run Python in notebook cells without starting from a local setup. That is why it is often convenient for first practice.

## A Local PC Uses a Terminal and Your Own Python Environment

On a local machine, installation commands usually run in a terminal. Python statements belong in a Python interpreter, notebook cell, or `.py` file.

## Perspective to Keep

- Environment and syntax are tied together.
- Terminal commands and Python code are not interchangeable.
- Colab and local execution solve similar tasks in different places.

## Short Check

- Can you explain where `%pip install numpy` belongs?
- Can you explain where `python -m pip install numpy` belongs?
- Can you explain where `import numpy as np` belongs?
- Can you explain why the same task uses different syntax in different environments?

## Sources and References

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-24.
- Python Packaging Authority, [Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
