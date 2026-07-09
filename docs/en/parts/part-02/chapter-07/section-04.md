# P2-7.4 Virtual Environments and Packages

> Section ID: `P2-7.4`
> Version: `v2026.07.07`

Running Python code is only part of the story. A more realistic question appears quickly: why does Python run, but NumPy still seem to be missing?

## Scope of This Section

This Section introduces `virtual environment`, `package`, `pip`, and `import` through the lens of project separation.

## Central Question

Why do package problems usually require looking at the Python environment, not only at the code?

## Perspective to Keep

- A virtual environment is a separated Python space for one project.
- `pip install ...` and `import ...` are not the same action.
- Colab runtime packages and local `.venv` packages belong to different spaces.

## Short Check

- Can you explain a virtual environment as a separated execution space?
- Can you explain why installation and import are different stages?
- Can you explain why the same code may behave differently in Colab and a local `.venv`?

## Sources and References

- Python Packaging Authority, [Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
