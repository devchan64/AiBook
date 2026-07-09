# P2-7.3 Python 解释器与脚本

> Section ID: `P2-7.3`
> Version: `v2026.07.07`

理解终端之后，下一个问题就是：Python 代码到底怎样被执行？

## 本节范围

本节区分 `Python interpreter`、`interactive mode`、`script`、`python -m ...` 这几种执行方式。

## 中心问题

为什么 `python`、`python example.py`、`print("hello")` 都和 Python 有关，却不在同一个层次上？

## 记住的视角

- `python` 是启动解释器的终端命令。
- `print("hello")` 是 Python 代码，不是 shell 命令。
- `python file.py` 是让 Python 运行一个脚本文件。
- `python -m ...` 是让 Python 运行某个模块。

## 简短检查

- 能区分 shell 命令与 Python 代码。
- 能说明交互执行与脚本执行的差异。
- 能说明为什么 `python -m ...` 和直接写 Python 代码仍然不是一回事。

## 来源与参考资料

- Python Software Foundation, [The Python Tutorial](https://docs.python.org/3/tutorial/interpreter.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
