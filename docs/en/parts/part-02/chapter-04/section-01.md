# P2-4.1 Rereading How We Learned Differentiation

> Section ID: `P2-4.1`
> Version: `v2026.07.09`

Chapter 3 recovered the shapes of data and model computation. Chapter 4 changes the question again: when values change, how should we ask about that change?

Differentiation is easy to lose as a stack of formulas. This Section starts somewhere simpler. It reconnects old memories such as slope, tangent line, speed, and acceleration to one shared question:

How much does the output change when the input changes a little?

## Scope of This Section

This Section rebuilds the entrance to differentiation through intuition and question framing. It does not yet focus on formal derivative calculation drills.

## Connection Flow to Hold

| Stage | Question to hold | Next link |
| --- | --- | --- |
| there is change | what is changing? | P2-4.2 rate of change and slope |
| compare the size of change | how much does output change when input changes? | P2-4.3 derivative and gradient |
| read direction of change | which way makes the value larger or smaller? | P2-6.1 to P2-6.3 loss and gradient descent |
| connect to learning | how should parameters move to reduce loss? | Part 4 backpropagation and optimizers |

## Terms to Fix First

| Term | Very short meaning | Role in this Section |
| --- | --- | --- |
| differentiation | reading how values change | starting point of the chapter |
| change comparison | looking at input and output change together | core perspective here |
| instantaneous rate of change | speed of change near one point | bridge to later Sections |
| tangent line | line showing local slope on a graph | familiar old image |
| memory recovery | rebuilding forgotten ideas as questions | practical purpose of this Section |

## Why This Entrance Matters

In AI learning, later explanations keep asking:

- if the parameter changes a little, what happens to the loss?
- which direction lowers the loss?
- how strong is the local change signal?

Those questions are easier once differentiation is recovered as a change-reading tool rather than a formula list.

## Perspective to Keep

- Differentiation begins as a change question.
- Old school memories such as slope and tangent line belong to the same question.
- This entrance matters because learning also depends on reading change.

## Short Check

- Can you restate differentiation as a question about change?
- Can you connect slope, tangent line, and instantaneous change?
- Can you explain why this question later matters for loss and learning?

## Sources and References

- OpenStax, [Calculus Volume 1](https://openstax.org/details/books/calculus-volume-1){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
- Khan Academy, [Differential calculus](https://www.khanacademy.org/math/differential-calculus){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
