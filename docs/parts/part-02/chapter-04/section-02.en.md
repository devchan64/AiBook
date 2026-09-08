# P2-4.2 Rate of Change and Slope

> Section ID: `P2-4.2`
> Version: `v2026.09.08`

Rate of change is output change divided by input change. Even for the same output change, the rate differs depending on how much the input changed.

## Amount of Change and Rate of Change

| Criterion | Why It Matters |
| --- | --- |
| Rate of change is output change relative to input change | Meaning appears only when we see not just the output, but also how much the input changed. |
| Slope is a visual expression of rate of change | It lets us quickly read increase, decrease, and sensitivity on a graph. |
| Average rate of change narrows into instantaneous rate of change | To read change near one point on a curve, the interval must be made smaller and smaller. |

## Output Change and Input Change

Rate of change is a way of seeing how much one value changes according to another.

The simplest example is distance over time.

1. We traveled 60 km in 1 hour.
2. The change in time is 1 hour.
3. The change in distance is 60 km.
4. So the rate of change is `60 km / 1 hour`, that is, 60 km/h.

Written as a formula, it is the following.

\[
\text{rate of change} = \frac{\text{change in output}}{\text{change in input}}
\]

In the context of a function, we write the input as \(x\) and the output as \(f(x)\), and then write it like this.

\[
\frac{\Delta y}{\Delta x}
\]

Here, \(\Delta\) means the amount of change. \(\Delta x\) is the change in input, and \(\Delta y\) is the change in output.

This notation does not look only at `how much did the output value change?` It always looks together at `when the input changed by how much, the output changed by how much?`

## Slope on a Graph

Slope is a way to see rate of change on a graph.

For example, suppose we have the following function.

\[
y = 2x + 1
\]

If we look at the values in a table, we get the following.

| \(x\) | \(y = 2x + 1\) |
| --- | --- |
| 0 | 1 |
| 1 | 3 |
| 2 | 5 |
| 3 | 7 |

Whenever \(x\) increases by 1, \(y\) increases by 2. So the rate of change is 2.

\[
\frac{\Delta y}{\Delta x} = \frac{2}{1} = 2
\]

On the graph, this value is the slope. If the absolute value of the slope is large, the output changes more for the same input change. If the slope is 0, the output does not change even if the input changes. If the slope is negative, the output decreases when the input increases.

![Example of a line's slope](/AiBook/assets/part-02/chapter-04/linear-slope-constant-en.svg)

1. If the slope is positive, it means the output tends to increase as the input increases.
2. If the slope is 0, it means the output tends not to change even when the input changes.
3. If the slope is negative, it means the output tends to decrease as the input increases.

## Constant Slope of a Line

In a line, the slope is the same everywhere.

\[
y = 2x + 1
\]

In this function, when \(x\) goes from 0 to 1, \(y\) increases by 2, and when \(x\) goes from 2 to 3, \(y\) also increases by 2.

1. When x goes from 0 to 1, y goes from 1 to 3, and the rate of change is 2.
2. When x goes from 2 to 3, y goes from 5 to 7, and the rate of change is also 2.

Lines are easy to handle because the rate of change is constant. The slope computed on one interval is the slope of the whole line.

But many real problems do not move like lines. They may change slowly at first and quickly later, or increase in one interval and decrease in another.

## Rates of Change Across a Curve

Now let us look at the following function.

\[
y = x^2
\]

If we look at the values in a table, we get the following.

| \(x\) | \(y = x^2\) |
| --- | --- |
| 0 | 0 |
| 1 | 1 |
| 2 | 4 |
| 3 | 9 |

When \(x\) goes from 0 to 1, \(y\) increases by 1.

\[
\frac{1 - 0}{1 - 0} = 1
\]

When \(x\) goes from 2 to 3, \(y\) increases by 5.

\[
\frac{9 - 4}{3 - 2} = 5
\]

It is the same function, but the rate of change differs by interval. This is why slope becomes harder when we deal with a curve.

![Example of a curve's slope](/AiBook/assets/part-02/chapter-04/curve-slope-changing-en.svg)

1. A line has the same slope no matter where you look.
2. A curve has a different slope depending on which interval you inspect.

## Order of Differentiation

The order of a derivative indicates how many times differentiation has been performed.

1. Order 0 is the original function itself.
2. Order 1 is the derivative obtained by differentiating once.
3. Order 2 is the derivative of that derivative.
4. Order n is the result of differentiating n times.

For position as a function of time, the first derivative is velocity and the second is acceleration. An equation containing a function and its derivatives is called a differential equation.

## Average Rate Between Two Points

If we pick two points on a curve and calculate the rate of change, we get the average rate of change.

\[
\text{average rate of change} = \frac{f(b) - f(a)}{b - a}
\]

For example, in \(f(x) = x^2\), the average rate of change from \(x = 1\) to \(x = 3\) is the following.

\[
\frac{f(3) - f(1)}{3 - 1}
= \frac{9 - 1}{2}
= 4
\]

This value is the rate of change computed by treating the entire interval between \(x=1\) and \(x=3\) like one straight line.

On the graph, we can think of the line connecting the two points. That line lets us read the curve roughly over one interval.

## Instantaneous Rate at a Point

Average rate of change is the change over an entire interval. But sometimes we want to know how the value is changing at one specific point.

For example, average rate of change alone is not enough for the following questions.

1. What is the speed at this exact moment?
2. At this exact point, is the function going up or down?
3. If we want to reduce the current loss, in which direction should we change the parameter?

These questions ask for the rate of change near a particular point. If the average rate converges to a value as the interval shrinks, that value is the instantaneous rate of change at that point.

This flow leads to the derivative.

\[
\text{average rate of change}
\rightarrow
\text{rate of change over a very small interval}
\rightarrow
\text{instantaneous rate of change}
\rightarrow
\text{differentiation}
\]

## Loss Slope and Adjustment Direction

In AI model learning, we usually want to reduce loss. Loss is the value that shows how different the model's prediction is from the desired result.

Learning roughly repeats the following questions.

1. What is the model's current loss?
2. If we change a parameter a little, how does the loss change?
3. In which direction does the loss decrease?
4. How much should we change it?

Here, `if we change it a little, how does the value change?` is exactly the question of rate of change. When this question is calculated for many parameters, it leads to the gradient.

If the loss slope with respect to one parameter is positive, a sufficiently small increase in that parameter increases the loss, and a sufficiently small decrease reduces it.

## Sign-Up Changes Across Ad-Spend Intervals

The following example records compare advertising spend and sign-ups.

| Week | Ad spend (10,000 KRW) | Sign-ups |
| --- | --- | --- |
| 1 | 100 | 50 |
| 2 | 200 | 60 |
| 3 | 300 | 62 |

From week 1 to week 2, the rate of change is `(60 − 50) / (200 − 100) = 0.1 sign-ups per 10,000 KRW`. From week 2 to week 3, it is `(62 − 60) / (300 − 200) = 0.02 sign-ups per 10,000 KRW`. The increase in sign-ups corresponding to the same additional 1 million KRW fell from 10 to 2.

Both values are average rates over their respective intervals. These three records cannot give the instantaneous rate at a particular spending level. Other conditions may vary between weeks, so the changes should not be interpreted directly as effects caused by the advertising spend.

## Checklist

- You can explain rate of change as output change relative to input change.
- You can explain that \(\Delta x\) and \(\Delta y\) mean input change and output change, respectively.
- You can explain that slope represents rate of change on a graph.
- You can explain that, in a line, the slope is constant, while in a curve, the rate of change can differ by interval.
- You can explain that average rate of change is the rate of change between two points.
- You can explain the flow by which instantaneous rate of change leads to differentiation.
- You can explain that, in AI learning, rate of change connects to the problem of finding the direction that reduces loss.
- You can distinguish the size of a value from `how much the output changed when the input changed by how much`.
- You can explain why we narrow from average rate of change toward instantaneous rate of change.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }. It supports secant slope, tangent slope, average and instantaneous velocity, and the definition of instantaneous rate of change. Checked: 2026-07-20.
