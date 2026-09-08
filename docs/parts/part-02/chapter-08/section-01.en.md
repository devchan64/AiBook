# P2-8.1 Values, Variables, and Types

> Section ID: `P2-8.1`
> Version: `v2026.09.08`

`82` and `"82"` look similar on screen but behave differently in calculations. `82 + 3` is `85`, while `"82" + 3` raises an error because numbers and strings have different types.

| Criterion | Why it matters |
| --- | --- |
| A value is data used in computation | Numbers, text, and truth values serve as inputs to operations. |
| A variable is a name referring to a value | A name lets you reuse a value and refer to another value later. |
| A type is the kind of a value | It distinguishes the operations that can be applied. |

## Values and Operations

Numbers `3` and `3.14`, the string `"AI"`, and truth values `True` and `False` are all values. An operation processes these values.

Adding numbers `3` and `2` gives `5`; adding strings `"AI"` and `"Book"` gives `AIBook`. This code prints both results in order.

```python
print(3 + 2)
print("AI" + "Book")
```

The same `+` performs addition for numbers and concatenation for strings.

## Variables and Assignment

Python uses `=` to connect a name with a value. This action is called assignment.

A rectangle of width `20` and height `45` has area `900`. Here, `width` and `height` refer to the lengths, and `area` to their product.

```python
width = 20
height = 45
area = width * height
print(area)
```

A mathematical equation expresses equality between two sides. A Python assignment evaluates the right side, then binds the left-side name to the result. `area = width * height` does not maintain a continuing relationship between area and the two lengths. Changing `width` later does not automatically recalculate `area`.

The same name can be assigned a new value. Here, `score` first refers to `10`, then to `12`, and the code prints `12`.

```python
score = 10
score = 12
print(score)
```

Variables are sometimes described as boxes, but in Python, names referring to values is more accurate: two names can refer to the same object.

## Basic Types

A type is the kind of a value and determines which operations are possible. Passing a value to `type()` reveals its type.

This code prints the types of `3`, `3.14`, `"AI"`, and `True`: `<class 'int'>`, `<class 'float'>`, `<class 'str'>`, and `<class 'bool'>`.

```python
print(type(3))
print(type(3.14))
print(type("AI"))
print(type(True))
```

| Type | Read as | Examples | Meaning |
| --- | --- | --- | --- |
| `int` | integer | `3`, `100` | Whole numbers |
| `float` | floating-point number | `3.14`, `0.5` | Floating-point numbers |
| `str` | string | `"AI"`, `"42"` | Text strings |
| `bool` | boolean | `True`, `False` | True or false |

`float` is often used for numbers with fractional parts. Values with a zero fractional part, such as `3.0`, can also be floats.

## Reassignment and Types

In Python, the same name can refer to values of different types. Assigning integer `82` and then string `"82"` to `score` changes the printed type from `<class 'int'>` to `<class 'str'>`.

```python
score = 82
print(type(score))

score = "82"
print(type(score))
```

The value referred to by the name has a type. Names need no advance type declaration, but operations follow type-specific rules. Adding string `"82"` and integer `3` raises `TypeError`.

```python
score = "82"
bonus = 3

print(score + bonus)
```

A string and an integer cannot be added directly with `+`. To add three bonus points to the score, first convert the score to a number.

## Python’s Language Characteristics

When types are checked, how code executes, and what it is used for are different classification criteria.

| Category | Meaning | Example |
| --- | --- | --- |
| Static typing | Checks types before execution | Java, C, and C++ may declare a type with code such as `int score`. |
| Dynamic typing | Operations use the value’s type during execution | Python’s `score` can refer to an integer and later a string. |
| Compilation | Transforms code into another executable form | C/C++ expose compilation steps for creating an executable. |
| Interpreter | A program that reads and executes code | Python runs interactive input or scripts through an interpreter. |
| Scripting/glue | Connects files and existing tools | Python reads data files and passes them to analysis libraries. |

These categories are not mutually exclusive. Python’s official summary describes it as a high-level, interpreted language with dynamic semantics.

## Numbers and Strings

Adding number `1` to number `30` gives `31`. Adding string `"1"` to string `"30"` prints `301`.

```python
age_number = 30
age_text = "30"

print(age_number + 1)
print(age_text + "1")
```

Values read from CSV or Excel can arrive as strings depending on the reading method and data contents. Check their actual types before quantity or score calculations.

| Source data | Meaning to a person | What to check |
| --- | --- | --- |
| `"100"` | Quantity 100 | String or number? |
| `"0.92"` | Probability score 0.92 | Is `float` conversion needed before calculation? |
| `"True"` | Text that looks true | Is it an actual `bool`? |
| `"2026-06-24"` | A date | String or date type? |

## Comparisons and Booleans

A comparison produces a boolean value, `True` or `False`. Comparing score `92` against a minimum of `60` gives `True`. The code prints that result and its type, `<class 'bool'>`.

```python
score = 92
passed = score >= 60

print(passed)
print(type(passed))
```

`>=` checks whether the left value is greater than or equal to the right. Decisions such as whether a prediction score meets a threshold or data has missing values can also be expressed as booleans.

## Case: Checking a String Score Against a Pass Threshold

Suppose we check whether student Kim’s score `82.5` meets threshold `60.0`. The name is a string, the score and threshold are numbers, and the result is a boolean. The code prints `Kim`, `82.5`, and `True` in order.

```python
student_name = "Kim"
score = 82.5
threshold = 60.0

passed = score >= threshold

print(student_name)
print(score)
print(passed)
```

If the score arrives from a file as string `"82.5"`, the same comparison fails. The following raises `TypeError` because `>=` cannot compare `str` and `float`.

```python
score = "82.5"
threshold = 60.0

print(score >= threshold)
```

Use `float()` to convert the number written in the string into a numeric value. This code prints the types before and after conversion, `<class 'str'>` and `<class 'float'>`, then the pass result `True`.

```python
score_text = "82.5"
score = float(score_text)
threshold = 60.0

print(type(score_text))
print(type(score))
print(score >= threshold)
```

`score_text` refers to the original string and `score` to the converted number. Changing `threshold` in the last code block to `90.0` makes the result `False`. Matching types enables the comparison; changing the criterion changes its result.

## Checklist

- You can distinguish values, variables, and types.
- You can explain `=` as assigning a value to a name in Python.
- You can explain the basic differences among `int`, `float`, `str`, and `bool`.
- You can distinguish a numeric-looking string from an actual number.
- You can check a value’s type with `type()`.
- You can explain why a type error calls for checking the data’s state.
- You can explain why actual types must be checked even when values look numeric on screen.

## Sources and References

- Python Software Foundation, [What is Python? Executive Summary](https://www.python.org/doc/essays/blurb/){: target="_blank" rel="noopener noreferrer" }, Python.org, checked on 2026-07-20. Used to confirm Python's dynamic semantics, dynamic typing, and high-level built-in data structures.
- Python Software Foundation, [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm how prompts, numbers, strings, and lists are introduced in interactive Python examples.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm basic types such as `int`, `float`, `str`, and `bool`, and differences in operations by type.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm that Python objects have identity, type, and value.
