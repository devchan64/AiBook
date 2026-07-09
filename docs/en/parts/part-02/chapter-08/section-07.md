# P2-8.7 Supplemental Learning: Distinguishing References, Shallow Copy, and Deep Copy

> Section ID: `P2-8.7`
> Version: `v2026.07.07`

After lists, many readers hit the same confusion: why did another name pointing to “the same list” also change?

## Scope of This Supplement

This Section gives a first distinction among `reference`, `shallow copy`, and `deep copy`.

## Central Question

Why does assigning another name not automatically create an independent new object?

## Perspective to Keep

- Assignment can create another reference to the same object.
- A shallow copy separates only one layer.
- A deep copy aims to separate nested layers too.

## Short Check

- Can you explain why another variable name does not guarantee another independent list?
- Can you explain the broad difference between shallow and deep copy?
- Can you explain why nested structures make copy questions harder?

## Sources and References

- Python Software Foundation, [copy — Shallow and deep copy operations](https://docs.python.org/3/library/copy.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
