# P5-13.2 通向 self-attention 的流程

Section ID: `P5-13.2`
Version: `v2026.07.18`

在 P5-13.1 里，我们把 attention 解释成了`更强地参考当前计算里重要位置的方式`。接下来立刻会跟出下一个问题。

如果不只是输入和输出分开的 encoder-decoder 参考，而是让同一句工作指令里的各个位置也能彼此直接参考，会发生什么变化？

这个问题的核心答案，就是 self-attention。

self-attention 是一种方式：序列里的每个 token 会参考同一序列里的其他 token，并重新计算自己的当前表示。

当需要在 Transformer 之前再次简短确认这个核心机制时，可以回到英文概念词汇表里的 [self-attention](/AiBook/en/reference/concept-glossary/#self-attention) 条目重新对齐。

## 本节范围

- self-attention 和 attention 有什么不同？
- 为什么`在同一序列内部彼此参考`这个想法很重要？
- self-attention 在计算感觉上和 RNN 有什么不同？
- 为什么它会走向 Transformer 的核心？

本节首先要抓住的核心，是`token 不再按顺序接收状态，而是重新去参考同一序列里的其他 token，并为自己生成新的表示`。所以这里比起 optimizer、regularization 之类的训练程序，我们更先看的是：同一序列里的 token 怎样通过重新计算关系来再次彼此参考，并更新自己的表示。

完整的 Transformer 结构会在 P5-14.1 和 P5-14.2 继续展开，query、key、value 与 multi-head attention 的入门说明，会在补充学习 P5-13.3 再回收。

本节必须收住的一句话只有一个。它不再是`token 会不会接收到顺序状态`，而是要让读者理解这种计算感觉的转移：`token 会不会重新参考彼此，并更新自己的表示。`

## 本节目标

- 能把 self-attention 解释成`序列内部 token 之间的相互参考`。
- 能说明 self-attention 给人的计算感觉和 RNN 式顺序传递不同。
- 能说明 self-attention 在并行处理和长上下文问题上带来什么优势。
- 能通过可运行的 Python 例子，确认 token 之间重要度参考的直觉。

## attention 和 self-attention 有什么不同

广义地说，attention 是`决定当前计算应该更强地参考哪些位置的方式`。而在 self-attention 里，关键差别是：这些参考目标就在同一序列内部。

例如，在一句话里面：

- 每个词都可以参考其他词
- 当前词的表示，也可以通过重新聚合同一句子里相关 token 的信息来更新

也就是说，self-attention 不是`从句子外面拿信息进来`，而是`重新阅读句子内部的关系`。

如果 P5-13.1 是在问`当前输出应该更强地参考输入的哪里`，那么这里问题就变成了`当前 token 会怎样重新参考同一句子里的其他 token`。

把同一场景放进这两种方式里，差异会更明显。

| 同一场景 | attention 里先看的关系 | self-attention 里先看的关系 |
| --- | --- | --- |
| 正在写一行多语言工作指令短语的时刻 | 当前输出短语该更强地参考输入步骤里的哪个位置 | 当前工作指令句子里的每个 token 会怎样重新参考其他 token |
| 正在生成一句交接摘要时 | 当前摘要句子该更多看原文哪一句 | 记录内部的 token 表示会怎样彼此重新参考并再次变化 |
| 正在解释一行维修代码时 | 当前输出该更强地参考前面的哪个输入位置 | 代码里的名字、条件、调用位置会怎样再次彼此连起来 |

也就是说，如果说 attention 更接近`当前输出该更强地看哪里`，那么 self-attention 更接近`句子内部每个位置该怎样重新阅读其他位置`。这里真正的关键，不只是参考目标移到了内部，而是：对每个当前 token 来说，重新计算出来的参考分布可能都不一样。

如果只把从 attention 过渡到 self-attention 的这一步压缩一下，可以这样读。

```mermaid
--8<-- "assets/part-05/chapter-13/attention-to-self-attention-bridge-zh.mmd"
```

也就是说，`当前输出该看输入里的哪里`这种参考方式，可以被理解成向内扩展成了`每个 token 该怎样重新看同一序列里的其他 token`。

## 为什么这件事重要

RNN 通常会给人一种很强的感觉：状态会顺着时间流向被一路传下去，无论是单向还是双向。self-attention 不一样，它让当前 token 在需要时，可以相对更直接地参考远处的 token。

核心差别在于，RNN 更接近`把状态继续传下去`，而 self-attention 更接近`重新计算需要的 token 关系`。

`RNN 更像是在传递记忆，而 self-attention 更像是在重新找到需要的词。`

也就是说，面对久远信息会变淡的问题，self-attention 提供的是一条更直接的参考路径。本节读 self-attention 的关键，不在于`它看见了整句话`，而在于`当前 token 会重新计算它真正需要的关系`。

这个差别还可以用下面这张更短的表来抓。

| 视角 | RNN 家族 | self-attention |
| --- | --- | --- |
| 基本感觉 | 把状态传给下一个 step | 重新计算所有 token 之间的相关性 |
| 获取远处信息 | 要经过很多 step 传递 | 可以更直接地参考 |
| 计算感觉 | 顺序传递 | 关系计算 |

读者这里必须抓住的一点，是`self-attention 不是在传递记忆，而是在重新计算关系的结构。`

## 句子内部会发生什么

例如，在句子：

`The animal didn't cross the road because it was tired.`

里，要理解 `it` 指的是谁，就必须看句子里其他词和它之间的关系。self-attention 对这种入门直觉非常贴切。

每个 token：

- 不只看自己
- 会计算自己和其他 token 的相关性
- 更强地吸收更重要 token 的信息
- 然后生成新的表示

也就是说，self-attention 会在上下文中把 token 的表示重新写一遍。

如果把这句话换成一个更短的例子，再读一次，会是下面这样。

```text
电池包放在工作台上，绝缘帽放在旁边的托盘里。它还没有被套上。
```

这里在读 `它` 时，如果只看紧挨着前面的一个词，并不足以稳定判断它指的是`托盘`还是`绝缘帽`。从 self-attention 的视角看，`它` 这个位置会重新参考句子里的其他词，并对更符合当前上下文的候选赋予更大权重。也就是说，核心感觉是：`为了理解当前一个 token，要把整句话重新混起来再读一次。`

## 为什么它会成为 Transformer 的核心

self-attention 重要，并不只是因为它`看起来更聪明`。更重要的是，它改变了计算结构本身。

尤其从读者角度看，下面两点差异最重要。

1. 它能更直接地参考远处的位置。
2. 它不必只靠顺序传状态，因此很适合并行计算。

也就是说，self-attention 看起来像是同时更好满足了长期依赖问题和并行处理需求的方向。这也是它为什么会成为 Transformer 核心部分的原因之一。

换句话说，self-attention 会走到结构中心，是因为`它更容易重新找到远处线索，同时也更容易把计算整体地一起处理`。这里真正重要的，不只是`这里有 attention`，而是`重新写每个 token 表示的这段计算`变成了以 block 为中心的结构。

读者还要再抓住一点：self-attention 并不只是`一个好用的功能`，而是成了`以 block 为中心的计算`。也就是说，Transformer 把`先用 self-attention 重新阅读关系，再把结果交给下一步计算`这种结构，当成了可重复的基本单元。这条连接正是 P5-14.1 的起点。

## 如果把它画得非常简单

```mermaid
--8<-- "assets/part-05/chapter-13/self-attention-token-graph-zh.mmd"
```

这张图压缩的是：每个 token 都可以参考其他 token 这个直觉。真实实现会更精细，但这里首先要确认的是：token 并不是只把信息从前传到后，而是会一起计算彼此的相关性。

`一个 token 不只是从前一个 token 那里接收信息，而是会把句子里的其他 token 一起重新参考，再重建自己的表示。`

如果再很短地固定一次：即使是在同一句输入里，只要当前 token 变化，重新要看的位置也会变，那么可以看成下面这样。

```mermaid
--8<-- "assets/part-05/chapter-13/self-attention-target-shift-zh.mmd"
```

如果把 attention 权重画成柱状图，这个差异会更直接。同样一份备忘录里，当当前 token 是 `它` 和当前 token 是 `套上` 时，重新参考的线索分布并不相同。

![当前 token `它` 的 self-attention 权重](../../../assets/part-05/chapter-13/self-attention-weight-it-zh.svg)

![当前 token `套上` 的 self-attention 权重](../../../assets/part-05/chapter-13/self-attention-weight-cover-zh.svg)

从这组比较里，首先要抓住的是下面几点。

- 即使读的是同一句话，`它` 重新看的线索和 `套上` 重新看的线索也不同。
- 所以 self-attention 的核心，不是`整句话只读一次`，而是`每个当前 token 重新看的位置都可能不同`。
- 只有先把这个感觉抓住，后面再看 QKV 和 multi-head，才更容易把它们读成`每个 token 的问题`和`被拆开的关系`这些计算名字。

## 为什么 self-attention 很适合并行处理

RNN 会按时间顺序传状态，因此计算流程给人的感觉很顺序化。self-attention 更容易把每个 token 的相关性计算放在一种更矩阵化的形式里处理，所以很适合 GPU 并行计算。

`self-attention 更接近一次性把 token 之间的关系都算出来，而不是只按顺序把 token 往前推。`

这一点也会自然地连接到 Part 5 里关于 GPU、batch、tensor 计算的讨论。

## 案例与示例

### 代表案例：句子内部的指代解释

假设一条安全检查备忘录写着：`电池包已经拆下，但绝缘帽还没有套上。那就是风险原因吗？` 人粗略读的时候，通常会先只看 `那` 旁边紧挨着的词来猜意思。但实际上，`那` 到底指的是绝缘帽，还是指拆下这件事，会直接改变后续处置内容。如果只跟着附近词走，就很容易漏掉这种指代关系。这里真正变化的地方，是判断标准从`只看前一个词`，转成了`把整句关系一起看`。self-attention 给人的直觉是：当前 token 会重新参考句子里的其他位置，更直接地计算它到底指的是什么。

所以，这个案例里要确认的结果是：当前 token `那` 是否不是只看前一个词，而是能更清楚地显示：句子里几个候选位置中，究竟哪一个应该被更强地重新参考。

同样的视角也会直接延伸到一句话里条件范围的解释，以及一行代码的阅读里。不过，本节真正要抓住的不是领域名称，而是`对于每个当前 token，要重新看的对象会不会不同，以及新的表示会不会跟着变。`

| 案例 | 当前位置需要重新看的对象 | 如果只跟着附近位置会出现的问题 | 用 self-attention 要确认的结果 |
| --- | --- | --- | --- |
| 代词解释 | 代词所指向的前面名词 | 如果只跟着相邻词，很可能错误连接 | 是否通过反映整句关系，选出了更合理的指代对象 |
| 条件范围解释 | 条件表达、动作表达、否定范围 | 如果只跟着动作词，就可能误读禁止到底延伸到哪里 | 是否通过重新阅读句子关系，把条件影响范围重新组合起来 |
| 一行代码解释 | 变量名、否定、逻辑运算符 | 如果只跟着最显眼的变量，就可能误读条件含义 | 是否通过重新阅读代码序列关系，把否定和组合顺序一起理解到位 |

| 人容易先看的标准 | 从 self-attention 视角重新读时的标准 |
| --- | --- |
| 觉得整句话读一遍之后，有一个共同上下文就够了 | 因为每个 token 从自己位置重新要看的对象不同，所以每个 token 的新表示也应该不同 |
| 觉得重要线索是整句只决定一次的 | `它` 觉得重要的线索，和 `套上` 觉得重要的线索，可能并不相同 |
| 容易把 self-attention 只理解成`它看到了整句话` | 核心不是平等地看整句话，而是为每个 token 重新计算关系 |

把这三个案例放在一起，会更清楚地看到：self-attention 的核心，不是`整句话读一次`，而是`每个当前 token 要重新看的东西会不同，因此新的表示也会不同`。

## 练习与例子

这个例子的目标，是直接确认：在一条安全检查备忘录里，像 `那` 这样的当前 token，到底会更强地参考哪些前面的候选对象，以及这样做之后它自己的表示会怎样变化。也就是说，我们要把 self-attention 当成`当前 token 重新阅读备忘录里相关线索的过程`来实验，而不是把它看成单纯的数值平均。

问题场景：

- 当前 token 的解释，只有在它重新参考的不只是邻近词，而是句子里多个位置时，才可能发生变化

输入：

- 一条短备忘录：`The battery pack was separated, but the insulating cap was not put on. Is that the cause of the risk?`
- 当前 token `that`、`cover` 对句子里各个 token 的参考分数
- 每个 token 的简单语义向量

输出：

- 把所有 token 一视同仁平均后的 baseline 表示
- 在 `that`、`cover` 位置上算出来的 attention 权重
- 经过 self-attention 后每个 token 的新表示
- 哪一组 token 被反映得最强的摘要

在看代码之前，如果先按顺序看下面这三个值，会更容易抓住 self-attention 和`把整句话直接平均`之间的差别。

| 先看的值 | 为什么应该先看它 |
| --- | --- |
| `baseline_representation` | 因为它会先显示：如果完全不区分权重，当前 token 的解释会被混得多模糊 |
| `weights` | 因为它能直接比较：当前 token 在句子里到底更强地重新看了哪些线索 |
| `representation_shift` | 因为最后它能把 attention 重算之后，当前 token 表示到底往哪个方向移动，归纳在一起 |

问题场景：

- 把 self-attention 理解成当前 token 对句子里其他 token 的重新参考，会更直观

要确认的概念：

- self-attention 是一种结构：当前 token 会重新参考句子里的其他 token，并改变自己的表示
- 在代词解释这种远处线索重要的场景里，比起简单平均，更需要按位置分配权重
- 即使句子相同，只要当前 token 改变，重新参考的对象也会改变
- 只有把 baseline 表示和新表示放在一起比较，self-attention 的作用才会显出来

在看代码之前，先猜一猜：即使句子相同，只要当前 token 变了，权重会往哪里聚，会更有帮助。

| 当前 token | baseline 里容易出现的误解 | 在 self-attention 里先应该预测的变化 |
| --- | --- | --- |
| `that` | 如果只看整条备忘录的平均值，很容易觉得不必区分哪条安全线索更重要 | 更高权重应该会落到 `insulating_cap` 和 `not_put_on` 附近 |
| `cover` | 因为还在同一份备忘录里，很容易觉得它的分布会和 `that` 差不多 | 在动作上下文里，更高权重可能会落到 `separated` 和 `insulating_cap` |
| 两者都是 | 很容易觉得一条句子只有一组共同的 attention 分布 | 每个 token 都应该从自己的角度重新决定要看哪里 |

这个表真正想让我们确认的差别正是这一点。`that` 需要重新缩小的是`风险原因到底指什么`，而 `cover` 需要重新缩小的是`缺失的动作上下文到底是什么`。也就是说，即使在同一份备忘录里，只要当前 token 不同，这个例子就应该让`需要重新看的线索`也随之不同。

输入：

这里使用上面整理好的 token 列表，以及每个 token 的向量表示。

```python
import math

tokens = ["battery_pack", "separated", "insulating_cap", "not_put_on", "that"]
token_vectors = {
    "battery_pack": [0.8, 0.1, 0.0],
    "separated": [0.9, 0.3, 0.1],
    "insulating_cap": [0.1, 0.9, 0.2],
    "not_put_on": [0.0, 0.6, 0.8],
    "that": [0.3, 0.3, 0.3],
}

# current token-specific raw scores:
# "that" focuses on what the risk refers to,
# while "not_put_on" focuses more on the action context around insulating the pack.
raw_scores_by_target = {
    "that": {
        "battery_pack": 0.2,
        "separated": 0.6,
        "insulating_cap": 2.1,
        "not_put_on": 1.2,
        "that": 0.7,
    },
    "not_put_on": {
        "battery_pack": 0.1,
        "separated": 1.4,
        "insulating_cap": 1.8,
        "not_put_on": 0.9,
        "that": 0.2,
    },
}

baseline_representation = [0.0, 0.0, 0.0]
uniform_weight = 1 / len(tokens)
for token in tokens:
    vector = token_vectors[token]
    for idx in range(len(vector)):
        baseline_representation[idx] += uniform_weight * vector[idx]

print("baseline_representation =", [round(value, 3) for value in baseline_representation])

print()

def run_self_attention(target_token, score_table):
    ordered_scores = [score_table[token] for token in tokens]
    exp_scores = [math.exp(score) for score in ordered_scores]
    total = sum(exp_scores)
    weights = [s / total for s in exp_scores]

    new_representation = [0.0, 0.0, 0.0]
    for weight, token in zip(weights, tokens):
        vector = token_vectors[token]
        for idx in range(len(vector)):
            new_representation[idx] += weight * vector[idx]

    print("target_token =", target_token)
    for token, weight in zip(tokens, weights):
        print(token, "weight =", round(weight, 3), "vector =", token_vectors[token])
    print("weights =", [round(w, 3) for w in weights])
    print("new_representation =", [round(value, 3) for value in new_representation])
    print(
        "representation_shift =",
        [round(new - base, 3) for new, base in zip(new_representation, baseline_representation)],
    )
    top_token = tokens[weights.index(max(weights))]
    print("top_token =", top_token)
    print(
        "cap_plus_not_applied_weight =",
        round(weights[tokens.index("insulating_cap")] + weights[tokens.index("not_put_on")], 3),
    )
    print()

run_self_attention("that", raw_scores_by_target["that"])
run_self_attention("not_put_on", raw_scores_by_target["not_put_on"])
```

在输出里，可以先比较每个 token 的 `weight`，看看即使还是同一句子，只要当前 token 变化，分布会怎样改变。然后再继续看 `new_representation` 和 `representation_shift` 会朝什么方向分开。

```text
baseline_representation = [0.42, 0.44, 0.28]
 
target_token = that
battery_pack weight = 0.074 vector = [0.8, 0.1, 0.0]
separated weight = 0.11 vector = [0.9, 0.3, 0.1]
insulating_cap weight = 0.494 vector = [0.1, 0.9, 0.2]
not_put_on weight = 0.201 vector = [0.0, 0.6, 0.8]
that weight = 0.122 vector = [0.3, 0.3, 0.3]
weights = [0.074, 0.11, 0.494, 0.201, 0.122]
new_representation = [0.244, 0.642, 0.307]
representation_shift = [-0.176, 0.202, 0.027]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.694

target_token = not_put_on
battery_pack weight = 0.074 vector = [0.8, 0.1, 0.0]
separated weight = 0.272 vector = [0.9, 0.3, 0.1]
insulating_cap weight = 0.406 vector = [0.1, 0.9, 0.2]
not_put_on weight = 0.165 vector = [0.0, 0.6, 0.8]
that weight = 0.082 vector = [0.3, 0.3, 0.3]
weights = [0.074, 0.272, 0.406, 0.165, 0.082]
new_representation = [0.37, 0.578, 0.265]
representation_shift = [-0.05, 0.138, -0.015]
top_token = insulating_cap
cap_plus_not_applied_weight = 0.571
```

| 先看的输出 | 这个输出意味着什么 | 如果改动它，会跟着改变什么 |
| --- | --- | --- |
| `weights` 里 `insulating_cap` 最大，`not_put_on` 也很高 | 说明当前 token `that` 并不是平均地看这条备忘录，而是会更强地重新参考某些安全线索 | 如果修改 raw score，真正牵引当前 token 解释的线索会立刻改变 |
| `that` 和 `not_put_on` 的 `weights` 分布并不相同 | 说明即使在同一条备忘录里，每个当前 token 重新看的对象也会不同 | 如果换 target token，哪个位置会成为 top token 也会立刻变化 |
| `top_token = insulating_cap` 和 `cap_plus_not_applied_weight = 0.694` 一起出现 | 说明拉动解释的不是单个词，而是一组彼此相关的线索 | 如果降低 `insulating_cap` 或 `not_put_on` 的分数，就能看到风险原因解释会往哪边摇动 |
| `representation_shift` 的第二个轴增加得很明显 | 说明经过 attention 后，当前 token 的表示确实又往一个特定上下文方向移动了 | 如果修改 token vector，就能直接比较哪个语义轴更容易被重新计算强调 |

| 当前 token | 如果只看 baseline，容易得到的判断 | 看过 self-attention 输出后会改变的判断 |
| --- | --- | --- |
| `that` | 因为整条备忘录像一个整体，容易把 `separated` 和 `insulating cap not applied` 当成差不多的线索 | 因为 `insulating_cap` 和 `not_put_on` 的权重更高，风险原因应优先检查到`绝缘帽未套上`这一侧 |
| `not_put_on` | 容易只顺着当前动作读成`有个动作没有做` | 因为它会重新强烈参考 `separated` 和 `insulating_cap`，所以还需要一起恢复`什么没有套到什么上`的作业上下文 |

也就是说，读这些数字的目的并不是记住`哪个 weight 最大`。真正要确认的是：即使在同一条备忘录里，只要当前 token 变化，`现在需要重新确认什么`也会真的分开。

- 在 baseline 平均里，`battery_pack`、`separated`、`insulating_cap`、`not_put_on` 都被用相同权重混在一起，因此并没有突出当前 token `that` 到底指向什么。
- 当前 token 的表示并不是只靠它自己决定，而是会通过重新参考备忘录里的其他 token 再计算一次。
- 在这个例子里，`that` 对 `insulating_cap` 和 `not_put_on` 的参考远大于对 `separated` 的参考，所以风险原因解释会向`绝缘帽未套上`这边倾斜。
- 即使还是同一条备忘录，只要把 `not_put_on` 当成当前 token，`separated` 和 `insulating_cap` 的比重又会重新升高，分布会和解释 `that` 时不同。
- `insulating_cap` 与 `not_put_on` 的合计权重达到 0.694，说明 self-attention 反映的不是单个词，而是一个相关线索束。
- `representation_shift` 里第二个轴明显增加，会给人一个直觉：当前 token 的表示又被拉向了 `insulating_cap/not_put_on` 这条上下文方向。
- 也就是说，self-attention 可以被读成一种方式：它会为每个 token 单独量化`现在要理解这个 token，句子里该重新看哪里`。

如果把这些结果重新翻回现场备忘录阅读，读 `that` 时，视线会集中到`到底缺了什么`；而读 `not_put_on` 时，视线会集中到`这个动作没有作用到什么对象上`。self-attention 就可以被理解成把这种`按 token 分开的重新确认路径`做成了计算。

这个例子也最好不要只读一遍结果就停下，而是继续看看：改哪些值，会让这种`重新参考`的感觉更清楚。

| 先看到的输出信号 | 现在就可以尝试的变化 | 先不要急着下的结论 |
| --- | --- | --- |
| `insulating_cap` 的权重最大 | 提高 `separated` 或 `battery_pack` 的 raw score，看看风险原因解释中心会往哪里移动 | 不要因为 attention 权重很大，就立刻断定完整语义理解已经被保证 |
| `cap_plus_not_applied_weight` 很高 | 降低或提高 `not_put_on` 的分数，看看线索束会怎样一起移动 | 不要因为两个线索都很高，就断定答案永远已经固定 |
| `representation_shift` 明显偏离 baseline | 修改 token vector 的各轴，比较哪个语义轴对重算更敏感 | 不要把这一段简单向量比较直接拿来替代真实的 multi-head self-attention 全部结构 |

也就是说，self-attention 是一种`看过上下文之后，再把表示重新计算一遍的方式`。

## 如果从重新解释当前 token 的角度再读这个例子

前面的数字并没有实现真正的大规模 self-attention 全部结构，但比较标准已经很清楚。

- baseline 平均更接近于`把整句话的信息一股脑混起来得到的表示`
- self-attention 的结果更接近于`重新去问当前 token that 现在应该更强地参考谁，然后据此重算出来的表示`
- 所以读者真正该区分的，不是单纯`有没有看整句话`，而是`有没有为每个当前 token 重新算出不同的 rereading priority`

也就是说，self-attention 并不只是一个`看见了整句话`的功能，而是一种`每个 token 都从自己的立场重新读完整句子，并生成新表示的计算`。只有抓住这个感觉，P5-13.3 里的 QKV 和 multi-head attention 才不会被读成`记名字的一节`，而会更像是`把这种重新参考计算解释得更有结构的一节`。

在 self-attention 里真正要确认的转折，是 attention 不再只是翻译的辅助装置，而是移动成了 sequence modeling 的中心计算方式。本节读者最后应该留下的结论也很简单。self-attention 不是`整句话只看一次`，而是`每个当前 token 都会重新计算要看的位置，并重建自己的表示`。下一章 P5-14.1 会继续解释：这种计算会怎样被组织成 Transformer block 的基本单元。

## 检查清单

- 能解释 self-attention 是同一序列里的 token 彼此参考的方式吗？
- 能说明顺序状态传递和关系重算之间的差别吗？
- 能把 self-attention 解释成不是`看整句话`，而是`每个 token 重新参考同一序列里的其他 token 并更新自己的表示`吗？
- 能说明它和 RNN 不同的优势：既能重新参考远处线索，又能让 token 计算更适合并行处理吗？
- 能通过例子说明：即使在同一句子里，只要当前 token 是 `that` 还是 `not_put_on` 不同，重新看的线索和判断优先级也会不同吗？
- 当 token 之间关系重算看起来比顺序传递更重要时，能先想到 self-attention 视角吗？
- 在读下一章 Transformer 时，是否已经准备好先问：`为什么 self-attention 会变成以 block 为中心的计算？`

## 来源与参考资料

- Ashish Vaswani et al., `Attention Is All You Need`, NeurIPS 2017, 确认日期：2026-06-29。
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, `Neural Machine Translation by Jointly Learning to Align and Translate`, ICLR 2015, 确认日期：2026-06-29。
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, 确认日期：2026-06-29。 [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
