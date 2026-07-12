# P2-7.4 Virtual Environments and Packages

> Section ID: `P2-7.4`
> Version: `v2026.07.12`

In P2-7.3, we looked at ways to run Python code. Now we move to a slightly more realistic problem.

For example, you often run into situations like these.

- Python runs, but it says NumPy is missing.
- It worked yesterday, but today the package version is different and the result has changed.
- It works on my computer, but it does not work on someone else's computer.

These problems are not solved by Python syntax alone. You need to look at both the space where the code runs and the packages installed in that space.

Here, we explain the relationship among `virtual environment`, `package`, `pip`, and `import`. Even when later sections revisit dependency lists or environment-checking steps, you should still read them based on the explanation here about which Python space installation and usage must be connected to.

Rather than learning the entire world of Python distribution and packaging, this section focuses on understanding why practice changes when you separate execution environments by project. If you understand the difference among virtual environments, packages, installation, and `import` here, that naturally carries forward when later sections cover dependency lists, reproducibility, and team collaboration environments, including what to record and what to install again.

| What to establish in this section | Question that follows immediately | Where it is used again later |
| --- | --- | --- |
| The idea that a virtual environment is a project-specific execution space | This leads to dependency lists and reproducibility in P2-7.5. | It is used again later whenever you interpret environment conflicts in local Python practice. |
| The idea that `pip install` and `import` are different stages | P2-7.9 examines errors in more detail when the installation environment and execution environment do not match. | It repeats in package installation errors, Colab vs. local differences, and library setup contexts. |
| The idea that the Colab runtime and a local `.venv` are different spaces | P2-7.6 and P2-7.7 add operating-system-specific installation and activation steps. | It becomes the basis for reproducing practice environments and guiding team collaboration after Part 3. |

| Term | Meaning to establish first in this section |
| --- | --- |
| virtual environment | A Python execution space separated by project. |
| package | A bundle of code you can bring into Python and use. |
| `pip` | A tool that installs packages. |
| `import` | A statement that loads an already prepared package into Python code. |
| `.venv` | A representative local virtual-environment directory name placed inside a project folder. |

## Scope of This Section

This section explains the concepts of virtual environments and packages. It does not go deeply into operating-system-specific activation commands, Python installation methods, PATH settings, or permission issues. Those environment-checking steps are gathered again in the P2-7.9 supplementary section. A detailed explanation of saving dependency lists and recording versions is covered again in P2-7.5.

Here, we answer the following questions.

Here, we answer the following questions.

- Why is a virtual environment necessary?
- What is a package?
- What does `pip` do?
- Why are installation and `import` different?

The problem of saving dependency lists and restoring the same environment on another computer is covered in P2-7.5.

| If this is your current symptom | Where to go first | Otherwise, what to hold onto in this section |
| --- | --- | --- |
| You are not even sure whether you first need to install Python on your local PC | P2-7.7 supplementary section | First understand that a virtual environment is a device that separates project-specific execution spaces after installation |
| You ran `pip install`, but `import` still fails | P2-7.9 supplementary section | For now, first keep the criterion that installation and execution may be looking at different environments |
| You only want to know why a package like NumPy ends up being needed separately for each project | Keep reading this section | First check why virtual environments reduce package conflicts |

## Goal of This Section

- You can explain a virtual environment as a project-specific Python execution space.
- You can explain a package as a bundle of code you bring into Python and use.
- You can explain `pip` as a tool that installs packages.
- You can explain that `pip install` and `import` do different jobs.
- You can explain that different package versions may be needed for different projects even on the same computer.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| A virtual environment is a project-specific Python execution space | Because each project may need different tool versions | Understand the virtual environment as a separation device that reduces conflicts |
| Installation and `import` are different stages | Installation is preparation, and `import` is the act of actually loading something inside code | You should be able to explain the difference in roles between terminal commands and Python code |
| The most common mistake is that the environment where you installed something and the environment where you ran it are different | There can be multiple Python spaces even on one computer | You should be able to distinguish the problem type called an environment mismatch |

## Why Did Virtual Environments Become Necessary?

To someone learning Python for the first time, a virtual environment can look like a somewhat inconvenient device. But it is not just a habit. It took root to solve real problems that appeared as the Python ecosystem grew.

PEP 405 is the proposal to add `venv` to the Python standard library. The document was created in 2011 and targeted Python 3.3. Its motivation explains that third-party virtual-environment tools such as `virtualenv` were already widely used for dependency management, isolation, installing and using packages without system administrator privileges, and automated testing across multiple Python versions.

If you compress that background from a beginner's perspective, it comes down to this.

- Python packages became numerous: different projects started to need different external code.
- It was hard to modify the system Python carelessly: you could break the Python environment used by the operating system or by other programs.
- There were many cases where installation had to happen without administrator privileges: in personal projects or server accounts, you often could not freely change the whole system.
- People had to test multiple projects and Python versions: one global installation space made conflicts hard to avoid.

So a virtual environment is not a device for making the learning process more complicated. It is a tool that came from the historical need to separate Python and packages by project in order to reduce conflicts.

## Why Is a Virtual Environment Necessary?

It may look as if one Python installation is enough. It is easy to think, "Install Python, install the packages you need, run the code, and that is it."

But as projects increase, problems appear.

For example, project requirements can differ like this.

- Project A was written for `numpy 1.x`.
- Project B was written for `numpy 2.x`.
- If you mix them in the same space, one side may break.

A virtual environment is a way to divide Python execution space by project to reduce these conflicts. The official Python documentation explains that `venv` creates lightweight virtual environments and that each environment can have its own independent set of Python packages.

Here, we understand a virtual environment as a `project-specific Python execution space`.
- Virtual environment for project A: install the packages needed for project A.
- Virtual environment for project B: install the packages needed for project B separately.

## A Virtual Environment Is Not Project Code

A virtual environment is the surrounding environment used to run a project. It is different from the manuscript or code of the project itself.

For example, inside a project folder you may see a folder named `.venv`. This folder is a local execution environment that contains the packages needed to run Python or build documents. It is not the body's source files or the code itself.

That is why virtual-environment folders are usually not committed to Git. The official Python documentation also explains that virtual environments can usually be created with a name such as `.venv` inside a project directory and are not typically placed under source control.

So people usually separate things like this.

- What to commit: manuscript files, code, configuration files, example files
- What not to commit: the virtual-environment folder created on my computer

Rather than sharing the virtual environment itself, it is safer to record which packages are needed and make them installable again. That problem continues in P2-7.5, which covers dependency and reproducibility.

## A Package Is a Bundle of Code You Bring In and Use

A package is a bundle of code distributed so that you can bring it into Python and use it. Tools such as NumPy, Pandas, and Matplotlib belong here.

Here too, keep three layers distinct.

- Python: the language and the execution program
- package: a bundle of code you bring into Python and use
- package repository: a place where packages can be downloaded

The Python Packaging User Guide introduces a flow that uses `pip` and `venv` to install packages inside a virtual environment. What matters here is that installing a package and loading it in code are different actions.

## `pip install` Means Installation, and `import` Means Use

The following command is a terminal command that installs a package.

```bash
python -m pip install numpy
```

This command is not a statement you write inside a Python code file. It is a command you run in the terminal. As in P2-7.3, `python -m` is a way to ask Python to run a specific module. Here, it runs `pip` to install NumPy.

By contrast, the following is Python code.

Problem situation: We check how a package is actually loaded inside Python code, in contrast with installation.
Input: the statement `import numpy as np`.
Expected output: there is no printed output, but NumPy becomes ready to use in the current Python code.
Concept to check: `pip install` is installation, while `import` is the stage where an already installed package is used inside code.

```python
import numpy as np
```

This code is a statement that loads already installed NumPy so that it can be used in the current Python code.

You should not mix the two statements.

| Purpose | Example | Where to enter it |
| --- | --- | --- |
| Package installation | `python -m pip install numpy` | Terminal |
| Package use | `import numpy as np` | Python code |

Here, we distinguish them like this.

- `install`: prepare the package in my execution environment
- `import`: use that package in the current Python code

## The Place Where You Installed It and the Place Where You Run It Must Match

There is an error you encounter often.

An error beginners frequently see is the situation, "I definitely installed it, but Python says it is not there."

At that point, you have to separate "where did I install it?" from "where am I running it?"

For example, the place where you installed it and the place where you ran it may differ like this.

- You installed it in the system Python, but you are running it with the virtual-environment Python.
- You installed it in virtual environment A, but you are running it in virtual environment B.
- You installed it in Colab, but you are running it on your local PC.

Packages are not installed abstractly "somewhere on the computer." They are installed into a specific Python execution environment. That is why, when you use a virtual environment, you should use the same virtual environment both when installing packages and when running the code.

## Looking at the Flow of a Virtual Environment Like a Diagram

Actual commands can differ depending on the operating system and the project situation. But the overall flow is usually similar to the following.

The actual flow is usually easiest to understand in the following order.

1. Move to the project folder.
2. Create a virtual environment.
3. Switch the virtual environment into an in-use state.
4. Install the necessary packages.
5. Run the Python code.

When expressed as terminal commands, you often see a flow similar to this.

Problem situation: We look at the whole flow from creating a virtual environment to installing packages and running a script.
Input: three command lines for creating `venv`, installing with `pip`, and running `python`.
Expected output: the order of creating a project-only environment, preparing packages, and running code becomes visible.
Concept to check: the use of virtual environments and packages should be understood as one continuous workflow.

```bash
python -m venv .venv
python -m pip install numpy
python example.py
```

There is an important omission here. In actual practice, you may need a step to activate the virtual environment. Activation commands look different on Windows, macOS, and Linux, so we do not memorize them here. The detailed procedure is covered in the P2-7.6 supplementary section, and why activation status and installation environments so often get crossed is revisited in the P2-7.9 supplementary section.

Here, keep only the following perspective.

- You created a virtual environment: that means you created a Python space dedicated to the project.
- You installed packages: that means you prepared tools inside that space.
- You used `import`: that means you loaded those tools inside Python code.

## Do You Really Need to Understand Virtual Environments in Colab?

Colab is a notebook environment that runs in a browser. In early learning, you can run code without knowing Python installation or virtual environments. That is why this book allowed Colab in earlier practice.

But even in Colab, package installation and execution-environment issues do not disappear.

Problem situation: We check that even in Colab, you may have to install packages directly into the current runtime.
Input: the `%pip install numpy` command in a code cell.
Expected output: NumPy is installed into the current Colab runtime.
Concept to check: Colab is convenient, but it is a separate execution space different from a local virtual environment.

```python
%pip install numpy
```

This command installs a package into the current notebook runtime. If the runtime is reset, you may need to install the package again. Also, your local PC's `.venv` and the Colab runtime are not the same space.

In summary, the two spaces are different.

- Colab runtime: an external execution environment outside the browser
- local virtual environment: an execution environment around the project folder on my computer

Colab may be enough at the beginning. But if you want to maintain a project for a long time or reproduce the same code with someone else, you need to understand virtual environments and dependency management.

## Case Study

### Case 1. Why `import` Fails Even Though NumPy Was Installed

Suppose a learner runs `python -m pip install numpy` in the terminal and then immediately runs an example file. But an error still appears at `import numpy as np`. People usually think first, "Did installation fail?" or "Did the `pip` command lie?"

But in cases like this, the cause often appears when the environment where the package was installed and the environment where the code was run are different, rather than in installation itself. It may have been installed into the system Python while the code was run with the virtual-environment Python, or the learner may have run the code while another project's virtual environment was active.

The key point of this section is to read `virtual environment`, `package`, `pip install`, and `import` as separate stages. Installation is preparation, and `import` is the act of actually loading something in the Python environment currently running.

The confirmable result appears when you check which Python environment is being used in the same terminal. If the installation command succeeded but `import numpy` fails only in the current virtual environment, you can explain that the problem lies in environment separation rather than in the package name.

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

- Carl Meyer, [PEP 405 – Python Virtual Environments](https://peps.python.org/pep-0405/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, checked on 2026-06-24.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, checked on 2026-06-24.
- Python Packaging Authority, [Installing Python Modules](https://docs.python.org/3/installing/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-06-24.
