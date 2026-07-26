<a id="hessian"></a>

## 海森矩阵

- 含义：海森矩阵收集多变量函数的二阶导数信息。 在本书的 boosting 语境里，可以把它入门地读成：损失函数在当前预测附近弯得有多敏感的二阶信息。
- 为什么重要：如果 gradient 先回答 `模型该往哪个方向动`，hessian 会再补充 `沿着这个方向动时要多谨慎`。 有些 boosting 实现在计算 split 和 leaf value 时会同时使用二阶信息，所以这个词能帮助读者理解为什么实现比较里会出现 hessian。
- 相关概念：`梯度(gradient)`，`损失函数(loss function)`，`梯度提升(gradient boosting)`
- 中心 Section：`P4-16.3`
- 出现 Section：`P4-16.3`
