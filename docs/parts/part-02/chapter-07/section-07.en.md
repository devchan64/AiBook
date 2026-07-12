# P2-7.7 Supplemental Learning: When Is Python Installation Needed?

> Section ID: `P2-7.7`
> Version: `v2026.07.12`

In P2-7.6, we looked at how to open a terminal and check the current location on Windows, macOS, and Linux. Now this question remains.

Do I absolutely need to install Python on my computer?

Here, we explain `the point at which Python installation becomes necessary`, `the first commands to check after installation`, and `the difference between installation and a virtual environment`.

This question follows naturally after looking at the big picture of the execution environment. Here, we organize the criteria for judging whether installation is needed now or later.

You do not always have to install it from the beginning. The earlier practice in this part can also be followed with browser execution environments such as Colab. But from a certain point onward, reasons arise to install Python on a local PC, create a virtual environment, and manage packages directly.

Here, rather than following installation buttons one by one, we focus on judging “when installation is needed,” “what should be checked after installation,” and “how installation and virtual environments should be distinguished.” Operating-system-specific screens can keep changing, and the Python distribution method can also change over time.

| Term | Meaning to establish first in this section |
| --- | --- |
| local installation | Preparing things so that the Python interpreter can be run directly on my computer. |
| Colab-first stage | A stage where you first build intuition for practice in the browser without installation. |
| `python --version` / `python3 --version` / `py --version` | The first checking commands to see which Python command in my environment is actually connected. |
| difference between installation and virtual environments | Installation prepares Python itself, while a virtual environment divides project-specific spaces on top of the installed Python. |
| official installation documentation | The reference material for checking the latest installation method and cautions by operating system. |

## Official Installation Manual Links

Link collection date: 2026-06-24

Installation screens and recommended methods can change over time. When actually performing an installation, do not look only at this section. Check the official documents below together with it.

- Overall installation and usage guide: Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }.
- Download page: Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }.
- Installation and execution on Windows: Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }.
- Installation and execution on macOS: Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }.
- Usage on Linux/Unix platforms: Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }.
- Virtual environments: Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }.

## Scope of This Supplement

Here, we cover the need for Python installation and the criteria for checking it. We do not cover the detailed step-by-step clicking process for each operating system, and checking environment mismatches after installation is recovered again in P2-7.9.

Here, we answer the following questions.

- When is Colab alone enough?
- When is Python installation on a local PC necessary?
- Why do installation methods look different on Windows, macOS, and Linux?
- Which commands should be used to check after installation?
- How are Python installation and virtual-environment creation different?
- When installation gets tangled, what should be checked first?

Here, we do not slowly follow each operating-system installation screen. We also do not go deeply into specific version installation, solving PATH issues, comparing Windows Store and python.org installation methods, Homebrew, pyenv, conda, Docker, or WSL setup. PATH and the post-installation checks that often block people are grouped again in the P2-7.9 supplementary section, and detailed comparison of installation methods is handled again when building a real project environment.

## Goal of This Supplement

- You can explain the difference in roles between Colab and local Python installation.
- You can judge when local installation is needed.
- You can explain that after installation, you should check with `python --version`, `python3 --version`, or `py --version`.
- You can explain that Python installation and virtual-environment creation are not the same thing.
- You can explain that operating-system-specific installation guidance should be rechecked against official documentation at the time of writing.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| Local installation is not absolutely necessary from the very beginning | Because small practice can start with Colab alone | Distinguish the roles of Colab and local installation |
| Local installation is the act of building the base for running the Python interpreter on my computer | If you see installation, virtual environments, and package preparation as one lump, judgment becomes blurry | You should be able to explain what installation is preparing |
| After installation, the first thing to check is the version and the execution command | Installation success and command-connection success are not the same thing | You should be able to explain the purpose of `python --version`-type checks |

## The Stage You Can Start with Colab

In early learning, Colab is often enough.

- running simple Python code
- checking NumPy array calculations
- handling small table data
- quickly drawing graphs
- following example code from the book cell by cell

Because Colab runs in the browser, it lets you postpone Python installation issues. That is a major advantage because it lets you first build the sense that “the code runs” before meeting installation, PATH, operating-system permissions, and terminal differences.

But Colab is not your own computer. The runtime is provided by an external service, the session can be reset, and it is hard to guarantee that files and package state will keep being preserved. So as learning moves to the next stage, the need for local installation grows.

## The Point Where Local Installation Becomes Necessary

The point when you need to install Python on a local PC is not “the first day you start learning Python,” but when you need to manage the execution environment directly.

For example, local installation may become necessary in the following situations.

- You need to run `.py` files directly on your computer.
- You need to manage multiple files together inside a project folder.
- You need to read and write data files from local folders.
- You need to run an example project received through Git.
- You need to create virtual environments and separate packages by project.
- You want to depend less on internet connection or the Colab runtime state.
- You need to use an editor, terminal, test tools, and document build tools together.

By contrast, Colab may still be enough at the following stage.

- You are checking one or two lines of calculation.
- You are running small code cells.
- Understanding concepts matters more than installation.
- You do not need to save results or manage project structure.

Therefore, here you first build the sense of execution with Colab, and later, when moving to project-level practice on a local PC, you think about Python installation more seriously.

## Installation Is the Act of Preparing the Python Interpreter

Python installation is the act of preparing the Python interpreter on my computer. The official Python documentation separately guides platform-specific Python environment setup, interpreter execution, and information that makes work easier.

When people say installation was done, it usually means the following has become possible.

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

## Check the Version First After Installation

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

Keep the following questions.

- Does `python` run?
- Does `python3` run?
- If on Windows, does `py` run?
- Is the printed version not too different from the book's examples?
- After turning on a virtual environment, does the same command still point to the same Python?

If you get blocked here, before editing Python code, you should first suspect an installation or command-connection problem.

## On Windows, You May Encounter Python Install Manager

The official Python Windows documentation explains that unlike most Unix systems, Windows does not include a system-supported Python installation by default. It says Python can be obtained from several distributors, and that to use the CPython team's distribution, you can use Python Install Manager.

Here, remember the following criteria.

- Windows may not have a reliable system Python you can assume exists.
- Python can be installed through the python.org download page or through Microsoft Store.
- After installation, check whether the `python` and `py` commands work.
- The official documentation recommends creating a virtual environment for each project.

The common problem on Windows is “I installed it, but the terminal cannot find the command.” In this case, it may not be a Python-code problem but an installation path or PATH-setting problem. Here, we do not go as far as directly editing PATH. How to read PATH and environment variables is revisited in the P2-7.8 supplementary section, and the post-installation checking order is grouped again in the P2-7.9 supplementary section. Here, we only go as far as checking the Troubleshooting section of the official documentation or rechecking the installation method.

## On macOS, Distinguish python.org Installation from Other Distributions

The official Python macOS documentation explains that there are several ways to get and install Python on macOS, and that there may be distributions other than the installer package provided on python.org. Current supported Python versions provide macOS installer packages on python.org.

Here, remember the following criteria.

- macOS may contain Python-related components used by system tools, so do not modify the system area carelessly.
- For learning Python, use the python.org installer package or another well-known distribution method.
- In the terminal, people often check `python3 --version` first.
- Even after installation, it is safer to separate project practice with virtual environments.

The macOS documentation explains that running scripts in the terminal and running them from Finder can differ. Running them while checking the current folder in the terminal is more transparent.

## On Linux, It May Already Be Installed

The official Python Unix-platform documentation explains that Python is preinstalled in most Linux distributions, and even when it is not, it is provided as a package.

Here, remember the following criteria.

- On Linux, `python3 --version` may already work.
- Python is often managed through the distribution's package manager.
- System Python may be used by operating-system tools, so do not delete or modify it carelessly.
- For project practice, it is safer to create a virtual environment and separate it.

In Linux materials, you may see commands like `sudo apt install python3`. But the package manager and package names can differ by distribution. Therefore, Linux installation commands should be checked against the official documentation of your own distribution.

## Python Installation and Virtual-Environment Creation Are Different

Python installation and virtual-environment creation are not the same thing.

| Category | What it does | Example |
| --- | --- | --- |
| Python installation | Prepares the Python interpreter on the computer | python.org installation, OS package installation |
| virtual-environment creation | Creates a Python execution space for a particular project | `python -m venv .venv` |
| package installation | Prepares external packages in that environment | `python -m pip install numpy` |

The official Python `venv` documentation explains that when a virtual environment is activated, the path is prefixed so that the Python interpreter from that environment is run. It also warns that virtual environments should be recreatable when needed, and that packages should be reinstallable using records such as `requirements.txt`.

Here, distinguish the flow like this.

1. Install Python.
2. Move to the project folder.
3. Create a virtual environment.
4. Activate the virtual environment.
5. Install the needed packages.
6. Run the Python code.

Here, we do not make you memorize the operating-system-specific activation commands in step 4. Activation commands can look different depending on Windows, macOS, Linux, and the type of shell. For now, remember the direction that “one installed Python is not shared unchanged by every project; instead, you create an environment for each project.”

## What to Check First When Installation Gets Tangled

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

## Cases And Examples

### Case 1. Until When Is Colab Enough, and From When Is Local Installation Needed?

Suppose a learner has followed examples only in Colab so far. But now a situation appears where a project with several `.py` files must be downloaded and run from a local folder. At that point, the learner first asks `do I really need installation now?` and `can't I just upload it to Colab?`

In the beginning, Colab may have been enough. But if the project-folder structure must be preserved, data files must be read locally, virtual environments must be separated, and package versions must be managed directly, then local Python installation becomes necessary.

The role of this section is not to list installation buttons, but to make the reader judge `the point at which installation is needed`. In other words, it gives a criterion for separating `is a browser runtime still enough?` from `must I now manage the execution environment directly on my own computer?`

A checkable result can be seen immediately with commands after installation. If one of `python --version`, `python3 --version`, or `py --version` actually runs the local interpreter, and virtual-environment and package installation can then continue, the learner is ready to move from Colab to a local environment.

## Checklist

- Can you explain the difference in roles between Colab and local Python installation?
- Can you judge the point at which local installation becomes necessary?
- Can you explain that after installation, you should check with `python --version`, `python3 --version`, or `py --version`?
- Can you explain that Python installation and virtual-environment creation are not the same thing?
- Can you explain that operating-system-specific installation guidance should be rechecked against official documentation at the time of writing?
- When installation gets tangled, can you separate `Python code error` from `execution-environment error`?

## Sources and References

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [Download Python](https://www.python.org/downloads/){: target="_blank" rel="noopener noreferrer" }, Python.org, checked on 2026-06-24.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [Using Python on macOS](https://docs.python.org/3/using/mac.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
