# P2-6.1 What Does Optimization Search For?

> Section ID: `P2-6.1`
> Version: `v2026.07.09`

After summarizing data and estimating from samples, the question changes again: how do we search for a better value among several candidates?

## Scope of This Section

This Section introduces optimization as a problem of comparing candidates using objectives and constraints. It does not go deep into detailed convex-optimization algorithms.

## Central Question

Why is optimization not just calculation, but a structured search among candidates?

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| optimization | problem of finding a better value | starting point of the chapter |
| candidate | possible choice not yet fixed | thing being compared |
| criterion | standard for “better” or “worse” | evaluation rule |
| constraint | condition that must be respected | realism boundary |
| minimization / maximization | direction of decrease or increase | basic optimization goal |

![Optimization flow comparing candidates under objectives and constraints](../../../assets/part-02/chapter-06/optimization-search-loop-en.svg)

## The Shared Toy Scene for Chapter 6

The chapter keeps one shared example: study time `x` and quiz score `y`, then several line candidates `y = ax + b`. This makes optimization easier to read as candidate comparison rather than abstract math.

## Perspective to Keep

- Optimization is a search problem among candidates.
- “Best” only makes sense under a stated objective and stated constraints.
- Model learning also becomes easier to read once it is treated as “searching for better parameters.”

## Short Check

- Can you explain optimization as a search among candidates?
- Can you distinguish candidate, objective, and constraint?
- Can you explain why “optimal” does not simply mean “perfect in every sense”?

## Sources and References

- Google for Developers, [ML Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
