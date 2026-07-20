# P5-12.1 为什么需要循环神经网络（RNN）、长短期记忆（LSTM）和门控循环单元（GRU）

Section ID: `P5-12.1`
Version: `v2026.07.18`

在 P5-11 章里，我们已经看到，CNN 能很好地处理图像这类具有空间结构的数据中的局部模式。把数据类型换一下，这里就会自然出现下一个问题。

像句子、语音、时间序列这样顺序（order）很重要的数据，该怎么处理？

尝试回答这个问题的结构，就是循环神经网络（RNN）、长短期记忆（LSTM）和门控循环单元（GRU）。

循环网络这一类结构，并不只看当前输入，而是想把前面见过的一部分信息继续带下去，用来处理序列数据（sequence data）。

如果关于顺序状态结构的基本名称又开始混在一起，可以一起回到英文概念词汇表里的 [RNN（recurrent neural network）](/AiBook/en/reference/concept-glossary/#rnn-recurrent-neural-network)、[LSTM（long short-term memory）](/AiBook/en/reference/concept-glossary/#lstm-long-short-term-memory)、[GRU（gated recurrent unit）](/AiBook/en/reference/concept-glossary/#gru-gated-recurrent-unit)条目重新对齐。

## 本节范围

- 为什么在序列数据里，顺序这个概念很重要？
- 只靠一般的 feed-forward 结构，会出现什么不顺手的地方？
- 循环神经网络引入了什么想法？
- 为什么后来还需要 LSTM 和 GRU？

本节首先要收住的核心，是`在序列数据里，改变当前判断的并不只是最后一个输入，而是前面累积下来的状态`。也就是说，这里先收住的是`为什么要把序列状态带下去`，以及`为什么只靠 basic RNN 很难长时间记住信息`。long-term dependency 问题会在下一节 P5-12.2 里更集中地展开。

## 本节目标

- 能说明为什么在序列数据问题里，`顺序`和`上下文（context）`很重要。
- 能把 RNN 解释成`把前一状态继续带下去的结构`。
- 能把 LSTM 和 GRU 的出现，与长期记忆维持问题联系起来。
- 能通过可运行的 Python 例子，确认累积的序列状态会怎样实际改变判断。

## 为什么序列数据是特殊的

在序列数据（sequence data）里，如果项目的顺序变了，含义也可能跟着变。

例如，在句子里，即使单词相同，只要顺序改变，意思就会不同。在语音里，即使是同一段声音碎片，也可能因为前后节奏不同而听起来像不同发音。在传感器数据里，很多时候比起最后一个数字本身，更重要的是它之前是怎样上升、怎样下降的。

也就是说，序列数据和简单的集合（set）或表格中的一行不同，它包含了`前后关系`。在序列数据里，重要的不只是出现了什么，还包括它是按照什么顺序出现的。

## 为什么只靠一般的 feed-forward 结构会觉得不顺手

一般的 feed-forward network 很适合一次性接收输入，再直接送出输出。但一到序列数据里，它的局限就会很快露出来。

例如，当我们读到句子结尾的`确认了`时，这个词的意义会因为前面是否已经出现过`阻断`、`泄漏`、`禁止`这样的线索而不同。在传感器数据里也是一样。最后一个值是 80，并不自动意味着每次都应得到同样判断。这个 80 到底是缓慢上升累积出来的，还是短暂跳高以后又重新上来的，会让当前状态被读成不同含义。

也就是说，在序列数据里，我们经常需要把`现在看到的输入`和`之前看过的输入`连起来。问题在于，一般的 feed-forward 结构并不擅长把这种累积流程直接保留在结构本身里。

这时，RNN 的基本想法就出现了。

把这种差异非常简短地并排放在一起，会是下面这样。

| 结构 | 读取输入时的感觉 |
| --- | --- |
| feed-forward | 一次收到输入，就直接送到输出 |
| RNN | 在看当前输入时，也把前一状态一起带着 |

把同一场景分别放进这两种结构里看，差异会更直接。

| 同一场景 | 用 feed-forward 先读时容易留下什么 | 用 RNN 先读时更能抓住什么 |
| --- | --- | --- |
| 句子结尾的否定表达 | 当前单词本身的即时信号 | 从前面单词一路累积下来的句子流向 |
| 解释一小段语音碎片 | 此刻听见的声音碎片形状 | 和前一声音片段连起来的时间上下文 |
| 判断最后一个传感器值 | 当前数字的大小本身 | 前面几个 step 的上升与下降趋势 |

## RNN 引入了什么

RNN 的核心想法其实可以概括得很简单：`在处理当前输入时，也把前一个 step 准备好的状态一起用上。`

也就是说，RNN 在每一个时间点（time step）都会接收：

- 当前输入 \(x_t\)
- 前一状态 \(h_{t-1}\)

然后生成新的状态 \(h_t\)。

关键点在于，RNN 想把之前看到的信息当作一种状态带着走，再和下一步计算一起传下去。所以在本节读 RNN 时，比起先记住`它看当前输入`，更适合先抓住`它把当前输入和前一状态一起看`这个差别。

把它画得非常简单，就是下面这样。

```mermaid
--8<-- "assets/part-05/chapter-12/rnn-state-flow-zh.mmd"
```

这张图里需要确认的结果是：当前输出并不是只由此刻输入决定的。前一时间点的状态会继续传到下一时间点，并和当前输入一起产生影响。

## 为什么只靠 RNN 还不够

basic RNN 提供了一个很重要的想法，但真实的序列数据并不会总是这么短、这么简单。状态不断被传到下一个 step 时，前面见过的线索会随着距离变远而慢慢变弱；而当前输入一旦很强，较早之前的信息就更容易被挤掉。

也就是说，`想记住`这个想法，和`真的能稳定地记很久`，是两回事。这种差距会直接通向下一节里的 long-term dependency 问题。

## 所以 LSTM 和 GRU 出现了

LSTM 和 GRU 是想更好处理 basic RNN 记忆问题的结构。

关键在于，LSTM 和 GRU 会更细致地控制：什么应该留下更久，什么应该丢掉，以及当前输入应该被反映多少。也就是说，它们不只是`更复杂的 RNN`，更适合被理解成`想把记忆管理得更好的 RNN`。

在入门阶段，把这个差异读成下面这样就足够了。

- basic RNN 展示的是`把状态继续带下去`这个想法
- LSTM 和 GRU 补强的是`怎样把这个状态保留得更久、更稳定`

## 为什么 LSTM 和 GRU 两个都要学

在入门阶段，名字一多容易混乱。但先像下面这样区分就够了。

- RNN：把序列状态继续带下去的最基本想法
- LSTM：更强地处理记忆维持问题的代表结构
- GRU：用稍微更简洁的形式实现相似目标的结构

也就是说，更适合把这三者看成不是互不相关的竞争者，而是`处理序列记忆问题的同一家族发展流向`。

在入门阶段，先抓住下面这张表里`状态传递`、`记忆调节`、`结构简化`的差别，就已经够用了。

| 名称 | 首先要抓住的直觉 |
| --- | --- |
| RNN | 把状态传给下一个 step |
| LSTM | 更细致地控制哪些信息该长期保留、哪些该丢弃 |
| GRU | 用更简洁的结构实现相似目标 |

与其把模型名字分开死记，不如顺手把在小型序列场景里首先该想到什么问题一起留下，这样整体流程会更稳。

| 小型序列场景 | 先想到的结构 | 为什么它会成为起点 |
| --- | --- | --- |
| 像短运维备忘录那样，只需要把前后几个词的流向接起来时 | RNN | 因为它最适合直接看见`当前输入 + 前一状态`这个最基本的序列状态想法 |
| 需要把句尾否定表达、句首主语这类稍远一点的线索保持更久时 | LSTM | 因为它通过更细致地控制保留与丢弃，更直接处理长期记忆维持问题 |
| 想实现和 LSTM 相近的目标，但希望结构更简洁一点时 | GRU | 因为它在保留序列记忆补强感的同时，让状态调节结构相对更易读 |

这张表的目的，并不是决定`哪个模型永远更强`。在本节里，只要先抓住这样一个问题场景手柄就够了：`第一次引入序列状态时先看 RNN，记忆维持变得更重要时再看 LSTM/GRU。`

## 案例与示例

### 代表案例：解释运维备忘录

可以想一想这样一句运维备忘录：`确认有泄漏，但没有批准重新启动。` 人在读备忘录时，如果中途看见`批准`或`重新启动`这样的词，很容易先往工作继续进行的方向理解。但只有当最后的否定表达`没有`和前面的`泄漏`线索一起留下来，才不会漏掉这句话真正的意思其实是`重新启动应暂缓`。如果只看最后几个词，或者把单词拆开来看，就很容易误读。也就是说，即使是在读当前位置的意思时，前面的词和中间上下文也一样重要。把序列状态继续带下去的结构，正是为这种`前面出现过的风险线索和后面出现的审批否定必须一起保留下来`的情况而需要的。

所以，这个案例里要确认的结果，是模型有没有只跟着最后那个`批准`类词走，而是把前面的泄漏线索和后面的否定表达一起保留下来，最终让判断真正收束为`重新启动暂缓`。

同样的视角也会直接延伸到设备警报声识别和时间序列预测里。不过，本节真正要抓住的核心不是领域名称，而是`同样的最后输入，只要前面积累下来的状态不同，结论会不会变。`

把这三个案例放在一起，会更清楚地看到：RNN/LSTM/GRU 不该只被读成`时间轴模型的名字`，而应该被读成`同样的最后输入，也会因为累积状态不同而导向不同结论的结构`。

| 案例 | 只看当前输入时容易漏掉什么 | 序列状态额外补进来的上下文 | 本节要确认的结果 |
| --- | --- | --- | --- |
| 运维备忘录解释 | `泄漏`、`阻断`这类前面线索的即时含义 | 即使最后的确认短语相同，也会因为前面线索不同而改变安全解释的流程 | 最终判断是否反映了前面的处置流程，而不是只看最后一个词 |
| 设备警报声识别 | 一小段波形碎片本身的含糊性 | 重复节奏和警报模式在前后碎片间延续的时间上下文 | 同一声音碎片是否会因为前后连接不同而被更稳定地解释 |
| 时间序列预测 | 最后一个数字本身的大小 | 前面几个 step 的上升与下降趋势 | 同样的最后值，是否会因为前面的流向不同而触发不同警报 |

| 人容易先看的标准 | 从序列状态视角重新读时的标准 |
| --- | --- |
| 如果最后一个词或最后一个值相同，应该会得到相似判断 | 即使最后输入相同，只要前面累积的流向不同，就会形成不同状态和不同结论 |
| 中间线索像是补充说明，不是关键 | 如果中间线索没有累积进状态里，最后输入本身的解释也很容易摇晃 |
| 很容易只把序列模型记成`用于时间轴数据的模型名字` | 真正的核心是：这里额外加入了`当前输入 + 前一状态`这种判断结构 |

## 练习与例子

这个例子的目标，是确认`把前一状态传给下一步`这句话在实际判断里到底会造成什么差别。这一次，我们把一个完全不带序列状态的简单 baseline，和一个会把序列状态继续带下去的 baseline 并排比较。也就是说，我们会通过实际输出来确认：`只看最后输入的判断`，和`把前面流向保留下来的判断`，到底会从哪里开始分开。

在读例子之前，先把本节实际需要确认的最小点固定下来，会更清楚。

| 确认点 | 在例子里直接要看的值 | 为什么重要 |
| --- | --- | --- |
| baseline 判断和状态型判断会从哪里分开 | `baseline_last_word_label`、`baseline_last_value_alert` 和最后的 `label`、`alert` | 说明序列模型看的不是最后一个输入，而是累积状态 |
| 状态会怎样一步一步累积 | 每一行输出里的 `state=` | 说明 RNN 家族结构的核心不是当前输入的即时判断，而是状态更新 |
| 为什么同样的最后输入也会导向不同结论 | `gradual_rise` 和 `temporary_spike` 在最后一个 step 的比较 | 让我们用眼睛直接确认：只要前一段流向不同，当前判断也会不同 |

输入：

- 三个具有相同最后确认短语的短运维备忘录
- 两条最后温度都为 `80` 的时间序列

输出：

- 只看最后输入的 baseline 判断
- 每个 step 更新的句子状态值
- 最终句子标签
- 只看最后一个值的 baseline 警报判断
- 每个 step 更新的传感器状态值
- 最后一个 step 的警报判断

问题场景：

- 在序列数据里，需要直接比较：只看最后值的方法，与持续更新中间状态的方法，到底有什么不同

要确认的概念：

- RNN 家族结构不是一次性看完整个输入，而是按 step 更新状态
- 和只看最后值的 baseline 放在一起比较时，序列状态更新的意义会更清楚

在看代码之前，先猜一猜 baseline 和状态型判断会在什么地方分开，会更有帮助。

| 场景 | 只看最后输入的 baseline 预测 | 累积状态一侧的预测 | 为什么要先抓住它 |
| --- | --- | --- | --- |
| `shutdown_confirmed` | 只看 `确认`，预测 `restart_allowed` | 前面的 `阻断` 处置仍然保留，所以预测 `hold_required` | 让我们看到：为什么即使最后一个词相同，前面的处置流向也必须保留在状态里 |
| `leak_confirmed` | 只看 `确认`，预测 `restart_allowed` | 前面的 `泄漏` 线索仍然保留，所以预测 `hold_required` | 让我们看到：即使最后一个词相同，只要前一状态不同，结论就会分开 |
| `gradual_rise` vs `temporary_spike` | 只看最后值 `80`，两者都预测为警报 | 只有持续上升那条会触发警报，短暂尖峰不会 | 让我们看到：即使最后值相同，只要前面趋势不同，留下的状态也会不同 |

输入（input）：

这里使用上面整理好的词信号、传感器信号和初始状态值。

![gradual rise 序列状态](/AiBook/assets/part-05/chapter-12/rnn-gradual-rise-state-zh.svg)

![temporary spike 序列状态](/AiBook/assets/part-05/chapter-12/rnn-temporary-spike-state-zh.svg)

这两张图会在运行代码前，先把`最后值相同`和`累积状态相同`分开来看。`gradual_rise` 和 `temporary_spike` 都以 80 结束，但因为序列状态也会保留前一段流向，所以最终警报解释可能不同。

```python
# 这个例子比较只看最后单词或最后传感器值的 baseline，与累积 sequential state 后的最终判断差异。
word_signal = {
    "leak": -2.2,
    "blocked": -1.5,
    "restart": 1.2,
    "confirmed": 0.8,
}

def classify_with_last_word(words):
    last_signal = word_signal.get(words[-1], 0.0)
    return "restart_allowed" if last_signal > 0 else "hold_required"

def run_sentence(name, words, alpha=0.7):
    state = 0.0
    print(f"[sentence: {name}]")
    print("baseline_last_word_label =", classify_with_last_word(words))
    for step, word in enumerate(words, start=1):
        signal = word_signal.get(word, 0.0)
        state = alpha * state + signal
        print(f"step {step}: word={word:>6}, signal={signal:>4}, state={state:>5.2f}")
    label = "restart_allowed" if state > 0 else "hold_required"
    print("final_label =", label)
    print()

def alert_with_last_value(sequence, threshold):
    return sequence[-1] >= threshold

def run_sequence(name, sequence, alpha=0.6, threshold=63):
    state = 0.0
    print(f"[sensor: {name}]")
    print("baseline_last_value_alert =", alert_with_last_value(sequence, threshold))
    for step, x in enumerate(sequence, start=1):
        state = alpha * state + (1 - alpha) * x
        alert = state >= threshold
        print(f"step {step}: input={x:>3}, state={state:>6.2f}, alert={alert}")
    print()

gradual_rise = [60, 65, 72, 80]
temporary_spike = [80, 60, 60, 80]

run_sentence("shutdown_confirmed", ["blocked", "confirmed"])
run_sentence("leak_confirmed", ["leak", "confirmed"])
run_sentence("restart_confirmed", ["restart", "confirmed"])
run_sequence("gradual_rise", gradual_rise)
run_sequence("temporary_spike", temporary_spike)
```

在输出里，可以先看 `baseline_last_word_label` 和 `final_label` 什么时候分开，再看中间的 `state` 是怎样累积的。

```text
[sentence: shutdown_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=  blocked, signal=-1.5, state=-1.50
step 2: word=confirmed, signal= 0.8, state=-0.25
final_label = hold_required

[sentence: leak_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=     leak, signal=-2.2, state=-2.20
step 2: word=confirmed, signal= 0.8, state=-0.74
final_label = hold_required

[sentence: restart_confirmed]
baseline_last_word_label = restart_allowed
step 1: word=  restart, signal= 1.2, state= 1.20
step 2: word=confirmed, signal= 0.8, state= 1.64
final_label = restart_allowed

[sensor: gradual_rise]
baseline_last_value_alert = True
step 1: input= 60, state= 24.00, alert=False
step 2: input= 65, state= 40.40, alert=False
step 3: input= 72, state= 53.04, alert=False
step 4: input= 80, state= 63.82, alert=True

[sensor: temporary_spike]
baseline_last_value_alert = True
step 1: input= 80, state= 32.00, alert=False
step 2: input= 60, state= 43.20, alert=False
step 3: input= 60, state= 49.92, alert=False
step 4: input= 80, state= 61.95, alert=False
```

- 在 `shutdown_confirmed` 和 `leak_confirmed` 里，只看最后一个词的 baseline 都给出 `restart_allowed`，但状态累积以后，前面的阻断与泄漏线索仍然留下来，所以最终会改成 `hold_required`
- `restart_confirmed` 则因为前一状态本身就是往重新启动方向累积，所以即使最后一个词相同，最终仍然保留 `restart_allowed`
- 在传感器例子里，两个序列都以 `80` 结束，所以 baseline 都会立刻报 True；但状态型判断会把前面趋势一起保留下来，因此只有 `gradual_rise` 在最后达到警报阈值

真正要先看的，不是最后一个词或最后一个值本身，而是：在中间各个 step 里，状态到底留下了什么。

| 比较 | 输出里先看到的现象 | 这组现象真正要抓住的意思 |
| --- | --- | --- |
| `shutdown_confirmed` 与 `leak_confirmed` | 最后词同样是 `确认`，但 `final_label` 仍然变成 `hold_required` | 说明前面的风险线索只要累积进状态里，就会改变最后那个词的解释 |
| `restart_confirmed` | 最后词也同样是 `确认`，但这次 `final_label` 保持 `restart_allowed` | 说明同样的最后输入，也会因为前一状态不同而落在不同结论 |
| `gradual_rise` 与 `temporary_spike` | 两者最后都到 80，但只有前者最后 `alert=True` | 说明状态保留下来的不只是最后值，还有它之前是怎样一路走过来的 |

也就是说，RNN 家族结构真正要解决的，不是`怎样把最后输入看得更清楚`，而是`怎样让当前判断不丢掉前面流程里已经出现过的重要线索。`

| 先看到的输出信号 | 现在就可以尝试的变化 | 先不要急着下的结论 |
| --- | --- | --- |
| `temporary_spike` 虽然最后值是 80，却没有触发警报 | 把 `alpha` 调高或调低，比较过去状态会被保留多久 | 不要立刻断定 RNN 家族总是无条件比最后值 baseline 更好 |
| 即使最后的 `confirmed` 相同，状态和结论仍然会分开 | 修改 `leak`、`blocked`、`restart` 的信号值，观察前面处置流向会留下多久 | 不要断定只靠几个词信号就能解释真实运维语言理解的全部 |
| 两条时间序列最后留下的 state 不同 | 把中间值再调高或调低，观察`持续趋势`和`短暂尖峰`会从哪里开始分开 | 不要把这一条简单的状态更新公式，当作对 LSTM、GRU 全部门控机制的替代 |

也就是说，RNN 的基本直觉，更接近`把前一状态带进来，再和当前输入一起形成新状态`，而不是`立刻对当前输入做分类`。LSTM 和 GRU，正可以被读成是为了把这个状态里的`哪些该多留一会儿`、`哪些该忘掉`控制得更好而出现的结构。

## 本节最少要记住什么

把下面这张表记住，本节就抓住核心了。

| 问题 | RNN 家族给出的起点 |
| --- | --- |
| 为什么序列数据不能只看最后一个输入？ | 因为前面的流向会累积成当前状态，一起改变判断 |
| RNN 的最基本想法是什么？ | 把前一状态和当前输入一起带进下一步计算 |
| 为什么还会出现 LSTM、GRU？ | 因为只靠 basic RNN，很难把状态稳定保留很久 |

换句话说，本节结尾首先要收住的不是 attention 预告，而是下面两句。

1. RNN 展示的是`把状态继续带下去`这个想法。
2. LSTM 和 GRU 补强的是`怎样把这个状态保留得更久、更稳。`

本节应该得到的判断标准其实很明确。即使最后一个词相同，或者最后一个数字相同，只要前面累积下来的流向不同，当前判断就可能不同。RNN 是最早把这种`累积状态`想法直接做进结构里的模型，而 LSTM 和 GRU 则是想补强这个状态，不让它过快变弱的结构。下一节 P5-12.2 会更具体地去看：这种`把状态继续传下去`的方式，会在什么地方开始摇晃，也就是为什么久远以前的线索很难一直抓到最后。

## 检查清单

- 能解释为什么在序列数据里，顺序和上下文会改变当前判断吗？
- 能把 RNN 说成`当前输入 + 前一状态`的结构吗？
- 能说明只看最后输入的 baseline，为什么会和状态型判断分开吗？
- 能把 LSTM、GRU 解释成对 RNN 记忆维持问题的补强吗？
- 能说明即使最后输入相同，只要累积状态不同，结论也会不同吗？
- 当看到句子、语音、时间序列时，能先想到`这里需要把前面状态带下去吗`这个问题吗？
- 能说明为什么 RNN、LSTM、GRU 会被归到同一家族里吗？
- 当输入类型本身不如前后顺序和累积上下文更重要时，能先想到序列状态视角吗？
- 能把 LSTM 和 GRU 解释成不是`另一个模型名字`，而是`想把状态更稳定地保留更久的补强结构`吗？

## 来源与参考资料

- David E. Rumelhart, Geoffrey E. Hinton, Ronald J. Williams, `Learning representations by back-propagating errors`, Nature, 1986, 确认日期：2026-06-29。
- Sepp Hochreiter, Jürgen Schmidhuber, `Long Short-Term Memory`, Neural Computation, 1997, 确认日期：2026-06-29。
- Kyunghyun Cho et al., `Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation`, arXiv, 2014, 确认日期：2026-06-29。
