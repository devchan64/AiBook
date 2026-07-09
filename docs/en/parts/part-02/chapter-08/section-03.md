# P2-8.3 Dictionaries: Structures That Find Values by Key

> Section ID: `P2-8.3`
> Version: `v2026.07.07`

Lists are useful when order matters. But not all data is read best through position. Sometimes the more natural question is: which named field, setting, or ID should I look up?

## Scope of This Section

This Section introduces `dictionary`, `key`, `value`, `mapping`, and `get()`.

## Central Question

Why is key-based access different from position-based access?

## Perspective to Keep

- A dictionary is a mapping from keys to values.
- The key answers “how do I look this up?”
- Early on, it is safer to understand dictionaries as mappings before worrying about internal hash-table implementation.

## Short Check

- Can you distinguish list access from dictionary access?
- Can you explain key and value separately?
- Can you explain why `get()` is useful when a key may be missing?

## Sources and References

- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
