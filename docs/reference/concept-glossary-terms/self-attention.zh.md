<a id="self-attention"></a>

## self-attention

- 含义: self-attention 是让同一序列中的每个 token 根据其他 token 重新更新自己表示的 attention 机制。
- 为什么重要: self-attention 让模型在一个序列内部直接比较 token 之间的关系，而不必只依赖一步一步传递的隐藏状态。它是 Transformer 的核心机制之一。
- 相关概念: `attention`, `QKV`, `Transformer`
- 核心 Section: `P5-13.2`
- 出现 Section: `P1-11.3`, `P5-13.3`, `P5-14.1`, `P5-14.2`, `P6-4.1`
