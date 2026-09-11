# P2-7.3 Python Interpreter and Script

> Section ID: `P2-7.3`
> Version: `v2026.09.08`

`python` is a terminal command that opens interactive Python; `python hello.py` runs code saved in a file. `print("hello")` is Python code read by the interpreter. The execution method determines where to enter code and how results are recorded.

## Background of Interactive and Script Execution

Python is difficult to understand as only `a language that runs programs saved in files from the beginning`. The official Python FAQ explains Python as an interpreted, interactive, object-oriented programming language. It also explains that Guido van Rossum started Python from the experience of implementing the ABC language and working on the Amoeba distributed operating system, and that there was a need for a more extensible scripting language in a situation where it was difficult to handle system-administration work only with C programs or Bourne shell scripts.

If we reduce that background from a beginner's point of view, it becomes the following.

- shell scripts: good for automating by chaining operating-system commands
- compiled languages such as C: fast and powerful, but can feel heavy for small automation and experiments
- Python: provides readable high-level syntax together with interactive execution and script execution

So in Python, two usage styles naturally appear together.

- interactive execution: directly test a small expression
- script execution: save several lines of work in a file and run them repeatedly

This also helps explain Python’s use in AI learning: small code can immediately check formulas, while longer experiments can be saved in files or notebooks.

## The Python Interpreter

The Python interpreter reads and executes Python code. The official documentation explains that it can be invoked from the command line; starting it from a terminal without a file or other execution options enters interactive mode.

## Interactive Mode and the Prompt

If you run Python in the terminal, you can use `interactive mode`.

```bash
python
```

Depending on the environment, the command name may be `python3`.

```bash
python3
```

When you enter interactive mode, you usually see the `>>>` prompt. The official Python documentation also explains that the default prompt in interactive mode is `>>>`.

Entering an expression or function call after `>>>` immediately displays the result. The `>>>` below is a prompt marker, not code to type.

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

## Scripts Saved in Files

A `script` is code saved in a file for execution. Python files usually use the `.py` extension.

For example, suppose the following contents were saved in a file called `hello.py`.

Save these two lines in `hello.py` and run it to print `hello` and `3` in order.

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

## Shell and Python Input Locations

At the shell prompt, `python hello.py` requests execution of a file. At Python’s `>>>` prompt, enter Python code such as `print("hello")`.

Entering a file-execution command in interactive Python produces an error such as:

```pycon
>>> python hello.py
  File "<stdin>", line 1
    python hello.py
           ^^^^^
SyntaxError: invalid syntax
```

The file `hello.py` does not need to be changed. Enter `exit()` at `>>>` to return to the shell, then run `python hello.py`. Error-message details can vary by Python version.

## Notebook Cells and Execution State

The `code cell` of Colab or Jupyter executes Python code in cell units.

A code cell displays results immediately, like interactive execution, while preserving a notebook record.

```python
# output-checking code is the same whether it runs from a terminal or a code cell.
print("hello")
```

A code cell is good for immediately checking results like interactive execution. At the same time, code, results, and explanations can be left together in the notebook file. So it is convenient for learning.

But a code cell also differs from a script file. If cell execution order changes, the result may change, and a variable created in one previous cell may be used by a later cell.

If we separate the three execution places again, they are as follows.

- interactive mode: quickly check one line at a time
- script file: save the whole file and run it repeatedly
- notebook code cell: leave explanation and results together while executing in cell units

Later, when practice gets longer, the situation `it worked in the notebook, but fails when moved into a script` can appear. At that time, we have to separately check cell execution order, file path, needed imports, and package installation state.

## The -m Module Execution Option

In the terminal, you often meet the following command.

```bash
python -m pip install numpy
```

Here `-m` is a way of asking Python to execute a specific `module` like a script. The official Python documentation explains that the form `python -m module` runs a library module as a script.

The two commands specify their execution targets differently.

- `python hello.py`: runs a file
- `python -m pip ...`: runs the module called `pip` through Python

`-m` is an interpreter option, not Python code syntax. `python -m pip` runs pip in the Python specified at the beginning of the command.

## Checking Errors by Execution Method

Even with the same Python code, the things to check change depending on the execution style.

| Situation | What to check first |
| --- | --- |
| it does not work in interactive mode | Am I inside the `>>>` prompt now? |
| the script file does not open | Is the file in the current working directory? |
| the `python` command cannot be found | Is Python installed, and is the command name correct? |
| it works in Colab but not locally | Are the same file and package present locally? |
| it fails when moved into a script | Is there a value that had depended on notebook cell execution order? |

## A Variable Left Only in the Notebook

If an earlier notebook cell runs `name = "Mina"`, another cell can run `print(name)` to print `Mina`. But copying only `print(name)` to `hello.py` raises `NameError` because a fresh Python execution has no `name` defined.

```python
# Define the required value before using it in a fresh execution.
name = "Mina"
print(name)
```

Saving both lines lets the script print `Mina` too. When moving notebook code into a file, include the variable definitions and imports used by the output cell.

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
