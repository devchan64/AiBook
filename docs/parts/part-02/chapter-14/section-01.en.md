# P2-14.1 Git as a Tool for Managing Change History

> Section ID: `P2-14.1`
> Version: `v2026.09.15`

## File Saving and Change Records

Saving a file preserves its current state. It does not automatically explain why the previous state changed or which files changed together.

For example, suppose you have done the following work.

- Written a section of the manuscript.
- Added a script that generates plots.
- Created two output images.
- Modified the site navigation settings.

These four tasks may seem separate, but they can form one meaningful change: “update a section’s plot explanation together with its linked assets.”

Git records this bundle as a commit.

A commit points to a snapshot of the tracked file state at that moment. Unchanged files also belong to that state, and comparing it with the previous commit reveals which lines changed. The commit message describes the purpose, but Git does not automatically judge the meaning of the files or the reasons for editing them.

## Previous States and Reasons for Changes

Version control lets you retrieve previous file states and compare changes. The author must record the reasons in places such as commit messages. Reading the history helps answer these questions.

- Which files changed?
- Why did they change?
- Which files changed together?
- When was a particular explanation introduced?
- After which change did a problem appear?

The official Git book describes version control as a system that records file changes over time so that particular versions can be recalled later. Documents and example code can be examined this way as well.

## Working Tree, Staging Area, and Repository

The working tree contains the files being edited. The staging area holds the file contents selected for the next commit. Committing records the staged state in the repository’s history.

```mermaid
--8<-- "assets/part-02/chapter-14/git-three-areas-flow-en.mmd"
```

The distinction between saving and committing matters in this flow.

Saving writes the current file contents from the editor to disk. Committing records a meaningful selection of changes in repository history.

This work can happen locally without an internet connection. Git is the version-control program; GitHub is a service for hosting Git repositories online and collaborating on them. Creating a local commit does not automatically upload it to GitHub.

## Checking State: git status

The first command to check when working with Git is usually `git status`.

The `docs/...` paths below assume execution from this book’s repository root. Git cannot report repository status in a folder that is not yet a repository. The “Recording 75 → 80 → 85” exercise below creates a new one.

```bash
git status
```

This command answers the following questions.

- Which files were modified?
- Are there any new files?
- Which files have been selected for this commit?
- What is the current branch?

The two positions before a file name distinguish its staging state.

```bash
git status --short
```

For ordinary edits without conflicts, the first position describes differences between the previous commit and the staging area. The second describes differences between the staging area and the working tree. In the table, `·` makes a blank visible; actual output uses a space.

| Marker | File State | What a Normal Commit Includes |
| --- | --- | --- |
| `??` | New, untracked file | Nothing |
| `·M` | Tracked file modified but not staged | The new edit is excluded |
| `M·` | Modification staged | The staged modification |
| `MM` | File edited again after staging | Only the modification staged earlier |
| `A·` | New file staged | The staged contents of the new file |

An empty `git diff` does not rule out `??` files. Ordinary `git diff` does not display the contents of untracked files, so also check `status`.

## Selecting Changes: git add

`git add` does not immediately save a file permanently in history. It places the changes selected for this commit in the staging area.

```bash
git add docs/parts/part-02/chapter-14/section-01.md
```

`git add` stages the file contents at the moment it runs. Further edits to that file are not staged automatically. Even if several files changed, they do not all need to enter one commit. Changes with different purposes are easier to read later if committed separately.

For example, these two tasks should generally be recorded separately.

| Change | Reason to Separate the Commits |
| --- | --- |
| Writing Chapter 14 | Adding book content |
| Modifying the CSS layout | Improving page presentation |

Combining them makes it harder to trace why the CSS changed.

To remove a mistakenly selected file from the next commit, unstage it as follows in a repository that already has a commit.

```bash
git restore --staged -- docs/parts/part-02/chapter-14/section-01.md
```

`--staged` changes the selection for the next commit while preserving edits in the working tree. Running `git restore` without this option can restore the file contents themselves, so the commands must not be treated as equivalent.

## Recording History: git commit

`git commit` records staged changes in repository history.

```bash
git commit -m "docs(part2): add git version control introduction"
```

A commit message gives future readers a title explaining what changed.

A useful message usually meets these conditions.

- It identifies what changed.
- It avoids overly broad wording.
- It conveys the purpose rather than just the file name.
- It remains meaningful when read later in `git log`.

The following is a poor example.

```bash
git commit -m "update"
```

It does not explain what was updated.

## Reading History: git log

As commits accumulate, inspect the history with `git log`.

```bash
git log --oneline
```

Each line of this compact list contains a short hash identifying a commit and its message title.

`HEAD` refers to the currently checked-out commit, usually through the current branch. These commands show the files and actual text changed in the latest commit.

```bash
git show --stat HEAD
git show HEAD -- docs/parts/part-02/chapter-14/section-01.md
```

The first command summarizes changes by file; the second shows changes to the specified file. A hash identifies a record. It is not a measure of change size or quality.

In a learning-document project, `git log` helps answer these questions.

- When was this section added?
- Which commit changed the navigation?
- Which manuscript accompanied the addition of a particular image?
- Which changes entered before deployment?

## Connecting Manuscripts, Code, and Images

A document project records the results of learning. Manuscripts, research notes, example code, images, and deployment settings change together. If a score threshold changes from 75 to 80, for example, the code implementing the condition and the explanation of its new result can be compared in the same commit.

Git can preserve these relationships.

| Output | Question the Record Can Help Answer |
| --- | --- |
| Manuscript Markdown | When was an explanation added? |
| Research notes | Which sources supported it? |
| Example code | Which output image did it generate? |
| Image file | Which code or section is it associated with? |
| Site navigation settings | Which document entered the published navigation? |

Patterns in `.gitignore` can exclude files such as temporary caches and virtual environments from tracking. This book’s `.tmp/` and `.venv/` folders are examples. Adding a pattern does not remove files already tracked from history. Also, putting code and an image in the same commit does not verify that the code generated that image. Record the execution command and input conditions as well.

## Case 1. Editing the Manuscript After add

Suppose you change a score threshold from 75 to 80 and run `git add`. You then change it to 85 and only save the file. The working tree now contains 85, while the staging area contains 80. A normal `git commit -m ...` records 80.

```bash
git diff -- docs/parts/part-02/chapter-14/section-01.md
git diff --cached -- docs/parts/part-02/chapter-14/section-01.md
```

The first command compares the staged 80 with the current file’s 85. The second compares the previous commit’s 75 with the staged 80. To record 85, run `git add` for the file again before committing.

If the manuscript and plot-generation code describe the same threshold, select them together. A manuscript using 85 and code using 75 leave a history but disagree about the result. Before committing, use `git diff --cached` to check that the selected contents serve the same purpose.

## Recording 75 → 80 → 85

Run this in Bash with Git installed. Create a previously nonexistent `git-record-practice` folder outside existing projects. The name and email below identify the commit author only in this practice repository; they are not online login credentials.

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

`printf` writes the specified text, and `\n` represents a newline. `>` replaces the practice file’s contents. After the first commit, staging 80 and saving 85 produces `MM lesson.txt`. After the second commit, `git show HEAD:lesson.txt` displays the recorded file’s `threshold=80`, while `cat lesson.txt` displays the working file’s `threshold=85`.

| Moment | Previous Commit | Staging Area | Working Tree |
| --- | --- | --- | --- |
| Just after the first commit | 75 | 75 | 75 |
| After staging 80 and saving 85 | 75 | 80 | 85 |
| Just after the second commit | 80 | 80 | 85 |

Now stage 85, check the `80 → 85` change with `git diff --cached`, and record it.

```bash
git add -- lesson.txt
git diff --cached -- lesson.txt
git commit -m "Raise threshold to 85"
git status --short
git log --oneline
```

With no other changes, the final status output is empty and the log contains three commits. Use the values in the three areas to explain why 85 would not be committed immediately if `git add` had been omitted after saving 85.

## Checklist

- Can you explain how Git records file states and change history?
- Can you distinguish saving a file from making a Git commit?
- Can you distinguish the working tree, staging area, and repository?
- Can you describe a commit as a meaningful bundle of changes?
- Can you explain the roles of `git status`, `git add`, `git commit`, and `git log`?
- Can you explain why a commit should have one purpose?
- Can you explain why edits made after `git add` are not committed automatically?
- Can you distinguish `MM` from `??` and identify the comparisons made by `git diff` and `git diff --cached`?
- Can you distinguish unstaging from restoring working-file contents?
- Can you explain how Git helps track relationships among manuscripts, code, images, and research notes?

## Sources and References

- [Pro Git, About Version Control](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Version records and retrieval of earlier states.
- [Pro Git, What is Git?](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Snapshots and local operations.
- [GitHub Docs, What is GitHub?](https://docs.github.com/en/get-started/start-your-journey/what-is-github){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Distinguishing Git from online hosting.
- [Git project, git-status](https://git-scm.com/docs/git-status){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. File state and the two-column short format.
- [Git project, git-add](https://git-scm.com/docs/git-add){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Staging file contents at execution time.
- [Git project, git-diff](https://git-scm.com/docs/git-diff){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Comparison of working tree, index, and commit.
- [Git project, git-commit](https://git-scm.com/docs/git-commit){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Recording index state in a new commit.
- [Git project, git-restore](https://git-scm.com/docs/git-restore){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Unstaging versus restoring the working tree.
- [Git project, git-show](https://git-scm.com/docs/git-show){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Inspecting commit changes and files at a given revision.
- [Git project, gitignore](https://git-scm.com/docs/gitignore){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Ignore rules and their limits for tracked files.
- [Git project, git-init](https://git-scm.com/docs/git-init){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Creating the practice repository and initial branch.
