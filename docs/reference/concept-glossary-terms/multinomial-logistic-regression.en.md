<a id="multinomial-logistic-regression"></a>

### multinomial logistic regression

- Meaning: Multinomial logistic regression extends logistic regression to problems where the model chooses one class from three or more classes by creating class-specific scores and turning them into a probability distribution.
- Why it matters: It carries the binary-classification intuition of `score -> probability -> class selection` into multiclass comparison. In multiclass settings, the reader usually needs to inspect the whole probability distribution and the argmax choice rather than a single 0.5 threshold.
- Related concepts: `logistic regression`, `softmax`, `classification`
- Core Section: `P4-11.4`
