# P2-14.2 Branches, Commits, and Document Reproducibility

> Section ID: `P2-14.2`
> Version: `v2026.07.17`

In P2-14.1, we treated Git as a tool for managing change history. Now, following the writing flow of a document project, we connect branches, commits, and the reproducibility of published documents.

This section is not for learning Git deeply. The goal is to understand why, as a learning document grows, the writing branch and the deployment branch should be separated, and why commit boundaries should be handled carefully. You need this flow now so that, even after Part 3 when model comparisons and experiment records increase, you do not mix up `judgment still under writing` with `explanation ready to publish`.

This section explains the basic distinctions among `branch`, `deployment`, `workflow`, `static deployment`, and `document reproducibility`. The representative explanation of `Git` itself and commit boundaries stays in P2-14.1 and the [Concept Glossary](/AiBook/reference/concept-glossary/). Here, we focus on how to separate those records by lines of work and by public-release standards.

This section focuses on separating workflows and setting deployment criteria. If the previous section asked how changes should be recorded, the question here changes into on which line of work that record should remain, and when it should be moved into public-release standards. So a branch is not an extra feature only for developers. It is an operating standard that separates the manuscript, code, and image interpretation created in the previous chapters into `judgment in progress` and `explanation fit for publication`.

| Handle That Changes Here | What to Check First Now |
| --- | --- |
| git history | Which reason for change should be left as one commit unit? |
| branch workflow | Should this change stay on the writing branch or the deployment branch? |
| deployment criteria | When is it ready to move into publicly visible explanation? |

## Scope of This Section

This section answers the following questions.

- Why is a branch needed?
- Why separate the writing branch from the deployment branch?
- How should commits be divided so document reproducibility improves?
- Why distinguish the document being deployed from the document still being written?
- What should be checked when manuscripts, code, images, and research notes are managed together?

The first question to solve here is this: `Even inside the same repository, why should judgment still being written and explanation ready to publish be left on different work lines and in different commit units?`

## Goals of This Section

- You can explain a branch as "a named history that separates workflows."
- You can explain the role difference between a writing branch and a deployment branch in a document project.
- You can divide commit units from the perspective of document reproducibility.
- You can explain which file relationships should be checked before deployment.
- You can explain what it means when a deployment branch update is reflected in a static deployment flow such as GitHub Pages.

## First Standard to Hold

The first standard to hold in this section is separating `judgment still under writing` from `explanation fit for publication`.

| What You Are Looking at Now | First Question to Ask |
| --- | --- |
| branch | Is this change part of the writing line or the deployment line? |
| commit | Can it be grouped under one reason for change? |
| deployment | Has it passed the checks required for a public document? |
| document reproducibility | Do the manuscript, code, image, and settings all fit together? |

In other words, Git should be read not as simple storage but as an operating tool that decides `what judgment is left, when, and under what publication standard`.

## Three Criteria

| Criterion | Why It Matters | Required Understanding in This Section |
| --- | --- | --- |
| Why is a branch needed? | It keeps in-progress judgment from mixing with public standards. | Understand that it is needed to separate writing work from published work. |
| How are the writing branch and deployment branch different? | It gives you an actual operating standard for workflow separation. | Understand that one handles writing and checking, while the other handles applying public-release standards. |
| What should be checked before deployment? | It keeps you from missing the scope of final public checks. | Understand that links, table of contents, build status, and branch direction should be checked together. |

| Term | Meaning to Hold First in This Section |
| --- | --- |
| branch | A named line of history that separates workflows inside the same repository. |
| deployment | The act of updating the static site or document result visible to readers into its actual public state. |
| workflow | An operating method that defines in what order and by what standards writing, checking, and deployment are separated. |
| static deployment | A method that publishes already generated document files as a site. |
| document reproducibility | The property that lets the same document result be created again by re-matching manuscript, code, image, and settings. |

The flow after this section is also simple.

- Right after this, Chapter 15 connects document-project automation and deployment flow to more practical operating scenes.
- Once experiment records and comparison tables grow after Part 3, the standards for branches, commits, and reproducibility established here are needed again as they are.

## A Branch Separates Workflows

The official Git book explains a branch as a lightweight pointer to a commit. Rather than memorizing all of that internal description, it is more important to understand a branch as `a named history used to separate workflows inside the same project`.

In a document project, you need branches in situations such as the following.

- You need to distinguish a manuscript still being written from a manuscript already being deployed.
- Experimental changes to the table of contents should not be reflected immediately in the published version.
- While images, code, and document structure are changing together, intermediate states should not be exposed publicly.
- If a deployment failure occurs, you need to trace which change caused it.

A branch is not merely a convenience feature for developers. It is a device that protects the stability of the document that readers actually see.

## In a Document Project, You Can Separate the Writing Branch and the Deployment Branch

In a document project, the branch for writing and the branch for deployment standards can be operated separately. Branch names differ by team, but you can separate roles, for example, into a writing branch and a deployment branch.

```mermaid
--8<-- "assets/part-02/chapter-14/branch-review-deploy-flow-en.mmd"
```

The writing branch is one example of a branch used for ordinary writing and editing. You can understand that work such as adding manuscript text, writing example code, editing charts, and organizing research notes happens on this kind of writing branch.

The deployment branch is one example of a branch that reflects public-release standards. In static-site deployment, reflecting changes into this branch may itself lead straight to deployment. Therefore, moving work into the deployment branch should be read not as simple saving but as an act of updating the public document.

This distinction is needed so that, in Part 3, intermediate judgments such as trying another baseline, redoing preprocessing, or refining the explanation of evaluation tables do not harden immediately into public standards. In short, the core of branch operation is separating `comparison still under writing` from `explanation ready for publication`.

## A Commit Should Be a Unit of Publishable Explanation

In a document project, a good commit is closer to "one unit of explanation was completed" than to "some files changed."

For example, when writing P2-13.3, the following files may change together.

| File Type | Example | Why They Should Be Seen Together |
| --- | --- | --- |
| manuscript | `section-03.md` | the main text read by readers |
| image-generation code | `p2_13_3_compare_and_save.py` | the source that can recreate the output image |
| image | `subplot-loss-accuracy.png` | the result inserted into the text |
| research note | `section-evidence-analysis.md` | the grounds and scope judgment behind the explanation |
| site navigation setting | navigation config file | the path exposed in the published document |

If these files are connected, grouping them in one commit is natural. By contrast, if CSS layout was also changed at the same time, it is easier to read the history later if that change is separated into another commit.

## Document Reproducibility Is Broader Than Code Reproducibility

In software, reproducibility is often explained as the ability to obtain the same result again with the same code and environment. In this book, we take document reproducibility a little more broadly.

Document reproducibility should be able to answer the following questions.

- On what grounds was this explanation written?
- By what code was the chart in the main text created?
- What package versions does the example code assume?
- At what point did it enter the deployment table of contents?
- If an error is found later, in which commit should it be fixed?

So document reproducibility is not a problem of the manuscript alone. The manuscript, code, image, research note, and deployment setting must all fit together. This standard also connects directly to experiment reproducibility in Part 3, because when you change the baseline, change the features, or reread an evaluation metric, it must stay clear `which version of the code and explanation is being compared`.

## Check the Connection Relationships Before Deployment

Before deployment, check at least the following connections.

| Item to Check | Checking Question |
| --- | --- |
| Markdown main text | Do the images and internal links point to actual files? |
| site table-of-contents settings | Is the new document connected into nav? |
| example code | Are the code shown in the main text and the generation script consistent with each other? |
| image | Is there any cropping, overlap, or misunderstanding risk? |
| research note | Are the claims in the main text actually connected to the sources? |
| build | Does `mkdocs build` pass? |

If you do not check these, then after reflecting to the deployment branch, the public page may have broken links, missing images, or explanations and examples that no longer match.

If you rewrite this into a shorter checklist:

| Pre-Deployment Check | Why It Is Needed |
| --- | --- |
| main text and links | to make sure the path the reader will actually follow is correct |
| images and code | to make sure the explanation and result do not diverge |
| nav and files | to make sure the document is actually exposed in the public document set |
| build | to make sure the whole site does not break |
| current branch | to avoid deploying in-progress changes by mistake |

## Reflecting to the Deployment Branch Requires a Separate Judgment

In a document project, it is safer not to reflect ordinary in-progress writing directly into the deployment branch, because reflecting to the deployment branch may lead directly to updating the public document.

So you can have an operating standard that moves work into the deployment branch only when the judgment "this change should now be reflected by public-document standards" is clear.

By contrast, in-progress manuscript edits and mid-experiment notes are safer when kept by default on the writing branch.

## Case Study

### Case 1. Problems That Appear If a Manuscript Still Under Check Reaches the Deployment Page

Suppose a writer is organizing a new chapter on the writing branch and is editing the main text, images, and site table-of-contents settings together. The build has not yet been fully checked, and even the internal links are still under review.

If this state is reflected immediately into the deployment branch, the public deployment page may expose that intermediate state as it is. The document may appear in the table of contents while its link is broken. The image file may already have been replaced while the explanation paragraph still stays at an earlier version. In other words, an in-progress draft becomes a public document as-is.

That is why separating the writing branch from the deployment branch is not just a habit. It is a device for protecting publication stability. On the writing branch, the manuscript and experiments proceed. Before moving to the deployment branch, the build, links, images, table of contents, and source connections should all be checked one more time.

This case shows why document reproducibility touches both commit boundaries and branch operation. A deployed book is not correct merely because the manuscript is correct. The code, assets, and settings around that manuscript must also fit together before the same result can be shown again.

This section is not about memorizing more Git commands. It is about deciding by what standards the calculations and interpretations built in the previous sections should be left behind.

| What the Previous Chapters Built | What This Section Decides | What It Still Does Not Do Here |
| --- | --- | --- |
| array calculation, table inspection, graph interpretation | decide which changes belong in one commit unit and on which branch they should remain | complex merge strategies, conflict resolution, advanced collaboration workflows |

## Short Return Table

| If You Get Stuck Here | Return First To |
| --- | --- |
| If it becomes blurry why Git is needed | `P2-14.1` |
| If the connection between reproducibility and dependencies becomes blurry | `P2-7.5`, `P2-10.3` |
| If it becomes blurry why notebooks, graphs, and manuscript records move together | Chapter 10, Chapter 13 |

## Checklist

- Can you explain a branch as a named history that separates workflows?
- Can you explain the role difference between the writing branch and the deployment branch?
- Can you explain that a commit should be a meaningful bundle of change rather than just a bundle of files?
- Can you choose which files should go into one commit by the purpose of the change?
- Can you explain that document reproducibility is not only about the manuscript, but requires code, images, research notes, and deployment navigation to fit together?
- Can you explain that reflecting into the deployment branch may lead to public deployment and therefore requires a separate judgment?
- When you need to manage in-progress changes separately from publishable changes, can you recall the perspective of branches and commit units first?
- Can you explain why site navigation settings, images, research notes, and the build should all be checked before deployment?

## Sources and References

- Scott Chacon and Ben Straub, `Pro Git 2nd Edition: Branches in a Nutshell`, Git documentation, checked on 2026-06-25. [https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell){: target="_blank" rel="noopener noreferrer" }
- Git project, `git-branch Documentation`, checked on 2026-06-25. [https://git-scm.com/docs/git-branch](https://git-scm.com/docs/git-branch){: target="_blank" rel="noopener noreferrer" }
- GitHub Docs, `What is GitHub Pages?`, checked on 2026-06-25. [https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages){: target="_blank" rel="noopener noreferrer" }
