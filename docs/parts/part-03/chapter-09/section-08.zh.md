# P3-9.8 一次预测到底决定什么，为什么分数和策略不是同一件事

> Section ID: `P3-9.8`
> Version: `v2026.07.20`

即使已经定义了输入和结果，预测问题也仍然只关了一半。即便同样是在预测 `review_needed`，它也可能表示把单次运行放进复核队列，也可能表示调整整个最近区间的告警强度。此外，模型输出的分数，和把这个分数转成真实行动的策略，也不是同一回事。

一个预测值必须连同它对应的行动单位一起写出来，而模型分数和运营策略也必须分开来看。

| 区分 | 问题 |
| --- | --- |
| 一次预测针对的单位 | 这个值指的是一次运行、一个最近区间，还是下一条单独案例？ |
| 模型输出 | 模型输出的是分数、0/1，还是排序？ |
| 策略规则 | 这个输出会按什么规则被转成行动？ |
| 真实行动 | 是进入复核队列、暂缓，还是触发自动处置？ |

| 层级 | 例子 |
| --- | --- |
| 模型输出 | `0.82`、`warning_score` |
| 策略规则 | `0.8 以上就复核`、`只看前 10%` |
| 真实行动 | 加入复核队列、调整优先级 |

即使分数一样，只要策略不同，行动也可能不同。而且有些问题只把分数拿来`做排序`，有些问题则希望把这个数字`近似当成概率来读`。这种差别也要先写清楚。因此，一次预测的意义并不只是`吐出一个数字`，而是这个数字会经过什么规则，再导向什么行动的整套决策结构。从更大的角度看，这一节是在把`模型输出`、`判定规则`、`真实行动`拆成不同层级，让一次预测值被放进运营决策结构里来读。

## 用一个小图来看

一次预测并不会停在分数上，而要继续看这个分数经过什么策略规则，最终变成什么行动。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-8-mermaid-01-zh.mmd"
```

## 来源与参考资料

- Google, *Thresholds and the confusion matrix*。用于确认：要把模型的原始数值输出转换成类别，需要选择分类阈值；阈值不同，预测结果也可能不同。 [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Classification: ROC and AUC*。用于确认：AUC 与把正例排在负例之前的能力相关，而实际分类取决于所选择的阈值。 [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google, *Machine Learning Glossary*, `classification threshold`, `AUC`。用于确认分类阈值和 AUC 的术语依据。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
