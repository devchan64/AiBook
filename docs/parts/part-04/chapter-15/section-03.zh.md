# P4-15.3 OOB(out-of-bag)与随机森林检查

> Section ID: `P4-15.3`
> Version: `v2026.07.26`

在 P4-15.1 里，我们看过[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)为什么能通过聚合很多棵树来得到更稳定的预测。 在 P4-15.2 里，我们又看过怎样更小心地阅读这片森林把什么看得重要，也就是[特征重要度(feature importance)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)。

那么接下来剩下的问题就是：

怎样检查这片森林是不是真的学得还不错？

在随机森林里， 针对这个问题最先出现的抓手之一就是 [OOB(out-of-bag)](/AiBook/zh/reference/concept-glossary-pinyin/o/#oob-score)。

OOB 是一种内部验证式方法： 它利用没有被抽进 [bootstrap](/AiBook/zh/reference/concept-glossary-pinyin/b/#bootstrap) 样本的样本， 让随机森林在训练过程中对自己做一个粗略检查。

也就是说， OOB 不是 `一个新模型`， 而是读取和检查随机森林的方法。

这一节也不会再长篇重复随机森林的基本结构。 核心直觉会通过 P4-15.1 和[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)条目重新连接， 这里聚焦的只是： bootstrap 与 OOB 是怎样连成检查装置的。

## OOB 与随机森林检查先收束的问题

本节回答以下问题。

- [OOB(out-of-bag)](/AiBook/zh/reference/concept-glossary-pinyin/o/#oob-score) 为什么会出现？
- [bootstrap](/AiBook/zh/reference/concept-glossary-pinyin/b/#bootstrap) 与 OOB 是什么关系？
- [`oob_score=True`](/AiBook/zh/reference/concept-glossary-pinyin/o/#oob-score) 是什么意思？
- OOB 分数与 train accuracy、validation score、test score 有什么不同？
- OOB 应该信到什么程度，又该在什么地方停下来？

OOB 的外围边界先固定到下面这个程度就够了。

| 项目 | 在当前正文里的回收状态 |
| --- | --- |
| [交叉验证(cross-validation)](/AiBook/zh/reference/concept-glossary-pinyin/j/#cross-validation)的全部变体 | 交叉验证的基本作用会在 P4-9.1、P4-9.3 重新连接，但本节不代替对全部变体的说明 |
| [概率校准(calibration)](/AiBook/zh/reference/concept-glossary-pinyin/g/#probability-calibration)与 [threshold](/AiBook/zh/reference/concept-glossary-pinyin/y/#threshold) 调整 | threshold 和 calibration 的基本感觉会在 P4-6.4、P4-11.1 重新连接，但本节不会把那些细节与 OOB 一起展开 |
| 梯度提升中的 OOB 性格差异 | boosting 的检查感会在 P4-16.1、P4-16.2 通过 validation 与 early stopping 再次连接，但本节不展开细致对比 |

换句话说， 本节集中做的事是把 OOB 固定成 `随机森林的内部检查板`， 而更宽的评价流程和分数运用策略， 更适合在后续按问题再分开重读。

## OOB 与随机森林检查要留下的判断标准

- 你可以把 OOB 解释成 `利用 bootstrap 漏掉样本得到的内部泛化估计`。
- 你可以说明为什么只有在 `bootstrap=True` 时 OOB 才成立。
- 你可以说明为什么把 OOB 分数和 test 分数直接当成一回事是危险的。
- 你可以形成在随机森林实验里把 `train / OOB / test` 一起读的基本态度。

## 为什么需要这一节

初次使用随机森林时， 人通常会经历下面这个流程。

1. 训练看起来很顺利。
2. train accuracy 很高。
3. 于是模型就让人感觉已经不错了。

但这个流程里有一个很大的空白。

`在训练数据上很贴合` 和 `在没见过的数据上也能撑住` 不是同一回事。

因为随机森林使用 bootstrap， 训练过程中自然会出现 `这棵树没有见过的样本`。 OOB 正是利用了这个缝隙。

所以 15.3 不是一节关于 `怎样相信森林给出的一个分数` 的课， 而是一节关于 `怎样用多个分数去检查森林状态` 的课。

## OOB 为什么会出现

scikit-learn 用户指南说明， 在随机森林里， 每棵树都是用 bootstrap sample，也就是有放回抽样(with replacement)得到的样本建起来的。 在这种抽样方式下， 某些样本会在一棵树里出现多次， 也有些样本会完全没进入那棵树的训练。

这些被漏掉的样本， 就是 out-of-bag sample。

可以这样去读。

- 一棵树不会看到全部训练数据
- 所以会出现 `这棵树没见过的训练样本`
- 这些样本可以用来局部检查这棵树

所以 OOB 是 bootstrap 产生的副产物， 而随机森林又把这个副产物重新拿来当作检查资源。

## bootstrap 与 OOB 的关系

如果用一个场景画出来，大概是这样。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-01-zh.mmd"
```

这个图里最重要的一点是： OOB 不是 `完全独立的额外数据集`。 它仍然属于训练集的一部分。 关键在于， 从某一棵树的角度看， 它是 `没见过的样本`。

## `oob_score=True` 是什么意思

scikit-learn API 文档把 `oob_score` 解释成： 是否要利用 out-of-bag samples 来估计 generalization score 的选项。 文档也说明， 只有在 `bootstrap=True` 时才能使用这个功能。

- `bootstrap=True`：每棵树都用 bootstrap 样本训练
- `oob_score=True`：把被漏掉的样本聚起来，计算内部检查分数

所以没有 bootstrap，就没有 OOB。 如果每棵树总是看到完整数据， 那 `没见过的样本` 这个概念本身就消失了。

## OOB 到底是什么分数

API 文档把 `oob_score_` 解释成： 在训练数据集上，通过 out-of-bag estimate 得到的 score。

这里读者要小心两件事。

1. OOB 不是训练数据之外一份完全全新的数据分数。
2. 但它也不是单纯的 train accuracy。

也就是说， OOB 处在两者之间， 更像一个 `内部泛化估计值`。

| 分数 | 它依据什么 |
| --- | --- |
| train accuracy | 模型在直接用于训练的数据上拟合得多好 |
| OOB score | 每个样本被那些没见过它的树预测得多准 |
| test score | 模型在完全单独留出的数据上表现得多好 |

所以 OOB 往往比 train score 更接近现实， 但如果直接把它当成 test score 的完全替代品，也很危险。

把这个差异压成分数模式，可以写成下面这样。

| 分数模式 | 先想到的解释 | 紧接着要问的问题 |
| --- | --- | --- |
| 只有 train 很高 | 它可能对训练数据贴得太紧 | OOB 和 test 也一样高吗？ |
| train 很高，而 OOB/test 跟得比较近 | 这片森林在内部检查和独立检查下可能相对稳定 | 还剩下哪些错误案例类型？ |
| train、OOB、test 都低 | 瓶颈可能是特征表达或数据质量，而不只是森林本身 | 要不要重看特征表达？ |

所以 OOB 这一节的核心不是 `一个分数`， 而是 `一组分数`。

## 为什么 OOB 会让人觉得方便

scikit-learn 的文档和例子说明， OOB error 能让读者在训练随机森林的同时拿到一种验证式估计。

这在实验早期非常实用。

- 小实验可以更快重复
- 它能减少只看 train score 的错误
- 它能更快检查树数(/AiBook/zh/reference/concept-glossary-pinyin/h/#hyperparameter))增加时状态怎么变化

所以 OOB 更接近 `快速内部检查板`， 而不是 `评价流程的终点`。

## 那么只看 OOB 就够了吗

这里必须先停一下。

`不。通常不能只靠 OOB 就结束。`

原因很简单。

- OOB 是依赖 bootstrap 结构的内部估计
- 它并不处在和真正新数据完全相同的条件下
- 当数据量小、类别不平衡、或评价指标很敏感时，单独留出的 validation/test 仍然很重要

OOB 的角色可以这样区分。

| 情况 | OOB 的角色 |
| --- | --- |
| 早期快速实验 | 非常有用的内部检查 |
| 粗略的超参数搜索 | 有用的参考指标 |
| 最终性能报告 | 要和 test/validation 一起看 |
| 部署前最终判断 | 不能只靠 OOB 一个分数结束 |

### 什么时候 OOB 特别有用

OOB 并不会替代所有评价， 但在随机森林实验前期， 它会是一个非常实用的内部检查板。

| 当前情况 | 为什么 OOB 特别有用 | 一起确认什么 |
| --- | --- | --- |
| 想快速比较多个森林设置 | 因为 bootstrap 内部就能一起得到检查分数 | 是否把 test 留作最后确认 |
| train 分数太高让人不安 | 因为 OOB 能给出比 train 更不乐观的估计 | OOB 与 test 的间隔 |
| 正在考虑是否增加 `n_estimators` | 因为树数变化时的内部稳定性可以很快检查 | 改善幅度相对于计算成本是否值得 |
| 是个小实验，难以拿出大的 validation 集 | 因为无需再切一刀就能多一个检查信号 | 是否把 OOB 误当成最终汇报分数 |
| 想确认 bootstrap 型森林是否运作正常 | 因为可以借由“树没见过的样本”来检查内部状态 | 是否真的设置了 `bootstrap=True` |

这张表的重点，是把 OOB 正确放在 不是 `最终真相`， 而是 `快速内部状态检查板` 的位置上。

## 为什么要把 train / OOB / test 一起看

检查随机森林时， 把这三个数字并排放在一起的习惯非常重要。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-02-zh.mmd"
```

例如：

- 如果 train 很高，但 OOB 和 test 低很多，就可以怀疑[过拟合(overfitting)](/AiBook/zh/reference/concept-glossary-pinyin/g/#overfitting)
- 如果 train、OOB、test 都差不多低，就可以怀疑表达能力不足或数据限制
- 如果 train 很高，而 OOB/test 跟得比较近，就可以把森林读成相对稳定

本节的核心不是某一个数字， 而是 `数字之间的间隔`。

## Python 示例：看 OOB 分数

这个例子是在乳腺癌(breast cancer)分类数据上， 把 train / OOB / test 一起打印出来的一个小练习。

- 问题场景：看随机森林是不是既很好地贴合训练，又在内部检查与独立 test 上维持相近状态
- 输入(input)：30 个连续特征
- 标签(label)：恶性 / 良性 class
- 要确认的概念：
  - OOB 通过 `oob_score_` 来读
  - OOB 在 train 与 test 之间扮演内部检查角色
  - 三个分数的间隔要一起读
- 可以改动的值：
  - 把 `n_estimators` 改成 100、300、600，观察 OOB 与 test 的间隔是否稳定。
  - 改变 `random_state`，检查 train/OOB/test 模式是否仍然保留。

```python
# 这个例子在乳腺癌分类中一起输出 train、OOB、test 分数，用来阅读它们的间隔。
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(
    n_estimators=300,
    bootstrap=True,
    oob_score=True,
    random_state=42
)
model.fit(X_train, y_train)

print("train accuracy:", round(model.score(X_train, y_train), 3))
print("oob score     :", round(model.oob_score_, 3))
print("test accuracy :", round(model.score(X_test, y_test), 3))
print("n_estimators  :", model.n_estimators)
```

示例输出可能大致如下。 实际值会因切分方式、库版本、随机设置而略有变化。

```text
train accuracy: 1.0
oob score     : 0.96
test accuracy : 0.947
n_estimators  : 300
```

这个结果的阅读顺序是：

1. train accuracy 是 1.0，说明森林把训练集解释得非常好
2. 但如果只看 train，会过于乐观
3. OOB 0.96 与 test 0.947 没有明显分叉，所以这次实验给出一个信号：森林并不只是学到幻觉

当然， 这还不能直接证明模型已经足够好。 但 OOB 的价值就在于， 它能阻止读者看到 `train 1.0` 就立刻相信。

## Python 示例：随着树数增加，OOB 会怎样变化

这个例子会改变 `n_estimators`， 一起看 OOB 与 test 怎么移动。

问题场景：

- 在随机森林里，需要练习随着树数增加，OOB 与 test 怎样一起变化

输入(input)：

- 乳腺癌数据集 `X`、`y`
- 几个不同的 `n_trees`

期望输出(output)：

- 不同树数下的 OOB score
- 不同树数下的 test score

要确认的概念：

- 树数增加后，OOB 往往会朝着更稳定的方向移动
- 但只是不断增加树数，并不能解决所有问题

可以改动的值：

- 在 `[10, 50, 100, 300]` 列表里加入 600，把改善幅度和计算成本一起看。
- 比较限制 `max_depth` 与不限制 `max_depth` 时 train/OOB/test 间隔的变化。

```python
# 这个例子改变 n_estimators，比较 OOB 分数和 test 分数如何变化。
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

X, y = load_breast_cancer(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

for n_trees in [10, 50, 100, 300]:
    model = RandomForestClassifier(
        n_estimators=n_trees,
        bootstrap=True,
        oob_score=True,
        random_state=42
    )
    model.fit(X_train, y_train)

    print(
        f"trees={n_trees:3d} | "
        f"oob={model.oob_score_:.3f} | "
        f"test={model.score(X_test, y_test):.3f}"
    )
```

示例输出可能大致如下。 实际值会因切分方式、库版本、随机设置而略有变化。

```text
trees= 10 | oob=0.942 | test=0.947
trees= 50 | oob=0.957 | test=0.947
trees=100 | oob=0.960 | test=0.947
trees=300 | oob=0.960 | test=0.947
```

在这个例子里， 读者应该读出：

- 树数太少时，OOB 可能还会有些晃
- 过了一定数量之后，OOB 会开始显得稳定
- 但因为 test 分数可能停在相似水平，所以不能读成 `树越来越多，性能就会一直涨`

也就是说， OOB 可以帮助检查 `森林大概从什么时候开始稳定`， 但它本身并不是性能保证书。

这时也最好不要只留下一个 OOB 数字， 而是把比较标准和残留案例一起整理下来。 即使 OOB 或 test 在数值上看起来相似， 重复出现的错误类型仍然可能不同。 所以分数模式和案例模式要一起读。

| 需要一起留下的项目 | 在本节里记什么 | 为什么需要 |
| --- | --- | --- |
| 内部比较标准 | train / OOB / test 的间隔 | 为了看训练拟合与泛化估计分开了多少 |
| 残留 review 案例 | 在 OOB 与 test 中反复出错的样本 | 为了判断是要增加森林，还是回头重看特征表达 |
| 下一步验证问题 | 树数、深度、特征表达该先动哪里 | 为了把分数解释转交给下一轮实验顺序 |

## 解读 OOB 时常见的误解

尤其常见的误解包括：

| 误解 | 更安全的解释 |
| --- | --- |
| OOB 高，就可以部署了 | OOB 只是内部检查信号，最终验证仍然需要另外完成 |
| 这次 OOB 和 test 很像，所以它们总是一样 | 它们只是这次实验恰好相近 |
| 有了 OOB，就不需要 validation split | 视情况而定，validation 仍然有必要 |
| OOB 低，就说明随机森林没用 | 还要一起看数据质量、特征表达与超参数 |

重要的是： `既不低估 OOB，也不高估 OOB 的态度。`

### 当 OOB 和 test 不一致时，先怀疑什么

初学者很容易觉得， OOB 和 test 只有长得相似才算正常。 但只要差距不算极端，二者略有不同本身并不奇怪。 更重要的是， 不要太快断定差异的原因。

| 看见的场景 | 先怀疑什么 | 原因 |
| --- | --- | --- |
| OOB 看起来还行，但 test 更低 | hold-out 切分差异、代表性差异 | 因为 OOB 是内部估计，而 test 是单独留出的样本 |
| OOB 更低，但 test 稍高 | bootstrap 型内部估计的波动、数据量较小 | 因为在某些实验里，OOB 也可能显得更保守 |
| 两者都很晃 | 数据太少、类别不平衡、特征表达偏弱 | 因为问题可能首先出在数据状态，而不是森林结构 |

这里重要的不是立刻选出 `谁才是真相`。 而是检查： 在重复实验时这种模式会不会保持、 残留错误案例是否类似、 以及数据切分是否失去了太多代表性。

## 案例与示例

### 案例 1. 训练分数完美时，想快速检查森林到底稳不稳

某个欺诈交易检测团队训练了随机森林， train accuracy 几乎完美。 人先看到的标准包括 `短时间内重复支付`、 `异常地区`、 `深夜交易` 等信号。

如果只看这个高 train 分数， 模型很容易让人觉得已经够好了。 但团队已经从决策树那里学过： `在训练数据上很贴合` 和 `在新数据上也能撑住` 并不是一回事。 因为 bootstrap 会自然产生每棵树没见过的样本， 所以团队用 OOB 分数做内部检查。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-3-mermaid-03-zh.mmd"
```

在这个场景里， OOB 应该被读成 `内部泛化估计`， 而不是 `最终性能分数`。 如果 train 很高，但 OOB 和 test 都低， 那就仍然要怀疑过拟合或表达问题。 如果 train、OOB、test 没有明显大差距地跟着走， 这片森林就可以被读成相对稳定。 换句话说， 真正重要的不是某一个数字， 而是数字之间的间隔。

可验证的结果会在 train / OOB / test 并排看时出现。 如果 OOB 比 train 低很多， 它能阻止过于乐观的解读。 如果 OOB 和 test 走得相近， 它就会成为一个快速检查森林状态的有用抓手。

如果把这个案例压成备忘录， 可以写成下面这样。

| 观察到的分数模式 | 立刻附上的解释 | 要留下的 review 案例 | 下一个问题 |
| --- | --- | --- | --- |
| train 很高，而 OOB/test 更低 | 森林可能对训练数据贴得太紧 | 重复出错的交易类型、稀有模式、类别不平衡案例 | 应该先减深度，还是先重做特征表达？ |
| train、OOB、test 跟得比较近 | 当前森林在内部检查与独立检查下都相对稳定 | 残留的误报/漏报案例 | 是否可以继续进入 threshold 或 importance 解读？ |

### 案例 2. OOB 看起来不错，但 test 比预期更低

假设某个质量检查团队训练了一个用于不良品检测的随机森林。 train 很高， OOB 看上去也不错。 这时很容易让人觉得： `是不是已经够用了？` 但单独留出的 test 却仍然可能比预期更低。

在这个场景里， 最容易做出的判断是 `OOB 错了` 或者 `test 只是碰巧不好`。 但更安全的解释不是立刻丢掉其中一个， 而是先问： `为什么内部估计和独立验证会拉开？` 比如要重新检查： 是否某个时间段数据更集中到了 test 里， 是否稀有缺陷类型更多地落在 hold-out 一边， 或者当前特征表达是否漏掉了某些模式。

所以当 OOB 和 test 不一致时， 核心并不是 `马上选一个当答案`， 而是利用这个差距来决定： `到底是在什么数据场景里差距变大了` 以及下一轮实验顺序应该怎样排。 在这种时候， 往往比起单纯把森林再变大， 先重看切分方式、重复错误案例和特征表达会更安全。

## 在实务里怎样用

如果改写成实务流程， OOB 通常可以这样读。

1. 先快速训练一个随机森林作为 baseline。
2. 把 train score 和 OOB score 一起看。
3. 不要只因为 train score 乐观就停下。
4. 如果需要，再用 validation/test 做二次确认。
5. 然后才进入 importance、threshold 等解释或调节步骤。

所以 OOB 是一种用来纠正 `检查顺序` 的装置。

本节的结果也可以立刻整理进同样的回顾结构里。

| 在 Part 4 里要留下的问题 | 在 Part 6 回顾文档里的语言 |
| --- | --- |
| train / OOB / test 分别是多少？ | 事实(fact) |
| 这些间隔更像在提示过拟合、稳定性，还是表达不足？ | 解读(interpretation) |
| 下一轮实验里，树数、特征、validation 设置该先改哪个？ | 下一问题(next question) |

例如， 如果只有 train 高而 OOB 低， 那当前森林可能只是对训练数据过于乐观地贴合。 这时就应该先回头检查深度、特征表达与 validation 切分。 反过来， 如果 OOB 和 test 一起低， 就更应该先看特征表达或数据质量，而不是一味怪森林。 只有加上这种判断， OOB 才会从一个分数说明， 变成决定下一轮实验顺序的标准。

这一节还会再停一步， 把 `现在立刻要改什么` 和 `这个阶段还不该急着做什么判断` 区分开来。

| 最先出现的信号 | 现在要读出的意思 | 紧接着的下一步动作 | 这个阶段先不要急的判断 |
| --- | --- | --- | --- |
| 只有 train 高，而 OOB/test 低 | 森林可能对训练数据贴得过紧 | 先回看深度、最小样本数、特征表达、validation 切分 | 不要先去改 threshold 或服务策略 |
| train、OOB、test 都低 | 特征表达或数据质量可能比森林本身更像瓶颈 | 先回看特征设计、缺失变量、数据质量与相对 baseline 的提升幅度 | 不要只靠继续增加树数来硬解 |
| OOB 和 test 跟得比较近 | 当前森林在内部检查与独立检查下状态相近 | 可以再往 importance、threshold、后续集成比较走 | 不要只靠 OOB 就结束最终部署判断 |

所以 OOB 这一节真正的核心， 不是只回答 `分数是多少`， 而是让读者能直接说出： `面对这种分数模式，下一步该改什么，什么还要先缓一缓。`

### 看完 OOB 后至少要留下的实验备忘

如果 OOB 只被写成一个数字， 它的含义很快就会变模糊。 最好至少把下面四行一起留下。

| 项目 | 示例记录 |
| --- | --- |
| observed scores | `train=1.00, OOB=0.96, test=0.947` |
| first interpretation | `train 到 OOB/test 有间隔，但还不是完全崩掉的状态` |
| review cases | `重新看稀有缺陷类型与反复出现的误报案例` |
| next action | `先回看特征表达与 validation 切分，而不是只继续加树数` |

有了这份备忘， OOB 这一节就不再只是一个分数介绍， 而会变成留下下一轮调节顺序的实验记录。

这一节后面的下一个场景就是梯度提升(gradient boosting)。 如果随机森林是 `把很多树并行聚起来，降低摇摆的方法`， 那么 P4-16 的 boosting 就会转到 `让下一棵树顺序地修正前一轮错误的方法`。

## 检查清单

- 你有没有把 OOB 当成和 test score 一样的东西？
- 你能不能说明只有 `bootstrap=True` 时 OOB 才成立？
- 你是否在一起阅读 train / OOB / test 之间的间隔？
- 你能不能把 OOB 解释成一种利用 bootstrap 漏掉样本的内部检查方式？
- 你能不能说明 `oob_score=True` 只有在 bootstrap 型随机森林里才有意义，而 OOB 往往比 train score 更贴近现实，但并不能完全替代 test score？
- 你是否知道检查随机森林时，把 `train / OOB / test` 一起读非常重要，而且 OOB 对快速实验很有用，但不是最终部署判断的唯一依据？

## 出处与参考资料

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
