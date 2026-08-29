<a id="cpu-offloading"></a>

## CPU offloading

- 含义：CPU offloading 是一种内存管理方式。在模型执行时，不把所有权重和中间计算长期放在 GPU VRAM 中，而是把暂时不用的模块或权重放在 CPU 内存侧，需要时再移动到 GPU。
- 为什么重要：它能帮助读者把“模型能不能在有限 GPU 内存中跑起来”和“生成结果质量好不好”分开记录。CPU offloading 可以降低 out-of-memory 失败的风险，但不会直接提升 prompt 遵循、pose 控制或输出质量。
- 相关概念：`计算限制(computational limit)`, `张量(tensor)`, `推断(inference)`, `开放权重模型(open-weight model)`
- 中心 Section: `P6-21.2`
- 出现 Section: `P7-5.1`, `P7-5.2`, `P7-5.3`, `P7-5.11`
