# P2-10.2 Difference Among Jupyter, Colab, and Local Execution

> Section ID: `P2-10.2`
> Version: `v2026.07.26`

In P2-10.1, we viewed a notebook as a computational document containing code, explanation, and output together. Now we separate the three execution styles that are encountered most often in practice.

Jupyter, Colab, and local execution.

These three names overlap visually. Colab also uses the Jupyter Notebook format, Jupyter can also run on your own computer, and local execution can also happen not only through notebooks but through `.py` scripts. So we separate `where it is executed`, `where it is stored`, and `what is shared`.

This Section explains the relation among `Jupyter`, `Colab`, `local execution`, `runtime`, and `.ipynb` files. If the previous Section explained the notebook document format, then here the standard is how that document is actually executed and what is shared together with it.
This distinction matters before anything else.
If the execution place changes, the meaning of the same notebook also changes.

## Core Criteria: the Difference Among Jupyter, Colab, and Local Execution

- You can explain Jupyter as an open-source notebook ecosystem, and Colab as a hosted service based on Jupyter.
- You can explain local execution as a style of running in your own computer's Python, file, terminal, and package environment.
- You can distinguish a notebook file (`.ipynb`) from a running runtime.
- You can explain that notebook contents may be shareable in Colab, while runtime files and installation state may not be shared as-is.
- You can judge which style to choose first among Colab, Jupyter, and local scripts depending on the learning situation.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| The relationship between Jupyter and Colab | It prevents misunderstanding their names as being at the same layer | Understand Colab as one service that provides Jupyter-style notebooks |
| The criterion for choosing an environment | It helps you consider execution location together with reproducibility conditions | View them through starting barrier, reproducibility, file access, and convenience of repeated execution |
| What to watch when sharing | It prevents confusion between a notebook file and a runtime | Check separately whether only the file is shared or whether the execution environment is the same too |

Even with the same `.ipynb` file, runtime and file access change depending on where it is executed. Colab is a hosted service, while local Jupyter and local scripts are environments you manage more directly. Also, a notebook file and a currently running runtime are different things. Once this distinction stands, Chapter 10 reads less like `a notebook service comparison` and more like `a Chapter about reading where execution records are placed and under what conditions`.

In other words, the core of this Chapter is that the question moves from `What shall we leave in one document?` to `Where and under what conditions is that document actually executed?` In P2-10.3, this execution difference is reorganized again as a habit of leaving reproducible records.

## Jupyter and Colab Are Not Words at the Same Layer

The Google Colab FAQ explains Jupyter as the open-source project on which Colab is based. It also explains Colab as a hosted service that lets you use and share Jupyter notebooks without downloading, installing, or running them yourself.

Distinguish them here like this.

| Name | What to understand first | Execution location |
| --- | --- | --- |
| Jupyter | an open-source notebook tool and ecosystem | often your own PC, server, or cloud |
| Colab | a hosted Jupyter Notebook service provided by Google | a remote runtime provided by Google |
| local execution | execution through your own computer's Python | your own PC |

So the question `Jupyter or Colab?` is not a completely opposing choice. Colab is a service based on the Jupyter Notebook format and workflow. What differs is that the user does not directly manage installation or server execution.

## Separate Notebook Files from Execution Location

A point that often causes confusion is treating the file and the execution state as if they were the same thing.

A notebook file is usually in `.ipynb` format. Jupyter architecture documentation explains that a Jupyter Notebook is structured data representing code, metadata, content, and output, and that when stored on disk it uses the `.ipynb` extension and a JSON structure.

But `having the file` and `having the code currently running` are not the same.

| Division | What it is | Example |
| --- | --- | --- |
| notebook file | a document storing code, explanation, and some output | `practice.ipynb` |
| runtime | the Python environment that actually executes the code | a Colab VM, a Jupyter kernel |
| file system | the file location that code reads and writes | a folder on your PC, a Colab VM, Google Drive |

The reason this distinction matters is simple. A notebook file can remain while a runtime disappears, and even if code cells remain, the packages installed in that runtime or temporary files made there can disappear.

The Colab FAQ also explains that Colab code runs in a virtual machine assigned to the account, and that the virtual machine may be deleted after some period of idleness and also has a maximum lifetime.

## Seeing the Difference Among the Three Environments at Once

The table below organizes only the differences a learner needs first.

| Criterion | Colab | local Jupyter | local script |
| --- | --- | --- | --- |
| execution location | Google remote runtime | your own PC or a server you launched | your own PC |
| installation burden | low | medium | medium |
| file access | Colab VM, upload, Drive integration | natural access to files on your PC | natural access to files on your PC |
| result recording | easy to leave in a notebook | easy to leave in a notebook | requires separate output or logs |
| repeated automation | limited | possible, but notebook characteristics need care | most natural |
| sharing | easy through a link | requires file sharing or server access | requires code files and environment explanation |
| point to watch | runtime limits, resource limits, Drive permissions | installation and package management | explanation and result records can split apart easily |

What matters in this table is not `Which one is always best?` The appropriate environment changes when the learning purpose and the execution purpose change.

## Colab Lowers the Starting Barrier

The major strength of Colab is that the starting barrier is low. Before installing Python, Jupyter, NumPy, and pandas directly on your own PC, you can run code in a browser.

For the kind of early practice in this Part, such as small mathematical calculations, list and dictionary examples, and simple NumPy checks, Colab can be enough.

Colab is useful in the following situations.

- Python is not installed yet.
- You want to open the same notebook on another computer too.
- You want to share code, explanation, and results through a link.
- You want to check concepts with small data.
- You want to briefly test acceleration environments such as GPU or TPU.

But Colab is an external service. Free resources are not guaranteed or unlimited, and usage limits and runtime-ending conditions can change. The Colab FAQ also explains that usage limits, idle termination, maximum runtime, and GPU types can change over time.

Therefore, it is safer to view Colab not as `my computer that is always there`, but as a remote workspace for quickly starting learning and experiments.

## Local Jupyter Runs Notebooks in Your Own Environment

Local Jupyter is the style of running Jupyter Notebook or JupyterLab on your own computer or on a server that you manage.

Its strength is that you control files and the environment directly.

- You can directly read and write files in folders on your PC.
- You can choose your virtual environment directly.
- You can manage package versions to match the project.
- You can depend less on internet connection or external-service policy.

Instead, more things need to be prepared.

- Python must already be installed.
- Jupyter-related packages may need to be installed.
- Virtual environments must be managed by project.
- If the work must be reproduced on another computer, dependencies must be recorded.

So here the natural route is to lower the execution barrier with Colab at first, and then treat the time when local installation and virtual environments become necessary separately in Part 2 Chapter 7 Section 7.

## Local Scripts Are Better for Repeated Execution and Reuse

Notebooks are good for learning records, but if all code remains only in notebooks, reuse can later become difficult.

For example, if you must read a data file every day and repeat the same processing, or if the same function must be reused across multiple projects, then a `.py` file is often more natural.

Problem situation: You want to move a computation first verified in a notebook into a function that can later be repeatedly reused.
Input: A function definition that receives a list of numbers and returns their mean.
Expected output: There is no output, but a reusable function form is created.
Concept to check: See that once repeated execution and reuse become necessary, notebook code can move into a `.py` function.

```python
# This example checks how functions, packages, and file paths vary by execution environment.
def mean(values):
    return sum(values) / len(values)
```

This function can first be tested in a notebook. But once it begins to be reused repeatedly, it may be better to move it into a file such as `stats_utils.py`.

The following order is natural here.

1. Understand it first through a small example in a notebook.
2. When the code grows, bundle it into a function.
3. When it is reused repeatedly, separate it into a `.py` file.
4. If it must run on another computer, record dependencies and the execution method.

Notebooks and scripts are not competitors. Notebooks are strong for exploration and explanation, while scripts are strong for repeated execution and reuse.

## When Sharing, Check What Is Actually Shared

The Colab FAQ explains that when you share a notebook, the full content of the notebook such as text, code, output, and comments can be shared. By contrast, it explains that the virtual machine you were using, the files prepared during execution, and the installed-library state are not shared as-is.

This difference is very important.

| What is shared | What may not be shared |
| --- | --- |
| explanation cells in the notebook | temporary files inside the runtime |
| code cells | the state of packages you installed directly |
| saved output | variables currently in memory |
| comments or document contents | Google Drive file permissions of a personal account |

So a notebook to be shared should keep the necessary preparation process inside the document itself.

For example, put the following content in an early cell.

Problem situation: You want someone else rerunning a Colab notebook to install the necessary package first.
Input: A `%pip` command to install `numpy`.
Expected output: `numpy` is installed in the current kernel.
Concept to check: See that a shared notebook should keep the required preparation process in the front cells so that rerunning becomes easy.

```python
# This example checks how functions, packages, and file paths vary by execution environment.
%pip install numpy
```

And in the code, keep the required imports explicit.

Problem situation: You want to show clearly which package the actual code uses after installation.
Input: Code importing `numpy` as `np`.
Expected output: There is no output, but later cells are prepared to use `np`.
Concept to check: See that separating the installation cell and the import cell makes execution-environment dependency more visible.

```python
# This example checks how functions, packages, and file paths vary by execution environment.
import numpy as np
```

If a file is needed, then where to obtain that file must also be written. Even if the file exists in your runtime, it may not exist in someone else's runtime.

## File Access Differs by Environment

Even with the same code, the file path can differ by execution environment.

For example, on a local PC, there may be `data/scores.csv` inside the current project folder.

Problem situation: You want to see through the simplest path example why file-reading code can differ by environment.
Input: A file-path string based on a local project.
Expected output: There is no output, but it becomes visible which file the code is trying to find.
Concept to check: See that file problems can arise not from code grammar but from execution environment and path differences.

```python
# This example checks how functions, packages, and file paths vary by execution environment.
path = "data/scores.csv"
```

In Colab, the same file may not exist in the runtime. The path changes depending on whether you uploaded the file, mounted Google Drive, or downloaded it from GitHub.

Check the following questions first here.

| Question | Reason |
| --- | --- |
| Where is this code being executed? | The file location differs depending on whether it is on a local PC or in Colab |
| Where is this file located? | A folder on my PC, a Colab VM, and Google Drive are different places |
| Will this file remain if I rerun later? | Temporary runtime files may disappear |
| Can another person access it too? | Personal Drive permissions may not be shared |

File problems can look like code errors, but in many cases the real issue is the execution environment.

## Which Environment Should Be Chosen First?

When following the practice in this Part, the following standard is enough to start.

| Situation | Environment to choose first |
| --- | --- |
| Installing Python still feels burdensome | Colab |
| Checking small mathematical calculations and table output | Colab or local Jupyter |
| Reading and writing many files on my own PC | local Jupyter or local script |
| Repeatedly executing or automating the same code | local script |
| Showing explanation and results together to another person | Colab or a Jupyter notebook |
| Strictly pinning package versions | local virtual environment |

There is no need to choose a perfect environment from the beginning. What matters is to separate `Is this a code problem, a package problem, a file-location problem, or a runtime problem?` when practice gets blocked.

## Case Study

### Case 1. Why does the same CSV file fail to open in Colab?

Suppose a learner read `data/scores.csv` successfully at home through local Jupyter, but the next day running the same code in Colab produced a `file not found` error. From the person's point of view, it can feel as if `the code that worked yesterday` itself has become wrong.

But the actual problem is more likely to be the execution location than the code. In local Jupyter, folders on your own computer are directly visible. In Colab, a remote runtime opens again, and inside it the same file may not exist. The result changes depending on whether Drive was connected, whether the file was uploaded, and whether a download cell exists.

This case helps you read `Jupyter`, `Colab`, and `local execution` not as feature names but as differences in execution environment. Even with the same `.ipynb` document, the file path, installation state, and preserved runtime can differ depending on where it is executed.

So when reading practice documents, first check `Where is this code being executed?`, `Where is this file located?`, and `Can another person still see the same file when rerunning it?` Once the environment distinction comes first, the cause of an error can also be narrowed down more quickly.

## Checklist

- Can you explain that Jupyter and Colab are not words at exactly the same layer?
- Can you distinguish a notebook file (`.ipynb`) from a runtime?
- Can you explain that code in Colab can run in a remote virtual machine?
- Can you explain that a shared notebook does not necessarily share runtime files and installation state too?
- Can you distinguish the strengths and weaknesses of local Jupyter and local scripts?
- Can you explain that a file-path problem can really be an execution-environment problem?
- Can you explain that even with the same `.ipynb` file, the file, package, and sharing conditions can differ depending on execution location and runtime?

## Sources and References

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-07-20. Used as the basis for distinguishing shared notebook contents from runtime, VM, file, and installed-library state that are not shared together.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, checked on 2026-07-20. Used as background for distinguishing Jupyter documents, interfaces, kernels, execution location, and runtime.
- Jupyter Notebook Team, [The Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/notebook.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Notebook documentation, checked on 2026-07-20. Used as the basis for explaining local notebook servers and browser-based notebook usage flow.
