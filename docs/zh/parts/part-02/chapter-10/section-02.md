# P2-10.2 Jupyter、Colab 与本地执行的区别

> Section ID: `P2-10.2`
> Version: `v2026.07.09`

P2-10.1 把 notebook 看成计算文档。这里再区分三种经常混在一起的执行方式：Jupyter、Colab、本地执行。

## 本节范围

本节只聚焦执行位置、runtime、文件访问、共享条件，不做功能手册。

## 中心问题

为什么看起来像同一个 notebook 文件，放在不同执行位置就会表现不同？

## 记住的视角

- Jupyter 是 notebook 工具生态。
- Colab 是基于 Jupyter notebook 风格的托管服务。
- 本地执行是直接用自己机器上的 Python、文件和包。
- notebook 文件和正在运行的 runtime 不是同一回事。

## 简短检查

- 能说明 Jupyter 和 Colab 的关系。
- 能说明为什么文件访问取决于执行位置。
- 能说明为什么共享 notebook 文件不等于共享相同 runtime。

## 来源与参考资料

- Google, [Colaboratory FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
