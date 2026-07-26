# P2-7.2 Terminal, Shell, and Working Directory

> Section ID: `P2-7.2`
> Version: `v2026.07.26`

In P2-7.1, we first looked at the place where code runs. Now we look at the first screen a reader usually meets when entering commands on a local PC.

When beginning programming, the following sentences appear often.

For example, introductory documents often contain sentences like these.

- Open the terminal and run it.
- Move to the project folder.
- Enter the command below.

These sentences are short, but several concepts are packed into them at once. If you cannot distinguish `terminal`, `shell`, `command`, and `working directory`, you often end up in the situation `I definitely typed the same thing, so why is it not working?`

Here we explain the basic distinction among `terminal`, `shell`, and `working directory`. Even when later Sections continue into Python execution, virtual-environment activation, and package-installation commands, the places where we type commands and the location from which they are interpreted reconnect on top of the explanation here.

Rather than learning every terminal feature by operating system, this Section focuses on building the minimum language needed to read and execute commands on a local PC. If you separate the roles of terminal, shell, and working directory here, then when you later see Python file execution, virtual environments, and package installation, you can first divide problems into code errors and location errors.

| What to secure in this Section now | The question that follows immediately next | Where it is used again later |
| --- | --- | --- |
| Distinguishing the roles of terminal, shell, and working directory | In P2-7.3, we see how Python files are actually executed. | It is reused later in every local practice when separating location problems from code problems. |
| Why `pwd`, `cd`, and `ls` are needed first | In P2-7.4, it continues into virtual environments and package-installation commands. | It repeats in the contexts of reading data files, running scripts, and moving to a project root. |
| The point that Colab shell and local terminal are not the same | We defer OS-specific differences and advanced shell syntax to the supplementary learning of P2-7.6 and P2-7.8. | It becomes the basis when reading practice-environment guidance after Part 3. |

| Term | Meaning to secure first in this Section |
| --- | --- |
| terminal | the window or app where we type commands and see results |
| shell | the program inside the terminal that reads, interprets, and runs commands |
| working directory | the folder used as the current base by the command |
| path | the string that points to where a file or folder is located |
| command | the execution sentence asking the shell to do something now |

## Core Criteria: Terminal, Shell, and Working Directory

- You can explain `terminal` as the screen where commands are entered and results are viewed.
- You can explain `shell` as the program that interprets and executes commands.
- You can explain that the words terminal and shell remain from older ways of using computers.
- You can explain `working directory` as the folder used as the current base by commands.
- You can explain why basic commands such as `pwd`, `cd`, and `ls` or `dir` are needed.
- When a command fails, you can first divide the issue into a code problem or a location problem.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| The terminal is the screen, and the shell is the program inside it that interprets commands | Confusion decreases only when the place of input and the interpreting agent are separated. | It is enough if you can explain terminal and shell as different roles. |
| The working directory determines the base location of commands | The same command can point to different files depending on the current location. | Secure the feel of separating location error from code error. |
| The first thing to check is the current location and the file list | Many failures begin from location problems rather than syntax. | You can explain the purpose of `pwd`, `cd`, and `ls` or their equivalents. |

## Why Do the Words Terminal and Shell Still Remain?

Terminal and shell are not names of recently created apps. Both keep traces of the era when many people used computers through text.

The early `terminal` was not an app inside a laptop like today. It was an input-output device connected to a central computer. Text-Terminal-HOWTO explains that real text terminals looked like a monitor and keyboard but displayed not pictures but a text-based `command-line interface`, and that they were widely used for connecting to mainframe computers in the late 1970s and 1980s. Later, real hardware terminals decreased, but today's terminal apps are closer to `terminal emulators` that imitate that behavior in software.

`Shell` is also an old concept. The GNU Bash manual explains that Bash is the shell, or `command language interpreter`, for the GNU operating system. It also explains that a Unix shell is both a command interpreter and a programming language.

You do not need to memorize the whole history. If you remember the flow below, you can explain why the words terminal and shell remain.

- past: people entered commands to a central computer through a separate terminal device
- present: terminal apps provide that text-based way of working through software
- shell: the program that interprets and executes the command entered by the user

That is why expressions such as `open the terminal`, `run it in the shell`, and `type it on the command line` remain even in modern development environments. All of these are connected to the flow `instead of pressing graphical buttons, enter commands as text and execute them`.

## Terminal Is the Screen, and the Shell Is the Program That Interprets Commands

The `terminal` is the screen where commands are entered and results are viewed. Terminal on macOS, Windows Terminal, and the Terminal panel in VS Code belong here.

The `shell` is the program that reads, interprets, and executes the commands entered by the user. Through the shell, the user can run and combine many utilities of the operating system.

Here we distinguish them like this.

- terminal: the window where commands are entered and results are viewed
- shell: the program inside the terminal that reads and executes commands
- command: the thing we ask the shell to do

So even inside the single phrase `I opened the terminal`, there are several cases.

| Environment | Terminal app | Example shell |
| --- | --- | --- |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Windows | Windows Terminal, PowerShell, VS Code Terminal | PowerShell, Command Prompt, WSL shell |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

Here we do not go deeply into differences among shells by operating system. But we try to mark what the command examples are based on.

## A Command Is Not a Sentence, but an Execution Request

The sentence entered in the terminal is not a natural-language sentence. It is an execution request that the shell reads according to fixed rules.

For example, the following is a command that checks the current location.

```bash
pwd
```

The next command moves to a folder.

```bash
cd docs
```

The next command looks at the file list of the current folder.

```bash
ls
```

In Windows PowerShell, `Get-Location` can be used to check the current location, and `Set-Location` can be used to move. Microsoft documentation explains that `Get-Location` displays the current location and that `Set-Location` sets the current working location.

You do not need to memorize all commands. What matters is `where the command is executed`.

The same command can target different files when the current folder is different.

## Working Directory Is the Base Location of a Command

The `working directory` is the folder currently used as the base by a command. It is also called the `current working directory` (CWD).

For example, suppose the following command is executed in the terminal.

```bash
python example.py
```

This command can usually be read as, `find the file called example.py in the current working directory and run it with Python`. But if there is no `example.py` in the current working directory, the command fails.

Did it fail because the file does not exist? Not necessarily.

In a common case, the file is not absent. The file exists, but I am in the wrong folder.

A common error begins not from code syntax, but from a location problem. The file may be in `downloads/`, but the terminal may be in `home/`. The project folder may be in `project-name/`, but the terminal may be in its parent folder.

So before practice, we check the current location.

```bash
pwd
```

Then we move to the needed folder.

```bash
cd /Users/someone/ws/project-name
```

In Windows PowerShell, you can check it like this.

```powershell
Get-Location
```

And move like this.

```powershell
Set-Location C:\Users\someone\ws\project-name
```

Even if the command names differ, the core is the same.

So first check these two questions.

- In what folder am I now?
- On what folder does this command execute as its base?

## Distinguish Relative Paths and Absolute Paths

A `path` is the string that indicates the location of a file or folder. Here we distinguish `relative path` and `absolute path`.

The two terms are distinguished as follows.

- relative path: a location found based on the current working directory
- absolute path: the full location written starting from the beginning of the file system

For example, if the current working directory is `/Users/someone/ws/project-name`, then the following relative path can point to the documents folder.

For example, `docs/parts` is a relative path.

By contrast, an absolute path writes everything from the starting point.

```text
/Users/someone/ws/project-name/docs/parts
```

Relative paths are short and convenient. But if the current working directory changes, their meaning changes too.

`docs/parts` has meaning when executed inside the `project-name` folder. But if it is executed from another project folder, it points to a completely different location or to a path that does not exist.

## Habit of Checking the File List Matters

When a command fails, before immediately editing the code, check the current folder and the file list.

In Unix-like shells, the following commands are usually used.

```bash
pwd
ls
```

In Windows PowerShell, the following commands can be used.

```powershell
Get-Location
Get-ChildItem
```

In PowerShell, `ls` often works as an alias of `Get-ChildItem`. But it is still helpful to look once at the original name rather than only the alias. Later, when searching documentation, you can search using the official name.

Here we first show commands based on macOS/Linux, and if Windows needs a different command, we mark it separately.

## Is There No Terminal in Colab?

Colab can also execute commands. But misunderstanding appears if it is understood as exactly the same thing as the local PC terminal.

If you put `!` like the following inside a Colab code cell, you can execute a shell command.

Problem situation: we see that even inside a Colab code cell, a shell command checking the current working location can be run.
Input: the `!pwd` command executed in a code cell.
Expected output: the current folder path is printed based on the Colab runtime.
Concept to check: the `!` command in Colab runs a shell command in the Colab runtime, not in my PC terminal.

```python
# This shell command checks the current working folder from a Colab code cell.
!pwd
```

At that time, the command is executed not on my laptop computer, but in the Colab runtime. So the file location, installed packages, and saved files can differ from the local PC.

In summary, it is as follows.

- terminal of my PC: executed on the basis of my computer's files and environment
- `!` command in a Colab code cell: executed on the basis of the Colab runtime's files and environment

This is also why in P2-3.5 we distinguished `!pip install numpy` from `%pip install numpy`. Even if shell commands can be executed inside a code cell, that does not mean they are Python syntax.

## Errors That Often Happen in the Terminal

Even when terminal errors look complicated, they can be divided into a few types.

| Situation | Question to check first |
| --- | --- |
| it says it cannot find a file | Is the current working directory correct? |
| it says it cannot find the command | Is that program installed, and can it be found from PATH? |
| the Python file does not run | Did I mix terminal commands and Python code? |
| it works in Colab but not locally | Is the same package installed in the local environment? |
| it works locally but not in Colab | Has the file been uploaded into the Colab runtime? |

This Section does not solve every error. But it builds the habit of dividing, when reading an error, between `an error in the code itself` and `an error in the location where the command was executed`.

## View It Through a Case

### Case 1. Why `python example.py` Fails Even Though the File Exists

Suppose a learner downloaded the file `example.py` and is trying to run it. The file definitely exists inside the project folder on the desktop, but when `python example.py` is entered in the terminal, an error appears saying that the file cannot be found.

People often first think, `Was the file broken?` or `Is Python strange?` But in this case, a more common cause is that the current working directory is not the project folder. The same command can look for a completely different file depending on from what folder it is executed.

If we distinguish the core words of this Section, `terminal`, `shell`, `working directory`, and `relative path`, the interpretation changes. The problem may not be the code itself but `from what location the command was executed as its base`, and that is why commands such as `pwd`, `ls`, and `cd` are needed first.

The confirmable result appears immediately when the current location is printed. If the result of `pwd` is not the project folder, then the reason the same `python example.py` command fails can be explained not as a code issue but as a location issue.

## Checklist

- You can explain the terminal as the screen for command input and result checking.
- You can explain the shell as the program that interprets and executes commands.
- You can explain that terminal apps inherited in software the role of older text-based terminal devices.
- You can explain the working directory as the current base location of commands.
- You can explain the difference between relative path and absolute path at an introductory level.
- You can explain why `pwd`, `cd`, and `ls` are needed.
- You know that in PowerShell, official command names such as `Get-Location`, `Set-Location`, and `Get-ChildItem` exist.
- You can explain that the `!` command in a Colab code cell is executed in the Colab runtime, not on the local PC.
- You can first check `what shell am I using`, `what folder am I in now`, and `what file or program is this command trying to find`.

## Sources and References

- David S. Lawyer, [Text-Terminal-HOWTO](https://tldp.org/HOWTO/Text-Terminal-HOWTO.html){: target="_blank" rel="noopener noreferrer" }, The Linux Documentation Project, checked 2026-07-20. Used as historical support for the relationship between older text terminals and modern command-line interfaces.
- Free Software Foundation, [Bash Reference Manual](https://www.gnu.org/software/bash/manual/bash.html){: target="_blank" rel="noopener noreferrer" }, GNU Bash 5.3 manual, checked 2026-07-20. Used to confirm that a shell is both a command interpreter and a programming language, and to support the Bash command-processing context.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked 2026-07-20. Used to confirm the official PowerShell command for checking the current working location and its `pwd` alias context.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked 2026-07-20. Used to confirm the official PowerShell command for changing the current working location and its `cd` alias context.
- Python Software Foundation, [os.getcwd](https://docs.python.org/3/library/os.html#os.getcwd){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-07-20. Used to support the point that Python code can read the current working directory as a string.
