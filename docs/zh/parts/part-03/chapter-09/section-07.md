# P3-9.7 输入和结果满足什么条件，才能被读成预测问题

> Section ID: `P3-9.7`
> Version: `v2026.07.10`

如果已经决定把问题提升成预测问题，那么现在就要把它的结构是否真的满足预测条件这一点关上。重要的不是长篇理论，而是四个检查：哪些列是输入，哪些列是结果候选，预测时点之后的信息有没有混进来，以及你究竟看到哪一段信息、要去预测哪个时点的结果。

这一节会先把四件事关上：输入/结果区分、泄漏防止、运营时点可复现性、以及时间边界。

| 先要关上的东西 | 如果改写成问题 |
| --- | --- |
| 输入和结果的区分 | 哪些列是特征，哪些列是目标候选？ |
| 防止未来信息泄漏 | 预测时点还不知道的值，有没有被混进来？ |
| 运营时点可复现性 | 训练时做出的输入，能不能在运营里按同样规则重新做出来？ |
| cutoff / horizon | 看到哪一段信息，又要去预测哪个后续结果？ |

即使样本边界保持不变，输入表达也不必只能固定成一种形式。有的情况下，一行特征向量更自然；也有的情况下，保留时间顺序的一组输入更自然。真正重要的是，不管采用哪种表达方式，先要满足的都是：`这个输入在预测时点是否真的可用`，以及`结果候选和时间边界是否已经一起被关上了`。所以这里处理的，不是`随便一张表`，而是样本边界和时间边界都已经关上的输入结构。核心不是`把表传过去`，而是`把在预测时点成立的输入/结果契约关上`。更广一点说，这里关上的，是`输入定义`、`结果定义`、`时点可用性`、`可复现性`一起匹配的预测契约。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `label leakage`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Dividing Datasets*, train/validation/test separation and real-world consistency. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }

