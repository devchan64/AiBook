# P2-7.9 Supplemental Learning: How to Check Common Local Python Environment Problems

> Section ID: `P2-7.9`
> Version: `v2026.07.19`

In P2-7.4, we looked at virtual environments and packages, and in P2-7.5, we looked at dependency and reproducibility. In P2-7.7 and P2-7.8, we separately organized Python installation and environment variables.

But in reality, even if you understand each of these concepts separately, it is easy to stop at the following problems.

`I definitely installed it, but it cannot find the command.`
`pip install succeeded, but import fails.`
`It worked yesterday, but not today.`
`It works on Windows, but on macOS the command is different.`

Here, we explain `the basic checking order for local Python environment problems`. We tie the concepts divided earlier back together and organize them in the order of `what should be checked first?`

This supplement ties these problems together in the order of `what should be checked first?`

| Term | Meaning to establish first in this section |
| --- | --- |
| command mapping | Checking which command among `python`, `python3`, and `py` actually points to Python. |
| environment mismatch | A state where the environment where something was installed and the environment where it is run are different. |
| PATH | The list that determines where the terminal looks for commands to execute. |
| difference between `pip install` and `import` | The point that installation success and code-usage success are not the same thing. |
| troubleshooting order | The procedure of checking the current Python, virtual environment, and package location before reinstalling. |

## Scope of This Supplement

Here, we cover introductory criteria for checking problems frequently encountered when the Python environment on a local PC gets tangled. Judging whether installation is needed is covered in P2-7.7, shell symbols and environment variables are covered in P2-7.8, and the conceptual explanations of virtual environments and dependencies reconnect to P2-7.4 and P2-7.5.

The first question to solve here is this: `When a problem appears, instead of starting with reinstallation, how do I first check which Python environment I am looking at right now?`

So this supplement answers the following questions.

- Which of `python`, `python3`, and `py` should be checked first?
- How are `whether the virtual environment is on` and `where the package was installed` connected?
- When `pip install` succeeded but `import` fails, what should be suspected?
- To what level should PATH, permissions, and operating-system-specific differences be read?
- When a problem appears, what should be checked before trying installation again?

Here, we first close the minimum checking order for confirming `which environment am I looking at right now?`, and focus on how to check the current Python, virtual environment, and package location before reinstalling.

The flow after this section is also simple.

- When you go back to P2-7.4 and P2-7.5, you read virtual environments, dependencies, and reproducibility together with the question `which Python am I looking at right now?`
- Later, when you encounter environment problems in Python example sections and project execution sections, you reuse the same checking order.

## Goal of This Supplement

- You can separate local Python environment problems into code errors and execution-environment errors.
- You can explain why checking `python --version`, `python3 --version`, and `py --version` is the first step.
- You can explain that whether a virtual environment is activated and where packages were installed must be checked together.
- You can explain again that `pip install` success and `import` success are not the same thing.
- You can explain that when installation gets tangled, it is better to check the current environment first rather than reinstall immediately.

## Criteria to Hold First

The criterion you should hold first in this supplement is to separate `code problems` from `environment problems`.

| Problem currently visible | What to suspect first |
| --- | --- |
| The `python` command does not work | command mapping, PATH |
| `pip install` succeeded | Is the installation environment the same as the execution environment? |
| `import` fails | Are you looking at a different Python or a different virtual environment? |
| It worked yesterday, but not today | Did the runtime, working folder, or virtual environment state change? |

In other words, the key point of this section is not memorizing new commands, but holding onto the order for first checking `which Python am I looking at now?`

## Learning Background

The reason beginners get blocked on a local PC is often not because they do not know Python syntax, but because `which Python is being run` is unclear.

For example, all of the following scenes look similar, but their causes are different.

- Python itself is not yet installed.
- Python is installed, but the command is not connected in the current terminal.
- A virtual environment was created, but it is not turned on.
- A package was installed into a different virtual environment.
- A package installed in Colab is mistaken for also existing locally.

So here, rather than making you memorize many solution commands, we focus on building criteria for reading the problem in small pieces.

This supplement is placed here for when you understood the concepts of virtual environments and packages in P2-7.4 but are confused about whether `pip install` and `import` are actually looking at the same environment, or when you read about requirements and reproducibility in P2-7.5 but the execution environment gets tangled again on a local PC. If you go back to P2-7.4 and P2-7.5, you can reconnect `virtual environment`, `dependency`, and `reproducibility` with the question `which Python am I looking at right now?`

## Four Things to Check First

| Question | What to check first |
| --- | --- |
| Is the Python command being recognized now? | Check which of `python`, `python3`, and `py` works in my environment. |
| Which environment am I using now? | Distinguish system Python, virtual environment, and Colab. |
| Where was the package installed? | Check whether the installation environment and the execution environment are the same. |
| Is this a code problem or an environment problem? | `SyntaxError` and `ModuleNotFoundError` are not the same type of problem. |

## 1. First Confirm That a Python Command Actually Works

The first thing to do is not edit Python code, but check which command in the terminal points to the Python interpreter.

Problem situation: First check whether Python is actually connected on the local PC.
Input: the commands `python --version`, `python3 --version`, and `py --version`.
Expected output: it becomes visible which Python command and version work in my environment.
Concept to check: the first step of solving the problem is confirming `which command points to Python?`

```bash
python --version
python3 --version
py --version
```

You do not need all three commands. What matters is knowing which command in my environment actually runs Python.

Here, read it like this.

- On Windows, you may see `py`.
- On macOS or Linux, `python3` may be more natural.
- Even if `python` does not work, that does not necessarily mean Python does not exist at all.

In other words, you should not immediately treat `the command does not work` and `Python does not exist` as the same statement.

## 2. First Distinguish Whether It Is System Python or a Virtual Environment

The next important step is distinguishing what the current environment is.

There can be several Pythons even inside the same computer.

- system Python
- the virtual environment for project A
- the virtual environment for project B
- an interpreter separately chosen by the editor

Problem situation: Check why the state where the virtual environment is on and the state where it is off are different.
Input: the virtual environment inside the project folder and version-checking commands.
Expected output: it becomes visible that even commands that look the same can point to different Pythons depending on activation status.
Concept to check: `which Python runs` can change depending on virtual-environment state.

```bash
python --version
python -m pip --version
```

Here, the key point is not the version number itself, but whether `python` and `python -m pip` are looking at the same environment.

Here, we do not again write out operating-system-specific activation commands at length. That procedure can be revisited in P2-7.6. We only recover the point that `whether the virtual environment is on or not` affects both package installation and execution.

## 3. Even If `pip install` Succeeds, `import` Can Still Fail

This is the point where beginners most often get confused.

Problem situation: Assume a situation where package installation succeeds, but Python code still cannot import it.
Input: the installation command and the code `import numpy as np`.
Expected output: even if there is a successful installation message, if the current Python environment is different, import can still fail.
Concept to check: installation and usage are different stages and must be based on the same environment.

```bash
python -m pip install numpy
```

```python
import numpy as np
```

These two stages are connected, but they are not the same action.

- installation: prepare the package in the current Python environment
- import: load that package in the current Python code

Therefore, all of the following cases are possible.

- It was installed into system Python, but it is absent in the virtual-environment Python.
- It was installed into virtual environment A, but it is absent in virtual environment B.
- It was installed in Colab, but it is absent on the local PC.

That is why saying only `I installed it, but it still does not work` is not enough. The more accurate question is `am I now running the code in the very Python environment where I installed it?`

## 4. A PATH Problem May Be a Command-Mapping Problem, Not an Installation Problem

If you separately looked at environment variables in P2-7.8, then here connect PATH to `the list that determines where the terminal looks for commands to execute`.

There are cases where installation is complete on Windows, but the `python` command cannot be found. On macOS or Linux as well, only `python3` may be connected rather than `python`.

At that point, instead of immediately suspecting Python code or `pip` options, first suspect command mapping.

Here, follow the following checking order first.

1. Does `python --version` work?
2. If not, does `python3 --version` work?
3. If on Windows, does `py --version` work?
4. Have I confirmed which command actually points to Python?

Here, we do not cover operating-system-specific procedures for editing PATH directly. For such detailed procedures, it is safer to follow real project environment documents or official documentation.

## 5. Distinguish Permission Problems from Environment Problems

When package installation fails, it does not always mean the package name is wrong. It may be a permission problem.

For example, if you try to install into a system area, it may fail because there is no write permission. In that situation, a virtual environment is not just a convenience feature. It is a device for separating packages by project and reducing conflicts with the system area.

Here, remember the following criteria.

- If installation into the whole system is blocked, it may be a permission problem.
- For project practice, installing inside a virtual environment is safer.
- A permission error and `ModuleNotFoundError` are not the same problem.

In other words, do not bundle everything under the one phrase `installation does not work`. You need to separate `can it not find the command?`, `is there no permission?`, and `was it installed into another environment?`

## 6. When a Problem Appears, Do Not Reinstall Immediately; Check in Order

The most common mistake when installation feels tangled is repeatedly mixing several installation commands. That only makes it harder to know which environment is the current reference.

First, inspect in the following order.

1. Which terminal did I open now?
2. Where is the current working folder?
3. Which of `python`, `python3`, and `py` works?
4. Is the virtual environment on?
5. Does `python -m pip` run based on the current Python?
6. Are the necessary packages actually installed in that environment?
7. If it still does not work, only then go back to installation or Troubleshooting in the official documentation.

The reason this order matters is that many problems are solved not by reinstalling, but by the fact that `I had been looking at the current environment incorrectly`.

If you compress it into one table again:

| Checking order | Why look at it first |
| --- | --- |
| Check Python command | To see whether Python itself is being recognized |
| Check virtual environment | To see which environment is being used |
| Check `python -m pip` | To see whether the installation target is the same as the current Python |
| Check `import` | To see whether installation and usage are actually connected |
| Then judge reinstallation | To avoid making the already existing environment more tangled |

## Where Should You Go Back?

After reading this section, rather than memorizing more new commands immediately, it is better to reconnect which question in the main flow you should reread.

| Question that is blocking now | Main section to go back to first |
| --- | --- |
| It is getting blurry again why virtual environments were separated | P2-7.4 Virtual Environments and Packages |
| It is getting blurry again why requirements and reproducibility records are needed | P2-7.5 Dependency and Reproducibility |
| The command differences among Windows, macOS, and Linux themselves feel unfamiliar | P2-7.6 Using Terminals |
| I need to judge again whether Python installation is needed and when | P2-7.7 When Is Python Installation Needed? |
| Expressions such as PATH, environment variables, and pipes feel unfamiliar again | P2-7.8 Shell Scripts and Environment Variables |

## Case Study

### Case 1. NumPy Was Installed, but the Example File Still Says It Is Missing

Suppose a learner runs `python -m pip install numpy` in the terminal. The installation log also looks successful. But when running `example.py`, the message `ModuleNotFoundError: No module named 'numpy'` appears.

In this scene, people usually suspect first, `did installation fail?` But the more common cause is not installation itself, but an environment mismatch. For example, NumPy may have been installed into system Python, while the actual file execution may be using another interpreter instead of the project's virtual environment.

So what you should look at first is not only `did installation succeed?`, but `is the Python running example.py the same as the Python on which I just ran pip install?` If you check `python --version` and `python -m pip --version` in the same terminal and review again whether the virtual environment is activated, you can narrow down the cause much faster.

The result that must be checked in this case is not only whether NumPy is installed, but `is the Python environment I am looking at now aligned as one?`

### Case 2. On Windows, `python` Does Not Work, but `py` Does

A Windows learner types `python --version`, and the terminal says the command cannot be found. So the learner may think Python installation completely failed. But `py --version` works normally.

In this case, the core is not a Python code error, but the command-mapping method. On Windows, depending on the installation method, `py` may appear to be the default entry point instead of `python`. In other words, it is not that Python does not exist, but that the command used in the current terminal to call Python may be different.

The result that must be checked in this case is not the fact that `python` does not work itself, but finding out `which command in my environment actually opens the Python interpreter?`

## Short Return Table

| Blocking scene | Where to return first |
| --- | --- |
| It is vague again why virtual environments are used | `P2-7.4`, `P2-7.5` |
| The command differences among Windows/macOS/Linux feel unfamiliar | `P2-7.6` |
| I need to judge again whether Python installation is needed | `P2-7.7` |
| PATH, environment variables, and shell syntax feel unfamiliar | `P2-7.8` |

## Checklist

- Can you explain which of `python`, `python3`, and `py` works in my environment?
- Can you distinguish system Python from virtual-environment Python?
- Can you explain that `pip install` success and `import` success are different stages?
- Can you distinguish a PATH problem from a package-missing problem?
- When a problem appears, can you recall the checking order before jumping straight to reinstallation?
- Can you first divide a local Python environment problem into `command`, `environment`, and `installation location`?

## Sources and References

- Python Software Foundation, [Python Setup and Usage](https://docs.python.org/3/using/index.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used as background for the local environment checking order by confirming the documentation structure for platform-specific Python setup and interpreter invocation.
- Python Software Foundation, [Using Python on Windows](https://docs.python.org/3/using/windows.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to confirm that Python execution commands and installation methods on Windows have separate official guidance.
- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to confirm that Python execution commands and installation paths on Unix/Linux can differ by environment.
- Python Software Foundation, [venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-19. Used to support checking virtual-environment activation together with package installation location.
