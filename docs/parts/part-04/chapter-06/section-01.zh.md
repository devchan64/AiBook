# P4-6.1 评价指标(metric)的作用

> Section ID: `P4-6.1`
> Version: `v2026.07.25`

在 P4-5 章里，我们看过[过拟合(overfitting)](/AiBook/zh/reference/concept-glossary-pinyin/g/#overfitting)和[泛化(generalization)](/AiBook/zh/reference/concept-glossary-pinyin/g/#generalization)。接下来会自然冒出一个问题：`在新数据上也站得住`，到底要靠什么来确认？这时出现的就是[评价指标(metric)](/AiBook/zh/reference/concept-glossary-pinyin/m/#metric)。

评价指标是把 model 拟合得怎样，用数字显示出来的工具。但更重要的一点是，metric 不只是记分牌，它还是一种 `我们决定把什么当成更重要` 的约定。即使是同一个 model，因为看的 metric 不同，它也可能显得不错，也可能显得有风险。

这一节说明评价指标(metric)、[准确率(accuracy)](/AiBook/zh/reference/concept-glossary-pinyin/a/#accuracy)、[精确率(precision)](/AiBook/zh/reference/concept-glossary-pinyin/j/#precision)、[召回率(recall)](/AiBook/zh/reference/concept-glossary-pinyin/z/#recall)、`F1` 的基本作用。下一节会沿着这个抓手继续判断当前语境，而 `到底把哪一类错误当成更重要` 的标准，会通过本节和 [概念词汇表](/AiBook/zh/reference/concept-glossary/) 再次接回。

## 本节范围

这一节是说明评价指标作用的导入节。这里把 accuracy、precision、recall、F1 score 先接到第一次见到的层次。像 ROC-AUC、PR-AUC、log loss、calibration、silhouette 这类指标，会在 P4-6.4 补充学习里另外回收；回归指标和聚类视角，则会在 P4-6.2 继续看。

也就是说，本篇核心的责任，是先把 `什么该被视为更重要` 固定下来。像概率分数的细致解释、reliability diagram、Brier score、threshold 的细调，这类更精细的读取，会留到 P4-6.4 和后面的 P4-15.3。这里先要明确的，是为什么 metric 不是只有一个。

这一节也会一起固定读 metric 的基本态度。在 [classification](/AiBook/zh/reference/concept-glossary-pinyin/c/#classification) 里，首先该看的是 [confusion matrix](/AiBook/zh/reference/concept-glossary-pinyin/h/#confusion-matrix) 和代表性的错误案例；后面的 P4-8.2 则会再拿 [baseline](/AiBook/zh/reference/concept-glossary-pinyin/b/#baseline) 来比较，看这种错误结构的变化到底算不算真的改进。也就是说，Part 4 里的评价，会沿着 `在哪些地方错了` 和 `相对什么变好了` 这个顺序继续，而不只是盯着 `一个数字`。

P4-6.2 会继续讨论：不同问题类型里，哪些评价标准应该被更优先地看。现在的重点，是先抓住 `为什么 metric 不只一个`、`为什么同样的数字也可能有不同含义`，以及 `为什么工作目标和错误成本必须进入 metric 选择`。

- 为什么需要评价指标(metric)？
- 为什么只看 accuracy 容易产生误解？
- precision 和 recall 分别回答什么问题？
- metric 除了显示 model 表现，还会一起暴露出我们重视什么吗？
- 为什么下一节要把指标按问题类型分开来看？

## 用评价指标(metric)的作用留下的判断标准

- 能把评价指标解释成 `读取 model 表现的标准`。
- 能理解 accuracy 不是所有场景的代表指标。
- 能说明 precision 和 recall 回答的是不同问题。
- 能说明工作目标与错误成本会影响 metric 的选择。
- 能为 P4-6.2 的按问题类型看评价标准做好准备。

## 学习背景

### 评价指标到底在做什么

scikit-learn 文档把 metrics and scoring 处理成 `把 prediction 质量数值化的工具`。同时，它也说明：到底选什么 metric，最终还是和 `这些 prediction 要被拿去做什么` 连在一起。

`评价指标(metric)是在用数字概括 model 结果的同时，也把我们认为哪种错误更重要一起暴露出来的标准。`

所以，metric 不只是说一句 `分数是多少`。

- 到底最想把什么做对？
- 尤其想减少哪一类失误？
- 这个 model 最终会接到什么真实决策上？

这些问题也会被一起拉进来。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-01-zh.mmd"
```

这张图说明：评价指标并不只是 model 内部数字的问题，它还是和真实决策语境连在一起的标准。即使是同样的 prediction，因为哪种错误更痛，最后先看的 metric 也会不同。

这条流程里的关键是：`metric 会接到 model 外部的决策语境`。model 负责做 prediction，而 metric 则让我们继续读出这些 prediction 在真实决策里意味着什么。

## 主要学习内容

### 为什么不能只靠 accuracy

Google 的 machine-learning glossary 把 accuracy 解释成 `所有 prediction 里预测正确的比例`。这个定义本身很简单，也很有用。但同一个 glossary 也说明：在 class imbalance 数据里，accuracy 可能会造成很大的误解。

例如，在 spam 邮件很少的数据里，就算 model 对所有邮件都预测成 `正常邮件`，accuracy 也可能很高。但这样的 model 并不能真正把 spam 挡住。

| 问题 | 只看 accuracy 时可能产生的误解 |
| --- | --- |
| 整体上答对了多少？ | 看起来像是答对了很多 |
| 有没有避免漏掉重要的正类案例？ | 对这个问题不一定回答得够好 |
| 有没有避免发出太多没必要的警报？ | 对这个问题也不一定回答得够好 |

所以，accuracy 可以是起点，但它不一定是一路负责到底的指标。

metric 阅读的起点，在于先确认 `现在首先想问的是哪一种错误或成功`。

| 当前担心什么 | 先拿出来的问题 | 先容易看的 metric |
| --- | --- | --- |
| 想先看整体答对多少 | 所有 prediction 里答对了多少？ | accuracy |
| 随便说成正类的失误很痛 | 被说成正类的里面，真正是正类的有多少？ | precision |
| 漏掉真正正类的失误很痛 | 真正的正类里，有多少没有被漏掉？ | recall |
| 想把 precision 和 recall 一起概括成一个数 | 能不能用一个数字看两者平衡？ | F1 |

### 先通过 confusion matrix 来读

要理解 precision 和 recall，应该先轻轻看一下 `confusion matrix`。Google glossary 把 confusion matrix 解释成 `把 model 做对和做错的情况整理成表的表格`。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-02-zh.mmd"
```

这张图说明了为什么 confusion matrix 会成为评价指标的起点。只有把真实值和预测值放进同一张表里，才能把 accuracy 之外的 FP、FN 这类不同错误分别读出来。

在 confusion matrix 里，读者首先要抓住的四个格子是下面这些。

| 项目 | 含义 |
| --- | --- |
| TP (true positive) | 实际为正，也正确预测成正 |
| TN (true negative) | 实际为负，也正确预测成负 |
| FP (false positive) | 实际为负，却错误预测成正 |
| FN (false negative) | 实际为正，却错误预测成负 |

这里最重要的一点是：`错` 其实也有两种。

- FP 是 `没必要响起的警报`
- FN 是 `该响却没响的警报`

因为这两种错误的成本不同，所以评价不可能只用一个 metric 结束。

用一个小例子来看会更快。

| 实际 / 预测 | 预测为正 | 预测为负 |
| --- | --- | --- |
| 实际正类 10 个 | 8 个 -> TP | 2 个 -> FN |
| 实际负类 90 个 | 6 个 -> FP | 84 个 -> TN |

如果把这张表重新翻回读者的问题，就是下面这样。

- 实际正类 10 个里抓到了 8 个 -> 是 recall 方向的问题
- 被说成正类的 14 个里，只有 8 个是真的正类 -> 是 precision 方向的问题

所以，即使面对同一张表，也可以问 `漏掉了多少真正的正类？`，也可以问 `有多少是没必要地被说成正类？`

即使是同一张结果表，读者先看的问题也不一定一样。如果漏掉更痛，就先看 recall；如果误报更痛，就先看 precision。

### precision 和 recall 回答的是不同问题

Google glossary 用下面这个问题来解释 recall。

> 当案例实际是正类时，model 把其中多少正确抓成了正类？

用同样的角度，把 precision 放在入门层次整理，就会变成下面这个问题。

> model 说成正类的那些里面，实际为正的比例有多少？

把两者分成表格，会更清楚。

| metric | 读者问题 | 特别在意的失误 |
| --- | --- | --- |
| accuracy | 整体答对了多少？ | 总体错误 |
| precision | 被说成正类的里面有多少是对的？ | 更偏向减少 FP |
| recall | 实际正类里有多少没被漏掉？ | 更偏向减少 FN |

只要理解这张表，就已经为下一节做好准备了。

## 细部学习内容

### 评价指标的历史背景

评价指标并不是最近 machine learning 才突然冒出来的工具。在 information retrieval 研究里，`什么才算好结果` 一直都是核心问题。C. J. van Rijsbergen 的经典教材把 evaluation 单列成一章，并通过社会性与经济性的问题来说明为什么需要评价。同一章还介绍了 recall 和 precision 这对指标，如何在 Cyril Cleverdon 的测量工作之后，成为说明检索系统有效性的核心搭配。

1. 计算机系统很早就必须区分 `相关的东西` 和 `不相关的东西`。
2. 所以问题不只是 `有没有找很多`，还变成了 `有没有漏掉该找的`、`有没有放出太多没用的东西`。
3. 这种思路后来从 information retrieval 延伸到 classification、detection 和 machine-learning evaluation。

所以，评价指标不是给数字加装饰，而是为了追问 `这个系统到底给用户带来什么帮助、又造成什么伤害` 而发展出来的语言。

## 案例与示例

### 案例 1. 要怎么读一个误报太多的不良检测 model

工厂检测系统正在根据产品照片区分 `不良` 和 `正常`。人最先使用的标准，是 `有没有裂纹`、`表面有没有污点`、`边角有没有破损` 这样的信号。

一开始，这个 model 因为 accuracy 很高而显得不错。但到了现场，它会把很多正常产品也送去复检。另一种 setting 则会减少复检，但实际漏掉的不良会变多。这时，就很难只靠 accuracy 说清到底哪个 model 更好。

```mermaid
--8<-- "assets/part-04/chapter-06/p4-6-1-mermaid-03-zh.mmd"
```

这里，评价指标就会变成揭示 `到底哪种痛更大` 的标准。如果现场最痛的是复检成本，就要更仔细看 precision；如果漏掉不良更危险，就要更优先看 recall。即使是同一张 confusion matrix，因为先读的错误成本不同，判断也会变化。

真正可检查的结果，会在把 confusion matrix、precision、recall 放在一起看时出现。只要分别数出 `有多少正常产品被白白说成不良`，以及 `有多少真正的不良被漏掉`，就能解释：为什么一个 accuracy 很高的 model，在真实运营里仍然会出问题。

### 示例 1. 工作目标会改变 metric

即使是同一个 classification 问题，只要工作目标不同，最先看的 metric 也会不同。

| 场景 | 更容易先看的 metric | 原因 |
| --- | --- | --- |
| 疾病筛查 | recall | 因为漏掉案例可能造成大问题 |
| spam 拦截 | precision 和 recall 一起看 | 因为既要避免误拦正常邮件，也要避免漏掉 spam |
| 广告点击预测 | 相比 accuracy，更可能先看 precision、recall 和 threshold 之后的表现 | 因为正类比例和成本结构并不简单 |
| 欺诈检测 | 会强看 recall，同时也看 FP 成本 | 因为漏报和误报都会变成运营成本 |

所以，metric 不只是数学公式的问题，它也是 `哪一类错误更痛` 的问题。

如果换成 software engineer 更熟悉的运营场景，会更直观一些。

| 运营问题 | 它和 machine-learning metric 问题像在哪里 |
| --- | --- |
| alert 会不会响太多？ | FP 会不会太多？ |
| 会不会漏掉真实故障？ | FN 会不会太多？ |
| 整体请求处理比例是不是很高？ | 是不是像 accuracy 一样在看整体比例？ |

这个比喻并不是完全同义。但在 `要减少哪一种失败，会决定先看什么数字` 这一点上，非常相似。

### 再用社会现象例子来看

这个问题不只出现在企业服务里。处理社会现象的分类和检测，也会遇到同样的问题。

| 场景 | 更先要看的问题 | 为什么 metric 必须换一种方式读 |
| --- | --- | --- |
| 灾难警报通知 | 真正的危险有多少没被漏掉？ | 如果 recall 低，重大事件可能被漏掉 |
| 福利对象筛选 | 需要帮助的人有多少没有被排除？ | 当 FN 增加时，需要支援的人会被漏掉 |
| 招聘简历自动分类 | 错误淘汰的比例有多高？ | 只看高 accuracy 可能看不到对特定群体的不利 |
| 在线仇恨表达检测 | 在不漏掉危险表达的同时，是否又没有过度封锁正常表达？ | 如果不把 recall 和 precision 一起看，社会成本会变大 |

这张表里重要的一点是：`好的 metric` 并不总是固定成一个。因为在社会现象里，错误会落到谁身上、以什么成本落下去，是不同的。

例如，在灾难警报里，漏报会特别严重；在自动简历分类里，错误淘汰可能成为很大的社会问题。像在线表达检测这种两边成本都高的场景，就必须把 precision 和 recall 一起看。

如果把福利对象筛选极度简化成一个小例子，可以这样理解。

| 场景 | 这个数字意味着什么 |
| --- | --- |
| recall 很低 | 很多真正需要支持的人可能正在被漏掉 |
| precision 很低 | 很多紧急程度较低的案例可能也被一起放进来了 |
| 只有 accuracy 很高 | 整体比例看起来不错，但重要的少数群体可能还是被漏掉了 |

这个例子之所以重要，是因为在社会现象里，常常 `谁被漏掉了`、`谁被错放进来了` 比 `整体答对了多少` 更重要。

### 即使 accuracy 一样，model 也可能完全不同

下面这张表说明：即使 accuracy 一样，解释也可能不同。

| model | accuracy | precision | recall | 读法 |
| --- | --- | --- | --- | --- |
| A | 0.95 | 0.91 | 0.42 | 它说成正类时大多是对的，但漏掉了很多真实正类 |
| B | 0.95 | 0.63 | 0.88 | 它抓到了更多正类，但也可能带来更多误报 |

如果只看 accuracy，这两个 model 看起来一样。但到底选哪一个，会因为你更想减少哪一类错误而不同。

- 高 accuracy 可以是不错的起点
- 但漏掉正类的问题，和无端说成正类的问题，并不是同一件事
- 所以 precision 和 recall 必须一起看

### F1 分数是把两者一起看的尝试

Google glossary 把 F1 score 解释成：把 precision 和 recall 一起使用的代表性概括指标。这里最先该抓住的定义是下面这句。

`F1 score 是当你想把 precision 和 recall 合并成一个数字一起看时使用的折中指标。`

但 F1 也不是魔法。

| 优点 | 限制 |
| --- | --- |
| 能把 precision 和 recall 一起看 | 可能把到底哪一边更重要藏起来 |
| 在不平衡数据里，往往比 accuracy 更有用 | 它仍然不能替代完整的工作成本结构 |

所以，F1 只是一个 `把两边一起看` 的概括，不一定总是最后结论。

这一节认为，比起记很多指标名字，更准确的是按下面这个顺序去读 classification evaluation。

| 阅读顺序 | 先确认什么 | 为什么需要这个顺序 |
| --- | --- | --- |
| 1 | confusion matrix | 因为要先看哪一类错误更多，才能减少 accuracy 幻觉 |
| 2 | 代表[错误案例(error case)](/AiBook/zh/reference/concept-glossary-pinyin/e/#error-case) | 因为即使都是 FN、FP，也要看具体漏掉了什么输入，才能发现数据问题和边界案例 |
| 3 | precision、recall、F1 | 因为先看完错误结构后，才知道哪个数字更能概括那个问题 |
| 4 | 和 baseline 比较 | 因为后面的 P4-8.2 还要再确认，这种分数变化到底算不算真的改进 |

## 练习与示例

### 用 Python 读 metric 的作用

下面这段代码不是实际训练，而是从 confusion matrix 数值出发，直接计算指标的例子。可以操作的值是 `tp`、`tn`、`fp`、`fn`。尤其要确认的是：在 `tn` 非常大的不平衡场景里，即使 accuracy 看起来几乎完美，precision 和 recall 也可能给出完全不同的信号。

输出里把 accuracy、precision、recall、F1 并排看，并思考哪个数字隐藏了当前的错误成本。

```python
# 这个例子用 TP、TN、FP、FN 计算准确率、精确率和召回率，确认评价指标的作用。
tp = 30
tn = 4999000
fp = 950
fn = 20

accuracy = (tp + tn) / (tp + tn + fp + fn)
precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

print("accuracy:", round(accuracy, 4))
print("precision:", round(precision, 4))
print("recall:", round(recall, 4))
print("f1:", round(f1, 4))
```

执行结果可以像下面这样来读。

```text
accuracy: 0.9998
precision: 0.0306
recall: 0.6
f1: 0.0583
```

这组数字会带来一个很重要的感觉。

- accuracy 看起来几乎完美
- 但 precision 非常低
- recall 只有 60% 左右

也就是说，`只看 accuracy 会觉得不错，但实际上问题很多的 model` 是真的可能存在的。

### 用表看同样 accuracy、不同解释

这一次，用一个简单记录来看：即使 accuracy 一样，precision 和 recall 也可能完全不同。

| model | accuracy | precision | recall | 先读出的解释 |
| --- | ---: | ---: | ---: | --- |
| `model_A` | 0.95 | 0.91 | 0.42 | 没必要的警报较少，但漏掉的情况可能很多 |
| `model_B` | 0.95 | 0.63 | 0.88 | 抓到的正类更多，但没必要的警报可能增加 |

这个例子里，重要的不是机械地选出 `谁更好`。更重要的是理解：`只要更重要的东西变了，解释就会跟着变。`

如果把它非常短地改写成运营语句，可以这样写：`Model A 漏掉的情况更多，所以应该先重新看危险案例。Model B 可能会带来更多误报，因此复检成本和 threshold 需要一起重新检查。`

这里的 [threshold](/AiBook/zh/reference/concept-glossary-pinyin/y/#threshold) 是判断正类的边界值。也就是说，看完指标表之后，下一句应该马上接到 `哪一类错误变多了`，以及 `因为这种错误，下一步应该检查什么`。

## Checklist

- 能不能说明为什么只看 accuracy 会漏掉重要的错误成本？
- 能不能说明在当前场景里，为什么会先看 precision，或者为什么会先看 recall？
- 能不能说明为什么应该先看 confusion matrix 和代表错误案例，再去读 metric？
- 能不能说明，评价指标是在用数字概括 model 结果的同时，也把哪种错误被看得更重要一起暴露出来？
- 能不能说明，accuracy 是有用的起点，但不是所有场景的代表指标；即使 accuracy 一样，只要 precision 和 recall 不同，解释和选择也可能改变？
- 能不能说明 precision、recall、F1 各自回答的是什么问题？

## 出处与参考资料

- scikit-learn developers, `Metrics and scoring: quantifying the quality of predictions`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/model_evaluation.html](https://scikit-learn.org/stable/modules/model_evaluation.html){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `Machine Learning Glossary`, 确认日期: 2026-07-26. [https://developers.google.com/machine-learning/glossary/](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }
- C. J. van Rijsbergen, `Foundation of Evaluation`, Journal of Documentation 30(4), 1974. 参考该文确认 information retrieval evaluation 中围绕 precision 和 recall 构成 effectiveness measure 的历史背景。确认日期: 2026-07-26. [https://doi.org/10.1108/eb026584](https://doi.org/10.1108/eb026584){: target="_blank" rel="noopener noreferrer" }
