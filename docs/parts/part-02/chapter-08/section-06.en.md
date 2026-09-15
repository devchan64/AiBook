# P2-8.6 Supplementary Learning: A First Look at Classes and Objects

> Section ID: `P2-8.6`
> Version: `v2026.09.15`

`text.lower()` lowercases a string, while `scores.append(91)` adds a value to a list. Before the dot (`.`) is the target object; after it is the method name. Available operations depend on the object's type.

## Objects and Types

Python objects have identity, type, and value. Numbers, strings, lists, and dictionaries are objects too. The code prints `<class 'int'>`, `<class 'str'>`, `<class 'list'>`, and `<class 'dict'>`.

```python
score = 82
text = "AI"
scores = [82, 75, 91]
student = {"name": "Kim", "score": 82}

print(type(score))
print(type(text))
print(type(scores))
print(type(student))
```

Strings provide `strip()` and `lower()`. Applied separately to `" AI is Useful "`, they print `AI is Useful` and ` ai is useful `, the latter retaining surrounding spaces.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

Both methods return a processed string without changing `text`. In contrast, list `append()` changes the original list. Adding `91` to `[82, 75]` prints `[82, 75, 91]`.

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

`text.append(91)` requests a method strings do not provide, raising `AttributeError`.

## Classes and Instances

A class defines what data and behavior a kind of object can have. An individual object created from that class is an instance.

| Object example | Class | Example methods |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`, `.strip()` |
| `[1, 2, 3]` | `list` | `.append()`, `.extend()` |
| `{"a": 1}` | `dict` | `.get()`, `.items()` |

A custom `Sample` class can create objects with text and a label. This code prints `AI is useful` and `positive`.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

`Sample` is the class; `sample` names the resulting instance. `sample.text` and `sample.label` read that object's attributes.

`__init__()` runs when initializing a new instance. It stores the supplied `text` and `label` in `self.text` and `self.label`, making them part of the object's data.

## self and Individual Object State

`self` is the conventional parameter name for the instance receiving a method call. With `sample.method()`, the object is passed automatically, so callers do not supply `self` separately.

Two objects from the same class can hold different values. The code changes only the first object's label to `positive`, printing `positive` and `None`.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

first = Sample("good product", None)
second = Sample("new review", None)
first.label = "positive"

print(first.label)
print(second.label)
```

During the first initialization, `self` is the first object; during the second, it is the second object. An attribute read externally as `first.label` is `self.label` inside that object's method.

## Dictionary Keys and Object Attributes

Text and labels can also be represented by a dictionary. Reading the two keys prints `AI is useful` and `positive`.

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

Use `sample.text` for the earlier `Sample` object and `sample["text"]` for a dictionary. Dictionaries are objects too, but keys and attributes use different access mechanisms.

| Aspect | Dictionary | Custom Sample instance |
| --- | --- | --- |
| Access | `sample["text"]` | `sample.text` |
| Storage | Associate values with keys | Store values in attributes |
| Processing | Can be used with separate functions | Can define methods in the class |
| Example use | Settings or data loaded from JSON | Samples with data and dedicated behavior |

A class name communicates meaning, but does not automatically validate attribute types or values.

## State and Methods

State is an object's current data; behavior reads or changes it. `TextSample` stores text and a label, and `is_labeled()` checks whether the label is `None`. The outputs are `AI is useful` and `True`.

```python
class TextSample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def is_labeled(self):
        return self.label is not None

sample = TextSample("AI is useful", "positive")

print(sample.text)
print(sample.is_labeled())
```

Set `sample.label` to `None` and call `sample.is_labeled()` again to get `False`. This method only checks whether the label is not `None`. Even `""` yields `True`; it does not validate label content.

A function and dictionary can express the same check. Checking the dictionary label `"positive"` prints `True`.

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

`is_labeled(sample)` passes the sample to a function; `sample.is_labeled()` calls its method. Dictionaries support key-based data lookup, while classes can define state together with dedicated behavior.

## Retrieving a Method Versus Calling It

`sample.is_labeled` retrieves a method; `sample.is_labeled()` executes it and receives its return value. Run this after the earlier `TextSample` definition to print `False` and `True`.

```python
sample = TextSample("new review", None)
check = sample.is_labeled
print(check())
sample.label = "positive"
print(check())
```

`check` is bound to `sample`. Since the label changes after the first call, the second reads the current state and returns `True`. Omitting parentheses, as in `if sample.is_labeled:`, does not run the check. This method object itself is truthy, so that condition passes even when the label is `None`.

## Function Calls and Method Calls

A function cleaning `" AI "` can call string methods internally. The code prints `function: ai` and `method: AI`.

```python
def clean_text(text):
    return text.strip().lower()

text = " AI "

print("function:", clean_text(text))
print("method:", text.strip())
```

`clean_text(text)` trims whitespace and lowercases. `text.strip()` removes only whitespace, leaving uppercase letters.

| Expression | Target and operation |
| --- | --- |
| `clean_text(text)` | Pass a string to a function |
| `text.strip()` | Call a string object's whitespace-removal method |
| `sample.is_labeled()` | Call a sample object's label-checking method |
| `model.predict(test_data)` | Pass data to a model object's prediction method |

## Case: Model State Before and After Training

Model objects store settings and learned values; methods change or use that state. `SimplePassModel` is a teaching class that stores the lowest passing score as a threshold. It does not implement a real machine-learning library's training algorithm.

Each pair in `[(62, False), (75, True), (83, True)]` contains a score and pass status. `fit()` stores `75`, the minimum passing score; `predict()` compares `[70, 78]` with that threshold.

```python
class SimplePassModel:
    def __init__(self):
        self.threshold = None

    def fit(self, train_data):
        # fit() reads training data and stores state in the object.
        passed_scores = [score for score, passed in train_data if passed]
        if not passed_scores:
            raise ValueError("at least one passing score is required")
        self.threshold = min(passed_scores)

    def predict(self, test_data):
        # predict() uses the state saved by fit().
        if self.threshold is None:
            raise ValueError("call fit() first")
        return [score >= self.threshold for score in test_data]


train_data = [(62, False), (75, True), (83, True)]
test_data = [70, 78]

model = SimplePassModel()

print("before fit:", model.threshold)
model.fit(train_data)
print("after fit:", model.threshold)
predictions = model.predict(test_data)
print("predictions:", predictions)
```

The output is:

```text
before fit: None
after fit: 75
predictions: [False, True]
```

`model.threshold` is `None` before training and `75` after `fit()`. Keep using the same object because `predict()` reads its stored threshold. Calling `predict()` on a new object raises the code's `ValueError` because no threshold has been stored.

Changing training pair `(75, True)` to `(68, True)` sets the threshold to `68` and predictions to `[True, True]`. Test scores stay fixed while changed model state changes the decisions.

The example requires at least one passing score. Otherwise `fit()` raises an explicit `ValueError`; inspect the input rather than continuing to predict after that exception. Failing scores are not used to calculate the threshold, so this rule cannot be directly applied to complex real classification problems.

## Checklist

- Explain objects as the actual entities holding Python values.
- Explain a class as a definition used to create objects.
- Explain a method as a function-like operation called through an object.
- Distinguish dictionaries and class-based objects at an introductory level.
- Explain bundling state and behavior through an example.
- Distinguish the call targets in `function(value)` and `value.method()`.
- Explain `self` as the name for the instance itself.
- Explain when functions and dictionaries suffice without a class.
- Read `model.fit()` and `model.predict()` as object method calls.

- Distinguish retrieving a method from calling it and explain why a condition without parentheses does not run the check.

## Sources and References


- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used as the official basis for the introductory explanation of class objects, instance objects, attribute references, and method objects.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used as background for the explanation that objects have identity, type, and value, and that behavior differs by type.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used to confirm the explanation of reading `value.method()` calls as function-like behavior attached to an object.
