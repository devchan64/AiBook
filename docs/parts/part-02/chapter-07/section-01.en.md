# P2-7.1 Local Environment and Runtime

> Section ID: `P2-7.1`
> Version: `v2026.07.19`

In P2-3.5, we first separated Colab and a local PC. At that time, the purpose was a preliminary guide so the reader could immediately follow the NumPy practice. Now we step down one layer more basic.

Up through P2-6, we read `what is being calculated`, such as formulas, loss, and optimization. But in reality, those calculations are executed somewhere, and some program has to read them before we can confirm them with our eyes. Starting from this Section, we are not pausing mathematical language. We are entering the part where we read the environment that turns those calculations into actual executable statements.

If we compress this transition in the shortest possible way, it becomes the following.

| Question we just held | New question we hold now | Why it must be read immediately after |
| --- | --- | --- |
| How do we reduce loss and change values? | Where and with what program do we execute that calculation? | Because all later NumPy, Pandas, and Git practice can only be confirmed on top of an actual execution environment. |

Here we explain the large distinction between `local environment` and `runtime`. Even if later Sections continue into terms such as `terminal`, `interpreter`, `virtual environment`, and `dependency`, the big picture of these two terms reconnects on top of the explanation here.

Rather than following Python installation screens one by one, this Section focuses on distinguishing where calculations are actually executed and who manages that place. If you first secure the relationship among local environment, runtime, Colab, and a local PC here, then when you later see terminal, interpreter, and virtual environment, you will read them not as `am I learning another new tool again?` but as `am I dividing the same execution place more finely?`

First, look at the smallest execution scene. The examples below all have the same goal.

Where should `hello` actually be typed so it runs?

| What you want to see | Where you type it | Example | Feel to check now |
| --- | --- | --- | --- |
| Run one line of Python in Colab | Colab code cell | `print("hello")` | It is visible inside the browser, but execution is handled by the Colab runtime. |
| Check whether Python exists on a local PC | terminal | `python --version` | This is not Python code but a terminal command. |
| Run one line of Python on a local PC | Python interpreter or `.py` file | `print("hello")` | Even the same code produces output only when a Python interpreter reads it. |
| Run one line of Python in a Jupyter notebook | notebook code cell | `print("hello")` | A notebook cell also ultimately runs on top of a Python execution environment. |

Problem situation: if you get confused about where to put the same `hello`, then explanations of the runtime can feel abstract.
Input: one terminal command and one line of Python code.
Expected output: in the terminal, the Python version appears; in the Python-code position, `hello` appears.
Concept to check: before asking `what code do we write?`, we first see that `where do we put it?` is different.

```bash
python --version
```

```python
print("hello")
```

The minimum distinction that must be fixed right here is two things.

- `python --version` is a command placed into the terminal.
- `print("hello")` is Python code placed into a Python interpreter or notebook cell.

In other words, saying that we distinguish the runtime starts not from grand installation theory, but from knowing the fact that `even if they look like the same screen, the place where you type can be different`.

## First Places to Return to by Problem Type

Chapter 7 is more efficient when you return to it by the kind of problem where you got stuck rather than reading everything in one sweep.

| Problem you are stuck on now | Section to revisit first | Why that Section comes first |
| --- | --- | --- |
| I keep mixing terminal commands and Python code | `P2-7.1`, `P2-7.3` | Because you need to distinguish the execution place and the role of the Python interpreter again. |
| I am confused about the current folder and file location | `P2-7.2` | Because the feel for the working folder must be fixed before the next command can be read. |
| Package installation and virtual environment are getting mixed together | `P2-7.4`, `P2-7.5` | Because the installation place and reproducibility management continue into one another. |
| I am unfamiliar with terminal windows by operating system | `P2-7.6` | Because you need to become familiar with the window and input place before the commands themselves. |
| I do not know whether I need to install Python now | `P2-7.7` | Because you should first separate the installation judgment so you do not get blocked by unnecessary setup. |
| Tutorial commands such as `|`, `>`, and environment variables feel strange | `P2-7.8` | Because you first need the minimum feel for reading runtime syntax. |
| I want to check whether local Python is actually running well | `P2-7.9` | Because you can follow the post-installation check procedure at once. |

The purpose of this table is not to make the reader memorize Chapter 7. It is to let the reader immediately find the shortest return path by the `type of blockage` they have right now.

| What to secure in this Section now | The question that follows immediately next | Where it is used again later |
| --- | --- | --- |
| The big picture that distinguishes local environment and runtime | In P2-7.2, it continues into how the terminal and working folder connect to that execution place. | It becomes the starting point of all later local practice, package installation, and error checking. |
| The point that both Colab and a local PC are runtimes, but their management styles differ | In P2-7.3 and P2-7.4, it continues into why interpreter and virtual environment are learned separately. | It repeats later as the criterion for reproducibility, team collaboration, and rerunning examples. |
| The point that Chapter 7 is not about `all of Python`, but about the `execution place` | It continues into the criterion for reading without mixing its role with Chapters 8 through 10. | It is used again when organizing the later NumPy, Pandas, and Git practice of Part 2 into different layers. |

Here we explain for readers who may not have basic programming knowledge. If you already know terminal, Python, and virtual environments, some of this may feel familiar, but these are words that repeat throughout later practice, so they need to be organized once.

This Section reads around the following four questions.

- Where is code executed?
- What does Python execute?
- What is different between local environment and runtime?
- Why does the phrase virtual environment appear?

| Term | Meaning to secure first in this Section |
| --- | --- |
| local environment | the bundle of programs, files, and settings prepared so code can run on my computer |
| runtime | the place where code actually runs and the connected bundle of programs there |
| Colab runtime | an environment managed by an external service even though we use it in the browser |
| local-PC execution | an execution style where the user directly manages Python, folders, and package state |
| virtual environment | a device that divides Python space more finely by project inside the local environment |

This question can look more practical than AI mathematics. But it is very important in machine-learning practice. Even with the same code, if the runtime is different, the result can differ or the code may not run at all.

In other words, the reason we learn these words now is simple. Later, when we create NumPy arrays, read Pandas data, and receive example projects with Git, we must be able to first distinguish `why does the code not run?` as a runtime problem rather than as a mathematics problem.

When reading Part 2 Chapters 7 through 10 afterward, keep the following three layers separate.

| Layer we are reading now | Central question | Representative Chapter |
| --- | --- | --- |
| runtime | where do we run it? | Chapter 7 |
| code syntax and data structures | what sentence do we write for what values and bundles? | Chapters 8-9 |
| notebook record | how do we record and rerun execution results? | Chapter 10 |

The key point of this table is that terminal, Python syntax, and notebooks may all sit under one name called `studying Python`, but they do not play the same role. Among them, Chapter 7 first distinguishes `execution place and manager`.

If we compress this flow more briefly using Part 2 Chapters 7 through 10, it becomes the following.

| Bundle we are reading now | Question to hold first | What becomes more concrete immediately after |
| --- | --- | --- |
| Chapter 7 runtime | Where do we run it? | terminal, interpreter, virtual environment |
| Chapters 8-9 code syntax and data structures | What do we write as what values and bundles? | values, variables, lists, dictionaries, feel for data structures |
| Chapter 10 notebook record | How do we leave and rerun execution results? | Jupyter, Colab, local execution, habits of reproducibility |

If we connect this transition to the surrounding Chapters at once, it can be organized like this.

| Previous Chapter | Current Chapter | Chapter that connects immediately after |
| --- | --- | --- |
| formulas and calculation: what shall we calculate? | runtime: where and with what program do we execute that calculation? | Python syntax: in what sentences do we write that calculation? |
| language of calculation | execution place and manager | code sentence |

So the core of this Chapter is that the handle changes from `what shall we calculate?` to `where shall we execute that calculation?`

## Scope of This Section

Here we cover only the following degree.

- local environment
- runtime
- why terminal, Python interpreter, and virtual environment appear in sequence

We already saw Colab and local-PC execution in P2-3.5, but here we allow repetition. We explain the same content again not from the practice perspective, but as `language for beginning programming`.

However, if terminal commands, working folders, Python script execution, virtual-environment creation, package installation, and reproducibility management are all put into one Section, they pass too quickly. So P2-7 is divided into the following flow.

P2-7 is divided into the following flow.

1. `P2-7.1` the big picture of the runtime
2. `P2-7.2` terminal and working folder
3. `P2-7.3` Python interpreter and script
4. `P2-7.4` virtual environment and package
5. `P2-7.5` dependency and reproducibility
6. `P2-7.6` supplementary learning: how to use terminals on Windows, macOS, and Linux
7. `P2-7.7` supplementary learning: when is Python installation necessary?

Python installation is not handled immediately in the early part of P2-7. If the reader meets installation screens and operating-system differences from the very start, they may get blocked by installation before the basic concept of where code runs. The earlier practice in this Part can to some extent be substituted with a browser runtime such as Colab. So first we build a feel for running code with Colab, and in the supplementary learning of P2-7.7 we separately handle the point at which Python should be installed on a local PC and how to check it.

If OS-specific terminal windows feel unfamiliar, you may read the supplementary learning of P2-7.6 before moving to P2-7.2. Conversely, if the more urgent question is `do I need to install Python on my computer right now?`, you may first look at the supplementary learning of P2-7.7 and then come back. The role of this Section is not to finish the installation procedure, but to first let the reader understand why such supplementary learning is separated out.

| Where you are stuck now | Go first | Main text to return to after finishing there |
| --- | --- | --- |
| I do not know where to open the terminal or how to check the current folder | P2-7.6 | for the big picture of the runtime go back to P2-7.1, and for the working folder go to P2-7.2 |
| I do not know whether I should install Python on my computer now | P2-7.7 | look at installation judgment first, then return to P2-7.1, and for the interpreter go to P2-7.3 |
| I am still more confused by conceptual distinctions than by OS-specific procedures | continue reading the current main text | continue into P2-7.2, P2-7.3, and P2-7.4 |

In other words, you move briefly to supplementary learning only when OS-specific procedures or installation judgment are what block you, and otherwise continue reading the main flow.

## Goals of This Section

- You can explain `local environment` as the conditions under which code runs on my computer.
- You can explain `runtime` as the place where code actually runs.
- You can explain why terminal, Python interpreter, and virtual environment appear in that order.
- You can explain that Colab and a local PC are both runtimes, but their management styles differ.

## Three Criteria

Here we distinguish the place where code runs, rather than the installation procedure itself. The following three criteria become the basis that ties together the later explanations of installation, terminal, and virtual environment.

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Code has to run somewhere | Because we need to distinguish text written in a file from actual execution | Understand that code alone does not finish the job; a program and place for running it are needed |
| The Python interpreter is the program that reads and runs Python code | Because terminal, script, and notebook execution are tied into one flow | You can explain with this distinction who reads `print("hello")` |
| Colab and a local PC are both runtimes, but the manager differs | Because it connects to why virtual environment and dependency become necessary later | Understand that Colab is managed more by the service, while local is managed more by the user |

## Why Does Python Appear So Often?

When studying AI, Python appears often. At that point the question can arise, `why Python in particular?`

Python was first developed by Guido van Rossum in the late 1980s and released in 1991. The official Python FAQ explains that Python was influenced by the experience of the ABC language and arose from the need for a more extensible scripting language in a situation where system-administration tasks were hard to handle only with C programs or shell scripts.

What matters in this history is that Python was from the start both a high-level language easy for humans to read and write and an execution tool connected to real system work.

That is why Python fits learning, automation, data processing, and experiment code well. The official Python FAQ also explains that Python is suitable as a first language because it has clear syntax, a large standard library, and an interactive interpreter.

The reason Python appears often in AI is connected to this same flow.

The reason Python appears often in AI is connected to this same flow.

- It is easy to move formulas into code.
- Small experiments can be run quickly.
- There are many tools such as NumPy, Pandas, and Matplotlib.
- Many machine-learning and deep-learning libraries gather in the Python ecosystem.

Of course, that does not mean Python is the only language. Inside real services, languages such as C++, Java, JavaScript, Go, and Rust are also used together. But at the entrance to AI learning and experimentation, there is a high chance of meeting Python. So in this Chapter, before installation, we first secure `where and how Python code is executed`.

## First Think About the Place Where Code Runs

When someone first begins programming, the phrase `write code` appears first. But code does not move by text alone. A program that reads and executes the code, and a place where it is executed, are needed.

Here we have to distinguish three words.

- code: a command written by a person
- execution: the computer processing that command
- runtime: the place where the programs, settings, packages, and files needed for execution are prepared

For example, the following is Python code.

Problem situation: we look at the smallest example that separates merely writing text from actually running it.
Input: one line of Python code that prints a string.
Expected output: if the Python interpreter reads it, `hello` is printed.
Concept to check: Python code becomes actual action only when there is a runtime and an interpreter.

```python
print("hello")
```

But if we only write this sentence in a text editor, nothing happens. The `Python interpreter` must read and execute this sentence.

## The Python Interpreter Is the Program That Reads and Executes Code

The `Python interpreter` is the program that reads and executes Python code. The official Python documentation explains that the Python interpreter can be invoked from the command line, and that in `interactive mode` commands can be entered at the `>>>` prompt.

Here we distinguish Python code and the Python interpreter as follows.

- Python code: a command written by a person
- Python interpreter: the program that reads and executes that command

There are several ways to run Python.

| Method | Example | Introductory explanation |
| --- | --- | --- |
| interactive execution | run `python`, then type at `>>>` | check one line immediately |
| script execution | `python example.py` | execute all code written in a file at once |
| notebook execution | Colab / Jupyter code cell | check code and results in cell units |

These three can look mixed. What matters is that they all share the same point: `the Python interpreter executes Python code`.

Python interpreter and script execution are revisited again in P2-7.3. Here, remember only the big picture that `Python code is executed by the Python interpreter`.

## The Terminal Is the Window for Sending Commands to the Computer

The `terminal` is the window where we enter commands to the computer. Programs such as Terminal on macOS, Windows Terminal, PowerShell, and a Linux shell belong here.

Terminal commands and Python code are different.

```bash
python --version
```

The command above is a command executed in the terminal. It is not a sentence written exactly as it is inside a Python code file.

By contrast, the following is Python code.

Problem situation: in contrast with a terminal command, we check again in what place Python code is written.
Input: Python code that prints a string.
Expected output: if run as Python code, `hello` is printed.
Concept to check: even if they look like similar sentences, terminal commands and Python code belong to different input places.

```python
print("hello")
```

This distinction matters.

Here too, we read by separating roles.

- terminal command: runs Python, installs packages, or executes files
- Python code: code read by the Python interpreter

The places that are often confusing are the following.

| Sentence | Where it is used |
| --- | --- |
| `python example.py` | terminal |
| `python -m pip install numpy` | terminal |
| `%pip install numpy` | Colab / Jupyter code cell |
| `import numpy as np` | Python code |
| `print("hello")` | Python code |

There is a reason we check again here the distinction we saw in P2-3.5. If we do not know the execution place, then when an error appears it becomes hard to judge what exactly should be fixed.

Terminal, shell, and working directory are handled separately in P2-7.2. Here, secure only the point that terminal commands and Python code are not the same sentence.

## The Local Environment Is the Execution Condition on My Computer

The `local environment` means the conditions under which code runs inside my computer. This can include the operating system, Python installation location, package installation state, current working folder, and environment variables.

Here we treat the local environment as `the conditions under which Python code runs on my computer`.

Even with the same code, the result can differ by computer.

For example, conditions can differ between computers in the following way.

- NumPy may be installed on my computer, but not on another computer.
- My computer may use Python 3.12, while another may use Python 3.10.
- A file path may be correct on my computer, but the file location may differ on another computer.

That is why in practice documents, `where is it executed?` matters as much as the code itself.

## The Runtime Is the Place Where Code Actually Runs

The `runtime` is the place where code actually runs. If you run on a local PC, your computer becomes the runtime. If you run on Colab, the notebook runtime provided by Google becomes the runtime.

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

## The Virtual Environment Is a Project-by-Project Execution Space

A `virtual environment` is a device that creates a separate execution space for each Python project. The official Python documentation explains that `venv` creates lightweight virtual environments and that each virtual environment can have an independent set of Python packages.

You can understand a virtual environment as `the Python execution space for each project`.

Why is it needed? Project A may need `numpy 1.x`, while project B may need `numpy 2.x`. If both are installed all mixed together on one computer, they can conflict, so the space is divided by project.

A virtual environment is not the project code itself. The official Python documentation also explains that virtual environments are usually created in directories such as `.venv` or `venv`, and are not put into source-control systems. In any project, `.venv` is the local environment for execution, not the body text file or code itself.

A commonly seen command is the following.

Problem situation: we first become familiar with what a command that creates a project-by-project execution space actually looks like.
Input: the terminal command `python -m venv .venv`.
Expected output: a virtual-environment directory called `.venv` is created.
Concept to check: a virtual environment is not only a conceptual explanation, but is connected to the command that actually creates a Python space by project.

```bash
python -m venv .venv
```

This command creates a virtual-environment directory called `.venv`. Here we do not memorize the OS-specific activation command. For now, secure only the meaning that `it creates the execution space by project`.

Virtual-environment creation and package installation are revisited in P2-7.4. Here, we look only at the reason why a virtual environment is needed.

## A Package Is a Bundle of Code Borrowed for Use

A `package` is a bundle of code created by someone else. Tools such as NumPy, Pandas, and Matplotlib belong here.

Here we read by distinguishing three layers.

- Python: the language and execution program
- package: the bundle of code borrowed inside Python
- `pip`: the tool that installs packages

For example, the command that installs NumPy and the code that imports it are different.

```bash
python -m pip install numpy
```

Problem situation: immediately after the installation command, we check how the position of installation and the position of Python code differ.
Input: Python code that imports NumPy under the name `np`.
Expected output: there is no printed output, but the current Python code becomes ready to use NumPy.
Concept to check: package installation is done in the terminal, while `import` happens inside Python code.

```python
import numpy as np
```

The first is installation. The second is the act of loading it for use inside Python code.

Package, dependency, and reproducibility are treated in more detail in P2-7.4 and P2-7.5. Here, keep only the point that installation and use are different actions.

## If You Do Not Know Programming, What Should You Distinguish First?

Rather than memorizing a lot of syntax, it is more important to secure distinctions first.

| Question | What to distinguish first |
| --- | --- |
| Where is this sentence entered? | terminal, code cell, or Python file |
| Who executes this code? | Python interpreter or shell |
| Did an error say a package is missing? | installation problem or import problem |
| Is the result different between my computer and Colab? | is the runtime different? |
| Does the example not work on another person's computer? | are the virtual environment and package versions different? |

This distinction is not itself a concept of machine learning. But in the process of learning machine learning, it can keep grabbing your ankle. So we organize it first in this Chapter.

## View It Through a Case

### Case 1. The Same Example File Works in Colab but Not on My Computer

Suppose a learner ran a book example in Colab and it worked well, but after downloading the same file and running it on a local PC, an error appeared. People often first suspect `is the code wrong?` or `was the download wrong?`

But in this situation, before syntax, the execution place must be distinguished first. In Colab, the code may already be using a prepared runtime and packages, while on the local PC the Python interpreter, working folder, and package installation state have to be checked directly.

The words emphasized in this Section, `local environment`, `runtime`, `interpreter`, and `virtual environment`, are exactly the language for reading this failure in separated pieces. In other words, if we distinguish `where was it executed?`, `who executed it?`, and `are the needed packages present in that place?`, then the problem can be narrowed down faster.

The confirmable result is simple. If `import numpy as np` works immediately in Colab but raises `ModuleNotFoundError` on the local PC, then we can conclude that before the code content, the package-preparation state of the local runtime should be checked first.

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

- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to support invoking the Python interpreter and distinguishing interactive input from script execution.
- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to confirm the basic description of Python as an interpreted, interactive programming language available on multiple operating systems.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to confirm that a virtual environment has its own Python installation and package state inside an isolated directory.
- Python Packaging Authority, [Install packages in a virtual environment using pip and venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/){: target="_blank" rel="noopener noreferrer" }, Python Packaging User Guide, checked 2026-07-19. Used to confirm the project-level flow of creating a virtual environment, activating it, and installing packages.
