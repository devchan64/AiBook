# P2-7.1 Local Environment and Runtime

> Section ID: `P2-7.1`
> Version: `v2026.09.08`

Python code is read and executed by an interpreter. The local environment consists of Python, packages, files, and settings on your computer; the runtime consists of the programs and resources where code actually runs. Code entered in a browser may run on another computer.

## Python for AI Experiments

When studying AI, Python appears often. At that point the question can arise, `why Python in particular?`

Python was first developed by Guido van Rossum in the late 1980s and released in 1991. The official Python FAQ explains that Python was influenced by the experience of the ABC language and arose from the need for a more extensible scripting language in a situation where system-administration tasks were hard to handle only with C programs or shell scripts.

What matters in this history is that Python was from the start both a high-level language easy for humans to read and write and an execution tool connected to real system work.

That is why Python fits learning, automation, data processing, and experiment code well. The official Python FAQ also explains that Python is suitable as a first language because it has clear syntax, a large standard library, and an interactive interpreter.

The reason Python appears often in AI is connected to this same flow.

- It is easy to move formulas into code.
- Small experiments can be run quickly.
- There are many tools such as NumPy, Pandas, and Matplotlib.
- Many machine-learning and deep-learning libraries gather in the Python ecosystem.

Python is not the only language. Real services also use languages such as C++, Java, JavaScript, Go, and Rust. However, Python is commonly encountered when learning and experimenting with AI.

## Terminal Commands and Python Code

A terminal is a window for exchanging commands and results; a shell is the program that interprets commands. You can use a shell in macOS Terminal or Windows Terminal. Bash and PowerShell are examples of shells.

Entering this command at a terminal’s shell prompt prints the Python version.

```bash
python --version
```

`print("hello")` is Python code. Enter it in a notebook code cell or Python interpreter to print `hello`.

```python
# A Python statement that prints a string.
print("hello")
```

Merely writing the statement in a text editor does not run it. A program must read and execute the Python code. Entering `python --version` in a terminal and entering `print("hello")` in Python are different actions.

| Statement | Input location | Result |
| --- | --- | --- |
| `python --version` | Terminal shell prompt | Prints the Python version |
| `python example.py` | Terminal shell prompt | Runs example.py |
| `print("hello")` | Python code or notebook code cell | Prints hello |
| `%pip install numpy` | IPython-based notebook code cell | Installs NumPy in that kernel |

## Ways to Run the Interpreter

The Python interpreter reads and executes Python code. Where you provide the code depends on the execution method.

| Method | How to use it |
| --- | --- |
| Interactive | Run `python` in a terminal, then enter Python code at `>>>` |
| Script | Save code in example.py and run `python example.py` in a terminal |
| Notebook | Run a code cell connected to a Python kernel |

To end interactive execution and return to the shell, enter `exit()` at `>>>`. The prompt `>>>` itself is not code to type.

## Components of a Local Environment

The `local environment` means the conditions under which code runs inside my computer. This can include the operating system, Python installation location, package installation state, current working folder, and environment variables.

Even with the same code, the result can differ by computer.

For example, conditions can differ between computers in the following way.

- NumPy may be installed on my computer, but not on another computer.
- My computer may use Python 3.12, while another may use Python 3.10.
- A file path may be correct on my computer, but the file location may differ on another computer.

That is why in practice documents, `where is it executed?` matters as much as the code itself.

## Local Execution and Colab Runtimes

The runtime is where code actually runs. For local execution, this is your computer. With a hosted Colab runtime, the environment provided by Google processes the code.

| Execution style | Runtime |
| --- | --- |
| run a Colab code cell | Colab runtime |
| run in my computer terminal | local Python environment |
| activate a virtual environment and run | the Python and packages of that virtual environment |

Colab is convenient. It can run in the browser without Python installation. But the runtime can disconnect, files can disappear, or the service policy can change.

A local PC is troublesome at first to set up. But you can directly manage your project files, package versions, and execution style.

In summary, it is as follows.

- Colab: easy to start with, and the runtime is managed by an external service.
- local PC: requires initial setup, but I manage the runtime.

## Virtual Environments by Project

A `virtual environment` is a device that creates a separate execution space for each Python project. The official Python documentation explains that `venv` creates lightweight virtual environments and that each virtual environment can have an independent set of Python packages.

Why is it needed? Project A may need `numpy 1.x`, while project B may need `numpy 2.x`. If both are installed all mixed together on one computer, they can conflict, so the space is divided by project.

A virtual environment is not the project code itself. The official Python documentation also explains that virtual environments are usually created in directories such as `.venv` or `venv`, and are not put into source-control systems. In any project, `.venv` is the local environment for execution, not the body text file or code itself.

Running the following command in a terminal in the project folder creates a virtual environment in `.venv`.

```bash
python -m venv .venv
```

Select the created virtual environment’s Python to use the packages installed there. See [Virtual Environments and Package Installation](section-04.en.md) for creation and activation commands.

## Package Installation and import

A package groups related code for reuse. NumPy, Pandas, and Matplotlib are examples.

The roles are:

- Python: the language and execution program
- package: the bundle of code borrowed inside Python
- `pip`: the tool that installs packages

For example, the command that installs NumPy and the code that imports it are different.

```bash
python -m pip install numpy
```

Running the following code in Python with NumPy installed imports it as `np`. Success produces no separate output, and execution continues to the next statement.

```python
# This checks whether NumPy can be imported in the current runtime environment.
import numpy as np
```

The first is installation. The second is the act of loading it for use inside Python code.

## When an Import Works in Colab but Fails Locally

Suppose `import numpy as np` works in Colab but raises this error locally.

```text
ModuleNotFoundError: No module named 'numpy'
```

The running Python cannot find NumPy. It may be installed in another Python or virtual environment, so first identify the interpreter actually in use. Run this code in the same notebook kernel or Python execution method that produced the error; it prints the interpreter’s file path.

```python
import sys

# The location of the Python running this code.
print(sys.executable)
```

Check whether this is the Python intended for the project. Once that Python is selected in the terminal, check installation with `python -m pip show numpy`. If NumPy is absent, install it into that Python with `python -m pip install numpy`.

If installation succeeds but the same error remains, compare the Python paths used for installation and code execution. Checking the package name alone cannot distinguish installation in different environments.

## Where to Check Execution Problems

| Problem | What to check |
| --- | --- |
| A file cannot be found | [Terminals and Working Folders](section-02.en.md) |
| Unsure how to run Python code | [Interpreters and Scripts](section-03.en.md) |
| An installed package cannot be imported | [Virtual Environments and Package Installation](section-04.en.md) |
| Results differ on another computer | [Dependencies and Reproducibility](section-05.en.md) |

## Checklist

- You can explain `local environment` as the conditions under which code runs on my computer.
- You can explain `runtime` as the place where code actually runs.
- You can distinguish terminal commands from Python code.
- You can explain the Python interpreter as the program that reads and executes Python code.
- You can explain a virtual environment to the degree that it is the execution space for each project.
- You can explain at an introductory level that package installation and `import` are different actions.
- You can explain that Colab and a local PC are both runtimes, but their management styles differ.
- You can first check `where it runs`, `what executes it`, `what package is needed`, and `where that package is installed`.

## Sources and References

- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to support invoking the Python interpreter and distinguishing interactive input from script execution.
- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm the basic description of Python as an interpreted, interactive programming language available on multiple operating systems.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that a virtual environment has its own Python installation and package state inside an isolated directory.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, checked 2026-07-20. Used to confirm the project-level flow of creating a virtual environment, activating it, and installing packages.

- Python Software Foundation, [sys.executable](https://docs.python.org/3/library/sys.html#sys.executable){: target="_blank" rel="noopener noreferrer" }, checked 2026-09-08. Used to identify the executable path of the current Python interpreter.
