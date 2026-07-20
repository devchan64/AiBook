# P2-7.3 Python Interpreter and Script

> Section ID: `P2-7.3`
> Version: `v2026.07.20`

In P2-7.2, we looked at terminal, shell, and working directory. Now we look at how Python code is actually executed in that terminal.

The easiest place to get confused is the following.

```text
python
python example.py
print("hello")
```

All three lines are related to Python, but they are not the same kind of sentence. Some are terminal commands, and some are Python code. Here we fix that boundary clearly.

Here we explain the distinction among `Python interpreter`, `script`, and `interactive mode`. Even when later Sections meet commands such as `python -m pip ...` or notebook execution again, how Python reads code and in what place it reads it reconnects on top of the explanation here.

Rather than learning Python syntax itself, this Section focuses on distinguishing where and how Python code is executed. If you secure the differences among interpreter, interactive execution, and script execution here, then later when you see virtual environments, package installation, and data-file execution, you can first divide whether `the command was written wrong` or `the execution place was chosen wrong`.

| What to secure in this Section now | The question that follows immediately next | Where it is used again later |
| --- | --- | --- |
| The difference between interactive execution and script execution | It continues into virtual environments and package-installation commands in P2-7.4. | It is used again later whenever distinguishing execution style and file structure in all Python practice. |
| The criterion for not mixing terminal commands and Python code | After P2-7.5, it continues into data files and library usage. | It becomes the basis when interpreting the difference between Colab and a local environment. |
| The place distinction among `python`, `python file.py`, and `python -m ...` | It is reinforced in P2-7.6 and P2-7.7 through OS-specific installation and execution procedures. | It repeats in package installation, module execution, and project-script execution. |

| Term | Meaning to secure first in this Section |
| --- | --- |
| Python interpreter | the program that reads and executes Python code |
| interactive mode | the execution mode where we type one line at a time and immediately check the result |
| script | the execution style where several lines of code are saved in a file and run at once |
| prompt | the marker that shows where to type now |
| `python -m ...` | a way of asking Python to execute a specific module |

## Goals of This Section

- You can explain the `Python interpreter` as the program that reads and executes Python code.
- You can explain the difference between `interactive mode` and `script` execution.
- You can distinguish terminal commands from Python code.
- You can explain at an introductory level how execution in Colab/Jupyter code cells differs from execution in the terminal.
- You can explain that even with the same code, if the execution style changes, the ways of saving, rerunning, and sharing also change.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| The interpreter is the program that reads and executes Python code | Only when we distinguish code from the execution program can we see the difference in execution style. | It is enough if you can explain the role of the interpreter in one sentence. |
| Script execution and interactive execution differ in execution unit | Because the ways of saving, rerunning, and sharing differ. | You can distinguish file-unit execution from one-line execution. |
| Terminal commands and Python code are entered in different places | Even if they all look like `Python-related sentences`, the interpreting agent differs. | Secure the feel of distinguishing shell prompts from Python prompts. |

## Why Did Interpreter and Script Appear Together?

Python is difficult to understand as only `a language that runs programs saved in files from the beginning`. The official Python FAQ explains Python as an interpreted, interactive, object-oriented programming language. It also explains that Guido van Rossum started Python from the experience of implementing the ABC language and working on the Amoeba distributed operating system, and that there was a need for a more extensible scripting language in a situation where it was difficult to handle system-administration work only with C programs or Bourne shell scripts.

If we reduce that background from a beginner's point of view, it becomes the following.

- shell scripts: good for automating by chaining operating-system commands
- compiled languages such as C: fast and powerful, but can feel heavy for small automation and experiments
- Python: provides readable high-level syntax together with interactive execution and script execution

So in Python, two usage styles naturally appear together.

- interactive execution: directly test a small expression
- script execution: save several lines of work in a file and run them repeatedly

The reason Python is often met in AI learning is also connected to this point. It is easy to immediately check formulas with small code, and if the experiment becomes a little longer, it is easy to leave it in a file or notebook. Here, however, we do not go deeply into Python language history, but keep only the feel for why the execution styles of interpreter and script are used together.

## The Interpreter Is the Program That Reads and Executes Code

The `Python interpreter` is the program that reads and executes Python code. The official Python documentation explains that the interpreter can be invoked from the command line, and if it is started without a file name or standard input, it enters `interactive mode`.

Here we understand it like this.

- Python code: a command written by a person
- Python interpreter: the program that reads and executes Python code

The following is Python code.

Problem situation: check what the simplest code read by the Python interpreter looks like.
Input: one line of Python code that prints a string.
Expected output: if executed, `hello` is printed.
Concept to check: the interpreter is the program that reads and executes Python sentences like this.

```python
# This Python statement is saved in a script file and then executed.
print("hello")
```

This code does not work by text alone. It runs only when the Python interpreter reads it.

## Interactive Mode Is the Style of Checking One Line at a Time

If you run Python in the terminal, you can use `interactive mode`.

```bash
python
```

Depending on the environment, the command name may be `python3`.

```bash
python3
```

When you enter interactive mode, you usually see the `>>>` prompt. The official Python documentation also explains that the default prompt in interactive mode is `>>>`.

Problem situation: in interactive mode, see how one-line calculation and output are checked immediately.
Input: the calculation `1 + 2` and the call `print("hello")`.
Expected output: `3` and `hello` are immediately printed.
Concept to check: interactive mode is an execution style for testing calculations one line at a time.

```pycon
>>> 1 + 2
3
>>> print("hello")
hello
```

Interactive mode is good for checking calculations immediately.

Interactive mode fits the following situations especially well.

- checking a short calculation
- trying out syntax
- printing a small value immediately

But what you type in interactive mode usually does not remain in a file. To run it again, you have to type it again. So when several lines of code must be run repeatedly, we use a `script` file.

## A Script Is an Execution Unit Saved in a File

A `script` is code saved in a file for execution. Python files usually use the `.py` extension.

For example, suppose the following contents were saved in a file called `hello.py`.

Problem situation: see the form of saving several lines of Python code in a file and running it as a script.
Input: the two lines of Python code inside `hello.py`.
Expected output: when executed, `hello` and the result of `1 + 2` are printed in order.
Concept to check: a script is the style of saving Python code as a file unit and running it repeatedly.

```python
# A script runs multiple statements from top to bottom.
print("hello")
print(1 + 2)
```

If you are in the same folder in the terminal, you can run it like this.

```bash
python hello.py
```

Depending on the environment, you may also use the following command.

```bash
python3 hello.py
```

Script execution differs from interactive execution.

| Execution style | Input location | Advantage | Point to watch |
| --- | --- | --- | --- |
| interactive execution | `>>>` prompt | good for checking one line at a time immediately | entered contents may not remain as a file |
| script execution | `.py` file | easy to save, modify, rerun, and share | need to check the current working directory and file path |

In AI learning, sometimes we check small calculations immediately, and sometimes we run the same code several times while editing it. That is why we meet both styles.

## Do Not Mix Terminal Commands and Python Code

The distinction that most often gets confused is this.

```bash
python hello.py
```

This is a terminal command. It is not a sentence written inside a Python code file.

By contrast, the following is Python code.

Problem situation: check again that even the same `print("hello")` works only in the Python execution place, not at the shell prompt.
Input: Python code that prints a string.
Expected output: if executed as Python code, `hello` is printed.
Concept to check: terminal commands and Python code should be distinguished not by how the sentence looks, but by where it is entered.

```python
# The same Python statement can also run inside a code cell.
print("hello")
```

This sentence is not a command typed directly into the terminal. Of course, it can be entered inside the Python interactive `>>>` prompt. But in the general shell prompt, it is interpreted not as Python code but as a shell command.

Here the habit of distinguishing prompts matters.

- shell prompt that looks like `$` or `%`: enter terminal commands
- `>>>` Python prompt: enter Python code
- Colab/Jupyter code cell: basically enter Python code

## A Code Cell Sits Between Script Execution and Interactive Execution

The `code cell` of Colab or Jupyter executes Python code in cell units.

Problem situation: check again the smallest execution of Python code in a notebook code cell.
Input: one line of Python code that prints a string.
Expected output: `hello` is printed as the cell execution result.
Concept to check: a code cell shows immediate results like interactive execution while also leaving a record in the notebook.

```python
# The output-checking code is the same whether it runs from a terminal or a code cell.
print("hello")
```

A code cell is good for immediately checking results like interactive execution. At the same time, code, results, and explanations can be left together in the notebook file. So it is convenient for learning.

But a code cell also differs from a script file. If cell execution order changes, the result may change, and a variable created in one previous cell may be used by a later cell.

If we separate the three execution places again, they are as follows.

- interactive mode: quickly check one line at a time
- script file: save the whole file and run it repeatedly
- notebook code cell: leave explanation and results together while executing in cell units

Later, when practice gets longer, the situation `it worked in the notebook, but fails when moved into a script` can appear. At that time, we have to separately check cell execution order, file path, needed imports, and package installation state.

## `python -m` Is a Way of Executing a Module

In the terminal, you often meet the following command.

```bash
python -m pip install numpy
```

Here `-m` is a way of asking Python to execute a specific `module` like a script. The official Python documentation explains that the form `python -m module` runs a library module as a script.

Here, understand it like this.

- `python hello.py`: runs a file
- `python -m pip ...`: runs the module called `pip` through Python

`pip` and package installation are revisited in P2-7.4. Here, remember only that `-m` is not Python code syntax, but an execution option given from the terminal to the Python interpreter.

## If the Execution Style Changes, What You Check Also Changes

Even with the same Python code, the things to check change depending on the execution style.

| Situation | What to check first |
| --- | --- |
| it does not work in interactive mode | Am I inside the `>>>` prompt now? |
| the script file does not open | Is the file in the current working directory? |
| the `python` command cannot be found | Is Python installed, and is the command name correct? |
| it works in Colab but not locally | Are the same file and package present locally? |
| it fails when moved into a script | Is there a value that had depended on notebook cell execution order? |

This Section does not cover every error solution. What matters is the perspective that `if the execution style changes, the cause of the error must also be narrowed differently`.

## View It Through a Case

### Case 1. Where Should `print("hello")` Be Typed?

Suppose a person learning Python for the first time followed a tutorial and typed `print("hello")` directly into the terminal. In some environments it may look as if it works, and in others it may produce a message saying the command cannot be found, causing confusion.

The standard a person was using is usually close to `it is a sentence related to Python, so it should work wherever I put it`. But in reality, the shell prompt, the Python interactive prompt, and the Colab code cell each use different input languages.

This is why this Section separates `interpreter`, `interactive mode`, `script`, and `code cell`. Even if they look like the same content, `python hello.py` is a terminal command, `print("hello")` is Python code, and the cause of the error differs depending on in which place it was entered.

The confirmable result appears by looking at the prompt. If `print("hello")` works inside `>>>` but not in the general shell prompt, then the problem is not Python syntax, but choosing the wrong execution place.

## Checklist

- You can explain the Python interpreter as the program that reads and executes Python code.
- You can explain that in interactive mode, Python code is entered at the `>>>` prompt.
- You can explain that a script is an execution unit saved in a `.py` file.
- You can distinguish that `python hello.py` is a terminal command, while `print("hello")` is Python code.
- You can explain that Colab/Jupyter code cells execute Python code in cell units.
- You can explain that in `python -m pip ...`, `-m` is an execution option given from the terminal to the Python interpreter.
- You can explain that when running Python, you should first check whether the current place is a shell, a Python prompt, or a code cell, and whether you are executing one line, a file, or a notebook cell.

## Sources and References

- Python Software Foundation, [General Python FAQ](https://docs.python.org/3/faq/general.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to support the description of Python as an interpreted, interactive programming language and to confirm Guido van Rossum's early development context.
- Python Software Foundation, [Using the Python Interpreter](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm interpreter invocation, interactive mode, and script-file execution.
- Python Software Foundation, [Command line and environment](https://docs.python.org/3/using/cmdline.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to confirm command-line execution forms such as `python script.py`, `python -c`, and `python -m module-name`.
