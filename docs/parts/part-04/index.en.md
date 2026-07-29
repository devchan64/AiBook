# Part 4. Machine Learning

> Section ID: `P4-index`
> Version: `v2026.07.26`

Part 2 restored the basics for reading formulas, Python, arrays, tables, graphs, and runtime environments. Now in Part 4, we organize what those tools are actually used for, namely what it means to `learn rules from data`.

Many readers have already used AI services, but here it matters more to regroup that experience into standard concepts. Rather than memorizing model names, first make clear what counts as a machine-learning problem, what data must be collected, what a model learns, what it means for learning to have gone well, and why some models can look accurate while still be risky in practice.

The core purpose of Part 4 is to read [machine learning](/AiBook/en/reference/concept-glossary-alpha/m/#machine-learning) not as a list of models, but as a flow of problem, data, learning, evaluation, and application. [Linear regression](/AiBook/en/reference/concept-glossary-alpha/l/#linear-regression), [logistic regression](/AiBook/en/reference/concept-glossary-alpha/l/#logistic-regression), [decision tree](/AiBook/en/reference/concept-glossary-alpha/d/#decision-tree), [random forest](/AiBook/en/reference/concept-glossary-alpha/r/#random-forest), boosting, [clustering](/AiBook/en/reference/concept-glossary-alpha/c/#clustering), [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction), and [reinforcement learning](/AiBook/en/reference/concept-glossary-alpha/r/#reinforcement-learning) are not separate items to memorize. They are options that appear depending on what problem is being solved, what the [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input) and [model output](/AiBook/en/reference/concept-glossary-alpha/m/#model-output) are, and what criteria define good or bad performance.

Part 4 follows the same rule as the other Parts: within the same Part, a major concept should receive its detailed explanation in one main Section first, and later Sections should keep only the minimum needed for the current context. So `supervised learning` is anchored first in `P4-2.1`, `unsupervised learning` in `P4-2.2`, `reinforcement learning` in `P4-2.3`, the role distinction between `validation` and `test` in `P4-4.2`, `overfitting` and `underfitting` in `P4-5.1`, `metric` in `P4-6.1`, `feature selection` in `P4-7.1`, `preprocessing` in `P4-7.2`, `baseline` in `P4-8.2`, `linear regression` in `P4-10.1`, `logistic regression` in `P4-11.1`, `k-NN` in `P4-12.1`, `SVM` in `P4-13.1`, `decision tree` in `P4-14.1`, `random forest` in `P4-15.1`, `gradient boosting` in `P4-16.1`, `clustering` in `P4-17.1`, and `dimensionality reduction` in `P4-18.1`. When they reappear, read them together with relevant glossary entries such as [machine learning](/AiBook/en/reference/concept-glossary-alpha/m/#machine-learning) and [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction), plus the current context.

So Part 4 reconnects the map of machine learning in the following order.

1. The distinction among AI, machine learning, and deep learning
2. The difference among supervised learning, unsupervised learning, and reinforcement learning
3. Data splitting, validation, overfitting, generalization, and evaluation metrics
4. Feature selection, preprocessing, model choice, baseline models, and tuning
5. Intuition for representative classical models
6. Extensions through clustering, dimensionality reduction, and reinforcement learning
7. A shared perspective that prepares the move into Part 5 on deep learning

## Main Questions in This Part

Part 4 does not begin by listing algorithm names. It first establishes the questions that must be held repeatedly when reading machine-learning explanations.

- What makes a problem [supervised learning](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning), [unsupervised learning](/AiBook/en/reference/concept-glossary-alpha/u/#unsupervised-learning), or [reinforcement learning](/AiBook/en/reference/concept-glossary-alpha/r/#reinforcement-learning)?
- What do [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input), [model output](/AiBook/en/reference/concept-glossary-alpha/m/#model-output), [supervised learning label](/AiBook/en/reference/concept-glossary-alpha/s/#supervised-learning-label), and [reward](/AiBook/en/reference/concept-glossary-alpha/r/#reward) each mean, and where are they separated?
- Why are [training](/AiBook/en/reference/concept-glossary-alpha/m/#model-training), [validation](/AiBook/en/reference/concept-glossary-alpha/v/#validation-data), and [test](/AiBook/en/reference/concept-glossary-alpha/t/#test-data) split apart, and how is [generalization](/AiBook/en/reference/concept-glossary-alpha/g/#generalization) checked?
- What kinds of errors do [metrics](/AiBook/en/reference/concept-glossary-alpha/m/#metric) reveal, and what kinds can they hide?
- Why should [feature selection](/AiBook/en/reference/concept-glossary-alpha/f/#feature-selection), [preprocessing](/AiBook/en/reference/concept-glossary-alpha/p/#preprocessing), [baseline models](/AiBook/en/reference/concept-glossary-alpha/b/#baseline-model), and tuning be checked before model names?
- What problem sense do representative classical models provide, and where do their strengths end and their limits begin?

## Reading Machine Learning as Shared Questions and Judgment Standards

This Part rebuilds the large structure of machine learning and reconnects introductory knowledge learned long ago into a standard flow.

Machine learning is not difficult only because there are many algorithms. Even with the same data, the reading frame changes depending on how the problem is defined: classification, regression, clustering, dimensionality reduction, or reinforcement learning. Before choosing a model, it matters more to understand why training data, validation data, and test data are separated, why overfitting and generalization must be distinguished, and how evaluation metrics should be read.

Part 4 establishes that base. The goal is not to dig deeply into the mathematics of every algorithm, but to let you reconstruct the flow of defining the problem, reading the data, deciding the input and output, deciding what the model should learn, separating learning from evaluation, reading metrics, and checking the model's limits and application conditions whenever you read about machine learning.

At this point, the three-way distinction established in P1-8 must be brought over directly. Supervised learning is a problem of matching target outputs from examples that contain `inputs and labels` together. Unsupervised learning is a problem of finding structure and representations `without human-attached labels`. Reinforcement learning is a problem of adjusting a policy using `rewards after actions instead of labels`. In particular, the reward in reinforcement learning is not the same signal as the label in supervised learning, and that distinction is maintained throughout Part 4.

## Core Questions To Close In Machine Learning

After reading Part 4, the target is to have roughly the following level of understanding.

- You can explain the relationship among AI, machine learning, and deep learning in broad flow.
- You can distinguish supervised learning, unsupervised learning, and reinforcement learning from the perspective of data and problem definition.
- You can explain why training, validation, and test data are separated.
- You can explain the difference among overfitting, underfitting, and generalization.
- You can understand that a metric is both a numerical property of the model and a criterion tied to business judgment.
- You can explain the role of feature selection, preprocessing, model selection, baseline models, and tuning.
- You can distinguish the intuition and use cases of linear regression, logistic regression, decision tree, random forest, and gradient boosting.
- You can explain clustering and dimensionality reduction as methods for reading structure without answer labels.
- You can understand reinforcement learning as learning that adjusts policy through actions and rewards, and distinguish value-based and policy-based approaches at an introductory level.

## Boundaries Machine Learning Explains And Questions Left Open

Part 4 explains the shared structure of machine learning. Within the main text, it therefore covers the following.

- The broad distinction among supervised learning, unsupervised learning, and reinforcement learning
- Data splitting, validation, overfitting, generalization, and evaluation metrics
- Feature selection, preprocessing, baseline models, model selection, and tuning
- The intuition of representative classical models, clustering, dimensionality reduction, and reinforcement learning

By contrast, the following topics are not all covered deeply in this Part.

- Strict mathematical derivations and proofs for each algorithm
- Automated systems for large-scale hyperparameter search
- Internal computation in recent deep-learning architectures and large generative models

This omission is not avoidance but scope control. The responsibility of Part 4 is to establish `the common questions for reading machine learning`. The main text on deep learning and large generative models is recovered in later Parts.

## What Is Explained

Part 4 is organized into four large flows.

First, it re-establishes the broad distinctions inside machine learning. It looks at the relationship among AI, machine learning, and deep learning, then organizes the difference among supervised learning, unsupervised learning, and reinforcement learning. The purpose of this segment is to understand `how the types of problems differ`, more than to memorize algorithm names.

The first comparison axis to hold here is the learning signal. Supervised learning reads human-attached labels, unsupervised learning reads unlabeled structure, and reinforcement learning reads rewards that return after actions. If this distinction shakes, later explanations of classification, clustering, and value-based reinforcement learning will stop being read as different problem setups.

Next it covers the shared base for reading learning. This includes data splitting, validation, overfitting, generalization, evaluation metrics, feature selection, preprocessing, model selection, baseline models, and tuning. This segment is the center of Part 4, because no matter which algorithm appears later, the reader must keep asking how the data were split, what the model learned, how the score should be read, and whether results that look good right now are actually trustworthy.

The scope of evaluation metrics is also set clearly inside this flow. In the main text of Part 4, the priority is on metrics that hold the question `what should be asked first for this problem type`, such as accuracy, precision, recall, F1, MAE, RMSE, and R2. Items that make score interpretation more delicate, such as ROC, PR, log loss, calibration, reliability, and silhouette, are collected as introductory support in P4-6.4 supplementary learning, and threshold and calibration reappear again in P4-15.3.

At this point, the reader should hold two comparison devices together. The [confusion matrix](/AiBook/en/reference/concept-glossary-alpha/c/#confusion-matrix) and [error cases](/AiBook/en/reference/concept-glossary-alpha/m/#model-validation) let you read `where and how the model was wrong`, and the [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#baseline) asks `whether the score is actually a meaningful improvement`. Rather than making readers memorize scores as isolated numbers, Part 4 puts more weight on building the habit of reading the error structure and the baseline together.

This flow is read in the following order.

| Evaluation reading order | Question to check first | Why it is needed |
| --- | --- | --- |
| Confusion matrix | In which cells does the model fail the most? | It reveals the error direction that a single accuracy number can hide. |
| Representative error cases | On which actual inputs, and why, does the model fail? | They expose data problems and boundary cases that numbers alone cannot show. |
| Baseline comparison | Is this improvement really meaningful? | It separates scores that only look high because the problem is easy from real improvement. |

The evaluations to hold especially tightly in the early part of Part 4 are the following three steps.

| What to look at first | The next question that follows | Where it continues in the next Sections |
| --- | --- | --- |
| Confusion matrix and error cases | Where is it wrong, and what inputs is it missing? | P4-6 evaluation metrics |
| Baseline comparison | Is this score really better than an easy reference point? | P4-8 baseline models |
| Tuning results | Does a small score increase justify the cost and complexity? | P4-9 hyperparameters |

This order can be compressed again into the following three lines.

| Minimum order for reading evaluation | Why this order comes first |
| --- | --- |
| Confusion matrix | Because you must see where the model is wrong before you can read the direction of a score. |
| Representative error cases | Because you must see the actual inputs before you can check data problems and edge cases. |
| Baseline comparison | Because only then can you judge whether the difference is a meaningful improvement. |

The recording language that runs through all of Part 4 is fixed inside this flow as well. Even when a score or structure looks plausible, what should be recorded as fact must be separated from interpretations that still require more checking.

| What should be recorded repeatedly in this Part | The shortest recording language |
| --- | --- |
| The scores, structures, and comparison results that were observed | fact |
| How far those results can be trusted and where judgment should stop | interpretation |
| The next experiment or next item to check | next question |

Next it turns to representative classical models. It covers linear regression, logistic regression, k-NN, SVM, decision tree, random forest, and gradient boosting, and asks what each does well and where caution begins. The goal here is problem sense rather than formula derivation.

Rather than memorizing model names, the task is to check `what should come to mind first in a small data scene` as shown below.

| Small data scene | Model family to recall first | Why that family is the starting point |
| --- | --- | --- |
| You must predict a continuous value from numeric inputs | Linear regression | It is good for quickly checking the simplest relationship and a baseline. |
| You must separate yes/no or other categories | Logistic regression, decision tree | They are good for comparing the basic baseline of classification and rule-like intuition. |
| You need strong candidates on tabular data | Random forest, gradient boosting | They are representative choices for handling nonlinear relations and feature interactions well. |
| You want to see similar groups without labels | Clustering | It is the most direct starting point for reading structure without answers. |
| There are too many variables and you want to reduce the axes first | Dimensionality reduction | Summarizing the representation and visualizing it matters more than prediction first. |
| You are dealing with a problem where action results return later | Reinforcement learning | State, action, and reward structure matter more than input-answer pairs. |

Finally, the Part expands toward unsupervised learning and reinforcement learning. Through clustering, dimensionality reduction, and reinforcement-learning algorithms, it organizes the point that machine learning also includes areas beyond `learning to get the answer right`.

## Why It Is Needed

Experience with AI services alone is not enough to claim full understanding of machine learning. Expressions such as `the model was fit on training data`, `the validation score rose but the test score fell`, `changing feature preprocessing reduced overfitting`, or `the model is 1% better than the baseline but the operational meaning is still unclear` appear often.

To read these sentences, you must know the structure before the algorithm names. You need to know what `fit` means, why validation and test are separated, and why a performance increase does not immediately carry operational meaning.

The following misunderstandings also appear often.

- Changing only the model will solve performance.
- A system is good as long as a single score is high.
- If there is a lot of data, generalization will happen automatically.
- Reinforcement learning teaches itself, so in reality you can just try many actions.

Part 4 reduces these misunderstandings. Rather than providing a model catalog, this Part builds the basic literacy to read, compare, and doubt machine-learning claims.

## Questions This Part Does Not Finish

Because Part 4 explains the shared structure of machine learning, it intentionally passes the following questions to Part 5 and Part 6.

- Why did representation learning become a larger turning point than classical models?
- How do gradient, loss, and optimizer extend into larger computational structures in neural networks?
- How do generative models and large language models expand this common structure?

These questions are recovered in the main text later: representation learning and neural-network computation in Part 5, and generative models and LLM expansion in Part 6.

## The Understanding You Gain After This Part

After this Part, you can view machine learning not as a simple list of models but as one workflow. Defining the problem, selecting the data, choosing the input and output, training the model, checking generalization, reading the metrics, and reviewing application conditions and limits begin to appear as one connected sequence.

Once this understanding forms, linear regression, logistic regression, random forest, clustering, and reinforcement learning no longer look like unrelated names. They become options for different problems, and it becomes visible that data definition and evaluation criteria always come before them, while application limits and operational judgment always follow them.

In other words, Part 4 is a Part that repeatedly records `problem structure -> inspection criteria -> next question` rather than a collection of model names. Here the inspection criteria should not jump directly to fixed causes or policy conclusions. They should first leave signals that require further review and the order of the next checks.

## Completion Criteria

- You can distinguish machine-learning problems from the perspective of supervised learning, unsupervised learning, and reinforcement learning.
- You can explain why training, validation, and test data are separated.
- You can describe the difference among overfitting, underfitting, and generalization with examples.
- You can explain that evaluation metrics change according to problem type and business goals.
- You can distinguish the role of feature selection, preprocessing, baseline models, and tuning.
- You can explain at an introductory level the intuition and difference among linear regression, logistic regression, decision tree, random forest, and gradient boosting.
- You can explain that clustering and dimensionality reduction are ways to read structure in unlabeled data.
- You can understand reinforcement learning as action-and-reward-centered learning and describe even its application cautions.
- You can explain why Part 4 handles deep learning separately and how it connects forward.

## Sources and References

This overview page is an internal overview that organizes the purpose and learning path of Part 4. It does not directly quote outside material.
