# P4-11.3 补充学习：第一次如何读 log-odds 与 MLE

> Section ID: `P4-11.3`
> Version: `v2026.07.26`

P4-11.1 把 [logistic regression](/AiBook/zh/reference/concept-glossary-pinyin/l/#logistic-regression) 介绍成 `生成可按 probability 来读的 score 的线性分类模型`，P4-11.2 又把这些 score 放回 input space，读成 [decision boundary](/AiBook/zh/reference/concept-glossary-pinyin/j/#decision-boundary)。走到这里，就会自然留下一个问题。

为什么不直接把 probability 当作线性公式来处理？为什么后面会跟着出现 [log-odds](/AiBook/zh/reference/concept-glossary-pinyin/l/#log-odds) 和 [最大似然估计(maximum likelihood estimation, MLE)](/AiBook/zh/reference/concept-glossary-pinyin/z/#maximum-likelihood-estimation-mle) 这样的词？

这一节就是用来回收这个问题的补充学习。中心是 `logistic regression 的 probability 解释` 和 `学习目标`。multinomial 扩展，以及 solver / regularization，会分到 P4-11.4 与 P4-11.5。

## log-odds 与 MLE 先收束的问题

这一节回答下面这些问题。

- 为什么会出现 log-odds？
- 为什么说 logistic regression 是用 MLE 学习的？
- [log loss](/AiBook/zh/reference/concept-glossary-pinyin/l/#log-loss) 和 MLE 是怎样连起来的？

这一节先把 log-odds 和 MLE 收束为连接 `probability 解释` 与 `学习目标` 的标准，并专注抓住为什么同一个 model 要用这样的数学语言重新读取。

同时，后面还要继续扩展的问题也很清楚。multinomial 扩展会在 P4-11.4 继续，solver 与 regularization 会在 P4-11.5 继续。

## log-odds 与 MLE 要留下的判断标准

- 能在入门层面解释 probability、odds、log-odds 之间的关系。
- 能说明 `z = 0`、`probability 0.5`、`odds 1` 指向的是同一个位置。
- 能说明 logistic regression 的学习方向是 `给正确答案更高的 probability`。
- 能把 MLE 和 log loss 读成同一个学习目标的两种表述。

## 学习背景

logistic regression 通常先从 `接上 sigmoid，把输出读成 0 到 1 之间的值` 开始。这个解释足够让人第一次进入，但再往下一点，就会遇到下面这些词。

- logit 或 log-odds
- likelihood 或 log-likelihood
- MLE
- log loss

初学者常常在这里卡住，是因为语言忽然变得像数学教材。但这些名字并不是各说各话，而是同一个问题从不同方向读出来的结果。

1. probability 被限制在 0 到 1 之间，不容易直接和 linear formula 接上。
2. 所以需要 log-odds 这种变换，把 probability 和 linear score 连接起来。
3. classification 的学习要问的是 `模型给正确答案分配了多高的 probability`。
4. 所以 likelihood、MLE、log loss 会一起出现。

也就是说，本节的核心不是背新算法，而是理解为什么 `probability 解释` 和 `学习目标` 会出现在同一章里。

## 主要学习内容

### 因为 probability 很难直接按线性公式处理，所以会出现 log-odds

像 P4-11.1 里看到的那样，logistic regression 会先产生 linear score \(z\)，再经过 sigmoid，把它读成 0 到 1 之间的值。

\[
p = \frac{1}{1 + e^{-z}}
\]

如果把这个式子当成 `把 probability p 反过来解回 z` 的感觉，一步一步往回读，就会得到下面这个过程。

\[
p = \frac{1}{1 + e^{-z}}
\]

\[
\frac{1}{p} = 1 + e^{-z}
\]

\[
\frac{1-p}{p} = e^{-z}
\]

\[
\frac{p}{1-p} = e^z
\]

最后对它取对数，就得到下面这个关系。

\[
\log \frac{p}{1-p} = z
\]

左边的 \(\frac{p}{1-p}\) 是 odds，而它的对数就是 log-odds 或 logit。这个关系重要的原因很简单。

- probability \(p\) 被困在 0 和 1 之间
- linear score \(z\) 可以自由地跨越负数和正数
- 所以如果想把 `适合线性处理的尺度` 和 `适合按 probability 读取的尺度` 连起来，就需要 log-odds 这样的桥梁

所以，log-odds 不是故意加难的术语，而是 `把 probability 和 linear formula 接起来的桥`。

看一个很小的表，会更有感觉。

| Probability \(p\) | odds \(p / (1-p)\) | log-odds |
| ---: | ---: | ---: |
| 0.10 | 0.111 | -2.197 |
| 0.50 | 1.000 | 0.000 |
| 0.80 | 4.000 | 1.386 |
| 0.90 | 9.000 | 2.197 |

这个表说明了下面这些点。

- probability 0.5 对应 log-odds 0
- 越确信属于 class 1，log-odds 就越大且为正
- 越确信属于 class 0，log-odds 就越小且为负

也就是说，在 P4-11.2 里说的 `decision boundary 是 linear score \(z = 0\) 的地方`，也可以重新读成 `probability 0.5`、`odds 1`、`log-odds 0` 指向同一个位置。

与其把这件事当作表格来硬背，不如先抓成 `同一个状态被不同刻度重新读取`。

![展示 probability 0.5、odds 1、log-odds 0 指向同一个决策中点的对应图](/AiBook/assets/part-04/chapter-11/p4-11-3-probability-odds-logit-zh.svg)

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-3-mermaid-01-zh.mmd"
```

### MLE 的意思是：找到能给正确答案高 probability 的参数

在 linear regression 里，用平方误差来思考很自然。但在 classification 里，正确答案只有 0 或 1，于是更重要的问题不是 `连续值离得多近`，而是 `给正确 class 的 probability 到底有多高`。

所以 logistic regression 通常会被解释成：最大化 likelihood，更常见的是最大化 log-likelihood。

如果某个二元分类样本的真实标签 \(y_i\) 是 0 或 1，而模型给出 class 1 的 probability 是 \(p_i\)，那么这个样本的概率可以压缩写成下面一行。

\[
P(y_i \mid x_i) = p_i^{y_i}(1-p_i)^{1-y_i}
\]

这个式子第一次看可能陌生，但它其实只是在压缩这句话：`如果正确答案是 1，就用 \(p_i\)；如果正确答案是 0，就用 \(1-p_i\)`。

- 当 \(y_i = 1\) 时，\(p_i^{1}(1-p_i)^0 = p_i\)
- 当 \(y_i = 0\) 时，\(p_i^{0}(1-p_i)^1 = 1-p_i\)

如果把全部 \(n\) 个样本放在一起，likelihood 会用乘积来表示。

\[
L(w, b) = \prod_{i=1}^{n} p_i^{y_i}(1-p_i)^{1-y_i}
\]

乘积不太好处理，所以通常会取 logarithm，把它变成 log-likelihood。

\[
\log L(w, b) = \sum_{i=1}^{n} \left(y_i \log p_i + (1-y_i)\log(1-p_i)\right)
\]

而在实现里，经常不会直接去最大化它，而是前面加一个负号，改成最小化 negative log-likelihood。

\[
-\log L(w, b) = - \sum_{i=1}^{n} \left(y_i \log p_i + (1-y_i)\log(1-p_i)\right)
\]

这就是二元 logistic regression 里经常出现的 log loss 的核心形式。

如果一行一行来读，它的意思是：

1. 一个样本，按 `给正确答案分了多高的 probability` 来读。
2. 整个数据集，按 `把所有样本的概率乘起来` 来读。
3. 为了让计算更方便，把乘积变成和，所以取对数。
4. 在实现里更容易做最小化，所以再加一个负号。

入门层面，先抓住下面这句话就足够了。

`MLE 就是在找一组参数，让当前 model 能把观察到的正确答案解释得尽可能像。`

### 为什么看 MLE 以后，就知道不能只用 accuracy 来解释学习

入门阶段最常见的误解之一是：`既然是分类，数对了多少不就够了吗？` 在评价阶段 accuracy 当然重要，但学习过程必须区分更细的差别。

例如，真实答案为 1 的样本：

- Model A 给出 0.51，几乎只是勉强猜对
- Model B 给出 0.99，对正确 class 的支持强得多

如果只看 accuracy，这两者都只是 `猜对了`。但训练时，不应该把它们当成一回事。MLE 正是让这种差别能够被看见的方式。

| 样本 | 真实答案 | Model A 的 class 1 probability | Model B 的 class 1 probability |
| --- | ---: | ---: | ---: |
| 1 | 1 | 0.55 | 0.90 |
| 2 | 0 | 0.45 | 0.10 |

在 threshold 0.5 下，这两个 model 都是对的。但 Model B 给正确 class 的 probability 高得多。这里出现的想法就是：`给正确答案更高 probability 的 model，应该被认为更好`。在 logistic regression 里，MLE 就是把这个想法写成数学表达。

这也是为什么学习过程里经常会连着看到 log loss。它可以读成：`如果给正确答案的 probability 太低，就会受到更大的惩罚`。所以 MLE 和 log loss，本质上是在从相反方向说同一个学习目标。

## 案例与示例

在进入案例前，可以先把本节的比较框架压成下面这样一张表。

| 场景 | 人最容易先用的标准 | 这个标准的限制 | logistic regression 改变的点 | 要确认的结果 |
| --- | --- | --- | --- | --- |
| probability 解释 | 只看 0 到 1 的数值 | 看不见它和 linear score 的连接 | 用 log-odds 把 probability 与 linear score 连起来 | \(z = 0\)、\(p = 0.5\)、odds 1 连在一起 |
| 学习目标 | 只看有没有猜对 | 会漏掉同样 accuracy 里的信心差别 | 用 MLE 与 log loss 重新读取信心差别 | 即使 accuracy 相同，学习评价也会不同 |

### 案例 1. 为什么边界附近的分数会让人觉得模糊

在考试及格预测里，如果某个学生的 class 1 probability 是 0.51，model 会偏向 `及格`。但这不是强确信，而是非常靠近边界的判断。只要把 log-odds 想起来，就会看到：`probability 刚刚高于 0.5` 这句话，也等于 `linear score \(z\) 刚刚高于 0`。

也就是说，本来在 probability 表里看起来模糊的感觉，会重新变成 `边界附近 score` 这个结构。

### 案例 2. 为什么 accuracy 一样，学习评价却可能不同

假设两个客户流失预测模型都在 100 个客户里猜对了 86 个。但其中一个模型经常对正确案例只给出 0.51、0.52 这样的分数，另一个模型则给出 0.80、0.88 这样的分数。它们的 accuracy 一样，但 `给正确答案的支持到底有多强` 并不一样。

这个场景正好说明为什么需要 MLE 和 log loss。分类模型要区分的不只是 `有没有猜对`，还包括 `对正确答案解释得有多像`。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-3-mermaid-02-zh.mmd"
```

## 练习与示例

### Python 例子：把 accuracy 和 log loss 一起读

下面这个例子展示的是：即使最终都猜对了，按照 probability 的确信程度不同，log loss 也会不同。

| 输入组 | 含义 |
| --- | --- |
| `true_binary` | 二元分类的真实标签 |
| `proba_model_a`, `proba_model_b` | 对同一组正确答案给出不同确信程度的两个 probability 例子 |

可以改动的值：

- 把 `proba_model_a` 改得更靠近边界，例如 `0.51`、`0.49`，可以观察 accuracy 不变时 log loss 是否会变大。
- 在 `proba_model_b` 里放入一个自信但错误的 probability，可以看到 log loss 会怎样强烈惩罚自信错误。

```python
# 这个例子计算 log-odds、似然和 MLE 如何连接到逻辑回归训练。
import numpy as np
from sklearn.metrics import log_loss

true_binary = np.array([1, 0, 1, 0])
proba_model_a = np.array([0.55, 0.45, 0.60, 0.40])
proba_model_b = np.array([0.90, 0.10, 0.85, 0.15])

pred_a = (proba_model_a >= 0.5).astype(int)
pred_b = (proba_model_b >= 0.5).astype(int)

print("binary accuracy A :", (pred_a == true_binary).mean())
print("binary accuracy B :", (pred_b == true_binary).mean())
print("log loss A        :", round(log_loss(true_binary, proba_model_a), 4))
print("log loss B        :", round(log_loss(true_binary, proba_model_b), 4))
```

示例输出如下。

```text
binary accuracy A : 1.0
binary accuracy B : 1.0
log loss A        : 0.5543
log loss B        : 0.1446
```

这个输出可以这样读。

- 两个 model 的 accuracy 可以完全一样，但 log loss 仍然不同。
- 所以从和 MLE 相连的学习视角看，`给正确答案的支持有多强` 会被区分出来。
- 因而理解 logistic regression 时，区分 `evaluation metric` 与 `training objective` 很重要。

## 出处与参考资料

- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006. 确认日期: 2026-07-26. [https://link.springer.com/book/9780387310732](https://link.springer.com/book/9780387310732){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `log_loss` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.log_loss.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-26
- scikit-learn, `LogisticRegression` API documentation, [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-26
