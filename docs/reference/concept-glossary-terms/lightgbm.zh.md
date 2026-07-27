<a id="lightgbm"></a>

## LightGBM

- 含义：LightGBM 是面向大规模表格数据的高效梯度提升决策树库。 它常和 histogram-based splitting、leaf-wise growth、GOSS、EFB 等效率化策略一起讨论。
- 为什么重要：LightGBM 说明即使同属 boosting，也会有优先追求更快、更轻重复训练的实现选择。 当 stage 数和数据规模变大时，速度与内存折中也会成为模型选择的一部分。
- 相关概念：`梯度提升(gradient boosting)`，`过拟合(overfitting)`
- 中心 Section：`P4-16.3`
- 出现 Section：`P4-16.3`
