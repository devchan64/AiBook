<a id="query-key-value-qkv"></a>

## query-key-value, QKV

- 含义: QKV 是 attention 里的三个角色。query 表示当前位置想找什么，key 表示每个位置能用什么条件被匹配，value 表示真正要被混合并传递出去的内容。
- 为什么重要: QKV 把 attention 从“看哪里”这种直觉，拆成“提出查询、匹配位置、取回内容”的计算流程。它也帮助读者区分相似度计算用的信息和真正传递下去的内容。
- 相关概念: `self-attention`, `multi-head attention`, `Transformer`
- 核心 Section: `P5-13.3`
- 出现 Section: `P5-14.1`, `P6-4.3`, `P6-4.4`
