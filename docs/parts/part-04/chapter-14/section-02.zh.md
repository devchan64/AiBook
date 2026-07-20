# P4-14.2 树的过拟合

> Section ID: `P4-14.2`
> Version: `v2026.07.20`

P4-14.1 把决策树(decision tree)读成了 `通过拆分问题来做预测的模型`。 那一节的优点很明确。

- 作为问题流很容易阅读
- 像条件语句一样容易解释
- 在表格型数据(tabular data)上常常很直观

但同样的性质也会直接变成风险。 如果模型能够一直继续加问题，树就可能几乎把训练数据记住。 这正是树的过拟合(overfitting)问题。

如果说 P4-14.1 讨论的是 `应该怎样阅读好的第一问题和下一问题`，那么这一节讨论的就是： `那条问题流从什么地方开始不再解释模式，而开始记忆例外？` 因此这里不仅要看“把树加深”什么时候有帮助，也要一起看它什么时候开始让结构变得不稳定。

这一节不会再长篇重复决策树的基本定义。 `通过问题拆分来预测` 这个核心直觉，会通过 P4-14.1 和[概念词典](/AiBook/en/reference/concept-glossary/)重新连接； 而过拟合本身的一般抓手，则应该和 P4-5.1 一起再次想起。

## 本节范围

本节回答以下问题。

- 为什么在决策树里，过拟合特别容易看出来？
- 随着树变深，会发生什么？
- `max_depth`、`min_samples_leaf`、`ccp_alpha` 各自起什么作用？
- 为什么 train 表现和 test 表现可能朝不同方向变化？

这些内容会在 P4-15、P4-16，以及 P4-9 的调参语境中再次连接。也就是说，这一节先抓住的是：树的问题流从哪里开始不再解释模式，而是在记忆例外。

## 用树的过拟合留下的判断标准

- 你可以把树的过拟合解释成 `过于细碎的问题开始记忆训练数据` 这一现象。
- 你可以说明深度(depth)、leaf 大小、pruning 是控制树复杂度的装置。
- 你可以再次确认更高的 train 表现并不保证更高的 test 表现。
- 你可以形成一个同时阅读树的优点与过拟合风险的标准。

## 学习背景

### 为什么树的过拟合特别容易看见

决策树本质上是一个 `不断重复 split，把 node 切成更小部分的结构`。 这种结构很强。 但如果没有限制，它就能长出更小、再更小的 leaf。

scikit-learn 用户指南说明，决策树学习器可能会长出 `over-complex trees`，而这样的树往往泛化(generalize)得不好。 同一文档把这叫作 overfitting，并说明为什么需要 pruning、`min_samples_leaf`、`max_depth` 等控制装置。

`树会随着问题不断增加，开始把训练数据里的例外也跟得很紧。但这些例外并没有保证会在新数据里重复出现。`

这里也最好把记录结构一起固定下来。 这一节不是只说一句 `树变深会危险`。 它还应该记录： `复杂度增加时新出现了什么失败`、 `哪些 review 案例仍然留下来了`、 `在哪个位置应该停止或削减分支`。 即使两个模型的平均分数差不多，更深的树也可能记住了新的案例组合，但原来的失败却还在。 这种差异必须单独去读。

| 建议一起留下的记录 | 为什么需要 |
| --- | --- |
| depth 或 leaf 大小的变化 | 为了看复杂度控制到底怎么动了 |
| train/test 差异 | 为了区分记忆与泛化 |
| 一直残留的失败案例 | 为了重新检查“分支变多了也没解决”的案例 |
| 下一步剪枝问题 | 为了决定接下来优先调 `max_depth`、`min_samples_leaf` 还是 `ccp_alpha` |

### 什么时候应该尽早怀疑树过拟合

想更快抓到过拟合，就不能只盯着分数。 还要一起问： `这些问题是不是已经细到过头了？`

| 看得见的信号 | 先怀疑什么 | 原因 |
| --- | --- | --- |
| train 几乎完美，但 test 掉下去 | 深度过大 | 树可能已经开始记忆训练数据 |
| 一个 leaf 里几乎没有样本 | leaf 太小 | 模型可能把例外当成了稳定模式 |
| 分支变多了，但同样的失败案例还在 | 错误方向的复杂度增加 | 只是问题数变多了，核心问题没有解决 |
| 第一处分裂之后，后面分支特别多 | 后段过细分裂 | 后面的枝条可能在追随机波动 |
| 说明更长了，但反而更难解释 | 需要 pruning | 原本“容易阅读”的优点正在消失 |

这个表能让读者不只停留在 `树变深有风险` 这个模糊结论。 它把真正的问题改写成： `从什么地方开始，这些问题不再描述模式，而开始描述例外？`

## 主要学习内容

### 用小树和大树比较的直觉

再想一遍客户流失数据。

| 树的状态 | 直觉 |
| --- | --- |
| 浅树 | 只看到大的趋势 |
| 深度适中的树 | 在主要模式和有意义的例外之间取得平衡 |
| 过深的树 | 跟着训练数据里的偶然波动走 |

同样的意思可以压缩成下面这张图。

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-01-zh.mmd"
```

这个图说明，树的过拟合不是 `问题越多越好`。 更多 split 确实可能让模型在训练数据上更贴合。 但在最后几个阶段，开始出现的可能不是泛化，而是记忆。

最关键的是最后一根箭头。

`更贴合` 和 `更能泛化` 不是同一句话。

如果改写成项目记录语言，可以写成这样。

| 记录项 | 例子 |
| --- | --- |
| 复杂度变化 | `max_depth 3 -> 5` |
| train 变化 | `0.971 -> 1.000` |
| test 变化 | `0.933 -> 0.911` |
| 是否需要 review | `深度增加了，但失败案例还在` |
| 下一步问题 | `应该扩大 leaf，还是做 pruning？` |

这个表让过拟合这一节被读成 `复杂度变化 -> 残留失败 -> 下一步剪枝问题` 的结构。 重要的不是某一个数字格子本身。 而是失败模式有没有变得更简单，还是只是更贴合训练数据。

### 树越深，会发生什么

树越深，每个 leaf 里剩下的样本就越少。 这样会发生几件事。

1. 一两个例外案例就可能新开出一条分支。
2. 某个 leaf 可能只看很少的样本就给出预测。
3. 在训练集上，模型可能几乎不再犯错。
4. 在测试集上，预测却会因为很小的变化而更容易摇动。

scikit-learn 文档提到，树每多一层，大致都需要更多样本去支撑，并建议用 `max_depth` 控制大小。 它也建议用 `min_samples_split` 和 `min_samples_leaf`，让决策不要只建立在极少样本之上。

把这段话压成一句：

`树越深，细节确实越多；但如果没有足够数据支撑这些细节，树不一定更聪明，反而可能更敏感。`

### 把过拟合读成数据流

如果把过拟合理解成一种流动过程，而不是只理解成公式，它会记得更久。

前面的分支常常能抓住比较大的模式。 问题通常从后面开始出现。 最后几层可能已经不再解释 `真实结构`，而是在解释 `只出现在训练数据里的偶然波动`。

把这个流程分成几个阶段，可以这样读。

| 流程阶段 | 树主要在做什么 | 先问什么 |
| --- | --- | --- |
| 前段分支 | 划开大的模式 | 它抓住的真的是重要差异吗？ |
| 中段分支 | 添加例外和子模式 | 它看到的还是会重复出现的结构吗？ |
| 后段分支 | 开始单独分出很小的案例组 | 现在是不是已经在记随机波动？ |
| 最后 leaf | 几乎成了训练集专用规则 | 这个 leaf 到了新数据里还会活下来吗？ |

比如前面的分支可能使用 `温度高且振动大吗？`、`访问下降和投诉信号是否同时出现？` 这样的大标准。 到了后面，就可能变成 `是不是只有第三个时间点波动过？`、`是不是只在某一周访问下降了两次？` 这样非常细的提问。

所以真正的问题，不是简单地说 `问题变多了`。 而是： `这些问题的性质，是否已经从解释大模式变成了解释训练数据里的例外？`

### 为什么必须把 train 和 test 一起看

当 train 表现和 test 表现一起看时，树的过拟合尤其容易暴露出来。

| 观察 | 解释 |
| --- | --- |
| train 和 test 都低 | 模型可能还太简单，没有学到足够的内容 |
| train 和 test 一起高 | 当前平衡看上去还不错 |
| 只有 train 很高，而 test 掉下去 | 应该怀疑过拟合 |

这个视角在决策树里经常出现，但其实它是 Part 4 的共同原则。 线性回归、逻辑回归、SVM、树模型，最终都要面对同一个问题： `在没见过的数据上，它到底撑得住吗？`

## 细化学习内容

### 为什么需要 `min_samples_leaf`

如果 `max_depth` 控制的是整棵树的高度，那么 `min_samples_leaf` 控制的就是“一个 leaf 允许缩小到什么程度”。

API 把 `min_samples_leaf` 解释为： 进入某个 leaf node 所需要的最少样本数。 它也提到，在回归(regression)里，这个值还可能带来一种 smoothing 效果。

`如果一个 leaf 只允许装下一两个案例，它更像是在说例外，而不是在说模式。`

例如：

- `min_samples_leaf=1`：哪怕 leaf 里只剩一个案例也允许
- `min_samples_leaf=5`：至少要有五个案例，才能被当成 leaf

这个差异也可以被重读成： `我们愿意相信多小的一组例外？`

### Python 示例：观察 leaf 大小控制

这次不固定深度，而是只改变 leaf 大小。

问题场景：

- 在同一份数据上，如果改变 leaf 允许多小，train 与 test 的阅读方式就可能变化

输入(input)：

- iris 数据集中的 `X_train`、`X_test`、`y_train`、`y_test`
- 多个 `leaf_size`

期望输出(output)：

- 不同 leaf 大小下的 train score
- 不同 leaf 大小下的 test score

要确认的概念：

- leaf 太小时，train 分数往往更容易升高
- 把 leaf 放大，结构可能会变得没那么敏感

```python
# 这个例子改变 min_samples_leaf，观察小 leaf 限制如何影响 train/test 分数和树结构。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for leaf_size in [1, 2, 5, 10]:
    model = DecisionTreeClassifier(
        min_samples_leaf=leaf_size,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(model.score(X_train, y_train), 3))
    print("  test accuracy  :", round(model.score(X_test, y_test), 3))
    print()
```

示例输出如下。

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933

min_samples_leaf=10
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
```

这个例子给出一个重要感觉。

`阻止 leaf 变得太小，并不一定会让性能变差。相反，test 侧有时会更稳定。`

### pruning 在做什么

如果说事先限制深度可以读成 pre-pruning，那么树长出来之后再把它变简单，就可以读成 pruning。

scikit-learn 支持 `Minimal Cost-Complexity Pruning`。 API 把 `ccp_alpha` 解释为这种 pruning 的复杂度参数。 值越大，越容易剪掉更多节点。

- `max_depth`、`min_samples_leaf`：从一开始就阻止树变得过于复杂
- `ccp_alpha`：树长出来后，再对复杂度施加代价，把结构缩回去

这两类方法的目标是一样的。

`与其把训练数据记住，不如留下在新数据上也站得住的结构。`

初学者最先要抓住的差异，是 `它们在什么时候介入`。

| 方法 | 什么时候介入 | 先读出的意思 |
| --- | --- | --- |
| `max_depth`、`min_samples_leaf` | 树生长过程中 | 从一开始就阻止过细分支 |
| pruning、`ccp_alpha` | 树已经长出来之后 | 把效果弱的小枝条再削掉 |

也就是说，pre-pruning 是 `防止树一开始就长得太深的手柄`； pruning 是 `树长出来一次之后，再重新挑选哪些枝条应该留下的手柄`。

看一个小场景会更清楚。

| 分支状态 | pruning 前 | pruning 后 |
| --- | --- | --- |
| 前面的大分支 | 保留 | 大体仍保留 |
| 只解释少数例外的 leaf | 可能还在 | 可能被剪掉 |
| train 分数 | 看起来更高 | 可能略降 |
| test 稳定性 | 可能摇动 | 可能更稳定 |

这个表的重点在于： pruning 不应该被读成 `把树弄坏了`。 它应该被读成 `保留大结构，把剩余的小问题去掉`。

假设某个后段分支又加了一条极窄的条件： `温度高`、`振动大`，而且 `只有第三个时间点的压力落在一个窄范围里`。 如果这个 leaf 只解释了训练数据里的两个产品，那么 pruning 就是在问： `这条小枝条真的值得留下吗？`

这也是为什么 `ccp_alpha` 不只是又多了一个数字选项。 它其实在重新追问： `这条小分支提升 train 分数的收益，真的大于它增加复杂度的代价吗？`

如果只先记方向，可以这样记。

- `ccp_alpha` 很小时，更容易留下更多分支
- `ccp_alpha` 变大后，更容易把小分支剪掉
- 太小容易偏向记忆
- 太大又可能把重要模式一起剪掉

### 把 pruning 读成一个流程

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-02-zh.mmd"
```

这一节不去计算 pruning 公式。 而是把重点放在： `哪些残枝不该留下` 以及 `为什么人们愿意牺牲一点 train 分数来换取更稳定的 test 表现` 上。

## 案例与示例

### 案例 1. 当不良检测树开始记住工厂数据里的例外

制造团队正在用传感器值建立一个决策树，用来区分产品是否不良。 人先看的标准包括： `温度是否高于阈值？` `振动是否超出范围？` `压力变化是否突然？`

问题加得越多，模型看起来越像“更聪明”。 实际上，树变深之后，训练数据上确实可能几乎不再犯错。 但如果去看后面的分支，就会出现只解释一两个例外产品的 leaf。 这些 leaf 一旦工艺稍微变化，就会在新数据上很容易摇动。

换成一个小场景，可以这样看。

| 产品 | 温度 | 振动 | 压力变化 | 人先看的判断 |
| --- | --- | --- | --- | --- |
| A | 高 | 大 | 剧烈 | 不良 review 优先级高 |
| B | 普通 | 小 | 稳定 | 更可能正常 |
| C | 高 | 中 | 略大 | review 候选 |
| D | 略高 | 短暂偏大 | 稳定 | 难以立刻判为不良 |

这里人先看的模式是 `温度升高 + 振动/压力异常` 这种相对大的模式。 但过深的树会继续加上 `只有第三次测量时振动短暂升高了吗？` 或者 `压力曲线是否在某个窄区间内弯折了两次？` 这样的细问题。 于是模型开始去解释训练数据里那些偶然和 D 相似的少数产品。

| 人先看的标准 | 过深的树容易抓住的东西 |
| --- | --- |
| 温度和振动异常是否同时出现 | 某个时间点的短暂波动 |
| 压力变化是否像工艺异常 | 训练数据里的稀有传感器组合 |
| 是否应该先列为 review 对象 | 只适合一两个产品的细碎分支 |

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-03-zh.mmd"
```

如果把同一场景分成 `相对简单的阅读` 和 `过深的阅读`，差异会更清楚。

| 阅读方式 | 怎样看产品 D |
| --- | --- |
| 相对简单的树 | 温度略高，但压力稳定，因此先保留为 review 候选 |
| 过深的树 | 通过短暂振动波动和稀有传感器组合，把它单独分到一个 leaf |

在这个场景里，过拟合应该被读成： `模型把问题细化得太多，以至于开始记住训练数据。` `max_depth` 限制树最多长多深。 `min_samples_leaf` 阻止 leaf 变成很小的例外集合。 `ccp_alpha` 再把已经长出来的枝条缩回去。 总之，问题更多并不总是更好的解释。

真正可验证的结果，要通过一起看 train accuracy 和 test accuracy 才能暴露出来。 如果 train 分数一直升高，但 test 分数停住甚至下降，那么后面的分支就更像是在记忆，而不是在泛化。 真正重要的问题不是 `它是不是把传感器异常描述得更细了？` 而是 `它有没有形成一个在新工厂数据上也会重复的标准？`

### 案例 2. 当客户流失树开始记住例外客户，而不是 review 规则

再想象一个订阅服务团队正在构建客户流失决策树。 人先看的标准是比较大的模式： `访问是否明显下降？` `有没有支付失败？` `客服接触之后是否出现了不满信号？`

但如果树继续加深，后面的分支就可能不断堆上这样的组合： `最近 17 天里是否只有 2 次访问？` `上个月支付金额是否刚好落在某个窄区间？` `促销邮件是否只打开过一次？` 这些组合在训练数据里可能很贴合一小群客户，但在真实运营里不一定会重复，也不一定有稳定意义。

换成一个小场景，可以这样看。

| 客户 | 最近访问变化 | 支付失败 | 不满信号 | 人先看的判断 |
| --- | --- | --- | --- | --- |
| A | 大幅下降 | 有 | 有 | review 优先级高 |
| B | 略有下降 | 无 | 无 | 很难立刻判为流失 |
| C | 大幅下降 | 无 | 有 | review 候选 |
| D | 几乎无变化 | 无 | 无 | 更可能留存 |

人先看的模式仍然是 `访问下降 + 支付/不满信号` 这种大模式。 但过深的树可能会改成 `第二周是否一次访问都没有？` 或 `活动邮件是否在周三上午打开？` 这种很细的问题。 然后模型开始为训练数据里少数和 C 相似的客户专门造出分支。

| 人先看的标准 | 过深的树容易抓住的东西 |
| --- | --- |
| 访问下降是否明显 | 某一周里的小波动 |
| 支付问题和不满信号是否同时出现 | 训练数据里的少数客户组合 |
| 是否应该优先列为 review 对象 | 只把某一个 leaf 拟合得很细的分支 |

如果把同一场景分成 `浅层阅读` 和 `过深阅读`，差异会更清楚。

| 阅读方式 | 怎样看客户 C |
| --- | --- |
| 相对简单的树 | 因为访问下降并伴随不满信号，所以把 C 列为 review 候选 |
| 过深的树 | 再叠加特定周次模式、金额区间和邮件反应，把它单独分到一个 leaf |

在这个场景里，过拟合应该被读成一种状态： `看起来解释力很强的细问题，其实没有让 review 标准更清楚，而是在记住训练数据里的偶然组合。` 所以读一棵树时，不仅要问 `说明是不是变详细了？` 还要问 `这种细节会不会在新客户身上重复出现？`、`它有没有真正改善实务中的 review 优先顺序？`

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-2-mermaid-04-zh.mmd"
```

如果不用分数表，而是用 leaf 场景重新阅读，同样的情况会更容易诊断。

| 观察 leaf 时先看什么 | 会被读成过拟合信号的场景 |
| --- | --- |
| leaf 内样本数 | 许多 leaf 只剩一两条案例 |
| 形成这个 leaf 的问题性质 | 大模式减少，按周次、时点、细碎组合的问题增加 |
| leaf 的实务意义 | 它更像训练案例备忘，而不是稳定的 review 规则 |

抓住这个表之后，就不容易因为 `train accuracy 变高了` 就直接夸这棵树。 对初学者来说，特别重要的是至少再问一句： `这个 leaf 在解释新客户，还是只是在单独记住少数训练客户？`

### 实务里要先看哪些手柄

刚开始时，与其一次把所有值都调动，不如先按角色分开看。

| 手柄 | 先读什么问题 |
| --- | --- |
| `max_depth` | 树最多应该允许长到多深？ |
| `min_samples_split` | 这个 node 里有没有足够样本继续分裂？ |
| `min_samples_leaf` | 是否要阻止某个 leaf 变得太小？ |
| `ccp_alpha` | 已经长出来的枝条要缩掉多少？ |

换成实务语言，就是下面这样。

- 说明太长、太复杂了 -> 先看 `max_depth`
- 只解释少数案例的 leaf 看起来太多 -> 先看 `min_samples_leaf`
- 分支太多、残枝太多 -> 考虑 `ccp_alpha`

## 练习与示例

### Python 示例：通过深度观察过拟合

这个练习在同一个决策树分类器上，只改变深度，观察 train/test 结果如何分开。

- 问题场景：用 iris 数据集分类品种
- 输入(input)：萼片和花瓣的长度、宽度
- 标签(label)：三种品种
- 要确认的概念：
- 深度变大时，train 表现通常更容易上升 - test 表现到了某一点之后可能停住甚至下降 - 树的深度是最重要的复杂度手柄之一

最好先明确要比较什么。

| 要比较的值 | 为什么要一起看 |
| --- | --- |
| `max_depth` | 为了看树被允许长到多深 |
| `leaves` | 为了看这种深度实际创造了多少终端节点 |
| train accuracy | 为了看训练数据上的拟合程度 |
| test accuracy | 为了看新数据上的泛化程度 |
| `train - test` gap | 为了看记忆与泛化究竟拉开了多大差距 |

```python
# 这个例子改变 max_depth，把树深度和 train-test gap 作为过拟合信号来阅读。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for depth in [1, 2, 3, 5, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"max_depth={depth}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

示例输出如下。

```text
max_depth=1
  depth          : 1
  leaves         : 2
  train accuracy : 0.667
  test accuracy  : 0.667
  train-test gap : 0.0

max_depth=2
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063

max_depth=3
  depth          : 3
  leaves         : 5
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

max_depth=5
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

max_depth=None
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089
```

从这个结果里要读出的重点如下。

1. 深度增加时，train accuracy 很容易继续上升。
2. test accuracy 在某一点之后可能不再继续提升。
3. `train-test gap` 越大，记忆信号可能越强。
4. 在当前示例里，`max_depth=3` 附近看起来更平衡。

所以阅读树的性能时，真正的问题不是只问一句 `它是不是更深了？` 而是要问 `它变深以后，train 和 test 是怎么分开的？`

另外，还要避免只盯着准确率数字。 `max_depth=5` 和 `max_depth=3` 的差异，不只是分数差异。 它还是结构差异： 更深的树会生成更多 leaf，并开始用更细的方式去解释训练数据。

### 再改一个值，同时阅读 `depth` 和 `leaf`

这次看看，当 leaf 大小和 depth 一起读时，判断会怎么变化。

- 要改的值：`min_samples_leaf`
- 改动原因：想看在相同 depth 限制下，阻止小 leaf 是否真的会减少例外记忆
- 要确认的概念：
- `max_depth` 和 `min_samples_leaf` 在不同位置控制同一个复杂度问题 - 即使 depth 看起来接近，更大的 leaf 也会改变 train/test 的解释 - 诊断过拟合时，最好把 `depth + leaf 大小 + gap` 放在一起读

```python
# 这个例子在相同深度限制下再改变 min_samples_leaf，一起阅读 leaf 大小和 gap。
for leaf_size in [1, 2, 5]:
    model = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=leaf_size,
        random_state=42,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"min_samples_leaf={leaf_size}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

示例输出如下。

```text
min_samples_leaf=1
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

min_samples_leaf=2
  depth          : 4
  leaves         : 7
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

min_samples_leaf=5
  depth          : 3
  leaves         : 4
  train accuracy : 0.971
  test accuracy  : 0.933
  train-test gap : 0.038
```

这个比较里首先该看的，是下面这一点： `即使 train accuracy 稍微下降，test accuracy 也可能变得更稳定。` 所以缓解过拟合，不应该被读成“牺牲分数的失败”。 它更接近于一种调整： `少记一点，但更能撑住。`

可以直接把下面三句话写下来。

1. `max_depth=5, min_samples_leaf=1` 在什么意义上是最敏感的结构？
2. 换成 `min_samples_leaf=2` 或 `5` 后，什么地方变得没那么敏感了？
3. 如果下一步再加 pruning，哪些残枝看起来会先被剪掉？

### 改动 `ccp_alpha`，读出 pruning 的方向

现在再让这棵树摇一次，这次改变“已经长出来的树要缩回多少”。

- 要改的值：`ccp_alpha`
- 改动原因：depth 与 leaf 大小调节是在一开始阻止生长，而 pruning 是在树已经长出来之后再简化
- 要确认的概念：
- `ccp_alpha` 越大，小分支越容易被剪掉 - train 分数可能略降，但 test 侧可能更稳定 - pruning 更接近 `重新选择应该留下的大结构`，而不是 `把树弄坏`

```python
# 这个例子改变 ccp_alpha，观察 pruning 如何改变深度、leaf 数量和 train/test gap。
for alpha in [0.0, 0.005, 0.02]:
    model = DecisionTreeClassifier(
        random_state=42,
        ccp_alpha=alpha,
    )
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"ccp_alpha={alpha}")
    print("  depth          :", model.get_depth())
    print("  leaves         :", model.get_n_leaves())
    print("  train accuracy :", round(train_score, 3))
    print("  test accuracy  :", round(test_score, 3))
    print("  train-test gap :", round(train_score - test_score, 3))
    print()
```

示例输出如下。

```text
ccp_alpha=0.0
  depth          : 5
  leaves         : 8
  train accuracy : 1.0
  test accuracy  : 0.911
  train-test gap : 0.089

ccp_alpha=0.005
  depth          : 4
  leaves         : 6
  train accuracy : 0.981
  test accuracy  : 0.933
  train-test gap : 0.048

ccp_alpha=0.02
  depth          : 2
  leaves         : 3
  train accuracy : 0.952
  test accuracy  : 0.889
  train-test gap : 0.063
```

这个结果里最先要读的一点是： `稍微剪一点更好了，但剪得太多又会错误地变得过于简单。` 所以 pruning 也不是 `越多越好`。 它是在寻找平衡： 去掉残枝，但保住大的模式。

如果可以，也请把下面几句写下来。

1. `ccp_alpha=0.005` 看起来像是削掉了哪种小分支？
2. 为什么 `ccp_alpha=0.02` 看起来像一个过度简化的候选？
3. 在 `max_depth`、`min_samples_leaf`、`ccp_alpha` 里面，你会先调哪个手柄？

### 练习：把复杂度手柄写成记录语言

如果已经跑了上面的实验，就不要停在“看结果”。 请留下一个简短的比较记录。

| 比较项 | 只改 depth 的实验 | 连 leaf 大小一起改的实验 |
| --- | --- | --- |
| 看起来最平衡的设置 |  |  |
| 看起来最敏感的设置 |  |  |
| train-test gap 最大的设置 |  |  |
| 下一步想调的手柄 |  |  |

填写这个表时，不要只写 `分数最高的设置`。 最好也一起写一句： 为什么你觉得那个设置更平衡。

如果可以，再为 pruning 实验多加一行。

| pruning 比较项 | 记录 |
| --- | --- |
| 看起来最平衡的 `ccp_alpha` |  |
| 感觉剪得过头的 `ccp_alpha` |  |
| 下一步要一起比较的手柄 |  |

例如，可以写成下面这样。

- `max_depth=3` 适合作为基准，因为 train 和 test 一起改善。
- `max_depth=5, min_samples_leaf=1` 在 train 上完美，但 gap 更大，因此更像在记忆例外。
- 下一步想看的是：用 `ccp_alpha` 剪掉残枝之后，同样的失败是否还会留下来。

## 检查清单

- 你有没有把 train 表现上升，直接读成 test 表现也会上升？
- leaf 是否已经小到开始像“例外规则”而不是“稳定模式”？
- 你是否清楚地区分了下一步该调的是深度限制、leaf 大小，还是 pruning？
- 能不能说明树虽然容易阅读，但如果没有限制就容易过度跟随训练数据，而且 depth 越大、leaf 越小，过拟合风险就越高？
- 能不能说明 train 表现变高，并不保证 test 表现也会一起变好？
- 能不能说明 `max_depth`、`min_samples_leaf`、`ccp_alpha` 分别以什么方式控制树的复杂度？

## 出处与参考资料

- scikit-learn developers, `1.10. Decision Trees`, scikit-learn User Guide, 确认日期: 2026-06-27. [https://scikit-learn.org/stable/modules/tree.html](https://scikit-learn.org/stable/modules/tree.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DecisionTreeClassifier`, scikit-learn API Reference, 确认日期: 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984, 确认日期: 2026-07-19. [https://doi.org/10.1201/9781315139470](https://doi.org/10.1201/9781315139470){: target="_blank" rel="noopener noreferrer" }
