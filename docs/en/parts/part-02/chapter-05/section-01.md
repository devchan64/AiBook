# P2-5.1 How Probability Represents Uncertainty as Numbers

> Section ID: `P2-5.1`
> Version: `v2026.07.09`

Chapter 4 used differentiation to read how values change. Chapter 5 needs another mathematical language: probability. Differentiation reads change. Probability reads uncertainty.

## Scope of This Section

This Section introduces `probability`, `uncertainty`, `event`, `outcome`, and `sample space` at an entry level. It does not cover full probability axioms, Bayes' rule, or detailed conditional-probability calculation.

## Central Question

Why do we need numbers for “not knowing,” and why is that number still not the same thing as the final decision?

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| probability | numeric expression of possibility | starting point of the chapter |
| uncertainty | state of not fully knowing | reason probability is needed |
| event | set of outcomes we care about | target of probability statements |
| outcome | one possible result | smallest unit in the setup |
| sample space | set of all possible outcomes | full frame containing events and outcomes |

## Uncertainty Comes First

Probability is not a guarantee number. It is a way to express uncertainty when information is incomplete, the future has not arrived yet, or observation is limited.

![A scale that expresses uncertainty with probability numbers between 0 and 1](../../../assets/part-02/chapter-05/probability-uncertainty-scale-en.svg)

## Probability Uses Numbers Between 0 and 1

At an entry level:

- `0` means “treated as impossible”
- `1` means “treated as certain”
- values in between express degrees of possibility

That still does not make probability a decision rule by itself.

## Outcome, Event, and Sample Space Must Be Separated

In a die example:

- outcomes: `1, 2, 3, 4, 5, 6`
- sample space: the full set `{1, 2, 3, 4, 5, 6}`
- event: for example, the even-number event `{2, 4, 6}`

![A die example showing sample space, event, and outcome](../../../assets/part-02/chapter-05/sample-space-event-outcome-en.svg)

## Probability Scores and Service Decisions Are Different

A model may output “spam probability 0.92,” but whether the system blocks, reviews, or allows the message is a policy decision layered on top of that score.

![Flow showing that a model probability score and a service action are not the same thing](../../../assets/part-02/chapter-05/probability-score-decision-threshold-en.svg)

## Perspective to Keep

- Probability is a language for uncertainty.
- Outcome, event, and sample space should be separated early.
- A probability score is not the same as the final service action.

## Short Check

- Can you explain uncertainty as a state rather than a number?
- Can you explain probability as a numeric expression of that state?
- Can you distinguish outcome, event, and sample space?
- Can you explain why model score and service decision are not identical?

## Sources and References

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
