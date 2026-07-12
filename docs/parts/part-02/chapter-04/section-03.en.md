# P2-4.3 Derivative and Gradient

> Section ID: `P2-4.3`
> Version: `v2026.07.12`

In P2-4.2, we looked at rate of change and slope. In a line, the slope is constant, but in a curve, the rate of change can differ by interval or position.

Now we connect that flow to derivative and gradient. Here, rather than memorizing many differentiation formulas, the focus is on distinguishing what words such as `derivative`, `gradient`, and `partial derivative` point to when they appear in AI documents.

This Section reorganizes derivative, derivative function, partial derivative, gradient, and nabla. If P2-4.2 read rate of change and slope, this Section now organizes how the instantaneous rate of change for one variable expands into information about change across multiple variables.

Here, instead of solving many differentiation exercises, the focus is on reading how the instantaneous rate of change for one variable expands into the gradient across multiple variables. If we hold onto the relationship among derivative, partial derivative, and gradient, then later, when reading loss, parameter, and optimization, the language of mathematics and the language of learning connect as one flow.

1. The rate of change with respect to one input is read as a derivative.
2. The bundle of rates of change with respect to multiple inputs is read as a gradient.

## Scope of This Section

This Section connects the derivative of a single-variable function, the partial derivative of a multivariable function, and the gradient at an introductory level.

The following topics are not treated in depth.

- systematic memorization of derivative formulas
- detailed calculation of the chain rule
- Jacobian and Hessian
- the update formula of gradient descent
- backpropagation

The first question to resolve here is this: `when the memory of one-variable slope remains, how does it expand into the gradient of several variables?`

So this Section first fixes only the following four places.

1. What does a derivative tell us as a number?
2. What does a partial derivative look at separately?
3. Why is a gradient a vector?
4. Why does the word gradient appear so often in AI learning?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| derivative | the instantaneous rate of change of one input | the basic concept that becomes the starting point |
| derivative function | a function that tells the derivative value at each point | the object that must be separated from the derivative coefficient |
| partial derivative | the rate of change when one of several inputs is changed | the basic reading of a multivariable function |
| gradient | a vector that gathers several partial derivatives | the central concept for the connection to AI learning |
| nabla | the symbol used when writing a gradient | the standard that makes formula notation less unfamiliar |

If the jump from high-school differentiation memory to gradient feels large, you may read the supplementary learning in P2-4.5 first. Here, we first fix the core concepts, and P2-4.5 more slowly rebuilds the flow `one-variable differentiation -> multivariable differentiation -> gradient -> gradient descent`.

The flow after this Section is also simple.

- In `P2-4.4`, we read why a gradient is actually needed in real learning procedures.
- In `P2-4.5` and `P2-6.3`, the explanation continues more slowly into gradient descent and update direction.
- In Part 4, the same notation repeats inside explanations of backpropagation and optimizers.

## Goals of This Section

- You can explain a derivative as the instantaneous rate of change with respect to one input.
- You can explain a partial derivative as the rate of change when one of several inputs is changed.
- You can explain a gradient as a vector that gathers several partial derivatives.
- You can explain at an introductory level that a gradient connects to the direction in which the value increases most rapidly.
- You can explain that, in AI learning, a gradient is needed to see how loss changes with respect to many parameters.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| A derivative is the instantaneous rate of change of one input | It is the starting point for reading slope and instantaneous rate of change in a one-variable problem. | Understand it as the value that shows how much the output changes when one input is changed a little. |
| A partial derivative looks at several inputs one by one | In a multivariable function, we must inspect separately how each input changes the result. | Understand it as keeping the other inputs temporarily fixed and watching only the change in one input. |
| A gradient is a vector that gathers several partial derivatives | In learning, we must read changes across many parameter directions at once. | Understand it as a vector that gathers the rate of change of each direction in order. |

## Why Gradient Feels Unfamiliar

Gradient may be an expression that appears relatively late in the common Korean mathematics-learning sequence. In high school or introductory general mathematics, the following flow usually comes first.

1. Set one input `x`.
2. Look at the function `y = f(x)`.
3. Read the slope of the tangent line.
4. Continue into derivative coefficient and derivative function.

In that flow, the graph is drawn on paper, and the slope is understood as the slope of one line. But the context in which gradient appears often is usually a problem with many inputs.

1. There are several inputs `x_1, x_2, x_3, ...`.
2. Look at the result `f(x_1, x_2, x_3, ...)`.
3. See how the result changes when each input is changed a little.
4. Gather those rates of change into one bundle.
5. That bundle is the gradient.

So gradient is less `a new kind of differentiation` and closer to an expansion of differential thinking into vector form in a situation with many inputs. If there is only one control knob, one slope is enough. If there are many control knobs, we must record together in which direction and with what sensitivity each knob should be read.

## A Derivative Is the Instantaneous Rate of Change with Respect to One Input

Suppose a function receives one input.

\[
y = f(x)
\]

Then the derivative shows how much \(y\) changes when \(x\) changes by a very small amount. Rewriting it in the language of P2-4.2, it is the instantaneous rate of change at a specific point.

For example, consider the following function.

\[
f(x) = x^2
\]

The derivative function of this function is the following.

\[
f'(x) = 2x
\]

This expression tells the slope at each position.

| \(x\) | \(f(x) = x^2\) | \(f'(x) = 2x\) |
| --- | --- | --- |
| 0 | 0 | 0 |
| 1 | 1 | 2 |
| 2 | 4 | 4 |
| 3 | 9 | 6 |

At \(x = 1\), the slope is 2, and at \(x = 3\), the slope is 6. Even in the same function, the rate of change differs by position.

What matters here is the interpretation more than the formula itself.

```text
f(x) = x^2      -> a function that turns input into output
f'(x) = 2x      -> a function that tells how quickly the output changes at each position
```

## Read Derivative Coefficient and Derivative Function Separately

When learning differentiation in Korean, we meet the expressions for `derivative coefficient` and `derivative function`.

| Expression | Introductory Meaning |
| --- | --- |
| derivative coefficient | the instantaneous rate of change at a specific point |
| derivative function | the function that tells the instantaneous rate of change at each point |

For example, in \(f(x) = x^2\), the derivative coefficient at \(x = 2\) is the following.

\[
f'(2) = 4
\]

By contrast, the derivative function is this whole function.

\[
f'(x) = 2x
\]

1. A derivative coefficient is the value at one point.
2. A derivative function is the function that tells the derivative coefficient at each point.

This distinction also matters later when reading model learning. Looking at how much the loss changes at one parameter value and calculating the direction of change across many positions are connected, but they are not the same expression.

## If There Are Several Inputs, Partial Derivatives Are Needed

In AI models, it is rare that there is only one input or one parameter. Usually several values exist together.

For example, suppose a loss function depends on two parameters \(w_1\) and \(w_2\).

\[
L(w_1, w_2)
\]

Then there is not only one question.

1. If we change `w_1` a little, how does the loss `L` change?
2. If we change `w_2` a little, how does the loss `L` change?

Calculating the rate of change while looking at each input one by one is the partial derivative.

\[
\frac{\partial L}{\partial w_1}
\]

\[
\frac{\partial L}{\partial w_2}
\]

Here, the symbol \(\partial\) is understood to mean that we are looking at the rate of change with respect to one among several variables. Even before we treat the strict calculation rules, for now we keep the following two standards.

1. An ordinary derivative is the rate of change when there is one input.
2. A partial derivative is the rate of change viewed one input at a time when there are several inputs.

## A Gradient Is a Vector That Gathers Partial Derivatives

Gradient is a vector that gathers several partial derivatives.

If the loss function depends on \(w_1\) and \(w_2\), the gradient can be written as follows.

\[
\nabla L =
\left[
\frac{\partial L}{\partial w_1},
\frac{\partial L}{\partial w_2}
\right]
\]

The symbol \(\nabla\) is read as nabla. Here, the meaning matters more than the symbol itself.

1. We inspect how the loss changes when each parameter is changed a little.
2. We gather those rates of change into one bundle.
3. That bundle is the gradient.

In P2-3, we looked at a vector as `a bundle of several numbers arranged in order`. A gradient is also a vector. But it is not a vector that gathers just any numbers. It is a vector that gathers the rate of change of each direction.

Rewritten in slightly more practical language, it becomes the following.

1. If there is only one control value that affects the result, one rate of change is enough.
2. If there are several control values that affect the result, we must look at the rate of change of each control value together.
3. That bundle is the gradient.

## A Gradient Carries Direction Information

The reason gradient matters is that it has meaning beyond being a bundle of numbers. In a function made of several variables, the gradient connects to the direction in which the value increases most rapidly.

At an introductory level, it is enough to remember the following.

1. The gradient direction is the direction in which the function value increases most rapidly.
2. The direction opposite the gradient is the direction in which the function value decreases.

In AI learning, we usually want to reduce loss. So, rather than the gradient itself, the direction opposite the gradient often becomes important.

But here, we only treat the point that a gradient connects to the direction of increase. How far to move, how to choose the learning rate, and how to perform repeated updates are treated in gradient descent.

## Read It Through a Small Example

Let us think about the following loss function.

\[
L(w_1, w_2) = w_1^2 + w_2^2
\]

This function grows as \(w_1\) and \(w_2\) move farther from 0.

The partial derivatives with respect to each parameter are the following.

\[
\frac{\partial L}{\partial w_1} = 2w_1
\]

\[
\frac{\partial L}{\partial w_2} = 2w_2
\]

So the gradient becomes:

\[
\nabla L = [2w_1,\ 2w_2]
\]

If the current values are \(w_1 = 3\), \(w_2 = 4\), then the gradient is:

\[
\nabla L = [6,\ 8]
\]

This means that, at the current position, the loss increases in the \(w_1\) direction and also in the \(w_2\) direction. If we want to reduce the loss, we naturally think of the opposite side.

```text
current position: [3, 4]
gradient: [6, 8]
intuitive direction for reducing loss: toward [-6, -8]
```

This example is much simpler than a real deep-learning model. But it helps establish the intuition that `a gradient is direction information made by gathering the rates of change of many parameters`.

## Gradient Examples That Appear in Practice

Gradient may appear more suddenly in practice documents than in a mathematics classroom. In the field, it is usually connected to the question `if we change something, in which direction does the result move?`

| Practical Situation | Several Inputs | Result We Want to Watch | Gradient-Style Question |
| --- | --- | --- | --- |
| product operations | price, discount rate, ad spend | revenue or profit | If we change one value a little, which result changes most sensitively? |
| recommendation system | freshness, popularity, personal preference score | recommendation score | Which weight change greatly changes the recommendation ranking? |
| search ranking | keyword match, document quality, click signal | ranking score | Which signal contributes more strongly to score change? |
| model learning | many parameters | loss | Which parameter should be adjusted in which direction to reduce the loss? |

This table is a simplified example of optimization in real services. In reality, data quality, experiment design, user behavior, policy constraints, and cost must also be considered together. Here, when first reading gradient, we organize it as the following question.

When there are several control values that create the result, we must ask together how the result changes when each control value is changed a little.

In AI learning, this question changes into the relationship between loss and parameters. Loss is the result we want to reduce, and parameters are the values adjusted inside the model. Gradient becomes the information that tells `how the loss changes along each parameter direction`.

### Example 1: A Situation Where Ad Spend and Discount Rate Are Adjusted Together

Suppose we operate an online product. Revenue is affected by several values.

1. Revenue is affected by price.
2. Revenue is also affected by the discount rate.
3. Revenue is also affected by ad spend.
4. Revenue is also affected by placement position.

At that point, the practical question is not simply `let us raise revenue`.

1. If ad spend increases a little, how much does revenue change?
2. If the discount rate increases a little, how much does revenue change?
3. If price decreases a little, how much does profit change?

These questions are all differential questions of `if we change a control value a little, how much does the result change?` If there are several control values, we must inspect the rate of change of each control value together. This intuition touches the gradient.

But in actual operations, it is not enough to look only at revenue. Revenue may rise when ad spend increases, but profit may fall. Sales volume may rise when discounts grow, but brand policy or inventory policy may be affected. Gradient is a language for reading direction, not a tool that replaces the whole decision process.

### Example 2: A Situation That Creates a Recommendation Score

A recommendation system does not create a result from only one reason. For example, we can imagine that the recommendation score of some content depends on the following factors.

1. The recommendation score is affected by similarity to the user's interests.
2. The recommendation score is also affected by the freshness of the content.
3. The recommendation score is also affected by the popularity of the content.
4. The recommendation score is also affected by how much it duplicates content the user has already seen.

In practice, the following questions appear.

1. If we make freshness more important, how does the recommendation result change?
2. If we make popularity more important, do we end up repeatedly recommending only popular content?
3. If we make similarity more important, do new discoveries decrease?

The work of seeing how the recommendation score changes when the weight of each factor changes a little connects to gradient-style thinking. Real recommendation systems also consider user satisfaction, diversity, fairness, and safety, but the point that `several inputs create the result together` becomes a good practical intuition for understanding gradient.

### Example 3: A Situation Where Loss Is Reduced in Model Learning

In AI model learning, the control values are not prices or ad spend that a person touches directly. They are parameters inside the model.

1. Loss is affected by parameter `w_1`.
2. Loss is also affected by parameter `w_2`.
3. Loss is also affected by parameter `w_3`.
4. In the same way, it is affected by many more parameters.

During learning, the following questions are repeated.

1. If we change `w_1` a little, does the loss decrease or increase?
2. If we change `w_2` a little, how sensitively does the loss change?
3. In which direction should countless parameters be adjusted together?

The information needed for these questions is the gradient. That is why, in deep-learning documents, gradient appears not as an abstract mathematical term but as the core signal for deciding in which direction learning should move next.

## Expressions Often Seen Together in Practice

If you understand the gradient, the following expressions feel less unfamiliar when you encounter them.

| Expression | Introductory Meaning | Where We Will See It Again Later |
| --- | --- | --- |
| gradient | a vector that gathers the rate of change along several input directions | this Section |
| gradient descent | a method of reducing loss by moving in the direction opposite the gradient | after P2-6 |
| learning rate | the value that decides how far to move at one time | in explanations of gradient descent |
| optimizer | a method that decides how to adjust parameters | in the machine learning and deep learning parts |
| backpropagation | the procedure that computes and passes gradients in a neural network | in the deep learning part |

Here, we do not explain all these expressions in full detail. We keep the center as `gradient is direction information that gathers several rates of change`.

## Why Does Gradient Repeat in AI Learning?

An AI model may have many parameters. In a deep-learning model, that number can become very large. Learning can be read as the process of adjusting these parameters to reduce loss.

At that point, the needed questions are the following.

1. If each parameter changes a little, how does the loss change?
2. Are there parameters that change the loss greatly?
3. In which direction should we move so that the loss decreases?

Gradient is the key language for answering these questions. That is why words such as gradient, gradient descent, and backpropagation repeatedly appear in machine learning and deep-learning documents.

Here, do not remember gradient only as the result of a calculation. Remember it as `a vector that gathers the rates of change of several directions`.

## View It Through a Case

### Case 1. When the Recommendation Score Is Not Made by Only One Knob

Suppose we operate a content recommendation screen. The recommendation score is calculated by reflecting together several factors such as `similarity to the user's interests`, `freshness`, and `popularity`. When people adjust the rules manually, they usually touch the knobs one by one, saying things like `let us raise freshness a little` or `let us reduce the weight of popularity`.

The problem is that this way alone makes it hard to see at once in which direction the whole score changes sensitively. If freshness is raised, exposure to new content may increase, but the match to personal taste may fall. If popularity is lowered, diversity may grow, but click-through rate may decrease.

At that point, the language of partial derivative and gradient becomes necessary. If we look separately at how much the score changes when each factor is changed a little, that is a partial derivative. If we gather those rates of change into one bundle, that is a gradient. In other words, it is the way of reading at once `which knob shakes the result more strongly in which direction?`

A checkable result is to compare the amount of score change when each weight is adjusted a little in the current recommendation score. For example, if the freshness weight is increased by 0.05, how much do the top 20 recommendations change, and if the popularity weight is lowered by 0.05, how much does the click-prediction score fall? Looking at this makes it clearer why a `bundle of rates of change` is needed.

## Checklist

- You can explain a derivative as the instantaneous rate of change with respect to one input.
- You can distinguish a derivative coefficient from a derivative function.
- You can explain a partial derivative as the rate of change viewed separately for one among several inputs.
- You can explain a gradient as a vector that gathers several partial derivatives.
- You can explain why a gradient may feel more unfamiliar than ordinary one-variable differentiation.
- You can explain that a gradient connects to the direction in which the function value increases rapidly.
- You can explain a gradient in practice as `the information used to see in which direction to change one among several control values`.
- You can distinguish gradient-style questions in product operations, recommendation systems, and model-learning examples.
- You can explain the broad flow in which, in AI learning, a gradient is used to find the direction that reduces loss.
- You can distinguish what `derivative`, `partial derivative`, and `gradient` each point to.

## Sources and References

- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-24.
- OpenStax, [Calculus Volume 3, 4.6 Directional Derivatives and the Gradient](https://openstax.org/books/calculus-volume-3/pages/4-6-directional-derivatives-and-the-gradient){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-24.
