# P2-7.2 Terminal, Shell, and Working Directory

> Section ID: `P2-7.2`
> Version: `v2026.09.08`

Running `python example.py` involves a shell that interprets the command and a base folder used to locate the file. The same command run from a different folder can fail even when the file exists.

| Term | Meaning |
| --- | --- |
| terminal | the window or app where we type commands and see results |
| shell | the program inside the terminal that reads, interprets, and runs commands |
| working directory | the folder used as the current base by the command |
| path | the string that points to where a file or folder is located |
| command | the execution sentence asking the shell to do something now |

## Command Interpretation and Base Location

| Criterion | Why it matters |
| --- | --- |
| The terminal is the screen, and the shell is the program inside it that interprets commands | Confusion decreases only when the place of input and the interpreting agent are separated. |
| The working directory determines the base location of commands | The same command can point to different files depending on the current location. |
| The first thing to check is the current location and the file list | Many failures begin from location problems rather than syntax. |

## Origins of Terminals and Shells

Terminal and shell are not names of recently created apps. Both keep traces of the era when many people used computers through text.

The early `terminal` was not an app inside a laptop like today. It was an input-output device connected to a central computer. Text-Terminal-HOWTO explains that real text terminals looked like a monitor and keyboard but displayed not pictures but a text-based `command-line interface`, and that they were widely used for connecting to mainframe computers in the late 1970s and 1980s. Later, real hardware terminals decreased, but today's terminal apps are closer to `terminal emulators` that imitate that behavior in software.

`Shell` is also an old concept. The GNU Bash manual explains that Bash is the shell, or `command language interpreter`, for the GNU operating system. It also explains that a Unix shell is both a command interpreter and a programming language.

Historical terminal devices connect to modern apps as follows.

- past: people entered commands to a central computer through a separate terminal device
- present: terminal apps provide that text-based way of working through software
- shell: the program that interprets and executes the command entered by the user

That is why expressions such as `open the terminal`, `run it in the shell`, and `type it on the command line` remain even in modern development environments. All of these are connected to the flow `instead of pressing graphical buttons, enter commands as text and execute them`.

## Terminal Apps and Shells

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

## Current Location, Navigation, and File Lists

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

In Windows PowerShell, use `Get-Location` to check the current location and `Set-Location` to change it. Aliases such as `pwd` and `cd` are also common in PowerShell. Microsoft documentation describes these commands as displaying and setting the current working location.

The same command can target different files when the current folder is different.

## Working Directories and Running Files

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

## Relative and Absolute Paths

A `path` is the string that indicates the location of a file or folder. Here we distinguish `relative path` and `absolute path`.

The two terms are distinguished as follows.

- relative path: a location found based on the current working directory
- absolute path: the full location written starting from the beginning of the file system

If the current working directory is `/Users/someone/ws/project-name`, the relative path `docs/parts` refers to the `docs/parts` folder beneath it.

By contrast, an absolute path writes everything from the starting point.

```text
/Users/someone/ws/project-name/docs/parts
```

Relative paths are short and convenient. But if the current working directory changes, their meaning changes too.

`docs/parts` has meaning when executed inside the `project-name` folder. But if it is executed from another project folder, it points to a completely different location or to a path that does not exist.

## Checking File Lists

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

## Shell Commands in a Colab Runtime

Colab can also execute commands. But misunderstanding appears if it is understood as exactly the same thing as the local PC terminal.

If you put `!` like the following inside a Colab code cell, you can execute a shell command.

Running `!pwd` in a Colab cell connected to a hosted runtime prints that runtime’s current folder path.

```python
# This shell command checks the current working folder from a Colab code cell.
!pwd
```

At that time, the command is executed not on my laptop computer, but in the Colab runtime. So the file location, installed packages, and saved files can differ from the local PC.

In summary, it is as follows.

- terminal of my PC: executed on the basis of my computer's files and environment
- `!` command in a Colab code cell: executed on the basis of the Colab runtime's files and environment

`!` runs shell commands in IPython-based notebooks; it is not syntax for a regular Python file.

## Common Terminal Errors

Even when terminal errors look complicated, they can be divided into a few types.

| Situation | Question to check first |
| --- | --- |
| it says it cannot find a file | Is the current working directory correct? |
| it says it cannot find the command | Is that program installed, and can it be found from PATH? |
| the Python file does not run | Did I mix terminal commands and Python code? |
| it works in Colab but not locally | Is the same package installed in the local environment? |
| it works locally but not in Colab | Has the file been uploaded into the Colab runtime? |

## When an Existing File Cannot Be Run

Suppose a `workspace` folder contains a `project` folder with `example.py` inside it.

```text
workspace/
└── project/
    └── example.py
```

If the current working directory is `workspace`, `python example.py` looks for `workspace/example.py`. That file is absent, so it cannot run. Check the file with `ls project`, then use either method below.

```bash
# Change to project, then run the file.
cd project
python example.py
```

Or remain in `workspace` and specify the file’s relative path.

```bash
python project/example.py
```

Both run the same script, but the working directory differs. If the script reads data using a relative path such as `data.csv`, the first method looks for `project/data.csv`, while the second looks for `workspace/data.csv`. Distinguish locating the script from locating data inside the script.

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
