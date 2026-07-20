# P2-7.8 Supplemental Learning: Reading Shell Scripts, Pipes, Redirection, and Environment Variables

> Section ID: `P2-7.8`
> Version: `v2026.07.20`

In P2-7.2 and P2-7.6, we covered opening a terminal and checking the current location. But once you follow real learning materials, you quickly encounter more unfamiliar expressions.

```bash
python train.py > train.log
cat data.csv | python inspect.py
export OPENAI_API_KEY=...
```

Here, we explain the basic criteria for reading `shell scripts`, `pipes`, `redirection`, and `environment variables`. This supplement organizes the standard for reading what kind of action these symbols represent when you encounter them in real documents.

In this supplement, rather than becoming able to freely use all of this syntax, we focus on making you able to at least read `what kind of action it is` when you see these expressions in documents or tutorials later.

## At First, These Are the Only Things You Need to Read

When you come back later while redoing practice or following a tutorial, it is enough to first recall the following four lines.

- `|` is a connection that passes the result of the previous command to the next command.
- `>` and `<` are notations that change the direction of input or output toward files.
- `KEY=...` or `export ...` is likely a scene where environment variables are being used to pass configuration values outside the code.
- If you see `sudo`, `rm`, exposure of secret values, or file overwriting, do not run it immediately before you understand what it means.

In other words, even if you do not reread this whole section from the beginning, if you first hold onto the four words `connection`, `direction`, `configuration value`, and `warning sign`, you can read an unfamiliar line much more safely.

| Term | Meaning to establish first in this section |
| --- | --- |
| shell script | A record of execution where multiple terminal commands are grouped together in a file. |
| pipe | A connection that passes the output of a previous command as the input to the next command. |
| redirection | Notation that changes the input/output direction of the screen or files. |
| environment variable | A configuration value read by a program from the outside execution environment. |
| warning sign | Something to check first, such as deletion, privilege escalation, network calls, or exposure of secret values. |

## First Reading Criteria: Reading Shell Scripts, Pipes, Redirection, and Environment Variables

- You can explain a shell script as a text file that groups multiple commands for execution.
- You can explain a pipe as a connection that passes the output of one command as the input of another.
- You can explain redirection as a way of sending screen output into a file or reading file contents as input.
- You can explain an environment variable as a named configuration value shared by the execution environment.
- When you see an unfamiliar command, you can first check for deletion, privilege escalation, network calls, and exposure of secret values.

## Four Things to Hold First

| Expression | The first sense to read |
| --- | --- |
| shell script | A way of writing several commands into one file |
| pipe `|` | A connection that passes the result of one command to the next |
| redirection `>` `<` | Symbols that change the input/output direction of the screen or files |
| environment variable | A configuration value read by a program from outside |

## A Shell Script Is a File That Bundles Commands

A shell script is something where commands to be executed in a shell are written in order into a text file. Here, understand it as `commands you used to type line by line in the terminal, gathered into a file so they can be run repeatedly`.

For example, you can write the following.

```bash
pwd
ls
python hello.py
```

This file can be read as a record bundling together `check current location -> check file list -> run Python`.

Read a shell script less as `an entirely new programming language` and more as `terminal commands gathered into several lines`.

## A Pipe Passes the Output of One Command to the Next Command

A pipe is written with the `|` symbol. Here, read it with the sentence `the result that the previous command was going to show on the screen is received by the next command like input and then processed further`.

For example, you can read the following line as meaning that `python inspect.py` receives and processes the preceding content.

```bash
cat data.txt | python inspect.py
```

For now, you do not need to know the detailed behavior of `cat` or `inspect.py`. The key point is that `|` means `connection`.

Why pipes are useful can be seen in the following table.

| Situation | What the pipe does |
| --- | --- |
| You want to see only the needed lines from a long output | It passes the previous command's result to the next command's filter |
| You want another program to read file contents immediately | It passes the file contents directly to the next processing step without printing them on screen |
| You want to write multiple processing stages in one line | It connects commands in order |

At this stage, it is more important to read `ah, it is passing the result to the next stage` when you see a pipe in documentation than to use pipes heavily yourself.

## Redirection Changes the Direction of Input and Output

Redirection is changing the destination toward which output or input goes.

The first notations you usually encounter are the following two.

| Notation | Meaning at an introductory level |
| --- | --- |
| `>` | Send output that would have been shown on the screen into a file |
| `<` | Read file contents as input |

For example, the following command can be read as sending what would appear on the screen into a file called `train.log`.

```bash
python train.py > train.log
```

The following command can be read as reading `input.txt` and feeding it into the program.

```bash
python read.py < input.txt
```

What matters here is not memorizing the symbols themselves, but the sense of `direction`.

- `>` generally sends something outward
- `<` generally reads something inward

The especially important warning here is the following.

- It may overwrite the output file
- You should visually check where the command is saving its result

In other words, when redirection is attached, it is safer to first check `is this command changing files as well as showing something on screen?`

## An Environment Variable Is a Configuration Value That a Program Reads from Outside

An environment variable is a named value that the execution environment passes to a program. Here, understand it as `a configuration value that the program reads from outside the execution environment rather than writing directly inside the code`.

For example, values such as an API key, a data path, or a mode selection may be passed through environment variables.

```bash
export OPENAI_API_KEY=...
python app.py
```

The key point of this example is that when `python app.py` runs, it can read a value called `OPENAI_API_KEY` from the outside environment.

In Windows PowerShell, the notation can look a little different. But at this stage, the concept that `an environment variable is a configuration value outside the body of the code` matters more than operating-system-specific syntax differences.

## Why Do These Expressions Appear So Often in AI Learning Documents?

AI learning documents and project examples often deal with files, logs, data, secret values, and execution environments. So even within one terminal line, the following things often happen together.

- reading files
- saving results
- connecting commands
- passing configuration values

In other words, pipes, redirection, and environment variables are not advanced decoration. They are closer to `basic notation for dealing with the execution environment`.

## Checkpoints to Inspect First

When you see an unfamiliar terminal command, rather than trying to interpret every meaning, first check the following.

1. Is there a command that deletes files?
2. Does it need administrator privileges?
3. Is it downloading something from the network?
4. Is it exposing an API key or other secret value directly?
5. Is it overwriting output into a file?

It is also fine to read it through the following table.

| Signal | Question to check first |
| --- | --- |
| `sudo` | Is administrator privilege really necessary? |
| `rm`, `del`, `Remove-Item` | Is it a command that deletes files? |
| `>` | Into which file is it saving or overwriting output? |
| `|` | Is it passing the previous result into the next stage? |
| `KEY=...`, `TOKEN=...` | Is it exposing a secret value directly? |

## What Should You Be Able to Read Now?

After finishing this supplement, you do not need to be able to freely write shell scripts immediately. The level needed now is about the following.

- When you see `|`, `>`, and `<`, you know that they are notation changing the direction of input and output
- You know that environment variables are configuration values outside the code
- You know that shell scripts are bundles of commands
- You inspect dangerous commands first instead of copying and running them casually

## Case Study

### Case 1. When a Single Tutorial Command Line Suddenly Looks Dangerous

Suppose a learner sees commands such as `python train.py > train.log` or `export OPENAI_API_KEY=...` in an internet tutorial. Because there are many symbols, it can feel like an entirely new syntax that has to be memorized.

The human default attitude is usually close to `for now, let me just copy and run it`. But in a line like this, different actions such as output saving, file overwriting, environment-variable passing, and command connection can all be present at once. So if you run it without knowing the meaning, you risk overwriting a log file, leaving a secret value exposed, or following a line mixed with dangerous deletion commands.

The level to aim for here is not the stage where you can freely use `pipes`, `redirection`, `environment variables`, and `shell scripts`, but the stage where you can at least read `what kind of action it is`. In other words, if you only have the sense that `|` is connection, `>` is output-direction change, and `KEY=...` is passing an outside configuration value, you can already read much more safely.

The confirmable result is whether you can split and read one command line by function. For example, if you can look at `python train.py > train.log` and explain `it runs training, and instead of screen output it saves the result into a log file`, then you have moved one step beyond the stage of copying and running commands without thinking.

## Checklist

- Can you explain a shell script as a file bundling multiple commands?
- Can you explain a pipe as a connection that passes the output of one command as the input of the next?
- Can you explain redirection as notation that changes the direction of input and output?
- Can you explain an environment variable as a configuration value outside the code?
- Do you remember that `sudo`, `rm`, `>`, `|`, and exposure of secret values should be checked first?
- Can you explain shell scripts, pipes, redirection, and environment variables together as `the language for reading the execution environment`?

## Sources and References

- GNU Project, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, checked 2026-07-20. Used to confirm Bash's shell role, pipelines, redirection, and variable/environment-variable syntax.
- Microsoft Learn, [about_Pipelines](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_pipelines){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that `|` is a pipeline operator that sends results from one command to the next in PowerShell.
- Microsoft Learn, [about_Redirection](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_redirection){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that redirection operators such as `>`, `>>`, and `n>` send or append output streams to files in PowerShell.
- Microsoft Learn, [about_Environment_Variables](https://learn.microsoft.com/powershell/module/microsoft.powershell.core/about/about_environment_variables){: target="_blank" rel="noopener noreferrer" }, PowerShell 7.6 documentation, checked 2026-07-20. Used to confirm that environment variables are string configuration values used by the operating system and programs and can be inherited by child processes.
