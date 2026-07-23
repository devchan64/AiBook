# P5-14.3 稳定深层重复的两个装置

> Section ID: `P5-14.3`
> Version: `v2026.07.23`

_副标题: residual 与 normalization 如何分别稳定信息流和值的范围？_

在 P5-14.2 中，我们看到了当前表示怎样经过 attention、feed-forward 和 residual 加法移动。但是 Transformer block 不只是不断堆叠新计算。它还同时放入稳定化装置：留下原始表示，并整理数值范围。

为什么 residual connection 和 layer normalization 在 Transformer block 中不是次要装饰？

核心不是`更强的 attention`，而是`能承受深层重复的信息流`。

## 稳定化装置处理的问题

- 只重复新计算时，可能出现什么问题？
- residual connection 为什么要把原始表示一起留下？
- layer normalization 为什么要在传给下一步计算前整理数值范围？

## 只相信新计算时，什么会摇晃？

深层 block 反复出现时，表示会不断改变。这时，如果新计算过度覆盖原始输入轴，重要线索可能消失；如果数值大小和分布摇晃，下一步计算也可能变得不稳定。

所以 Transformer block 通常同时保留下面两种直觉。

| 装置 | 想要防止的问题 | 先要留下的直觉 |
| --- | --- | --- |
| residual connection | 新计算过度覆盖原始信息 | 把原始表示一起留下 |
| layer normalization | 数值范围摇晃，使下一步计算不稳定 | 整理表示范围 |

## 案例与示例

### 案例：action token 不应失去原本意义

在故障响应句子中，action token 原本有一个叫`恢复状态`的轴。即使 attention 和 feed-forward 反映了新上下文，如果这个原本轴完全消失，当前表示就会变得不稳定。表示应该随着 rollback 是否已确认而变化，但 action token 指向处置状态这一基本意义必须保持。

这时，residual connection 会把新计算和原始表示一起留下，从而保存处置轴。layer normalization 会把这个结果整理到下一个 block 更容易处理的范围。

人快速看时容易采用的标准是`新上下文反映得越强，表示越好`。但在深层 block 重复中，只强烈留下新上下文并不总是安全。如果原始处置轴消失，下一层 block 很容易失去当前表示是以什么为基准发生变化的。

把这个场景分成三个阶段，residual 和 normalization 的角色会更清楚。

| 阶段 | 读取当前表示的问题 | 缺少时出现的问题 |
| --- | --- | --- |
| 只留下新计算 | 新上下文怎样改变了当前处置表示？ | 原始 action token 的处置轴可能变弱 |
| residual 之后 | 新上下文和原始处置轴是否一起留下？ | 数值轴相加后，大小和分布可能摇晃 |
| normalization 之后 | 是否是下一个 block 容易处理的数值范围？ | 下一步 attention 和 feed-forward 可能收到不稳定输入 |

![residual 之后的处置 token 比较](/AiBook/assets/part-05/chapter-14/transformer-block-action-residual-compare-zh.png)

| 比较点 | rollback confirmed | rollback not confirmed | 为什么重要 |
| --- | --- | --- | --- |
| action token after residual | `[1.026, 1.978]` | `[1.238, 1.814]` | 处置是否确认，会让当前位置表示朝不同方向移动。 |
| 解读 | 恢复状态轴更强 | 症状/原因轴相对保留更多 | 必须一起看新上下文反映和原始信息保留。 |

这张图并不是在展示 normalization 之后的新数值。应先确认 residual 之后原始处置轴和新上下文轴是否一起留下，再把 normalization 读成把这些合并后的值对齐到下一个 block 容易处理的基准线的步骤。

读数字时，与其先问哪个值是绝对正确答案，不如先看两个轴都一起留下了。`rollback confirmed` 中，恢复状态轴更强，但原始 action token 的处置轴也不应消失。`rollback not confirmed` 中，症状/原因轴相对保留更多，但它也必须仍然能被追踪为附着在某个处置上的意义。residual 留下这条追踪路径，normalization 则把合并后的值对齐到下一个 block 容易处理的范围。

这个案例要确认的结果是：residual 和 normalization 不是`重新生成答案的部件`，而是在新计算进入之后，仍然保护 action token 的基本轴和下一步计算稳定性的装置。

## 练习与例子

### 练习：去掉 residual 和 normalization 会缺什么？

请把下面问题分成 residual 和 normalization 的角色来回答。

| 问题 | 答案 | 解说 |
| --- | --- | --- |
| 如果只留下 attention 和 feed-forward 的结果，丢弃原始输入表示，会有什么风险？ | 新计算可能覆盖重要的出发线索 | residual connection 会把原始表示一起留下，让新上下文进入时，基本信息流也不被切断。 |
| residual 之后的值过大或过小时，下一层 block 会出现什么问题？ | 下一步计算可能变得不稳定 | layer normalization 会整理数值范围和分布，把更容易处理的表示传给下一个 block。 |
| residual 和 normalization 是让答案更聪明的装置，还是让深层重复计算撑得住的装置？ | 更接近让深层重复计算撑得住的装置 | 它们与其说是创造新意义的主角，不如说是帮助 block 重复时不丢失信息流和数值范围的稳定化轴。 |

解说：这个练习的核心，是不要把 residual 和 normalization 读成`提升性能的装饰`。深层 Transformer block 会不断堆叠新计算，因此需要原始信息留下的路径，也需要下一步计算能够承受的数值范围。

### 练习：诊断 action token 轴

在下面场景中，选出首先更直接需要的稳定化装置。

| 场景 | 更直接需要的装置 | 解说 |
| --- | --- | --- |
| 新计算之后，只强烈留下了`阻断`、`风险`意义，而要阻断什么变弱了 | residual connection | 原始 action token 的处置轴必须一起留下，后面的 block 才不会丢失对象。 |
| residual 把原始轴和新上下文相加后，只有某一个轴的值过大 | layer normalization | 必须整理数值范围，避免下一步计算被某个轴过度牵引。 |
| rollback confirmed 和 not confirmed 朝不同方向移动，但两者都必须保持处置状态轴 | residual connection | 各场景的新意义可以不同，但当前位置是处置 token 这一基本轴必须留下。 |
| 经过多个 block 时，表示值大小每次都大幅变化 | layer normalization | 要让重复 block 在相近的基准线上继续计算。 |

解说：这个练习是为了避免把 residual 和 normalization 当成一团来背。如果`失去的是什么`是原始信息，先想到 residual；如果`以什么范围计算`在摇晃，先想到 normalization。

## 检查清单

- 能说明 residual connection 为什么保存原始信息流吗？
- 能解释 layer normalization 会整理数值范围，从而稳定下一步计算吗？
- 能把 Transformer block 解释成`混入上下文 + 按位置加工 + 保存原始信息 + 稳定化`的组合吗？

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-07-19. [https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html](https://papers.nips.cc/paper/2017/hash/3f5ee243547dee91fbd053c1c4a845aa-Abstract.html){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
