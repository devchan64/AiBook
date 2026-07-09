# P2-10.3 把笔记本整理成可重新执行的记录

> Section ID: `P2-10.3`
> Version: `v2026.07.09`

P2-10.1 介绍了 notebook 作为“代码加说明”的文档，P2-10.2 区分了执行位置。这里进一步问：什么样的 notebook 才值得以后继续相信？

## 本节范围

本节入门介绍 `re-runnable record`、`execution order`、`hidden state`、`runtime state`。

## 中心问题

怎样把一个“可读”的 notebook，整理成一个也“可重跑”的记录？

## 记住的视角

- 好的 notebook 既要可读，也要可重跑。
- 单元顺序很重要，因为隐藏的 runtime 状态会改变结果。
- import、setup、数据准备、输出、解释都应该有意识地安排。
- 有些最初写在 notebook 里的代码，之后应该转移到 `.py` 文件中复用。

## 简短检查

- 能说明为什么“能跑一次”还不够。
- 能用入门方式解释 hidden state。
- 能说明为什么“重启后从上到下重跑”是有价值的检查。

## 来源与参考资料

- Jupyter, [Notebook Basics](https://jupyter-notebook.readthedocs.io/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
