# P4-4.1 训练数据与评估数据

> Section ID: `P4-4.1`
> Version: `v2026.07.19`

在 P4-3 章里，我们看过怎样利用 heuristic 先缩小要尝试的模型候选。接下来就会出现一个重要问题：怎样确认这个选择在现实里到底合不合理？

在机器学习里，model 只是在已经看过的数据上拟合得很好，还远远不够。我们真正想要的是：它在以后会进来的新数据上也能做出可用的判断。所以，数据不会全部都只拿去训练，而是会另外留出一部分专门用于评估。

训练数据，是 model 用来学习的数据。评估数据，是用来检查 model 学到了什么的数据。这里最重要的第一个视角其实很简单：`如果只用已经学过的练习题去考试，就很容易高估自己的实力。`

## 本节范围

这一节解释为什么要拆分数据。validation data 和 test data 的细致区分会在 P4-4.2 处理，这里先把 `用于学习的数据` 和 `专门留出来评估的数据` 的差别固定下来。

overfitting 和 generalization 会在 P4-5 详细处理。accuracy、precision、recall 这类 metric 会在 P4-6 处理。本节的重点是 `为什么必须先分开再确认`。

- 为什么不能把全部数据都只拿去训练？
- training data 和 evaluation data 分别承担什么角色？
- model 只在已经看过的数据上表现好，为什么危险？
- 数据拆分能减少哪些误解？
- 当数据很少时，需要特别小心什么？

## 本节目标

- 能区分 training data 和 evaluation data 的角色。
- 能说明如果用同一份数据同时训练和评估，就可能高估性能。
- 能理解 evaluation data 是 `为了估计 model 在新数据上的表现而准备的代理场景`。
- 能说明为什么数据拆分会继续连接到 model selection、overfitting 和 generalization。
- 能保持一个边界感：validation 和 test 的细致区分会在下一节展开。

## 学习背景

### 先用一个场景来理解

假设一个学生背熟了 100 道数学题。如果你把同样的 100 道题再给他一次，他当然可能拿到很高分。但这还不能证明他真的会做新题。

机器学习 model 也是类似的。model 会在 training data 里找 pattern。但如果评估时也用同一份数据，就很难区分：它到底是学会了模式，还是只是把具体例子记住了。

| 情况 | 表面结果 | 真正要小心的地方 |
| --- | --- | --- |
| 用训练过的数据再评估一次 | 分数可能会很高 | model 可能只是记住了这些样本 |
| 用另外留出来的数据评估 | 分数可能会更低 | 这更接近它在新数据上的真实表现 |
| 在新数据上失败 | 如果只看训练分数，很容易忽略 | 这时就需要数据拆分和 generalization 检查 |

这个比喻并不完美，但它抓住了数据拆分的核心。model 的目的不是把已经见过的例子重新答对，而是要能应对还没见过的例子。

实际工作里，首先要判断的是：`当前问题应该先用哪一种拆分视角。`

| 当前问题状态 | 应先抓住的拆分视角 | 原因 |
| --- | --- | --- |
| 在表格型数据里，预测新案例是中心任务 | 先分成 training data 和 evaluation data | 因为必须把见过的案例和没见过的案例分开 |
| 数据里时间顺序是核心 | 用过去数据训练，用后面的时间点评估 | 因为如果未来信息泄漏进过去学习，结果会被扭曲 |
| 稀有 label 很少 | 拆分后先检查 label 比例 | 因为如果一边过于偏斜，评估本身就会不稳定 |

## 主要学习内容

### 数据会按角色拆开

最基本的拆分，就是 `用于学习的一部分` 和 `用于评估的一部分`。

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-1-mermaid-01-zh.mmd"
```

在这张图里，evaluation data 指的是没有直接参与学习过程的数据。先用 training data 构建 model，再用 evaluation data 检查这个 model 在别的例子上是否还能工作。

这里的 `evaluation data` 是广义表达。真实项目里，validation data 和 test data 往往还会进一步分开，这个区分会在 P4-4.2 展开。

如果换成一个很小的表格，会更直观。

| 客户 ID | 最近购买次数 | 咨询次数 | 是否流失 | 用在哪里 |
| --- | --- | --- | --- | --- |
| C01 | 8 | 0 | 留存 | training data |
| C02 | 2 | 3 | 流失 | training data |
| C03 | 6 | 1 | 留存 | training data |
| C04 | 1 | 4 | 流失 | evaluation data |
| C05 | 7 | 0 | 留存 | evaluation data |

在这个例子里，先用 C01、C02、C03 学出规则，再用 C04、C05 检查规则是否还能成立。如果连 C04、C05 也一起拿去训练，model 就已经见过这些案例，评估的意义会变弱。

把同样的想法换成代码，可以像下面这样看。下面的例子会把客户 feature 列表 `X` 和流失 label `y` 按同一个基准一起拆开，并确认哪些样本和 label 进入 training 侧、哪些进入 evaluation 侧。结果中会一起查看 training 输入/label、evaluation 输入/label、两边的样本数和 `churn` 比例。

要确认的核心是，`train_test_split` 会按同一个基准同时拆分输入和 label。拆分之后，比起先看性能分数，更重要的是养成先检查数量和 label 比例的习惯。

```python
# 这个例子把输入特征 X 和目标 y 分成训练集与评估集，并检查标签比例。
from sklearn.model_selection import train_test_split

X = [
    [8, 0],  # recent purchases, support tickets
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
]
y = ["stay", "churn", "stay", "churn", "stay"]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
)

print("training inputs:", X_train)
print("evaluation inputs:", X_eval)
print("training labels:", y_train)
print("evaluation labels:", y_eval)
print("training sample count:", len(X_train))
print("evaluation sample count:", len(X_eval))
print("training churn ratio:", y_train.count("churn") / len(y_train))
print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
```

一个示例输出可以这样读。

```text
training inputs: [[6, 1], [8, 0], [1, 4]]
evaluation inputs: [[2, 3], [7, 0]]
training labels: ['stay', 'stay', 'churn']
evaluation labels: ['churn', 'stay']
training sample count: 3
evaluation sample count: 2
training churn ratio: 0.3333333333333333
evaluation churn ratio: 0.5
```

这段代码展示了最基本的结构：不是把整份数据一次性送进 model，而是先拆成 training 部分和 evaluation 部分。`X_train`、`y_train` 用来学习，`X_eval`、`y_eval` 则专门留给后续检查。

这里一起打印出来的值，还不是 model 的性能 metric。它们是拆分数据后最应该立刻检查的基础项。

- training 样本数和 evaluation 样本数是怎样分开的
- churn label 比例有没有严重偏向某一边

光看这些输出，也能更具体地理解 `model 即将开始学习的环境到底是什么样子`。

如果换成更接近实务的写法，通常会先从 `DataFrame` 里分出输入列和目标列，然后再拆分。下面的例子使用 feature 列列表 `feature_columns`、目标列 `target_column` 和表格数据 `df`，来确认 `X_train`、`X_eval` 的 `shape` 以及 training/evaluation 两侧的 label 比例。

要确认的核心是，实务型拆分应按 `先分出输入列集合 X 和答案列 y` 的顺序来读。`shape` 和 label 比例是检查拆分结果的基本输出。

```python
# 这个例子把输入特征 X 和目标 y 分成训练集与评估集，并检查标签比例。
import pandas as pd
from sklearn.model_selection import train_test_split

feature_columns = ["recent_purchases", "support_tickets", "days_since_login"]
target_column = "churned"

df = pd.DataFrame(
    [
        {"recent_purchases": 8, "support_tickets": 0, "days_since_login": 2, "churned": "stay"},
        {"recent_purchases": 4, "support_tickets": 1, "days_since_login": 5, "churned": "stay"},
        {"recent_purchases": 6, "support_tickets": 1, "days_since_login": 4, "churned": "stay"},
        {"recent_purchases": 1, "support_tickets": 4, "days_since_login": 21, "churned": "churn"},
        {"recent_purchases": 7, "support_tickets": 0, "days_since_login": 3, "churned": "stay"},
    ]
)

X = df[feature_columns]
y = df[target_column]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

print("X_train shape:", X_train.shape)
print("X_eval shape:", X_eval.shape)
print("training label ratio:")
print(y_train.value_counts(normalize=True))
print("evaluation label ratio:")
print(y_eval.value_counts(normalize=True))
```

一个示例输出会像下面这样。

```text
X_train shape: (4, 3)
X_eval shape: (1, 3)
training label ratio:
churned
stay     0.75
churn    0.25
Name: proportion, dtype: float64
evaluation label ratio:
churned
stay    1.0
Name: proportion, dtype: float64
```

这里真正重要的不是语法本身，而是角色拆分。只要能读出 `先把输入 X 和答案 y 分开，再把它们拆成 training 和 evaluation` 这个顺序，就已经够用了。`shape` 和 label 比例的输出，则是最快判断拆分是否过于偏斜的基本检查。

### 数据拆分也要符合问题本身

`拆分数据` 这句话并不总是意味着一律随机切开。拆分基准也会随着问题的性质而改变。

| 情况 | 先想到的拆分方式 | 原因 |
| --- | --- | --- |
| 像客户流失、分数预测这样的表格型数据 | random split | 因为很多时候希望 training 和 evaluation 具有相近分布 |
| 像月度销售、传感器日志、股价这样时间顺序重要的数据 | time-based split | 因为把未来信息混进过去训练，会扭曲真实部署情境 |
| 像缺陷检测、罕见疾病这样稀有 label 很少的数据 | stratified split | 因为如果稀有 label 只集中到一边，评估会变得不稳定 |

例如，假设你收集了某个网店从 1 月到 6 月的数据。

| 月份 | 客户数 | 流失客户数 | 用在哪里 |
| --- | --- | --- | --- |
| 1 月 | 100 | 8 | training data |
| 2 月 | 110 | 9 | training data |
| 3 月 | 120 | 11 | training data |
| 4 月 | 115 | 12 | training data |
| 5 月 | 125 | 15 | evaluation data |
| 6 月 | 130 | 18 | evaluation data |

在这种情况下，用 1 月到 4 月训练，再用 5 月、6 月评估，会更接近真实运营流程。相反，如果把 6 月数据切一部分混进 2 月、3 月一起训练，未来才出现的模式就可能泄漏回过去。

## 细部学习内容

### 如果拆分方式不对，会出现什么误解

就算数据确实拆开了，如果拆分方式和问题本身不匹配，也仍然可能制造错误的安心感。

| 拆分方式 | 表面上看起来为什么像是可以接受 | 实际风险 |
| --- | --- | --- |
| 随机拆分整份数据 | 快而且简单 | 对时间顺序重要的问题，未来信息可能会混进来 |
| 不看 label 比例就直接拆分 | 代码会更简单 | 如果评估侧几乎没有某类 label，分数会失真 |
| 同一个客户、设备或文档片段同时出现在两边 | 数据量看起来很多 | 其实 model 已经见过非常相似的案例，评估会变得过于容易 |

如果用一个很小的流失例子来看，这个问题会更明显。

| 拆分结果 | training 侧的 label | evaluation 侧的 label | 可能出现的问题 |
| --- | --- | --- | --- |
| 好例子 | `stay, stay, churn, stay` | `stay, churn` | 两边都还能检查基本模式 |
| 坏例子 | `stay, stay, stay, stay` | `churn, churn` | training 侧完全没有流失案例，model 很难真正学会流失 |

在这种情况下，就算 evaluation 分数低，也很难分清是 model 差，还是拆分本身一开始就错了。所以，拆分之后不仅要看样本数，也要看 label 分布。

### 为什么用同一份数据来学习和评估会有风险

model 会从数据中找 pattern。但如果 model 很灵活，或者数据量很小，它就可能不仅抓住一般模式，还会连 training data 里的偶然痕迹一起学进去。

例如，在客户流失预测里，training data 里恰好有很多 `在某个活动期间注册的客户` 都发生了流失。如果 model 过度相信这个痕迹，它就可能把与该活动无关的新客户也判断错。

如果评估也用同一份数据，这种问题就会被遮住。因为 model 正在重新匹配自己已经见过的痕迹，所以会拿到高分。但如果用单独留下来的数据评估，就能更现实地检查：这种判断在别的例子上是否也成立。

### training score 和 evaluation score 要分开读

training data 上的分数和 evaluation data 上的分数，含义并不一样。

| 分数 | 在看什么 | 高就能立刻放心吗？ |
| --- | --- | --- |
| training score | model 对 training data 拟合得有多好 | 不能。它可能只是记住了这些样本 |
| evaluation score | 它在留下来的数据上还能工作到什么程度 | 它比 training score 更接近对新数据表现的估计 |

如果 training score 高，evaluation score 也高，这通常是比较好的信号。如果 training score 很高，但 evaluation score 很低，就说明 model 可能过度贴合 training data。这个问题就叫 overfitting，会在 P4-5 里详细说明。

反过来，如果 training score 和 evaluation score 都低，就可能是 model 还没学够。这会接到 underfitting，同样会在 P4-5 里一起处理。

一个很短的实务型例子，可以这样读。

| model | training score | evaluation score | 先能读出的信号 |
| --- | --- | --- | --- |
| A | 0.98 | 0.62 | 它可能过度贴合了 training data |
| B | 0.81 | 0.79 | 它在新数据上也许相对稳定 |
| C | 0.58 | 0.55 | 它可能还没有学到足够多 |

这张表并不意味着某个固定阈值。它更像是在举例说明：`training score 和 evaluation score 的间隔应该怎么读`，而不是说这些数字必须达到什么标准。

### evaluation data 并不是未来的完美替身

evaluation data 是一种 `模拟尚未见过数据` 的装置。但它并不保证能够完美代表未来。

例如，假设你收集了某个网店从 1 月到 6 月的数据，并把其中一部分留作 evaluation data。这些 evaluation data 展示的是同一大段时期里的客户行为，但它未必能完美代表 11 月大促，或下一年的客户行为。

所以，数据拆分是必要的起点，但不是全部。时间变化、sampling bias、数据收集方式、服务 policy 变化，也都必须一起看。关于样本与偏差的基本感觉，你已经在前面的概率与统计复习段里见过，在机器学习中，它会在 P4-5 和 P4-6 再次接回来。

### 数据少时要更加小心

如果数据足够多，就算留出一部分专门评估，training 侧也通常还会比较充足。但如果数据太小，连 `拆分` 这件事本身都会变难。

数据小时，常见的问题有下面这些。

- training data 太少，model 可能学不好
- evaluation data 太少，分数会大幅波动
- 一次拆分结果可能很受偶然因素影响
- 某个类别或稀有案例可能只落到一边

正因为如此，人们有时会使用 cross-validation。不过，这一节不会完整解释 cross-validation 的做法。当前只要先固定住一点：`数据越小，evaluation score 就越不稳定。` cross-validation 会在 P4-4.2 和 P4-8 再按需要出现。

## 案例与示例

### 案例 1. 在优惠券反应预测里，分数看起来太好时

假设某个营销团队想预测：给客户发优惠券之后，是否真的会带来购买。人一开始先看的信号，是 `最近是否买过东西`、`是否经常访问 App`、`以前是否用过优惠券` 这些。

问题在于：因为数据量不多，团队想直接把整张表同时拿去训练和评估。这样做时，分数看起来可能很好，但很难知道 model 在新客户上是否也会一样有效。它可能只是重新匹配了自己见过的订单记录。

这里，数据拆分会改变判断方式。先把一部分客户记录留给 training，再把另一部分专门留给 evaluation，就能检查 model 在第一次看到的客户记录上是否也有相近表现。也更容易分清：人觉得重要的标准，到底是真正会重复出现的信号，还是只是这张表里偶然显得很强的痕迹。

真正可检查的结果也很明确。只要把 `在整份数据上评估时的分数` 和 `在单独留下来的 evaluation data 上的分数` 并排比较，就能看出有没有明显差距。如果只有 training score 很高，而 evaluation score 掉得很多，就应该把这读成：`没有做数据拆分时，解释过于乐观了。`

```mermaid
--8<-- "assets/part-04/chapter-04/p4-4-1-mermaid-02-zh.mmd"
```

## 案例与示例

### 数据拆分能减少的误解

数据拆分能减少下面这些误解。

| 误解 | 为什么会发生 | 数据拆分带来的帮助 |
| --- | --- | --- |
| model 分数高，所以学得很好 | 只看了 training data 上的分数 | 会在留下来的数据上再次确认 |
| 复杂 model 一定更好 | 它在 training data 上可能更容易拟合 | 会在 evaluation data 上检查这种提升是否真实 |
| 只要有一次好分数就够了 | 这可能只是一次幸运的拆分结果 | 会让你想到多次拆分或 cross-validation 的必要性 |
| 只要数据多就行 | 很容易忽略代表性或收集偏差 | 会连 evaluation data 的组成一起检查 |

数据拆分不是为了故意压低 model 的成绩，而是为了更诚实地阅读成绩。

## 练习与示例

### 小型 Python 练习

这一节暂时不需要真的训练 model。目标是亲手习惯：拆分数据之后，应该优先检查哪些值。

### 练习 1. 改变 `test_size`

下面的代码会用两种比例来拆分同一份数据。它使用客户 feature 列表 `X`、流失 label `y` 和两个 `test_size` 值，确认每种比例下的 training/evaluation 样本数和 `churn` 比例。

要确认的核心是，`test_size` 越大，evaluation data 越多，而 training data 越少。样本数变化和 label 比例变化必须一起看。

```python
# 这个例子把输入特征 X 和目标 y 分成训练集与评估集，并检查标签比例。
from sklearn.model_selection import train_test_split

X = [
    [8, 0],
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
    [3, 2],
    [9, 0],
    [2, 5],
]
y = ["stay", "churn", "stay", "churn", "stay", "churn", "stay", "churn"]

for ratio in [0.25, 0.5]:
    X_train, X_eval, y_train, y_eval = train_test_split(
        X,
        y,
        test_size=ratio,
        random_state=42,
    )

    print("test_size =", ratio)
    print("training sample count:", len(X_train))
    print("evaluation sample count:", len(X_eval))
    print("training churn ratio:", y_train.count("churn") / len(y_train))
    print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
    print("-" * 30)
```

一个示例输出可能会像下面这样。

```text
test_size = 0.25
training sample count: 6
evaluation sample count: 2
training churn ratio: 0.3333333333333333
evaluation churn ratio: 1.0
------------------------------
test_size = 0.5
training sample count: 4
evaluation sample count: 4
training churn ratio: 0.25
evaluation churn ratio: 0.75
------------------------------
```

这个练习里，重点不是分数，而是拆分结果本身。`test_size` 越大，evaluation data 就越多，而 training data 就越少。数据非常小时，这种差别会显得更明显。

### 练习 2. 改变 `random_state`

即使数据相同，只要打乱基准不同，拆分结果也可能不同。下面的例子使用相同的 `X`、`y` 和不同的 `random_state` 值，比较每个 seed 下的 evaluation label 列表和 evaluation data 的 `churn` 比例。

要确认的核心是，`random_state` 是为了复现拆分结果而设置的参考值。在小数据里，就算只改 seed，evaluation 组成也可能大幅波动。

```python
# 这个例子把输入特征 X 和目标 y 分成训练集与评估集，并检查标签比例。
from sklearn.model_selection import train_test_split

X = [
    [8, 0],
    [2, 3],
    [6, 1],
    [1, 4],
    [7, 0],
    [3, 2],
    [9, 0],
    [2, 5],
]
y = ["stay", "churn", "stay", "churn", "stay", "churn", "stay", "churn"]

for seed in [0, 7, 42]:
    X_train, X_eval, y_train, y_eval = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=seed,
    )

    print("random_state =", seed)
    print("evaluation labels:", y_eval)
    print("evaluation churn ratio:", y_eval.count("churn") / len(y_eval))
    print("-" * 30)
```

一个示例输出可能会这样变化。

```text
random_state = 0
evaluation labels: ['stay', 'stay']
evaluation churn ratio: 0.0
------------------------------
random_state = 7
evaluation labels: ['stay', 'churn']
evaluation churn ratio: 0.5
------------------------------
random_state = 42
evaluation labels: ['churn', 'churn']
evaluation churn ratio: 1.0
------------------------------
```

这个练习展示了为什么必须记下 `random_state`。如果希望下次再运行同样代码时还能得到同样的拆分结果，就要把这个参考值固定住。

### 练习 3. 看看当数据偏斜时会出现什么问题

下面这个例子展示的是：当 `churn` 样本本来就很少时，拆分结果会多么容易波动。它会拆分带有稀疏 `churn` label 的 `X`、`y`，并确认 training label 列表、evaluation label 列表以及每一侧的 `churn` 个数。

要确认的核心是，在类别不平衡的数据里，就算只是普通随机拆分，label 分布也很容易波动。这也就是为什么拆分之后要立刻把 label 组成打印出来。

```python
# 这个例子把输入特征 X 和目标 y 分成训练集与评估集，并检查标签比例。
from sklearn.model_selection import train_test_split

X = [[i] for i in range(10)]
y = ["stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "stay", "churn"]

X_train, X_eval, y_train, y_eval = train_test_split(
    X,
    y,
    test_size=0.3,
    random_state=42,
)

print("training labels:", y_train)
print("evaluation labels:", y_eval)
print("training churn count:", y_train.count("churn"))
print("evaluation churn count:", y_eval.count("churn"))
```

一个示例输出可以这样读。

```text
training labels: ['stay', 'stay', 'stay', 'churn', 'stay', 'stay', 'stay']
evaluation labels: ['stay', 'stay', 'stay']
training churn count: 1
evaluation churn count: 0
```

在这个练习里，某一边可能几乎没有 `churn`，甚至完全没有。到了这种状态，model 就会很难学习流失模式，也很难正确评估它们。也正因为这样，下一节才会再次回到 stratified split。

## 检查清单

- 能不能说明为什么同一份数据同时拿来学习和评估时，性能很容易被高估？
- 能不能说明为什么在时间顺序数据和稀有 label 数据里，拆分方式应该不同？
- 能不能区分 training score 和 evaluation score 各自在说明什么？
- 能不能说明 training data 是用来学习的，而 evaluation data 是专门留下来检查 model 学到了什么的？
- 能不能说明 evaluation data 是为了估计 model 在新数据上的行为而准备的代理场景？
- 能不能说明当数据很少时，连 evaluation score 也会波动，所以必须更谨慎地读取？

## 来源与参考资料

- scikit-learn developers, `Cross-validation: evaluating estimator performance`, scikit-learn User Guide, 确认日期：2026-07-19. [https://scikit-learn.org/stable/modules/cross_validation.html](https://scikit-learn.org/stable/modules/cross_validation.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `train_test_split`, scikit-learn API Reference, 确认日期：2026-07-19. [https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html){: target="_blank" rel="noopener noreferrer" }
- Gareth James, Daniela Witten, Trevor Hastie, Robert Tibshirani, Jonathan Taylor, `An Introduction to Statistical Learning`, Springer, 官方网站确认日期：2026-07-19. [https://www.statlearning.com/](https://www.statlearning.com/){: target="_blank" rel="noopener noreferrer" }
