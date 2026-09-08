# P2-2.2 Sigma and Repeated Computation

> Section ID: `P2-2.2`
> Version: `v2026.09.08`

Sigma is notation that compresses the addition of multiple values.

\[
\sum
\]

Sigma may look unfamiliar, but the core is simple. It means that several values should be added repeatedly. In AI documents, it appears frequently when explaining the sum over many data points, means, sums of loss, and batch-level computation.

## Repetition Range and Terms

| Criterion | Why It Matters |
| --- | --- |
| Sigma is compressed notation that tells you to repeat addition of the same shape | It lets you reread an unfamiliar symbol as computational structure. |
| The index is the name that distinguishes which item is being added | It keeps you from losing the repeated position. |
| Sigma appears often in AI documents because many data points are gathered into sums, means, and losses | It shows why statistics and loss aggregation share the same notation. |

## Parts of Sigma Notation

Sigma notation specifies both the repetition range and the term to add.

\[
\sum_{i=1}^{n}x_i
\]

This one line contains four pieces of information.

- the large symbol \(\sum\): the command to add
- the lower part \(i=1\): where the repetition starts
- the upper part \(n\): where the repetition ends
- the right-hand term \(x_i\): what is added each time

If you separate it like this, sigma stops looking like a suddenly appearing difficult symbol and starts reading like a sentence that writes repeated addition briefly.

1. Start `i` from 1.
2. Repeat until `i` reaches `n`.
3. Add `x_i` each time.

So sigma is not only a symbol that says "sum." It is notation that also writes what is gathered, in what order, and over what range. This viewpoint is also useful when you recall a loop in code.

That does not mean sigma is exactly the same thing as a code loop. Mathematical notation shows computational structure in compressed form, while code unfolds it into actual execution procedure.

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

## Indices and Loops

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

the list `values` containing four values. the total sum `10` is printed.

```python
# values is the list of values to add repeatedly.
values = [1, 2, 3, 4]

# total accumulates the sum as the loop passes through the values.
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

## Sums and Means

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

the list `values` containing four values. the mean value `2.5` is printed.

```python
# values is the data to average, and mean is the summary value.
values = [1, 2, 3, 4]
mean = sum(values) / len(values)

print(mean)
```

Example execution result:

```text
2.5
```

If you use a NumPy array, it becomes shorter.

the NumPy array `values` that holds four values. the mean value `2.5` is printed.

```python
import numpy as np

# values is the repeated-calculation target converted into a NumPy array.
values = np.array([1, 2, 3, 4])

# mean aggregates the whole array into one average value.
mean = values.mean()

print(mean)
```

Example execution result:

```text
2.5
```

Here, `values.mean()` performs the mean calculation internally. It does not write sigma directly, but the structure of gathering many values and computing over them remains the same.

## Per-Sample Loss and Mean Loss

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

the prediction list `predictions` and the answer list `targets`. the average of the sample losses is printed.

```python
# predictions and targets are paired lists of predicted and real values for each sample.
predictions = [2.8, 4.1, 5.0]
targets = [3.0, 4.0, 4.5]

# losses collects each sample's squared error in order.
losses = []
for prediction, target in zip(predictions, targets):
    loss = (prediction - target) ** 2
    losses.append(loss)

# mean_loss summarizes the losses from several samples as one average loss.
mean_loss = sum(losses) / len(losses)
print(mean_loss)
```

Example execution result:

```text
0.09999999999999999
```

This example simplifies real deep-learning training code. The key point is that, because there are many data items, the same computation is repeated and the repeated results are summed or averaged.

## Aggregating Batch Loss

In deep learning, it is common not to process data one by one, but to process them as a batch. Inside one batch are many samples, and the model creates one output for each sample. Here, `batch` is the bundle of many input data items, `prediction` is the model output for each input, `loss` is the gap between each output and reference value, and `mean_loss` is the mean of the losses inside the batch.

Even here, the sigma viewpoint remains the same. You inspect each sample inside the batch, compute the loss for each sample, and then sum or average those losses.

## Loops and Array Operations

For the three samples above, the squared errors are approximately `0.04`, `0.01`, and `0.25`. Their mean is `(0.04 + 0.01 + 0.25) / 3 = 0.1`. NumPy applies subtraction and squaring at each array position, then computes the mean with `mean()`.

The inputs are prediction and target arrays. The code prints their mean loss.

```python
import numpy as np

# predictions and targets are arrays of predicted and real values to compare at once.
predictions = np.array([2.8, 4.1, 5.0])
targets = np.array([3.0, 4.0, 4.5])

# losses is the per-sample squared-error array, and mean_loss is its average.
losses = (predictions - targets) ** 2
mean_loss = losses.mean()

print(mean_loss)
```

Example execution result:

```text
0.09999999999999999
```

The loop is not visible, but the repeated computation has not disappeared. The array computation has only changed the expression so that many values are handled at once.

## Checklist

- Can you explain sigma as compressed notation for repeated addition?
- Can you distinguish the index, the start position, the end position, and the term to be added?
- Can you explain a mean both with sigma notation and with code?
- Can you explain the flow of summing or averaging losses over many data items?
- Can you explain that loops and array computation can connect to sigma notation?
- When sigma appears, can you unfold it by asking, `what is being added, and how many times?`
- Can you explain why sigma helps later when reading statistics, loss calculation, batch computation, and optimization?
- Can you expand a simple sigma expression into terms and compute the sum or mean?
- Can you connect mean, loss, and batch computation by explaining that they share the same aggregation structure through sigma and code?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked on 2026-07-19.
- NumPy Developers, [numpy.sum](https://numpy.org/doc/stable/reference/generated/numpy.sum.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This official reference explains summing array elements and sums along axes.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This official reference supports the mean calculation and `mean()` examples.
