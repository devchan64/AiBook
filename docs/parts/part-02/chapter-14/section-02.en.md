# P2-14.2 Branches, Commits, and Document Reproducibility

> Section ID: `P2-14.2`
> Version: `v2026.09.15`

## Branches and Commits

The official Git book describes a branch as a lightweight pointer to a commit. Two branches starting at the same commit can accumulate different commits and continue along separate lines of history.

Branches help with situations such as these in a document project.

- Distinguishing work in progress from the published manuscript.
- Keeping experimental navigation changes out of the published version.
- Keeping intermediate states off the published site while images, code, and document structure change together.
- Tracing which change caused a deployment failure.

A branch name alone does not determine whether its contents are public. Deployment configuration determines which branch’s changes reach the site.

## A Branch Points to a Commit

Suppose both `main` and `dev` point to commit A. Creating commit B on `dev` moves `dev` to B, while `main` stays at A. The branches have not copied the entire project into separate folders. They share history through A but now point to different commits.

```mermaid
--8<-- "assets/part-02/chapter-14/branch-commit-pointers-en.mmd"
```

The solid arrow shows that B was created after A; dotted arrows show what the branches and `HEAD` refer to. A and B are explanatory labels, not hashes to use in Git commands.

Inspect the current branch and commit connections with these commands.

```bash
git branch --show-current
git log --oneline --graph --decorate --all -5
```

The first prints the current branch name. The second shows the connections and branch names for the five most recent commits. `--all` queries history reachable from multiple references; it does not download the remote server’s latest state.

After creating all three commits in the previous section’s `git-record-practice` repository, create a separate working branch.

```bash
git status --short
git switch -c revise-chart
git branch --show-current
git switch practice
```

Starting with a clean working tree, this creates and switches to `revise-chart` at the current commit, then returns to `practice`. Without any new commit, both branches point to the same commit. In contrast, `git branch revise-chart` creates the branch without switching to it.

Switching branches updates the working tree and staging area to the target branch’s file state. Uncommitted changes may follow you when compatible; Git refuses a switch that would overwrite them. Switching branches therefore does not automatically store pending edits in a separate compartment.

## Writing and Deployment Branches

This book uses `dev` for writing and editing, and `main` as the deployment source. These are repository conventions, not functions that Git assigns to those names. Other projects may use one branch or different names.

```mermaid
--8<-- "assets/part-02/chapter-14/branch-review-deploy-flow-en.mmd"
```

The writing branch records changes to text, example code, and charts. The deployment branch can be maintained to point to the state selected for publication.

A deployment branch is one way to identify the publication source. Updating it can trigger deployment in a static-site setup. Moving changes into that branch can therefore lead to an update of the public document.

## Commit, Push, and Deploy

A remote repository is a Git repository at another location. `origin` is a conventional alias for its address, not the name of the GitHub service itself.

| Action | What Changes | What Is Not Yet Guaranteed |
| --- | --- | --- |
| Commit locally | Local history and the current branch | Remote update |
| Push to a remote | The remote branch and required Git objects | Successful site deployment |
| Run deployment | The process of building and publishing the site | Correct numbers and explanations |

With a remote address configured and write permission available, this command uploads local `dev` to `dev` at `origin`. The practice repository above has no remote configured, so it is not ready to run this command as written.

```bash
git push origin dev
```

A normal push can be rejected if the remote has commits absent from the local history. Inspect the remote history and integrate the changes before pushing again. Merely switching to local `main` does not incorporate changes from `dev`. Combining changes from the two histories is called merging; edits to the same area may require a person to resolve a conflict.

## Grouping Related Files

Commits can record work in progress. When choosing a commit to publish, check that the manuscript and its linked assets agree.

For example, writing P2-13.3 may involve these files.

| File Type | Example | Why to Check Them Together |
| --- | --- | --- |
| Manuscript | `section-03.md` | Text the reader sees |
| Image-generation code | `p2_13_3_compare_and_save.py` | Source for regenerating the images |
| Images | `subplot-loss-accuracy-en.svg` and language variants | Results inserted into the manuscript |
| Source records | References in the text and necessary evidence notes | Support for claims and scope decisions |
| Site navigation settings | Navigation configuration file | Paths exposed in the published document |

When these files are connected, grouping them in one commit is natural. An unrelated CSS layout change made at the same time is easier to trace in a separate commit.

## Document Reproducibility

In software, reproducibility often means obtaining the same result again from the same code and environment. This book uses document reproducibility somewhat more broadly.

Document reproducibility should let us answer these questions.

- What evidence supports this explanation?
- Which code produced the chart in the manuscript?
- Which package versions does the example code assume?
- When did the section enter the published navigation?
- Which commit introduced an error, and which corrective commit fixed it?

Reproducibility therefore involves more than the manuscript. Text, code, images, research notes, and deployment settings must agree. Using text and code from the same commit, together with the required data, package versions, and settings, helps trace the conditions needed to reproduce an earlier document result.

A commit fixes the recorded files, but it does not automatically preserve virtual environments, installed fonts, or external data files. The same plot code can produce different text widths and layouts with different Matplotlib or font versions. Record seeds when randomness is involved, while recognizing that one seed does not guarantee identical files across all environments.

| Target to Reproduce | Conditions to Record Together | Result to Compare |
| --- | --- | --- |
| Calculated values | Code, input data, package versions, settings | Values, array shapes, tolerance |
| Plot appearance | Calculation conditions, fonts, axis ranges, size | Curves, labels, legend, clipping |
| File bytes | Fixed renderer versions and metadata | File hash |

The P2-13.3 script can generate charts in a separate folder without overwriting manuscript assets. Run it from the repository root in a Python environment with Matplotlib, NumPy, and the default font `Noto Sans CJK JP` installed. Choosing another font with `--font-family` can change the appearance.

[Chart-generation code](/AiBook/assets/part-02/chapter-13/p2_13_3_compare_and_save.py)

```bash
python docs/assets/part-02/chapter-13/p2_13_3_compare_and_save.py --language all --output-dir .tmp/p2-14-reproduce
```

This creates six SVG files across the three languages. When comparing `subplot-loss-accuracy-en.svg` with the manuscript image, check the final accuracy, axis ranges, and legend as well as the file’s existence. In the same environment, file hashes can also be compared. If they differ, first distinguish a numerical change from a formatting change.

## Checking Connections Before Publication

Before deployment, check at least these relationships.

| Target | Question |
| --- | --- |
| Markdown text | Do images and internal links point to existing files? |
| Site navigation | Is the new document connected to nav? |
| Example code | Does the manuscript code agree with the generation script? |
| Images | Is there clipping, overlap, or a misleading presentation? |
| Source records | Do the sources support the claims? |
| Build | Does `mkdocs build` pass? |

Otherwise, publishing the deployment branch may expose broken links, missing images, or disagreements between explanations and examples.

## Case 1. The Text Says 0.86 but the Chart Shows 0.88

Suppose the published document contains a chart whose final accuracy is 0.88. On the writing branch, you change the final accuracy to 0.86 and update the text to say “accuracy remains at 0.86 for the last three epochs.” If you edit the generation code without regenerating the image, the text and chart describe different results.

| State | Manuscript | Generation Code | Image |
| --- | --- | --- | --- |
| Previous published version | Final accuracy 0.88 | Final value 0.88 | Final point 0.88 |
| Work in progress | Final accuracy 0.86 | Final value 0.86 | Final point 0.88 |
| Checked version | Final accuracy 0.86 | Final value 0.86 | Final point 0.86 |

Intermediate commits on the writing branch preserve the editing process. Before publication, run the generation code and check that the text references the updated image. A successful site build does not automatically verify numerical consistency.

If deployment is triggered by a push to a specific branch, integrating the checked state into that branch and uploading it starts the deployment job. A local commit alone does not change the public site. Check the job’s success and the actual page to determine what is published.

## Selecting the Modified Files

Suppose the manuscript and code now use a final accuracy of 0.86, the chart has not yet been regenerated, and a separate edit changes a CSS color. Choose what belongs in a “correct accuracy explanation” commit.

1. Decide whether the existing chart still agrees with the explanation.
2. Regenerate it, then select the manuscript, code, and corresponding image together.
3. Decide whether the CSS change is independent of the accuracy explanation.

Here the chart needs updating, while the independent CSS change belongs in a separate commit. Even after pushing the first commit to `dev`, the public site remains unchanged if deployment is connected only to `main`.

## Checklist

- Can you describe a branch as a named line of history that separates work?
- Can you explain the roles of writing and deployment branches?
- Can you explain why a commit should group changes by purpose?
- Can you select the files for a commit based on that purpose?
- Can you explain why reproducibility depends on agreement among text, code, images, research notes, and navigation?
- Can you explain why updating a deployment branch requires a publication decision?
- Can you explain why an intermediate commit and a publication commit need different checks?
- Can you explain why two branches can point to the same commit immediately after branch creation?
- Can you distinguish commit, push, and deployment, and switching from merging?
- Can you explain why a code commit alone does not guarantee the environment or chart reproduction?
- Can you explain why navigation, images, research notes, and the build need checking before deployment?

## Sources and References

- [Pro Git, Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Relationships among branches, commits, and HEAD.
- [Git project, git-branch](https://git-scm.com/docs/git-branch){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Creating and inspecting branches.
- [Git project, git-switch](https://git-scm.com/docs/git-switch){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Switching branches and protecting uncommitted changes.
- [Git project, git-log](https://git-scm.com/docs/git-log){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Inspecting history with graphs, names, and multiple references.
- [Git project, git-push](https://git-scm.com/docs/git-push){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Updating remote references and reasons for push rejection.
- [Git project, git-merge](https://git-scm.com/docs/git-merge){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Integrating histories and handling conflicts.
- [GitHub Docs, Configuring a publishing source for your GitHub Pages site](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site){: target="_blank" rel="noopener noreferrer" } Checked on: 2026-09-15. Branch-based and Actions-based publishing settings.
