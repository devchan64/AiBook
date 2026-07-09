# P2-7.1 Local Environments and Runtimes

> Section ID: `P2-7.1`
> Version: `v2026.07.09`

Earlier, Colab and a local PC were separated only enough to run NumPy practice. This Section steps down one level further: where does code actually run, and what program is responsible for running it?

## Scope of This Section

This Section introduces the large distinction between a `local environment` and a `runtime`. It is not a full installation manual.

## Central Question

If a calculation is ready, where is it executed, and which program is actually reading it?

## One Small Scene

| What you want to see | Where you type it | Example |
| --- | --- | --- |
| run one Python line in Colab | Colab code cell | `print("hello")` |
| check Python on a local PC | terminal | `python --version` |
| run one Python line locally | interpreter or `.py` file | `print("hello")` |

## Perspective to Keep

- The same-looking text can belong to different execution places.
- A runtime is the currently active Python execution state.
- A local environment and a hosted environment can feel similar on the surface but behave differently in files, packages, and persistence.

## Short Check

- Can you explain the difference between “where code is written” and “where code runs”?
- Can you explain why `python --version` and `print("hello")` belong to different places?
- Can you explain what a runtime means at an entry level?

## Sources and References

- Python Software Foundation, [The Python Tutorial](https://docs.python.org/3/tutorial/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
