# P2-8.4 Loops: Processing Iterables One by One

> Section ID: `P2-8.4`
> Version: `v2026.07.20`

In P2-8.2, we looked at lists, and in P2-8.3, we looked at dictionaries. Now we separate out the loop that processes these groups one by one.

Python loops become structurally clearer when read not as `how many times is it repeated?` but as `from what is what taken out one by one?` In this section, we organize iterable, iterator, and loop patterns at the level of basic concepts.

Here, we explain the basic distinction among `loop`, `iterable`, and `iterator`. The representative explanation of `list` and `dictionary` is left in P2-8.2, P2-8.3, and in the [Concept Glossary](/AiBook/reference/concept-glossary/), and here we focus on turning values from those groups into a processing flow by taking them out one by one.

Loops are not syntax that exists only in Python. In data processing, statistical calculation, and model evaluation, several items are almost always processed one after another by the same criterion. Python's `for` is an example that shows that general flow in an easy-to-read form.

Here, rather than memorizing loop syntax by type, we turn grouped data structures into actual processing flow. If the earlier sections on lists and dictionaries dealt with `in what structure are values stored?`, here we read what is being made by taking values out one by one from that structure. If this transition is first established, then even in the later section on functions, it becomes natural to move to the perspective of `reusing something that wrapped a loop`.

## What to Take Away First

This section contains both an introduction to loop patterns and a supplementary explanation of loop abstraction. On a first reading, it is enough to first grasp only the `essential` items below.

| Category | What to take away first |
| --- | --- |
| essential | The point that `for item in items` is a structure that takes values out one by one from a group |
| essential | The point that `enumerate()` is used when position and value must be seen together, and `.items()` is used when the key and value of a dictionary must be seen together |
| essential | The point that `zip()` is used when two or more groups are read side by side |
| essential | The point that loop results often appear as output, making a new group, or accumulation |
| extended | A stricter explanation that distinguishes iterable and iterator more precisely |
| extended | The history of PEP 234 and the iteration interface |
| extended | A feeling for loop abstraction that continues to later topics such as generators |

| What to establish in this section | Question that follows immediately | Where it is used again later |
| --- | --- | --- |
| The point that `for item in items` is a structure that takes items one by one from a group | This leads to how such loop processing is wrapped into functions and reused in P2-8.5. | It continues to be used in preprocessing, evaluation, file handling, and organizing model outputs. |
| The point that lists and dictionaries are traversed differently inside loops | This makes it clearer when to use `enumerate()`, `.items()`, and `zip()`. | It repeats later in DataFrame row handling, iterating over configuration values, and result aggregation. |
| The point that loop results often appear as output, a new group, or an accumulated value | This leads to the criterion for reading comprehension and accumulation patterns in the same frame. | It becomes the basis later in preprocessing before NumPy, basic Python practice, and reading project code. |

| Term | Meaning to establish first in this section |
| --- | --- |
| loop | A flow that applies the same criterion of processing to several values one after another. |
| iterable | A structure that can send out values one by one and can therefore become a loop target. |
| iterator | The actual loop device that takes out the next value one by one. |
| accumulation | A pattern that adds or gathers values during a loop to make one result. |
| comprehension | A compact expression that makes a new list or dictionary by looping. |

## Goal of This Section

- You can read a `for item in items` loop.
- You can distinguish iterable and iterator at an introductory level.
- You can explain that the word `iterable` is used to cover not only sequences, but also targets such as dictionaries, files, and generators that can send out values one by one.
- You can explain what kind of loop pattern `enumerate()`, `.items()`, and `zip()` are.
- You can distinguish filtering, transformation, accumulation, and condition-based separation loops.
- You can read list comprehension and dictionary comprehension as `expressions that create a new data structure by looping`.
- You can read the pattern that gathers results into an empty list and the pattern that accumulates values by key into a dictionary.
- You can explain that directly changing the original collection during a loop can create problems.

## Criteria to Hold First

The criterion that must be held first in this section is that `a loop is a flow that applies the same processing to several values one after another`.

| Loop scene | Question to ask first |
| --- | --- |
| `for score in scores` | What is being taken out one by one? |
| `enumerate(scores)` | Is the position also needed? |
| `metrics.items()` | Do name and value need to be seen together? |
| `zip(a, b)` | Are two or more groups being read side by side? |

In other words, rather than memorizing loop syntax, it is more important first to read `what is being taken out from a group, and what is being made from it?`

## Learning Background

A loop is not a stage of simply learning one more Python syntax. It is a stage of recovering the basic data-work flow that `several values are processed by the same criterion`. Even if you have already seen lists and dictionaries, once a loop is attached, the code must be read as `looking at items`, `making a new group`, or `accumulating a value`.

Here, we treat that transition clearly. So instead of syntax memorization, the structure is built so that `what is being taken out from a group, and what is being made from it?` is read first.

## Three Criteria

Here, rather than loop syntax, we first establish the feeling of `taking values out one by one from a group and processing them`. The following three criteria become the foundation for reading later sections on function reuse and preprocessing examples.

| Criterion | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| A loop is a way of applying the same processing to several values | It lets you see the purpose before memorizing the `for` statement | Understand it as a structure that takes values out one by one from a list and prints them |
| Python loops are more naturally read as `from what is something taken out one by one?` than as `how many times?` | This connects item-centered looping to the iterable concept | You should be able to explain that `for score in scores` is a structure that takes values out one by one from `scores` |
| Loop results often appear as output, making a new group, or making an accumulated value | It becomes easier later to read comprehension and data-preprocessing examples | Understand that a loop can create a new list or dictionary |

## Main Learning Content

### A Loop Is a Way of Applying the Same Processing to Several Values

In general, a loop is a way of processing a data group one item at a time. It applies the same rule to several items, and then the result is printed, made into a new group, or gathered into an accumulated value.

Python's `for` loop clearly shows the perspective that `items are taken out one by one from a group and processed`.

Problem situation: I want to see the most basic loop that takes values out one by one from a list and applies the same processing.
Input: the score list `scores`.
Expected output: each score is printed on its own line.
Concept to check: `for item in items` is the basic structure that takes items out one by one from a group and processes them.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

This code uses values taken one by one from the list `scores` under the name `score`.

A person who learned another language first may imagine a loop centered on numeric indexes.

Problem situation: I want to compare how the same loop looks when written using position numbers.
Input: the score list `scores`.
Expected output: the scores accessed by index are printed in order.
Concept to check: item-centered loops and position-centered loops can produce the same result, but the reading perspective is different.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]

for i in range(len(scores)):
    print(scores[i])
```

This way also works. But if the purpose is to process items one by one, a form like `for score in scores`, which is item-centered, shows the intention more clearly.

The official Python tutorial also explains that the `for` statement is a little different from the numeric progression style familiar from C or Pascal, and that it iterates through the items of a sequence such as a list or string in order.

| Perspective | General explanation | In Python |
| --- | --- | --- |
| loop | A procedure that processes the values of a group one by one | The form `for item in items` is often used |
| loop target | A group from which values can be taken out one by one | It is called an iterable |
| loop result | output, a new group, an accumulated value, or a separated group | It appears as `print`, `append`, an accumulation variable, dictionary accumulation, and so on |

If these three are rewritten again in a practical form:

| Loop result | Commonly seen shape |
| --- | --- |
| output | `print(score)` |
| making a new list | `results.append(...)` |
| making an accumulated value | `total += score` |
| condition-based separation | selecting only some items with `if ...:` |

### Why Is It Called an Iterable?

From here, the nature becomes a little more `extended`. If the earlier feeling for item-centered loops, `enumerate()`, `.items()`, and `zip()` is already established, this paragraph does not need to be fully digested at once.

`iterable` means “a target that can be looped over.” In Korean, it can be translated as iterable, repeatable object, or repeatable target. This expression is needed because Python loops are not tied only to sequences such as lists.

From older memories of learning programming, it is easy to first imagine loops like this.

- A numeric variable is increased one by one.
- The positions 0, 1, 2 of an array are accessed in order.
- The loop stops when it reaches the ending position.

This way is natural when handling arrays or lists. But not every loop target is `an array that can be accessed by numeric index`. A dictionary finds values by key, a file reads one line at a time, and a generator creates values one at a time when needed. To handle all these targets with a `for` statement, what matters more than `does it have indexes?` is `can it send out values one by one?`

This flow can also be confirmed in Python's history. PEP 234 is a proposal written in 2001 that proposed an iteration interface through which an object can control the behavior of a `for` loop. The proposal connects to the loop structure around Python 2.2 and shows the flow by which the `for` statement came to handle several kinds of repeatable objects consistently beyond the older sequence-centered loop.

The core of PEP 234 can be generalized as follows.

| Loop that is easy to imagine earlier | Python's iterable perspective |
| --- | --- |
| Which numbered position should be taken out? | Can I receive the next value one by one? |
| Does it need indexes like an array or list? | Even if it is not a list, can it still form a loop flow? |
| Must the loop know the inside of the structure? | Can the object provide its own way of looping? |

In official Python terminology, an iterable is an object capable of returning its members one at a time. Not only sequences such as lists, strings, and tuples, but also dictionaries, file objects, and classes made directly by the programmer can be iterable. And the `for` statement makes an iterator from that iterable, and then processes the values given by that iterator one by one.

This perspective is important. When seeing `for item in items`, you must not assume `items` is necessarily a list. `items` may be a list, the result of `.items()` from a dictionary, a file, or a generator that will be seen later. The names differ, but the common question is the same.

Can this target send out values one by one?

### The Feeling of Iterable and Iterator

When reading Python code, you encounter various loop patterns.

Problem situation: I want to reconfirm the shortest `for` example that loops over items only.
Input: `scores`.
Expected output: the scores are printed one by one.
Concept to check: even if loop patterns differ, the starting point is taking values out one by one from an iterable.

```python
# This example checks how a loop takes items one by one from a value collection.
for score in scores:
    print(score)
```

Problem situation: I want to briefly check the loop pattern where position and value are seen together.
Input: `enumerate(scores)`.
Expected output: position and score are printed together.
Concept to check: `enumerate()` is a loop tool used when you also need to know which numbered value it is.

```python
# This example checks how a loop takes items one by one from a value collection.
for index, score in enumerate(scores):
    print(index, score)
```

Problem situation: I want to see the shortest example that loops over name and value together from a dictionary.
Input: `metrics.items()`.
Expected output: the metric name and value are printed together.
Concept to check: in dictionary loops, `.items()` is the basic pattern that takes out key and value together.

```python
# This example checks how a loop takes items one by one from a value collection.
for name, value in metrics.items():
    print(name, value)
```

The outward shapes differ, but they have something in common. Python's `for` processes values one by one from a `repeatable target`.

In official terminology, a repeatable target is called an iterable. An iterable is an object that can return its members one at a time. Lists, strings, tuples, dictionaries, and file objects are examples of iterables.

An iterator is an object that actually takes out the stream of values one by one. In this section, more than the detailed usage of `iter()` and `next()`, we first keep the sense that `for` internally creates this kind of loop flow.

If very simplified, it can be seen like this.

| Term | Introductory explanation | Example |
| --- | --- | --- |
| iterable | a target that can be taken out one by one | list, string, dictionary, file |
| iterator | the flow that actually sends out the next value one by one | an object obtained through `iter(scores)` |
| loop | code that receives and processes those values one by one | `for score in scores` |

Because of this structure, several loop patterns in Python connect under the same principle. What matters is `what is being looped over` and `what is being made as the loop result`.

## Detailed Learning Content

### Main Types of Loop Structures

Python loops are better read by distinguishing patterns rather than by memorizing only one syntax.

In this section, we look at loop patterns in the following order. First, we see the basic form that takes out items one by one, then position, key-value pairs, and pairing of two groups. After that, we look at flows that make a new list or accumulate values as the result of the loop, and that separate values according to conditions.

| Flow | Central question |
| --- | --- |
| item loop | What is being taken out one by one? |
| loop with position | Is the numbered position also needed? |
| key-value loop | Must the name and the value be seen together? |
| result building | Is a new list or dictionary being made? |
| accumulation and separation | Is a value being accumulated, or split by condition? |

### Process Items One by One

This is the most basic loop.

Problem situation: I want to fix once more the basic form of item loops.
Input: the score list `scores`.
Expected output: each score is printed in order.
Concept to check: item loops center the value itself more than the position.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]

for score in scores:
    print(score)
```

The way to read it is simple.

Take `score` out one by one from `scores` and process it.

In AI practice, this is used often when looking one by one at samples, sentences, file names, and prediction results.

### Look at Position and Item Together

When the numbered position is also needed, use `enumerate()`.

Problem situation: I want to see a loop where the numbered position must also be checked together.
Input: `enumerate(scores)`.
Expected output: the position number and score are printed together.
Concept to check: `enumerate()` lets the loop proceed by attaching position information to the value.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]

for index, score in enumerate(scores):
    print(index, score)
```

Read it as follows.

Take out position and value together from `scores` and process them.

It is useful when checking which sample number produced an error, or when checking only the first few results.

### Look at the Key and Value of a Dictionary Together

For dictionaries, `.items()` is often used.

Problem situation: I want to see a loop that checks a dictionary's key and value at the same time.
Input: the metric dictionary `metrics`.
Expected output: `accuracy`, `loss`, and their values are printed.
Concept to check: dictionary loops are often read not only as keys, but as key-value pairs.

```python
# This example checks how a loop takes items one by one from a value collection.
metrics = {"accuracy": 0.91, "loss": 0.32}

for name, value in metrics.items():
    print(name, value)
```

Read it as follows.

Take out metric name and value together from `metrics` and process them.

This is often seen when checking configuration values, evaluation metrics, and API responses.

### Look at Two Groups Side by Side

When you want to see two lists paired by the same position, you may encounter `zip()`.

Problem situation: I want to see input texts and labels together by pairing the same positions.
Input: the two lists `texts` and `labels`.
Expected output: text and label are printed as pairs.
Concept to check: `zip()` makes the loop proceed with items from the same positions of several iterables together.

```python
# This example checks how a loop takes items one by one from a value collection.
texts = ["good", "bad", "great"]
labels = ["positive", "negative", "positive"]

for text, label in zip(texts, labels):
    print(text, label)
```

Read it as follows.

Take out `texts` and `labels` together by the same order and process them one by one.

This pattern appears when handling together input sentences and labels, predictions and correct answers, or file names and paths.

### Gather Only the Values That Fit a Condition into a New Group

In P2-8.2, we said that an empty list can be created first. In loops, that empty list is often used as the container that gathers results.

While looping, only values that satisfy a condition can be made into a new list.

Problem situation: I want to see a filtering loop that gathers only valid values into a new list from a score list containing `0`.
Input: the score list `scores`, which includes `0`.
Expected output: `valid_scores`, containing only scores other than `0`.
Concept to check: loops are often used to make a new group by selecting only the items that satisfy a condition.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 0, 75, 0, 91]
valid_scores = []

for score in scores:
    if score != 0:
        valid_scores.append(score)

print(valid_scores)
```

Read it as follows.

Look at `scores` one by one, and gather only the values that satisfy the condition into `valid_scores`.

This is often seen in preprocessing such as removing missing values, excluding values below a criterion, or selecting only a specific label.

### Change Values and Make a New Group

A loop is also used to change existing values into different values.

Problem situation: I want to see a transformation loop that changes scores into values between 0 and 1 and makes a new list.
Input: the score list `scores`.
Expected output: `normalized_scores`, where each score is divided by 100.
Concept to check: a loop can apply the same transformation to every item and make a new result group.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

Read it as follows.

Look at `scores` one by one, and change each value into something like a value between 0 and 1, then store it in a new list.

This pattern appears when doing normalization, lowercasing, trimming leading and trailing spaces, and other cases where `the same processing is applied to every item`.

### Make a New List with List Comprehension

If the loop rule is short and the result is a new list, you may encounter list comprehension.

Problem situation: I want to see an example that makes a new list in one line from a short loop rule.
Input: `range(5)`.
Expected output: `squares`, a list of square values.
Concept to check: list comprehension is a compact expression that makes a new list by looping.

```python
# This example checks how a loop takes items one by one from a value collection.
squares = [number * number for number in range(5)]

print(squares)
```

This code makes the list of square values from `0` to `4`.

If a condition is attached, filtering and transformation can also be written together in one line.

Problem situation: I want to see an example that selects only fitting values and makes a new list with comprehension.
Input: the score list `scores` containing `0`.
Expected output: `valid_scores`, collecting only values other than `0`.
Concept to check: comprehension can combine filtering and new-list creation in one expression.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 0, 75, 0, 91]

valid_scores = [score for score in scores if score != 0]

print(valid_scores)
```

Read it as follows.

Look at `score` one by one from `scores`, and make a new list containing only values that are not `0`.

In this section, we place things in the order of first checking the structure through a long `for` statement, then reading the compact expression.

### Python Also Puts Loops Inside Data-Structure Definitions

In Python code, you often encounter patterns that make it look as if a loop statement has been placed inside the syntax of defining a list or dictionary. This is called comprehension.

Comprehension is an expression that makes a new collection by processing the items of an existing iterable one by one. The official Python tutorial describes list comprehension as a compact way of making a new list. In this section, we broaden that perspective slightly and understand it as a loop expression for making a new data structure such as a list or dictionary.

By definition, the following three elements are seen together.

| Element | Question | Example |
| --- | --- | --- |
| input iterable | From what is something taken out one by one? | `scores` |
| loop variable | By what name is the value taken out called? | `score` |
| result expression | What is being made and put in from the value taken out? | `score / 100` |

So `[score / 100 for score in scores]` is read like this.

Take `score` out one by one from `scores`, and make a new list where each `score` is changed into `score / 100`.

If written as a long `for` statement, it looks like this.

Problem situation: I want to first see the ordinary `for` statement structure before comprehension.
Input: the score list `scores`.
Expected output: the normalized score list `normalized_scores`.
Concept to check: comprehension is usually a shortened form of a loop that uses `append()`.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91]
normalized_scores = []

for score in scores:
    normalized_scores.append(score / 100)

print(normalized_scores)
```

If the same intention is written as a list comprehension, it becomes shorter like this.

Problem situation: I want to compare how the shape changes when the loop just above is shortened into a comprehension.
Input: the score list `scores`.
Expected output: a one-line expression making the same normalized result.
Concept to check: comprehension is especially easy to read when the goal of the loop is making a new data structure.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91]

normalized_scores = [score / 100 for score in scores]

print(normalized_scores)
```

This expression means `take score one by one from scores, and make a new list by changing each value into score / 100`. It does not hide the loop; it reveals through its shape that the purpose of the loop is making a new list.

A dictionary can also be made in the same way.

Problem situation: I want to see a comprehension example that makes a new dictionary by looping.
Input: the label list `labels` and `enumerate(labels)`.
Expected output: `label_to_id`, where the label name is the key and the position is the value.
Concept to check: dictionary comprehension is also an expression that makes a new mapping structure by looping.

```python
# This example checks how a loop takes items one by one from a value collection.
labels = ["negative", "positive", "neutral"]

label_to_id = {label: index for index, label in enumerate(labels)}

print(label_to_id)
```

This code makes a dictionary where the label name is the key and the position number is the value.

The reasons comprehension is preferred are the following.

| Reason | Explanation |
| --- | --- |
| intention | The purpose of making a new list or dictionary is visible immediately |
| compactness | It reduces the procedure of making an empty list and calling `append()` |
| consistency | What is taken out and what it becomes are gathered into one line |
| data processing | It expresses often-used patterns such as filtering, transformation, and mapping shortly |

But comprehension is not always better. If the condition is long, if there are many nested loops, or if intermediate calculations must be given names, a normal `for` statement is easier to read.

Problem situation: I want to see a case where a normal `for` statement is easier to read because intermediate calculation and condition appear together.
Input: a loop that checks `item["score"]` and normalizes it.
Expected output: code that adds only values that passed the condition to `results`.
Concept to check: there are cases where ordinary loops that show the steps are more suitable than comprehension.

```python
# This example checks how a loop takes items one by one from a value collection.
results = []

for item in items:
    if item["score"] >= 60:
        normalized_score = item["score"] / 100
        results.append(normalized_score)
```

In code like this, it is better that the several steps are visible. Therefore, in this section, we use the following criteria.

- If the loop result is a new list or dictionary and the rule is short, you can read comprehension.
- If the processing is long or needs explanation, use an ordinary `for` statement.
- Rather than memorizing comprehension as `advanced syntax`, understand it as `an expression that makes a new data structure by looping`.

### Calculate an Accumulated Value

A loop is also used to accumulate values one by one.

Problem situation: I want to see an example that builds the total score one by one through a loop.
Input: the score list `scores` and the initial value `total = 0`.
Expected output: the total sum of all scores.
Concept to check: an accumulation loop keeps updating the result so far in a variable.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 75, 91, 68]
total = 0

for score in scores:
    total = total + score

print(total)
```

Read it as follows.

Look at `scores` one by one, and keep adding them into `total`.

This structure appears in calculations that are accumulated repeatedly, such as sums, counts, occurrence frequencies, and accumulated loss.

### Separate by Condition

One group can also be split into two groups.

Problem situation: I want to see a loop that separates a score list into passed and failed groups.
Input: the score list `scores` and the criterion `60`.
Expected output: the two lists `passed` and `failed`.
Concept to check: if you use a loop and a conditional together, one group can be separated into several result groups.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 55, 91, 42, 68]
passed = []
failed = []

for score in scores:
    if score >= 60:
        passed.append(score)
    else:
        failed.append(score)

print(passed)
print(failed)
```

Read it as follows.

Look at `scores` one by one, and place them into different lists according to the condition.

This becomes the basic feeling later for splitting training data and test data, separating normal and abnormal data, and separating data by label.

### Accumulate into a Dictionary

In P2-8.3, we saw dictionaries as structures that find values by key. When used together with loops, they become `structures that accumulate values by key`.

When loops and dictionaries are used together, aggregation by key becomes possible.

Problem situation: I want to see a loop that counts how many times each label appears by key.
Input: the label list `labels`.
Expected output: `label_counts`, which contains the count of each label.
Concept to check: together with a loop, a dictionary can build accumulated aggregation by key.

```python
# This example checks how a loop takes items one by one from a value collection.
labels = ["positive", "negative", "positive", "neutral", "positive"]
label_counts = {}

for label in labels:
    label_counts[label] = label_counts.get(label, 0) + 1

print(label_counts)
```

Read it as follows.

Look at `labels` one by one, and accumulate in the dictionary how many times the same label appears.

This pattern is often used when checking label distribution in classification data.

## Cases and Examples

### A Small Data-Processing Example

The following example looks at the scores of several students and puts only the students who exceeded the criterion into a passed list.

Problem situation: I want to see a small data-processing example where lists, dictionaries, and conditional loops are used together.
Input: `students`, a list containing student dictionaries.
Expected output: `passed_students`, which contains only the names of students who passed.
Concept to check: in real data processing, a group of samples, field lookup, and conditional filtering appear together inside one loop.

```python
# This example checks how a loop takes items one by one from a value collection.
students = [
    {"name": "Kim", "score": 82.5},
    {"name": "Lee", "score": 55.0},
    {"name": "Park", "score": 91.0},
]

passed_students = []

for student in students:
    if student["score"] >= 60:
        passed_students.append(student["name"])

print(passed_students)
```

Three structures appear together here.

| Code | Meaning |
| --- | --- |
| `students` | a list containing student information |
| `{"name": "Kim", "score": 82.5}` | a dictionary expressing one student |
| `for student in students` | a loop that takes out student information one by one |

This example is small, but it resembles the basic structure of AI practice.

- A dataset is a group of several samples.
- One sample can have several fields.
- The loop checks samples one by one.
- The conditional chooses needed samples or changes the processing method.

### Be Careful About Changing the Original During a Loop

If the same list or dictionary is directly changed while looping over it, results different from what was expected can appear.

For example, code that deletes items while iterating over the same list must be handled carefully.

Problem situation: I want to see a safe filtering method that makes a new result list instead of deleting directly from the original.
Input: the score list `scores` containing `0`.
Expected output: the new list `filtered_scores`, excluding `0`.
Concept to check: it is clearer to make a new collection rather than directly changing the original collection during a loop.

```python
# This example checks how a loop takes items one by one from a value collection.
scores = [82, 0, 75, 0, 91]
filtered_scores = []

for score in scores:
    if score != 0:
        filtered_scores.append(score)

print(filtered_scores)
```

This example does not directly delete from the original `scores`, but makes a new list `filtered_scores`. The official Python tutorial also explains that code that modifies the same collection while iterating over it can be tricky, and that iterating over a copy or making a new collection can be clearer.

This principle is also useful in data preprocessing.

- Preserve the original data.
- Place the filtered result under a new name.
- Leave in the code by what criterion it was filtered.

### Case 1. If You Want to Pick Only the Passed Ones from Several Samples, What Are You Looping Over?

Suppose a learner wants to look at several text samples and gather only those samples that have labels. A person may be able to look at one sample and judge it at first, but once the number of samples exceeds dozens, the same criterion must be applied repeatedly.

At that point, if a loop is seen only as `syntax that loops several times`, it becomes easy to miss the structure. What actually matters is `from what is what taken out one by one?` and `what is being made as the result?` The core flow is taking samples one by one from a sample list, checking a condition, and gathering results into a new list or dictionary.

This is also why this section divides loops into patterns such as iterable, item loop, accumulation, filtering, and aggregation by key. In practice, a loop is not simply a device for writing long code; it is the basic structure for processing many pieces of data by the same criterion.

The confirmable result can be seen by whether a new result group is made. For example, if after iterating once over a sample list, a result such as `passed_samples` or `label_counts` appears, then the loop performed not simple printing, but filtering or accumulation.

## Practice and Examples

### Common Questions for Reading Examples

As examples of lists, dictionaries, and loops increase, you can get lost by following only the syntax. At that point, read the code with the following questions.

1. What is the group?
2. Is order important in that group, or is key important?
3. What is the loop taking out one by one?
4. What is done with the value taken out?
5. Is the result a new list, a new dictionary, output, or an accumulated value?

For example, look at the following code.

Problem situation: I want to read a loop that makes a list of sentence lengths from a sentence list through common questions.
Input: the sentence list `texts`.
Expected output: `lengths`, containing the length of each sentence.
Concept to check: loop code can be read in the frame of group, value taken out one by one, processing, and result.

```python
# This example checks how a loop takes items one by one from a value collection.
texts = ["AI is useful", "Models can fail", "Data matters"]
lengths = []

for text in texts:
    lengths.append(len(text))

print(lengths)
```

This code is read like this.

| Question | Answer |
| --- | --- |
| What is the group? | `texts` |
| Is order important, or is key important? | It is a sentence list, so it is an ordered list |
| What is taken out one by one? | one sentence at a time |
| What is done with the value taken out? | its length is calculated |
| What is the result? | the list of lengths, `lengths` |

This question can be used later as-is when reading NumPy, Pandas, and machine-learning data-processing code. Even if the tool changes, the structure of `group, value taken out one by one, processing, result` remains.

## Checklist

- Can you read `for item in items`?
- Can you say when `enumerate()`, `.items()`, and `zip()` are used?
- Can you distinguish whether the loop result is output, a new group, or accumulation?
- You can read a `for item in items` loop and explain the execution flow.
- You can distinguish iterable and iterator at an introductory level.
- You can explain that the word iterable is used to cover not only sequences, but also targets such as dictionaries, files, and generators that can send out values one by one.
- You can explain that `enumerate()` can be used when position is needed.
- You can explain that `.items()` can be used when the key and value of a dictionary need to be seen together.
- You can explain that `zip()` can be encountered when two groups are looked at side by side.
- You can distinguish item loops, transformation loops, accumulation loops, and condition-based separation loops.
- You can read list comprehension and dictionary comprehension as expressions that make new data structures by looping.
- You can explain that when comprehension becomes complex, an ordinary `for` statement may be more suitable.
- You can explain that directly changing the original data during a loop can create problems.
- You can explain that before syntax, you should first check the input group and the shape of the result.

## Sources and References

- Python Software Foundation, [More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as the official basis for `for`, `range()`, function-definition examples, and control-flow descriptions.
- Python Software Foundation, [Data Structures](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm list comprehensions, dictionary iteration, `items()` examples, and cautions about modifying a collection while iterating.
- Python Software Foundation, [Glossary: iterable, iterator](https://docs.python.org/3/glossary.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as the basis for distinguishing iterable and iterator at an introductory level.
- Python Software Foundation, [The for statement](https://docs.python.org/3/reference/compound_stmts.html#the-for-statement){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm that a `for` statement assigns items one by one from an iterator over an iterable expression.
- Ka-Ping Yee, Guido van Rossum, [PEP 234 -- Iterators](https://peps.python.org/pep-0234/){: target="_blank" rel="noopener noreferrer" }, Python Enhancement Proposals, 2001, checked on 2026-07-20. Used to confirm the historical background in which Python's iteration interface moved beyond sequence-centered iteration toward objects providing their own iteration behavior.
