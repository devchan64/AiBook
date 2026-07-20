# P4-11.4 补充学习：如何读取多类别(multinomial)逻辑回归

> Section ID: `P4-11.4`
> Version: `v2026.07.19`

P4-11.3 里介绍的 log-odds 和 MLE，基本上是按 `二元分类(binary classification)` 来说明的，也就是在两个 class 里做选择。但现实中的分类问题，经常要在三个、四个或更多 class 里做选择。

本节的中心问题如下。

在二元分类里学会的 `score -> probability -> class 选择` 这个感觉，在多类别问题里会怎样继续下去？

## 本节范围

这一节回答下面这些问题。

- 在 multinomial 问题里，什么保持不变？
- 为什么会出现 softmax？
- one-vs-rest 和 multinomial 应该怎样区分？

这一节先把 multinomial logistic regression 收束为 `score -> probability distribution -> class 选择` 结构在多个 class 上继续扩展，并专注抓住 threshold 感觉怎样转移到 argmax 感觉上。

同时，下一步还要继续缩小来看清的问题也很明确。solver 与 regularization 的实现视角，会在 P4-11.5 继续。

## 本节目标

- 能说明在 multiclass 里，`input -> score -> probability 比较 -> class 选择` 这个结构仍然保持不变。
- 能把 softmax 读成 `把每个 class 的 score 变成 probability distribution 的函数`。
- 能在入门层面说明 one-vs-rest 和 multinomial 的差别。

## 学习背景

在 P4-11.1 第一次看 logistic regression 时，读者通常只盯着一个 `class 1 probability`，再和 threshold 比较。但很多现实问题，例如新闻分类、客户咨询分类、图像分类，都不是在两个里选一个，而是在多个 class 里选一个。

例如：

| 问题 | class 例子 |
| --- | --- |
| 新闻分类 | 政治 / 经济 / 体育 |
| 客户咨询分类 | 退款 / 配送 / 账号 |
| 图像分类 | 猫 / 狗 / 鸟 |

这里首先要抓住的，不是 `完全不同的新模型开始了`，而是 `在二元分类里学到的读取框架被扩展了`。

## 主要学习内容

### 在 multiclass 里，score 和 probability 比较的结构仍然保留

在多类别场景里，可以把 model 想成：会为每个 class \(k\) 生成一个 score \(z_k\)。

\[
z_k = w_k^\top x + b_k
\]

然后，为了把这些 score 变成一个 probability distribution，通常会使用 softmax。

\[
P(y = k \mid x) = \frac{e^{z_k}}{\sum_{j=1}^{K} e^{z_j}}
\]

这个式子的核心意思很简单。

- 分子是 `当前 class k 的 score`
- 分母是 `所有 class score 的总和`
- 所以某个 class 的 probability，永远是在 `所有 class 之间的相对比较` 里决定的

所以，multinomial logistic regression 的最小结构可以先压成两句话：`先为每个 class 生成 score`，再 `把这些 score 一起正规化成 probability distribution`。

### 二元分类里的 threshold 感觉，会转到 argmax 的感觉上

在二元分类里，最重要的直觉是 `它有没有超过 0.5`；到了 multiclass 里，最重要的直觉通常会变成 `哪个 class 的 probability 最大`。

- 二元分类：盯着一个 `class 1 probability`，和 threshold 比较
- 多类别分类：看 `所有 class 的 probability`，选择最大的那个

这个变化会直接连回 P4-11.1。初学者在这里很容易误会：是不是输出多个 probability，就变成了一个完全不同、更复杂的模型？其实核心结构依然还是 `input -> score -> probability 比较 -> class 选择`。

### one-vs-rest 和 multinomial 的差别，在于比较方式不同

在入门阶段，one-vs-rest 与 multinomial 的差别，大致先抓到下面这个层次就足够。

- one-vs-rest：把每个 class 分别当成 `是不是这个 class` 来单独判断，最后再比较
- multinomial：把所有 class 一次性放在一起，直接做相对比较

换成一个很小的客户咨询分类例子，就更容易看出来。

| 读取方式 | 同一条咨询会怎样被看 |
| --- | --- |
| one-vs-rest | 分别问 `是不是退款？`、`是不是配送？`、`是不是账号？`，然后再比较 |
| multinomial | 直接把 `退款 / 配送 / 账号` 放在一起，一次比较哪一边更像 |

这一节不需要把矩阵公式或 softmax 的完整展开都硬推到底。更重要的是，看到：在二元分类里学到的 `score 与 probability 比较` 的感觉，仍然会延伸到多个 class。

likelihood 的形式，也是在和二元分类同样的思路上扩展。假设正确答案是 one-hot vector，那么 multiclass 的 log-likelihood 通常可以读成下面这种求和形式。

\[
\log L = \sum_{i=1}^{n}\sum_{k=1}^{K} y_{ik} \log P(y=k \mid x_i)
\]

这里的 \(y_{ik}\) 表示：`如果样本 i 的真实答案是 class k，就取 1，否则取 0`。这个式子最终说的，也还是同一句话：`给正确 class 更高 probability 的方向，更值得被选择`，只是改成了多类别版本。

## 案例与示例

在进入案例前，可以先把本节的比较框架压成下面这张表。

| 场景 | 人最容易先用的标准 | 这个标准的限制 | 多类别 logistic regression 改变的点 | 要确认的结果 |
| --- | --- | --- | --- | --- |
| 多类别分类 | 继续把 0.5 当成主要标准 | 会把多个 class 的比较误读成二元问题 | 用 softmax 和 argmax 改成相对比较 | 选择 probability 最大的 class |
| 实现选择 | 把每个 class 分开看 | 会漏掉 class 之间的相对竞争 | 用 multinomial 结构一次性把所有 class 放在一起比较 | 要一起看完整 class distribution |

### 案例 1. 在 multiclass 里，比起 0.5，更重要的是相对比较

假设一个客户咨询分类任务有三个 class：`退款`、`配送`、`账号`。如果某条咨询的 probability 是 `[0.41, 0.39, 0.20]`，那么没有一个值超过 0.5。即使如此，model 仍然会把 `退款` 读成最像的 class。

这个场景说明：在多类别分类里，比起 `有没有超过 0.5`，更关键的问题是 `谁最大`。

### 案例 2. 同一个输入，one-vs-rest 和 multinomial 的读法会不同

如果一条咨询里同时混着 `退款`、`取消付款`、`账号锁定` 这样的词，one-vs-rest 会把每个 class 分开检查，再做比较；而 multinomial 会把所有 class 一次性放在一起，直接决定相对 probability。对初学者来说，后者常常更容易被读成 `一次性的比较结构`。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-4-mermaid-01-zh.mmd"
```

## 练习与示例

### Python 例子：读取多类别 probability 表

下面这个例子想展示的，是在 multiclass 里应该抓住的基本感觉：比起 `有没有超过 0.5`，更重要的是 `哪个 probability 最大`。

| 输入组 | 含义 |
| --- | --- |
| `class_names` | class 名称列表 |
| `multi_proba` | 每个 class 的 probability distribution 例子 |

```python
# 这个例子比较多类别逻辑回归中的各类别分数和 softmax 概率。
import numpy as np

class_names = ["refund", "shipping", "account"]
multi_proba = np.array([
    [0.41, 0.39, 0.20],
    [0.18, 0.63, 0.19],
    [0.22, 0.28, 0.50],
])

print("multiclass predictions")
for row in multi_proba:
    best_idx = int(np.argmax(row))
    print(
        "  probs =",
        np.round(row, 2),
        "->",
        class_names[best_idx],
    )
```

示例输出如下。

```text
multiclass predictions
  probs = [0.41 0.39 0.2 ] -> refund
  probs = [0.18 0.63 0.19] -> shipping
  probs = [0.22 0.28 0.5 ] -> account
```

这个输出可以这样读。

- 第一行里，虽然没有一个值超过 0.5，但因为 `refund` 的 probability 最大，所以仍然会被选中。
- 在 multiclass 里，重要的是 `整张 probability distribution 的相对比较`，而不是 `一个 probability 对一个 threshold`。
- 所以基本感觉会从 threshold 转向 argmax。

## 出处与参考资料

- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006. 确认日期: 2026-07-19. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, linear models user guide, [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09
- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09
