# P1-7.1 Search Space and Computational Limits

> Section ID: `P1-7.1`
> Version: `v2026.07.12`

Chapter 6 dealt with incomplete information and probabilistic judgment. Now we turn to a different kind of difficulty. Some problems are hard because information is missing, but some are hard because there are simply too many possible choices.

The central question here is:

> when there are too many possible solutions,  
> what is it that AI can no longer afford to look at exhaustively?

To understand `heuristics`, we first need a baseline understanding of `search` and `search space`.

In Part 1, this section fixes the basic distinction among `search`, `search space`, `computational limit`, and `exhaustive search`. Chapter 6 focused first on uncertainty and probability. Here the focus shifts to a different kind of difficulty: problems where there are so many candidates that we cannot realistically inspect all of them. The concrete role of heuristics is developed next in 7.2.

The contrast between Chapters 6 and 7 can appear side by side even inside the same service:

| Scene inside the same service | Core difficulty | First approach to recall |
| --- | --- | --- |
| estimating why a delivery is delayed | information is incomplete and several causes remain possible | uncertainty, probability, evidence update |
| deciding today’s delivery route | there are too many candidate routes to compare all of them | search, pruning, heuristics |

The key is to separate `problems that are hard because we do not know what is true` from `problems that are hard because there are too many candidates to inspect`.

> once the number of candidates explodes, the problem is no longer only defining the right answer, but finding a path to it

## Scope of This Section

This section does not implement specific search algorithms. We do not calculate breadth-first search, depth-first search, or A* here.

It also does not fully explain heuristic functions yet. Heuristics are handled directly in 7.2.

The focus here is only this:

> when the number of possible states and choices grows too large,  
> a method that inspects every case quickly hits a limit

## Goal of This Section

- Understand `search` as the process of looking through possible candidates to find a solution.
- Distinguish `state`, `action`, `goal`, `path`, and `cost` at an introductory level.
- Understand why a large `search space` creates `computational limits`.
- Explain why `exhaustive search` becomes unrealistic in many real problems.
- Prepare for why heuristics are needed in 7.2.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| search is the process of moving through candidates to find a solution | This helps us see AI problems not only as calculation but as structured choice. | Keep the intuition of route finding: we choose one direction after another. |
| search space is the whole set of possible states and choices | This explains why the number of candidates can suddenly become very large. | Understand that the number of cases can grow quickly as steps increase. |
| computational limits mean we cannot inspect every case realistically | This connects directly to why heuristics are needed next. | Understand that exhaustive search may be possible in theory but too slow in practice. |

At this stage, a short role split is enough:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| search | process of following possible candidates toward a solution | the large frame for problem solving |
| search space | the whole set of possible states and choices | the frame that explains why candidate count grows |
| state | one current form of the problem | shows where the search currently is |
| action | a choice that changes state | the unit that creates the next candidate |
| path | the sequence of connected states | the actual trail toward a solution |
| cost | the standard used to compare better paths | distance, time, resource use, and so on |
| computational limit | the point where we cannot realistically inspect all candidates | the reason heuristics become necessary |

## Search Is a Way of Solving Problems by Looking Through Candidates

Poole and Mackworth explain that the problem of finding a way for an agent to achieve a goal can be abstracted as finding a path from a start node to a goal node in a graph. *Artificial Intelligence: A Modern Approach* also places problem solving and search among the first core topics of introductory AI.

Poole and Mackworth summarize the importance of this perspective directly:

> “Search underlies much of AI.”  
> — David L. Poole, Alan K. Mackworth, *Artificial Intelligence: Foundations of Computational Agents*

Here we read search as:

> starting from the current state,  
> follow available choices until a path to the goal is found

For route finding:

| Element | Route-finding example |
| --- | --- |
| state | current location |
| action | move along the next road |
| goal | arrival at the destination |
| path | the sequence of roads and intersections traversed |
| cost | distance, time, toll, or energy |

This structure is not limited to route finding. It can also be used for scheduling, puzzle solving, game moves, code-edit sequences, or comparing document-outline candidates.

## Search Space Is the Whole Set of Possible States and Choices

The `search space` is the overall structure of states and actions that can be considered while solving a problem.

Take a simple example:

> decide what to do in the morning  
> first choices: exercise, reading, checking email  
> next choices: commute, prepare for a meeting, buy groceries

If there are 3 choices at the first step and 3 more at the next, there are already 9 combinations. When the number of stages increases, the number of candidates grows quickly.

| Number of stages | Possible combinations when each stage has 3 choices |
| ---: | ---: |
| 1 | 3 |
| 2 | 9 |
| 3 | 27 |
| 4 | 81 |
| 5 | 243 |
| 10 | 59,049 |

The important intuition is simple:

> even if each step adds only a few choices,  
> the total number of combinations can grow very quickly

That is why the idea `why not just check them all?` quickly becomes difficult.

## Why Exhaustive Search Becomes Hard

`Exhaustive search` means inspecting every possible case without omission. For small problems, it can be a useful reference point. But once the number of candidates grows, time and memory run out quickly.

Think about problems like these:

| Problem | Why the number of candidates grows |
| --- | --- |
| delivery routing | the order of stops becomes numerous |
| meeting scheduling | people, time windows, and room conditions interact |
| chess or Go | each move opens many next moves |
| document writing | many candidates exist for outline, sentences, examples, and evidence placement |
| model tuning | many combinations of model type, features, and hyperparameters exist |

Poole and Mackworth note that the difficulty of search lies at the heart of problem solving, and that there are problems where recognizing a solution is easy while finding one efficiently is hard.

That distinction matters:

> recognizing a correct solution may be easy  
> but finding a path to it may still be hard

## Computational Limit Does Not Just Mean the Computer Is Slow

`Computational limit` does not simply mean weak hardware. If the number of candidates grows too quickly because of the problem’s structure, then even a fast computer may fail to inspect all cases within realistic time.

| Distinction | Meaning |
| --- | --- |
| implementation is slow | code improvements may help |
| data is large | storage, transfer, or parallelism may help |
| search space explodes | the candidates themselves grow too quickly |
| the goal criterion is complex | it is hard even to evaluate what counts as a better solution |

Faster CPUs, GPUs, more memory, and parallel processing matter. But performance improvements do not eliminate every search problem, because the problem can grow faster than the available compute.

> a faster computer lets us look farther,  
> but it does not let us see every path

## Modern Examples: AlphaDev and FunSearch

The ideas of `search space` and `computational limit` are not only old textbook topics. They also appear in modern AI research.

AlphaDev is a vivid example of an enormous search space. It searched through combinations of assembly instructions to discover faster sorting algorithms. DeepMind described the difficulty using this phrase:

> “enormous number of possible combinations of instructions”  
> — Google DeepMind, *AlphaDev discovers faster sorting algorithms*

That line fits the intuition of 7.1 exactly: when the number of combinations becomes too large, checking every candidate becomes unrealistic.

FunSearch shows a slightly different case. Instead of searching directly over final answers, it searches over functions or programs that can produce answers.

> “functions written in computer code”  
> — Google DeepMind, *FunSearch: Making new discoveries in mathematical sciences using Large Language Models*

This does not mean all AI problems are reinforcement-learning problems or that all LLM systems simply search training data. The point is narrower:

> in modern AI too, search space still matters  
> and the thing being searched can vary by problem: states, paths, instruction combinations, functions, or programs

## Search Deals with a Different Difficulty than Probability

Chapter 6 focused on uncertainty and probability. Search begins from a different kind of difficulty.

| Difficulty | Core question | Representative approach |
| --- | --- | --- |
| uncertainty | we do not know what is true | probability, evidence update, calibration |
| search space | there are too many possible candidates | search, pruning, heuristics |
| learning | it is too hard for people to write all judgment criteria explicitly | data-driven models |

In real problems these three can appear together. Route planning may involve many candidate paths, uncertain traffic conditions, and learned arrival-time estimates. But at the introductory level it is safer to distinguish them first:

> not knowing the truth,  
> having too many candidates,  
> and needing to learn judgment criteria  
> are connected, but they are not the same difficulty

## A Document-Structure Example

Search is not limited to route finding and games. It also appears in organizing document structure.

| Element | Example in document-structure work |
| --- | --- |
| state | the current outline and section arrangement |
| action | add a section, change order, strengthen evidence, revise phrasing |
| goal | a structure that readers can follow easily |
| cost | reader confusion, weak evidence, excess length, writing time |
| constraint | evidence-centered writing, section-boundary preservation, terminology consistency |

The number of possible outline combinations can become very large. Since we cannot build and compare every candidate, we usually fix a large structure first, then narrow the field by using central questions and scope constraints.

This is not a full search algorithm, but it is a useful analogy for understanding why candidate reduction becomes necessary.

## Why Heuristics Become Necessary Next

Once the search space grows too large, we cannot inspect every candidate. Then the next question appears:

> which candidates should be inspected first?  
> which candidates can be abandoned early?  
> where should we stop and call the solution good enough?

That question leads directly to heuristics. Poole and Mackworth explain that the difficulty of search, together with the fact that people can solve some search problems efficiently, suggests that computer agents should also use extra knowledge about special cases to guide solution finding. They call such extra guidance `heuristic knowledge`.

So the next section treats heuristics as:

> an empirical standard that does not guarantee the exact answer,  
> but reduces the amount of search

## What to Remember from This Section

Search is a problem-solving method that looks through possible candidates to find a path to the goal. As the search space grows, methods that try every candidate quickly hit computational limits.

So AI ends up asking:

> if we cannot inspect every candidate,  
> what should we inspect first,  
> what should we reduce,  
> and where should we stop?

That question leads directly into the heuristic discussion in 7.2.

## Checklist

- Explain search as the process of looking through possible candidates to find a solution.
- Explain `state`, `action`, `goal`, `path`, and `cost` with a route-finding example.
- Explain that the number of combinations can grow quickly as the search space expands.
- Explain why exhaustive search may work for small problems but hit computational limits for large ones.
- Distinguish the difficulties of uncertainty, search space, and learning.
- Explain why heuristics become necessary once the search space grows too large.

## When to Recall This View First

Recall this section when a problem feels difficult not because truth is unclear, but because the number of possible candidates has become too large to inspect comfortably.

- when you need to explain why route choice, scheduling, game play, or outline design turns into a search problem
- when you need to separate `not knowing what is true` from `having too many candidates`
- when you need to prepare the intuition for why heuristics and pruning come next

## Sources and Further Reading

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., Chapter 3 Searching for Solutions](https://artint.info/3e/html/ArtInt3e.Ch3.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- David L. Poole, Alan K. Mackworth, [3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google DeepMind, Daniel J. Mankowitz and Andrea Michi, [AlphaDev discovers faster sorting algorithms](https://deepmind.google/discover/blog/alphadev-discovers-faster-sorting-algorithms/){: target="_blank" rel="noopener noreferrer" }, 2023-06-07, accessed 2026-06-23.
- Google DeepMind, Alhussein Fawzi and Bernardino Romera-Paredes, [FunSearch: Making new discoveries in mathematical sciences using Large Language Models](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/){: target="_blank" rel="noopener noreferrer" }, 2023-12-14, accessed 2026-06-23.
