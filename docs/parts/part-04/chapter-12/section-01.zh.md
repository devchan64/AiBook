# P4-12.1 k-NN 的直觉

> Section ID: `P4-12.1`
> Version: `v2026.07.31`

在 P4-11.2 里，我们看到 [logistic regression](/AiBook/zh/reference/concept-glossary-pinyin/l/#logistic-regression) 是 `通过在 input space 里画出 boundary 来切开 class 的模型`。现在要把问题换一下。

如果不先画一条直线，而是先看周围相似的案例，能不能做出判断？

这正是 k-NN(k-nearest neighbors) 的出发点。更准确地说，k-NN 不太像 `先写出一个公式的模型`，而更像 `先去寻找新输入周围相似案例的模型`。

## k-NN 直觉先收束的问题

这一节回答下面这些问题。

- k-NN 是按什么想法来做判断的？
- `query`、`neighbor`、`label`、`k` 各自扮演什么角色？
- `k` 改变时，判断的性格会怎样变化？
- 在 k-NN 里，training 应该被理解成什么？

这一节先收束 `k-NN 是按什么基本想法，从周围案例出发做判断的`。distance function 和 scale 为什么会改变结果，会在 `P4-12.2 距离与尺度` 里继续处理；实际使用时的检查指南，会在 `P4-12.3 使用 k-NN 时应先检查什么` 里继续处理。

## k-NN 直觉要留下的判断标准

- 能把 k-NN 解释成 `把附近案例聚起来，再用多数表决或平均来判断的方法`。
- 能说明 `query`、`training data`、`neighbor`、`label` 在判断里各自做什么。
- 能说明 `k` 太小和太大时会出现什么差别。
- 能说明 k-NN 的 training 与其说是 `构造复杂公式`，不如说更接近 `准备好可比较的参考案例`。

## k-NN 依据邻近案例进行判断

k-NN 会先看一个新的输入，也就是 [query](/AiBook/zh/reference/concept-glossary-pinyin/m/#model-input)。接着，它会在已经有 [supervised learning label](/AiBook/zh/reference/concept-glossary-pinyin/j/#supervised-learning-label) 的 [training data](/AiBook/zh/reference/concept-glossary-pinyin/x/#training-data) 里找出和 query 距离最近的案例。最后，再把这些 [neighbors](/AiBook/zh/reference/concept-glossary-pinyin/n/#nearest-neighbor) 的 label 收集起来，用多数表决或平均做出结果。

简单压成下面四步。

1. 来了一个新的输入(query)
2. 在已有 training data 里找到距离最近的案例
3. 收集这些近邻案例的 label
4. 用多数表决或平均生成结果

所以，k-NN 可以被读成：`它不会单独解释一个新点，而是把这个点和周围已经知道的案例拿来比较`。

### 各个术语在判断里做什么

| 术语 | 在判断里扮演的角色 |
| --- | --- |
| query | 现在要预测的新输入 |
| training data | 已经同时拥有输入和 label 的参考案例集合 |
| neighbor | 因为离 query 近而被选进判断的案例 |
| label | 每个参考案例已经带着的答案或类别 |
| `k` | 决定要看多少个 neighbor 的数值 |

这张表很重要，因为 k-NN 与其说更接近 `在模型内部算出一个公式`，不如说更接近 `怎样读取参考案例`。

### 为什么要把附近案例当作依据

k-NN 的核心假设是：`相似的输入，很可能有相似的输出`。这个假设并不总是成立，但在局部相似性(local similarity) 真的有意义的问题里，它会是一个很强的起点。

例如：

- 购买模式相似的客户，可能会有相似的反应
- 点击路径相似的用户，可能会靠近相似的商品兴趣类别
- 分数模式相似的学生，可能会落到相似的结果类别

把这种直觉压成一个计算流程，可以画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-1-mermaid-01-zh.mmd"
```

不过，`近` 并不自动等于 `对`。只要用来计算近远的标准改变，neighbor 本身就可能改变。这正是下一节要处理的点。

### `k` 到底改变什么

`k` 决定的是：判断时要看多少个 neighbor。

- `k = 1` 时，只看最近的一个
- `k = 3` 时，看最近的三个
- `k = 5` 时，会用更宽一点的局部区域来判断

即使是同一个 query，只要 `k` 改变，判断的性格也会跟着改变。

| `k` 的取值 | 会出现的性格 |
| --- | --- |
| 太小 | 会对一两个近邻异常值非常敏感 |
| 适中 | 能保留局部模式，同时减少摇晃 |
| 太大 | 会把较远案例也混进来，让 boundary 变钝 |

一个很小的 toy example 会更清楚。

| query 周围的 label | `k = 1` | `k = 3` | `k = 5` |
| --- | --- | --- | --- |
| `1, 0, 0, 0, 0` | `1` | `0` | `0` |

这个例子说明：如果只看最近的一个点，结果是 `1`；但一旦把邻域放宽到三个或五个，局部多数就会把结果改成 `0`。所以 `k` 不是一个单纯的数字，而是决定 `看得多窄`、`看得多宽` 的把手。

### 在 k-NN 里，training 意味着什么

在 linear regression 或 logistic regression 里，通常会说模型 `学习了 coefficient`。k-NN 的感觉不一样。

在入门层面，k-NN 的 training 大致更接近下面这些事情。

- 把输入和 label 存起来
- 为之后新输入到来时的比较做好准备
- 如果需要，就使用能够加快 distance 计算的内部结构

所以，k-NN 更应该被读成 `为以后比较准备参考案例的学习`，而不是 `预先构造出精细公式的学习`。

也正因为如此，k-NN 会同时带着两个特征。

- 数据怎样整理、怎样表示很重要
- prediction 时的比较成本可能会变大

例如 training data 有 100 个时，一个 query 只要比较 100 次；但如果有 10 万个 training cases，同一个 query 就可能需要大量比较。说 `training 很简单`，并不等于说准备工作不重要，而是更接近：判断成本可能会在 prediction time 比 training time 更明显地冒出来。

### 它和线性 boundary 模型有什么不同

logistic regression 会先问：`怎样用一条公式或一条边界，把整个空间切得比较好？` 相比之下，k-NN 先问的是：`这个点周围聚着什么样的案例？`

| 模型视角 | 中心问题 |
| --- | --- |
| logistic regression | 画什么 boundary 才能把 class 分得比较好？ |
| k-NN | 这个新点周围的相似案例属于什么 class？ |

正因为这个差别，k-NN 把 `局部 neighbors` 放在 `全局规则` 前面。

## 案例与示例

### 案例 1. 当团队想先通过相似老客户来判断新客户

某个订阅服务团队想判断一个新客户的流失风险。人通常会先看 `最近访问次数`、`投诉频率`、`支付金额`、`登录时段` 这样的信号。

但团队还没有找到足够简单、足够稳定的规则，能直接说 `流失客户总是满足这种条件`。不过看已有记录时，又常常发现行为相似的客户，最后结果也比较像。这时，k-NN 不会单独解释新客户，而是会先去找周围比较相似的老客户，把他们的 label 当作依据。

```mermaid
--8<-- "assets/part-04/chapter-12/p4-12-1-mermaid-02-zh.mmd"
```

这个案例显示了三个重点。

- k-NN 更像 `先参考周围案例的模型`，而不是 `先写规则的模型`
- 如果 `k=1`，判断会对一个异常案例很敏感；如果 `k=5`，可能更稳定，但边界也会变钝
- 如果 neighbor 组成开始分裂，那首先是一个信号，告诉读者 `这个 query 需要再 review`

## 练习与示例

### Python 例子：看一个很小的 k-NN

- 问题场景：看看一个新点更靠近哪一组
- 输入(input)：可以当作二维坐标来读的两个 feature
- label：class 0 / class 1
- 要检查的概念：
  - prediction 是通过读取 neighbor label 做出来的
  - 即使 query 相同，只要 `k` 改变，结果也可能真的改变
  - 靠近边界的 query 很容易让解释摇晃

可以改动的值：

- 把 `query` 改成 `(4.3, 4.1)` 或 `(3.9, 4.0)`，观察最近邻顺序怎样变化。
- 把 `k` 列表改成 `[1, 2, 3, 5]` 这类形式，检查偶数 `k` 是否可能产生平票。

```python
# 这个例子计算新 query 与已有样本之间的距离，用来选择 k-NN 邻居和预测标签。
from math import dist
from collections import Counter

train = [
    ((4.1, 4.1), 1),
    ((3.7, 4.0), 0),
    ((3.8, 4.3), 0),
    ((4.2, 3.8), 0),
    ((4.4, 4.0), 1),
]

query = (4.0, 4.2)

def knn_predict(train, query, k):
    ranked = sorted(
        [(dist(point, query), point, label) for point, label in train],
        key=lambda x: x[0],
    )
    neighbors = ranked[:k]
    labels = [label for _, _, label in neighbors]
    prediction = Counter(labels).most_common(1)[0][0]
    return prediction, neighbors

for k in [1, 3, 5]:
    prediction, neighbors = knn_predict(train, query, k)
    print(f"k={k}, prediction={prediction}")
    for d, point, label in neighbors:
        print(" ", point, "label=", label, "distance=", round(d, 3))
    print()
```

示例输出如下。

```text
k=1, prediction=1
  (4.1, 4.1) label= 1 distance= 0.141

k=3, prediction=0
  (4.1, 4.1) label= 1 distance= 0.141
  (3.8, 4.3) label= 0 distance= 0.224
  (3.7, 4.0) label= 0 distance= 0.361

k=5, prediction=0
  (4.1, 4.1) label= 1 distance= 0.141
  (3.8, 4.3) label= 0 distance= 0.224
  (3.7, 4.0) label= 0 distance= 0.361
  (4.4, 4.0) label= 1 distance= 0.447
  (4.2, 3.8) label= 0 distance= 0.447
```

这个输出直接说明：`k` 不是单纯的数字，而是会改变判断范围的把手。

- 在 `k=1` 下，最近的一个点是 class 1，所以 prediction 是 `1`
- 一旦放宽到 `k=3`，三个最近点里有两个是 class 0，于是 prediction 变成 `0`
- 在 `k=5` 下，class 0 仍然更多，所以结果继续保持 `0`

也就是说，这个例子把一个点的例外和更宽一点的局部多数，可能会说出不同的话，这一点真正闭合了。这里首先该读的，不是 score，而是 `哪些 neighbor 被纳入了`，以及 `因此多数表决怎样改变了`。

## 检查清单

- 能不能把 k-NN 解释成 `把附近案例聚起来再判断的方法`？
- 是否理解 `query`、`neighbor`、`label`、`k` 在判断里承担不同角色？
- 能不能说明 `k` 不是单纯的数字，而是改变判断范围的把手？
- 能不能说明 `k` 太小和太大时的差别？
- 是否理解 k-NN 的 training 更接近 `准备比较基准案例`，而不是 `构造公式`？
- 是否知道在 k-NN 里，prediction time 的比较成本可能会变大？

## 出处与参考资料

- scikit-learn, *Nearest Neighbors*, scikit-learn User Guide, 确认日期: 2026-07-26. <https://scikit-learn.org/stable/modules/neighbors.html>{: target="_blank" rel="noopener noreferrer" }
