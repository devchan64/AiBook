# P2-6.1 What Does Optimization Search for?

> Section ID: `P2-6.1`
> Version: `v2026.09.08`

Optimization searches for values that minimize or maximize an objective function under specified conditions. To judge which choice is better, we must define the values we can change, the comparison criterion, and the constraints.

## Study Time and Predicted Scores

Suppose four students have the following study times and quiz scores.

| Student | Study time `x` | Quiz score `y` |
| --- | ---: | ---: |
| A | 1 | 55 |
| B | 2 | 65 |
| C | 3 | 80 |
| D | 4 | 90 |

Now the question is: `if we input study time, how should we choose the line y = ax + b that predicts the score?` Here, instead of writing `a` and `b` directly as the answer, the problem of comparing several candidate lines and finding the better one is exactly optimization.

- `a = 10, b = 45` is one candidate.
- `a = 12, b = 40` is another candidate.
- To decide what is better, we need a criterion such as how well it matches the actual score.
- A numerical criterion summarizing the difference between predictions and actual scores is called loss.

The predictions of the two candidates are:

| Study time | Actual score | a = 10, b = 45 | a = 12, b = 40 |
| --- | --- | --- | --- |
| 1 | 55 | 55 | 52 |
| 2 | 65 | 65 | 64 |
| 3 | 80 | 75 | 76 |
| 4 | 90 | 85 | 88 |

Comparing the mean of squared prediction errors gives `(0 + 0 + 25 + 25) / 4 = 12.5` for the first candidate and `(9 + 1 + 16 + 4) / 4 = 7.5` for the second. The first fits two points exactly, but the second is better across all four points under this criterion.

![Optimization flow for comparing candidate values under evaluation criteria and constraints to find a better candidate](/AiBook/assets/part-02/chapter-06/optimization-search-loop-en.svg)

## Candidates, Objectives, and Constraints

| Criterion | Why it matters |
| --- | --- |
| Optimization is the problem of finding a better choice among possible candidates | It shows that a comparison criterion is needed before the calculation itself. |
| Objective and constraint decide what counts as good | It makes clear that the word optimal is not an absolute quality, but a conditional judgment. |
| AI learning is also the process of finding better parameters that reduce loss | It connects optimization not to abstract mathematics, but to the entrance of the learning procedure. |

## Elements of an Optimization Problem

The elements of an optimization problem are:

| Term | Meaning to understand first |
| --- | --- |
| variable | a value we can try changing |
| constraint | a condition that must be respected |
| objective function | the criterion that calculates good and bad |
| minimize / maximize | the direction we want to reduce or increase |

## Available Choices and Constraints

In the line example, each combination of `a` and `b` is a candidate. Even with the same data, changing the evaluation criterion can change the ranking of candidates.

Even if there are many candidates, we cannot compare them without a `criterion`.

| Situation | Candidate | Criterion |
| --- | --- | --- |
| choosing a travel route | several routes | is the travel time shorter? |
| purchasing goods | several products | is the cost lower? |
| choosing a waiting line | several lines | is the waiting time shorter? |
| choosing model settings | several setting values | is the evaluation score better? |

Reality also has `constraints`. For example, the cost must not exceed 100,000 won, response time must finish within 1 second, memory must not exceed a certain capacity, laws and policies must be obeyed, or the user experience must not be harmed.

So optimization is not simply about making one number as good as possible. It is the problem of looking at candidates, criteria, and constraints together.

## Optimization Across Fields

Optimization is not a way of thinking used only in AI. Whenever `we want a good choice, but there are criteria and constraints`, a similar problem appears.

| Field | What we want to find | Criterion | Constraint |
| --- | --- | --- | --- |
| logistics | delivery routes | travel distance, time, cost | number of vehicles, time limits, delivery order |
| manufacturing | production plan | output volume, defect rate, cost | equipment capacity, inventory, due dates |
| advertising | budget allocation | conversion rate, sales, click-through rate | budget, exposure limits, policies |
| service operations | server-resource placement | response speed, stability, cost | server cost, traffic variation |
| search / recommendation | result ordering | clicks, satisfaction, relevance | diversity, safety, policies |
| machine learning | model parameters | loss, accuracy, evaluation score | data, computation, time |

## Resource Allocation and Linear Programming

Optimization is not a word that appeared suddenly with AI. In an older flow, it was closer to the problem, `how do we allocate limited resources among several options?`

For example, in war, logistics, production, and scheduling, important questions included which route to run with limited vehicles, which work to assign with limited staff, how much of which product to make with limited raw materials, and in what order to handle work within limited time.

These questions are not solved simply by `calculating harder`. There are too many candidates, and criteria and constraints exist together. So mathematics and computing tried to turn such problems into computable forms.

`Linear programming` is a representative historical example that shows this flow. We set an objective, add constraints, and then find the better value among the possible choices. George Dantzig's `simplex method` is often mentioned together with real problems such as logistics, scheduling, and network optimization.

## Minimization and Maximization

Optimization problems are usually expressed in two directions. The direction of reducing a value when smaller is better is `minimization`, and the direction of increasing a value when larger is better is `maximization`.

For example, we usually want to reduce travel time, cost, error, and loss.

By contrast, values such as accuracy, revenue, and satisfaction are usually values we want to increase.

In AI learning, we often want to reduce a value. We quantify how much predictions differ from actual values and adjust model values to reduce it. This criterion is the loss function.

## Optima Depend on Objectives and Scope

The word `optimal` needs to be read carefully. By name alone it sounds like a perfect answer, but in practice that is often not the case.

A global optimum has the best objective value among all candidates satisfying the constraints. Whether the best result found by comparing only some candidates is a global optimum requires a separate check.

So when we look at an optimization result, we should ask the following together.

- By what criterion was it called optimal?
- Within what range of candidates was it found?
- What constraints were reflected?
- Were other real-world conditions left out?

This perspective carries directly into AI model evaluation too. Even if one model gets a high score on a certain benchmark, that does not mean it is optimal for every real-world problem. We have to keep asking, `good by what criterion?`

## Optimizing Model Parameters

In the line model, `a` and `b` are model parameters. Learning can repeatedly change these parameters, make predictions, calculate the loss against actual scores, and adjust the parameters to reduce that loss.

Each candidate is a combination of parameter values, and the objective is the loss to minimize. Model parameters are adjusted through learning; distinguish this context from statistical parameters describing properties such as a population mean.

## Advertising Budget and Conversions

Suppose the objective is `maximize expected conversions`, subject to `total cost at most 10 million won`. All other conditions are equal, and only the following three plans are available.

| Plan | Total cost | Expected conversions | Within budget |
| --- | --- | --- | --- |
| A | 9.8 million won | 1,200 | Yes |
| B | 9 million won | 1,150 | Yes |
| C | 10.5 million won | 1,260 | No |

C has the most expected conversions but exceeds the budget and is excluded. A is selected over B because it has more conversions.

If the objective changes to `minimize cost per conversion`, A costs about `8,167 won/conversion` and B about `7,826 won/conversion`, so B is selected. The same candidates and budget can yield a different optimum when the objective changes. These are constructed estimates for comparison, not guarantees of actual conversions.

## Checklist

- You can explain optimization not as writing the answer directly, but as the process of finding a better candidate.
- You can distinguish `candidate`, `criterion`, and `constraint`.
- You can explain `minimization` and `maximization` with examples.
- You can explain that `optimal` does not always mean the perfectly complete answer in reality.
- You can explain AI learning as the process of adjusting model parameters to improve a criterion.
- You can reread learning not as simple calculation, but as the problem of `finding a better value`.

- You can separate what to compare from what to respect when candidates, criteria, and constraints appear mixed together.

## Sources and References

- Stephen Boyd, Lieven Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2004, checked 2026-07-20. Used to confirm the optimization-problem form that minimizes a value under an objective function and constraints.
- SciPy Developers, [Optimization and root finding](https://docs.scipy.org/doc/scipy/reference/optimize.html){: target="_blank" rel="noopener noreferrer" }, SciPy API Reference, checked 2026-07-20. Used to confirm the API context where optimization minimizes or maximizes objective functions and may include constraints.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to confirm the deep-learning context in which parameters are adjusted by reducing a cost function.
- Gary Wolf, [The Optimizer](https://www.wired.com/2001/12/dantzig/){: target="_blank" rel="noopener noreferrer" }, Wired, 2001-12-01, checked 2026-07-20. Used to confirm the historical context connecting George Dantzig and the simplex method to real problems such as logistics, scheduling, and network optimization.
