# P2-2.4 Why Do Log and Exp Keep Reappearing?

> Section ID: `P2-2.4`
> Version: `v2026.07.12`

After reconnecting limits, one more kind of notation still tends to block later machine learning and deep learning explanations: expressions such as `log`, `exp`, and `e^x`. These are not separate pieces of advanced mathematical decoration. They keep appearing when we explain `how fast a value grows or shrinks`, `how a multiplicative relationship can be reread as an additive one`, and `how to handle a score that behaves like a probability`.

Here we reconnect logarithms and exponentials as the minimum calculation language needed to read `logistic regression`, `log loss`, and `softmax`. When you want to recheck the terms quickly, also refer to the [concept glossary](../../../reference/concept-glossary.md).

## Scope of This Section

This section does not cover the full formal theory of logarithms and exponentials. Proofs of change-of-base formulas, complex logarithms, and the detailed derivation of continuous compounding stay outside the scope here.

The first question to settle is this: `why do later Parts keep calling log and exp back when they explain probabilities, scores, and loss?`

So this section fixes only four places first.

- What kind of change does an exponential describe?
- Why is a logarithm described as a `function that reads in reverse`?
- Why do multiplication and division turn into addition and subtraction once they meet logs?
- Why does this notation lead into loss, probability scores, and softmax explanations?

The flow after this section is also simple.

- In Part 4, we use the same intuition about logs and exponentials again when reading `log loss` and `sigmoid`.
- In Part 6, the same intuition appears again when reading how `softmax` turns scores into comparable ratios.
- So the goal now is not to complete every formula, but to fix the calculation language that connects `score -> ratio -> loss`.

## Goals of This Section

- You can read `exp(x)` as a power of `e`.
- You can explain `log(x)` as a function that reads in the opposite direction of an exponential.
- You can build the intuition that exponentials describe repeated ratio change and logs reread that ratio.
- You can explain why multiplicative relationships are reread as additive relationships in log space.
- You can explain why logs and exponentials keep reappearing in `logistic regression`, `activation function`, and `softmax` explanations.

## One Scene to Hold First

The first scene to hold in this section is the four lines below.

| Expression | First way to read it now | Where it reappears later |
| --- | --- | --- |
| `exp(2) \approx 7.39` | A calculation that spreads score 2 into a larger weight | `sigmoid`, `softmax` |
| `log(exp(2)) = 2` | Reading a value sent into exponential space back on the original axis | logit, log-odds |
| `0.9 x 0.8 x 0.7 = 0.504` | Directly multiplying probabilities makes the value shrink quickly | likelihood, joint probability |
| `log(0.9) + log(0.8) + log(0.7)` | Rereading multiplication as addition | log loss, log-likelihood |

So logs and exponentials are not separate mathematical decoration. They are the language that makes calculations easier to read when moving from `score -> ratio -> probability-like value -> loss`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Exponentials are the language for recording repetition of the `same ratio` | Because they keep us from mixing linear increase with ratio increase. | Understand that `e^x` expresses the speed at which growth expands. |
| A logarithm reads in the opposite direction of an exponential | Because it lets us see `log` as a function read backward instead of memorizing it as a new symbol. | Understand that `exp` and `log` play opposite roles. |
| Logs and exponentials are part of the score-interpretation language of later Parts | Because they keep loss, probability, and softmax from looking like suddenly unfamiliar symbols. | It is enough to grasp why they keep returning later. |

## An Exponential Is Repeated Ratio Change

If addition makes it easier to see `whether the same amount is added again and again`, an exponential can be read as making it easier to see `whether something keeps growing or shrinking by the same ratio`.

\[
e^x
\]

This notation is an exponential function with base `e`. The important point here is that even if `x` grows only a little, the value grows faster in a way that differs from linear growth.

For example, when `x` increases to 1, 2, and 3:

- `x` itself grows linearly by 1 each time.
- `e^x` grows by a larger ratio even for the same increase of 1.

So exponentials appear often when we need to read `a structure where a small difference widens into a much larger difference as we move further along`.

The contrast becomes clearer if we place change by adding the same amount next to change by growing at the same ratio.

| Step | Linear growth example: always `+10` | Ratio growth example: always `x1.1` |
| --- | --- | --- |
| Start | 100 | 100 |
| After 1 step | 110 | 110 |
| After 2 steps | 120 | 121 |
| After 3 steps | 130 | 133.1 |

At first the two changes may look similar, but as the number of steps increases, ratio growth speeds up more and more. An exponential function is exactly the language for this kind of ratio change.

## A Logarithm Reads an Exponential Backward

A logarithm asks in reverse, `what had to be put on the exponential side for this value to come out?`

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

The three shortest values that confirm this intuition are the following.

| Expression | How to read it |
| --- | --- |
| `exp(0) = 1` | If the exponential-side input is 0, it returns to the reference size 1. |
| `log(1) = 0` | We can read 1 as the reference point before exponential change has been applied. |
| `log(exp(x)) = x` | Log returns a value sent into exponential space back to the original axis. |

## Why Multiplication Looks Like Addition Once It Meets Logs

Logs are used often because they change the calculation structure into a form that is easier to read.

- Multiplication is read like addition in log space.
- Division is read like subtraction in log space.

For a beginner, the important thing is not memorizing the formula. The key intuition is that when handling `products of very small or very large numbers`, logs make the calculation less unstable and the comparison easier.

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

There is one question the reader should catch immediately here.

| Scene you are looking at now | Question to ask first |
| --- | --- |
| A value grows step by step like `x1.1`, `x1.2` | Is this growth by the same amount or by the same ratio? |
| Several small probabilities keep being multiplied | Does the value become too small and hard to read? |
| A score is being turned into something like a probability | Does an exponential first enlarge the relative weight? |
| A wrong probability prediction is punished strongly | Does a log read the probability gap more sensitively? |

This perspective becomes especially important in later model explanations.

- In Part 4, it is needed when reading why `log loss` punishes probability predictions that way.
- In Part 6, it is needed when following why `softmax` turns several scores into values that can be read like probabilities.

## Scenes Where This Calculation Reappears

Logs and exponentials do not end inside this section. We are only making the minimum preparation so they do not suddenly feel unfamiliar in the scenes below.

| Scene encountered again later | Intuition to leave here first |
| --- | --- |
| `sigmoid` in logistic regression | An exponential function can be used to turn a score into a value between 0 and 1. |
| log loss | A log is the language that punishes confidently wrong probabilities more strongly. |
| softmax | The process of rereading several scores as comparable probabilities includes intuition about exponentials and logs. |

So the core of this section is that `logs and exponentials are not a math-exam topic but a language for interpreting scores`.

## A Very Short Calculation Example

Even the same linear score cannot be read directly as a probability. So later we meet a transition like this.

1. First compute a score.
2. Then turn that score with an exponential function or read it with log loss.
3. Then compare the result like a probability or bundle it as loss.

For example, if two candidates have scores `2` and `1`, the score difference is `1`, but that is not yet a probability. If we take the exponential here:

\[
e^2 \approx 7.39,\quad e^1 \approx 2.72
\]

the larger score gets a much larger weight. If we divide these values by their sum again, they become ready to be read as `comparable ratios`, like softmax.

If we rewrite that scene more briefly as a table, it looks like this.

| Step | Calculation | What it reads |
| --- | --- | --- |
| Original score | `2`, `1` | Still a simple score, not yet a probability |
| Apply exponential | `exp(2) \approx 7.39`, `exp(1) \approx 2.72` | Gives a larger weight to the larger score |
| Normalize by the sum | `7.39 / (7.39 + 2.72)` | Ready to change into a comparable ratio |

On the other hand, if we read with a log the case where the correct probability is predicted well as `0.9` and the case where it is predicted badly as `0.1`, the wrong one receives a much larger penalty. This is why log loss punishes `predictions that are wrong but confident` more strongly.

Using the same standard, if we look at `-log(p)`:

| Correct probability `p` | Feeling of `-log(p)` |
| --- | --- |
| `0.9` | The loss is small |
| `0.5` | The loss becomes larger |
| `0.1` | The loss becomes very large |

So log loss works in the direction of punishing `predictions that are wrong even though the model was confident` more strongly.

Logs and exponentials are the language that makes calculations easier to read when moving between score, probability, and loss.

## Perspectives to Remember from This Section

- Exponentials are the language for reading `same-ratio increase`, not `same-amount increase`.
- A log is the inverse-direction function that rereads exponential change back on the original axis.
- If small probabilities keep being multiplied, the value shrinks quickly, so logs let us reread multiplication as addition.
- `sigmoid`, `softmax`, and `log loss` all call this intuition back when moving between scores and probabilities.
- When `exp`, `log`, `softmax`, and `log loss` appear in later Parts, first recall `how a score is turned into ratio and loss`.

## Checklist

- Can you read `exp(x)` as a power of `e`?
- Can you explain why `log(x)` reads an exponential backward?
- Can you state the difference between increase by the same amount and increase by the same ratio?
- Can you explain why taking a log makes several multiplied probabilities easier to read?
- Can you explain why logs and exponentials reappear in `softmax` and `log loss`?
- Can you connect exponentials and logs as `same-ratio increase`, `a way to reread multiplication as addition`, and `the calculation that turns scores into probabilities and loss`?

## Sources and References

- Python Software Foundation, `math — Mathematical functions`, Python 3 documentation. Because it lets us directly check the basic meaning of `math.exp` and `math.log`, it supports the minimum standard in this section for rereading exponentials and logarithms as calculation language. [https://docs.python.org/3/library/math.html](https://docs.python.org/3/library/math.html){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-08
- Google for Developers, `Machine Learning Glossary`. Because it lets us check key later-Part terms such as `log loss`, `softmax`, and `sigmoid` together, it serves as a reference point for seeing why logs and exponentials keep reappearing as the language for interpreting machine learning scores. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-08
