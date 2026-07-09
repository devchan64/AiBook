# P2-6.3 The Intuition of Gradient Descent

> Section ID: `P2-6.3`
> Version: `v2026.07.09`

P2-6.1 introduced optimization as candidate search. P2-6.2 turned wrongness into loss. Now the next question becomes concrete: once we have a number to reduce, how do we actually move the model values?

## Scope of This Section

This Section introduces `gradient descent`, `gradient`, `learning rate`, `update`, and `iteration` through intuition. It does not fully derive update formulas or detailed optimizer variants.

## Central Question

Why does learning move little by little from the current position instead of jumping to the answer in one step?

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| gradient descent | repeated method that moves toward lower loss | central method here |
| gradient | local direction in which loss increases | clue for movement direction |
| learning rate | step size of one movement | size of the step |
| update | replacement of old parameter values with new ones | one movement result |
| iteration | repeating the same adjustment loop | what makes learning procedural |

## One Loss-Curve View

![Flow of gradient descent moving in small steps toward lower loss on a loss curve](../../../assets/part-02/chapter-06/gradient-descent-loss-curve-en.svg)

The key intuition is simple:

1. read the local direction
2. move against it
3. repeat with a controlled step size

## Why the Mountain Metaphor Helps, but Only Partly

The common “walking downhill” metaphor is useful at first, but the important point is not that we see the entire landscape. We usually read only the local slope, move a little, and check again.

## Perspective to Keep

- Gradient descent is repeated local adjustment, not one-step perfection.
- The gradient gives the uphill direction, so descent moves the other way.
- Learning rate controls how large one movement should be.

## Short Check

- Can you explain why gradient descent is repetitive?
- Can you explain why the move goes against the gradient?
- Can you explain learning rate as step size?
- Can you explain why a correct direction can still fail if the step size is poor?

## Sources and References

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
