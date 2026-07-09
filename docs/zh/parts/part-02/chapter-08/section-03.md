# P2-8.3 字典：按键查值的结构

> Section ID: `P2-8.3`
> Version: `v2026.07.07`

列表适合顺序重要的场景，但并不是所有数据都最适合按位置来读。有时更自然的问题是：我应该按哪个名字、字段或 ID 去查？

## 本节范围

本节入门介绍 `dictionary`、`key`、`value`、`mapping`、`get()`。

## 中心问题

为什么按 key 查找和按位置查找不是一回事？

## 记住的视角

- dictionary 是从 key 到 value 的映射。
- key 回答的是“我靠什么来查”。
- 初学阶段，先把 dictionary 理解成 mapping，会比一开始就陷进 hash table 实现更安全。

## 简短检查

- 能区分 list 访问和 dictionary 访问。
- 能分别解释 key 与 value。
- 能说明当 key 可能不存在时，为什么 `get()` 有帮助。

## 来源与参考资料

- Python Software Foundation, [Mapping Types — dict](https://docs.python.org/3/library/stdtypes.html#mapping-types-dict){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
