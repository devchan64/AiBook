# P4-14.1 决策树(decision tree)

> Section ID: `P4-14.1`
> Version: `v2026.07.11`

P4-11 通过画边界(boundary)来理解分类。
P4-12 通过最近邻来理解分类。
P4-13 又把 margin 当作更好边界的标准来阅读同一个问题。
现在，我们要用完全不同的方式重新阅读同一个监督学习(supervised learning)问题。

如果说 P4-13.2 抓住了 `同一份数据可以放到不同的表征空间(feature space)里重新看` 这一点，那么这一节要做的事是把同样的表格型数据换成另一个问题来整理：
`应该按什么提问顺序把它分开来读？`
改变的不是问题本身。
改变的是概括同一个问题的单位。

与其一次画出一条直线，不如想象把案例按问题一步一步拆开。
这样更容易看清决策树(decision tree)的出发点。
决策树不会试图一次把数据全部解释完。
它会重复 yes/no 问题，把更相似的案例逐渐分到一起，再给出预测。
所以决策树更接近 `问题流(question flow)`，而不是 `单一边界线`。

这一节解释 `决策树(decision tree)`、`分裂(split)`、`节点(node)`、`叶(leaf)` 的基本含义。
后续小节会以这些抓手继续推进当前语境中的判断，而 `把问题串起来再给出预测` 的基础直觉，也会通过这一节和[概念词典](/AiBook/en/reference/concept-glossary/)重新连接起来。

## 本节范围

本节回答以下问题。

- 决策树是怎样做预测的？
- `split`、`node`、`leaf` 分别是什么？
- 为什么树常被认为是相对容易阅读的模型？
- 训练时会比较哪些问题候选？
- 为什么它既能做分类(classification)，也能做回归(regression)？

本节不深入展开以下内容。

- 树加深时出现的过拟合(overfitting)
- 剪枝(pruning)的细节步骤
- 随机森林(random forest)与梯度提升(gradient boosting)
- 熵(entropy)、信息增益(information gain)的公式推导

这些内容会在 P4-14.2、P4-15、P4-16 继续展开。

## 本节目标

- 你可以把决策树解释成 `通过拆分问题来做预测的模型`。
- 你可以说明 split、node、leaf、threshold 的含义。
- 你可以理解决策树既能用于分类也能用于回归。
- 你可以解释训练过程其实是 `不断挑选看起来更好的问题`。
- 你可以区分 `易读性` 与 `过度加深的风险`。

## 学习背景

前面章节里见过的代表模型，大体会留下这样的印象。

- 线性回归(linear regression)：用直线或平面读关系
- 逻辑回归(logistic regression)：读分类边界和类似概率的输出
- k-NN：读附近的邻居
- SVM：读留出余量的边界

决策树在这里把问题本身换掉了。

| 前一节的视角 | 决策树改写后的问题 |
| --- | --- |
| 能不能把一条边界画好？ | 用什么问题把数据分开比较好？ |
| 距离和 margin 重要吗？ | 现在分裂一次，label 会不会更整齐？ |
| 用公式表达整体趋势吗？ | 能不能像条件语句一样把案例分开？ |

也就是说，决策树把视角从 `在空间里画线的模型` 改成了 `把问题串起来的模型`。
这个视角也会直接连接到后面理解随机森林和 boosting。

这一节还会直接接回 Part 4 一直在整理的比较记录结构。
当我们把树当成候选模型时，不能只留下 `第一处分裂是什么`。
还要一起记下 `哪些案例留在这个分裂附近`、`比 baseline 或其他候选更容易读懂的地方是什么`、`下一步还要再检查什么分裂问题`。
即使分数看起来差不多，有的树在某个 leaf 里仍可能混入更多其他类别。
所以分裂之后留下来的模式差异，也要单独去读。

| 建议一起留下的记录 | 为什么需要 |
| --- | --- |
| baseline 与决策树比较 | 为了看规则型问题流究竟多解释了什么 |
| 第一处分裂附近的案例 | 为了重看哪些案例在问题边界附近仍然模糊 |
| 每个 leaf 里聚集的代表案例 | 为了确认分裂结果到底形成了什么分组 |
| 下一步问题 | 为了决定要不要继续加深，或改用别的特征分裂 |

### 什么时候适合优先把决策树列为候选

当 `问题流本身` 就是解释的一部分时，决策树往往是很强的第一候选。

| 当前问题状态 | 先考虑决策树的理由 | 先检查什么 |
| --- | --- | --- |
| 条件语句式说明很重要 | 分支流程更接近人类语言中的规则 | 第一处分裂是否偏离领域常识太多 |
| 表格型(tabular)特征是主体 | 数值和类别特征都容易转成阈值问题 | 哪些特征在主导分裂 |
| 比起线性边界或距离标准，问题顺序更自然 | 分步区分可能比一次划开整个空间更有解释力 | 每个 leaf 里是否仍然混得太多 |
| 想用同一套结构比较分类与回归 | 只改 leaf 输出，就能重用相似结构 | 评价指标是否对应问题类型 |
| 之后可能扩展到随机森林或 boosting | 可以先建立整个树模型家族的起点结构 | 是否已经理解 depth 与 leaf 大小控制 |

这个表的重点，不是把决策树停留在 `容易阅读的模型`。
而是把它放到 `当问题顺序本身成为真实解释单位时，值得优先尝试的候选` 这个位置上。

## 主要学习内容

### 决策树是什么样的模型

scikit-learn 用户指南把决策树介绍为用于分类和回归的非参数(non-parametric)监督学习方法。
同一份文档还把它的目标解释为：
`学习由数据特征(feature)推导出的简单决策规则(simple decision rules)，从而预测目标值(target value)`。
它还补充说，这种结构也可以被看成 piecewise constant approximation。

把这段话换成更容易读的版本，可以写成下面这样。

`决策树查看输入特征，连续提出“是否大于某个阈值”之类的问题，把输入空间分成若干块，并在每一块上放一个代表性的预测值。`

可以把它想成订阅服务中的客户流失(churn)预测。

| 特征(feature) | 问题示例 |
| --- | --- |
| 最近 30 天访问次数 | 访问次数是否不超过 3 次？ |
| 是否有延迟支付 | 最近是否发生过延迟支付？ |
| 客服咨询次数 | 咨询是否达到 2 次以上？ |

决策树会先从这些问题中挑一个。
然后根据答案把数据分成不同分支。
接着在每个分支里继续问下一个问题。

### 先把它读成一个小流程

先不要急着把决策树当成“学习器”。
先把它读成 `沿着问题往下走的决策流程`。

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-01-zh.mmd"
```

这个图会帮助读者把决策树理解成 `沿着问题走到某个 leaf 的流程`。
与一次画出一条边界线的模型不同，树会经过中间问题，一步一步把案例收窄到更相似的组里。

这个图里最重要的点如下。

- 中间的问题框是 `node`
- 根据答案分开的地方是 `split`
- 不再继续提问、直接输出预测的终点是 `leaf`

所以，决策树可以被读成 `沿着问题 node 一直走到 leaf 的结构`。

如果把它压缩成项目记录语言，大概可以写成下面这样。

| 记录项 | 例子 |
| --- | --- |
| first split | `visits <= 3` |
| near-split cases | `customer C`, `customer D` |
| 当前 leaf 预测 | `churn` 或 `stay` |
| 是否需要 review | `接近分裂边界的客户需要再看一次` |
| 下一步问题 | `late_payment` 要不要放到下一处分裂？ |

有了这个表，决策树的入门就会被读成 `候选比较 -> 分裂附近案例 -> 下一步问题` 的结构。
这时要把 near-split cases 和 leaf 组成一起看。
只有这样，才能区分“更容易读的树”和“看上去精度相近但更脆弱的树”。

### node、split、leaf 应该怎么理解

这一节最重要的是把术语切得短而清楚。

| 术语 | 简单解释 | 本节里的作用 |
| --- | --- | --- |
| node | 放置问题的位置 | 在这里摆放划分数据的标准 |
| split | 根据问题结果发生的分支 | 试图把数据分成更相似的组 |
| leaf | 写着最终预测的终点 | 输出类别或数值 |
| threshold | 切分数值的标准值 | 生成 `x <= 3.5` 这样的提问 |

这些术语也会马上连到后面的超参数讨论。

- `max_depth` 关系到树最多允许长多深。
- `min_samples_split` 关系到一个 node 是否有足够样本继续分裂。

不过在这一节里，重点还不是 `应该允许它长到多深`。
重点仍然是 `通过提问来拆分的模型，本身是一种什么结构`。

## 细化学习内容

### 为什么说它是相对容易阅读的模型

在 Part 4 初次遇到的模型里，决策树属于相对 `能像规则一样去读` 的一类。
scikit-learn 用户指南把这一点放在 `white box model` 的视角下解释。
如果模型内部出现了某种情况，人往往可以用比较直接的布尔逻辑(boolean logic)把条件说出来。
和线性模型的权重(weight)、SVM 的 margin 相比，`顺着问题走下去就能看到预测` 这个结构对很多人更熟悉。

可以比较下面两种说法。

- 线性模型：几个特征的加权和大于阈值就预测为 positive
- 决策树：最近访问次数少，而且有延迟支付，则更可能 churn

两者都是模型。
但后者更像人们阅读业务规则的方式。

这种优点在实务里也经常被提到。

| 场景 | 决策树带来的优点 |
| --- | --- |
| 客户流失分析 | 更容易看出树是按什么问题顺序把流失分开的 |
| 贷款审核辅助 | 更容易说明哪个条件先形成了第一处分支 |
| 设备异常检测 | 更容易读出是哪些传感器范围形成了分支 |

但与此同时，也要立刻补上一句提醒。

`容易阅读，不等于一定能得到更好的泛化。`

这个风险会在下一节 P4-14.2 里直接展开。

### 既能做分类又能做回归，是什么意思

决策树既可以用于分类(classification)，也可以用于回归(regression)。
变化的地方在于 `leaf 输出什么`。

| 问题类型 | leaf 输出的内容 |
| --- | --- |
| 分类 | 最多的类别，或类别比例 |
| 回归 | 例如该 leaf 内样本值的平均数等代表数值 |

例如：

- 客户流失预测：`流失`、`保留`
- 房价预测：`预测价格 5.2 亿韩元`

也就是说，树的结构可以很相似，但最后输出的性质不同。
scikit-learn 对 `predict_proba` 的说明也把分类树中的预测概率读成“该 leaf 中同类样本所占比例”。
因此，正如 Part 4 的评价指标章节一再强调的，先确认当前问题是分类还是回归，比先盯着算法名称更重要。

### 训练是怎样挑选问题的

决策树训练的核心是 `比较看起来更好的问题候选`。

1. 查看多个 feature。
2. 在每个 feature 上生成 threshold 候选。
3. 计算分裂之后是否比之前让 label 更整齐。
4. 把最好的问题放到当前 node。
5. 如有需要，在每个分支里继续重复。

把这个过程简化画出来，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-02-zh.mmd"
```

这个图说明，决策树训练本质上就是 `不断挑第一好问题和下一好问题`。
它比较 feature 与 threshold 候选，挑出能更好降低 impurity 的 split，然后在每个分支里重复同样的过程。

这里的 `impurity` 指的是 node 内部混杂的程度。
按 API 文档的说法，分类树可以使用 `gini`、`entropy`、`log_loss` 等 criterion。
在现阶段，与其先背公式，不如先抓住这个直觉：
`一个 node 里类别越混杂，impurity 越高；越向单一类别整理，impurity 越低。`

### 用直觉去读 impurity

在分类树里，我们想知道的是：
`提出这个问题之后，label 有没有变得更整齐？`

比如某个 node 里有 10 个客户：

- 5 个 churn
- 5 个 stay

那么这个 node 就相当混杂。

如果通过某个问题分裂之后变成：

- 左支：4 个 churn，1 个 stay
- 右支：1 个 churn，4 个 stay

那么两个分支都可以被读成比原来更整齐。

所以，一个好的 split 往往就是：
`把一个混杂的 node 变成几个更不混杂的 node 的问题。`

## 案例与示例

### 案例 1. 当你想把客户流失问题一步一步缩小到提问流程里

某订阅服务团队正在做客户流失预测模型。
人们最先看的标准是这样一些问题：
`最近访问次数是不是很少？`
`是否有延迟支付？`
`客服咨询是否频繁？`

这个团队不想像线性模型那样一次算出一个总分。
他们希望业务侧能读懂问题流。
于是模型先问 `访问次数是否不超过 3 次？`，再问 `是否有延迟支付？`
这样一来，行为更相似的客户就会逐渐被分到同一条分支里。
在这里，决策树不再被读成一条边界线，而是一个寻找 `更好问题顺序` 的模型。

```mermaid
--8<-- "assets/part-04/chapter-14/p4-14-1-mermaid-03-zh.mmd"
```

这个场景里最重要的一点，是问题本身来自数据选择。
模型不是随便拿一个条件来用。
它会比较特征和阈值，找到能更好整理当前 node 的 split，把它作为第一处分支，再继续重复这个过程。
所以决策树不是“人随意写规则”的模型。
它是“把更能整理数据的问题不断累积起来”的模型。

可验证的结果会体现在两处：
一是第一处分裂候选的比较分数；
二是最后形成的小树结构。
如果 `visits <= 3` 比别的问题更能把数据分开，我们就能说明为什么这个问题会放在第一个 node。
再看每个 leaf 里聚集了哪些客户，也能确认树是怎样像规则一样被读出来的。

### 在实务场景里可以怎么读

当 `表格型数据(tabular data)` 是主体时，决策树尤其常被优先想到。
原因很简单：
数值和类别特征都比较自然地能写成阈值问题或条件问题。

| 工作场景 | 决策树式问题示例 |
| --- | --- |
| 客户流失 | 最近访问次数是否偏低？是否有延迟支付？ |
| 贷款审核辅助 | 收入是否高于阈值？是否有逾期记录？ |
| 设备异常检测 | 温度是否超过标准？振动是否超出范围？ |
| 营销响应预测 | 最近是否有购买？折扣消息响应率是否高？ |

在这些场景里，决策树可能比线性模型更直观。
但如果数据遵循非常平滑的连续关系，或者结构会因微小扰动而剧烈变化，就需要额外小心。
正如 API 文档提醒的，如果不加大小控制值，树可能会长成 fully grown and unpruned 的结构。
这正是下一节要接上的过拟合问题。

## 练习与示例

### 用 Python 找到 `好的第一问题`

这个练习不直接调用 scikit-learn 的学习器。
它是一个小实验，让读者直接体验决策树是怎样选第一处分裂的。

- 问题场景：为客户流失分类挑第一问题
- 输入(input)：`visits`、`late_payment`
- 标签(label)：`stay`、`churn`
- 要确认的概念：
  - feature 和 threshold 一变，split 分数也会变
  - 更能整理 label 的问题，有机会成为更好的第一处分裂
  - 树训练就是在不断重复这种选择

```python
rows = [
    {"customer": "A", "visits": 1, "late_payment": 1, "label": "churn"},
    {"customer": "B", "visits": 2, "late_payment": 1, "label": "churn"},
    {"customer": "C", "visits": 2, "late_payment": 0, "label": "stay"},
    {"customer": "D", "visits": 4, "late_payment": 0, "label": "stay"},
    {"customer": "E", "visits": 5, "late_payment": 0, "label": "stay"},
    {"customer": "F", "visits": 6, "late_payment": 1, "label": "stay"},
]


def gini(group):
    total = len(group)
    if total == 0:
        return 0.0

    counts = {}
    for row in group:
        counts[row["label"]] = counts.get(row["label"], 0) + 1

    score = 1.0
    for count in counts.values():
        p = count / total
        score -= p * p
    return score


def weighted_gini(left, right):
    total = len(left) + len(right)
    return (len(left) / total) * gini(left) + (len(right) / total) * gini(right)


candidates = [
    ("visits", 1.5),
    ("visits", 3.0),
    ("visits", 5.5),
    ("late_payment", 0.5),
]

best = None

for feature, threshold in candidates:
    left = [row for row in rows if row[feature] <= threshold]
    right = [row for row in rows if row[feature] > threshold]
    score = weighted_gini(left, right)

    print(f"feature={feature:12} threshold={threshold:>3} weighted_gini={score:.3f}")
    print("  left :", [(row["customer"], row["label"]) for row in left])
    print("  right:", [(row["customer"], row["label"]) for row in right])
    print()

    if best is None or score < best["score"]:
        best = {"feature": feature, "threshold": threshold, "score": score}

print("best first split")
print(best)
```

示例输出如下。

```text
feature=visits       threshold=1.5 weighted_gini=0.400
  left : [('A', 'churn')]
  right: [('B', 'churn'), ('C', 'stay'), ('D', 'stay'), ('E', 'stay'), ('F', 'stay')]

feature=visits       threshold=3.0 weighted_gini=0.222
  left : [('A', 'churn'), ('B', 'churn'), ('C', 'stay')]
  right: [('D', 'stay'), ('E', 'stay'), ('F', 'stay')]

feature=visits       threshold=5.5 weighted_gini=0.400
  left : [('A', 'churn'), ('B', 'churn'), ('C', 'stay'), ('D', 'stay'), ('E', 'stay')]
  right: [('F', 'stay')]

feature=late_payment threshold=0.5 weighted_gini=0.250
  left : [('C', 'stay'), ('D', 'stay'), ('E', 'stay')]
  right: [('A', 'churn'), ('B', 'churn'), ('F', 'stay')]

best first split
{'feature': 'visits', 'threshold': 3.0, 'score': 0.2222222222222222}
```

这个输出里要读的重点有三点。

1. 不是所有问题都会给出同样的质量。
2. 在当前数据里，`visits <= 3.0` 看起来是最能整理数据的第一问题。
3. 树就是靠不断重复这种比较来生成结构。

也就是说，决策树不是 `靠人直觉写问题` 的模型。
它是 `不断寻找更能整理数据的问题` 的模型。

再往前一步看，还要注意：
`好的第一问题` 也可能随着很小的数据变化而改变。
如果客户 `F` 的 label 不是 `stay` 而是 `churn`，那么 `late_payment` 这个问题就可能显得更强。
所以第一处分裂并不是绝对规则。
它依赖于当前训练数据正在形成什么分组。

### 改一个值，看第一处分裂会不会摇动

保留同一个例子，只改一个值。
这样更容易看出 `第一问题到底有多敏感`。

- 要改的值：客户 `F` 的 `label`
- 改动原因：故意制造一个让 `late_payment` 看起来更强的场景
- 要确认的概念：
  - 数据组成一变，split 分数也会跟着变
  - 决策树会沿着“更能整理当前数据”的方向改变问题流
  - 读第一处分裂时，除了分数，也要一起读改变标准的案例是谁

```python
changed_rows = [row.copy() for row in rows]
for row in changed_rows:
    if row["customer"] == "F":
        row["label"] = "churn"

best_changed = None

for feature, threshold in candidates:
    left = [row for row in changed_rows if row[feature] <= threshold]
    right = [row for row in changed_rows if row[feature] > threshold]
    score = weighted_gini(left, right)

    print(f"feature={feature:12} threshold={threshold:>3} weighted_gini={score:.3f}")

    if best_changed is None or score < best_changed["score"]:
        best_changed = {"feature": feature, "threshold": threshold, "score": score}

print("best first split after one label change")
print(best_changed)
```

示例输出如下。

```text
feature=visits       threshold=1.5 weighted_gini=0.500
feature=visits       threshold=3.0 weighted_gini=0.444
feature=visits       threshold=5.5 weighted_gini=0.267
feature=late_payment threshold=0.5 weighted_gini=0.250
best first split after one label change
{'feature': 'late_payment', 'threshold': 0.5, 'score': 0.25}
```

这个比较里最关键的一点是：
`一开始 visits 更像好的问题，但只改了一个 label，late_payment 就升到了第一问题。`
这并不是要把树简单断定成不稳定。
而是提醒我们在阅读分支结构时，要一起看 `当前数据把哪些案例放到了哪里`。

如果先用简短记录语言整理一次，同样的比较可以写成这样。

| 比较点 | 原始数据 | 改 label 之后 |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| 摇动结构的案例 | `F` 不会改变第一处分裂 | 改动 `F` 的 label 后，第一处分裂改变 |
| 先重看的内容 | 为什么 `C` 会被 `visits` 一起分到左边？ | 为什么 `F` 会让 `late_payment` 推动结构变化？ |

这个表的目的不只是总结 `发生了什么变化`。
对于初学者来说，把 `究竟是哪一个案例真的改变了问题选择` 记下来一次很有帮助。
这样到了下一节，就更容易自然理解 depth 和 leaf 大小为什么会让结构更容易摇动。

也可以直接回答下面这些问题。

1. 是哪一个单独案例改变了第一处分裂？
2. 当分数差距很小时，人类可读性是否也应该一起考虑？
3. 这种敏感性看起来会怎样连到下一节里的 depth、leaf 大小和过拟合风险？

如果可以，再亲自写一句：
`在当前数据里，visits 是第一问题，但只把 F 的 label 改掉，late_payment 就成了更好的第一问题。`
把这句话直接写出来，会更清楚地看到：决策树不是 `背固定规则`，而是在 `挑选更能整理当前数据的问题`。

### 亲手应用一个非常小的树

根据上面找到的第一处分裂，人可以手写出这样一个很小的树。

```text
if visits <= 3:
    if late_payment == 1:
        predict churn
    else:
        predict stay
else:
    predict stay
```

这段代码不是 `完整学习器`。
它只是对训练结果的人类可读化简。
当人们说决策树看起来比较可解释，通常脑中想的就是这种形状。

如果把同样的结构用一小段 Python 跑一下，会更直观。

问题场景：

- 与其只把决策树规则当成图片看，不如把实际输入放进去，直接检查结果是怎么出来的

输入(input)：

- 一个简单树规则 `predict`
- 客户示例列表 `examples`

期望输出(output)：

- 每个客户示例对应的预测结果

要确认的概念：

- 决策树可以被读成 if-else 形式的分支规则
- 所谓更高的可解释性，接近于说人能够跟着这条分支路径走下去

```python
def predict(tree_input):
    if tree_input["visits"] <= 3:
        if tree_input["late_payment"] == 1:
            return "churn"
        return "stay"
    return "stay"


examples = [
    {"customer": "G", "visits": 2, "late_payment": 1},
    {"customer": "H", "visits": 2, "late_payment": 0},
    {"customer": "I", "visits": 5, "late_payment": 1},
]

for row in examples:
    print(row["customer"], "->", predict(row))
```

示例输出如下。

```text
G -> churn
H -> stay
I -> stay
```

这个例子展示了决策树的三个重要特征。

- 可以沿着预测路径一步一步读
- 很容易说明到底在哪一个问题处分开了
- 但如果继续不断加问题，结构会很快变大

最后一点，正是下一节的主题。

### 练习：自己留下一个小树记录

如果你已经跑过上面两个练习，就不要只停留在“看结果”。
请留下一个简短记录。

1. 写下原始数据中的第一处分裂是什么。
2. 写下改动一个 label 之后，第一处分裂变成了什么。
3. 两种情况下各挑一个 `最模糊的案例`。
4. 最后写一句：你想立刻把树加深，还是想先在下一节里查看 depth 限制。

如果可以，自己填一下下面这个格式。

| 记录项 | 原始数据 | 改 label 之后 |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| 最模糊的案例 | `C` | `F` |
| leaf 最混杂的位置 | `visits <= 3.0` 左边分组 | `late_payment > 0.5` 右边分组 |
| 下一步问题 | `late_payment` 要不要做下一处分裂？ | 是不是该先检查 leaf，再继续加深？ |

这个练习的重点，不是背答案。
而是养成把决策树读成 `问题结构 + 案例分组`，而不是只读成 `一个分数` 的习惯。

刚开始时，即使只留下更短的记录也够了。

| 记录示例 | 原始数据 | 改 label 之后 |
| --- | --- | --- |
| first split | `visits <= 3.0` | `late_payment <= 0.5` |
| 最模糊的案例 | `C` | `F` |
| 下一步问题 | `late_payment` 要不要做下一处分裂？ | 是不是该先检查 leaf，再继续加深？ |

### 回收 Part 4 的目标

这一节的例子和练习，用四种方式重新展示了 Part 4 的共同目标。

- 问题定义：当前任务是 `为分类问题挑一个更好的第一问题`
- 输入表征：`visits`、`late_payment` 这样的 feature 会真正变成问题候选
- 评价阅读：weighted gini 越低，split 就越朝着更好整理 label 的方向被选中
- 下一步问题：不能只停在一个 split，还要继续判断哪些案例会摇动结构、是否要继续增加深度

所以，决策树入门真正要学的，不只是 `树能像条件语句一样去读` 这一句。
而是 `比较问题候选、阅读案例分组、同时思考下一处分裂和下一种限制` 这一整条流程。

| 显示出来的结构 | 解释边界 | 下一步问题 |
| --- | --- | --- |
| 第一处分裂来自“谁更能整理数据”的问题候选比较 | 当前数据一变，第一处分裂也可能改变 | 加上 depth 限制和最小样本数后，结构会怎样变？ |
| leaf 一边输出分类结果，一边也形成案例分组 | 即使分数相近，leaf 内部的混杂程度也可能不同 | 如果把每个 leaf 的代表案例单独留下，会多看到什么？ |
| 树能形成一条人容易跟着读的分支流程 | 易读性本身不等于泛化保证 | 下一节该怎样把过拟合和 pruning 接起来？ |

## 本节要记住的视角

- 决策树是 `通过拆分问题来做预测的模型`。
- node 是问题，split 是分支，leaf 是最终预测。
- 好的 split 往往会把 label 变成更不混杂的分组。
- 决策树既可以用于分类，也可以用于回归。
- 它相对容易读，但随着树加深，风险也会一起增长。

## 检查清单

- 在当前问题里，比起直线边界，问题流是不是更自然？
- 能不能重新查看第一处分裂和 leaf 组成到底形成了什么案例分组？
- 有没有把“易读性”和“泛化性能”混成同一句话？

## 什么时候要优先想起这个视角

- 当数据更适合按问题顺序逐步拆开来解释，而不是画一条线时，先想起决策树的问题流视角。
- 当你需要说明哪个 `feature + threshold` 真的把分组分得更好时，重新把 split 读成问题候选。
- 当你开始混淆 leaf 输出的是类别结果还是数值预测时，重新想起树结构既能用于分类也能用于回归。

## 出处与参考资料

- scikit-learn developers, `1.10. Decision Trees`, scikit-learn User Guide, 确认日期: 2026-06-27. [https://scikit-learn.org/stable/modules/tree.html](https://scikit-learn.org/stable/modules/tree.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `DecisionTreeClassifier`, scikit-learn API Reference, 确认日期: 2026-06-27. [https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, Jerome Friedman, Richard Olshen, Charles Stone, *Classification and Regression Trees*, Routledge, 1984.
