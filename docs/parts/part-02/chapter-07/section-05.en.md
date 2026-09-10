# P2-7.5 Dependency and Reproducibility

> Section ID: `P2-7.5`
> Version: `v2026.09.08`

Rerunning the same code also requires matching packages, Python version, data files, and execution location. Dependencies are external elements the code requires; reproducibility means being able to verify the same behavior or results after recreating the execution conditions.

| Term | Meaning to establish first in this section |
| --- | --- |
| dependency | External packages and execution conditions that my code relies on. |
| reproducibility | The property of leaving conditions so that the same code can be run again later. |
| `requirements.txt` | A representative file that records the list of required packages and their versions. |
| version pinning | A method of reducing environment differences by specifying particular package versions. |
| environment record | Notes needed for rerunning, such as the Python version, package list, and execution location. |

## Recording Code and Execution Conditions

| Criterion | Why it matters |
| --- | --- |
| Dependency is the external packages and execution conditions that the code relies on | It explains why looking at the code alone is not enough for execution |
| Reproducibility is the act of leaving conditions so that the same code can be run again later | Learning and collaboration do not end after running something once |
| A requirements file records the needed package list and version range | It becomes the starting point when someone else rebuilds the environment |

## Direct and Indirect Dependencies

Dependency is an external condition that my code needs in order to run. In Python practice, package dependencies are usually the first kind you encounter.

For example, the following code needs NumPy.

Calculating the mean of the NumPy array `[1, 2, 3]` prints `2.0`. Because the code imports NumPy, that package must be available in the execution environment.

```python
# This example imports the packages needed to run NumPy and Pandas examples in a reproducible environment.
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

Installing one package can also install other packages it requires.

## Conditions for Rerunning Code

Reproducibility is the property that lets you expect the same behavior when you run the same code again under the same conditions.

In AI and data practice, reproducibility is important. At the stage of reading mathematical explanations, it may not look like a big problem, but the moment you run code, environment differences can change the result.

- The Python version may differ.
- The package versions may differ.
- The operating system may differ.
- The data file location may differ.
- The Colab runtime may have been reset.

Therefore, if you want to share practice, giving only the code may not be enough. You also need to leave “which environment did I run this in?”

## A Reset Notebook Runtime

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

## The requirements.txt Installation List

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

The file serves the following role.

- `requirements.txt` is not Python code.
- It is not a terminal command either.
- It is a file where the list of packages to install is written down.

If this file exists, another person can more easily understand “which packages does this project require?”

## A CSV Mean Calculation Project

Suppose a small practice folder is organized like this.

```text
score-summary/
  summary.py
  scores.csv
  requirements.txt
```

`summary.py` reads a CSV file and calculates the mean.

Download [scores.csv](/AiBook/assets/part-02/chapter-07/scores.csv) and place it beside `summary.py`. Each CSV row represents a student; the `score` column contains `82, 91, 77, 88`. Running from the `score-summary` folder prints the mean `84.5`.

```python
# This example imports the packages needed to run NumPy and Pandas examples in a reproducible environment.
import pandas as pd

# Read scores.csv and calculate the mean of the score column in the table data.
scores = pd.read_csv("scores.csv")
print(scores["score"].mean())
```

List `pandas`, the package this code uses directly, in `requirements.txt`.

```text
pandas
```

The receiver can move into the folder and prepare the necessary package with the following command.

```bash
python -m pip install -r requirements.txt
```

Use the same project Python for installation and execution. Once prepared, run `python summary.py`. Installing the requirements alone cannot supply a missing CSV; the data file is also necessary.

## Specifying Versions and Recording Installed Packages

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
python -m pip freeze > requirements-snapshot.txt
```

And in another environment, you can install like this.

```bash
python -m pip install -r requirements-snapshot.txt
```

`>` saves output to a file, overwriting an existing file with the same name. `pip freeze` lists packages installed in the environment and may include packages the project does not use.

Version pinning does not make all execution conditions identical. The operating system, Python version, hardware, and package availability can still matter.

For example, when making learning materials, you can think about the difference between the following two methods.

- `pandas`: the latest version may be installed, so the environment may change over time.
- `pandas==2.2.2`: because it requires a specific version, it can be matched more closely to the environment from that time.

These version numbers illustrate the notation. Record versions that have been checked by running the actual project.

## Installation Lists and Project Metadata

Requirements files and a project’s distribution installation requirements serve different purposes.

- requirements file: a list of things to install in order to build a specific environment
- project configuration file: a file that distributes a package or describes project metadata

## Notebook Installation Commands and Environment Records

Colab is easy to start with. But reproducibility problems do not disappear.

The Colab runtime can be reset. At that point, packages installed there can disappear. Also, the default package versions provided by Colab can change over time.

That is why it is useful to leave the required installation commands at the top of the notebook or to build the habit of recording which environment it was run in.

The following cell installs NumPy, pandas, and Matplotlib in the current notebook kernel. It can prepare the required packages after creating a new runtime.

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

## Execution Record Contents

Include the following in an execution record.

- Which Python version was used to run it
- Which packages are needed
- What the versions of important packages are
- Which folder the code is run from
- Where the data files are supposed to be
- Whether the environment is Colab or a local PC

If you have this information, it becomes easier to narrow down the cause when an error happens later.

## Missing Packages Versus Missing Files

Omitting different requirements from the CSV mean project leads to different failure points.

| Execution condition | Result | What to restore |
| --- | --- | --- |
| pandas is absent | `ModuleNotFoundError` at `import pandas` | Install the package into the running Python |
| pandas exists but scores.csv is absent | `FileNotFoundError` at `read_csv` | Check the data file and working directory |
| Both package and CSV are ready | Prints mean `84.5` | Record these conditions and the execution command |

Changing the CSV score `82` to `100` changes the mean to `89.0`, even with identical code and packages. To compare results, check that the input data matches as well as the environment.

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
