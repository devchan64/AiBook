# P2-2.2 Sigma and Repeated Computation

> Section ID: `P2-2.2`
> Version: `v2026.07.12`

In P2-2.1, we reread variables, functions, and expressions. Now we move to the notation for repeated computation that appears very often in formulas.

\[
\sum
\]

Sigma may look unfamiliar, but the core is simple. It means that several values should be added repeatedly. In AI documents, it appears frequently when explaining the sum over many data points, means, sums of loss, and batch-level computation.

Here, we show the structure that sigma is `notation that compresses repeated addition`, and explain how it connects to loops in code, array computation, and mean-loss calculation.

Here, we reorganize again `sigma`, `index`, `mean`, `repeated computation`, and `loss aggregation`. If 2.1 read the minimum grammar of variables, functions, and expressions, this section organizes into what compressed notation that grammar changes when it is repeated across many data points.

## Scope of This Section

This section handles sigma and repeated computation. Limits are handled in `P2-2.3`. Vectors, matrices, and matrix multiplication are handled in `P2-3.1` and `P2-3.3`. Loss functions and optimization return in `P2-6.2` and `P2-6.1`.

The question to solve first here is this: `When sigma is attached to one line of notation, how do you immediately read what is being added and how many times?`

So this section first fixes only the following four places.

- What does sigma tell you to keep adding?
- How does an index show the repeated position?
- Why does sigma appear so often in mean and loss calculation?
- How does sigma notation become loops and array computation in code?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| sigma | notation that tells you to repeat the same shape of addition | the central symbol of this section |
| index | the name that shows which item you are looking at | the standard for reading repeated position |
| mean | the value obtained by adding many values and dividing by the count | the easiest example of sigma |
| repeated computation | the structure that applies the same calculation to many data items | the background of loops and array computation |
| loss aggregation | the process of summing or averaging the losses of many samples | the bridge into machine learning |

If the previous section handled the minimum grammar of one line of notation, here we read what compressed notation that grammar turns into when repeated over many data points. In the immediately following sections on limits, vectors, and loss, this repeated structure continues more concretely into rate of change, array computation, and total loss aggregation.

This section sets the standard for reading `what is being added, and how many times`. The details of statistical formulas and loss functions are recovered later.

The flow after this section is also simple.

- In the next section, `P2-2.3`, we move away from repetition and aggregation and read how a function changes when a value changes slightly.
- In Chapter 3 and Chapter 11, we continue into how this repeated structure appears inside vectors, arrays, and batch computation.
- In Chapter 6 and Part 4, we read again the structure of summing or averaging loss over many samples.

Once you understand sigma, many later topics become easier to read. In particular, the structure `when there are many data points, the same calculation is repeated and the results are gathered` starts to become visible.

- It becomes easier to read statistical notation such as mean, variance, and standard deviation, which summarize many values.
- It becomes easier to understand why loss and mean loss are calculated over many data items.
- It becomes easier to follow the flow in vectors, matrices, and batch computation where many components or samples are handled at once.
- It becomes easier to accept explanations such as "the effects of many terms are combined" when learning gradients and optimization.
- It prepares you to see Python loops, NumPy array computation, and tensor operations in deep-learning frameworks as different expressions of the same repeated structure.

## Goals of This Section

- You can read sigma as compressed notation for repeated addition.
- You can distinguish the index, the start value, the end value, and the term to be added.
- You can explain a mean from both the sigma viewpoint and the code viewpoint.
- You can read intuitively the flow of summing or averaging losses over many data points.
- When sigma appears, you can first ask, "What is being added, and how many times?"
- You can read sigma notation by separating the upper part, lower part, and right-hand term.
- You can explain why sigma later continues into statistics, loss calculation, batch computation, and optimization.
- You can expand a simple sigma expression and compute the actual sum.

## Three Criteria

The following three viewpoints act as standards while reading the main text.

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| Sigma is compressed notation that tells you to repeat addition of the same shape | It lets you reread an unfamiliar symbol as computational structure. | Understand that when you see sigma, you ask what is being added and how many times. |
| The index is the name that distinguishes which item is being added | It keeps you from losing the repeated position. | Understand that you connect subscripts with the repeated index. |
| Sigma appears often in AI documents because many data points are gathered into sums, means, and losses | It shows why statistics and loss aggregation share the same notation. | Understand that mean and loss aggregation both have the structure of repeated addition. |

## Reading Sigma from a Math-Education Viewpoint

In mathematics education, sigma is usually introduced as "the symbol for a sum." But when rereading it for the first time, it is more helpful to split the roles inside the notation than to stop at the definition that it is a sum symbol.

\[
\sum_{i=1}^{n}x_i
\]

This one line contains three pieces of information.

- the large symbol \(\sum\): the command to add
- the lower part \(i=1\): where the repetition starts
- the upper part \(n\): where the repetition ends
- the right-hand term \(x_i\): what is added each time

If you separate it like this, sigma stops looking like a suddenly appearing difficult symbol and starts reading like a sentence that writes repeated addition briefly.

1. Start `i` from 1.
2. Repeat until `i` reaches `n`.
3. Add `x_i` each time.

So sigma is not only a symbol that says "sum." It is notation that also writes what is gathered, in what order, and over what range. This viewpoint is also useful when you recall a loop in code.

That does not mean sigma is exactly the same thing as a code loop. Mathematical notation shows computational structure in compressed form, while code unfolds it into actual execution procedure. Here, the connection is only that the two expressions show the same repeated structure in different ways.

## Expanding a Simple Sigma Expression

The best way to read sigma is to expand a short expression directly.

\[
\sum_{i=1}^{3} i
\]

This expression means that as `i` changes from 1 to 3, you add `i` itself.

```text
value added when i = 1: 1
value added when i = 2: 2
value added when i = 3: 3
```

So it can be expanded as follows.

\[
\sum_{i=1}^{3} i = 1 + 2 + 3 = 6
\]

If you look at a form closer to AI documents, you get the following.

\[
\sum_{i=1}^{3}x_i
\]

If \(x_1=2\), \(x_2=4\), and \(x_3=6\), then you compute it as follows.

\[
\sum_{i=1}^{3}x_i = x_1 + x_2 + x_3 = 2 + 4 + 6 = 12
\]

If you go on to compute the mean, it becomes the following.

\[
\frac{1}{3}\sum_{i=1}^{3}x_i = \frac{1}{3}(2 + 4 + 6) = 4
\]

Even being able to do only this much expansion is enough to prepare you to read notation such as mean loss, batch loss, and the sum over a whole dataset in AI documents. What matters is not memorizing a formula, but building the habit that when sigma appears, you first expand it and compute it.

## Sigma Writes Repeated Addition in Short Form

Suppose the following data exists.

\[
x_1 = 1,\quad x_2 = 2,\quad x_3 = 3,\quad x_4 = 4
\]

If you add all four values directly, it becomes the following.

\[
x_1 + x_2 + x_3 + x_4
\]

Sigma writes this repetition more briefly.

\[
\sum_{i=1}^{4}x_i
\]

Read this as follows.

1. Change `i` from 1 to 4.
2. Bring out `x_i` one by one.
3. Add them all.

In other words, it is the same as the following calculation.

\[
x_1 + x_2 + x_3 + x_4
\]

When you see sigma, the first thing to look at is not the shape of the symbol, but the repeated structure. First look at what is being added, where it starts, where it ends, and what name marks the repeated position.

## The Index Marks the Repeated Position

In sigma, `i` is the index. The index is the name that tells you which position you are looking at now.

\[
\sum_{i=1}^{n}x_i
\]

Here, each part is read as follows.

- `i`: the index that marks the repeated position
- `1`: the starting position
- `n`: the ending position
- `x_i`: the i-th value
- `Σ`: the sign that tells you to change `i` and add values

In code, it looks roughly like the following.

Problem situation: translate the repeated-addition structure of sigma into a code loop.
Input: the list `values` containing four values.
Expected output: the total sum `10` is printed.
Concept to check: the repeated structure of sigma notation can appear in code as a loop and an accumulated total.

```python
values = [1, 2, 3, 4]
total = 0

for value in values:
    total = total + value

print(total)
```

Example execution result:

```text
10
```

The `i` in the formula and the `value` in code are not completely the same thing. But they connect in that both indicate the current item being looked at during repetition.

## A Mean Is the Sum Divided by the Count

A mean is a good example for understanding sigma. When you add all the values and divide by the count, you get the mean.

\[
\mathrm{mean} = \frac{x_1 + x_2 + x_3 + x_4}{4}
\]

Written with sigma, it is compressed as follows.

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

This expression can be read as follows.

1. Change `i` from 1 to `n` and add all the `x_i`.
2. Divide that sum by `n`.

In code, you can write it as follows.

Problem situation: compute the mean formula through code using `sum` and `len` instead of reading it only through sigma notation.
Input: the list `values` containing four values.
Expected output: the mean value `2.5` is printed.
Concept to check: a mean is a repeated structure in which many values are added and then divided by the count.

```python
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

Example execution result:

```text
2.5
```

If you use a NumPy array, it becomes shorter.

Problem situation: express the same mean calculation more briefly with a NumPy array method.
Input: the NumPy array `values` that holds four values.
Expected output: the mean value `2.5` is printed.
Concept to check: even if sigma is not written directly, the same repeated structure is still inside the array computation.

```python
import numpy as np

values = np.array([1, 2, 3, 4])
mean = values.mean()

print(mean)
```

Example execution result:

```text
2.5
```

Here, `values.mean()` performs the mean calculation internally. It does not write sigma directly, but the structure of gathering many values and computing over them remains the same.

## Loss Is Also Repeated Across Many Data Points

In machine learning, loss expresses numerically the gap between the model output and the reference value. If there is only one data point, then only one loss needs to be computed.

\[
\mathrm{loss} = (\mathrm{prediction} - \mathrm{target})^2
\]

But in real learning, there are many data points. For each data point, there is a prediction and a target, and for each data point a loss is created.

\[
\mathrm{loss}_1,\ \mathrm{loss}_2,\ \mathrm{loss}_3,\ \cdots,\ \mathrm{loss}_n
\]

If you simply add the whole loss, it becomes the following.

\[
\mathrm{total\_loss} = \mathrm{loss}_1 + \mathrm{loss}_2 + \cdots + \mathrm{loss}_n
\]

Written with sigma, it becomes the following.

\[
\mathrm{total\_loss} = \sum_{i=1}^{n}\mathrm{loss}_i
\]

Mean loss is that sum divided by the number of data items.

\[
\mathrm{mean\_loss} = \frac{1}{n}\sum_{i=1}^{n}\mathrm{loss}_i
\]

In code, it can be seen as follows.

Problem situation: repeatedly compute the losses for many data points and then find the mean loss.
Input: the prediction list `predictions` and the answer list `targets`.
Expected output: the average of the sample losses is printed.
Concept to check: loss also has the structure of repeating the same calculation over many data points and then taking the mean of the results.

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

Example execution result:

```text
0.09999999999999998
```

This example simplifies real deep-learning training code. The key point is that, because there are many data items, the same computation is repeated and the repeated results are summed or averaged.

## Batch Computation Is Read with the Same Perspective

In deep learning, it is common not to process data one by one, but to process them as a batch. Inside one batch are many samples, and the model creates one output for each sample. Here, `batch` is the bundle of many input data items, `prediction` is the model output for each input, `loss` is the gap between each output and reference value, and `mean_loss` is the mean of the losses inside the batch.

Even here, the sigma viewpoint remains the same. You inspect each sample inside the batch, compute the loss for each sample, and then sum or average those losses.

## Case Study

### Case 1. Why Batch Loss Must Be Read as the Sum of Many Cases Rather Than as One Case

When a learner sees a model loss formula, they may feel, "Why is sigma attached here at all?" If you look at only the prediction error for one case, it looks simple. But actual learning usually judges by looking at many data items at once and gathering their loss.

For example, if four images are fed in as one batch, then one loss appears for each image. At that point, sigma compresses the repeated structure `compute the loss of each of the four images and add them all`. Mean loss is then the value obtained by dividing that sum again by the number of data items.

This case reveals that sigma is not mere mathematical decoration. In almost every scene that summarizes many values together, such as mean, variance, total loss, and batch loss, sigma is in charge of the structure `repeat the same computation and gather the results`.

So when you see sigma, the first question should be `what is being added, and how many times?` Holding on to only this question already makes complicated-looking loss and statistics formulas feel much less foreign.

Library code can hide this repetition.

Problem situation: express the repeated loss computation above all at once with NumPy array operations.
Input: the prediction array `predictions` and the target array `targets`.
Expected output: the mean loss value is printed.
Concept to check: even if a loop is not visible, the same repeated structure is still executed inside array computation.

```python
import numpy as np

predictions = np.array([2.8, 4.1, 5.0])
targets = np.array([3.0, 4.0, 4.5])

losses = (predictions - targets) ** 2
mean_loss = losses.mean()

print(mean_loss)
```

Example execution result:

```text
0.09999999999999998
```

The loop is not visible, but the repeated computation has not disappeared. The array computation has only changed the expression so that many values are handled at once.

## The Order for Reading Sigma

When sigma appears, read it in the following order.

1. What is the thing being added?
2. What is the repeated index?
3. Where is the start and where is the end?
4. Is the result a sum or a mean?
5. In code, does it appear as a loop or as array computation?

For example, look at the following expression.

\[
\frac{1}{n}\sum_{i=1}^{n}(\mathrm{prediction}_i - \mathrm{target}_i)^2
\]

This can be read as: for the i-th prediction and the i-th target, compute the difference, square that difference, add them all while changing `i` from 1 to `n`, and finally divide by `n` to obtain the mean.

This leads into the intuition of mean squared error (MSE). But MSE itself can be handled later in the sections on evaluation metric and loss function. Here, remember only that sigma compresses repeated computation.

## Why Sigma Feels Difficult

Sigma does not feel difficult because addition itself is difficult. It feels difficult because compressed information such as the repeated variable, repeated range, term to add, total sum, and whether the result is a mean are all gathered in one place.

When all that information enters one line, it can feel unfamiliar. But if you unfold it into code, it is usually nothing more than a loop or an array computation.

Sigma notation can unfold in code into a loop, an array operation, and the computation of a sum or a mean.

So rather than memorizing sigma, it is more important to practice expanding it.

## Checklist

- Can you explain sigma as compressed notation for repeated addition?
- Can you distinguish the index, the start position, the end position, and the term to be added?
- Can you explain a mean both with sigma notation and with code?
- Can you explain the flow of summing or averaging losses over many data items?
- Can you explain that loops and array computation can connect to sigma notation?
- When sigma appears, can you unfold it by asking, `what is being added, and how many times?`
- Can you explain why sigma helps later when reading statistics, loss calculation, batch computation, and optimization?
- Can you expand a simple sigma expression into terms and compute the sum or mean?
- Can you explain sigma less as a symbol to memorize and more as the first sign for reading repetition and aggregation?
- Can you connect mean, loss, and batch computation by explaining that they share the same aggregation structure through sigma and code?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked on 2026-06-24.
