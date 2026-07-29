<a id="vector-database"></a>

## 向量数据库

- 含义：向量数据库是存储 embedding 向量，并同时管理搜索索引、metadata、过滤和更新的检索系统。它不是只保存几个向量的地方，而是实际搜索服务所需的基础设施层。
- 为什么重要：RAG 实现依赖的不只是向量比较算法，还包括存储、metadata 过滤、权限、更新和运营。这个概念能帮助读者把“寻找邻近向量”的数学问题，与“安全、快速、最新地取回哪些文档”的服务问题连接起来。
- 相关概念：`搜索索引(search index)`，`近似最近邻(ANN, approximate nearest neighbor)`，`元数据(metadata)`
- 核心 Section：`P6-12.1`
- 出现 Section：`P1-13.4`, `P6-3.2`, `P6-12.2`
