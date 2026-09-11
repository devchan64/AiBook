# P2-2.3 Limits and the Intuition of Change

> Section ID: `P2-2.3`
> Version: `v2026.09.08`

A limit describes where a function value approaches as its input approaches a particular value.

\[
\lim_{x \to a} f(x)
\]

A limit is slightly different from the feeling of "just plug in the value exactly." It is notation for observing where the output of a function gets closer to as some value gets closer. In AI documents, the limit itself is less important than the intuition it connects to: rate of change, derivatives, gradients, and optimization.

## Changes in Input and Function Value

For the following function, let the input approach 2.

\[
f(x) = x^2
\]

Move the value around `x = 2` a little.

| Input `x` | Function value `f(x)` | Difference from `f(2)` |
| --- | ---: | ---: |
| 2.0 | 4.0000 | - |
| 2.1 | 4.4100 | 0.4100 |
| 2.01 | 4.0401 | 0.0401 |
| 2.001 | 4.004001 | 0.004001 |

As `x` approaches 2, `f(x)` approaches 4, and its difference from `f(2)` decreases.

## Substitution and Nearby Values

| Criterion | Why it matters |
| --- | --- |
| A limit describes behavior as we approach a point rather than the point itself | It keeps substitution and limits distinct. |
| A limit examines nearby changes rather than simply substituting a value | It lets us read changes near a point where the function is undefined. |
| Reducing the input change gives the limit of the rate of change | We can calculate the direction and magnitude of the function's change at a point. |

## Parts of Limit Notation

Limit notation identifies the approaching input, the function being observed, and the value that the function approaches.

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

## Solving Simple Limits

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

The key here is not to stop at "if the denominator becomes 0, then it is impossible." If direct substitution does not work, first rearrange whether the nearby form can be seen more clearly, and then confirm the value being approached.

## Input Changes and Rates of Change

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

This expression compares how much the function value changed with how much the input changed.

We can calculate the rate of change while reducing the input change.

| Compared Interval | Input Change | Output Change | Rate of Change |
| --- | ---: | ---: | ---: |
| 2.0 -> 2.1 | 0.1 | 0.41 | 4.1 |
| 2.0 -> 2.01 | 0.01 | 0.0401 | 4.01 |
| 2.0 -> 2.001 | 0.001 | 0.004001 | 4.001 |

As the interval shrinks, the rate of change approaches 4: it is `4.1` for an input change of `0.1`, `4.01` for `0.01`, and `4.001` for `0.001`.

## The Limit of the Rate of Change

A derivative is the idea of looking at the rate of change for a very small change. If you narrow an average rate of change into a smaller and smaller interval, you begin to see in what direction and by how much a function changes near one point.

In the previous example `f(x) = x^2`, when the interval near `x = 2` became smaller and smaller, the rate of change got closer to 4. This one scene shows the connection between limits and derivatives in the shortest possible way.

1. First, the input gets close to some value.
2. Then, you look at where the function value gets close.
3. Next, you also look at where the change ratio gets close.
4. That question continues into instantaneous rate of change and derivatives.

\[
\frac{f(x+h) - f(x)}{h}
\]

This expression looks at how much the function value changes when you move by `h` from `x`. If you send `h` closer and closer to 0, you can begin to think about the rate of change near one point.

\[
\lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
\]

If this limit exists, it is the instantaneous rate of change, or derivative, at that point.

## Parameter Changes and Loss

In machine learning and deep learning, learning is usually explained as the process of adjusting parameters so that loss decreases. At that time, the important questions are the following.

- If the parameter is changed a little, how does the loss change?
- In which direction does loss decrease?
- What problem appears if the value is changed too much?

These questions continue into rate of change and gradient. A limit is the notation that lets you think about this rate of change more precisely.

When a function value changes, you compare the change amount, then look at the rate of change, then read the tendency of a very small change, and that flow continues into derivatives and gradients, eventually helping you find the direction that reduces loss.

## Checklist

- Can you explain a limit as notation that looks at a process of getting closer?
- Can you distinguish the meanings of \(x \to a\), \(h \to 0\), and \(f(x) \to L\)?
- Can you explain that a limit and simple substitution do not always mean the same thing?
- Can you explain convergence as the phenomenon that values get closer to one value, without declaring it identical to a limit?
- Can you explain the relationship between a small change and a rate of change?
- Can you explain why limits prepare you for reading derivatives, gradients, and optimization?
- Can you compute the approached value in a simple limit expression either by direct substitution or by algebraic rearrangement?
- Can you explain limit as a language for reading the tendency of a small change rather than only direct substitution?

## Sources and References

- Marc Peter Deisenroth, A. Aldo Faisal, Cheng Soon Ong, [Mathematics for Machine Learning](https://mml-book.github.io/){: target="_blank" rel="noopener noreferrer" }, Cambridge University Press, 2020, checked on 2026-07-19.
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, [Deep Learning](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2016, checked on 2026-07-19.
- Catherine F. Higham, Desmond J. Higham, [Deep Learning: An Introduction for Applied Mathematicians](https://arxiv.org/abs/1801.05894){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, checked on 2026-07-19.
- OpenStax, [Calculus Volume 1, 2.2 The Limit of a Function](https://openstax.org/books/calculus-volume-1/pages/2-2-the-limit-of-a-function){: target="_blank" rel="noopener noreferrer" }, Rice University, checked on 2026-07-19. This reference supports estimating limits with tables and nearby values.
- OpenStax, [Calculus Volume 1, 3.1 Defining the Derivative](https://openstax.org/books/calculus-volume-1/pages/3-1-defining-the-derivative){: target="_blank" rel="noopener noreferrer" }, Rice University, checked on 2026-07-19. This reference supports the connection from rate of change and difference quotients to derivative intuition.
