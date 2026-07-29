# P2-4.6 Composite Functions and the Chain Rule

> Section ID: `P2-4.6`
> Version: `v2026.07.26`

After reading derivatives, gradients, and gradient descent, one sentence still remains: `backpropagation uses the chain rule`. If we do not know the chain rule here, backpropagation easily looks like a memorized sentence rather than a calculation structure.

The core intuition is that `when a function is connected through several stages, a change in an earlier stage is passed through later stages until it affects the final result`. Without that intuition, it is hard to read how loss is connected to each layer and parameter. When you want to recheck the terms quickly, also refer to the [gradient glossary entry](/AiBook/en/reference/concept-glossary-alpha/g.en/#gradient).

## Core Criteria: Composite Functions and the Chain Rule

- You can explain a composite function as `a structure where the output enters the next function as input`.
- You can describe the chain rule as `a rule that reads stage-by-stage rates of change by linking them multiplicatively`.
- You can build the intuition that if an earlier value changes, the later result changes with it through several stages.
- You can explain at an entry level why backpropagation needs the chain rule.

## One Scene to Hold First

The first scene to hold in this section is a two-stage calculation that flows as `x -> y -> z`.

| Stage | Expression | Question to read now |
| --- | --- | --- |
| stage 1 | `y = 2x + 1` | if `x` changes a little, how much does `y` change? |
| stage 2 | `z = y^2` | how much more does the changed `y` change `z`? |
| whole | `z = (2x + 1)^2` | how does the change in `x` travel all the way to the final result `z`? |

So the chain rule is not about memorizing one more symbol. It is about reading `the path through which a change in the front stage is delivered through a middle stage to the later result`.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| Read a composite function like a `calculation pipeline` | Because it connects naturally to explanations of neural-network layers. | Understand that one function passes through several stages. |
| The chain rule is a `change-transfer rule` | Because it lets us read how a change in an earlier stage reaches the final output. | Understand that stage-wise rates of change are connected. |
| Backpropagation is not the chain rule itself, but a procedure that uses it | Because it keeps us from mixing the concept with the algorithmic procedure. | It is enough to distinguish the roles clearly. |

## A Composite Function Is a Structure That Joins Several Functions into One Line

For example:

\[
z = f(g(x))
\]

When written like this, we read it as: first calculate `g(x)`, and then feed that result into `f`.

So the calculation order is:

1. `x` enters.
2. `g` makes an intermediate result.
3. `f` receives that intermediate result and makes the final result `z`.

This same intuition returns directly when we look at neural networks, because the output of one layer becomes the input of the next layer.

It becomes more intuitive if we see it as the following flow.

```mermaid
--8<-- "assets/part-02/chapter-04/chain-rule-composition-flow-en.mmd"
```

If we write it more like an everyday calculation:

\[
x \rightarrow 2x + 1 \rightarrow (2x + 1)^2
\]

First we make an intermediate score `2x + 1`, and then we square that value to make the final result. Once calculation stages are connected like this, a small change in the earlier stage changes the intermediate score, and that change is then delivered again to the final result.

## Chain Rule Is the Rule That Sends an Earlier Change Forward

In a composite function, when the earlier stage changes a little, that change affects the final output through the middle stages. The chain rule is the way to read that transfer rule.

For a beginner, the most important sentence is the following:

`The chain rule is the rule for reading, in a function made of several stages, how much a change in an earlier stage reaches the final output by following the rates of change stage by stage.`

If we look at just one short formula:

\[
\frac{dz}{dx} = \frac{dz}{dy} \cdot \frac{dy}{dx}
\]

What matters here is not the shape of the symbols themselves, but the structure that `an earlier change is passed through an intermediate value to the later result`.

It becomes more intuitive if we use the same example directly.

\[
y = 2x + 1,\quad z = y^2
\]

If `x` changes, then `y` changes first, and then the changed `y` changes `z` again. To read the influence of `x` on the final result `z`, we have to look separately at the change `x -> y` and the change `y -> z`, and then connect them. That is the core of the chain rule.

For example, when `x = 1`:

- `y = 2(1) + 1 = 3`
- `z = 3^2 = 9`

If we increase `x` a little at this point, `y` increases first, and because the increased `y` is squared, `z` changes more strongly. In other words, the effect of an earlier-stage change accumulates as it passes through later stages.

If we rewrite this scene again as a table:

| Question | How to read it |
| --- | --- |
| how sensitive is `x -> y`? | `dy/dx` |
| how sensitive is `y -> z`? | `dz/dy` |
| how sensitive is the whole `x -> z` path? | read the two changes in connection |

## Why One-Step Differentiation Is Not Enough

In a simple function such as `z = x^2`, `x` changes `z` directly. But in a composite function, `x` does not change `z` directly. It affects `z` by passing through intermediate stages.

So in a composite function, we must look separately at the following two questions.

1. How much does the earlier-stage value change the intermediate value?
2. How much does that intermediate value change the final result?

The chain rule is the rule that joins those two questions into one expression. What the reader should hold here is not that the chain rule is `a harder rule added on top of differentiation`, but that it is `a way of reading the path of influence by following the stages of calculation`.

If we rewrite that difference very briefly:

| Function form | How to read its derivative |
| --- | --- |
| `z = x^2` | `x` changes `z` directly |
| `z = (2x + 1)^2` | `x` first changes the intermediate value `y`, and that `y` changes `z` again |

## Why the Chain Rule Is Needed in Backpropagation Explanations

Backpropagation is a procedure that calculates, moving backward from the loss computed at the end of a neural network, how much each layer and each parameter influences that loss. The minimum rule needed for that is the chain rule.

In other words:

- The chain rule is the mathematical rule for the transfer of change.
- Backpropagation is the procedure that uses that rule to efficiently calculate the gradients of many parameters.

Without this distinction, it becomes easy to read `chain rule = backprop`.

Before moving into later Parts, we can leave the minimum connection in the following form.

| Expression seen later | How to read it now first |
| --- | --- |
| `loss -> layer -> parameter` | the change in loss is transferred through layers until it reaches parameters |
| backpropagation | a calculation procedure that follows that transfer path from back to front |
| gradient | the result of the transferred rate of change |

## Scenes Where This Structure Reappears

| Scene encountered again later | Intuition to leave here first |
| --- | --- |
| backpropagation in Part 5 | The sentence “loss is delivered from back to front” is hard to read without the chain rule. |
| deep neural networks in Part 5 | As the layers get deeper, the composite-function structure also gets longer. |
| optimizer and gradient calculation | A gradient should be read not as a number that appears suddenly, but as the result of a delivered rate of change. |

The key sentence to keep from this section is simple. `A composite function is a structure that bundles several stages of calculation into one line, and the chain rule is the rule that transfers rates of change by following those stages.` Once this sentence is stable, even when reading backpropagation later, the layers no longer look like completely separate calculations.

## Checklist

- Can you explain a composite function as `a function whose stages are connected`?
- In `y = 2x + 1`, `z = y^2`, can you explain why `x -> y` and `y -> z` must be read separately?
- Can you explain the chain rule as `a rule that reads rates of change by connecting them stage by stage`?
- Can you explain the difference in role between backpropagation and the chain rule?
- Can you explain backpropagation as a picture in which the change in loss is transferred through several stages?

## Sources and References

- OpenStax, [Calculus Volume 1, 3.6 The Chain Rule](https://openstax.org/books/calculus-volume-1/pages/3-6-the-chain-rule){: target="_blank" rel="noopener noreferrer" }. It supports differentiating composite functions, the chain rule, and applying the chain rule to compositions of two or more functions. Checked: 2026-07-20.
- Google for Developers, `Machine Learning Glossary`. Because it lets us confirm terms such as `backpropagation` and `gradient` together, it serves as the minimum reference point for reading why the chain rule is tied to explanations of backpropagation. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Checked: 2026-07-20
- Same-Part internal links: [P2-4.3 Derivative and Gradient](section-03.md), [P2-4.5 Gradient Supplement: From High-School Differentiation to Multivariable Differentiation](section-05.md). This section strengthens the link `composite function -> chain rule -> backpropagation` between those two sections.
