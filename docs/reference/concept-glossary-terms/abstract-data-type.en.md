<a id="abstract-data-type"></a>

## abstract data type

- Meaning: An abstract data type defines a data structure by the operations it must provide, not by the way it is stored internally. The important promise is what users can do with it, such as push, pop, enqueue, dequeue, or inspect the front item.
- Why it matters: This separates the visible behavior of a structure from its implementation. A stack or queue can be implemented with an array, a linked structure, or another internal layout, while still offering the same conceptual operations. This distinction helps readers understand API design, implementation choices, and why the same idea can have several concrete forms.
- Related concepts: `data structure`, `operation`, `implementation`
- Core Section: `P2-9.1`
- Appears in: `P2-9.4`
