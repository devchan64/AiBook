# P2-3.5 Python 运行环境：Colab 与本地 PC

> Section ID: `P2-3.5`
> Version: `v2026.07.09`

在用 NumPy 检查线性代数之前，先要区分“代码到底在哪里运行”。

这里先按两个环境说明：

1. 浏览器里的 Google Colab
2. 本地电脑上的终端与 Python 安装环境

## 本节范围

本节只区分执行位置与命令形态，不展开完整安装流程。

## 先抓住的一张表

| 想做的事 | Colab 代码单元 | 本地终端 | Python 代码 |
| --- | --- | --- | --- |
| 安装 NumPy | `%pip install numpy` | `python -m pip install numpy` | 这里不用 |
| 导入 NumPy | `import numpy as np` | 这里不用 | `import numpy as np` |
| 运行简单计算 | `print(np.array([1, 2]))` | `python example.py` | `print(np.array([1, 2]))` |

## 为什么会混淆

初学者最常见的问题不是内容完全错，而是“把对的句子写在了错的位置”。

## 记住的视角

- 环境和语法是绑在一起的。
- 终端命令与 Python 代码不能混着读。
- Colab 与本地环境是在不同位置完成相似的任务。

## 简短检查

- 能说明 `%pip install numpy` 应该写在哪里。
- 能说明 `python -m pip install numpy` 应该写在哪里。
- 能说明 `import numpy as np` 应该写在哪里。

## 来源与参考资料

- Google, [Google Colab FAQ](https://research.google.com/colaboratory/faq.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-06-24.
