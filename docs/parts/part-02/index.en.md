# Part 2. Rebuilding the Foundations

> Section ID: `P2-index`
> Version: `v2026.07.31`

The first plan for this opening page is to connect `reading formulas`, `running Python`, `arrays and tables`, `graphs`, and `records` as one preparation flow. Python examples keep the reference source intact; when needed, the surrounding explanation separates input, computation, output, and the reason for recording the result.

Part 2 is the section for recovering math, Python, data tools, and document-management instincts before studying machine learning and deep learning again. It does not try to prove mathematics deeply or make you memorize all Python syntax. Instead, it builds the foundation needed to read model training, data splitting, evaluation, overfitting, and generalization in Part 3 and to verify them with small code examples.

Within the same Part, Part 2 also places the detailed explanation of each major concept in one representative Section first whenever possible. Later sections keep only the minimum connection needed for the current context. Concepts that keep returning, such as reading formulas, vectors and matrices, derivatives, probability, optimization, arrays, and tabular data, should first be read in the representative Sections and then rechecked through those representative Sections when they reappear.

The central purpose here is `to become able to read again the language of computation that keeps appearing in AI documents and example code`. Formulas, arrays, tables, graphs, runtime environments, and Git history are not separate topics. They are tools used together to read model computation, inspect datasets, visualize results, and leave learning records.

Keep checking questions such as `What is this formula calculating?`, `What value does this code put in and what result does it check?`, and `Why is this tool needed now?` Math, Python, NumPy, Pandas, and Git connect as one shared preparation set for reading the machine-learning main text in Part 3.

So Part 2 reconnects the foundations.

1. It rereads mathematical notation.
2. It restores intuition for linear algebra, derivatives, probability, statistics, and optimization.
3. It reviews Python runtime environments and syntax.
4. It checks small computations with NumPy, Pandas, and Matplotlib.
5. It manages the history of document and code changes with Git.
6. It sets review criteria before moving into Part 3 on machine learning.

## First Anchors

Before reading Part 2 in full, first hold the following four lines.

| Anchor to hold first | Why it matters | Where to return first if blocked |
| --- | --- | --- |
| What a formula is calculating | To reread means, errors, losses, and gradients as sentences | `P2-1`, `P2-2`, `P2-4`, `P2-5`, `P2-6` |
| What shape an array and a table have | To read `X`, `y`, sample, and feature | `P2-11`, `P2-12` |
| Where code runs | To avoid mixing Colab, a local PC, the terminal, and notebooks | `P2-3.5`, Chapter 7, Chapter 10 |
| Whether you can leave what changed and why | To carry experiment and document reproducibility together | Chapter 13, Chapter 14, `P2-15.2` |

In other words, Part 2 is not a Part where math, Python, and tools are each finished separately. It is a Part that restores the `minimum common language needed to read data and learning flow in Part 3`.

## Why Math Recovery Is Needed

Part 2 is the section that reorganizes math and software tools you may have learned long ago, or only encountered partially, into a language for relearning AI.

When people get blocked while returning to AI, the reason is not always that math itself is hard. The problem is that expressions such as \(x\), \(\sum\), \(\frac{1}{n}\), vector, matrix, derivative, gradient, probability, mean, and loss all appear at once inside code, data, and model explanations.

The key axes that serve as the backbone of this Part are the following.

| Representative axis | Representative place to read first | Why it is needed first |
| --- | --- | --- |
| The role of math in AI computation | `P2-1.1` | To read math as computational language rather than as an exam subject |
| The connection among formula, code, and data | `P2-1.2` | To read documents, code, and results together in later examples |
| Sigma, log, and exponential notation | `P2-2.1`, `P2-2.2`, `P2-2.4` | To read compressed notation and the language of probability scores |
| Vectors, matrices, dot product, and distance | `P2-3.1`, `P2-3.4`, `P2-11.1` | To read data shape and vector-comparison standards |
| Derivatives, the chain rule, probability, and optimization | `P2-4.1`, `P2-4.6`, `P2-5.1`, `P2-6.1` | To read loss, gradient, backpropagation, uncertainty, and learning direction |

Python, NumPy, Pandas, Matplotlib, and Git also scatter if learned separately. But in machine-learning context, they connect as one flow: execute a small computation in Python, handle vectors and matrices with NumPy, read tabular data with Pandas, draw data and learning flow with Matplotlib, and leave the change history of documents, code, and experiment records with Git.

Part 2 restores that connection. The goal is not expert-level mathematical proof or software mastery. The goal is to let you follow `what this computation is doing` while reading the machine-learning explanations in Part 3.

### Current Reading Principles

Part 2 should be read with the following principles.

| Principle | Meaning |
| --- | --- |
| Look at role before tool | First fix the roles: NumPy for array computation, Pandas for tabular data, Matplotlib for visualization, and Git for change-history management. |
| If blocked, detour briefly through supplemental learning | Topics beyond the current scope, such as OS-specific installation, terminals, classes, or traditional data structures, should be recovered only as much as needed in supplemental learning. |
| Keep picturing the scene that returns in Part 3 | Keep checking that this is preparation for reading expressions such as `X`, `y`, sample, feature, loss, and metric. |

The more practical question for reading all of Part 2 can be compressed as follows.

| Question to keep asking while reading | Why this question is needed |
| --- | --- |
| To which scene in Part 3 does what I am reading now connect? | So the explanation does not settle only inside the current Section |
| If I get blocked here, where can I return briefly? | So I can recover without rereading all of Part 2 from the beginning |
| What is the minimum sentence I should keep from here? | So I can choose the real standard that should remain after a long explanation |

## Mathematical Anchors for Reading AI Computation

After reading Part 2, the goal is to have understanding at about the following level.

- You can reread variable, function, expression, sigma, and limit as reading language for AI documents.
- You can explain why expressions such as log, exp, and log loss keep appearing repeatedly.
- You can explain scalar, vector, matrix, vector space, and matrix multiplication from the viewpoint of data and model computation.
- You can explain dot product, norm, distance, and similarity as standards for comparing vectors.
- You can understand derivative, gradient, loss function, and gradient descent as `direction and standard for adjusting values toward something better`.
- You can explain composite function and the chain rule as the minimum background before backpropagation.
- You can use probability, distribution, mean, variance, sample, estimation, and error as the basic language of data judgment.
- You can distinguish Python runtime environments, terminal, virtual environment, dependencies, and notebook execution flow.
- You can explain the introductory role of Python values, variables, lists, dictionaries, loops, functions, and classes.
- You can connect NumPy arrays, shape, axis, indexing, slicing, broadcasting, and vectorization to model computation.
- You can read a Pandas DataFrame through row, column, and index, and hold the intuition needed for dataset preparation.
- You can visually inspect formulas, distributions, relationships, and loss curves through Matplotlib.
- You can understand Git commits and branches as tools for managing the reproducibility of learning documents.

## Scope of the Math Recovery and Questions Left Open

Part 2 is a foundation-recovery Part for AI learning. So within the main text, it explains the following.

- The minimum standard for rereading formulas and computational language
- Introductory intuition for linear algebra, derivatives, probability, statistics, and optimization
- Python runtime environments and basic syntax
- The learning role of NumPy, Pandas, Matplotlib, and Git

By contrast, it does not cover the following in full depth.

- Rigorous development of mathematical theorems and proofs
- Advanced Python syntax and large-scale software design
- The full system of data engineering and collaboration automation tools
- A long combinatorics-style explanation of the growth of search-space cases

This omission is not avoidance of explanation. It is scope control. The responsibility of Part 2 is `to make the computational language readable again`, while advanced tool usage and higher mathematical proof are left to later study or separate references. The sense that choice counts grow rapidly in search space is first fixed through the table and examples in P1-7.1, and it is not expanded here again into a separate combinatorics section.

## Reading Standard for Introductory Readers

Part 2 can look like different subjects at once because math, Python, data tools, and Git all appear together. At first, rather than trying to finish every syntax rule and formula at once, read using the following three questions.

| Question to hold first | Why this question is needed | What is enough to capture in this Part |
| --- | --- | --- |
| What is this formula trying to calculate? | Even if the symbols are unfamiliar, you can move to the next Section if you first hold the purpose of the computation. | Read what is being reduced or compared, such as mean, sum, gradient, and error. |
| What values does this code take in, and what result does it show? | Before Python syntax itself, the input, computation, and output flow must be visible to follow the practice. | Read what output comes from a small list, array, or table. |
| Why is this tool needed right now? | If only the tool names are memorized, they scatter quickly. | First hold the roles: NumPy for array computation, Pandas for tabular data, Matplotlib for visualization, Git for change history. |

1. Math is a language for writing computation briefly.
2. Python is the tool that executes that computation.
3. NumPy, Pandas, and Matplotlib help you read and inspect data.
4. Git leaves what you changed.

Even if many tool names appear, the following five are the main current to hold first.

| Main current to hold first | Why it is needed now | Where it is reused immediately later |
| --- | --- | --- |
| Formulas, means, errors, and gradients | Needed to read the explanations of loss and evaluation in Part 3 | Part 3 |
| The Python flow of input, computation, and output | Needed to follow what the example code is checking | Part 3, Part 4, Part 5 |
| NumPy arrays, `shape`, and `axis` | Needed to read data direction and model input shape | Part 3, Part 4, Part 5, Part 6 |
| Pandas rows, columns, and `DataFrame` | Needed to distinguish feature and label inside a table | Part 3 |
| Git commits and records of change reasons | Needed to leave experiment comparison and document history together | Part 3, Part 4, Part 7 |

## What It Explains

Part 2 consists of 15 chapters.

It first rereads math as a language of computation. It restores variables, functions, expressions, sigma, and limit, and reconnects log and exponentials as the language of probability scores that returns in later Parts. It builds the perspective of rechecking formulas again inside code and data.

Next it covers the core math needed to read model computation. In linear algebra, it goes through scalar, vector, matrix, vector space, and matrix multiplication, and it also fixes `how should vectors be compared` through dot product, norm, distance, and similarity. In derivatives, it reads rate of change, slope, gradient, and why derivatives are needed in learning, then strengthens the minimum link before backpropagation through composite functions and the chain rule. In probability and statistics, it organizes how uncertainty is expressed as numbers, and how bundles of data are read through mean, variance, distribution, sample, estimation, and error. Here, instead of fully comparing frequentism and Bayesianism, it restores only the minimum distinction between `long-run frequency` and `degree of belief`, and leaves Bayes' rule at the level of intuition for belief updating. In optimization, it approaches the problem not as directly writing the best answer, but as searching for a better value.

In the middle, it deals with runtime environments and Python basics. It distinguishes Colab and a local PC, terminal and shell, Python interpreter and script, virtual environment and package, and dependency and reproducibility. Then it restores the basic intuition of Python values, variables, types, lists, dictionaries, loops, functions, and classes.

In the later half, it covers data structures and data tools. It builds intuition for arrays, tables, trees, and graphs, and then looks at how to leave code and explanation together through Jupyter and Colab notebooks. It uses NumPy to compute vectors and matrices, Pandas to handle tabular data, and Matplotlib to inspect the shape of numbers.

Finally, it covers Git and document management. In projects where documents, example code, images, and experiment records change together, change history and reproducibility matter. At the end of Part 2, it organizes a small procedure for moving formulas into code and checks the intuition needed before moving into Part 3.

## Why It Is Needed

When studying machine learning, many explanations appear in the following form.

1. There is input data \(X\) and label \(y\).
2. The model produces prediction \(\hat{y}\).
3. The loss function turns the difference between prediction and actual value into a number.
4. Learning adjusts parameters in the direction that reduces that loss.
5. Evaluation checks the result on unseen data.

To read that explanation, several foundations are needed at once. You need to be able to see \(X\) and \(y\) as arrays and tables, read loss through mean and summation, inspect learning flow through graphs, and also trace in what environment the example code runs and in what commit the result image and manuscript changed together.

Part 2 does not dig those foundations too deeply. Instead, it prepares the minimum language and hands-on intuition so that you do not get blocked while reading models and data flow in Part 3.

## Quick Return Table Before Moving into Part 3

| Expression that blocks you in Part 3 | First place to return in Part 2 |
| --- | --- |
| `X`, `y`, feature, label | `P2-12.3`, `P2-15.2` |
| `shape`, `axis`, row, column | `P2-11.2`, `P2-15.2` |
| mean, error, loss | Chapter 5, Chapter 6, `P2-15.2` |
| `fit`, `predict`, train/test | `P2-12.3`, `P2-15.2` |
| Colab, terminal, notebook, runtime environment | `P2-3.5`, Chapter 7, Chapter 10 |

## Questions Handed to the Next Part

Because Part 2 focuses on recovering the foundations, it intentionally leaves the following questions to Part 3 and beyond.

- How do loss and optimization connect in actual model training?
- Why are train, validation, and test splits needed?
- Why do neural networks and deep-learning structures require larger computational resources?

These questions are recovered through the main explanations in Part 3, Part 4, and Part 5.

## Understanding That Connects Formulas to Code

After this Part, instead of memorizing math and software tools separately, you can see them as one learning flow.

1. Formulas write down computational intent.
2. Python executes small computations.
3. NumPy reuses vector and matrix computation.
4. Pandas lets datasets be read as tables.
5. Matplotlib lets you inspect the shape of numbers.
6. Git leaves the change history of manuscript, code, and results.

Once that understanding appears, expressions such as `X`, `y`, `fit`, `predict`, loss, metric, train, validation, and test in the machine-learning text of Part 3 no longer feel like completely unfamiliar language. Part 2 is not where every foundation is finished. It is where the minimum shared base for moving into machine learning is built.

## Completion Criteria

- You can explain how variables, functions, sigma, mean, and error in formulas connect to actual computational procedures.
- You can say where vectors and matrices are used in data and model computation.
- You can explain derivative, gradient, loss function, and gradient descent at an introductory level.
- You can distinguish probability, distribution, mean, variance, sample, and estimation as the language of data judgment.
- You can explain where Python code runs and what the difference is between Colab and a local PC.
- You can explain the basic role of Python lists, dictionaries, loops, functions, and classes.
- You can verify NumPy array shape, axis, indexing, slicing, and broadcasting with small examples.
- You can read a Pandas DataFrame through rows and columns and explain the need for learning-oriented dataset preparation.
- You can inspect function shape, scatter plots, histograms, and loss curves through Matplotlib.
- You can explain Git commits and branches from the viewpoint of managing the history of changes to documents, code, images, and experiment records.
- Before moving into Part 3, you can say the basic meaning of `X`, `y`, sample, feature, fit, and predict.

## Checklist

- Can you explain that formulas, arrays, tables, graphs, and Git connect as the same learning flow in Part 3?
- Can you choose which chapter to return to when you see one blocked expression?
- Can you explain `X`, `y`, shape, mean, error, and runtime environment in one sentence each?

## Sources and References

This document is an original overview that organizes the purpose and learning path of Part 2. It does not directly quote external sources.
