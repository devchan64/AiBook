# P2-4.1 Revisiting How We Learned Differentiation

> Section ID: `P2-4.1`
> Version: `v2026.09.08`

Differentiation calculates how quickly the output changes when the input changes slightly. The slope of a tangent and instantaneous velocity describe this rate of change in different situations.

## Tangents, Derivative Values, and Derivative Functions

If you have studied differentiation, you may recall tangent slope, instantaneous rate of change, instantaneous velocity, the derivative at a point, and the derivative function. These expressions are connected as follows.

| Expression | What it refers to |
| --- | --- |
| Slope of a tangent | The instantaneous rate of change at a point on a graph |
| Derivative at a point | A number representing the instantaneous rate of change at a particular input |
| Derivative function | A function that gives the derivative value for each input |
| Instantaneous velocity | The instantaneous rate of change of position with respect to time |

A line through two points on a graph is a secant. We can calculate its slope, then consider the limit of that slope as one point approaches the other. If this limit exists, it is the derivative at that point and the slope of the tangent.

## Position, Velocity, and Acceleration

If an object moving along a straight line changes position from 10 m to 16 m in one second, its average velocity over that interval is `(16 − 10) / 1 = 6 m/s`. Reducing the observation interval to find the rate of change of position at an instant gives instantaneous velocity.

If velocity changes from `6 m/s` to `8 m/s` in one second, average acceleration is `(8 − 6) / 1 = 2 m/s²`. Differentiating position with respect to time gives velocity; differentiating velocity gives acceleration. Velocity is distinct from speed, the rate of change of distance traveled.

## Rates of Change and Accumulation

Imagining a line traced by a moving point, or a solid built by stacking cross sections, connects to the intuition of accumulation. For example, adding `0.1 m` of height to a column with a constant cross-sectional area of `2 m²` increases its volume by `0.2 m³`.

Here, `volume increase / height increase = 0.2 / 0.1 = 2 m²`. Stacking cross sections describes accumulated volume; calculating how volume changes with height gives the cross-sectional area.

## Changes in Order Volume and Delivery Time

Suppose delivery records are simplified as follows.

| Daily orders | Average delivery time |
| --- | --- |
| 100 | 24 hours |
| 110 | 26 hours |

Order volume increased by `10 orders`, and average delivery time increased by `2 hours`. The rate of change between the two records is `2 hours / 10 orders = 0.2 hours/order`. Over this interval, each additional daily order corresponded to an average delivery-time increase of `12 minutes`.

This is the average rate of change between two records. It does not give the instantaneous rate at 100 daily orders. If other conditions, such as region or staffing, also changed, we cannot attribute the delivery delay solely to order volume.

## Checklist

- Can you say whether tangent slope, instantaneous rate of change, or instantaneous velocity comes to mind when you hear differentiation?
- When a formula comes to mind first, can you ask what change it describes?
- Can you explain the relationship between position, velocity, and acceleration through rates of change?
- Can you connect points, lines, areas, and volumes to the intuition of accumulation?
- Can you read differentiation as the question of how small changes affect the output, beyond memorizing formulas?
- Can you connect tangent, derivative at a point, and instantaneous velocity through one question about change?
- Can you distinguish the average rate between two records from the instantaneous rate at a point?

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-20. This reference supports the standard introduction to differentiation through tangents, secants, derivatives, velocity, and instantaneous rate of change.
