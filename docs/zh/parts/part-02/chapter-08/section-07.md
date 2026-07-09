# P2-8.7 补充学习：第一次区分引用、浅拷贝与深拷贝

> Section ID: `P2-8.7`
> Version: `v2026.07.07`

看过列表之后，很多读者会马上卡在同一个地方：为什么换了一个名字，原来的列表也一起变了？

## 本补充节范围

本节给出 `reference`、`shallow copy`、`deep copy` 的第一层区分。

## 中心问题

为什么给同一个对象再起一个名字，并不会自动生成一个新的独立副本？

## 记住的视角

- assignment 可以只是让另一个名字也指向同一个对象。
- shallow copy 只分开一层。
- deep copy 试图把嵌套层也分开。

## 简短检查

- 能说明为什么新变量名不等于新列表副本。
- 能说明 shallow copy 和 deep copy 的大区别。
- 能说明为什么一旦结构嵌套，复制问题会更麻烦。

## 来源与参考资料

- Python Software Foundation, [copy — Shallow and deep copy operations](https://docs.python.org/3/library/copy.html){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
