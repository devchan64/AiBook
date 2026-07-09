# P2-14.2 分支、提交与文档可复现性

> Section ID: `P2-14.2`
> Version: `v2026.07.09`

P2-14.2 把 Git 从“单个提交”继续推进到“工作流分离”。它解释为什么写作分支与发布分支，不应该总被当成同一条工作线。

## 本节范围

本节聚焦 branch 角色、commit 分组、deployment 判断与 document reproducibility。

## 中心问题

为什么“写作中的判断”与“可以发布的说明”应该留在不同 branch 和不同 commit 单位上？

## 记住的视角

- branch 是用来分离工作流的具名历史线。
- 写作与发布常需要不同的判断标准。
- 好的 commit 边界提升的不只是代码整理，也包括文档可复现性。
- 在 deployment 前，应把链接、导航、资源与说明范围一起检查。

## 简短检查

- 能说明为什么文档项目也需要 branch 分离。
- 能说明什么样的 commit 边界更利于复现。
- 能说明为什么 deployment 是一次发布判断，而不只是另一次保存。

## 来源与参考资料

- Scott Chacon and Ben Straub, [Git Branching](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
- GitHub Docs, [About GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages){: target="_blank" rel="noopener noreferrer" }, 确认日期: 2026-07-09.
