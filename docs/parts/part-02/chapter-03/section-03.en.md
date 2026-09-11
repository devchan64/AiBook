# P2-3.3 What Does Matrix Multiplication Reuse?

> Section ID: `P2-3.3`
> Version: `v2026.09.08`

Matrix multiplication looks at first like a simple multiplication rule, but in practice it is closer to `a calculation that reuses the same weighted-sum pattern many times`.

1. Bundle input values together with weights and add them.
2. Make one new value.
3. Repeat the same calculation for several outputs.
4. Apply it to several inputs at once.

## Weighted Sums and Dimension Requirements

| Criterion | Why it matters |
| --- | --- |
| Matrix multiplication reuses weighted sums | Because it is the basic calculation that can create not only one output, but several outputs at once. |
| Shape decides whether the calculation is possible | Because if the inner dimensions do not match, we cannot decide which value corresponds to which weight. |
| Linear transformation changes representation | Because explanations of neural-network layers and classifiers all continue into calculations that turn an input into a new representation. |

## Element-Wise and Matrix Multiplication

In P2-3.1, we said that vectors or matrices with the same shape can be added position by position. Multiplication can also be written as element-wise multiplication.

\[
[1,\ 2,\ 3] \odot [4,\ 5,\ 6] = [4,\ 10,\ 18]
\]

Here, \(\odot\) marks multiplication of values at the same positions. This calculation processes each position separately.

Matrix multiplication is different. Matrix multiplication is not a calculation that multiplies only matching positions. It creates new values by combining a row from one side with a column from the other.

1. Element-wise multiplication multiplies matching positions.
2. Matrix multiplication multiplies and adds by matching rows and columns.

We need to separate these two first. If matrix multiplication is misunderstood as element-wise multiplication, we misread both shape errors and the meaning of the calculation.

## A Weighted Sum and One Output

First, think about one vector and one set of weights.

\[
\mathbf{x} = [2,\ 3]
\]

\[
\mathbf{w} = [4,\ 5]
\]

If we multiply matching positions and then add them, one number comes out.

\[
2 \times 4 + 3 \times 5 = 8 + 15 = 23
\]

This calculation can be read as follows.

1. Multiply the first input value by the first weight.
2. Multiply the second input value by the second weight.
3. Add the results.
4. Make one output value.

This is the basic form of a weighted sum.

\[
y = x_1w_1 + x_2w_2
\]

In AI models, input values do not always carry the same importance. Some values can be reflected strongly, some weakly, and some in a negative direction. A weight expresses this degree of influence as a number.

## Weighted Sums for Multiple Outputs

To make one output, we needed one weight vector. If we want to make two outputs, we need two weight vectors.

\[
\mathbf{x} = [2,\ 3]
\]

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

Here, \(W\) is a weight matrix. The first column can be read as the weights for making the first output value, and the second column as the weights for making the second output value.

\[
\mathbf{y} = \mathbf{x}W
\]

When calculated, it becomes the following.

\[
\mathbf{y}
=
[2,\ 3]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

\[
=
[2 \times 4 + 3 \times 5,\ 2 \times 1 + 3 \times 2]
\]

\[
=
[23,\ 8]
\]

This calculation has reused the weighted sum twice.

```text
First output: 2 x 4 + 3 x 5 = 23
Second output: 2 x 1 + 3 x 2 = 8
```

Matrix multiplication repeatedly applies the small calculation `multiply and add` to several outputs. That is why matrix multiplication becomes a tool for turning one input vector into an output vector of another shape. In this example, the input vector has length 2, the weight matrix has shape `(2, 2)`, and the output vector also has length 2.

## Input Length and Matrix Row Count

In matrix multiplication, shape is extremely important. The number of values in the input vector must match the number of rows of the weight matrix.

\[
[2,\ 3]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

In this calculation, the input vector has length 2 and the matrix also has 2 rows. So each input value can correspond to the weights in each row.

By contrast, the following calculation does not match immediately.

\[
[2,\ 3,\ 4]
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

The input has 3 values, but the weight matrix has a shape that can receive only 2 inputs.

1. The input length and the input-side size of the weight matrix must match.
2. If they do not match, we cannot decide which value should be multiplied with which weight.

This is one reason shape errors appear so often in AI code. Matrix multiplication is, both mathematically and in code, a calculation that can run only when the shapes match.

## Batch Calculation of Multiple Inputs

The power of matrix multiplication is not only in handling one input. We can gather several inputs into a matrix and calculate them at once.

For example, suppose we have two input vectors.

\[
X =
\begin{bmatrix}
2 & 3 \\
1 & 4
\end{bmatrix}
\]

Each row is one input sample.

```text
First sample: [2, 3]
Second sample: [1, 4]
```

Now multiply by the same weight matrix \(W\).

\[
W =
\begin{bmatrix}
4 & 1 \\
5 & 2
\end{bmatrix}
\]

\[
Y = XW
\]

The calculation result becomes:

\[
Y =
\begin{bmatrix}
23 & 8 \\
24 & 9
\end{bmatrix}
\]

The first row is the output of the first sample, and the second row is the output of the second sample.

1. Gather several input samples into a matrix.
2. Multiply by the same weight matrix.
3. Obtain several output samples at once.

This connects to the basic intuition of batch calculation. A model can process inputs one by one, but if several inputs are bundled and calculated at once, the same calculation structure can be reused repeatedly.

## Linear Transformations and Output Dimensions

Linear transformation can first be understood as a calculation that changes one vector into another by multiplying by a matrix.

1. Prepare the input vector.
2. Apply the weight matrix.
3. Obtain the output vector.

For example, if the input has 2 values and the output has 3 values, the weight matrix must have a shape that can receive 2 inputs and produce 3 outputs.

\[
\mathbf{x} \in \mathbb{R}^{2}
\]

\[
W \in \mathbb{R}^{2 \times 3}
\]

\[
\mathbf{y} = \mathbf{x}W,\quad \mathbf{y} \in \mathbb{R}^{3}
\]

This can be read as follows.

1. Receive an input represented by 2 values.
2. Change it into an output represented by 3 values.

In two dimensions, this change can be seen in a drawing. The following example shows an input vector \(\mathbf{x} = [2,\ 3]\) multiplied by a simple matrix \(W\), moving to \(\mathbf{y} = [2,\ 4]\).

![Example of matrix multiplication changing a vector position](/AiBook/assets/part-02/chapter-03/matrix-multiplication-position-change-en.svg)

The transformation in the figure keeps the first coordinate and changes the second from 3 to 4.

```text
Input position: [2, 3]
Apply matrix W.
Output position: [2, 4]
```

In actual AI models, this kind of transformation happens in far more dimensions than a 2D picture. So it is hard for a person to draw directly, but the basic way of thinking stays the same. An input representation moves into another representation as it passes through a weight matrix.

This perspective matters in AI. A model does not leave the input representation as it is. It changes it through several stages of calculation into another representation.

1. There is an original input representation.
2. It passes through the first transformation.
3. We obtain an intermediate representation.
4. It passes through the next transformation.
5. It moves toward a representation closer to the final output.

The layers of a neural network can be seen as a structure that stacks these transformations several times. Of course, a real neural network is not made only of linear transformations. Other calculations such as activation functions, normalization, and attention also appear together.

## Checklist

- Can you distinguish matrix multiplication from element-wise multiplication?
- Can you explain weighted sum as a calculation that multiplies input values by weights and adds them?
- Can you read matrix multiplication as a way of calculating several weighted sums at once?
- Can you explain that the length of the input vector must match the input-side size of the weight matrix?
- Can you explain the intuition of batch calculation, where several samples are bundled into a matrix and the same weight matrix is applied?
- Can you explain linear transformation as a calculation that changes an input representation into another output representation?
- Can you explain why matrix multiplication reappears in neural-network layers, embeddings, and classification?
- Can you explain matrix multiplication as the reusable weighted-sum structure of `input -> weight matrix -> output`?

- Can you read input dimension, output dimension, and weight matrix shape together and distinguish matrix multiplication from element-wise multiplication?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
- NumPy Developers, [numpy.matmul](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This official reference supports the shape condition of matrix multiplication and the meaning of the `@` operator.
- Google for Developers, [Neural networks: Nodes and hidden layers](https://developers.google.com/machine-learning/crash-course/neural-networks/nodes-hidden-layers){: target="_blank" rel="noopener noreferrer" }, Machine Learning Crash Course, checked on 2026-07-19. This official educational reference explains that neural-network node values are calculated by summing products of inputs and weights.
