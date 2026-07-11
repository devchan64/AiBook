# P4-11.2 决策边界(decision boundary)

> Section ID: `P4-11.2`
> Version: `v2026.07.11`

在 P4-11.1 里，我们把 logistic regression 看成 `生成可按 probability 来读的 score 的线性模型`。现在要把问题再换一步。

为什么这个 score 会把某些输入读成 class 0，把另一些输入读成 class 1？

要回答这个问题，只问 `probability 是多少` 还不够。还必须看见 `到哪里为止按 class 0 来读，从哪里开始按 class 1 来读`。把这个 기준放回 input space 里来读的视角，就是 decision boundary。

所以，`模型在输入空间里把线画在哪里` 这个说法更接近结果，而不是最根本的意思。更本质的问题是：

模型究竟按什么规则，把输入读成两个不同的区域？

如果说 P4-11.1 是从 output 角度来读，那么 P4-11.2 就是回头看 input 的 Section。

`decision boundary 是把 class 0 和 class 1 分开的 기준线或 기준面。`

这一节不会重新长篇重复 logistic regression 的基本定义。`会生成可按 probability 来读的 score 的线性分类器` 这个核心直觉，会通过 P4-11.1 和 [概念词汇表](../../../reference/concept-glossary.md) 再接回来。这里专注的是：那个 score 怎样切开 input space。

## 本节范围

这一节回答下面这些问题。

- 什么是 decision boundary？
- 在一维输入里，boundary 会怎样出现？
- 在二维输入里，为什么它会像一条线？
- coefficient 和 boundary 的方向有什么关系？
- threshold 改变时，boundary 会怎样改变？

这一节不会深入讲下面这些内容。

- 高维空间里 hyperplane 的严格几何解释
- multiclass classification 的 boundary 划分
- kernel 方法与 nonlinear boundary 的数学展开
- 绘制 boundary 的实现细节

hyperplane 的基础直觉会在 P4-1.2 再接回来，kernel 方法与 nonlinear boundary 会在 P4-13.1、P4-13.2 再处理。像 `C`、`gamma`、threshold 调整这样的设置与计算成本，会在 P4-9.1、P4-9.2 再接回来。multiclass boundary 的细分和 plot 实现细节暂时放在本书当前正文范围之外。

## 本节目标

- 能把 decision boundary 解释成不是 `输出 score`，而是 `切开 input space 的 기준`。
- 能理解在一维时它像 `一个点`，在二维时通常像 `一条线`。
- 能说明 logistic regression 的 coefficient 会参与改变 boundary 的方向。
- 能说明 threshold 改变时，boundary 的解释也可能跟着移动。
- 能把 11.1 的概率输出视角和 11.2 的 boundary 视角，连回成同一个 model 的两种读法。

## 学习背景

### 为什么要单独看 decision boundary

在 11.1 里，我们看到的是 `0.58`、`0.73` 这样的 score。但在学习和实际工作里，下面这些问题常常更重要。

- 某个输入为什么变成了 class 0？
- 某个输入为什么变成了 class 1？
- 两个 class 之间的 기준到底在哪里？

这些问题单靠 output 表并不能充分回答。output 表会告诉你 `结果是什么`，但不够说明 `为什么会得到这个结果`。

这就是必须看 decision boundary 的原因。

- 为了说明某个输入为什么会落到 class 0
- 为了说明某个输入为什么会落到 class 1
- 为了说清楚两个 class 的分界 기준在哪里
- 为了单独识别那些边界附近的模糊案例

所以，decision boundary 不是单纯的可视化装饰，而是一个 `读取分类理由的解释工具`。

当我们必须问 `模型到底是在哪个 기준上把空间切成两边的`，就会出现 decision boundary 这个视角。

而且它还必须和下面四样东西一起看。

| 要一起看的东西 | 为什么需要 |
| --- | --- |
| baseline 分类结果 | 因为还要知道这个线性 boundary 是否真的比简单规则更好 |
| threshold 位置 | 因为即使 score 相同，也要看到 class 到底从哪里开始改变 |
| confusion matrix 里出问题的格子 | 因为需要看这个 boundary 让哪一类错误变多了 |
| 边界附近的代表案例 | 因为必须解释为什么那些模糊输入会跨到另一边 |

所以，这一节不是在学怎样把线画得漂亮，而是在一起读取 `相对什么更好了`、`class 在哪里改变`、`结果造成了什么错误`。

再加上一点，decision boundary 会和运营解释连得更紧。边界附近的案例不是单纯的 `模糊点`，而是应该优先留下来做 review 的对象。也就是说，decision boundary 还可以被读成一个比较框架，用来决定 `哪些输入应该由人再看一遍`。边界附近这个事实本身说明了变化信号和 review 优先级，但并不会自动完成原因解释。

这里也要尽量维持同样的比较框架。应该在相同 baseline、相同 score 区间、相同代表失败案例上看 boundary 前后，才能减少把 `score 变化`、`threshold policy 变化`、`feature 表达不足` 混在一起。

| 看 boundary 时要一起留下的记录 | 为什么需要 |
| --- | --- |
| 边界附近案例 ID | 为了再次找到 review 对象 |
| 相对 baseline 改变的分类结果 | 为了看清相比简单规则到底多分开了哪些案例 |
| threshold 改变后移动的案例 | 为了知道哪些输入是因为 policy 变化而跨线 |
| 下一步检查问题 | 为了决定要补 feature 还是调整 threshold |

## 主要学习内容

### 什么是 decision boundary

分类模型通常会在内部先计算一个 score，再用这个 score 来切 class。decision boundary 就是 `这个 score 刚好等于 기준值的位置`。

如果把 logistic regression 在入门层面上简化，可以先这样想。

\[
z = w_1x_1 + w_2x_2 + \cdots + w_nx_n + b
\]

把这个 linear score \(z\) 放进 sigmoid 后，就会得到 0 到 1 之间的值。如果使用 threshold 0.5，那么 sigmoid 输出等于 0.5 的地方，就成为 class 的边界。

而 sigmoid 输出 0.5，又对应 linear score \(z = 0\)。所以 logistic regression 的 decision boundary 通常可以理解成 `linear score 等于 0 的地方`。

`decision boundary 既是 probability 最模糊的位置，也是 class 开始分开的地方。`

### 一维输入时，boundary 会像一个点

如果输入只有一个，boundary 看起来就不是一条线，而更像 `一个点`。

例如输入只有 `study_hours`，模型就会在某个时间点附近把不及格与及格分开。

| 学习时间 | class 1 分数 | 预测 |
| ---: | ---: | --- |
| 3 | 0.17 | 不及格 |
| 4 | 0.31 | 不及格 |
| 5 | 0.55 | 及格 |
| 6 | 0.76 | 及格 |

在这个例子里，boundary 可以读成 `大约落在 4 小时和 5 小时之间`。所以一维 decision boundary 很接近 `一个 cutoff point`。

这个想法可以简单画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-01-en.mmd"
```

这张图的关键是：随着输入值上升，score 也跟着上升，并且在 `score 0.50` 的边界点附近，把轴分成了 class 0 一侧和 class 1 一侧。

这一点在检查 threshold 时尤其重要。11.1 里像 score 表一样出现的东西，在 11.2 会重新变成 `输入轴上的一个 boundary point`。

### 二维输入时，boundary 会像一条线

现在假设输入有两个，例如 `exam_1` 和 `exam_2`，任务是判断及格还是不及格。此时 input space 会更像一个平面，而不是一张单列表。

- 一个轴是 `exam_1`
- 另一个轴是 `exam_2`
- 每个学生都是平面上的一个点

在这种情况下，logistic regression 会尝试找到一条 기준线，把这些点分成两边。所以在二维里，decision boundary 通常会像 `一条直线`。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-02-en.mmd"
```

这张图展示的是：logistic regression 的 decision boundary 可以被读成 `把 score z 和 0 作比较` 这一条规则，在输入空间里留下的痕迹。重点不是先有一条线，而是因为 linear score 在平面两侧的符号变了，class 也跟着变了。

`输入维度多一个，boundary 就会从一个点变成一条线。`

这里重要的不是 `先有线，再有 class`，而是 `因为规则在比较 z 和 0，所以结果上平面里出现了 boundary line`。

### coefficient 和 boundary 的方向有什么关系

logistic regression 的 coefficient 不只是用来计算 score。从 input space 的角度看，它们还会影响 boundary 朝哪个方向放置。

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

在 11.1 里，我们看到 threshold 改变时最终行为会变。到了 11.2，这句话要从空间视角再读一遍。

threshold 为 0.5 时的 boundary，与 threshold 为 0.7 时的 boundary，不一定在同一个位置。理由很简单。

- threshold 0.5：从 score 达到这个值开始读成 class 1
- threshold 0.7：需要更高的 score 才会读成 class 1

所以，当 threshold 提高时，被分到 class 1 的区域会缩小，boundary 也会向更保守的方向移动。

`模型的 coefficient 决定 boundary 的方向，而 threshold 可以进一步调整 boundary 具体落在哪里。`

这个移动可以概念化地画成下面这样。

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-03-en.mmd"
```

这里的关键是：即使不重新训练 model，只要 threshold 更严格，同一条 score 轴上的有效 boundary 就会向右移动，class 1 区域会被读得更小。所以 boundary 的移动，应该先读成一种 policy change，而不是把 feature 的原因解释已经完成。

在 decision boundary 记录里，最好把下面三句话一起留下。

- 边界附近案例是提高 review 优先级的信号，而不是自动确认。
- threshold 一改，同一个输入也可能变成不同的行为。
- 看到了 boundary 的移动，并不等于原因解释已经完成。

### 什么时候 decision boundary 这个视角特别重要

decision boundary 不是只有在画图时才重要。当你必须问 `为什么这个输入跨到另一个 class 去了` 时，它尤其重要。

| 当前想看的东西 | 为什么需要 decision boundary 视角 | 要一起检查什么 |
| --- | --- | --- |
| 边界附近的模糊案例 | 因为光看 score 不足以说明为什么会分开 | threshold 与 review 区间 |
| 某类误分重复出现 | 因为需要看 boundary 到底朝哪边倾斜 | confusion matrix 里出问题的格子 |
| 正在考虑是否调整 threshold | 因为 policy 变化会让哪些输入跨线，必须在空间里看 | threshold 前后案例变化 |
| 怀疑还需要更多 feature | 因为需要确认当前 boundary 是否过于简单 | 相对 baseline 新分开的案例 |
| 需要选出人工 review 对象 | 因为边界附近案例会决定 review 优先级 | 案例 ID 与 score 区间 |

这张表的目的，不是为了欣赏 boundary 图长得好不好看，而是为了追踪 `分类规则到底在哪里分开、又错过了什么`。

## 案例与示例

在进入具体案例前，可以先把本节的公共比较框架整理成下面这样。

| 场景 | 人最容易先用的 기준 | 这个 기준 的限制 | decision boundary 视角改变的点 | 要确认的结果 |
| --- | --- | --- | --- | --- |
| 合格预测 | 对单一分数设一条合格线 | 多个 feature 一起起作用时解释很弱 | 改成组合型 기준线 | boundary 不再只是一个点，而会变成线或面 |
| 客户流失 | 只看一个变量判断风险 | 会漏掉组合模式 | 看多个 feature 的组合是否形成风险区域 | 说明哪些组合跨过了 boundary |
| 医疗风险 | 用一个数值判断风险 | 会漏掉模糊的组合案例 | 把边界附近案例单独拿出来看 | 识别 review 优先级更高的对象 |
| 贷款 / 垃圾邮件 | 用单一规则解释通过与拦截 | 会漏掉混合特征和线性 boundary 的限制 | 观察 boundary 到底切开了哪些组合 | 同时读取线性 boundary 的优点与限制 |

```mermaid
--8<-- "assets/part-04/chapter-11/p4-11-2-mermaid-04-en.mmd"
```

## 练习与示例

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

这个结果说明：像 `0.62` 这样的分数，从模型角度看已经偏向 class 1，但在更严格的 threshold 下，它仍然可能留在 class 1 区域之外。

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

### 这个练习怎样回收到 Part 4 的目标

这个练习让分类模型不再只是 `算 probability 的机器`，而重新读成 `可以调整 operating boundary 的装置`。Part 4 里重要的，不是单独让某个 score 变高，而是读取当 threshold 改变时，哪些案例会从自动处理移到 review，错误成本又会怎么跟着变化。把同一组 score 只改变 boundary 反复读取，是在训练你把 `model output` 和 `applied judgment` 分开看。

| 通用记录语言 | 这次练习里应立刻留下的内容 |
| --- | --- |
| 看见的结构 | 同一组 score 里，threshold 提高后 class 1 区域缩小，原本自动处理的案例重新回到 review |
| 解释边界 | 更保守的 threshold 不一定就等于更好的 policy，还必须连同 false-negative 成本一起看 |
| 下一步问题 | 当前减少的 false positive 风险，是否真的比增加的 false negative 与 review 成本更重要？ |

## 补充读取点

### 主要争议点通常从哪里出现

decision boundary 看起来像一张简单的图，但读者很常在下面这些点上误解它。

### 1. boundary 是一堵墙吗

不是。decision boundary 不是现实世界里的墙，而是 `model 为了方便而画出的分离 기준`。边界附近的样本，稍微变动就可能跨到另一边。

### 2. 离 boundary 越远，就一定越确定吗

在 logistic regression 里，离 boundary 越远，score 通常会更强烈地偏向某一边 class。但这并不保证现实世界里就一定完全确定。数据质量与分布仍然重要。

### 3. 线性 boundary 一定够用吗

不一定。如果数据呈曲线形混在一起，或 class 结构很复杂，一条直线可能就不够。这正是后面会出现更复杂模型的原因。

### 4. 数据变了，boundary 还会固定吗

不会。训练数据一变，coefficient 和 intercept 就可能改变，boundary 的位置与方向也会跟着变。所以 decision boundary 更接近 `当前数据与 model 共同产生的学习结果`，而不是 `从自然里发现的一条现成的线`。

这一点会直接连到：为什么 train/test split、sample bias、dataset 更新都很重要。

### 5. 为什么边界附近样本要特别看重

离 boundary 很远的样本通常会被更稳定地分类；反过来，边界附近样本很容易因为微小变化而改变 class。

因此在实际服务里，常常会附带下面这样的 policy。

- 离边界远：自动处理
- 边界附近：交给人工 review
- 把边界附近案例单独收集起来做质量检查

也就是说，decision boundary 不只是拿来分 class，还可以用来找出 `哪些案例模糊、哪些案例有更高的运营风险`。

### 6. 好的 boundary 和好的 service 一定是同一回事吗

不一定。从 model 角度看分类很漂亮，也不代表从 service 角度看就是合适的。如果不同 class 的误分类成本不同，那么运营上更安全的 boundary，可能并不是数学上看起来最干净的那条。

这一点会连到 11.1 里的 threshold、Part 4 前半段的评价指标，以及后面的 model selection。

## 本节要记住的视角

- decision boundary 是切开 class 的 기준线或 기준面。
- 在一维里它像一个点，在二维里通常像一条线。
- logistic regression 的 coefficient 与 intercept 会参与决定 boundary 的方向和位置。
- threshold 一改，class 区域与 boundary 的解释也会跟着改变。
- boundary 是把 model 的计算结果放回 input space 里来读的一种方法。

这一节不是在学怎么画线，而是在评价流程里读 boundary。

| 要一起看的东西 | 这一节里先问的问题 | 后面会再接到哪里 |
| --- | --- | --- |
| threshold 位置 | class 到底从哪里开始分开，boundary 有多保守 | P4-6 分类指标，P4-15.3 threshold 调整 |
| confusion matrix 里出问题的格子 | 这个 boundary 到底让 FP 还是 FN 增加得更多 | P4-6 评价指标 |
| 边界附近代表案例与 baseline 比较 | 模糊输入为什么跨线，相比简单规则到底有没有更好 | P4-8 baseline，后续分类算法比较 |

## 检查清单

- 是否不仅在看 output score，也在看 input space 里到底从哪里开始分开？
- 是否把因为 threshold 改变而跨线的案例，与因为 feature 表达不足而预测错误的案例区分开？
- 是否把边界附近案例留作 review 优先级信号，而不是直接自动确认？

## 什么时候要先想起这个视角

- 当分类 score 看得见，但解释不清 input space 到底在哪里分开时，先把 decision boundary 画出来。
- 当你必须解释 threshold 改完以后哪些样本跨到了另一边时，要一起看 boundary 位置与 class 区域变化。
- 当你模糊地觉得线性模型不够用时，要把这一节当成起点，先区分问题到底是出在直线 boundary 本身，还是出在表达不足。

## 与后续章节的连接

P4-11.2 展示了 logistic regression `把线画在哪里`。接下来的问题会继续变化。

- 直线 boundary 够不够？
- 还有哪些分类算法能更好地解释数据？
- 评价指标和 model selection 又是怎样比较这些 boundary 的？

所以，11.2 是读者开始把分类模型看成 `切开空间的装置` 的 Section。这个视角会直接接到后面的 tree、SVM 以及更复杂的分类器。

## 出处与参考资料

- Ronald A. Fisher, `The Use of Multiple Measurements in Taxonomic Problems`, *Annals of Eugenics*, 1936, DOI: [https://doi.org/10.1111/j.1469-1809.1936.tb02137.x](https://doi.org/10.1111/j.1469-1809.1936.tb02137.x){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-29.
- Benyamin Ghojogh, Mark Crowley, `Linear and Quadratic Discriminant Analysis: Tutorial`, arXiv, 2019, [https://arxiv.org/abs/1906.02590](https://arxiv.org/abs/1906.02590){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-29.
- scikit-learn, `1.1.11. Logistic regression`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `LogisticRegression`, scikit-learn API Reference, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html){: target="_blank" rel="noopener noreferrer" }
