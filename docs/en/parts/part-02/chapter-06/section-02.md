# P2-6.2 Loss Functions and Objective Functions

> Section ID: `P2-6.2`
> Version: `v2026.07.09`

P2-6.1 treated optimization as candidate comparison. This Section asks what that comparison becomes inside model learning.

## Scope of This Section

This Section introduces `loss function`, `objective function`, `error`, `mean loss`, and `metric`. It does not list every problem-specific loss design.

## Central Question

How is “the model is wrong” turned into a numeric criterion that learning can actually move?

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| loss function | function that turns wrongness into a number | entry point for learning criteria |
| objective function | full criterion minimized or maximized in training | target of optimization |
| error | difference between prediction and truth | ingredient behind many losses |
| mean loss | combined loss across many samples | whole-dataset tendency |
| metric | human-facing comparison measure | should not be confused automatically with loss |

## One Shared Scene

Chapter 6 keeps the same study-time and quiz-score example. A candidate line predicts values. The loss function measures how badly that candidate misses the real scores.

## Loss Is Not Automatically the Same as Metric

The number used to update the model and the number used to report model quality can be related, but they do not have to be identical.

## Perspective to Keep

- Loss turns wrongness into a numeric signal.
- Objective is the broader criterion that training tries to improve.
- Metric and loss should be distinguished instead of merged automatically.

## Short Check

- Can you explain a loss function as a way to numericize wrongness?
- Can you explain how mean loss differs from one-sample loss?
- Can you explain why a reporting metric and a training loss are not always the same?

## Sources and References

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
