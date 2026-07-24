# P5-9.1 GPU 与并行处理（parallel processing）

> Section ID: `P5-9.1`
> Version: `v2026.07.20`

到 P5-8 章为止，我们主要看的是深度学习模型内部发生的学习计算和 regularization。把视野再稍微放宽一点，接下来就会冒出一个问题。

深度学习明明需要这么多 parameter 和重复计算，为什么偏偏是到了某个时期之后，才突然开始显得实用了？

要回答这个问题，很难绕开 GPU（graphics processing unit）和并行处理（parallel processing）。

深度学习的扩散，并不是只靠算法想法本身发生的。它也和能把大量相同运算同时处理掉的计算资源发展，紧紧连在一起。

如果之后又觉得计算资源这件事重新变得抽象，更适合一起回到[英文概念词汇表里的 GPU 条目](/AiBook/reference/concept-glossary-parts/09-jieut/#gpugraphics-processing-unit)和[parallel processing 条目](/AiBook/reference/concept-glossary-parts/06-bieup/#parallel-processing)，重新对齐这两个概念。

## GPU 与并行处理相连的问题

- 为什么深度学习的计算量这么大？
- 在入门层面，CPU 和 GPU 该怎样区分？
- 什么叫并行处理，它为什么和深度学习这么合拍？
- 为什么在深度学习历史里，GPU 常常被说成一个转折点？

这一节先关住的是：为什么深度学习更像`海量重复相同数值运算的问题`，以及为什么这种重复计算会和 GPU、并行处理特别契合。也就是说，这里先专注于抓住`计算资源的大图景`。

同时，这一节也明确把接下来会继续具体化的问题交出去。GPU 擅长处理的深度学习计算，真实会以什么样的数据分组和 shape 被交给模型，会在下一节 P5-9.2 里继续通过 batch 和 tensor 计算说明。Transformer 为什么又会和 GPU 式并行处理特别契合，则会在后面的 P5-14.4 再重新接回。

## 重复运算与计算资源的判断标准

- 能说明深度学习为什么会因为大矩阵运算和重复计算而对计算资源敏感。
- 能从`任务是怎么被打包的`这个角度，直观解释 CPU 和 GPU 的区别。
- 能说明并行处理怎样影响深度学习训练速度与实用性。
- 能从 GPU 的视角重新读 AlexNet 这类历史转折点。

## 为什么深度学习的计算量这么大

深度学习模型哪怕只是做一次预测，也要执行很多次乘法和加法。到了学习阶段，还会在此基础上继续叠上 loss 计算、backpropagation、optimizer update。

例如：

- 输入很多
- 隐藏层很大
- 数据很多
- epoch 还要重复很多次

那么运算量就会非常快地膨胀。

在深度学习里，下面这些计算尤其会反复出现。

- vector 和 matrix 的乘法
- 大 tensor 级别的加法与乘法
- 按 batch 重复的计算

也就是说，深度学习与其说像是`一个单独而复杂的问题`，不如说更接近`把非常相似的数值运算重复海量次的问题`。

## 在入门层面怎样区分 CPU 和 GPU

最安全的比喻是下面这样。

- CPU 更像是少量但很强的工作者，灵活地处理各种不同任务
- GPU 更像是非常多的工作者，把相似任务拆开后同时处理

这并不是精确的硬件定义，但已经足够用来解释：为什么 GPU 会和深度学习这么合拍。

也就是说：

- 操作系统、浏览器、复杂条件分支这类工作，更带有 CPU 的感觉
- 大量重复同类数值运算的工作，则更带有 GPU 的感觉

深度学习恰好非常适合后者。

## 什么是并行处理

并行处理，是把多个计算拆开后同时处理的方式。先理解到下面这个程度就够了。

`不是把彼此独立或相似的计算一项项排队算完，而是把它们分到多个计算资源上同时处理。`

在深度学习里，尤其下面这些对象很适合并行化：

- 一个 batch 里的多个样本
- 矩阵里的许多元素计算
- 多个 channel 和 feature map 运算

也就是说，正因为深度学习`会反复执行大量同一模式的数值运算`，它天生就很适合 GPU 式的并行处理结构。

## 为什么深度学习和并行处理这么合拍

深度学习计算大体可以压成下面三个特征。

- 会形成大矩阵
- 会把同样运算施加在很多位置上
- 会一次处理很多样本

这种结构`本身就比较容易被拆分成许多独立计算块`。

例如：

- 把 convolution 应用在一张图片的不同位置
- 把同一个 linear layer 应用到 batch 里的多个样本
- 同时计算矩阵里的很多元素

这些都很契合 GPU 的强项。

`正因为深度学习会大量重复同一种数值计算，所以它和许多计算单元同时开动的方式天然合拍。`

如果把这种差别画成顺序处理和并行处理的对照，大致就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-09/cpu-gpu-parallel-flow-zh.mmd"
```

这张图里首先要确认的结果是：GPU 的关键并不是`它会做更复杂的计算`，而是`同样的计算更容易一次性铺到许多样本和位置上`。

## 为什么 GPU 在历史里会显得像转折点

深度学习的核心想法并不是最近才突然出现。perceptron、多层神经网络、backpropagation 这些关键概念，在更早以前就已经存在了。可深度学习会在某个时间点后迅速扩散，其中一个重要原因正是：`它终于算得动了。`

尤其是 2012 年的 AlexNet，常常会被描述成下面这些因素一起汇合的转折点。

- 大规模数据（ImageNet）
- 更深的 CNN 结构
- 基于 GPU 的训练
- 训练技术和 regularization 技术的组合

也就是说，只有想法本身还不够，还必须有`能把这些想法在真实规模上跑起来的计算资源`一起到位。

## 为什么 AlexNet 会被反复提起

AlexNet 更适合这样理解。

`让深度学习不再只是研究概念，而开始像是真正性能转折点的代表性案例`

AlexNet 之所以被反复提起，并不只是因为模型很大，而是因为基于 GPU 的大规模训练在图像识别上拉开了明显性能差距，也让深度学习的实用性开始被广泛看见。

因此，GPU 不只是一个零件，而更像是深度学习历史里`把想法抬到工业规模实验上的装置`。

## 案例与示例

### 案例. 同样的风险分数，一条条算和按 batch 一起算

假设我们要根据 4 条工厂生产线的传感器数值，计算风险分数。每条生产线都有 3 个 feature，而且所有生产线都使用同一组权重向量。人一开始很容易觉得：既然最后结果一样，那把`line 1 score`、`line 2 score`、`line 3 score`一个个顺着算，似乎也没什么大差别。在一个很小的例子里，这种感觉确实没错。即使只用 CPU，也足够追踪每条生产线的分数是怎么被算出来的。

但这一节更重要的差异，不在最后那一个分数上，而在`计算是怎样被组织起来的`。如果生产线不是 4 条，而是 4,000 条，而且同一个线性运算要在每个学习 step 里反复执行，那么`把同样计算一条条按顺序跑完`和`把整个 batch 一次性打包起来`的差异就会马上变大。GPU 和并行处理真正的核心，也正是在这里。它们不是突然把数学变得更复杂，而是把海量同类乘法和加法组织成更容易同时执行的结构。

因此，这个案例里首先要确认的是两件事。

- 按样本逐个重复的计算，和按 batch 的矩阵计算，能不能得到同样的分数？
- batch 越大，顺序重复计算的负担会多快变重？

先把这个案例固定住，下面例子里为什么会同时去看 `same result` 和 `scalar multiply count`，就会更自然地接上。

## 练习与例子

这个例子的目标，是把`同一个线性运算只施加在单个样本上`和`一次施加在整个 batch 上`这两种情况并排放在一起。

输入：

- 一个很小的 batch，包含 4 条生产线，每条有 3 个 feature
- 一组会对所有生产线共同使用的 3 个权重

输出：

- 每条生产线的风险分数
- 一次矩阵计算得到的分数
- 重复计算次数
- 当 batch 变大时，重复计算规模会怎样继续增长的比较

问题场景：

- 需要直接确认：batch 计算的本质，是把本来要按样本重复的同一个运算，改成一次矩阵运算来处理
- 即使只是小例子，只要把重复次数的增长一起看进去，也会更容易读出：为什么计算资源会改变哪些实验真正可做

要确认的概念：

- batch 矩阵计算会一次性给出多个样本的分数
- 一旦确认重复计算和矩阵计算会得到同样结果，batch 处理的意义就会更清楚
- 还要一起看到：随着 batch 增大，顺序重复计算的规模会立刻膨胀

从初学者角度，更适合按下面三个步骤来读这个例子。

| 阅读步骤 | 先看什么 | 接着马上要抓住的问题 |
| --- | --- | --- |
| 1 | 每条生产线的分数是怎么算出来的 | 按样本重复计算和 batch 计算会不会得到同样分数？ |
| 2 | `scalar multiply count` 到底是多少 | 当同一种运算随着 batch 放大时，它会多快膨胀？ |
| 3 | 为什么要把 CPU 和 GPU 分开讲 | 即使结果一样，计算组织方式会不会改变实验真正可行的范围？ |

输入（input）：

我们使用上面整理好的生产线 batch 和共同权重向量。

在看代码之前，可以先预测：什么会保持不变，什么会继续变大。

| 比较 | 可以先预测的比较 | 预测理由 |
| --- | --- | --- |
| `scores_one_by_one` vs `scores_batch` | 很可能会得到同样结果 | 因为计算含义本身没变，只是打包方式不同 |
| `scalar multiply count` | 很可能会随着 batch 和 feature 数增长而立刻变大 | 因为乘法重复次数会按样本数和 feature 数一起累计 |
| 实验负担 | 随着 batch 和模型变大，CPU 式顺序计算会更吃力 | 因为同类重复计算会很快增长 |

这里真正要确认的差异，也不会停在简单的计算量比较上。哪怕最后分数一样，CPU 侧的读法也应该继续连到`做完这一个实验到底要花多久`，而 GPU 侧的读法则应该继续连到`batch 大小、输入 feature 数、权重设置还能被改多少次再试一遍`。也就是说，这一节的计算差异，最终必须一路连到`实验回转速度`的差异。

这张表的目的，是把`结果相同`和`计算负担增长`拆开来读。下面这段代码把 `batch size` 和 `feature count` 都保留成可直接改动的值，好让读者立刻实验：到底是哪一类值对重复计算的膨胀更敏感。

```python
# 这个例子比较逐样本产线风险评分和 batch 矩阵评分，并检查乘法次数如何随 batch 和 feature 大小增长。
import numpy as np

# 4 lines, 3 features each
batch = np.array([
    [1.0, 0.5, 2.0],
    [0.2, 1.5, 0.3],
    [1.2, 0.1, 0.7],
    [0.0, 2.0, 1.0],
])

weights = np.array([0.4, 0.8, -0.3])
probe_batch_sizes = [4, 8, 16, 32]
probe_feature_sizes = [3, 6]


def scalar_multiply_count(batch_size, feature_count):
    return batch_size * feature_count


scores_one_by_one = []
scalar_multiply_total = 0
for sample in batch:
    score = 0.0
    for x, w in zip(sample, weights):
        score += x * w
        scalar_multiply_total += 1
    scores_one_by_one.append(round(score, 3))

scores_batch = batch @ weights
scaling_table = {
    feature_count: [
        scalar_multiply_count(batch_size, feature_count)
        for batch_size in probe_batch_sizes
    ]
    for feature_count in probe_feature_sizes
}

print("batch shape =", batch.shape)
print("weights shape =", weights.shape)
print("scores_one_by_one =", scores_one_by_one)
print("scores_batch =", np.round(scores_batch, 3).tolist())
print("scalar multiply count =", scalar_multiply_total)
print("same result =", np.allclose(scores_one_by_one, np.round(scores_batch, 3)))
print("probe batch sizes =", probe_batch_sizes)
print("estimated scalar multiplies when feature count = 3 =", scaling_table[3])
print("estimated scalar multiplies when feature count = 6 =", scaling_table[6])
```

读输出时，先看 `scores_one_by_one` 和 `scores_batch` 是否一致，再看 `scalar multiply count` 和 `estimated scalar multiplies` 是怎样继续增长的。

```text
batch shape = (4, 3)
weights shape = (3,)
scores_one_by_one = [0.2, 1.19, 0.35, 1.3]
scores_batch = [0.2, 1.19, 0.35, 1.3]
scalar multiply count = 12
same result = True
probe batch sizes = [4, 8, 16, 32]
estimated scalar multiplies when feature count = 3 = [12, 24, 48, 96]
estimated scalar multiplies when feature count = 6 = [24, 48, 96, 192]
```

- 即使计算内容本身相同，真实的深度学习框架也会把这类运算组织成`整个 batch 的矩阵计算`
- 即使在这个小数据里，同一种乘法也重复了 12 次；batch 或 feature 一变大，这个重复次数就会马上增加
- GPU 的强项，就在于把这类重复乘法和加法大规模并行处理

第一份产物是逐条生产线的风险分数。按样本重复计算和按 batch 的矩阵计算会得到同样分数，但这张图真正要显示的重点不只是`结果相同`，而是`同一个结果可以通过不同的计算组织方式得到`。

![逐条循环与 batch 矩阵计算的风险分数比较](/AiBook/assets/part-05/chapter-09/gpu-batch-score-comparison-zh.png)

第二份产物是 scalar multiply count 的增长曲线。当前例子里 4 条生产线、3 个 feature 需要 12 次乘法，但如果把 batch 大小和 feature 数一起放大，就能更直接地读出同类重复计算会多快膨胀。

![batch 与 feature 增长时的 scalar multiply count 比较](/AiBook/assets/part-05/chapter-09/gpu-scalar-multiply-scaling-zh.png)

| 比较 | 现在要读的核心 |
| --- | --- |
| `scores_one_by_one` vs `scores_batch` | 结果相同，但计算组织方式不同。 |
| `12 -> 24 -> 48 -> 96` 的增长 | batch 和 feature 越大，同类乘法负担就越快膨胀。 |
| CPU vs GPU 的感觉 | GPU 的价值不只是更快完成同一个计算，还在于让更大的 batch 和更多次实验真正变得可行。 |

读输出数字时，也要把`是否得到同样结果`和`为了得到这个结果需要承担多大计算规模`分开来看。从初学者角度，可以像下面这样逐行重读输出。

| 输出行 | 马上要读出的含义 | 接着会连到的问题 |
| --- | --- | --- |
| `same result = True` | 按样本重复计算和 batch 计算在数学上做的是同一件事。 | 那么真正差异是不是在于计算如何被组织起来？ |
| `scalar multiply count = 12` | 即使只是小 batch，同一种乘法也已经重复了多次。 | 样本数、feature 数、layer 数继续变大时，重复负担会涨到哪里？ |
| `estimated scalar multiplies when feature count = 3/6` | 不只是 batch，feature 数也会一起推高重复计算的增长速度。 | 到什么输入大小和模型宽度为止，实验才仍然是现实可行的？ |

| 比较 | 输出里首先看到的 | 只看结果时容易留下的解读 | 把 GPU 视角一起算进去之后会改变的解读 |
| --- | --- | --- | --- |
| `scores_one_by_one` vs `scores_batch` | 分数完全相同。 | 容易认为计算方式差异并不重要。 | 即使数学运算相同，怎样打包和处理它，也会改变实际速度和处理规模。 |
| `12 -> 24 -> 48 -> 96` 的增长 | batch 和 feature 变大时，重复计算估计值会快速增加。 | 在小例子里数字很简单，容易觉得真实负担也只是简单增加。 | 真实模型里 batch、feature、layer 会一起变大，重复计算很快会变成实验瓶颈。 |
| CPU vs GPU 的感觉 | 小例子用 CPU 也完全能跑完。 | 容易把 GPU 看成方便一点的加速器。 | 计算资源不只是速度差异，而是把更大 batch 和更多尝试变成可达工作范围的条件。 |

| 实验运行标准 | 只按 CPU 式读法时容易做出的判断 | 加上 GPU 视角后会改变的判断 |
| --- | --- | --- |
| batch 大小调整 | 只要分数一样，就容易觉得没有太大理由改变 batch | 一旦知道 batch 变大时重复计算负担会如何增加，就会先估计实验能跑到什么范围 |
| hyperparameter search | 多次改变 learning rate 或模型宽度，看起来只是多花一点时间的问题 | 同类运算一旦快速膨胀，就会先看到可尝试的设置数量本身会随计算资源改变 |
| 模型规模扩大 | 容易觉得增加 feature 或 layer 只会提高准确率 | 实际上重复计算和 memory 负担会一起增加，所以在期待性能之前，必须先问`能不能实际跑起来` |

把这个结果再翻回真实实验运转，CPU 式读法很容易流向`只要分数一样，计算方式差异就是次要的`，而 GPU 式读法会更早先问：`什么 batch、什么设置，才是真正还能持续重复实验的。` 这一节真正要读出的转折点，不只是速度更快，而是这种`实验设计可行范围`的差异。

Part 5 里 GPU 这一节之所以重要，不只是为了补一段硬件知识。如果把深度学习只看成纯数学理论，就会解释不出：为什么某个时期之后，它会突然引发产业级扩散。

这一节正在把下面这些东西连起来。

- Part 2 里的 vector / matrix / NumPy 计算
- Part 5 里的 backpropagation 与 optimizer
- 后续章节里 LLM 的大规模训练与推理成本

也就是说，GPU 这一节其实是那条历史桥梁，用来说明`为什么深度学习会变成大规模计算产业。`

先在这里停一下，把`什么时候该比模型结构更早想到计算资源视角`这条判断基准固定住，后面的章节会更不容易摇晃。

| 先冒出的提问 | 为什么此时更需要 GPU / parallel processing 视角 | 这一节还不会继续深挖的东西 |
| --- | --- | --- |
| 为什么模型突然变得特别慢？ | 因为要先确认是不是海量同类运算在反复出现，batch 与矩阵计算是不是已经成了瓶颈 | framework kernel 优化、CUDA 内部实现 |
| 为什么实验需要反复跑很多次，却总是太耗时？ | 因为计算资源不只是速度问题，而是实验回转本身能不能成立的条件 | TPU、NPU、分布式训练基础设施细节 |
| 为什么模型一旦变大，连能不能训练都不一样了？ | 因为 parameter 数和输入规模增大时，会一起推高 memory 和运算上限 | memory bandwidth、硬件架构细节 |

## 检查清单

- 能说明 GPU（graphics processing unit）和并行处理（parallel processing）为什么与深度学习扩散紧密相连吗？
- 能说明计算资源的发展怎样和模型结构的发展相互咬合吗？
- 能说明深度学习是一类反复执行大规模数值运算的计算问题吗？
- 能说出 GPU 擅长同时处理大量相似计算吗？
- 能不只把 GPU 说成`让深度学习跑得更快的零件`，而是说成`把大规模重复计算抬到实际实验规模的条件`吗？
- 能说明同一个分数既可以通过按样本重复计算得到，也可以通过 batch 矩阵计算得到，但计算组织方式会改变实验可行范围吗？
- 当执行速度和实验回转比模型结构更像瓶颈时，能先想到计算资源视角吗？
- 知道 AlexNet 常常被读作数据、模型、GPU、训练技术结合在一起的转折点吗？

## 出处与参考资料

- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, `ImageNet Classification with Deep Convolutional Neural Networks`, NeurIPS 2012, 确认日期：2026-06-29。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- NVIDIA, `What Is a GPU?`, NVIDIA Docs / corporate documentation, 确认日期：2026-06-29。 [https://www.nvidia.com/en-us/glossary/gpu/](https://www.nvidia.com/en-us/glossary/gpu/){: target="_blank" rel="noopener noreferrer" }
