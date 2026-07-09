# P2-8.4 循环：逐个处理 iterable

> Section ID: `P2-8.4`
> Version: `v2026.07.09`

看过列表和字典之后，下一个问题就是：怎样把一组值一个一个处理掉？

## 本节范围

本节入门介绍 `loop`、`iterable`、`for`、`enumerate()`、`items()`、`zip()`。

## 中心问题

在重复处理里，我们到底是在逐个拿出什么，又是在逐步生成什么结果？

## 记住的视角

- loop 不是单纯重复，而通常是对 iterable 做结构化遍历。
- `enumerate()` 适合位置也重要的时候。
- `.items()` 适合 key 和 value 要一起读的时候。
- `zip()` 适合把多个 iterable 并排对齐来读。

## 简短检查

- 能把 loop 解释成对 iterable 的逐个处理。
- 能说明什么时候 `enumerate()` 比普通 `for item in items` 更自然。
- 能说明什么时候该想到 `.items()` 或 `zip()`。

## 来源与参考资料

- Python Software Foundation, [Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
