# P2-1.1 What Math Does in AI Computation

> Section ID: `P2-1.1`
> Version: `v2026.07.09`

Part 1 viewed AI on a broad map of rules, models, learning, generation, and service structure. Starting in Part 2, we rebuild the foundations needed to read that map. The first question is how much math you really need in order to relearn AI.

You do not need to prove every theorem. But if you cannot read what mathematical notation is trying to express, you will keep getting stuck on models, data, loss, probability, optimization, and embeddings.

So here, math is not treated as an exam subject. It is treated as a language, structure, and compressed notation for reading AI computation.

## One Shared Scene to Hold First

Chapter 1 keeps reusing one small data scene. Suppose four students studied for the following number of hours and got the following quiz scores.

| Student | Study time `x` | Quiz score `y` |
| --- | --- | --- |
| A | 1 hour | 55 |
| B | 2 hours | 65 |
| C | 3 hours | 80 |
| D | 4 hours | 90 |

This scene returns through several later questions.

- A mean shows the rough center of the scores.
- Looking at `x` and `y` together lets you read an input-output relationship.
- Adding a model turns it into a prediction problem.
- Adding loss lets you express how far a prediction is from the real score.

The important standard is simple: math is the tool that lets you reread a small table like this in the language of means, functions, error, and optimization.

## Scope of This Section

This Section does not explain each math concept deeply. Sigma and limits return in Chapter 2. Vectors return in Chapter 3, derivatives in Chapter 4, probability in Chapter 5, and optimization in Chapter 6.

The first question to settle is: why should AI readers revisit math as a computational language rather than as an exam subject?

So this Section fixes only five places first.

- Math expresses AI model computation compactly.
- Math tells us what shape data should take.
- Math explains what learning is reducing or changing.
- Math has to meet code before it can really be checked.
- Later Chapters make those places more concrete through sigma, vectors, derivatives, probability, and optimization.

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| Math is a computational language, not mainly a test of correct answers | It gives you a starting point even if you cannot derive every formula | Understand that formulas compress computational structure |
| Math explains both the shape of data and the direction of learning | It connects why vectors, matrices, loss, and gradients belong in the same Part | Understand what is being represented and what is being reduced or changed |
| Formulas ultimately have to be checked again through code and results | AI learning does not end with reading formulas alone | Understand that small code confirms what a computation is doing |

## Math Shows Computation in a Compressed Form

In AI documents, math often compresses a long procedure. For example, taking a mean can be described in words: add all the values and divide by the number of values.

\[
\mathrm{mean} = \frac{x_1 + x_2 + \cdots + x_n}{n}
\]

With sigma, the same structure becomes even shorter:

\[
\mathrm{mean} = \frac{1}{n}\sum_{i=1}^{n}x_i
\]

That is what formulas often do in machine learning documents: they shorten repeated calculation, many data points, sums of losses, and products of probabilities into one readable line.

## Math Determines the Shape of Data

AI models do not compute directly on raw sentences, images, or tables. Those are usually converted into arrays, vectors, matrices, and tensors.

That means math also tells us what shape the data has. A vector is a list of values. A matrix arranges values by rows and columns. A tensor can be viewed as an array with more axes.

This matters even for the small study-time and quiz-score table. To humans it is a story. To computation, it is an input vector, an output vector, or a small table. Without that conversion instinct, later terms such as `X`, `y`, `shape`, `feature`, and `target` feel like a new topic.

## Math Explains What Learning Changes

In AI, learning is not a vague process where the system “gets smarter.” It is usually described as adjusting model parameters so loss decreases.

Several math concepts attach to that flow.

- A function expresses how input becomes output.
- A loss function expresses how wrong the model is.
- Derivatives and gradients help find the direction that reduces loss.
- Optimization keeps searching for a better value.
- Probability and statistics handle patterns and error in uncertain data.

Here the point is not to calculate those ideas yet. The point is to fix why they keep appearing in learning explanations.

## Math Has to Be Checked Together with Code

Math notation alone often feels abstract. Code turns that abstract expression into an executable procedure.

```python
import numpy as np

x = np.array([1, 2, 3, 4])
mean = x.mean()

print(mean)
```

Example output:

```text
2.5
```

The point is not advanced library usage. The point is that formulas, data, code, and output are different expressions of the same computation.

1. The formula compresses the structure.
2. The data supplies the values.
3. The code executes the procedure.
4. The result confirms what happened.

## Perspective to Keep from This Section

In AI, math mainly does three jobs.

1. It represents data in forms such as vectors, matrices, and distributions.
2. It compares things such as predictions, targets, distances, and probabilities.
3. It adjusts values by helping us find the direction that reduces loss.

If you keep those three jobs in mind, the math topics in Part 2 stop looking disconnected.

## Short Check

- You can explain that in AI, math is used as a language for reading computational structure.
- You can connect formulas, data, code, and output.
- You can explain that vectors, matrices, and tensors express the computable shape of data.
- You can explain learning as adjusting parameters to reduce loss.
- You can explain why Part 2 revisits linear algebra, derivatives, probability and statistics, and optimization.

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-06-24.
