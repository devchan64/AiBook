# P2-8.5 Functions and Small-Scale Reuse

> Section ID: `P2-8.5`
> Version: `v2026.09.15`

## Defining and Calling Functions

A function generally receives input, performs processing, and returns a result. Mathematics emphasizes the input-output relationship; programming expresses it as executable code.

Python uses `def` to name a function and parameters to name its inputs.

Score `82` meets the threshold `60`, so `pass` is printed. This version uses a conditional without a function.

```python
score = 82

if score >= 60:
    result = "pass"
else:
    result = "fail"

print(result)
```

For a single decision, this may be enough. Repeating the same decision for many scores, however, duplicates code.

Naming the decision `pass_or_fail` lets callers vary only the score. The outputs below are `pass` and `fail`.

```python
def pass_or_fail(score):
    if score >= 60:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(55))
```

`pass_or_fail` is the function name, and `score` names its input. `return` sends the result back to the call site and ends the current call. With `82`, it returns `"pass"` and never reaches `return "fail"`.

### Mathematical Functions and Python Functions

In mathematics, functions are usually described through input-output relationships.

$$
f(x) = x + 1
$$

The mathematical function \(f(x)=x+1\) can be implemented as follows. Passing argument `3` prints `4`.

```python
def f(x):
    return x + 1

print(f(3))
```

| Aspect | Mathematical function | Python function |
| --- | --- | --- |
| Main focus | Input-output relationship | Executed code and results |
| Notation | \(f(x) = x + 1\) | `def f(x): return x + 1` |
| Side effects | Usually treated as a pure relationship | Can print, save files, or change lists |
| Errors | Inputs outside the domain are treated mathematically | Can raise type, key, or execution errors |

AI exercises need both perspectives.

- Understand loss functions as mathematical relationships.
- Use Python functions to reuse those calculations as code.
- Use library functions through their input-output contracts without knowing every implementation detail.

### Parameters and Arguments

A parameter names an input in a function definition. An argument is the value supplied when calling it.

Adding bonus `5` to score `80` returns `85`. The definition uses parameters `score` and `bonus`; the call supplies arguments `80` and `5`.

```python
def add_bonus(score, bonus):
    return score + bonus

result = add_bonus(80, 5)

print(result)
```

| Term | Location | Example |
| --- | --- | --- |
| Parameter | Input name in the definition | `score`, `bonus` |
| Argument | Actual value at the call | `80`, `5` |
| Return value | Result sent back by the function | `85` |

### Returning and Printing

`return` sends the function's computed result back to its call site.

Divide score `82` out of 100 by 100 and return the result. The caller stores `0.82` in `normalized` and prints it.

```python
def normalize_score(score):
    return score / 100

normalized = normalize_score(82)

print(normalized)
```

`normalize_score(82)` returns `0.82`, which is assigned the name `normalized`.

`print()` and `return` are different operations.

`show_score(82)` prints `82`. Without a `return`, however, it returns `None`, so `print(result)` prints `None`.

```python
def show_score(score):
    print(score)

result = show_score(82)

print(result)
```

A function reaching its end without `return` returns `None`. The displayed `82` is not stored in `result`. Computing `result + 1` raises `TypeError`, because `None` cannot be added to an integer.

## Reusing Repeated Calculations

Giving a repeated calculation a name exposes its intent.

Applying `normalize_score()` to four scores prints `[0.82, 0.75, 0.91, 0.68]`. The loop retrieves scores; the function divides each by 100.

```python
def normalize_score(score):
    return score / 100

scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(normalize_score(score))

print(normalized_scores)
```

A simple expression does not always need a function. Functions help when the calculation appears in multiple places or a name makes its purpose clearer.

### Processing One Sample

AI exercises often use functions that process one sample.

Check whether both `"text"` and `"label"` keys exist. This input contains both, so the code prints `True`.

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

sample = {"text": "AI is useful", "label": "positive"}

print(has_required_keys(sample))
```

This checks key presence only. `{"text": "", "label": None}` also returns `True`. It does not check for empty text or an allowed label value.

The same function can process multiple samples.

Apply the key check to three samples. The second lacks `"label"`, so only the first and third dictionaries remain in the result list.

```python
def has_required_keys(sample):
    return "text" in sample and "label" in sample

samples = [
    {"text": "AI is useful", "label": "positive"},
    {"text": "missing label"},
    {"text": "Models can fail", "label": "negative"},
]

samples_with_keys = []

for sample in samples:
    if has_required_keys(sample):
        samples_with_keys.append(sample)

print(samples_with_keys)
```

### Default Parameter Values

Function parameters can have default values.

With the default threshold `60`, score `82` returns `pass`; with `threshold=90`, it returns `fail`. Only the threshold differs between these calls.

```python
def pass_or_fail(score, threshold=60):
    if score >= threshold:
        return "pass"
    return "fail"

print(pass_or_fail(82))
print(pass_or_fail(82, threshold=90))
```

The first call omits a threshold, so it uses `60`. The second supplies `threshold=90` explicitly.

AI tools and libraries commonly use this form.

- `batch_size=32`
- `learning_rate=0.001`
- `shuffle=True`
- `max_tokens=100`

Defaults are convenient, but assuming the wrong default leads to misunderstandings. Check the defaults in library documentation.

### Passing Function Objects

Python functions are objects, and function names refer to those objects.

`normalize = normalize_score` adds another name for the function object. `normalize(82)` also prints `0.82`.

```python
def normalize_score(score):
    return score / 100

normalize = normalize_score

print(normalize(82))
```

`normalize` does not define a new calculation; it refers to `normalize_score` under another name. Distinguish the function object `normalize_score` from its call result `normalize_score(82)`.

Pass scores `[82, 75, 91]` together with `normalize_score`. `apply_to_scores()` applies that function to each score and returns `[0.82, 0.75, 0.91]`; the outer `print()` displays it.

```python
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

`apply_to_scores()` receives both the list and the function. At `function(score)`, it calls the supplied function for the current score.

This pattern appears throughout data processing and AI libraries.

- Pass a function as a sorting key.
- Pass preprocessing functions to repeated processing.
- Pass metric functions to training code.
- Use callbacks to specify actions at particular times.

### Functions and Methods

`function(value)` calls a function by name; `value.method()` retrieves and calls a method on an object.

A function is an independently defined processing unit. A method looks like a function called through an associated object.

Apply whitespace removal and lowercasing to `" AI is Useful "`. `clean_text(text)` prints `ai is useful`, `text.strip()` prints `AI is Useful`, and `text.lower()` prints ` ai is useful ` with surrounding spaces intact.

```python
def clean_text(text):
    return text.strip().lower()

text = " AI is Useful "

print(clean_text(text))
print(text.strip())
print(text.lower())
```

`clean_text(text)` is an independent function call; `strip()` and `lower()` are methods provided by strings. Methods also use parentheses, but the target object appears before the method name.

| Form | Introductory explanation | Example |
| --- | --- | --- |
| Function | Named independent processing unit | `clean_text(text)` |
| Method | Function-like operation called through an object | `text.strip()` |

### Separating Processing Steps

Small functions make inputs, processing, and outputs clear. A function doing too many jobs obscures its responsibilities.

For example, suppose one function performs all these tasks:

1. Read a file.
2. Remove empty rows.
3. Convert scores to numbers.
4. Calculate the mean.
5. Save the result.

Such a function may look simple, yet changing just one part later can be difficult.

## Case: Removing Empty Text After Trimming

Clean `[" AI is Useful ", "", " Models can FAIL "]`, then remove empty strings. The output is `['ai is useful', 'models can fail']`.

```python
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

`clean_text()` cleans one string; `is_not_empty()` checks whether characters remain. Adding `"   "` to the input leaves the output unchanged because trimming makes it empty. Checking emptiness before cleaning would accept that length-3 string. Call order affects the result.

## Case: Changing the Maximum Score

Suppose division by 100 was copied into two places, then the exam maximum changed to 50. Updating only one place to `/ 50` makes score 40 become `0.8` in one place and `0.4` in the other.

Accepting the maximum as a parameter lets callers pass both score and maximum to one function. Both 80 out of 100 and 40 out of 50 return `0.8`.

```python
def score_ratio(score, maximum):
    return score / maximum

print(score_ratio(80, 100))
print(score_ratio(40, 50))
```

Changing the second call's maximum to `100` produces `0.4`. A function centralizes the formula, but callers must supply the correct maximum. This function assumes a positive maximum and scores between zero and that maximum.

## Mutating Inputs and Reassigning Names

Passing a list makes the parameter refer to that list. Calling `append()` inside the function changes what the caller sees. Assigning a new list to the parameter name, however, does not reassign the caller's name.

```python
def add_score(scores):
    scores.append(91)

def replace_scores(scores):
    scores = [100]

original = [82, 75]
add_score(original)
print(original)
replace_scores(original)
print(original)
```

Both outputs are `[82, 75, 91]`. The first function mutates the shared list; the second only rebinds its local name. Callers need to know whether a function changes its input or returns a new result.

## Shared List Defaults

A mutable default such as `def collect(score, results=[]):` does not create an empty list on every call. Defaults are evaluated once when the function is defined, so earlier additions may remain in later calls. To create a new result for each call, default to `None` and create the list inside the function.

```python
def collect(score, results=None):
    if results is None:
        results = []
    results.append(score)
    return results

print(collect(82))
print(collect(75))
```

The outputs are `[82]` and `[75]`. These calls omit `results`, creating separate lists. Explicitly passing the same list instead keeps appending to that shared list.

## Checklist

- Read function definitions beginning with `def`.
- Distinguish parameters and arguments.
- Explain `print()` versus `return`.
- Extract repeated calculations into functions.
- Write a function for one sample and reuse it in a loop.
- Explain assigning functions to names and passing them as arguments.
- Distinguish function and method call syntax.
- Explain how a function name should communicate intent.
- Explain how functions turn repeated processing into named reusable units.

- Distinguish input mutation from parameter reassignment and use a `None` default when each call needs a new list.

## Sources and References


- Python Software Foundation, [More Control Flow Tools: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used as the official basis for `def`, parameters, `return`, and function-call examples.
- Python Software Foundation, [More Control Flow Tools: Default Argument Values](https://docs.python.org/3/tutorial/controlflow.html#default-argument-values){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used to confirm default-parameter examples and the caution about mutable defaults.
- Python Software Foundation, [Function definitions](https://docs.python.org/3/reference/compound_stmts.html#function-definitions){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm function-definition syntax, parameter lists, and function-object creation.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used as background for the explanation that functions can be treated as objects in Python.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used as the basis for distinguishing function-call and method-call forms at an introductory level.
