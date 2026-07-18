# P5-8.3 补充学习：让深层计算不再摇晃的条件 - 初始化（initialization）、数值稳定性（numerical stability）、批归一化（batch normalization）

Section ID: `P5-8.3`
Version: `v2026.07.17`

在 P5-8.1 和 P5-8.2 里，我们已经看过：怎样在学习循环里加入目标函数控制和结构层面的控制。但即使加上这些控制，只要深层计算本身仍然不稳定，学习还是会继续摇晃。在 P5-6.4 里，我们也已经看到：为什么 dropout 和 batch normalization 会对 training mode 与 evaluation mode 的差异这么敏感。现在沿着这个背景，再补上一条初学者经常会留下的问题。

为什么层数堆得更深，并不意味着模型立刻就能学得很好？

要回答这个问题，与其把 initialization、numerical stability、batch normalization 分开死记，不如把它们一起放到一条轴上来读：`深层网络为什么在实践里能变得没那么容易摇晃。` 从第 8 章整体的 흐름来看，前两节处理的是`应该让什么变得不那么受偏好`和`应该减少什么样的路径依赖`，而这一节要收拢的是：`让计算本身能够撑住的条件。`

初始化负责决定学习开始时的出发点，数值稳定性负责检查数值和 gradient 在计算过程中会不会过大或过小，而 batch normalization 则是把学习中的 activation distribution 重新整理到更容易处理的范围里的装置。

如果之后这条轴又变模糊了，更适合一起回到[英文概念词汇表里的 training mode 条目](/AiBook/en/reference/concept-glossary/#training-mode)、[batch normalization 条目](/AiBook/en/reference/concept-glossary/#batch-normalization)、[initialization 条目](/AiBook/en/reference/concept-glossary/#initialization)、[numerical stability 条目](/AiBook/en/reference/concept-glossary/#numerical-stability)，重新把这几个概念并排对齐。

## 本节范围

- 为什么深层网络不是只要继续加层就会立刻学得更好？
- initialization 到底在决定什么？
- numerical stability 关心的到底是哪一类问题？
- 为什么 batch normalization 常常会被和学习稳定化一起提起？
- 这三个概念和 optimizer、regularization 回答的是怎样不同的问题？

ReLU 系列和深度学习扩展开来的大 흐름，会在 P5-3.4 再次接回；batch normalization 为什么对 train/eval mode 的差异敏感，则是在 P5-6.4 已经建立的基准上继续重读。regularization 和 normalization 的大视角承接自 P5-8.1，而 optimizer 的 update 本身会再连回 P5-7.1、P5-7.2。

这一节的角色，是把`让深层计算同时撑住 forward 与 backward 的条件`集中放在同一个位置里。

## 本节目标

- 能把 initialization 解释成`学习起点的数值布置`。
- 能把 numerical stability 解释成`让数值和 gradient 在计算中维持在可承受范围内的问题`。
- 能把 batch normalization 解释成`把 activation distribution 整理好，从而让学习没那么容易摇晃的装置`。
- 能区分 optimizer、regularization、batch normalization 回答的是不同问题。
- 能说明这一节在第 8 章中承担的是`计算稳定化装置`的角色。
- 能说明为什么下一节 P5-8.4 的 Python 例子有必要，以及那个例子要验证的到底是什么。

## 为什么要把这三个概念放在一起读

第一次学习深层网络时，常见的误解大致有下面这些。

- 只要层数继续往上堆，模型就会自动学得更好
- 只要把 optimizer 换成 Adam，大部分问题就会解决
- batch normalization 只是某个库里的一个选项而已

但实际情况是：学习开始时的出发点、中间计算里数值怎样变大或缩小、每一层把什么规模的值交给下一层，这些因素会一起互相咬合。

把这个 흐름压成很短的一张图，就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-08/stabilization-bridge-flow-zh.mmd"
```

这里的核心点，是`学习进展不顺`并不总是只来自某一个单独原因。

- 起始值可能太相似，或者太极端
- 数值可能在层与层之间越传越大，或者几乎消失
- activation distribution 也可能一直在摇晃后续计算

所以这一节要把这三者一起收成：`让深度学习真正可行的条件。`

## initialization 在决定什么

初始化，是在学习开始之前，决定要把什么数值放进 parameter 的动作。

表面上看，它像是只在决定一个出发点，但实际上它会直接连到下面两个问题。

1. 不同的 neuron 能不能从一开始就有机会学到不同的角色？
2. 前几次 forward 和 backward 里，数值会不会一下子变得太大或太小？

例如，如果所有权重都从完全一样的值开始，尤其是都从 `0` 开始，那么多个 neuron 就会对同样的输入产生同样的反应，并收到同样的 gradient。这样一来，即使网络堆了很多层，也很难让它们真的分头学会不同特征。

因此，初始化的第一责任，与其说是`不要随便开始`，不如说更接近`不要让所有 neuron 都以完全一样的方式开始。`

## 为什么出发点不能完全相同

如果只是一个 perceptron，起始值稍微笨拙一点，看起来也许没那么严重。但在多层结构里，同一层里的多个 neuron 本来就需要去学不同的组合。

如果出发点完全一样：

- 它们会看到同样的输入
- 给出同样的输出
- 收到同样的 gradient
- 再朝同样的方向更新

结果就是，多放几个 neuron 的优势会被削弱。

对初学者来说，这个点可以压成一句话。

`初始化不只是写下第一个数字，而是在给多个 neuron 留下分化成不同角色的可能性。`

## numerical stability 在担心什么

数值稳定性，是检查数值或 gradient 在计算过程中会不会变得太大或太小，以至于让学习开始摇晃的标准。

这里先只要记住下面两个场景就足够。

- 数值在穿过层时不断变大，最后爆掉
- 数值或 gradient 在穿过层时变得太小，小到几乎等于消失

深度学习会在一层又一层里重复同类计算。所以某一步里看起来很小的不稳定，到了很多层之后就可能被进一步放大。

| 问题场景 | 初学者的直觉 | 学习里会出现的结果 |
| --- | --- | --- |
| 数值太大 | 下一层不断收到过大的数字 | 输出和 gradient 都更容易跟着摇晃 |
| 数值太小 | 下一层几乎只看到相差不大的小数字 | gradient 可能会变弱，学习也会变慢 |

这一节不做数学证明，但重要直觉很清楚。

`深度学习既是堆很多层的问题，也是让这许多次计算都能在可用数值范围内撑住的问题。`

## 为什么只换 activation function 还不够

正如 P5-3.4 已经看到的，ReLU 系列在深层网络里非常常见。但只靠把 activation function 换掉，并不会自动解决所有问题。

实际中，下面这些因素会一起咬合。

- activation function 如何把数值继续往后传
- initialization 是否避免了过小或过大的起始值
- optimizer 和 learning rate 的设置
- 像 batch normalization 这样的 distribution stabilization 装置

也就是说，`深度学习变得实用`通常不是指某一个单独发明，而更接近于多个稳定化装置开始一起工作。

## 为什么 batch normalization 很重要

batch normalization 会参考一个 batch 里的 mean 和 variance，把 activation distribution 再次整理一遍。

从初学者的角度，先读到下面这个程度就够了。

- 如果前一层的输出忽大忽小
- 下一层就必须在一个不断摇晃的 distribution 上学习
- 结果会同时影响学习速度和稳定性

因此，batch normalization 更适合读成：`以当前 batch 为 기준，再把数值整理成更容易处理的范围，然后再交给下一层的装置。`

P5-6.4 里看到的 mode 差异，也会在这里重新接回。

- 训练中，它参考的是当前 batch 的统计量
- 评估中，它更多会依赖训练期间累计下来的 기준

所以 batch normalization 并不只是`另一个 normalization 名字`，而是一个典型案例，让读者必须把学习稳定化和 mode 切换一起读。

## 它和 regularization 有什么不同

初学者很容易把 batch normalization、dropout、weight decay 全都看成一团`帮助学习的选项`。但它们回答的问题其实不同。

| 项目 | 首先回答的问题 |
| --- | --- |
| initialization | 学习应该从什么样的起点开始？ |
| numerical stability | 在重复计算里，数值和 gradient 是否还留在可承受范围？ |
| batch normalization | activation distribution 要不要再整理到更容易处理的范围？ |
| optimizer | gradient 要按什么步幅和规则变成实际 update？ |
| regularization | 要加上什么样的限制，避免模型走向过于复杂的解？ |

先把这张表固定住，后面即使又遇到新的技术名字，也更容易把它拆进`出发点`、`计算稳定性`、`更新`、`泛化`中的哪一类。

## 案例与示例

如果想把前面说的`深层网络为什么能变得没那么容易摇晃`读成具体场景，那么与其分别死记三个术语，不如一起看：`同一个深层计算场景，会在哪里开始摇晃，又是什么在减少这种摇晃。` 下面两个案例，把同一个深层网络拆成`一开始就不稳定的场景`和`被重新整理后较不容易摇晃的场景`。

### 案例 1. 深层网络从一开始就摇晃的场景

先想象一个输入 `x = 2` 的小型深层网络。第一层有两个 neuron，而且权重都从 `0` 开始。这样一来，这两个 neuron 一开始就会给出相同的输出，在反向传播里也容易拿到相同的 gradient，并一起沿着 `0 -> 0.3 -> 0.6` 这种路径移动。第一个场景里马上出现的问题，就是：`如果初始化把出发点设错了，多个 neuron 就无法真正分化成不同角色。`

再往后加一个条件：假设后面几层的起始权重尺度也很大。前一层里长得很像的值继续传给下一层，而大权重又不断重复，那么数值范围就可能像 `0.6 -> 1.8 -> 5.4` 那样越来越快地膨胀。此时摇晃的，不只是输出数字本身。activation reaction 可能会偏掉，gradient path 也可能一起变得不稳定。数值稳定性就是在这里出现：它问的是`深层计算到底能不能撑住这种数值范围。`

最后，再想象不同 batch 之间的中间 activation distribution 差得很大。某个 batch 里，它们可能集中在 `0.5, 0.8, 1.0` 附近；另一个 batch 里，却可能直接跳到 `15, 20, 24` 这种大范围。这样下一层每次拿到的输入规模都不一样，学习也就更容易摇晃。到了这个位置，batch normalization 的必要性就出现了：它负责把层与层之间已经产生的 activation distribution，重新整理成下一层更容易处理的范围。

也就是说，这个案例并不是在分别展示三个断开的问题。`被绑在同一起点上的 neuron`、`随着深度扩大而增大的数值范围`、`每个 batch 都在摇晃的中间 distribution`是在同一个场景里连着发生的，因此深层网络如果想没那么容易摇晃，就必须同时抓住`出发点`、`重复计算范围`、`层间 distribution`。

### 案例 2. 让深层网络没那么容易摇晃的场景

现在重新看同样的结构，但改变起始条件。假设第一层的两个 neuron 不再从完全相同的权重开始，而是一个稍小、一个稍微不同。这样一来，它们从一开始就不会无限重复同样的反应，而是有机会对不同输入组合走出略微不同的路径。这里初始化的角色，首先不是`找到好数字`，而是`提供一个不会复制同一路径的起点`。

接着，如果各层权重尺度没有被设得过大，那么数值范围就可能像 `0.6 -> 0.9 -> 1.1` 那样更缓慢地移动。当然，真实模型比这复杂得多，但对入门读者来说，这个场景已经足够。深层网络想没那么容易摇晃，就必须即使层数很多，也能让计算不至于一下子爆掉或消失。此时 numerical stability 就是在读：`什么样的起始尺度和计算 흐름，能让深层重复计算撑得住。`

最后，即使层间传递的 activation distribution 在不同 batch 之间并不完全相同，只要把 batch normalization 插进去，下一层收到的就不会再是`每次规模都完全不同`的输入，而会是`被重新整理回可比较范围的输入`。因此，batch normalization 的第一角色不是背名字，而是负责把已经开始摇晃的中间 distribution 整理好，让下一层还能继续撑住。

所以，这个案例里要确认的结果很清楚。深层网络之所以没那么容易摇晃，不是因为技术名字变多了，而是因为 initialization 让起点分开，numerical stability 让重复计算范围撑得住，而 batch normalization 则重新整理层与层之间的 distribution。

从初学者角度，把案例 1 和案例 2 再折回去，最适合按下面这个顺序来读。

```mermaid
--8<-- "assets/part-05/chapter-08/stabilization-case-reading-flow-zh.mmd"
```

这张 흐름图里首先要抓住的点只有一个。深层网络稳定化并不是`技术名称清单`，而是一个判断顺序：`起点有没有分开 -> 重复计算范围撑不撑得住 -> 层间 distribution 会不会继续摇晃下一层。`

![不稳定场景与稳定化场景里的 neuron 路径比较](/AiBook/assets/part-05/chapter-08/stabilization-neuron-paths-zh.png)

这张图说明：在不稳定场景里，两个 neuron 的路径几乎重叠；而在稳定化场景里，它们不再完全重复同一条路径。

![不稳定场景与稳定化场景里的逐层 activation range 比较](/AiBook/assets/part-05/chapter-08/stabilization-layer-range-zh.png)

这张图说明：随着层数加深，不稳定场景里的范围会更快扩张，而稳定化场景里的范围则移动得更缓。

![不稳定场景与稳定化场景里的按 batch 中间 activation range 比较](/AiBook/assets/part-05/chapter-08/stabilization-batch-spread-zh.png)

这张图说明：在不稳定场景里，不同 batch 的中间 distribution 差异更大；而在稳定化场景里，下一层更容易收到规模可比较的数值。

把这两个案例再折回成一条 흐름，这一节要一起读的稳定化轴可以整理成下面这样。

| 阶段 | 最先开始摇晃的东西 | 最先该抓住的装置 |
| --- | --- | --- |
| 学习开始之前 | neuron 会不会被绑在同一个起点上 | initialization |
| 计算在层间反复进行时 | 数值和 gradient 的范围会不会放大或缩小 | numerical stability 视角 |
| 数值从一层传到下一层时 | 中间 activation distribution 会不会持续摇晃下一层 | batch normalization |

也就是说，哪怕这两个案例看起来像是`一个问题案例`和`一个解决案例`，真正更好的读法仍然是：它们一起构成了一条稳定化轴，分别抓住`出发点`、`重复计算范围`、`层间 distribution`，从而让深度学习没那么容易摇晃。

| 人最容易先看的标准 | 用 initialization、numerical stability、batch normalization 视角重读的标准 |
| --- | --- |
| 容易觉得只要层数更多、表达能力更强，学习自然就会更好 | 层堆得越深，出发点、数值范围、activation distribution 越可能一起摇晃，因此必须把稳定化条件一起看 |
| 容易觉得只要把 optimizer 换成 Adam，多数问题就会解决 | optimizer 负责的是 update 规则，而 initialization、numerical stability、batch normalization 负责的是在那之前让计算本身撑住 |
| 容易觉得 batch normalization 只是某个库选项 | batch normalization 是一个稳定化装置，它整理学习中的 activation distribution，并迫使读者一起考虑 mode 差异 |
| 容易觉得只要增加 neuron 数量或层数，模型就会自动学到不同特征 | 如果初始化完全相同，多个 neuron 还是可能沿着同一路径移动，而过大的数值也会在重复计算里进一步放大不稳定 |

这些案例里最终要确认的结果很清楚。深层网络稳定化的核心，不是`背了多少技术名字`，而是理解：initialization 处理的是起点，numerical stability 处理的是重复计算的范围，batch normalization 处理的是中间 distribution，而这三者一起让学习没那么容易摇晃。

## 练习与例子

只要能回答下面这些问题，这一节的角色就算关住了。

| 问题 | 要确认的视角 |
| --- | --- |
| initialization 在决定什么？ | 它给多个 neuron 留下从不同出发点开始分工的可能性。 |
| numerical stability 在担心什么？ | 它检查深层重复计算里，数值与 gradient 是否留在可承受范围。 |
| batch normalization 会介入哪里？ | 它把中间 activation distribution 重新整理成下一层更容易处理的 기준。 |

这一节先关住的是概念地图，因此这里不马上重复可执行代码。下一节 [P5-8.4](section-04.zh.md) 会再单独用 Python 例子和图表确认：较大的 initialization scale 会怎样在深层中放大数值，以及一旦插入 batch normalization，什么又会跟着改变。

## 检查清单

- 能说明深层网络既是堆结构的问题，也是让计算撑得住的问题吗？
- 能从`布置起始权重`的视角解释 initialization 吗？
- 能从`深层重复计算会怎样摇晃数值范围`的视角解释 numerical stability 吗？
- 能说明为什么 batch normalization 会和学习稳定化、mode 差异说明一起出现吗？
- 能说明 batch normalization 是一种把 activation distribution 整理到更容易处理范围里的学习稳定化装置吗？
- 能区分 optimizer、regularization、batch normalization 回答的是不同问题吗？

## 出处与参考资料

- Aston Zhang, Zachary C. Lipton, Mu Li, Alexander J. Smola, `Dive into Deep Learning`, `5.4 Numerical Stability and Initialization`, `8.5 Batch Normalization`, `12 Optimization Algorithms`, 确认日期：2026-07-11。 [https://d2l.ai/](https://d2l.ai/){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, Part II `Modern Practical Deep Networks`, 确认日期：2026-07-11。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Stanford `CS231n: Deep Learning for Computer Vision`, Schedule and course notes on `Regularization and Optimization`, `Neural Networks and Backpropagation`, `CNN Architectures`, 确认日期：2026-07-11。 [https://cs231n.stanford.edu/](https://cs231n.stanford.edu/){: target="_blank" rel="noopener noreferrer" }

