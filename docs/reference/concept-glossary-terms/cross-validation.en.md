<a id="cross-validation"></a>

## cross-validation

- Meaning: Cross-validation is a method that splits the available data multiple times and evaluates models or settings on different validation portions. It is often used when the dataset is small or one split may be too dependent on chance.
- Why it matters: Choosing a model from one validation score can be pulled around by the accident of a particular split. Cross-validation makes the comparison more cautious by repeating validation across several splits, but it does not magically remove the need for a final test check.
- Related concepts: `validation data`, `test data`, `model selection`, `generalization`
- Core Section: `P4-4.2`
- Appears in: `P4-4.2`, `P4-5.2`, `P4-8.1`, `P4-9.1`, `P4-9.2`, `P4-9.3`
