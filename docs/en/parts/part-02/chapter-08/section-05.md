# P2-8.5 Functions and Small Reuse

> Section ID: `P2-8.5`
> Version: `v2026.07.09`

Values, data structures, and loops all lead to another practical question: when should repeated handling be grouped into a reusable small unit?

## Scope of This Section

This Section introduces functions through `input -> process -> output` structure, along with the difference between `print` and `return`.

## Central Question

How do we turn something we were already doing into a reusable small unit?

## Perspective to Keep

- A function gives a name to a repeated flow.
- The useful early contract is `input -> process -> output`.
- `print` shows something; `return` hands a result back.

## Short Check

- Can you explain why not every repeated block should stay copied in several places?
- Can you explain the difference between printing a result and returning it?
- Can you explain what makes a function feel like a small reusable contract?

## Sources and References

- Python Software Foundation, [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
