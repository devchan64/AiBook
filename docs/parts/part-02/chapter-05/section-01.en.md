# P2-5.1 How Probability Represents Uncertainty as Numbers

> Section ID: `P2-5.1`
> Version: `v2026.09.08`

Probability expresses the chance of an event as a number between 0 and 1. AI uses probabilities for uncertain judgments, such as whether an email is spam or a picture contains a cat. A probability value must be distinguished from the decision based on it.

## Uncertainty and Probability

| Criterion | Why It Matters |
| --- | --- |
| Uncertainty is a state of not yet knowing | Before the number itself, we must understand what kind of state probability is expressing. |
| Probability expresses that state numerically | To compare possibilities and use them as judgment material, we need a language of expression. |
| AI repeatedly uses the language of probability | Because prediction and judgment are often not certain, possibility must be handled numerically. |

## Incomplete Information and Uncertainty

Uncertainty is not itself a number. Uncertainty is a state in which we do not yet know.

For example, think about the following questions.

- Will it rain tomorrow?
- Is this email spam?
- Is the object in this picture a cat?
- Will this user still use the service next month?

These questions are hard to determine completely right now. Information may be insufficient, the future may not have arrived yet, or observation may be incomplete.

Probability is the method of expressing this uncertain state numerically. For example, we may write a 70% chance of rain, a 95% chance of spam, an 82% chance of cat, or a 30% chance of churn.

Here, the number does not mean `we already know the answer`. It is the way of expressing, based on the current information and model, which side looks more plausible.

The chart below shows the intuition of expressing an uncertain state with a probability number between 0 and 1.

![A scale that expresses uncertainty with probability numbers between 0 and 1](/AiBook/assets/part-02/chapter-05/probability-uncertainty-scale-en.svg)

## Probability Values Between 0 and 1

Probability values lie between 0 and 1, inclusive. In finite-outcome models such as a die, `0` represents an impossible event and `1` a certain event. A probability of `0.5` means the event and its complement have equal probabilities.

Written as percentages:

```text
0.7 = 70%
0.2 = 20%
1.0 = 100%
```

The important point is that probability is not a number that directly says `good` or `bad`. Probability represents how likely some event is. For example, an 80% probability of rain means that the event of rain is likely. Whether that is good weather or bad weather depends on the purpose.

This distinction is also important in AI services. If a model outputs `spam probability 0.95`, that is a possibility score for the event of being spam. Whether to block the result, warn the user, or ask a person to review it is a separate decision layered on top of that score.

## Outcomes, Events, and Sample Spaces

To read probability, we must first separate three words.

| Term | English | Working Definition |
| --- | --- | --- |
| result | outcome | one individual result that can actually occur in a single trial |
| event | event | a bundle of results we care about |
| sample space | sample space | the set of all possible results |

Let us look at the situation of throwing one die. The possible outcomes are `1, 2, 3, 4, 5, 6`, and the sample space is `{1, 2, 3, 4, 5, 6}`. At that point, the event of getting an even number can be written as `{2, 4, 6}`.

If we assume the die is fair, the probability of getting an even number can be calculated as follows.

\[
P(\text{even}) = \frac{3}{6} = 0.5
\]

This calculation divides `the number of outcomes we care about` by `the number of all possible outcomes`. Here, the outcomes we care about are `2, 4, 6`, and the whole outcomes are `1, 2, 3, 4, 5, 6`, so the probability is `3 / 6`.

As in the chart below, an event is a bundle of the outcomes we care about inside the sample space.

![A die example showing the relationship among sample space, event, and outcome](/AiBook/assets/part-02/chapter-05/sample-space-event-outcome-en.svg)

But this method applies directly only when we can treat all outcomes as equally likely. In real data, outcomes are often not equally likely.

## Equally Likely Outcomes and Data-Based Estimates

Coins and dice appear often when probability is first taught for a simple reason. It is easy to list the possible outcomes, and if we assume a fair coin or die, it is easy to assume that each outcome has a similar chance.

For a coin, the possibilities are heads and tails. For a die, the possibilities can be listed simply as `1, 2, 3, 4, 5, 6`.

But real AI problems are more complex. We may think of questions such as whether a customer will churn, whether a sentence has positive sentiment, whether an image contains a pedestrian, or how risky a loan application is.

In these problems, it is hard to divide the possible outcomes into simple equal ratios. So we estimate possibility by using data, features, and models.

At that point, probability expands from `a problem where we can count like a die` into `a problem where we estimate possibility from observed data`.

## Long-Run Frequency and Degree of Belief

When understanding probability, two perspectives often appear.

One is long-run frequency. This is the perspective that repeats the same experiment many times, looks at the proportion with which some result appears, and interprets that proportion as probability.

If we throw a fair coin many times, we can expect the proportion of heads to come close to 0.5. This perspective is intuitive when explaining repeatable experiments.

The other is degree of belief. This is the perspective that expresses numerically how plausible some event seems based on the information currently available.

For example, a doctor may judge the possibility of a disease by looking at symptoms and test results, or a model may calculate the possibility that an email is spam by looking at its content. We cannot clone the same person infinitely and repeat the experiment, but we can still express possibility based on current information.

The long-run frequency perspective focuses on proportions observed in repeated trials. The degree-of-belief perspective focuses on judgments of plausibility given available information. The same problem can be explained differently under these perspectives.

In AI, both perspectives appear. We use frequencies observed in data, and we also use possibility scores based on the model's current information.

## New Evidence and Probability Updates

Bayes' rule calculates conditional probabilities using newly observed information. Under the degree-of-belief interpretation, it updates probabilities from before an observation to probabilities after it.

In English, it is often expressed with the following terms.

| Term | English | Working Explanation |
| --- | --- | --- |
| prior belief | prior belief | the possibility judgment we had before seeing new evidence |
| evidence | evidence | the observed information that changes that belief |
| posterior belief | posterior belief | the updated possibility judgment after seeing the evidence |

For example, suppose we initially judged that an email had a low chance of being spam. If new evidence appears such as many links, repeated suspicious phrases, and an unfamiliar sender, the judgment may change.

The chart below shows Bayes' rule not as a formula but as `a flow that updates belief with new evidence`.

```mermaid
--8<-- "assets/part-02/chapter-05/belief-update-flow-en.mmd"
```

The important word here is evidence. Evidence does not mean only `supporting material`. It is also used to mean the observed information that changes a probabilistic judgment. When the word evidence appears in AI documents, it helps to ask `what changed the judgment?`

## Reliability of Probability Values

If we read probability as `the answer`, misunderstanding occurs. For example, `70% chance of rain` does not mean that it must rain, `95% probability of spam` does not mean that it is absolutely spam, and `82% probability of cat` does not mean only that the model understood the word cat.

Probability is an expression for dealing with uncertainty. Whether that expression is trustworthy is a separate question. We must separately ask whether the data is sufficient, whether the data is biased, by what criterion the model calculated possibility, whether the probability score matches real frequency well, and what the decision threshold is.

## Class Probabilities in Classification Models

In many cases, AI does not operate only with certain rules. It finds patterns in data and, based on those patterns, calculates possibilities for new inputs.

For example, an image-classification model may give scores such as `cat: 0.82`, `dog: 0.12`, `rabbit: 0.04`, and `other: 0.02`.

These numbers show how plausible the model considers each candidate. If we choose the largest value, the prediction becomes `cat`. But inside the model, the distribution of possibilities among candidates is often more important than a single final answer.

## Probability, Uncertainty, and Stochastic Processes

Probability, uncertainty, and stochastic refer respectively to a numerical expression, a state of information, and a property of a process.

| Term | English | Distinction |
| --- | --- | --- |
| uncertainty | uncertainty | the state of not yet knowing |
| probability | probability | the language that expresses uncertainty numerically |
| stochastic | stochastic | the property that a process or action includes probabilistic variation |

For example, throwing a die can be seen as a stochastic process. It is hard to say in advance which face will come out, and when we repeat the process, the result can vary.

By contrast, the situation `I cannot confidently know whether this customer will churn because I have not fully observed the customer's mind` is a problem of uncertainty. If a model expresses this uncertainty with a number such as 0.3, that becomes probability.

So uncertainty is the state of not knowing, probability is the numerical expression of that state, and `stochastic` is the property that the process itself contains probabilistic variation.

## Spam Probability and Handling Rules

Suppose a mail classifier uses features such as subject, body, and sender to output spam probability `0.92`. With the following service rules, this message goes to the spam folder.

| Model spam probability p | Example handling rule |
| --- | --- |
| 0.99 ≤ p | Block automatically |
| 0.80 ≤ p < 0.99 | Move to the spam folder |
| 0.50 ≤ p < 0.80 | Keep in the inbox with a warning |
| p < 0.50 | Keep in the inbox |

If another service sets its automatic-blocking threshold at `0.90`, the same `0.92` results in blocking. The model's judgment is unchanged, but the handling rule changes the action. These thresholds are illustrative; actual thresholds account for costs such as blocking legitimate mail and missing spam.

The reliability of the probabilities also needs a separate check. If 100 messages scored around `0.9` are reviewed and only 60 are spam, the observed proportion is `60 / 100 = 0.6`. In this sample, the model has overestimated spam probability. Comparing more records across score ranges helps assess how well probability scores match observed proportions.

![Flow that separates an AI model's probability score from a service's operating decision rule](/AiBook/assets/part-02/chapter-05/probability-score-decision-threshold-en.svg)

## Checklist

- You can explain uncertainty not as the number itself, but as a state of not knowing.
- You can explain probability as the numerical language between 0 and 1 that expresses uncertainty.
- You can distinguish outcome, event, and sample space.
- You can calculate the probability of getting an even number from a fair die as \(3/6\).
- You can explain that probability is not always a number that guarantees the answer, but an expression based on the current information and model.
- You can distinguish long-run frequency and degree of belief.
- Even without calculating Bayes' rule, you can explain it as a flow that updates belief with new evidence.
- You can explain why probability, uncertainty, and stochastic should not be used as if they were the same word.
- You can explain that an AI model's output probability and the actual operating decision must be separated.
- You can connect probability not only to coin and die calculation, but also to AI prediction scores.

## Sources and References

- Barbara Illowsky, Susan Dean, [Introductory Statistics, 3.1 Terminology](https://openstax.org/books/introductory-statistics/pages/3-1-terminology){: target="_blank" rel="noopener noreferrer" }, OpenStax, checked 2026-07-20. Used to confirm probability, outcome, sample space, event, probabilities between 0 and 1, long-run relative frequency, and conditional probability terminology.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning, Chapter 3: Probability and Information Theory](https://www.deeplearningbook.org/contents/prob.html){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked 2026-07-20. Used as support for explaining probability theory as a framework for representing uncertainty in AI and machine learning.
