# P2-7.4 Virtual Environments and Packages

> Section ID: `P2-7.4`
> Version: `v2026.09.08`

A virtual environment gives each project a separate set of Python packages. If packages are installed with a different Python from the one running the code, installation can succeed while `import` fails.

| Term | Meaning to establish first in this section |
| --- | --- |
| virtual environment | A Python execution space separated by project. |
| package | A bundle of code you can bring into Python and use. |
| `pip` | A tool that installs packages. |
| `import` | A statement that loads an already prepared package into Python code. |
| `.venv` | A representative local virtual-environment directory name placed inside a project folder. |

## Project Separation and Installation Location

| Criterion | Why it matters |
| --- | --- |
| A virtual environment is a project-specific Python execution space | Because each project may need different tool versions |
| Installation and `import` are different stages | Installation is preparation, and `import` is the act of actually loading something inside code |
| The most common mistake is that the environment where you installed something and the environment where you ran it are different | There can be multiple Python spaces even on one computer |

## Background of venv

PEP 405 is the proposal to add `venv` to the Python standard library. The document was created in 2011 and targeted Python 3.3. Its motivation explains that third-party virtual-environment tools such as `virtualenv` were already widely used for dependency management, isolation, installing and using packages without system administrator privileges, and automated testing across multiple Python versions.

If you compress that background from a beginner's perspective, it comes down to this.

- Python packages became numerous: different projects started to need different external code.
- It was hard to modify the system Python carelessly: you could break the Python environment used by the operating system or by other programs.
- There were many cases where installation had to happen without administrator privileges: in personal projects or server accounts, you often could not freely change the whole system.
- People had to test multiple projects and Python versions: one global installation space made conflicts hard to avoid.

## Package Versions by Project

For example, project requirements can differ like this.

- Project A was written for `numpy 1.x`.
- Project B was written for `numpy 2.x`.
- If you mix them in the same space, one side may break.

A virtual environment is a way to divide Python execution space by project to reduce these conflicts. The official Python documentation explains that `venv` creates lightweight virtual environments and that each environment can have its own independent set of Python packages.

- Virtual environment for project A: install the packages needed for project A.
- Virtual environment for project B: install the packages needed for project B separately.

## Virtual Environments and Shared Files

A virtual environment is the surrounding environment used to run a project. It is different from the manuscript or code of the project itself.

For example, inside a project folder you may see a folder named `.venv`. This folder is a local execution environment that contains the packages needed to run Python or build documents. It is not the body's source files or the code itself.

That is why virtual-environment folders are usually not committed to Git. The official Python documentation also explains that virtual environments can usually be created with a name such as `.venv` inside a project directory and are not typically placed under source control.

So people usually separate things like this.

- What to commit: manuscript files, code, configuration files, example files
- What not to commit: the virtual-environment folder created on my computer

Rather than sharing the virtual environment itself, record the required packages so they can be installed again.

## Python Packages

A package is a bundle of code distributed so that you can bring it into Python and use it. Tools such as NumPy, Pandas, and Matplotlib belong here.

Here too, keep three layers distinct.

- Python: the language and the execution program
- package: a bundle of code you bring into Python and use
- package repository: a place where packages can be downloaded

The Python Packaging User Guide introduces a flow that uses `pip` and `venv` to install packages inside a virtual environment. What matters here is that installing a package and loading it in code are different actions.

## pip Installation and import

The following command is a terminal command that installs a package.

```bash
python -m pip install numpy
```

This is a terminal command, not a statement for a Python code file. `python -m` runs a module using the specified Python; here it runs pip to install NumPy.

By contrast, the following is Python code.

With NumPy installed in the selected Python, `import numpy as np` makes it available as `np` without printing output.

```python
# This imports the NumPy package installed in the current environment.
import numpy as np
```

This code is a statement that loads already installed NumPy so that it can be used in the current Python code.

You should not mix the two statements.

| Purpose | Example | Where to enter it |
| --- | --- | --- |
| Package installation | `python -m pip install numpy` | Terminal |
| Package use | `import numpy as np` | Python code |

- `install`: prepare the package in my execution environment
- `import`: use that package in the current Python code

## Installation and Execution Environments

An error beginners frequently see is the situation, "I definitely installed it, but Python says it is not there."

At that point, you have to separate "where did I install it?" from "where am I running it?"

For example, the place where you installed it and the place where you ran it may differ like this.

- You installed it in the system Python, but you are running it with the virtual-environment Python.
- You installed it in virtual environment A, but you are running it in virtual environment B.
- You installed it in Colab, but you are running it on your local PC.

Packages are not installed abstractly "somewhere on the computer." They are installed into a specific Python execution environment. That is why, when you use a virtual environment, you should use the same virtual environment both when installing packages and when running the code.

## Installing and Running with the Environment’s Python

After creating a virtual environment in the project folder, specify its Python path directly to install and import packages. This does not depend on activation.

Run these commands in order in a macOS/Linux terminal. Python must be available as `python3`.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install numpy
.venv/bin/python -c "import numpy; print(numpy.__version__)"
```

In Windows PowerShell, if Python is available as `python`, use:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install numpy
.\.venv\Scripts\python.exe -c "import numpy; print(numpy.__version__)"
```

The first command creates `.venv`, and the second installs NumPy there. In the last command, `-c` executes the following string as Python code, printing the installed NumPy version.

Creating `.venv` alone and then running an ordinary `python -m pip install numpy` can install into another Python. Activation is another option, but specifying the executable path as above makes the selected environment visible in the command.

## Packages in a Colab Runtime

Colab lets you edit code in a browser and execute it in a runtime. With a hosted runtime, local Python installation is unnecessary.

But even in Colab, package installation and execution-environment issues do not disappear.

In Colab code cells, `%pip` installs packages into the current notebook kernel. Running the following cell prepares NumPy in that environment.

```python
# This installs NumPy into the current Colab/Jupyter runtime from a code cell.
%pip install numpy
```

This command installs a package into the current notebook runtime. If the runtime is reset, you may need to install the package again. Also, your local PC's `.venv` and the Colab runtime are not the same space.

In summary, the two spaces are different.

- Colab runtime: an external execution environment outside the browser
- local virtual environment: an execution environment around the project folder on my computer

## Same Folder Name, Different Environments

Suppose two projects each have a `.venv`.

```text
project-a/.venv/
project-b/.venv/
```

Installing NumPy into the Python in `project-a/.venv` does not automatically install it in `project-b/.venv`. If both environments use their default creation settings and B has no NumPy, importing it in B’s Python raises `ModuleNotFoundError`.

The same folder name `.venv` denotes separate environments when the full paths differ. Compare the Python path printed by `sys.executable` with the path used in the installation command to identify the project environment where installation occurred.

## Checklist

- You can explain a virtual environment as a project-specific Python execution space.
- You can explain that the virtual-environment folder is an execution environment, not the manuscript or code of the project itself.
- You can explain a package as a bundle of code you bring into Python and use.
- You can explain that `pip` is a tool that installs packages.
- You can distinguish that `python -m pip install numpy` is a terminal command, while `import numpy as np` is Python code.
- You can explain that packages are installed into a specific Python execution environment.
- You can explain that the Colab runtime and a local virtual environment are not the same space.
- You can check `which Python environment am I using now?`, `are the required packages installed in that environment?`, and `are the installation command and the execution of the Python code looking at the same environment?`

## Sources and References

- Carl Meyer, [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, checked 2026-07-20. Used as design support for virtual environments having their own package set and Python executable while being isolated from system site-packages.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked 2026-09-08. Used to confirm creating and activating virtual environments with `venv`, and the separation of Python and package state inside an environment.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, checked 2026-07-20. Used to confirm the project-level flow of creating a virtual environment and installing packages with `python -m pip install`.
- Python Software Foundation, [Installing Python Modules](https://docs.python.org/3/installing/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm the basic roles of `pip`, `venv`, PyPI, and `python -m pip install`, and the context for preferring virtual environments over system-wide installation.
