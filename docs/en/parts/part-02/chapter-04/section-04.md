# P2-4.4 Why Learning Needs Differentiation

> Section ID: `P2-4.4`
> Version: `v2026.07.09`

P2-4.3 treated derivatives and gradients as the language of change. This Section connects that language to model learning.

The conclusion is simple:

1. loss tells us how wrong the current model is
2. differentiation tells us which way to adjust parameters

## Scope of This Section

This Section introduces the relation among training, loss, parameters, and direction-of-adjustment information. It does not yet derive gradient descent formally.

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| learning | improving performance by changing parameters | broad background |
| loss | numeric summary of current wrongness | value we want to reduce |
| parameter | adjustable number inside the model | thing that actually moves |
| adjustment direction | which way would reduce the loss | key information provided by differentiation |
| backpropagation | efficient gradient computation procedure | later concept preview |

## Learning Is Parameter Adjustment

A model does not improve by seeing “wrong” as a word. It improves only if internal numeric values are changed.

## Loss Alone Is Not Enough

Loss can tell us the size of the problem, but not the direction of the fix.

That is the crucial point. A large loss says “this is bad,” but not “move this parameter up” or “move that parameter down.”

## Derivatives and Gradients Add Direction

Once we measure local change, we can ask:

- if this parameter increases slightly, does the loss rise or fall?
- which parameter direction looks more sensitive?

That is why differentiation is tied directly to learning.

## A Small Learning Scene

In a house-price model or score-prediction model, simply knowing that the prediction missed the target is not enough. The model needs a directional signal for how to change its parameters next.

## Perspective to Keep

- Learning means changing parameters.
- Loss gives severity, not direction.
- Differentiation gives directional information for adjustment.

## Short Check

- Can you explain why loss alone cannot complete learning?
- Can you explain what parameters are in this context?
- Can you explain how differentiation helps connect wrongness to adjustment?

## Sources and References

- Google for Developers, [ML Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
