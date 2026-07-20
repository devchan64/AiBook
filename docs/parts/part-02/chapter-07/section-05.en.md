# P2-7.5 Dependency and Reproducibility

> Section ID: `P2-7.5`
> Version: `v2026.07.20`

In P2-7.4, we looked at virtual environments and packages. Now one question remains.

Is installing packages enough?

It may look that way. But even when learning code gets only a little longer, the following problems appear.

- It runs on my computer.
- It does not run on someone else's computer.
- It ran yesterday.
- Today the package version changed and the result changed.
- It works in Colab.
- It does not work on the local PC.

This problem is related less to the code itself than to whether the execution environment can be rebuilt. That is why dependency and reproducibility have to be considered separately.

Here, we explain the basic distinctions among `dependency`, `reproducibility`, `requirements.txt`, and `version pinning`. Even when later sections revisit example projects or collaboration environments, you should reconnect them based on the explanation here about what must be recorded together with the code.

Rather than learning the Python package distribution system in depth, this section focuses on understanding what must be recorded together if you want to run the same code again later. If you establish the roles of dependencies, requirements files, and version records here, then later, in team collaboration or long-term practice, you will be able to judge more accurately whether `having only the code is enough`.

| What to establish in this section | Question that follows immediately | Where it is used again later |
| --- | --- | --- |
| The idea that dependency and reproducibility are management targets separate from the code | This leads to the actual order of local environment checks in P2-7.9. | It is used again later in all practice and shared team environments. |
| The role of `requirements.txt` and version records | This leads to questions about operating-system-specific installation and Python version checks. | It repeats in rerunning examples, handing projects over, and collaboration guidance after Part 3. |
| The idea that reproducibility problems do not disappear even in Colab | This leads to a standard for comparing local and cloud environments. | It becomes the basis for long-running experiments, rerunning reports, and validating projects in Part 6. |

| Term | Meaning to establish first in this section |
| --- | --- |
| dependency | External packages and execution conditions that my code relies on. |
| reproducibility | The property of leaving conditions so that the same code can be run again later. |
| `requirements.txt` | A representative file that records the list of required packages and their versions. |
| version pinning | A method of reducing environment differences by specifying particular package versions. |
| environment record | Notes needed for rerunning, such as the Python version, package list, and execution location. |

## Goal of This Section

- You can explain dependency as the external packages needed for my code to run.
- You can explain reproducibility as the condition that allows the same code to be run again later.
- You can explain that `requirements.txt` is a file containing the list of packages to install.
- You can explain the necessity and limits of version pinning at an introductory level.
- You can understand that “it works on my computer” is not a sufficient explanation.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| Dependency is the external packages and execution conditions that the code relies on | It explains why looking at the code alone is not enough for execution | If you see `import`, you should be able to connect it to which external package is needed |
| Reproducibility is the act of leaving conditions so that the same code can be run again later | Learning and collaboration do not end after running something once | Understand that environment conditions must also be left together with the code |
| A requirements file records the needed package list and version range | It becomes the starting point when someone else rebuilds the environment | You should be able to explain the role of `requirements.txt` in one sentence |

## Dependency Is an External Condition That My Code Relies On

Dependency is an external condition that my code needs in order to run. In Python practice, package dependencies are usually the first kind you encounter.

For example, the following code needs NumPy.

Problem situation: We check the simplest example of which external package a piece of code depends on.
Input: code that creates a NumPy array and prints the mean.
Expected output: if NumPy is installed, the mean value `2.0` is printed.
Concept to check: when you see `import numpy as np`, that means this code depends on the NumPy package.

```python
import numpy as np

# values is a small array used to check both NumPy installation and mean calculation.
values = np.array([1, 2, 3])
print(values.mean())
```

Python alone is not enough for this code. NumPy must be installed.

- My code: uses `import numpy as np`.
- Required external package: NumPy.
- Therefore, NumPy is a dependency of this code.

Dependencies can be divided into direct dependencies and indirect dependencies.

- direct dependency: a package that I use directly in my code
- indirect dependency: another package that a package I installed internally needs

You do not need to memorize this whole structure. But you do need the sense that “behind one package I installed, several other packages may come along together.”

## Example: The Same Code Fails in Some Places

Think about the following situation. You downloaded an example from the book and ran a Python file that calculates a mean.

Problem situation: We see that the same mean-calculation code can work in Colab but fail on a local PC because a package is missing.
Input: short code that calculates a mean with a NumPy array.
Expected output: in an environment where NumPy is prepared, the mean is printed, but in an environment without it, the code may fail at the import stage.
Concept to check: confirm that you have to separate code problems from execution-environment problems.

```python
import numpy as np

# scores is the score data used to calculate a mean in the example environment.
scores = np.array([82, 91, 77, 88])
print(scores.mean())
```

It runs in Colab. But on a local PC terminal, you may get an error like this.

```text
ModuleNotFoundError: No module named 'numpy'
```

This error does not mean the mean calculation code is wrong. It means NumPy is not prepared in the current Python environment.

At this point, it becomes easier to find the cause if you divide the problem like this.

- What the code requires: NumPy
- What is missing in the current environment: the NumPy package
- Direction of the solution: install NumPy into the Python environment currently in use, or look at the list of required packages and rebuild the environment

That is why the memory that “I installed the package” is not enough. You must leave which environment, which package, and which version were installed.

## Reproducibility Is the Condition That Lets You Run It Again Later

Reproducibility is the property that lets you expect the same behavior when you run the same code again under the same conditions.

In AI and data practice, reproducibility is important. At the stage of reading mathematical explanations, it may not look like a big problem, but the moment you run code, environment differences can change the result.

- The Python version may differ.
- The package versions may differ.
- The operating system may differ.
- The data file location may differ.
- The Colab runtime may have been reset.

Therefore, if you want to share practice, giving only the code may not be enough. You also need to leave “which environment did I run this in?”

## Example: Opening a Learning Notebook Again One Month Later

In AI learning, it is common to open again “the notebook I ran today” one month later.

On the day it was run, the following conditions were in place.

- The Colab runtime was active.
- `numpy`, `pandas`, and `matplotlib` were already installed.
- The data file had been uploaded into the `/content/data/` folder.
- The code cells were run in order from top to bottom.

One month later, the situation may be different.

- The Colab runtime was reset, so packages installed manually are gone.
- The data file was not uploaded again.
- Execution started from a middle cell, so variables created earlier are missing.
- The default package versions changed.

If you immediately decide “the code is wrong,” you can miss the cause. First, you have to check whether the execution conditions were rebuilt. Reproducibility is a record-keeping habit that makes this check easier.

## A Requirements File Is a Way to Leave an Installation List

The pip documentation explains requirements files as files containing a list of installation items to pass to `pip install`. The common name is `requirements.txt`.

For example, you can make a file like the following.

```text
numpy
pandas
matplotlib
```

And then install with the following.

```bash
python -m pip install -r requirements.txt
```

Here, understand it like this.

- `requirements.txt` is not Python code.
- It is not a terminal command either.
- It is a file where the list of packages to install is written down.

If this file exists, another person can more easily understand “which packages does this project require?”

## Example: Handing a Small Practice Folder to Someone Else

Suppose a small practice folder is organized like this.

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py` reads a CSV file and calculates the mean.

Problem situation: We check which packages are needed by a small practice program handed to another person.
Input: a script that reads a CSV with `pandas` and calculates the mean.
Expected output: if the required environment is prepared, the average score is printed.
Concept to check: if you hand over only the code, it is hard to know which packages are needed, so a requirements file is needed together with it.

```python
import pandas as pd

# Read scores.csv and calculate the mean of the score column in the table data.
scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

If you hand over only this file, the receiver cannot immediately know whether `pandas` is needed. So you write the necessary package in `requirements.txt`.

```text
pandas
```

The receiver can move into the folder and prepare the necessary package with the following command.

```bash
python -m pip install -r requirements.txt
```

The important point in this example is that `requirements.txt` is not the file that runs the code. It is the file that leaves the list of external packages the code relies on.

## Pinning a Version Means Narrowing the Range

Packages change over time. There is no guarantee that the NumPy you install today will be the same version as the NumPy you install a year later.

That is why you can write down versions.

```text
numpy==2.0.0
pandas==2.2.2
matplotlib==3.9.0
```

`==` means that a specific version is being specified. This method can be called version pinning.

The pip user guide explains that the result of `pip freeze` can be placed into a requirements file and used for repeatable installs. At that point, the file records the packages and versions that were installed when `pip freeze` was run.

For example, you may encounter the following command.

```bash
python -m pip freeze > requirements.txt
```

And in another environment, you can install like this.

```bash
python -m pip install -r requirements.txt
```

But pinning versions does not make every problem disappear. The operating system, Python version, hardware, and package distribution state can still matter. Here, understand it as `the starting point for increasing reproducibility`.

For example, when making learning materials, you can think about the difference between the following two methods.

- `pandas`: the latest version may be installed, so the environment may change over time.
- `pandas==2.2.2`: because it requires a specific version, it can be matched more closely to the environment from that time.

When you first start studying, you do not need to pin every package strictly. But for code such as book examples, class materials, or team projects that another person must run again, the importance of version records becomes greater.

## Requirements Files and Project Configuration Files Have Different Roles

The Python Packaging User Guide distinguishes between requirements files and a package's installation requirements. Here, the following difference is worth remembering.

- requirements file: a list of things to install in order to build a specific environment
- project configuration file: a file that distributes a package or describes project metadata

This part's practice does not deal with complex package distribution structures. Therefore, understand `requirements.txt` as “the installation list for rebuilding the practice environment.”

## Reproducibility Does Not Disappear in Colab Either

Colab is easy to start with. But reproducibility problems do not disappear.

The Colab runtime can be reset. At that point, packages installed there can disappear. Also, the default package versions provided by Colab can change over time.

That is why it is useful to leave the required installation commands at the top of the notebook or to build the habit of recording which environment it was run in.

Problem situation: When you open a Colab notebook again, you want to be able to prepare the needed packages first.
Input: a `%pip` command to install NumPy, pandas, and matplotlib.
Expected output: the three packages are installed into the current Colab runtime.
Concept to check: even in Colab, if you want to improve reproducibility, you need to leave both the necessary installation commands and environment notes.

```python
# Install the main packages needed to reproduce the notebook in the current code-cell environment.
%pip install numpy pandas matplotlib
```

This command is convenient, but in the long run it is safer to leave the package versions and the execution date together.

For example, at the top of a notebook, you can leave a short note like this.

- Date created: 2026-07-20
- Execution environment: Google Colab
- Main packages: numpy, pandas, matplotlib
- Things to check when rerunning: whether the runtime was reset, whether the data file was uploaded

Even a note at this level can reduce the time spent repeatedly tracing the same error later.

## Minimum Information to Leave in a Practice Project

You do not need to create a perfect reproducible environment all at once. But it is a good habit to leave the following information.

- Which Python version was used to run it
- Which packages are needed
- What the versions of important packages are
- Which folder the code is run from
- Where the data files are supposed to be
- Whether the environment is Colab or a local PC

If you have this information, it becomes easier to narrow down the cause when an error happens later.

## Case Study

### Case 1. Why Does a Notebook Opened Again One Month Later Suddenly Stop Working?

Suppose a learner opens again a data analysis notebook that ran well last month. At that time, the graphs displayed properly and the CSV loaded correctly, but this time both package errors and file path errors appear together.

People can easily think, “Did the notebook file get broken?” But in reality, it is more likely that the Colab runtime was reset, the package versions changed, or the data file location became different. In other words, it is not primarily the code itself, but the failure to reproduce the execution conditions.

The `dependency`, `reproducibility`, `requirements.txt`, and `version pinning` discussed in this section are devices for reducing this kind of failure. If code is to be runnable again, then which packages and which versions it expected must also be left together.

The confirmable result can be judged by whether an installation list and version record exist. If packages were left only to memory without `requirements.txt`, reproducibility is weak. By contrast, if the necessary packages and versions are recorded, a starting point exists for rebuilding the same environment.

## Checklist

- You can explain dependency as the external packages needed for my code to run.
- You can explain reproducibility as the condition that lets the same code be run again later.
- You can explain that `requirements.txt` is a file containing the list of packages to install.
- You can explain that `python -m pip install -r requirements.txt` is the command that installs packages based on a requirements file.
- You can explain that `pip freeze` can be used to record the packages and versions installed in the current environment.
- You can explain that version pinning can improve reproducibility, but does not solve every problem.
- You can check which external packages the code relies on, in which Python environment they are installed, and whether there is a record to rebuild that environment later.

## Sources and References

- Python Packaging Authority, [User Guide](https://pip.pypa.io/en/stable/user_guide/){: target="_blank" rel="noopener noreferrer" }, pip documentation v26.1.2, checked 2026-07-20. Used to confirm `python -m pip`, package installation, requirements files, and the use of `pip freeze` for repeatable installs.
- Python Packaging Authority, [pip freeze](https://pip.pypa.io/en/stable/cli/pip_freeze/){: target="_blank" rel="noopener noreferrer" }, pip documentation v26.1.2, checked 2026-07-20. Used to confirm that it outputs installed packages in requirements format for the current environment.
- Python Packaging Authority, [install_requires vs requirements files](https://packaging.python.org/en/latest/discussions/install-requires-vs-requirements/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, checked 2026-07-20. Used to confirm the distinction between dependency metadata for project distribution and requirements files for reproducing an execution environment.
