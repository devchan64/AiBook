# P1-7.2 What Does a Heuristic Reduce?

> Section ID: `P1-7.2`
> Version: `v2026.07.19`

Section 7.1 showed that when the search space grows, methods that inspect every candidate quickly hit computational limits. Now we move to the next question:

> if we cannot inspect every candidate,  
> by what standard do we decide what to inspect first and what to cut down?

In Part 1, this section fixes the basic distinction among `heuristic`, `heuristic function`, and `good-enough solution`. Section 7.1 first established why search spaces create computational limits. Here the focus shifts to what kinds of standards reduce that burden. The boundary between heuristics, probabilistic models, and learned models is clarified further in 7.3.

> a heuristic is not a formula that guarantees the right answer; it is an empirical standard that decides which candidates to inspect first

## Etymology: A Way of Helping Discovery

The origin of the word helps. The Online Etymology Dictionary explains that `heuristic` comes from the Greek `heuriskein`, meaning to find or discover, and is related to the same root as `eureka`.

So it is safer to read heuristic not as `a trick that already knows the answer`, but as `a method that helps us find the answer`.

> a heuristic does not mean the answer is already known  
> it means we have a way to decide where to look first

This fits naturally with the idea of search from 7.1. When the search space is too wide, heuristics direct attention toward places that look more promising.

## The Idea: People Do Not Inspect Every Case

One historical reason heuristics became central in AI is the question, `How do people actually solve problems?`

Early AI research by Allen Newell and Herbert A. Simon did not view computers merely as fast calculators. It also asked how human problem solving could be simulated. The ACM material on Newell explains that he encountered George Pólya’s lectures on mathematical problem solving and recognized that people do not have enough time or processing capacity to solve every problem through fully exhaustive algorithms. Instead, they use simplified rules that support `selective search`.

The same flow connects with Simon’s work. Nobel Prize and ACM materials describe his idea that real people and organizations often make boundedly rational choices rather than fully optimizing choices, and therefore accept solutions that are satisfactory enough under limits of time and information.

At an introductory level, the safest summary is:

> the heuristic idea is less about romantic claims that a computer thinks like a person  
> and more about building selective standards that avoid inspecting every candidate under limited time and information

This way of thinking led into early AI systems like Logic Theorist and the General Problem Solver. They tried to reduce the gap between current state and goal state and to inspect promising directions first rather than enumerate everything blindly.

So heuristic should not be understood merely as `guessing` or `a handy shortcut`. In early AI, it was an answer to this problem:

> if exhaustive search is unrealistic,  
> by what standard should a computer reduce candidates the way people do in constrained problem solving?

This section does not calculate the technical conditions of A*, greedy best-first search, admissible heuristics, or consistent heuristics.

It also does not explain heuristics as if they were the same thing as probabilistic or learned models. That difference is handled in 7.3.

The focus here is narrower:

> when the search space is too large,  
> heuristics are standards that reduce candidate count, time, memory, and evaluation burden

## Goal of This Section

- Understand a heuristic as an empirical standard that guides search or judgment toward promising directions.
- Explain how heuristics reduce candidate count, time, memory, and evaluation burden.
- Understand a heuristic function as a way of assigning an estimate or score to candidates.
- Understand why `good-enough solutions` matter.
- Remember that heuristics can speed judgment without guaranteeing the optimal solution.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a heuristic is not an answer formula but a standard for deciding what to inspect first | This prevents us from reducing heuristics to mere `tips` or `guesswork`. | Understand it as a standard that reduces search even without guaranteeing the answer. |
| heuristics reduce time, memory, and evaluation burden | This shows how computational limits connect to practical problem solving. | Read it as a device for avoiding inspection of every candidate. |
| good-enough solutions matter in reality | This moves us away from the idea that only optimal solutions matter. | Understand that usable answers under time limits are often more important than perfect ones. |

A short role separation is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| heuristic | an empirical standard that decides which candidates to inspect first and which to cut down | the core idea for reducing search |
| heuristic function | a standard that assigns an estimate of promise to a candidate | a concrete form for computing priority |
| good-enough solution | a usable answer found under limited time | the practical goal in many real problems |
| optimal solution | the best answer among all candidates | the ideal goal that heuristics do not always guarantee |
| verification | the step that checks what a heuristic may have missed | the safeguard against trusting fast judgment too much |

## A Heuristic Is a Standard for Avoiding Full Inspection

Poole and Mackworth explain that people often do not find optimal solutions for every problem, but instead search for good-enough solutions. They also explain that when the search space alone is not enough, extra knowledge about special cases can guide solution finding; they call this `heuristic knowledge`.

So at an intuitive level:

> when there are too many candidates,  
> a heuristic is a standard that makes more promising candidates inspected first

Take route finding. Straight-line distance to the destination seems useful. Moving toward the destination looks reasonable. But in real roads there may be rivers, bridges, mountains, construction zones, or one-way streets.

So straight-line distance can be a useful hint without guaranteeing the true shortest path.

| Perspective | Explanation |
| --- | --- |
| what helps | it lets us delay candidates that move too far away from the destination |
| what it reduces | number of candidates to inspect, comparison time |
| what it risks | it may miss a better route if real constraints are ignored |
| attitude needed | do not treat the heuristic as truth; verify it |

## What Does a Heuristic Reduce?

Heuristics are not just `ways to guess quickly`. It becomes clearer if we ask what exactly they reduce.

| What is reduced | Meaning | Example |
| --- | --- | --- |
| candidate set | instead of checking every candidate, inspect some first | delay roads that move far away from the destination |
| search depth | stop overly long paths early | move to a different candidate after repeated failure |
| time | reduce time spent on comparison and calculation | check the most promising candidates first |
| memory | reduce the number of intermediate states that must be stored | keep only some paths instead of every path |
| evaluation burden | reduce the cost of deciding what is better | assign a simple score and prioritize by it |
| rework cost | reduce the need for large fixes later | leave weakly grounded sentences out of the first draft |

The key distinction is:

> a heuristic can reduce search  
> but it does not guarantee that the best answer always remains among the reduced candidates

## Modern Heuristic Examples

Heuristics did not disappear in modern AI. They continue to appear wherever a system cannot inspect every candidate and needs some way to reduce or prioritize them.

These examples do not all belong to the same technical layer. Some are human-defined operating standards, some are development strategies, and some are automated evaluation procedures. What they share is candidate reduction or prioritization.

| Modern situation | Heuristic-like standard | What it reduces | What still needs verification |
| --- | --- | --- | --- |
| operating a classification model | set a threshold that separates automatic handling from human review | number of requests people must inspect, automation candidates | false positives, false negatives, threshold-side effects |
| model development | start with simpler models and drop candidates with poor validation scores | model candidates, tuning time, experiment cost | overfitting to the validation set |
| hyperparameter tuning | narrow the range of learning rate, model size, or regularization instead of trying everything | combination explosion, training time | a better candidate may exist outside the searched range |
| generative-AI review | remove unsupported, out-of-scope, or repetitive sentences from drafts | number of sentences to review, rewrite cost | fluent but ungrounded text |
| agent workflow | decide the order of search, file reading, build, and test tools | unnecessary tool calls, repeated work | omissions caused by bad sequencing |
| program search | as in FunSearch, automatically evaluate generated programs and reuse high-scoring ones | program candidates, human comparison burden | whether the evaluation function matches the real goal |

Google’s Machine Learning Glossary explains that classification thresholds are human-chosen values that affect the numbers of false positives and false negatives. That threshold is not the model’s learned parameter. It is an operating standard for deciding which candidates are handled automatically.

FunSearch gives another modern example. It evaluates program candidates generated with help from an LLM and feeds higher-scoring ones back into later exploration. In the online bin packing problem, it found program candidates that used fewer bins than earlier human-designed heuristic rules in that setup.

The important point is not that modern AI removed heuristics. It is this:

> modern AI did not eliminate heuristics  
> it redistributed them into human-defined rules, validation criteria, evaluation functions, and automated search procedures

## A Heuristic Function Assigns an Estimate to Candidates

AI textbooks often explain heuristics through `heuristic functions`. The word `function` can sound technical, but the baseline reading here is simple:

> a heuristic function takes a candidate as input  
> and returns an estimate of how promising it looks

Using route finding:

| Candidate | Example heuristic estimate |
| --- | ---: |
| intersection A | 2 km straight-line distance to destination |
| intersection B | 5 km straight-line distance |
| intersection C | 9 km straight-line distance |

Then we may decide to inspect A before B or C. But the number is still not the exact travel time or final truth. A short straight-line distance may still hide blocked roads, while a longer one may lead to a faster highway.

So a heuristic function is better read as an `estimation function for search order`, not as an answer function.

## Why Good-Enough Solutions Matter

For very small problems, finding the optimal solution feels natural. But when candidates are too many or time is limited, real systems often need solutions that are good enough.

Suppose we choose a delivery route:

| Goal | Explanation |
| --- | --- |
| optimal solution | the shortest or cheapest route among all possible routes |
| good-enough solution | a route that satisfies service quality within the time limit |

This does not mean optimal solutions never matter. In safety-critical, medical, financial, or legal contexts, stronger verification is often required. But in many operational settings, `a verified usable answer now` matters more than `a perfect answer too late`.

That is where heuristics become meaningful:

> they do not guarantee perfection,  
> but they help us reach usable candidates under limited time and resources

## We Can Also See Heuristics in Familiar Work

Heuristics are not limited to route finding or algorithm design. Similar standards appear in familiar structuring work too. This is only an analogy to build intuition.

| Writing situation | Possible heuristic | What it reduces |
| --- | --- | --- |
| section topic is drifting | keep one central question per section | scope expansion, reader confusion |
| the explanation becomes too bold | hold claims that have no external grounding yet | error risk |
| a term may be misunderstood | write academic terms in Korean and English together | meaning confusion |
| content invades another chapter | move it to the next section or later chapter | domain leakage |
| too many examples accumulate | keep only examples that explain the core concept | excess length |

These standards do not guarantee the final best document, but they reduce the space of candidates and make later verification easier.

> heuristics do not replace verification  
> they reduce the scope that needs careful checking

## Risks of Heuristics

Heuristics are useful, but they also carry risk. To reduce search means that some candidates are inspected less or not at all.

| Risk | Explanation | Response |
| --- | --- | --- |
| missing the optimal solution | a better candidate may be dropped too early | sample and re-check some discarded cases |
| bias | past experience can tilt judgment in one direction | compare against other criteria |
| overconfidence | fast judgment may be mistaken for the right answer | record failure cases |
| context mismatch | a standard that worked in one problem may fail in another | state the conditions where it applies |
| missing evidence | a plausible explanation may look like fact | separate sources and verification from quick filtering |

Heuristics accelerate thought, but fast thought can still be wrong. The more we use heuristics, the more explicit verification standards matter.

## Heuristics Are Not the Same as Rules, Probability, or Learning

Heuristics are easily mixed with neighboring ideas. Here is the working separation:

| Distinction | Central role | Difference from heuristics |
| --- | --- | --- |
| rule | explicitly states action under conditions | heuristics often give priority or direction rather than a final condition |
| probabilistic model | expresses uncertainty with numbers and distributions | a heuristic may look numeric without being a calibrated probability |
| optimization | searches for a better solution under an objective function | heuristics may support optimization but are not optimization itself |
| learning | adjusts criteria or representations from data | heuristics may be hand-built or learned, but the concept is different |
| model | the structure that turns input into output | a heuristic may be one part of a model or system, not the whole model |

This separation leads directly into 7.3, especially the boundary between heuristics and probabilistic models.

## Checklist

- Explain a heuristic as an empirical standard for reducing candidates and deciding priority.
- Explain that heuristics reduce candidate count, time, memory, and evaluation burden.
- Explain a heuristic function as a standard that attaches an estimate to candidates.
- Distinguish a good-enough solution from an optimal solution.
- Explain why heuristics are not the same thing as the answer, a probabilistic model, or a learned model.
- Explain why the more we rely on heuristics, the more explicit verification standards matter.
- Explain both what a heuristic reduces and what it does not guarantee.
- Explain where heuristic functions, good-enough solutions, and verification standards connect.

## Sources and Further Reading

- Douglas Harper, [Online Etymology Dictionary, heuristic](https://www.etymonline.com/word/heuristic){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- ACM A.M. Turing Award, [Allen Newell](https://amturing.acm.org/award_winners/newell_3167755.cfm){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- ACM A.M. Turing Award, [Herbert A. Simon](https://amturing.acm.org/award_winners/simon_1031467.cfm){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Nobel Prize, [Herbert Simon - Facts](https://www.nobelprize.org/prizes/economic-sciences/1978/simon/facts/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., 3.1 Problem Solving as Search](https://artint.info/3e/html/ArtInt3e.Ch3.S1.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google DeepMind, Alhussein Fawzi and Bernardino Romera-Paredes, [FunSearch: Making new discoveries in mathematical sciences using Large Language Models](https://deepmind.google/discover/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/){: target="_blank" rel="noopener noreferrer" }, 2023-12-14, accessed 2026-06-23.
