# P2-4.1 Revisiting How We Learned Differentiation

> Section ID: `P2-4.1`
> Version: `v2026.09.14`

Memories of learning differentiation can differ. You may recall drawing a tangent to a curve, hearing that differentiating position gives velocity, or learning that the derivative of `x²` is `2x`. These express the same calculation through a picture, a physical phenomenon, and symbols. If differentiation is new to you, connecting these three scenes can help you understand its meaning.

All three ask the same question: **How rapidly does the output change as the input changes?** In a graph, the input and output are the horizontal and vertical coordinates; in motion, they are time and position. Differentiation finds the instantaneous rate of change near a particular input value. The output itself and how rapidly it changes are different pieces of information.

## Differentiation Learned Through Velocity

Consider an object moving along a straight line. Take rightward as the positive direction from a reference point, measure time `t` in seconds, and position `s` in meters. Suppose its position follows the rule below. `s(t)` means the position at time `t`; the equation relates the numerical values of time and position measured in seconds and meters, respectively.

\[
s(t)=t^2
\]

| Time | Position |
| --- | --- |
| 1 s | 1 m |
| 2 s | 4 m |
| 3 s | 9 m |

From 1 to 2 seconds, position changes by `4−1=3m` in one second, so the average velocity is `3m/s`. From 2 to 3 seconds, position changes by `9−4=5m`, giving an average velocity of `5m/s`. Both intervals last one second, but the object moves farther in the later one. Its velocity is not constant.

What, then, is its velocity at exactly 2 seconds? `4m` is its position at that time, not its velocity. The earlier interval's average of `3m/s` and the later interval's average of `5m/s` each summarize an interval.

## Examining an Instant Through Short Intervals

Narrow the observation interval around 2 seconds. Average velocity is calculated as `change in position ÷ change in time`.

| Observation interval | Change in time | Change in position | Average velocity |
| --- | --- | --- | --- |
| 2 s → 3 s | 1 s | `9−4=5m` | `5m/s` |
| 2 s → 2.1 s | 0.1 s | `4.41−4=0.41m` | `4.1m/s` |
| 2 s → 2.01 s | 0.01 s | `4.0401−4=0.0401m` | `4.01m/s` |
| 1.9 s → 2 s | 0.1 s | `4−3.61=0.39m` | `3.9m/s` |
| 1.99 s → 2 s | 0.01 s | `4−3.9601=0.0399m` | `3.99m/s` |

As the interval after 2 seconds shrinks, average velocity approaches 4 through values such as `4.1` and `4.01`. From before 2 seconds, it approaches the same value through `3.9` and `3.99`. Calling the instantaneous velocity `4m/s` does not mean setting the time interval to zero and dividing by it. **We shrink the interval while keeping it nonzero and examine the value that average velocity approaches.**

The value approached in this way is called a limit. A few numbers in a table do not prove that a limit exists, but for `s(t)=t²`, continuing this process makes average velocity approach 4. This is the instantaneous velocity at 2 seconds. Average velocity over a sufficiently short interval approximates that instantaneous velocity; instantaneous velocity is the limit as the interval keeps shrinking.

## Differentiation Learned Through Tangents

Plot the same motion with time on the horizontal axis and position on the vertical axis. For example, `(2, 4)` means a position of 4 meters at 2 seconds. A **secant line** joins two points on the graph, and its slope is the vertical change divided by the horizontal change. Thus, on a position–time graph, a secant's slope is the average velocity over that interval.

Keep `(2, 4)` fixed and move the other point closer along the curve. The secant's slope changes as well. The values `5`, `4.1`, and `4.01` in the table are also the slopes of these secants. If the slope approaches a finite value, that value is the **tangent slope** at the point. Here, the tangent slope at 2 seconds is `4m/s`, the same value as the instantaneous velocity.

Remembering a tangent merely as “a line that meets a curve only once” can cause confusion with other curves. A tangent may meet the curve again elsewhere. What matters is its slope, which represents the direction of change of the curve near a particular point.

## Differentiation Learned Through Formulas

You may remember the rule that differentiating `x²` gives `2x`. For the motion whose position is `s(t)=t²`, this becomes `s′(t)=2t`. The prime symbol `′` denotes the function obtained by differentiation.

\[
s'(t)=2t,\qquad s'(2)=4
\]

`s′(2)=4` means an instantaneous velocity of `4m/s` at 2 seconds. It is the same value we found by shrinking the interval. `s′(t)=2t` gives the instantaneous velocity at other times as well: `2m/s` at 1 second and `6m/s` at 3 seconds.

| Expression | Meaning in this motion |
| --- | --- |
| Function `s(t)=t²` | Gives position when a time is supplied |
| Derivative at a point `s′(2)=4` | Instantaneous rate of change at the specific time of 2 seconds |
| Derivative function `s′(t)=2t` | Gives the instantaneous rate of change at each time |

The derivative at a point is a **number** for one input value; the derivative function is a **function** that supplies that number for each input. The formula gives the rate of change without repeating the shrinking-interval calculation each time. We must also interpret the result: substituting a time into this derivative function gives velocity, not position.

## Differentiating Position Twice

The velocity of this motion is `v(t)=2t`. From 1 to 2 seconds, it changes from `2m/s` to `4m/s`; from 2 to 3 seconds, it changes from `4m/s` to `6m/s`. Velocity increases by `2m/s` every second.

Acceleration, the rate of change of velocity, is `2m/s²`. In this example, velocity increases at a constant rate with time, so average acceleration is the same over any interval, and instantaneous acceleration has that value too. Differentiating position with respect to time gives velocity; differentiating velocity with respect to time gives acceleration.

| Quantity | Question | Unit |
| --- | --- | --- |
| Position | How far and in which direction is the object from the reference point? | `m` |
| Velocity | How rapidly does position change with time? | `m/s` |
| Acceleration | How rapidly does velocity change with time? | `m/s²` |

The object here moves rightward, but velocity can be negative when an object moves leftward and its position decreases. Speed measures how fast it moves without direction; in straight-line motion, speed is the absolute value of velocity. Distinguish velocity, the derivative of position, from speed, the rate of change of total distance traveled.

## Connecting Accumulation and Rate of Change

Building volume by stacking cross sections is a view of accumulation. If a column with a constant cross-sectional area of `2m²` gains `0.1m` in height, its volume increases by `2×0.1=0.2m³`. Adding `0.01m` in height increases its volume by `0.02m³`.

In either case, `increase in volume ÷ increase in height` is `2m²`. Stacking gives the volume accumulated with height; examining the rate of change gives the cross-sectional area, the volume increase per unit height. Differentiation is not limited to time as the input. Here, height is the input and volume is the output.

## What Order Records Can Tell Us

Suppose average delivery time was 24 hours with 100 orders per day and 26 hours with 110 orders per day. The average rate of change between the records is `(26−24)/(110−100)=0.2 hours/order`, or `12 minutes/order`.

This describes the change in average delivery time associated with the increase in orders across this interval. It does not mean every additional order necessarily adds 12 minutes. Orders are recorded as integers, so these two observations do not let us shrink the interval indefinitely. Discussing a derivative at a point requires additional assumptions, such as approximating the relationship between order count and delivery time with a continuous function. If region or staffing also changed, we cannot attribute the delay to order count alone.

Even if we know tangent and derivative formulas, we must separately judge which rates of change the observations support. What these records directly provide is the average rate of change between two observations.

## Exercise: Distinguishing Position and Velocity

For the same motion `s(t)=t²`, find the position at 3 seconds, average velocity from 2 to 3 seconds, and instantaneous velocity at 3 seconds. Include units and explain whether the three values represent the same quantity.

??? note "Calculation and explanation"
    Position is `s(3)=9m`, average velocity is `(9−4)/(3−2)=5m/s`, and instantaneous velocity is `s′(3)=2×3=6m/s`. Position is a coordinate at a time; average velocity is the rate of position change across an interval; instantaneous velocity is that rate at a particular time. Because the object is speeding up, its instantaneous velocity at the end of the interval exceeds its average velocity over the interval.

## Checklist

- Can you explain how a tangent diagram, a velocity explanation, and a differentiation formula describe the same rate of change?
- Can you explain the difference between setting a time interval to zero and shrinking it toward zero?
- Can you distinguish a position of `4m` from an instantaneous velocity of `4m/s`?
- Can you distinguish the derivative at one point as a number from the derivative function as a function of the input?
- Can you explain how the units differ for position, velocity, and acceleration?
- Can you explain why two delivery records cannot determine an instantaneous rate of change?

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }, accessed: 2026-09-14. Used to check explanations of secants and tangents, average and instantaneous velocity, and the derivative at a point. The motion tables, constant-cross-section column, and delivery examples were constructed for this section.
