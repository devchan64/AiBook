# P2-8.3 Dictionaries: Structures That Find Values by Key

> Section ID: `P2-8.3`
> Version: `v2026.07.26`

In P2-8.2, we looked at lists, which are ordered groups of values. But not all data is read only through order.

In situations where you look up a setting value by setting name, a label name by label number, or user information by user ID, the name tag matters more than the position. In Python, this kind of structure is handled with a dictionary.

Here, we explain the basic distinction between a `dictionary` and a `key`. The representative explanation of `list` and order-based access is placed in P2-8.2, and the representative explanation of `value` and `type` is placed in P2-8.1 and in the [dictionary glossary entry](/AiBook/en/reference/concept-glossary-alpha/d.en/#dictionary). Here, we focus on `by which criterion should a value be found?`

If the list in the previous section was read around `which numbered value is it?`, here the center becomes `by which name or identifier is it found?` If you first establish this difference, then even later, when iterating over lists and dictionaries in the same loop, it becomes easier to distinguish `by what criterion is something being taken out?`

| What to establish in this section | Question that follows immediately | Where it is used again later |
| --- | --- | --- |
| The point that a dictionary is a structure that finds a value by key | This leads to how lists and dictionaries are traversed by iteration in P2-8.4. | It repeats later when reading configuration values, JSON responses, metadata, and evaluation results. |
| The point that the difference between a list and a dictionary is the difference between position and key | This leads to the criterion for judging which structure is more natural for which data. | It is reused later in DataFrame columns, label maps, and API response interpretation. |
| The point that `dict[key]` and `get()` differ in failure handling | This leads to how to handle inputs where a key may be absent. | It matters later in preprocessing, prediction-result parsing, and checking external responses. |

| Term | Meaning to establish first in this section |
| --- | --- |
| dictionary | A mapping structure where keys and values are connected. |
| key | A criterion name or identifier used to find a value. |
| value | The actual data connected to a key. |
| mapping | A structure that connects some criterion to some target. |
| `get()` | A way of access that lets a situation where a key may be absent be read a little more safely. |

## Core Criteria: Dictionaries: Structures That Find Values by Key

- You can explain a dictionary as a group of keys and values.
- You can explain a dictionary as a general-purpose mapping structure.
- You can explain the difference between a list and a dictionary as the difference between index and key.
- You can explain the difference between `dict[key]` and `dict.get(key)`.
- You can read examples of configuration values, label maps, sample ID lookup, and column descriptions.

## Three Criteria

Here, rather than syntax, we first look at `by what criterion will the value be found?` The following three criteria become the basis for reading later explanations of iteration and missing-key handling.

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| A dictionary is a structure that finds values by key | It lets you grasp the difference from a list most quickly | Understand it as a structure that finds by a name tag or identifier rather than by position |
| Key and value are the criterion to search by and the connected content | It lets configuration values, label maps, and ID lookups all be read as the same structure | You should be able to explain it as a structure where `"score"` finds a score and `0` finds a label name |
| It is safer to understand a dictionary first as a mapping | It prevents you from getting trapped too quickly in the implementation term hash map | At the code-reading stage, read it as a structure connecting keys to values |

## A Dictionary Is a Structure That Finds Values by Criterion

In general, a mapping is a structure that connects some criterion to a value. That criterion can be called a key, and the target connected to the key can be called a value.

In Python, this kind of mapping structure is often expressed with a dictionary.

Problem situation: I first want to see the simplest dictionary example where a value is found by a name tag.
Input: the dictionary `student`, which has the keys `name`, `score`, and `passed`.
Expected output: the values of `student["name"]` and `student["score"]` are printed.
Concept to check: a dictionary is a mapping structure that finds a value by key rather than by position.

```python
# This example checks how a dictionary finds and connects values by key.
student = {
    "name": "Kim",
    "score": 82.5,
    "passed": True,
}

print(student["name"])
print(student["score"])
```

If a list finds a value by position, a Python dictionary finds a value by key.

| Structure | Criterion for finding the value | Example |
| --- | --- | --- |
| list | position | `scores[0]` |
| dictionary | key | `student["score"]` |

Dictionaries appear often in AI practice.

- group of configuration values: `{"learning_rate": 0.01, "epochs": 10}`
- one row of data: `{"text": "hello", "label": "positive"}`
- part of an API response: `{"model": "example", "tokens": 120}`
- model evaluation result: `{"accuracy": 0.91, "loss": 0.32}`

A dictionary is used when `which named value is it?` matters more than `which numbered value is it in order?`

| Perspective | General explanation | In Python |
| --- | --- | --- |
| mapping | A structure that connects some criterion to a value | Uses a dictionary |
| key | The criterion for finding a value | Can be a hashable value such as a string or a number |
| value | The target connected to the key | Can be many kinds of values such as numbers, strings, lists, or dictionaries |

## A Dictionary Is Often Used as a General-Purpose Map Structure

A dictionary is not simply syntax that gathers several values in one place. The official Python documentation describes a dictionary as a mapping type. A mapping is a structure that connects some key to some value. This explanation continues directly beyond Python when reading configuration files, JSON responses, label maps, and metadata.

In this section, understand a dictionary by the following criterion.

A dictionary is a general-purpose map for finding the connected value when given a key.

Problem situation: I want to see the smallest correspondence table that changes a numeric label into a human-readable name.
Input: the dictionary `label_name`, which connects `0` and `1` to string labels, and the prediction value `1`.
Expected output: `"positive"`, which corresponds to prediction value `1`, is printed.
Concept to check: if given a criterion key, a dictionary can immediately take out the connected value.

```python
# This example checks how a dictionary finds and connects values by key.
label_name = {
    0: "negative",
    1: "positive",
}

prediction = 1
print(label_name[prediction])
```

In the example above, if `prediction` is `1`, the dictionary finds `"positive"` connected to the key `1`. Rather than a human having to think `which numbered slot should I search through?` like with a list, the value is taken out by key.

This feeling appears often in practical work and AI practice.

| Situation | How to see it as a dictionary |
| --- | --- |
| Change a label number into a human-readable name | `{0: "negative", 1: "positive"}` |
| Find a setting value by setting name | `{"batch_size": 32, "learning_rate": 0.001}` |
| Find user information by user ID | `{"u001": {"name": "Kim"}}` |
| Find the meaning of data by column name | `{"score": "exam score", "label": "correct label"}` |

The reason a dictionary feels like a general-purpose map becomes visible in situations like these. If the key exists, the value can be found immediately; if the key does not exist, that fact can be confirmed too.

Problem situation: I want to check the basic pattern of taking out a value only when a setting name exists in the dictionary.
Input: the configuration dictionary `config` and the key `learning_rate` to find.
Expected output: if the key exists, the corresponding setting value is printed.
Concept to check: a dictionary can safely take out a value after checking whether the key exists.

```python
# This example checks how a dictionary finds and connects values by key.
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

name = "learning_rate"

if name in config:
    print(config[name])
```

But when talking about performance, care is needed. A dictionary is generally used as a very useful and fast structure for key-based lookup, but that does not mean it is always the best in every situation. The key must be hashable, and if the order of data itself is important, a list or another structure may fit better.

## Is a Dictionary a Hash Map?

When looking at a Python dictionary, the question `is this a hash map?` naturally appears. The short answer is: from the usage perspective, a dictionary can be understood as a mapping structure that finds a value by key, and from the implementation perspective, it can be understood as a data structure that uses hashing.

But in this section, we do not immediately call a dictionary only a `hash map`. There are three reasons.

First, the official Python documentation describes a dictionary as the standard mapping type. The first perspective the reader needs to become familiar with is `it connects a key to a value`.

Second, the word hash map is closer to an implementation method. Detailed concepts such as hash, hashability, collision, and table come along with it. The purpose of this section is to understand `why do we find by key rather than by position?` when reading Python code, rather than the internal implementation.

Third, a Python dictionary does not correspond exactly to one named container in the C++ STL. If you understand it centered on key sorting like C++ `std::map`, that can be wrong; and if you understand it as a multi-index structure that looks up one piece of data simultaneously through several indexes, that is also too much. The official Python documentation explains that dictionary keys preserve insertion order, but that does not mean keys are sorted.

Even so, the connection to hash should be remembered. The key of a Python dictionary must be hashable. That is why unchanging values such as strings, numbers, and tuples are often used as keys, while changeable values such as lists usually cannot be used as dictionary keys.

Problem situation: I want to see a simple dictionary example that finds a score by a string key.
Input: `scores_by_name`, where names are keys and scores are values.
Expected output: the score `82` connected to the key `"Kim"`.
Concept to check: dictionary lookup is the action of finding a value based on a stable key.

```python
# This example checks how a dictionary finds and connects values by key.
scores_by_name = {
    "Kim": 82,
    "Lee": 91,
}

print(scores_by_name["Kim"])
```

In this example, `"Kim"` is a key, and Python uses this key to find the connected value. Even without knowing the internal implementation in detail, the feeling that `if you want to find a value by key, the key must identify it stably` should remain.

| Question | Answer in this section |
| --- | --- |
| Is a dictionary a hash map? | From the implementation perspective, it can be understood as a hash-based mapping. |
| Then should I just memorize it as a hash map? | Early on, it is safer to understand it first as `a mapping that finds values by key`. |
| Is it sorted like a map tree? | According to the official documentation, it preserves insertion order, but it is not explained as a structure sorted by key. |
| Is it a multi-index structure? | No. One dictionary is a mapping that finds a value by one key. If several lookup criteria are needed, the structure must be designed separately. |
| Why is there a restriction on keys? | Because the key is the criterion for finding a value, it must be hashable. |
| Do I need to learn hash tables now? | Not in this section. They are looked at more deeply later when data structures are handled. |

One more thing to be careful about is that the same key cannot be stored several times. If a new value is stored under the same key, the old value is replaced by the new one.

Problem situation: I want to confirm that if a value is placed under the same key twice, only the last value remains.
Input: an empty dictionary `scores` and two assignments to the key `"Kim"`.
Expected output: a dictionary where only the last value `91` remains under the key `"Kim"`.
Concept to check: one key points only to one current value, and upon reassignment the previous value is overwritten.

```python
# This example checks how a dictionary finds and connects values by key.
scores = {}

scores["Kim"] = 82
scores["Kim"] = 91

print(scores)
```

This code does not store both scores under the key `"Kim"`. Only the last value, `91`, remains. If you want to gather several values under one key, you must place a list on the value side.

Problem situation: I want to see how to store several scores for one person under one key.
Input: a dictionary where the key `"Kim"` is connected to the score list `[82, 91]`.
Expected output: the score list connected to the key `"Kim"` is printed.
Concept to check: if several values are needed under one key, a grouped structure such as a list must be placed on the value side.

```python
# This example checks how a dictionary finds and connects values by key.
scores = {
    "Kim": [82, 91],
}

print(scores["Kim"])
```

Therefore, a Python dictionary can feel like `a structure that is easy to access quickly by key`, but it is not an all-purpose index structure for large-scale data. If the data becomes very large, if several criteria must be searched at once, or if sorting and range search become important, databases, pandas, or separate index structures should be considered. In this section, as the stage before that, we learn the key-based mapping feeling most often encountered in Python code.

Here, remember the following criteria.

- Use a list when order and position matter.
- Use a dictionary when finding values by key matters.
- A dictionary is suitable for data that is found by name, such as configuration values, label maps, and metadata.
- A dictionary is connected to hash-based implementation, but in this section it is read first from the perspective of mapping.
- A dictionary is not assumed to be a key-sorted tree or a multi-index structure.
- The pattern of accumulating values in a dictionary while repeating, such as counting by key, is handled in P2-8.4.

## Situations Where Dictionaries Are Used

A dictionary is suitable when `by what criterion should a value be found?` is clear.

### Group of Configuration Values

Problem situation: I want to see a typical dictionary-use example where a learning setting value is found by setting name.
Input: `config`, which contains `batch_size`, `learning_rate`, and `epochs`.
Expected output: the value of `learning_rate` is printed.
Concept to check: configuration data fits dictionaries well because names matter more than order.

```python
# This example checks how a dictionary finds and connects values by key.
config = {
    "batch_size": 32,
    "learning_rate": 0.001,
    "epochs": 10,
}

print(config["learning_rate"])
```

For configuration values, names matter more than order. If you find a value through the name `learning_rate`, the meaning is clearer than finding it by position like `config[1]`.

### Changing a Label Number into a Name

Problem situation: I want to see an example that changes the model's numeric label into a human-readable string name.
Input: `label_map`, which connects numeric keys to sentiment names, and the predicted label `2`.
Expected output: the string `neutral` is printed.
Concept to check: a dictionary is often used as a correspondence table between label number and label name.

```python
# This example checks how a dictionary finds and connects values by key.
label_map = {
    0: "negative",
    1: "positive",
    2: "neutral",
}

predicted_label = 2

print(label_map[predicted_label])
```

When a model output is a numeric label, a dictionary can be used to change it into a name a human can read.

### Finding Data by Sample ID

Problem situation: I want to see a structure that immediately finds the text of the corresponding data by one sample ID.
Input: `samples_by_id`, which uses sample IDs as keys and sample information as values.
Expected output: the text `"good product"` corresponding to `"s001"` is printed.
Concept to check: a dictionary can be used as a lookup structure that goes from identifier to data body.

```python
# This example checks how a dictionary finds and connects values by key.
samples_by_id = {
    "s001": {"text": "good product", "label": "positive"},
    "s002": {"text": "bad service", "label": "negative"},
}

sample_id = "s001"

print(samples_by_id[sample_id]["text"])
```

As data grows, `which piece of data has which ID?` can matter more than `which numbered piece of data is it?` At that point, a dictionary is used like a map from ID to sample.

### Attaching Meaning by Column Name

Problem situation: I want to see an example where what a column name means is managed in a separate explanation table.
Input: `column_description`, which connects column names to explanatory strings.
Expected output: the explanation for the key `"score"` is printed.
Concept to check: a dictionary is suitable for organizing metadata and explanatory information by name.

```python
# This example checks how a dictionary finds and connects values by key.
column_description = {
    "text": "input sentence",
    "label": "correct label",
    "score": "model score",
}

print(column_description["score"])
```

When reading a dataset, if the meaning of column names is organized separately, later preprocessing and documentation become easier.

## A Dictionary Can Look Similar to an Object, but They Are Not the Same Word

Because of the examples seen so far, a dictionary can look similar to an object in JSON or to the object notation of some languages. That is because it uses braces and finds values by name. So when looking at API responses or configuration files, dictionaries and objects can appear in similar shapes.

But in this section, we do not call a dictionary an object. In Python, object is a broader word. Numbers, strings, lists, dictionaries, and functions can all be seen as objects. By contrast, a dictionary is specifically a mapping structure that connects keys to values.

| Perspective | Python dictionary | General object perspective |
| --- | --- | --- |
| central idea | a mapping that finds values by key | a target that has state and behavior together |
| criterion for finding a value | key | attribute, field |
| AI-practice connection | configuration values, label maps, API responses, metadata | class instances, model objects, library objects |
| point of caution | if the key is absent, an error can occur | the access method can differ by object |

Therefore, it causes less misunderstanding to first read a dictionary not as `a light object`, but as `a structure that finds values by key`. Object, class, and method go beyond the central scope of this chapter, so they are handled separately when needed later.

## Be Careful That a Key May Be Missing

If you immediately take out a missing key from a dictionary, an error can occur.

Problem situation: I want to show what risk appears when an absent key is looked up immediately.
Input: the dictionary `student`, which has only `name` and `score`, and the absent key `"label"`.
Expected output: an example where looking up the absent key fails.
Concept to check: an error can occur if a dictionary is read under the assumption that every key is always present.

```python
# This example checks how a dictionary finds and connects values by key.
student = {"name": "Kim", "score": 82.5}

print(student["label"])
```

This code fails because the key `"label"` does not exist.

In situations where a key may be absent, `get()` can be used.

Problem situation: I want to check how to read an absent key a little more safely.
Input: `student.get("label")` and `student.get("label", "unknown")`.
Expected output: by default `None`, and if a default is given, `"unknown"` is printed.
Concept to check: `get()` is a safe lookup tool when handling data where a key may be missing.

```python
# This example checks how a dictionary finds and connects values by key.
student = {"name": "Kim", "score": 82.5}

print(student.get("label"))
print(student.get("label", "unknown"))
```

When handling data files or API responses, problems can appear if you assume every key always exists. Real data can mix in missing values, differently named values, and types different from what was expected.

## Case Study

### Case 1. When You Want to Change a Label Number into a Human-Readable Name

Suppose a sentiment classification model returns only numbers such as `0`, `1`, and `2` as prediction results. A person cannot immediately understand the meaning from these numbers alone, and for a report or a screen, names such as `negative`, `positive`, and `neutral` are needed.

At that point, the first method you might think of is placing them into a list in order. But what matters here is not which numbered value it is, but `which number corresponds to which name`. In other words, the criterion key matters more than position.

A dictionary is a structure suited to reading and writing this kind of correspondence table. If keys and values are connected like `0 -> negative` and `1 -> positive`, the prediction number can easily be changed into a human-readable name. Configuration values, sample IDs, and column descriptions can all be seen in the same way.

The confirmable result is whether the name immediately comes out when the numeric prediction label is put in. If the desired string can be obtained through `label_map[prediction]`, then it is more natural to read this problem with a dictionary than with a list.

## Checklist

- You can explain a dictionary as a group of keys and values.
- You can explain a dictionary as a mapping structure.
- You can explain a dictionary from the usage perspective as a mapping and from the implementation perspective as a hash-based structure.
- You can explain the difference that a list finds values by position while a dictionary finds values by key.
- You can explain that `get()` is useful in situations where a key may be absent.
- You can read examples of label maps, configuration values, sample ID lookup, and column descriptions.
- You can distinguish how to read lookups when a key may be absent.

## Sources and References

- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm dictionary creation, key-based value access, and iteration examples using `items()`.
- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm that `dict` is a mutable mapping type and a structure for finding values through keys.
- Python Software Foundation, [Glossary: dictionary, hashable](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm the glossary definitions of dictionary and hashable.
- Python Software Foundation, [Data model](https://docs.python.org/3/reference/datamodel.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as background for dictionary key constraints by confirming object identity/type/value and hashability.
