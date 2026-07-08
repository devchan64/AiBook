# P1-11.2 RNN、Seq2Seq 与 Attention

> Section ID: `P1-11.2`
> Version: `v2026.07.07`

在 11.1 中，我们看了语言模型(language model)与嵌入(embedding)。语言模型会以概率方式处理单词和 token 的顺序，而嵌入会把单词和 token 变成可计算的向量表示(vector representation)。

这里要看的是：神经网络曾经如何尝试处理具有顺序的数据。

这里的核心问题是：当单词和 token 被转成向量之后，模型如何在内部处理它们的顺序与上下文？

这里重要的脉络是：

> RNN 通过把前一个状态传给下一次计算来处理顺序，  
> Seq2Seq 建立了把输入序列变成输出序列的结构，  
> Attention 则让模型在每个输出时刻都能重新参考输入中相关的位置。

在 Part 1 中，本节先建立 `RNN(recurrent neural network)`、`hidden state`、`LSTM`、`GRU`、`Seq2Seq(sequence-to-sequence)`、`Encoder-Decoder`、`Attention`、`fixed-length vector` 瓶颈之间的基本区分。11.1 讨论的是语言模型与嵌入，这里则处理更窄的问题：`变成向量后的 token 顺序和上下文，是如何被处理的`。Transformer 还不会在这里展开，而会在 11.3 继续。

## 本节范围

这里不会解释 Transformer。Transformer 会在 11.3 里讨论。

`RNN`、`hidden state`、`LSTM`、`Seq2Seq`、`Attention` 在开始时都可能听起来像顺序模型里的相似部件。先简短区分一下它们的作用：

| 术语 | 极简含义 | 本节中的作用 |
| --- | --- | --- |
| RNN | 把前一个状态传给下一步的顺序神经网络 | 处理顺序的第一种结构 |
| hidden state | 累积到当前为止输入信息的内部状态 | RNN 式上下文处理的核心 |
| LSTM/GRU | 为了更稳定地处理长上下文而设计的 RNN 变体 | 对 RNN 限制的补强 |
| Seq2Seq | 把输入序列映射成输出序列的结构 | 翻译、摘要等任务的框架 |
| Encoder-Decoder | 读取输入的部分与生成输出的部分 | Seq2Seq 的基本结构 |
| Attention | 在生成输出时回头参考相关输入位置的结构 | 通往 Transformer 的关键转折 |

这里至少要保留的区分是：`RNN 会累积顺序`、`Seq2Seq 做输入到输出的转换`、`Attention 会重新回看相关输入位置`。

这里主要聚焦 Transformer 之前的三条重要脉络：

| 主题 | 本节要看的问题 |
| --- | --- |
| RNN(recurrent neural network) | 模型如何把有顺序的输入逐步累积起来处理？ |
| Seq2Seq(sequence-to-sequence) | 输入句子如何变成输出句子？ |
| Attention | 在生成每个输出词时，模型如何决定输入的哪一部分更重要？ |

LSTM(long short-term memory) 与 GRU(gated recurrent unit) 是 RNN 家族里为处理长依赖(long-range dependency)而出现的重要结构。不过这里不会深入 gate 的公式与内部细节，只会说明它们为什么需要出现。

另外，这里也不会解释 `预训练(pretraining)` 或 `BERT/GPT` 的区别。这些主题会在 11.3 里与 Transformer 一起重新整理。

## 本节目标

- 把 RNN(recurrent neural network)理解为处理顺序数据的神经网络结构。
- 把 hidden state 理解为模型内部累计出来的状态，而不是人的记忆。
- 看到 LSTM 和 GRU 是为了处理长上下文而出现的 RNN 变体。
- 把 Seq2Seq 理解为把输入序列(input sequence)变成输出序列(output sequence)的结构。
- 理解 Encoder-Decoder 结构中的 fixed-length vector 瓶颈。
- 把 Attention 理解为在每个输出时刻，用权重去参考输入中相关位置的结构。
- 不把 Attention 夸大成人类有意识的注意或逻辑理解。

## 三个基准

这里不会先看公式，而是先看神经网络是如何尝试处理顺序与上下文的。只要抓住下面三个基准，整体脉络就会清楚。

| 基准 | 为什么重要 | 本节所需的理解水平 |
| --- | --- | --- |
| RNN 通过把前一个状态传给下一步计算来处理顺序 | 这能说明为什么顺序数据需要专门结构。 | 只要理解成前面的信息会一点点被带到后面即可。 |
| Seq2Seq 是把输入序列变成输出序列的结构 | 这能帮助理解翻译、摘要这类问题是如何被建模的。 | 只要把它看成“把一句话变成另一句话”的框架即可。 |
| Attention 让模型在输出时回看相关输入部分 | 这为进入 Transformer 做好关键铺垫。 | 只要理解成它试图不再把所有信息都硬塞进一个固定向量即可。 |

## RNN 会把前一个状态传给下一次计算

n-gram 语言模型只使用较短的前文。但句子本身是顺序数据(sequence data)：前面出现的信息会影响后面的解释。

例如下面这句话：

> 我今天早上把昨天从图书馆借来的书读完了。

如果想理解 `读完了`，只看紧挨着的前一个词往往不够；如果能保留前面已经出现过 `书` 这一信息，会更有帮助。

RNN(recurrent neural network)正是为处理这类顺序数据而提出：它会把前一个时间步的 hidden state 传给下一步计算。

> 输入 1 -> 状态 1  
> 输入 2 + 状态 1 -> 状态 2  
> 输入 3 + 状态 2 -> 状态 3

这里的 hidden state 并不等于人类有意识的记忆(memory)。它是模型在处理到当前时，由前面输入累计出来的内部向量状态。

> hidden state：  
> 让前面输入能够继续影响当前计算的内部状态

正因为如此，RNN 才能被用于句子、语音、时间序列(time series)这类顺序很重要的数据。

## RNN 在长上下文上会遇到困难

RNN 的基本想法很直接，也很强，但要稳定地学习长上下文并不容易。为了学习相距较远的词之间的关系，误差信号必须跨越许多时间步回传。在这个过程中，gradient 可能会变得太小(vanishing gradient)或太大(exploding gradient)。

在入门阶段，可以这样理解：

> 短上下文：  
> 前面的信息比较容易传到后面
>
> 长上下文：  
> 重要信息可能在多步传递后变弱或变得不稳定

LSTM(long short-term memory) 就是为了解决这类长依赖问题而被广泛使用的 RNN 变体。它使用 cell state 和 gate 结构，来调节哪些信息应该保留、哪些应新接收、哪些应被输出使用。

GRU(gated recurrent unit) 则是另一种较简化的门控结构，但目的相近。这里不会详细比较 LSTM 与 GRU。更重要的是看到：RNN 家族的研究，是围绕 `如何在顺序数据中更久地保留和处理有用信息` 这个问题发展起来的。

## Seq2Seq 会把输入顺序变成输出顺序

Seq2Seq(sequence-to-sequence) 是一种接收输入序列并生成输出序列的结构。最典型的例子是机器翻译(machine translation)。

> 输入序列：  
> I read a book.
>
> 输出序列：  
> 我读了一本书。

Seq2Seq 的基本结构就是 Encoder-Decoder。

| 组成 | 作用 |
| --- | --- |
| Encoder | 读取输入序列并构造内部表示。 |
| Decoder | 根据该内部表示生成输出序列。 |

Sutskever、Vinyals、Le 在 2014 年的论文中提出了一种通用 sequence learning 方法：一个 LSTM 把输入序列变成固定维度向量，再由另一个 LSTM 从该向量中生成输出序列。Cho 等人的 RNN Encoder-Decoder 论文也提出：一个 RNN 把符号序列编码成 fixed-length vector，再由另一个 RNN 把它解码成另一串符号序列。

从入门角度看，可以把它想成：

> 输入句子  
> -> Encoder  
> -> 句子向量  
> -> Decoder  
> -> 输出句子

这和 11.1 中讲到的嵌入是相连的。模型不只是把单词表示成向量，还会把整句话进一步压缩成某种内部向量表示。

## fixed-length vector 可能成为瓶颈

基础的 Encoder-Decoder 结构有一个重要弱点：整个输入句子都必须被压进一个 `fixed-length vector`。

对于很短的句子，这看起来还可以接受：

```text
I read.
-> [句子向量]
-> 我读了。
```

但如果句子很长：

```text
把一段同时包含预算、时间表、风险、负责人和下一步任务的会议内容翻译出来。
-> [一个句子向量]
-> 输出句子
```

当所有输入信息都必须压缩进一个向量时，一些重要细节就可能变弱或丢失。Bahdanau、Cho、Bengio 的 Attention 论文正是把这种 fixed-length vector 视作基础 encoder-decoder 结构中的瓶颈(bottleneck)，并提出：在生成每个输出词时，模型应该能重新查看输入句子中相关的部分。

## Attention 会重新查看重要的输入位置

Attention 是一种在每个输出步骤中，按照权重(weight)去参考多个输入位置的结构。

例如，把英语句子翻译成韩语时：

> Source:  
> The cat sat on the mat.
>
> 正在生成的 Target：  
> 猫 ...

当模型生成对应 `cat` 的部分时，source 里的 `cat` 更重要；而当它生成对应 `on the mat` 的部分时，source 后面的那一段会更重要。

Attention 让模型更像这样工作：

> 在每个输出步骤里  
> 给输入各位置打分  
> 把这些分数规范化成权重  
> 按这些权重混合输入表示形成 context vector  
> 再用这个 context vector 生成下一个输出词

Bahdanau 等人的论文把这描述成 decoder 对 source sentence 中相关部分进行自动 `soft-search`。这里的 `soft` 不表示只挑一个固定位置，而是表示可以把权重分配给多个输入位置。

## Attention 不等于人类的有意识注意

因为名字叫 Attention，人们很容易把它理解成人类那种有意识的注意力。本节不会用这种解释。

更安全的说法是：

> Attention：  
> 为当前输出计算输入各位置权重的一种结构

Attention 能帮助模型更多地参考输入中相关的部分。在某些情况下，attention weight 也可以被可视化，因此更容易观察模型大致参考了哪里。

但 attention weight 不能直接被当成“模型真正的理由”或“完整的人类式理解”。在这里，Attention 只保持在更安全的角色上：

> 它是缓解 sequence-to-sequence 模型瓶颈的重要结构

## 为什么这会通向 Transformer

RNN、Seq2Seq、Attention 都是 LLM 直接谱系中非常重要的一部分。但如果要解释现代 LLM 的核心结构，还需要再往前走一步。

基于 RNN 的模型必须按顺序一步步计算，因为它总是把前一个状态传给后一个状态。处理长序列时，这种顺序计算本身就会形成负担。

Attention 展示了更强的想法：直接去参考输入中相关的位置。Transformer 则把这件事推进得更彻底，它把 Attention 放在中心位置，并使用 self-attention，让同一序列中的 token 在没有 recurrence 的情况下互相参考。

这里先记住这些就够了：

> RNN：  
> 通过传递前一个状态来处理顺序
>
> Seq2Seq：  
> 把输入序列转换成输出序列
>
> Attention：  
> 在每个输出时刻按权重参考相关输入位置
>
> Transformer：  
> 把 Attention 扩展成中心结构

Transformer 的具体结构以及预训练 LLM(pretrained LLM)会在 11.3 中继续。

## 本节应记住的视角

RNN、Seq2Seq、Attention 都属于同一条努力：它们试图不再把语言看成简单的单词列表，而是看成带有顺序与上下文的数据。

> RNN 会在内部状态里累积顺序。  
> Seq2Seq 会把输入顺序变成输出顺序。  
> Attention 会在生成输出时重新查看相关输入部分。

知道这条脉络，就不容易把 Transformer 和 LLM 误看成凭空出现的结构。Transformer 应该放在更早的问题意识之上理解：长上下文、输入输出对应、瓶颈减少，以及更强并行计算的需要。

## 简短检查

- 我可以说明 RNN(recurrent neural network)会把前一个 hidden state 传给下一次计算。
- 我可以把 hidden state 解释成内部向量状态，而不是人的记忆。
- 我可以把 LSTM 与 GRU 解释成处理长依赖的 RNN 变体。
- 我可以把 Seq2Seq(sequence-to-sequence)解释成从输入序列到输出序列的结构。
- 我可以区分 Encoder 和 Decoder 的角色。
- 我可以说明 fixed-length vector 为什么会成为瓶颈。
- 我可以把 Attention 解释成对输入各位置加权参考相关信息的结构。
- 我可以避免把 Attention 夸大成有意识注意或完整可解释性。
- 我已经准备好在 11.3 里继续理解 Transformer 为什么把 Attention 放到中心。

## 什么时候要先想起这个视角

当 Transformer 之前的 sequence modeling 脉络消失了，导致现代 LLM 看起来像突然冒出来的结构时，就可以先想起本节。

- 当需要重新说明 RNN 为什么要为顺序数据单独设计时
- 当需要整理 Seq2Seq(sequence-to-sequence) 与 Encoder-Decoder 如何建模翻译、摘要等任务时
- 当需要把 Attention 和 fixed-length vector 瓶颈的缓解联系起来时

此时可以先区分：`累积顺序的结构`、`把输入序列变成输出序列的结构`、`在生成输出时重新回看相关输入位置的结构`。这样就不会把 Transformer 误看成单独的发明，而会把它放在前面一连串问题与解法之上理解。

## 来源与参考资料

- Kyunghyun Cho et al., [Learning Phrase Representations using RNN Encoder-Decoder for Statistical Machine Translation](https://arxiv.org/abs/1406.1078){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, 确认日期: 2026-06-23.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, 确认日期: 2026-06-23.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, 确认日期: 2026-06-23.
- Graham Neubig, [Neural Machine Translation and Sequence-to-sequence Models: A Tutorial](https://arxiv.org/abs/1703.01619){: target="_blank" rel="noopener noreferrer" }, arXiv, 2017, 确认日期: 2026-06-23.
