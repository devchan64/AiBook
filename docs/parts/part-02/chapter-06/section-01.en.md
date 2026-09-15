# P2-6.1 What Does Optimization Search for?

> Section ID: `P2-6.1`
> Version: `v2026.09.15`

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

Here, study times `x` and actual scores `y` are fixed observations. We change the slope `a` and intercept `b` of the line. The slope gives the change in predicted score when study time increases by 1; the intercept gives the line’s predicted score at study time 0.

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

```mermaid
--8<-- "assets/part-02/chapter-06/optimization-search-loop-en.mmd"
```

The diagram applies two parameter combinations to the same data and compares their losses. Selecting the second candidate means it is better among the two compared; it does not establish that it is the best of all possible lines.

## Elements of an Optimization Problem

| Element | Meaning in the line-prediction example |
| --- | --- |
| Variable | The adjustable parameters `a, b` |
| Candidate | One combination of values, such as `a=10, b=45` |
| Objective function | The mean squared prediction error over the four points |
| Minimization | Searching for a candidate with a smaller mean loss |
| Constraint | Here, `a, b` are real numbers with no additional restrictions |

Optimization problems can be unconstrained. If a mandatory limit such as an advertising budget is imposed, however, a candidate that exceeds it cannot be selected even if its objective value is favorable.

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

Linear programming expresses the objective and constraints as linear expressions in the variables. Each variable is multiplied by a constant coefficient and the terms are added; variables are not multiplied together or squared. George Dantzig’s simplex method is a representative method for solving these problems.

Suppose `u, v` are the production volumes of two liquid products in liters. Profit per liter is 3 and 2 thousand won, and raw-material consumption is 2kg and 1kg, respectively. There are 8kg of raw material, and at most 3 liters of the first product can be sold. Fractional liters are allowed.

| Element | Expression | Meaning |
| --- | --- | --- |
| Objective | Maximize `3u + 2v` | Total profit in thousand won |
| Material constraint | `2u + v ≤ 8` | At most 8kg of raw material |
| Sales constraint | `u ≤ 3` | At most 3 liters of the first product |
| Production conditions | `u ≥ 0, v ≥ 0` | Production volumes cannot be negative |

With `u=3, v=2`, material use is 8kg and profit is 13 thousand won. With `u=0, v=8`, material use is also 8kg, but profit is 16 thousand won. Although the first product earns more per liter, it uses twice as much material, so the second plan is better under the material limit. The plan `u=3, v=3` earns 15 thousand won but is excluded because it requires 9kg of material.

## Minimization and Maximization

Optimization problems are usually expressed in two directions. The direction of reducing a value when smaller is better is `minimization`, and the direction of increasing a value when larger is better is `maximization`.

For example, we usually want to reduce travel time, cost, error, and loss.

By contrast, values such as accuracy, revenue, and satisfaction are usually values we want to increase.

In AI learning, we often want to reduce a value. We quantify how much predictions differ from actual values and adjust model values to reduce it. This criterion is the loss function.

## Optima Depend on Objectives and Scope

The word `optimal` needs to be read carefully. By name alone it sounds like a perfect answer, but in practice that is often not the case.

A global optimal solution is a candidate with the best objective value among all candidates satisfying the constraints. Whether the best result found by comparing only some candidates is a global optimum requires a separate check.

The material-allocation example also lets us establish an upper bound for every feasible candidate. Rewrite profit as `3u+2v = 2(2u+v)−u`. Because `2u+v≤8` and `u≥0`, profit cannot exceed 16 thousand won. The plan `u=0, v=8` attains that profit, so it is a global optimal solution under these conditions. The **optimal solution** is the production combination `(0, 8)`; the **optimal value** is its objective value, `16`.

So when we look at an optimization result, we should ask the following together.

- By what criterion was it called optimal?
- Within what range of candidates was it found?
- What constraints were reflected?
- Were other real-world conditions left out?

This perspective carries directly into AI model evaluation too. Even if one model gets a high score on a certain benchmark, that does not mean it is optimal for every real-world problem. We have to keep asking, `good by what criterion?`

## How Changing Parameters Changes Loss

The second candidate, `a=12, b=40`, predicts `52, 64, 76, 88`. These values fall below the actual scores by `3, 1, 4, 2`, respectively. Because all four predictions are low, we can keep the slope at `a=12` and raise the intercept `b`. Increasing the intercept by 2 raises every prediction by 2.

| Fixed slope a | Adjusted intercept b | Predictions | Mean squared error |
| --- | --- | --- | --- |
| 12 | 40 | 52, 64, 76, 88 | 7.5 |
| 12 | 42 | 54, 66, 78, 90 | 1.5 |
| 12 | 42.5 | 54.5, 66.5, 78.5, 90.5 | 1.25 |
| 12 | 43 | 55, 67, 79, 91 | 1.5 |
| 12 | 45 | 57, 69, 81, 93 | 7.5 |

At `b=42.5`, actual minus predicted scores are `0.5, −1.5, 1.5, −0.5`, with mean squared error `(0.25 + 2.25 + 2.25 + 0.25)/4 = 1.25`. Raising the intercept initially reduces loss, but continuing to raise it increases loss again. Optimization does not mean always increasing values or always changing them in the same direction.

Here, `a, b` are model parameters adjusted through learning. We keep observations fixed, change parameters, and recalculate predictions and loss. The candidate table shows comparison results but does not supply a rule for automatically choosing the next candidate. Distinguish the **optimization problem**, which specifies what to find, from the **optimization algorithm**, which searches for it.

The loss reduced here is the loss on these four students’ data. Whether predictions also improve for new students must be checked on separate data. Distinguish this use of model parameters from statistical parameters describing properties such as a population mean.

## Advertising Budget and Conversions

Suppose the objective is `maximize expected conversions`, subject to `total cost at most 10 million won`. All other conditions are equal, and only the following three plans are available.

| Plan | Total cost | Expected conversions | Within budget |
| --- | --- | --- | --- |
| A | 9.8 million won | 1,200 | Yes |
| B | 9 million won | 1,150 | Yes |
| C | 10.5 million won | 1,260 | No |

C has the most expected conversions but exceeds the budget and is excluded. A is selected over B because it has more conversions.

If the objective changes to `minimize cost per conversion`, A costs about `8,167 won/conversion` and B about `7,826 won/conversion`, so B is selected. The same candidates and budget can yield a different optimum when the objective changes. These are constructed estimates for comparison, not guarantees of actual conversions.

## Choosing Again After Conditions Change

Recalculate or select candidates under the following changed conditions. A change in budget or sales limits requires checking whether the previous choice remains valid.

1. Keeping `a=12`, what predictions and mean loss result from `b=41`? Is this better than `b=40`?
2. If the second liquid product also has a sales limit `v≤4`, which production volumes maximize profit with 8kg of material?
3. Which advertising plan is selected if the budget falls to 9 million won? Is any plan feasible at 8.5 million won? Limit candidates to the three plans in the text.

**Answers:** ① Predictions are `53, 65, 77, 89`; mean loss is `(4+0+9+1)/4=3.5`, below 7.5. ② `u=2, v=4` gives profit of 14 thousand won. Since `3u+2v = 1.5(2u+v)+0.5v ≤ 12+2=14`, no greater profit is possible. ③ Only B is feasible at 9 million won, and no plan is feasible at 8.5 million won. When no candidate meets the constraints, the candidate that exceeds a limit by the least cannot be selected as an optimal solution.

## Checklist

- You can explain optimization not as writing the answer directly, but as the process of finding a better candidate.
- You can distinguish `candidate`, `criterion`, and `constraint`.
- You can explain `minimization` and `maximization` with examples.
- You can explain that `optimal` does not always mean the perfectly complete answer in reality.
- You can explain AI learning as the process of adjusting model parameters to improve a criterion.
- You can reread learning not as simple calculation, but as the problem of `finding a better value`.

- You can separate what to compare from what to respect when candidates, criteria, and constraints appear mixed together.

- You can distinguish fixed data from adjustable parameters and calculate a candidate’s predictions and loss.
- You can change conditions and distinguish an optimal solution, an optimal value, and the absence of feasible candidates.

## Sources and References

- Stephen Boyd, Lieven Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2004, checked 2026-09-15. Sections 1.1–1.2 support the optimization formulation, linear objectives and constraints, and the simplex method. The liquid-product material-allocation numbers are an original example.
- SciPy Developers, [Optimization and root finding](https://docs.scipy.org/doc/scipy/reference/optimize.html){: target="_blank" rel="noopener noreferrer" }, SciPy API Reference, checked 2026-07-20. Used to confirm the API context where optimization minimizes or maximizes objective functions and may include constraints.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used to confirm the deep-learning context in which parameters are adjusted by reducing a cost function.
- Gary Wolf, [The Optimizer](https://www.wired.com/2001/12/dantzig/){: target="_blank" rel="noopener noreferrer" }, Wired, 2001-12-01, checked 2026-07-20. Used to confirm the historical context connecting George Dantzig and the simplex method to real problems such as logistics, scheduling, and network optimization.
