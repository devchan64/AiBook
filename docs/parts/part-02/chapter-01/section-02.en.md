# P2-1.2 Where Formulas, Code, and Data Meet

> Section ID: `P2-1.2`
> Version: `v2026.07.12`

In P2-1.1, we treated mathematics as the language for reading AI computation. Now we look at where that language actually sits in real learning. When studying AI, formulas, code, and data are not separate things. They are closer to three faces that show the same computation in different ways.

1. A formula compresses the computational structure.
2. Code executes the computational procedure.
3. Data provides the target of the computation and the result to inspect.

This section shows the structure that formulas, code, and data can all point to the same calculation.

Later, even when you read formulas for means, vectors, loss, and gradients, you should be able to read together `to what data this expression is applied` and `where it is executed in code`.

Here, we organize together `formula`, `code`, `data`, `output`, and `shape`. If 1.1 first fixed why mathematics should be read as a computational language, here we organize how that computational language points to the same calculation inside `documents, code cells, and real values`.

## One Shared Scene to Hold First

We bring over the same small table from the previous section.

| Student | Study time `x` | Quiz score `y` |
| --- | --- | --- |
| A | 1 hour | 55 |
| B | 2 hours | 65 |
| C | 3 hours | 80 |
| D | 4 hours | 90 |

This table can be used as the smallest scene in Chapter 1 where formulas, code, and data meet.

- As data, it is a small table with two columns, `x` and `y`.
- As a formula, it is material for writing a mean, a function, and an error.
- As code, it is an input that can be translated into lists, arrays, and variables.

What the reader easily misses here is that `table`, `formula`, and `code` can look like different study topics. But in practice, they are only different surfaces for reading the same scene. The purpose of this section is to fix that correspondence.

## Scope of This Section

This section does not explain the entire notation system of formulas. Variables, functions, sigma, and limits return in Part 2 Chapter 2. Vectors, matrices, and arrays are examined in more detail in Part 2 Chapter 3 and Part 2 Chapter 11.

The question to solve right now is this: `When a formula from a document comes down into a code cell and real data, what remains the same and what changes only in form?`

So this section first fixes only the following four places.

- What is the formula saying?
- How does code execute that formula?
- In what shape does data enter the formula and code?
- How should the result be interpreted again afterward?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| formula | a compressed expression of computational structure | the blueprint inside the document |
| code | a procedure that actually executes the computation | the unfolded execution surface of the formula |
| data | the values and shape that go into the computation | the material and the object to verify |
| output | the result obtained after computation | the observation point that still needs interpretation |
| shape | information about an array's dimensions and lengths | the basic clue for reading computable form |

If the previous section asked `why mathematics should be reread as a computational language`, here we read how that computational language points to the same computation inside documents, code, and data. In later sections on sigma, vectors, arrays, and loss, this connection splits more concretely into particular notations and code patterns.

This section sets the standard for why Part 2 looks at formulas and Python together. The details of individual symbols and array computation are recovered in later sections.

The flow after this section is also simple.

- In Chapter 2, we read more directly the variables, functions, and sigma inside formulas.
- In Chapter 3 and Chapter 11, we look at how data shape continues into vector, array, and table computation.
- In Part 3 and Part 4, this sense of connection is used to read model inputs, prediction, loss, and metrics.

## Goals of This Section

- You can read a formula as a compressed expression of computation.
- You can view code as the translation of that formula into an executable procedure.
- You can view data as both the values fed into the computation and the results that must be checked afterward.
- You can explain one small mean computation from the viewpoints of formula, code, and data.
- You prepare to move back and forth between formula notation and Python practice in later sections.

## Three Criteria

This section shows the place where mathematics and programming meet. The three viewpoints that act as standards while reading are the following.

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| The same computation can look different as `formula`, `code`, and `data` | This gives you the sense that you are still reading the same content even when the expression changes. | Understand that one mean can be explained in three ways. |
| A formula `compresses computational structure`, while code `unfolds execution order` | This explains why a document and example code look different from one another. | Understand what gets added and divided, and in what order it is executed in code. |
| The result must still be `reinterpreted in context`, not just read as a number | This connects directly to how loss and metrics will later be read. | Understand that you can explain in one sentence what a mean such as 72.5 means. |

## One Calculation Seen in Three Ways

Take the mean as the simplest example. A mean is the calculation that adds several values and divides by the count.

If you pull out only the score column from the table above, the data becomes `55, 65, 80, 90`.

Written as a formula, it becomes the following.

\[
\mathrm{mean} = \frac{55 + 65 + 80 + 90}{4}
\]

Written as code, it becomes the following.

Problem situation:

- even for the same mean calculation, once you move from a formula to code, you may not immediately connect what execution order it unfolds into

Input:

- the list of values `scores = [55, 65, 80, 90]`

Expected output:

- the mean value `72.5`

Concept to check:

- `sum(scores) / len(scores)` in code is the mean formula written out as an execution order
- even if formula, code, and data look different, they can point to the same calculation

```python
scores = [55, 65, 80, 90]
mean = sum(scores) / len(scores)

print(mean)
```

Example execution result:

```text
72.5
```

The three expressions look different, but they do the same thing.

- data: the score bundle `55, 65, 80, 90`
- formula: the compressed structure that adds the values and divides by the count
- code: the actual execution procedure the computer follows
- output: the value checked after the computation ends

This viewpoint matters. In AI documents, a formula alone can look abstract. Code alone can look like only library usage. Data alone can look like only a list of numbers. Only when the three are connected does it become visible `what is being computed`.

This example is useful because the same table can later be reread through different questions. Mean score is one summary value, the relationship between `x` and `y` is a problem of function and prediction, and the gap between predicted and real values is a problem of loss. In other words, one data scene becomes the reference point that ties together many explanations in Chapter 1.

## Formulas Give Names and Compress Relationships

The first thing to read in a formula is not the exact shape of the symbols, but the names and relationship.

\[
y = f(x)
\]

This expression does not look complicated, but it is one of the most important basic structures in AI documents.

- `x`: the input
- `f`: the function or model that turns input into output
- `y`: the output

In a machine-learning context, you can read this as `input data x passes through the model f and becomes output y`.

If you attach it directly to the table above, `x` is study time and `y` is score. Even before there is a complex model, the thought experiment "a function that predicts a score from study time" is enough to fix the input-transformation-output structure.

In code, it may appear as the following.

Problem situation:

- even if you can read the formula `y = f(x)`, you may not immediately feel how it appears in real code

Input:

- the input value `x`
- the model or function `model` that turns input into output

Output:

- the execution result `y`

Concept to check:

- the input-transformation-output relationship of the formula is expressed with the same structure in code
- the goal of this example is reading relationship expression rather than carrying out a complex calculation

```python
y = model(x)
```

The formula and the code do not use exactly the same grammar. But both show the same relationship: input becomes output through some transformation. Once you can read that relationship, it becomes easier to place the later ideas of model, prediction, loss, and learning.

## Data Enters in a Computable Shape

Real-world data is usually not computed on immediately as it is. Sentences, images, tables, and logs first become computable values.

For example, the sentence `"I am studying AI again"` can become tokens, numeric IDs, and vectors. An image can continue into pixels, a numeric array, and a tensor. Table data can enter in the form of an array, matrix, or DataFrame based on rows and columns.

At that point, the shape of the data becomes important. Whether there is one value, a list of values, a table with rows and columns, or an array with multiple axes changes the formula and the code that will be used.

Problem situation:

- even with the same numbers, one value, a vector, and a matrix are treated as different shapes in computation

Input:

- the scalar-like array `one_value`
- the one-dimensional array `vector`
- the two-dimensional array `matrix`

Expected output:

- the `shape` of each array

Concept to check:

- data shape is the basic information that distinguishes computable structure
- NumPy shows that even the same numbers are separated by axis and dimension

```python
import numpy as np

one_value = np.array(3)
vector = np.array([1, 2, 3])
matrix = np.array([[1, 2, 3], [4, 5, 6]])

print(one_value.shape)
print(vector.shape)
print(matrix.shape)
```

Example execution result:

```text
()
(3,)
(2, 3)
```

This example is not for learning deep NumPy usage. It is for checking that, even with the same numbers, the meaning of the computation changes depending on the shape in which they are stored.

The study-time and score table above is the same. If you look only at the score column, it can be treated like a one-dimensional vector. But if you look at `x` and `y` together, it becomes a table structure with two columns. The later reasons for separating `X` and `y` or checking `shape` also ultimately come from turning `what kind of question this data is for` into a computable form.

## Code Turns a Formula into an Executable Procedure

A formula shows the computational structure briefly, but real execution needs code. For example, a mean is simple as a formula.

\[
\mathrm{mean} = \frac{\sum_{i=1}^{n}x_i}{n}
\]

But in code, you must decide where the data is, how many items there are, by what function they will be added, and where the result will be stored.

Problem situation:

- a mean formula with sigma is short, but in code the computation steps may need to be written in a finer-grained way

Input:

- the score list `scores = [55, 65, 80, 90]`

Output:

- the count `n`
- the total `total`
- the mean `mean`

Concept to check:

- in code, one line of a formula can unfold into several intermediate variables and execution stages
- not only the final result but also intermediate variables become observation points that help interpret the formula

```python
scores = [55, 65, 80, 90]
n = len(scores)
total = sum(scores)
mean = total / n

print(n)
print(total)
print(mean)
```

Example execution result:

```text
4
290
72.5
```

Code can become longer than a formula. But code reveals the execution order. It prepares the values, counts them, adds them, divides by the count, and finally stores the result. If you look at `4`, `290`, and `72.5` in order, you can immediately check into what intermediate stages a one-line sigma formula unfolds in code.

Push the same scene a bit further, and later you start storing it as `study_hours = [1, 2, 3, 4]` and `quiz_scores = [55, 65, 80, 90]`, separating input and output. From there, you naturally move from mean computation alone into model computation that describes a relationship.

The same thing happens in AI learning. In a paper or textbook, a loss function may appear as a short formula, but in real code the sequence unfolds into many lines: data loading, preprocessing, model execution, loss computation, and parameter update.

## Results Must Be Interpreted Again

Understanding does not end just because a calculation is over. The output still has to be interpreted again in the context of the problem.

If the mean is 72.5, that means the center of the four students' scores lies roughly around 72.5 points.

The same is true in machine learning.

If loss is 0.2, it means that when the gap between model output and reference was computed in some specific way, the result was 0.2.

If accuracy is 90%, it means that 90% of the evaluation data were predicted correctly. But which cases were wrong must still be checked separately.

A numeric result does not automatically become meaning. You must check together what data it came from, by what formula it was computed, and what code was executed.

## Connecting It to a Small Learning Flow

If you shrink AI learning as much as possible, you can read it as the flow of preparing data, feeding it into a model, obtaining an output, comparing it with a reference to compute loss, adjusting parameters, and repeating this process.

This is exactly the place where formula, code, and data all enter together.

- data provides the input and target
- formula expresses the model output, loss, and update direction
- code executes this calculation in real order
- results are checked as metrics, loss, and prediction

This is why Part 2 handles mathematics and Python together. If you see only formulas, execution does not appear. If you see only code, the intention of the computation can become blurry. If you see only data, it is hard to see what the model is learning.

## Case Study

### Case 1. Even One Mean Calculation Can Leave Formula, Code, and Data Disconnected

Suppose a learner feels they understand the formula for a mean, but when they move to a code cell cannot immediately connect why `sum(scores) / len(scores)` appears. On the other hand, if they see only code, they may carry out the computation but miss why the values are added and divided in that order.

At that point, if you place the actual data `55, 65, 80, 90` in front of you, the three expressions meet in one place. Data is the object of the computation. The formula compresses the structure `add them all and divide by the count`. The code unfolds that structure into the real execution order. The output `72.5` then makes you interpret again where the center of the original scores lies.

This case shows why Part 2 does not separate formulas from Python. Only when you can move across one calculation in these three ways can later vectors, matrices, loss, and probability calculations be read with the sense that `the expression is different, but the structure is the same`.

So the mean example is not just a simple arithmetic exercise. It is a reduced version of the basic frame for reading all of AI learning. Formula handles the structure of the computation, code handles the execution procedure, and data handles the material of the computation and the thing to be interpreted afterward. This distinction of places continues directly into vectors, matrices, loss, and probability calculations in later chapters.

## Checklist

- Can you explain that formula, code, and data can express the same computation in different ways?
- Can you read `y = f(x)` as the relationship among input, function, and output?
- Can you explain that the shape of data affects the way a computation is carried out?
- Can you explain that code turns a formula into an executable procedure?
- Can you explain that output must be interpreted together with data, formula, code, and problem context?
- Can you explain the flow that mathematics is checked through code, code is verified with data, and the result is interpreted again by returning to the formula and problem definition?
- When formula, code, and data start looking separated, can you tie them back together as different expressions of the same computation?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-06-24.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked on 2026-06-24.
