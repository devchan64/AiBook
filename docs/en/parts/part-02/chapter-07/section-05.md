# P2-7.5 Dependency and Reproducibility

> Section ID: `P2-7.5`
> Version: `v2026.07.07`

After virtual environments and packages, one more question remains: if the package is installed once, is that enough?

## Scope of This Section

This Section introduces `dependency`, `reproducibility`, `requirements.txt`, and `version pinning`.

## Central Question

Why is code alone not enough if we want the same result again later or on another machine?

## Perspective to Keep

- Dependencies are external conditions your code relies on.
- Reproducibility means leaving enough information to rebuild the same environment.
- `requirements.txt` and version records help turn “works here” into “can be rerun elsewhere.”

## Short Check

- Can you explain dependency as something outside your own code that your code still needs?
- Can you explain reproducibility as an environment problem as well as a code problem?
- Can you explain why package versions may affect results?

## Sources and References

- Python Packaging Authority, [Requirements Files](https://pip.pypa.io/en/stable/reference/requirements-file-format/){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
