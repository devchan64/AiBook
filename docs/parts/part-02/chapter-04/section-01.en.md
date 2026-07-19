# P2-4.1 Rereading How We Learned Differentiation

> Section ID: `P2-4.1`
> Version: `v2026.07.19`

In Part 2 Chapter 3, we looked at the shapes of data and model computation through scalars, vectors, and matrices. Now, in Part 2 Chapter 4, we move to differentiation.

But if formulas come first, it becomes easy to lose the connection to the question of change. Here, we first bring back old memories and then turn those memories again into questions needed for AI learning.

This Section reorganizes differentiation, change comparison, instantaneous rate of change, tangent line, and memory recovery. If Chapter 3 read the shapes of data and vector computation, this Chapter begins again from the entrance question of what we should ask when values change.

Here, the focus is not on full training in derivative formulas. It is on recovering the question of rate of change. If we reset differentiation as the question `when the input changes a little, how much does the output change?`, then later sections on loss, gradient, and parameter updates connect with less interruption.

For the reader, it is better to place one more bridge here. The reason to reread differentiation in Chapter 4 is to read the direction that reduces loss in Chapter 6. In other words, the flow continues as `question of change -> rate of change -> gradient -> learning update`.

| What to Hold in This Section Now | The Question That Connects Immediately Next | Where It Is Used Again Later |
| --- | --- | --- |
| The point that differentiation is a question of comparing change before it is a formula | In `P2-4.2`, we look more directly at rate of change and slope. | We use it again in `P2-6.1`, `P2-6.2`, and `P2-6.3` when reading the direction in which loss decreases. |
| The method of turning old math memory into a current question again | It connects to later derivative and graph interpretation in P2-4.3 and after. | It becomes the background when reading backpropagation and gradient explanations in Part 4. |
| Intuition from distance, speed, and acceleration | In `P2-4.2`, we distinguish average rate of change and instantaneous rate of change. | It appears again when interpreting the direction and size of value changes in model learning. |

## Connection Flow to See First

If we compress why we are holding the entrance to differentiation right now into one table, it looks like this.

| Current Stage | Question the Reader Should Hold | Immediate Next Connection |
| --- | --- | --- |
| the fact that there is change | What is changing? | rate of change and slope in `P2-4.2` |
| comparing the size of change | If the input changes a little, how much does the output change? | differentiation and gradient in `P2-4.3`, `P2-4.4` |
| reading the direction of change | In which direction does the value become larger or smaller? | loss and gradient descent in `P2-6.1` to `P2-6.3` |
| the learning connection | How should parameters change to reduce loss? | backpropagation and optimizers in Part 4 |

Seen from this table, Chapter 4 is not a chapter for memorizing formulas. It is a chapter that prepares `why learning must read the direction of change`.

## Scope of This Section

This Section recalls what kinds of explanations we heard when we first learned differentiation and organizes what questions those explanations lead to.

Detailed rate of change, slope, and average rate of change are covered in P2-4.2.

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| differentiation | a method for reading how values change | the starting point of this whole chapter |
| change comparison | a question that looks at input change and output change together | the core perspective for rereading differentiation |
| instantaneous rate of change | the speed of change near one point | the standard that leads to the rate-of-change explanation in `P2-4.2` |
| tangent line | a line that shows the slope at one point on a graph | a representative image that calls old memories back |
| memory recovery | the process of rebuilding a forgotten concept in question form | the practical purpose of this Section |

## Goals of This Section

- You can explain why differentiation feels distant.
- You can reread differentiation as the question of `comparing changes in value` before seeing it as a formula.
- You can say why the intuition of differentiation connects to explanations of loss and learning.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| Reread differentiation as a question of comparing change | If only formula memories remain, they must be reconnected to the meaning of change so that the mathematics in later sections breaks less. | Understand differentiation as the question `if the input changes a little, how much does the output change?` |
| Turn old math memories into present questions | Memories such as tangent line, instantaneous speed, and derivative coefficient need to be tied back into one flow. | Understand that those old memories are all expressions placed around the question of rate of change. |
| This question continues to loss and learning | AI learning also continues as the problem of reading value changes and adjustment directions. | Understand that the entrance to differentiation is the starting point for loss, gradient, and parameter-adjustment explanations. |

## Words That Come to Mind When Learning Differentiation

If you learned differentiation long ago, the following expressions may come to mind first.

1. You may remember the slope of a tangent line.
2. You may remember the instantaneous rate of change.
3. You may remember instantaneous speed.
4. You may remember the derivative function and derivative coefficient.
5. You may remember the limit-based definition and formula-calculation problems.

All of these expressions are related to differentiation. But when people first learn them, they are often remembered less as one connected flow and more like a bundle of formulas for solving test problems.

You can ask yourself the following questions.

1. When you hear the word differentiation, what comes to mind first?
   It may be the slope of a tangent line, a formula, or instantaneous speed.
2. Is that memory closer to a calculation method or to a meaning?
   If only formulas come to mind, the calculation method may remain while the meaning has blurred.
3. What should be revisited first to recover the meaning?
   Start again from the statement that values change, and that we compare that change.

For example, you may have learned it like this.

1. Draw a tangent line on the graph of a function.
2. Calculate the slope between two points.
3. Bring the two points closer and closer together.
4. Take the limit and obtain the slope at one point.
5. Call this value the derivative coefficient or the derivative.

This explanation matches the standard introduction to differentiation well. But as time passes, `why bring the two points closer together?`, `why is slope important?`, and `what does this have to do with AI learning?` can all become blurred.

## The Memory of Distance, Speed, and Acceleration

An example that is easy to remember when learning differentiation is the relation among distance, speed, and acceleration over time.

Distance shows how much position changes over time. Speed shows how quickly distance changes over time. Acceleration shows how quickly speed changes over time.

1. Distance changes over time.
2. The rate of change of distance with respect to time is velocity.
3. The rate of change of velocity with respect to time is acceleration.

This example helps us read differentiation not as `formula calculation`, but as `a structure in which the change of one value becomes the meaning of another value`.

AI learning needs a similar way of thinking. We must read how loss changes in order to decide in which direction to change a parameter.

Here as well, we can change the question.

1. If we look at distance with respect to time, it becomes speed.
2. If we look at speed with respect to time, it becomes acceleration.
3. So differentiation can be read as a tool for seeing how much one value changes with respect to another.

## The Memory of Point, Line, Area, and Volume

Another memory may be the relationship that continues from point, to line, to area, to volume.

1. Think of a point.
2. If points are connected, you can imagine a line.
3. If a line moves or is stacked, you can imagine an area.
4. If areas are stacked, you can imagine a volume.

If points are connected, we can think of a line. If a line moves or is stacked, we can think of an area. If areas are stacked, we can think of a volume.

This flow is closer to the intuition of accumulation: small changes pile up to make a larger object. Differentiation, in the opposite direction, connects to the perspective of reading a very small rate of change from the larger flow of change.

But here we do not treat integration or dimension in depth. We only hold onto the memory that change and accumulation were connected mathematical ways of thinking.

This memory can be organized as follows.

1. What can you imagine if points are connected?
   You can imagine a line.
2. What can you imagine if a line moves or is stacked?
   You can imagine an area.
3. What can you imagine if areas are stacked?
   You can imagine a volume.
4. Is this flow differentiation, or accumulation?
   It is closer to the intuition of accumulation. But it becomes an important background memory when understanding differentiation and integration together.

## Questions for Rereading Differentiation

Now reread differentiation not as a formula, but through the following questions.

1. If the input changes a little, how much does the output change?
2. At this point, is the value increasing or decreasing?
3. If we want to reduce the value, in which direction should we move?
4. If small changes accumulate, what does the total change look like?

Once these questions are understood, terms such as rate of change, slope, derivative, and gradient no longer appear only as completely unfamiliar words.

## Cases And Examples

### Case 1. When Delivery Time Grows Longer, What Should We Ask First?

Suppose a logistics team operates an order-processing system. A report comes in that the average delivery time has become longer than last week. In the field, people first look at numbers such as `number of delayed cases`, `average delivery time`, and `the order that took the longest`.

But if we only list numbers, it is hard to explain what is changing. We still do not know whether delivery became slower because order volume increased, whether only deliveries to a specific region became delayed, or whether dispatch-processing speed changed.

The needed question here is not only `what is the value?`, but `when some input changes, how does the result change?` We must compare the change itself, such as how much delivery time increases when order volume rises a little, or how much delay worsens when the share of nighttime orders grows.

The first step in rereading differentiation is similar. Here, instead of using formulas immediately, we first ask `what changed, and what result difference did that change lead to?` The reason we learn rate of change and slope in later sections is also to make this question more precise.

A checkable result can be set in the following way. We can first test `do the changes move together?` by comparing, in a table or simple scatter plot, whether the average delivery time rises on days when order volume is 10% higher, or whether delayed cases increase as the share of orders from a specific time period grows.

## Checklist

- Can you say whether the slope of a tangent line, the instantaneous rate of change, or instantaneous speed comes to mind first when you hear differentiation?
- When a formula comes to mind first, can you ask again what meaning of change that formula is dealing with?
- Can you explain the relationship among distance, speed, and acceleration as an example of rate of change?
- Can you explain that the relationship among point, line, area, and volume connects to the intuition of accumulation?
- Can you reread differentiation not as formula memorization, but as the question `what effect does a small change have on the output?`
- Can you tie together the words tangent line, derivative coefficient, and instantaneous speed as one question about change?
- Can you explain why the question `how much is the value changing?` needs to be recovered before reading explanations of loss or gradient?

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }, checked on 2026-07-19. Used as the standard reference for tangent lines, secant lines, derivatives, velocity, and instantaneous rates of change at the entrance to differentiation.
