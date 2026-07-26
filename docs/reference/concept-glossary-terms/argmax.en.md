<a id="argmax"></a>

### argmax

- Meaning: Argmax selects the position or class with the largest value among several values. In multiclass classification, it is often used to choose the class with the largest predicted probability.
- Why it matters: In multiclass settings, the key question is often `which class is largest?` rather than `does one probability exceed 0.5?` Argmax makes the final class-selection step explicit.
- Related concepts: `multinomial logistic regression`, `softmax`, `classification`
- Core Section: `P4-11.4`
