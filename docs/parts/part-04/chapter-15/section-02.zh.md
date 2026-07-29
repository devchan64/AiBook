# P4-15.2 特征重要度(feature importance)

> Section ID: `P4-15.2`
> Version: `v2026.07.26`

在 P4-15.1 里，我们看过[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)为什么能通过聚合很多棵树， 得到更稳定的预测。 接下来立刻会冒出一个问题。

这片森林在做判断时，到底把什么看得更重要？

这个问题就是[特征重要度(feature importance)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)的出发点。

特征重要度是一个把模型更常使用、或使用得更重的特征总结成数字的方法， 但如果把这个数字直接读成原因或真相的排序，就会很危险。

特征重要度是有用的总结， 同时也是带着解释陷阱的工具。

这一节不会再长篇重复随机森林的基本定义。 `通过多棵树的合意来降低摇摆` 这个核心直觉， 会通过 P4-15.1 和[随机森林(random forest)](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest)条目重新连接。 这里聚焦的只是： 应该怎样解释这片森林把什么看得重要。

## 特征重要度先收束的问题

本节回答以下问题。

- 在随机森林里，特征重要度是怎样产生的？
- [`feature_importances_`](/AiBook/zh/reference/concept-glossary-pinyin/s/#random-forest) 是什么意思？
- impurity-based importance 和置换重要度(permutation importance)有什么不同？
- 为什么一个看起来很重要的数字仍然可能制造误解？
- 部分依赖图(PDP, partial dependence plot)、SHAP与 importance 相比，到底在问什么不同的问题？
- 为什么不能把 importance 的解释直接跳成[因果推断(causal inference)](/AiBook/zh/reference/concept-glossary-pinyin/y/#causal-inference)？
- 当真实数据里相关特征(correlated features)非常强时，需要怎样更保守的解释策略？

这一节不会只停在画出 importance 解释的外围边界。 它还会在当前 Section 里直接回收： `当数字总结不够时该再看什么`、 `为什么要与原因解释分开`、 以及 `相关性很强时应该怎样更保守地读`。

| 项目 | 本节里的处理方式 |
| --- | --- |
| PDP(partial dependence plot)、SHAP | 本节会直接回收它们和 importance 在“问题类型”上的差别，但不会展开全部实现选项 |
| importance 的因果推断视角 | 本节会直接回收为什么要区分 `模型使用量` 与 `因果效果`，但不会展开完整估计流程 |
| 强相关真实大数据的解释策略 | 本节会直接回收到最小解释顺序，但不会展开完整生产流水线 |

本节的重点，是先建立一种 `阅读数字的态度`。

## 特征重要度要留下的判断标准

- 你可以把特征重要度解释成 `模型内部使用量的总结`。
- 你可以区分基于不纯度的重要度(MDI, mean decrease in impurity)与置换重要度(permutation importance)。
- 你可以说明特征重要度并不直接等于因果关系(causality)或真正的原因排序。
- 你可以说明为什么相关特征(correlated features)与高基数特征(high-cardinality feature)会扭曲解释。

## 学习背景

学完随机森林后， 读者很容易自然期待下面这些事。

- 这片森林预测得不错
- 森林里有很多树
- 那它应该也能很好地告诉我什么最重要

这种期待只对了一半。

| 期待 | 现实里更接近的是 |
| --- | --- |
| importance 数字大，就说明它是原因 | 它更接近说明模型大量使用了它 |
| importance 数字低，就说明这个特征没用 | 它可能与别的特征重叠，或被别的特征替代了 |
| importance 永远是公平的排序 | 计算方式不同，本身就可能带来偏差 |

所以 15.2 不是一节关于 `怎样相信 importance 数字` 的课， 而是一节关于 `怎样不要过度相信 importance 数字` 的课。

这里也把记录结构一起固定下来。 这一节不只是要把数字排个序。 它还是一节要留下 `观察到什么重要度现象`、 `哪些还在解释边界内`、 以及 `下一步数据补强问题是什么` 的课。 即使两份重要度排序看起来相似， 也还是要另外检查： 哪些特征组合在互相代替， 以及重要度差异是不是真的连到了性能模式差异。

| 建议一起留下的记录 | 为什么需要 |
| --- | --- |
| 观察到的重要度排序 | 为了看模型更多地使用了哪些特征 |
| 解释边界句子 | 为了不把 importance 数字直接写成原因排序 |
| 需要复查的特征 | 为了重新检查相关特征或 high-cardinality 列 |
| 下一个问题 | 为了决定接下来补采什么特征，或要做什么比较实验 |

### 什么时候应该尤其小心 importance 数字

importance 很方便， 但某些数据结构特别容易让解释被过度相信。

| 看见的场景 | 为什么要先小心 | 一起检查什么 |
| --- | --- | --- |
| 拥有很多唯一值的列排到了前面 | 可能是 high-cardinality 偏差 | 和 permutation importance 对照 |
| 有几列几乎表达同样意思的特征 | importance 可能被分散到可替代特征上 | 检查相关特征组 |
| importance 差距很小，但排名分开了 | 很容易把排名差误读成真相差 | 和实际性能变化一起看 |
| importance 很高，但解释却很别扭 | 模型使用量与真实世界原因不是同一件事 | 一起看领域含义和案例 |
| 某个低 importance 特征看起来想删掉 | 它可能只是与别的特征一起发挥作用 | 做删除前后比较实验 |

这个表的重点，不是要你丢掉这个数字。 而是让读者先看见： `什么时候这个数字特别容易引发误解。`

## 主要学习内容

### 特征重要度来自什么想法

scikit-learn 用户指南解释说， 在树里，上方的 decision node 会影响更多样本的最终预测， 而相对重要度可以通过 每个 split 降低了多少 impurity 来估计。 把这个想法在许多随机化树上做平均， 就会得到 mean decrease in impurity，也就是 MDI。

特征重要度，就是把某个特征多频繁、又多大程度地帮助了更好的 split， 总结成一个值。

`如果一个特征经常带来较大的 split 改善，就把这个特征读成更重要。`

这个解释一开始看起来很自然。 而且在实务里也很快、很方便。 但必须马上加上一句重要限定。

`这个值总结的是模型在训练数据里如何使用分支。`

importance 更接近 `模型内部的使用记录`， 而不是世界里的真正重要程度， 也不是原因大小本身。

### 什么是 MDI(mean decrease in impurity)

scikit-learn 文档把树集成的特征重要度 解释成 impurity-based feature importance， 并把在多棵树上的平均称作 MDI。

MDI 的计算顺序如下。

1. 看树里每个 split 让 impurity 降低了多少。
2. 把这部分降低量记到产生这个 split 的 feature 上。
3. 在一棵树里加总。
4. 在整个森林上做平均。
5. 再归一化(normalize)到总和为 1。

简短画出来就是：

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-01-zh.mmd"
```

正因为有这个结构， `feature_importances_` 计算很快， 而且在训练完随机森林后就能立刻读取。

### 为什么上层 split 会显得更大

scikit-learn 文档说明， 树上层分支使用到的特征， 会影响更多输入样本的最终预测。 所以即使 impurity 降低量相同， 改变了更多样本流向的 split， 也会在最终 importance 里显得更大。

压成一句话就是：

`树前面的提问分开了更多样本，后面的提问只分开少数样本。所以前面 split 用到的特征，更容易在总 importance 里显得大。`

### `feature_importances_` 应该怎样读

API 文档把 `feature_importances_` 说明为 impurity-based feature importances。 这些值为正， 而且总和是 1.0。

第一层读法如下。

| 数字样子 | 含义 |
| --- | --- |
| 值大 | 模型相对更多地使用了这个特征 |
| 值小 | 模型相对更少地使用了这个特征 |
| 总和为 1 | 它应该被读成相对占比，而不是绝对分数 |

这里关键的是 `相对占比` 这个说法。

例如如果 importance 是：

- `visits = 0.45`
- `late_payment = 0.35`
- `support_calls = 0.20`

那可以读成： 在这个模型内部的分支标准里， `visits` 扮演了最大的作用。 但这不等于 `访问次数是现实世界里最强的原因`。

### 为什么还需要 permutation importance

scikit-learn 文档把 permutation importance 作为 impurity-based feature importance 的替代或补充视角提出。 permutation importance 会看： 当某一个特征的值被随机打乱后， 模型性能会变差多少。

如果说 MDI 更接近 `内部使用记录`， 那么 permutation importance 就更接近 `如果把这个特征破坏掉，真实预测性能会摇多少`。

对比起来是这样。

| 方式 | 核心问题 |
| --- | --- |
| MDI | 这个特征在分支里被用了多少次、用了多大？ |
| permutation importance | 如果把这个特征打乱，模型性能会掉多少？ |

这个差异非常重要。 一个更接近 `模型内部的使用痕迹`， 另一个更接近 `通过性能来检查依赖程度`。

### 把 permutation importance 读成流程

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-02-zh.mmd"
```

这个流程之所以重要， 是因为它让读者重新把 importance 读成 不是 `数字的属性`， 而是 `性能变化实验`。

## 细化学习内容

### 为什么要小心 impurity-based importance

scikit-learn 用户指南对 impurity-based importance 提出了两个主要警告。

1. 它依赖训练数据上计算出来的统计量，
所以不一定反映 hold-out 数据上的泛化重要度。
2. 它可能偏爱 unique value 很多的 high-cardinality feature。

换成更直白的话：

`MDI 虽然快又方便，但它可能高估那些在训练数据里很容易切出细碎分支的特征。`

例如， 如果有客户 ID 这种唯一值非常多的列， 那它可能只是因为便于在训练数据里切得很细， 就显得 importance 很高， 即使它对泛化帮助很小。

### 为什么相关特征会让人糊涂

scikit-learn 的例子展示了： 当特征之间存在 multicollinear 或 correlated 关系时， permutation importance 也可能和直觉不一样。 如果多个特征带着几乎一样的信息， 那么把其中一个打乱， 模型可能仍然靠另一个特征顶住， 于是性能下降没有想象中大。

这会制造下面的误解。

- test accuracy 很高
- 但某个特征的 permutation importance 很低
- 那是不是这个特征不重要？

不一定。

它不一定表示 `不重要`， 也可能表示 `另一个相关特征已经在提供类似信息`。

所以 importance 的解释不只是看一个特征。 它还要一起读特征之间的关系。

把同一个场景缩成一个小表：

| feature | 实际含义 |
| --- | --- |
| `monthly_spend` | 最近一个月的消费额 |
| `yearly_spend_div_12` | 最近一年消费额除以 12 |

这两列可能带着几乎一样方向的信息。 于是模型可能更多地用其中一个， 更少地用另一个。 但这不表示被少用的那个就完全没价值。 我们应该先想到 `importance 之所以分散，是不是因为这两个特征共享了相似信息`。

同样的场景， 在 permutation importance 里也会让人困惑。 如果把 `monthly_spend` 打乱了， 而 `yearly_spend_div_12` 还留着， 性能下降就可能比预想的小。 于是连 permutation importance 也可能显得低， 进一步引出误解： `那是不是两个都不重要？` 但现实里， 模型可能只是因为替代特征还在， 所以没有明显崩掉。

因此当相关性很强时， 不能从 `数字低` 直接跳到 `它不重要`。 应该先问： `是不是还有别的特征在替它解释？`

## PDP 和 SHAP 到底在问什么不同的问题

特征重要度总结的是 `模型大量使用了什么`。 但读者很快还会继续想问：

- 这个特征的值如果变大，预测会朝哪个方向移动？
- 在这一条样本里，到底是什么把预测推高了？

这正是 PDP(partial dependence plot) 与 SHAP 出场的位置。

| 工具 | 它首先想回答的问题 |
| --- | --- |
| feature importance | 模型大量使用了什么？ |
| PDP | 当一个特征值变化时，预测平均会怎样变化？ |
| SHAP | 在这条样本里，各个特征怎样贡献了这个预测？ |

所以 importance 更接近 `使用量总结`， PDP 更接近 `平均方向关系`， SHAP 更接近 `单条预测的贡献拆解`。

再压缩一点：

| 现在想看的东西 | 更该先想到的工具 |
| --- | --- |
| 整个模型主要在看什么 | feature importance |
| 某个特征变大时，预测会上升还是下降 | PDP |
| 这一条案例里是什么把预测推上去了 | SHAP |

因此， 如果只靠 importance 数字， 就想说明 `它会把预测往哪个方向推`， 信息是不够的。 importance 可能很高， 但它本身并不告诉我们： 值变大后预测是升还是降。 这种方向性问题， PDP 一类的工具回答得更直接。

同样地， 即使 importance 很高， 也不能假定它在样本 A 和样本 B 里的作用方式完全一样。 想更直接地读出这种个体贡献， 就是 SHAP 出场的问题。

所以， PDP 和 SHAP 不是用来替代 importance 的名字。 它们更适合被读成： `importance 这个数字本身无法结束掉的、另一类解释问题的工具`。

## 为什么 importance 和因果推断不是一回事

看 importance 数字时， 读者很容易跳到下面这句话：

`这个特征很重要，所以它就是结果的原因。`

但这种跳法并不安全。

| importance 解释告诉我们的 | 因果解释在追问什么 |
| --- | --- |
| 模型在预测里大量使用了哪个特征 | 如果真的去改变这个特征，结果会不会变？ |
| 数据里的统计关系 | 干预(intervention)与因果效果 |

假设 `recent_visits` 的 importance 很高。 这表示模型在做预测时大量使用了最近访问次数。 但这并不能让我们立刻说： `只要增加访问次数，响应率就一定会上升。` 现实里可能是：

- 访问次数本身是原因
- 或者本来就更感兴趣的用户，同时有更高访问次数和更高响应率
- 也可能是另一个隐藏因素同时推动了这两者

所以， importance 是预测模型内部的解释工具， 而因果推断属于另一个层次： 它更严格地在问 `如果我们真的去改变它，结果会怎样变？`

这一节里读者必须留下的边界如下。

| 看完数字后很容易直接写出的句子 | 更安全的句子 |
| --- | --- |
| `这个特征就是原因` | `这个模型大量使用了这个特征来做预测` |
| `改掉这个特征，结果就会变化` | `结果是否会变，需要另外做因果检验` |

因此， importance 解释可以帮助产生 `候选的因果假设`， 但它本身并不是因果证明。

## 在真实数据里相关特征很强时，应该怎样读

在真实的大型数据集里， 常常不是只有几列， 而是会有几十列含义接近的特征一起进入模型。 这时如果只看 `某一列的 importance` 就下结论， 解释几乎一定会走向过度自信。

更保守的解释策略， 最好按下面的顺序固定下来。

| 顺序 | 先做什么 | 为什么 |
| --- | --- | --- |
| 1 | 把含义接近的特征按组来看 | 因为 importance 可能分散到多列上 |
| 2 | 把 MDI 和 permutation importance 放在一起看 | 为了区分内部使用量和性能依赖度 |
| 3 | 做删除前后比较实验 | 为了确认它是不是真的可被替代 |
| 4 | 留下组层级的解释笔记，而不是只盯单列 | 因为在大数据里，角色不一定固定在单列上 |

例如， 下面这种读法会更安全。

| 危险读法 | 更安全的读法 |
| --- | --- |
| `A 列 importance 低，所以删掉` | `先看 A 列是不是被同组其他特征替代了` |
| `B 列排第一，所以它是最重要的业务原因` | `包含 B 列的特征组被模型大量使用了` |
| `permutation drop 很小，所以没必要` | `drop 小可能只是因为替代特征还在` |

所以在相关性很强的场景里， 比起只看 `单列排名表`， 更重要的是看 `相似特征组`、 `删除前后比较`、 以及 `不同 importance 方法的对照`。 重点不是让你更强地相信某一个数字， 而是留下一套更保守地阅读这个数字的标准。

### 看完 importance 数字后，下一步该做什么

这通常是初学者最常卡住的地方。 `所以我看到了数字。那接下来要做什么？`

在这一节里， 最小顺序可以固定成下面这样。

| 顺序 | 先问什么 | 为什么需要 |
| --- | --- | --- |
| 1 | 哪些是最上面的特征？ | 为了先确认模型主要在看什么 |
| 2 | 这到底是 MDI 还是 permutation？ | 因为即使都叫 importance，意义也不一样 |
| 3 | 有没有 high-cardinality 列或相关特征？ | 因为要先检查数字是否可能被扭曲 |
| 4 | 这种解释跟领域含义相符吗？ | 因为模型使用量与现实解释可能不同 |
| 5 | 在删除或改策略前，有没有做比较实验？ | 因为只看 importance 就下结论会很危险 |

这个顺序的目的， 不是把事情搞复杂。 而是让读者把特征重要度重新读成 不是 `成绩单`， 而是 `检查单`。

### 从高或低 importance 很容易跳出的错误结论

importance 数字大小很直观， 所以读者很容易直接跳到行动结论。 但更安全的解释会多经过一步。

| 现在看见的数字 | 很容易立刻跳出的结论 | 更安全的解释 |
| --- | --- | --- |
| importance 很高 | 它就是最重要的原因 | 模型大量使用了这个特征 |
| importance 很低 | 可以删掉 | 它可能被别的特征盖住了 |
| permutation drop 很小 | 它对性能不重要 | 可能还有替代特征留下来 |
| MDI 非常大 | 有这一个特征就够了 | 要先检查训练数据分支偏差的可能性 |

熟悉这张表之后， 看 importance 数字后的第一反应会稍微慢一点。 这种慢下来， 正是保护解释质量的装置。

## 案例与示例

### 案例 1. 为什么不能因为 importance 高，就立刻说它是原因

营销团队用随机森林来预测客户响应， 并想看看哪些特征更重要。 人先看到的标准包括 `最近访问次数`、`点击优惠消息`、`购买金额`、`会员等级` 等信号。

模型训练完成后， `feature_importances_` 显示 `recent_visits` 和 `discount_clicks` 较高。 这时团队很容易立刻说： `访问次数就是最大的原因。` 但这个数字首先总结的是 `模型在分支里多频繁地使用了它`， 而不是现实世界的原因排序。

```mermaid
--8<-- "assets/part-04/chapter-15/p4-15-2-mermaid-03-zh.mmd"
```

在这个场景里， 特征重要度应该被读成 `解释的出发点`。 MDI 总结模型内部的使用痕迹， 而 permutation importance 则检查： 如果把该特征打乱，真实性能会摇多少。 另外， 如果有多个含义相似的特征， 其中一个高、另一个低， 也不表示低的那个没有意义， 而可能只是它们在彼此替代。

可验证的结果会出现在： 把 MDI 和 permutation importance 并排看， 并一起检查是否存在 high-cardinality 列或相关特征的时候。 与其只根据一个 importance 数字改策略， 不如先把 模型内部用了什么 和 真正会摇动性能的是什么 分开来读。

### 案例 2. 为什么 importance 看起来低，也不能立刻删掉

假设有个团队做了订阅取消预测模型。 其特征包括 `monthly_spend`、`yearly_spend_div_12`、`recent_visits`、`late_payment_count`。 看 importance 时， `monthly_spend` 在中上， 而 `yearly_spend_div_12` 几乎排在底部。

人最容易做出的判断是： `yearly_spend_div_12 没用，删掉吧。` 但如果这两个特征携带的是几乎一样的信息， 那么低 importance 更接近 `另一个特征已经提供了类似解释`， 而不是 `这个特征毫无价值`。

这里真正重要的不是 importance 数字本身， 而是 `删除前后的比较`。 删掉这个低 importance 特征后， 要一起看性能和解释怎样变化。 如果性能几乎不变， 那冗余可能确实很强。 但如果某些案例解释崩掉了， 或 permutation 结果变化明显， 那它就可能仍然承担着辅助作用。

所以， 与其把低 importance 直接读成 `该丢掉的特征`， 不如先问： `信息是不是重叠了`、 `它是不是只在某些案例里发挥作用`、 以及 `删除前后究竟变了什么`。

### 在实务里更适合怎样读

特征重要度更保守的用法如下。

| 好的用法 | 危险的用法 |
| --- | --- |
| 检查模型主要在看哪些信号 | 把 importance 排名直接写成原因排名 |
| 检查有没有奇怪的列跑到了前面 | 看到数字低就立刻删特征 |
| 和 permutation 结果交叉核对 | 只看一个基于训练数据的 MDI 就下结论 |
| 一起检查相关关系和数据含义 | 只看数字就改策略 |

最终， importance 是 `解释工具的起点`， 而不是 `最终判决书`。

如果压成项目笔记语言， 可以写成下面这样。

| 记录项 | 例子 |
| --- | --- |
| observed importance | `petal length = 0.444` |
| safe interpretation | `这个模型经常使用这个特征` |
| review_needed | `存在相关特征，不能过度相信` |
| next_question | `要不要再看 permutation importance？` |

有了这个表， 特征重要度这一节就会被读成 `观察到的重要度 -> 解释边界 -> 下一个问题`。 真正重要的不是排名顺序本身， 而是有没有同时写下 `这次 importance 观察能帮助解释什么` 以及 `从什么地方开始还不能过度相信`。

### 看完 importance 后至少要留下的解释备忘

在实务中， 人们很容易只保存一个 importance 表就结束。 但这样一来， 之后再看时就不知道 `为什么我们相信这个数字` 以及 `我们在哪一步停下了解释`。

最好至少一起留下下面四行。

| 项目 | 示例记录 |
| --- | --- |
| observed importance | `recent_visits 是最高的` |
| interpretation boundary | `这个值是模型内部的使用痕迹，不是原因排序` |
| review target | `需要检查 discount_clicks 和 recent_visits 的相关关系` |
| next action | `补上 permutation importance 与删除前后比较实验` |

有了这份备忘， importance 这一节就不会只停在说明， 而会变成能通向下一次实验的学习记录。

## 练习与示例

### Python 示例：观察 MDI

这个例子是训练完随机森林后， 直接读取 `feature_importances_` 的最小练习。

- 问题场景：看 iris 数据里哪些特征被更重要地使用
- 输入(input)：iris 的 4 个特征
- 标签(label)：品种 class
- 要确认的概念：
  - importance 是相对占比
  - 所有值加总会接近 1
- 可以改动的值：
  - 把 `n_estimators` 改成 50、200、500，观察重要度排序会摇动多少。
  - 改变 `random_state`，检查大致模式是否仍然保留。

```python
# 这个例子通过随机森林的 feature_importances_ 阅读基于 MDI 的特征重要度。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("test accuracy:", round(model.score(X_test, y_test), 3))
print("feature importances:")

for name, score in zip(feature_names, model.feature_importances_):
    print(f"  {name:20} {score:.3f}")

print("sum:", round(model.feature_importances_.sum(), 3))
```

示例输出如下。

```text
test accuracy: 0.911
feature importances:
  sepal length (cm)    0.098
  sepal width (cm)     0.028
  petal length (cm)    0.444
  petal width (cm)     0.430
sum: 1.0
```

这个例子应该读出的是：

1. importance 是相对占比
2. 在这个模型里，petal length 和 petal width 被用得更多
3. 这只是 `这个模型的分支使用痕迹`，不是立刻就能拿去做因果解释的东西

### Python 示例：和 permutation importance 并排看

这次我们对同一个模型一起观察 permutation importance。

问题场景：

- importance 数字看起来像固定事实，
但一旦计算方法变了，结果也可能变化

输入(input)：

- iris 数据集
- 一个训练好的随机森林模型

期望输出(output)：

- 基于 MDI 的 importance
- permutation importance 的结果

要确认的概念：

- MDI 和 permutation importance 不一定给出相同的值
- 如果两个数字不同，先想到它们回答的是不同问题

可以改动的值：

- 把 `n_repeats` 改成 5、20、50，观察 permutation 结果的摇动。
- 改变 `test_size`，观察评估数据划分会让 permutation importance 改变多少。

```python
# 这个例子在同一个模型上并排比较 MDI 和 permutation importance。
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance

iris = load_iris()
X, y = iris.data, iris.target
feature_names = iris.feature_names

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

baseline_accuracy = model.score(X_test, y_test)

perm = permutation_importance(
    model,
    X_test,
    y_test,
    n_repeats=20,
    random_state=42
)

print("baseline accuracy:", round(baseline_accuracy, 3))
print("feature".ljust(20), "MDI".rjust(8), "perm_mean".rjust(12))
for i, name in enumerate(feature_names):
    mdi = model.feature_importances_[i]
    pmean = perm.importances_mean[i]
    print(f"{name:20} {mdi:8.3f} {pmean:12.3f}")
```

示例输出如下。

```text
baseline accuracy: 0.911
feature                   MDI    perm_mean
sepal length (cm)       0.098        0.011
sepal width (cm)        0.028        0.000
petal length (cm)       0.444        0.222
petal width (cm)        0.430        0.189
```

这个结果说明的是：

- 两种方法的排序有时相似，有时也可能不一样
- 即使是同一个特征，`它在分支里被用了多少` 和 `打乱后性能掉多少` 是两种不同的问题
- 因此，只看一个 importance 数字就结束解释，是危险的

### 试着自己先判断

先看下面这些观察，再自己选一遍：哪一种解释更安全？

| 观察 | 容易冲出去的结论 | 更安全的解释 |
| --- | --- | --- |
| `petal length` 的 MDI 最大 | 它就是最强的原因 | 它是在这个模型里分支使用最多的特征 |
| `sepal width` 的 permutation 值接近 0 | 它完全没用 | 可能还有别的特征在替它提供类似信息 |
| MDI 和 permutation 数值不一样 | 其中一个错了 | 它们在回答不同的问题 |

这个表的目的不是做对一道题，而是养成一个习惯：看见数字后，先再问一次 `这个数字到底在回答什么问题？`

### 为什么要小心 high-cardinality feature

树模型家族很容易对 unique value 很多的特征起反应。 因为这种特征会给训练数据里的细碎 split 创造很多机会。

例如：

- 客户 ID
- 订单编号
- 原始时间戳

这些列之所以看起来重要， 可能不是因为业务意义， 而只是因为 `它们提供了太多 split 候选`。

所以每次看 importance， 都要顺手再问一次：

`这真的是有意义的变量，还是只是一个很容易被切得很细的列？`

### 为什么要小心相关特征(correlated features)

例如如果 `monthly_spend` 和 `yearly_spend / 12` 这种几乎表达同样意思的列一起进入模型， 模型就可能更多地使用其中一个， 而更少地使用另一个。

于是结果会变成：

- 一边 importance 高
- 另一边 importance 低

但这不表示低的那个就没有价值。 它只是可能因为信息重叠而被替代了。

因此 importance 的解释总要和下面这些问题一起走。

- 有没有几列表达相似意思的 feature？
- 数字高的那个 feature 真的是独立重要的吗？
- 数字低的那个 feature 会不会只是被别的 feature 挡住了？

## 检查清单

- 你有没有把 importance 当成原因排序来读？
- 你能不能区分 MDI 和 permutation importance 回答的是不同问题？
- 你是否先检查了相关特征与 high-cardinality 列？
- 你能不能说明特征重要度是总结模型看了什么的工具，MDI 是内部总结，而 permutation importance 是外部检查？
- 你能不能说明 importance 数字并不直接等于因果关系或真正的原因排序？
- 你能不能说明 high-cardinality 与 correlated feature 都会扭曲解释？

## 出处与参考资料

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `RandomForestClassifier`, scikit-learn API Reference, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, `Permutation feature importance`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/permutation_importance.html](https://scikit-learn.org/stable/modules/permutation_importance.html){: target="_blank" rel="noopener noreferrer" }
- Gilles Louppe, *Understanding Random Forests: From Theory to Practice*, PhD Thesis, University of Liege, 2014, 确认日期: 2026-07-26. [https://arxiv.org/abs/1407.7502](https://arxiv.org/abs/1407.7502){: target="_blank" rel="noopener noreferrer" }
