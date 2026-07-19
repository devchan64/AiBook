# P2-10.1 Why Are Notebooks Useful for Learning?

> Section ID: `P2-10.1`
> Version: `v2026.07.19`

In Part 2 Chapter 7, we separated where Python is executed, including the terminal, shell, interpreter, script, and virtual environment. In Part 2 Chapters 8 and 9, we recovered Python syntax and data structures through small examples.

Now we look separately at notebook environments such as Jupyter Notebook and Google Colab. Here, notebook does not mean a paper notebook. It means a computational notebook where code, output, and explanation can remain together in one document.

Notebooks appear especially often in AI learning. That is because formulas can be turned into code and checked, data tables can be printed, charts can be drawn, and interpretation can be written right beside them.

This Section explains the basic distinctions among `notebook`, `code cell`, `markdown cell`, and `output`. If Chapter 7 dealt with where execution happens, and Chapters 8 through 9 dealt with what is written in what kind of sentences, here the topic is how that execution and computation are left and reread together inside one document. A notebook is more accurately read not as a new execution-environment name, but as a format that bundles already executed code and output into a learning record. When these concepts appear again in later Sections, use the [Concept Glossary](/AiBook/reference/concept-glossary/) as a reference point too.

When reading this Chapter in the flow of Part 2, first hold the following minimum line.

| Minimum to capture first here | What can be left to the next Section |
| --- | --- |
| The point that a notebook is a recording format that keeps code, output, and explanation in one document | Detailed differences between Colab and Jupyter |
| The point that code cells, markdown cells, and output each have different roles | A more detailed distinction of runtime and file access |
| The point that notebooks are strong for learning and exploration, but do not completely replace scripts | Concrete habits for organizing reproducible records |

| Term | Meaning to capture first in this Section |
| --- | --- |
| notebook | A computational document that contains code, explanation, and output together |
| code cell | A block that runs actual Python code |
| markdown cell | A block that leaves questions, explanation, and interpretation in writing |
| output | The visible result of code execution, such as values, tables, charts, and error messages |
| computational notebook | A format that leaves computation and explanation together inside one document |

It is enough to understand a notebook not as `new syntax`, but as `a place that keeps computation and interpretation together`. Execution location and reproducibility are handled more concretely in P2-10.2 and P2-10.3.

## Scope of This Section

This Section is not for explaining how to install a notebook or how to use Colab in detail. The difference between Colab and a local PC environment was already seen in P2-3.5 and Part 2 Chapter 7, and the difference between Jupyter and Colab is handled separately in P2-10.2.

This Section answers the following questions.

- What is a notebook?
- How are code cells, markdown cells, and output used together?
- Why is a notebook useful for learning records?
- Why is a notebook not always better than a script?
- With what attitude is it useful to use notebooks in the AI relearning process?

This Section first closes the question of why notebooks are useful for learning: code, output, and explanation can remain together as one record. The distinction between an `.ipynb` file and a running runtime is reconnected immediately in P2-10.2 and P2-10.3. The internal structure of servers and kernels stays outside the current scope of the main text.

## Goals of This Section

- You can explain a notebook as a computational document containing code, explanation, and output together.
- You can distinguish the roles of a code cell and a markdown cell.
- You can explain why notebooks are useful for experiments and learning records.
- You can explain that cell execution order and hidden state are important cautions in notebooks.
- You can explain that notebooks can be used as learning drafts, but repeatedly reused code may need to be separated into scripts or modules.

## Three Criteria

| Criterion | Why it matters | Level of understanding needed in this Section |
| --- | --- | --- |
| What a notebook is | It helps you read a notebook not as new syntax, but as a document that keeps computation and interpretation together | Understand it as a document-style practice space where code, explanation, and execution results remain together |
| Why it is useful for learning | It connects the strength of small-step practice and immediate confirmation to the current question | Hold the point that code can be run cell by cell and results can be checked immediately |
| What is the biggest point to watch | It helps you see reproducibility risk together with convenience | Understand that if cell execution order becomes mixed up, result interpretation can become wrong |

## A Notebook Is a Document Where Code and Explanation Stay Together

Project Jupyter's official documentation explains notebooks as shareable documents that can combine code, plain-text explanation, data, visualizations, and interactive elements. Jupyter architecture documentation also explains a notebook as an editable document that stores code, output, and markdown notes together.

Here, understand a notebook both as `a document that runs code` and as `a learning record that keeps execution results and explanation together`.

A normal Python script file is usually code-centered.

Problem situation: You want to see simply what gets executed when a script file contains only computation code.
Input: A student score list and an average calculation expression.
Expected output: The average score is printed through `print`.
Concept to check: See that in a script, code execution itself often comes before explanation.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
print(average)
```

In contrast, in a notebook, explanation and result can be placed around the same computation together. For example, in a markdown cell you could write, `In this cell, we calculate the average score of three students.`

Problem situation: In a notebook, you want to check that a computation result can be seen directly as cell output without storing it only through `print`.
Input: A student score list and an average calculation expression.
Expected output: The value of `average` on the last line of the cell is shown directly.
Concept to check: Confirm that in a notebook, explanation and output are read together inside one document.

```python
scores = [82, 75, 45]
average = sum(scores) / len(scores)
average
```

Looking at the output, you can immediately confirm that the average is about `67.3`.

This difference may look small, but it matters in learning. `What was calculated`, `why it was calculated`, and `how the result was interpreted` all remain in one document.

## Cells Are the Basic Units of a Notebook

A notebook is usually made of cells. A cell is a small block inside the document.

| Cell type | English | Role |
| --- | --- | --- |
| code cell | code cell | runs Python code and similar content |
| markdown cell | markdown cell | writes explanation, titles, lists, formulas, and links |
| output | output | shows execution results, tables, charts, and error messages |

The flow can be seen like this.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-cell-learning-flow-en.mmd"
```

The core of notebook learning is to repeat in a short cycle the four steps: `write the question`, `run the code`, `look at the result`, and `leave the interpretation`.

This method is useful when relearning AI mathematics and Python. For example, when learning sigma, mean, variance, and gradient, reading only the formulas can feel abstract. In a notebook, they can be confirmed numerically in the cell directly below.

## Notebooks Are Good for Leaving Learning Traces

The first reason notebooks are useful for learning is that they make it easy to leave traces of thought.

For example, when learning averages, if only the final code remains, it becomes easy to forget later why that calculation was done.

Problem situation: You want to see what it looks like when only average-calculation code remains and the question and interpretation are missing.
Input: A one-line average calculation using a student score list.
Expected output: The average value is calculated, but there is no explanation left in the code for why it was calculated.
Concept to check: See that code containing only a result and a notebook record containing question and interpretation together have different learning effects.

```python
scores = [82, 75, 45]
sum(scores) / len(scores)
```

In a notebook, before the calculation you can leave a question such as, `If we summarize the scores of three students into one representative value, what can we see?`

And after the calculation, you can attach an interpretation such as, `The average is useful for seeing the center of the whole score set, but the fact that a low value like 45 is mixed in does not become fully visible through the average alone.`

This kind of record becomes helpful later when revisiting generalization in P3-5, evaluation metrics in P3-6, and residual and error in P3-10.2.

## Notebooks Are Good for Breaking Experiments into Small Parts

The second reason is that code can be divided and run cell by cell.

For example, you can imagine the following flow.

```mermaid
--8<-- "assets/part-02/chapter-10/notebook-experiment-flow-en.mmd"
```

The same thing can be done in a script too, but compared with running a whole file at once, checking one cell at a time can feel less burdensome.

Small practice can be divided like this.

The first cell prepares the data.

Problem situation: When dividing notebook practice into small steps, you want to put a separate data-preparation cell first.
Input: A list containing five scores.
Expected output: There is no output, but the data used by later cells is prepared.
Concept to check: See that in a notebook, separating data preparation into its own cell makes later dependencies easier to see.

```python
scores = [82, 75, 45, 90, 61]
```

The second cell calculates a summary value.

Problem situation: You want to calculate only the average from the prepared data and inspect the intermediate result.
Input: The `scores` list created in the previous cell.
Expected output: The average score `mean_score` is shown as cell output.
Concept to check: See that if one cell performs only one calculation, it becomes easier to read at which step the value changes.

```python
mean_score = sum(scores) / len(scores)
mean_score
```

The third cell changes the condition.

Problem situation: You want to immediately compare which values remain when the condition changes on the same data.
Input: The `scores` list and the condition `60 or above`.
Expected output: A list containing only the passing scores is shown.
Concept to check: See that notebooks are good for quickly checking result differences while changing one condition at a time.

```python
passed = [score for score in scores if score >= 60]
passed
```

When divided like this, it becomes easier to see `What changed at which step?`

## The Strength Is That Output Can Be Seen Immediately

Notebooks show output directly below the code. Numbers, tables, charts, and error messages remain close to the code.

This matters in AI learning.

| Learning scene | What is easy to check in a notebook |
| --- | --- |
| recovering formulas | small numeric computation results |
| recovering statistics | results of mean, variance, and sample calculations |
| checking data | tables, row counts, missing values |
| visualization | line charts, scatter plots, histograms |
| model experiments | loss values, evaluation metrics, prediction results |

Saying that output can be seen immediately does not mean `the result is always correct`. Rather, what matters is that you can immediately ask questions such as `Is the value larger than expected?`, `Is the number of rows in the table correct?`, `Is the chart shaped the way I expected?`, and `In which cell did the error message occur?`

The notebook is a good environment for repeating these questions.

## A Caution of Notebooks: Cell Execution Order

Notebooks are convenient, but they also have points to watch. The most important is execution order.

Look at the following example.

Problem situation: You assume that a variable used in a later cell is created first in an earlier cell.
Input: Code that stores `10` in the variable `x`.
Expected output: There is no output, but the runtime state on which the next cell depends is created.
Concept to check: See that notebook cells create runtime state beyond the code visibly written in the document.

```python
x = 10
```

In another cell, the following code is run.

Problem situation: A variable created in an earlier cell is used immediately in a later cell for computation.
Input: The variable `x`, assumed to have already been defined.
Expected output: `15` is calculated.
Concept to check: Confirm that if the earlier cell has not run, or if the order becomes tangled, the later result also changes.

```python
x + 5
```

This code runs only if `x` has been created earlier. But if you skip a middle cell, or if a value left from a previously run cell remains, then the visible order of the document and the actual execution state can differ.

The following habits are important here.

| What to check | Reason |
| --- | --- |
| rerun from top to bottom | reduce hidden state |
| gather necessary imports near the front | make visible which packages are needed |
| keep a clear data-preparation cell | make visible what later cells depend on |
| write interpretation directly below the result | preserve context for later reading |

Because a notebook can be executed freely, the execution order can instead become disordered more easily. This requires more caution than a script.

## Case Study

### Case 1. A learning note that checks mean and variance again

Suppose someone relearning statistics wants to understand `mean` and `variance` together. If the code is written as one long script file, the calculation runs, but why the calculation was done and how the result should be read can quickly become blurred.

In a notebook, you can first write a question such as `What becomes visible if we summarize five scores into one representative value?`, then calculate the average in the next cell, and directly below it attach an interpretation such as `The average alone does not sufficiently reveal that one low score is mixed in.` If you then add a variance-calculation cell, you can compare spread within the same data too.

This flow shows that a notebook is not merely an execution tool. A person can bundle the question, calculation, output, and interpretation in one document, and when opening it later can immediately recover what was checked.

At the same time, this case also reveals a caution of notebooks. If only the cell that changes the average is rerun and the interpretation cell is not corrected, then the visible explanation and the actual computed result can diverge. That is why a notebook must be treated both as `a document with execution results beside it` and as `a record that must be rerun and verified`.

## A Notebook Does Not Replace Scripts

Notebooks are good for learning and exploration, but they do not fit every situation.

Code that must be run repeatedly, code reused in other projects, and code that must be automated may be better separated into `.py` scripts or modules.

| Situation | Is a notebook good? | Is a script good? |
| --- | --- | --- |
| experimenting with a concept for the first time | yes | possible, but explanation must be kept separately |
| interpreting data and charts while looking at them | yes | possible, but intermediate-result checking may feel inconvenient |
| running the same work automatically every day | may be disadvantageous | yes |
| reusing functions across several projects | may be disadvantageous | yes |
| sharing documents together with experiment records | yes | a separate document is needed |

Therefore, here we view notebooks as a tool for learning records and small experiments. Later, if the code grows longer and repeated execution becomes necessary, then a judgment is needed to move it into scripts and package structure.

## How to Use Notebooks in AI Relearning

For the reader of this document, a notebook is closer to `a workspace for recovering understanding` than to `a file for submitting correct answers`.

It is good to use it in the following order.

1. First write the question in a markdown cell.
2. Write a small data or numeric example in a code cell.
3. Output the result.
4. Briefly interpret whether the result matches your expectation.
5. Rerun the cells from top to bottom.

For example, when studying probability and statistics, you can begin with a question such as `How much can the sample mean change when the data changes?`

Problem situation: You want to compare the means of two different samples in one notebook cell.
Input: Two sample lists, `sample_a` and `sample_b`, with different value composition.
Expected output: The two sample means are shown together.
Concept to check: See that a notebook is good for leaving a small sample-comparison experiment together with question, calculation, and interpretation.

```python
sample_a = [10, 12, 13, 11, 14]
sample_b = [8, 16, 9, 15, 12]

mean_a = sum(sample_a) / len(sample_a)
mean_b = sum(sample_b) / len(sample_b)

mean_a, mean_b
```

If you then attach an interpretation such as `The two samples have different value composition, but their means can still be similar. The mean alone does not reveal every difference in the distribution.`, then the computation result remains as a record.

This method continues later in machine-learning practice too. Rather than trying to complete data preparation, model learning, evaluation, and interpretation all at once, confirm small questions cell by cell.

## Checklist

- You can explain a notebook as a computational document containing code, explanation, and output together.
- You can distinguish a code cell and a markdown cell.
- You can explain why notebooks are useful for AI mathematics and Python practice records.
- You can explain that cell execution order can affect the result.
- You can explain that a notebook does not completely replace scripts.
- You can leave question, code, output, and interpretation together in a learning notebook.
- You can explain notebooks both as execution tools and as learning-record documents.

## Sources and References

- Project Jupyter, [Project Jupyter Documentation](https://docs.jupyter.org/en/latest/){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, checked on 2026-07-19. Used to confirm that notebooks are documents combining code, explanation, data, visualization, and interaction.
- Project Jupyter, [Architecture](https://docs.jupyter.org/en/latest/projects/architecture/content-architecture.html){: target="_blank" rel="noopener noreferrer" }, Jupyter Documentation 4.1.1 alpha, checked on 2026-07-19. Used as background for distinguishing notebook documents, user interfaces, kernels, and related components.
- Google, [Welcome to Colab](https://colab.research.google.com/notebooks/intro.ipynb){: target="_blank" rel="noopener noreferrer" }, Google Colab, checked on 2026-07-19. Used to confirm examples of running and recording code with explanations in a browser-based notebook environment.
