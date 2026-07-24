# P3-9.10 标签延迟确认与未完成的负类

> Section ID: `P3-9.10`
> Version: `v2026.07.23`

_副标题: 延迟确认的标签与尚未闭合的 0 标签应该如何区分？_

在选择[目标标签候选（target candidate）](/AiBook/reference/concept-glossary-parts/05-mieum/#glossary-target-candidate)时，必须区分`结果什么时候才算确认`，以及`是否已经观察得足够久，以至于可以贴 0 标签`。如果把这两件事混在一起，最近事件就会过早地看起来像 0，或者还处于临时状态的值会被误读成确认标签。标签确认延迟和观察尚未完成的负例，是两种不同问题，所以必须先分开。

| 区分 | 中心问题 |
| --- | --- |
| 标签确认延迟 | 结果已经出现了，但它什么时候才真正闭合为答案？ |
| 观察未完成的负例 | 到底有没有看得足够久，足以说没有发生结果？ |

例如，如果 target 设成`接下来 7 天内是否 failure`，就必须把下面两行一起写出来。

- 结果观察 horizon 是 7 天
- 在贴 0 之前，是否真的完整观察了这 7 天

| 先写下的备注 | 为什么需要 |
| --- | --- |
| 目标标签通常在什么时候确认 | 为了知道答案收集的延迟 |
| 确认前是否存在临时状态 | 为了把 `pending` 和确认状态分开 |
| 给 0 贴标签所需的最小追踪期 | 为了不把已闭合负例和未完成观察混在一起 |

## 用一个小图来看

如果读完表格以后，`还没确认`和`完整观察后贴 0`还是容易混在一起，就再顺着下面的顺序看一遍。

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-10-mermaid-01-zh.mmd"
```

所以，这里真正重要的不是`把 0 和 1 切得更细的技术`，而是一种观察完结性区分：不要把还没闭合的标签，与已经充分观察到的负例混成同一个值。这一节把`结果确认延迟`、`观察期未完成`、`状态备注`区分开来，使得标签是否已经闭合，本身就成为一个数据建模条件。

## 来源与参考资料

- Google, *Machine Learning Glossary*, `label`, `proxy labels`。用于确认术语依据：标签是一个样本的答案或结果部分，而 proxy label 是在数据集中无法直接取得标签时用来近似实际标签的数据。本节对`观察未完成的负例`的解释，是把 proxy label 的说明扩展到运营观察完结性的语境里来使用。 [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*。用于确认 provenance 视角下应保留处理步骤、可复现性、版本管理和派生关系。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Corbin, Baiocchi, Chen, *Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection*, 2023。用于区分`已闭合的 0`和`尚未观察到的状态`：如果预测时点之后缺少足够的追踪记录，部分样本的 class label 可能仍然无法被观察到。 [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
