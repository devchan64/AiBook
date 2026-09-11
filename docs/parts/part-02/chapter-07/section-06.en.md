# P2-7.6 Supplemental Learning: Opening Terminals by Operating System

> Section ID: `P2-7.6`
> Version: `v2026.09.08`

Use `Get-Location` in Windows PowerShell and `pwd` in macOS/Linux shells to check your current location. Opening the terminal and writing paths differ, but the tasks of checking the location, listing files, and changing folders are the same.

| Term | Meaning to establish first in this section |
| --- | --- |
| Windows Terminal / PowerShell | A terminal-app-and-shell combination you often encounter when starting command input on Windows. |
| Terminal / zsh | A default terminal-app-and-shell combination you often encounter on macOS. |
| `pwd`, `ls`, `cd` | Basic commands for checking the current location, checking the file list, and moving folders. |
| `Get-Location`, `Get-ChildItem`, `Set-Location` | Commands in PowerShell that serve the same purposes. |
| path difference | The difference in location notation by operating system, such as Windows `C:\\...` versus macOS/Linux `/...`. |

## Operating Systems, Paths, and Shortcuts

| Criterion | Why it matters |
| --- | --- |
| If the operating system is different, the terminal app, default shell, and path notation are also slightly different | If you copy examples from another operating system as-is, the path and command can mismatch |
| Even so, what you look at first in common is the current location and the file list | Even across operating systems, the order of checks before practice does not differ much |
| Terminal shortcuts can behave differently from general apps | If you confuse copy-paste with interrupting execution, your work can stop unexpectedly |

## Terminals and Shells by Operating System

The first confusion in terminal usage is usually that the “terminal app” and the “shell running inside it” get mixed together.

Microsoft documentation explains Windows Terminal as a modern host application for running command-line shells such as Command Prompt, PowerShell, and WSL's bash. In other words, Windows Terminal does not mean a single shell. It is closer to an app where you can open multiple shells in tabs.

Apple's Terminal User Guide introduces Terminal on macOS as a tool for creating and managing shell scripts. When you open Terminal on macOS, you generally use a Unix-like shell.

Ubuntu documentation explains that Linux also has a GUI, but traditional Unix environments use a command-line interface, and in most Linux distributions, you can enter similar commands into the terminal.

Examples of terminal apps and shells are:

| Operating system | Frequently encountered terminal apps | Frequently encountered shells |
| --- | --- | --- |
| Windows | Windows Terminal, PowerShell, Command Prompt | PowerShell, Command Prompt, WSL bash |
| macOS | Terminal, iTerm2, VS Code Terminal | zsh, bash |
| Linux | GNOME Terminal, Konsole, VS Code Terminal | bash, zsh |

## Opening PowerShell on Windows

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

## Opening Terminal on macOS

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

## Opening a Terminal on Linux

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

## Terminal Shortcuts

Terminals can assign different shortcuts to copying and interrupting execution.

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

`Ctrl + C` can request an interrupt from a running program. To copy text, use the copy shortcut in the table. Behavior may depend on app settings and whether text is selected; if it differs from expectations, check the menu shortcut.

## Checking Location After Changing Folders

After moving into the practice folder, check the location and file list again to catch path mistakes.

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

## Path Notation by Operating System

Windows and macOS/Linux write paths differently.

| Category | Windows example | macOS/Linux example |
| --- | --- | --- |
| User folder | `C:\Users\someone` | `/Users/someone`, `/home/someone` |
| Folder separator | `\` | `/` |
| Project example | `C:\Users\someone\ws\project-name` | `/Users/someone/ws/project-name` |

If you see a path such as `/Users/someone/ws/project-name` in a document, it is likely a macOS example. On Linux, it may be closer to `/home/someone/ws/project-name`, and on Windows, it may be closer to `C:\Users\someone\ws\project-name`.

Therefore, when copying path examples, you need to change them to the actual folder location on your computer.

## Checking Python Commands

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

Use the printed version to determine which command runs Python. If installation is needed, see [Installing Python](section-07.en.md).

## Prompts and Actual Commands

It is common to copy and paste commands from documentation. That is not itself a bad habit. Ubuntu documentation also explains that even experienced users often copy and paste commands.

However, you should read a copied command before running it.

First, check the following.

- Which folder is the command assuming?
- Is it a command for Windows, or for macOS/Linux?
- Is it just checking something, or is it a command that changes the system?
- Does it include parts such as `sudo`, package installation, deletion, or moving paths?
- Does it include prompt symbols such as `$`, `>`, or `PS>` at the front?

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

## Checks by Error Type

Identify what the error message refers to.

| Error situation | What to check first |
| --- | --- |
| Cannot find the file | current working folder and file list |
| Cannot find the command | whether the program is installed and the PATH setting |
| Cannot find the package | current Python environment and whether the package is installed |
| A permission error occurs | execution location, file permissions, and whether administrator privileges are needed |
| It works in Colab but not locally | local Python and package-installation state |

## Project Paths Containing Spaces

If the project folder is named `ai practice`, pass the space as part of one path. Substitute your actual username and folder location, and quote the entire path.

Windows PowerShell:

```powershell
Set-Location "C:\Users\someone\ws\ai practice"
Get-Location
```

macOS:

```bash
cd "/Users/someone/ws/ai practice"
pwd
```

Linux:

```bash
cd "/home/someone/ws/ai practice"
pwd
```

Check that each result is the project location ending in `ai practice`. Without quotes, a shell may split a path containing spaces into multiple arguments and fail to change folders. Even when commands share a purpose, the actual path and argument boundaries must match.

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

- Microsoft, [What is Windows Terminal?](https://learn.microsoft.com/en-us/windows/terminal/){: target="_blank" rel="noopener noreferrer" }, Microsoft Learn, checked 2026-07-20. Used to confirm that Windows Terminal is a host app for command-line shells such as Command Prompt, PowerShell, and WSL bash.
- Apple, [Keyboard shortcuts in Terminal on Mac](https://support.apple.com/guide/terminal/keyboard-shortcuts-trmlshtcts/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, checked 2026-07-20. Used to confirm macOS Terminal shortcuts for windows/tabs, copy and paste, `Tab`, and `Ctrl-C`-type behavior.
- Apple, [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac){: target="_blank" rel="noopener noreferrer" }, Apple Support, checked 2026-07-20. Used to confirm the role of macOS Terminal and its guidance for executing commands and specifying files and folders.
- Ubuntu Documentation, [UsingTheTerminal](https://help.ubuntu.com/community/UsingTheTerminal){: target="_blank" rel="noopener noreferrer" }, Ubuntu Community Help Wiki, checked 2026-07-20. Used to confirm the introductory context for opening a terminal and performing command-line work on Ubuntu/Linux.
- Microsoft, [Get-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked 2026-07-20. Used to confirm the PowerShell command for checking the current working location and its `pwd` alias.
- Microsoft, [Set-Location](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-location?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked 2026-07-20. Used to confirm the PowerShell command for changing the current working location and its `cd` alias.
- Microsoft, [Get-ChildItem](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/get-childitem?view=powershell-7.5){: target="_blank" rel="noopener noreferrer" }, PowerShell documentation, checked 2026-07-20. Used to confirm the PowerShell command for listing files and folders and its `ls` alias.
