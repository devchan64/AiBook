# P4-15.1 随机森林(random forest)

> Section ID: `P4-15.1`
> Version: `v2026.07.26`

在 P4-14 里，我们看过[决策树(decision tree)](/AiBook/zh/reference/concept-glossary-pinyin/d/#decision-tree)为什么既直观， 又容易掉进[过拟合(overfitting)](/AiBook/zh/reference/concept-glossary-pinyin/g/#overfitting)。 尤其是我们确认过： 即使调整 `max_depth`、`min_samples_leaf`、`ccp_alpha`， 单棵树的结构摇摆也不一定会完全消失。 于是下一个问题自然出现。

有没有办法既保留树的优点， 又减少单棵树过度摇摆的问题？

这个问题就是[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)的出发点。

随机森林是把许多训练得略有不同的决策树的预测汇集起来， 尝试得到比单棵树更稳定判断的模型。

也就是说，随机森林不是 `把树丢掉的模型`， 而是 `把很多树聚在一起并减少其弱点的模型`。

这一节说明[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)、[集成(ensemble)](/AiBook/zh/reference/concept-glossary-pinyin/j/#ensemble)、[bootstrap](/AiBook/zh/reference/concept-glossary-pinyin/b/#bootstrap)、`特征随机选择` 的基本含义。 后面的 Section 会沿着这些抓手继续往前推进， 而通过多棵树的合意来降低摇摆的基础直觉， 也会通过这一节和对应的概念词条重新连接。

## 随机森林先收束的问题

本节回答以下问题。

- 为什么随机森林要使用多棵树？
- [bootstrap](/AiBook/zh/reference/concept-glossary-pinyin/b/#bootstrap)、[max_features](/AiBook/zh/reference/concept-glossary-pinyin/m/#max-features)、`averaging` 分别起什么作用？
- 为什么它会比单棵树看起来更稳定？
- 在分类与回归里，随机森林是怎样合并输出的？
- [n_estimators](/AiBook/zh/reference/concept-glossary-pinyin/n/#n-estimators)、[max_features](/AiBook/zh/reference/concept-glossary-pinyin/m/#max-features)、[bootstrap](/AiBook/zh/reference/concept-glossary-pinyin/b/#bootstrap)、[oob_score](/AiBook/zh/reference/concept-glossary-pinyin/o/#oob-score) 各自是什么意思？

这一节会先收束 `为什么把多棵树聚合起来，会试图做出比单棵树更稳定的判断` 这个问题。 特征重要度会在 P4-15.2 继续，OOB(out-of-bag) 分数的评价解读会在 P4-15.3 继续，Extra Trees 比较会在补充学习 P4-15.4 继续，与梯度提升(gradient boosting)的对比会在 P4-16.1、P4-16.2 继续。

## 随机森林要留下的判断标准

- 你可以把随机森林解释成 `多棵随机化树的平均 / 聚合模型`。
- 你可以说明为什么需要 bootstrap 抽样与特征随机选择。
- 你可以理解随机森林是在尝试降低决策树的方差(variance)。
- 你可以在入门层面区分代表性超参数(hyperparameter)的作用。

## 学习背景

读到决策树这一章时， 读者通常会同时拥有两种感觉。

- 感觉不错的地方：容易阅读，而且看起来很适合表格型数据
- 感到不安的地方：树一深起来，好像就会记住太多东西

随机森林正是在这种张力上出现的。

| 第 14 章留下的问题 | 15.1 想回答的方向 |
| --- | --- |
| 如果单棵树会摇摆，该怎么办？ | 把很多棵树放在一起，对摇摆做平均 |
| 能不能减少被例外样本拉走的分支？ | 让每棵树都不一样，使错误不要绑在一起 |
| 会不会完全失去可解释性？ | 会损失一部分，但往往能换来稳定性和性能 |

所以，随机森林并不是 `否定决策树的弱点`， 而是 `通过多棵树的集成结构来缓和这些弱点`。

再加上一点，这一节会直接接回 Part 4 一直在整理的比较记录结构。 把随机森林列为候选时， 不能只留下 `它用了很多树` 这一句。 还应该一起记下： `比起单棵树，哪些错误案例变得没那么摇摆`、 `还有哪些模糊案例仍然留下来`、 `接下来还要看哪一种森林设置`。 即使平均分数看起来差不多， 也还是要单独去看哪一个模型更常重复某类错误， 以及哪一个模型在 seed 改动后更稳定。

| 建议一起留下的记录 | 为什么需要 |
| --- | --- |
| 单棵树与随机森林比较 | 为了看集成到底稳定了什么 |
| 残留错误案例 | 为了重看即使聚合很多树也仍然错或仍然模糊的案例 |
| 摇摆是否减少 | 为了看的不是一次高分，而是平均稳定性是否变好 |
| 下一步实验问题 | 为了决定接下来调 `n_estimators`、`max_features` 还是 `bootstrap` |

树模型家族中的提问变化可以整理成下面这样。

| 模型 | 先抓住的问题 | 更强调的标准 |
| --- | --- | --- |
| 决策树 | 应该按什么提问顺序把数据拆开？ | 易读的分支结构与 leaf 规则 |
| 随机森林 | 怎样减少单棵树的摇摆？ | 多棵树之间的多样性与平均稳定性 |
| 梯度提升 | 下一阶段怎样修正前一阶段的误差？ | 顺序修正与 residual 减少 |

所以对随机森林来说，核心不是 `用了更多的树`， 而是 `把不同树的摇摆汇总后再压低`。 只要这个标准固定下来， 后面的梯度提升就不会只是又一个集成名字， 而会被读成 `稳定性中心集成` 与 `误差修正中心集成` 的对比。

### 什么时候适合优先把随机森林列为候选

当你想在表格型数据上快速建立一个更稳定的默认候选， 并愿意牺牲一部分单棵树可解释性的时候， 随机森林往往很强。

| 当前问题状态 | 优先考虑随机森林的理由 | 先检查什么 |
| --- | --- | --- |
| 单棵树经常摇摆 | 因为多棵树平均可以降低方差 | 分数会不会随着 seed 或切分而明显变化 |
| 需要一个强的表格型数据默认候选 | 因为能保留树模型优点，同时更容易得到稳定性 | depth 和 leaf 大小是否已经受控 |
| 怀疑线性模型漏掉了非线性模式 | 因为树集成可以更灵活地容纳复杂分支结构 | 是否同时在看过拟合与计算成本 |
| 在可解释性之前先要稳一点的 baseline | 因为它往往比单棵树更不敏感 | 还剩下哪些错误案例 |
| 之后还想一起看 importance 或 OOB | 因为树模型家族自带内部检查抓手 | 是否没有过度相信 importance 和 OOB |

这个表的重点，是把随机森林读成 `降低单棵树摇摆的稳定性候选`， 而不是简单的 `多用几棵树`。

## 主要学习内容

### 叫做集成(ensemble)的大框架

scikit-learn 用户指南把 ensemble methods 解释为： 通过组合多个 base estimator 的预测， 来获得比单个 estimator 更好的 generalizability 与 robustness 的方法。

随机森林就是这个集成家族里的代表例子之一， 它使用了很多树。

随机森林是一种把许多略有不同的树的判断聚起来， 尝试得到更稳定答案的集成方式。

`与其直接相信一个模型的判断，不如把几个略有不同的模型判断聚在一起，让答案更稳定。`

一旦看到这个大框架， 随机森林为什么会出现就更清楚了。

### 随机森林是什么样的模型

scikit-learn 文档把 random forests 解释成 `基于决策树的 averaging algorithm`。 每棵树都在训练集上用有放回抽样(with replacement)得到的 bootstrap sample 来训练， 并且每个 split 只看一个随机特征子集。

这里有两种关键随机性。

1. 样本抽得不一样。
2. 每个分支看到的特征也不一样。

最后再把很多树的预测聚起来。

压成一句话就是：

`随机森林不会把完全相同的数据喂给每一棵树。它让每棵树看到略有不同的数据和略有不同的特征候选，再在最后把结果合起来。`

### 先用一个画面来读

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-01-zh.mmd"
```

这个图里最重要的一点是 `每棵树看到的东西并不完全一样`。 这样才会留下制造不同错误的空间， 后面也才有机会把这些错误拿来做平均或投票。

### 为什么光把同一棵树重复很多次还不够

初学者在这里常会问：

`如果把决策树训练 100 次，不就等于随机森林了吗？`

核心问题在于 `这 100 棵树是不是真的彼此不同`。 如果用几乎一样的数据、 一样的特征候选、 一样的规则去建立很多树， 那它们犯的错也可能朝几乎相同的方向重复。 那样的情况更接近 `把同一种判断大声重复很多次`， 而不是 `把许多真正不同的判断聚起来`。

随机森林的重要性，不在于只增加了 `树的数量`， 而在于它制造了 `树彼此不同的理由`。

| 比较场景 | 实际发生的事 | 应该读出的结论 |
| --- | --- | --- |
| 把几乎同一棵树复制很多次 | 分支和错误几乎朝同一方向重复 | 做平均也不太能减少摇摆 |
| 只改变 bootstrap 样本 | 每棵树看到的案例组合略有不同 | 被例外样本拉走的程度会有些变化 |
| 再把特征候选也随机限制 | 第一处分裂和后续路径会分得更开 | 树彼此不像，合意就更有意义 |
| 最后做聚合 | 单棵树的过度自信会被缓和 | 整个森林更容易被读成稳定判断 |

所以，随机森林的核心不是 `很多树`， 而是 `把彼此更不像的树做聚合`。

### 为什么聚很多棵树会更稳定

决策树常被说成 high-variance 模型。 scikit-learn 用户指南也说明， 单棵决策树方差大，而且容易过拟合。 随机森林就是通过组合许多 diverse tree 来降低这种方差。

读者要抓住的直觉很简单。

- 一棵树可能被某个例外案例拉得太厉害
- 另一棵树因为 bootstrap 样本不同，可能不会那么强烈地看到那个例外
- 还有一棵树则可能因为分支特征候选不同，而走出完全不同的路径
- 把很多树的答案聚起来后，单棵树的过度摇摆就会显得没那么强

也就是说，随机森林通常选择的是 `很多棵树的合意`， 而不是 `一棵树的强烈自信`。

如果改成项目笔记语言，可以写成下面这样。

| 记录项 | 例子 |
| --- | --- |
| baseline 或单一候选 | `single tree` |
| ensemble 候选 | `random forest` |
| 残留 review 案例 | `customer X 仍然模糊` |
| 摇摆变化 | `即使改 seed，test 分数差也变小了` |
| 下一个问题 | `树再多一点，稳定性会不会更好` |

有了这个表， 随机森林这一节就会被读成 `比较候选 -> 残留错误案例 -> 下一个问题`。 它的优势不是从一个平均数字里最明显地跳出来， 而是在看 `残留失败模式是不是没那么摇摆` 时更清楚。

因此，随机森林在实务上常被考虑的场景， 大体是 `单棵树太摇摆，但数据规模或结构又还不到自然直接跳去神经网络的表格型问题`。 这时真正期待的不是 `一次最好的分数`， 而是 `一个更稳的默认候选`。

### bootstrap 做了什么

随机森林的第一种随机性来自 bootstrap sampling。

scikit-learn 文档说明， 每棵树都是用从训练集里有放回抽取出的 bootstrap sample 建起来的。 因为是有放回抽样， 某些样本可能在同一棵树里出现两次， 也有些样本会完全没被抽到。

这里的直觉是：

`每棵树都不是在一份完整数据的拷贝上学习。每棵树都经历了略有不同的训练经验。`

想一个非常小的例子。

如果原始数据是 `A, B, C, D, E`， 某个 bootstrap sample 可能长这样。

- tree 1: `A, B, B, D, E`
- tree 2: `A, C, D, D, E`
- tree 3: `B, C, C, D, E`

即使都从同一份原始数据出发， 每棵树的视角也会变得有些不同。

压成一句话：

`bootstrap 会给每棵树制造不同的训练经验，让所有树不会把同一个例外案例完全一样地记住。`

### 特征随机选择做了什么

第二种随机性来自特征子采样(feature sub-sampling)。

scikit-learn 文档说明， 每个 split 只会检查一个随机的候选特征子集。 负责这个作用的代表超参数就是 `max_features`。

为什么需要它？

如果有一个很强的特征总能统治每棵树的第一处分裂， 那这些树就会变得太像。 这样即使聚了很多树， 整个森林的多样性也仍然不足。

因此，一旦每个 split 只允许看到部分特征候选：

- 某棵树可能主要按 feature A 分裂
- 另一棵树可能先看 feature B
- 还有的树可能会走出别的绕行路径

所以，对 `max_features` 更重要的读法， 不是把它只看成速度选项， 而是把它看成 `让树彼此更不像的装置`。

把 bootstrap 和 `max_features` 放在一起看， 它们的角色差异就更清楚了。

| 装置 | 直接改变什么 | 想阻止什么问题 |
| --- | --- | --- |
| `bootstrap` | 每棵树看到的样本束 | 所有树都被完全相同的案例拉走 |
| `max_features` | 每个 split 能看到的特征候选 | 同一个特征统治所有树 |
| `averaging` 或 vote | 最后的预测合并方式 | 一棵树的过度自信支配最终答案 |

有了这张表， 随机森林就不再只是一个模糊的 `随机混一混`。 它会更像是分别设计了 `样本多样性`、`分支多样性`、`最终聚合` 的结构。

### 在分类和回归里怎样合并输出

随机森林既能用于分类(classification)，也能用于回归(regression)。 变化的是很多棵树的输出怎样合并。

| 问题类型 | 多棵树的输出 | 最终聚合 |
| --- | --- | --- |
| 分类 | 每棵树的 class 或 class probability | 投票或概率平均 |
| 回归 | 每棵树的预测数值 | 平均 |

scikit-learn 文档说明， 在分类森林里， 树的概率预测会被做平均。 `majority vote` 仍可作为大的直觉， 但如果按 scikit-learn 的实现细节来读， 概率平均会更准确。

### 把随机森林读成一个流程

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-02-zh.mmd"
```

这里的核心不是 `树更多` 本身， 而是 `能够制造不同错误的树`。

## 细化学习内容

### 代表性超参数应该怎样读

按 API 文档来看， 在随机森林里读者最先应该认识的大致是这些抓手。

| 超参数 | 先读什么问题 |
| --- | --- |
| `n_estimators` | 要造多少棵树？ |
| `max_features` | 每个 split 要看多少特征候选？ |
| `bootstrap` | 每棵树是否用 bootstrap 样本训练？ |
| `max_depth` | 每棵树最多能长多深？ |
| `min_samples_leaf` | 是否要避免每棵树长出太小的 leaf？ |
| `oob_score` | 是否要用 bootstrap 留下的样本做内部检查？ |

在 15.1 这个层次， 最重要的三个是：

- `n_estimators`：森林大小
- `max_features`：树的多样性能有多大
- `bootstrap`：每棵树是否拥有不同训练经验

与其只背名字， 更重要的是一起读出值变化后会发生什么。

| 超参数 | 改值后最先出现的变化 | 首先要警惕什么 |
| --- | --- | --- |
| `n_estimators` | 树变多后，平均判断可能更稳定 | 计算成本会上升，而且改善可能很快变平 |
| `max_features` | 树会彼此更不像或更像 | 太大则树太像，太小则单棵树可能太弱 |
| `bootstrap` | 树与树之间会出现训练经验差异 | 如果关掉，树的多样性会下降，森林优势也会变弱 |
| `max_depth` | 每棵树的复杂度会变化 | 太深的话，森林里的每棵树仍然可能过度记忆例外 |
| `min_samples_leaf` | 它会阻止 leaf 切得过细 | 太大又可能让必要的分支变钝 |

在实务里， 可以先这样读。

- 如果分数还可以，但随着 seed 改动会晃，就先看 `n_estimators` 和 `max_features`。
- 如果感觉所有树都太像，就怀疑 `max_features` 会不会太大。
- 如果每棵树看起来都在过度记忆例外，也要一起看 `max_depth` 与 `min_samples_leaf`。

### 什么是 OOB(out-of-bag)

一旦使用 bootstrap sampling， 某些样本就会对某棵树来说没有被拿去训练。 scikit-learn 文档说明， 这些被留在外面的样本， 可以用来做 OOB(out-of-bag) 的泛化误差估计。

因此，OOB 可以被理解成： 利用每棵树没有见过的样本， 得到一种部分接近验证的感觉。

但 OOB 不应该被理解成 `能替代所有评价流程的万能装置`。 在这一节里， 我们只先固定它的名字和角色。

不过，仍然有必要知道为什么这里会提到 OOB。 因为随机森林使用了 bootstrap， 于是自然会出现 `某棵树没学过的样本`。 OOB 只是把这些剩下来的样本再次利用。 所以它不是从外面硬贴上的评价技巧， 而更自然地应该被读成 `跟着 bootstrap 一起出现的内部检查抓手`。

## 案例与示例

### 案例 1. 在客户流失预测里，为什么多棵树的合意会比一棵规则更好

某个订阅服务团队先用决策树做客户流失(churn)预测。 人先看到的标准包括 `最近访问次数`、`延迟支付`、`咨询次数`、`会员等级` 等信号。

单棵树的规则确实容易阅读， 但边界很容易被少数例外客户拉走。 某些数据切分下它看起来很准， 换一个切分时， 第一处分裂与预测结果又会轻易摇晃。 团队想保留树的提问流程， 同时减少单棵树过度敏感的问题。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-1-mermaid-03-zh.mmd"
```

在这个场景里， 随机森林应该被读成 `不是把树抛弃的方法`， 而是 `把许多略有不同的树聚起来形成合意的方法`。 如果 bootstrap 让每棵树看到略有不同的客户组合， 而 `max_features` 又让分支候选不同， 那么单棵树被某个例外拉走的现象， 在整个森林里平均起来就可能弱很多。

如果压成工作笔记， 顺序大致是下面这样。

| 阶段 | 团队实际看到什么 |
| --- | --- |
| 人先看到的标准 | `最近访问次数`、`延迟支付`、`咨询次数`、`会员等级` |
| 单棵树的限制 | 少数例外客户会轻易摇动第一处分裂与边界 |
| 随机森林改变的地方 | 多棵树看到不同客户组合与不同分支候选 |
| 最终判断方式 | 看的不是一棵树的过强规则，而是很多树的合意 |
| 可验证结果 | 不只看最高分，也一起看 seed 间摇摆与残留错误案例 |

可验证的结果不只出现在单棵树与随机森林的 test 分数里， 还会出现在多组随机 seed 下的波动比较里。 如果平均稳定性比一次最高分更明显地改善， 我们就能说明随机森林的优点不是 `更复杂的规则`， 而是 `更不摇摆的合意`。

### 案例 2. 在实务场景里可以怎样读

随机森林在下面这些场景里尤其容易这样去读。

| 工作场景 | 为什么随机森林会显得有利 |
| --- | --- |
| 客户流失预测 | 它不那么容易被单棵树的例外分支拉走，也容易从表格型数据起步 |
| 贷款审核辅助 | 它能抓住非线性关系，同时保留树模型家族的感觉 |
| 设备异常检测 | 它能用很多树去拆开复杂的传感器组合 |
| 营销响应预测 | 它比过度依赖一两个特征的单棵树更容易得到稳定性 |

反过来，如果可解释性是最高优先级， 而且每一次预测都需要立刻用单条规则来解释， 随机森林就可能比单棵决策树更不占优。 因为整片森林比一棵树难读得多。

## 练习与示例

### Python 示例：比较一棵树和很多棵树

这个例子是在同一个 iris 分类问题上， 比较一棵决策树与一个随机森林的小练习。

- 问题场景：观察一棵树与一片森林的差别
- 输入(input)：iris 的 4 个特征
- 标签(label)：品种 class
- 要确认的概念：
  - random forest 会聚合很多棵树
  - 即使是同一份数据，test 性能与稳定性也可能不同
  - `n_estimators` 与森林大小直接相关

可以改动的值：

- `n_estimators`：比较 10、50、100 等森林大小，同时观察分数和计算时间。
- `random_state`：观察单棵树和森林面对同样 seed 变化时，摇摆程度有何不同。
- `max_features`：比较默认值和 `None`，看看树的多样性减少时会发生什么。

```python
# 这个例子在 iris 分类中并排比较单棵决策树和随机森林的分数与结构。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

single_tree = DecisionTreeClassifier(random_state=42)
single_tree.fit(X_train, y_train)

forest = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)
forest.fit(X_train, y_train)

print("single tree")
print("  train accuracy:", round(single_tree.score(X_train, y_train), 3))
print("  test accuracy :", round(single_tree.score(X_test, y_test), 3))
print("  depth         :", single_tree.get_depth())
print("  leaves        :", single_tree.get_n_leaves())
print()

print("random forest")
print("  train accuracy:", round(forest.score(X_train, y_train), 3))
print("  test accuracy :", round(forest.score(X_test, y_test), 3))
print("  trees         :", len(forest.estimators_))
print("  first depth   :", forest.estimators_[0].get_depth())
```

示例输出如下。

```text
single tree
  train accuracy: 1.0
  test accuracy : 0.911
  depth         : 5
  leaves        : 8

random forest
  train accuracy: 1.0
  test accuracy : 0.911
  trees         : 100
  first depth   : 4
```

光看这个很小的结果， 两者可能会显得差不多。 所以接下来还要继续看的就是： `random_state 改变时，它们会怎么摇晃？`

### Python 示例：观察摇摆差异

这个例子会在同一个数据切分上， 用多个随机 seed 反复比较单棵树与随机森林的 test 表现会怎样摇晃。

问题场景：

- 做模型比较时，不只要看最高分，还要一起看在多次切分下分数会不会摇晃

输入(input)：

- iris 数据集
- 单棵决策树模型
- 随机森林模型
- 多个随机 seed

期望输出(output)：

- 每个 seed 下的树分数与随机森林分数
- 两种模型的平均值或摇摆差异

要确认的概念：

- 随机森林的优势，往往比起最高分，更容易在 `摇摆减少` 上看出来
- 比较多个 seed，是阅读稳定性最简单的方法

可以改动的值：

- `range(10)`：把重复 seed 数改成 5 或 20，观察平均值是否更稳定。
- `n_estimators`：比较 10 和 100，看看树的数量怎样影响摇摆。
- `max_depth`：同时限制单棵树和森林内部树的深度，观察平均分数怎样变化。

```python
# 这个例子比较多个 random_state 下单棵树和随机森林的 test 分数波动。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

X, y = load_iris(return_X_y=True)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

tree_scores = []
forest_scores = []

for seed in range(10):
    tree = DecisionTreeClassifier(random_state=seed)
    tree.fit(X_train, y_train)
    tree_scores.append(tree.score(X_test, y_test))

    forest = RandomForestClassifier(n_estimators=100, random_state=seed)
    forest.fit(X_train, y_train)
    forest_scores.append(forest.score(X_test, y_test))

print("single tree test scores :", [round(s, 3) for s in tree_scores])
print("forest test scores      :", [round(s, 3) for s in forest_scores])
print("tree avg                :", round(sum(tree_scores) / len(tree_scores), 3))
print("forest avg              :", round(sum(forest_scores) / len(forest_scores), 3))
```

示例输出如下。

```text
single tree test scores : [0.978, 0.933, 0.911, 0.933, 0.911, 0.911, 0.933, 0.911, 0.911, 0.933]
forest test scores      : [0.978, 0.956, 0.933, 0.933, 0.933, 0.933, 0.956, 0.933, 0.933, 0.956]
tree avg                : 0.927
forest avg              : 0.944
```

这个例子想说明的点是下面这些。

1. 单棵树在某些 seed 下也可能表现很好。
2. 但随机森林通常平均起来更不摇摆，也更稳定。
3. 随机森林的价值，不是来自 `完全新的结构`，
而是来自 `把不稳定的树做平均`。

## 检查清单

- 你能把随机森林解释成 `多个 randomized decision tree 的聚合模型` 吗？
- 你是否正按同类错误案例去比较，而不是只看单次最高分，来确认它是否真的比单棵树更少摇摆？
- 你是否理解 bootstrap 和特征随机选择是为了让树彼此没那么像？
- 你能说明它是想通过汇总多棵树的预测来降低单棵树的方差(variance)吗？
- 你是否把随机森林的优势读成平均稳定性，而不是一次性的最高分？
- 你是否知道它的可解释性可能会比单棵树更低？
- 你是否能区分 `n_estimators`、`max_features`、`bootstrap` 里当前更重要的把手是什么？

## 出处与参考资料

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- Leo Breiman, `Random Forests`, Machine Learning, 45(1), 5-32, 2001, 确认日期: 2026-07-26. [https://doi.org/10.1023/A:1010933404324](https://doi.org/10.1023/A:1010933404324){: target="_blank" rel="noopener noreferrer" }
