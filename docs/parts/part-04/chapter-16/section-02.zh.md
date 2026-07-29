# P4-16.2 提升模型的性能与风险

> Section ID: `P4-16.2`
> Version: `v2026.07.26`

在 P4-16.1 里，我们看过梯度提升(gradient boosting)是怎样让下一阶段顺序修正前一阶段误差的。 正是在这里，boosting 的强项与风险会一起出现。

如果把同一个问题说得更准确一点，可以变成：

既然它会不断减少误差， 为什么它一方面看起来性能很强， 另一方面又会对[过拟合(overfitting)](/AiBook/zh/reference/concept-glossary-pinyin/g/#overfitting)这么敏感？

Boosting 可以通过堆很多小修正来做出很强的性能， 但也正因为如此，它会更容易把数据里的偶然波动一起追进去。

所以 boosting 的优点是 `精细修正`， 而风险则是 `修正变得过于精细`。

这一节不会长篇重复梯度提升的基本定义。 `顺序修正误差` 的核心直觉会通过 P4-16.1 和概念词典重新连接， 这里聚焦的是：为什么这个结构会同时带来强项和风险。

## 提升风险先收束的问题

本节回答以下问题。

- 为什么梯度提升常被说成是表格型数据(tabular data)上的强候选？
- 为什么学习率(learning rate)、tree size、`n_estimators` 会变成一个很敏感的组合？
- 过拟合会以什么样子出现？
- [收缩(shrinkage)](/AiBook/zh/reference/concept-glossary-pinyin/s/#shrinkage)、[子采样(subsampling)](/AiBook/zh/reference/concept-glossary-pinyin/z/#subsampling)、[早停(early stopping)](/AiBook/zh/reference/concept-glossary-pinyin/z/#early-stopping) 分别在试图降低什么风险？
- 和随机森林相比，什么场景下 boosting 会显得更强，什么场景下又需要更谨慎？

这一节围绕的问题是： `为什么 boosting 强，同时又为什么危险。` 实现感和计算结构一侧，会在补充学习 P4-16.3 继续。

## 提升风险要留下的判断标准

- 你可以同时说明 boosting 的高性能可能性与高调参敏感性。
- 你可以说明 `learning_rate`、`n_estimators`、tree size 是彼此连在一起的。
- 你可以在入门层面解释 shrinkage、subsampling、early stopping 为什么必要。
- 你可以形成一种检查态度：即使 train 性能看起来很好，也不能立刻相信。

## 为什么需要这一节

第一次接触梯度提升时， 读者往往会同时获得两种印象。

- 印象 1：它一直在修误差，所以看起来很聪明
- 印象 2：阶段越多，好像又越让人不安

这两种感觉都没错。

| 为什么 boosting 会显得很强 | 为什么它同时会变危险 |
| --- | --- |
| 它直接瞄准剩余误差做修正 | 它可能开始去追偶然的噪声(noise) |
| 它能不断累积小的非线性模式 | 阶段过多时，过度修正会越堆越多 |
| 它很容易在表格型数据上成为强候选 | 它对超参数组合很敏感 |

所以 16.2 这节，就是把 `为什么 boosting 很强` 和 `为什么又必须谨慎` 同时抓住的地方。

### 什么时候要先怀疑 boosting 的风险信号

Boosting 看起来越强， 就越要更早地问： `它现在学到的到底还是结构，还是已经开始连噪声也一起修了？`

| 看见的信号 | 先怀疑什么 | 原因 |
| --- | --- | --- |
| train 一直更好，但 validation 停住了 | stage 过多 | 后面的阶段可能已经开始追噪声 |
| learning rate 一大，分数就晃 | 修正过强 | 单阶段的影响可能被放大得太厉害 |
| tree size 一大，波动比改善更明显 | 单阶段表达力过剩 | 一个阶段就可能记太多内容 |
| 小模式抓得很好，但新数据上保持差 | 过拟合在累积 | 顺序修正可能只贴合了训练数据 |
| 一直在加 stage，却没有 early stopping | 缺少验证控制 | 复杂度可能在没有停点的情况下不断累积 |

这个表的目的不是让读者害怕 boosting， 而是让读者先看到： `性能信号一旦变强，应该同时检查什么风险。`

## 为什么 boosting 会显得性能很强

scikit-learn 用户指南经常把 gradient-boosted trees 和 histogram-based gradient boosting 列为实务里的强性能候选。 背后的关键就是顺序修正结构。

- 它不是一次找一条大规则
- 而是不断加小规则
- 再继续压低还错着的部分

这种方式很适合处理表格型数据里常见的 `彼此有些重叠的模式`。

例如在 churn 预测里：

- 会员时长较短
- 最近访问量下降
- 出现过支付失败
- 咨询次数也增加了

像这样几种信号一起重叠时， boosting 会是强候选， 因为它可以一阶段一阶段地把这些碎片化模式加进去。

更具体一点的输入表可以这样看。

| 客户 | 会员时长 | 最近 30 天访问 | 支付失败 | 咨询增加 | 实际流失 |
| --- | --- | --- | --- | --- | --- |
| A | 短 | 大幅下降 | 有 | 有 | 高 |
| B | 长 | 稳定 | 无 | 无 | 低 |
| C | 中等 | 下降 | 无 | 有 | 中等 |
| D | 短 | 稳定 | 有 | 无 | 中等 |

像这样的表， 很难只靠一条条件解释流失。 Boosting 可以把 `短会员时长 + 访问下降 + 支付失败` 这样的重叠信号按阶段继续反映进去， 所以它才常被提到是表格型数据上的强候选。

## 那为什么它又对过拟合敏感

如 16.1 所示， 梯度提升会根据 `前一阶段剩下的误差` 来生成下一阶段。 这个结构很强， 但也很危险。

因为随着阶段越来越往后， 模型会开始对更小的差异、 更细碎的残余波动作出反应。

压成一句话就是：

`前面阶段修的是大错误，后面阶段则可能开始去修小错误，甚至连偶然噪声也一起修。`

过拟合就发生在这个地方。

## 过拟合会长什么样

scikit-learn 文档说明， 随着阶段数增加， 可以通过 `train_score_`、staged prediction 等方式检查性能流， 这也会成为 early stopping 的根据。

在入门层面， 下面这张图很重要。

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-2-mermaid-01-zh.mmd"
```

它的意思很简单。

- 阶段太少时，模型还没学够
- 走到合适位置时，泛化(generalization)会更好
- 走得太多时，模型会开始记住训练数据里的细碎波动

所以在 boosting 里， `越多越好` 从来都不是默认答案。

## 为什么 `learning_rate` 和 `n_estimators` 要一起看

scikit-learn 文档把 learning rate 解释成 shrinkage， 并指出较小的 learning rate 需要更多 weak learner。

这组关系就是 boosting 的关键感觉之一。

| 设置 | 看上去的优点 | 风险 |
| --- | --- | --- |
| 大 learning rate + 少 stage | 改善很快 | 可能因为过强修正而摇晃 |
| 小 learning rate + 多 stage | 修得更慢、更细 | 如果阶段太多，最后仍然会过拟合 |

所以 `learning_rate` 和 `n_estimators` 像是一组此消彼长的把手。

因为它们要一起决定： `一次修多重` 和 `要修多少次`。

再把 tree size 一起放进来， boosting 的敏感性会更清楚。

| 把手 | 变大后先出现什么变化 | 一起要看的风险 |
| --- | --- | --- |
| `learning_rate` | 单阶段修正反映得更强 | validation 可能因为模型弯得太快而开始晃 |
| `n_estimators` | 修正机会变多 | 后面阶段可能开始追噪声 |
| tree size | 单阶段能解释更复杂的模式 | 单阶段本身就更容易记住例外 |

所以 boosting 不是一个适合只单看某个把手的模型。 更适合一起去读的是： `修多重`、`修多少轮`、`每轮修得有多复杂`。

## 为什么 tree size 会变得这么重要

scikit-learn 文档说明， 在梯度提升里， tree size 与模型能够捕捉的 interaction 复杂度直接相关。

- 小树：一阶段只做比较简单的修正
- 大树：一阶段能做更复杂的修正

因此，一旦树变大：

- 单阶段表达力会上升
- 但单阶段记住太多东西的风险也会上升

这表示 boosting 的复杂度， 并不只取决于 `阶段数`， 也强烈取决于 `每个阶段树有多大`。

在实务上，更安全的读法通常是把它们成组看。

- 如果 `learning_rate` 很大而 tree size 也大，单阶段就可能过于激进
- 即使 `learning_rate` 小，只要 `n_estimators` 和 tree size 都在涨，总复杂度仍然会继续上升
- 如果只是因为 train 性能看起来好，就一直加 stage 或 depth，那可能代表的不是 `修得更好`，而是 `把例外记得更细`

## shrinkage 在阻止什么

scikit-learn 文档介绍了 Friedman(2001) 的 shrinkage 策略， 说明每个 weak learner 的贡献都会通过 learning rate 被缩小。

入门层面的读法可以很简单：

`不要让新阶段一下子把答案推得太猛，先把速度放慢。`

所以 shrinkage 就像 boosting 的刹车。

如果没有这道刹车：

- train score 可能会很快往上冲
- 但模型也可能很快弯得太过

因此在 boosting 里， learning rate 更重要的身份不是“速度旋钮”， 而是 `控制过拟合的装置`。

## subsampling 在阻止什么

scikit-learn 文档在解释 stochastic gradient boosting 时提到， 每一阶段的 base learner 不一定非要用完整数据集训练， 也可以只看一个 `subsample`。

可以这样去读：

`不要让每个阶段都死死贴住完整数据；让它只看一部分，从而少一点执着。`

所以 subsampling：

- 会给修正方向加入一些随机性
- 有助于降低 variance
- 试图缓和过度拟合

它和随机森林里的 bootstrap 不是完全相同的结构， 但在感觉上仍然可以类比成： `给修正稍微晃一晃，不让它老是朝同一个方向贴得太死。`

## 为什么需要 early stopping

scikit-learn 文档说明， 读者可以通过 staged prediction、validation 分数流等方法， 找到合适的阶段数； 而 histogram-based gradient boosting 也直接提供了 `early_stopping`、`validation_fraction`、`n_iter_no_change` 等选项。

可以这样理解 early stopping：

`就算看起来还能继续学，只要 validation 不再变好，就应该停。`

这是 boosting 非常重要的一种运作感觉。

- train score 可能会持续变好
- 但 validation/test 在某个点之后可能不再进步，甚至会变差

所以 early stopping 是一种安全装置， 它避免读者只凭感觉去决定 `要不要继续加阶段`。

这里真正重要的是： early stopping 不是单纯的便利功能。 因为 boosting 走到后期时， 越来越难区分 `剩余结构` 和 `剩余噪声`。 所以一旦 validation 不再改善， 就该把那个位置当作停点。

## 和随机森林相比，会怎样

它们之间的差异在下面这个比较里最清楚。

| 问题 | 随机森林 | 梯度提升 |
| --- | --- | --- |
| 默认是否更稳定 | 相对是 | 会更敏感 |
| 少量调参下是否也较稳妥 | 相对比较稳妥 | 往往需要更仔细调整 |
| 是否更容易成为高性能候选 | 经常是很好的 baseline | 更常显示出更高的上限 |
| 过拟合控制是否重要 | 重要，但相对没那么敏感 | 非常重要 |

所以如果把随机森林读成 `稳定的起跑线`， 那么梯度提升更接近 `更激进的性能候选`。

## 如果放在同一个表格数据场景里再比较一次

想把 Part 4 Module 5 读成一整组的话， 最好把同一个表格问题再摆到三种模型前面一次。

例如同样是客户流失场景， 可以这样对比。

| 模型 | 最先看的信号 | 强项 | 第一个警戒点 | 紧接着的问题 |
| --- | --- | --- | --- | --- |
| 决策树 | train 和 test 从哪里开始分开 | 规则流最容易读 | 深了以后容易记例外 | depth 或 leaf 该停在哪里？ |
| 随机森林 | train/OOB/test 的间隔怎么动 | 更容易做出稳定平均预测 | 容易把 OOB 过度当成最终验证 | 还要继续加森林，还是回头看特征表达？ |
| 梯度提升 | validation/test 从什么时候开始停住或摇晃 | 更容易把剩余误差继续压下去 | 对 learning rate、阶段数、depth 很敏感 | early stopping 应该放在哪？ |

这个比较真正重要的， 不是 `哪个模型分数更高`， 而是： `在同一份数据场景里，它会先逼你检查什么。`

决策树会先让读者去看提问是不是变得太细， 随机森林会先让读者去看泛化估计之间的间隔， 而 boosting 会先让读者去看修正与停点。

如果把 16.2 再压成一句话， 就是：

`Boosting 能把剩余误差压得更低，所以它很强；也正因为如此，它更需要严格地管理“修到哪里”和“停在哪里”。`

## 案例与示例

### 案例 1：欺诈检测模型在训练数据上几乎完美，但运营性能在摇晃

假设某个支付欺诈团队训练了一个 gradient boosting 模型， 它在训练数据上几乎把所有欺诈交易都抓到了。 这会让人觉得 `性能非常好`， 但在真实运营数据里， 它可能把某些时期的偶然模式也一起学进去了， 导致误报增加，甚至错过新型欺诈。

这时团队需要一起下调阶段数、learning rate 与树深， 再加上 early stopping 与 validation 检查， 重新确认的重点就不该是 `训练分数`， 而应该是 `它在没见过的数据上还能不能站得住`。

也就是说， 对 boosting 来说， 比起一个高分数， 更重要的是管理 `修到哪里、停在哪里`。

如果团队的检查备忘像下面这样， 风险信号就会更清楚。

| 检查项 | 观测值 | 含义 |
| --- | --- | --- |
| train recall | 0.98 | 训练数据里的欺诈模式几乎都抓住了 |
| validation recall | 0.81 | 到了新数据上，有些模式就不稳了 |
| false positive 增加 | 周末深夜的正常支付更常被拦下来 | 可能把某些时期性偶然模式学得太深了 |
| best iteration 之后还继续加 stage | train 继续变好，但 validation 不再改善 | 可能已经越过停点了 |

所以， 只说 `它抓欺诈很强` 是不够的。 还要一起看： 哪些正常交易开始变得像可疑交易， 以及 validation 是从哪一阶段开始不再改善的。

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-2-mermaid-02-zh.mmd"
```

这个场景也可以压成一句更短的记录： `如果 train 几乎完美，但 validation/test 开始摇晃，那么 boosting 现在更可能是在学习噪声而不是结构。下一步应一起下调 learning rate、阶段数与树深，并重新确认 early stopping 标准。`

| 最先看到的信号 | 这个信号意味着什么 | 紧接着的下一步动作 |
| --- | --- | --- |
| 只有 train 很高，而 validation/test 开始晃 | 可能已经开始追偶然波动，而不是剩余结构 | 一起下调 learning rate、阶段数、树深，并重看 early stopping 标准 |
| train、validation、test 都低 | 更可能是输入表达或数据信号本身偏弱 | 先回看特征表达、数据质量、与 baseline 的提升幅度 |
| validation/test 在某个点之后不再改善 | 那个点可能就是停点候选 | 先把该阶段数留下当参考，不要立刻继续加 depth 或 stage |

### 案例 2：客户流失模型在 train 上更好，但真实活动响应变差

假设某个订阅服务团队把 gradient boosting 用到 churn 预测中。 新模型在 train 和 validation 上都比 baseline 好一点， 但真实的挽回活动效果却比预期差。

进一步看会发现， 模型开始把 `最近访问只是暂时下降` 的客户也更广地归入高风险组， 结果连本来很可能自行回来的客户，也被更大范围地拉进了补贴名单。

这里真正重要的， 不是某一个 AUC 数字， 而是： `到底是什么样的一群客户开始被放进高风险桶里。` Boosting 在努力压残余误差时， 更容易把边界附近那些含糊客户切得更细。 于是分数可能略好一点， 但一旦进入真实运营动作，性价比却可能变差。

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-2-mermaid-03-zh.mmd"
```

所以在这个场景里， 比起 `validation AUC 升了一点`， 更该先看的是 `活动目标人群到底怎么变了。` 当 boosting 模型被拿去接运营动作时， 读者不仅要调整阶段数和 learning rate， 还要一起检查： 预测顶部风险区里，实际进来的都是哪些案例。

## 练习与示例

这个例子用玩具数字说明： 当 learning rate 太大时， 修正会怎样变得过强。 它也会继续加上一个额外 correction stage， 一起看 residual 怎样往下掉。

- 问题场景：沿着剩余误差的方向去修正当前预测，并观察“修得太猛”会发生什么
- 输入(input)：真实值、当前预测、correction 值
- 期望输出(output)：小 learning rate 和大 learning rate 的差别
- 要确认的概念：
  - 真正重要的不是 correction 本身，而是它被反映得有多强
  - 大 learning rate 容易造成 overshoot
- 可以改动的值：
  - 把 `lr` 列表改成 `[0.1, 0.3, 0.8]` 这样的值，比较不同修正强度下的 residual 变化
  - 把 `correction` 的大小调大，确认大 learning rate 下摇晃是否更快变大

```python
# 这个例子比较小 learning rate 和大 learning rate 如何不同地反映同一个 correction。
actual = [120, 110, 90, 80]
pred = [100, 100, 100, 100]
correction = [15, 10, -10, -15]

for lr in [0.1, 0.8]:
    updated = [p + lr * c for p, c in zip(pred, correction)]
    residual = [a - u for a, u in zip(actual, updated)]

    print(f"learning_rate={lr}")
    print("  updated prediction:", [round(x, 1) for x in updated])
    print("  new residual      :", [round(x, 1) for x in residual])
```

输出结果如下。

```text
learning_rate=0.1
  updated prediction: [101.5, 101.0, 99.0, 98.5]
  new residual      : [18.5, 9.0, -9.0, -18.5]
learning_rate=0.8
  updated prediction: [112.0, 108.0, 92.0, 88.0]
  new residual      : [8.0, 2.0, -2.0, -8.0]
```

只看这些数字时， 很容易觉得 `0.8 更快变好`。 前期确实经常如此。 但 boosting 真正的风险点在后面的阶段。

- 如果 correction 稍微偏了，大 learning rate 会把摇晃放大得更快
- 如果数据里的噪声比较多，更强的修正也会更容易去追那些偶然波动

所以大 learning rate 可以让前期改善看起来很快， 但它也会更快地把模型推向危险的一边。

### 改一个值看看：再加一个 correction stage，residual 会怎样下降？

这次保留 `learning_rate = 0.1`， 再加一个 correction stage。

- 可以改动的值：
  - 把 `tree2_correction` 调小或调大，比较第二阶段的影响会怎样留在 residual 里
  - 保持 `learning_rate` 不变，单独观察阶段数增加的效果

```python
# 这个例子保持较小 learning rate，再加入第二个修正阶段，观察 residual 如何继续下降。
actual = [120, 110, 90, 80]
pred_stage0 = [100, 100, 100, 100]
tree1_correction = [15, 10, -10, -15]
tree2_correction = [10, 8, -8, -10]
learning_rate = 0.1

pred_stage1 = [p + learning_rate * c for p, c in zip(pred_stage0, tree1_correction)]
pred_stage2 = [p + learning_rate * c for p, c in zip(pred_stage1, tree2_correction)]
residual_stage3 = [a - p for a, p in zip(actual, pred_stage2)]

print("stage2 prediction:", [round(x, 1) for x in pred_stage2])
print("stage3 residual  :", [round(x, 1) for x in residual_stage3])
```

```text
stage2 prediction: [102.5, 101.8, 98.2, 97.5]
stage3 residual  : [17.5, 8.2, -8.2, -17.5]
```

加上第二个修正后， residual 又往下掉了一点。 这正是 boosting 里 `n_estimators` 的含义。 模型获得了更多修正机会， 但与此同时， 后面阶段也更可能开始追噪声而不是追剩余结构。

所以真正的问题不是 `阶段越多越好`， 而是 `走到哪里时，泛化还能保持住。`

### 这个例子里要一起读什么

这里重要的， 不只是 `residual 下降了`。 更重要的是一起读出： `它是以多大强度下降的` 以及 `这种下降能不能继续保持在 validation/test 上。`

| 通用记录语言 | 这次练习里要立刻留下的内容 |
| --- | --- |
| 看见的结构 | residual 下降速度与修正强度，会随着 learning rate 和阶段数一起变化 |
| 解释边界 | residual 下降，并不自动保证 validation/test 泛化，或保证停点一定安全 |
| 下一问题 | validation/test 会从哪一阶段开始停住或晃起来，early stopping 应该放在哪里？ |

## 如果改写成实务检查表

在实务里读取 boosting 时， 通常会把下面这些项目一起看。

| 检查项 | 为什么要看 |
| --- | --- |
| train 性能 | 看模型解释训练数据的程度 |
| validation/test 性能 | 看它在新数据上能不能站得住 |
| 阶段数(`n_estimators`) | 看它是不是还太短，或者已经太长 |
| learning rate | 看修正速度会不会太激进 |
| tree size / depth | 看单阶段会不会已经太复杂 |
| subsample | 看有没有装置去缓和过度贴合 |

这张表会直接说明： boosting 不是那种 `靠一个好默认值就能结束` 的模型， 而是那种 `调整与验证特别重要` 的模型。

例如， 假设同一场 churn 实验比较了两种设置：

| 设置 | train AUC | validation AUC | 解释 |
| --- | --- | --- | --- |
| `learning_rate=0.1`, `n_estimators=120`, `max_depth=3` | 0.91 | 0.84 | 可能仍然是泛化保持住的候选 |
| `learning_rate=0.3`, `n_estimators=300`, `max_depth=6` | 0.99 | 0.78 | 很可能已经开始过度贴合训练数据 |

这个比较最关键的点不是 `左边 train 分数更低，所以更差`。 反过来，哪怕 train 看上去没那么亮眼， 只要 validation 还撑得住， 它作为运营候选反而可能更安全。

在这一节里， 重要的记录结构也不是分数本身， 而是 `应该从哪里停下来`。 即使 validation/test 看起来差不多， 一种设置也可能在减少某类错误上更有效， 而另一种设置已经在追噪声。 所以残留案例模式也要一起留下。

| 需要一起留下的项目 | 本节里该写什么 | 为什么重要 |
| --- | --- | --- |
| 性能变化 | stage 增加时 train 与 validation/test 怎么变 | 为了看修正是否真的帮助了泛化 |
| 过拟合信号 | 从哪一点开始 validation/test 不再改善 | 为了抓住过度修正开始的地方 |
| 中断判断 | early stopping 或下一轮调整标准该放哪里 | 为了让下一次实验不是靠感觉停 |

## 检查清单

- 你是不是在同时看 validation/test，而不是只看到 train 分数好就相信？
- 你是不是把 `learning_rate`、`n_estimators`、tree size 当成同一组来读，而不是分开？
- 你能不能区分现在更需要的是 shrinkage、subsampling，还是 early stopping？
- 你能不能说明 boosting 能成为高性能候选，但也因此更需要调节与验证？
- 你能不能说明 learning rate、阶段数、tree size 要一起读，shrinkage 是放慢过强修正的装置，而 subsampling 是加入随机性以降低过拟合的装置？
- 你能不能说明 early stopping 是在泛化性能不再改善时及时停下来的安全装置？

## 出处与参考资料

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, 确认日期: 2026-07-26. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- Jerome H. Friedman, `Greedy Function Approximation: A Gradient Boosting Machine`, Annals of Statistics, 2001, 确认日期: 2026-07-26. [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451){: target="_blank" rel="noopener noreferrer" }
- Jerome H. Friedman, `Stochastic Gradient Boosting`, Computational Statistics & Data Analysis, 2002, 确认日期: 2026-07-26. [https://doi.org/10.1016/S0167-9473(01)00065-2](<https://doi.org/10.1016/S0167-9473(01)00065-2>){: target="_blank" rel="noopener noreferrer" }
