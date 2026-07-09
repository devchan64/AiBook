# Part 2. Rebuilding the Foundations

> Section ID: `P2-index`
> Version: `v2026.07.09`

Part 2 is the stage where you recover the math, Python, data-tool, and documentation instincts needed before returning to machine learning and deep learning. Here, you do not prove mathematics in depth or memorize all Python syntax. Instead, you build the foundation required to read model training, data splitting, evaluation, overfitting, and generalization in Part 3, and to verify them with small pieces of code.

Within the same Part, Part 2 also tries to place the detailed explanation of each major concept in one representative Section first whenever possible. Later Sections keep only the minimum connection needed for the current context. Concepts you meet repeatedly, such as reading formulas, vectors and matrices, derivatives, probability, optimization, arrays, and tabular data, should first be read in their representative Sections and then rechecked together with the [Concept Glossary](../../reference/concept-glossary.md) when they reappear.

The central purpose here is `to make the computational language that repeatedly appears in AI documents and example code readable again`. Formulas, arrays, tables, graphs, runtime environments, and Git history are not separate topics. They are tools used together to read model computation, inspect datasets, visualize results, and leave learning records.

Keep checking questions such as `What is this formula calculating?`, `What values does this code put in and what result is it checking?`, and `Why is this tool needed right now?` Math, Python, NumPy, Pandas, and Git connect as one shared preparation set for reading the machine-learning main text in Part 3.

So Part 2 reconnects the foundations.

1. It rereads formula notation.
2. It restores intuition for linear algebra, derivatives, probability, statistics, and optimization.
3. It reviews Python runtime environments and syntax.
4. It checks small computations with NumPy, Pandas, and Matplotlib.
5. It manages document and code change history with Git.
6. It sets review criteria before moving into Part 3 on machine learning.

## First Anchors

Before reading Part 2 in full, it is enough to hold the following four lines first.

| First anchor to hold now | Why it matters | Where to return first if blocked |
| --- | --- | --- |
| What a formula is calculating | To reread means, errors, losses, and gradients as sentences | `P2-1`, `P2-2`, `P2-4`, `P2-5`, `P2-6` |
| What shape an array and a table have | To read `X`, `y`, sample, and feature | `P2-11`, `P2-12` |
| Where the code is running | To avoid mixing up Colab, a local PC, the terminal, and notebooks | `P2-3.5`, Chapter 7, Chapter 10 |
| Whether you can leave what changed and why | To carry experiment and document reproducibility together | Chapter 13, Chapter 14, `P2-15.2` |

In other words, Part 2 is not a Part where math, Python, and tools are each finished separately. It is a Part where you restore the `minimum common language needed to read data and learning flows in Part 3`.

## Purpose of This Part

Part 2 is the stage where math and software tools you may have learned long ago, or only encountered partially, are reorganized into a language for relearning AI.

When people get blocked while returning to AI, the reason is not always that math itself is hard. The difficulty is that expressions such as \(x\), \(\sum\), \(\frac{1}{n}\), vector, matrix, derivative, gradient, probability, mean, and loss all appear together inside code, data, and model explanations.

The key axes of this Part are the following.

| Representative axis | Representative starting point | Why it is needed first |
| --- | --- | --- |
| The role of math in AI computation | `P2-1.1` | To read math as computational language rather than as an exam subject |
| Formula-code-data connection | `P2-1.2` | To read documents, code, and outputs together in later examples |
| Sigma, log, and exponential notation | `P2-2.1`, `P2-2.2`, `P2-2.4` | To read compressed notation and the language of probability scores |
| Vectors, matrices, dot products, and distance | `P2-3.1`, `P2-3.4`, `P2-11.1` | To read data shapes and vector comparison standards |
| Derivatives, the chain rule, probability, and optimization | `P2-4.1`, `P2-4.6`, `P2-5.1`, `P2-6.1` | To read loss, gradients, backpropagation, uncertainty, and learning direction |

Python, NumPy, Pandas, Matplotlib, and Git also scatter if learned separately. But in machine-learning context, they connect as one flow: execute a small calculation in Python, handle vectors and matrices in NumPy, read tabular data with Pandas, draw data and learning flow with Matplotlib, and leave the change history of documents, code, and experiment records with Git.

Part 2 restores this connection. The goal is not expert-level mathematical proof or software mastery. The goal is to let you follow `what this calculation is doing` while reading the machine-learning explanations in Part 3.

### Current Reading Principle

Part 2 should be read with the following principles.

| Principle | Meaning |
| --- | --- |
| Look at role before tool | First hold that NumPy is for array computation, Pandas is for tabular data, Matplotlib is for visualization, and Git is for change-history management. |
| If blocked, detour briefly through supplemental learning | Topics that go beyond the current scope, such as OS-specific installation, terminals, classes, or traditional data structures, should be recovered only as much as needed in supplemental learning. |
| Keep picturing the scene that returns in Part 3 | Keep checking that this is preparation for reading expressions such as `X`, `y`, sample, feature, loss, and metric. |

The more practical question for reading all of Part 2 can be compressed as follows.

| Question to keep asking while reading | Why this question is needed |
| --- | --- |
| To which scene in Part 3 does what I am seeing now connect? | So the explanation does not close only inside the current Section |
| If I get blocked in this Section, where can I return briefly? | So I can recover without rereading all of Part 2 from the beginning |
| What is the minimum sentence I should leave in hand here? | So I can choose the real standard to keep from a long explanation |

## Goals of This Part

After reading Part 2, the goal is to have understanding at about the following level.

- You can reread variable, function, expression, sigma, and limit as reading tools for AI documents.
- You can explain why expressions such as log, exp, and log loss keep appearing repeatedly.
- You can explain scalar, vector, matrix, vector space, and matrix multiplication from the viewpoint of data and model computation.
- You can explain dot product, norm, distance, and similarity as standards for comparing vectors.
- You can understand derivative, gradient, loss function, and gradient descent as `direction and standard for adjusting values toward something better`.
- You can explain composite function and the chain rule as the minimum background before backpropagation.
- You can use probability, distribution, mean, variance, sample, estimation, and error as the basic language of data judgment.
- You can distinguish Python runtime environments, terminals, virtual environments, dependencies, and notebook execution flow.
- You can explain the introductory role of Python values, variables, lists, dictionaries, loops, functions, and classes.
- You can connect NumPy arrays, shape, axis, indexing, slicing, broadcasting, and vectorization to model computation.
- You can read a Pandas DataFrame through rows, columns, and index, and hold the intuition needed for dataset preparation.
- You can visually inspect formulas, distributions, relationships, and loss curves through Matplotlib.
- You can understand Git commits and branches as tools for managing the reproducibility of learning documents.

## What This Part Explains and What It Does Not

Part 2 is a foundation-recovery Part for AI learning. So within the main text, it explains the following.

- The minimum standard for rereading formulas and computational language
- Introductory intuition for linear algebra, derivatives, probability, statistics, and optimization
- Python runtime environment and basic syntax
- The learning role of NumPy, Pandas, Matplotlib, and Git

By contrast, it does not cover the following in full depth.

- Rigorous development of mathematical theorems and proofs
- Advanced Python syntax and large-scale software design
- The full system of data engineering and collaboration automation tools
- A long combinatorics-style development of search-space growth

This omission is not an avoidance of explanation. It is scope control. The responsibility of Part 2 is `to make the computational language readable again`, while advanced tool usage and rigorous higher mathematics are left to later learning or separate references. The intuition that the number of cases grows rapidly in search spaces is first captured through the table and examples in P1-7.1, and here it is not expanded again into a separate combinatorics Section.

## Reading Standard for Introductory Readers

Part 2 can look like different subjects at once because math, Python, data tools, and Git all appear together. At first, rather than trying to finish every syntax rule and formula at once, read using the following three questions.

| Question to hold first | Why this question is needed | What is enough to capture in this Part |
| --- | --- | --- |
| What is this formula trying to calculate? | Even if the symbols are unfamiliar, you can move to the next Section if you hold the computational purpose first. | Read what is being reduced or compared, such as mean, sum, gradient, and error. |
| What value does this code take in, and what result does it show? | Before Python syntax itself, the flow of input, calculation, and output has to be visible to follow the practice. | Read what output comes from a small list, array, or table. |
| Why is this tool needed right now? | If only the tool names are memorized, they scatter quickly. | First hold the roles: NumPy for array calculation, Pandas for tabular data, Matplotlib for visualization, Git for change history. |

1. Math is a language for writing computation briefly.
2. Python is the tool that executes that computation.
3. NumPy, Pandas, and Matplotlib help you read and inspect data.
4. Git leaves what you changed.

Even if many tool names appear, you only need to hold the following five as the main current.

| Main current to hold first | Why it is needed now | Where it is reused immediately later |
| --- | --- | --- |
| Formulas, means, errors, and gradients | Needed to read the explanations of loss and evaluation in Part 3 | Part 3 |
| The Python flow of input, calculation, and output | Needed to follow what the example code is checking | Part 3, Part 4, Part 5 |
| NumPy arrays, `shape`, and `axis` | Needed to read data direction and model input shape | Part 3, Part 4, Part 5, Part 6 |
| Pandas rows, columns, and `DataFrame` | Needed to distinguish feature and label inside a table | Part 3 |
| Git commits and the record of change reasons | Needed to leave experiment comparison and document history together | Part 3, Part 4, Part 7 |

## What It Explains

Part 2 consists of 15 Chapters.

First, it rereads math as computational language. It restores variables, functions, expressions, sigma, and limit, and then reconnects log and exponentials as the probability-score language used again in later Parts. It builds the viewpoint of rechecking formulas again inside code and data.

Next, it deals with the core math needed to read model computation. In linear algebra, it covers scalars, vectors, matrices, vector space, and matrix multiplication, and then also holds on to `how should vectors be compared` through dot product, norm, distance, and similarity. In derivatives, it looks at rate of change, slope, gradient, and why derivatives are needed in learning, then strengthens the minimum link before backpropagation through composite functions and the chain rule. In probability and statistics, it organizes how to express uncertainty as numbers and how to read bundles of data through mean, variance, distribution, sample, and error. Here, instead of fully comparing frequentism and Bayesianism, it restores only the minimum distinction between `long-run frequency` and `degree of belief`, and leaves Bayes' rule at the intuition of belief updating. In optimization, it approaches the problem not as directly writing the best answer, but as searching for a better value.

In the middle, it covers runtime environments and Python basics. It distinguishes Colab and a local PC, the terminal and the shell, the Python interpreter and scripts, virtual environments and packages, and dependencies and reproducibility. Then it restores the basic intuition of Python values, variables, types, lists, dictionaries, loops, functions, and classes.

In the later half, it deals with data structures and data tools. It builds intuition for arrays, tables, trees, and graphs, and then looks at how to leave code and explanation together through Jupyter and Colab notebooks. It calculates vectors and matrices with NumPy, handles tabular data with Pandas, and checks the shape of numbers with Matplotlib.

Finally, it covers Git and document management. In projects where documents, example code, images, and experiment records change together, change history and reproducibility matter. At the end of Part 2, it organizes the small procedure of translating formulas into code and checks the intuition needed before moving into Part 3.

## Why It Is Needed

When studying machine learning, many explanations appear in the following form.

1. There is input data \(X\) and label \(y\).
2. The model produces prediction \(\hat{y}\).
3. The loss function turns the difference between prediction and actual value into a number.
4. Learning adjusts parameters in the direction that reduces that loss.
5. Evaluation checks the result on data that was not seen before.

To read this explanation, several foundations are needed at once. You need to be able to see \(X\) and \(y\) as arrays and tables, read loss through mean and summation, inspect learning flow through graphs, and also trace in what environment the example code runs and in what commit the result image and manuscript changed together.

Part 2 does not dig each of these too deeply. Instead, it prepares the minimum language and hands-on intuition so that you do not get blocked when reading models and data flow in Part 3.

## Connection with the Previous Part

If Part 1 set the overall map of AI and the shared terminology, Part 2 is the first stage that turns that terminology into actual computational language.

- The distinction among data, model, learning, and model execution from Part 1 appears again as formulas and code.
- Words from Part 1 such as prompt, embedding, and RAG also ultimately rest on arrays, vectors, tables, and runtime environments.

In other words, Part 2 is not a Part that throws away the map and moves into a new subject. It is a Part that moves the map into actual computational notation and execution tools.

## Connection to Later Parts

After Part 2 ends, the following questions naturally lead into Part 3 on machine learning.

- How should input \(X\) and label \(y\) actually be read?
- How do loss and evaluation metrics change across problems?
- Why are data splitting and generalization important?

So Part 2 is not the Part where tools and foundations are finished. It is the Part where the common floor for reading machine-learning explanations is built.

## Quick Return Table Before Moving into Part 3

| Expression that blocks you in Part 3 | First place to return in Part 2 |
| --- | --- |
| `X`, `y`, feature, label | `P2-12.3`, `P2-15.2` |
| `shape`, `axis`, row, column | `P2-11.2`, `P2-15.2` |
| mean, error, loss | Chapter 5, Chapter 6, `P2-15.2` |
| `fit`, `predict`, train/test | `P2-12.3`, `P2-15.2` |
| Colab, terminal, notebook, runtime environment | `P2-3.5`, Chapter 7, Chapter 10 |

## Questions This Part Does Not Finish

Because Part 2 focuses on recovering the foundations, it intentionally leaves the following questions to Part 3 and beyond.

- How do loss and optimization connect in actual model training?
- Why are train, validation, and test splits needed?
- Why do neural networks and deep-learning structures require larger computational resources?

These questions are recovered as actual main-text explanations in Part 3, Part 4, and Part 5.

## Perspective That Connects to the Next Part

What matters most in the next Part is the `shared structure of reading a problem, splitting data, and setting evaluation standards`.

The formula, array, table, graph, and Git intuition recovered in Part 2 are tied together again in Part 3 as the flow `problem definition -> data split -> learning -> evaluation`.

Before moving into Part 3, check by the standard of `can I try this right now?` as follows.

| Small check to try before Part 3 | Why it matters |
| --- | --- |
| Look at a small table and say which column is feature and which column is label | Because this becomes the starting point of machine-learning problem definition |
| Write `X` and `y` as a very small array or table | To confirm that formulas and code point to the same object |
| Directly check a mean, error, or difference through Python output | Because this is the minimum intuition needed to follow evaluation metrics and loss explanations |
| Change an array's `shape` and `axis` and explain the difference | So you do not confuse data direction and calculation direction |
| Picture one Git commit where code and records changed together | Because experiment and document reproducibility must be left together |

## The Understanding You Gain After This Part

After this Part, instead of memorizing math and software tools separately, you can see them as one learning flow.

1. Formulas write down computational intent.
2. Python executes small calculations.
3. NumPy reuses vector and matrix computation.
4. Pandas lets datasets be read as tables.
5. Matplotlib lets the shape of numbers be checked.
6. Git leaves the change history of manuscript, code, and results.

Once this understanding appears, you no longer see expressions such as `X`, `y`, `fit`, `predict`, loss, metric, train, validation, and test as completely unfamiliar language in the machine-learning text of Part 3. Part 2 is not the stage where every foundation is finished. It is the stage where the minimum shared base for moving into machine learning is built.

## Completion Criteria

- You can explain how variables, functions, sigma, means, and errors in formulas connect to concrete computational procedures.
- You can say where vectors and matrices are used in data and model computation.
- You can explain derivatives, gradients, loss functions, and gradient descent at an introductory level.
- You can distinguish probability, distribution, mean, variance, sample, and estimation as the language of data judgment.
- You can explain where Python code runs and what the difference is between Colab and a local PC.
- You can explain the basic role of Python lists, dictionaries, loops, functions, and classes.
- You can verify NumPy array shape, axis, indexing, slicing, and broadcasting with small examples.
- You can read a Pandas DataFrame around rows and columns and explain the need for learning-oriented dataset preparation.
- You can inspect function shapes, scatter plots, histograms, and loss curves with Matplotlib.
- You can explain Git commits and branches from the viewpoint of managing the change history of documents, code, images, and experiment records.
- Before moving into Part 3, you can state the basic meaning of `X`, `y`, sample, feature, fit, and predict.

## Short Check

- Can you explain that formulas, arrays, tables, graphs, and Git all connect into the same learning flow in Part 3?
- Can you look at `one expression that blocks you now` and choose to which Chapter you should return?
- Can you explain `X`, `y`, shape, mean, error, and runtime environment in one sentence each?

## Sources and References

This document is an internal overview that organizes the purpose and learning path of Part 2. It does not directly quote outside sources.
