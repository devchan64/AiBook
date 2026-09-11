# P2-2.4 Why Do Log and Exp Keep Reappearing?

> Section ID: `P2-2.4`
> Version: `v2026.09.08`

Machine learning and deep learning formulas often contain expressions such as `log`, `exp`, and `e^x`. These describe how quickly values grow or shrink, how multiplicative relationships can be read as additive ones, and how to handle probability-like scores.

Logarithms and exponentials are used in logistic regression, [log loss](/AiBook/en/reference/concept-glossary-alpha/l/#log-loss), and softmax calculations.

## Exponential and Logarithmic Calculations

| Expression | Meaning of the calculation | Example uses |
| --- | --- | --- |
| `exp(2) \approx 7.39` | A calculation that spreads score 2 into a larger weight | `sigmoid`, `softmax` |
| `log(exp(2)) = 2` | Reading a value sent into exponential space back on the original axis | logit, log-odds |
| `0.9 x 0.8 x 0.7 = 0.504` | Directly multiplying probabilities makes the value shrink quickly | likelihood, joint probability |
| `log(0.9) + log(0.8) + log(0.7)` | Rereading multiplication as addition | log loss, log-likelihood |

So logs and exponentials are not separate mathematical decoration. They are the language that makes calculations easier to read when moving from `score -> ratio -> probability-like value -> loss`.

## Equal Amounts and Equal Ratios

If addition makes it easier to see `whether the same amount is added again and again`, an exponential can be read as making it easier to see `whether something keeps growing or shrinking by the same ratio`.

\[
e^x
\]

This notation is an exponential function with base `e`. The important point here is that even if `x` grows only a little, the value grows faster in a way that differs from linear growth.

For example, when `x` increases to 1, 2, and 3:

- `x` itself grows linearly by 1 each time.
- `e^x` grows by the same factor, `e`, each time, so the amount added becomes larger.

So exponentials appear often when we need to read `a structure where a small difference widens into a much larger difference as we move further along`.

The contrast becomes clearer if we place change by adding the same amount next to change by growing at the same ratio.

| Step | Linear growth example: always `+10` | Ratio growth example: always `x1.1` |
| --- | --- | --- |
| Start | 100 | 100 |
| After 1 step | 110 | 110 |
| After 2 steps | 120 | 121 |
| After 3 steps | 130 | 133.1 |

At first the two changes may look similar, but as the number of steps increases, ratio growth speeds up more and more. An exponential function is exactly the language for this kind of ratio change.

## Inverse Relationship Between Exp and Log

Here, `log` is the natural logarithm, with base `e`. A logarithm asks in reverse which input to the exponential function would produce this value.

\[
\log(x)
\]

When you see this, you can think of it as reading back `which exponential input produced x`.

For example:

- `exp(2)` is `e^2`.
- `log(e^2)` returns to 2.

So logs and exponentials are functions that move in opposite directions.

| Forward reading | Reverse reading |
| --- | --- |
| `exp(x)` | `log(x)` |
| `How much does it grow by ratio?` | `What value on the exponential side produced it?` |

Substituting 0 and 1 into exponentials and logarithms gives the following relationships.

| Expression | How to read it |
| --- | --- |
| `exp(0) = 1` | If the exponential-side input is 0, it returns to the reference size 1. |
| `log(1) = 0` | We can read 1 as the reference point before exponential change has been applied. |
| `log(exp(x)) = x` | Log returns a value sent into exponential space back to the original axis. |

## Logarithms of Products and Sums of Logarithms

Logs are used often because they change the calculation structure into a form that is easier to read.

- Multiplication is read like addition in log space.
- Division is read like subtraction in log space.

Adding log probabilities instead of multiplying small probabilities directly can reduce the risk that the product becomes too small for the computer to represent.

For example, suppose we multiply three probabilities.

\[
0.9 \times 0.8 \times 0.7 = 0.504
\]

If more values are added, this kind of product shrinks quickly. But once we take a log, the product is reread as a `sum`.

\[
\log(0.9 \times 0.8 \times 0.7)
=
\log(0.9) + \log(0.8) + \log(0.7)
\]

After changing it this way, we can separate and inspect the contribution of several terms more easily. That is why, in machine learning, scenes that read a value as loss or score after taking a log appear more often than scenes that multiply probabilities directly.

| Scene you are looking at now | Question to ask first |
| --- | --- |
| A value grows step by step like `x1.1`, `x1.2` | Is this growth by the same amount or by the same ratio? |
| Several small probabilities keep being multiplied | Does the value become too small and hard to read? |
| A score is being turned into something like a probability | Does an exponential first enlarge the relative weight? |
| A wrong probability prediction is punished strongly | Does a log read the probability gap more sensitively? |

## Score Normalization and Log Loss

To compare scores as probabilities, their range and sum need to be adjusted.

1. First compute a score.
2. Then turn that score with an exponential function or read it with log loss.
3. Then compare the result like a probability or bundle it as loss.

For example, if two candidates have scores `2` and `1`, the score difference is `1`, but that is not yet a probability. If we take the exponential here:

\[
e^2 \approx 7.39,\quad e^1 \approx 2.72
\]

Dividing each value by their sum gives approximately `0.731` and `0.269`, ratios that sum to 1. This is the result of applying softmax to the two scores.

If we rewrite that scene more briefly as a table, it looks like this.

| Step | Calculation | What it reads |
| --- | --- | --- |
| Original score | `2`, `1` | Still a simple score, not yet a probability |
| Apply exponential | `exp(2) \approx 7.39`, `exp(1) \approx 2.72` | Gives a larger weight to the larger score |
| Normalize by the sum | `7.39 / (7.39 + 2.72)` | A ratio of approximately `0.731` |

On the other hand, if we read with a log the case where the correct probability is predicted well as `0.9` and the case where it is predicted badly as `0.1`, the wrong one receives a much larger penalty. This is why log loss punishes `predictions that are wrong but confident` more strongly.

Using the same standard, if we look at `-log(p)`:

| Correct probability `p` | Value of `-log(p)` |
| --- | --- |
| `0.9` | Approximately `0.105` |
| `0.5` | Approximately `0.693` |
| `0.1` | Approximately `2.303` |

So log loss works in the direction of punishing `predictions that are wrong even though the model was confident` more strongly.

Logs and exponentials are the language that makes calculations easier to read when moving between score, probability, and loss.

## Checklist

- Can you read `exp(x)` as a power of `e`?
- Can you explain why `log(x)` reads an exponential backward?
- Can you state the difference between increase by the same amount and increase by the same ratio?
- Can you explain why taking a log makes several multiplied probabilities easier to read?
- Can you explain why logs and exponentials reappear in `softmax` and `log loss`?
- Can you connect exponentials and logs as `same-ratio increase`, `a way to reread multiplication as addition`, and `the calculation that turns scores into probabilities and loss`?

## Sources and References

- Python Software Foundation, `math — Mathematical functions`, Python 3 documentation. Because it lets us directly check the basic meaning of `math.exp` and `math.log`, it supports the minimum standard in this section for rereading exponentials and logarithms as calculation language. [https://docs.python.org/3/library/math.html](https://docs.python.org/3/library/math.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-09-08
- Google for Developers, `Machine Learning Glossary`. Because it lets us check key later-Part terms such as `log loss`, `softmax`, and `sigmoid` together, it serves as a reference point for seeing why logs and exponentials keep reappearing as the language for interpreting machine learning scores. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-09-08
- OpenStax, [Calculus Volume 1, 6.8 Exponential Growth and Decay](https://openstax.org/books/calculus-volume-1/pages/6-8-exponential-growth-and-decay){: target="_blank" rel="noopener noreferrer" }, Rice University, checked on 2026-07-19. This reference supports reading exponentials as same-ratio change.
- OpenStax, [Calculus Volume 1, 1.5 Exponential and Logarithmic Functions](https://openstax.org/books/calculus-volume-1/pages/1-5-exponential-and-logarithmic-functions){: target="_blank" rel="noopener noreferrer" }, Rice University, checked on 2026-07-19. This reference supports the inverse relationship between logarithms and exponentials and the product-to-sum property of logarithms.
