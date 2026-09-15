# P2-10.2 Jupyter, Colab, and Local Execution

> Section ID: `P2-10.2`
> Version: `v2026.09.15`

## Tools and Execution Location

The Colab FAQ describes Jupyter as the open-source project on which Colab is based. Colab is a hosted service for using and sharing Jupyter notebooks without managing a local installation and server.

Jupyter names tools and an ecosystem; Colab names a service; local execution describes a location. The Colab discussion below assumes Google's managed remote runtime. The Colab interface can also connect to a local runtime.

| Name | Meaning | Execution location |
| --- | --- | --- |
| Jupyter | Open-source notebook tools and ecosystem | Local PC, server, cloud, and other environments |
| Colab | Google's hosted Jupyter Notebook service | Google-provided remote runtime |
| Local execution | Run with Python on your computer | Your PC |

“Jupyter or Colab?” is therefore not a choice between unrelated alternatives. Colab uses the Jupyter Notebook format and workflow, while handling installation and server operation for the user.

## Documents, Runtimes, and Files

A common confusion is treating a file and execution state as the same thing.

Notebook files usually use `.ipynb`. Jupyter's architecture documentation describes structured data for code, metadata, content, and output, stored on disk as JSON with this extension.

Having the file does not mean its code is currently running.

| Component | What it is | Example |
| --- | --- | --- |
| Notebook file | Document storing code, explanations, and some output | `practice.ipynb` |
| Kernel | Process executing code and retaining variables | Python kernel connected to the notebook |
| Runtime environment | Python, packages, and computing resources used by the kernel | Environment inside a Colab VM; local virtual environment |
| File system | Locations where code reads and writes files | PC folders, Colab VM, Google Drive |

The notebook can survive after its runtime disappears. Code cells can remain even when packages installed or temporary files created by those cells are gone.

The Colab FAQ explains that code runs in an account-specific virtual machine, which is deleted after inactivity and has a maximum lifetime.

## Comparing Execution Setups

Even with the same notebook format, the executing computer and accessible files can differ.

| Criterion | Colab | Local Jupyter | Local script |
| --- | --- | --- | --- |
| Execution location | Google remote runtime | Your PC | Your PC |
| Setup burden | Low | Moderate | Moderate |
| File access | Colab VM, uploads, Drive integration | Direct access to PC files | Direct access to PC files |
| Result records | Easy to retain in notebook | Easy to retain in notebook | Separate output/log needed |
| Repeated automation | Limited | Possible, with notebook-state considerations | Natural fit |
| Sharing | Easy link sharing | File or server access needed | Code and environment instructions needed |
| Considerations | Runtime/resource limits, Drive permissions | Installation and package management | Explanation and results can become separated |

There is no environment that is always best. Learning goals and execution requirements lead to different choices.

## Colab Setup and Resources

Colab has a low starting barrier. You can run code in a browser before installing Python, Jupyter, NumPy, or pandas on your PC.

Colab can be sufficient for the small mathematical calculations, list and dictionary examples, and basic NumPy work introduced earlier in this part.

Colab is useful when:

- Python is not yet installed.
- You want to open the same notebook on another computer.
- You want to share code, explanations, and results by link.
- You want to explore a concept with small data.
- You want to briefly experiment with GPU or TPU acceleration.

Colab is an external service. Free resources are neither guaranteed nor unlimited, and usage and termination conditions can change. Its FAQ notes that limits, idle timeouts, maximum runtime, and GPU types vary over time.

Treat Colab as a remote workspace for starting experiments quickly, rather than as a permanently available personal computer.

## Managing Local Jupyter Environments

Local Jupyter runs Jupyter Notebook or JupyterLab and a kernel on your computer. If you connect to Jupyter running on a server, file access is relative to that server instead.

The advantage is direct control over files and environments.

- Read and write files in PC folders directly.
- Choose virtual environments yourself.
- Manage package versions for each project.
- Depend less on connectivity and external service policies.

This requires more preparation:

- Install Python.
- Install Jupyter packages if needed.
- Manage project-specific virtual environments.
- Record dependencies to reproduce work on another computer.

A browser interface does not tell you where Python executes. Available files and packages depend on whether the kernel runs on your PC or a server.

## When an Installed Package Cannot Be Found

A successful terminal installation of NumPy can still be followed by a failing notebook `import numpy`. Different Python environments have different installed packages. This cell shows the current kernel's executable and Python version.

```python
import sys

print("Python executable:", sys.executable)
print("Python version:", sys.version.split()[0])
```

Executable paths vary by computer. If a local kernel does not use the expected project environment, check the notebook's kernel selection. To install NumPy into the current kernel environment, run this command in a notebook code cell.

```text title="IPython · notebook code cell"
%pip install numpy
```

You still need to run `import numpy as np` after installation. Upgrading an already imported package may require restarting the kernel and rerunning preparation cells. Investigate installation issues through the execution environment, and missing files through the working directory and paths.

## Extracting Functions into a Module

Notebooks are useful learning records, but code kept only in notebooks can become hard to reuse.

A `.py` file is often a better fit when reading and processing data daily or reusing a function across projects.

Save this function in `stats_utils.py`. It returns the mean of a nonempty score list. Saving the file alone does not execute the function.

```python
def mean(values):
    return sum(values) / len(values)
```

If the file is in a working directory where Python can find it, a notebook or another script can import it. The following output is `67.33333333333333`.

```python
from stats_utils import mean

print(mean([82, 75, 45]))
```

The notebook keeps inputs and interpretations; the module enables reuse. An imported module remains in memory, so editing its `.py` file and repeating the same import may not load the change. For this example, restart the kernel and rerun from the import cell to check the edited function.

## Shared Documents and Required Setup

The Colab FAQ says sharing includes the notebook's text, code, output, and comments. It does not include the virtual machine, files prepared during execution, or the installed-library environment.

| Shared | May not be shared |
| --- | --- |
| Explanation cells | Runtime temporary files |
| Code cells | Manually installed package state |
| Saved output | Current variables in memory |
| Comments or document content | Permissions for personal Drive files |

A shared notebook therefore needs to document its preparation steps.

After the installation cell described earlier, import the package and record its version.

This cell prints the NumPy version and the mean `67.33333333333333`. The version depends on the environment.

```python
import numpy as np

print(np.__version__)
print(np.mean([82, 75, 45]))
```

If files are needed, also explain where to obtain them. A file in your runtime may be absent from someone else's.

## Choosing an Environment for a Task

Choose according to file locations, result-recording needs, and repeated execution.

| Situation | First choice |
| --- | --- |
| Installing Python feels difficult | Colab |
| Check small calculations and tables | Colab or local Jupyter |
| Read and write many PC files | Local Jupyter or scripts |
| Repeat or automate the same code | Local scripts |
| Show explanations alongside results | Colab or Jupyter notebooks |
| Strictly control package versions | Local virtual environment |

Missing packages and incorrect paths need different remedies. Check the environment's preparation along with the error.

## Case: A CSV That Exists Only Locally

Suppose a notebook reads `project/data/scores.csv` from your PC's `project` directory, then opens in a fresh remote Colab runtime. The string `data/scores.csv` travels with the document; the PC file does not.

This code prints the working directory, resolved file path, and whether the file exists. `Path.cwd()` refers to the working directory of the environment executing the code.

```python
from pathlib import Path

path = Path("data/scores.csv")
print("working directory:", Path.cwd())
print("resolved path:", path.resolve())
print("file exists:", path.is_file())
```

If the file exists under the local working directory, the final output is `True`. In a new environment without that relative path, it is `False`. Opening the missing file raises `FileNotFoundError`.

Once the file is prepared in the new environment, match its location and the code path. A file uploaded as `scores.csv` directly under the working directory requires `Path("scores.csv")`. To retain `data/scores.csv`, put the file in the `data` folder.

When handing over a notebook, document input locations, access permissions, and package installation so others can rerun the same calculation.

## Checklist

- Explain why Jupyter and Colab name different layers.
- Distinguish a notebook file (`.ipynb`) from its runtime.
- Explain that Colab code can execute on a remote virtual machine.
- Explain why sharing a notebook does not share runtime files or installed packages.
- Compare local Jupyter with local scripts.
- Explain how file-path problems can arise from execution environments.
- Explain how the same `.ipynb` can have different file, package, and sharing conditions depending on where it executes.

## Sources and References

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-09-15. Used as the basis for distinguishing shared notebook contents from runtime, VM, file, and installed-library state that are not shared together.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation, checked on 2026-09-15. Used as background for distinguishing Jupyter documents, interfaces, kernels, execution location, and runtime.
- Jupyter Notebook Team, [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Notebook documentation, checked on 2026-07-20. Used as the basis for explaining local notebook servers and browser-based notebook usage flow.
- Python Software Foundation, [sys.executable](https://docs.python.org/3/library/sys.html#sys.executable){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Reference for identifying the kernel Python executable.
- Python Software Foundation, [Modules](https://docs.python.org/3/tutorial/modules.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Reference for module imports and reuse within a session.
- IPython, [%pip](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip){: target="_blank" rel="noopener noreferrer" }, checked on 2026-09-15. Reference for installation into the current kernel environment.
