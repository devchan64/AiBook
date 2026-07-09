# P2-7.2 Terminal, Shell, and Working Directory

> Section ID: `P2-7.2`
> Version: `v2026.07.07`

After separating execution places, the next screen to understand on a local machine is the terminal.

## Scope of This Section

This Section introduces `terminal`, `shell`, `working directory`, `path`, and `command`. It does not try to teach every terminal feature.

## Central Question

When a tutorial says “open the terminal, move to the project folder, and run this command,” what do those words each mean?

## Terms to Fix First

| Term | Very short meaning |
| --- | --- |
| terminal | window or app where commands are entered |
| shell | program inside the terminal that reads and runs commands |
| working directory | folder the current command is using as its base |
| path | text that points to a file or folder location |
| command | sentence asking the shell to do something |

## Perspective to Keep

- Terminal and shell are related but not identical.
- Many beginner problems are really location problems, not code problems.
- `pwd`, `cd`, and `ls` matter because commands are interpreted relative to a working directory.

## Short Check

- Can you distinguish terminal from shell?
- Can you explain why the working directory matters?
- Can you explain why a command can fail even when the text is correct but the location is wrong?

## Sources and References

- Python Software Foundation, [Using Python on Unix platforms](https://docs.python.org/3/using/unix.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
