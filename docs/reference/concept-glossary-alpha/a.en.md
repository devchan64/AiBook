# Concept Glossary: A

This page lists English glossary entries for this letter directly. Each entry is written for English readers without sending them to another glossary page.

<a id="abstract-data-type"></a>

## abstract data type

- Meaning: An abstract data type defines a data structure by the operations it must provide, not by the way it is stored internally. The important promise is what users can do with it, such as push, pop, enqueue, dequeue, or inspect the front item.
- Why it matters: This separates the visible behavior of a structure from its implementation. A stack or queue can be implemented with an array, a linked structure, or another internal layout, while still offering the same conceptual operations. This distinction helps readers understand API design, implementation choices, and why the same idea can have several concrete forms.
- Related concepts: `data structure`, `operation`, `implementation`
- Core Section: `P2-9.1`
- Appears in: `P2-9.4`

<a id="accountability"></a>

## accountability

- Meaning: Accountability is the principle that an AI system's outputs, decisions, and automated actions must have identifiable human or organizational responsibility behind them. It asks who reviewed, approved, explained, corrected, and operated the system when something goes wrong.
- Why it matters: AI results can look fluent or authoritative even when they create risk. In high-impact settings, logs, approval records, review procedures, and ownership boundaries are needed so a problem is not dismissed as something the model simply did. Accountability is not only about blame after failure; it is a design principle for making responsibility visible before deployment.
- Related concepts: `human oversight`, `safety`, `review`, `log`
- Core Section: `P1-15.1`
- Appears in: `P1-10.3`

<a id="accuracy"></a>

## accuracy

- Meaning: Accuracy is the fraction of predictions that are correct: correct predictions divided by all predictions. It is one of the most intuitive metrics for classification because it quickly summarizes how often a model chose the right answer.
- Why it matters: Accuracy is useful as a first check, but it can hide important failure patterns. With imbalanced data, a model can look accurate while ignoring rare but important cases. Readers should treat accuracy as a starting point and then ask what kinds of mistakes remain, whether some errors cost more than others, and whether other metrics are needed.
- Related concepts: `loss curve`, `validation`, `test`
- Core Section: `P2-13.3`
- Appears in: `P2-14.2`

<a id="action"></a>

## action

- Meaning: An action is something an agent actually chooses and executes in a given state. In search or reinforcement learning it changes the environment; in a service agent it may mean searching, reading a file, calling an API, editing a document, or reporting a result.
- Why it matters: Actions are where reasoning turns into state change. The available action set controls what the agent can accomplish, what risks it can create, and what observations it can gather next. This concept helps separate internal computation from external execution, and it makes clear why tool permissions and action design matter for both capability and safety.
- Related concepts: `state`, `policy`, `reward`, `observation`
- Core Section: `P1-8.3`
- Appears in: `P1-7.1`, `P1-14.3`

<a id="action-bucket"></a>

## action bucket

- Meaning: An action bucket is an operational category that says what kind of follow-up is needed, such as immediate fix, recheck, or improvement in a later iteration. It classifies an issue by the next practical response rather than by a theoretical failure type alone.
- Why it matters: Similar-looking signals can require different handling. Some issues interrupt the reader and need immediate correction; some should be reproduced first; others belong in a later improvement plan. Action buckets keep operational records from becoming passive issue lists and connect each observation to a concrete next step.
- Related concepts: `next action`, `priority`, `recheck`, `improvement plan`, `incident record`
- Core Section: `P7-7.3`
- Appears in: `P7-7.2`, `P7-7.4`

<a id="activation"></a>

## activation

- Meaning: An activation is an intermediate value produced inside a model layer or computation step. It is not the final answer, but a temporary internal response created as input passes through the network.
- Why it matters: Neural networks do not jump directly from input to answer. They build a chain of intermediate representations, and activations are the values that carry those representations forward. Understanding activations helps readers see a network as a sequence of computations rather than as a sealed answer box.
- Related concepts: `representation`, `vector`, `parameter`
- Core Section: `P1-3.3`
- Appears in: `P1-4.3`, `P1-8.2`, `P3-6.1`, `P3-6.2`, `P5-10.1`, `P5-10.2`

<a id="activation-function"></a>

## activation function

- Meaning: An activation function transforms a weighted sum or intermediate score before it is passed to the next layer or output. It introduces a non-linear response instead of passing a simple linear combination forward unchanged.
- Why it matters: Repeating only linear combinations would not give a deep network much more expressive power. Activation functions let layers form more complex decision boundaries and representations, while also affecting gradient flow and training stability. They explain why deep networks need both stacked layers and non-linear response curves.
- Related concepts: `linear combination`, `activation`, `hidden layer`
- Core Section: `P5-1.2`
- Appears in: `P5-3.1`, `P5-3.2`

<a id="adapter"></a>

## adapter

- Meaning: An adapter is a small additional module inserted around or between parts of a base model so the model can be adapted without retraining the whole body. It collects task-specific changes in a smaller component while the main model remains largely shared.
- Why it matters: Adapter methods belong to the broader family of efficient adaptation techniques. They are related to LoRA and fine-tuning, but differ in where the added structure sits and how updates are stored. This helps readers see efficient tuning as a family of design choices, not a single method name.
- Related concepts: `LoRA`, `fine-tuning`, `parameter`
- Core Section: `P6-9.5`

<a id="agent"></a>

## agent

- Meaning: An agent is an execution structure that receives a goal, inspects state, chooses actions, observes results, and continues across multiple steps. In this book, the term usually refers to service or system agents that coordinate search, tool use, review, and retries.
- Why it matters: A single chatbot answer and a multi-step agent workflow are different things. Agent quality depends not only on the model, but also on planning, tool selection, state tracking, stopping conditions, and recovery from failed steps. This concept also helps distinguish service agents from reinforcement-learning agents.
- Related concepts: `tool`, `orchestration`, `harness`, `observation`, `stop condition`
- Core Section: `P1-14.3`
- Appears in: `P1-14.4`, `P1-14.5`, `P1-14.6`, `P6-14.1`, `P6-14.2`, `P6-15.1`, `P6-15.2`, `P7-6.1`, `P7-6.2`

<a id="aggregation"></a>

## aggregation

- Meaning: Aggregation turns many rows or values into smaller summary values such as a mean, sum, count, or ratio. It is a way to read a table through grouped or summarized patterns rather than through each row one by one.
- Why it matters: Large tables do not answer questions just by being large. Aggregation helps decide which summary represents the current question and whether a pattern appears only after rows are grouped. It also warns readers that a single average may hide counts, ratios, or subgroup differences.
- Related concepts: `groupby`, `filtering`, `column`
- Core Section: `P2-12.2`
- Appears in: `P2-12.3`, `P3-1.2`

<a id="ai-artificial-intelligence"></a>

## AI, artificial intelligence

- Meaning: Artificial intelligence is a broad field and system category for computational methods that perform functions associated with intelligence, such as rule-based reasoning, search, learning, generation, and planning. It is not the name of one model or one recent technology.
- Why it matters: AI, machine learning, deep learning, generative AI, and LLMs are often mixed together in casual speech. This concept gives readers the top-level category needed to separate the problem area, the learning method, the model family, and the deployed service. It also helps make claims about AI progress more precise.
- Related concepts: `machine learning`, `deep learning`, `generative AI`, `large language model`
- Core Section: `P1-1.1`
- Appears in: `P1-index`, `P1-1.2`, `P1-summary`

<a id="alert-grade"></a>

## alert grade

- Meaning: An alert grade is a finer operational label for review urgency, such as watch, review, or action. It does not prove that an issue is real; it marks how quickly and carefully the signal should be inspected.
- Why it matters: A large gap alone should not always trigger immediate action, especially when sample size is small or the signal may be a one-time spike. Alert grades combine difference size, repeatability, recency, and reader impact into a more practical review order. They help operations move from raw signals to prioritized inspection.
- Related concepts: `action bucket`, `priority`, `recheck`, `status inspection`, `incident record`
- Core Section: `P7-7.4`
- Appears in: `P7-summary`

<a id="alexnet"></a>

## AlexNet

- Meaning: AlexNet is the model that made the power of deep convolutional neural networks and GPU training widely visible through the 2012 ImageNet competition. It is both a specific model and a symbol of a turning point in deep learning.
- Why it matters: AlexNet shows why deep learning became more than a research trend in image recognition. Its impact came from the combination of large data, deeper CNNs, and large-scale computation. It helps readers understand why later models built on the idea that learned representations could replace many hand-designed image features.
- Related concepts: `deep learning`, `CNN, convolutional neural network`, `learned representation`
- Core Section: `P1-9.1`

<a id="alignment"></a>

## alignment

- Meaning: Alignment is the design problem of making a model's behavior fit human intent, safety rules, and policy constraints. It is not only about understanding instructions, but also about avoiding unacceptable outputs and acting cautiously in sensitive contexts.
- Why it matters: A more capable model is not automatically a safer model. Alignment separates usefulness from acceptable behavior and shows why performance, truthfulness, refusal boundaries, and safety constraints must be considered together. It also separates model behavior from external controls such as permissions and approval workflows.
- Related concepts: `instruction tuning`, `prompt`, `evaluation`
- Core Section: `P6-9.2`
- Appears in: `P6-16.1`

<a id="ann-approximate-nearest-neighbor"></a>

## ANN, approximate nearest neighbor

- Meaning: Approximate nearest neighbor search finds sufficiently close vector candidates quickly instead of always guaranteeing the exact closest item. It intentionally trades perfect optimality for speed at scale.
- Why it matters: Large vector collections make exact comparison expensive. ANN methods explain why real search systems often prefer fast, good-enough candidates over exact answers that arrive too slowly. This concept connects vector search quality with latency, memory use, and service constraints.
- Related concepts: `nearest neighbor`, `search index`, `vector database`
- Core Section: `P1-13.4`
- Appears in: `P6-3.4`

<a id="application"></a>

## application

- Meaning: An application is the product layer through which users send requests and receive results. It includes input collection, output display, approval flows, error handling, logging, and the interaction design around a model.
- Why it matters: Users experience an AI service through the application, not through the model alone. The same model can feel reliable or confusing depending on the surrounding app flow. This concept helps readers see that product quality depends on interface design, workflow design, and operational controls as well as model capability.
- Related concepts: `model`, `tool`, `orchestration`, `agent`
- Core Section: `P1-14.1`
- Appears in: `P1-14.2`, `P1-14.3`

<a id="approval"></a>

## approval

- Meaning: Approval is the step that checks whether a person or policy allows an action before it is executed. Permission describes what may be possible; approval asks whether this specific action should proceed now.
- Why it matters: AI services can trigger actions that change files, send messages, make payments, or affect real users. Approval creates a control point before such actions occur. It helps balance automation speed with human oversight and makes the difference between capability and authorization explicit.
- Related concepts: `tool use`, `tool call`, `orchestration`, `permission`, `human oversight`
- Core Section: `P1-14.2`
- Appears in: `P6-15.2`, `P6-17.2`, `P7-6.2`

<a id="approval-policy"></a>

## approval policy

- Meaning: An approval policy defines which actions may run automatically, which require human approval, and which should be held or blocked. It is a reusable operating rule rather than a one-time yes-or-no decision.
- Why it matters: The risk of the same tool changes with context. Reading a file, modifying a file, running a test, and changing production state should not be governed by the same default. Approval policies keep automation consistent and make scope, logs, and hold states part of the system design.
- Related concepts: `approval`, `permission`, `scope`, `hold state`, `log`
- Core Section: `P7-6.3`
- Appears in: `P1-14.5`, `P7-6.1`, `P7-6.2`

<a id="argument"></a>

## argument

- Meaning: An argument is the actual value passed when a function is called. A parameter is the name in the function definition; an argument is the concrete value supplied at call time.
- Why it matters: Function definitions and function calls answer different questions. The definition says what the function expects, while the call shows what is being provided now. This distinction helps readers interpret examples, error messages, and why the same function can behave differently with different inputs.
- Related concepts: `parameter`, `function`, `return value`
- Core Section: `P2-8.5`
- Appears in: `P2-8.6`, `P2-10.3`

<a id="array"></a>

## array

- Meaning: An array is a structure that stores values so they can be read by position and index. In numerical computing it usually means a shaped block of values arranged along axes and processed together.
- Why it matters: Arrays are not only containers; they are computation shapes. Understanding arrays prepares readers for shape, axis, broadcasting, slicing, and vectorized operations. It also separates a simple list of values from data arranged so that whole groups of values can be computed at once.
- Related concepts: `table`, `index`, `data structure`
- Core Section: `P2-9.2`
- Appears in: `P2-11.1`, `P2-11.2`, `P2-12.1`

<a id="assignment"></a>

## assignment

- Meaning: Assignment connects a name to a value or object. It does not always create a new copy; often it makes a name refer to an existing object.
- Why it matters: In Python, misunderstanding assignment leads to confusion when mutable objects such as lists or dictionaries appear to change through more than one variable. Assignment is the starting point for understanding references, copying, object sharing, and why `=` in code is not the same as mathematical equality.
- Related concepts: `variable`, `reference`, `value`
- Core Section: `P2-8.7`
- Appears in: `P3-7.4`

<a id="attention"></a>

## Attention

- Meaning: Attention is a structure that lets a model weight different positions in an input sequence when producing an output. Instead of treating every input position equally, it gives more influence to the parts that are most relevant to the current computation.
- Why it matters: Attention reduces the bottleneck of compressing a long input into one fixed vector and marks a key transition toward Transformer-based models. It prepares readers for self-attention, multi-head attention, and long-context behavior by showing that a model can redistribute focus depending on the task.
- Related concepts: `Seq2Seq`, `Transformer`, `language modeling`, `self-attention`, `fixed-length vector`
- Core Section: `P1-11.2`
- Appears in: `P1-9.3`, `P5-12.2`, `P5-13.1`, `P5-13.2`, `P5-14.1`, `P5-14.2`

<a id="attribute"></a>

## attribute

- Meaning: An attribute is a value or state attached to an object, usually accessed with dot notation. For example, an expression such as `sample.text` reads information held by the object.
- Why it matters: Dot notation can mean different things. Some dotted names read attributes, while others call methods such as `model.fit()`. Understanding attributes helps readers separate stored information from executable behavior when reading object-oriented code and library documentation.
- Related concepts: `object`, `method`, `class`
- Core Section: `P2-8.6`
- Appears in: `P2-11.1`, `P2-12.1`

<a id="augmentation"></a>

## augmentation

- Meaning: In RAG, augmentation is the step that attaches retrieved material to the current input context so the model can use it when generating an answer. It is more than finding documents; it is arranging the found material as usable context.
- Why it matters: Retrieval alone does not guarantee a grounded answer. The quality of a RAG system depends on what is attached, how much is attached, and in what order or format it is placed in the prompt. Augmentation helps readers separate finding information from making that information available to generation.
- Related concepts: `retrieval-augmented generation`, `generation`, `prompt`
- Core Section: `P1-13.3`
- Appears in: `P1-14.1`

<a id="automatic-evaluation"></a>

## automatic evaluation

- Meaning: Automatic evaluation repeatedly checks outputs with programmatic rules or evaluation models when the criteria can be made explicit enough, such as format validity, basic scoring, or regression checks.
- Why it matters: Automatic evaluation is useful for comparing many candidates quickly and detecting regressions under the same rule. It does not replace human judgment for context, ambiguity, or user impact. The concept helps readers distinguish scalable repeated measurement from deeper interpretive review.
- Related concepts: `evaluation`, `human evaluation`, `regression`, `grader`
- Core Section: `P6-16.2`
- Appears in: `P6-17.1`

<a id="automatic-prompt-optimization"></a>

## automatic prompt optimization

- Meaning: Automatic prompt optimization treats prompt design as an iterative search problem. Candidate prompts are generated, tested across inputs, scored, compared, and refined under an evaluation loop.
- Why it matters: Prompt improvement does not have to rely only on manual wording intuition. This concept shows how prompt design can be connected to candidate generation, evaluation criteria, and selection. It also makes clear that finding a better prompt depends on defining what better means.
- Related concepts: `prompt engineering`, `evaluation`, `self-consistency`
- Core Section: `P6-10.3`

<a id="axes"></a>

## Axes

- Meaning: In Matplotlib, an Axes is the individual plotting area where data is drawn. Although the word looks plural, it usually refers to one graph panel inside a Figure.
- Why it matters: A Figure can contain several Axes, and plotting commands apply to a specific panel. Understanding Axes helps readers distinguish settings for the whole figure from settings for one plot, such as labels, lines, legends, and titles.
- Related concepts: `Figure`, `axis`, `plot`
- Core Section: `P2-13.1`
- Appears in: `P2-13.2`, `P2-13.3`

<a id="axis"></a>

## axis

- Meaning: An axis is the direction along which an array operation reads, groups, reduces, or selects values. It is not just a number; it defines the direction of interpretation inside an array.
- Why it matters: The same calculation can produce different shapes and meanings depending on which axis is reduced or preserved. Axis awareness prevents readers from mixing rows with columns, batches with features, or samples with channels. It turns array operations from memorized syntax into questions about direction and structure.
- Related concepts: `indexing`, `slicing`, `shape`
- Core Section: `P2-11.2`
- Appears in: `P2-11.3`, `P2-12.1`
