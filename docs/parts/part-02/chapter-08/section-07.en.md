# P2-8.7 Supplemental Learning: Distinguishing References and Copies

> Section ID: `P2-8.7`
> Version: `v2026.07.23`

In P2-8.2, we saw that assigning a list to another name does not automatically create a new copy. Many readers get confused immediately at this point.

`Is this the same value under another name?`  
`Or did we create another similar value?`

This supplement gives a basic explanation that distinguishes `reference`, `shallow copy`, and `deep copy`. It organizes the criteria for deciding whether a list or dictionary structure is looking at the same actual object or at a separate copy.

Rather than explaining Python's memory model in depth, this supplement builds the minimum criteria needed to read whether `the original changes together` in data work and practice code.

| Term | Meaning to capture first in this Section |
| --- | --- |
| reference | A state where multiple names point to the same object together. |
| assignment | An operation that connects a name to another value or object without guaranteeing a new copy. |
| shallow copy | A copy that makes only the outer container new and may still share inner values. |
| deep copy | A copy that also creates new nested inner values so that they are separated from the original. |
| nested structure | A structure where another grouped value exists inside, such as a list inside a list. |

## First Reading Criteria: How to First Distinguish References, Shallow Copy, and Deep Copy

- You can explain that two names can point to the same object together.
- You can explain shallow copy as a copy that creates only the outer shell anew.
- You can explain deep copy as a way of copying that also recreates nested inner values.
- You can explain why shallow copy in a nested list can look as if it changes together with the original.
- You can explain that when preserving the original is important in data preprocessing, you should check copying first.

## Learning Background

In early Python learning, many scenes involve putting one value into a variable and changing it. But once you start handling structures that contain many values inside, such as lists, dictionaries, and DataFrames, `which object did I change?` becomes as important as `what did I change?`

This sense becomes necessary again later in Pandas and data preprocessing. When handling tables, interpretation can change depending on whether you preserve the original, create a new intermediate result, or have multiple names referring to the same object.

## Main Learning Content

This supplement first captures the following three distinctions as a large frame.

| Distinction | Question to hold first | Core sense at this stage |
| --- | --- | --- |
| assignment | Did we create a new value, or are we calling the same object by another name? | Assignment does not automatically mean copying |
| shallow copy | Up to where is something newly created, and up to where is it still shared? | It creates only the outside anew, while the inside may still be shared |
| deep copy | Do we need a copy completely separated from the original? | It recreates even the nested inner values |

If you capture these three distinctions first, you can read `why did the original also change?` more quickly in later list-handling and data-preprocessing examples.

## Detailed Learning Content

### Two names can point to the same list together

The first point to hold is that assignment does not always mean copy.

Problem situation: You want to check whether two names are looking at the same list after assigning one list to another variable.
Input: A list `scores` and `other_scores` pointing to the same list.
Expected output: When you add a value through one name, the result viewed through both names changes together.
Concept to check: Simple assignment does not guarantee creation of a new copy.

```python
# This example checks how reference and copying differ for mutable values such as lists.
scores = [82, 75, 91]
other_scores = scores

other_scores.append(68)

print(scores)
print(other_scores)
```

The example output is as follows.

```text
[82, 75, 91, 68]
[82, 75, 91, 68]
```

Here, `scores` and `other_scores` point to the same list. So when you add a value through one name, the same change appears when you look through the other name as well.

Remember it this way here.

- `a = b` does not automatically guarantee that a new copy was created.
- Multiple names can look at the same mutable object together.

### A shallow copy creates only the outside anew

A shallow copy creates a new outer container, while the values inside may still be referred to as they are.

Problem situation: You want to see how a shallow copy that recreated only the outer list differs from the original.
Input: A list `scores` and `copied_scores` created with `scores.copy()`.
Expected output: A value is added only to `copied_scores`, while the original `scores` remains as it was.
Concept to check: Because shallow copy creates the outer container anew, top-level addition and deletion can become separate.

```python
# This example checks how reference and copying differ for mutable values such as lists.
scores = [82, 75, 91]
copied_scores = scores.copy()

copied_scores.append(68)

print(scores)
print(copied_scores)
```

The example output is as follows.

```text
[82, 75, 91]
[82, 75, 91, 68]
```

In this case, the outer list itself was created anew, so the result of `append()` is not directly reflected in the original.

But if we stop here, we have not fully understood shallow copy. The story changes when another list exists inside.

### Shallow copy becomes easy to misunderstand in a nested list

Now look at a case where a list contains another list.

Problem situation: You want to directly check why shallow copy becomes confusing in a nested list.
Input: A nested list `matrix` and its shallow copy `shallow`.
Expected output: When you change an inner list, the original and the shallow copy both change together.
Concept to check: A shallow copy may not recreate nested inner objects.

```python
# This example checks how reference and copying differ for mutable values such as lists.
matrix = [[1, 2], [3, 4]]
shallow = matrix.copy()

shallow[0][0] = 99

print(matrix)
print(shallow)
```

The example output is as follows.

```text
[[99, 2], [3, 4]]
[[99, 2], [3, 4]]
```

Why does this happen?

- The outer list `matrix` was copied anew.
- But the inner lists `[1, 2]` and `[3, 4]` may still be shared as they are.

In other words, it helps to understand shallow copy with the image: `we created only the outer box again, but the smaller boxes inside may remain the same`.

### A deep copy recreates the inside too

A deep copy also copies nested inner values anew.

Problem situation: You want to check whether a deep copy also separates nested inner values.
Input: `deep` created with `copy.deepcopy(matrix)`.
Expected output: Even if you change `deep`, the original `matrix` remains unchanged.
Concept to check: A deep copy recreates even nested inner structures and separates them from the original.

```python
# This example checks how reference and copying differ for mutable values such as lists.
import copy

matrix = [[1, 2], [3, 4]]
deep = copy.deepcopy(matrix)

deep[0][0] = 99

print(matrix)
print(deep)
```

The example output is as follows.

```text
[[1, 2], [3, 4]]
[[99, 2], [3, 4]]
```

Now even the inner lists were newly created, so changing `deep` does not affect `matrix`.

Distinguish them here with the following criteria.

| Method | Intuition | Point to watch in nested structures |
| --- | --- | --- |
| assignment | We see the same object under another name | A change on one side can appear together as it is |
| shallow copy | Only the outside is newly created | Nested inner values may still be shared |
| deep copy | Even the inside is newly created | Better for preserving the original, but may cost more |

## Cases and Examples

In data preprocessing, you often want to keep the original table and make a separate experimental copy.

- Keep the original data.
- Make a separate experimental version with derived columns.
- Keep intermediate versions too when comparing filtered results.

If you do not stay aware of copying, you may think you preserved the original while actually changing the same object together.

You need to be even more careful about this in Pandas. However, this Section does not go deeply into the details of Pandas `copy()` and view or view-like behavior. Instead, it connects to the attitude of asking first in Part 2 Chapter 12, `Do I need to preserve the original dataset?`

### Case 1. Why the original also changes when I thought I made a separate preprocessing list

Suppose a learner wanted to preserve the original score list while modifying only an experimental list. So they wrote `experiment_scores = base_scores` and changed only one list, but later found that the original had changed too.

The human-first assumption is often `I created a new name, so it must have been copied.` But with mutable structures, assignment does not necessarily mean a new copy. In a nested structure where a list contains another list, the result changes a lot depending on whether only the outer layer was copied or the inner layer was recreated too.

This is also why this supplement separates reference, shallow copy, and deep copy. In data preprocessing, preserving the original is often important, so you should first check `Is the object I am changing actually separated from the original?`

The checkable result is whether the value seen through another name also changes when you modify one side. If changing one side immediately changes the other side too, there is a high chance both names are looking at the same object together. In a nested structure, if only the outside was copied, you should suspect shallow copy.

## Practice and Examples

Look at the following code and first guess whether each case is `assignment`, `shallow copy`, or `deep copy`.

Problem situation: You want to compare assignment, shallow copy, and deep copy at once and see the difference directly.
Input: A nested list `base` and `case_a`, `case_b`, `case_c`.
Expected output: In A and B, the original changes together; in C, the original stays preserved.
Concept to check: In a nested structure, assignment and shallow copy can still share the original, while deep copy breaks that sharing.

```python
# This example checks how reference and copying differ for mutable values such as lists.
import copy

base = [[10, 20], [30, 40]]

case_a = base
case_b = base.copy()
case_c = copy.deepcopy(base)

case_a[0][0] = -1
print("A:", base, case_a)

base = [[10, 20], [30, 40]]
case_b = base.copy()
case_b[0][0] = -1
print("B:", base, case_b)

base = [[10, 20], [30, 40]]
case_c = copy.deepcopy(base)
case_c[0][0] = -1
print("C:", base, case_c)
```

The example output is as follows.

```text
A: [[-1, 20], [30, 40]] [[-1, 20], [30, 40]]
B: [[-1, 20], [30, 40]] [[-1, 20], [30, 40]]
C: [[10, 20], [30, 40]] [[-1, 20], [30, 40]]
```

The key point here is B. The outer layer was copied, but the inner list changed together, so you can directly see how far shallow copy creates a new target.

## Checklist

- Can you explain that two names can point to the same list together?
- Can you explain the difference between a shallow copy and a deep copy through a nested-list example?
- Can you explain why data preprocessing needs caution about whether copying happened?
- Can you distinguish assignment, shallow copy, and deep copy by whether the original is still shared?

## Sources and References

- Python Software Foundation, [The Python Tutorial - More on Lists](https://docs.python.org/3/tutorial/datastructures.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used to confirm list assignment, `list.copy()`, slice copying, and list-method examples.
- Python Software Foundation, [Standard Library - `copy`](https://docs.python.org/3/library/copy.html){: target="_blank" rel="noopener noreferrer" }, Python 3.14.6 documentation, checked on 2026-07-20. Used as the core basis for the difference between assignment and copying, the definitions of shallow and deep copy, and the copying difference for nested objects.
