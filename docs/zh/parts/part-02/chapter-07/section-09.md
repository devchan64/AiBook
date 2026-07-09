# P2-7.9 补充学习：检查常见的本地 Python 环境问题

> Section ID: `P2-7.9`
> Version: `v2026.07.09`

虚拟环境、依赖、安装、环境变量都看过之后，一个实际问题又会回来：本地 Python 环境不断出错时，应该怎样检查？

## 本补充节范围

本节给出常见本地 Python 环境问题的第一层检查顺序，不试图成为完整排障百科。

## 中心问题

在“全部重装”之前，怎样先确认自己现在到底在看哪一个 Python 环境？

## 记住的视角

- 先把代码问题和环境问题分开。
- 在盲目改包之前，先问“当前激活的是哪一个 Python？”
- 重新安装不是第一个问题，先识别当前环境才是。

## 简短检查

- 能说明为什么“我现在用的是哪个 Python”是前置诊断问题。
- 能说明为什么环境问题和代码问题必须分开。
- 能说明为什么包状态、路径、激活的虚拟环境要一起看。

## 来源与参考资料

- Python Packaging Authority, [Python Packaging User Guide](https://packaging.python.org/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
