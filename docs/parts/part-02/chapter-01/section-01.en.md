# P2-1.1 What Math Does in AI Computation

> Section ID: `P2-1.1`
> Version: `v2026.09.08`

In Part 1, we viewed AI on a broad map of rules, models, learning, generation, and service structure. Starting in Part 2, we recover the foundations needed to read that map. The first question is how much math you need in order to relearn AI.

The answer in this section is not simple. You do not need to prove all the mathematics. But if you cannot read at all what mathematical notation is trying to express, you keep getting blocked whenever you read models, data, loss, probability, optimization, and embeddings.

So here, mathematics is not treated as an exam subject for getting the right answer. It is treated as a language, structure, and compressed notation for reading AI computation.

The reason to revisit mathematics here is closer to `recovering literacy for reading expressions such as X, y, loss, and metric in Part 3 and Part 4` than to `solving problems to prepare for a test`. Once this standard is in place, it also becomes easier to read why vectors, derivatives, probability, and optimization are grouped into one part later on.

Here, we reorganize again the `role of math`, `computational language`, `compressed notation`, `loss`, and `optimization`. Before later sections and later chapters fully separate individual symbols and math topics, this section first clarifies `why mathematics must be reread as part of AI computational literacy`.

## A Shared Example to Start With

Chapter 1 keeps reusing one small data scene. Suppose the study hours and quiz scores of four students are as follows.

| Student | Study time `x` | Quiz score `y` |
| --- | --- | --- |
| A | 1 hour | 55 |
| B | 2 hours | 65 |
| C | 3 hours | 80 |
| D | 4 hours | 90 |

This scene reappears later through several questions.

- If you compute the mean, you can see roughly where the center of the scores lies.
- If you look at `x` and `y` together, you can read the relationship between input and output.
- If you attach a model, you can turn the scene into a prediction problem: "How does the score change as study time increases?"
- If you attach loss, you can calculate with a number how different the prediction is from the real score.

So here, mathematics is not a separate subject for learning difficult symbols. It is a tool that makes you reread a small table like this in the language of `mean`, `function`, `error`, and `optimization`. If a reader is not to get lost later when meeting sigma, vectors, and derivatives, they first need the standard that `math is ultimately a language for reading, comparing, and adjusting data like this`.

## Core Criteria: What Math Does in AI Computation

- You can explain why math is needed in AI from the viewpoint of expression and computation rather than proof.
- You can treat a formula not as something merely to memorize, but as something to recheck through code and data.
- You can explain what purpose each math topic in Part 2 serves.
- You can reduce the burden of "not knowing math," while also understanding the limits that appear if mathematical notation is skipped entirely.

## Three Criteria

What is needed first here is not proof, but a distinction of roles.

| Criterion | Why It Matters |
| --- | --- |
| Math is a `computational language`, not a `test of correct answers` | This gives you a starting point for reading documents even if you cannot solve every formula. |
| Math explains the `shape of data` and the `direction of learning` | This explains why vectors, matrices, loss, and gradients appear in the same part. |
| Formulas must ultimately be checked again through `code and results` | In AI learning, reading formulas alone is not the end. |

## Math Shows Computation in Compressed Form

In AI documents, mathematics compresses a long computational procedure. For example, when there are many data values, the idea of taking a mean can also be explained in everyday language. If you expand the procedure into words, you add all the values and divide that sum by the number of values.

A formula writes that procedure more briefly.

\[
\mathrm{mean} = \frac{x_1 + x_2 + \cdots + x_n}{n}
\]

With sigma, it becomes even more compressed.

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

Here, `x_i` represents each data value, and `n` represents the number of values. Even when the values or their number change, the rule remains the same: `add all the values, then divide by their number`. A formula compresses a rule that applies across many cases. When people share the meanings of the symbols, they can communicate and check the same calculation rule even when working with different data. Mathematical notation becomes a tool for communicating generalized calculation rules.

You can unpack a formula by asking the following questions.

- What does it take as input?
- What does it add or compare?
- What is it trying to reduce or increase?
- Which variable represents the result in code?

If you return to the study-time and quiz-score table above, the mean score is the computation that adds `55, 65, 80, 90` and divides by the number of students. The formula writes that repetition briefly, and the code in a later section unfolds it into an actual procedure. What the reader should hold here is not the symbol itself, but `the repeated structure that handles many values at once`.

## Math Determines the Shape of Data

AI models do not handle raw sentences, images, sounds, and tables directly. These inputs are usually transformed into computable forms such as arrays, vectors, matrices, and tensors.

A sentence can be transformed into tokens, numeric IDs, and vectors. An image can become a pixel-value array and a tensor. Tabular data can become a matrix or DataFrame with rows and columns.

Here, mathematics explains `what shape this data has`. A vector is a list of values. A matrix is a structure that arranges values by rows and columns. A tensor can be viewed as an array with more axes.

This viewpoint is important when rereading embeddings and vector search from Part 1. The phrase "express text as a vector" does not mean a person writes semantic coordinates directly. It means transforming text into a representation inside a numerical space so that a model and search system can compute on it.

If you apply the same standard to the table above, the `x` column and `y` column are also just lists of numbers in the end. To a human, they look like the story of `study time` and `score`, but a model reads them as an `input vector` and `output vector`, or as a small table of data. Without this sense of transformation, later terms such as `X`, `y`, `shape`, `feature`, and `target` feel like a completely new topic.

## Math Explains What Learning Changes

In AI, learning is not vaguely "the process of getting smarter." It is usually explained as the process of adjusting model parameters so that loss decreases. If you unfold this flow in order, input data enters, the model produces output, the output is compared with a reference to compute loss, and then the parameters are adjusted in the direction that reduces that loss. This is repeated again and again.

Several math concepts attach to this flow.

- function: expresses the relationship that turns input into output
- loss function: expresses with a number how wrong the model is
- derivative and gradient: find the direction in which changing values reduces loss
- optimization: repeatedly search for a better value
- probability and statistics: handle patterns and error in uncertain data

Here, rather than computing these concepts directly, we first organize why they keep appearing in AI learning explanations.

Suppose you attach a very simple line to the study-time and score table. If the model predicts "How many points would appear after 1 hour of study?" and the difference from the real score is large, then the loss becomes large. Learning is the process of changing the slope and position of that line little by little in the direction that reduces the difference. In this one short scene, input, output, prediction, error, loss, and optimization all appear together.

## Math Has to Be Checked Together with Code

When you read only mathematical notation, it feels abstract. Code turns that abstract expression into an executable procedure. In particular, array-computation tools such as NumPy let you check vector and matrix computation directly in code.

Problem situation:

- even a familiar math concept such as the mean can feel abstract if you see only the formula

Input:

- the numeric array `x = [1, 2, 3, 4]`

Expected output:

- the mean value `2.5`

Concept to check:

- the mean calculation written in a formula can be executed in code with the same meaning
- a small array example is the simplest starting point for connecting mathematical notation with actual computational results

```python
# This example stores study-hour data in a NumPy array and checks the input values used for the mean.
import numpy as np

# x is the small numeric array used to check the mean.
x = np.array([1, 2, 3, 4])

# mean is the representative average value of the values in x.
mean = x.mean()

print(mean)
```

Example execution result:

```text
2.5
```

This code checks the mathematical concept of a mean using small data. The key point here is not advanced library usage, but that formula, data, and code all express the same computation in different ways. The moment the reader sees `2.5`, they can see directly that the mean has returned from an abstract symbol to an actual value.

1. A formula shows the structure of the computation in compressed form.
2. Data provides the values that become the subject of the computation.
3. Code executes the computation in practice.
4. The result lets you check what the computation actually did.

Part 2 keeps connecting these four things. Mathematics is not left alone as "theory that must be understood," but is rechecked through small code and data.

## A Math Path for Reading AI Computation

Part 2 follows a sequence for rebuilding the math needed to read AI computation, rather than for exploring mathematical proofs in depth.

- **formula notation**: reread variables, functions, expressions, sigma, and limits
- **linear algebra**: view scalars, vectors, matrices, and matrix multiplication from the viewpoint of data representation
- **derivatives and gradients**: view rate of change, slope, and gradient as the language of learning direction
- **probability and statistics**: view uncertainty, distribution, mean, variance, and sample as the language of data interpretation
- **optimization**: view it as the method of repeatedly finding values that reduce loss
- **Python and NumPy**: check how formulas become executable code

This order is not "finish mathematics first, then go to AI." It is the order that builds the minimum path by which mathematical notation encountered while reading AI documents can be reused again.

## How to Reduce the Burden of “Not Knowing Math”

Most math learned a long time ago becomes blurred in memory. In particular, expressions such as limits, sigma, derivatives, and matrices may sound familiar in name, but their actual use may not return immediately. Here, that is not treated as failure.

Still, the following two points are distinguished.

1. Not understanding every proof is allowed in Part 2.
2. On the other hand, if you cannot read at all what a formula is trying to compute, then you will keep getting blocked when reading machine learning and deep learning.

So the goal is not to become a fully trained mathematician. The goal is to become able to read `which part of data, model, loss, and learning this formula is explaining`.

## A Loss Function Compresses the Differences Between Predictions and Actual Values

Take the two students with actual scores of `55` and `65` from the study-time and quiz-score table above. Suppose the model predicts a score of `60` for both students.

| Student | Actual score | Predicted score | Predicted − actual | Squared difference |
| --- | --- | --- | --- | --- |
| A | 55 | 60 | 5 | 25 |
| B | 65 | 60 | −5 | 25 |

Adding the differences directly gives `5 + (−5) = 0`. Both predictions are off by 5 points, yet the sum makes it look as though there is no difference. Squaring each difference gives `25 + 25 = 50`, so the positive and negative differences no longer cancel out. Dividing by the number of students, 2, gives `25`. In this example, we use this average of the squared differences as the loss.

The following formula compresses this calculation.

\[
L = \frac{1}{n}\sum_{i=1}^{n}(\hat{y}_i-y_i)^2
\]

`y_i` is one student's actual score, and \(\hat{y}_i\) is the predicted score for that student. `n` is the number of students, and `L` is the loss. \(\sum\) means to add the values calculated for all the students. The formula therefore adds the last column of the table and divides by the number of students. Substituting the values above gives `L = (25 + 25) / 2 = 25`.

Now suppose that after adjusting the model, its predictions change to `56` and `64`. Using the same rule, the loss is `(1² + (−1)²) / 2 = 1`. This is smaller than the original `25`, so for these two students, we can say that the predictions after the adjustment are closer to the actual scores.

The same formula applies when there are more students or different scores. Sharing this formula as the calculation rule allows another person to calculate the loss from the same data and predictions and compare the model before and after an adjustment.

## Checklist

- You can explain that in AI, mathematics is used as a language for reading computational structure rather than mainly as proof.
- You can connect formula, data, code, and output together.
- You can explain that vectors, matrices, and tensors express the computable shape of data.
- You can explain learning as the process of adjusting parameters to reduce loss.
- You can explain why Part 2 revisits linear algebra, derivatives, probability and statistics, and optimization.
- You can explain Part 2 through the flow that mathematics in AI does the three jobs of `representation`, `comparison`, and `adjustment`.
- You can explain why sigma, vectors and matrices, derivatives, and probability and statistics reappear together in one part.

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-07-19.
- Catherine F. Higham, Desmond J. Higham, [Deep Learning: An Introduction for Applied Mathematicians](https://arxiv.org/abs/1801.05894){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, checked on 2026-07-19.
- Charles R. Harris et al., [Array Programming with NumPy](https://arxiv.org/abs/2006.10256){: target="_blank" rel="noopener noreferrer" }, Nature, 2020, checked on 2026-07-19.
- NumPy Developers, [numpy.mean](https://numpy.org/doc/stable/reference/generated/numpy.mean.html){: target="_blank" rel="noopener noreferrer" }, NumPy User Guide, checked on 2026-07-19. This is the direct reference for checking the mean example in code.
