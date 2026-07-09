# P2-7.4 虚拟环境与包

> Section ID: `P2-7.4`
> Version: `v2026.07.07`

会运行 Python 代码只是第一步。更现实的问题很快就会出现：为什么 Python 能跑，但 NumPy 却像是不存在？

## 本节范围

本节入门介绍 `virtual environment`、`package`、`pip`、`import`。

## 中心问题

为什么包的问题通常要去看 Python 环境，而不是只盯着代码本身？

## 记住的视角

- 虚拟环境是给一个项目单独分开的 Python 空间。
- `pip install ...` 和 `import ...` 不是同一个动作。
- Colab runtime 里的包和本地 `.venv` 里的包不属于同一个空间。

## 简短检查

- 能把虚拟环境解释成分开的执行空间。
- 能说明安装与 import 为什么是两个阶段。
- 能说明为什么同一段代码在 Colab 和本地 `.venv` 里可能表现不同。

## 来源与参考资料

- Python Packaging Authority, [Installing packages](https://packaging.python.org/en/latest/tutorials/installing-packages/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
