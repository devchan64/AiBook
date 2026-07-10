# P3-9.12 即使 target 名称相同，为什么也要先写清哪种错误更痛

> Section ID: `P3-9.12`
> Version: `v2026.07.10`

即使 target 名称相同，不同问题里更痛的错误也可能不一样。哪怕都是在预测 `review_needed`，漏掉风险案例更危险，还是把本来不需要的人也送去复核更有负担，都会随着运营语境不同而改变。也就是说，即使 target 相同，漏判和误报的成本也可能不同，所以必须先把这种差别写下来，才能明确当前更想减少的是哪一种判断错误。

| 错误类型 | 在运营里可能发生的事情 |
| --- | --- |
| false negative | 漏掉风险案例，可能扩散成更大的异常 |
| false positive | 人会白白花时间，增加复核负担 |

| 先写下的备注 | 为什么需要 |
| --- | --- |
| 哪种错误更痛？ | 为了固定当前要优先减少哪类判断 |
| 这种成本在真实运营中以什么形式出现？ | 为了把它解释成行动负担，而不只是数字 |
| 当前更想减少什么？ | 为了即使 target 相同，也能固定解释方向 |

所以，不要只靠准确率就把问题关上，而是先要看：为什么`想优先减少哪一类错误`这件事必须先写出来。这一节把`漏判成本`、`过检成本`和`判定规则调整`捆在一起，先固定错误成本结构，再看它如何改变目标的解释方式。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `false negative`, `false positive`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Thresholds and the Confusion Matrix*, threshold choice under asymmetric costs. [https://developers.google.com/machine-learning/crash-course/classification/thresholding](https://developers.google.com/machine-learning/crash-course/classification/thresholding){: target="_blank" rel="noopener noreferrer" }

