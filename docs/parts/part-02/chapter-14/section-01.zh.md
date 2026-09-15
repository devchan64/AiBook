# P2-14.1 Git 是管理变更历史的工具

> Section ID: `P2-14.1`
> Version: `v2026.09.15`

## 保存文件与记录变更

保存文件会留下当前状态，但不会自动说明之前的状态为何改变，也不会说明哪些文件一起发生了变化。

例如，假设完成了以下工作。

- 编写一节正文。
- 添加生成图表的脚本。
- 生成两张输出图片。
- 修改网站目录配置。

这四项工作看起来各自独立，实际上可以组成一个有意义的变更：“把一节的图表说明和相关资源一起更新。”

Git 用提交（commit）记录这样的变更组合。

提交指向当时已跟踪文件状态的快照。没有修改的文件也是该状态的一部分，与上一次提交比较就能看到哪些行发生了变化。提交信息用于说明修改目的，但 Git 不会自动判断文件的含义或修改理由。

## 过去的状态与修改理由

版本控制（version control）让我们找回文件的过去状态并比较变更。修改理由需要作者在提交信息等位置记录。阅读历史可以帮助回答以下问题。

- 哪些文件变了？
- 为什么改变？
- 哪些文件一起变了？
- 某段说明是什么时候加入的？
- 问题出现在哪次修改之后？

Git 官方书将版本控制解释为随时间记录文件变化、以后可以找回特定版本的系统。正文和示例代码也可以用这种方式检查过去的状态。

## 工作区、暂存区与仓库

工作区（working tree）存放正在编辑的文件，暂存区（staging area）保存选入下次提交的文件内容。提交会将暂存的状态记录到仓库（repository）的历史中。

```mermaid
--8<-- "assets/part-02/chapter-14/git-three-areas-flow-zh.mmd"
```

这条流程中需要区分“保存”和“提交”。

保存是在编辑器中把当前内容写入磁盘。提交是把选出的、有意义的一组变更记入仓库历史。

这些操作可以在本地计算机上离线完成。Git 是版本控制程序，GitHub 是在线托管 Git 仓库并支持协作的服务。只创建本地提交，不会自动上传到 GitHub。

## 查看状态：git status

使用 Git 时，通常首先用 `git status` 查看状态。

下面命令中的 `docs/...` 路径以本书仓库根目录为执行位置。尚未建立 Git 仓库的文件夹无法显示仓库状态；后面的“75 → 80 → 85 记录练习”会创建新仓库。

```bash
git status
```

这个命令回答以下问题。

- 哪些文件被修改了？
- 有没有新文件？
- 哪些文件已选入这次提交？
- 当前分支是什么？

文件名前的两个位置可以帮助区分暂存状态。

```bash
git status --short
```

在没有冲突的普通编辑状态下，第一列表示上次提交与暂存区之间的差异，第二列表示暂存区与工作区之间的差异。表中的 `·` 用来显示空格，实际输出中是空白。

| 标记 | 文件状态 | 普通提交包含的内容 |
| --- | --- | --- |
| `??` | 尚未跟踪的新文件 | 不包含 |
| `·M` | 已跟踪文件被修改，但未暂存 | 不包含新修改 |
| `M·` | 已暂存修改 | 已暂存的修改 |
| `MM` | 暂存后又修改同一文件 | 只包含先前暂存的修改 |
| `A·` | 新文件已暂存 | 暂存的新文件内容 |

即使 `git diff` 输出为空，也可能存在 `??` 文件。普通的 `git diff` 不显示未跟踪文件的内容，因此还要检查 `status`。

## 选择变更：git add

`git add` 并不意味着立刻把文件永久记录到历史中。它将选入本次提交的变更放进暂存区。

```bash
git add docs/parts/part-02/chapter-14/section-01.md
```

`git add` 暂存的是执行时的文件内容。之后再修改同一文件，新修改不会自动暂存。即使多个文件发生变化，也不必放进同一个提交。不同目的的变更分开提交，以后更容易阅读。

例如，以下两类工作通常适合分开记录。

| 变更 | 分开提交的理由 |
| --- | --- |
| 编写 Chapter 14 正文 | 目的是增加书的内容 |
| 修改 CSS 布局 | 目的是改善页面显示 |

将它们混在一起，会增加以后追踪“为什么修改 CSS”的难度。

如果误选了文件，可以在已经有提交的仓库中执行以下命令，只取消暂存，将它移出下一次提交。

```bash
git restore --staged -- docs/parts/part-02/chapter-14/section-01.md
```

`--staged` 保留工作区中的修改，只撤回下次提交的选择。不带这个选项的 `git restore` 可能还原文件内容本身，不能把两种操作视为相同。

## 记录历史：git commit

`git commit` 将暂存的变更写入仓库历史。

```bash
git commit -m "docs(part2): add git version control introduction"
```

提交信息为以后阅读历史的人提供一个说明“这次改了什么”的标题。

有用的提交信息通常符合以下条件。

- 能看出修改内容。
- 避免过于宽泛的表述。
- 表达修改目的，而不只是文件名。
- 以后在 `git log` 中阅读时仍有意义。

下面是一个不好的例子。

```bash
git commit -m "update"
```

它没有说明更新了什么。

## 阅读历史：git log

提交积累起来后，可以用 `git log` 查看历史。

```bash
git log --oneline
```

这个简短列表的每一行包含用于识别提交的短哈希和提交信息标题。

`HEAD` 指向当前检出的提交，通常通过当前分支引用该提交。要查看最近一次提交修改了哪些文件和具体文字，可以使用以下命令。

```bash
git show --stat HEAD
git show HEAD -- docs/parts/part-02/chapter-14/section-01.md
```

第一个命令按文件汇总修改，第二个显示指定文件的变更。哈希是寻找特定记录的标识，不是修改数量或质量分数。

在学习文档项目中，`git log` 有助于回答以下问题。

- 这一节是什么时候添加的？
- 哪次提交修改了目录？
- 某张图片与哪篇正文一起添加？
- 部署之前加入了哪些变更？

## 连接正文、代码与图片

文档项目记录学习过程的结果。正文、调查笔记、示例代码、图片和部署配置都会一起变化。例如，把分数阈值从 75 改为 80 时，可以将实现条件的代码和新结果说明放进同一个提交进行比较。

Git 可以保留以下关系。

| 产物 | 记录有助于回答的问题 |
| --- | --- |
| 正文 Markdown | 某段说明何时加入？ |
| 调查笔记 | 依据了哪些资料？ |
| 示例代码 | 生成了哪张输出图片？ |
| 图片文件 | 与哪些代码或章节相关？ |
| 网站导航配置 | 哪篇文档进入了发布目录？ |

可以在 `.gitignore` 中写入模式，排除不需要跟踪的临时缓存或虚拟环境，例如本书的 `.tmp/`、`.venv/` 文件夹。但添加忽略规则不会让已跟踪的文件从历史中消失。另外，代码和图片位于同一提交，并不证明这张图片确实由该代码生成。还需要记录执行命令和输入条件。

## 案例 1. add 后再次修改正文

假设把正文中的分数阈值从 75 改为 80，然后执行 `git add`。之后再改成 85，但只保存文件。此时工作区中是 85，暂存区中是 80。执行普通的 `git commit -m ...`，记录的是 80。

```bash
git diff -- docs/parts/part-02/chapter-14/section-01.md
git diff --cached -- docs/parts/part-02/chapter-14/section-01.md
```

第一个命令比较暂存的 80 与当前文件中的 85。第二个比较上次提交中的 75 与暂存的 80。要记录 85，需要再次对该文件执行 `git add`，然后提交。

如果正文与图表生成代码描述同一个阈值，就需要一起选择。正文写 85 而代码仍使用 75，即使留下历史，说明与运行结果也不一致。提交前用 `git diff --cached` 确认本次记录的内容是否属于同一个修改目的。

## 75 → 80 → 85 记录练习

在已安装 Git 的环境中使用 Bash 执行。在现有项目之外创建尚不存在的 `git-record-practice` 文件夹。下面的姓名和邮箱只作为这个练习仓库的提交作者信息，不是在线登录信息。

```bash
mkdir git-record-practice
cd git-record-practice
git init -b practice
git config user.name "Book Learner"
git config user.email "learner@example.com"
printf 'threshold=75\n' > lesson.txt
git add -- lesson.txt
git commit -m "Record threshold 75"
printf 'threshold=80\n' > lesson.txt
git add -- lesson.txt
printf 'threshold=85\n' > lesson.txt
git status --short
git diff -- lesson.txt
git diff --cached -- lesson.txt
git commit -m "Raise threshold to 80"
git show HEAD:lesson.txt
cat lesson.txt
```

`printf` 写入指定内容，`\n` 表示换行。`>` 将这个练习文件的内容替换为新内容。第一次提交之后暂存 80，再保存 85，状态就是 `MM lesson.txt`。第二次提交后，`git show HEAD:lesson.txt` 显示已记录文件中的 `threshold=80`，而 `cat lesson.txt` 显示工作文件中的 `threshold=85`。

| 时点 | 上次提交 | 暂存区 | 工作区 |
| --- | --- | --- | --- |
| 第一次提交之后 | 75 | 75 | 75 |
| 暂存 80 后保存 85 | 75 | 80 | 85 |
| 第二次提交之后 | 80 | 80 | 85 |

接着暂存 85，用 `git diff --cached` 确认 `80 → 85`，然后记录。

```bash
git add -- lesson.txt
git diff --cached -- lesson.txt
git commit -m "Raise threshold to 85"
git status --short
git log --oneline
```

没有其他修改时，最后的状态输出为空，日志中有三个提交。请根据三个区域中的值，说明保存 85 后省略 `git add` 时为什么不能直接提交 85。

## 检查清单

- 能说明 Git 如何记录文件状态和变更历史吗？
- 能区分保存文件与 Git 提交吗？
- 能区分工作区、暂存区和仓库吗？
- 能将提交描述为一组有意义的变更吗？
- 能说明 `git status`、`git add`、`git commit`、`git log` 的作用吗？
- 能说明为什么一个提交应围绕一个目的吗？
- 能说明 `git add` 之后的新修改为什么不会自动进入提交吗？
- 能区分 `MM` 与 `??`，并说出 `git diff` 和 `git diff --cached` 的比较对象吗？
- 能区分取消暂存与恢复工作文件内容吗？
- 能说明 Git 如何帮助追踪正文、代码、图片和调查笔记之间的关系吗？

## 来源与参考资料

- [Pro Git, About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 版本记录与过去状态的查询。
- [Pro Git, What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 快照与本地操作。
- [GitHub Docs, What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 区分 Git 与在线托管服务。
- [Git project, git-status](https://git-scm.com/docs/git-status){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 文件状态与两列简短输出格式。
- [Git project, git-add](https://git-scm.com/docs/git-add){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 暂存执行时的文件内容。
- [Git project, git-diff](https://git-scm.com/docs/git-diff){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 工作区、索引与提交的比较对象。
- [Git project, git-commit](https://git-scm.com/docs/git-commit){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 将索引状态记录为新提交。
- [Git project, git-restore](https://git-scm.com/docs/git-restore){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 区分取消暂存与恢复工作区。
- [Git project, git-show](https://git-scm.com/docs/git-show){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 查询提交变更及特定版本的文件。
- [Git project, gitignore](https://git-scm.com/docs/gitignore){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 忽略规则及其对已跟踪文件的限制。
- [Git project, git-init](https://git-scm.com/docs/git-init){: target="_blank" rel="noopener noreferrer" } 确认日期: 2026-09-15. 创建练习仓库与初始分支。
