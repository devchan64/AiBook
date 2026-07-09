# P2-14.1 Git as a Tool for Managing Change History

> Section ID: `P2-14.1`
> Version: `v2026.07.07`

P2-14.1 moves from reading arrays, tables, and plots to recording what changed and why. The point is not just to save files, but to preserve meaningful change groups for later explanation.

## Scope of This Section

This Section introduces Git, version control, commit, staging area, and repository at an entry level.

## Central Question

Why is tracking change history different from simply saving the latest version of a file?

## Perspective to Keep

- Git records change history with explanations, not just the latest file state.
- `git add` and `git commit` are separated because choosing changes and finalizing a record are different actions.
- `git status`, `git add`, `git commit`, and `git log` form the smallest useful Git reading loop.
- Documentation, code, images, and notes often belong to the same change unit in learning projects.

## Short Check

- Can you explain why a commit is more than a save action?
- Can you explain the difference among working tree, staging area, and repository?
- Can you explain why Git matters even in a document-heavy AI study project?

## Sources and References

- Scott Chacon and Ben Straub, [Pro Git, 2nd Edition](https://git-scm.com/book/en/v2){: target="_blank" rel="noopener noreferrer" }, checked 2026-07-09.
