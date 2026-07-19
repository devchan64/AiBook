# P4-11.2 决策边界(decision boundary)

> Section ID: `P4-11.2`
> Version: `v2026.07.17`

在 P4-11.1 里，我们把 logistic regression 看成 `生成可按 probability 来读的 score 的线性模型`。
现在要把问题再换一步。

为什么这个 score 会把某些输入读成 class 0，把另一些输入读成 class 1？

要回答这个问题，只问 `probability 是多少` 还不够。
还必须看见 `到哪里为止按 class 0 来读，从哪里开始按 class 1 来读`。
把这个标准放回 input space 里来读的视角，就是 decision boundary。

所以，`模型在输入空间里把线画在哪里` 这个说法更接近结果，而不是最根本的意思。
更本质的问题是：

模型究竟按什么规则，把输入读成两个不同的区域？

如果说 P4-11.1 是从 output 角度来读，那么 P4-11.2 就是回头看 input 的 Section。

`decision boundary 是把 class 0 和 class 1 分开的标准线或标准面。
`

这一节不会重新长篇重复 logistic regression 的基本定义。
`会生成可按 probability 来读的 score 的线性分类器` 这个核心直觉，会通过 P4-11.1 和 [概念词汇表](/AiBook/en/reference/concept-glossary/) 再接回来。
这里专注的是：
那个 score 怎样切开 input space。

## 本节范围

这一节回答下面这些问题。

- 什么是 decision boundary？
- 在一维输入里，boundary 会怎样出现？
- 在二维输入里，为什么它会像一条线？
- coefficient 和 boundary 的方向有什么关系？
- threshold 改变时，boundary 会怎样改变？

这一节先把 decision boundary 收束为 `切分 input space 的标准`，并专注抓住 output score 里出现的 threshold 在 input space 里会怎样被读成 boundary。

同时，后面还要继续扩展的问题也很清楚。hyperplane 的基础直觉会在 P4-1.2 再接回来，kernel 方法与 nonlinear boundary 会在 P4-13.1、P4-13.2 再处理。像 `C`、`gamma`、threshold 调整这样的设置与计算成本，会在 P4-9.1、P4-9.2 再接回来，multiclass 扩展会在 P4-11.4 继续展开。

## 本节目标

- 能把 decision boundary 解释成不是 `输出 score`，而是 `切开 input space 的标准`。
- 能理解在一维时它像 `一个点`，在二维时通常像 `一条线`。
- 能说明 logistic regression 的 coefficient 会参与改变 boundary 的方向。
- 能说明 threshold 改变时，boundary 的解释也可能跟着移动。
- 能把 11.1 的概率输出视角和 11.2 的 boundary 视角，连回成同一个 model 的两种读法。

## 学习背景

### 为什么要单独看 decision boundary

在 11.1 里，我们看到的是 `0.58`、`0.73` 这样的 score。
但在学习和实际工作里，下面这些问题常常更重要。

- 某个输入为什么变成了 class 0？
- 某个输入为什么变成了 class 1？
- 两个 class 之间的标准到底在哪里？

这些问题单靠 output 表并不能充分回答。
output 表会告诉你 `结果是什么`，但不够说明 `为什么会得到这个结果`。

这就是必须看 decision boundary 的原因。

- 为了说明某个输入为什么会落到 class 0
- 为了说明某个输入为什么会落到 class 1
- 为了说清楚两个 class 的分界标准在哪里
- 为了单独识别那些边界附近的模糊案例

所以，decision boundary 不是单纯的可视化装饰，而是一个 `读取分类理由的解释工具`。

当我们必须问 `模型到底是按什么标准把空间切成两边的`，就会出现 decision boundary 这个视角。

而且它还必须和下面四样东西一起看。

| 要一起看的东西 | 为什么需要 |
| --- | --- |
| baseline 分类结果 | 因为还要知道这个线性 boundary 是否真的比简单规则更好 |
| threshold 位置 | 因为即使 score 相同，也要看到 class 到底从哪里开始改变 |
| confusion matrix 里出问题的格子 | 因为需要看这个 boundary 让哪一类错误变多了 |
| 边界附近的代表案例 | 因为必须解释为什么那些模糊输入会跨到另一边 |

所以，这一节不是在学怎样把线画得漂亮，而是在一起读取 `相对什么更好了`、`class 在哪里改变`、`结果造成了什么错误`。

再加上一点，decision boundary 会和运营解释连得更紧。
边界附近的案例不是单纯的 `模糊点`，而是应该优先留下来做 review 的对象。
也就是说，decision boundary 还可以被读成一个比较框架，用来决定 `哪些输入应该由人再看一遍`。
边界附近这个事实本身说明了变化信号和 review 优先级，但并不会自动完成原因解释。

这里也要尽量维持同样的比较框架。
应该在相同 baseline、相同 score 区间、相同代表失败案例上看 boundary 前后，才能减少把 `score 变化`、`threshold policy 变化`、`feature 表达不足` 混在一起。

| 看 boundary 时要一起留下的记录 | 为什么需要 |
| --- | --- |
| 边界附近案例 ID | 为了再次找到 review 对象 |
| 相对 baseline 改变的分类结果 | 为了看清相比简单规则到底多分开了哪些案例 |
| threshold 改变后移动的案例 | 为了知道哪些输入是因为 policy 变化而跨线 |
| 下一步检查问题 | 为了决定要补 feature 还是调整 threshold |

## 主要学习内容

### 什么是 decision boundary

分类模型通常会在内部先计算一个 score，再用这个 score 来切 class。
decision boundary 就是 `这个 score 刚好等于标准值的位置`。

如果把 logistic regression 在入门层面上简化，可以先这样想。

\[
z = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

把这个 linear score \(z\) 放进 sigmoid 后，就会得到 0 到 1 之间的值。
如果使用 threshold 0.5，那么 sigmoid 输出等于 0.5 的地方，就成为 class 的边界。

而 sigmoid 输出 0.5，又对应 linear score \(z = 0\)。
所以 logistic regression 的 decision boundary 通常可以理解成 `linear score 等于 0 的地方`。

`decision boundary 既是 probability 最模糊的位置，也是 class 开始分开的地方。
`

### 一维输入时，boundary 会像一个点

如果输入只有一个，boundary 看起来就不是一条线，而更像 `一个点`。

例如输入只有 `study_hours`，模型就会在某个时间点附近把不及格与及格分开。

| 学习时间 | class 1 分数 | 预测 |
| ---: | ---: | --- |
| 3 | 0.17 | 不及格 |
| 4 | 0.31 | 不及格 |
| 5 | 0.55 | 及格 |
| 6 | 0.76 | 及格 |

在这个例子里，boundary 可以读成 `大约落在 4 小时和 5 小时之间`。
所以一维 decision boundary 很接近 `一个 cutoff point`。

把单变量时的 cutoff point 和双变量时的 boundary line 放进同一张图比较，会更容易抓住这个变化。

![比较一维 cutoff point 与二维 decision boundary line 的图](/AiBook/assets/part-04/chapter-11/p4-11-2-cutoff-boundary-zh.svg)

这个想法可以简单画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-01-zh.mmd"
```

这张图的关键是：
随着输入值上升，score 也跟着上升，并且在 `score 0.50` 的边界点附近，把轴分成了 class 0 一侧和 class 1 一侧。

这一点在检查 threshold 时尤其重要。
11.1 里像 score 表一样出现的东西，在 11.2 会重新变成 `输入轴上的一个 boundary point`。

### 二维输入时，boundary 会像一条线

现在假设输入有两个，例如 `exam_1` 和 `exam_2`，任务是判断及格还是不及格。
此时 input space 会更像一个平面，而不是一张单列表。

- 一个轴是 `exam_1`
- 另一个轴是 `exam_2`
- 每个学生都是平面上的一个点

在这种情况下，logistic regression 会尝试找到一条标准线，把这些点分成两边。
所以在二维里，decision boundary 通常会像 `一条直线`。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-02-zh.mmd"
```

这张图展示的是：
logistic regression 的 decision boundary 可以被读成 `把 score z 和 0 作比较` 这一条规则，在输入空间里留下的痕迹。
重点不是先有一条线，而是因为 linear score 在平面两侧的符号变了，class 也跟着变了。

`输入维度多一个，boundary 就会从一个点变成一条线。
`

这里重要的不是 `先有线，再有 class`，而是 `因为规则在比较 z 和 0，所以结果上平面里出现了 boundary line`。

### coefficient 和 boundary 的方向有什么关系

logistic regression 的 coefficient 不只是用来计算 score。
从 input space 的角度看，它们还会影响 boundary 朝哪个方向放置。

如果有两个 feature，

\[
z = w_1x_1 + w_2x_2 + b
\]

那么 \(w_1\) 与 \(w_2\) 的相对大小和符号，就会改变 boundary line 的斜率和方向。

这里比起公式推导，更重要的是下面这些感觉。

- 某个 feature 的 coefficient 变大时，对应轴的影响可能会更强。
- 两个 coefficient 的组合一变，切 class 的 boundary 倾斜方向也会变。
- intercept 会让 boundary 平行移动。

所以在 11.1 里，coefficient 是 `制造 score 的数字`；到了 11.2，它也会重新读成 `决定 boundary 的数字`。

### threshold 改变时，boundary 也可能移动

在 11.1 里，我们看到 threshold 改变时最终行为会变。
到了 11.2，这句话要从空间视角再读一遍。

threshold 为 0.5 时的 boundary，与 threshold 为 0.7 时的 boundary，不一定在同一个位置。
理由很简单。

- threshold 0.5：从 score 达到这个值开始读成 class 1
- threshold 0.7：需要更高的 score 才会读成 class 1

所以，当 threshold 提高时，被分到 class 1 的区域会缩小，boundary 也会向更保守的方向移动。

`模型的 coefficient 决定 boundary 的方向，而 threshold 可以进一步调整 boundary 具体落在哪里。
`

把同一组 score 只改 threshold 时，score 轴上的 cutoff 移动会怎样在输入空间里变成 `class 1 区域缩小`，放到坐标型比较里可以像下面这样看。

![展示同一条分数轴上把 threshold 从 0.5 提高到 0.7 后，class 1 区域缩小的比较图](/AiBook/assets/part-04/chapter-11/p4-11-2-threshold-shift-zh.png)

这个移动可以概念化地画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-03-zh.mmd"
```

这里的关键是：
即使不重新训练 model，只要 threshold 更严格，同一条 score 轴上的有效 boundary 就会向右移动，class 1 区域会被读得更小。
所以 boundary 的移动，应该先读成一种 policy change，而不是把 feature 的原因解释已经完成。

在 decision boundary 记录里，最好把下面三句话一起留下。

- 边界附近案例是提高 review 优先级的信号，而不是自动确认。
- threshold 一改，同一个输入也可能变成不同的行为。
- 看到了 boundary 的移动，并不等于原因解释已经完成。

### 什么时候 decision boundary 这个视角特别重要

decision boundary 不是只有在画图时才重要。
当你必须问 `为什么这个输入跨到另一个 class 去了` 时，它尤其重要。

| 当前想看的东西 | 为什么需要 decision boundary 视角 | 要一起检查什么 |
| --- | --- | --- |
| 边界附近的模糊案例 | 因为光看 score 不足以说明为什么会分开 | threshold 与 review 区间 |
| 某类误分重复出现 | 因为需要看 boundary 到底朝哪边倾斜 | confusion matrix 里出问题的格子 |
| 正在考虑是否调整 threshold | 因为 policy 变化会让哪些输入跨线，必须在空间里看 | threshold 前后案例变化 |
| 怀疑还需要更多 feature | 因为需要确认当前 boundary 是否过于简单 | 相对 baseline 新分开的案例 |
| 需要选出人工 review 对象 | 因为边界附近案例会决定 review 优先级 | 案例 ID 与 score 区间 |

这张表的目的，不是为了欣赏 boundary 图长得好不好看，而是为了追踪 `分类规则到底在哪里分开、又错过了什么`。

## 补充读取点

### 历史背景与阅读流向

下面两个视角不是不同的模型，而是同一个模型的两种读法。

- 11.1 的视角：logistic regression 会生成可按 probability 来读的 score
- 11.2 的视角：logistic regression 会在 input space 里画出 boundary，并用它把 class 分开

在现代机器学习里，decision boundary 视角之所以重要，也很明显。
后面会出现的 SVM、decision tree、neural network，最终都可以再读回同一个问题：
`model 到底怎样切开 input space？
`

`classification 既是一个算 score 的问题，同时也是一个怎样切开 input space 的问题。
`

## 案例与示例

在进入具体案例前，可以先把本节的公共比较框架整理成下面这样。

| 场景 | 人最容易先用的标准 | 这个标准的限制 | decision boundary 视角改变的点 | 要确认的结果 |
| --- | --- | --- | --- | --- |
| 合格预测 | 对单一分数设一条合格线 | 多个 feature 一起起作用时解释很弱 | 改成组合型标准线 | boundary 不再只是一个点，而会变成线或面 |
| 客户流失 | 只看一个变量判断风险 | 会漏掉组合模式 | 看多个 feature 的组合是否形成风险区域 | 说明哪些组合跨过了 boundary |
| 医疗风险 | 用一个数值判断风险 | 会漏掉模糊的组合案例 | 把边界附近案例单独拿出来看 | 识别 review 优先级更高的对象 |
| 贷款 / 垃圾邮件 | 用单一规则解释通过与拦截 | 会漏掉混合特征和线性 boundary 的限制 | 观察 boundary 到底切开了哪些组合 | 同时读取线性 boundary 的优点与限制 |

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-04-zh.mmd"
```

### 案例 1. 合格预测

如果只有一个分数，一个 cutoff point 就会成为 boundary。
但如果变成两个科目，就会出现像 `数学高、英语低` 这样的抵消关系。
此时，比起只看单科，更适合用把两个分数一起读进去的 boundary line。

| 学生 | 数学分数 | 英语分数 | boundary 解释 |
| --- | ---: | ---: | --- |
| A | 92 | 38 | 一科很高，但另一科较低，可能仍然停留在边界附近 |
| B | 71 | 68 | 两科都在中等以上，更容易跨到及格一侧 |
| C | 45 | 44 | 两科都低，更可能留在不及格一侧 |

这张表的关键是，像 `数学是否超过 90 分` 这样的单一规则，并不足以解释 A 和 B 的差别。
decision boundary 视角会迫使读者去看：
`两个分数的组合到底落在哪一边。
`

### 案例 2. 客户流失预测

| 客户 | 最近 30 天登录天数 | 最近 30 天支付次数 | 咨询次数 | boundary 解释 |
| --- | ---: | ---: | ---: | --- |
| A | 22 | 3 | 0 | 更可能留在留存区域 |
| B | 11 | 1 | 2 | 很容易被读成边界附近的 review 对象 |
| C | 4 | 0 | 4 | 容易被读成已经跨入风险区域 |

这里最重要的是 B。
只看登录天数，它还不算极低；但如果支付频率下降、咨询上升一起出现，这个样本就可能变成边界附近案例。

### 案例 3. 医疗风险分类

| 患者 | 血压 | 血糖 | 年龄 | boundary 解释 |
| --- | ---: | ---: | ---: | --- |
| P1 | 正常 | 正常 | 34 | 离风险区域较远 |
| P2 | 略高 | 接近边界值 | 58 | 作为边界附近案例，可能需要追加检查 |
| P3 | 高 | 高 | 67 | 容易被读成已经跨入风险区域 |

这说明 `边界附近患者` 为什么特别重要。
实际决策里，比起一个分数明显很高的患者，多个指标模糊地堆在边界附近的患者，往往更难判断。

### 案例 4. 贷款审核

| 申请人 | 收入 | 负债率 | 逾期记录 | boundary 解释 |
| --- | --- | --- | --- | --- |
| D1 | 高 | 低 | 无 | 容易被读在批准一侧 |
| D2 | 中等 | 高 | 无 | 可能在边界附近，需要补充材料复核 |
| D3 | 低 | 高 | 有 | 容易被读成已跨入拒绝一侧 |

重要的是，现实里确实存在很多不能用一个标准解释完的申请人。
收入可以高，但负债率也高；工作年限可以短，但没有逾期记录。

### 案例 5. 垃圾邮件与正常邮件的分离

| 邮件 | 链接数 | 发件人是否异常 | 标题表达 | boundary 解释 |
| --- | ---: | --- | --- | --- |
| M1 | 0 | 否 | 普通工作标题 | 接近正常区域 |
| M2 | 2 | 否 | 有夸张表达 | 可作为边界附近案例交给人工 review |
| M3 | 5 | 是 | 反复夸张措辞 | 容易被读成已跨入垃圾区域 |

这个案例也同时展示了 linear boundary 的优点与限制。
简单分离很快，也容易解释；但现实中的垃圾邮件形式非常混杂，一条直线未必足够。

## 练习与示例

### Python 例子：读取一个二维 decision boundary

这个例子是一个很小的二元分类练习：
用两门考试分数 `exam_1`、`exam_2` 去分类学生是否 `passed`。

| 输入组 | 含义 |
| --- | --- |
| `X` | 由两门分数组成的二维输入 |
| `y` | 通过 / 未通过标签 |
| `samples` | 用来观察边界下方、边界附近、边界上方的样本 |

```python
import numpy as np
from sklearn.linear_model import LogisticRegression

X = np.array([
    [35, 40],
    [40, 45],
    [45, 35],
    [55, 60],
    [60, 55],
    [65, 70],
    [50, 52],
    [48, 46],
])
y = np.array([0, 0, 0, 1, 1, 1, 1, 0])

model = LogisticRegression()
model.fit(X, y)

samples = np.array([
    [42, 42],
    [50, 50],
    [62, 60],
])

print("coef            :", np.round(model.coef_[0], 3))
print("intercept       :", round(model.intercept_[0], 3))
print("decision score  :", np.round(model.decision_function(samples), 3))
print("predict_proba   :", np.round(model.predict_proba(samples), 3))
print("prediction      :", model.predict(samples))
```

示例输出如下。

```text
coef            : [0.518 0.471]
intercept       : -48.263
decision score  : [-4.102  0.187 12.979]
predict_proba   : [[0.984 0.016]
                   [0.453 0.547]
                   [0.    1.   ]]
prediction      : [0 1 1]
```

| 样本 | 输入 | decision score \(z\) | 与 boundary \(z = 0\) 的关系 | 预测 |
| --- | --- | ---: | --- | --- |
| A | `[42, 42]` | -4.102 | 低于 boundary | class 0 |
| B | `[50, 50]` | 0.187 | 刚好在 boundary 上方 | class 1 |
| C | `[62, 60]` | 12.979 | 明显高于 boundary | class 1 |

在实际运营里，这种读法会直接继续下去。

- 离 boundary 很远的样本，更容易作为自动处理候选
- 离 boundary 很近的样本，更容易被单独划成 review 对象
- 所以 decision boundary 不只是一个图，也会连到寻找模糊案例的运营标准

### Python 例子：同一组 score，在两个 threshold 下分别怎么读

```python
import numpy as np

proba_class_1 = np.array([0.48, 0.62, 0.81])

pred_05 = (proba_class_1 >= 0.5).astype(int)
pred_07 = (proba_class_1 >= 0.7).astype(int)

print("class 1 scores  :", proba_class_1)
print("threshold 0.5   :", pred_05)
print("threshold 0.7   :", pred_07)
```

示例输出如下。

```text
class 1 scores  : [0.48 0.62 0.81]
threshold 0.5   : [0 1 1]
threshold 0.7   : [0 0 1]
```

这个结果说明：
像 `0.62` 这样的分数，从模型角度看已经偏向 class 1，但在更严格的 threshold 下，它仍然可能留在 class 1 区域之外。

### 再改一个值：如果 threshold 继续升高，什么保持不变，什么会改变

现在保持同样的 score 数组，把 threshold 再提高到 `0.9`。

```python
import numpy as np

proba_class_1 = np.array([0.48, 0.62, 0.81])

pred_07 = (proba_class_1 >= 0.7).astype(int)
pred_09 = (proba_class_1 >= 0.9).astype(int)

print("class 1 scores  :", proba_class_1)
print("threshold 0.7   :", pred_07)
print("threshold 0.9   :", pred_09)
```

示例输出如下。

```text
class 1 scores  : [0.48 0.62 0.81]
threshold 0.7   : [0 0 1]
threshold 0.9   : [0 0 0]
```

### 什么保持了不变，什么发生了改变

- 保持不变的点：score 的相对顺序没有变。`0.81` 仍然最接近 class 1，`0.48` 仍然最远。
- 发生变化的点：threshold 再提高以后，原本看起来已经比较确定的 `0.81` 也不再自动进入 class 1。
- 首先要留下的判断：score 本身和最终行为不是同一个阶段。并不只是边界附近案例会受影响，原本看起来比较确定的案例，也可能因为 operating criterion 的改变重新回到 review 对象里。

## 细部学习内容补充

### 主要争议点通常从哪里出现

decision boundary 看起来像一张简单的图，但读者很常在下面这些点上误解它。

### 1. boundary 是一堵墙吗

不是。
decision boundary 不是现实世界里的墙，而是 `model 为了方便而画出的分离标准`。
边界附近的样本，稍微变动就可能跨到另一边。

### 2. 离 boundary 越远，就一定越确定吗

在 logistic regression 里，离 boundary 越远，score 通常会更强烈地偏向某一边 class。
但这并不保证现实世界里就一定完全确定。
数据质量与分布仍然重要。

### 3. 线性 boundary 一定够用吗

不一定。
如果数据呈曲线形混在一起，或 class 结构很复杂，一条直线可能就不够。
这正是后面会出现更复杂模型的原因。

### 4. 数据变了，boundary 还会固定吗

不会。
训练数据一变，coefficient 和 intercept 就可能改变，boundary 的位置与方向也会跟着变。
所以 decision boundary 更接近 `当前数据与 model 共同产生的学习结果`，而不是 `从自然里发现的一条现成的线`。

这一点会直接连到：
为什么 train/test split、sample bias、dataset 更新都很重要。

### 5. 为什么边界附近样本要特别看重

离 boundary 很远的样本通常会被更稳定地分类；反过来，边界附近样本很容易因为微小变化而改变 class。

因此在实际服务里，常常会附带下面这样的 policy。

- 离边界远：自动处理
- 边界附近：交给人工 review
- 把边界附近案例单独收集起来做质量检查

也就是说，decision boundary 不只是拿来分 class，还可以用来找出 `哪些案例模糊、哪些案例有更高的运营风险`。

### 6. 好的 boundary 和好的 service 一定是同一回事吗

不一定。
从 model 角度看分类很漂亮，也不代表从 service 角度看就是合适的。
如果不同 class 的误分类成本不同，那么运营上更安全的 boundary，可能并不是数学上看起来最干净的那条。

这一点会连到 11.1 里的 threshold、Part 4 前半段的评价指标，以及后面的 model selection。

## 检查清单

- 是否不仅在看 output score，也在看 input space 里到底从哪里开始分开？
- 是否把因为 threshold 改变而跨线的案例，与因为 feature 表达不足而预测错误的案例区分开？
- 是否把边界附近案例留作 review 优先级信号，而不是直接自动确认？
- 能不能说明 decision boundary 不是图形装饰，而是读取分类规则在哪里翻转的方法？
- 能不能说明 coefficient 与 intercept 会塑造 boundary 的方向与位置，而 threshold 会移动真正应用的标准？
- 能不能说明边界附近案例之所以重要，不是因为它们自动证明了原因，而是因为它们会变成 review 优先级信号？

## 出处与参考资料

- Ronald A. Fisher, `The Use of Multiple Measurements in Taxonomic Problems`, *Annals of Eugenics*, 1936, DOI: [https://doi.org/10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-29.
- Benyamin Ghojogh, Mark Crowley, `Linear and Quadratic Discriminant Analysis: Tutorial`, arXiv, 2019, [https://arxiv.org/abs/1906.02590](https://arxiv.org/abs/1906.02590){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-29.
- scikit-learn, `1.1.11. Logistic regression`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `LogisticRegression`, scikit-learn API Reference, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }
