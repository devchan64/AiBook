# P2-14.1 Git 是管理变更历史的工具

> Section ID: `P2-14.1`
> Version: `v2026.07.07`

P2-14.1 把焦点从数组、表与图，转到“什么改了、为什么改了”的记录问题。重点不只是保存文件，而是把有意义的变更组合保留下来，方便之后解释。

## 本节范围

本节以入门层级介绍 Git、version control、commit、staging area、repository。

## 中心问题

为什么追踪变更历史，不等于简单保存文件的最新版本？

## 记住的视角

- Git 记录的是带说明的变更历史，而不只是最新文件状态。
- `git add` 与 `git commit` 分开，是因为“挑哪些变更”和“确认这条记录”是两件事。
- `git status`、`git add`、`git commit`、`git log` 构成最小可用的 Git 读取循环。
- 在学习项目里，文档、代码、图片、笔记常属于同一个变更单位。

## 简短检查

- 能说明为什么 commit 不只是一次保存动作。
- 能说明 working tree、staging area、repository 的区别。
- 能说明为什么即使是以文档为主的 AI 学习项目也需要 Git。

## 来源与参考资料

- Scott Chacon and Ben Straub, [Pro Git, 2nd Edition](https://git-scm.com/book/en/v2){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
