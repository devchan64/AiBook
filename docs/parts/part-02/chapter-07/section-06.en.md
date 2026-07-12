# P2-7.6 Supplemental Learning: Using Terminals on Windows, macOS, and Linux

> Section ID: `P2-7.6`
> Version: `v2026.07.12`

In P2-7.2, we looked at the concepts of a terminal, a shell, and a working directory. Here, we cover how to check those concepts on actual operating systems.

Here, we supplement `how to enter a terminal by operating system` and the `basic commands for checking your current location`.

This supplement does not explain Python syntax. It also does not go deeply into Python installation. Python installation is handled separately in P2-7.7. This supplement practices “where do I enter commands, how do I check my current location, and how do I move to the practice folder?”

This supplement organizes the procedure for opening a terminal, checking the current location, and moving to the practice folder on Windows, macOS, and Linux. The execution-environment concept itself is covered in P2-7.1 and P2-7.2.

| Term | Meaning to establish first in this section |
| --- | --- |
| Windows Terminal / PowerShell | A terminal-app-and-shell combination you often encounter when starting command input on Windows. |
| Terminal / zsh | A default terminal-app-and-shell combination you often encounter on macOS. |
| `pwd`, `ls`, `cd` | Basic commands for checking the current location, checking the file list, and moving folders. |
| `Get-Location`, `Get-ChildItem`, `Set-Location` | Commands in PowerShell that serve the same purposes. |
| path difference | The difference in location notation by operating system, such as Windows `C:\\...` versus macOS/Linux `/...`. |

## Scope of This Supplement

This supplement covers the minimum procedure to open a terminal for the first time and check things before practice on Windows, macOS, and Linux. The conceptual definitions of terminal and shell are covered again in P2-7.2, deciding whether Python needs to be installed is covered again in P2-7.7, shell symbols and environment variables are covered again in P2-7.8, and the order for checking a local environment is covered again in P2-7.9.

Here, we answer the following questions.

- What terminal can you open on Windows?
- How should you understand Terminal on macOS?
- Why does terminal usage appear so often on Linux?
- How do you check the current location and file list?
- Why are Windows commands and macOS/Linux commands slightly different?
- What should you be careful about when running copied-and-pasted commands?

Shell scripts, pipes, redirection, administrator privileges, and environment variables are not covered deeply here. Those expressions are recovered separately in the P2-7.8 supplementary section, and in Part 6, permissions and logs are connected again in a project context.

## Goal of This Supplement

- You can explain at an introductory level how to open a terminal on Windows, macOS, and Linux.
- You can explain that when you open a terminal, you should first check the current location.
- You can explain that Windows PowerShell commands and macOS/Linux shell commands differ in some places.
- You can explain what `pwd`, `ls`, `cd`, `Get-Location`, `Get-ChildItem`, and `Set-Location` are used for.
- Before copying and running a command, you can check the current folder and the purpose of the command.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| If the operating system is different, the terminal app, default shell, and path notation are also slightly different | If you copy examples from another operating system as-is, the path and command can mismatch | Understand that even for the same purpose, command notation can differ slightly |
| Even so, what you look at first in common is the current location and the file list | Even across operating systems, the order of checks before practice does not differ much | Keep the criterion that location checking comes first |
| Terminal shortcuts can behave differently from general apps | If you confuse copy-paste with interrupting execution, your work can stop unexpectedly | Remember that `Ctrl+C`-type behavior must be handled carefully by environment |

## The Terminal App and the Shell Can Differ by Operating System

The first confusion in terminal usage is usually that the “terminal app” and the “shell running inside it” get mixed together.

Microsoft documentation explains Windows Terminal as a modern host application for running command-line shells such as Command Prompt, PowerShell, and WSL's bash. In other words, Windows Terminal does not mean a single shell. It is closer to an app where you can open multiple shells in tabs.

Apple's Terminal User Guide introduces Terminal on macOS as a tool for creating and managing shell scripts. When you open Terminal on macOS, you generally use a Unix-like shell.

Ubuntu documentation explains that Linux also has a GUI, but traditional Unix environments use a command-line interface, and in most Linux distributions, you can enter similar commands into the terminal.

Here, we organize it like this.

| Operating system | Frequently encountered terminal apps | Frequently encountered shells |
| --- | --- | --- |
| Windows | Windows Terminal, PowerShell, Command Prompt | PowerShell, Command Prompt, WSL bash |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

Practice in this part marks, as much as possible, which environment a command is based on. If it is not marked, it is often based on a macOS/Linux-like shell.

## On Windows, Use PowerShell as the First Default Reference

There are several kinds of command-input windows you encounter on Windows.

- Windows Terminal
- PowerShell
- Command Prompt
- the Terminal panel in VS Code
- if WSL is installed, a Linux shell

Here, when Windows-specific explanation is needed, PowerShell is treated as the first default reference. Command Prompt appears often in old materials, but in Python learning and modern development environments, you may encounter PowerShell or Windows Terminal more often.

The easiest ways to open a terminal on Windows are usually one of the following.

1. Search for `Terminal` or `PowerShell` in the Start menu.
2. If you are using VS Code, choose `Terminal > New Terminal` from the top menu.
3. You can use a terminal-opening feature from the right-click menu in the project folder. This menu name can differ depending on the Windows version and installed tools.

After opening the terminal, first check the current location.

```powershell
Get-Location
```

Check the file and folder list.

```powershell
Get-ChildItem
```

Move to a folder.

```powershell
Set-Location C:\Users\someone\ws\project-name
```

Short aliases are also often used in PowerShell.

```powershell
pwd
ls
cd C:\Users\someone\ws\project-name
```

But when you first study this, it is better to also know the official command names. Later, when you look up documentation, searching for `Get-Location`, `Get-ChildItem`, and `Set-Location` makes it easier to find more accurate material.

## On macOS, You Often Open Terminal and Encounter the zsh Shell

On macOS, you can use the default app Terminal.

There are several ways to open Terminal.

1. Type `Terminal` in Spotlight search.
2. In Finder, open `Applications > Utilities > Terminal`.
3. If you are using VS Code, choose `Terminal > New Terminal`.

After opening the terminal, check the current location.

```bash
pwd
```

Check the file and folder list.

```bash
ls
```

Move to the project folder.

```bash
cd /Users/someone/ws/project-name
```

On macOS, paths often appear in the form `/Users/...`. This differs from the Windows form `C:\Users\...`, so if you copy an example from another operating system as-is, the path may not match.

When pasting terminal commands on macOS, be especially careful with commands that begin with `sudo`. `sudo` can make a command run with administrator privileges. In the early practice of this part, `sudo` is usually not needed.

## On Linux, the Terminal Appears Often in Learning Materials

In Linux distributions, terminal usage appears often in learning materials. Ubuntu documentation introduces ways to open the terminal such as search and shortcuts like `Ctrl + Alt + T`. The menu name can differ by desktop environment, but in many Linux environments, you can open the terminal app by searching for it.

After opening a terminal on Linux, first check the current location.

```bash
pwd
```

Check the file and folder list.

```bash
ls
```

Move to the project folder.

```bash
cd /home/someone/ws/project-name
```

On Linux, the user's home folder is often in the form `/home/username`. This differs from macOS `/Users/username`.

In Linux materials, you also often see commands like `sudo apt install ...`. Those commands can install system packages. In this Python-introduction section, do not run them blindly. First check why the command is needed.

## Tip: Remember Only a Small Number of Terminal Shortcuts

You do not need to memorize all terminal shortcuts. For now, use “open, copy-paste, tab, command completion, interrupt execution” as the standard.

| Situation | Windows Terminal | macOS Terminal | Linux/Ubuntu family |
| --- | --- | --- | --- |
| Open a new tab | `Ctrl + Shift + T` | `Command + T` | It differs by terminal app, but `Ctrl + Shift + T` is common |
| Copy | `Ctrl + Shift + C` | `Command + C` | `Ctrl + Shift + C` is common |
| Paste | `Ctrl + Shift + V` is common | `Command + V` | `Ctrl + Shift + V` is common |
| Interrupt a running command | `Ctrl + C` | `Control + C` or `Command + .` | `Ctrl + C` |
| Auto-complete a file or folder name | `Tab` | `Tab` | `Tab` |
| Review the previous command again | `↑` | `↑` | `↑` |

This table does not mean “it is always exactly the same in every environment.” It can differ depending on the terminal app, shell, keyboard layout, and whether you are in a terminal inside an editor such as VS Code. If the actual shortcuts differ, check the app menu or settings.

What is especially useful here is `Tab`. Instead of typing a folder name to the end, you can type only the beginning and then press `Tab` to complete a possible file or folder name.

For example, if you want to move into the `docs` folder, you can type the following and then press `Tab`.

```bash
cd do
```

If the terminal can find `docs`, it completes it automatically. If there are multiple candidates, it may not complete at once. Then you enter a little more, or in some terminals, press `Tab` twice to see the available candidates.

Shortcuts are tools for increasing speed. But in the beginning, checking your current location and the command you are about to run matters more than speed.

## Tip: Ctrl+C and Ctrl+V Can Look Different in a Terminal

In ordinary apps, people are used to `Ctrl + C` for copy and `Ctrl + V` for paste. But in a terminal, they can behave differently. In particular, `Ctrl + C` is often used as a signal to interrupt a running command.

For example, if you are running a Python server, a long installation command, or a program that repeats forever in a terminal, pressing `Ctrl + C` can request an interrupt, not a copy.

That is why in a terminal, it is safer to remember copy and paste shortcuts separately.

| Environment | Copy | Paste | Interrupt execution |
| --- | --- | --- | --- |
| Windows Terminal | `Ctrl + Shift + C` | `Ctrl + Shift + V` is common | `Ctrl + C` |
| macOS Terminal | `Command + C` | `Command + V` | `Control + C` or `Command + .` |
| Linux/Ubuntu family terminal | `Ctrl + Shift + C` is common | `Ctrl + Shift + V` is common | `Ctrl + C` |

This distinction is important.

- When copying text in a normal document, you use `Ctrl + C` or `Command + C`.
- When stopping a running command inside a terminal, you usually use `Ctrl + C`.
- When copying text inside a terminal, you often use `Ctrl + Shift + C` on Windows/Linux.
- When pasting into a terminal, you often use `Ctrl + Shift + V` on Windows/Linux.

However, shortcuts can change depending on terminal-app settings. Windows Terminal lets you change keyboard shortcuts, and macOS Terminal shows the actual shortcuts in the menu. If a shortcut does not behave as expected, check the menu and settings of the terminal app you are using now.

Here, remember the following criteria first.

- If you press `Ctrl + C` and it does not copy, in a terminal it may mean interrupt execution.
- If copy-paste does not work in a Windows/Linux terminal, check `Ctrl + Shift + C` and `Ctrl + Shift + V`.
- In macOS Terminal, first think of `Command + C` and `Command + V` as in normal Mac apps.

## What to Check First in Common Across All Three Operating Systems

Even if the operating system differs, the pre-practice checking order is similar.

1. Open the terminal.
2. Check the current location.
3. Check the file list.
4. Move to the practice folder.
5. Check the current location and the file list again.
6. Run the Python command or the package-installation command.

From the perspective of Windows PowerShell, the flow looks like this.

```powershell
Get-Location
Get-ChildItem
Set-Location C:\Users\someone\ws\project-name
Get-Location
Get-ChildItem
```

From the perspective of macOS/Linux, the flow looks like this.

```bash
pwd
ls
cd /Users/someone/ws/project-name
pwd
ls
```

On Linux, the movement path can look like the following.

```bash
cd /home/someone/ws/project-name
```

What matters is not memorizing many command names. It is the habit of first checking “which folder am I in now?”

## Path Separators Differ

Windows and macOS/Linux write paths differently.

| Category | Windows example | macOS/Linux example |
| --- | --- | --- |
| User folder | `C:\Users\someone` | `/Users/someone`, `/home/someone` |
| Folder separator | `\` | `/` |
| Project example | `C:\Users\someone\ws\project-name` | `/Users/someone/ws/project-name` |

If you see a path such as `/Users/someone/ws/project-name` in a document, it is likely a macOS example. On Linux, it may be closer to `/home/someone/ws/project-name`, and on Windows, it may be closer to `C:\Users\someone\ws\project-name`.

Therefore, when copying path examples, you need to change them to the actual folder location on your computer.

## What to Check Before Running a Python Command

Before running Python in a terminal, check the following.

- Is the terminal currently opened with the project folder as the base?
- Is the `.py` file you want to run in the current folder?
- Are the required data files in the same folder or in the specified path?
- If you need to use a virtual environment, is the current virtual environment activated?
- Among `python`, `python3`, and `py`, which command works in my environment?

Depending on the operating system and the installation method, the Python execution command can differ.

```bash
python --version
```

```bash
python3 --version
```

On Windows, if Python Launcher is installed, you may also see the following command.

```powershell
py --version
```

Here, we do not solve Python installation itself. We only go as far as checking “which command points to Python in my environment?” The point where installation becomes necessary is handled separately in P2-7.7.

## Read Copied-and-Pasted Commands Before Running Them

It is common to copy and paste commands from documentation. That is not itself a bad habit. Ubuntu documentation also explains that even experienced users often copy and paste commands.

However, you should read a copied command before running it.

First, check the following.

- Which folder is the command assuming?
- Is it a command for Windows, or for macOS/Linux?
- Is it just checking something, or is it a command that changes the system?
- Does it include parts such as `sudo`, package installation, deletion, or moving paths?
- Does it include prompt symbols such as `$`, `>`, or `PS>` at the front?

Especially in early practice, it is better to stop at the habit of checking `current location`, `command purpose`, and `operating-system match` before running a copied command.

In documentation, a terminal prompt may appear like the following in order to explain the prompt itself.

```text
$ python example.py
```

At that point, `$` may not be a character you are supposed to type. It is usually expressing the prompt symbol. What you actually type is the following part.

```bash
python example.py
```

In PowerShell documentation, it may appear like this.

```text
PS C:\Users\someone> python example.py
```

Here too, you do not type the whole `PS C:\Users\someone>`. The actual command is `python example.py`.

## If an Error Appears, Separate Location and Environment First

When you encounter a terminal error, do not immediately decide `I am bad at Python`. First divide the problem.

| Error situation | What to check first |
| --- | --- |
| Cannot find the file | current working folder and file list |
| Cannot find the command | whether the program is installed and the PATH setting |
| Cannot find the package | current Python environment and whether the package is installed |
| A permission error occurs | execution location, file permissions, and whether administrator privileges are needed |
| It works in Colab but not locally | local Python and package-installation state |

In early practice, the most common problems are not deep code errors. They are problems such as being in the wrong current folder, having the package installed in a different environment, or mistaking Colab and the local PC for the same environment.

## Cases And Examples

### Case 1. When the Same Command Is Copied but Looks Different on Windows and macOS

Suppose you copied the command `cd /Users/someone/ws/project-name` from a learning resource exactly as written and tried to run it. It looks natural on macOS, but in Windows PowerShell the path format itself looks unfamiliar, and for some learners even the paste shortcut can behave differently and become a blocker.

The criterion people often start with is simply `it is a command written in the document, so I should be able to paste it as it is`. But in reality, terminal apps, default shells, path notation, and copy-paste behavior differ a little by operating system.

The difference this section tries to reduce is exactly that operating-system-specific notation difference. The key is not to memorize every command, but to read the common purposes: `check current location`, `check file list`, and `move to the project folder`. On Windows, `Get-Location`, `Set-Location`, and `Get-ChildItem` match those purposes. On macOS/Linux, `pwd`, `cd`, and `ls` match them.

A checkable result can be seen immediately through the command that shows the current location. Even if the operating system differs, if you can ultimately confirm `which folder am I in now?`, the initial confusion caused by path-notation differences becomes much smaller.

## Checklist

- Can you explain that Windows Terminal is a host app that can run multiple command-line shells?
- Can you check your location and move around in macOS Terminal with `pwd`, `ls`, and `cd`?
- Can you open a terminal on Linux and check the current location and the file list?
- Can you explain the purpose of `Get-Location`, `Get-ChildItem`, and `Set-Location` in Windows PowerShell?
- Can you explain the path-notation difference between Windows and macOS/Linux?
- Can you explain that terminal shortcuts can differ by environment, and that you should first check `Tab`, `Ctrl + C`, and copy-paste behavior?
- Can you explain that `Ctrl + C` and `Ctrl + V` in general apps can differ from terminal copy, paste, and interrupt shortcuts?
- Can you distinguish prompt symbols from the actual command to type in a copied command?
- Can you explain that commands such as `sudo`, `rm`, `del`, and `Remove-Item` should not be run before their meaning is understood?
- Can you explain the order `open the terminal -> check the current location -> check the file list -> move to the practice folder -> check the location and file list again -> run the Python command`?

## Sources and References

- Microsoft, [What is Windows Terminal?](https://learn.microsoft.com/en-us/windows/terminal/){: target="_blank" rel="noopener noreferrer" }, Microsoft Learn, checked on 2026-06-24.
- Apple, [Keyboard shortcuts in Terminal on Mac](https://support.apple.com/guide/terminal/keyboard-shortcuts-trmlshtcts/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, checked on 2026-06-24.
- Apple, [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, checked on 2026-06-24.
- Ubuntu Documentation, [UsingTheTerminal](https://help.ubuntu.com/community/UsingTheTerminal){: target="_blank" rel="noopener noreferrer" }, Ubuntu Community Help Wiki, checked on 2026-06-24.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked on 2026-06-24.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked on 2026-06-24.
- Microsoft, [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked on 2026-06-24.
