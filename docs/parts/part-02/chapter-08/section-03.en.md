# P2-8.3 Dictionaries: Finding Values by Key

> Section ID: `P2-8.3`
> Version: `v2026.09.15`

## Keys and Values

A mapping connects a lookup criterion to a value. The criterion is called a key, and the associated object is its value.

Python commonly represents mappings with dictionaries.

Associate the name `"Kim"`, score `82.5`, and pass status `True` with the keys `"name"`, `"score"`, and `"passed"`. Looking up the name and score prints `Kim` and `82.5`.

```python
student = {
    "name": "Kim",
    "score": 82.5,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

Lists retrieve values by position; Python dictionaries retrieve them by key.

| Structure | Lookup criterion | Example |
| --- | --- | --- |
| List | Index | `scores[0]` |
| Dictionary | Key | `student["score"]` |

Dictionaries are common in AI exercises.

- Configuration: `{"learning_rate": 0.01, "epochs": 10}`
- A data row: `{"text": "hello", "label": "positive"}`
- Part of an API response: `{"model": "example", "tokens": 120}`
- Evaluation results: `{"accuracy": 0.91, "loss": 0.32}`

Use dictionaries when a value's name matters more than its position.

| Concept | General meaning | In Python |
| --- | --- | --- |
| Mapping | Connects a criterion to a value | Represented with a dictionary |
| Key | Criterion for lookup | A hashable value, such as a string or number |
| Value | Object associated with a key | May be a number, string, list, dictionary, and more |

## Label Mappings and Key Checks

Label `0` maps to `"negative"` and `1` to `"positive"`. Looking up prediction `1` prints `positive`.

```python
label_name = {
    0: "negative",
    1: "positive",
}

prediction = 1
print(label_name[prediction])
```

When `prediction` is `1`, the dictionary returns `"positive"` associated with that key. The numeric key `1` is an identifier, not the second position.

Configuration names, IDs, and column names can also be keys.

| Situation | Dictionary representation |
| --- | --- |
| Turn label IDs into readable names | `{0: "negative", 1: "positive"}` |
| Look up configuration by name | `{"batch_size": 32, "learning_rate": 0.001}` |
| Look up a user by ID | `{"u001": {"name": "Kim"}}` |
| Describe columns by name | `{"score": "exam score", "label": "ground-truth label"}` |

`key in dictionary` tests whether a key exists.

Use `in` to check for `"learning_rate"` and print its value if present. This configuration prints `0.001`; changing `name` to the missing key `"dropout"` prints nothing.

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

name = "learning_rate"

if name in config:
    print(config[name])
```

## Hashable Keys

Python documents dictionaries as mapping types. A mapping associates keys with values; hashing is used to implement lookup. Dictionary keys must be hashable.

Strings and numbers can be keys. A tuple can be a key if all its elements are hashable. Lists are not hashable and cannot be keys.

Looking up `"Kim"` prints the associated score `82`.

```python
scores_by_name = {
    "Kim": 82,
    "Lee": 91,
}

print(scores_by_name["Kim"])
```

Dictionaries preserve key insertion order, without automatically sorting by size or spelling. Here `"Lee"` was inserted first, so the key list is `['Lee', 'Kim']`.

```python
scores_by_name = {"Lee": 91, "Kim": 82}
print(list(scores_by_name))
```

`list(dictionary)` creates a list of keys. This differs from retrieving a value with `scores_by_name["Kim"]`.

## Replacing a Value at the Same Key

Storing a new value at an existing key replaces the old value.

Store `82` and then `91` under `"Kim"` in an empty dictionary. It prints `{'Kim': 91}`: the original score is overwritten.

```python
scores = {}

scores["Kim"] = 82
scores["Kim"] = 91

print(scores)
```

This does not keep both scores under `"Kim"`; only `91` remains. To collect multiple values at one key, use a list or another collection as the value.

A list can store two scores for one person. Looking up `"Kim"` now returns `[82, 91]`.

```python
scores = {
    "Kim": [82, 91],
}

print(scores["Kim"])
```

## Looking Up Settings, Labels, and IDs

Dictionaries suit data with a clear lookup criterion.

### Configuration Values

Looking up the learning-rate key `"learning_rate"` prints `0.001`.

```python
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

print(config["learning_rate"])
```

`config[1]` does not request the second setting. It requests integer key `1`, which is absent here, so it raises `KeyError`.

### Turning Label IDs into Names

Mapping numeric label `2` to a sentiment name prints `neutral`.

```python
label_map = {
    0: "negative",
    1: "positive",
    2: "neutral",
}

predicted_label = 2

print(label_map[predicted_label])
```

A dictionary can turn a model's numeric labels into names people can read.

### Finding Data by Sample ID

The value at `"s001"` is another dictionary containing sample information. Looking up its `"text"` prints `good product`.

```python
samples_by_id = {
    "s001": {"text": "good product", "label": "positive"},
    "s002": {"text": "bad service", "label": "negative"},
}

sample_id = "s001"

print(samples_by_id[sample_id]["text"])
```

As data grows, its ID may matter more than its position. A dictionary then acts as a map from ID to sample.

### Describing Columns by Name

Associating column names with descriptions lets a lookup of `"score"` return `model score`.

```python
column_description = {
    "text": "input sentence",
    "label": "ground-truth label",
    "score": "model score",
}

print(column_description["score"])
```

Recording column meanings when reading a dataset helps later preprocessing and documentation.

## Dictionaries and Objects

A dictionary is one kind of Python object. Numbers, strings, lists, and functions are also objects; dictionaries specifically map keys to values. Their braces resemble JSON objects, but not every Python object is a dictionary.

Key access differs from attribute access. Read the student's name with `student["name"]`. Using `student.name` on that dictionary raises `AttributeError` instead of returning the name.

## Missing Keys and Defaults

Directly retrieving a missing dictionary key can raise an error.

`student` contains only `"name"` and `"score"`. Looking up the absent `"label"` with brackets raises `KeyError`.

```python
student = {"name": "Kim", "score": 82.5}

print(student["label"])
```

`KeyError` means the requested key is missing.

Use `get()` when a key may be missing.

For a missing key, `get()` returns the specified default. These calls print `None` when no default is supplied and `unknown` when it is specified.

```python
student = {"name": "Kim", "score": 82.5}

print(student.get("label"))
print(student.get("label", "unknown"))
```

Returning a default does not insert the key. If a required field is missing, inspect the error and fix the input; an optional field can use a default through `get()`.

## A Missing Key Versus a Missing Value

An absent key differs from a present key whose value is `None`. The default in `get()` is used only when the key is absent.

```python
sample = {"text": "hello", "label": None}
print(sample.get("label", "unknown"))
print(sample.get("source", "unknown"))
print("label" in sample)
print("hello" in sample)
```

The outputs are `None`, `unknown`, `True`, and `False`. Since `"label"` exists, its value is not replaced by the default. `in` tests keys, not values, so the last result is `False` even though `"hello"` is a value.

With `sample["label"] = ""`, `get("label", "unknown")` still returns the empty string. Required-label validation must separately check that the key exists and that its value is an allowed label.

## Case: Nonconsecutive Label IDs

Suppose sentiment labels use IDs `10`, `20`, and `90`. Using these as list indices requires many unused positions; a dictionary only needs the relevant IDs and names. The code prints `neutral` for prediction `90` and the default `unknown` for absent ID `30`.

```python
label_map = {10: "negative", 20: "positive", 90: "neutral"}
prediction = 90

print(label_map[prediction])
print(label_map.get(30, "unknown"))
```

Changing `prediction` to `20` makes the first output `positive`. Changing it to `30` raises `KeyError` at the first lookup, so the next print is not reached. Define both the label mapping and how missing IDs are handled.

## Checklist

- Explain a dictionary as a collection of keys and values.
- Explain a dictionary as a mapping.
- Distinguish its mapping interface from its hash-based implementation.
- Explain list lookup by position versus dictionary lookup by key.
- Explain why `get()` helps when a key may be absent.
- Read label-map, configuration, sample-ID, and column-description examples.
- Choose a lookup method according to whether keys may be missing.

- Distinguish a missing key from a `None` value and explain when the default in `get()` applies.

## Sources and References


- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm dictionary creation, key-based value access, and iteration examples using `items()`.
- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-09-15. Used to confirm that `dict` is a mutable mapping type and a structure for finding values through keys.
- Python Software Foundation, [Glossary: dictionary, hashable](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used to confirm the glossary definitions of dictionary and hashable.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3 documentation, checked on 2026-07-20. Used as background for dictionary key constraints by confirming object identity/type/value and hashability.
