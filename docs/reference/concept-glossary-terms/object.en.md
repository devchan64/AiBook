## object

- Meaning: An object is an actual value that Python handles in memory. Numbers, strings, lists, DataFrames, and model instances can all be understood as objects, and each object carries data and behavior according to its type. In this sense, an object is not just a bundle of data; it is a runtime target that combines `what kind of value it is` with `what it can do`.
- Why it matters: Variable names may look similar, but the attributes and methods available depend on the actual object bound to the name. This helps readers interpret code by asking `what kind of target is this?` rather than only `what is this name?` It is also necessary for understanding Python behavior such as copying values, sharing references, and calling methods at the level of actual runtime objects.
- Related concepts: `class`, `type`, `value`
- Core Section: `P2-8.6`
- Appears in: `P2-9.1`, `P2-11.1`
