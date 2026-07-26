<a id="penalty"></a>

## penalty

- Meaning: A penalty is an extra cost added to an objective function so a model prefers some solutions less. In logistic regression settings, it usually refers to the regularization form, such as L1, L2, or Elastic-Net, that controls how conservatively coefficients are kept.
- Why it matters: Changing the penalty can change how the model avoids large coefficients, whether some coefficients are pushed toward zero, and which solver combinations are supported. Performance and coefficient comparisons therefore need the penalty setting recorded separately.
- Related concepts: `regularization`, `objective function`, `solver`
- Core Section: `P4-11.5`
- Appears in: `P4-11.5`
