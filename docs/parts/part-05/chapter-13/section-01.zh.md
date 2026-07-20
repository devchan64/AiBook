# P5-13.1 注意力（Attention）的直觉

> Section ID: `P5-13.1`
> Version: `v2026.07.19`

在 P5-12.2 里，我们已经看到：因为长期依赖（long-term dependency），序列模型可能很难把很早之前的信息充分保留到当前位置。这里就会出现下一个问题。

能不能让当前位置更直接地重新参考它真正需要的过去信息？

这个问题最具代表性的回答，就是注意力（Attention）。

注意力是一种方式：它会对当前计算里真正重要的位置或 token 赋予更大的权重，让需要的信息能被更直接地参考到。

当需要再次用很短的话重新抓住 attention 的基本问题意识时，可以回到英文概念词汇表里的 [attention](/AiBook/en/reference/concept-glossary/#attention) 条目重新对齐。

## 本节范围

- attention 想解决的是什么问题？
- `更强地看需要的位置` 这句话到底是什么意思？
- attention 和 RNN 家族是怎样连起来的？
- 为什么 attention 会让人觉得像一个很大的转折点？

本节首先要收住的核心，是`与其只是努力把信息记得更久，不如引入一种方式，让模型能重新去看当前真正需要的位置`。

self-attention 与 Transformer 的连接会在下一节和下一章继续展开。query、key、value 与 multi-head attention 的入门说明，会在补充学习 P5-13.3 再回收。

## 本节目标

- 能把 attention 解释成`更直接地参考重要位置的方式`。
- 能说明长期依赖问题和 attention 之间的连接。
- 能解释为什么在早期 encoder-decoder 结构和运维文档转换场景里，attention 会很重要。
- 能通过可运行的 Python 例子，确认 attention 作为加权平均的直觉。

## attention 为什么会出现

在 basic RNN 或 encoder-decoder 结构里，常常会倾向于把整段长输入压进一个压缩状态（state）里。输入短的时候还能撑住，但一旦长度变大，当前真正需要的那条线索就很容易在这个压缩状态里变得模糊。

attention 用另一种方式看这个问题。

`在生成当前输出时，直接计算整段输入里哪些位置应该被更强地参考。`

也就是说，它不再只是把早期信息勉强塞进一个越来越淡的状态里，而是引入了`需要时再把它找回来看看`的想法。本节读 attention 的关键，比起`让模型记得更久`，更在于`让模型重新找到当前需要的位置`。

## `更强地看` 是什么意思

attention 的核心，是给当前任务更相关的位置更大的权重，然后再把信息聚合回来。重要的是，它不会预先把所有位置一视同仁。

- 在当前位置上
- 模型会扫过过去输入或其他位置
- 给更重要的位置更高的分数
- 再根据这些分数把信息聚合起来

也就是说，attention 不是把每个位置都同样地看，而是`更强地参考当前任务更相关的位置`。所以即使输入相同，只要当前问题变了，应该被更强地看见的位置也会跟着改变。

把这条流程用很短的表压一下，会是下面这样。

| 步骤 | 当前正在发生什么 |
| --- | --- |
| 1 | 当前位置扫过其他位置 |
| 2 | 给更相关的位置更高分 |
| 3 | 根据这些分数聚合上下文信息 |

下面这句短句，会用一个当前句子更强地参考后句原因线索的场景，展示 `扫过 -> 打分 -> 聚合上下文`。

```text
重启被延后了。原因是压力不稳定。
```

如果模型现在正在回答`原因是什么？`，它就不会给每个词完全相同的权重，而是会把更大的比重放到 `压力`、`不稳定`、`原因` 这些位置上。也就是说，在 attention 里，`更强地看` 的意思，就是`和当前问题更直接连接的位置，会在计算里被更强地反映出来。`

## 为什么把它看成直接引用例子会更直观

attention 在历史上是在 sequence-to-sequence translation 背景下获得了很大力量，但从读者角度看，把它读成`当前正在写的这句工作指令，到底该回头看输入里的哪里`这种工作指令转换场景，会更直接。

例如，把英文运转步骤转成中文作业指令时，在模型正在形成当前输出短语的那个时刻：

- 它可以在整句输入里判断，哪些词现在最相关
- 然后更强地参考那些位置

也就是说，每形成一个输出词或短语，模型都可以重新扫整段输入，但会把更多权重放到当前真正需要的位置上。

`attention 是一种装置：它会让模型找到和当前正在写的工作指令短语最匹配的输入位置，并更重地参考那里。`

## attention 是怎样回答长期依赖问题的

长期依赖问题说的是：很久以前的信息，可能在传到当前时已经变弱甚至消失。attention 对这个问题的回答大致是下面这样。

- 不要只把早期信息作为状态里的微弱痕迹留下
- 在当前 step 上，重新扫一遍过去所有位置
- 直接把真正重要的地方选出来参考

也就是说，attention 更接近`把需要的信息找得更准`，而不是单纯`把记忆保留得更久`。

如果说 P5-12.2 是在讲`状态里的信息会随着距离变远而变淡`，那这一节就是把问题翻过来，变成`那就重新看一遍当前真正需要的位置`。

如果只把这个转折再压成很短的流程，可以这样读。

```mermaid
--8<-- "assets/part-05/chapter-13/attention-direct-reference-bridge-zh.mmd"
```

这张图真正要抓住的点，是手柄从`长期带着走`变成了`需要时重新找回来`。

## 如果把它画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-13/attention-focus-flow-zh.mmd"
```

这张图把 attention 压成了`找到需要的位置 -> 分配权重 -> 形成聚焦的上下文`。

如果再很短地固定一次：同样的输入句子里，一旦当前问题变化，重新要看的位置也会跟着变化，那么可以看到下面这样。

```mermaid
--8<-- "assets/part-05/chapter-13/attention-question-shift-zh.mmd"
```

在这张比较图里，首先要抓住的是下面几点。

- 即使输入句子相同，只要`问的是什么`变了，获得高权重的位置也会一起改变。
- 所以 attention 的核心，不是`预先选出一句固定的重要句子`，而是根据当前问题重新决定参考位置。
- 只有抓住这个感觉，下一节 self-attention 里`不同 token 会重新看不同位置`的说明才会更自然。

## 如果把 attention 误解成`摘要`，会在哪儿偏掉

第一次接触 attention 时，很容易把它想成一种`只留下重要部分的摘要装置`。但这里最好先更准确地区分一下。

- attention 会给当前计算里更重要的位置更大的权重
- 所以上下文会被重新读成一种`重要部分被更强强调的状态`
- 但 attention 本身并不会直接缩短输入长度，也不是把内容单独压缩存起来

也就是说，attention 的核心不在于`把上下文变短`，而在于`在上下文里面，哪些位置应该被更强地参考`。

把这个差别缩成一句话，就是下面这样。

`attention 与其说是把上下文压成更短摘要的装置，不如说是让当前计算里更重要的位置被更强地读出来的装置。`

## 为什么它看起来像一个很大的转折点

attention 并不只是一个把性能稍微提高一点的辅助技巧。它真正带来的，是 sequence modeling 视角本身的变化。

在 attention 之前：

- 中心做法更像是把长句塞进一个压缩状态里

在 attention 之后：

- 更强调的是保留整段输入，并在其中有选择地参考当前需要的位置

这个变化后来一路延伸到 self-attention 和 Transformer，构成了从 RNN 中心流向外转的一个很大拐点。本节读者真正该抓住的也是这个点：问题本身从`要不要把信息长期带着走？`变成了`要不要重新去看当前真正需要的位置？`

## 案例与示例

### 代表案例：运转步骤文档转换

想象一下：我们要把英文运转步骤文档改写成中文作业指令。人一开始很容易觉得，只要从左到右顺着读，再直接搬过来就够了。但实际上，模型在形成当前这句中文指令时，经常需要重新确认：整句输入里，哪一个位置和现在正在写的这段指令最直接相关。比如，如果漏掉了句首主体和句尾安全条件之间的关系，结果看上去可能语法没问题，但到底是谁先做什么，会变得很别扭。人自己在翻步骤文档时，通常也会回头重新找一眼和当前词最匹配的输入位置。attention 很适合这种直觉：`更强地看当前正在生成的输出短语最相关的输入位置`，也可以被理解成一种减少在长句里漏掉远处关键单词的方向。

所以，这个案例里要确认的结果是：当前翻译出来的短语，是否没有只跟着附近单词走，而是真的重新参考了前面的主体和后面的安全条件，最后收束成条件式的作业指令。

同样的视角也会直接延伸到故障备忘录摘要和手册问答里。不过，本节真正要抓住的不是领域名称，而是`一旦当前问题或输出目标变了，需要被更强地参考的位置是不是也会跟着变。`

把三个案例放在一起，会更清楚地看到：attention 不该被读成`粗略摘要重要部分的装置`，而应该被读成`会随着当前问题或输出目标变化，而改变重新参考位置的结构`。

| 人容易先看的标准 | 从 attention 视角重新读时的标准 |
| --- | --- |
| 觉得只靠读完整句后留下的整体印象，也能回答当前问题 | 一旦当前问题或输出目标变化，需要重新看的位置也会一起变化 |
| 觉得重要句子从一开始就是固定的 | 即使是同一份文档，获得最高权重的位置也会随着`问的是什么`而变化 |
| 容易把 attention 理解成简单的摘要装置 | 核心不在压缩长度，而在根据当前任务重新分配参考权重 |

## 练习与例子

这个例子的目标，是确认 attention 作为一种给重要位置更大权重、再形成加权平均的直觉。它不再是简单的数值平均，而是改写成一个小型问答场景：给定`问题`和`句子候选`时，模型到底会更强地看哪里。

问题场景：

- 如果把所有输入位置一视同仁地平均，和当前问题直接相关的信息就可能被冲淡

输入：

- 两个问题
- 三个句子候选值
- 每个问题对应的一组候选相关度分数

输出：

- 对所有候选一视同仁平均得到的 baseline 上下文值
- 随问题变化而变化的归一化权重
- 随问题变化而变化的上下文值
- 哪个候选被最强反映出来的摘要

要确认的概念：

- attention 不会对所有候选给相同权重，而是会更强地看当前问题更相关的位置
- 只有把 baseline 平均和 attention 加权平均放在一起比较，才会看清为什么要选择重要位置
- 即使候选集合相同，只要问题改变，权重也会重新分配
- 改成问答场景以后，attention 是`该更强地看哪里`这个问题会变得更清楚

在看代码之前，先猜一猜：同样的候选集合里，如果只换问题，权重会集中到哪里，会更有帮助。

| 问题 | baseline 里容易出现的误解 | 在 attention 里先应该预测的变化 |
| --- | --- | --- |
| `压力释放保持时间是多少？` | 容易觉得所有候选都可以差不多地混在一起 | `pressure_hold_time` 的权重应该最大 |
| `冷却水流量标准是什么？` | 容易觉得候选集合没变，上下文也应该和前一个问题差不多 | `coolant_flow_limit` 的权重应该最大 |
| 两个问题都是 | 容易觉得一个平均值就够了 | 只要问题变了，即使候选相同，上下文也应该变化 |

输入（input）：

这里使用上面整理好的问题和各句子的分数候选。

```python
# 这个例子比较同一组候选句子中问题改变时，baseline 平均和 attention 加权 context 如何不同。
import math

question = "What is the pressure-release holding time?"
flow_question = "What is the coolant-flow criterion?"
sentences = {
    "pressure_hold_time": 3.0,
    "coolant_flow_limit": 12.0,
    "high_temp_exception": 5.0,
}
scores_for_pressure = {
    "pressure_hold_time": 2.5,
    "coolant_flow_limit": 0.9,
    "high_temp_exception": 0.3,
}
scores_for_flow = {
    "pressure_hold_time": 0.8,
    "coolant_flow_limit": 2.4,
    "high_temp_exception": 0.4,
}

ordered_names = list(sentences.keys())
values = [sentences[name] for name in ordered_names]

uniform_weight = 1 / len(values)
baseline_context = sum(uniform_weight * v for v in values)

def run_attention(question, score_table):
    raw_scores = [score_table[name] for name in ordered_names]
    exp_scores = [math.exp(s) for s in raw_scores]
    total = sum(exp_scores)
    weights = [s / total for s in exp_scores]
    context = sum(w * v for w, v in zip(weights, values))

    print("question =", question)
    print("baseline_uniform_context =", round(baseline_context, 3))
    for name, weight in zip(ordered_names, weights):
        print(name, "weight =", round(weight, 3), "value =", sentences[name])
    print("weights =", [round(w, 3) for w in weights])
    print("context =", round(context, 3))
    print("shift_from_baseline =", round(context - baseline_context, 3))
    print()

run_attention(question, scores_for_pressure)
run_attention(flow_question, scores_for_flow)
```

在输出里，可以先看：权重到底有多强地集中到了和问题相关的候选上。

```text
question = What is the pressure-release holding time?
baseline_uniform_context = 6.667
pressure_hold_time weight = 0.762 value = 3.0
coolant_flow_limit weight = 0.154 value = 12.0
high_temp_exception weight = 0.084 value = 5.0
weights = [0.762, 0.154, 0.084]
context = 4.553
shift_from_baseline = -2.114

question = What is the coolant-flow criterion?
baseline_uniform_context = 6.667
pressure_hold_time weight = 0.151 value = 3.0
coolant_flow_limit weight = 0.748 value = 12.0
high_temp_exception weight = 0.101 value = 5.0
weights = [0.151, 0.748, 0.101]
context = 9.933
shift_from_baseline = 3.266
```

- 如果像 baseline 那样把所有候选完全平均，`coolant_flow_limit` 和 `high_temp_exception` 这类并不直接对应当前问题的值，也会被同样混进上下文里，于是上下文值会落在 `6.667`
- 在第一个问题里，获得最大权重的是 `pressure_hold_time`
- 所以最终上下文会主要被压力释放保持时间对应的句子拉过去
- `shift_from_baseline` 为负，表示当前问题直接相关的候选获得更大权重后，上下文表示被进一步拉向`压力释放保持时间`一侧
- 在第二个问题里，最大的权重会重新转到 `coolant_flow_limit`
- 于是即使候选集合完全没变，最后上下文也会明显改向冷却水流量标准
- 也就是说，attention 不会把所有位置一视同仁地平均，而是会更强地反映当前问题更相关的位置

这个例子里首先要看的产物，是不同问题下的 attention 权重。压力释放保持时间问题里，`pressure_hold_time` 的权重最大；冷却水流量标准问题里，`coolant_flow_limit` 的权重最大。

![压力释放保持时间问题的 attention 权重](/AiBook/assets/part-05/chapter-13/attention-pressure-question-weights-zh.png)

![冷却水流量标准问题的 attention 权重](/AiBook/assets/part-05/chapter-13/attention-flow-question-weights-zh.png)

第二个要看的产物，是上下文值。baseline 平均无法区分两个问题，所以停在 `6.667`；但 attention context 会随着问题不同，变成 `4.553` 和 `9.933`。

![baseline 与不同问题 attention 上下文比较](/AiBook/assets/part-05/chapter-13/attention-context-comparison-zh.png)

读输出数字时，也要把`同一组候选`和`随问题改变的权重`分开看。

| 比较 | 输出里先看到的东西 | 只看平均值时容易留下的解释 | 加上 attention 后改变的解释 |
| --- | --- | --- | --- |
| `baseline_uniform_context` | 两个问题的 baseline 都是 `6.667` | 候选集合相同，所以上下文也应该差不多不变 | baseline 无法反映问题，所以即使当前需要的位置改变，也停在同一个平均值 |
| `pressure_hold_time` 问题 | `pressure_hold_time` 权重最大，为 `0.762` | 数字 `3.0` 较小，所以 context 只是单纯下降了 | 问题指向保持时间，所以 attention 会重新分配权重，让保持时间候选被更强地参考 |
| `What is the coolant-flow criterion?` 问题 | `coolant_flow_limit` 权重最大，为 `0.748` | 候选相同，只是这次偶然选到了较大的数字 | 问题一改变，同一组候选的参考权重也重新分配，流量标准一侧的 context 被更强地形成 |

## 从问题-候选比较视角重新看

上面的数字并没有计算真实的完整词向量空间，但直觉很清楚。

- baseline 平均只反映`这些句子只是一起出现了`这个事实。
- attention 加权平均会按照`当前问题是什么`，在候选之间重新分配权重。
- 所以当问题从`压力释放保持时间`变成`冷却水流量标准`时，即使候选集合相同，最强参考的位置也会改变。

也就是说，attention 不是单纯收集更多信息的方式，而是`根据当前问题重新决定哪些信息应该被更强地混合`的方式。

attention 在 sequence-to-sequence translation 研究中获得了很大影响力，后来又延伸到 self-attention 和 Transformer，成为现代深度学习里重要的上下文参考方式。本节读者要留下的结论很简单：attention 与其说是`长期带着信息走的结构`，不如说更接近`重新强烈查看当前需要位置的结构`。下一节 P5-13.2 会继续说明，这种直接参考的想法怎样延伸为同一序列中的 token 彼此重新读取的结构。

## 检查清单

- 能解释 attention 是`重新参考需要位置的方式`吗？
- 能说明长期依赖问题和 attention 之间的连接吗？
- 能说明 attention 是一种在当前计算中更强地参考重要位置的方式吗？
- 能说出这是对长期依赖问题更直接的回应吗？
- 能把 attention 解释成不是`让记忆保留更久的方法`，而是`重新更强地查看当前需要位置的方法`吗？
- 能以当前问题为标准，说明 baseline 平均和加权平均之间的差异吗？
- 当只用长期保留状态的解释不足以说明为什么性能受阻时，能先想起 attention 的直接参考视角吗？
- 读下一节 self-attention 时，是否已经准备好先问：`当前 token 需要重新看同一序列里的哪里？`

## 来源与参考资料

- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, 确认日期：2026-07-19. [https://arxiv.org/abs/1409.0473](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, 确认日期：2026-07-19. [https://arxiv.org/abs/1406.1078](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }
