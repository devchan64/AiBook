# P2-2.1 Rereading Variables, Functions, and Expressions

> Section ID: `P2-2.1`
> Version: `v2026.07.20`

In P2-1.2, we established the perspective that formulas, code, and data are different ways of showing the same computation. Now we recover the basic notation that appears first whenever you read a formula.

\[
x
\]

\[
y = f(x)
\]

\[
\mathrm{loss} = f(\mathrm{prediction}, \mathrm{target})
\]

These expressions may have felt too basic to matter when you first learned mathematics long ago. But in AI documents, if you cannot read variables, functions, and expressions, it becomes hard to locate models, inputs, outputs, loss, and parameters.

Here, the focus is on building the habit of reading what the symbols inside a formula point to as `what value`, `what relationship`, and `what computation`.

Here, we reorganize again `variable`, `function`, `expression`, `input`, and `output`. If 1.2 gave you the sense that formula, code, and data are different faces of the same computation, this section organizes the minimum symbolic grammar needed to read that computation.

## Goals of This Section

- You can read a variable as a name attached to a value or data.
- You can read a function as a relationship that turns input into output.
- You can view an expression as a compressed expression of a computable relationship or procedure.
- You can interpret `y = f(x)` as the simplest form of model inference.
- You can connect mathematical variables and code variables without confusing them.

## Three Criteria

The following three viewpoints act as standards while reading the main text.

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| A variable is a name that points to a value, not the value itself | It prevents you from immediately confusing the symbol with the thing it refers to. | Understand that a variable is a name that holds a value. |
| A function is a relationship that turns input into output | It lets you read models and rules inside the same structure. | Understand that `y = f(x)` is read as input-transformation-output. |
| An expression is a short way of writing a calculation or relationship | It becomes the starting point for interpreting formulas for loss, prediction, and error. | Understand that an expression is a compressed form of a computational procedure. |

## A Variable Is a Name That Points to a Value

A variable is a name that points to a value. In mathematics, short symbols such as `x`, `y`, `n`, and `w` are often used.

\[
x = 3,\quad y = 2,\quad n = 4
\]

Here, `x`, `y`, and `n` are not the values themselves. They are names that point to the values. In AI documents, variable names often carry more meaning. For example, `x` is often used for input data, `y` for an answer or target, `w` for weight, `b` for bias, `ŷ` for the prediction made by a model, and `L` for loss.

The symbols can differ from document to document. So when you see a formula, the first thing to find is: `What has this text defined this symbol to mean?` Even the same `x` may be one value in one document, a vector in another, and an entire dataset in another.

## Variables in Code and Variables in Math

Variables are also used in Python code.

Problem situation: check in the simplest example how variables in mathematics correspond to variables in code.
Input: two integer values and the variables that hold their sum.
Expected output: there is no printed output, but a structure is created in which variable names point to concrete values.
Concept to check: a code variable is also a name that points to a value, but it handles a concrete storage target that can be reassigned during execution.

```python
# x and y are named values used in the calculation.
x = 3
y = 2

# total is the result of the expression that adds the two values.
total = x + y
```

Example result:

```text
x points to 3, y points to 2, and total points to 5.
```

Mathematical variables and code variables are similar. Both attach a name to some value. But they are not completely the same.

| Perspective | Variable in Math | Variable in Code |
| --- | --- | --- |
| Main role | express a relationship compactly | store a value and refer to it during execution |
| Change of value | fixed or changing depending on context | can be reassigned during execution flow |
| Data type | usually inferred from context | has a concrete type such as int, float, string, or array |
| Error | hard to interpret if the definition is ambiguous | type, shape, or naming errors can appear during execution |

This difference matters. In a formula, it may be enough to say that `x` is a vector. In code, however, you must check what shape `x` actually has, what type it has, and whether it is empty.

Problem situation: turn the mathematical `x` into a real array value in code and inspect its shape and type.
Input: the NumPy array `x` holding three values.
Expected output: the array value, `shape`, and `dtype` are printed.
Concept to check: in code, it is not enough to read only the name; the actual value, shape, and type must also be checked together.

```python
import numpy as np

# x is an array variable that contains several numbers.
x = np.array([1, 2, 3])

print(x)

# shape and dtype are observation points for the array's form and value type.
print(x.shape)
print(x.dtype)
```

Example execution result:

```text
[1 2 3]
(3,)
int64
```

This example is the smallest example that turns the mathematical notation `x` into a value that can be checked in code. What the reader must see immediately here is that the name `x` alone is not enough. The value itself, its `shape`, and its `dtype` must be read together.

## A Function Is a Relationship That Turns Input into Output

A function is a relationship that takes an input and produces an output.

\[
y = f(x)
\]

This expression is read as `x goes in, passes through the relationship or rule called f, and y comes out`.

In an AI context, `f` can be a rule written directly by a person, or it can be a learned model. For example, if it is a rule-based function, you can read it as "if age is 19 or older, classify as adult." If it is a learned model, you can read it as "predict the purchase possibility from input features."

In code, both may be called like functions.

Problem situation: confirm that even a rule-based judgment can appear in code as a function call.
Input: the function `is_adult`, which receives an age and returns whether the person is an adult, and the input `20`.
Expected output: `True` is printed.
Concept to check: a function is the relationship that receives input and produces output, and this can be seen in the simplest rule example.

```python
def is_adult(age):
    # age is the input to judge, and True/False is the function output.
    return age >= 19

print(is_adult(20))
```

Example execution result:

```text
True
```

A model can also be treated broadly as a function that takes input and produces output.

Problem situation: look at the minimum form in which a model call is also read like a function call.
Input: the call expression `model(input_data)` that takes `input_data` and creates a prediction.
Expected output: there is no printed output, but it shows the structure that stores the result in the variable `prediction`.
Concept to check: in an AI context, a model can also be read as a function that turns input into output.

```python
# input_data is the input passed into the model, and prediction is the value returned by it.
prediction = model(input_data)
```

However, a machine-learning model is different from a simple rule function. Inside the model are learned parameters, and even with the same function structure, the output changes depending on the learned parameter values.

## An Expression Represents a Computational Relationship

An expression is something formed by values, variables, operators, and functions to represent a computational relationship.

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

In mathematical documents, expressions appear briefly, but they contain an order of computation.

\[
(\mathrm{prediction} - \mathrm{target})^2
\]

This expression can be read as subtracting the target value from the predicted value, then squaring that gap so that the magnitude of the error becomes positive.

In code, it can be written as follows.

Problem situation: unfold the expression `(prediction - target)^2` into a code procedure and compute it.
Input: the prediction value `2.8` and the target value `3.0`.
Expected output: the squared-error value is printed.
Concept to check: an expression is not an abstract symbol game but something that can be unfolded into a real computation order.

```python
# prediction is the model's predicted value, and target is the real value to compare against.
prediction = 2.8
target = 3.0

# error and squared_error show how far the prediction is from the target.
error = prediction - target
squared_error = error ** 2

print(squared_error)
```

Example execution result:

```text
0.04000000000000007
```

What matters here is that an expression is not mere symbol play. An expression decides what values are compared, what values are made larger or smaller in importance, and what result is produced.

## Basic Relationships Often Seen in AI

If you simplify the relationships often seen in AI documents as much as possible, they become the following.

```text
prediction = model(input)
loss = compare(prediction, target)
updated_parameters = update(parameters, loss)
```

This is not an exact statement of a real learning algorithm. But it helps you fix the places of variables, functions, and expressions.

- `input`: the data that enters the model
- `model`: the function or system that turns input into output
- `prediction`: the output produced by the model
- `target`: the value that acts as the comparison standard
- `loss`: the value that expresses numerically the gap between prediction and target
- `parameters`: the values adjusted during learning
- `update`: the procedure that changes parameters so that loss decreases

Once you know this structure, the formulas you meet later feel a bit less foreign. Even a complex formula can eventually be read as a way of naming values, transforming them through relationships, and comparing the result of a computation.

## Names Help Understanding, but They Do Not Guarantee It

Variable names help understanding. Names such as `input_data`, `target`, and `prediction` are easier to read than only `x` and `y`. But you should not trust the names alone.

Problem situation: look at a case where a variable name looks plausible, yet the value meaning and structure still need to be checked separately.
Input: two lists that look like predictions and answers.
Expected output: there is no printed output, but it shows a state in which the name alone does not reveal the full type and meaning of the values.
Concept to check: the variable name is only a clue, and the real value's shape and meaning must still be checked additionally.

```python
# prediction and target are lists for comparing several predicted and real sample values.
prediction = [0, 1, 1, 0]
target = [0, 1, 0, 0]
```

From the names alone, this code seems to tell us what prediction and target are. But in reality, we still have to check whether each value is a class index, a probability, or a true/false value, whether the two data bundles are the same length, and whether their order matches.

In AI, errors often occur at the connection point between formulas and data or code. Even when a variable name looks reasonable, you still have to check the shape, type, meaning, and unit of the actual value.

## Case Study

### Case 1. The Moment When `y = f(x)` Stops Looking Like an Abstract Formula and Starts Reading as Model Execution

Suppose a learner sees `y = f(x)` and feels that it is only a function problem from an old math class. But in AI documents, this expression often appears as the most basic computational structure: `put input x into model f and obtain output y`.

For example, suppose customer information is the input, and the model outputs purchase probability. Then `x` can be read as the bundle of customer features, `f` as the learned model, and `y` as the prediction score or classification result. That is, the three symbols each occupy the place of data, model, and output.

This case shows why variables and functions are not merely simple math words. You need to connect `x` and `y` not only to names of values, but also to contexts such as input, answer, prediction, and weight, in order to read AI formulas.

In the end, what matters is not the symbol itself but the role. Once you can read what goes in and what comes out of this expression, you can interpret later additions such as loss and parameters on top of the same structure.

## Checklist

- Can you explain a variable as a name attached to a value or data?
- Can you explain a function as a relationship that turns input into output?
- Can you explain an expression as a compressed expression of a computable relationship?
- Can you read `y = f(x)` as the basic structure of AI model execution?
- Can you explain that code variables and mathematical variables are similar, but differ in type, shape, and reassignment?
- Can you explain that you should not trust variable names alone, but also check meaning, type, and shape?
- Can you check together the value's meaning, the input/output relation, and the type and shape in code when reading variables, functions, and expressions?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked on 2026-07-19.
- Python Software Foundation, [Assignment statements](https://docs.python.org/3/reference/simple_stmts.html#assignment-statements){: target="_blank" rel="noopener noreferrer" }, Python Language Reference, checked on 2026-07-19. This is the direct reference for code variables and reassignment.
- NumPy Developers, [numpy.ndarray](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This official reference supports the examples that check an array variable's `shape` and `dtype`.
