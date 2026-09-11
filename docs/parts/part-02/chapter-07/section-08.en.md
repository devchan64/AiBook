# P2-7.8 Supplementary Learning: Reading Shell Execution Flow

> Section ID: `P2-7.8`
> Version: `v2026.09.08`

In a shell, `|` connects one command’s output to the next command’s input. `>` and `<` connect output and input to files, while environment variables pass configuration values to programs. The shell commands below use Bash and assume Python is available as `python`.

## Standard Input and Standard Output

Command-line programs can receive data through standard input and send results through standard output. In direct terminal use, these usually connect to the keyboard and screen, but can be redirected to files or other programs.

Save the following code as `read_numbers.py`. It reads one number per input line and prints the sum. Input `10`, `20`, `30` produces `60`.

```python
import sys

# Read integers line by line from standard input and sum them.
numbers = [int(line) for line in sys.stdin if line.strip()]
print(sum(numbers))
```

In Bash, create the input file `numbers.txt` using the following command. `printf` converts `\n` into a newline.

```bash
printf '10\n20\n30\n' > numbers.txt
```

## Connecting Commands with a Pipe

`cat` sends file contents to standard output. Connecting it with `|` makes those contents the Python program’s standard input.

```bash
cat numbers.txt | python read_numbers.py
```

The output is `60`. The programs exchange data directly, without displaying the file for a person to retype. The receiving program must be written to read standard input for this connection to be useful.

A pipe does not simply mean execute commands in sequence. It connects the first command’s standard output to the next command’s standard input. Standard error, used for error messages, is not included by default.

## Connecting Files to Input and Output

`<` connects the same file to Python’s standard input without using `cat`.

```bash
python read_numbers.py < numbers.txt
```

Add `>` to save the result to `total.txt` instead of the screen.

```bash
python read_numbers.py < numbers.txt > total.txt
```

On success, the sum is not displayed on screen; `total.txt` contains `60` and a newline. Check it with `cat total.txt`.

| Bash notation | Action |
| --- | --- |
| `< input.txt` | Connects the file to standard input |
| `> output.txt` | Writes standard output to the file, overwriting existing content |
| `>> output.txt` | Appends standard output to the file |
| `2> errors.log` | Writes standard error to a separate file |

`python train.py > train.log` likewise saves only standard output. Do not assume all error messages also go into that file. File paths are interpreted relative to the working directory.

## Saving Commands as a Shell Script

Save commands to repeat in `run_summary.sh`.

```bash
python read_numbers.py < numbers.txt > total.txt
cat total.txt
```

From the folder containing the three files, run this command. Bash reads the script, saves the sum, and prints it.

```bash
bash run_summary.sh
```

A shell script is a command file interpreted by a shell. The interpreting program differs from that used for a `.py` file containing Python code.

## Passing Settings with Environment Variables

An environment variable is a name-value pair passed when a program runs. For example, it can specify a data folder outside the code.

Run this command in Bash.

```bash
export BOOK_DATA_DIR="./data"
```

`export` passes the value to child processes subsequently started by this shell. It does not change the environment of other terminals already running.

Save this code in `show_config.py` and run `python show_config.py` in the same shell to print `./data`.

```python
import os

# Print the fallback when the environment variable is not set.
print(os.environ.get("BOOK_DATA_DIR", "not set"))
```

In Windows PowerShell, set the environment variable as follows.

```powershell
$env:BOOK_DATA_DIR = "./data"
python show_config.py
```

Environment variable values are strings. Setting a folder path does not create the folder. Secrets such as API keys can also be passed this way, but must not be left in code or output logs.

## Changing Numbers and Output Storage

Changing the last number in `numbers.txt` from `30` to `40` changes the sum from `60` to `70`. Run this command to leave only the new sum `70` in `total.txt`.

```bash
python read_numbers.py < numbers.txt > total.txt
```

With the same input, change `>` to `>>` and run again; the file now contains two lines of `70`. The calculation code is unchanged; only the shell’s output connection differs.

## Checking What a Command Changes

| Notation | What to check |
| --- | --- |
| `>` | The path of the file to overwrite |
| `rm`, `del`, `Remove-Item` | Files and folders to delete |
| `sudo` | The command to run with elevated privileges |
| Environment variables containing secrets | Whether values remain in command history, logs, or the repository |

PowerShell pipelines can also pass objects between commands, and their syntax is not identical to Bash. In particular, do not copy the `<` input redirection above directly into PowerShell.

## Checklist

- You can distinguish the programs that interpret shell scripts and Python scripts.
- You can explain that `|` connects standard output to standard input.
- You can distinguish file input, overwriting, and appending with `<`, `>`, and `>>`.
- You can explain that standard output and standard error are separate streams.
- You can read a setting passed through an environment variable in Python.
- You can check how file contents change when input numbers or output connections change.

## Sources and References

- GNU Project, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, checked 2026-07-20. Used to confirm Bash's shell role, pipelines, redirection, and variable/environment-variable syntax.
- Microsoft Learn, [about_Pipelines](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_pipelines){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that `|` is a pipeline operator that sends results from one command to the next in PowerShell.
- Microsoft Learn, [about_Redirection](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that redirection operators such as `>`, `>>`, and `n>` send or append output streams to files in PowerShell.
- Microsoft Learn, [about_Environment_Variables](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that environment variables are string configuration values used by the operating system and programs and can be inherited by child processes.
