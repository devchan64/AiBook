# P4-11.1 Intuition For Logistic Regression

> Section ID: `P4-11.1`
> Version: `v2026.07.11`

In P4-10, linear regression showed `how to predict a continuous value with a line`. The next step is to see how that same linear way of thinking changes when the task becomes classification.

The central question of this Section is the following.

How can we keep a linear calculation but read the output as a value between 0 and 1?

That question is the starting point of logistic regression.

The name often causes confusion. If it is called `regression`, why is it used for classification? The final purpose of logistic regression is classification, but internally it still computes a linear combination and then turns that value into a form that can be read like a probability. That is why the name remains.

In other words, logistic regression is not `linear regression used directly for classification`. It is `a model that changes the output of a linear calculation so it can be interpreted like a classification probability`.

This Section explains the basic meanings of `logistic regression`, `sigmoid`, `predict_proba`, and `threshold`. The next Section continues the judgment of the current context from that handle, and the basic sense of reading a linear calculation as a classification probability reconnects through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section answers the following questions.

- Why is logistic regression used for classification problems?
- Why is it still called `regression` if the result is read as classification?
- How does a linear combination become a value between 0 and 1?
- What does an output such as `predict_proba` mean?
- Why is a threshold needed?

This Section does not treat the following topics deeply.

- a rigorous derivation of log-odds
- a full equation-level explanation of maximum likelihood estimation (MLE)
- detailed equations of multinomial logistic regression
- solver differences and regularization settings

The spatial interpretation of a decision boundary and a threshold continues immediately in P4-11.2. Why log-odds appears and why maximum likelihood estimation is used is recovered in P4-11.3. How binary classification expands into multinomial classification is recovered in P4-11.4. Why solver and regularization appear as implementation settings is recovered in P4-11.5. The broader perspective on regularization and reading hyperparameters reconnects again in P4-9.1, P4-9.2, and P5-8.1.

## Goals Of This Section

- You can explain logistic regression as `a linear model that produces an output that can be read like a probability in a classification problem`.
- You can distinguish the common structure and the difference between linear regression and logistic regression.
- You can explain at an introductory level why the sigmoid function appears.
- You can understand that `predict_proba` and the final class prediction are different stages.
- You can explain that a threshold intervenes in classification judgment.

## Learning Background

The algorithm flow of Part 4 is designed so the move from regression to classification does not feel abrupt. Linear regression came first to show that logistic regression is not a completely unrelated world. It is a case where the interpretation of the output changes inside the same family of linear models.

| Curriculum position | Role of logistic regression |
| --- | --- |
| after P4-10 linear regression | extends linear thinking to classification problems |
| after P4-6 evaluation metrics | prepares the connection between probabilistic outputs and classification metrics |
| before P4-11.2 | introduces the concept of a decision boundary |

So, P4-11.1 is both `the first Section that introduces a classification model` and `the Section that shows continuity with linear regression`.

## Main Learning Content

### What Kind Of Problem Does Logistic Regression Handle?

Logistic regression is usually introduced first for `binary classification`, where the model chooses one of two classes.

Examples include the following.

| Work situation | Value to predict |
| --- | --- |
| Will a customer churn? | churn / not churn |
| Is an email spam? | spam / normal |
| Is a transaction fraud? | fraud / normal |
| Does a patient have high risk of a certain disease? | high risk / not high risk |

The common point in these problems is that the output is not a continuous number but a `category`. Even so, the internal calculation still happens with numbers.

`Logistic regression is a model that estimates, from the input, how likely one class is, maps that value into the range from 0 to 1, and then uses it to make a classification decision.`

### Why Is It Called Regression If It Performs Classification?

This is the first misunderstanding to clear up. Logistic regression performs classification, but internally it still computes a linear score.

The simplest form can be imagined as follows.

\[
z = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

This structure is the same one seen in linear regression. The difference is that logistic regression does not stop there. Linear regression tried to read this value directly as the prediction. Logistic regression passes it through a sigmoid function and changes it into a value between 0 and 1.

So the word `regression` remains as a trace of the linear combination and the numerical estimation method, while the practical purpose is closer to `classification`.

### Why Is The Sigmoid Function Needed?

If a classification problem used the output of a linear formula directly, values like `1.7`, `-2.3`, and `5.8` would appear. Those are hard to read directly in classification. Usually we want to read `how likely is this class?` in a range between 0 and 1.

The sigmoid function does exactly that.

- A very large positive input is sent to a value close to 1.
- A very large negative input is sent to a value close to 0.
- A middle value is sent near 0.5.

`Sigmoid is the function that compresses the result of a linear calculation into a 0-1 range that is easier to read for classification.`

This flow can be drawn simply as follows.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-1-mermaid-01-en.mmd"
```

The key point is that logistic regression does not throw away the line. It `keeps the linear calculation and adds one more transformation layer for interpretation`.

### What Is The Same And What Is Different Between Linear Regression And Logistic Regression?

The two models resemble each other because both use a linear combination. But the meaning of the output is different.

| Item | Linear regression | Logistic regression |
| --- | --- | --- |
| Main problem type | regression | classification |
| Internal calculation | linear combination | linear combination |
| Final output | continuous value | 0-1 score and class decision |
| Introductory interpretation | predict points, minutes, money | estimate which class is more likely |

So logistic regression is not a model with a completely different starting point. It is a model that reinterprets the same linear structure for classification.

### What Does `predict_proba` Show?

One of the important outputs in the scikit-learn logistic regression documentation is `predict_proba`. Readers often treat it immediately like the final answer, but in practice it is the information of one stage earlier.

For example, if the value is `0.82`, it usually means `the model considers the positive class fairly likely`. But whether the final class is written as `0` or `1` is determined by the threshold.

In other words:

- `predict_proba`: the degree of possibility
- `predict`: the final classification decision

If this distinction is missed, it becomes easy to confuse a `score` with a `decision`.

It becomes clearer in a tiny example.

| User | Class 1 score read through `predict_proba` | Decision under threshold 0.5 |
| --- | ---: | --- |
| A | 0.18 | class 0 |
| B | 0.49 | class 0 |
| C | 0.51 | class 1 |
| D | 0.87 | class 1 |

The important rows in this table are B and C. The difference in score is not large, but once threshold 0.5 is used, the final class changes. The score space created by the model is continuous, but the service decision can split discontinuously on top of it.

### Why Is A Threshold Needed?

Logistic regression is often introduced first with the rule that it decides the class using `0.5`.

- if the probability-like value is `>= 0.5`, choose class 1
- if the probability-like value is `< 0.5`, choose class 0

But this criterion is not a law of nature. It is a chosen policy.

In fraud detection, for example, the cost of missing a fraud can be high, so a service may want to catch cases more aggressively. In another service, blocking normal users too often may be unacceptable, so the threshold can be set more conservatively.

That means logistic regression produces `a probability-like score`, and the service decides `where to draw the line` on top of that score.

This point connects directly with the evaluation metrics of P4-6, the baseline of P4-8, and the tuning discussion of P4-9.

Consider one more small example.

| Customer | Churn score | threshold = 0.5 | threshold = 0.7 |
| --- | ---: | --- | --- |
| E | 0.42 | keep | keep |
| F | 0.58 | alert | keep |
| G | 0.73 | alert | alert |

Even with the same score, service behavior changes when the threshold changes. This is why logistic regression should be read with `model score` and `operating policy` separated. Cases near the boundary are first signals to raise review priority. Changing the threshold alone is not a complete explanation of the cause.

The same comparison frame should be kept here too. Thresholds must be compared over the same baseline, the same score range, and the same representative failure cases so that `what changed because of policy` and `what remains because of weak representation` do not get mixed together.

When this point is rewritten as project notes, it becomes even clearer. If logistic regression is used as the first comparison model, the team should not leave only the score table. It should also record `which score range becomes a review target`, `which examples change behavior when the threshold changes`, and `what actually improved compared with the baseline`.

| Record to keep together | Why it is needed |
| --- | --- |
| score comparison between the baseline and logistic regression | to see what really improved beyond a simple rule |
| examples of behavior changes by threshold | to record how service policy changes even with the same score |
| review score range | to reread near-boundary cases as human review candidates |
| next adjustment question | to decide whether to change the threshold, add features, or compare another candidate model |

This record keeps statements like `the score improved`, `the threshold changed`, and `the number of alerts increased` from being mixed together.

### When Is Logistic Regression A Good First Candidate?

Logistic regression is often the first comparison model for a classification problem, but the reason is not that it is simply famous. It is because it is a linear classification model that makes it comparatively easy to separate score and policy.

| Current problem state | Why raise logistic regression first | What to check first |
| --- | --- | --- |
| the goal is binary classification | because it is easy to read both a 0-1 score and a final class together | whether the output is really a categorical decision |
| an explainable first classification model is needed | because the linear score, coefficients, and threshold can be explained relatively directly | whether a linear boundary is sufficient |
| a score model slightly stronger than the baseline is needed | because actual improvement beyond a majority-class rule is easy to compare | what changed inside the confusion matrix |
| a review score range should be left for humans | because `predict_proba` and threshold can be separated to define review targets | whether near-boundary cases are being recorded separately |
| service policy must be separated from model output | because the structure that the model makes the score and policy decides behavior stays visible | whether threshold change and model improvement are being mixed |

The key point of this table is to use logistic regression as both `a comparison model that goes beyond a first classification baseline` and `a training model for reading score and policy separately`.

## Cases And Examples

### Case 1. Why Does Logistic Regression Fit Churn Prediction Well As A First Model?

Suppose a team wants to predict customer churn from login frequency, time since last purchase, and complaint count. If a class 1 score of `0.82` appears, the model is not directly ordering `take action now`. It is saying `this user is read as quite likely to belong to the churn class`.

That interpretation is useful because the team can still decide what to do with a threshold:

- immediate campaign
- human review
- monitoring only

So logistic regression is often useful not because it finishes the policy, but because it separates `score creation` from `behavior decision`.

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-1-mermaid-02-en.mmd"
```

### Case 2. Why Is Spam Filtering Not Finished By The Probability Alone?

Imagine an email has a spam score of `0.49`. Under threshold `0.5`, it remains in the normal inbox. But this does not mean the message is certainly safe. It only means it falls on the class 0 side under the current threshold.

The service may still:

- surface it to a manual moderation queue,
- apply a softer warning,
- or compare it with representative false-negative cases.

This case shows why `probability-like output` and `final behavior` should not be read as the same sentence.

## Practice And Example

### Python Example: Reading `predict_proba` And `predict` Separately

The example below shows that logistic regression creates a score first and then turns it into a class through a threshold.

```python
import numpy as np

scores = np.array([0.18, 0.49, 0.51, 0.87])
pred_05 = (scores >= 0.5).astype(int)

print("scores        :", scores)
print("threshold 0.5 :", pred_05)
```

An example output is as follows.

```text
scores        : [0.18 0.49 0.51 0.87]
threshold 0.5 : [0 0 1 1]
```

This output shows that `0.49` and `0.51` are close as scores, but once the threshold is applied they end up on different sides of the final class decision.

### Python Example: Reading Threshold Difference Together

Now, look directly at how the final behavior changes when the threshold changes, even if the score is the same.

- problem situation: assume the model has already produced churn scores
- input: computed class 1 scores
- expected output: how the decision changes under thresholds 0.5 and 0.7
- concept to check:
  - the score may stay the same while the policy criterion changes the class decision
  - the model output and the service action should be read separately

```python
import numpy as np

scores = np.array([0.42, 0.58, 0.73])

pred_05 = (scores >= 0.5).astype(int)
pred_07 = (scores >= 0.7).astype(int)

print("scores          :", scores)
print("threshold 0.5   :", pred_05)
print("threshold 0.7   :", pred_07)
```

An example output is as follows.

```text
scores          : [0.42 0.58 0.73]
threshold 0.5   : [0 1 1]
threshold 0.7   : [0 0 1]
```

This output again shows that the model creates the score, but the operating rule decides how that score becomes behavior.

### Change One More Value: How Does Interpretation Shake If One Near-Boundary Label Changes?

Now change the near-boundary case `study_hours = 4` from `fail (0)` to `pass (1)` in the training data.

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)
passed_original = np.array([0, 0, 0, 0, 1, 1, 1, 1])
passed_shifted = np.array([0, 0, 0, 1, 1, 1, 1, 1])

model_original = LogisticRegression()
model_original.fit(study_hours, passed_original)

model_shifted = LogisticRegression()
model_shifted.fit(study_hours, passed_shifted)

score_original = model_original.predict_proba([[4]])[0][1]
score_shifted = model_shifted.predict_proba([[4]])[0][1]

print("class 1 score at x=4, original labels :", round(score_original, 3))
print("class 1 score at x=4, shifted labels  :", round(score_shifted, 3))
```

An example output is as follows.

```text
class 1 score at x=4, original labels : 0.327
class 1 score at x=4, shifted labels  : 0.579
```

### What Stayed The Same And What Changed?

- What stayed the same: the overall direction still says that more study time tends to raise the score toward the pass side.
- What changed: once one near-boundary label changed, the class 1 score at `x=4` moved sharply from `0.327` to `0.579`.
- Judgment to leave first: the score of logistic regression is not a probability discovered from nature. It is an interpretation produced by the current data boundary.

### How This Exercise Recovers The Goal Of Part 4

This exercise makes logistic regression readable again not merely as `a model that prints scores`, but as `a classification rule that is sensitive to near-boundary examples`. The goal of Part 4 is not to trust one number by itself. It is to read how a change in one example shakes score interpretation and threshold judgment. Repeating the same example with one changed value makes it more visible that there is always one more layer between model output and service action: data interpretation.

| Common record language | What to record immediately from this exercise |
| --- | --- |
| structure observed | even one changed near-boundary label strongly changed the interpretation of the class 1 score for the same input |
| interpretation boundary | this score change alone does not prove that the real-world probability suddenly changed; the sample and the data boundary still need to be read together |
| next question | if more near-boundary cases are collected, does the score become less unstable, and what changes once threshold policy is added? |

## Perspectives To Remember In This Section

- Logistic regression is a linear model that produces outputs that can be read like probabilities in a classification problem.
- The internal calculation is still a linear combination, but the final interpretation changes into a 0-1 range through sigmoid.
- `predict_proba` is the score stage, while `predict` is the decision stage after the threshold.
- Coefficients are useful for reading direction, but they do not automatically prove cause.
- The threshold is less a law of the model than a judgment criterion tied to service policy.

## Checklist

- Did you first confirm that the current task is binary classification?
- Are you avoiding reading `predict_proba` and final `predict` as the same thing?
- Can you explain threshold change separately from improvement of the model itself?

## When To Recall This Perspective First

- When a binary classification task is being described as though the score and the final decision were one thing, recall the separation between `predict_proba` and `predict` first.
- When threshold adjustment and retraining the model are being treated like the same kind of change, separate policy boundary and the model itself.
- When coefficient interpretation, sigmoid, and probability-like output feel tangled together, return to the perspective that logistic regression is `a linear combination plus one more interpretation layer`.

## Connection To The Next Section

P4-11.1 looked at logistic regression as `a linear model that produces scores that can be read like probabilities`. The next Section, P4-11.2, moves to how those scores can be read as a boundary in the input space, that is, the perspective of a decision boundary.

If 11.1 is the Section of `output interpretation`, 11.2 is the Section of `space and boundary interpretation`.

## Sources And References

- scikit-learn, `1.1.11. Logistic regression`, scikit-learn User Guide, checked on 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `LogisticRegression`, scikit-learn API Reference, checked on 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }
