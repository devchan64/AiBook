# P2-2.3 Limits and the Intuition of Change

> Section ID: `P2-2.3`
> Version: `v2026.07.09`

P2-2.2 reread sigma as compressed notation for repeated addition. Now we move to another notation that often feels unfamiliar:

\[
\lim_{x \to a} f(x)
\]

A limit is different from simply plugging in a value. It asks where the output of a function is heading as the input gets closer and closer to some value. In AI documents, the limit itself appears less often than the intuition it supports: rate of change, derivatives, gradients, and optimization.

## Scope of This Section

The key question is this: why is looking at a tendency near a value different from direct substitution, and why does that distinction lead into rate of change?

So this Section fixes four places first.

- What does it mean for something to approach something else?
- How is a limit different from substitution?
- How do small changes show the behavior of a function?
- Why does the idea of a limit lead into derivatives and optimization?

## A Small Bridge Example First

Take:

\[
f(x) = x^2
\]

Look at values near `x = 2`.

| Input `x` | Function value `f(x)` | Difference from the earlier value |
| --- | ---: | ---: |
| 2.0 | 4.0000 | - |
| 2.1 | 4.4100 | 0.4100 |
| 2.01 | 4.0401 | 0.0401 |
| 2.001 | 4.004001 | 0.004001 |

The first thing to see is that as `x` gets closer to 2, `f(x)` gets closer to 4. But one step later, you naturally want to ask not only where it is heading, but how quickly it is changing. That next question leads directly into rate of change and then derivatives.

## Three Criteria

| Criterion | Why it matters | Understanding needed here |
| --- | --- | --- |
| A limit looks at the tendency near a point rather than only the point itself | It prevents substitution and limits from being mixed together | Understand that you first ask what is approaching what |
| A limit observes what happens nearby, not just whether you can plug in one value | It creates the intuition for reading behavior near special points | Understand that substitution and limits are different actions |
| Limits matter in AI because derivatives use them to read how small changes affect results | It builds the bridge into optimization language | Understand limits as preparation for rate of change |

## A Simple Limit Example

\[
\lim_{x \to 2}(x + 1) = 3
\]

That case works by direct substitution. But not every limit does.

\[
\lim_{x \to 1}\frac{x^2 - 1}{x - 1}
\]

If you substitute `x = 1` directly, the denominator becomes 0. So you simplify:

\[
\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1}
\]

Near 1, this behaves like `x + 1`, so:

\[
\lim_{x \to 1}\frac{x^2 - 1}{x - 1} = 2
\]

That shows the main point: a limit is not always “the exact value after plugging in.” It is the tendency of the expression near that value.

## Small Changes Reveal How a Function Behaves

With

\[
f(x) = x^2
\]

and `x = 2`,

\[
f(2) = 4
\]

If you move `x` a little:

\[
f(2.1) = 4.41
\]

the input changed by `0.1`, and the output changed by `0.41`. That gives the starting intuition of rate of change:

\[
\frac{f(2.1) - f(2)}{2.1 - 2}
\]

If you keep shrinking the interval, the bridge into derivatives becomes clearer.

| Interval | Input change | Output change | Rate of change |
| --- | ---: | ---: | ---: |
| 2.0 -> 2.1 | 0.1 | 0.41 | 4.1 |
| 2.0 -> 2.01 | 0.01 | 0.0401 | 4.01 |
| 2.0 -> 2.001 | 0.001 | 0.004001 | 4.001 |

As the interval becomes smaller, the rate of change gets closer to 4.

## A Limit Leads into Derivatives

The bridge can be stated in one line:

\[
\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
\]

You do not need the formal derivative rules yet. What matters is the bridge: a limit is the notation that lets us ask what happens when a change becomes very small.

## Perspective to Keep from This Section

Limits read a tendency near a value. They are different from direct substitution. And the reason they matter in AI is that they prepare you to read how small changes in input or parameters affect outputs and loss.

## Short Check

- You can explain a limit as observing what happens near a value.
- You can distinguish substitution from a limit.
- You can explain convergence as values getting closer to one value.
- You can connect limits to rate of change.
- You can explain why that connection matters for derivatives and optimization.

## Sources and References

This Section organizes the minimum intuition for rereading limits in Part 2 and does not directly quote external material.
