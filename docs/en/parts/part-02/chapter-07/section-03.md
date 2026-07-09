# P2-7.3 The Python Interpreter and Scripts

> Section ID: `P2-7.3`
> Version: `v2026.07.07`

Once the terminal is in place, the next question is how Python code itself gets executed.

## Scope of This Section

This Section distinguishes the `Python interpreter`, `interactive mode`, `script`, and `python -m ...` style execution.

## Central Question

Why do `python`, `python example.py`, and `print("hello")` all relate to Python but still belong to different layers?

## Perspective to Keep

- `python` is a terminal command that starts the interpreter.
- `print("hello")` is Python code, not a shell command.
- `python file.py` asks Python to run a script file.
- `python -m ...` asks Python to run a module.

## Short Check

- Can you distinguish shell commands from Python code?
- Can you explain interactive execution versus script execution?
- Can you explain why `python -m ...` is still different from writing plain Python code directly?

## Sources and References

- Python Software Foundation, [The Python Tutorial](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
