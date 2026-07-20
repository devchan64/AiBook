# P2-3.1 Scalar, Vector, and Matrix

> Section ID: `P2-3.1`
> Version: `v2026.07.20`

Part 2 Chapter 2 reread mathematical notation. Variables, functions, expressions, sigma, and limits were the basic grammar for reading what a formula is saying. From here, we move to the basic expressions of linear algebra that appear often when AI data is turned into a calculable shape.

1. We look at a single number.
2. We look at a list of values.
3. We look at a table with rows and columns.

These three lead to scalar, vector, and matrix. Here the focus is on building the habit of recognizing what we are seeing when an AI document represents data as one number, a list, or a table.

Here we reorganize `scalar`, `vector`, `matrix`, `shape`, and `array`. If Chapter 2 was about reading the grammar and repeated notation inside one line of mathematics, this chapter is about recognizing what that expression becomes once it unfolds into an actual data shape.

The emphasis here is not the whole mathematical theory, but the basic shapes of AI data. Once scalar, vector, matrix, and shape are separated clearly, questions such as `what is the shape of input X`, `how many rows are samples`, and `how many columns are features` become much easier to read.

| What to fix in this section now | Question that follows immediately | Where it reappears later |
| --- | --- | --- |
| Basic distinction among scalar, vector, and matrix | In P2-3.2, we examine why a vector can be read like a position. | It returns in Part 3 when reading feature vectors and input matrices, and in Parts 5 and 6 when reading embedding vectors and score vectors. |
| The intuition that shape changes the calculation rule | In P2-3.3, we examine matrix multiplication and dimension matching. | It returns in Part 3 when checking the shapes of input matrix `X`, target `y`, and train/test split results. |
| The view that table data is a numeric array | In P2-3.6, it leads into NumPy array calculation. | It returns in Part 3 when reading the flow that turns a dataframe into an array for model input. |

## Core Criteria: Scalar, Vector, and Matrix

- You can explain a scalar as a single number.
- You can explain a vector as an ordered list of values.
- You can explain a matrix as a numeric array with rows and columns.
- You can understand that the shape of data affects the way a calculation works.
- You can explain why text, image, and table data are turned into calculable numeric arrays.
- You can explain why scalar, vector, and matrix return later in embedding, feature, batch, and model calculation.
- You can explain why the basic mathematical operations of scalar, vector, and matrix require shape.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| A scalar is one number | Because it becomes the basic unit for reading single values such as loss, probability, and learning rate. | Understand that one number can represent one calculation result or one configuration value. |
| A vector is an ordered list of values | Because it is the most common shape for representing one object through several features. | Understand that order changes meaning and that several numbers are read as one bundle. |
| A matrix is a table that holds several vectors together | Because row and column structure is needed when calculating several samples and several features at once. | Understand that rows can be read as objects and columns as features, and that shape sets the calculation rule. |

## Why Look at Linear Algebra First

AI models do not calculate directly on real-world sentences, images, sounds, or tables. Most of the time, they turn them into numbers and handle those numbers in the form of arrays.

1. Sentences are turned through tokens into numeric IDs and vectors.
2. Images are turned into arrays that hold pixel values.
3. Table data is read as a matrix or dataframe with a row-and-column structure.

Linear algebra is the basic language for reading these numeric arrays. Before deep proofs, the first thing needed is the intuition captured in the following questions.

1. Is there only one value?
2. Are the values gathered in one line?
3. Are the values arranged into rows and columns?
4. Are several pieces of data bundled together at once?

These questions matter in real code as well. One common reason AI code fails is not misunderstanding the meaning of a value, but misunderstanding its shape.

## A Way of Thinking That Extends from One Number to Space

Scalar, vector, matrix, and position can look like separate concepts, but in AI calculation they form one connected flow.

1. A scalar expresses one value.
2. A vector expresses several values bundled in order.
3. A matrix gathers several vectors into rows and columns.
4. Position is the perspective of comparing vectors like coordinates in the same space.

For example, if we look only at one person’s age, it is a scalar.

\[
30
\]

If we look at age, height, and number of visits together, it becomes a vector.

\[
[30,\ 172,\ 5]
\]

If we collect the vectors of several people, it becomes a matrix.

\[
\begin{bmatrix}
30 & 172 & 5 \\
24 & 165 & 2 \\
41 & 180 & 7
\end{bmatrix}
\]

And if we see each person’s vector as a position in the same space, we can think about how close or far people are from one another.

1. We look at one value.
2. We bundle several values to represent one object.
3. We gather several objects at once.
4. We compare the objects in the same space.

This flow is why linear algebra appears so often in AI. Linear algebra is not only a subject for learning matrix calculation rules. It is a language that lets us build calculable representations of data and compare relationships between those representations.

## A Scalar Is One Number

A scalar is one number. For example, all of the following can be treated as scalars.

\[
3
\]

\[
0.8
\]

\[
-1.2
\]

In AI contexts, scalars appear in many places.

- one temperature value
- one probability
- one loss
- one accuracy
- one learning rate

For example, if the average loss of a model is 0.25, the value itself is a scalar.

\[
\mathrm{loss} = 0.25
\]

A scalar looks small, but it matters. When evaluating a model, we often summarize many calculation results into one number. But one number also compresses a great deal of information. The statement that the loss is 0.25 does not tell us which data the model handled well and which data it got wrong.

## What Changes Mathematically

Scalar, vector, and matrix do not differ only in shape. Mathematically, what changes is `which calculations are possible`.

Because a scalar is one number, we can immediately think of ordinary arithmetic.

\[
2 + 3 = 5
\]

\[
2 \times 3 = 6
\]

Vectors can be added by matching values at the same positions.

\[
[1,\ 2,\ 3] + [4,\ 5,\ 6] = [5,\ 7,\ 9]
\]

If a scalar is multiplied by a vector, the same number is multiplied into each value of the vector.

\[
2[1,\ 2,\ 3] = [2,\ 4,\ 6]
\]

Matrices can also be added position by position when they have the same shape.

\[
\begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
+
\begin{bmatrix}
5 & 6 \\
7 & 8
\end{bmatrix}
=
\begin{bmatrix}
6 & 8 \\
10 & 12
\end{bmatrix}
\]

These are less like advanced linear algebra and more like the rule `calculate by matching the same positions`. This is where shape becomes important. Vectors with different lengths or matrices with different numbers of rows and columns cannot immediately be calculated position by position.

1. If the shape is the same, position-wise calculation is possible.
2. If the shape is different, we first have to decide which values should be combined.

We do not cover matrix multiplication yet. Matrix multiplication is not simple position-wise multiplication. It creates new values by combining rows and columns. That content is handled separately in P2-3.3.

Here we first fix the standard for reading data shape, without going into the full development of vector-space axioms or matrix-multiplication procedures. The position intuition is narrowed again in P2-3.2, and matrix multiplication and linear transformation are narrowed again in P2-3.3.

## A Vector Is a List of Values

A vector can be read as an ordered list of values.

\[
\mathbf{x} = [1,\ 2,\ 3]
\]

Here, \(\mathbf{x}\) is a vector with three values. We do not explain it deeply here as `a mathematical object with direction and magnitude`. In the AI-data perspective, we first read it as `a bundle of several numbers`.

For example, suppose one person is represented by three values: `age: 30`, `height: 172`, and `monthly visits: 5`.

Written as a vector, it looks like this.

\[
\mathbf{x} = [30,\ 172,\ 5]
\]

This vector represents one person’s features as a list of numbers. In machine learning, it is common to gather several features this way and use them as one input.

Order matters in a vector. It must already be fixed whether the first value means age, height, or number of visits.

```text
[30, 172, 5]
-> [age, height, monthly visits]
```

If the order changes, the same numbers mean something different.

```text
[172, 30, 5]
-> [height, age, monthly visits]
```

So a vector is not merely a bunch of numbers. It is a bundle of numbers where each position carries meaning.

## A Matrix Is a Numeric Array with Rows and Columns

A matrix is a structure in which numbers are arranged into rows and columns.

\[
X =
\begin{bmatrix}
1 & 2 & 3 \\
4 & 5 & 6
\end{bmatrix}
\]

This matrix has 2 rows and 3 columns. We usually call it a \(2 \times 3\) matrix. A row is one horizontal line, a column is one vertical line, and shape is the count of rows and columns.

In AI data, one row can be read as one data sample, and one column can be read as one feature.

For example, if we represent the data of 3 people through age, height, and number of visits, we get the following.

\[
X =
\begin{bmatrix}
30 & 172 & 5 \\
24 & 165 & 2 \\
41 & 180 & 7
\end{bmatrix}
\]

In this case there are 3 rows and 3 columns. That means the 3 rows are 3 people, and the 3 columns are age, height, and monthly visits.

This perspective is very important when reading a machine learning dataset. In many beginner materials, \(X\) means the full input data, and \(y\) means the target value or label corresponding to each row.

## Shape Is the Condition of Calculation

Shape is the form of data. It is the information that tells us whether we are looking at one value, a list of values, or an array with rows and columns.

Problem situation: We want to compare at once how scalar, vector, and matrix look in code.
Input: A scalar array, a one-dimensional vector array, and a two-dimensional matrix array.
Expected output: The `shape` of each is printed in order.
Concept to check: Shape is the basic information that distinguishes whether data is one number, a list, or a row-and-column structure.

```python
# This example creates scalars, vectors, and matrices as NumPy arrays and checks their data shapes.
import numpy as np

# scalar, vector, and matrix are three arrays for comparing stored data shape.
scalar = np.array(3)
vector = np.array([1, 2, 3])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

# The shape output makes you read dimension and size before the numeric values.
print(scalar.shape)
print(vector.shape)
print(matrix.shape)
```

This code checks the shape of the three values. The result is read like scalar `()`, vector `(3,)`, and matrix `(2, 3)`.

Depending on the library or settings, the appearance of a scalar can differ slightly, but the core remains the same. A scalar is one number, a vector is a list of numbers, and a matrix is a numeric array with rows and columns.

Shape matters because whether a calculation is possible changes with shape. For example, vectors with different lengths are difficult to add position by position.

\[
[1,\ 2,\ 3] + [4,\ 5]
\]

This expression does not align which values should be added together. In code as well, if the shape does not match, an error can occur or the calculation can proceed in a way you did not intend.

## The Meaning of Rows and Columns Is Decided by the Problem

A matrix is a numeric array, but the meaning of those numbers is decided by the problem definition. Even for the same \(3 \times 3\) matrix, rows may mean people and columns may mean features in table data; rows and columns may represent pixel positions in part of an image; rows may mean tokens and columns may mean embedding dimensions in sentence data; and rows may mean samples and columns may mean features in batch data.

So when reading a matrix, do not look only at the shape of the numbers. Check what a row represents, what a column represents, what unit each value has, and whether the order of rows and columns is fixed.

When you encounter phrases such as `input matrix`, `feature matrix`, or `embedding matrix` in AI documents, first confirm the meaning of the rows and columns.

## Looking Through a Case

### Case 1. One Customer Becomes a Vector and Several Customers Become a Matrix

When a learner looks at a customer data table, it is usually read around people, such as name, age, and number of visits. But once that table is turned into model input, several attributes of one person begin to be read as one vector, and several people’s vectors begin to stack as one matrix.

For example, if one customer is represented by the three numbers `age`, `monthly visits`, and `average purchase amount`, that becomes a vector of length 3. If five customers are gathered in the same way, the result is a `5 x 3` matrix. At that point, a row means one customer and a column means one type of feature.

This case shows why scalar, vector, and matrix are learned separately. When you look only at one number, a scalar is enough. When one object is expressed through several values, a vector is needed. When several objects must be calculated together, a matrix is needed.

So an introduction to linear algebra is closer to learning `how to fold real-world data into a calculable shape` than to memorizing abstract symbols. Without this intuition, it becomes difficult to read later concepts such as feature matrices, batch inputs, and embeddings in the same language.

## Where Scalar, Vector, and Matrix Reappear

Scalar, vector, and matrix reappear in almost every later explanation of AI calculation.

- embedding: text or items are represented as vectors
- feature: one data sample is represented as a vector of several values
- batch: several samples are grouped into a matrix or a higher-dimensional array
- loss: several calculation results may be summarized into one scalar
- model parameter: weights can take the form of vectors or matrices
- matrix multiplication: it becomes the basic tool for calculating many inputs and weights at once

We still do not calculate matrix multiplication here. For now, we only fix the intuition that AI data is often represented as one number, a list of numbers, or a table of numbers.

## A Simple Reading Example

Suppose we have the following data.

\[
X =
\begin{bmatrix}
2 & 8 \\
4 & 6 \\
5 & 9
\end{bmatrix}
\]

Assume that in this matrix, each row means a student and the columns mean `[study time, quiz score]`.

Then this matrix means that the first student has study time 2 and quiz score 8, the second student has study time 4 and quiz score 6, and the third student has study time 5 and quiz score 9.

Here, the data for one student is a vector.

\[
\mathbf{x}_1 = [2,\ 8]
\]

If we gather the data of all three students, it becomes a matrix.

\[
X =
\begin{bmatrix}
\mathbf{x}_1 \\
\mathbf{x}_2 \\
\mathbf{x}_3
\end{bmatrix}
\]

What matters in this example is not the calculation but the reading method. One value is a scalar, one student’s bundle of features is a vector, and several students’ bundles of features are a matrix.

## Checklist

- Can you explain a scalar as one number?
- Can you explain a vector as an ordered list of values?
- Can you explain a matrix as a numeric array with rows and columns?
- Can you explain that shape can affect whether a calculation is possible and whether an error occurs?
- Can you explain that the meaning of rows and columns depends on the problem definition?
- Can you read one sample as a vector and several samples as a matrix?
- Can you explain why scalar, vector, and matrix reappear in embedding, feature, batch, loss, and parameters?
- Can you explain that vectors and matrices with the same shape can be added position by position, and that scalar multiplication multiplies the same number into each value?
- Can you explain the flow of thinking that extends from scalar to vector, matrix, and position comparison?
- Can you explain scalar, vector, and matrix both as linear algebra terms and as the language for reading data shape?
- When the shape of `X`, the number of samples, and the number of features become mixed up, can you separate them again through shape intuition?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked 2026-07-19.
- NumPy Developers, [numpy.ndarray.shape](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This official reference supports reading `shape` as array dimension information and checking it in code.
- scikit-learn developers, [Glossary of Common Terms and API Elements](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }, scikit-learn User Guide, checked on 2026-07-19. This is a reference for the convention of reading `X` as an input data matrix and `y` as the target.
