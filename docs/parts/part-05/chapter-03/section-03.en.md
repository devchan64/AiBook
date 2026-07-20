# P5-3.3 Tanh

> Section ID: `P5-3.3`
> Version: `v2026.07.20`

In P5-3.2, we saw how the sigmoid compresses scores into the range between 0 and 1. Tanh also makes an S-shaped compression, but differs in that its output range is from \(-1\) to \(1\).

Tanh becomes an important comparison point when you want to keep both negative and positive values while building a representation centered on 0.

## The Question Of Tanh's Zero-Centered Transformation

- What formula and output range does tanh have?
- Why is it called zero-centered, unlike the sigmoid?
- Why is it important that it keeps both negative and positive signs?
- What kind of limit does the saturation range of tanh create?

The formula comparison that also includes the sigmoid and ReLU is organized together in P5-3.5. The problem of output-layer choice is handled separately in P5-3.6.

## Standards For Keeping Negative And Positive Signals

- You can explain tanh as `a zero-centered function that compresses values between -1 and 1`.
- You can understand that tanh keeps negative and positive signs more directly than the sigmoid.
- You can say that saturation appears at large positive and large negative values.
- You can explain what kind of feel tanh gives in hidden-layer representation.

## The Formula Of Tanh

Tanh is written as follows.

\[
\tanh(z)=\frac{e^z-e^{-z}}{e^z+e^{-z}}
\]

The result of this formula is always between \(-1\) and \(1\).

- If \(z\) is a large positive value, the output becomes close to 1.
- If \(z=0\), the output is 0.
- If \(z\) is a large negative value, the output becomes close to -1.

Unlike the sigmoid, which keeps values only between 0 and 1, tanh expresses both the negative direction and the positive direction.

## The Phrase Zero-Centered

Tanh is called zero-centered because when \(z=0\), the output is also 0, negative inputs remain negative outputs, and positive inputs remain positive outputs.

![Tanh activation-function curve](/AiBook/assets/part-05/chapter-03/tanh-curve-en.svg)

| Input range | Feel of the output | What the reader should read first |
| --- | --- | --- |
| Large negative values | Close to -1 | A stable-side or opposite-direction signal remains as a negative value. |
| Near 0 | Close to 0 | A weak change appears together with its sign. |
| Large positive values | Close to 1 | It is a strong positive signal, but the change becomes dull even if it grows more. |

This property is intuitive in hidden layers when you want to leave behind `which direction the signal points`. The values do not all gather only on the positive side, but can extend in both directions around 0.

## Cases And Examples

Suppose that while reading equipment state, one hidden node expresses both `a signal toward stability` and `a signal toward warning`. Let us say that negative values are read as the stable side, positive values as the warning side, and that as the absolute value becomes larger, the direction becomes stronger. If the output remained only at 0 or above, then both the stable side and the warning side would tend to look only like `weak/strong`, making the direction difference harder to catch at a glance.

With tanh, negative values can be read as stable-side signals and positive values as warning-side signals.

| Scene | \(z\) | Intuition of the tanh output | Judgment that remains first |
| --- | --- | --- | --- |
| Strong stable signal | \(-2\) | It stays close to -1, so the stable-side direction remains strongly visible. | The sign `it leans toward stability` is visible immediately. |
| Weak stable signal | \(-0.3\) | It is slightly below 0, so it is on the stable side but not strongly. | It can be read as `toward stability, but still close to neutral`. |
| Almost neutral | \(0\) | It remains at 0, so it does not lean strongly to either side. | The direction is not fixed strongly yet. |
| Weak warning signal | \(0.3\) | It is slightly above 0, so it is on the warning side but not strongly. | It can be read as `toward warning, but still weak`. |
| Strong warning signal | \(2\) | It stays close to 1, so the warning-side direction remains strongly visible. | The sign `it leans strongly toward warning` is visible immediately. |

What should be read first in this case is that `left and right split around 0`. \(-0.3\) and \(0.3\) are both small values, but one is on the stable side and the other is on the warning side. Tanh keeps even this weak directional difference through the sign.

The other important point is saturation. If \(z=2\) is already close to 1, then even if it moves to a larger positive value, the output difference will gradually survive less. The negative side behaves the same way: large negative values are compressed near -1.

The result to confirm in this case is that tanh is not merely a function that shrinks values, but a function that creates `an internal representation with direction centered on 0`, while also saturating toward both ends at large positive and large negative values.

## Practice And Exercise

Suppose the following values are passed into tanh.

| \(z\) | Output to predict first | Question to check first |
| --- | --- | --- |
| \(-4\) | Very close to -1 | How far down do large negative values go? |
| \(-0.2\) | Slightly below 0 | Does a weak stable-side signal remain? |
| \(0\) | 0 | Why is it called zero-centered? |
| \(0.2\) | Slightly above 0 | Does a weak warning-side signal remain? |
| \(4\) | Very close to 1 | How far up do large positive values go? |
| \(8\) | Even closer to 1 | Compared with \(4\), how much difference still remains? |

When reading this table, the following two questions must be closed directly.

1. \(-0.2\) and \(0.2\) are both small values, but why can they still be read through tanh as `weak stability` and `weak warning`, that is, as opposite directions?
2. Even if \(z=4\) is raised to \(z=8\), why does the output difference survive less strongly than when going from \(z=0\) to \(z=0.2\)?

The direction of the answer is clear. Near 0, tanh still leaves even small changes relatively directly together with their negative or positive sign, but in large positive and large negative ranges it approaches 1 and -1 respectively and compresses the difference. So when reading tanh, you should examine together `which direction it points`, `how far it is from 0`, and `whether it has already entered the saturation range`.

## Checklist

- Can you state the tanh formula and its output range from \(-1\) to \(1\)?
- Can you explain why the output becomes 0 when \(z=0\)?
- Do you understand that tanh is closer to a zero-centered representation than the sigmoid?
- Can you say that saturation appears at large positive and large negative values?
- Can you anticipate by what standard tanh will be compared in the formula comparison of P5-3.5?

## Sources And References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, date checked: 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher M. Bishop, `Pattern Recognition and Machine Learning`, Springer, 2006, date checked: 2026-07-19. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
