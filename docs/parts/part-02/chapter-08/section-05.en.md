# P2-8.5 Functions and Small Reuse

> Section ID: `P2-8.5`
> Version: `v2026.07.26`

In P2-8.1, we looked at values, variables, and types. From P2-8.2 to P2-8.4, we looked at ways of handling multiple values through lists, dictionaries, and loops.

Now one question remains:

What should we do if we need to use the same handling many times?

In Python, we use functions. A function is a structure that gives a name to repeated handling, receives the values it needs, performs a calculation, and then returns the result.

Here we explain the basic distinction among `function`, `parameter`, `argument`, and `return value`. The representative explanations of `value`, `variable`, and `loop` remain in P2-8.1, P2-8.4, and the [function glossary entry](/AiBook/en/reference/concept-glossary-alpha/f.en/#function). Here we focus on reading the input-process-output contract as a small unit of reuse.

Rather than memorizing all function syntax, this section builds the sense of how mathematical functions and Python functions are similar and different, and how to divide small data-processing code into reusable units.

In a more general sense, a function is a way to bundle `input, process, and output` into one unit. Python syntax is one way of expressing that unit, and the same perspective continues into mathematical functions, model functions, API functions, and library functions.

Rather than learning advanced function features here, we bundle the loops and data-structure handling from the previous sections into small reusable units. If we previously read lists, dictionaries, and loops separately, here we move to the point where that processing flow is given a name so that it can be used again. If we grab this handle first, then later, when reading library functions or model APIs, it becomes easier to read the `input-process-output contract` before the `syntax`.

| Term | Meaning to fix first in this section |
| --- | --- |
| function | a named unit of code that receives input, processes it, and returns a result |
| parameter | the input name written when defining a function |
| argument | the value actually passed when calling a function |
| return value | the result a function gives back after calculation |
| method | a function-like form called while attached to some value or object |

## Core Criteria: Functions and Small Reuse

- You can read the basic form of function definition with `def`.
- You can distinguish parameter and argument.
- You can explain that `return` is the syntax that returns a function result.
- You can separate repeated calculations and data processing into small functions.
- You can explain the difference between a mathematical function and a Python function.
- You can explain that a Python function can be stored in a variable like a value and passed into another function.
- You can distinguish at an entry level that a function and a method can have different calling forms.

## Learning Background

Here we look first not at function syntax but at `how to give repeated handling a name and reuse it`. The following three criteria become the basis for reading library functions and methods later.

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| A function bundles input, process, and output into one unit | It lets us read mathematical functions and code functions inside the same large frame. | Understand it as named code that receives values and returns results. |
| If the same handling repeats, it is often easier to separate it as a function | It helps us understand why small data-processing code turns into a reusable structure. | Read things like pass/fail judgment or normalization as functions. |
| `print` and `return` play different roles | It is important for distinguishing execution output from calculation result. | Be able to explain that showing something on screen is different from returning something into the next calculation. |

## Main Learning Content

### A Function Is a Way to Separate a Processing Unit with a Name

In general, a function is a unit that receives input, performs some processing, and returns the result. Mathematics emphasizes the relation between input and output, while programming expresses that relation as code that can actually run.

In Python, we give a function a name with `def` and write the needed input names as parameters.

The following code judges pass or fail based on a score.

Problem situation: Before dividing code into a function, we want to see code that directly judges one score first.
Input: The score value `82`.
Expected output: The string `pass`.
Concept to check: Repeated judgment can first be expressed through an ordinary conditional.

```python
# This example checks how a function connects input and output as a small reusable unit.
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

If this judgment is used only once, we can leave it as it is. But if we need the same judgment again and again for many scores, the code begins to repeat.

If we use a function, we can give that handling a name.

Problem situation: We want to see an example where the same pass/fail judgment is bundled into a function so it can be reused many times.
Input: The function `pass_or_fail` and the scores `82`, `55`.
Expected output: `pass`, `fail` for each score.
Concept to check: A function lets us name repeated handling and use it again.

```python
# This example checks how a function connects input and output as a small reusable unit.
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail` is the function name. `score` is the input name used inside the function. `return` sends the result back outside the function.

In this section, we understand a function by the following standard:

A function is named code that receives input, processes it, and returns a result.

| Perspective | General explanation | In Python |
| --- | --- | --- |
| function | a unit that bundles input, process, and output | defined with `def` |
| input | the value that the function will handle | distinguished into parameter and argument |
| output | the result that will be passed into the next calculation | returned with `return` |

### Mathematical Functions and Python Functions

In mathematics, a function is usually explained through the relation between input and output.

$$
f(x) = x + 1
$$

In Python, we can write it like this.

Problem situation: We want to see the smallest example that moves the mathematical function \(f(x)=x+1\) into a Python function.
Input: The input value `3`.
Expected output: `4`.
Concept to check: The input-output relation of a mathematical function can also be expressed as a function in Python.

```python
# This example checks how a function connects input and output as a small reusable unit.
def f(x):
    return x + 1

print(f(3))
```

The two are similar. There is an input `x`, and there is a result.

But they are not completely the same.

| Perspective | Mathematical function | Python function |
| --- | --- | --- |
| central concern | the relation between input and output | the code that runs and the result it produces |
| expression | \(f(x) = x + 1\) | `def f(x): return x + 1` |
| side effect | usually treated as a pure relation | can print, save files, or change a list |
| error | handled mathematically if outside the domain | can raise type errors, key errors, or runtime errors |

In AI practice, we need both perspectives.

- A loss function should be understood as a mathematical relation.
- A Python function lets us reuse that calculation in code.
- A library function lets us trust and use its input-output contract even without knowing its internal implementation.

### Distinguishing Parameter and Argument

Once we have seen that both mathematical functions and Python functions receive input, we can distinguish the terms that appear often in Python documents. When learning functions, the words parameter and argument appear.

Problem situation: We want to distinguish parameter and argument through a real call example.
Input: The function `add_bonus(score, bonus)` and the call arguments `80`, `5`.
Expected output: The added result `85`.
Concept to check: The names on the function-definition side are parameters, and the actual values passed at call time are arguments.

```python
# This example checks how a function connects input and output as a small reusable unit.
def add_bonus(score, bonus):
    return score + bonus

result = add_bonus(80, 5)

print(result)
```

In this code, `score` and `bonus` are parameters. They are the names used inside the function definition for the values the function will receive.

`80` and `5` are arguments. They are the actual values passed when calling the function.

| Distinction | Location | Example |
| --- | --- | --- |
| parameter | the name used when defining the function | `score`, `bonus` |
| argument | the actual value inserted when calling the function | `80`, `5` |
| return value | the result returned by the function | `85` |

This distinction keeps appearing later when reading model functions, loss functions, API functions, and library-function documents.

### `return` Sends Back a Result

`return` is the syntax that sends the result calculated by a function back to the place where the function was called.

Problem situation: We want to see an example where the result of a function is reused in the next calculation.
Input: The score `82`.
Expected output: The normalized result `0.82`.
Concept to check: `return` sends the function result back to the caller.

```python
# This example checks how a function connects input and output as a small reusable unit.
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

When `normalize_score(82)` runs, the result `0.82` is returned. That result is then attached to the name `normalized`.

`print()` and `return` are different.

Problem situation: We want to compare the fact that what is shown on screen can differ from the actual returned value.
Input: The score `82`.
Expected output: Inside the function, `82` is printed, but the outside variable `result` receives `None`.
Concept to check: `print()` is output for display, while `return` is delivery of a calculation result.

```python
# This example checks how a function connects input and output as a small reusable unit.
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

This function prints `82` to the screen, but it does not return a value. In Python, if a value is not explicitly returned, the result is usually read as `None`.

In this section, we distinguish the following.

- `print()` is output shown to a human.
- `return` is the action that returns a result for the next calculation.

## Detailed Learning Content

### Separate Repeated Calculations into Functions

If we give a repeated calculation a name, the intention of the code becomes visible.

Problem situation: We want to see an example where score normalization is separated into a function and reused in a loop.
Input: The score list `scores`.
Expected output: The normalized score list `normalized_scores`.
Concept to check: If the same calculation appears inside a loop, intention becomes clearer when it is separated as a function.

```python
# This example checks how a function connects input and output as a small reusable unit.
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

Now, before the expression `score / 100`, the intention `normalize` is visible first.

When the calculation is very simple, it is not always necessary to divide it into a function. But a function becomes useful when the same calculation is used in several places, or when giving it a name makes the intention clearer.

### A Function That Processes One Piece of Data

In AI practice, we often create functions that process one data sample.

Problem situation: We want to see a function that checks whether one sample contains all required keys.
Input: A sample dictionary with the keys `text` and `label`.
Expected output: The validity result `True`.
Concept to check: A function can encapsulate the rule for checking one piece of data.

```python
# This example checks how a function connects input and output as a small reusable unit.
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(is_valid_sample(sample))
```

This function checks whether the sample has the keys `text` and `label`.

It can be used for many samples.

Problem situation: We want to see an example where the sample-check function we just made is applied repeatedly to several samples.
Input: The sample dictionary list `samples`.
Expected output: The `valid_samples` list containing only valid samples.
Concept to check: A function that processes one piece of data gains more reuse value when combined with a loop.

```python
# This example checks how a function connects input and output as a small reusable unit.
def is_valid_sample(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

valid_samples = []

for sample in samples:
    if is_valid_sample(sample):
        valid_samples.append(sample)

print(valid_samples)
```

This structure is small, but important.

- The loop pulls out several samples one by one.
- The function checks one sample.
- The conditional changes the handling based on the result.

This kind of small combination becomes the basic shape of later preprocessing, evaluation, and filtering code.

### We Can Give Default Values

We can give default values to function parameters.

Problem situation: We want to see how a default value works in a function where the threshold is not changed often.
Input: `score`, the default `threshold=60`, and the explicitly supplied `threshold=90`.
Expected output: Different pass/fail results for the same score according to the threshold.
Concept to check: A default parameter lets the function keep a default behavior even when the argument is omitted.

```python
# This example checks how a function connects input and output as a small reusable unit.
def pass_or_fail(score, threshold=60):
    if score >= threshold:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(82, threshold=90))
```

In the first call, no threshold was given explicitly, so `60` is used. In the second call, `threshold=90` is specified directly.

We often see this shape again in AI tools and libraries.

- `batch_size=32`
- `learning_rate=0.001`
- `shuffle=True`
- `max_tokens=100`

Default values are convenient, but if we use them without knowing what the default is, we can misunderstand the behavior of the code. That is why we need the habit of checking default values in library documents.

### A Python Function Can Be Treated Like a Value

To someone who learned C or Java first, a Python function can look a little different. In Python, functions are also objects. So a function name can be read not only as the label of a code location, but as a name that points to a function object.

For example, we can store a function under another name.

Problem situation: We want to confirm that a function can be stored under another variable name and called like a value.
Input: The function `normalize_score` and the new name `normalize`.
Expected output: The result `0.82` from `normalize(82)`.
Concept to check: A Python function is an object, so it can be stored in a variable and referred to by another name.

```python
# This example checks how a function connects input and output as a small reusable unit.
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize` did not create a new calculation. It only points to the same function object as `normalize_score` under another name. This feeling can seem unfamiliar, but it appears often in Python library code.

We can also pass a function as an argument to another function.

Problem situation: We want to see an example where one function is passed as an argument into another function and applied inside a common repetition logic.
Input: The score list `scores` and the function `normalize_score`.
Expected output: The normalized score list made by `apply_to_scores`.
Concept to check: In Python, functions can also be passed like other values.

```python
# This example checks how a function connects input and output as a small reusable unit.
def normalize_score(score):
    return score / 100

def apply_to_scores(scores, function):
    results = []
    for score in scores:
        results.append(function(score))
    return results

scores = [82, 75, 91]

print(apply_to_scores(scores, normalize_score))
```

In this example, `apply_to_scores()` receives both a list of scores and a function. It then applies that function to each score. Here, the function is used not only as `a piece of code to run`, but like `a value that can be passed`.

This style appears often later in data processing and AI libraries.

- A sorting standard is passed as a function.
- A preprocessing function is passed into repeated handling.
- A metric function is passed into training code.
- A callback function is used to specify behavior at a specific time.

This section does not cover advanced functional programming. The current main text does not separately expand functional programming itself, and the required range here stops at the intuition that `a function can be passed like a value`. Still, if we know that Python functions can be passed like values, library APIs feel less unfamiliar.

### Functions and Methods Have Different Centers of Calling

When reading Python code, we see both code that calls like `function(value)` and code that calls like `value.method()`. In this section, we do not enter the detailed concept of classes. We only distinguish the calling shapes of function and method.

A function is an independently defined unit of processing. A method looks like a function that is called while attached to an object.

Problem situation: I want to compare the shapes of an independent function call and string method calls at once.
Input: The string `text = " AI is Useful "`.
Expected output: The results of `clean_text(text)`, `text.strip()`, and `text.lower()` are each printed.
Concept to check: A function is called through an independent name, while a method is called while attached to a value or object.

```python
# This example checks how a function connects input and output as a small reusable unit.
def clean_text(text):
    return text.strip().lower()

text = " AI is Useful "

print(clean_text(text))
print(text.strip())
print(text.lower())
```

Here, `clean_text(text)` is an independent function call, and `strip()` and `lower()` are methods provided by the string object. They are called with parentheses like functions, but methods have a target object in front of them.

In this section, we remember only the following level.

| Expression | Entry-level explanation | Example |
| --- | --- | --- |
| function | an independent named processing unit | `clean_text(text)` |
| method | a function-like form called while attached to a value or object | `text.strip()` |

Classes and objects return in the P2-8.6 supplementary learning section. Here we only distinguish that `function(value)` and `value.method()` both `call behavior`, but the center of the call is different.

### If One Function Does Too Many Things, Split It

Small functions make input, process, and output clear. By contrast, if one function does too many things, the range of its responsibility becomes blurry.

For example, imagine one function that contains all of the following jobs.

1. Read a file.
2. Remove empty rows.
3. Convert scores into numbers.
4. Calculate the average.
5. Save the result.

Such a function can look simple at first, but later it becomes hard to change only part of it.

In this section, we use the following questions when deciding whether to split a function.

- Does this function do one thing?
- Does the function name explain the actual behavior well?
- Are the input and output clear?
- Are screen output and returned result mixed together?
- Is the same handling repeated in many places?

These standards are useful in AI practice as well. If data loading, preprocessing, model execution, and evaluation are separated a little, it becomes easier to find errors.

## Cases and Examples

### A Small Reuse Example

The following example lightly cleans text samples and keeps only the samples that are not empty.

Problem situation: We want to see an example where two small functions are combined to clean and filter several pieces of text.
Input: The text list `texts`, which contains spaces and empty strings.
Expected output: `cleaned_texts`, which keeps only cleaned and non-empty text.
Concept to check: Functions create small processing units, and loops apply those units to several pieces of data.

```python
# This example checks how a function connects input and output as a small reusable unit.
def clean_text(text):
    return text.strip().lower()

def is_not_empty(text):
    return len(text) > 0

texts = [" AI is Useful ", "", " Models can FAIL "]
cleaned_texts = []

for text in texts:
    cleaned = clean_text(text)
    if is_not_empty(cleaned):
        cleaned_texts.append(cleaned)

print(cleaned_texts)
```

This code is simple as Python syntax, but it shows an important data-processing flow.

- `clean_text()` cleans one piece of text.
- `is_not_empty()` checks one piece of text.
- The loop applies the same handling to several texts.
- The result is stored in a new list.

When many such small functions gather, they help later when reading Pandas, NumPy, and machine learning library code.

### Case 1. Why Should We Not Keep Copying the Same Normalization Calculation?

Suppose a learner copied score-normalization code into several notebook cells. It may look like quick progress at first, but later, when the normalization standard has to change, every cell must be found and edited again.

The first human criterion may be `it is short, so let me just write it once more`. But once the same handling starts repeating, it becomes easier both to read and to modify if we separate `what named job this handling is` before focusing on the calculation expression itself.

This is exactly the point where a function becomes necessary. If we bundle input, process, and output into one unit and give it a name, then when the same calculation is used again we reduce code duplication and reveal intention more clearly. The reason we distinguish `print` and `return` is also to separate what a person sees from what the next calculation receives.

The confirmable result appears in the number of places that need editing. If changing the normalization standard requires editing only one function and all calling results change together, then the reuse structure is better organized than simple copied repetition.

## Practice and Examples

The following small exercises are enough to recheck the core of this section.

- Make a function that receives one score and returns a grade, then apply it repeatedly to several scores.
- Make one function that only uses `print()` and another that uses `return`, and compare the difference in results.
- Separate a function that cleans one string and a function that checks whether it is empty, and then filter several texts.

## Checklist

- You can read a function definition that starts with `def`.
- You can distinguish parameter and argument.
- You can explain the difference between `print()` and `return`.
- You can separate a repeated calculation into a function.
- You can make a function that handles one piece of data and reuse it in a loop.
- You can explain that a Python function can be stored in a variable and passed as an argument to another function.
- You can explain the difference in calling shape between a function and a method.
- You can explain that a function name should reveal the intention of the code.
- You can explain why a function turns repeated handling into a named reusable unit.

## Sources and References

- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as the official basis for `def`, parameters, `return`, and function-call examples.
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm default-parameter examples and the caution about mutable defaults.
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm function-definition syntax, parameter lists, and function-object creation.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as background for the explanation that functions can be treated as objects in Python.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as the basis for distinguishing function-call and method-call forms at an introductory level.
