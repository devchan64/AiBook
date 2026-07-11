# P4-11.5 补充学习：第一次如何读 solver 与 regularization

> Section ID: `P4-11.5`
> Version: `v2026.07.11`

一旦通过 library 使用 logistic regression，很快就会遇到 solver、penalty、`C` 这样的参数。初学者常常在这里觉得：是不是话题突然跳进了实现细节？但这些设置并不是和理论完全无关的噪声。

本节的中心问题如下。

为什么即使模型名字都还是 logistic regression，也必须把 solver 和 regularization 设置一起记录、一起比较？

## 本节范围

这一节回答下面这些问题。

- solver 到底在做什么？
- regularization 在调什么？
- penalty 和 `C` 应该往哪个方向来读？

这一节不会深入讲下面这些内容。

- 各个 solver 内部优化算法的证明
- 一般 convex optimization 理论
- regularization 的严格统计解释

这些内容先放在本书当前范围之外。

## 本节目标

- 能把 solver 说明成 `真正去找参数的计算过程`。
- 能把 regularization 说明成 `防止模型把训练数据贴得过紧的装置`。
- 能在入门层面读取 L1、L2、Elastic-Net、`C` 的方向性。
- 能说明：即使模型名一样，设置差异也会改变结果解释。

## 学习背景

logistic regression 通常不是直接写出一个 closed-form solution，而是通过反复计算去找到比较好的参数。所以当数据规模不同、输入是否稀疏、所用 penalty 不同时，设置选择就会变得重要。

regularization 可以先读成 `防止模型把训练数据贴得过紧的装置`。即使都叫 logistic regression，如果数据很少、feature 很多，coefficient 就可能变得不稳定，或者过度依赖少数 feature。regularization 会帮助模型把这些 coefficient 拉得更保守。

## 主要学习内容

### solver 是把学习真正算出来的过程

首先，solver 会连到 `这个模型的参数到底是怎样被实际算出来的`。

先用下面这张表来抓最基本的意思就够了。

| 设置 | 本节先要理解的意思 | 后面可以再深看的问题 |
| --- | --- | --- |
| solver | 真正去找参数的计算过程 | 不同数据规模、稀疏性下什么更合适 |
| penalty | 决定 coefficient 要多保守的 regularization 方式 | L1 与 L2 会造成什么差别 |
| `C` | regularization 强度的反向控制值 | 怎样读取过拟合与欠拟合之间的变化 |

所以，solver 不是 `library 里无关紧要的小选项`，而是把 MLE 或 log loss 所定义的学习目标真正落到计算上的抓手。

下面这张表，概括的是 `2026-07-09` 查看的 scikit-learn stable 文档里的实现说明。solver 的支持范围和默认值会随着版本变化，所以在真实项目里，还是要回头确认你正在使用的文档版本。

| solver | multinomial 支持 | penalty / regularization | 首先要读出的特点 |
| --- | --- | --- | --- |
| `lbfgs` | 支持 | L2 或无 penalty | 作为默认起点通常比较稳妥 |
| `liblinear` | 不直接支持 multinomial | L1, L2 | 在小数据和二元分类里常被提到 |
| `newton-cg` | 支持 | L2 或无 penalty | 使用二阶信息的优化家族 |
| `newton-cholesky` | 支持 | L2 或无 penalty | 当 `n_samples` 很大且 one-hot 特征很多时可考虑 |
| `sag` | 支持 | L2 或无 penalty | 大数据上常较快，但对 scale 较敏感 |
| `saga` | 支持 | L1, L2, Elastic-Net | 对 sparse input 和 Elastic-Net 都比较容易处理 |

读取这张表时，最先要抓住的大致判断是下面这些。

- 先看是否需要直接支持 multinomial。
- 再看是否需要 `L1` 或 `Elastic-Net`。
- 如果数据很大、feature 也很多，就优先想到适合大数据的家族。
- 如果只是需要一个稳妥起点，`lbfgs` 常常是合理的第一候选。

### regularization 是让 coefficient 更保守的装置

在 regularization 一侧，至少应该把下面这些感觉固定下来。

| 设置 | 公式里的形状 | 入门上怎么读 |
| --- | --- | --- |
| L2 | \(\lambda \sum_j w_j^2\) | 整体压小 coefficient，减少过度不稳定 |
| L1 | \(\lambda \sum_j |w_j|\) | 可以把一些 coefficient 直接推向 0，产生稀疏性 |
| Elastic-Net | \(\lambda_1 \sum_j |w_j| + \lambda_2 \sum_j w_j^2\) | 混合 L1 和 L2 的性格 |
| `C` | regularization 强度的逆 | `C` 越小，regularization 越强 |

把这些式子立刻改写成解释语言，就是下面这些意思。

- L2 表示 `整体上不太偏好特别大的 coefficient`，所以可以读成减少 boundary 被某一个 feature 过度拉扯。
- L1 表示 `一些不太重要的 feature 可能被直接推到 0`，所以更容易和 feature selection 联系起来。
- Elastic-Net 可以读成一种折中：`整体先收缩，同时也希望一部分 coefficient 直接归零`。
- `C` 是 scikit-learn 里经常会看到的调节把手，必须牢牢记住它的方向：`越小表示 regularization 越强`。

### solver 和 regularization 不是实现选项，而是比较条件

在 P4-8 里，我们说过 baseline 比较要放在 `相同的数据拆分、相同的指标、相同的失败案例` 上。solver 和 regularization 也必须用同样的方式来读。

- solver 一换，计算路径和收敛特性就可能跟着变。
- regularization 强度一换，coefficient 的大小和 boundary 的保守程度也可能跟着变。

所以，即使两个实验都叫 `logistic regression`，在真正比较时仍然必须把 solver 和 regularization 设置写出来。否则，就无法区分性能差异到底来自 `模型结构`，还是来自 `设置差异`。

## 案例与示例

在进入案例前，可以先把本节的比较框架压成下面这样。

| 场景 | 人最容易先用的 기준 | 这个 기준 的限制 | solver / regularization 改变的点 | 要确认的结果 |
| --- | --- | --- | --- | --- |
| 设置选择 | 以为默认值永远足够 | 会漏掉数据结构与设置差异 | 逼着读者把计算过程和 regularization 强度都当成比较条件 | 即使模型名一样，结果解释也会不同 |
| coefficient 解读 | 直接接受大的 coefficient | 会漏掉数据少或 feature 多带来的不稳定 | 通过 regularization 让 coefficient 的解释更保守 | boundary 与 coefficient 的稳定性可能改变 |

### 案例 1. 为什么稀疏文本分类和表格数据不能总用一模一样的设置来读

在垃圾邮件分类里，单词很多，输入往往既高维又稀疏；而在客户流失预测这类表格数据里，feature 数量可能较少，解释性可能更重要。此时 solver 和 regularization 不是固定不变的普适常数，而是要根据数据结构与运营目的重新读取的把手。

### 案例 2. 怎样判断性能差异来自模型，还是来自设置

如果实验 A 和实验 B 都是 logistic regression，但一个用了 `lbfgs + L2`，另一个用了 `saga + Elastic-Net`，那就不能简单地把结果变化读成 `logistic regression 变好了`。在这种情况下，设置差异本身就可能比模型名字更重要。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-5-mermaid-01-en.mmd"
```

## 练习与示例

### Python 例子：看看比较记录应该怎样留下来

下面这段代码是一个 toy example，重点不在真正训练，而在展示 `比较记录应该怎么写下来`。

```python
from sklearn.linear_model import LogisticRegression

configs = [
    {
        "name": "baseline_lr",
        "solver": "lbfgs",
        "penalty": "l2",
        "C": 1.0,
    },
    {
        "name": "sparse_candidate",
        "solver": "saga",
        "penalty": "elasticnet",
        "l1_ratio": 0.5,
        "C": 0.5,
    },
]

models = []
for cfg in configs:
    kwargs = {
        "solver": cfg["solver"],
        "penalty": cfg["penalty"],
        "C": cfg["C"],
        "max_iter": 1000,
    }
    if "l1_ratio" in cfg:
        kwargs["l1_ratio"] = cfg["l1_ratio"]
    models.append((cfg["name"], LogisticRegression(**kwargs)))

for name, model in models:
    print(name, "->", model)
```

这个例子里真正重要的，不是马上把 model 跑起来，而是把 `虽然都叫 logistic regression，但到底比较了哪些设置组合` 明确地分开记录。

示例输出如下。

```text
baseline_lr -> LogisticRegression(max_iter=1000)
sparse_candidate -> LogisticRegression(C=0.5, l1_ratio=0.5, max_iter=1000,
                                       penalty='elasticnet', solver='saga')
```

## 与下一节的连接

到这里，Chapter 11 的补充学习轴就闭合了。也就是说，logistic regression 现在可以拆成五个层次来读：`可按 probability 来读的 score`、`boundary`、`log-odds 与 MLE`、`multiclass 扩展`、`训练计算与 regularization 设置`。

## 出处与参考资料

- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09
- scikit-learn, linear models user guide, [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09
