<a id="argmax"></a>

### argmax

- 含义：argmax 是从多个值中选择最大值所在位置或 class 的运算。在 multiclass classification 中，它常用来选择 predicted probability 最大的 class。
- 为什么重要：多类别场景里，关键问题常常不是 `有没有超过 0.5`，而是 `哪个 class 最大`。argmax 会把最终 class selection 这一步明确表示出来。
- 相关概念：`multinomial logistic regression`, `softmax`, `classification`
- 中心 Section：`P4-11.4`
