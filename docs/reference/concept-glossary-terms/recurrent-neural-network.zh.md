<a id="recurrent-neural-network"></a>
<a id="rnn-recurrent-neural-network"></a>

## RNN，循环神经网络

- 含义: RNN 是一种把上一步的隐藏状态传给下一步计算、用来处理有顺序数据的神经网络结构。它不是一次看完整个输入，而是按顺序一步一步读取，并把信息累积在内部状态里。
- 为什么重要: RNN 展示了神经网络早期怎样尝试处理语言、时间序列等顺序数据。理解 RNN，才能更清楚地比较门控记忆设计和后来的 Transformer 为什么要用不同方式处理长距离上下文。
- 相关概念: `隐藏状态`, `长程依赖`, `Transformer 架构(Transformer)`
- 核心 Section: `P1-11.2`
- 出现 Section: `P5-12.1`, `P5-12.2`
