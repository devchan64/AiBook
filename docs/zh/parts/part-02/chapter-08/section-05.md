# P2-8.5 函数与小规模复用

> Section ID: `P2-8.5`
> Version: `v2026.07.09`

值、数据结构、循环最终都会指向另一个实际问题：什么时候该把重复处理收束成一个可复用的小单元？

## 本节范围

本节通过 `input -> process -> output` 结构介绍函数，也会区分 `print` 与 `return`。

## 中心问题

怎样把我们已经在做的事情，整理成一个可复用的小单元？

## 记住的视角

- 函数是在给重复流程命名。
- 最有用的早期契约是 `input -> process -> output`。
- `print` 是显示结果，`return` 是把结果交回去。

## 简短检查

- 能说明为什么重复代码不该一直靠复制粘贴维持。
- 能说明打印结果和返回结果的区别。
- 能说明为什么函数像一个小型可复用契约。

## 来源与参考资料

- Python Software Foundation, [Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
