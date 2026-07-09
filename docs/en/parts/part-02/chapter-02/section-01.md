# P2-2.1 Rereading Variables, Functions, and Expressions

> Section ID: `P2-2.1`
> Version: `v2026.07.09`

P2-1.2 established the idea that formulas, code, and data are different faces of the same computation. Now we return to the basic notation that appears first whenever you read a formula.

\[
x
\]

\[
y = f(x)
\]

\[
\mathrm{loss} = f(\mathrm{prediction}, \mathrm{target})
\]

These expressions may have looked too basic to matter when you first learned math. But in AI documents, if you cannot read variables, functions, and expressions, it becomes hard to place models, inputs, outputs, loss, and parameters.

## Scope of This Section

This Section treats variables, functions, and expressions at the level needed for reading AI documents. Repeated computation with sigma is handled in `P2-2.2`, and limits and change intuition are handled in `P2-2.3`.

The question to settle first is this: when you see one line of notation, how do you distinguish what is a value, what is a relationship, and what is a calculation?

So this Section fixes only four places first.

- What kind of name is a variable?
- What kind of relationship is a function?
- What kind of computation does an expression represent?
- How are variables in code similar to and different from variables in math?

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| A variable is a name that points to a value, not the value itself | It prevents you from confusing symbols with the objects they represent | Understand that variables are names for values |
| A function is a relationship that turns input into output | It lets you read models and rules inside one common structure | Understand `y = f(x)` as input, transformation, and output |
| An expression is a compact statement of a calculation or relationship | It is the starting point for interpreting formulas for prediction, loss, and error | Understand that expressions compress computational procedure |

## A Variable Is a Name That Points to a Value

A variable is a name that refers to a value. In math, this is often written with short symbols such as `x`, `y`, `n`, or `w`.

\[
x = 3,\quad y = 2,\quad n = 4
\]

In AI documents, these names often carry extra meaning. `x` often refers to input data, `y` to an answer or target, `w` to weights, `b` to bias, `ŷ` to a prediction, and `L` to loss.

The same symbol can mean different things in different documents. So when you read a formula, the first question should be: what has this symbol been defined to mean in this text?

## Variables in Code and Variables in Math

```python
x = 3
y = 2
total = x + y
```

Example result:

```text
x points to 3, y points to 2, and total points to 5.
```

Variables in mathematics and variables in code are similar because both attach names to values. But they are not identical.

| Perspective | Mathematical variable | Code variable |
| --- | --- | --- |
| Main role | Express a relationship compactly | Store and refer to a value during execution |
| Value changes | Fixed or varying depending on context | Can be reassigned during execution |
| Type | Often inferred from context | Has a concrete type such as int, float, string, or array |

In code, the value, its shape, and its type all matter together.

```python
import numpy as np

x = np.array([1, 2, 3])

print(x)
print(x.shape)
print(x.dtype)
```

Example output:

```text
[1 2 3]
(3,)
int64
```

## A Function Is a Relationship That Turns Input into Output

\[
y = f(x)
\]

This can be read as “`x` goes in, passes through the rule or relationship `f`, and comes out as `y`.”

In AI contexts, `f` may be a hand-written rule, or it may be a learned model.

```python
def is_adult(age):
    return age >= 19

print(is_adult(20))
```

Example output:

```text
True
```

A model can also be read broadly as a function:

```python
prediction = model(input_data)
```

## An Expression Represents a Computational Relationship

An expression is a combination of values, variables, operators, and functions that represents a calculation or relationship.

\[
x + y
\]

\[
2x + 1
\]

\[
f(x)
\]

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

For example:

```python
prediction = 2.8
target = 3.0
error = prediction - target
squared_error = error ** 2

print(squared_error)
```

Example output:

```text
0.04000000000000007
```

The important point is that an expression is not symbolic decoration. It determines which values are compared and what result is produced.

## Perspective to Keep from This Section

Variables are names for values. Functions are relationships from input to output. Expressions are compressed statements of calculation. If you keep those three distinctions in place, later formulas for prediction, loss, and learning become much easier to place.

## Short Check

- You can explain a variable as a name for a value.
- You can explain a function as a relationship that turns input into output.
- You can explain an expression as a compact representation of a calculation.
- You can read `y = f(x)` as the simplest input-transformation-output structure.

## Sources and References

This Section organizes the minimum notation needed to read Part 2 and does not directly quote external material.
