# P2-2.3 Limits and the Intuition of Change

> Section ID: `P2-2.3`
> Version: `v2026.07.09`

In P2-2.2, we read sigma as compressed notation for repeated addition. Now we move to another unfamiliar-looking notation: the limit.

\[
\lim_{x \to a} f(x)
\]

A limit is slightly different from the feeling of "just plug in the value exactly." It is notation for observing where the output of a function gets closer to as some value gets closer. In AI documents, the limit itself is less important than the intuition it connects to: rate of change, derivatives, gradients, and optimization.

Here, we read a limit notation by asking, "What is getting closer to what?" and explain that this becomes the preparation stage for small changes in a function and for derivatives.

Here, we reorganize again `limit`, `convergence`, `rate of change`, `substitution`, and `approach`. If 2.2 read the notation of repetition and aggregation, here we organize the notation used when reading how a function reacts as one value changes only a little.

From the reader's viewpoint, one more step is needed here. If you stop only at reading a limit as `the tendency of getting closer`, understanding can stop. What is really needed in Part 2 is the next question as well: `When it gets a little closer, how much does the function value change?`

## Scope of This Section

This section handles limits at the level of reading formula notation. It does not handle the rigorous \(\epsilon\)-\(\delta\) definition, proofs of continuity, or calculations of derivative formulas. Rate of change, derivatives, and gradients return in `P2-4.1`, `P2-4.2`, and `P2-4.3`.

The question to solve first here is this: `Why is directly substituting a value different from looking at the tendency near that value, and why does that difference lead into rate of change?`

So this section first fixes only the following four places.

- What does it mean that something approaches something else?
- How is a limit different from substitution?
- How does a small change reveal the change of a function?
- Why does a limit continue into derivatives and optimization?

| Term | Very Short Meaning | Role in This Section |
| --- | --- | --- |
| limit | notation that observes the tendency as something gets close to a value | the central symbol of this section |
| convergence | the phenomenon that a value gets closer to a certain value | the easiest language for reading limits |
| rate of change | how much the output changes compared with a change in input | the starting point of derivative intuition |
| substitution | the calculation of directly placing a certain value into an expression | the basic action that must be distinguished from limits |
| approach | the viewpoint that examines the neighborhood even without becoming exactly equal | the core intuition of limits |

If the previous section's sigma read the notation that repeats and gathers many data points, here we move into notation that reads how a function reacts when one value is moved only a little. In the immediately following sections on derivatives, gradients, and optimization, this viewpoint of small change becomes more concrete as slope and the direction of loss reduction.

This section sets the standard for reading `how does something change as it gets closer?` The details of derivative formulas and optimization calculations are recovered later.

The flow after this section is also simple.

- In Chapter 4, this viewpoint of `approach` is read more directly as rate of change and derivatives.
- In Chapter 6 and Part 4, we read again how the learning direction changes when loss is changed a little.
- So here, the goal is not to complete the limit itself, but to fix the entrance into the language of change that comes next.

## A Small Bridge Example to Look at First

The smallest scene that moves from limits into derivatives can be seen as follows.

\[
f(x) = x^2
\]

Move the value around `x = 2` a little.

| Input `x` | Function value `f(x)` | Difference from the previous value |
| --- | ---: | ---: |
| 2.0 | 4.0000 | - |
| 2.1 | 4.4100 | 0.4100 |
| 2.01 | 4.0401 | 0.0401 |
| 2.001 | 4.004001 | 0.004001 |

The first thing the reader should see in this table is that as `x` gets closer to 2, `f(x)` also gets closer to 4. But if you go one step further, you begin to want not only to ask `where is it getting close to?`, but also `how fast is it changing?` That question leads directly to rate of change, and then to derivatives in the next chapter.

So the limit is not an endpoint. It is a bridge.

- To what value is `x` getting close?
- To what value is `f(x)` getting close?
- During that process, how quickly is the function value changing?

Only when this third question appears does the limit connect properly to the entrance of derivatives.

Once you understand limits, many later topics become easier to read. In particular, you start to gain the sense of seeing `the tendency near a value` rather than only `one exact point`.

- When learning derivatives, it becomes easier to understand why we think about the ratio of a very small change.
- When reading gradients, it becomes easier to accept the language that asks in which direction loss changes.
- When learning optimization, it becomes easier to understand the flow of changing values little by little to find a better direction.
- In numerical computation, it becomes easier to feel why very small values, values near 0, and approximations must be handled carefully.
- In deep-learning training explanations, it becomes visible that the phrase `the direction that reduces loss` is not only a metaphor, but is connected to the language of function change.

## Goals of This Section

- You can read a limit as `notation that observes values getting closer`.
- You can explain the difference between \(x \to a\) and \(f(x) \to L\).
- You can distinguish a limit from simple substitution.
- You can explain convergence as the phenomenon that values get closer to one value.
- You can connect the intuition of a small change and the intuition of rate of change.
- You can explain why limits prepare you for reading derivatives, gradients, and optimization later.
- You can read a limit notation by separating the moving value, the value being approached, and the function value being observed.
- You can try simple limit expressions by direct substitution, algebraic rearrangement, and checking nearby values.

## Three Criteria

The following three viewpoints act as standards while reading the main text.

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| A limit looks at the tendency near a point rather than the point itself | It keeps substitution and limits from being mixed together. | Understand that you first read `what is getting close to what`. |
| A limit is notation for observing nearby change rather than just plugging in a value | It creates the sense for reading behavior near a point that may be special or undefined. | Understand that substitution and limits are different. |
| The reason limits connect to AI is that they prepare for derivatives, which read how much a small change affects the result | It builds the bridge into derivatives and optimization in advance. | Understand that a limit is the preparation stage for the intuition of rate of change. |

## Reading Limits from a Math-Education Viewpoint

In mathematics education, a limit is usually taught as "the value of a function when something gets arbitrarily close." Here, instead of memorizing that sentence, we split the roles inside the notation.

\[
\lim_{x \to a} f(x) = L
\]

This one line contains four pieces of information.

- \(\lim\): the mark that says we will observe a tendency of approaching
- \(x \to a\): the input `x` is getting close to `a`
- \(f(x)\): the function value we are observing at that time
- \(L\): the target value to which the function value gets close

If you separate it like this, a limit stops feeling like a difficult calculation symbol and starts reading like a sentence that observes a situation of approaching.

1. `x` gets close to `a`.
2. At that time, look at `f(x)`.
3. Check whether `f(x)` gets close to `L`.

What matters in this viewpoint is distinguishing `gets closer` from `is equal`. A limit is notation for reading the tendency seen in the neighborhood. Whether the function is actually defined at that exact point, or whether you can substitute that exact value directly, must be checked separately.

## Convergence Is the Phenomenon of Getting Close

One phrase often met in Korean mathematical language is convergence. Convergence is the phenomenon in which values get closer and closer to one value.

If values get closer to one value, you can say they converge to that value.

A limit is used to express and confirm whether this kind of convergence is happening, and if it is, to what value it is happening. So the following sentence is natural.

\[
\lim_{x \to a} f(x) = L
\]

That is read as, `when x gets closer to a, f(x) converges to L`.

Still, you should not use limit and convergence as if they were completely identical words. Convergence is the phenomenon of getting close, while a limit is the concept and notation used to express or confirm that value of getting close. If values do not get closer to one value, then you say they do not converge, and it becomes difficult to speak of that limit in that form.

We do not prove convergence deeply here. But it helps understanding if, when you see a limit notation, you ask `what is converging to what?`

## A Simple Limit Example

You build the intuition for limits by trying short examples directly. The easiest case is when direct substitution works without a problem.

\[
\lim_{x \to 2}(x + 1)
\]

This expression asks where `x + 1` gets close to when `x` gets close to 2. In this case, there is no problem even if you substitute `x = 2` directly.

\[
2 + 1 = 3
\]

So you can write the following.

\[
\lim_{x \to 2}(x + 1) = 3
\]

In this case, you can say that as `x` gets close to 2, `x + 1` converges to 3.

But not every limit ends this way. In the following expression, if you directly put in \(x=1\), the denominator becomes 0.

\[
\lim_{x \to 1}\frac{x^2 - 1}{x - 1}
\]

So first rearrange the expression.

\[
x^2 - 1 = (x - 1)(x + 1)
\]

\[
\frac{x^2 - 1}{x - 1} = \frac{(x - 1)(x + 1)}{x - 1}
\]

For nearby values where \(x\) is not exactly 1, you can cancel \(x-1\) and look at it as follows.

\[
\frac{x^2 - 1}{x - 1} = x + 1 \quad (x \ne 1)
\]

Then, when `x` gets close to 1, `x + 1` gets close to 2.

\[
\lim_{x \to 1}\frac{x^2 - 1}{x - 1} = 2
\]

Even here, what matters is not the substitution value at exactly 1, but the fact that as `x` gets close to 1, the expression converges to 2.

The key here is not to stop at "if the denominator becomes 0, then it is impossible." If direct substitution does not work, first rearrange whether the nearby form can be seen more clearly, and then confirm the value being approached. Even this level of intuition is enough to prepare for reading later notation of rate of change and derivatives.

## A Limit Reads the Process of Getting Close

Look at the following notation.

\[
\lim_{x \to a} f(x) = L
\]

This expression is read as follows.

1. Look at when `x` gets close to `a`.
2. Check whether `f(x)` gets close to `L`.

What matters here is not that `x` is exactly equal to `a`. It is that as `x` gets closer to `a`, the function value `f(x)` gets closer to some value `L`.

When you read a limit, separate the following.

- \(x \to a\): to what is the input getting close?
- \(f(x)\): what function value is being observed?
- \(L\): to what is the function value getting close?

So a limit is not notation that looks at just one value. It is notation that looks together at the direction of getting closer and the result during that process.

## Substitution and Limits Can Be Different

It is easy to understand a limit as "just try plugging in the value." In fact, in many simple functions, the value after substituting \(x=a\) and the limit value are the same.

\[
f(x) = x + 1
\]

\[
\lim_{x \to 2} f(x) = 3
\]

Here, if you plug in \(x=2\), you also get \(f(2)=3\). So substitution and limit look the same.

But the core of the limit is not substitution. It is the process of getting closer. Some expressions are hard to compute directly at one specific point, or may not be defined there, and still you can observe where they get close in the neighborhood.

\[
g(x) = \frac{x^2 - 1}{x - 1}
\]

If you directly put in \(x=1\), the denominator becomes 0. But if you inspect the nearby form, you can rearrange it as follows.

\[
g(x) = \frac{(x - 1)(x + 1)}{x - 1}
\]

\[
g(x) = x + 1 \quad (x \ne 1)
\]

So when `x` gets close to 1, `g(x)` gets close to 2.

\[
\lim_{x \to 1} \frac{x^2 - 1}{x - 1} = 2
\]

This example shows that a limit is not "put in exactly that value," but rather "look at where it gets close to in the neighborhood."

## A Small Change Reveals the Change of a Function

In AI learning, what matters is how a function value changes. If the input changes a little, how much does the output change? If a parameter changes a little, how much does the loss change? These become important.

Suppose there is a very simple function.

\[
f(x) = x^2
\]

When \(x\) is 2, the function value is the following.

\[
f(2) = 4
\]

Now increase `x` a little.

\[
f(2.1) = 4.41
\]

The input changed by `0.1`, and the function value changed by `0.41`.

1. The input changes from 2 to 2.1.
2. The output changes from 4 to 4.41.

This observation is the starting point of rate of change.

\[
\frac{f(2.1) - f(2)}{2.1 - 2}
\]

This expression looks at `how much the function value changed compared with how much the input changed.` We do not compute derivatives yet here. What matters is the viewpoint that tries to see the change of the function as a ratio.

If you narrow the same scene further, the bridge toward rate of change becomes clearer.

| Compared Interval | Input Change | Output Change | Rate of Change |
| --- | ---: | ---: | ---: |
| 2.0 -> 2.1 | 0.1 | 0.41 | 4.1 |
| 2.0 -> 2.01 | 0.01 | 0.0401 | 4.01 |
| 2.0 -> 2.001 | 0.001 | 0.004001 | 4.001 |

As the interval becomes smaller, the rate of change gets closer to 4. Here, you do not yet need to use the word derivative in full. The core point the reader should hold is that the old question of `what is getting closer to what` is now changing into the new question `to what is the change ratio getting closer?`

## A Limit Leads into Derivatives

A derivative is the idea of looking at the rate of change for a very small change. If you narrow an average rate of change into a smaller and smaller interval, you begin to see in what direction and by how much a function changes near one point.

In the previous example `f(x) = x^2`, when the interval near `x = 2` became smaller and smaller, the rate of change got closer to 4. This one scene shows the connection between limits and derivatives in the shortest possible way.

1. First, the input gets close to some value.
2. Then, you look at where the function value gets close.
3. Next, you also look at where the change ratio gets close.
4. That question continues into instantaneous rate of change and derivatives.

So the limit in Chapter 2 recovers the language for reading `getting close`, and the derivative in Chapter 4 recovers the language for reading `direction and size of change` by using that getting-close structure.

\[
\frac{f(x+h) - f(x)}{h}
\]

This expression looks at how much the function value changes when you move by `h` from `x`. If you send `h` closer and closer to 0, you can begin to think about the rate of change near one point.

\[
\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
\]

This notation leads into the core intuition of the derivative. Still, we do not handle derivative formulas or calculation rules here. Hold only the point that `a limit is the notation that looks at the tendency as a small change becomes smaller and smaller, and therefore becomes the language of derivatives`.

## Why Is It Needed in AI Learning?

In machine learning and deep learning, learning is usually explained as the process of adjusting parameters so that loss decreases. At that time, the important questions are the following.

- If the parameter is changed a little, how does the loss change?
- In which direction does loss decrease?
- What problem appears if the value is changed too much?

These questions continue into rate of change and gradient. A limit is the notation that lets you think about this rate of change more precisely.

Put simply, the following flow appears.

When a function value changes, you compare the change amount, then look at the rate of change, then read the tendency of a very small change, and that flow continues into derivatives and gradients, eventually helping you find the direction that reduces loss.

So a limit is not notation that directly runs an AI model. It is preparation for reading the explanation that learning `changes values little by little while searching for a better direction`.

## The Order for Reading a Limit

When a limit notation appears, read it in the following order.

1. What is moving?
2. To what is it getting close?
3. What function value is being observed?
4. To what is that function value getting close?
5. Is this notation preparing for rate of change or derivatives?

For example, look at the following expression.

\[
\lim_{h \to 0} \frac{f(x+h)-f(x)}{h}
\]

This can be read as follows.

- `h` gets close to 0.
- Look at the change in the function value after moving by `h` from `x`.
- Divide that change amount by `h` to see the rate of change.
- Make `h` smaller and smaller, and observe the tendency of change near one point.

This expression reappears in P2-4.1 and P2-4.2 when reading derivatives and rate of change again. Here, understand it as `notation that looks at a small change`.

## Case Study

### Case 1. Why Must We Look at How Much the Result Changes When Loss Changes a Little?

A learner may see a limit and first ask, "Where is this used in AI?" Even if the limit itself is not directly computed often, that intuition is needed because model learning constantly asks `if the value is changed a little, how does the loss change?`

For example, suppose you want to know whether loss increases sharply or barely changes when one parameter is raised only a little. At that point, what matters is not just one exact point value, but the viewpoint that looks at how the function changes in the neighborhood of that point and in which direction.

A limit is precisely the notation that reads this `tendency while getting close`. So the phrase `send h toward 0` is not just a formal trick, but the preparation stage for looking at the ratio in a very small change. This flow continues into derivatives and gradients later.

This case connects limits not to an isolated mathematical concept, but to the stage just before reading learning direction. Right now, what matters more than proving the formula completely is grasping the feeling that `we are looking at the tendency of a small change`.

## Why Limits Feel Difficult

Limits feel difficult not because the calculation itself is difficult, but because the way of expression is unfamiliar. In particular, when the approaching input, the function value at that time, and the difference between exact substitution and neighborhood tendency all mix together, the notation can feel hard.

When recovering limits for the first time, it is better to unpack them in words before moving to rigorous proof. For example, you should first be able to ask, `When x gets close to a, where does f(x) get close to?` and `When h gets close to 0, to what value does the change ratio get close?`

Once you can ask these questions, you are prepared to read derivatives and gradients later.

## Perspective to Remember from This Section

A limit is notation for looking not at `put in exactly that value`, but at `to what does the result get close when a value gets close to something`.

The input gets close to some value, the function value is observed, the change ratio is read, and that sense continues into derivatives and gradients.

In AI learning, you need to know how values change in order to reduce loss. A limit is the entrance into the mathematical language that reads that change.

This viewpoint returns again when derivatives are redefined in P2-4.1 and P2-4.2, when gradients are read in P2-4.5, and when optimization and loss reduction are explained in P2-6.1 and P2-6.3. A limit is not itself an AI learning algorithm, but it remains in the background as `the language for reading the tendency of a small change`.

## Short Check

- Can you explain a limit as notation that looks at a process of getting closer?
- Can you distinguish the meanings of \(x \to a\), \(h \to 0\), and \(f(x) \to L\)?
- Can you explain that a limit and simple substitution do not always mean the same thing?
- Can you explain convergence as the phenomenon that values get closer to one value, without declaring it identical to a limit?
- Can you explain the relationship between a small change and a rate of change?
- Can you explain why limits prepare you for reading derivatives, gradients, and optimization?
- Can you explain why limits return later in derivatives, gradients, optimization, and numerical computation?
- Can you compute the approached value in a simple limit expression either by direct substitution or by algebraic rearrangement?

## When Should You Recall This Perspective First?

- When you are reading a limit as if it meant the same thing as direct substitution
- When you lose the connection of why a small change and the tendency of a function value continue into derivatives and optimization
- When you need to look again at what change happens in the neighborhood of one point rather than only at the value of that point

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-06-24.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-06-24.
- Catherine F. Higham, Desmond J. Higham, [Deep Learning: An Introduction for Applied Mathematicians](https://arxiv.org/abs/1801.05894){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, checked on 2026-06-24.
