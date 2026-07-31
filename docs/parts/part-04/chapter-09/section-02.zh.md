# P4-9.2 调优(tuning)与验证成本

> Section ID: `P4-9.2`
> Version: `v2026.07.31`

在 P4-9.1 里，我们看过什么是 [hyperparameter](/AiBook/zh/reference/concept-glossary-pinyin/h/#hyperparameter)，以及为什么它很早以前就被当成一个单独问题来处理。现在要进入下一个问题。

那些看起来不错的设置值，到底该怎样实际选出来？

这个问题，正是 tuning 的出发点。

人们常常把 tuning 理解成 `把各种值都试一遍`。但实际它是一项更窄、更严格的工作。tuning 不只是让性能数字上升，而是在可验证的流程里比较 hyperparameter 候选，并同时管理这种比较带来的计算成本和验证成本。

也就是说，tuning 当然是在 `找更好的值`，但同时它也是 `不破坏比较本身的实验设计`。

这一节不会再长篇重复 hyperparameter 本身的定义。`学出来的值` 和 `预先定好的值` 之间的基本区分，会继续通过 P4-9.1 和概念词汇表接回；这里则只集中在：这些设置值到底该如何比较、如何管理。

## 调优与验证成本先收束的问题

这一节回答下面这些问题。

- tuning 是在做什么工作？
- 为什么 hyperparameter 摸得越多，并不一定越好？
- 为什么会产生验证成本(validation cost)？
- 为什么 test data 必须只在最后使用？
- grid search 和 random search，入门层面应该怎样理解？

这一节先收束 `应该在什么验证流程里比较设置值候选`。Bayesian optimization、Hyperband、nested cross-validation、实验追踪和分布式调优的大图景，会在 P4-9.3 再整理。

## 调优与验证成本要留下的判断标准

- 能把 tuning 解释成 `在 validation 流程里比较设置值` 这件事。
- 能区分计算成本(computational cost)和验证成本(validation cost)。
- 能说明为什么一边看 test data 一边选设置会很危险。
- 能在入门层面说明 grid search 和 random search 的差别。
- 能理解为什么在读 baseline 之后的改进时，validation 流程比 tuning 日志本身更重要。

## 学习背景

到 P4-8.2 为止，我们已经整理了 `应该拿什么做比较标准`，而在 P4-9.1 里又看过了 `同一个 model 家族里有哪些设置值`。但如果停在这里，实验仍然只准备了一半。

- 即使有候选 model，如果不决定设置值该怎么选，比较就会摇晃。
- 设置值候选一多，计算时间和实验次数就会一起增加。
- 如果验证流程太松散，就会把某个“碰巧看起来不错”的值误判成真实改进。

也就是说，这一节是在把 `存在 hyperparameter` 这个事实，推进到 `需要一种公平地选择 hyperparameter 的方法` 这个事实。

如果这里再固定住一点，tuning 这一节的解释会更稳定。tuning 是在改 `model 内部的数字`，但在这之前，关于 `把什么看成一个样本`、`正在和什么 baseline 比较`、`想减少什么错误场景` 的笔记，必须已经先固定好。如果没有这些笔记，就算 validation 分数涨了一点，也很难解释到底什么真的变好了。分数差首先应该被读成变化信号，而对原因的解释则要等代表错误案例和输入表达再检查一遍之后再加上去。

| 在 tuning 前应先留下什么 | 为什么需要 |
| --- | --- |
| 样本单位和输入表达 | 因为即使是同一个 model，是直接用原始时序，还是改成一次动作汇总行，比较意义都会不同 |
| baseline 和当前候选分数 | 因为必须读出 tuning 到底比出发点多改善了什么 |
| 代表错误案例或大误差区间 | 因为必须确认分数上升到底减少了哪些失败 |
| 复查笔记 | 因为需要留下下一步该缩小还是扩大哪些设置的依据 |

tuning 的比较顺序，可以先固定成下面这样。

| 先看什么 | 紧接着问的问题 | 只在最后确认什么 |
| --- | --- | --- |
| baseline 和候选 model 的 validation 比较 | 这次设置变化，是否真的减少了同一类错误场景 | test 分数是不是也在同样方向上跟着变 |
| 混淆矩阵中的问题格子和代表错误案例 | 分数上升到底是 FN 变少、FP 变少，还是大误差变少 | 这种改进能不能正当化增加的计算成本和复杂度 |
| 候选设置之间的 validation 差异 | 这个值只是偶然好看，还是重复时也差不多 | 下一节或下一轮实验里，该进一步缩小哪个候选 |

| 课程位置 | 本节的作用 |
| --- | --- |
| 在 P4-9.1 之后 | 把“存在设置值”连接到实验流程上 |
| 在 P4-10 之后算法章节之前 | 为阅读各算法的 hyperparameter 提供标准 |
| 在项目实作之前 | 准备“同时看实验成本和验证成本”的习惯 |

## 调优是用验证分数选择 hyperparameter 候选

scikit-learn 的 hyperparameter tuning 文档说明了一种流程：先把 estimator 的设置值整理成候选集合，再用 [cross-validation](/AiBook/zh/reference/concept-glossary-pinyin/j/#cross-validation) 分数来比较。

`tuning 是先固定一组 hyperparameter 候选，然后用验证分数比较，选出更适合当前数据和目标的设置。`

这里重要的是两点。

1. 不是把任何值都无限地乱改。
2. 比较必须在 train 内部的 validation 流程里完成。

也就是说，tuning 不是凭感觉点一个 `看起来不错的值`，而是在预先定好的候选空间和验证规则里做比较。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-2-mermaid-01-zh.mmd"
```

这张图说明：tuning 的核心，是 `先选一个 model，再用 validation 分数比较候选设置，最后才只检查一次 test`。这里尤其重要的是角色分工：`test 不是拿来选的，而是拿来做最后确认的。`

这张图的核心就是：`test 只在最后看一次`。tuning 的主体其实在 `B -> C -> D` 这一段。

### 计算成本和验证成本有什么不同

一说到成本(cost)，人们很容易只想到训练时间。但在 tuning 里，至少要把两种成本分开。

| 成本类型 | 含义 |
| --- | --- |
| 计算成本(computational cost) | 反复训练 model、打分所花的时间、内存、GPU/CPU 资源 |
| 验证成本(validation cost) | 在反复看 validation 数据挑设置时产生的[过拟合](/AiBook/zh/reference/concept-glossary-pinyin/g/#overfitting)风险 |

计算成本相对更容易看见。

- 候选值越多，就越耗时。
- 交叉验证 fold 越多，就越耗时。
- 单个 model 的训练时间越长，总调优时间就越大。

但验证成本不会像数字那样直接冒出来，所以反而更危险。

- 如果盯着 validation 分数看太久，就可能开始对 validation 数据本身做出适配。
- 这样一来，它在 validation 上看起来更好，但在真正的新数据上未必还那么好。

也就是说，计算成本是 `贵不贵` 的问题，而验证成本是 `比较到底靠不靠谱` 的问题。

验证成本也应该一起读成 `反复实验记录成本`。如果只记分数不记过程，之后就很难再回头确认：validation 跑了多少次、哪些候选被丢掉了、哪些错误一直在重复出现。也就是说，验证成本不只是计算量，还包括 `留下以后还能读懂的比较记录` 这种负担。

下面这张图用最简单的方式说明了为什么计算成本会涨得这么快。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-2-mermaid-02-zh.mmd"
```

这张图说明的是：hyperparameter 候选只要稍微增加一点，实际训练次数就会以乘法方式迅速膨胀。这就意味着 tuning 不是简单的“玩一玩数值”，而是必须连同计算成本和实验设计一起管理的工作。

## 细部学习内容

### 为什么 test data 只能在最后使用

scikit-learn 的 common pitfalls 文档说明，如果 test data 被混进 model selection 或 preprocessing，性能估计就可能显得过于乐观。这条原则在 tuning 上完全同样适用。

`test 是用来看分数的，不是用来做决定的。`

也就是说：

- train 用来学习
- validation 用来选择
- test 用来最终确认

这就是基本分工。

如果把这个顺序倒过来，会发生什么？

| 错误用法 | 产生的问题 |
| --- | --- |
| 一边看 test 分数一边选 hyperparameter | test 失去“真正新数据”的角色 |
| 反复看 test 并据此改 model | 最终分数可能显得过于好看 |
| 连 preprocessing 都参考 test | leakage 和过高估计会一起出现 |

这种角色分工的核心，和前面那张图是同一个意思。如果 `train 用来学，validation 用来比候选，test 用来做最后确认` 这个顺序被打乱了，那么分数即使看起来不错，放到真正新数据上的可信度也会下降。

关键点在于，test 不是 `帮助比较的数据`，而是 `比较结束后保留下来的确认数据`。

### 应该怎样理解 grid search 和 random search

scikit-learn 提供了 grid search 和 randomized search 作为代表性的搜索方式。

可以先用下面这张表来区分。

| 方法 | 入门理解 |
| --- | --- |
| grid search | 把预先列好的候选表全部跑一遍 |
| random search | 在预先设好的分布或范围内抽出一部分组合来比较 |

grid search 很简单，也容易解释。

- 很清楚到底试了哪些值。
- 如果候选不多，实施和说明都比较方便。

但一旦候选轴增多，它很快就会变贵。

例如，如果只有：

- `max_depth`: 4 个候选
- `min_samples_split`: 5 个候选
- `criterion`: 2 个候选

那就已经有 `4 x 5 x 2 = 40` 个组合了。如果再加上 5-fold cross-validation，实际训练就可能发生 200 次。

random search 不需要看完所有组合，所以可以用更便宜的方式扫更宽的空间。Bergstra 和 Bengio 的论文说明，如果真正重要的性能轴只有一部分，那么 random search 可能更高效。

- grid search: 当候选表较窄，需要仔细比全时
- random search: 当候选范围较宽，希望更便宜地扫一遍时

也就是说，两者差别更适合读成：`要不要把所有组合都看一遍`，还是 `只策略性地看一部分`，而不只是一个方法名字差异。

### 应该怎样读取 baseline 之后的改进

在 P4-8.2 里先放 baseline 的理由，在这里会更清楚。调优之后就算分数高了一点，也不一定代表改进很大。

例如，可以想下面这种场景。

| 比较场景 | 解释问题 |
| --- | --- |
| baseline 0.90 -> 候选模型 0.91 | 这个差距真的有意义吗？ |
| 候选模型 0.91 -> 调优后 0.912 | 值不值得为它付出更高计算成本？ |
| 候选模型 recall 上升、precision 下降 | 它到底减少了哪一类错误成本？ |

### 应该先用哪种 tuning 方式

tuning 也不应该一上来就无限铺开，而应该根据当前候选数和计算预算来选择比较方式。

| 当前情况 | 最先想到的方式 | 原因 |
| --- | --- | --- |
| 候选值不多，而且解释清楚的比较很重要 | grid search | 因为容易直接确认所有组合 |
| 范围很宽，但资源有限 | random search | 因为可以用采样方式扫较大的空间 |
| 自己开始忍不住想一直看 test | 重新固定 validation 流程 | 因为 test 必须从选择过程里拿掉，只留到最后确认 |
| 只是在反复出现很小的分数差 | 重新检查错误案例和成本 | 因为必须重看这种改进到底值不值额外成本 |
| 候选组合数迅速膨胀 | 缩小搜索空间 | 因为计算成本会以乘法方式增长 |

这张表会让读者把 tuning 读成：不是 `多跑一点的技术`，而是 `管理验证流程和成本的选择`。

也就是说，tuning 不是 `把数字抬得更高的工作`，而是 `读出用了什么成本、换来了什么类型改进的工作`。

所以在读 tuning 时，始终要一起看三件事。

1. 相比 baseline，到底改善了多少？
2. 在 validation 标准下，这个改善是不是一贯存在？
3. 这种改善是否值得为它支付更高的计算成本和复杂度？

这里比较单位也不能摇晃。当 baseline、候选 model、调优后 model 并排摆在一起时，应该尽量按同样的样本单位、同样的输入表达、同样的错误场景来读。只有这样，`分数稍微涨了一点` 才能被判断成它是否真的意味着相同失败在减少。

如果是分类问题，这里还要再多看一遍代表错误案例。即使分数比 baseline 略高，model 也可能仍然在漏同样的少数类，或继续陷在同样的混淆区间。特别是，即使最近区间的分数上升了，这个差值本身也不会自动告诉你“为什么变好了”。

所以，调优之后不能停在 `分数上升了`，而是必须重新确认：到底是哪些错误场景真的变了。

只有在同样的最近区间、同样的混淆矩阵问题格子、同样的代表错误案例上比较时，读者才能更稳定地说出 `到底什么真的变好了`。

| 调优后要重新看的东西 | 为什么必须重新看 |
| --- | --- |
| 相比 baseline 的关键指标差 | 因为必须先确认相对出发点到底进步了多少 |
| 混淆矩阵中的问题格子 | 因为必须知道分数上升到底是 FP 变少、FN 变少，还是大误差模式变少 |
| 代表错误案例(error case) | 因为必须确认是否还在漏同类型输入，还是已经变成了另一种失败 |
| 计算成本和 model 复杂度 | 因为必须判断一点点分数上升是否值得更长训练时间和更难的运营 |

如果把这张表改写成项目笔记格式，会更清楚。

| 应该留在实验笔记里的项目 | 示例 |
| --- | --- |
| 相比 baseline 的变化 | `recall +0.03`, `MAE -0.12` |
| 仍然没变的失败 | `仍然漏掉同一少数类 2 次` |
| 新增成本 | `训练时间增加 3 倍`, `比较了 40 个设置候选` |
| 下一轮实验问题 | `应该继续加深 depth，还是换到别的候选 model` |

只有留下这种笔记，tuning 才会保留成 `维持比较结构的反复实验`，而不是只剩 `数字优化`。

只看分数流动时，它看起来可能很简单。但真正的读取问题会越来越严格。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-2-mermaid-03-zh.mmd"
```

### 为什么在实务里会提前停止 tuning

在实务里，人们并不总是追到最高分为止。下面这些情况里，提前停止 tuning 反而可能更好。

- 已经存在一个比 baseline 足够好的简单 model
- 计算成本上涨得很快
- validation 分数提升已经非常小
- 可解释性或部署速度更重要

也就是说，tuning 的目标不一定是 `尽可能高的数字`，而可能是 `相对于当前目的已经足够好的 model`。

这个视角在后面的算法章节里也会持续重要，因为很多场景里，运营差异比性能差异更关键。

## 案例及示例

### 案例 1. 即使跑了很多设置，为什么结果仍然不该立刻相信

一个构建欺诈检测 model 的团队，想把决策树和随机森林的设置值在很宽的范围里都试一遍。人们最先看的标准，是 `短时间内重复支付`、`和平时不同的地区`、`奇怪时间段的交易` 这类信号。

团队觉得候选越多越好，于是把 `max_depth`、`min_samples_split`、`n_estimators` 的值都密密地全跑一遍。这样一来，计算成本会迅速上升；而且 validation 分数看得越久，把碰巧表现好的组合误当成真实改进的风险也会越大。尤其是一旦中途还开始检查 test 分数，留给最终确认的数据也会逐渐失去意义。

在这个场景里，tuning 应该被读成不是 `多改一点值`，而是 `在 validation 流程里比较候选`。设置比较应该发生在 train 内部的 validation 中，test 只能最后看一次。grid search 和 random search 的差别，最终也都连回到了一个成本管理问题：`要不要把所有组合都看完`，还是 `只抽样看一部分大空间`。

能确认的结果，会出现在把组合数和交叉验证次数相乘后的训练次数，以及把 validation 最高分和最终 test 分数分开来读的时候。即使同样是 0.002 的提升，也必须连同它付出了多少倍的计算成本、承担了多大的验证风险一起看，调优才算是可解释的。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-2-mermaid-04-zh.mmd"
```

### 示例 1. 当候选组合数增加时，计算成本会怎样增长

如果只看定义，计算成本和验证成本会显得很抽象。但只要把它换成真实实验场景，就会更清楚地看见为什么这两个成本必须分开读。

正如这一节前面看到的，只要 hyperparameter 轴多出几个，组合数就会按乘法增长。

- `max_depth`: 4 个候选
- `min_samples_split`: 5 个候选
- `criterion`: 2 个候选

光这三个轴就已经有 40 个组合。再加上 5-fold 交叉验证，实际训练就可能发生 200 次。

这个数字在玩具例子里看起来或许还能承受，但一旦进入“训练一个 model 就要几分钟或几小时”的任务，它的意义就完全不同了。

| 场景 | 同样的 200 次训练意味着什么 |
| --- | --- |
| 小决策树练习 | 很快就结束的比较 |
| 大型文本分类 model | 很长的实验等待时间 |
| 大规模图像 model | GPU 成本上升和实验日程拉长 |

也就是说，计算成本不是抽象理论，而是直接限制 `你到底能放多少候选进去` 的现实约束。

### 示例 2. 如果盯 validation 看太久，比较流程本身也可能开始摇晃

scikit-learn 的 common pitfalls 文档说明，如果把 test data 混进 model selection，性能估计就可能显得过于乐观。读者很容易把这个警告理解成“只和 test 有关”，但如果 validation 也被反复盯着看太久，类似的问题也会朝同一个方向出现。

例如，可以想象下面这样的场景。

1. 只要 validation 分数稍微涨一点，就继续增加候选。
2. 只记住表现好的设置，把表现差的组合扔掉。
3. 在同一个 validation 切分上，一次又一次做细微调整。

这个过程拖得越久，model 就越可能开始适应 `那个 validation 切分的偶然特征`，而不是 `更一般的规律`。

`validation 是用来选择的，但如果把它用在选择上太久，它本身也会部分变成学习对象。`

也就是说，验证成本不是一种额外金钱成本，而是 `一点一点侵蚀比较可信度的成本`。

### 示例 3. 一点点性能上升，在运营上可能意义并不大

如果读者已经看过 P4-8.2 里的 baseline，那么现在就需要更保守地去读候选 model 和调优后 model 之间的差别。

例如，考虑下面这样的比较。

| 阶段 | 分数 | 第一眼感觉 |
| --- | --- | --- |
| baseline | 0.900 | 出发点 |
| 候选模型 | 0.910 | 看起来像有改进 |
| 调优后 | 0.912 | 看起来又更好了 |

但在直接相信这个场景之前，还得重新问：

- 这额外的 0.002 提升，在 validation 标准下是不是一贯存在？
- 为了这一点点差距，组合数翻了几倍？
- 有没有牺牲预测速度、可解释性或运营简洁性？

也就是说，在实务里，`分数稍微更高` 和 `选择稍微更好` 并不一定是同一句话。

### 示例 4. 为什么 random search 有意义？因为整个空间并不是都同样重要

Bergstra 和 Bengio 的论文说明，在 hyperparameter 空间里，真正强烈摇动性能的轴，往往只有一部分。因此，相比把所有轴都按同样间距扫完的 grid search，更广泛抽样部分组合的 random search 可能更高效。

- 搜索空间里的每一条轴，不一定都同样重要。
- 所以，`更仔细` 并不总等于 `更高效`。
- 实证案例说明，搜索方法本身也会成为比较对象。

也就是说，tuning 不只是选值，它也是一个实验设计问题，里面还包括 `比较本身到底用什么方式进行`。

## 练习与示例

### 用 Python 例子看一个小型 tuning 流程

下面这个例子是一个很小的练习：为同一个决策树 model 准备 `max_depth` 和 `min_samples_split` 候选，再用 `GridSearchCV` 做比较。

- 问题场景: 把花数据(iris)当成品种[分类](/AiBook/zh/reference/concept-glossary-pinyin/c/#classification)问题。
- 输入(input): 四个数值[特征](/AiBook/zh/reference/concept-glossary-pinyin/f/#feature)。
- 正答(label): 三种品种。
- 要确认的概念:
  - 可以在 validation 流程里比较多个 hyperparameter 组合
  - 必须把 `best_params_`, `best_score_`, `test score` 分开来读

可以改动的值:

- 在 `param_grid` 的 `"max_depth"` 候选里加入 `4` 或 `5`，可以看到候选组合数和 `total model fits` 一起增加。
- 把 `cv=5` 改成 `3` 或 `10`，可以确认同一张候选表下，交叉验证 fold 数怎样改变计算成本。

```python
# 这个例子用验证数据反复评估多个超参数候选，以确认调优成本。
from sklearn.datasets import load_iris
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.tree import DecisionTreeClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

param_grid = {
    "max_depth": [1, 2, 3, None],
    "min_samples_split": [2, 4, 6],
}

search = GridSearchCV(
    estimator=DecisionTreeClassifier(random_state=42),
    param_grid=param_grid,
    cv=5,
)

search.fit(X_train, y_train)

candidate_count = len(search.cv_results_["params"])
cv_folds = search.cv

print("candidate combinations:", candidate_count)
print("cv folds              :", cv_folds)
print("total model fits      :", candidate_count * cv_folds)
print("best params           :", search.best_params_)
print("best cv score         :", round(search.best_score_, 3))
print("test score            :", round(search.score(X_test, y_test), 3))
```

执行结果示例如下。

```text
candidate combinations: 12
cv folds              : 5
total model fits      : 60
best params           : {'max_depth': 3, 'min_samples_split': 2}
best cv score         : 0.952
test score            : 0.978
```

这个例子说明的内容很简单。

- 候选组合数会直接连到计算成本。
- 再乘上 `cv folds`，就能粗略看到实际要 fit model 多少次。
- `best cv score` 是 validation 流程内部最好的分数。
- `test score` 是最后确认分数。

这两个数字不能被当成同一格里的数来读。

这个玩具例子也可以读成一个小型实证案例。

- 在小练习里，12 个候选组合还不算很大负担。
- 但即使用 5-fold CV，实际 fit 也已经是 60 次。如果按同样方式再增加几条轴，计算成本就会迅速上升。
- `best cv score` 和 `test score` 不相同这一点，再次说明了 validation 和最终确认拥有不同角色。

例如，如果候选模型是 0.910，而调优后变成 0.912，读者也不会立刻下部署结论。必须先重新检查：到底是不是某些组合只过度适配了同一个 validation 切分，以及这 0.002 提升是否值得更长的推理时间和更复杂的运营。也就是说，tuning 章节的核心，不是记住 `最高分`，而是一路确认 `一点点改进是否在现实里仍然成立`。在这里，分数差依旧只是抬高复查优先级的信号，在重新确认输入表达和错误场景之前，它并不会直接进入原因解释。

## Checklist

- 你是不是在用 validation 选设置，并把 test 只保留给最后确认？
- 你有没有把计算成本和验证成本分开看，而不是把它们混在一起？
- 当看到一点分数上升时，你有没有把代表错误案例和运营成本一起重新检查？
- 你现在看到的分数，到底是来自 train、validation 还是 test？
- 你是否理解 hyperparameter 候选数会直接连到计算成本？
- 你能不能说明为什么一边看 test 一边选设置会有危险？
- 你是不是在认真判断：相对 baseline 的改进到底有没有实际意义？
- 你是否已经对什么时候该用 grid search，什么时候该用 random search，有了基本感觉？
- 你能不能说明，tuning 是通过 validation 流程比较 hyperparameter 候选的工作？
- 你能不能说明，计算成本和验证成本并不相同，而且 test data 必须留到最后确认时再用？
- 你能不能把 grid search 和 random search 都理解成 `比较候选的方式`？

## 出处与参考资料

- scikit-learn, `3.2. Tuning the hyper-parameters of an estimator`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/grid_search.html](https://scikit-learn.org/stable/modules/grid_search.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `12. Common pitfalls and recommended practices`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }
- James Bergstra, Yoshua Bengio, `Random Search for Hyper-Parameter Optimization`, Journal of Machine Learning Research, 2012, 确认日期: 2026-07-26. [https://jmlr.org/beta/papers/v13/bergstra12a.html](https://jmlr.org/beta/papers/v13/bergstra12a.html){: target="_blank" rel="noopener noreferrer" }
