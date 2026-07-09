# P2-2.4 Why Log and Exp Keep Reappearing

> Section ID: `P2-2.4`
> Version: `v2026.07.09`

Even after limits are back in place, one more kind of notation keeps blocking readers in later machine learning and deep learning explanations: `log`, `exp`, and expressions such as `e^x`. These are not advanced decorative math. They keep showing up whenever we need to describe how fast values grow or shrink, how multiplicative relationships can be reread additively, and how score-like numbers can be handled like probabilities.

## Scope of This Section

The question to settle first is this: why do later Parts keep calling `log` and `exp` back when they explain probabilities, scores, and loss?

So this Section fixes four places first.

- What kind of change does an exponential describe?
- Why is a logarithm often described as reading the exponential in reverse?
- Why do multiplication and division become addition and subtraction in log space?
- Why does that notation later return in loss, probability scores, and softmax?

## One Scene to Hold First

| Expression | How to read it first | Where it reappears later |
| --- | --- | --- |
| `exp(2) \approx 7.39` | A score of 2 is spread into a much larger weight | `sigmoid`, `softmax` |
| `log(exp(2)) = 2` | A value sent into exponential space is read back on the original axis | logit, log-odds |
| `0.9 x 0.8 x 0.7 = 0.504` | Probabilities become small quickly when multiplied directly | likelihood, joint probability |
| `log(0.9) + log(0.8) + log(0.7)` | Multiplication is reread as addition | log loss, log-likelihood |

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| Exponentials are the language of repeated ratio change | It keeps linear increase separate from multiplicative growth | Understand that `e^x` expresses the speed of ratio-based growth |
| A logarithm reads the exponential in reverse | It stops `log` from feeling like an isolated symbol | Understand that `exp` and `log` play opposite roles |
| Logs and exponentials are the language of later score interpretation | It stops loss, probability, and softmax from feeling like sudden alien notation | Understanding the later connection is enough here |

## An Exponential Represents Repeated Ratio Change

\[
e^x
\]

This is the exponential function with base `e`. The important point is that when `x` grows a little, `e^x` does not grow linearly. It widens by ratio.

| Step | Linear increase: always `+10` | Ratio increase: always `x1.1` |
| --- | --- | --- |
| Start | 100 | 100 |
| After step 1 | 110 | 110 |
| After step 2 | 120 | 121 |
| After step 3 | 130 | 133.1 |

## A Logarithm Reads the Exponential in Reverse

\[
\log(x)
\]

For example:

- `exp(2)` means `e^2`
- `log(e^2)` returns to `2`

So logs and exponentials are inverse directions of the same relationship.

## Why Multiplication Looks Like Addition in Log Space

Suppose we multiply three probabilities:

\[
0.9 \times 0.8 \times 0.7 = 0.504
\]

If many more values are multiplied, the product becomes small very quickly. But once you take logs, the same product is read as a sum:

\[
\log(0.9 \times 0.8 \times 0.7)
=
\log(0.9) + \log(0.8) + \log(0.7)
\]

That is why machine learning more often uses expressions in log space than direct products of many probabilities.

## Where This Reappears

| Later scene | Intuition to keep now |
| --- | --- |
| `sigmoid` in logistic regression | An exponential can help turn a score into a value between 0 and 1 |
| Log loss | Log language can penalize confident wrong probability predictions more strongly |
| Softmax | Exponentials and logs help turn several scores into comparable probability-like ratios |

## A Very Short Calculation Example

Suppose two candidates have scores `2` and `1`. The scores are not probabilities yet. If you exponentiate them:

\[
e^2 \approx 7.39,\quad e^1 \approx 2.72
\]

the larger score gets a much larger weight.

| Step | Calculation | What you are reading |
| --- | --- | --- |
| Original score | `2`, `1` | Still just scores |
| After exponentiation | `exp(2) \approx 7.39`, `exp(1) \approx 2.72` | Larger scores receive larger weight |
| After normalization | `7.39 / (7.39 + 2.72)` | Ready to be read as comparable ratios |

The same intuition appears in log loss:

| Correct probability `p` | Intuition of `-log(p)` |
| --- | --- |
| `0.9` | Small loss |
| `0.5` | Larger loss |
| `0.1` | Very large loss |

## Perspective to Keep from This Section

- Exponentials read repeated ratio growth, not repeated fixed-size increase.
- Logs read exponential change back on the original axis.
- When many small probabilities are multiplied, logs let you reread the product as a sum.
- `sigmoid`, `softmax`, and `log loss` all call this score-to-ratio language back.

## Short Check

- Can you read `exp(x)` as a power of `e`?
- Can you explain why `log(x)` reads exponential change in reverse?
- Can you explain the difference between additive growth and ratio-based growth?
- Can you explain why logs make products of many small probabilities easier to read?
- Can you explain why logs and exponentials reappear in softmax and log loss?

## Sources and References

- Python Software Foundation, [math — Mathematical functions](https://docs.python.org/3/library/math.html){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-08.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-08.
