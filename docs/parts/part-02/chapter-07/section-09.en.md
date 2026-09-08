# P2-7.9 Supplementary Learning: Checking Local Python Environment Problems

> Section ID: `P2-7.9`
> Version: `v2026.09.08`

A missing `python` command and a failed `import numpy` occur at different points. The former requires checking how the shell finds commands; the latter requires checking packages in the running Python. Identical Python versions can belong to different virtual environments, so compare executable paths too.

## Error Messages and What to Check

| Message or situation | What to check |
| --- | --- |
| `python: command not found` | Command name, installation, and PATH |
| `ModuleNotFoundError: No module named 'numpy'` | NumPy installation in the current Python |
| `FileNotFoundError` | Working directory and data path |
| `Permission denied` | Destination and access permissions |
| `SyntaxError` | Python syntax; whether a shell command was entered into Python |

## The Python Command Being Run

Check the version of the Python command used in the terminal.

```bash
python --version
```

On macOS/Linux, `python3 --version` may work; on Windows, `py --version` may work depending on installation. One failure does not prove that no interpreter exists.

PATH is the directory list the shell searches for executable files. An installed Python may not be invoked because of the command name, PATH, or execution aliases. For operating-system-specific installation and command checks, see the official links in [Installing Python](section-07.en.md).

## The Actual Interpreter and Working Directory

Run this code in the notebook kernel or script environment where the error occurred. It prints the current Python executable, environment path, and working directory.

```python
import os
import sys

print("Python:", sys.executable)
print("Environment:", sys.prefix)
print("Virtual environment:", sys.prefix != sys.base_prefix)
print("Working directory:", os.getcwd())
```

In a standard `venv`, `sys.prefix` differs from `sys.base_prefix`. This directly checks the environment of the running Python instead of relying on memory of activation. An editor or notebook may select a different interpreter from the terminal.

## Different Virtual Environments with the Same Version

The following illustrates outputs from Python in two different projects.

| Item | Environment used for installation | Environment used for the example |
| --- | --- | --- |
| Python version | 3.12.3 | 3.12.3 |
| Executable | `/home/user/project-a/.venv/bin/python` | `/home/user/project-b/.venv/bin/python` |
| NumPy | Installed | Not installed |

The versions match, but the paths identify separate environments. Installation can succeed in A while `import numpy` fails in B. To run project B, install the required packages in B’s Python. Different paths do not always indicate an error; what matters is whether the selected environment meets the project’s requirements.

## pip and Package Locations

In a terminal with the intended Python selected, run:

```bash
python -m pip --version
python -m pip show numpy
```

The first command shows pip’s version and installation location. If NumPy is installed, the second shows its version and `Location`; otherwise, it reports that the package was not found.

`python -m pip` runs pip using the Python specified at the start of the command. Run the actual code with the same Python to use that installation. See [Installing and Running with the Environment’s Python](section-04.en.md) for directly specifying its path.

If the required NumPy is absent, install it with the same Python.

```bash
python -m pip install numpy
```

Running this code in that environment prints NumPy’s version and the location of the imported file.

```python
import numpy as np

print("NumPy:", np.__version__)
print("File:", np.__file__)
```

If an installation list is provided, use `python -m pip install -r requirements.txt` to prepare the project requirements instead of installing packages individually.

## Permission Errors and Missing Packages

Installing packages into a system location can fail due to missing write permissions. Creating a virtual environment in the project folder and installing with its Python can prepare packages without changing system packages.

`Permission denied` concerns access permissions; `ModuleNotFoundError` means the running Python cannot find a module. For the latter, check whether installation occurred in another environment, was incomplete, or the imported name is wrong.

## Actions Based on Check Results

| Finding | Next action |
| --- | --- |
| No usable Python command | Check installation and operating-system-specific commands |
| The editor uses another project’s Python | Select the intended project interpreter |
| A required package is absent from the selected environment | Install with that Python’s pip |
| Packages are present but the data file is missing | Check file location, working directory, and input data preparation |
| Environment and input match but the error persists | Check the complete error message and required versions |

Keep these environment checks with the installation list, data, and execution-location records described in [Dependencies and Reproducibility](section-05.en.md), so later runs can be compared.

## Checklist

- You can distinguish missing-command errors from missing-package errors.
- You can explain that the same Python version may have different executable paths.
- You can inspect the current environment with `sys.executable` and `sys.prefix`.
- You can compare the Python used for installation with the Python running the code.
- You can check package installation and usage locations with `pip show` and import results.
- You can use error messages to separate command, environment, permission, and file problems.

## Sources and References

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used as background for the local environment checking order by confirming the documentation structure for platform-specific Python setup and interpreter invocation.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that Python execution commands and installation methods on Windows have separate official guidance.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that Python execution commands and installation paths on Unix/Linux can differ by environment.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to support checking virtual-environment activation together with package installation location.

- Python Software Foundation, [sys — System-specific parameters and functions](https://docs.python.org/3/library/sys.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-09-08. Source for sys.executable, sys.prefix, and sys.base_prefix when checking interpreter and virtual-environment paths.
