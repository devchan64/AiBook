<a id="weighted-sum"></a>

## weighted sum

- Meaning: A weighted sum multiplies each input by its own weight and then adds the results into one value. For example, \(x_1w_1 + x_2w_2\) folds two inputs into one score while reflecting them with different strengths.
- Why it matters: Many AI model calculations, including linear layers, matrix multiplication, and attention scores, repeat this pattern. The term keeps the role of the weight clear: a weight is not just a number being multiplied, but a value that controls how strongly an input is reflected.
- Related concepts: `weight`, `linear combination`, `matrix multiplication`, `activation function`
- Core Section: `P2-3.3`
- Appears in: `P5-1.1`, `P5-1.2`
