<a id="support-vector-machine"></a>

## SVM, support vector machine

- Meaning: A classification model that searches for a boundary while trying to keep a large margin between that boundary and the closest cases from each class. Instead of only asking whether two groups can be separated, it also asks how much safety gap can be left around the boundary.
- Why it matters: SVM shows a classification intuition that considers boundary stability, not only the act of drawing a separating line. It helps distinguish a boundary that barely separates the training data from a boundary that may hold up better on new data, and it makes the closest cases central to the reader's sense of generalization. In short, SVM asks both `how should we separate the classes?` and `how much room does that separation leave?`
- Related concepts: `margin`, `decision boundary`, `kernel`, `classification`
- Core Section: `P4-13.1`
- Appears in: `P4-13.1`, `P4-13.2`
