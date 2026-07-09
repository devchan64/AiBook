# P2-2.2 Sigma and Repeated Computation

> Section ID: `P2-2.2`
> Version: `v2026.07.09`

P2-2.1 reread variables, functions, and expressions. Now we move to one of the most common notations for repeated computation.

\[
\sum
\]

Sigma may look unfamiliar, but its core meaning is simple: keep adding repeated terms. In AI documents, it appears whenever we talk about sums over many data points, means, aggregated loss, and batch-level computation.

## Scope of This Section

This Section focuses on sigma and repeated computation. The key question is simple: when sigma appears in one line of notation, how do you immediately read what is being added and how many times?

So this Section fixes four places first.

- What does sigma tell you to keep adding?
- How does the index mark the repeated position?
- Why do means and loss calculations so often use sigma?
- How does sigma notation become loops and array computation in code?

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| Sigma is compressed notation for repeated addition | It lets you reread an unfamiliar symbol as computational structure | Understand that sigma makes you ask what is being added and how many times |
| The index marks which item is being added | It helps you track the repeated position | Understand how the repeated index connects to subscripted terms |
| Sigma appears often in AI because many documents aggregate means and losses over many data points | It shows why statistics and loss aggregation share the same notation | Understand that means and loss aggregation are both repeated-addition structures |

## Sigma Compresses Repeated Addition

Suppose the following values exist:

\[
x_1 = 1,\quad x_2 = 2,\quad x_3 = 3,\quad x_4 = 4
\]

Adding them directly gives:

\[
x_1 + x_2 + x_3 + x_4
\]

Sigma writes the same repetition more compactly:

\[
\sum_{i=1}^{4}x_i
\]

Read it like this:

1. Let `i` move from 1 to 4.
2. Take `x_i` one by one.
3. Add them all.

## The Index Marks the Repeated Position

In sigma notation, `i` is the index. It tells you which position you are looking at.

\[
\sum_{i=1}^{n}x_i
\]

In code, the same structure can look like this:

```python
values = [1, 2, 3, 4]
total = 0

for value in values:
    total = total + value

print(total)
```

Example output:

```text
10
```

## A Mean Is a Sum Divided by the Count

A mean is the easiest example for understanding sigma.

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

In code:

```python
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

Example output:

```text
2.5
```

With NumPy:

```python
import numpy as np

values = np.array([1, 2, 3, 4])
mean = values.mean()

print(mean)
```

Example output:

```text
2.5
```

## Loss Is Also Repeated over Many Data Points

With one sample, loss can be written as:

\[
\mathrm{loss} = (\mathrm{prediction} - \mathrm{target})^2
\]

But actual learning uses many data points, so the same computation is repeated many times:

\[
\mathrm{total\_loss} = \sum_{i=1}^{n}\mathrm{loss}_i
\]

\[
\mathrm{mean\_loss} = \frac{1}{n}\sum_{i=1}^{n}\mathrm{loss}_i
\]

In code:

```python
predictions = [2.8, 4.1, 5.0]
targets = [3.0, 4.0, 4.5]

losses = []
for prediction, target in zip(predictions, targets):
    loss = (prediction - target) ** 2
    losses.append(loss)

mean_loss = sum(losses) / len(losses)
print(mean_loss)
```

Example output:

```text
0.09999999999999998
```

## Perspective to Keep from This Section

Sigma is a short way to write repeated addition. The index marks which item you are currently reading. Means and loss aggregation both use sigma because both are structures that collect many repeated terms into one summary.

## Short Check

- You can read sigma as repeated addition.
- You can identify the repeated term, the start, the end, and the index.
- You can explain a mean from both sigma notation and code.
- You can explain why many losses are summed or averaged during learning.

## Sources and References

This Section organizes the notation needed to reread repeated computation in Part 2 and does not directly quote external material.
