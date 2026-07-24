# P4-9.3 补充学习：模型选择之后的工具地图

> Section ID: `P4-9.3`
> Version: `v2026.07.23`

_副标题: 高级模型选择、调优自动化与实验追踪分别划分哪一层问题？_

在 P4-8 和 P4-9 里，我们已经建立了这样一条基本流程：先立 model 候选，再放 baseline，然后在 validation 流程内比较 hyperparameter。接下来，通常会出现下面这些名字。

- 信息准则(AIC, BIC)
- AutoML
- benchmark 和 leaderboard
- Bayesian optimization, Hyperband
- nested cross-validation
- experiment tracking

这里要留下的标准，不是去熟悉它们各自的实现细节，而是整理 `这些名字为什么会出现，以及它们各自在处理哪一层的问题`。

这份补充学习也不会从头再讲一遍 hyperparameter 和 tuning 的基本定义。基础抓手仍然放在 P4-9.1、P4-9.2 和 [概念词汇表](/AiBook/reference/concept-glossary/)，这里则只按整体脉络整理那些接在后面的高级名字。

## 这份补充学习的范围

这一节回答下面这些问题。

- 信息准则(AIC, BIC)出现在什么类型的模型选择问题里？
- AutoML 和大规模搜索系统，到底想自动化什么？
- benchmark 和 leaderboard 让人能够比较什么，又可能隐藏什么？
- 为什么 Bayesian optimization 和 Hyperband 会在 grid search 之后出现？
- 为什么 nested cross-validation 和 experiment tracking 会在降低可复现性问题与过高估计风险上变得重要？

这一节先收束 `高级模型选择、调优自动化、实验追踪分别在处理哪些不同问题`。GPU 计算结构会在 Part 5 里重新处理，大规模运维约束会在 Part 6 里重新接回。

## 这份补充学习的目标

- 你可以区分：高级模型选择主题并不都是同一层位的概念。
- 你可以把 AIC/BIC、AutoML、benchmark、experiment tracking 分别解释成不同问题的解法。
- 你可以形成一种视角，区分 `跑得更多` 和 `比得更公平`。

## 把层位分开

这些项目排成一行时看起来很像，但实际上它们回答的是不同的问题。

| 名称 | 主要回答的问题 |
| --- | --- |
| AIC, BIC | 应该怎样把统计模型的复杂度和拟合度放在一起看？ |
| Bayesian optimization, Hyperband | 应该怎样更高效地搜索大量设置值候选？ |
| nested cross-validation | 应该怎样连同模型选择过程一起，进一步减少过高估计？ |
| AutoML | 候选生成、preprocessing、部分 tuning 应该自动化到什么程度？ |
| benchmark, leaderboard | 多个 model 或系统应该用什么共同标准来比较？ |
| experiment tracking | 大量实验结果应该怎样不丢失并重新解释？ |

也就是说，这些东西都和 `选出好的 model` 有关，但它们要解决的细部问题并不一样。

## AIC 和 BIC 放在哪里

AIC、BIC 主要出现在统计模型选择语境里。

- 如果只看是否贴合数据，复杂模型就可能更占优势。
- 人们可能会希望把模型过于复杂这件事，作为一种惩罚反映进去。
- AIC、BIC 就是试图把这种平衡用数字来比较。

在本书当前流程中，机器学习实作的比较结构优先，所以这里先抓住 `为什么会出现“同时看拟合度与复杂度”这种想法` 就足够了。

## AutoML 和大规模搜索系统在自动化什么

AutoML 通常沿着自动化下面这一组内容的方向发展。

1. 生成 preprocessing 候选。
2. 生成 model 候选。
3. 搜索 hyperparameter 候选。
4. 按 validation 分数整理结果。

也就是说，AutoML 更接近的不是 `一个 model 的按钮`，而是 `自动重复模型选择与 tuning 流程一部分的体系`。

不过，即使在这里，同样的风险也还存在。

- 如果 validation 流程不严，即使自动化了，过高估计也仍然会留下来。
- 搜索范围越宽，计算成本就越可能变得更大。
- 结果的可解释性可能下降。

## 为什么 benchmark 和 leaderboard 要分开看

benchmark 是一种装置，目的是让多个 model 在同一份数据和同一套评估规则上比较。leaderboard 则是把这个结果以排名形式展示出来的形式。

它们很有用，但也会制造下面这些错觉。

- 即使排名差距很小，也可能看起来像本质差异。
- 单个数据集上的强项，可能看起来像一般性优势。
- preprocessing、时间预算、tuning 预算的差异可能被藏起来。

因此，benchmark 和 leaderboard 是 `让比较开始的表`，而不是它们本身就等于最终真相。

## 为什么会出现 Bayesian Optimization 和 Hyperband

正如在 P4-9.2 里看到的，grid search 虽然容易解释，但组合数会快速膨胀。于是就会出现下面这些需求。

- 想更快找到重要的轴
- 想在可能性低的候选上少花时间
- 想在有限的计算预算里看到更多候选

在这个脉络里，可以这样读取。

- Bayesian optimization：一种想更聪明地决定 `下一步要试哪里` 的方法
- Hyperband：一种想通过 `尽早停止不太有前景的候选` 来节省预算的方法

## 为什么 nested cross-validation 要被单独提起

如果只把 nested cross-validation 读成“把交叉验证再更复杂地多跑一层”的技巧，它就会变模糊。核心是下面这一点。

`人们希望把用于模型选择的验证，和最终性能估计，更严格地分开。`

也就是说，它是在试图降低这样一种乐观估计：同一套 validation 流程同时被拿来做选择和评估时，容易产生的乐观估计。在小数据上想把比较做得更严格时，这个名字经常会被提起。

这一节把它处理成 `一种试图更强地分开选择与评估的高级验证结构`。

## 为什么 experiment tracking 变成了建模主题

当实验很少时，只靠 notebook 文件名或简单笔记也能撑住。但一旦候选 model、preprocessing、parameter 组合增加，很快就会出现下面这些问题。

- 会忘记哪个实验用了哪些设置
- 分数留下来了，但 data 版本没有留下来
- 很难解释为什么变好了

所以，experiment tracking 不只是简单的记录习惯，而是让模型选择和 tuning 再次变得可解释的基础。

| 必须留下来的东西 | 理由 |
| --- | --- |
| data 版本 | 为了确认是不是同一份数据 |
| preprocessing 规则 | 为了确认输入是不是相同 |
| hyperparameter | 为了解释改了什么 |
| metric | 为了比较什么变好了 |

## 什么时候该先想到哪一种高级工具

高级模型选择工具看起来都像是 `多跑一些的技术`，但实际上它们瞄准的是不同的瓶颈。

| 现在卡住的位置 | 最先想到的类别 | 理由 |
| --- | --- | --- |
| 想把统计模型的拟合度和复杂度放在一起看 | AIC, BIC | 因为它们会把拟合度和复杂度惩罚一起比较 |
| 搜索空间很宽，grid search 太贵 | Bayesian optimization, Hyperband | 因为它们通过下一候选选择或早停来降低搜索成本 |
| 想更严格地分开选择和最终评估 | nested cross-validation | 因为它会进一步降低选择过程里的乐观偏差 |
| 想自动重复候选生成和一部分 tuning | AutoML | 因为它会自动化 preprocessing、候选生成和部分搜索 |
| 实验太多，开始失去比较依据 | experiment tracking | 因为它能重新追踪 data 版本、规则、分数和设置变更理由 |

这张表的核心，不是背名字，而是区分：会因为 `现在的瓶颈是什么`，而出现不同的工具。

## 案例及示例

### 案例 1. 实验很多，但说不清为什么某个组合更好时

一个推荐系统团队正在同时跑多个 model 候选和 tuning 组合。人们最先看的标准，是 `最近点击`、`类型偏好`、`相似用户行为` 这类信号。

几天之后，分数表还在，但大家已经开始记不清：哪个实验用了什么 preprocessing 规则、它对应什么 hyperparameter 组合、是不是用了同一个 data 版本。在这种情况下，就算 leaderboard 上有一个高分摆在那里，也很难说明它到底是不是真的来自一次公平比较。像 AutoML、benchmark、nested cross-validation 这些名字之所以会被需要，最终也是为了把这种规模下的比较处理得更系统。

在这个场景里，这些高级模型选择工具都应该被读成：分别解决不同问题的装置。benchmark 和 leaderboard 用来搭比较板，AutoML 自动化候选生成和部分搜索，nested cross-validation 更严格地分开选择与评估，而 experiment tracking 则让这一切过程都能重新被解释。

可确认的结果，会立刻表现在记录项目有没有留下来。如果 data 版本、preprocessing 规则、hyperparameter、metric、执行时间都一起留下来了，就能重新检查为什么某个组合更好；但如果只剩分数，这个比较就不容易被复现。

```mermaid
--8<-- "assets/part-04/chapter-09/p4-9-3-mermaid-01-zh.mmd"
```

## Checklist

- 有没有把 AIC/BIC、搜索技术、AutoML、tracking 混成同一层位的解法？
- 现在需要的到底是更宽的搜索、更严格的验证分离，还是更好的记录体系，你有没有区分开？
- 你看到的是否不只是 leaderboard 的高分，还包括比较条件和记录可保留性？
- 你能不能不把 AIC/BIC 和 hyperparameter tuning 混成同一层位的问题？
- 你能不能不把 benchmark 排名和真实泛化性能立刻视为同一回事？
- 你能不能解释：为什么 experiment tracking 不是 `便利功能`，而是可复现性的一部分？
- 你能不能说明，AIC/BIC 是统计模型选择的语言，而 Bayesian optimization 与 Hyperband 是降低搜索成本的语言？
- 你能不能说明，nested cross-validation 是更严格分开选择与评估的语言，而 AutoML、benchmark、leaderboard、experiment tracking 是把实验做得更大规模的语言？

## 出处与参考资料

- scikit-learn developers, [Tuning the hyper-parameters of an estimator](https://scikit-learn.org/stable/modules/grid_search.html){: target="_blank" rel="noopener noreferrer" }，确认日期：2026-07-01。
- Takuya Akiba et al., [Optuna: A Next-generation Hyperparameter Optimization Framework](https://arxiv.org/abs/1907.10902){: target="_blank" rel="noopener noreferrer" }，确认日期：2026-07-01。
- MLflow, [Tracking](https://mlflow.org/docs/latest/ml/tracking/){: target="_blank" rel="noopener noreferrer" }，确认日期：2026-07-01。
