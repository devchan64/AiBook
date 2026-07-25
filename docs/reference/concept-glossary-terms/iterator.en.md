<a id="iterator"></a>

## iterator

- Meaning: An iterator is the object that actually produces the next value from an iterable. It carries the current progress of iteration and advances one step at a time.
- Why it matters: Iterators explain why some loops are consumed after one pass and why files or generators may need a new iterator to be read again. They make iteration a stateful execution process rather than just syntax.
- Related concepts: `iterable`, `loop`, `value`
- Core Section: `P2-8.4`
- Appears in: `P2-8.5`, `P2-10.1`
