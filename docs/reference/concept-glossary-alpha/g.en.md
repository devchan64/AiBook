# Concept Glossary: G

This page lists English glossary entries for this letter directly. Each entry is written for English readers without sending them to another glossary page.

<a id="generalization"></a>

## generalization

- Meaning: Generalization is the state in which a model captures a relationship that still works reasonably well on data it did not see during training. It means the model has learned a broader pattern instead of merely memorizing the training examples.
- Why it matters: Generalization is the key difference between learning and memorization. It explains why validation and test data are needed even when training scores look good, and why overfitting and underfitting are both forms of generalization failure. Model performance is not just about fitting known examples; it is about holding up in similar new situations.
- Related concepts: `overfitting`, `underfitting`
- Core Section: `P1-3.2`
- Appears in: `P5-8.1`, `P5-8.2`

<a id="generation"></a>

## generation

- Meaning: Generation is the task of producing new text, images, speech, code, or other output from instructions, conditions, examples, and context. It is not choosing one item from a fixed list; it is building an output through a sequence of smaller choices.
- Why it matters: Generation separates generative AI from classification or ranking tasks. The quality of a generated result depends not only on a final choice, but also on context, sampling settings, and the sequence of intermediate decisions that form the output.
- Related concepts: `recommendation`, `ranking`, `large language model`, `sampling`, `next-output generation`
- Core Section: `P1-10.1`
- Appears in: `P1-1.2`, `P1-13.3`, `P5-15.1`, `P5-15.2`, `P5-15.3`

<a id="aigenerative-ai"></a>

## generative AI

- Meaning: Generative AI is the broad category of models and services that create new content such as text, images, audio, video, and code. It is defined by the character of the output, not by one specific model architecture.
- Why it matters: This concept keeps deep learning methods, LLM model families, and user-facing AI services from being collapsed into one vague idea. It also helps readers see why evaluating generated content requires different standards from evaluating a simple classification label.
- Related concepts: `generation`, `deep learning`, `large language model`
- Core Section: `P1-10.1`
- Appears in: `P1-1.3`

<a id="generative-model"></a>

## generative model

- Meaning: A generative model learns patterns or candidate distributions from data and can produce new samples or next outputs. It does more than map an input to a fixed label; it can draw an output from what it has learned about possible data.
- Why it matters: Generative models mark the shift from deciding what category is correct to producing something new. They require readers to consider diversity, consistency, conditioning, and distribution fit, not only accuracy.
- Related concepts: `generation`, `sampling`, `next-token prediction`
- Core Section: `P5-15.2`
- Appears in: `P5-15.1`, `P5-15.3`

<a id="git"></a>

## Git

- Meaning: Git is a distributed version-control tool that records and tracks changes, explanations, and history rather than simply storing the latest file. It lets each worker keep local history, compare states, and recover earlier versions.
- Why it matters: Projects that combine documents, code, images, and notes need to know what changed, when, and why. Git turns file management into change-history management, which is the foundation for review, collaboration, and deployment workflows.
- Related concepts: `version control`, `commit`, `repository`
- Core Section: `P2-14.1`
- Appears in: `P2-14.2`, `P2-15.2`

<a id="goal"></a>

## goal

- Meaning: A goal states the result to reach or the work to finish in a form that can guide action. It is more concrete than a broad wish because it helps decide when the current run can be considered complete.
- Why it matters: In agent execution, an unclear goal makes planning, tool choice, and stopping conditions unstable. A goal sets the boundary before detailed planning begins and separates the wider problem from what this execution should actually finish.
- Related concepts: `agent`, `state`, `stop condition`
- Core Section: `P1-14.3`
- Appears in: `P1-14.5`

<a id="good-enough-solution"></a>

## good-enough solution

- Meaning: A good-enough solution is an answer that is sufficient for the current purpose under limited time and resources. It is not necessarily a mathematically proven optimum; it is a practical stopping point.
- Why it matters: Real systems often cannot wait for a perfect answer. This concept explains why heuristics, search shortcuts, recommendation systems, and agents often prefer useful quality within time and cost limits over theoretical optimality.
- Related concepts: `heuristic`, `exhaustive search`, `optimization`
- Core Section: `P1-7.2`

<a id="gpt"></a>

## GPT

- Meaning: GPT is a family of language models based on Transformer decoders and pretrained to generate the next token from preceding context. It is best read as a generative model family that builds output one token at a time.
- Why it matters: GPT-style models form a direct lineage for much of the modern LLM user experience, including chat, code generation, summarization, and tool-using workflows. The concept also helps distinguish decoder-based generation from encoder-style representation models such as BERT.
- Related concepts: `decoder`, `pretraining`, `in-context learning`
- Core Section: `P6-5.1`
- Appears in: `P1-11.3`

<a id="gpugraphics-processing-unit"></a>

## GPU, graphics processing unit

- Meaning: A GPU is an accelerator designed to perform many similar numerical operations in parallel. Originally important for graphics, it became central to AI because neural-network training and inference rely heavily on repeated matrix and tensor computation.
- Why it matters: Deep learning became practical not only because of model ideas, but also because large-scale computation became available. GPUs explain why training time, experiment scale, cost, and feasible model size depend strongly on hardware.
- Related concepts: `parallel processing`, `batch`, `tensor`
- Core Section: `P5-9.1`

<a id="grader"></a>

## grader

- Meaning: A grader is an evaluation mechanism that judges results as scores, pass/fail outcomes, or criterion matches. It may be a human procedure, a rule-based checker, or another evaluation model, but the key is that the same judging process can be run repeatedly.
- Why it matters: Generative AI outputs often do not have a single fixed answer. Graders make comparison and regression checking possible by turning vague impressions into repeatable criteria. They also clarify what automatic evaluation can measure and what still needs human review.
- Related concepts: `evaluation`, `automatic evaluation`, `harness`, `reproducibility`
- Core Section: `P1-14.5`
- Appears in: `P1-14.6`

<a id="gradient"></a>

## gradient

- Meaning: A gradient is a vector of partial derivatives that shows how a value, usually loss, changes with respect to multiple parameters. It acts like a direction signal for how parameter changes would affect the loss.
- Why it matters: Gradients are the link between loss and learning. They explain why parameters are not changed randomly, but updated in directions that are expected to reduce loss. Without gradients, gradient descent and backpropagation cannot be read as concrete computation.
- Related concepts: `partial derivative`, `vector`, `training`
- Core Section: `P2-4.3`
- Appears in: `P2-4.4`, `P2-6.3`, `P5-5.1`, `P5-5.2`, `P5-6.1`, `P5-7.1`

<a id="gradient-boosting"></a>

## gradient boosting

- Meaning: Gradient boosting is an ensemble method that builds models sequentially so each new model corrects errors left by the previous ones. In practice, it often adds small decision trees step by step to reduce remaining residuals.
- Why it matters: Gradient boosting is a strong candidate for many tabular-data problems, but it is also sensitive to tuning and overfitting. It shows that ensembles can work by sequential correction, not only by training many independent models and averaging them.
- Related concepts: `ensemble`, `residual`, `hyperparameter`
- Core Section: `P4-16.1`
- Appears in: `P4-16.2`

<a id="gradient-descent"></a>

## gradient descent

- Meaning: Gradient descent is an iterative optimization method that changes parameters little by little in a direction expected to reduce loss. It does not solve for the best parameters at once; it repeatedly follows a local direction signal.
- Why it matters: Gradient descent shows how gradients become actual learning updates. It helps readers see training as movement across a loss landscape, where the model adjusts values step by step rather than discovering a final answer in one calculation.
- Related concepts: `gradient`, `optimization`, `learning rate`
- Core Section: `P2-6.3`
- Appears in: `P2-15.2`

<a id="graph"></a>

## graph

- Meaning: A graph represents objects as nodes and relationships as edges. Its focus is not only the properties of each item, but how items are connected.
- Why it matters: Some data is best understood by following relationships rather than reading rows in a table. Graphs support questions about neighbors, paths, dependencies, influence, and connection patterns. They change the unit of interpretation from isolated values to networks of relations.
- Related concepts: `node`, `edge`, `weight`
- Core Section: `P2-9.3`
- Appears in: `P2-9.2`, `P2-9.4`

<a id="graph-based-search"></a>

## graph-based search

- Meaning: Graph-based search stores nearby vectors or candidates as connected nodes and follows those connections to narrow the search. Instead of comparing everything every time, it moves through promising neighborhoods.
- Why it matters: This is a core intuition behind scalable approximate nearest-neighbor search. A search index is not just storage; it is a structure for reaching likely candidates faster than brute-force comparison.
- Related concepts: `graph`, `ANN, approximate nearest neighbor`, `search index`, `brute-force search`
- Core Section: `P1-13.4`
- Appears in: `P1-13.3`, `P6-3.4`, `P6-12.2`

<a id="groupby"></a>

## groupby

- Meaning: In Pandas, `groupby` first groups rows that share a category value and then calculates summaries such as counts or averages for each group. It changes table reading from row-by-row reading to group-by-group reading.
- Why it matters: Many patterns appear only after rows are grouped by customer, region, month, status, or another category. `groupby` is not just syntax for computing a mean; it is a choice about which groups should be compared and what question the table should answer.
- Related concepts: `aggregation`, `filtering`, `column`
- Core Section: `P2-12.2`
- Appears in: `P2-12.3`

<a id="gru-gated-recurrent-unit"></a>

## GRU, gated recurrent unit

- Meaning: A gated recurrent unit is a recurrent neural-network structure that uses gates to control how much information is kept and how much is updated. It is a simpler memory-control design than LSTM, while still aiming to handle sequence context more stably than a basic RNN.
- Why it matters: GRU shows that progress in sequence models was not only about adding more layers, but also about controlling memory and update behavior. It helps readers understand how recurrent models tried to reduce the difficulty of learning longer dependencies.
- Related concepts: `RNN, recurrent neural network`, `LSTM, long short-term memory`, `hidden state`
- Core Section: `P1-11.2`
- Appears in: `P5-12.1`
