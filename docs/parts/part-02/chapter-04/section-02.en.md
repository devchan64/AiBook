# P2-4.2 Rate of Change and Slope

> Section ID: `P2-4.2`
> Version: `v2026.07.19`

In P2-4.1, we brought back memories of learning differentiation. The slope of a tangent line, instantaneous rate of change, distance and speed, and the flow from point to volume all connect to a mathematical way of thinking that tries to understand change and accumulation.

Now we narrow that memory into a slightly more calculable language. Here, we read `how much a value changes` through rate of change and slope.

This Section reorganizes rate of change, slope, average rate of change, instantaneous rate of change, and curve. If P2-4.1 reopened differentiation as a question, now we make that question more concrete as a comparison of change over an interval and near one point.

Here, rather than immediately calculating derivative formulas, the focus is on narrowing our view from the rate of change over an interval to the rate of change near a single point. If we hold onto the connection among rate of change, slope, average rate of change, and instantaneous rate of change, then later, when reading the direction that reduces loss and the gradient, we can directly connect why the first question is `if we change it a little, how much does it change?`

The point readers most often miss here is stopping after reading `slope` as only a graph problem. But in the learning context, slope is the preparation for asking `if I change this value a little now, in which direction and by how much will the result move?`

## Scope of This Section

This Section deals with the intuition of rate of change, average rate of change, and slope. Derivative, gradient, gradient descent, and backpropagation are covered in the next Section and later chapters.

The first question to solve here is this: `why must we look not only at how much the output changed, but also at how much the input changed when that change happened?`

So this Section first fixes only the following four places.

1. What does rate of change compare?
2. Why is slope a visual expression of rate of change?
3. How are input change and output change connected?
4. Why does differentiation begin from slope and continue into learning?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| rate of change | output change relative to input change | the central question of this Section |
| slope | the value that reads rate of change on a graph | the standard for visual interpretation |
| average rate of change | the rate of change over a whole interval | the starting point for comparing lines and curves |
| instantaneous rate of change | the rate of change near one point | the bridge to differentiation |
| curve | a function shape whose rate of change can differ by interval | the object that shows why differentiation is needed |

The flow after this Section is also simple.

- In `P2-4.3`, we read this question of rate of change more directly through the notation of derivative, partial derivative, and gradient.
- From `P2-6.1` to `P2-6.3`, we read again in the language of rate of change how much loss can be reduced and in which direction parameters should change.
- In Part 4, the same question repeats in the language of `gradient`, `update`, and `optimizer`.

## Goals of This Section

- You can explain rate of change as output change relative to input change.
- You can read slope as the ratio of change between two values.
- You can explain why the slope of a line and the slope of a curve feel different.
- You can describe the flow from average rate of change to instantaneous rate of change and differentiation.
- You can understand that the reason for learning differentiation in AI learning is `to judge how values should be changed`.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| Rate of change is output change relative to input change | Meaning appears only when we see not just the output, but also how much the input changed. | Understand it as the comparison structure `output change / input change`. |
| Slope is a visual expression of rate of change | It lets us quickly read increase, decrease, and sensitivity on a graph. | Understand slope as a value that reads rate of change on a picture. |
| Average rate of change narrows into instantaneous rate of change | To read change near one point on a curve, the interval must be made smaller and smaller. | Understand average rate of change as the middle stage that leads to differentiation. |

## What Does Rate of Change Compare?

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

## Slope Is a Way to Read Rate of Change as a Picture

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

On the graph, this value is the slope. If the slope is large, the output changes more for the same input change. If the slope is 0, the output does not change even if the input changes. If the slope is negative, the output decreases when the input increases.

![Example of a line's slope](/AiBook/assets/part-02/chapter-04/linear-slope-constant-en.svg)

1. If the slope is positive, it means the output tends to increase as the input increases.
2. If the slope is 0, it means the output tends not to change even when the input changes.
3. If the slope is negative, it means the output tends to decrease as the input increases.

## In a Line, the Slope Is Constant

In a line, the slope is the same everywhere.

\[
y = 2x + 1
\]

In this function, when \(x\) goes from 0 to 1, \(y\) increases by 2, and when \(x\) goes from 2 to 3, \(y\) also increases by 2.

1. When x goes from 0 to 1, y goes from 1 to 3, and the rate of change is 2.
2. When x goes from 2 to 3, y goes from 5 to 7, and the rate of change is also 2.

Lines are easy to handle because the rate of change is constant. The slope computed on one interval is the slope of the whole line.

But many real problems do not move like lines. They may change slowly at first and quickly later, or increase in one interval and decrease in another.

## In a Curve, the Rate of Change Differs by Interval

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

## How Should We Hold the Memory of 0th, 1st, and n-th Order?

Memories of learning differentiation may also include expressions such as `0th order`, `1st order`, `2nd order`, and `n-th order`. We do not treat differential equations in depth here, but we should still fix the direction of the terms carefully.

The first expression to remember here is the order of derivative.

1. 0th order is the perspective of looking at the original function itself.
2. 1st order is the perspective of differentiating once to see the rate of change.
3. 2nd order is the perspective of seeing how that rate of change changes again.
4. n-th order is the perspective of repeating this many times to inspect the structure of change.

Seen through the example of distance, speed, and acceleration, it connects as follows.

1. Distance is the position function with respect to time.
2. Speed is the first-order rate of change of distance.
3. Acceleration is the rate of change of speed, that is, the second-order rate of change of distance.

By contrast, a differential equation is an equation in which a function and its derivatives appear together. Here, instead of solving differential equations, we first organize the memory of `order` as `how many times are we looking at the rate of change?`

## Average Rate of Change Is Change over an Interval

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

## When We Move to Instantaneous Rate of Change, Differentiation Appears

Average rate of change is the change over an entire interval. But sometimes we want to know how the value is changing at one specific point.

For example, average rate of change alone is not enough for the following questions.

1. What is the speed at this exact moment?
2. At this exact point, is the function going up or down?
3. If we want to reduce the current loss, in which direction should we change the parameter?

These questions ask for the rate of change near a specific point. If we narrow the interval more and more, average rate of change gets closer to the instantaneous rate of change at that point.

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

Here, we organize only the flow by which average rate of change leads to instantaneous rate of change and differentiation. The calculation method for derivatives is treated in the next Section.

## A Short Judgment Flow Read in the Learning Context

If we compress one more time why rate of change and slope continue into learning, it becomes the following.

| Scene | Value We Look at First | Question We Ask Next | Learning Connection |
| --- | --- | --- | --- |
| line | Is the slope constant? | If the input increases, how much does the output increase? | starting point for reading a simple relationship |
| curve | Does the slope vary by interval? | At the current position, how sensitive is it? | the sense for reading the current position on a loss curve |
| average rate of change | How much did it change over the whole interval? | What is the overall flow? | the perspective of bundling multiple steps together |
| instantaneous rate of change | How much does it change at this exact point? | Where should we move now? | preparation for gradient and update direction |

In other words, `reading the slope on a graph` later becomes `reading in which direction we should move to reduce loss`.

## Why Is This Needed in AI Learning?

In AI model learning, we usually want to reduce loss. Loss is the value that shows how different the model's prediction is from the desired result.

Learning roughly repeats the following questions.

1. What is the model's current loss?
2. If we change a parameter a little, how does the loss change?
3. In which direction does the loss decrease?
4. How much should we change it?

Here, `if we change it a little, how does the value change?` is exactly the question of rate of change. When this question is calculated for many parameters, it leads to the gradient. Gradient is treated in the next Section and later optimization chapters.

So the reason for learning differentiation is not only to memorize formulas. It is because, if we want the model to move in a better direction, we must read in which direction and by how much the value changes.

For example, if the slope at some point on a loss curve is positive, we can read that moving farther in that direction is likely to increase the loss. On the other hand, if we want to reduce the loss, we first suspect the opposite direction. This interpretive sense connects directly to the derivative notation in the next Section and to gradient descent in Chapter 6.

## View It Through a Case

### Case 1. As Advertising Spend Increases, How Much Does the Number of Sign-Ups Change?

Suppose a service team runs advertising to increase the number of sign-ups. A practitioner first looks at `this week's ad spend`, `number of visits`, and `number of completed sign-ups`. The numbers can be checked immediately, but these numbers alone make it hard to decide whether to spend more on ads or spend less.

For example, if sign-ups increase by 10 when ad spend increases by 1 million won, a person may interpret that as `it did increase`. But if, the next week, ad spend increases by another 1 million won and sign-ups increase by only 2, then even though the increase is in the same direction, the meaning is completely different.

The needed concept here is rate of change. We must look together at `when ad spend increased by how much, sign-ups increased by how much`, and if we read this ratio on a graph, we can change the name to slope. If the response is constant like a line, interpretation is easy. But in a real campaign, efficiency may drop sharply after a certain interval.

A checkable result is to place weekly ad spend and sign-ups in a table and calculate `increase in sign-ups relative to increase in ad spend`. If this value differs by interval, we read the response as curve-like, and right at that point we distinguish average rate of change from instantaneous rate of change.

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

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }. It supports secant slope, tangent slope, average and instantaneous velocity, and the definition of instantaneous rate of change. Checked: 2026-07-19.
