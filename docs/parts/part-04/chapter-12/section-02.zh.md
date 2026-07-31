# P4-12.2 距离(distance)与尺度(scale)

> Section ID: `P4-12.2`
> Version: `v2026.07.31`

P4-12.1 里说过，k-NN 是 `通过看附近案例来做判断的模型`。但在这里，真正最重要的词其实是 `近`。

到底什么才算近？

如果跳过这个问题，读者其实只是看到了结果，而没有真的理解模型。因为在 k-NN 里，`用什么规则来计算近远` 本身就是模型的一部分。

## distance 与 feature scale 先收束的问题

这一节回答下面这些问题。

- distance 在 k-NN 里扮演什么角色？
- 如果 distance function 改变，neighbor 顺序和 prediction 会不会改变？
- 为什么 scale 会扭曲 distance 计算？
- standardization 会怎样改变 k-NN 的解释？

这一节先收束 `为什么在 k-NN 里，distance 和 scale 会改变 neighbor 与 prediction`。preprocessing 的目的和类型，仍然以 [P4-7.2 Preprocessing](../chapter-07/section-02.zh.md) 作为基准说明位置；这里专注的是 [distance](/AiBook/zh/reference/concept-glossary-pinyin/d/#distance) 和 [feature scale](/AiBook/zh/reference/concept-glossary-pinyin/b/#standardization) 改变判断的场景。

## distance 与 feature scale 要留下的判断标准

- 能说明 distance function 不是 `模型外部的设置`，而是 `判断规则的一部分`
- 能说明 distance function 一旦改变，neighbor 顺序和 prediction 也可能改变
- 能说明 feature 的 scale 不同时，大轴可能会支配 distance
- 能说明 standardization 不是 `把数字弄好看`，而是 `重新对齐比较标准`

## 距离是 k-NN 的判断规则

k-NN 会先计算新输入与已有数据之间的 [distance](/AiBook/zh/reference/concept-glossary-pinyin/d/#distance)，然后再找出最近的 neighbor。所以 distance function 不是单纯的计算工具，而是决定 `谁会被选成 neighbor` 的规则。

- Euclidean distance：把距离读成直线长度的方式
- Manhattan distance：把沿轴移动的量加起来的方式

即使是同一个 query，只要 distance rule 改变，neighbor 顺序就可能改变，prediction 也可能跟着改变。

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-01-zh.mmd"
```

这里最关键的一句话是：

`distance function 是解释输入的一部分视角。`

### distance function 改变时，neighbor 顺序也会改变

假设 query 和两个候选点如下。

| 对象 | 坐标 |
| --- | --- |
| query | (0, 0) |
| 点 A | (3, 0) |
| 点 B | (2, 2) |

如果按 Euclidean distance 来看：

- query 到 A 的距离 = 3
- query 到 B 的距离 = 约 2.83

所以 B 更近。

但如果按 Manhattan distance 来看：

- query 到 A 的距离 = 3
- query 到 B 的距离 = 4

这次就变成 A 更近。

这个例子展示的是：`distance rule 改变 -> neighbor 顺序改变`。在真正的 k-NN 里，一旦 neighbor 顺序改变，进入多数表决的 label 也会跟着改变，最终 prediction 当然也可能改变。

### 为什么 scale 会扭曲 distance 计算

和 distance function 一样重要的，是 scale。两个 feature 都是数字，不代表 distance 计算时它们就会被同样看待。

例如，假设有下面两个 feature。

- annual income：数值可能是几百万到几千万
- late payments：可能只是 0、1、2、7 这样的计数

它们都可能很重要。但如果直接保留原始范围，annual income 这一轴在数值上会显得大得多。于是 distance 会更强烈地问 `谁的收入数字更像`，而不是 `谁的逾期模式更像`。

这里要分开看的，是下面两件事。

- 单位差异：例如货币、秒数、次数，本来就属于不同的数字体系
- 分散程度差异：即使都是数值型 feature，也可能某个轴的波动远大于另一个轴

这两件事最终都会导向类似的问题：`大的轴支配了 distance`

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-02-zh.mmd"
```

### standardization 改变了什么

[standardization](/AiBook/zh/reference/concept-glossary-pinyin/b/#standardization) 不是为了让数字变得更漂亮。更准确地说，它是在 `重新平衡每个 feature 在 distance 计算里施加的影响`。

入门层面，按下面这个顺序来理解就足够了。

- 对每个 feature 先减去 mean
- 再除以 standard deviation
- 让大单位和小单位的轴进入一个更可比的范围

所以，standardization 可以被读成：`把原来被淹没的 feature 再拉回比较里`

但这并不等于它 `一定会提升性能`。重新被带回来的 feature 可能包含有用信息，也可能只是在带回噪声。

## 案例与示例

### 案例 1. 在贷款风险分类里，收入这个大数字掩盖了逾期记录

某个贷款筛查辅助模型想把新申请人分成 `safe` 和 `risky`。人首先会看 `annual income`、`late-payment count`、`existing loan size`、`repayment history` 这些信号。

问题在于，这些列的单位差得很大。annual income 可能是很大的数字，而 late-payment count 只是在 0 到几次之间。如果在这种状态下直接计算 k-NN distance，那么 late-payment count 就算在现实里很重要，也可能会被 income 这一轴淹没。

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-2-mermaid-03-zh.mmd"
```

这个案例显示了下面几个关键点。

- distance 和 scale 不是 preprocessing 之外的小选择，而是判断规则的一部分
- 即使数据本身不变，只要表示方式变了，`谁被算作近邻` 就可能改变
- 所以在 scale 调整前后，应该首先看 `哪些 neighbors 进来了，哪些出去 了`，而不是只盯着最后一个 score

## 练习与示例

### Python 例子：比较原始距离和 scale 调整后的距离

- 问题场景：看看一个新客户更接近 `safe` 还是 `risky`
- 输入(input)：annual income 与 late-payment count
- label：`safe` / `risky`
- 要检查的概念：
  - 在原始数字下，收入这一大单位轴可能会支配 distance
  - standardization 后，小轴的信息可能会重新进入比较
  - 因此，即使 query 相同，最近邻顺序也可能改变

可以改动的值：

- 把 `query` 的 income 改成 `5000000` 或 `7000000`，观察原始距离里哪一个轴更支配比较。
- 把 `k=3` 的检查改成 `raw_ranked[:2]`、`scaled_ranked[:2]` 这样的切片，先看 prediction 之前的 neighbor 组成。

可以按下面这个顺序来读。

1. 先看原始距离下，哪一组更近
2. 再看 standardization 后，哪些 neighbors 重新变得更近
3. 如果出现差异，先把它解释成 `nearness 的计算规则改变了`，而不是 `模型本身改变了`

```python
# 这个例子检查特征尺度差异如何改变距离计算和 k-NN 邻居选择。
from math import sqrt
from collections import Counter

train = [
    ((1800000, 1), "safe"),
    ((2200000, 0), "safe"),
    ((9000000, 7), "risky"),
    ((9500000, 8), "risky"),
]

query = (6000000, 0)

def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def zscore_from_train(train_points):
    cols = list(zip(*train_points))
    means = [sum(col) / len(col) for col in cols]
    stds = []
    for i, col in enumerate(cols):
        m = means[i]
        var = sum((x - m) ** 2 for x in col) / len(col)
        stds.append(var ** 0.5)
    return means, stds

def scale(point, means, stds):
    return tuple((x - m) / s for x, m, s in zip(point, means, stds))

def ranked_neighbors(points_with_labels, query_point):
    ranked = []
    for point, label in points_with_labels:
        ranked.append((euclidean(point, query_point), point, label))
    return sorted(ranked, key=lambda x: x[0])

def majority_vote(labels):
    return Counter(labels).most_common(1)[0][0]

train_points = [point for point, _ in train]
means, stds = zscore_from_train(train_points)

print("raw distances")
raw_ranked = ranked_neighbors(train, query)
for distance, point, label in raw_ranked:
    print(point, label, round(distance, 3))

print()

scaled_query = scale(query, means, stds)
print("scaled distances")
scaled_ranked = []
for point, label in train:
    scaled_point = scale(point, means, stds)
    scaled_ranked.append((euclidean(scaled_point, scaled_query), point, label, scaled_point))
scaled_ranked.sort(key=lambda x: x[0])

for distance, point, label, scaled_point in scaled_ranked:
    print(
        point,
        label,
        "scaled =", tuple(round(v, 3) for v in scaled_point),
        "distance =", round(distance, 3),
    )

print()
print("top-2 neighbors before scaling =", [(point, label) for _, point, label in raw_ranked[:2]])
print("top-2 neighbors after scaling =", [(point, label) for _, point, label, _ in scaled_ranked[:2]])
raw_top3_labels = [label for _, _, label in raw_ranked[:3]]
scaled_top3_labels = [label for _, _, label, _ in scaled_ranked[:3]]
print("k=3 labels before scaling =", raw_top3_labels)
print("k=3 labels after scaling =", scaled_top3_labels)
print("k=3 prediction before scaling =", majority_vote(raw_top3_labels))
print("k=3 prediction after scaling =", majority_vote(scaled_top3_labels))
```

示例输出如下。

```text
raw distances
(9000000, 7) risky 3000000.0
(9500000, 8) risky 3500000.0
(2200000, 0) safe 3800000.0
(1800000, 1) safe 4200000.0

scaled distances
(2200000, 0) safe scaled = (-0.943, -1.131) distance = 1.046
(1800000, 1) safe scaled = (-1.053, -0.849) distance = 1.305
(9000000, 7) risky scaled = (0.929, 0.849) distance = 1.897
(9500000, 8) risky scaled = (1.067, 1.131) distance = 2.179

top-2 neighbors before scaling = [((9000000, 7), 'risky'), ((9500000, 8), 'risky')]
top-2 neighbors after scaling = [((2200000, 0), 'safe'), ((1800000, 1), 'safe')]
k=3 labels before scaling = ['risky', 'risky', 'safe']
k=3 labels after scaling = ['safe', 'safe', 'risky']
k=3 prediction before scaling = risky
k=3 prediction after scaling = safe
```

这个输出里，首先要抓住下面这句话。

`k-NN 的结果不仅依赖数据本身，也依赖数据是怎样被表示的。`

在原始距离下，先出现的是 `risky` 组；standardization 之后，先出现的是 `safe` 组。如果再用 `k=3` 来看，原始距离里是 `risky, risky, safe`，所以最后 prediction 是 `risky`；standardization 之后是 `safe, safe, risky`，于是 prediction 变成 `safe`。因此，这个例子首先应该让读者看到的，不只是 score 变了，而是 `neighbor 顺序本身变了，而且这种变化真的传到了 k-NN 的判断上`。

### 再改一个值：在相同 scale 下，只增加 late-payment count，会怎样重新打乱 neighbor 顺序

现在保持同一个 standardization 方式，只把 query 的 late-payment count 从 `0` 改成 `2`。

可以改动的值：

- 把 `scaled_query_2` 的第二个值改成 `1`、`3`、`5`，观察 neighbor 顺序什么时候再次混合。
- 把 `ranked_0[:2]` 改成 `ranked_0[:3]`，检查 neighbor 替换是否继续影响多数表决。

```python
# 这个例子检查特征尺度差异如何改变距离计算和 k-NN 邻居选择。
from math import sqrt

train = [
    ((1800000, 1), "safe"),
    ((2200000, 0), "safe"),
    ((9000000, 7), "risky"),
    ((9500000, 8), "risky"),
]

def euclidean(a, b):
    return sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def zscore_from_train(train_points):
    cols = list(zip(*train_points))
    means = [sum(col) / len(col) for col in cols]
    stds = []
    for i, col in enumerate(cols):
        m = means[i]
        var = sum((x - m) ** 2 for x in col) / len(col)
        stds.append(var ** 0.5)
    return means, stds

def scale(point, means, stds):
    return tuple((x - m) / s for x, m, s in zip(point, means, stds))

def ranked_neighbors(points_with_labels, query_point):
    ranked = []
    for point, label in points_with_labels:
        ranked.append((euclidean(point, query_point), point, label))
    return sorted(ranked, key=lambda x: x[0])

train_points = [point for point, _ in train]
means, stds = zscore_from_train(train_points)

scaled_query_0 = scale((6000000, 0), means, stds)
scaled_query_2 = scale((6000000, 2), means, stds)

ranked_0 = ranked_neighbors([(scale(point, means, stds), label) for point, label in train], scaled_query_0)
ranked_2 = ranked_neighbors([(scale(point, means, stds), label) for point, label in train], scaled_query_2)

print("top-2 after scaling, late_payment=0 :", [(label, round(distance, 3)) for distance, _, label in ranked_0[:2]])
print("top-2 after scaling, late_payment=2 :", [(label, round(distance, 3)) for distance, _, label in ranked_2[:2]])
```

示例输出如下。

```text
top-2 after scaling, late_payment=0 : [('safe', 1.046), ('safe', 1.305)]
top-2 after scaling, late_payment=2 : [('safe', 0.975), ('risky', 1.184)]
```

### 什么保持了不变，什么发生了改变

- 保持不变的点：scale 调整之后，distance 仍然不再只看 income，一样会让 late-payment 轴真正参与比较
- 发生变化的点：只把 late-payment count 稍微提高一点，第二个 neighbor 就开始从 `safe` 换成 `risky`
- 首先要留下的判断：standardization 不是一次做完就结束的技术检查，它也是重新观察 `feature 变化会怎样摇动 neighbor 组成与 prediction` 的出发点

通过这个比较，k-NN 不再只是 `找来近邻案例的模型`，而会被重新读成 `对表示方式和输入变化都很敏感的比较规则`。重要的不是背下 `k` 的数值，而是能够说明：即使是同一个 query，只要表示方式或 feature 数值稍有变化，哪些 neighbor 会进来，哪些会出去。反复改一处的练习，真正的学习效果也不在于只说 `prediction 变了`，而在于能指出 `改了什么以后，比较标准的哪一部分又被重新打乱了`。

| 通用记录语言 | 这次练习里应立刻留下的内容 |
| --- | --- |
| 看见的结构 | scale 对齐之后，即使很小的 feature 变化，也会重新打乱 neighbor 组成和最终判断 |
| 解释边界 | 只凭某一个 query 的 neighbor 变化，不能直接断定某个 feature 永远更重要 |
| 下一个问题 | 如果改变 `k`，neighbor 的替换会不会继续传到最终多数表决？其他 query 上也会不会出现同样的敏感度？ |

## 检查清单

- 能不能说明为什么 distance function 是判断规则的一部分？
- 是否理解了 distance function 改变时，neighbor 顺序和 prediction 也会改变？
- 是否理解了大轴支配 distance 时，小轴上的重要信息可能会被埋掉？
- 能不能把 standardization 解释成重新平衡比较标准？
- 是否在同一个 query 上，比较了 scale 调整前后哪些 neighbor 进来、哪些出去？
- 即使 standardization 后出现了差异，是否也没有把它单独当成完整的原因解释？

## 出处与参考资料

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, 确认日期: 2026-07-26. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
- scikit-learn, *Importance of Feature Scaling*, scikit-learn Examples, 确认日期: 2026-07-26. <https://scikit-learn.org/stable/auto_examples/preprocessing/plot_scaling_importance.html>{: target="_blank" rel="noopener noreferrer" }
