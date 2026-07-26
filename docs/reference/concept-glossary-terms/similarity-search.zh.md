<a id="similarity-search"></a>

## 相似度检索

- 含义：相似度检索会寻找与问题或文档的向量表达接近的其他向量，并选择相关候选。它不只寻找完全相同的字符串，而是在表达空间中寻找语义上接近的候选。
- 为什么重要：相似度检索是 RAG 中寻找相关文档片段的核心步骤，因为它把 embedding 连接到实际检索流程。理解它也能看清关键词检索和向量检索并不只是竞争关系，有些问题需要两者结合，才能更稳定地找到依据。
- 相关概念：`embedding`，`retrieval-augmented generation, RAG`，`vector`，`similarity`，`top-k`
- 核心 Section：`P1-13.2`
- 出现 Section：`P1-13.3`, `P1-13.4`, `P6-3.1`

