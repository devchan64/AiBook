# P4-3.1 为什么需要启发式

> Section ID: `P4-3.1`
> Version: `v2026.07.11`

在 P4-2 章里，我们把 supervised learning、unsupervised learning、reinforcement learning 看成几种大的学习类型。接下来就会自然出现一个问题：真正去解决现实问题时，应该先看哪些数据、先试哪些 model、结果到什么程度才进入下一阶段？

这时就会出现 `heuristic` 这个词。heuristic 不是保证完整证明或最优解的规则，而是在时间和信息都有限的条件下，帮助你快速做出较为可信选择的判断标准。

heuristic 很容易被误解成 `大概猜一下`。但在机器学习实务中，heuristic 不是随机猜测，而是根据经验、问题结构、计算成本和验证结果来缩小候选集的方法。

这一节会说明 `heuristic`、`不用完全穷举而是先缩小候选的判断`、`可验证的工作假设` 这些概念。后面的章节会带着这个抓手继续判断当前语境，而 `把实务判断读成假设与验证结构` 这一层基础含义，会通过本节和 [概念词汇表](../../../reference/concept-glossary.md) 再次接回。

## 本节范围

这一节解释为什么需要 heuristic。具体的 model selection、feature selection、preprocessing、hyperparameter tuning 会在后面分别展开。模型选择 heuristics 会在 P4-8 再次处理，feature selection 和 preprocessing 会在 P4-7 再次处理，hyperparameter tuning 会在 P4-9 再次处理。

这一节回答下面这些问题。

- heuristic 是什么？
- 为什么不能把所有情况都完整算完？
- heuristic 和 algorithm、optimization 有什么不同？
- heuristic 会在机器学习的哪些位置使用？
- 使用 heuristic 时，为什么还必须要有 validation？

## 本节目标

- 能把 heuristic 解释成在受限条件下用于缩小候选集的实用判断标准。
- 能理解 heuristic 并不保证最优解。
- 能用例子说明为什么在时间、数据、计算量和成本限制下，heuristic 会变得必要。
- 能说明为什么 heuristic 必须和 validation 一起使用。
- 能把 heuristic 看成可验证的 working hypothesis，而不是个人直觉。

## 先用一个场景来理解

假设你正在做一个新的客户流失预测模型。数据还不完美，时间也有限。

| 需要决定的东西 | 可能的选择 | 为什么很难全部都试一遍 |
| --- | --- | --- |
| 要使用的 feature | 访问次数、购买金额、登录间隔、咨询记录 | feature 组合会越来越多。 |
| 要使用的 model | logistic regression、decision tree、random forest、boosting | 每种 model 都需要训练和调参时间。 |
| 评估标准 | accuracy、precision、recall、F1 | 哪个更重要会随着业务目标而变化。 |
| 调参范围 | 树深、学习率、迭代次数 | 如果每种组合都试，成本会变得很高。 |

在这种情况下，`把所有可能组合都试到底，再挑出最好的` 这个想法在理论上听起来不错，但在现实里往往做不到。所以才需要 heuristic，例如先立一个简单 baseline、先去掉明显没必要的 feature、先选择符合业务目标的 metric。

## heuristic 是缩小候选集的方法

heuristic 会减少为了解决问题而必须先看的候选。它不是把所有路径都走完，而是先挑出值得优先检查的路径。

```mermaid
--8<-- "assets/part-04/chapter-03/heuristic-candidate-reduction-flow-zh.mmd"
```

在这张图里，heuristic 不是最终结论。它只是先决定要尝试哪些候选的方法。真正用数据验证之后，如果不合适，就必须调整它。

## 为什么不能把所有东西都算完

这时会出现一个问题：`计算机不是很快吗，为什么不能全都算？` 原因在于，选择空间会比想象中膨胀得更快。

例如，想一想从 20 个 feature 里挑出要不要用哪些 feature 这个问题。就算每个 feature 只有 `用` 和 `不用` 两种状态，可能的组合数也会非常大。如果再把 model 类型、hyperparameter、数据拆分方式叠加进去，实验次数会继续膨胀。

| 会膨胀的要素 | 为什么会变难 |
| --- | --- |
| feature 数量 | 组合数会快速增长。 |
| model 候选 | 每种 model 都要付出训练时间。 |
| hyperparameter | 设置组合会越来越多。 |
| 数据规模 | 一次训练的成本会变大。 |
| 评估条件 | 要同时查看多种 metric 和多种验证拆分。 |

所以在实务里，比起完全穷举所有可能性，更常见的做法是先缩小较可信的候选，再一边验证一边修正方向。

## heuristic 和 algorithm 的差别

algorithm 是按固定步骤解题的方法。heuristic 则是用来决定：在这些步骤内外，先看哪些候选、算到什么程度、优先做哪些选择。

| 区分 | 先联想到的话 | 例子 |
| --- | --- | --- |
| algorithm | 固定步骤 | 用给定数据训练 decision tree。 |
| heuristic | 缩小候选的判断标准 | 先试可解释的 model。 |
| optimization | 寻找能让目标函数更好的值 | 找到能减少 loss 的参数值。 |
| validation | 检查这个选择是否真的可接受 | 在 validation data 上确认性能。 |

heuristic 并不会替代 algorithm。相反，它是用来决定先试哪个 algorithm、先看哪一组设置、以及结果到什么程度就该进入下一阶段。

## 有限理性与足够好的选择

理解 heuristic 时，Herbert A. Simon 的 `bounded rationality` 视角很有帮助。Stanford Encyclopedia of Philosophy 把 bounded rationality 解释成：离开完全理性假设，转而研究在信息获取能力和计算能力都受限的主体身上，什么样的理性才是合适的。

这个视角同样很适合机器学习实务。我们并没有完整信息、无限计算时间，也没有完美评估环境。所以，比起 `理论上可能存在的最优解`，更重要的是 `在当前条件下可验证、足够好的选择`。

这并不意味着放弃准确性。相反，它意味着承认限制，并在这些限制之内以更合理的方式作出更好的选择。

## heuristic 在机器学习里会用到哪些地方

在机器学习里，heuristic 经常会用在下面这些位置。

| 位置 | heuristic 例子 | 后面会在哪里再处理 |
| --- | --- | --- |
| feature selection | 与其一开始塞进太多 feature，不如先看更容易解释的 feature。 | P4-7 |
| preprocessing | 先检查缺失值很多的列。 | P4-7 |
| model selection | 先建立一个简单 baseline model。 | P4-8 |
| tuning | 先试小范围，再考虑更宽的范围。 | P4-9 |
| evaluation | 先看业务上更危险的错误类型。 | P4-6 |

这张表里最重要的一点是：heuristic 不是 `最终答案`。它只是开始实验的方向。如果 validation 结果不好，就必须修改 heuristic。

## 好 heuristic 和坏 heuristic

heuristic 可能很有用，但它不总是对的。一个好的 heuristic，既要能快速缩小问题，又必须保留可验证性。

| heuristic | 为什么可以用 | 还必须验证什么 |
| --- | --- | --- |
| 先做一个简单 model。 | 可以很快建立比较标准。 | 要比较复杂 model 是否真的更好。 |
| 先怀疑缺失值很多的 feature。 | 可以更快发现数据质量问题。 | 仍然要确认这个 feature 会不会包含重要信号。 |
| 先使用可解释的 feature。 | 更容易和业务负责人一起讨论。 | 要确认性能没有被牺牲得太多。 |
| 先做计算成本更低的实验。 | 可以更快找到方向。 | 要确认小实验的结果是否也能延伸到更大数据上。 |

坏 heuristic 则是没有验证、只是反复沿用的习惯。比如 `永远先上 random forest`，或者 `有缺失值就整列丢掉`，都可能随着情境不同而变错。heuristic 必须和当前问题一起读。

## heuristic 是工作假设

这一节把 heuristic 当成 `working hypothesis` 来处理。也就是说，它是一个出发点，表示 `先这样做可能是合理的`。

只要把它当成 working hypothesis，就会出现下面这条流程。

1. 先说明为什么这个选择看起来合理。
2. 用小数据或 baseline model 先确认一下。
3. 看 validation 结果。
4. 如果不对，就修改。
5. 如果看起来还成立，再扩展到下一阶段。

这条流程的好处是：既不丢掉现场经验判断，又能把它转成一种可验证的形式。

实际工作里，首先要判断的是 `现在能不能用 heuristic`，以及 `哪些东西不能原样直接相信`。

| 当前状态 | 使用 heuristic 的方式 | 不能原样放着不管的东西 |
| --- | --- | --- |
| 候选太多，时间和计算成本都有限 | 把 heuristic 当成先缩小候选的出发点 | 把 heuristic 当成最终答案固定住 |
| 可以用 baseline 和小规模验证快速确认 | 把它写成工作假设，并立刻验证 | 没有验证就把它当习惯重复使用 |
| explainability、performance、cost 相互冲突 | 先写清楚优先哪个约束，再缩小候选 | 只看单一标准，忽略其他约束 |

## 案例与示例

### 案例 1. 想先找出退货可能性高的订单时

假设某个网店运营团队，想提前检查那些退货可能性高的订单。人一开始先看的标准，是 `是不是服饰类商品`、`折扣幅度是不是很大`、`同一个客户最近是不是经常退货` 这样的几个信号。

这些标准作为出发点很有用，但一旦订单数量很多，就很难由人直接把所有组合都比较一遍。而且不同团队可能会优先看不同标准，于是即便面对同样数据，优先级也会变得不稳定。

这时 heuristic 就可以变成这样一个工作假设：`先不要把所有 feature 全部放进去，而是先用那些最可能直接和退货相关的 feature 做一个小 baseline model。` 例如，可以先选最近退货次数、商品类别、订单金额、是否延迟配送，做一个小型分类实验。

这种判断到底对不对，仍然必须通过验证来确认。你可以比较 `只用这一小组 feature` 和 `用更大 feature 集` 时的性能差异，也要确认人工认为重要的标准是否真的在数据里形成了信号。如果结果差不多，说明这个简单起点是有效的；如果差很多，就要修改 heuristic。

```mermaid
--8<-- "assets/part-04/chapter-03/return-risk-heuristic-flow-zh.mmd"
```

## 本节要记住的视角

- heuristic 是在有限时间和有限信息里缩小候选的实用判断标准。
- heuristic 不保证最优解或最终答案。
- 在机器学习里，feature selection、preprocessing、model selection、tuning、评估标准选择都需要 heuristic。
- heuristic 不会取代 algorithm，而是用来决定先试哪些候选、按什么顺序去试。
- 好 heuristic 必须是可验证的。
- heuristic 应该被当成 working hypothesis，而不是个人感觉。

## 检查清单

- 能不能说明在什么状态下，heuristic 不是 `随便猜`，而是缩小候选集的装置？
- 能不能说明为什么 heuristic 总要和 baseline model 或 validation data 一起出现？
- 能不能说明当 explainability、cost、performance 冲突时，为什么必须把优先项记录下来？

## 什么时候要先想到这个视角

- 当你遇到 `无法把所有组合都算完，必须先缩小候选` 的问题时，就先想到 heuristic 视角。
- 当需要把 heuristic 从 `大概猜一下` 重新整理成 `可验证的 working hypothesis` 时，就回到这一节。
- 当 performance、explainability、cost 冲突，需要重新整理先保留什么、先记录什么时，这一节就是基准。

## 来源与参考资料

- Juliette R. V. Kenens, Matteo Colombo, and Stephan Hartmann, `Bounded Rationality`, Stanford Encyclopedia of Philosophy, substantive revision 2024-12-13, 确认日期：2026-06-25. [https://plato.stanford.edu/entries/bounded-rationality/](https://plato.stanford.edu/entries/bounded-rationality/){: target="_blank" rel="noopener noreferrer" }
- Stuart Russell and Peter Norvig, `Artificial Intelligence: A Modern Approach`, 第 4 版，Pearson，2020，确认日期：2026-06-25. [https://aima.cs.berkeley.edu/](https://aima.cs.berkeley.edu/){: target="_blank" rel="noopener noreferrer" }
- Judea Pearl, `Heuristics: Intelligent Search Strategies for Computer Problem Solving`, Addison-Wesley, 1984.
