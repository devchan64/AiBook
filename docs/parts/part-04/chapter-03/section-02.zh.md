# P4-3.2 启发式与模型选择

> Section ID: `P4-3.2`
> Version: `v2026.07.17`

在 P4-3.1 里，我们把 heuristic 看成 `在有限时间和有限信息下缩小候选集的判断标准`。这一节要把这个视角应用到 model selection 上。

学习机器学习时，`到底该用哪个 model？` 这个问题常常会显得很大。但 model selection 并不是单纯挑一个有名算法名字，而是把问题形态、数据状态、可解释性、计算成本、评估标准一起摆出来，然后先缩小 `应该先试什么` 的候选集合。

这里 heuristic 不是最终结论，而是出发点。你会先决定 `这个问题先从这些 model 开始试`，然后再去验证这种选择在真实数据上到底是否合适。

这一节不会再次把 heuristic 本身讲很长。`缩小候选集的判断` 这一基础含义，会通过 P4-3.1 和 [概念词汇表](/AiBook/en/reference/concept-glossary/) 再接回来；这里专注的是，这种判断在 model selection 阶段到底怎样发挥作用。

## 本节范围

这一节先把 `model selection 中 heuristic 缩减的是什么，以及它会建立怎样的比较起点` 关上。数据拆分和 validation 会在 P4-4 继续处理，overfitting 和 generalization 会在 P4-5 继续处理，metric 会在 P4-6 继续处理，preprocessing 和 feature 会在 P4-7 继续处理，model selection 的流程会在 P4-8 继续处理，hyperparameter tuning 会在 P4-9 继续处理。具体 model 会从 P4-10 到 P4-19 按问题类型再次遇到。

这一节回答下面这些问题。

- 在 model selection 里，heuristic 到底缩减的是什么？
- 问题类型会怎样缩小 model 候选？
- 为什么需要 baseline model？
- performance、interpretability、cost 会怎样彼此冲突？
- 如果想把 heuristic 留成可验证的记录，应该写下什么？

## 本节目标

- 能把 model selection 解释成 `缩小候选并进行验证的流程`，而不是单纯挑 model 名字。
- 能说明为什么随着问题类型不同，先看的 model 候选也会不同。
- 能说明 baseline model 是用来判断复杂 model 是否值得使用的比较基准。
- 能理解 model selection 不只受 performance 影响，还会同时受到 interpretability、计算成本和当前数据状态影响。
- 能学会把 model-selection heuristic 记录成 working hypothesis。

## 先用一个场景来理解

想一想一个小型客户流失预测项目。数据里有客户最近登录次数、购买金额、咨询次数、订阅时长。目标是找出下个月更可能流失的客户。

在这个场景里，可选 model 很多。但一开始就把所有 model 全试一遍，并不一定是好的起点。

| 候选 | 为什么会先想到它 | 要小心什么 | 后面会在哪里再处理 |
| --- | --- | --- | --- |
| logistic regression | 在预测流失/留存这类两类输出时，它是很自然的简单 baseline。 | 只靠线性关系可能不够。 | P4-11 |
| decision tree | 很容易解释 `在什么条件下流失增加`。 | 如果长得太深，可能过度贴合训练数据。 | P4-14 |
| random forest | 把很多树组合起来，往往能期待更稳定的表现。 | 比单棵树更难解释。 | P4-15 |
| gradient boosting | 在表格型数据上经常能表现很强。 | 调参与验证要更谨慎。 | P4-16 |

这里 heuristic 并不是说 `logistic regression 就是答案`。它更像是在安排实验顺序：`先立一个简单 baseline，再比较解释性和性能是否还需要更强的候选。`

把这个判断画成案例流程后，就会更清楚地看到：model selection 不是 `挑名字`，而是 `根据问题与约束先缩小候选，再做一个小比较集合`。

```mermaid
--8<-- "assets/part-04/chapter-03/churn-model-selection-flow-zh.mmd"
```

## 模型选择是缩小候选集的过程

model selection 通常会按下面这样的流程推进。

```mermaid
--8<-- "assets/part-04/chapter-03/model-selection-basic-flow-zh.mmd"
```

这里最重要的一点是：它并不试图一步就猜中最终 model。它会先看问题类型，再确认约束，再立 baseline，然后比较一个小候选集合。如果 validation 结果不好，就再次调整候选集合。

## 先根据问题类型缩小第一轮候选

最先要看的，是问题类型。要预测的是数值、类别，还是没有标签的结构，这会直接改变你首先想到的候选。

| 问题 | 问题类型 | 首先想到的候选 | 后面会在哪里再处理 |
| --- | --- | --- | --- |
| 要预测像房价、营收、温度这样的数字吗？ | regression | linear regression、tree-based regression | P4-10、P4-14 |
| 要预测像通过/未通过、流失/留存这样的类别吗？ | classification | logistic regression、decision tree | P4-11、P4-14 |
| 想在没有标签时寻找相似分组吗？ | clustering | k-means、DBSCAN | P4-17 |
| 想把很多 feature 压成较少的轴吗？ | dimensionality reduction | PCA、t-SNE | P4-18 |
| 是在选择动作并接收 reward 吗？ | reinforcement learning | Q-learning、policy gradient | P4-19 |

这张表不是答案表，而是缩小候选的地图。真正的选择仍然要通过数据和评估结果再次确认。

## baseline model 是比较基准

baseline model 不是一开始就为了拿到最好性能的 model。它是用来判断 `复杂 model 到底值不值得上` 的比较基准。

例如，在流失预测里，就算完全不用 model，只是一直预测 `大部分用户不会流失`，accuracy 也可能看起来不低。此时，如果一个复杂 model 只把 accuracy 稍微提高一点，也很难说它就真的有实际价值。还必须一起看 precision、recall、cost 和业务目的。

baseline model 会帮助回答下面这些问题。

- 它有没有比完全不用 model 的简单规则更好？
- 复杂 model 到底有没有比简单 model 好到值得使用？
- 性能提升是否值得牺牲解释性或运营成本？
- 在当前数据条件下，是不是该先修数据质量，而不是继续推 model？

baseline 会在 P4-8.2 里更详细地处理。这里先只把它当成 model-selection heuristic 的第一个固定比较点。

## 不能只按 performance 来选

在 model selection 里，performance 很重要。但如果只按 performance 来选，实务中很容易出问题。

| 基准 | 要问的问题 | 例子 |
| --- | --- | --- |
| performance | validation data 上目标指标够好吗？ | 在 recall 很重要的问题里，不能只看 accuracy。 |
| interpretability | 人能不能解释并检查结果？ | 如果业务人员必须理解规则，简单 model 可能更合适。 |
| computational cost | 训练和预测时间是否可接受？ | 在实时服务里，prediction latency 会很重要。 |
| data requirement | 它适合当前数据规模和质量吗？ | 如果数据太少，复杂 model 可能会很不稳定。 |
| operability | 能不能部署、监控、再训练？ | 就算 model 很好，如果难以运营，也可能失败。 |

这些基准会相互冲突。容易解释的 model 可能性能一般，而性能强的 model 可能更贵或更难解释。model-selection heuristic 的作用之一，就是提前把这些冲突显露出来。

## 常见的模型选择 heuristic

下面这些 heuristic 在前期实验中经常使用。但全部都仍然需要 validation。

| heuristic | 为什么可以用 | 一定要确认的点 |
| --- | --- | --- |
| 先做一个简单 model。 | 可以很快立住 baseline。 | 要确认简单 model 是否已经足够，以及复杂 model 是否真的更好。 |
| 按问题类型分候选。 | regression、classification、clustering 的目标不同。 | 要重新确认实际目标是否定义清楚。 |
| 如果业务要求解释，就先看可解释 model。 | 因为结果可能需要解释给人听。 | 不能因为好解释就忽视 performance 风险。 |
| 数据小的时候，不要急着上很复杂的 model。 | overfitting 风险可能更高。 | 仍要检查数据拆分和 validation 结果。 |
| 对 feature scale 敏感的 model，要连同 preprocessing 一起看。 | k-NN、SVM 这类 model 会受距离与尺度影响。 | preprocessing 条件要公平地纳入比较。 |
| 如果连 baseline 都很弱，先怀疑数据。 | 问题可能在 label、缺失值或样本，而不在 model。 | 要重新检查数据质量和问题定义。 |

这些 heuristic 不是 `永远都要这样做` 的规则，而是让前期探索更有秩序的起点。

在真实工作里，更核心的是先判断：`当前应该先缩减哪些 model 候选。`

| 当前问题状态 | 先缩减到哪一类候选 | 原因 |
| --- | --- | --- |
| 输出是类别，而且解释性也很重要 | 先看 logistic regression、decision tree 这类简单分类候选 | 因为它们很适合快速比较 baseline 和规则感。 |
| 在表格型数据里怀疑存在非线性关系 | 把 tree family 候选一起放进来 | 因为它们更可能抓到 feature 交互。 |
| 当前比起 label，更需要结构探索 | 把方向切到 clustering 或 dimensionality reduction 候选 | 因为此时目标是先理解结构，而不是比较 prediction model。 |
| 连 baseline 都非常弱 | 先回头重看数据和 label，而不是继续换 model | 因为问题定义或数据质量可能已经先不稳。 |

## heuristic 必须被记录下来

如果 heuristic 只留在脑子里，就很难验证。在 model selection 过程中，必须记录：为什么先看这个 model、担心什么、以及以后按什么标准决定是否更换。

| 记录项 | 例子 |
| --- | --- |
| 选中的候选 | 先比较 logistic regression 和 decision tree。 |
| 选择理由 | 这是一个流失分类问题，而且需要解释性。 |
| 预期风险 | 线性关系可能不够，或者 tree 可能会过拟合。 |
| 验证方式 | 用 P4-4 会处理的 validation data 来比较。 |
| 评估标准 | 一起看 P4-6 会处理的 recall 和 precision。 |
| 下一步动作 | 如果没有明显优于 baseline，就回头重看数据和 feature。 |

像这样写下来，heuristic 就不再是 `凭感觉挑的`，而会变成 `从一个可验证的 working hypothesis 出发`。

## 这一节里要小心的误解

在 model selection 里，最常见的误解之一，就是认为越有名的 model 就一定越好。现实里，如果数据很少、label 不稳定、或者解释性非常重要，简单 model 反而可能更合适。

第二个误解，是只看一个 validation score 就决定 model。这也可能导致过度贴合 validation data。这个问题会在 P4-5 的 overfitting 和 generalization 里再次处理。

第三个误解，是把 model selection 看成纯粹的 model 问题。如果性能不好，在把 model 变复杂之前，应该先确认 data、label、feature、evaluation 基准 是否真的适合当前问题。

## 案例与示例

### 案例 1. 客户咨询分类里，应该先比较哪一种 model？

假设客服中心想把咨询自动分成 `退款`、`配送延迟`、`账户问题`、`商品咨询`。业务人员到现在为止，一直是通过标题里有没有 `退款`、`取消`、`配送` 等词，先用手工规则做初步分类。

这种方式在起步时很快，但只要表述稍微变化，漏掉的咨询就会变多。像 `我想退款` 这种句子能抓到，但 `这笔支付能取消吗` 这种换了说法、意思相近的句子，就很容易被规则漏掉。于是，团队必须在 `直接上最复杂 model` 和 `继续只用原规则` 之间找到起点。

这时 model-selection heuristic 可以变成：`先用 logistic regression 这类简单 baseline，看文本分类大致能走到什么程度；然后再比较是不是还需要更强的性能或更好的解释性。` 接着再把 decision tree 或更强的候选加进来比较，就能看见 `复杂度上升之后到底有没有真正收益`。

真正可检查的结果也很明确。你可以比较 baseline model 和 rule-based classifier 的错误类型，再看各个 class 的 precision 和 recall，就能知道到底是哪一类咨询得到了改善。如果 baseline 已经能稳定抓住大多数重复咨询，就可以把更复杂 model 延后。反之，如果在表达变化很大的咨询上持续出错，就应该考虑更强的表示模型。

```mermaid
--8<-- "assets/part-04/chapter-03/inquiry-classification-model-selection-flow-zh.mmd"
```

## Checklist

- 能不能说明为什么 model selection 不是 `挑一个有名 model`，而是 `先缩小候选集`？
- 能不能说明在什么状态下，比起继续加复杂度，更应该先重新检查 data 和 label？
- 能不能说明为什么 baseline model 会成为解释复杂候选性能的比较基准？
- 能不能说明，model selection 不是猜 model 名字，而是缩小候选并验证的过程？
- 能不能说明，问题类型是缩小 model 候选的第一基准，而 baseline model 是比较复杂候选的最小标准？
- 能不能说明为什么 performance、interpretability、computational cost、data state、operability 必须一起看？

## 来源与参考资料

- scikit-learn developers, `Choosing the right estimator`, scikit-learn User Guide, 确认日期：2026-06-25. [https://scikit-learn.org/stable/machine_learning_map.html](https://scikit-learn.org/stable/machine_learning_map.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, 确认日期：2026-06-25. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, 官方网站确认日期：2026-06-25. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
