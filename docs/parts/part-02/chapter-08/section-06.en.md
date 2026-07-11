# P2-8.6 Supplemental Learning: First Meeting Classes and Objects

> Section ID: `P2-8.6`
> Version: `v2026.07.09`

In P2-8.5, we looked at functions as small units of reuse. Functions receive input, process it, and return a result. But when reading Python code, we often meet expressions that look similar to function calls but are slightly different.

Here we provide a basic supplemental explanation for reading `class`, `object`, and `method`. This supplemental learning organizes the standard for reading call shapes such as `value.method()` and `model.fit()`. The representative explanations of `value`, `type`, and `dictionary` remain in P2-8.1, P2-8.3, and the [concept glossary](../../../reference/concept-glossary.md), and here we read class and object on top of that.

Problem situation: We want to see, through the smallest example, how a dot-based call differs from an ordinary function call.
Input: The string `text = " AI is Useful "`.
Expected output: A string with spaces removed and a string converted to lowercase.
Concept to check: A form like `value.method()` is the shape of calling an action provided by a value or object.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

`strip()` and `lower()` are called with parentheses like functions, but they have `text.` in front of them. To understand this kind of expression, we need a very light introduction to object, method, and class.

This section does not teach the full syntax of classes. The goal is to give the minimum standard so that later, when reading library code, we do not stop at expressions such as `value.method()`, `model.fit()`, or `dataset.map()`.

Here we organize questions such as `why do strings use .lower(), while lists use .append()?` under the standard that `an object provides actions in method form according to its type`.

Because this is supplemental learning, the explanation is slightly more detailed. But the goal is not to design classes freely. The goal is to read the shape of Python library code that we will meet later.

| Term | Meaning to fix first in this section |
| --- | --- |
| object | a thing we handle that has both values and the actions connected to those values |
| class | the definition or template for making such objects |
| method | a function-like action called while attached to an object |
| attribute | a value or name tag that an object has |
| `value.method()` | the shape of calling an action provided by a specific value or object |

## Scope of This Supplemental Learning

Here we cover only the entry-level intuition of Python objects and classes. The basic explanations of value, type, and function reconnect through P2-8.1 and P2-8.5, while effects created by object sharing, such as reference and copy, are recovered separately in P2-8.7.

The first question to solve here is this: `by what standard should we read an expression that looks like a function call but has a dot in front of it?`

So this supplement answers the following questions.

- What is an object?
- What is a class?
- How is a method different from a function?
- How are value, type, and class connected in Python?
- Why do we see expressions like `model.fit()` so often in library code?

It does not cover the detailed rules of inheritance, encapsulation, polymorphism, magic methods, class variables, or instance variables.

The flow after this section is also simple.

- In `P2-8.7`, we look again at effects created by object sharing and reference.
- Later, when reading AI libraries, the same standard repeats in expressions such as `model.fit()`, `dataset.map()`, and `tokenizer.encode()`.

## Goals of This Supplemental Learning

- You can explain an object as a thing that has both values and actions.
- You can explain a class as the definition for creating objects.
- You can read a method as a function-like form that is called while attached to an object.
- You can explain at an entry level the difference between `function(value)` and `value.method()`.
- You can read expressions such as `model.fit()` and `model.predict()` in AI libraries from the perspective of classes and methods.

## The First Standard to Hold

The first standard to hold in this supplement is this: `a call with a dot is an action provided by an object`.

| Expression | First way to read it |
| --- | --- |
| `text.lower()` | an action provided by a string object |
| `scores.append(91)` | an action provided by a list object |
| `model.fit(X, y)` | a form in which a model object provides a training action |
| `sample.text` | a value or attribute owned by an object |

So the core of this section is not learning to design classes freely, but building a standard that does not stop at `value.method()` and `object.attribute`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| An object is one thing we handle that has both value and action | It becomes the starting point for reading call forms such as `value.method()`. | Understand it as a thing that has both values and methods together. |
| A class is the definition for making such objects | It explains why attributes and methods appear as one bundle. | Be able to explain it as something like a blueprint. |
| These expressions appear often in AI libraries because it is convenient to handle a model or dataset as one bundle | It helps us read `model.fit()` structurally instead of reading only the syntax. | Understand that models, datasets, and settings are handled like objects. |

## In Python, Many Things Are Objects

The Python official documentation explains an object as something that has identity, type, and value. Here it is enough to understand it like this:

An object is the actual thing Python is handling as a value.

Numbers, strings, lists, and dictionaries can all be read as objects.

Problem situation: We want to confirm through type output that different kinds of values are all handled as Python objects.
Input: Integer, string, list, and dictionary values.
Expected output: The type of each value is printed in order.
Concept to check: In Python, many kinds of values are all objects, and type reveals their character.

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

What matters here is `type()`. Each value has a type, and in Python that type affects what actions are available.

For example, strings provide methods suited to strings.

Problem situation: We want to see how methods provided by a string object are called.
Input: The string `text` containing spaces and uppercase letters.
Expected output: The results of `strip()` and `lower()`.
Concept to check: An object provides actions in method form according to its type.

```python
text = " AI is Useful "

print(text.strip())
print(text.lower())
```

Lists provide methods suited to lists.

Problem situation: We want to confirm that a list object also has methods suited to its own type.
Input: The list `scores = [82, 75]` and the value `91` to add.
Expected output: The list after the value is added.
Concept to check: If the type differs, the methods that can be used also differ.

```python
scores = [82, 75]

scores.append(91)

print(scores)
```

Strings have `strip()`, and lists have `append()`. Because the types differ, the available actions also differ.

## A Class Is the Definition for Making Objects

A class is the definition used to make objects. More simply, it is a template that decides what kind of data and what kind of actions a certain object should have.

Even Python’s built-in types can be read this way.

| Value | Type or class | Common actions |
| --- | --- | --- |
| `"AI"` | `str` | `.lower()`, `.strip()` |
| `[1, 2, 3]` | `list` | `.append()`, `.extend()` |
| `{"a": 1}` | `dict` | `.get()`, `.items()` |

The reader can also make a class directly.

Problem situation: We want to see the smallest example of defining a class and making an object from it.
Input: The values `"AI is useful"` and `"positive"` for text and label.
Expected output: The object’s `text` and `label` attributes are printed.
Concept to check: A class is the definition for creating objects, and an object can hold its own data.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

This code defines a class called `Sample` and creates an object called `sample`. `sample.text` and `sample.label` are values held by the object.

There is no need here to memorize the detailed rules of `__init__`. The key point is only that a class is the definition for creating objects, and an object can hold its own data.

## Why Dictionaries and Classes Can Feel Different

In P2-8.3, we said that a dictionary is a structure that looks up values by key. In fact, one small piece of data can also be represented by a dictionary.

Problem situation: We want to see an example where small data with text and label is represented as a dictionary.
Input: The dictionary `sample` with the keys `text` and `label`.
Expected output: The values of `sample["text"]` and `sample["label"]`.
Concept to check: A dictionary is the most direct data representation that finds values by key.

```python
sample = {
    "text": "AI is useful",
    "label": "positive",
}

print(sample["text"])
print(sample["label"])
```

If we represent the same data through a class, it looks like this.

Problem situation: We want to compare how the same data changes in shape when represented as a class-based object.
Input: The class `Sample` and the construction arguments `"AI is useful"`, `"positive"`.
Expected output: The values of `sample.text` and `sample.label`.
Concept to check: A class-based object lets us read data through attribute access rather than key lookup.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

sample = Sample("AI is useful", "positive")

print(sample.text)
print(sample.label)
```

Both pieces of code hold text and label. But the way we read them feels different.

| Perspective | dictionary | object made from a class |
| --- | --- | --- |
| central thought | find values by key | make a certain kind of thing |
| access form | `sample["text"]` | `sample.text` |
| explicitness of structure | the key name is confirmed during execution | the class name reveals the meaning of the target |
| adding behavior | used together with separate functions | methods can be placed inside the object |
| suitable situation | simple data, JSON, configuration values | targets that handle state and behavior together |

At the beginning, dictionaries are easier. Real data files and API responses also often read like dictionaries. That is why this book introduced dictionaries first.

The moment classes start to matter is when we want not only data, but also the actions to be bundled together with that data.

## State and Behavior Are Bundled Together

When explaining objects, the words `state` and `behavior` appear often.

State means the values an object currently has.

Behavior means the things that object can do.

The following example shows a text sample that has its own state and also has an action that checks that state.

Problem situation: We want to confirm through a class example that an object has both values and actions.
Input: A `TextSample` object with text and label.
Expected output: The object’s `text` value and the result of `is_labeled()`.
Concept to check: State is the values an object has, and behavior is the method the object provides.

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

Here, `sample.text` and `sample.label` are the state of the object. `sample.is_labeled()` is its behavior.

The same work can also be done with functions.

Problem situation: We want to see that the same label-checking work can also be expressed through the combination of a function and a dictionary.
Input: A sample dictionary with the key `label`.
Expected output: The result `True` from `is_labeled(sample)`.
Concept to check: Even without a class, a similar handling structure can be made through a function and a dictionary.

```python
def is_labeled(sample):
    return sample["label"] is not None

sample = {"text": "AI is useful", "label": "positive"}

print(is_labeled(sample))
```

We cannot say that one is always better than the other. What matters is the purpose of the structure.

| Purpose | Simpler approach |
| --- | --- |
| read data such as JSON as it is | dictionary |
| quickly find many values by key | dictionary |
| bundle data and behavior as one target | class |
| use a library that provides stateful targets | class-based object |

In the early stage of AI practice, dictionaries and functions are often enough. But once we start using libraries, targets such as models, datasets, tokenizers, and optimizers are often provided as objects. Those targets have internal state, and methods run on the basis of that state.

## A Method Looks Like a Function Called While Attached to an Object

We usually call a function like this.

Problem situation: We want to look at an independent function call first and then compare it with a method call.
Input: The string `" AI "`.
Expected output: The cleaned string.
Concept to check: `function(value)` is the form of putting a value into a function and processing it.

```python
def clean_text(text):
    return text.strip().lower()

print(clean_text(" AI "))
```

A method is called while attached to an object.

Problem situation: We want to see how the same string cleaning looks in method-call form.
Input: The string `text = " AI "`.
Expected output: The result of `text.strip()`.
Concept to check: A method is called with the object in front of the dot as the center.

```python
text = " AI "

print(text.strip())
```

Both expressions run an action. But the center of the call is different.

| Expression | Center of the call | How to read it |
| --- | --- | --- |
| `clean_text(text)` | the function name | put `text` into the function and process it |
| `text.strip()` | the object `text` | call the `strip()` action provided by the `text` object |

We can also put methods into a class we defined ourselves.

Problem situation: We want to confirm that an object we defined ourselves can also have its own method.
Input: A `Sample` object and the method `has_label()`.
Expected output: The result `True` from `sample.has_label()`.
Concept to check: A method can also be placed inside a user-defined class.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label

    def has_label(self):
        return self.label is not None

sample = Sample("AI is useful", "positive")

print(sample.has_label())
```

`sample.has_label()` is a method called while attached to the object `sample`. It looks like a function, but the target object appears in front.

When reading methods, the following questions help.

1. What is the target in front of the dot (`.`)?
2. What state does that target have?
3. Does the method after the dot read that state or change it?
4. What additional values are passed inside the parentheses?

For example, if we see `model.predict(test_data)`, we can read it like this.

| Question | Answer |
| --- | --- |
| target before the dot | `model` |
| meaning of the target | likely a trained model object |
| method after the dot | `predict()` |
| value being passed | `test_data` |
| full interpretation | the model object performs a prediction action on the test data |

## `self` Is the Name That Refers to the Object Itself

In Python class examples, we often see the name `self`.

Problem situation: We want the smallest example of what place `self` takes inside a class.
Input: The `__init__` method of the `Sample` class and the input `text`.
Expected output: A class definition that stores `self.text` inside the object.
Concept to check: `self` is the conventional name that refers to the object itself inside a method.

```python
class Sample:
    def __init__(self, text):
        self.text = text
```

Here, it is enough to understand `self` as “the object that is currently being created or used.” `self.text = text` means “store the value `text` inside this object.”

Someone who learned another language first can read it as playing a role similar to `this`. But in Python, what stands out is that `self` is written explicitly in the method definition.

For now, remember only the following.

- `self` is a conventional name.
- It is used when reading or changing the values of the object itself inside a method.
- When we call something like `sample.has_label()`, we do not pass `self` directly by hand.

If `self` feels unfamiliar, compare the following two lines.

Problem situation: We want to connect attribute access seen from outside a class with the inside-class use of `self`.
Input: The object `sample` created as `Sample("AI is useful", "positive")`.
Expected output: The value of `sample.label` is printed.
Concept to check: Outside the class we read `sample.label`, while inside the class the same place is read as `self.label`.

```python
sample = Sample("AI is useful", "positive")

print(sample.label)
```

`sample.label` is the expression that reads the `label` value stored inside the object `sample`. Inside the class, we call that object by the name `self`.

Problem situation: We want to recheck the class definition that stores attributes using forms such as `self.label`.
Input: The `__init__` method of the `Sample` class.
Expected output: A class definition that stores `self.text` and `self.label`.
Concept to check: Inside the class, the object’s own attributes are handled through `self`.

```python
class Sample:
    def __init__(self, text, label):
        self.text = text
        self.label = label
```

So, from outside we read `sample.label`, and from inside the class we read `self.label`. For now, it is enough to hold this correspondence exactly.

## Is a Class Always Necessary?

No. Learning Python does not mean every piece of code must be turned into a class.

The following standard is more practical here.

| Situation | Approach to consider first |
| --- | --- |
| calculate one value | function |
| handle several values in order | list |
| find a value by name | dictionary |
| repeat the same handling | loop and function |
| make a target that has both state and behavior | class |

Classes are powerful, but if used too early, they can make the structure heavy. On the other hand, when reading library code, we often cannot avoid classes and objects. Here we focus less on `making everything into a class` and more on `being able to read code that was made through classes`.

## Why Do Classes and Methods Appear So Often in AI Libraries?

In AI practice, we often see code like the following.

Problem situation: We want to see the method-call form that appears often in AI libraries in the simplest way.
Input: `model`, `train_data`, `test_data`.
Expected output: Example calls such as `model.fit(...)` and `model.predict(...)`.
Concept to check: Because library objects have both state and behavior, method-call form appears often.

```python
model.fit(train_data)
predictions = model.predict(test_data)
```

This code differs by library, but the reading method is similar.

| Expression | Entry-level interpretation |
| --- | --- |
| `model` | a model object |
| `.fit()` | a method that performs training |
| `.predict()` | a method that performs prediction |
| `train_data`, `test_data` | the data passed into the method |

Why is this style used? Because a model is not just one simple function. It can hold many kinds of state. Learned parameters, settings, internal structure, and preprocessing information can all live together inside the object. So a library makes the model an object and attaches methods such as `fit()`, `predict()`, and `save()` to that object.

This perspective matters later when reading machine learning libraries and deep learning frameworks.

- A function separates one kind of processing by name.
- An object can bundle state and behavior together.
- A class is the definition for making such objects.
- A method is an action called while attached to an object.

Here we read it like this.

Problem situation: We want to fix a one-line example of a `fit()` method call one more time.
Input: `model`, `train_data`.
Expected output: The example call `model.fit(train_data)`.
Concept to check: A method call can be an action where an object changes or uses its own state.

```python
model.fit(train_data)
```

There is an object called `model`, and that object runs the method `fit()`. Here `fit()` may do more than a simple calculation. It can change the state inside the model object. For example, learned parameters may be stored inside the object.

Problem situation: We want a one-line example showing that a prediction method uses the learned state of an object.
Input: `model`, `test_data`.
Expected output: The example call `predictions = model.predict(test_data)`.
Concept to check: A method can create a result by using the state of an object.

```python
predictions = model.predict(test_data)
```

`predict()` makes prediction results by using the state of a model object that has already been trained. So instead of looking only at one function, we also need to think about what state the object is holding.

This perspective matters later in machine learning.

- A model before training and a model after training can look like the same object, but their internal state can differ.
- `fit()` can be a method that changes state.
- `predict()` can be a method that uses state to make a result.
- `save()` can be a method that stores state into a file.

## Perspective to Keep from This Section

- In Python, many values are handled as objects.
- A class is the definition used to make such objects.
- A method is an action called while attached to an object.
- `function(value)` and `value.method()` may look similar, but the reading direction is different.
- Later, when `model.fit()`, `model.predict()`, or `dataset.map()` appears, first ask `what state and action does this object hold together?`

It is better not to start classes through difficult syntax. First distinguish the call shapes that appear in Python code.

`function(value)` is the form of putting a value into a function.

`value.method()` is the form of calling an action provided by a value or object.

When we meet expressions like `model.fit()` in AI libraries, we can read them as `the model object calls its training method`. Even this alone helps us not stop when first reading many pieces of code.

This supplemental learning can reconnect safely with the main flow if we recover only the following standard.

| What to recover here | Main-text question to return to | Where to keep reading next |
| --- | --- | --- |
| the difference in calling center between `function(value)` and `value.method()` | why different actions are used depending on value and type | values, variables, and types in P2-8.1; lists and dictionaries in P2-8.2 to P2-8.3 |
| the fact that expressions such as `model.fit()` are object-method calls | how to read the target before the dot (`.`) in library code | functions in P2-8.5; later library examples in the main text of Part 3 |

In other words, if we can read what the target before the dot is, and if we understand that a method is an action attached to an object, then it is safer not to stay too long here and instead return to the main text.

## Looking Through a Case

### Case 1. Why Doesn’t `model.fit()` Look Like an Ordinary Function?

Suppose a learner sees `model.fit(train_data)` and `model.predict(test_data)` for the first time in a machine learning example. A person may expect a function form like `fit(model, train_data)`, and then stop when they see the dot-based call form.

What matters here is not memorizing syntax, but reading the center of the call. `model` is likely to be an object that holds some state, `fit()` can be an action that changes that object’s state, and `predict()` can be an action that uses that state to make a result.

So when first meeting classes and objects, we need to hold the standard that `an object has both values and actions`, and that `a method is called while attached to that object`. The string call `text.strip()` and the model call `model.fit()` differ greatly in complexity, but they share the same call shape.

The confirmable result is that if the target before the call changes, the action also changes. `text.lower()` handles a string, `scores.append(91)` changes a list, and `model.predict(test_data)` uses model state. If we can read what the target before the dot is, code interpretation becomes much easier.

## Short Check

- Can you explain an object as `a target that has both values and actions`?
- Can you state the difference between a class and an object?
- Can you distinguish `function(value)` from `value.method()`?
- Can you explain why expressions such as `model.fit()` need the perspective of class and method?
- Can you explain an object as the actual target Python handles as a value?
- Can you explain a class as the definition for creating objects?
- Can you explain a method as a function-like form called while attached to an object?
- Can you explain at an entry level the difference between a dictionary and a class-based object?
- Can you explain through an example what it means to bundle state and behavior together?
- Can you explain the difference in calling center between `function(value)` and `value.method()`?
- Can you explain `self` as the name that refers to the object itself?
- Can you explain that classes are not always necessary, and that in some cases functions and dictionaries are enough?
- Can you read AI-library expressions such as `model.fit()` and `model.predict()` from the perspective of object and method?

## When Should You Recall This Perspective First

- Recall it when you need to reread why dot-based calls such as `model.fit()` or `text.lower()` look different from ordinary functions.
- Recall it when you need to place strings, lists, and model objects into one frame through the perspective that an object has both value and action.
- Recall it when you need to judge again whether a dictionary or a class-based object feels more natural according to how tightly data and behavior need to be bundled together.

## Sources and References

- Python Software Foundation, [Classes](https://docs.python.org/3/tutorial/classes.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-06-25.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-06-25.
- Python Software Foundation, [Classes: Method Objects](https://docs.python.org/3/tutorial/classes.html#method-objects){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked 2026-06-25.
