<a id="decision-boundary"></a>

### 决策边界(decision boundary)

- 含义：decision boundary 是分类模型在 input space 中分开不同 class 区域的标准线、标准面，或更高维的标准。在 logistic regression 中，通常可以读成 linear score \(z\) 等于分类标准的位置。
- 为什么重要：有了 decision boundary，才能说明某个输入为什么被放到某个 class，也能说明边界附近案例为什么常被留作 review 对象。threshold 改变时，它还帮助我们把 model score、运营标准和实际 class 区域分开读取。
- 相关概念：`logistic regression`, `threshold`, `classification`, `hyperplane`
- 中心 Section：`P4-11.2`
- 出现 Section：`P4-11.3`, `P5-1.2`
