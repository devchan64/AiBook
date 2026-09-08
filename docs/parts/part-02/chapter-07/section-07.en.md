# P2-7.7 Supplemental Learning: When Is Python Installation Needed?

> Section ID: `P2-7.7`
> Version: `v2026.09.08`

A hosted Colab runtime does not require Python on your computer. Running `.py` files or processing local files on your own computer requires a local interpreter. Python may already be installed, so first check execution commands and versions.

## Official Installation Manual Links

Link collection date: 2026-07-20

Installation screens and recommended methods can change over time. When actually performing an installation, do not look only at this section. Check the official documents below together with it.

- Overall installation and usage guide: Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- Download page: Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Installation and execution on Windows: Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- Installation and execution on macOS: Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Usage on Linux/Unix platforms: Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- Virtual environments: Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## Execution Location and Installation

| Criterion | Why it matters |
| --- | --- |
| Local installation is not absolutely necessary from the very beginning | Because small practice can start with Colab alone |
| Local installation is the act of building the base for running the Python interpreter on my computer | If you see installation, virtual environments, and package preparation as one lump, judgment becomes blurry |
| After installation, the first thing to check is the version and the execution command | Installation success and command-connection success are not the same thing |

## Hosted Colab Runtimes

In early learning, Colab is often enough.

- running simple Python code
- checking NumPy array calculations
- handling small table data
- quickly drawing graphs
- following example code from the book cell by cell

The browser handles code input and result display, while the hosted runtime executes Python code. These tasks can be done without installing Python locally.

Colab is not your own computer. Its runtime is provided by an external service, sessions can be reset, and persistent file and package state is not guaranteed.

## Tasks Requiring a Local Interpreter

Local Python is needed to perform these tasks on your own computer:

- Run `.py` files from a terminal or editor.
- Read local data files and save results on the same computer.
- Create project virtual environments and manage packages.
- Run Python calculations without an internet connection.

Having multiple files or a Git repository does not by itself require local execution. Projects and packages can also be managed in remote runtimes. The deciding factor is where the code will actually run, not the number of files.

## Python Installation and Command Setup

Python installation is the act of preparing the Python interpreter on my computer. The official Python documentation separately guides platform-specific Python environment setup, interpreter execution, and information that makes work easier.

Once installation, command setup, and required components are ready, the following become possible.

- You can run Python commands in the terminal.
- You can run `.py` files with Python.
- You can install packages through `pip`.
- You can create virtual environments.

But installation alone does not finish everything.

Even after installing Python, the following problems may remain.

- The `python` command may not work in the terminal.
- On macOS/Linux, you may need to use the `python3` command.
- On Windows, you may encounter the `py` command.
- Multiple versions of Python may be installed.
- If you do not use virtual environments, project-specific packages may get mixed together.

So right after installation, instead of stopping at “it was installed,” you must check “which command points to which Python?”

## Checking the Python Version for Each Command

Check the following command in the terminal.

```bash
python --version
```

On macOS or Linux, the following command may be more natural.

```bash
python3 --version
```

On Windows, depending on the Python installation method, you may encounter the following command.

```powershell
py --version
```

Even if one of these works, that does not mean the others necessarily work. What matters is checking which command in my environment runs the Python interpreter.

If no version is printed, check installation and command setup before the code. Different commands may print different versions, so choose the Python to use for the project.

## Windows Installation Options

The official Python Windows documentation explains that unlike most Unix systems, Windows does not include a system-supported Python installation by default. It says Python can be obtained from several distributors, and that to use the CPython team's distribution, you can use Python Install Manager.

Check the following for installation and execution.

- Windows may not have a reliable system Python you can assume exists.
- Python can be installed through the python.org download page or through Microsoft Store.
- After installation, check whether the `python` and `py` commands work.
- The official documentation recommends creating a virtual environment for each project.

If Python is installed but the command cannot be found, check the installation path, execution aliases, and PATH settings. The Troubleshooting section of the official Windows documentation lists checks for each installation method.

## macOS Installation Options

The official Python macOS documentation explains that there are several ways to get and install Python on macOS, and that there may be distributions other than the installer package provided on python.org. Current supported Python versions provide macOS installer packages on python.org.

Check the following for installation and execution.

- macOS may contain Python-related components used by system tools, so do not modify the system area carelessly.
- For learning Python, use the python.org installer package or another well-known distribution method.
- In the terminal, people often check `python3 --version` first.
- Even after installation, it is safer to separate project practice with virtual environments.

The macOS documentation explains that running scripts in the terminal and running them from Finder can differ. Running them while checking the current folder in the terminal is more transparent.

## Distribution Python on Linux

The official Python Unix-platform documentation explains that Python is preinstalled in most Linux distributions, and even when it is not, it is provided as a package.

Check the following for installation and execution.

- On Linux, `python3 --version` may already work.
- Python is often managed through the distribution's package manager.
- System Python may be used by operating-system tools, so do not delete or modify it carelessly.
- For project practice, it is safer to create a virtual environment and separate it.

In Linux materials, you may see commands like `sudo apt install python3`. But the package manager and package names can differ by distribution. Therefore, Linux installation commands should be checked against the official documentation of your own distribution.

## Interpreter, Virtual Environment, and Packages

Python installation and virtual-environment creation are not the same thing.

| Category | What it does | Example |
| --- | --- | --- |
| Python installation | Prepares the Python interpreter on the computer | python.org installation, OS package installation |
| virtual-environment creation | Creates a Python execution space for a particular project | `python -m venv .venv` |
| package installation | Prepares external packages in that environment | `python -m pip install numpy` |

The official Python `venv` documentation explains that when a virtual environment is activated, the path is prefixed so that the Python interpreter from that environment is run. It also warns that virtual environments should be recreatable when needed, and that packages should be reinstallable using records such as `requirements.txt`.

Prepare the project environment in this order.

1. Install Python.
2. Move to the project folder.
3. Create a virtual environment.
4. Activate the virtual environment or directly specify its Python path.
5. Install the needed packages.
6. Run the Python code.

## Checking Installation and Execution Environments

When Python installation gets tangled, do not jump straight to reinstalling. Check these things first.

- Which terminal did I open now?
- Where is the current working folder?
- Does `python --version` work?
- Does `python3 --version` work?
- If on Windows, does `py --version` work?
- Are multiple Python versions installed?
- Is a virtual environment currently turned on?
- Is the Python where packages were installed the same Python that is running the code?

The following situations are especially common.

- You installed packages into system Python, but you are running with virtual-environment Python.
- You installed packages into the virtual environment, but you are running after turning the virtual environment off.
- You assume that a package installed in Colab is also installed on the local PC.
- On Windows, `python` does not work, but `py` does.
- On macOS/Linux, `python` is missing or points to Python 2, while `python3` points to the real Python 3.

When reading error messages, you need the habit of separating “Python code error” from “execution-environment error.”

## Does One Missing Command Require Reinstallation?

Suppose a Linux terminal shows the following. The version number only illustrates the output format.

```text
$ python --version
bash: python: command not found
$ python3 --version
Python 3.12.3
```

This environment has no command named `python`, but it has an interpreter run by `python3`. Before reinstalling, you can run a script with `python3 example.py` or create a project environment with `python3 -m venv .venv`.

If none of the relevant Python commands is available and local execution is needed, follow the installation procedure for the operating system. Distinguishing one failed command from an absent interpreter avoids unnecessary reinstallation.

## Checklist

- You can explain the difference in roles between Colab and local Python installation.
- You can judge when local installation is needed.
- You can explain the purpose of `python --version`, `python3 --version`, and `py --version`.
- You can explain that Python installation methods may look different on Windows, macOS, and Linux.
- You can distinguish Python installation, virtual-environment creation, and package installation.
- You can explain that when an installation error occurs, the execution environment should be checked before the code.
- You can check `which command runs Python in my terminal`, `which Python version that command points to`, `whether I am ready to create a project-specific virtual environment`, and `whether the package-installation environment and code-execution environment are the same`.

## Sources and References

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm the documentation structure for platform-specific Python environment setup, interpreter invocation, and installation guidance.
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org, checked 2026-07-20. Used to confirm the latest Python download and operating-system-specific download entry points.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that Python installation and execution on Windows has separate official guidance.
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm the python.org distribution and post-installation package-use guidance on macOS.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that Linux/Unix installation paths can differ by operating system, such as distribution packages or source builds.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm that project-specific virtual environments may be created as a separate step from installing Python itself.
