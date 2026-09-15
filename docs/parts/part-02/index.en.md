# Part 2. Rebuilding the Foundations

> Section ID: `P2-index`
> Version: `v2026.09.15`

After exploring the main areas of AI and the distinction between learning and execution in [Part 1](../part-01/summary.en.md), Part 2 builds the foundation for reading the formulas and code used in those explanations. Whether mathematics is new to you or you have forgotten what you learned, you can begin with small calculations. You will execute mathematical rules in Python, inspect data in arrays and tables, and record results through graphs and change history.

For example, predicting exam results from study time requires separating input values from correct answers and calculating how wrong the predictions are. Mathematics supplies the calculation criteria, Python supplies the steps to execute, and data tools reveal the structure of the values and the results. The tools in Part 2 work together to make this process visible.

## From formulas to execution and records

Part 2 contains 15 chapters. When reading from the beginning, first understand what formulas mean and run small calculations, then move on to data shapes and ways to record your work.

| Learning sequence | Question to check | Reading |
| --- | --- | --- |
| Reading formulas | What calculations do variables, functions, sums, means, and logarithms represent? | [Mathematics and AI computation](chapter-01/section-01.en.md), [Variables, functions, and expressions](chapter-02/section-01.en.md) |
| Calculating with multiple values | How do vectors and matrices group and compare data? | [Scalars, vectors, and matrices](chapter-03/section-01.en.md), [Dot products and distances](chapter-03/section-04.en.md) |
| Change and uncertainty | How does changing a value affect the result, and how do we read the spread of data? | [Derivatives and gradients](chapter-04/section-03.en.md), [Probability](chapter-05/section-01.en.md), [Optimization](chapter-06/section-01.en.md) |
| Running Python | Where does code run, and what roles do values, loops, and functions play? | [Execution environments](chapter-07/section-01.en.md), [Python basics](chapter-08/section-01.en.md) |
| Data structures and notebooks | How do we represent relationships between values and record execution order? | [Data structures](chapter-09/section-01.en.md), [Notebooks](chapter-10/section-01.en.md) |
| Arrays, tables, and graphs | Can we inspect the shape of values, select the data we need, and visualize it? | [NumPy](chapter-11/section-01.en.md), [Pandas](chapter-12/section-01.en.md), [Matplotlib](chapter-13/section-01.en.md) |
| Change history and a combined check | Can we revisit the conditions of a calculation and identify what changed? | [Git](chapter-14/section-01.en.md), [Translating formulas into code](chapter-15/section-01.en.md) |

The mathematics chapters cover introductory concepts and small calculations in linear algebra, differentiation, probability, statistics, and optimization. In Python, you will learn execution environments and basic syntax. NumPy handles array calculations, Pandas supports table selection and organization, Matplotlib provides visualization, and Git manages change history. The focus is on the connections needed to read and run later model-training examples, rather than advanced proofs or every feature of each tool.

## Finding the right section for an unfamiliar term

When a symbol or tool name stops you, use this table to find the relevant calculation or execution context. Further explanations of installation, classes, and traditional data structures appear in the supplementary sections of each chapter.

| Unfamiliar term | What to check | Return to |
| --- | --- | --- |
| Sigma, logarithms, exponentials | Compact notation for repeated calculations and functions that are inverses of each other | [Sigma](chapter-02/section-02.en.md), [Logarithms and exponentials](chapter-02/section-04.en.md) |
| Vectors, matrices, dot products | Grouping multiple values and comparing vectors | [Vectors and matrices](chapter-03/section-01.en.md), [Dot products and distances](chapter-03/section-04.en.md) |
| Derivatives, gradients, loss | Rates of change and the calculation criterion to reduce | [Derivatives and gradients](chapter-04/section-03.en.md), [Loss functions](chapter-06/section-02.en.md) |
| Mean, variance, probability | Data summaries and uncertainty | [Mean and variance](chapter-05/section-02.en.md), [Probability](chapter-05/section-01.en.md) |
| `X`, `y`, features, targets | Inputs supplied to a model and correct answers used for comparison | [Preparing datasets](chapter-12/section-03.en.md) |
| `shape`, `axis`, rows, columns | Array shapes and the axis along which to calculate | [Array shapes and axes](chapter-11/section-02.en.md) |
| Colab, terminal, notebook | Where code runs and in what order | [Colab and local PCs](chapter-03/section-05.en.md), [Rerunning notebooks](chapter-10/section-03.en.md) |
| Commits, branches | Recording file states and reasons for changes | [Git change history](chapter-14/section-01.en.md), [Commits and branches](chapter-14/section-02.en.md) |

## Preparing to read about model training

By the end of this Part, you should be able to connect a formula's inputs, calculation, and outputs to a small program and explain what rows and columns mean in arrays and tables. You should also distinguish what a single mean tells you from what a distribution reveals, and distinguish the size of a loss from the direction in which to reduce it. Alongside the results, record the data, execution environment, and changed conditions as well as the code.

[Part 3](../part-03/index.en.md) builds on this foundation to explore models that learn rules from data. The next questions are how to train a model and how to judge its performance on data not used for training. Before moving on, check your preparation with the small calculations in the [combined check](chapter-15/section-02.en.md) and the [Part 2 summary](summary.en.md).

## Checklist

- Can you identify the inputs and calculations represented by the symbols in a formula?
- Can you explain which questions vector and matrix shapes, rates of change, and probability distributions each answer?
- Can you run a small Python calculation and inspect its results using arrays, tables, and graphs?
- Can you preserve the data, code, environment, and change history needed to revisit a result?

## Sources and further reading

This is an original overview based on the Part 2 chapters. The sources supporting each concept are listed in the linked sections.
