# P2-4.5 Gradient Supplement: From School Differentiation to Multivariable Differentiation

> Section ID: `P2-4.5`
> Version: `v2026.07.12`

In P2-4.3, we connected derivative, partial derivative, and gradient, and in P2-4.4, we looked at why differentiation is needed in learning.

Here, we provide supplementary learning to reduce the unfamiliarity that appears when moving from school-level differentiation memory to the gradient. The representative explanation of `gradient` stays in P2-4.3, and the representative explanation of `gradient descent` stays in P2-6.3. This Section more slowly organizes only the background needed to fill the gap between them. When you want to check terms quickly again, you can also look at the [concept glossary](../../../reference/concept-glossary.md).

This Section reads mainly background concepts that passed quickly in the main text, such as supplementary learning, directional derivative, and vector calculus. Instead of pushing `gradient`, `gradient descent`, and `backpropagation` as formulas from the beginning, the goal is to recover what kind of concepts they are trying to look at.
The purpose is to make the jump from one remembered slope to many-direction change feel readable again.

From the reader's point of view, this Section can feel especially long. So it helps more to enter by first organizing briefly `where does the school-level differentiation memory break?`

## The Break Point to See First

| School Memory | Why It Gets Stuck Here | Expression to Hold Again in This Section |
| --- | --- | --- |
| one-variable function `y = f(x)` | the moment the number of inputs grows, the number of questions is no longer one | multivariable function |
| one slope | loss reacts to many parameters at the same time | a bundle of several partial derivatives |
| slope of a tangent line | we rarely separated axis directions from arbitrary directions | partial derivative, directional derivative |
| differentiation formula calculation | in learning, `which way should we move?` matters more than the result of the calculation itself | gradient, gradient descent |
| solving one differentiation problem | in deep learning, we must compute many gradients efficiently | backpropagation |

If you hold this table first, it becomes clearer that the unfamiliar-looking terms are not `new mathematics`, but rather `the memory of one-variable rate of change extended into many directions`.

## Fix the Definitions First

In this supplementary learning, we first place working distinctions for reading AI learning documents rather than strict university-level definitions. At the same time, we do not copy the representative definitions of the same Part at length again, and leave only the connections needed in this Section.

| Term | Working Definition |
| --- | --- |
| derivative | the rate of change showing how much the output changes when one input changes by a very small amount |
| partial derivative | the rate of change calculated by assuming that, among several inputs, only one has changed |
| directional derivative | the rate of change showing how much the function value changes when moving a little in a chosen direction |
| gradient | a vector that gathers several partial derivatives in order |
| vector calculus | a mathematical system that deals together with vectors, functions, and rates of change on spaces |
| gradient descent | a repeated method that uses the gradient to change parameters little by little toward lower loss |
| backpropagation | the procedure that efficiently computes the gradient of each parameter in a deep-learning model |

Said briefly, a derivative is the rate of change in one direction, and a partial derivative is the value obtained by looking at several directions one by one. A directional derivative is the way of reading change in a direction that I choose, and a gradient is a vector that gathers such rates of change into one bundle. Gradient descent is the method of moving by referring to that vector, and backpropagation is the procedure that computes that vector efficiently inside a deep-learning model.

## Scope of This Supplementary Learning

Here, the role is to act as a bridge from school-level differentiation memory to the gradient.

The following topics are too large to treat deeply here.

- the strict calculation of partial derivatives
- the formula of the directional derivative
- the full system of vector calculus
- the update formula of gradient descent
- the calculation procedure of backpropagation

But that does not mean we leave those concepts behind with only their names. Here, we provide definitions, analogies, learning order, and charts that can be understood at the high-school level. It means we are not going deep into calculation, not that we avoid explaining the concepts.

Here, we focus on the following questions.

- Why does the gradient feel unfamiliar?
- What is different between one-variable differentiation and multivariable differentiation?
- What do partial derivatives and directional derivatives see differently?
- How are gradient and gradient descent connected?
- Why does backpropagation appear later?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| supplementary learning | an additional explanatory section that fills the gap between main sections | the formal role of this Section |
| directional derivative | the rate of change viewed in the direction I choose | the expanded concept that must be distinguished from partial derivatives |
| gradient descent | a method that repeatedly moves toward lower loss | the connection point that recalls the representative explanation in P2-6.3 |
| backpropagation | the procedure that computes the gradient efficiently | the connection point that leads into deep learning |
| vector calculus | the mathematical frame that deals with vectors and rates of change on spaces | the perspective that sees the background of the gradient more broadly |

## How Should We Study It?

This Section continues in the following order.

1. Recall differentiation again as the rate of change in one direction.
2. Think that, when there are many inputs, there are also many directions.
3. Understand that a partial derivative is the method of looking at those directions one by one.
4. Understand that a directional derivative is the rate of change seen in a direction I choose.
5. Understand that a gradient is a vector that gathers several partial derivatives into one bundle.
6. Understand that gradient descent is a repeated method of lowering loss by referring to that vector.
7. Understand that backpropagation is the procedure that computes the gradient efficiently in a deep-learning model.

When reading this flow, it helps to keep asking together: `what is changing?`, `in which direction is it changing?`, `does that change increase or decrease the loss?`, `why must rates of change from many directions be gathered?`, and `how does model learning use that bundle?`

These questions become the starting point when we meet optimization, gradient descent, and backpropagation again later.

## Goals of This Supplementary Learning

- You can explain why the gradient may feel unfamiliar when starting only from school-level differentiation memory.
- You can explain the difference between a single-variable function and a multivariable function.
- You can explain a partial derivative as the rate of change viewed one input at a time among many inputs.
- You can explain a directional derivative as the rate of change viewed along a chosen direction.
- You can explain a gradient as a vector that gathers several partial derivatives.
- You can explain gradient descent as a repeated method that lowers loss by using the gradient.
- You can distinguish backpropagation as the procedure that computes gradients efficiently in a deep-learning model.

## Three Criteria

| Criterion | Why It Matters | Level of Understanding Needed in This Section |
| --- | --- | --- |
| First see why a supplementary section is needed | because the gap between school-level differentiation memory and AI learning's multivariable differentiation is large | Understand it as a recovery section that bridges one-variable differentiation to multivariable differentiation. |
| Distinguish gradient, gradient descent, and backpropagation | If these three words are mixed as if they had the same role, the learning procedure becomes hard to read. | Understand that gradient is directional information, gradient descent is a method of moving, and backpropagation is a calculation procedure. |
| See role and connection before calculation | If the concept is fixed first, later formulas and optimization explanations break less. | Understand each term at the level where you can explain what kind of concept it is trying to look at. |

## Midway Summary: Where Have We Come So Far?

If we fold the connections up to this point briefly, the order is as follows.

| Stage | One-Sentence Summary |
| --- | --- |
| derivative | look at how much the output changes when one input is changed a little |
| partial derivative | when there are many inputs, change them one by one separately |
| directional derivative | look at change not only along axis directions, but along a chosen direction |
| gradient | gather several partial derivatives into one vector |
| gradient descent | move in the direction that lowers loss by using that vector |
| backpropagation | compute that vector efficiently in deep learning |

Once this middle table is visible, even if the main text becomes long, the reader can return to what level of explanation they are reading now.

## School Differentiation Memory Usually Starts from One Direction

When we think of school-level differentiation, we usually remember `y = f(x)`, the slope of a tangent line, instantaneous rate of change, derivative coefficient, derivative function, and speed and acceleration.

Most of this flow starts from a function with one input.

\[
y = f(x)
\]

Then the question is relatively simple. It asks `if x changes a little, how much does y change?`

So the rate of change is also easy to understand as one direction. It is like seeing how much the height changes when we move a little forward on a line.

In other words, one input \(x\) corresponds to one output \(y\), and the intuition of reading the slope at one point of that relationship was the starting point of school-level differentiation.

This memory is very important. Gradient is not a concept that throws away that memory. It is a concept that expands that memory when there are many inputs.

The chart below shows the flow by which one-direction differentiation expands into partial derivatives in many directions and then into a gradient.

![Flow that expands one-variable differentiation into partial derivatives and a gradient in many directions](/AiBook/assets/part-02/chapter-04/gradient-single-to-multiple-directions-en.svg)

## Why the Gradient Feels Unfamiliar

There are usually two reasons that gradient feels unfamiliar.

First, a gradient appears naturally in a function with many inputs.

\[
z = f(x, y)
\]

Now the questions increase to more than one, such as `if x changes a little, how does z change?` and `if y changes a little, how does z change?`

Second, the result of a gradient does not end as one number. It appears as a vector.

If we look together at the rate of change in the \(x\)-direction and the rate of change in the \(y\)-direction, it becomes a vector that bundles the two values.

If school-level differentiation memory is used to `one slope`, then a gradient looks like `a bundle of slopes`. That is why it becomes easy to wonder whether it is part of the same family of differential concepts or some entirely new mathematics.

## A Partial Derivative Is the Rate of Change Seen One by One

Let us look at one multivariable function.

\[
L(w_1, w_2)
\]

In the AI context, we may think of \(L\) as loss and of \(w_1\) and \(w_2\) as parameters.

Looking at how \(L\) changes when only \(w_1\) is changed a little is the partial derivative with respect to \(w_1\).

\[
\frac{\partial L}{\partial w_1}
\]

Looking at how \(L\) changes when only \(w_2\) is changed a little is the partial derivative with respect to \(w_2\).

\[
\frac{\partial L}{\partial w_2}
\]

Here, understand a derivative as the rate of change when there is one input, and a partial derivative as the rate of change when one input is viewed separately among many inputs.

Even if the strict calculation method is treated later, what matters now is the intuition of `looking at sensitivity one control value at a time among many`.

## A Directional Derivative Is the Rate of Change Seen Along the Direction We Want

Partial derivatives usually look at axis directions one by one. The reference directions are fixed, such as the \(w_1\)-direction and the \(w_2\)-direction.

A directional derivative asks a slightly more general question.

Instead of the axis direction, it asks how much the function value changes if we move in some direction that I choose.

Partial derivatives and directional derivatives both deal with rates of change, but they look in different directions. In the chart below, the partial derivative is distinguished as the rate of change that looks at axis directions one by one, while the directional derivative is the rate of change that follows an arbitrary direction.

![Chart comparing the directions observed by partial derivatives and directional derivatives](/AiBook/assets/part-02/chapter-04/partial-vs-directional-derivative-en.svg)

Here, we do not calculate the formula of the directional derivative. What we need now is the following distinction.

A partial derivative is the rate of change seen along a reference axis direction, and a directional derivative is the rate of change seen along a direction I chose.

## A Gradient Is a Vector That Gathers Several Partial Derivatives

Gradient is a vector that gathers several partial derivatives in order.

\[
\nabla L =
\left[
\frac{\partial L}{\partial w_1},
\frac{\partial L}{\partial w_2}
\right]
\]

This expression contains in one bundle the answers to the two questions: `if we change w_1, how does the loss change?` and `if we change w_2, how does the loss change?`

In practical language, it becomes the following.

If there is only one control knob, one slope is enough. But if there are many knobs, we must look at the rate of change for each knob together. That bundle of rates of change is the gradient.

The point that a gradient is a vector also becomes natural here. A vector is an expression that gathers several numbers in order. Among such vectors, a gradient is the vector that gathers `the rate of change of each direction`.

Vector calculus is the wider mathematical language that deals with this relationship more broadly. Here, instead of learning the whole system, we only confirm that if we read the direction of change at each point of a scalar field, it becomes a gradient, and if such vectors are placed over space, they can be seen as a vector field.

![Chart showing where scalar fields, gradients, and vector fields connect in vector calculus](/AiBook/assets/part-02/chapter-04/vector-calculus-context-en.svg)

## What Direction Does the Gradient Tell Us?

A gradient connects to the direction in which the value increases most rapidly in a multivariable function. In AI learning, we usually want to reduce loss. So, rather than the gradient itself, the direction opposite the gradient often becomes more important.

The gradient direction connects to the side where loss grows, and the direction opposite the gradient connects to the side where loss becomes smaller.

The chart below shows how, at one point of a loss function, the gradient direction and the direction that reduces loss become opposites.

![Chart comparing the gradient direction and the descending direction on contours of a loss function](/AiBook/assets/part-02/chapter-04/gradient-direction-loss-contour-en.svg)

What matters here is that a gradient does not tell us the whole map. It tells us direction information near the current position. It tells us which side from the current position is likely to increase the value and which side is likely to decrease it.

## Why Is the Gradient Needed in AI Learning?

In AI learning, we want to reduce loss. Loss tells us how wrong the model currently is, but the loss value alone makes it hard to know which parameter should be changed in which direction.

If the loss is large, it means the current result is not good. But we still do not know what should be changed or how.

The gradient tells us how the loss changes when each parameter is changed at the current position.

The gradient is the bundle that gathers the loss's rate of change with respect to each parameter, and when we want to find the direction that reduces loss, the clue becomes the direction opposite the gradient.

This leads to gradient descent. In other words, in a loss function with many parameters, the gradient is the bundle of rates of change that tells us in which direction the value changes.

## How Should We Read the Name Gradient Descent?

The name gradient descent itself can feel unfamiliar. If we break the English expression apart, it becomes a little easier.

| Expression | Introductory Meaning |
| --- | --- |
| gradient | the direction in which the value increases most rapidly at the current position |
| descent | going down, moving toward the lower side |
| gradient descent | a repeated method that uses the gradient as a clue and moves toward the side where the value becomes lower |

Written in a definition-like way, gradient descent is an optimization method that repeatedly calculates the gradient of the loss function at the current parameter position and moves the parameters a little in the direction in which the loss decreases.

This sentence contains four elements.

| Element | Meaning |
| --- | --- |
| current parameter position | the current state of the numbers inside the model |
| loss function | the criterion that calculates how wrong the current model is |
| gradient | the bundle of rates of change that tells us in which direction and by how much the loss changes |
| move a little | adjusting the value by a small step instead of changing it drastically all at once |

That is why gradient descent is often explained with the analogy of coming down from a mountain. From the current position, we look at the surrounding slope and move a little in the direction that becomes lower. We do not teleport to the correct place at once. We move a little and then check the slope again, repeating this process.

Like the chart below, gradient descent is not a method that moves to the center in one jump. It moves a little in the direction where loss decreases from the current position, then reads the direction again from the new position.

![Chart showing gradient descent as repeated small movement toward lower loss](/AiBook/assets/part-02/chapter-04/gradient-descent-steps-en.svg)

In other words, it repeats the process of looking at the loss at the current position, reading the direction of change through the gradient, moving a little toward the side where loss decreases, and then looking at the loss again.

## What Does the Gradient-Descent Update Mean?

Gradient descent is usually explained with an update expression like the following.

\[
w_{\text{next}} = w - \eta \nabla L
\]

We do not need to calculate this formula fully right now. But we can understand what role each symbol is playing.

| Symbol | Introductory Meaning |
| --- | --- |
| \(w\) | the current parameter value |
| \(w_{\text{next}}\) | the next parameter value |
| \(\nabla L\) | the directional information about how loss changes at the current position |
| \(\eta\) | the learning rate that decides how far to move at one time |
| \(-\eta \nabla L\) | the small amount of movement toward the side where loss decreases |

The word `a little` is important here. If we move too far, we may overshoot the lower place. If we move too little, it may take too long. We meet this movement width again under the name learning rate in P5-7.1.

The chart below shows the update expression of gradient descent intuitively. Memorizing the formula is not the goal, but we should remember the structure `move a little from the current value in the direction opposite the gradient by the amount of the learning rate`.

![Chart showing that the gradient-descent update means moving a little from the current value in the direction opposite the gradient](/AiBook/assets/part-02/chapter-04/gradient-descent-update-intuition-en.svg)

Another important point is that gradient descent is not a magical method that always guarantees the perfect answer. It is a method that tries to go in a better direction by using the slope seen at the current position. The result can differ depending on the starting position, the shape of the loss function, the movement width, and the number of repetitions.

Here, we organize only up to the point that the gradient gives directional information at the current position. How to choose the learning rate, when to stop the repetition, and how to compute across many parameters are treated again in P2-6.3.

## Backpropagation Is Not the Same Thing as Gradient Descent

Backpropagation is connected to gradient descent, but it is not the same thing.

Gradient descent is an optimization method that uses the gradient to adjust values, while backpropagation is the procedure that efficiently computes the gradients of many parameters inside a deep-learning model.

A deep-learning model is a structure in which the calculations of many layers are connected. The input passes through many layers, becomes an output, and from that output the loss is calculated.

We can read it as a structure such as `input -> layer 1 calculation -> layer 2 calculation -> output -> loss`.

To learn, we must know how the loss changes with respect to the parameters of each layer. Backpropagation is the procedure that computes this information efficiently by passing it from the back toward the front.

As in the chart below, the forward pass calculates values from input to output and loss, while the backward pass calculates from the loss backward how much each layer's parameters affect the loss.

![Chart comparing the direction of computation in the forward pass and the direction in which gradients are sent back in backpropagation](/AiBook/assets/part-02/chapter-04/backpropagation-gradient-flow-en.svg)

Here, we separate them as follows: gradient descent deals with how to change values in order to reduce loss, and backpropagation deals with calculating how much each layer's parameters affect the loss.

## Words We Should Use Carefully from the Curriculum Viewpoint

In the 2022 revised Korean high school curriculum, `AI Mathematics` includes loss functions and gradient descent. So it may be inaccurate to say that `there is nothing in the high school curriculum that connects to gradient at all`.

However, `AI Mathematics` may not be a familiar course title to readers who learned school mathematics a long time ago. For such readers, it is natural not to think of loss functions or gradient descent as part of high school mathematics. Here, rather than treating that memory as wrong, we explain again by connecting it with the flow newly confirmed in the current curriculum.

Based on the checked text of the high school curriculum documents, the terms `gradient`, `partial derivative`, and `directional derivative` were not found. The gradient descent in `AI Mathematics` is also closer to the level of intuitively understanding a loss function defined as a one-variable function and its derivative coefficient.

So here, we state that although loss functions and gradient descent may be introduced in the high school curriculum, the system of gradient and partial derivatives may still need separate supplementary explanation.

This wording respects both the reader's learning memory and the scope of official materials.

## What We Leave as Supplementary Learning

Here, we do not need to calculate the gradient completely. Instead, remember the following boundaries.

| Distinction | Understanding Needed Now |
| --- | --- |
| derivative | the instantaneous rate of change with respect to one input |
| partial derivative | the rate of change viewed one by one among several inputs |
| directional derivative | the rate of change viewed in a chosen direction |
| vector calculus | the wider mathematical language that deals together with rates of change and vectors in space |
| gradient | a vector that gathers partial derivatives |
| gradient descent | the repeated method that uses the gradient to reduce loss |
| backpropagation | the procedure that computes the gradients of many parameters efficiently |

The calculations by which partial derivatives continue into gradient descent reappear in P2-6.3, how loss is passed to each weight reappears in P5-5.1 and P5-5.2, and the actual update rules reappear in P5-7.1 and P5-7.2. For now, the goal is to hold how the terms connect to each other and why they repeatedly appear in AI learning.

## Perspective to Keep from This Section

Gradient is not a completely separate world from the differentiation learned in school. It is the expression that appears when familiar differentiation expands to a function with many inputs.

Derivative is the rate of change in one direction, and a partial derivative is the rate of change viewed separately among many directions. Gradient is a vector that gathers the rates of change of many directions, and gradient descent is the repeated method that lowers loss by using that vector. Backpropagation is the procedure that computes that vector inside a deep-learning model.

In AI learning, a model has many parameters. So, to reduce loss, one rate of change is not enough. We need a bundle of rates of change. That bundle is the gradient.

## View It Through a Case

### Case 1. When We Must Read a Mixer Panel with Many Control Knobs at Once

Suppose we are handling an audio mixer panel. There are many knobs such as volume, bass, treble, and reverb, and the final sound is the result made by those values together. When a person adjusts it by hand, they usually turn one knob at a time while listening for questions such as `did the sound become clearer?` or `did the voice become too thin?`

But as the number of knobs grows, one adjustment begins to get entangled with other properties. If we raise the treble, clarity may improve, but the sound may become harsh. If we increase reverb, the sound may feel richer, but speech may become blurred. The intuition of `change just one thing and see` is still valid, but overall we need to read the rates of change of many directions together in order to adjust more stably.

That is also why gradient supplementary learning is needed. School differentiation is closer to the intuition of seeing the change when one knob is turned, while multivariable differentiation and gradient are closer to the intuition of reading a panel that has many knobs at once. Gradient descent is the repeated method of adjusting little by little in the direction that improves the result, and backpropagation can be seen as the procedure that efficiently calculates how much each knob matters inside a complex machine.

A checkable result is to record how the final sound-quality score changes when each knob is adjusted by only a very small amount. For example, we can compare how much the noise score grows when the volume is raised by one step, or how much the speech-clarity score improves when the bass is lowered by one step. Then we can intuitively see the difference between `the rate of change in one direction` and `the bundle of rates of change in many directions`.

## Checklist

- You can explain that school-level differentiation memory mainly starts from the rate of change of a one-variable function.
- You can explain that the gradient naturally appears in a function with several inputs.
- You can explain a partial derivative as `the rate of change viewed one input at a time among several inputs`.
- You can explain a directional derivative as `the rate of change viewed in a chosen direction`.
- You can explain a gradient as `a vector that gathers partial derivatives`.
- You can explain gradient descent as `the repeated method that reduces loss using the gradient`.
- You can explain backpropagation as `the procedure that efficiently computes the gradients of many parameters`.
- You can explain that, even in the high school `AI Mathematics` curriculum, gradient descent appears, but the systems of gradient and partial derivatives may still need separate supplementary explanation.
- You can explain the gap between school-level differentiation and the later language of gradient, gradient descent, and backpropagation.

## Sources and References

- Ministry of Education, `Ministry of Education Notice No. 2022-33 [Appendix 4] High School Curriculum (I)`, checked 2026-06-24.
- Ministry of Education, `Ministry of Education Notice No. 2022-33 [Appendix 4] High School Curriculum (II)`, checked 2026-06-24.
- Ministry of Education, `Ministry of Education Notice No. 2022-33 [Appendix 4] High School Curriculum (III)`, checked 2026-06-24.
- KOCW, `Calculus 2: 14.7 Directional Derivatives and the Gradient`, checked 2026-06-24.
