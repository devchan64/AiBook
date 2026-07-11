# P3-9.1 现在的问题应该提升到哪一层

> Section ID: `P3-9.1`
> Version: `v2026.07.11`

看现实记录时，人们常常会先反应成：`既然有事件记录，也多少有一点结果备注，那是不是可以直接提升成分类问题？` 但在现实记录里，这个想法往往太快了。有些问题确实可以做成预测问题，但也有些问题更诚实的做法，是先把它留在`更好地挑出复核候选`这一层，而且这也更符合当前的数据状态。既然解释边界已经立住，下一步就要决定：当前问题应该提升到 alert、review candidate、label prediction 中的哪一层。

首先要抓住的判断是：`当前数据究竟诚实地支撑到哪里。` alert 仅凭比较结构和差值就可以开始；review candidate 还需要优先级标准；label prediction 则需要相对稳定的目标标签和评估结构。

| 区分 | 在当前阶段的含义 | 所需证据强度 |
| --- | --- | --- |
| alert | 看到了和平时不同的变化，因此先提醒去看 | 比较结构和差值 |
| review candidate | 实际上值得人工重新确认的案例 | 变化信号 + 判断语境 + 优先级判断 |
| label prediction | 去预测已经定义好的目标标签 | 相对稳定的标签和学习结构 |

alert 是最轻的一层。只要看见了与基线不同的变化，就可以做出来。review candidate 要更重一层，不仅要有变化，还要值得由人工再次确认。label prediction 最重。它要求要预测什么的目标标签足够明确，这个标签能相对稳定地附着，而且学习与评估结构也已经准备好。

不能把这种差别只读成`问题简单还是复杂`。更重要的问题是：`在当前数据状态下，什么话可以诚实地说。` alert 仅凭比较结构也能启动，但 label prediction 需要比这更强得多的前提。因此，把问题往上提，并不是越高越好，而是意味着它变成了一个需要更强证据的问题。

现实问题里最困难的，往往正是最后这一层。比如，像`需要复核`这样的判断列可以做出来，但像`真实原因`或`细分状态类型`这样的确认标签却可能很弱。一个征兆可能来自多个原因，人也可能是在很后面才补写原因。在这种情况下，如果硬要把问题做成分类问题，就会先把复杂的问题框架搭起来，而标签质量其实还没准备好。

在当前阶段，下面三个问题要立刻确认。

- 现在真正需要的是自动匹配，还是复核优先级？
- 标签实际上够不够？
- 与其做分类问题，比较报告是不是更现实？

把这种差别写得更实务一些，会变成下面这样。

| 阶段 | 输入示例 | 输出示例 | 先要有的东西 | 如果还没有，就不要提升到这一层的东西 |
| --- | --- | --- | --- | --- |
| alert | 最近区间与基线的差异 | `注意` | 比较结构和差值 | 原因标签 |
| review candidate | 差值 + 重复性 + 判断条件 | `优先确认` | alert + 重复性 + 优先级标准 | 稳定的目标标签 |
| label prediction | 按事件整理的特征表 | `正常/异常` 或某个具体状态 | 相对稳定的目标标签和评估结构 | 在标签不足时先强行搭复杂分类问题 |

所以，并不是因为`想把问题提升到更高层`，就立刻往上走。只有当下面一层的证据积累够了，才提升到下一层。

如果像下面这样判断`现在该停在哪里`，就能减少勉强的问题类型上提。

| 当前已确认的状态 | 在这一层的产物 | 还不提升的层 |
| --- | --- | --- |
| 只稳定地看到相对基线的差异 | alert | review candidate、label prediction |
| 差异之外还有重复性和优先级标准 | review candidate | label prediction |
| 目标标签相对稳定，评估结构也存在 | label prediction | 无 |

把这张表放到真实判断流程里，通常会变成下面这个顺序。

1. 先比较最近区间和基线，做出 alert 信号。
2. 再加上重复性、样本量和判断语境，选出 review candidate。
3. 如果在这个过程中积累起相对稳定的判断标签，再考虑 prediction problem。

也就是说，预测问题不是起点，而是在前面几层的证据和结构都足够清楚之后，才值得讨论的事情。有些问题，最终一直停留在 comparison report 和 review queue，反而会更诚实。只凭比较结构就已经能很好支撑的判断，没有必要硬抬成 label prediction 问题。

## 用一个小图来看

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-1-mermaid-01-zh.mmd"
```

这张图说明，把问题往上提，并不是`无条件上升一层`，而是一个要问当前证据到底到了哪一层的分支判断。它不是在列标签名称，而是在一层层判断：是停在`alert`，还是走到`review candidate`，还是再提升成`label prediction`。关键在于：`alert 是变化信号，review candidate 是复核优先级，而 label prediction 是比它们都更强的问题设定。` 现在的问题能提升到哪一层，判断标准不应该是`是不是更高级`，而应是`当前数据究竟诚实地支撑到哪里`。

## 来源与参考资料

- U.S. Bureau of Labor Statistics (BLS), *BLS Handbook of Methods: Glossary*, baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" }
- National Cancer Institute (NCI), *NCI Dictionary of Cancer Terms: baseline*, baseline. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Glossary*, `label`, `labeled example`, `proxy labels`, 确认日 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- NIST/SEMATECH, *e-Handbook of Statistical Methods: What are Control Charts?*, signal detection and process monitoring. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" }
