<a id="cross-entropy"></a>

## cross-entropy

- Meaning: Cross-entropy is a probability-based loss that becomes larger when the model assigns a low probability to the correct answer. It is often used in classification and next-token prediction.
- Why it matters: It reads not only whether the top answer was correct, but also how much probability the model gave to the correct candidate. This connects classification loss, softmax output, and LLM next-token loss.
- Related concepts: `loss function`, `softmax`, `log loss`, `next-token prediction`
- Core Section: `P5-4.2`
- Appears in: `P5-4.1`
