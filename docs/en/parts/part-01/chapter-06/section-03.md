# P1-6.3 Where Probabilistic Judgment Is Used in AI

> Section ID: `P1-6.3`
> Version: `v2026.07.07`

Section 6.2 distinguished `uncertainty`, `probability`, and `stochastic`. This section turns that distinction into a more practical question: where in actual AI systems is probability used, and how should those numbers be read carefully?

Saying that AI uses probability does not mean it answers arbitrarily. It is closer to saying that when information is incomplete or several candidates remain possible, the system compares how plausible different outcomes are by using numbers.

In Part 1, this section fixes the baseline for how probability-like numbers are used in actual AI systems. Section 6.2 first fixed the vocabulary. Here the focus is on what role those numbers play in classification, prediction, generation, and decision making, and why they must not be read directly as the final answer or as the responsible decision itself.

## Scope of This Section

This section does not explain the mathematics of probability itself. Conditional probability, Bayes’ rule, and probability distributions return later in Part 2.

It also does not explain the full generation algorithm of LLMs. Generation settings such as temperature, top-p, and sampling return later in Part 6.

The baseline here is only this:

> probability is used in classification, prediction, generation, and decision making  
> but probabilistic output is not itself the final answer or the final responsible decision

## Goal of This Section

- Understand how probability estimates are used in classification.
- Understand that prediction tasks can involve not only one value, but also uncertainty around that value.
- Understand at an introductory level why generation is tied to choosing among candidates and why temperature appears there.
- Understand that probabilistic output is material for judgment, not the final decision itself.
- Build an intuition for why calibration, thresholds, and human review are needed.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| in classification, probability scores compare candidate plausibility | This reduces the mistake of reading a high score as immediate truth. | A score like 0.68 means one candidate was rated highest under the current setup, not that it is absolutely true. |
| in prediction and generation, uncertainty and candidate selection also matter | This prevents us from narrowing the role of probability to classification alone. | We should look not only at one number, but also at ranges, candidates, and selection process. |
| probabilistic output is not identical to the final business decision | This shows why policy, thresholds, and human review still matter. | Model scores are followed by service policy, cost judgment, and sometimes human review. |

A short role separation helps here:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| probability estimate | a number showing how plausible a candidate looks | the comparison basis in classification and prediction |
| threshold | a cutoff line that changes behavior | the line between automation, hold, and human review |
| calibration | checking whether a score can be read like an actual confidence level | used to judge how much to trust `0.80` |
| generation setting | a value that changes how output candidates are chosen | used for output variability control, such as temperature |
| decision making | choosing an action while combining model numbers with cost and policy | the stage that connects probability to service behavior |

## One View at a Glance

Probabilistic thinking appears in several positions inside AI systems:

| Where it appears | Example | What probability does there? | Main caution |
| --- | --- | --- | --- |
| classification | divide a support message into delivery, refund, or payment | compare the plausibility of candidate labels | the highest score is not automatically the truth |
| prediction | predict arrival time, demand, or price | express both a value and sometimes its uncertainty | one average number alone may be misleading |
| generation | choose the next token, sentence, or image candidate | control how one choice is made among many candidates | outputs may vary for the same input depending on settings |
| decision | choose automation, delay, or human review | connect probability to action under cost and policy | probability alone should not replace responsible judgment |

## Classification: Which Candidate Looks More Plausible?

Classification divides an input into one or more predefined candidates. For example, a support message may be classified like this:

| Candidate label | Probability estimate |
| --- | ---: |
| delivery inquiry | 0.68 |
| refund inquiry | 0.21 |
| payment inquiry | 0.08 |
| other | 0.03 |

This suggests that delivery is the most plausible candidate. But `0.68` does not mean `delivery is absolutely true`. It means that under the current input, data, model, and calculation method, delivery was scored highest.

Google’s Machine Learning Glossary explains that in multiclass classification, softmax computes probabilities for possible classes and that their sum becomes 1. scikit-learn also notes that in classification we often want not only a label but also the probability assigned to that label.

In practice, a service may then define thresholds:

| Condition | Handling |
| --- | --- |
| top score 0.90 or higher | automatic classification |
| top score between 0.60 and 0.90 | propose candidates and send to human review |
| top score below 0.60 | ask an extra question or hold the case |

The threshold is not just a technical value. It also depends on the cost of wrong automation, user inconvenience, safety needs, and legal responsibility.

## Probabilistic Output May Need Calibration

If a model outputs `0.80`, that does not guarantee the number can always be read as a real 80% confidence level. scikit-learn explains that some models estimate class probabilities poorly, and that in a well-calibrated classifier, `predict_proba` outputs can be interpreted more directly as confidence-like levels.

The safe reading of calibration starts with this question:

> if we collect the cases where the model said 0.80,  
> are roughly 80% of them actually correct?

That is the basic calibration question.

In this section, we do not calculate calibration. We only keep the key caution: a model’s probability output may not automatically equal a trustworthy real-world probability.

## Prediction: Sometimes a Range Matters More Than One Number

Prediction is not only about choosing labels. It can also mean predicting numbers such as delivery arrival time, next-month demand, server cost, or product price.

Suppose we predict delivery arrival time:

| Output style | Example | Interpretation |
| --- | --- | --- |
| point prediction | arrives tomorrow at 3 PM | gives one representative value |
| range prediction | likely to arrive between 1 PM and 6 PM tomorrow | shows uncertainty together with the value |
| probabilistic prediction | 60% before 3 PM, 90% before 6 PM | expresses time-dependent likelihood numerically |

Google’s glossary explains that a probabilistic regression model can generate both a predicted value and the uncertainty of that prediction.

This matters because two situations can share the same average prediction while having very different uncertainty:

| Situation | Average prediction | Uncertainty |
| --- | ---: | --- |
| same-day urban delivery | 4 hours | low |
| long-distance delivery during heavy rain | 4 hours | high |

The mean may be the same, but operational judgment should not be.

## Generation: Which Candidate Should Be Chosen?

Generative AI produces text, images, audio, code, and similar outputs. Even here, the system does not face only one possible continuation. It must choose among several candidates.

Suppose we continue this sentence:

> When AI handles incomplete information

Several next expressions are possible:

| Candidate | 느낌 |
| --- | --- |
| it uses probability | more explanatory |
| it waits for more evidence | focused on the judgment process |
| it compares several possibilities | more general |
| it asks for human review | focused on service operation |

Google’s Machine Learning Glossary describes temperature as a hyperparameter that controls the degree of randomness in model output. Higher temperature tends toward more varied output; lower temperature tends toward less varied output.

The key caution is the same as earlier chapters: temperature is not a learned model parameter. It is a setting used when running the model.

So the baseline here is:

> generation is connected to choosing one candidate among several  
> settings such as temperature control the variability of that choice

## Decision Making: Probability Is Material for Judgment, Not the Judgment Itself

In AI systems, probability is often connected to action choice:

| Model output | Possible action |
| --- | --- |
| delivery inquiry 0.95 | automatic delivery reply |
| delivery 0.68, refund 0.25 | propose candidates to an agent |
| all candidates below 0.40 | ask an extra question |
| risky transaction 0.82 | hold and review rather than auto-block immediately |

The important point is that probability does not replace decision making. Decisions also involve cost, risk, policy, user experience, and legal responsibility.

For example, in spam filtering, falsely marking a normal email as spam can be costly. In medical-support systems, missing a critical signal can be dangerous. In customer-support automation, low-confidence auto-replies can increase user dissatisfaction.

So probabilistic output should be read with questions like:

> what cost appears if this number is wrong?  
> where is human review needed?  
> who sets the threshold, and under what responsibility?

## The Same Number Means Different Things in Different Contexts

Even a number like `0.70` changes meaning with context:

| Context | Possible meaning of `0.70` | Caution |
| --- | --- | --- |
| message classification | score for the delivery-inquiry candidate | check whether it is calibrated |
| image classification | probability of a specific class | its meaning can shift if data distribution changes |
| delivery prediction | likelihood of arriving within a certain time | the conditions and prediction range must be read together |
| generation | relative likelihood during candidate selection | it does not guarantee output quality or factuality |

So when we see a probabilistic number, the first question should always be:

> probability of what?

Probability numbers do not carry meaning by themselves. They have to be read inside a task, data source, model, calibration condition, threshold, and responsibility structure.

## What to Remember from This Section

Probabilistic judgment in AI is used widely across classification, prediction, generation, and decision making. But the probabilistic output is not the final answer. It is material for judgment.

> uncertain input arrives  
> the model expresses the plausibility of several candidates numerically  
> the system decides action by combining those numbers with policy  
> when needed, the case moves to human review

Those four lines form the baseline that prevents us from reading `probability number -> direct truth`.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- scikit-learn, [1.16. Probability calibration](https://scikit-learn.org/stable/modules/calibration.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
