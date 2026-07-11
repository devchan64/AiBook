# P4-11.1 逻辑回归(logistic regression)的直觉

> Section ID: `P4-11.1`
> Version: `v2026.07.11`

在 P4-10 里，我们通过 linear regression 看到了 `怎样用一条直线预测连续值`。现在要接着看：同样是线性思路，到了 classification 问题时会怎样变化。

本节的中心问题如下。

如果想保留线性计算，但把输出读成 0 和 1 之间的值，应该怎么做？

这正是 logistic regression 的出发点。

这个名字经常会让人困惑。既然叫 `regression`，为什么最后做的是 classification？因为 logistic regression 的最终目的虽然是分类，但内部仍然先计算一个 linear combination，再把这个值变成可以像 probability 一样读取的形式，所以这个名字就保留了下来。

也就是说，logistic regression 不是 `把 linear regression 原样拿去做分类`，而是 `把线性计算的输出改写成可以按分类概率来解释的模型`。

这一节会说明 `logistic regression`、`sigmoid`、`predict_proba`、`threshold` 的基本含义。后面的章节会沿着这个抓手继续当前语境下的判断，而把线性计算先读成分类概率的基础感觉，也会通过这一节和 [概念词汇表](../../../reference/concept-glossary.md) 再接回来。

## 本节范围

这一节回答下面这些问题。

- logistic regression 为什么会用在 classification 问题里？
- 为什么名字里是 `regression`，结果却按分类来读？
- linear combination 是怎样变成 0 到 1 之间的值的？
- `predict_proba` 这样的输出到底表示什么？
- 为什么还需要 threshold？

这一节不会深入讲下面这些内容。

- log-odds 的严格推导
- 最大似然估计(maximum likelihood estimation, MLE)的完整公式展开
- 多类别(multinomial) logistic regression 的细节公式
- solver 差异和 regularization 设置

decision boundary 与 threshold 的空间解释，会在 P4-11.2 立刻继续；为什么会看到 log-odds，为什么会用 MLE，会在 P4-11.3 回收；二元分类怎样扩展到 multinomial，会在 P4-11.4 回收；solver 与 regularization 为什么会作为实现设置出现，会在 P4-11.5 回收。regularization 的更大视角以及 hyperparameter 的读取，也会在 P4-9.1、P4-9.2、P5-8.1 再接回来。

## 本节目标

- 能把 logistic regression 说明成 `在分类问题里生成可按概率读取输出的线性模型`。
- 能区分 linear regression 和 logistic regression 的共同点与差别。
- 能在入门层面解释为什么会出现 sigmoid。
- 能理解 `predict_proba` 和最终 class prediction 不是同一个阶段。
- 能说明 threshold 会介入分类判断。

## 学习背景

Part 4 的算法流程，是故意让回归到分类之间不要突然断开的。先看 linear regression，是为了说明 logistic regression 不是完全不同的新世界，而是同一个 linear model 家族里 `输出解释方式发生变化` 的一个例子。

| 课程位置 | logistic regression 的作用 |
| --- | --- |
| 在 P4-10 linear regression 之后 | 把线性思路扩展到 classification |
| 在 P4-6 评价指标之后 | 为概率输出与分类指标的连接做准备 |
| 在 P4-11.2 之前 | 引入 decision boundary 的概念 |

所以，P4-11.1 既是 `第一次正式介绍分类模型的 Section`，也是 `说明它与 linear regression 连续相接的 Section`。

## 主要学习内容

### logistic regression 处理什么问题

logistic regression 通常首先用 `二元分类(binary classification)` 来介绍，也就是在两个 class 里做选择的问题。

例如：

| 业务场景 | 要预测的值 |
| --- | --- |
| 客户会不会流失？ | 流失 / 不流失 |
| 邮件是不是垃圾邮件？ | 垃圾 / 正常 |
| 交易是不是欺诈？ | 欺诈 / 正常 |
| 患者是不是有较高疾病风险？ | 高风险 / 非高风险 |

这些问题的共同点是：输出不是连续数值，而是 `类别`。但内部计算仍然是数字。

`logistic regression 是先根据输入估计样本属于某个 class 的可能性，再把它读成 0 到 1 之间的分数，最后据此做分类判断的模型。`

### 为什么名字叫 regression，却在做 classification

这里首先要拆开的误解就是这一点。logistic regression 虽然用于分类，但内部仍然先计算一个 linear score。

最简单地可以把它想成下面这样。

\[
z = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

这个结构和 linear regression 里看到的是一样的。不同之处在于，它不会停在这里。linear regression 想把这个值直接当成 prediction 来读，而 logistic regression 会把它送进 sigmoid，把它变成 0 到 1 之间的值。

所以，名字里的 `regression` 更像是保留了线性组合与数值估计方式的痕迹，而真正的使用目的则更接近 `classification`。

### 为什么需要 sigmoid

如果在分类问题里直接使用 linear formula 的输出，就可能得到 `1.7`、`-2.3`、`5.8` 这样的值。但分类场景里，这样的值并不好直接读取。我们通常更想把它读成 `属于这个 class 的可能性有多大`，而这个值最好落在 0 和 1 之间。

sigmoid 正是做这件事的函数。

- 很大的正输入会被送到接近 1 的值
- 很大的负输入会被送到接近 0 的值
- 中间值会被送到 0.5 附近

`sigmoid 是把线性计算结果压进 0 到 1 范围，让它更容易按分类分数读取的函数。`

这个流程可以简单画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-1-mermaid-01-en.mmd"
```

关键点在于，logistic regression 不是把直线丢掉，而是 `在直线式计算之后，再加上一层解释用的变换`。

### linear regression 和 logistic regression 有什么相同，又有什么不同

这两个模型都使用 linear combination，所以很像。但输出的意义不同。

| 项目 | linear regression | logistic regression |
| --- | --- | --- |
| 主要处理的问题 | regression | classification |
| 内部计算 | linear combination | linear combination |
| 最终输出 | 连续值 | 0 到 1 的分数，以及 class 决定 |
| 入门解释 | 预测多少分、多少分钟、多少钱 | 哪个 class 的可能性更大 |

所以 logistic regression 不是一个起点完全不同的模型，而是把同样的线性结构改写成分类读取方式的模型。

### `predict_proba` 显示的是什么

在 scikit-learn 的 logistic regression 文档里，一个很重要的输出就是 `predict_proba`。读者很容易直接把它当成最终答案，但实际上它是前一层的信息。

例如，如果看到 `0.82`，通常表示 `model 认为这个样本属于 positive class 的可能性相当高`。但最终到底是把 class 记成 0 还是 1，则由 threshold 决定。

也就是说：

- `predict_proba`：可能性的程度
- `predict`：最终的分类决定

如果忽略这个差别，就很容易把 `score` 和 `decision` 当成同一件事。

看一个很小的例子会更清楚。

| 用户 | 用 `predict_proba` 读到的 class 1 分数 | 以 0.5 为 기준的判断 |
| --- | ---: | --- |
| A | 0.18 | class 0 |
| B | 0.49 | class 0 |
| C | 0.51 | class 1 |
| D | 0.87 | class 1 |

这个表里最重要的是 B 和 C。两个人的分数差距并不大，但在 threshold 0.5 下最终 class 已经分开了。也就是说，模型 만든 score 空间是连续的，而服务行为可能在上面不连续地分开。

### 为什么还需要 threshold

logistic regression 最常见的入门介绍，是把 `0.5` 当作分类 기준。

- 如果概率样的值 `>= 0.5`，就判为 class 1
- 如果概率样的值 `< 0.5`，就判为 class 0

但这个 기준并不是自然法则，而是被选择的 policy。

例如在 fraud detection 里，漏掉欺诈的代价可能很高，所以服务可能希望更积极地抓住可疑案例。反过来，如果服务不能过度阻挡正常用户，就可能把 threshold 设得更保守。

也就是说，logistic regression 负责生成 `像 probability 一样可读的分数`，而实际服务再在上面决定 `线到底画在哪里`。

这一点会直接连到 P4-6 的评价指标、P4-8 的 baseline、P4-9 的 tuning。

再看一个小例子。

| 客户 | 流失分数 | threshold = 0.5 | threshold = 0.7 |
| --- | ---: | --- | --- |
| E | 0.42 | 维持 | 维持 |
| F | 0.58 | 警告 | 维持 |
| G | 0.73 | 警告 | 警告 |

同样的 score，在 threshold 改变后，服务行为也会改变。所以读取 logistic regression 时，必须把 `模型分数` 和 `运营 policy` 分开来看。边界附近的案例首先应该被读成需要提高 review 优先级的信号，而不是把 threshold 一改就当作原因解释已经完成。

这里也要维持同样的比较框架。应该在相同的 baseline、相同的 score 区间、相同的代表失败案例上比较 threshold 前后，才能更清楚地分开 `哪些变化来自 policy`，`哪些问题来自特征表达不足`。

如果把这一点改写成项目记录语言，会更清楚。把 logistic regression 作为第一个比较模型时，不应该只留下 score 表，还应一起记录 `哪些 score 区间会被当作 review 对象`、`threshold 改变时哪些案例会改变行为`、`相比 baseline 到底改善了什么`。

| 需要一起留下的记录 | 为什么需要 |
| --- | --- |
| baseline 和 logistic regression 的 score 对比 | 为了看清到底比简单 기준改善了什么 |
| 不同 threshold 下行为变化的案例 | 为了记录同样分数在服务 policy 下会怎样变化 |
| review 대상 score 区间 | 为了把边界附近案例重新读成需要人工检查的对象 |
| 下一步调整问题 | 为了决定是改 threshold、补 feature，还是比较其他候选模型 |

这样才能把 `分数提高了`、`threshold 改了`、`警告变多了` 这些事实分开读取。

### 什么时候适合先把 logistic regression 放上候选

logistic regression 很常作为分类问题的第一个比较模型，但原因不是因为它单纯有名，而是因为它是一个比较容易把 score 和 policy 分开来读的线性分类模型。

| 当前问题状态 | 为什么先放 logistic regression | 先检查什么 |
| --- | --- | --- |
| 目标是 binary classification | 因为 0 到 1 的分数和最终 class 可以一起容易读取 | 输出到底是不是类别判断 |
| 需要一个可解释的首个分类模型 | 因为 linear score、coefficient、threshold 比较容易直接说明 | 线性边界是否足够 |
| 需要一个比 baseline 稍强的 score 模型 | 因为和多数类 기준相比，实际提升比较容易看 | confusion matrix 里到底哪里变好了 |
| 想留下人工 review 대상 score 区间 | 因为可以把 `predict_proba` 与 threshold 分开，定义 review 对象 | 是否单独记录了边界附近案例 |
| 必须区分服务 policy 与模型输出 | 因为 `模型负责产出 score，policy 决定行为` 这个结构很清楚 | 是否把 threshold 变化和模型改进混在一起 |

这张表的核心，是把 logistic regression 既当成 `超过第一个分类 baseline 的比较模型`，也当成 `训练如何分开读取 score 与 policy 的练习模型`。

## 案例与示例

### 案例 1. 为什么客户流失预测常把 logistic regression 作为第一个模型

假设团队想根据登录频率、上次购买时间、投诉次数来预测客户流失。如果某个用户得到 class 1 score `0.82`，这并不是在直接命令系统 `立刻采取行动`，而是在说 `按当前模型看，这个用户相当像流失 class`。

这种解释很有用，因为团队还可以在 threshold 之上决定：

- 立刻发优惠活动
- 交给人工 review
- 只做监控

所以 logistic regression 常常适合作为起点，不是因为它自动完成 policy，而是因为它把 `score 的生成` 和 `行为的决定` 清楚地拆开。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-1-mermaid-02-en.mmd"
```

### 案例 2. 为什么垃圾邮件过滤不能只看 probability

如果一封邮件的 spam score 是 `0.49`，在 threshold `0.5` 下它会留在正常收件箱里。但这并不等于它绝对安全，只表示在当前 threshold 下它落在 class 0 一侧。

服务仍然可以：

- 把它送进人工审核队列
- 给出更轻的提醒
- 或和代表性的 false-negative 案例再比较

这个场景说明：`像概率一样的输出` 与 `最终行为` 不能用同一句话来读。

## 练习与示例

### Python 例子：把 `predict_proba` 和 `predict` 分开读取

下面的例子说明 logistic regression 会先产出 score，然后再通过 threshold 把它变成 class。

```python
import numpy as np

scores = np.array([0.18, 0.49, 0.51, 0.87])
pred_05 = (scores >= 0.5).astype(int)

print("scores        :", scores)
print("threshold 0.5 :", pred_05)
```

示例输出如下。

```text
scores        : [0.18 0.49 0.51 0.87]
threshold 0.5 : [0 0 1 1]
```

这个输出说明：`0.49` 和 `0.51` 的 score 很接近，但只要 threshold 落下去，最终 class 就已经分开了。

### Python 例子：同时看 threshold 差异

这次直接观察：即使 score 相同，只要 threshold 改变，最终行为也会变化。

- 问题场景：假设已经得到了客户流失分数
- 输入(input)：已经算出的 class 1 分数
- 期待输出(output)：threshold 0.5 与 0.7 下判断如何改变
- 要检查的概念：
  - 即使 score 不变，policy 기준变化也会改变 class decision
  - 模型输出和服务行为必须分开读取

```python
import numpy as np

scores = np.array([0.42, 0.58, 0.73])

pred_05 = (scores >= 0.5).astype(int)
pred_07 = (scores >= 0.7).astype(int)

print("scores          :", scores)
print("threshold 0.5   :", pred_05)
print("threshold 0.7   :", pred_07)
```

示例输出如下。

```text
scores          : [0.42 0.58 0.73]
threshold 0.5   : [0 1 1]
threshold 0.7   : [0 0 1]
```

这个输出再次说明：是 model 负责生成 score，而是 operating rule 决定这个 score 如何变成行为。

### 再改一个值：如果边界附近的一个标签变了，分数解释会怎样摇晃

现在把训练数据里边界附近的 `study_hours = 4` 从 `不及格(0)` 改成 `及格(1)`。

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

study_hours = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(-1, 1)
passed_original = np.array([0, 0, 0, 0, 1, 1, 1, 1])
passed_shifted = np.array([0, 0, 0, 1, 1, 1, 1, 1])

model_original = LogisticRegression()
model_original.fit(study_hours, passed_original)

model_shifted = LogisticRegression()
model_shifted.fit(study_hours, passed_shifted)

score_original = model_original.predict_proba([[4]])[0][1]
score_shifted = model_shifted.predict_proba([[4]])[0][1]

print("class 1 score at x=4, original labels :", round(score_original, 3))
print("class 1 score at x=4, shifted labels  :", round(score_shifted, 3))
```

示例输出如下。

```text
class 1 score at x=4, original labels : 0.327
class 1 score at x=4, shifted labels  : 0.579
```

### 什么保持了不变，什么发生了改变

- 保持不变的点：整体方向仍然是学习时间越多，越倾向于及格一侧。
- 发生变化的点：只改了一个边界附近标签，`x=4` 的 class 1 score 就从 `0.327` 大幅移动到 `0.579`。
- 首先要留下的判断：logistic regression 的分数不是从自然里发现的原始概率，而是当前数据边界所形成的解释结果。

### 这个练习怎样回收到 Part 4 的目标

这个练习让 logistic regression 不再只是 `打印 score 的模型`，而重新读成 `对边界附近案例很敏感的分类规则`。Part 4 的目标，不是单独相信某个数字，而是读取某个案例变化会怎样摇动 score 解释和 threshold 判断。把同一个例子反复改一处再看，会更清楚地看到：在 model output 和 service action 之间，始终还隔着一层数据解释。

| 通用记录语言 | 这次练习里应立刻留下的内容 |
| --- | --- |
| 看见的结构 | 只改了一个边界附近标签，同一输入的 class 1 score 解释就大幅变化 |
| 解释边界 | 不能只凭这个 score 变化就断定真实世界概率突然改变，仍要把 sample 与 data boundary 一起看 |
| 下一个问题 | 如果再收集更多边界附近案例，score 会不会更稳定？加上 threshold policy 后又会怎样变化？ |

## 本节要记住的视角

- logistic regression 是在分类问题里生成可按概率来读的输出的线性模型。
- 内部计算仍然是 linear combination，但最终解释会通过 sigmoid 变成 0 到 1 的范围。
- `predict_proba` 是 score 阶段，`predict` 是应用 threshold 之后的 decision 阶段。
- coefficient 适合读取方向，但不会自动证明原因。
- threshold 更像是和 service policy 绑在一起的判断 기준，而不是模型本身的自然法则。

## 检查清单

- 现在的问题是不是 binary classification，是否已经先确认？
- 有没有把 `predict_proba` 和最终 `predict` 当成同一件事来读？
- 能不能把 threshold 变化和模型本身的改进分开说明？

## 什么时候要先想起这个视角

- 当 binary classification 的说明里把 score 和最终 decision 混成一句话时，要先想起 `predict_proba` 与 `predict` 的区分。
- 当调整 threshold 和重新训练模型被当成同一种修改时，要先把 policy boundary 和 model 本身拆开。
- 当 coefficient、sigmoid、像 probability 一样的输出一次性缠在一起时，要重新拿出 `线性计算后再加一层解释变换` 这个观点。

## 与下一节的连接

P4-11.1 把 logistic regression 读成 `生成可按 probability 来读的分数的线性模型`。下一节 P4-11.2 会转到：这些分数在 input space 里会形成怎样的 boundary，也就是 decision boundary 的视角。

如果 11.1 是 `输出解释` 的 Section，11.2 就是 `空间与边界解释` 的 Section。

## 出处与参考资料

- scikit-learn, `1.1.11. Logistic regression`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `LogisticRegression`, scikit-learn API Reference, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }
