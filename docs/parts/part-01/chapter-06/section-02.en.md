# P1-6.2 Distinguishing Probability, Uncertainty, and Stochastic Processes

> Section ID: `P1-6.2`
> Version: `v2026.07.12`

Section 6.1 showed why some problems are difficult to handle with explicit rules alone. When information is incomplete, observations are unstable, and several outcomes remain possible, AI has to deal with uncertainty.

This section separates three expressions that are often mixed:

> uncertainty = the state of not knowing for sure  
> probability = the numerical language used to express that uncertainty  
> stochastic = a process or property that includes probabilistic variation in the process itself

These are connected, but they are not the same thing.

In Part 1, this section fixes the baseline distinction among `uncertainty`, `probability`, and `stochastic process`. Section 6.1 first fixed the problem conditions that require those terms. Here we set the vocabulary needed to read those conditions. Search and heuristics return in P1-7, and fuller probability formulas return in Part 2 and Part 4.

## Why This Distinction Is Needed

The sentence `AI answers probabilistically` looks simple on the surface, but it actually splits into several different questions:

| Question | Connected concept |
| --- | --- |
| would the judgment change if more information were observed? | uncertainty, evidence |
| how much should we trust the number 0.70 produced by the model? | probability, calibration |
| why do results vary slightly even when the same action is repeated? | stochastic process |
| is missing knowledge the same thing as the world itself being variable? | epistemic uncertainty, aleatoric uncertainty |

Hüllermeier and Waegeman explain that uncertainty is a central methodological issue in machine learning, and that the distinction between aleatoric and epistemic uncertainty becomes increasingly important as practical deployment and safety demands grow. We do not go deeply into those two categories here. It is enough to keep the sense that uncertainty itself also has kinds.

The three baseline questions are:

> is this a kind of not-knowing that decreases if we observe more?  
> is this a kind of variation that remains even when we repeat?  
> do the model’s numbers match real-world frequencies well?

## Scope of This Section

This section does not go deeply into probability formulas. Conditional probability, Bayes’ rule, and probability-distribution calculations return in Part 2 and Part 4.

It also does not explain LLM generation in detail. Sampling, temperature, top-p, and next-token prediction return later in Part 6.

Here we set only the vocabulary baseline needed to read AI documents.

## Goal of This Section

- Understand uncertainty as a state of not knowing.
- Understand probability as the numerical language used to express and update uncertainty.
- Understand stochastic as a property of a process that includes probabilistic variation.
- Avoid treating random, nondeterministic, and stochastic as if they were all the same.
- Set a translation baseline so that `uncertainty`, `probability`, and related Korean expressions do not collapse into one.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| uncertainty is the state of not yet knowing | This prevents it from being mixed directly with numerical probability. | Understand it as ignorance before a number is assigned. |
| probability is the numerical language that expresses that ignorance | This is the starting point for reading model scores and uncertainty numerically. | See it as a tool for comparing which candidate is more plausible. |
| stochastic means the process itself contains variation | This reduces the mistake of using uncertainty, probability, and randomness as one word. | Understand that not only results, but the process itself may vary. |

A short role separation is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| uncertainty | not knowing | the state before a numerical expression |
| probability | number | the numerical expression of that state |
| stochastic process | varying process | a process whose behavior includes probabilistic variation |
| random | arbitrary selection or randomness | a word that must not be used too loosely |
| nondeterministic | result not fixed to one outcome | not always the same as probabilistic |

## Uncertainty Is the State of Not Knowing

`Uncertainty` means a state where some fact, state, or outcome cannot be stated with certainty.

| Situation | What is uncertain? |
| --- | --- |
| customer-support message | whether the real intent is delivery or refund |
| sensor input | whether the measured value matches the real distance |
| medical diagnosis | whether symptoms alone identify the cause |
| delivery forecast | whether it will arrive tomorrow or be delayed |

Poole and Mackworth explain that agents in the real world do not know everything and must update beliefs from observations. The Stanford Encyclopedia of Philosophy entry on AI also notes that purely logic-based approaches cannot always determine truth or falsity for every proposition, because ignorance, physical indeterminacy, and ambiguity often require probabilistic handling.

> uncertainty = a state that cannot yet be stated with confidence

Uncertainty is not itself a number. It is the problem state before the numerical expression.

## Probability Is the Numerical Language of Uncertainty

Probability is the mathematical language used to handle uncertain states. Poole and Mackworth explain probability as a calculus of belief that can be updated when new information arrives.

Suppose a support-message classifier produces the following scores:

| Candidate | Score |
| --- | ---: |
| delivery | 0.70 |
| refund | 0.20 |
| other | 0.10 |

That number does not mean `delivery is absolutely true`. It is closer to saying that, given the model’s information and criteria, delivery currently looks more plausible.

Poole and Mackworth describe probability as a number between 0 and 1, where 0 corresponds to believing something false and 1 to believing it true. A value in between does not mean the fact is partially true. It means the agent does not know for sure whether it is true or false.

> uncertainty: we do not know whether this is delivery or refund  
> probability: we express it as delivery 0.70, refund 0.20, other 0.10

So probability is not uncertainty itself. It is a way to express, compare, and compute with uncertainty.

## How Much Can We Trust a Number Like 0.70?

If a model assigns `0.70`, that does not automatically mean the number always matches a 70% real-world frequency. scikit-learn explains that in classification, people often want not only class labels but also probabilities, yet some models estimate class probabilities poorly.

That raises the question of calibration:

> if we collect the cases where the model said 0.70,  
> are roughly 70% of those cases actually correct?

A `well-calibrated classifier` makes it more reasonable to read predicted probabilities as confidence-like numbers. For example, if a classifier repeatedly outputs values around 0.80 for many binary-classification samples, we can check whether the positive class actually occurs in roughly 80% of those cases.

So in this section, a score like `delivery 0.70` should be read cautiously:

| Hasty reading | Safer reading |
| --- | --- |
| delivery is 70% true | under the current data and model criteria, delivery was scored at 0.70 |
| the model said 70%, so we can trust it | we should separately check whether that model’s probability output is calibrated |
| 0.70 is an absolute trust level | its meaning depends on data, model, and evaluation method |

## Evidence Is Observed Information That Updates Belief

Poole and Mackworth describe observed information as `evidence`, and explain the perspective of updating prior probability into posterior probability based on that evidence.

In the support-message example:

| Stage | Example |
| --- | --- |
| prior judgment | from `tracking does not work` alone, delivery seems likely |
| additional evidence | payment logs show duplicate payment |
| updated judgment | this may not be a simple delivery issue; payment must also be considered |

We do not compute Bayes’ rule here. The important point is simply that as new observation arrives, the plausibility of different conclusions can change.

> when observation changes,  
> the plausibility of different conclusions can also change

## Stochastic Means the Process Includes Probabilistic Variation

`Stochastic` is often translated simply as `probabilistic`, but it is not identical to `probability`.

| English expression | Meaning used here | Central idea |
| --- | --- | --- |
| probability | probability | a number or distribution expressing uncertainty |
| probabilistic | probabilistic | using probability in expression or computation |
| stochastic | stochastic process or stochastic property | a process, action, or outcome includes probabilistic variation |

Poole and Mackworth explain that actions can behave as stochastic processes. For example, a robot may overshoot a target slightly when moving, and teaching some material to a student does not guarantee the student will learn it every time.

The useful intuition is:

> even if we repeat the same action,  
> the same result is not guaranteed every time

Examples:

| Situation | Why it can be read as stochastic |
| --- | --- |
| robot movement | the same command can lead to slightly different positions because of friction, sensors, or floor condition |
| user response | showing the same recommendation does not guarantee the same click behavior |
| LLM response generation | the same prompt can produce different wording depending on generation settings and sampling |

But `stochastic` does not mean `completely arbitrary`. It means the variation follows some probabilistic rule or distribution.

## Random, Stochastic, and Nondeterministic Should Be Used Carefully

In Korean, words corresponding to `random`, `stochastic`, and `nondeterministic` are often mixed. In AI writing, it is safer to separate them.

| English expression | Preferred meaning here | Caution |
| --- | --- | --- |
| random | arbitrary or random choice | do not use it as if it meant pure chaos |
| stochastic | a process that includes probabilistic variation | a process may vary without being structureless |
| nondeterministic | not fixed to one result for the same state and input | it may not explicitly specify a probability distribution |
| probabilistic | expressed or computed using probability | may be the modeling language for a stochastic process |

For example, if an LLM can answer differently to the same prompt, it is imprecise to say `it answers any which way`. The safer wording is:

> depending on generation settings and sampling, the output may vary

## A Note on Korean Wording

In Korean writing, words corresponding to `uncertainty` and `indeterminacy` sometimes appear together. In this book, for general AI explanation, `uncertainty` is preferred.

The reason is practical: `uncertainty` works well for missing information, incomplete observation, and predictive uncertainty. The other word can be read with stronger associations to specific fields such as physics. So the baseline here is:

| Korean-side category | English expression | Use standard in this book |
| --- | --- | --- |
| uncertainty | uncertainty | use in general AI contexts for states of not knowing |
| probability | probability | use for the numeric expression of that state |
| probabilistic or stochastic | probabilistic, stochastic | use when explaining probability-based modeling or varying processes |

The goal is not to force language mechanically, but to help readers avoid mixing several levels together.

## The Same Example Again

Take the support sentence again:

> I ordered yesterday, but tracking still does not work.

| Perspective | Explanation |
| --- | --- |
| uncertainty | we do not know whether the real cause is delivery delay, system update delay, or a payment issue |
| probability | with current information, we may express it as delivery 0.70, payment 0.20, other 0.10 |
| evidence | extra observations such as order time, payment log, or carrier integration state |
| stochastic process | delivery time or user response may vary probabilistically even under similar conditions |

Keeping this distinction helps us read the sentence `AI behaves probabilistically` more carefully. Some part concerns uncertainty, some part concerns numerical probability, and some part concerns the stochastic nature of a process.

## Checklist

- You can explain `uncertainty` as a state of not knowing rather than as a number.
- You can explain `probability` as the numerical language used to express and update uncertainty.
- You can explain that `evidence` is observed information that updates a judgment.
- You can explain `stochastic` as the property that a process or action includes probabilistic variation.
- You can explain why `random`, `stochastic`, `nondeterministic`, and `probabilistic` should not be treated as the same word.
- You can explain why general AI discussion should prefer `uncertainty` over collapsing several different ideas into one vague label.
- You can distinguish whether a sentence is talking about a state of not knowing, a numerical expression, or a property of a process.
- You can distinguish not-knowing that may shrink with more observation from variability that remains in the process itself.

## Sources and Further Reading

- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Eyke Hüllermeier, Willem Waegeman, [Aleatoric and Epistemic Uncertainty in Machine Learning: An Introduction to Concepts and Methods](https://arxiv.org/abs/1910.09457){: target="_blank" rel="noopener noreferrer" }, 2019-10-21, accessed 2026-06-22.
- scikit-learn, [1.16. Probability calibration](https://scikit-learn.org/stable/modules/calibration.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
