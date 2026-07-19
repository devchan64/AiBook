# P2-6.1 What Does Optimization Search For?

> Section ID: `P2-6.1`
> Version: `v2026.07.19`

In Chapter 5, we summarized data into numbers, estimated the whole from samples, and checked mean and variance through code. Now the question changes.

Is it enough just to calculate a value? How do we find a better value among several candidates? By what standard can we say that something is good?

This question feels a little unfamiliar. Mean or variance gives a result as soon as we compute it. But finding a `better value` is different. The answer is not given from the start, and we have to compare several candidates.

This is the point where the word `optimization` appears. Here we treat optimization as a name for holding onto the question, "If we choose a value, which one makes things better?"

Here we reorganize `optimization`, `candidate`, `criterion`, `constraint`, and `minimization / maximization`. If Chapter 5 was about reading data and estimation, this Section reorganizes the problem of finding a better value among several candidates as the entrance to learning.

Rather than calculating optimization algorithms here, we focus on rereading learning as the problem of searching for a better value. If you secure the feel of candidates, criteria, constraints, and minimization here, then when you later meet loss function, gradient descent, and optimizer, the problem scene appears before the formulas do.

## The Shared Common Scene to Hold First

In Chapter 6, one small example is reused across three Sections. Suppose four students have the following study time `x` and quiz score `y`.

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
- In the later Sections, we call this criterion `loss`, and the method of moving the line toward the side where that loss decreases is called `gradient descent`.

| What to secure in this Section now | The question that follows immediately next | Where it is used again later |
| --- | --- | --- |
| The feel that optimization is the problem of finding a good value | In P2-6.2, we look at loss function and objective function. | It is used again in Part 3 model selection and Part 4 learning-procedure explanations. |
| The way of separating candidate, criterion, and constraint | In P2-6.3, we look at how gradient descent moves toward a better candidate. | It becomes the basis when reading discussions of optimizers and hyperparameters. |
| The perspective of reading learning as a parameter-adjustment problem | In `P2-6.2` and `P2-6.3`, it continues into the meaning of moving in the direction that reduces loss. | It reappears in Part 4 backpropagation and in the tuning and evaluation context of Part 5. |

In textbook language, optimization is the problem of finding the value that minimizes or maximizes an objective function within given variables and constraints.

But if we see only this definition first, it is difficult. So here we do not erase the definition; we look together at the scene that makes the definition necessary.

You do not need to know the exact formulas or algorithms yet. The purpose here is to build the feel that instead of writing the answer directly, we place candidates, compare them by a criterion, and move toward the more favorable side.

![Optimization flow for comparing candidate values under evaluation criteria and constraints to find a better candidate](/AiBook/assets/part-02/chapter-06/optimization-search-loop-en.svg)

## Scope of This Section

This Section introduces `optimization` as a way of thinking needed before entering AI learning. This Section first closes what we will call a good value, and how to read candidates, criteria, and constraints separately.

Loss function and objective function continue immediately in P2-6.2. How to move a candidate toward the side where loss decreases returns in P2-6.3. Loss by problem type continues in P4-4.1 and P4-4.2, and backpropagation and optimizers reconnect in P4-5.1, P4-7.1, and P4-7.2. Here we organize the key scene that should come to mind when you hear the word optimization.

Here we focus on the following questions.

- Why does optimization become necessary?
- What are candidate, criterion, and constraint?
- Does the word optimal mean perfect?
- Why is optimization necessary in AI learning?

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| optimization | the problem of searching for a better value | the starting point of the whole chapter |
| candidate | a value that can be tried and is not yet fixed | the object of comparison |
| criterion | the scale that calculates good and bad | the ruler used to evaluate a candidate |
| constraint | a condition that must be respected | the device that reflects the limits of reality |
| minimization / maximization | the direction of reducing or increasing | the basic goal of optimization |

## Goals of This Section

- You can explain optimization not as writing the answer directly, but as the perspective of finding a better candidate.
- You can distinguish `candidate`, `criterion`, and `constraint`.
- You can explain `minimization` and `maximization` as the basic directions.
- You can explain that `optimal` does not always mean the perfectly complete answer in reality.
- You can explain the perspective that in AI learning, instead of writing the rule directly, the model adjusts values in the direction that decreases or increases a criterion.

## Three Criteria

| Criterion | Why it matters | Needed level of understanding here |
| --- | --- | --- |
| Optimization is the problem of finding a better choice among possible candidates | It shows that a comparison criterion is needed before the calculation itself. | It is enough to understand it as the problem of placing candidates and finding a better value. |
| Objective and constraint decide what counts as good | It makes clear that the word optimal is not an absolute quality, but a conditional judgment. | Understand that comparison is possible only when criterion and constraint exist together. |
| AI learning is also the process of finding better parameters that reduce loss | It connects optimization not to abstract mathematics, but to the entrance of the learning procedure. | Secure the perspective of reading learning as a value-adjustment problem. |

## Start from the Scene of Finding a Good Value

If you try to understand `optimization` from mathematical terminology from the beginning, it feels stiff. First think of a `scene of finding a good value`. For example, finding the shortest travel route, buying goods at the lowest cost, choosing the line with the shortest waiting time, or finding the setting that gives the highest score.

We do not need to call all these examples mathematical optimization. But they are good for learning the feel of optimization. What they share is that there are several candidates, there is a criterion for judging which is better, and in reality there are also constraints because we cannot choose anything at all.

In mathematics and AI, people try to turn this flow into a computable form. That is when the word `optimization` appears in earnest.

The earlier study-time and score table has the same structure. We can make many candidate lines, but to know which line is better, we need a criterion that calculates the difference from the actual score. In other words, a `good line` is not determined by eyeballing; it is determined on top of a comparison criterion.

## Reread the Definition in Simpler Terms

Let us bring back the textbook-style definition we saw above. Optimization is the problem of finding the value that minimizes or maximizes an objective function within given variables and constraints.

This sentence contains four terms.

| Term | Meaning to understand first |
| --- | --- |
| variable | a value we can try changing |
| constraint | a condition that must be respected |
| objective function | the criterion that calculates good and bad |
| minimize / maximize | the direction we want to reduce or increase |

The reason the definition feels difficult is not only that the formulas are hard. It is also because the act of turning the word `good` into a number, fixing the range of possible choices, and then finding a better value inside that range is itself unfamiliar.

## Separate Candidate, Criterion, and Constraint

Optimization does not start by holding the `answer` from the beginning. First there is a `candidate`. A candidate is not the fixed answer yet. It is a value we can try while asking, "What if it were this one?"

For example, suppose we want to draw one line and fit it to data.

```text
y = ax + b
```

Here the line changes depending on how we set `a` and `b`.

```text
a = 1, b = 0
a = 2, b = -3
a = 0.5, b = 4
```

Each combination is one candidate. Optimization is the attempt to find, among such candidates, the value that matches the criterion better.

If we read it through the common scene of Chapter 6, it becomes the task of changing `a` and `b` to find the line that better explains the study-time and score data. The loss function in the later Section turns `which candidate fits better` into a number, and gradient descent explains `how to move toward the side where that number decreases`.

Even if there are many candidates, we cannot compare them without a `criterion`.

| Situation | Candidate | Criterion |
| --- | --- | --- |
| choosing a travel route | several routes | is the travel time shorter? |
| purchasing goods | several products | is the cost lower? |
| choosing a waiting line | several lines | is the waiting time shorter? |
| choosing model settings | several setting values | is the evaluation score better? |

Reality also has `constraints`. For example, the cost must not exceed 100,000 won, response time must finish within 1 second, memory must not exceed a certain capacity, laws and policies must be obeyed, or the user experience must not be harmed.

So optimization is not simply about making one number as good as possible. It is the problem of looking at candidates, criteria, and constraints together.

## Many Fields Need This Kind of Thinking

Optimization is not a way of thinking used only in AI. Whenever `we want a good choice, but there are criteria and constraints`, a similar problem appears.

| Field | What we want to find | Criterion | Constraint |
| --- | --- | --- | --- |
| logistics | delivery routes | travel distance, time, cost | number of vehicles, time limits, delivery order |
| manufacturing | production plan | output volume, defect rate, cost | equipment capacity, inventory, due dates |
| advertising | budget allocation | conversion rate, sales, click-through rate | budget, exposure limits, policies |
| service operations | server-resource placement | response speed, stability, cost | server cost, traffic variation |
| search / recommendation | result ordering | clicks, satisfaction, relevance | diversity, safety, policies |
| machine learning | model parameters | loss, accuracy, evaluation score | data, computation, time |

At work, these questions appear like this.

- If we spend more cost, how much better does it become?
- Under the current criterion, what should be reduced?
- If we increase speed, does quality fall?
- If we increase accuracy, do cost or latency rise?
- What is the best choice that still respects the constraints?

These questions are hard to answer by writing the answer at once. We have to set the criterion, compare candidates, and check constraints while searching for a better choice.

## Historically, It Grew from Computable Choice Problems

Optimization is not a word that appeared suddenly with AI. In an older flow, it was closer to the problem, `how do we allocate limited resources among several options?`

For example, in war, logistics, production, and scheduling, important questions included which route to run with limited vehicles, which work to assign with limited staff, how much of which product to make with limited raw materials, and in what order to handle work within limited time.

These questions are not solved simply by `calculating harder`. There are too many candidates, and criteria and constraints exist together. So mathematics and computing tried to turn such problems into computable forms.

`Linear programming` is a representative historical example that shows this flow. We set an objective, add constraints, and then find the better value among the possible choices. George Dantzig's `simplex method` is often mentioned together with real problems such as logistics, scheduling, and network optimization.

Here we do not cover the calculation procedures of linear programming or the simplex method. What matters is the historical direction. Real-world choice problems were turned into calculation problems with criteria and constraints, then organized again into algorithms that search for better values, and that flow later connected to the problem of adjusting model values in AI learning.

So optimization can be understood not as `an AI-only technique`, but as an old computational way of thinking about finding a better value under criteria and constraints that entered AI learning.

## There Are Minimization and Maximization

Optimization problems are usually expressed in two directions. The direction of reducing a value when smaller is better is `minimization`, and the direction of increasing a value when larger is better is `maximization`.

For example, we usually want to reduce travel time, cost, error, and loss.

By contrast, values such as accuracy, revenue, and satisfaction are usually values we want to increase.

In AI learning, values we want to reduce appear often. We turn how different the prediction is from the actual value into a number, and then adjust the model values in the direction that reduces that number. You do not need to know that number exactly yet. In the next Section, we will see it again under the name `loss function`.

## Optimal Does Not Mean Perfect

The word `optimal` needs to be read carefully. By name alone it sounds like a perfect answer, but in practice that is often not the case.

Usually it means a better value found within a given range of candidates, for a given criterion, while respecting given constraints.

So when we look at an optimization result, we should ask the following together.

- By what criterion was it called optimal?
- Within what range of candidates was it found?
- What constraints were reflected?
- Were other real-world conditions left out?

This perspective carries directly into AI model evaluation too. Even if one model gets a high score on a certain benchmark, that does not mean it is optimal for every real-world problem. We have to keep asking, `good by what criterion?`

## AI Learning Can Be Seen as an Optimization Problem

In AI learning, people often do not write the rule directly one by one. Instead, they adjust the values the model has so it fits the data better. This is the unfamiliar point.

Learning can look like the following. First make a prediction, see how wrong it is, correct it a little, and then predict again.

If we write the flow a little more technically, the model predicts, calculates the difference between prediction and reality, adjusts its values in the direction that reduces that difference, and then predicts again.

This flow can be read from the perspective of optimization. It is okay if you do not fully understand it yet. For now, it is enough to secure only the connection that learning can be explained as a repeated process of searching for better values. Here the candidate is the current model parameter, the criterion is the number that shows how bad the prediction is, and the goal is to reduce that number.

There is one point to be careful about here. The `parameter` in this Section means a value the model adjusts through learning. Its context is different from the statistical `parameter` we saw in P2-5.3. A model parameter is a value adjusted in the learning process, while a statistical parameter is an actual property of the population.

Even with the same English word, we have to check the context. In the next Section, we organize this `number that shows how bad the prediction is` under the words `loss function` and `objective function`.

## View It Through a Case

### Case 1. How Should We Allocate the Advertising Budget?

Suppose a team wants to distribute this month's 10 million won advertising budget across search ads, banner ads, and retargeting ads. In practice, people usually first check things like `which channel did well last month`, `which one was expensive`, and `which one had low conversion`.

But even if we pour the whole budget into the channel that performed well, it does not immediately become the best choice. Search ads may already be saturated so extra budget has little effect, banner ads may have many impressions but low conversion, and retargeting ads may be efficient but have a limited number of reachable users.

In this scene, optimization is not `knowing the answer`. It is `comparing several candidate allocation plans through criteria and constraints`. The candidates are budget allocation plans, the criterion may be conversions or sales, and the constraints are conditions such as total budget, minimum spending by channel, and exposure policies. In other words, before we can say what a good allocation is, we first have to decide together `what we will count as good` and `what must not be exceeded`.

The confirmable result is to compare expected conversions and costs in a table across several allocation plans. For example, if Plan A gives 1,200 conversions at a cost of 9.8 million won, Plan B gives 1,150 conversions at a cost of 9 million won, and Plan C gives 1,260 conversions but exceeds the policy limit, then it becomes clear not just which number is largest, but which candidate is better while satisfying criteria and constraints together.

## Checklist

- You can explain optimization not as writing the answer directly, but as the process of finding a better candidate.
- You can distinguish `candidate`, `criterion`, and `constraint`.
- You can explain `minimization` and `maximization` with examples.
- You can explain that `optimal` does not always mean the perfectly complete answer in reality.
- You can explain AI learning as the process of adjusting model parameters to improve a criterion.
- You can explain the boundary that loss function and gradient descent are treated more concretely in the next Section.
- You can reread learning not as simple calculation, but as the problem of `finding a better value`.

## Sources and References

- Stephen Boyd, Lieven Vandenberghe, [Convex Optimization](https://web.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2004, checked 2026-07-19. Used to confirm the optimization-problem form that minimizes a value under an objective function and constraints.
- SciPy Developers, [Optimization and root finding](https://docs.scipy.org/doc/scipy/reference/optimize.html){: target="_blank" rel="noopener noreferrer" }, SciPy API Reference, checked 2026-07-19. Used to confirm the API context where optimization minimizes or maximizes objective functions and may include constraints.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 8: Optimization for Training Deep Models](https://www.deeplearningbook.org/contents/optimization.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-19. Used to confirm the deep-learning context in which parameters are adjusted by reducing a cost function.
- Gary Wolf, [The Optimizer](https://www.wired.com/2001/12/dantzig/){: target="_blank" rel="noopener noreferrer" }, Wired, 2001-12-01, checked 2026-07-19. Used to confirm the historical context connecting George Dantzig and the simplex method to real problems such as logistics, scheduling, and network optimization.
