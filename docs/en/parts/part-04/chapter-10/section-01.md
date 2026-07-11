# P4-10.1 Intuition For Linear Regression

> Section ID: `P4-10.1`
> Version: `v2026.07.11`

In P4-9.2, the discussion used tuning and validation cost to ask `how should promising settings be compared?` Now it is time to connect that comparison procedure to one actual algorithm.

The reason this Part begins with linear regression is straightforward. Linear regression is both the most basic starting point for a regression problem and the model that shows the relationship between input and output most transparently through a `slope` and an `intercept`.

The central question of this Section is the following.

How can a model express the relationship that output tends to increase or decrease as input increases in the simplest possible way?

Linear regression answers this question first with a `line`.

This Section explains the basic meanings of `regression`, `linear regression`, `coefficient`, and `intercept`. Later Sections continue the surrounding judgment from this handle, and the basic sense of reading a continuous prediction with a line reconnects through this Section and the [concept glossary](../../../reference/concept-glossary.md).

## Scope Of This Section

This Section answers the following questions.

- What kind of problem does regression handle?
- Why is linear regression described as expressing a relationship with a `line`?
- How can direction and size between an input feature and an output target be read?
- Why is linear regression the first algorithm studied in Part 4?

This Section does not treat the following topics deeply.

- statistical properties of residuals
- a rigorous derivation of ordinary least squares
- multicollinearity, regularization, and hypothesis testing
- detailed comparison among evaluation metrics such as R², MAE, and RMSE

Evaluation metrics and residual interpretation continue immediately in the next Section, P4-10.2. Basic reading of multicollinearity, statistical tests, and regression diagnostics is reorganized again in the supplementary learning of P4-10.3. The broader perspective on regularization and related hyperparameters reconnects again through P4-9.1 and P4-9.2.

## Goals Of This Section

- You can explain regression as `a problem that predicts a continuous value`.
- You can describe linear regression as `a model that first approximates the relationship between input and output with a line`.
- You can explain that `linear` here means `the whole input is read as one weighted sum`.
- You can explain the intuition of a slope and an intercept.
- You can explain at an introductory level what linear regression tries to reduce.
- You can understand why linear regression is both a good baseline and a good starting point.

## Learning Background

Earlier in Part 4, the discussion organized data splitting, baselines, tuning, and evaluation criteria first. The reason was to help the reader first read `what problem is being solved in what form` instead of memorizing algorithm names from the start.

In this curriculum, linear regression plays the following role.

| Curriculum position | Role of linear regression |
| --- | --- |
| after P4-4 regression and classification | connects a regression problem to an actual model |
| after P4-8 baseline | provides the first comparison model that is simple but interpretable |
| before classification models after P4-11 | prepares the difference between continuous prediction and probabilistic classification |

In other words, linear regression comes first not because it is `the easiest algorithm`, but because it is `the algorithm that explains the relationship between input and output most clearly`.

## Main Learning Content

### What Kind Of Problem Does Regression Handle?

Regression does not predict a category like classification does. Instead, it predicts a numeric value that changes continuously.

Examples include the following.

| Work situation | Value to predict |
| --- | --- |
| predict housing prices from home size and location | price |
| predict sales from advertising budget and seasonal information | sales amount |
| predict delivery time from travel distance and traffic conditions | time |
| predict a final score from study time and assignment results | score |

The common point in these problems is that the output is a number, not `yes or no`.

`Regression is the problem of estimating one continuous value from an input.`

### Why Does Linear Regression Express The Relationship With A Line?

The linear-model documentation of scikit-learn describes linear regression as a family of models that learn the relationship between observed values and a linear combination. This Section rewrites that idea into an easier question.

`If the input increases a little, by how much does the output increase on average?`

The simplest formula that answers this question has the following form.

\[
y = wx + b
\]

- `x`: input
- `y`: prediction
- `w`: coefficient
- `b`: intercept

The coefficient `w` means `how much y changes when x changes by 1`. The intercept `b` is the starting point that the model places when the input is 0.

If that structure is read like a diagram, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-1-mermaid-01-en.mmd"
```

This diagram shows one-variable linear regression as a structure in which one input passes through a coefficient and an intercept to reach a prediction. The first point to hold here is that linear regression is not a model that memorizes data. It is a model that reads in numbers how a change in the input pushes the output upward or pulls it downward.

The key point is that linear regression does not claim that `reality is perfectly a line`. Rather, it asks `is there a relationship that can first be explained with a line?`

However, one more point should be fixed more accurately here. Readers often remember linear regression only as `a model that always draws one line on a two-dimensional graph`. That memory is correct for a one-variable example, but it is too narrow to explain the algorithm itself.

### What Exactly Does Linear Mean?

The word `linear` in linear regression is often introduced first through the image of a line, but in theory it is closer to the idea that `inputs are read as a sum with weights`.

When there is one input, the form is

\[
y = wx + b
\]

When there are several inputs, it expands as follows.

\[
y = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

In other words, linear regression places one coefficient on each input feature and creates the final prediction by adding up their contributions.

`Linear regression is a model that assigns one numeric contribution to each input and adds those contributions together to produce one prediction.`

If this is drawn simply, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-1-mermaid-02-en.mmd"
```

This diagram shows that even when the number of inputs increases, the core structure of linear regression stays the same. Even if each feature has its own meaning, the model ultimately gathers them into one weighted sum to produce a single prediction. That is the central intuition of the word `linear`.

So, in a one-variable example, the reader sees a `line`. With two or more variables, the reader moves on to a `plane` or a higher-dimensional `linear relationship`. The reader does not need to master all the mathematics of dimensionality here. It is enough to keep the point that `even when inputs increase, the structure is still a weighted sum`.

### Why Is The Assumption Of A Line Useful?

Most real-world data do not sit exactly on one perfect line. Even so, linear regression still matters for three reasons.

1. It allows the simplest explanation to be tried first.
2. The coefficient and intercept are relatively easy to interpret.
3. It provides a reference point for deciding whether a more complex model is truly needed.

For example, if test scores tend to rise as study time rises, linear regression first summarizes that relationship with the question `when study time increases by one hour, how many points does the score change on average?`

Even if that line is not perfect, it still lets the reader answer questions like the following right away.

- Is the direction of the relationship positive or negative?
- Is the size of the change large or small?
- Is there a pattern that this simple summary misses?

In other words, linear regression is not mainly a tool that contains all of reality. It is closer to the first coordinate axis for reading reality.

### What Does Linear Regression Learn?

In an algorithm chapter, the intuition `it reads with a line` is not quite enough. The reader also needs to fix what the model actually learns.

Linear regression creates predictions for data points and adjusts the coefficient and intercept so that the overall difference between those predictions and the actual values becomes small.

For each data point, this creates

- an actual value
- a prediction
- and the difference between them, called a residual or error

Linear regression chooses the line in a direction that keeps these differences from becoming too large overall.

`LinearRegression` in scikit-learn uses a solution corresponding to ordinary least squares by default. That flow can be read immediately through the following sentence.

`A method that tries to find the line that leaves the least prediction error across the whole dataset`

At this stage, what matters is not a rigorous proof or matrix calculation. The key point is that the line is chosen not by `drawing a line that looks good`, but by `using a criterion that reduces error`.

If this flow is drawn as simply as possible, it becomes the following.

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-1-mermaid-03-en.mmd"
```

This diagram shows that linear regression is not merely drawing a line. It is a process of searching for a better line under a criterion that reduces error. That means the heart of the algorithm is not the visible shape of the line, but `how the model tries to reduce the difference between prediction and reality overall`.

So linear regression is both `a model that draws a line` and `a model that reduces error`. The word algorithm becomes clearer especially from this second point of view.

### When Is It Good To Raise Linear Regression First?

Linear regression is often a good starting point not because it is `the simplest regression model`, but because it is often the clearest first model for reading the direction and size of a relationship.

| Current problem state | Why raise linear regression first | What to check first |
| --- | --- | --- |
| the goal is to predict a continuous value | because it is easy to interpret as a regression baseline | whether the output is numeric rather than categorical |
| the first need is to read direction and size between input and output | because the relationship is easy to explain with coefficients and an intercept | how units and preprocessing affect interpretation |
| it is still unclear whether a complex model is necessary | because it is possible to test first whether a simple model already explains enough | whether the error actually improves beyond the baseline |
| interpretability is important | because the contribution of each feature is easy to explain through a weighted-sum structure | whether correlation is being confused with causality |
| the first comparison model for a regression experiment is needed | because it creates a starting point for comparison with later complex models | whether there is a nonlinear relationship or a missing feature |

The key point of this table is not that linear regression is `always the right model`, but that it is often the first comparison model that reveals the structure of the problem.

## Detailed Learning Content

### What Misunderstandings Happen Most Often In Interpretation?

In linear regression, mistakes happen more often in interpretation than in formulas. The following three are especially common.

### 1. A Large Coefficient May Be Mistaken For An Automatically Important Feature

Even if the coefficient is numerically large, that does not automatically mean the feature is more important.

That is because the size of the coefficient is affected by the scale and measurement unit of the input.

- If the input is `time`, one unit means one hour.
- If the input is `currency`, one unit may mean one dollar or one won.
- If the input is `distance`, one unit may mean one kilometer.

So when features use different units, interpretation can become unstable if the reader compares only the raw coefficient numbers.

`A coefficient is especially useful for reading direction. To compare size, unit and preprocessing must be checked together.`

### 2. A Positive Coefficient May Be Mistaken For A Cause

What linear regression first shows is a `tendency to move together`. That does not itself mean causality.

For example, even if ad spending and sales increase together, that number alone does not prove that increasing ad spending is the only cause of higher sales.

Other explanations may still exist in between, such as

- a seasonal effect
- a promotion period
- prior brand recognition
- or an unmeasured outside variable

So the coefficient of linear regression is first an interpretive tool that shows `direction and size of a relationship`. It is not a tool that automatically proves a cause.

### 3. A Prediction May Be Read As If It Were The Actual Value

The output of linear regression is not a perfect copy of the world. It is an estimate obtained under the current data and the current assumptions.

For example, if the output says `7 study hours -> predicted score 76.4`, that does not mean

- the person will definitely receive exactly 76.4 points

It means

- under the currently learned line, a value near that point is expected

This distinction prepares the reader to read residuals and error in the next Section.

### What Assumptions Does Linear Regression Place Implicitly?

When studying an algorithm, it is important to build the habit of first asking `how does this model simplify the world?` before asking only about performance. Linear regression makes the following simplifications.

### 1. The Relationship Is Roughly Linear

It assumes that when the input changes, the output also moves in a roughly consistent direction and proportion.

For example, scores may rise as study time rises, but in reality the amount of increase may shrink after a certain point. Even so, linear regression first summarizes the overall direction with one line.

### 2. The Influence Of Each Input Can Be Added

When several features exist, linear regression first views them not as complex interactions, but as `the sum of each feature's contribution`.

For example, in a housing-price problem, if size, distance, and age all matter, linear regression first reads the final price as the sum of how much each element contributes.

### 3. Error Remains As The Unexplained Part

The model cannot explain every fluctuation of reality. Linear regression leaves the unexplained difference as error and places the model so that this error becomes small overall.

These three points do not explain every rigorous statistical assumption. Still, they are the key criteria for understanding the worldview of linear regression.

`Linear regression is a model that simplifies relationships into a sum with one direction and treats the remaining difference as error.`

### Why Is Linear Regression A Good First Baseline?

Linear regression is often used as a baseline model because of its interpretability and simplicity.

Before trying a more complex model, running linear regression first lets the reader check the following.

- Can a simple linear relationship already explain some part of the problem?
- Do the directions between feature and target match what was expected?
- How necessary is a more complex model?

So linear regression is useful not only as a model aimed at high performance, but also as a reference model that first tests `how linearly the problem can be read`.

Linear regression is also especially useful for training interpretation. More complex models may achieve somewhat higher performance, but in many cases it becomes difficult to explain directly why a certain prediction appeared. Linear regression, by contrast, answers the following questions relatively directly.

- In what direction did the model read the relationship?
- As which inputs increase, does the prediction also increase?
- Is the problem too rough to be explained well by one line?

In other words, linear regression is not only the starting point of performance but also the starting point of interpretation.

This comparison also connects to later algorithm chapters.

- In P4-11 logistic regression, the line will be read again as a probabilistic classification boundary.
- In P4-14 decision trees, the relationship will be read through branching rules instead of a line.
- In P4-15 random forests, several trees will be combined to handle nonlinear relationships.

## Cases And Examples

### Case 1. How Can The Claim That Sales Rise When Ad Spending Rises Be Expressed In The Simplest Way?

A small online-shopping team wants first to read the relationship between monthly advertising spend and sales. The criteria people first used were questions such as `in months when ad spending rises, does the number of orders also rise?` and `does a similar flow still appear in ordinary months without special events?`

At that point, the team tries the simplest linear regression before a complex model. This is because a single line can first summarize how much sales move on average as ad spending rises, letting the reader immediately read whether the direction is positive or negative and how large the change roughly is. Reality may not be a perfect line, but as a first reference point for `what change is made on average by one unit of increase`, the model is already useful enough.

In this scene, linear regression is not a model that declares `reality is a line`. It is a model that asks `can the relationship first be explained by a line?` If ad spending and sales move mostly in the same direction, the coefficient and intercept become the first explanation that shows that relationship most transparently.

The confirmable result appears in the learned line and the interpretation of the coefficients. If the coefficient is positive, the reader can read the tendency that ad spending and sales increase together. If the difference between prediction and actual value is also inspected, the reader can immediately see how rough it is to explain the whole situation with one line.

```mermaid
--8<-- "assets/part-04/chapter-10/p4-10-1-mermaid-04-en.mmd"
```

## Cases And Examples

### Reading One-Variable Linear Regression In The Simplest Way

Consider an example of study time and exam score.

| study_hours | exam_score |
| --- | --- |
| 1 | 52 |
| 2 | 55 |
| 3 | 61 |
| 4 | 64 |
| 5 | 68 |
| 6 | 72 |

Looking at this data, the score does not rise by a perfectly fixed amount every time, but in general the score rises as time increases. Linear regression looks at this scene and tries to find one line such as the following.

`A line in which exam scores rise on average as study time rises`

What matters here is not `a line that passes through every point exactly`, but `a line that explains the overall direction most reasonably`. As discussed just above, linear regression chooses a better line under a criterion that reduces the difference between prediction and reality, and then uses that result again for predicting new inputs.

If this expression is rewritten a little more theoretically, it becomes the following.

- Some error may remain for each individual data point.
- But across the whole dataset, some lines leave smaller error and some lines leave larger error.
- Linear regression chooses `the line that reduces overall error better`.

In other words, linear regression is not a model that matches each individual point perfectly. It is a model that `summarizes the overall tendency most economically`.

### How Should The Coefficient And Intercept Be Read?

When first learning linear regression, many readers see the formula but miss the meaning. This Section fixes interpretation before calculation.

### Coefficient

The coefficient shows in what direction and by how much the output changes when the input changes.

- coefficient > 0: the output tends to increase as the input increases
- coefficient < 0: the output tends to decrease as the input increases
- large coefficient magnitude: the output changes more sensitively as the input changes

For example, if sales are expected to increase by about 3 units on average whenever ad spend increases by 1 unit, the coefficient can be read roughly as `+3`.

Still, interpretation should always keep two things together.

- `direction`: does the relationship increase or decrease?
- `unit`: what does one unit of the input actually mean?

For instance, whether the input unit means `one hour of study` or `ten thousand won of ad spend` completely changes the meaning of the same number 3. So the coefficient should be read not mainly through the number alone, but through the sentence `when what changes by 1 unit, how much does what else change?`

### Intercept

The intercept is the starting point that the model places when the input is 0. However, the intercept is not always easy to interpret in reality.

For example, predicting a score when study time is 0 can still be read to some degree within the context. But interpreting a house price when the house size is 0 square meters may have little real-world meaning.

So the intercept should be read as follows.

`It is the mathematical starting point of the model, but the direct interpretability depends on the domain.`

## Practice And Example

### A Small Linear Regression Example In Python

The example below is a very small linear-regression practice that predicts exam score from `study_hours`.

- problem situation: roughly predict a score from study time
- input: study time
- label: actual exam score
- concepts to check:
  - linear regression learns one line
  - `coef_` is the coefficient and `intercept_` is the starting point
  - the model can create a continuous-value prediction for a new input

```python
import numpy as np
from sklearn.linear_model import LinearRegression

study_hours = np.array([1, 2, 3, 4, 5, 6]).reshape(-1, 1)
exam_score = np.array([52, 55, 61, 64, 68, 72])

model = LinearRegression()
model.fit(study_hours, exam_score)

pred_2 = model.predict([[2]])[0]
pred_7 = model.predict([[7]])[0]

print("sample count      :", len(study_hours))
print("coefficient       :", round(model.coef_[0], 3))
print("intercept         :", round(model.intercept_, 3))
print("prediction at x=2 :", round(pred_2, 3))
print("prediction at x=7 :", round(pred_7, 3))
```

An example output is the following.

```text
sample count      : 6
coefficient       : 4.114
intercept         : 47.6
prediction at x=2 : 55.829
prediction at x=7 : 76.4
```

This result can be read as follows.

- A coefficient of about `4.114` means that when study time increases by one hour, the score tends to rise by about four points on average.
- An intercept of about `47.6` is the mathematical starting point that the model places.

## Sources And References

- scikit-learn developers, [Linear Models](https://scikit-learn.org/stable/modules/linear_model.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-01.
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, [An Introduction to Statistical Learning](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-01.
