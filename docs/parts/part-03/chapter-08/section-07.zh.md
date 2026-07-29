# P3-8.7 运营介入改变的数据解读

> Section ID: `P3-8.7`
> Version: `v2026.07.25`

_副标题: 当复核规则和处置改变后续数据时，为什么不能把它读成自然过程？_

在[解释边界](/AiBook/zh/reference/concept-glossary-pinyin/j/#interpretation-boundary)里，最后一个必须注意的点，是当前的[干预反馈(intervention feedback)](/AiBook/zh/reference/concept-glossary-pinyin/g/#glossary-intervention-feedback)。如果 `review_needed=1` 的案例被人工很快处理了，那么之后留下的数据，就可能和原本的自然发展过程不同。如果把这一点隐藏起来，`后续数据看起来更安全`这样的句子就会被写得过于轻易。

如果当前的复核规则或处置会改变后续数据和[选择性标签(selective labels)](/AiBook/zh/reference/concept-glossary-pinyin/x/#glossary-selective-labels)，那么之后的数据就不能再被当作与干预前自然发展过程具有同样含义的数据来读。

| 当前规则或处置 | 在后续数据里可能发生变化的内容 |
| --- | --- |
| 立即复核 | 可能在大异常扩散之前就采取动作，从而让后续事件减少 |
| 提前中止 | 日志长度和后续模式都可能变短 |
| 强化检查周期 | 在特定条件下可能留下更详细的记录 |

来看下面这张表。

| event_id | review_needed | intervention | failure_within_7d |
| --- | ---: | --- | ---: |
| A | 1 | immediate_check | 0 |
| B | 1 | immediate_check | 0 |
| C | 0 | none | 1 |

表面上看，`review_needed=1` 好像更安全。但实际上，A 和 B 未必天生就更安全，它们也可能只是因为先接受了处置，才让失败减少。因此，解读句子里还必须一起写明，这个结果是`干预后的结果`，还是`自然发展过程中的结果`。

| 先写下的备注 | 为什么需要它 |
| --- | --- |
| 哪个输出真正触发了处置 | 为了知道干预是从什么时候开始的 |
| 这个处置会不会改写后续日志或标签 | 为了避免把解读对象读错 |
| 你要看的是干预前信号，还是干预后的运营结果 | 为了避免把同一个结果列里的含义混在一起 |

这里关键的是：`如果当前运营规则已经在改变未来数据，那么后面看到的差异，就可能同时包含原始模式差异和干预效果。` 这一节不必被看成某个团队特有的案例，而可以看成一个更一般的问题：`观测对象是否已经会被策略与干预改变`，也就是 intervention feedback。换句话说，后续数据不一定只是自然过程的延伸，它也可能已经是当前规则和处置回馈之后的结果，因此必须连同这个背景一起解读。

## 用一个小图来看

这一节的核心，是当前规则与处置未必会把后续数据原样保留下来。只要复核规则会触发干预，而干预又会改写后续数据，那么后面看到的差异就必须拆开读成 `原始模式` 和 `干预效果`。

--8<-- "assets/part-03/chapter-08/p3-8-7-mermaid-01-zh.mmd"

## 来源与参考资料

- W3C, `PROV-Overview`。它提供了追踪某些数据和结果是经过哪些 activity 生成的 provenance 视角，因此可支持本节的说明：如果复核规则或处置会改变后续日志与标签，那么后续数据就必须连同干预背景一起阅读。 [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Google for Developers, `Datasets: Dividing the original dataset`。它说明训练/评估数据可能与真实运营中遇到的数据不同，而且相同的转换也需要在 real-world data 上重现，因此可用来一般化本节的提醒：当前运营干预会改变后续数据分布以及这些数据本身的含义。 [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
- Conor K. Corbin, Michael Baiocchi, Jonathan H. Chen, `Avoiding Biased Clinical Machine Learning Model Performance Estimates in the Presence of Label Selection`, 2023。它说明已部署的临床预测模型可能形成 feedback loop，影响 prospectively collected data 和 label selection；如果只用观测到的标签集合估计性能，结论可能偏离部署人群。因此它直接支持本节的提醒：当前复核规则和处置可能改变后续数据本身的含义。 [https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/](https://pmc.ncbi.nlm.nih.gov/articles/PMC10283136/){: target="_blank" rel="noopener noreferrer" } / 确认日: 2026-07-20
