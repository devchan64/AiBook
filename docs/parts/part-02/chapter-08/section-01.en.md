# P2-8.1 Values, Variables, and Types

> Section ID: `P2-8.1`
> Version: `v2026.07.20`

In P2-7, we looked at where code runs. You can run it in Colab, or you can run the Python interpreter on the terminal of a local PC.

From now on, we recover Python syntax very narrowly. But the purpose is not to memorize how to use Python. It is to establish general concepts that you will repeatedly meet later when reading formulas and data as code.

Here, rather than becoming “a person who is good at Python,” we focus on recovering the basic words of Python enough to read mathematical calculations, small data checks, and NumPy and Pandas practice.

In other words, the reason for learning these words now is also clear. Later, when reading lists, dictionaries, NumPy arrays, and Pandas DataFrames, even small examples quickly become blocking if you cannot distinguish `is the thing being handled now a value?`, `what is its name?`, and `is it a number or a string?`

The first words are value, variable, and type.

Here, we explain the basic distinction among `value`, `variable`, and `type`. These three words are not expressions trapped only inside Python. They are the minimum units shared by most programming languages and data-processing tools. When you meet these concepts again later in Part 2, also use the [Concept Glossary](/AiBook/reference/concept-glossary/) as a reference point.

## Three Sentences to Leave from This Section

When reading for the first time, it is enough to first hold onto the following three sentences.

1. A value is the data itself that computation actually handles.
2. A variable is a name attached so that the value can be called again.
3. A type is kind information that distinguishes what can be done with that value.

In other words, later when reading lists, dictionaries, NumPy arrays, and Pandas DataFrames, you first ask `is the thing I am seeing now a value?`, `by what name is it being referred to again?`, and `because it is what type, which operations are possible?`

If the execution environment in the previous chapter dealt with `where and with which program should this computation run?`, here we read which values are actually created in that execution place, by which names they are referred to again, and by which types they are distinguished. In the next sections, these values expand into bigger structures and processing flows such as lists, dictionaries, iteration, and functions.

| Term | Meaning to establish first in this section |
| --- | --- |
| value | The data itself that computation actually handles. |
| variable | A name attached to refer to the value again. |
| type | Kind information that distinguishes what can be done with that value. |
| assign | The action in Python that connects a value to a name. |
| basic type | Frequently encountered value kinds such as `int`, `float`, `str`, and `bool`. |

## Goal of This Section

- You can distinguish value, variable, and type.
- You can explain that `=` does not mean exactly the same thing as a mathematical equal sign, but in Python it is syntax that assigns a value to a name.
- You can explain the basic differences among `int`, `float`, `str`, and `bool`.
- You can check the type of a value with `type()`.
- You can explain that a string that looks like a number must be distinguished from an actual number.
- You can explain why Python looks like a dynamically typed language, and why that still does not mean types are mixed loosely without rules.

## Three Criteria

Here, rather than Python syntax itself, we look at how code handles data. The following three criteria are the foundation for reading later sections on lists, dictionaries, and iteration.

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| A value is the thing computation actually handles | This is where the difference begins in why numbers, strings, and truth values behave differently | Understand that `3`, `"AI"`, and `True` inside code are all values |
| A variable is a name for referring to a value again | This is needed to distinguish the mathematical equal sign from Python's `=` | You should be able to explain that `score = 82` is not an equation but naming |
| A type determines which operations are possible on a value | It explains why strings and numbers mix and cause errors | Understand that even the same `+` can behave differently depending on the kind of value |

## A Value Is the Actual Thing Computation Handles

In general, a value is the object of computation. Real data handled by a program, such as numbers, text, and truth values, is a value.

In Python, values such as numbers, strings, and truth values are directly created inside code and participate in computation.

For example, all of the following are values.

- `3`
- `3.14`
- `"AI"`
- `True`
- `False`

Values can stand alone, and they can also participate in computation.

Problem situation: I want to first see the smallest example where a single numeric value directly participates in computation.
Input: the integer values `3` and `2`.
Expected output: the expression `3 + 2` that adds the two values.
Concept to check: a value can appear directly in code and become the input of an operation.

```python
3 + 2
```

Problem situation: I want to check how the same `+` symbol behaves differently for strings.
Input: the strings `"AI"` and `"Book"`.
Expected output: an expression that joins the two strings.
Concept to check: even the same operator can have different meanings depending on the type of the value.

```python
"AI" + "Book"
```

Both lines above use `+`, but their meanings are different. The first is numeric addition, and the second is the action of joining strings. Even the same symbol can behave differently depending on the type of the value.

The official Python tutorial also introduces numbers and text first while using the Python interpreter like a calculator. In this section, we use that flow as the starting point for reading Python code.

In summary, it looks like this.

| Perspective | General explanation | In Python |
| --- | --- | --- |
| value | The actual data that computation handles | Can be written directly in code, such as `3`, `3.14`, `"AI"`, and `True` |
| operation | Processing applied to a value | Expressed through `+`, `>=`, function calls, and so on |
| type | Information limiting what actions are possible on a value | Even the same `+` can behave differently for numbers and strings |

## A Small Example Showing the Relationship Between Name and Type

In Python, the same name can point to values of different types as time passes.

Problem situation: I want to directly check that the same variable name can point to values of different types.
Input: first `82` as an integer, then `"82"` as a string, both assigned to `score`.
Expected output: the type of `score` changes from `int` to `str`.
Concept to check: in Python, values have types rather than names, and when reassignment happens, the type can also change.

```python
score = 82
print(type(score))

score = "82"
print(type(score))
```

The first `score` points to an integer (`int`). The second `score` points to a string (`str`). The name is the same, but the value changed, and the type of the value also changed.

Because of this, Python can feel shorter in writing procedure at the beginning. You do not have to write a type declaration first every time you create a variable.

But a shorter writing procedure does not mean you can mix any values however you want.

Problem situation: I want to see what kind of problem happens if I try to add a string and a number as they are.
Input: the string `"82"` and the integer `3`.
Expected output: an example where the computation does not proceed as intended because the types do not match.
Concept to check: even if it looks like a dynamically typed language, operations that do not fit the types can still raise errors.

```python
score = "82"
bonus = 3

print(score + bonus)
```

This code does not work as intended. That is because a string and a number cannot be added directly.

So we organize this example by the following criteria.

- Even without writing many type declarations first, you can run small code quickly.
- Read with the criterion that values have types more than names do.
- If types do not fit during execution, an error can occur.
- That is why the habit of checking with `type()` is important when handling data.

## A Variable Is a Name Attached to a Value

In general, a variable is a name attached so that a value can be reused. The declaration style and type rules differ by language, but the role of “referring to a value by a name” appears in common.

In Python, you attach a name to a value by using `=`.

Problem situation: I want to check the most basic pattern of attaching names to values and then computing again with those names.
Input: `width = 20`, `height = 45`.
Expected output: `area`, the product of the two values, is printed.
Concept to check: `=` is not a mathematical equal sign but assignment syntax that connects a name and a value.

```python
width = 20
height = 45
area = width * height
print(area)
```

Here, `width`, `height`, and `area` are variables.

When seeing `x = 3` in mathematics, people often read it like an equation. But in Python code, `width = 20` is closer not to a claim that “the left and right are equal,” but to an execution sentence meaning “attach the name `width` to the value `20`.”

Therefore, you can also attach a different value again to the same name like this.

Problem situation: I want to confirm that when the same variable name is used again, only the last value remains.
Input: assign `10` and then `12` to `score`.
Expected output: in the end, `12` is printed.
Concept to check: reassignment makes the same name point to a different value.

```python
score = 10
score = 12
print(score)
```

The printed value is `12`. That is because the name `score` first pointed to `10`, and later came to point to `12`.

Variables are sometimes explained as “boxes.” But in Python context, the criterion “a name attached to a value” is more accurate. This difference matters especially when dealing with mutable values such as lists. That content is revisited in P2-8.2.

| Perspective | General explanation | In Python |
| --- | --- | --- |
| variable | A name for referring to a value | If you understand it as a name pointing to an object, it connects later to explanations of lists |
| assignment | The action connecting a name and a value | Uses `=` like `score = 82` |
| reassignment | The action by which the same name comes to point to a different value | Can attach a value of a different type to the same name, such as `score = "82"` |

## A Type Limits What Can Be Done with a Value

In general, a type is the kind of a value. More broadly, type is information that determines which computations can be done with that value and which cannot.

In Python, you can check the type of a value with `type()`.

Problem situation: I want to see at once which types representative basic values are read as.
Input: `3`, `3.14`, `"AI"`, `True`.
Expected output: the result of `type(...)` for each value.
Concept to check: basic numbers, strings, and booleans are distinguished as different types.

```python
print(type(3))
print(type(3.14))
print(type("AI"))
print(type(True))
```

Representative basic types are as follows.

| Type | How to read it | Example | Meaning |
| --- | --- | --- | --- |
| `int` | integer | `3`, `100` | whole number |
| `float` | floating-point number | `3.14`, `0.5` | number with a decimal part |
| `str` | string | `"AI"`, `"42"` | text string |
| `bool` | boolean | `True`, `False` | true or false |

The official Python documentation explains that whole-number values are of type `int`, and numbers with fractional parts are of type `float`. Text is handled as strings of type `str`.

## Python's Place Among General Language Types

Only after seeing values, variables, and types can we see Python's characteristics a little more accurately. Programming languages can be divided by many criteria, but here we look only at a few perspectives needed for reading Python code, rather than memorizing a deep classification.

| Category | Common explanation | Important point when looking at Python |
| --- | --- | --- |
| static typing | A tendency to check the types of variables or expressions more strictly before execution | If you think of languages such as Java, C, or C++, you often first see type declarations like `int score` |
| dynamic typing | A tendency for values to have actual types during execution, while names point to those values | In Python, you attach a value to a name like `score = 82.5`, and the type of the value is checked during execution |
| compiled language | A case where a separate translation step before execution is prominently visible | In languages such as C/C++, the compilation stage can appear strongly from the beginning of learning |
| interpreted language | A case where the flow of running code and checking immediately stands out | Python supports a flow of quickly checking small code through the interactive prompt and script execution |
| scripting/glue language | A language often used to connect existing tools, files, and systems | Python is often encountered in practice that connects data files, libraries, and analysis tools |

This table is not for classifying languages rigorously. Actual languages and execution environments are more complex. What matters here is that Python is not so much “a language where you begin by declaring many types in advance,” but one where the flow of making values and checking through execution is strong.

The official summary of Python also describes Python as a high-level language with interpreted execution and dynamic semantics. That explanation connects to why, in this section, Python is used as an example language for quickly checking small calculations. But because type issues may not show up until execution, the habit of checking with `type()` is important.

## Even If It Looks Like a Number, It Can Be a String

A confusion you encounter often is between numbers and strings.

Problem situation: I want to confirm that even if they look similar on the surface, numbers and strings produce different computation results.
Input: the number `30` and the string `"30"`.
Expected output: on the number side, `31`; on the string side, a joined result such as `"301"`.
Concept to check: a string that looks like a number behaves differently from actual numeric computation.

```python
age_number = 30
age_text = "30"

print(age_number + 1)
print(age_text + "1")
```

`30` is a number. `"30"` is a string.

So `age_number + 1` becomes `31`, but `age_text + "1"` joins strings and becomes something like `"301"`.

This distinction is also important in AI practice. Values read from CSV files or Excel files may look like numbers on the surface but still come in as strings. Model calculations expect numeric types, but if the data is a string, the calculation fails or preprocessing becomes necessary.

For example, you can think about the following situations.

| Original data | Meaning a human sees | What must be checked in Python |
| --- | --- | --- |
| `"100"` | quantity 100 | Check whether it is a string or a number |
| `"0.92"` | probability score 0.92 | Check whether it should be converted to `float` |
| `"True"` | text that looks like truth | Check whether it is an actual `bool` |
| `"2026-06-24"` | date | Check whether it is a string or a date type |

In this section, instead of memorizing every type conversion, we leave as the criterion the point that “how a value looks” and “which type Python handles it as” can differ.

## Boolean Is the Basic Material of Condition Judgment

A boolean is a type that has the values `True` or `False`.

Problem situation: I want to see with a simple score threshold that a comparison operation creates a boolean value.
Input: `score = 92` and a threshold of `60`.
Expected output: the value `passed` and its type are printed.
Concept to check: the result of a comparison expression is of type `bool` and is either `True` or `False`.

```python
score = 92
passed = score >= 60

print(passed)
print(type(passed))
```

`score >= 60` is a comparison. The result of this comparison is `True` or `False`.

In AI practice, booleans are encountered often.

- Is the score above the criterion?
- Is there a missing value in the data?
- Did the prediction value exceed a threshold?
- Does it satisfy the condition for dividing training data and test data?

In Part 2 Chapter 5, we distinguished probability scores from service decisions. There too, the model score was a number, and the result of passing a policy condition led to action. In Python, this kind of condition judgment is expressed as a boolean value.

## A Small Data-Processing Example

The following example handles one student score as a number and checks whether it exceeds the criterion.

Problem situation: I want to see a small example like real data where name, score, criterion, and pass status are handled together.
Input: a student name, a score of `82.5`, and a threshold of `60.0`.
Expected output: the name, score, and pass status are printed in order.
Concept to check: a string, a floating-point number, and a boolean can all be used together in one example with different roles.

```python
student_name = "Kim"
score = 82.5
threshold = 60.0

passed = score >= threshold

print(student_name)
print(score)
print(passed)
```

If you separate the values and types here, it looks like this.

| Name | Value | Type | Meaning |
| --- | --- | --- | --- |
| `student_name` | `"Kim"` | `str` | student name |
| `score` | `82.5` | `float` | score |
| `threshold` | `60.0` | `float` | passing criterion |
| `passed` | `True` | `bool` | whether the criterion was passed |

This example is simple, but it repeats continuously later in data processing and model evaluation.

Data comes in as values. Variables attach names to those values. Types determine in what way those values can be computed.

## A Type Error Can Be a Good Signal

In Python, if types do not fit, an error can occur.

Problem situation: I want to see why a problem appears when comparing a string that looks like a number and an actual number.
Input: the string `"82.5"` and the float `60.0`.
Expected output: an example where comparison does not work as intended.
Concept to check: even if data looks like a number, if the actual type is different, comparison and computation can fail.

```python
score = "82.5"
threshold = 60.0

print(score >= threshold)
```

This code does not work as intended. `score` looks like a number, but it is actually a string, while `threshold` is a float.

When you meet an error like this, instead of seeing it as `Python is strange`, first change the question.

- What type is this value actually?
- Did it not come in as a string during file reading?
- Is it a value that should be converted into a number?
- Did I check it with `type()`?

In data processing, a type error is an annoying obstacle, but at the same time it is also a signal telling you the state of the data.

## Case Study

### Case 1. Why Does a Score Read from CSV Not Get Calculated?

Suppose a learner tries to read a student-score CSV and calculate the mean. On the screen, the values look like numbers such as `82.5`, `91.0`, and `77.0`, but when trying to add or compare them, they may not behave as expected.

The human default criterion is usually `if it looks like a number, it must be a number`. But in actual code, it may be a string such as `"82.5"`, and in that case addition or comparison does not behave numerically.

The distinction of `value`, `variable`, and `type` in this section is exactly the basic tool for reading this failure. A value is the actual data, a variable is the name attached to that value, and a type determines what operations are possible on that value. So more important than appearance is the habit of checking the actual type with `type()`.

The confirmable result is simple. Even if it looks the same as `82.5` on screen, if `type(score)` is `str`, conversion is needed before numeric computation; if it is `float`, it can be used immediately in numerical calculation.

## Checklist

- You can distinguish value, variable, and type.
- You can explain that Python's `=` is syntax for assigning a value to a name.
- You can explain the basic differences among `int`, `float`, `str`, and `bool`.
- You can distinguish a string that looks like a number from an actual number.
- You can check the type of a value with `type()`.
- You can explain that when a type error occurs, the state of the data should be checked first.
- You can first distinguish whether the current thing is the value itself, the name attached to it, or its type.
- You can explain why a value that only looks like a number may still need type checking before calculation.

## Sources and References

- Python Software Foundation, [What is Python? Executive Summary](https://www.python.org/doc/essays/blurb/){: target="_blank" rel="noopener noreferrer" }, Python.org, checked on 2026-07-20. Used to confirm Python's dynamic semantics, dynamic typing, and high-level built-in data structures.
- Python Software Foundation, [An Informal Introduction to Python](https://docs.python.org/3/tutorial/introduction.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm how prompts, numbers, strings, and lists are introduced in interactive Python examples.
- Python Software Foundation, [Built-in Types](https://docs.python.org/3/library/stdtypes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm basic types such as `int`, `float`, `str`, and `bool`, and differences in operations by type.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm that Python objects have identity, type, and value.
