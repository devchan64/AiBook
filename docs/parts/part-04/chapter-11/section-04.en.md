# P4-11.4 Supplementary Learning: How To Read Multinomial Logistic Regression

> Section ID: `P4-11.4`
> Version: `v2026.07.31`

P4-11.3 explained [log-odds](/AiBook/en/reference/concept-glossary-alpha/l/#logistic-regression) and [MLE](/AiBook/en/reference/concept-glossary-alpha/m/#maximum-likelihood-estimation-mle) mainly on the basis of `binary classification`, where the model chooses one of two classes. But many real classification problems ask the model to choose one out of three or more classes.

The central question of this Section is the following.

How does the intuition of `score -> probability -> class selection` learned in binary classification continue in a multiple-class problem?

## Questions Closed By Multinomial Logistic Regression

This Section answers the following questions.

- What stays the same in a multinomial problem?
- Why does [softmax](/AiBook/en/reference/concept-glossary-alpha/s/#softmax) appear?
- How should one-vs-rest and [multinomial logistic regression](/AiBook/en/reference/concept-glossary-alpha/l/#logistic-regression) be distinguished?

This Section first closes [multinomial logistic regression](/AiBook/en/reference/concept-glossary-alpha/l/#logistic-regression) as an extension where the structure `score -> probability distribution -> class selection` continues across multiple classes, and focuses on holding onto how the threshold intuition moves into an [argmax](/AiBook/en/reference/concept-glossary-alpha/s/#softmax) intuition.

At the same time, the narrower question that should be revisited next is also clear. The implementation perspective on solver and regularization continues in P4-11.5.

## Judgments To Keep From Multinomial Logistic Regression

- You can explain that the structure `input -> score -> probability comparison -> class selection` remains in multiclass settings too.
- You can read softmax as `the function that turns class-specific scores into a probability distribution`.
- You can explain the difference between one-vs-rest and multinomial at an introductory level.

## Learning Background

When logistic regression is first introduced in P4-11.1, the reader usually watches one `class 1 probability` and compares it with a threshold. But many real problems, such as news classification, customer inquiry classification, and image classification, ask the model to choose not one of two but one of many classes.

Examples include the following.

| Problem | Example classes |
| --- | --- |
| news classification | politics / business / sports |
| customer inquiry classification | refund / shipping / account |
| image classification | cat / dog / bird |

The first point the reader should hold here is not `a completely different model begins`. It is that `the reading frame learned in binary classification widens`.

## The Score and Probability Comparison Structure Remains in Multiclass Settings

In a multiclass setting, one can think of the model as creating one score \(z_k\) for each class \(k\).

\[
z_k = w_k^\top x + b_k
\]

And to convert those scores into a probability distribution, softmax is commonly used.

\[
P(y = k \mid x) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}
\]

The core meaning of this expression is simple.

- the numerator is `the score of the current class k`
- the denominator is `the sum over all class scores`
- therefore one class probability is determined by `relative comparison among all classes`

So the minimal structural description of multinomial logistic regression is only two lines: `make a score for each class`, then `normalize all of those scores together into a probability distribution`.

### The Threshold Intuition Of Binary Classification Moves Toward An Argmax Intuition

In binary classification, the key intuition was `does it pass 0.5?` In multiclass classification, the key intuition usually becomes `which class probability is the largest?`

- binary classification: compare one `class 1 probability` with a threshold
- multiclass classification: compare `all class probabilities` and choose the largest

This change connects directly back to P4-11.1. Beginners can mistakenly think that producing several probabilities means a totally different and more complicated model. But the basic structure still remains `input -> score -> probability comparison -> class selection`.

### One-Vs-Rest And Multinomial Differ In The Way They Compare

At the introductory stage, the difference between one-vs-rest and multinomial can be held at the following level.

- one-vs-rest: treat each class separately as `is it this class or not?`, then compare
- multinomial: place all classes together and compare them at once

The difference becomes easier to read in a tiny inquiry-classification example.

| Reading style | How the same inquiry is read |
| --- | --- |
| one-vs-rest | ask separately `is it a refund inquiry?`, `is it a shipping inquiry?`, `is it an account inquiry?`, and compare later |
| multinomial | place `refund / shipping / account` together and compare immediately which is most plausible |

There is no need to force all the matrix equations or the full softmax expansion in the current Section. What matters is the connection that `the score and probability-comparison intuition learned in binary classification continues into multiple classes`.

The shape of the likelihood expands in the same spirit as binary classification. If the correct class is imagined as a one-hot vector, the log-likelihood of the multiclass case is usually read in the following summed form.

\[
\log L = \sum_{i=1}^{n}\sum_{k=1}^{K} y_{ik} \log P(y=k \mid x_i)
\]

Here \(y_{ik}\) means `1 if the correct class of sample i is class k, and 0 otherwise`. This equation also says, in the end, `prefer the direction that gives high probability to the correct class`, only in multiclass form.

## Cases And Examples

Before the cases, the comparison frame of this Section can be summarized as follows.

| Scene | Easy rule a person might use first | Limit of that rule | What multinomial logistic regression changes | Result to check |
| --- | --- | --- | --- | --- |
| multiple-class classification | keep thinking in terms of threshold 0.5 | misreads the problem as if it were still binary | move to relative comparison through softmax and argmax | choose the class with the largest probability |
| implementation choice | inspect each class one by one | misses the relative comparison among classes | read classes as competing together inside a multinomial structure | inspect the whole class distribution together |

### Case 1. In Multiclass Settings, Relative Comparison Matters More Than 0.5

Suppose a customer-inquiry task has three classes: `refund`, `shipping`, and `account`. If the predicted probability vector for one inquiry is `[0.41, 0.39, 0.20]`, nothing exceeds 0.5. Even so, the model still sees `refund` as the most plausible class.

This scene shows that in multiclass classification the key question becomes not `does it exceed 0.5?` but `which is the largest?`

### Case 2. The Same Input Can Be Read Differently By One-Vs-Rest And Multinomial

If the inquiry text contains mixed words such as `refund`, `payment cancellation`, and `account lock`, one-vs-rest checks each class separately and compares later. Multinomial compares the entire class set at once and decides the relative probabilities directly. For beginners, the latter can often be easier to read as `one comparison structure`.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-4-mermaid-01-en.mmd"
```

## Practice And Example

### Python Example: Read A Multiclass Probability Table

The example below shows the basic intuition that, in multiclass classification, the reader should ask not `does it exceed 0.5?` but `which probability is the largest?`

| Input bundle | Meaning |
| --- | --- |
| `class_names` | list of class names |
| `multi_proba` | example probability distributions across classes |

Values to change:

- Change the first row to something closer such as `[0.34, 0.33, 0.33]` to see that argmax still chooses one class even when the judgment is much more ambiguous.
- Change the last row to `[0.22, 0.28, 0.49]` to check that the largest class can still be selected even when no value exceeds 0.5.

```python
# This example compares class-wise scores and softmax probabilities in multinomial logistic regression.
import numpy as np

class_names = ["refund", "shipping", "account"]
multi_proba = np.array([
    [0.41, 0.39, 0.20],
    [0.18, 0.63, 0.19],
    [0.22, 0.28, 0.50],
])

print("multiclass predictions")
for row in multi_proba:
    best_idx = int(np.argmax(row))
    print(
        "  probs =",
        np.round(row, 2),
        "->",
        class_names[best_idx],
    )
```

An example output is as follows.

```text
multiclass predictions
  probs = [0.41 0.39 0.2 ] -> refund
  probs = [0.18 0.63 0.19] -> shipping
  probs = [0.22 0.28 0.5 ] -> account
```

This output can be read as follows.

- In the first row, even though no value exceeds 0.5, the model still chooses `refund` because it has the largest probability.
- In multiclass settings, `relative comparison across the whole probability distribution` matters more than `one probability vs one threshold`.
- So the basic intuition shifts from threshold toward argmax.

## Sources And References

- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006. Checked on 2026-07-26. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, linear models user guide, [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-26
- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-26
