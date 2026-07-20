# P4-9.1 超参数(hyperparameter)

> Section ID: `P4-9.1`
> Version: `v2026.07.20`

在 P4-8 里，我们选好了 model 候选，也用 baseline 立好了比较的出发点。现在要进入下一个问题。

即使是同一个 model 家族，也应该用什么配置值来训练？

这个问题，正是 hyperparameter 的出发点。

人们常常把 hyperparameter 理解成 `复杂的高级选项`。但实际上，它是一个更基础得多的概念。hyperparameter 是人在模型开始学习之前，先从外部设好的配置值。也就是说，它不是 model 从数据里自己学出来的值，而是从外部决定“它要怎样学”的值。

scikit-learn 文档把 hyperparameter 解释成 `不会在 estimator 内部直接学出来的 parameter`。同一份文档还说明，这些值会在建立 estimator 时以构造参数的形式传入。

hyperparameter 不是 model 会学到的规则本身，而是预先决定这个 model 要以什么形状、什么强度去学习的值。

这一节会说明 `超参数(hyperparameter)`、`学出来的值和预先固定的值之间的区分`、以及 `配置值会怎样影响比较实验`。后面的章节会沿着这个抓手继续当前语境，而从 model 外部先固定的配置值到底是什么意思，也会通过这一节和 [概念词汇表](/AiBook/en/reference/concept-glossary/) 再接回来。

最先要分清的标准是下面这个。

| 当前看到的值 | 先抛的问题 |
| --- | --- |
| 权重(weight)、截距(intercept) | `这个值是从数据里学出来的吗？` |
| `max_depth`, `n_neighbors`, `C` | `这个值是在训练前由人先定下来的吗？` |
| `random_state` | `这个值更偏向实验复现，而不是直接追求性能吗？` |

## 本节范围

这一节回答下面这些问题。

- 什么是 hyperparameter？
- 会在学习中改变的值，和人在外部先定好的值，到底有什么不同？
- 为什么即使是同一个算法，也会因为 hyperparameter 而看起来完全不同？
- 读者第一次应该先分清哪些代表性 hyperparameter？

这一节先收束 `怎样区分学习中得到的值和由人先固定的配置值`。GridSearchCV 和 RandomizedSearchCV 的基本比较，以及验证成本，会在下一节 P4-9.2 直接接着讲；高级 search space 设计和分布式实验管理，则会在 P4-9.3 补充学习里再整理。

## 用超参数(hyperparameter)留下的判断标准

- 能把 hyperparameter 解释成 `学习开始前先固定的配置值`。
- 能区分 model parameter 和 hyperparameter。
- 能说明即使是同一个算法，也会因为 hyperparameter 的值不同，而在复杂度、泛化、计算成本上表现不同。
- 能理解为什么下一节需要一个独立任务叫 tuning。

## 学习背景

走到 P4-8.2 之后，读者很容易产生这样的误解。

`候选 model 既然已经选好了，后面比较不是就会自动开始吗？`

但实际并不是这样。因为即使在同一个算法名字下面，也藏着很多配置。

- 决策树(decision tree)必须先决定能长多深。
- k-NN 必须先决定要看多少个邻居。
- 逻辑回归(logistic regression)必须先决定 regularization 要压得多强。

也就是说，如果 model selection 是在决定 `要测试哪个家族`，那么 hyperparameter 就是在决定 `这个家族要用什么设置去测试`。

| 课程位置 | 本节的作用 |
| --- | --- |
| 在 P4-8 模型选择之后 | 让读者理解同一 model 家族内部的设置差异 |
| 在 P4-9.2 调优之前 | 让读者先准备好理解为什么会出现搜索成本和验证成本 |
| 在 P4-10 之后算法章节之前 | 让读者先熟悉那些会在各算法章节里重复出现的配置值名字 |

也就是说，这一节是从 `知道 model 名字` 走向 `会读 model 设置` 的入口。

这里必须固定住的连接是下面这样。

| 紧接着前一步 | 现在新比较的是什么 | 后面还会再确认什么 |
| --- | --- | --- |
| 用 baseline 立起出发点分数 | 看同一个算法内部，哪些配置值会改变它的性格 | 看哪些设置变化会连着错误案例和验证分数一起改变 |

也就是说，baseline 决定的是 `要拿什么去比较`，而 hyperparameter 决定的是 `在同一个 model 名字里，到底要改什么、改多少`。只有把这个标准立住，后面的 tuning 才会被读成 `可比较的实验设计`，而不是简单地乱调选项。

## 主要学习内容

### parameter 和 hyperparameter 到底有什么不同

最先必须分清的是下面这一点。

| 区分 | 谁来决定 | 例子 |
| --- | --- | --- |
| model parameter | 在学习过程中由数据决定 | 线性回归的权重(weight)、截距(intercept) |
| hyperparameter | 在训练前由人决定 | `max_depth`, `n_neighbors`, `C` |

这个区分会在整个机器学习里反复出现。

- parameter 是 model 通过学习 `得到的值`
- hyperparameter 是人在实验设计里 `先放进去的值`

如果把这个差别画得非常短，就是下面这样。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-1-mermaid-01-zh.mmd"
```

这张图的核心是：`hyperparameter 是学习的输入`，而 `parameter 是学习的结果`。

把读者最容易混淆的实际句子改写一下，就是下面这样。

- 不能说 `model 学会了 depth`。
- 更准确的说法是 `人先定下 depth，然后树在这个条件下去学习`。

只要抓住这个差别，后面的 tuning 章节也会变得更清楚。

### 为什么即使是同一个算法，也会因为设置不同而改变

hyperparameter 不只是一个选项名字，它可以改变 model 看待数据的方式本身。

例如，考虑决策树(decision tree)。

- 如果 `max_depth=1`，它只能建立很浅的规则。
- 如果 `max_depth=10`，它就能建立更复杂得多的规则。

两者都叫决策树，但实际运行时，很可能像完全不同性格的 model。

这个差别可以整理成下面这样。

| hyperparameter 变化 | 经常跟着变化的东西 |
| --- | --- |
| model 复杂度(complexity) | 它会拟合得多细 |
| 泛化(generalization) | 它在新数据上能不能撑住 |
| 计算成本(computational cost) | 训练和预测要花多少时间 |
| 结果可解释性(interpretability) | 人是否容易读懂 |

也就是说，hyperparameter 是改变 model `性格` 的手柄。

如果把它再压缩成给读者的一句话，可以记成下面这样。

`hyperparameter 是在同一个 model 名字内部，改变 model 性格的旋钮。`

### 经常遇到的 hyperparameter 例子

与其去背每个算法的全部设置，不如先看“哪些类型的设置会反复出现”。

| model 家族 | 代表 hyperparameter | 给读者的问题 |
| --- | --- | --- |
| 决策树(decision tree) | `max_depth` | 树到底允许长到多深？ |
| k-NN | `n_neighbors` | 要看多少个邻居再做判断？ |
| 逻辑回归(logistic regression) | `C` | regularization 要多弱或多强？ |
| 随机森林(random forest) | `n_estimators` | 要组合多少棵树？ |
| SVM | `kernel`, `C`, `gamma` | 要形成什么边界、对变化多敏感？ |

这张表的目的不是讲细节公式，而是帮助读者建立这样一种感觉：`即使 hyperparameter 名字不同，它们最终也常常是在调复杂度、敏感度、regularization 强度、计算量。`

也就是说，前面说的那个 `改变性格的手柄`，在实际里就是以这些名字出现。从这里开始，核心问题就变成：到底应该先怀疑哪些设置值。

### 第一次应该先怀疑哪些 hyperparameter

第一次看 hyperparameter 时，比起把名字全背下来，更重要的是先看：`这个值到底在改变 model 的哪种性格`。

| 当前看到的设置 | 先读的轴 | 为什么先看它 |
| --- | --- | --- |
| `max_depth`, `min_samples_leaf` | model 复杂度 | 因为它们会立刻摇动过拟合和规则深度 |
| `n_neighbors` | 局部性 / 平滑性 | 因为它会改变是看窄一些还是宽一些的邻域 |
| `C`, `alpha` | regularization 强度 | 因为它们会直接调节“过度贴合”和“泛化” |
| `n_estimators` | 计算量和稳定性 | 因为性能可能上升，但时间和资源成本也会一起增加 |
| `random_state` | 可复现性 | 因为它首先固定的是实验能否重复，而不是性能 |

这张表的目的，不是替代按算法细讲的公式，而是让读者快速读懂：`现在在改的这个值，到底是 model 的哪个手柄`。

`为什么这类设置值会从很早以前就被当成一个单独问题来讲？`

这个问题很重要，因为如果读者只把 hyperparameter 看成一个选项表，就很容易误以为它只是 `需要时再逐个调一调的值`。而实际上，这些值会一起摇动比较公平性、泛化和计算成本。

## 细部学习内容

### 为什么 hyperparameter 会成为单独主题

如果非常粗略地总结 hyperparameter 的历史背景，大概可以写成下面这个流程。

1. 最初，研究者和实务人员主要靠经验手动调值。
2. 后来，人们广泛使用预先列出候选表、逐个全部试过的 grid search。
3. 随着 model 和数据越来越复杂，hyperparameter search 本身也成了一个独立研究主题。

Marc Claesen 和 Bart De Moor 的综述论文说明，很多学习算法都带有必须在训练前决定的 hyperparameter，而这些值的选择会大幅影响性能。同一篇论文也总结说，在很长一段实务时期里，hyperparameter search 主要围绕 manual search、经验规则(rules of thumb)、grid search 来进行。

如果把这个说明换回正文的叙述流，可以整理成下面这样。

`在机器学习里，长久以来，影响结果的不只是算法本身，还有这些算法的设置值到底调得怎么样。`

James Bergstra、Daniel Yamins、David Cox 在 2012 年的论文里指出，很多计算机视觉算法依赖多种设置值，而这些设置该怎么调，常常虽然被当成附属工作，实际上却可能决定性能评估结果。这篇论文还进一步说明，有时很难分清：一个方法到底是真的更好，还是只是调得更好。

这里的重要信息是下面几点。

- hyperparameter 不是最近突然加上去的选项。
- 很早以前，它就已经是 `让算法比较变得不公平的重要因素`。
- 所以，hyperparameter search 越来越需要被当成 `可复现的流程` 来处理，而不是靠个人感觉。

也就是说，hyperparameter 的历史，不该读成 `选项变多了`，而要读成 `让 model 比较更公平的需要变大了`。

`hyperparameter 难，不是因为名字多，而是因为即使同一个 model，只要设置变了，结果就可能完全不同。`

## 案例及示例

### 案例 1. 为什么明明都是同一个决策树，结果却一直不同

一个运营团队在做客户流失预测实验时，把决策树列成了候选。人们最先看的标准，是 `最近访问次数`、`咨询次数`、`是否支付失败` 这样的行为信号。

但即使都说自己试的是同一个决策树，团队成员得到的结果还是会有些不同。一边用的是浅树，所以规则简单，但分数低；另一边把深度开得很大，训练分数很高，但验证分数变得摇晃。这里的问题不是 `算法不同`，而是 `同一个算法的设置值不同`。

在这个场景里，hyperparameter 应该被读成一种“从 model 外部先固定好的手柄”。如果把 `max_depth` 设得小，就只允许简单规则；如果设得大，就允许更复杂的规则。也就是说，数据决定决策树学到什么，但它能复杂到什么程度，是人先决定的。

可确认的结果，会在同时查看 train 分数和 validation 分数时出现。只要比较不同 depth 下训练分数和验证分数是怎样变化的，就能说明：为什么 hyperparameter 不是简单选项，而是改变 model 性格的设置。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-1-mermaid-02-zh.mmd"
```

只讲历史说明，感觉可能还是不够直接。实际上，hyperparameter 不是 `附加选项`，而是会强烈摇动结果的因素，这一点在很多案例里反复被观察到。

#### 案例 1. 在计算机视觉里，即使同一家族也会因为调参而让比较摇晃

Bergstra、Yamins、Cox 2012 年的论文说明，很多计算机视觉算法依赖多种设置值，而这些设置调得怎样，会决定人们如何评估这个算法的潜力。该论文使用自动化 model search 流程，在人脸验证(LFW)、人脸识别(PubFig83)、物体识别(CIFAR-10)等三个不同任务上报告了强结果。

这个案例的重要之处很简单。

- 只说 `哪个算法更好` 还不够。
- 即使是同一个算法家族，只要设置不同，看起来就可能完全不在一个层次。
- 所以，很难把“算法比较”和“hyperparameter 比较”彻底拆开。

#### 案例 2. grid search 并不总是高效

Bergstra 和 Bengio 2012 年的 JMLR 论文说明，在 hyperparameter 空间里，真正强烈影响性能的值，往往只有少数几个。论文展示了：在这种情况下，random search 可能比 grid search 更高效。

- 把所有轴都按相同间距密密地扫一遍，并不总是好方法。
- 实际上，往往只有少数重要 hyperparameter 会强烈摇动结果，而其他值没那么重要。
- 所以，重要的已经不再是 `跑了很多次`，而是 `在什么空间里、用什么方式看`。

也就是说，hyperparameter 问题逐渐发展成了：不只是“多试几个值”，而是 `如何设计搜索方法本身`。

#### 案例 3. 本节的小决策树例子也显示了同样现象

上面的 Python 小例子虽然只是玩具实验，但它已经直接显示了 hyperparameter 的实证意义。

- 在 `max_depth=1` 时，train 和 test 分数都低。
- 在 `max_depth=3` 时，train 分数和 test 分数一起上升。
- 在 `max_depth=None` 时，train 分数最高，但 test 分数反而可能变弱。

光是这个小例子，就已经能看到 hyperparameter 会同时摇动下面三件事。

| 观察 | 含义 |
| --- | --- |
| train 分数上升 | model 更贴近训练数据 |
| test 分数停滞或下降 | 泛化并不会总是一起变好 |
| 同一个算法，不同结果 | 设置值本身也成了比较对象 |

也就是说，hyperparameter 的历史并不只是某个宏大独立领域的历史。它本来就是在小练习里也会立刻出现的问题，而随着这个问题变大，它才成为研究和实务的共同主题。

### 为什么 hyperparameter 必须由人来直接决定

scikit-learn 的 hyperparameter tuning 文档说明，因为这些值不会在 estimator 内部直接学出来，所以可以也应该基于交叉验证(cross-validation)分数来搜索这些值。这个说明可以直接压缩成下面这句话。

`因为数据不会自己告诉你 hyperparameter，所以只能试多个值，再通过验证分数比较。`

也就是说，即使数据会直接让 model 学出 parameter，hyperparameter 往往还是必须 `通过实验` 才能选出来。

在这里，真正重要的就是搜索范围这个问题：`到底要试哪些值，要试到什么程度。`

`到底要试哪些值，要试到什么程度？`

这个问题，就是 tuning。

### 为什么在实务里不能随便不断增加 hyperparameter 调整

人们常常会觉得：hyperparameter 调得越多，性能就会一直更好。但实际上，反方向的风险同样很大。

- 实验次数可能会急剧增加。
- 如果老是盯着验证数据看，就可能过拟合到验证集。
- 某个“碰巧看起来不错”的设置，可能会被误判成 `真实改进`。

scikit-learn 的 common pitfalls 文档说明，如果 test data 被卷入 model selection，性能估计就可能显得过于乐观。这种风险不仅在预处理里出现，在 hyperparameter 选择里也会朝同一个方向出现。也就是说，如果你是看着 test 数据来选设置，那你做的可能不是 `把 model 做好`，而是 `把它调到 test 上去了`。

在实务里，下面这些规则很重要。

1. 先分开 train 和 test。
2. hyperparameter 比较要在 train 内部的验证流程里做。
3. test 只保留到最后确认时再看。

这一节先把这个原则固定成基线规则，实际搜索方法会在下一节处理。

### 用一个小例子先抓感觉

即使是同一个决策树，如果给它不同的深度，会发生什么？

下面是一个非常小的玩具例子。

| 设置 | 读者直觉 |
| --- | --- |
| `max_depth=1` | 只允许非常简单的规则 |
| `max_depth=3` | 允许稍微更复杂的规则 |
| `max_depth=None` | 在停止条件到来之前可以一直继续变深 |

光看这张表，就已经能感受到：hyperparameter 不改变 `model 类型`，却会改变 `model 的行为范围`。

也就是说，这一节里读者应该抓住的感觉是下面这些。

- 即使 model 名字相同，只要设置不同，比较结果就可能不同。
- 所以，只写 `用了什么 model` 并不够。
- 还必须写下 `用了什么设置`，实验才会重新变得可读。

## 练习与示例

### 用 Python 例子看 hyperparameter 差异

下面这个例子只改变同一个决策树算法里的 `max_depth`，用来观察训练结果会怎样变化。

- 问题场景: 把花数据(iris)当成品种分类(classification)问题。
- 输入(input): 萼片长度、宽度、花瓣长度、宽度四个特征(feature)。
- 正答(label): 三个品种(class)。
- 要确认的概念: 即使是同一个算法，只要 hyperparameter 改了，train 分数和 test 分数就可能改变。

```python
# 这个例子用 Iris 数据比较超参数设置如何改变模型性能和性质。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for depth in [1, 3, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)

    print(f"max_depth={depth}")
    print("  train accuracy:", round(train_score, 3))
    print("  test accuracy :", round(test_score, 3))
    print("  tree depth    :", model.get_depth())
    print()
```

执行结果示例如下。

```text
max_depth=1
  train accuracy: 0.667
  test accuracy : 0.667
  tree depth    : 1

max_depth=3
  train accuracy: 0.981
  test accuracy : 0.933
  tree depth    : 3

max_depth=None
  train accuracy: 1.0
  test accuracy : 0.911
  tree depth    : 5
```

这个例子说明的内容很简单。

- 即使是同一个决策树，只要 `max_depth` 值不同，结果就会不同。
- 如果允许无限加深，train accuracy 可能会非常高。
- 但 test accuracy 不一定会一起变好。

也就是说，hyperparameter 是一种 `不改变 model 类型，却会改变泛化性质的设置值`。

## 细部学习内容补充

### `random_state` 属于什么样的 hyperparameter

读者最容易混淆的一个值是 `random_state`。

这个值通常不会直接改变 model 复杂度，但在包含随机性(randomness)的训练或数据切分里，它会帮助你复现相同结果。

scikit-learn 文档说明，有些 estimator 和交叉验证切分器天生包含随机性，而 `random_state` 正是在控制这种随机性。

`random_state` 与其说是提高性能的手柄，不如说是一个让你在重复实验时更容易确认同样结果的手柄。

所以，`random_state` 和其他 hyperparameter 的角色有一点不同。

| hyperparameter 类型 | 代表作用 |
| --- | --- |
| 改变 model 性格的值 | `max_depth`, `n_neighbors`, `C` |
| 帮助实验可复现性的值 | `random_state` |

这个区分在后面整理实验比较时会特别重要。

## 检查清单

- 你现在看的这个值，是学习出来的 parameter，还是预先定好的 hyperparameter？
- 你是否理解：即使同一个算法，只要设置值变了，结果也会不同？
- 你能不能说明为什么要同时看 train 分数和 test 分数？
- 你有没有分清 `random_state` 与其说和性能提升相关，不如说和可复现性更相关？
- 你能不能预见为什么下一节要把 `搜索范围` 和 `验证成本` 一起看？
- 你能不能说明 hyperparameter 是人在学习前先固定的配置值，而 parameter 是从数据里学出来的？
- 你能不能说明即使是同一个算法，也会因为 hyperparameter 而在复杂度、泛化、计算成本上不同？
- 你能不能说明频繁改动 hyperparameter，也就意味着实验成本和验证成本一起增加？

## 出处与参考资料

- scikit-learn, `Glossary of Common Terms and API Elements`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/glossary.html](https://scikit-learn.org/stable/glossary.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/modules/grid_search.html](https://scikit-learn.org/stable/modules/grid_search.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `12. Common pitfalls and recommended practices`, scikit-learn User Guide, 确认日期: 2026-06-26. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }
- Marc Claesen, Bart De Moor, `Hyperparameter Search in Machine Learning`, arXiv, 2015, 确认日期: 2026-06-26. [https://arxiv.org/abs/1502.02127](https://arxiv.org/abs/1502.02127){: target="_blank" rel="noopener noreferrer" }
- James Bergstra, Daniel Yamins, David D. Cox, `Making a Science of Model Search`, arXiv, 2012, 确认日期: 2026-06-26. [https://arxiv.org/abs/1209.5111](https://arxiv.org/abs/1209.5111){: target="_blank" rel="noopener noreferrer" }
- James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, Journal of Machine Learning Research, 2012, 确认日期: 2026-06-26. [https://jmlr.org/beta/papers/v13/bergstra12a.html](https://jmlr.org/beta/papers/v13/bergstra12a.html){: target="_blank" rel="noopener noreferrer" }
