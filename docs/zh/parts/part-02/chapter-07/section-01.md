# P2-7.1 本地环境与运行时

> Section ID: `P2-7.1`
> Version: `v2026.07.09`

前面只是为了跑 NumPy 练习，先把 Colab 和本地 PC 粗略分开。这里再往下一层：代码到底在哪里执行，又是谁在负责执行？

## 本节范围

本节入门区分 `local environment` 与 `runtime`，不展开完整安装教程。

## 中心问题

当一个计算已经准备好时，它到底在哪里执行，又是哪一个程序在读取它？

## 记住的视角

- 看起来相似的文本，可能属于完全不同的执行位置。
- runtime 可以先理解成当前正在运行 Python 的那套执行状态。
- 本地环境与托管环境表面相似，但在文件、包、持久性上会有实际差别。

## 简短检查

- 能说明“代码写在哪里”和“代码跑在哪里”的不同。
- 能说明为什么 `python --version` 和 `print("hello")` 不属于同一个位置。
- 能用入门方式解释 runtime。

## 来源与参考资料

- Python Software Foundation, [The Python Tutorial](https://docs.python.org/3/tutorial/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
