# P2-7.5 依赖与可复现性

> Section ID: `P2-7.5`
> Version: `v2026.07.07`

理解虚拟环境和包之后，还会剩下一个问题：包安装过一次就结束了吗？

## 本节范围

本节入门介绍 `dependency`、`reproducibility`、`requirements.txt`、`version pinning`。

## 中心问题

为什么只保存代码还不够，如果我们想在以后或别的机器上得到同样的结果？

## 记住的视角

- 依赖是代码之外、但代码又必须依靠的条件。
- 可复现性意味着要留下足够信息，重新搭回同样环境。
- `requirements.txt` 和版本记录是在把“这里能跑”变成“别处也能重跑”。

## 简短检查

- 能说明什么是 dependency。
- 能说明为什么 reproducibility 既是环境问题也是代码问题。
- 能说明为什么包版本会影响结果。

## 来源与参考资料

- Python Packaging Authority, [Requirements Files](https://pip.pypa.io/en/stable/reference/requirements-file-format/){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
