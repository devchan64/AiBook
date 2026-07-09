# P2-12.2 选择、过滤与聚合

> Section ID: `P2-12.2`
> Version: `v2026.07.09`

P2-12.2 整理三种常见的表读取动作：挑出某些列或行、保留满足条件的行、把许多值压缩成更少的总结数字。

## 本节范围

本节以入门层级介绍基本 selection、filtering、aggregation 与 `groupby`。

## 中心问题

为什么“保留什么”“丢掉什么”“概括什么”虽然都发生在同一个 DataFrame 上，却是不同的表动作？

## 记住的视角

- selection 选择要看的表部分。
- filtering 按条件保留或丢弃行。
- aggregation 把很多行压缩成更小的总结。
- 当总结问题依赖类别时，`groupby` 很常出现。

## 简短检查

- 能说明选一列与过滤多行的区别。
- 能说明为什么 aggregation 回答的是不同于 selection 的问题。
- 能说明为什么 `groupby` 常出现在模型检查或报告之前。

## 来源与参考资料

- pandas, [Indexing and selecting data](https://pandas.pydata.org/docs/user_guide/indexing.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- pandas, [Group by: split-apply-combine](https://pandas.pydata.org/docs/user_guide/groupby.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
