# Table of Contents

> Section ID: `BOOK-toc`
> Version: `v2026.09.15`

This contents page lists available English manuscripts in the order of the Korean source. Sections without an English manuscript are omitted.

This document is the reader-facing table of contents for AiBook. Rather than listing files only, it gives a quick view of the relearning sequence from `Introduction to AI and the Landscape -> Foundational Recovery -> Data Modeling -> Machine Learning -> Deep Learning -> LLMs and Generative AI -> Projects`.

Here, `adopted` means that this sequence has been chosen as the book's reference structure. It does not mean that every chapter has already been fully written or finally verified. The main text may continue to be strengthened, but the learning dependencies among Parts and Chapters are tracked against this document.

## Quick Start

If you are reading for the first time, start with the [Introduction](index.md) to understand the book's purpose and reading path, then move through Part 1 in order. When a term becomes unclear, use the [Concept Glossary](reference/concept-glossary.md) to find the representative explanation location.

| Reader state | Recommended starting path |
| --- | --- |
| The overall AI flow feels unfamiliar | Introduction -> Part 1 -> Part 2 |
| Mathematics or Python feels rusty | Introduction -> Part 1 -> Part 2 -> Part 3 |
| AI tools are familiar but the internal structure is weak | Introduction -> Part 1 -> Part 3 -> Part 4 |
| LLM and generative-AI structure is the main interest | LLM preview in Part 1 -> Part 5 -> Part 6 |
| The goal is to validate learning through outputs | Check the needed concepts in Parts 1-6 -> Part 7 |

## Overall Flow

```mermaid
flowchart LR
  A[Introduction to AI and the Landscape]
  B[Foundational Recovery]
  C[Data Modeling]
  D[Machine Learning]
  E[Deep Learning]
  F[LLMs and Generative AI]
  G[Projects]

  A --> B --> C --> D --> E --> F --> G
```

This diagram shows the learning dependency structure in which earlier Parts become prerequisites for later Parts.

| Part | Core role | Question handed to the next Part |
| --- | --- | --- |
| Part 1. Introduction to AI and the Landscape | Establishes the scope and history of AI, the difference between rules and learning, and the basic vocabulary for the LLM user experience. | What foundations are needed to read AI model computation? |
| Part 2. Foundational Recovery | Restores mathematics, Python, data tools, and execution environments as languages for reading model computation. | How should raw data be turned into a learnable structure? |
| Part 3. Data Modeling | Reorganizes data into samples, features, baselines, and comparison structures. | What does a model learn from this structured data? |
| Part 4. Machine Learning | Reads problem setup, learning, validation, evaluation, and representative algorithms as one common structure. | How do neural networks extend this structure computationally? |
| Part 5. Deep Learning | Covers neural-network computation, backpropagation, CNNs, RNNs, attention, and Transformer structure. | How is this structure used in LLM and generative-AI services? |
| Part 6. LLMs and Generative AI | Connects tokens, prompts, generation settings, embeddings, retrieval, RAG, AI agents, and evaluation. | How can the learned material be validated and recorded in small projects? |
| Part 7. Projects | Combines questions, inputs, baselines, comparisons, execution logs, and operational reflection into one output. | What should be improved in the next iteration? |

## Notation

In public-facing explanation, the book is read as a `Part > Module > Chapter > Section` structure. The actual source tree uses a `Part > Chapter > Section` directory structure, and `Module` is an editorial unit that groups several Chapters into one reading flow.

This document uses the following notation so the tree structure remains visible.

- `## Part`: a major learning segment of the book
- `### Module`: a thematic grouping inside a Part
- `#### Chapter` or `#### Project`: an independent learning unit inside a Module. Part 7 may be described as `Project` because of its practical character, but the directory names still keep the `chapter-XX` format.
- Section item: the actual document unit to be written and maintained

Even if the same major concept appears again in multiple sections, the first section where it appears in the table of contents is often the representative detailed explanation for that Part. Later sections then reconnect that concept in a different problem scene or computational context.

## Part 1. Introduction to AI and the Landscape

Before going deeply into individual technologies, this Part rebuilds the large map of AI.

### Module 1. Scope and History of AI

#### Chapter 1. What Is AI `Concept Definition`

- **P1-1.1 Scope of the Word AI**: reduces confusion caused when the word AI is used too broadly
- **P1-1.2 Problems AI Handles**: reviews problem types such as recognition, search, prediction, and generation
- **P1-1.3 Relationship Among AI, Machine Learning, Deep Learning, and Generative AI**: fixes the place of terms that will keep returning later

#### Chapter 2. History of AI and Shifts in Paradigm `History and Paradigm`

- **P1-2.1 Symbolic AI and Rule-Based Approaches**: reviews the core thinking style and limits of early AI
- **P1-2.2 Search, Knowledge Representation, and Probabilistic Reasoning**: connects earlier flows for problem solving and uncertainty
- **P1-2.3 Flow Toward Machine Learning, Deep Learning, and Generative AI**: explains why data-centered approaches became central

### Module 2. Rules, Models, and Learning

#### Chapter 3. From Rules to Learning `History and Paradigm`

- **P1-3.1 Strengths and Limits of Rule-Based Systems**: organizes the advantages and tradeoffs of writing rules directly by hand
- **P1-3.2 What It Means to Learn Patterns from Data**: explains the key shift behind learning-based AI
- **P1-3.3 Rule-Based Approaches and Representation Learning**: separates rules, patterns, and representations

#### Chapter 4. Turning a Problem into a Model `Modeling Perspective`

- **P1-4.1 Becoming Comfortable with the Word Model**: treats the model as a simplified representation and distinguishes it from the real problem
- **P1-4.2 Input, Output, and Data**: fixes the starting point for turning a real problem into computational form
- **P1-4.3 Features, Representations, and Parameters**: reviews how data is handled inside a model
- **P1-4.4 How Problem Definition Determines the Model**: shows that good problem definition comes before a good model

#### Chapter 5. Learning and Inference `Learning Principles`

- **P1-5.1 What Does Learning Change?**: reviews what it means for parameters and representations to change during learning
- **P1-5.2 What Does Model Execution Run?**: separates the use of a trained model from the learning process
- **P1-5.3 Distinguishing Inference-Related Terms**: distinguishes `inference` from `reasoning`

### Module 3. Uncertainty and Problem Solving

#### Chapter 6. Uncertainty and Probabilistic Judgment `Mathematical Foundations`

- **P1-6.1 Problems with Incomplete Information and Many Exceptions**: explains lack of information, noise, and exception-heavy cases that rules alone cannot handle well
- **P1-6.2 Distinguishing Probability, Uncertainty, and Stochastic Processes**: separates commonly mixed expressions
- **P1-6.3 Where Probabilistic Judgment Is Used in AI**: reviews how probabilistic viewpoints appear in classification, prediction, and generation

#### Chapter 7. Search and Heuristics `Practical Heuristics`

- **P1-7.1 Search Space and Computational Limits**: explains why not every possible answer can be checked exhaustively
- **P1-7.2 What Does a Heuristic Reduce?**: reviews criteria that reduce time, computation, and candidate sets
- **P1-7.3 Difference Between Heuristics and Probabilistic Models**: keeps experience-based rules from being mixed with probability models
- **P1-7.4 Supplemental Learning: Route Finding to Autonomous-Driving Path Planning**: extends search and heuristics into a real planning case

#### Chapter 8. Basic Distinctions Among Learning Types `Learning Principles`

- **P1-8.1 Supervised Learning: Input and Label**: reviews learning from labeled data
- **P1-8.2 Unsupervised Learning: Structure and Representation**: reviews how structure is found without labels
- **P1-8.3 Reinforcement Learning: Action and Reward**: reviews learning through reward after action

### Module 4. Transition to Deep Learning and Generative AI

#### Chapter 9. Spread of the Deep-Learning Paradigm `History and Paradigm`

- **P1-9.1 Image Recognition and Representation Learning**: reviews how deep learning came to learn features directly
- **P1-9.2 Cases of Object Detection and Speech Generation**: treats YOLO and WaveNet as surrounding evidence for the spread of deep learning
- **P1-9.3 Direct Lineage and Surrounding Evidence for LLMs**: separates the spread of deep learning from the direct development line of LLMs

#### Chapter 10. Introduction to Generative AI `Concept Definition`

- **P1-10.1 Difference Among Classification, Prediction, and Generation**: reviews what makes generative AI different from earlier model uses
- **P1-10.2 Next-Output Generation Intuition**: builds a shared intuition across text, image, and speech generation
- **P1-10.3 Quality and Risk of Generated Outputs**: connects generation to hallucination, missing evidence, copyright, and safety

#### Chapter 11. Where Did LLMs Come From? `History and Paradigm`

This chapter is a short preview of the direct lineage of LLMs. The more detailed development history is revisited in the relevant chapters of Part 5 and Part 6.

- **P1-11.1 Statistical Language Models and Embeddings**: reviews the background before LLM-era language modeling
- **P1-11.2 RNN, Seq2Seq, and Attention**: fixes the transition points created by sequence data and translation research
- **P1-11.3 Transformers and Pretrained LLMs**: sketches the direct line that leads to current LLMs

### Module 5. Core Elements of the LLM User Experience

This Module fixes the basic vocabulary and large flow needed for LLM use. The fuller explanation of each topic continues in the relevant chapters of Part 6.

#### Chapter 12. Prompt Basics and the Feel of Using LLMs `LLM Core`

- **P1-12.1 What Does a Prompt Specify?**: builds the basic sense of giving instruction, condition, and context as input
- **P1-12.2 Instructions, Context, and Examples**: organizes the basic parts of a prompt
- **P1-12.3 Prompt Limits and Evaluation**: reviews what prompts cannot guarantee and how to check them early

#### Chapter 13. Embeddings and Vector Search `LLM Core`

- **P1-13.1 What It Means to Represent Text as Vectors**: builds the intuition of placing meaning in numerical space
- **P1-13.2 Similarity Search Intuition**: reviews the idea and limits of finding nearby vectors
- **P1-13.3 Flow Leading into RAG**: explains why search results need to be connected to LLM input
- **P1-13.4 Vector Search Implementation Intuition**: lightly connects vector databases, indexes, and graph-based approximate search

#### Chapter 14. AI Service Architecture and Execution Environments `Service Structure`

- **P1-14.1 Model, Application, Data, and Tool**: separates the major components of an AI service
- **P1-14.2 Place of RAG and Tool Use**: reviews why external material and tool calls become necessary
- **P1-14.3 Agent: A Structure That Carries a Goal Through a Workflow**: reviews the large picture in which a model links multi-step work and tool use
- **P1-14.4 MCP and the Standardization of Tool Connections**: fixes the interface flow through which agents connect to outside tools and data
- **P1-14.5 Harness and the Evaluation Execution Environment**: previews the surrounding structures for execution, logging, testing, evaluation, and reproducibility
- **P1-14.6 Constraints AI Services Meet in Real World**: surveys cost, latency, usage limits, and failure response

### Module 6. Social Issues and Application

#### Chapter 15. AI Ethics, Copyright, and Security `Law and Policy`

- **P1-15.1 Bias, Safety, and Accountability**: reviews the social responsibility that follows AI outputs
- **P1-15.2 Copyright and Training Data**: fixes the review points around Korean publications and training-data controversy
- **P1-15.3 Security and Privacy**: reviews risks around input data, output results, and service operation

#### Chapter 16. Cases of Practical Application `Project Practice`

- **P1-16.1 Personal Learning and Documentation**: uses the book itself as one practical application case
- **P1-16.2 Work Automation and Search**: reviews cases of repetitive work, document retrieval, and summarization
- **P1-16.3 How to Validate with a Project**: organizes ways to check understanding through small outputs

#### Chapter 17. The Future of AI `Forecasting`

- **P1-17.1 What Evidence Should Forecasts Rely On?**: fixes the evidence standard needed for predictive writing
- **P1-17.2 Reading News, Columns, and Reports**: reviews how to compare date-sensitive external sources
- **P1-17.3 Distinguishing Prediction from a Working Hypothesis**: keeps personal interpretation from being written as if it were established fact

## Part 2. Foundational Recovery

This Part restores the minimum foundations needed to read AI model computation and reproduce small examples in code, rather than proving mathematics in full depth. Instead of memorizing mathematical notation, Python runtime setup, data tools, and visualization separately, it reconnects them as shared foundations for moving into Part 3 data modeling and Part 4 machine learning.

### Module 1. Reading Mathematics Again as a Computational Language

#### Chapter 1. Why Mathematics Is Needed in AI `Mathematical Foundations`

- **P2-1.1 What Math Does in AI Computation**: introduces mathematics as the language for reading model computation rather than only as a subject of proof
- **P2-1.2 Translating Formulas into Code to Calculate with Data**: translates the mean formula into Python code and examines data shape and the meaning of the result

#### Chapter 2. Reading Mathematical Notation Again `Mathematical Foundations`

- **P2-2.1 Reading Variables, Functions, and Expressions Again**: restores basic notation for reading AI documents
- **P2-2.2 Sigma and Repeated Computation**: reviews how summation appears in grouped data, averages, and loss calculation
- **P2-2.3 Limits and the Intuition of Change**: rebuilds limits more as intuition for change, approximation, and derivatives than as a formal proof topic
- **P2-2.4 Why Do Log and Exp Keep Reappearing?**: rebuilds logarithms and exponentials as computational language before reading log loss, sigmoid, and softmax

### Module 2. Core Mathematics for Reading Model Computation

#### Chapter 3. What Linear Algebra Models `Mathematical Foundations`

- **P2-3.1 Scalar, Vector, and Matrix**: fixes the basic representations in which data becomes numbers, lists, and tables
- **P2-3.2 Vector Space and the Intuition of Position**: builds the minimum intuition needed for embeddings and feature representation
- **P2-3.3 What Does Matrix Multiplication Reuse?**: reviews the meaning of linear transformation and batch calculation from a code perspective
- **P2-3.4 Dot Product, Norm, Distance, and Similarity**: restores vector comparison criteria before k-NN, embeddings, and vector search
- **P2-3.5 Python Runtime Environments: Colab and Local PC**: separates browser-based Colab from terminal execution on a personal machine
- **P2-3.6 Checking Linear Algebra with NumPy**: reproduces vectors, matrices, and matrix multiplication in small code

#### Chapter 4. What Derivatives Are a Tool for Finding `Mathematical Foundations`

- **P2-4.1 Revisiting How We Learned Differentiation**: pulls older memories of tangents, instantaneous rate of change, speed, and accumulation back into current learning questions
- **P2-4.2 Rate of Change and Slope**: introduces derivatives as a tool for reading how a function changes
- **P2-4.3 Derivative and Gradient**: reviews the minimum concept needed for finding directions that reduce loss
- **P2-4.4 Why Learning Needs Differentiation**: keeps only the connections needed before moving into optimization and backpropagation
- **P2-4.5 Gradient Supplement: from School Differentiation to Multivariable Differentiation**: Compares directional rates of change and gradient vector fields, distinguishing an instantaneous tangent-direction rate from the actual change.
- **P2-4.6 Composite Functions and the Chain Rule**: restores how rates of change are passed along when functions are connected through multiple steps before reading backpropagation

#### Chapter 5. Why Probability and Statistics Are Needed `Mathematical Foundations`

- **P2-5.1 How Probability Represents Uncertainty as Numbers**: rebuilds probability as a numerical language for unknown states
- **P2-5.2 Distribution, Mean, and Variance**: reviews the basic tools for summarizing the shape of grouped data
- **P2-5.3 Sample, Estimation, and Error**: reviews what statistics estimates from data
- **P2-5.4 Checking Probability and Statistics with Small Data**: checks mean, variance, and distribution through code and charts
- **P2-5.5 Supplementary Learning: Reading Standard Deviation, Correlation, and Confidence Intervals**: adds the minimum interpretation standard for statistical terms that often return

#### Chapter 6. What Kind of Problem Optimization Solves `Learning Principles`

- **P2-6.1 What Does Optimization Search for?**: explains optimization as a search for better values rather than directly writing the right answer
- **P2-6.2 Loss Functions and Objective Functions**: reviews the criteria that express what a model tries to reduce or increase
- **P2-6.3 The Intuition of Gradient Descent**: fixes the iterative flow of adjusting values without deep formal proof

### Module 3. Runtime Environment and Python Fundamentals

#### Chapter 7. Setting Up the Learning Environment `Software Tools`

- **P2-7.1 Local Environment and Runtime**: fixes where code runs and how a local machine differs from an outside runtime
- **P2-7.2 Terminal, Shell, and Working Directory**: explains where commands are typed and why current location matters
- **P2-7.3 Python Interpreter and Script**: reviews how Python code runs and how file execution differs from interactive execution
- **P2-7.4 Virtual Environments and Packages**: reviews project-specific execution spaces and how packages such as NumPy and Pandas fit into them
- **P2-7.5 Dependency and Reproducibility**: organizes what is needed to rerun the same exercise on another machine
- **P2-7.6 Supplemental Learning: Opening Terminals by Operating System**: separately organizes how to open terminals, the basic differences in commands, and what to check before exercises
- **P2-7.7 Supplemental Learning: When Is Python Installation Needed?**: explains when local Python installation is needed after beginning with Colab
- **P2-7.8 Supplementary Learning: Reading Shell Execution Flow**: supplements shell syntax that appears often during terminal practice
- **P2-7.9 Supplementary Learning: Checking Local Python Environment Problems**: organizes what to inspect first when installation and execution do not line up

#### Chapter 8. Review of Core Python Syntax `Software Tools`

- **P2-8.1 Values, Variables, and Types**: restores Python syntax only to the degree needed for mathematical computation and data handling
- **P2-8.2 Lists: Ordered Groups of Values**: checks ordered data groups and list initialization patterns
- **P2-8.3 Dictionaries: Structures That Find Values by Key**: reviews key-value mapping and frequently used map patterns in practice
- **P2-8.4 Loops: Processing Iterables One by One**: separates item iteration, index iteration, key-value iteration, and filtering iteration
- **P2-8.5 Functions and Small Reuse**: reviews how mathematical functions and Python functions are similar and different
- **P2-8.6 Supplemental Learning: First Meeting Classes and Objects**: slowly reads objects, classes, methods, `self`, and library calls such as `model.fit()`
- **P2-8.7 Supplemental Learning: Distinguishing References and Copies**: adds the minimum standard for avoiding confusion when values change together

#### Chapter 9. Intuition for Data Structures and Graphs `Software Tools`

- **P2-9.1 Why Are Data Structures Needed?**: reviews how the shape in which data is stored affects the way it is computed
- **P2-9.2 Intuition of Arrays, Tables, Trees, and Graphs**: lightly separates structures that appear often in AI and search
- **P2-9.3 How Does a Graph Represent Relationships?**: builds the minimum intuition of representing relations through nodes and edges
- **P2-9.4 Supplemental Learning: How to First Read Traditional Data Structure Names**: scans arrays, linked lists, stacks, queues, trees, graphs, and hash tables through reasoning flow rather than implementation detail

#### Chapter 10. Jupyter and Colab Notebooks `Software Tools`

- **P2-10.1 Why Are Notebooks Useful for Learning?**: reviews the strengths and tradeoffs of keeping code, results, and explanation together
- **P2-10.2 Difference Among Jupyter, Colab, and Local Execution**: organizes differences in execution location, file access, and practice records
- **P2-10.3 Organizing Notebooks as Re-runnable Records**: organizes execution order, dependency handling, data preparation, and sharing caution

### Module 4. Data Computation and Visualization Tools

#### Chapter 11. Reusing Vectors and Matrices with NumPy `Software Tools`

- **P2-11.1 Building Vectors and Matrices with NumPy Arrays**: reproduces linear-algebra notation in actual array computation
- **P2-11.2 Indexing, Slicing, and Axis**: builds the basic sense of reading position and direction in arrays
- **P2-11.3 Broadcasting and Vectorization**: reviews how to compute at the array level instead of with explicit loops
- **P2-11.4 Supplemental: How to Read Shape and Shared Origins Together in NumPy**: adds why view/copy, `shape`, and `newaxis` are easily confused together

#### Chapter 12. Handling Data Structure with Pandas `Software Tools`

- **P2-12.1 What Does a Pandas DataFrame Represent?**: reviews how tabular data is organized by rows, columns, and index
- **P2-12.2 Selection, Filtering, and Aggregation**: restores repeated operations used in data analysis
- **P2-12.3 Intuition of Preparing a Learning Dataset**: reviews why data has to be cleaned and separated before model training

#### Chapter 13. Visualizing Concepts with Matplotlib `Software Tools`

- **P2-13.1 What Does a Plot Reveal?**: checks visually visible patterns that do not stand out from a numeric table alone
- **P2-13.2 Basic Charts and Checking the Shape of Formulas**: uses line charts, scatter plots, and histograms to inspect functions, distributions, and loss changes
- **P2-13.3 Comparing and Saving Multiple Plots**: reviews the flow of arranging multiple axes and saving results to files

### Module 5. Reproducibility and Integrated Review

#### Chapter 14. Git and Document Management `Software Tools`

- **P2-14.1 Git as a Tool for Managing Change History**: fixes the basic idea of tracking changes in learning documents and code
- **P2-14.2 Branches, Commits, and Document Reproducibility**: connects the book's dev/main workflow to the management of drafts and supporting material

#### Chapter 15. Reading Mathematics Again Through Software `Project Practice`

- **P2-15.1 A Small Procedure for Translating Formulas into Code**: organizes the order for moving one mathematical expression into Python computation
- **P2-15.2 Final Check Before Moving to Part 3**: checks the mathematical and software sense needed before data modeling

## Part 3. Data Modeling

This Part deals with rebuilding raw data into comparable samples and table structure instead of putting it directly into a model. It also notes that in front of data modeling there is a broader flow of data-centered systems such as `DSS/BI/DW/OLAP`, which connect collected data to decision-making. Part 2 and Part 3 together form the foundational checkpoint zone of the book. Part 3 acts as a `data-science foundations supplement for Part 4, Part 5, and Part 6`, fixing storage structure, sample units, event data and time records, baseline comparison, feature design, and interpretation boundaries before later Parts recover those ideas in fuller technical form.

### Module 1. Roles and Problem Scenes

#### Chapter 1. What Data Modeling Tries to Achieve and How It Proceeds `Modeling Perspective`

- **P3-1.1 What Is Data Modeling Trying to Achieve**: fixes how raw data has to be redesigned into samples, features, comparisons, and output structure
- **P3-1.2 In What Sequence Does Data Modeling Proceed**: reviews the basic order of fixing question, sample, table, feature, baseline, and output structure
- **P3-1.3 How Should a Data Question Be Written So the Problem Structure Appears Before the Model**: organizes how to write question sentences that reveal sample unit, comparison standard, and result form first

#### Chapter 2. Reading Storage Structure and Design Axes First `Modeling Perspective`

- **P3-2.1 Why Are Stored Records Not Yet a Dataset**: reviews why storage structure alone is not yet a comparable dataset
- **P3-2.2 What Structures Go Inside a Dataset Candidate**: reviews how samples, features, baselines, and output structure are bundled together
- **P3-2.3 What Should Be Written Down First When a New Table Arrives**: organizes table-reading notes that first check row meaning, identifiers, time or order columns, and comparability

#### Chapter 3. A Dataset Is Not Given from the Beginning `Modeling Perspective`

- **P3-3.1 Why Source Data Should Not Be Read as a Learning Problem Right Away**: organizes the questions that disappear when record structure is mistaken for learning structure
- **P3-3.2 How Should a Dataset Be Redesigned to Match the Question**: reviews that a dataset is a reconstructed structure aligned to the question
- **P3-3.3 Which Columns Should Be Sketched First to Move a Question into the First Table Draft**: organizes how to sketch identifier, feature-candidate, comparison, and result columns

### Module 2. Samples and Table Structure

#### Chapter 4. How to Determine the Sample Unit `Modeling Perspective`

- **P3-4.1 How Do We Decide One Comparable Sample**: distinguishes one row from one sample and fixes the unit of comparison
- **P3-4.2 What Else Starts to Drift When the Sample Unit Drifts**: shows that features, labels, and evaluation also depend on the sample unit
- **P3-4.3 How Are One Row, One Sample, and One Recent Segment Different**: separates time records, one event, and one recent aggregated window to reduce level confusion
- **P3-4.4 What Signals Show That the Sample Unit Was Chosen Wrong**: checks warning signs such as repeated labels, unexplained features, and awkward review sentences
- **P3-4.5 How Well Does the Sample Set We Collected Represent the Overall Operating Situation**: organizes how representativeness can still be weak even when the sample unit itself is correct

#### Chapter 5. How to Turn Raw Logs into Summary Tables `Modeling Perspective`

- **P3-5.1 How Do We Turn Raw Logs into Comparable Tables**: reviews the procedure that moves from raw logs to summary and aggregated tables
- **P3-5.2 How Does a Summary Table Preserve Patterns Beyond the Average**: reviews how differences hidden by averages can still be preserved
- **P3-5.3 Why Can We Not Immediately Call Raw Time Series a Learning Input**: organizes the difference between raw time series and learning inputs and how input boundaries are decided
- **P3-5.4 Where Do We Cut the Input Window and How Do We Align Its Length**: reviews how start point, end point, length, and alignment are fixed against the problem question
- **P3-5.5 How Do We Handle Samples with Missing Values or Empty Segments**: organizes how to distinguish partial missing values, missing segments, and collapsed sample boundaries
- **P3-5.6 Overlapping Input Windows and Sample Counts**: distinguishes number of windows from number of source events
- **P3-5.7 Rules for Folding Multiple Follow-Up Events**: reviews how rules such as `any`, `first`, `worst`, and `count` change the meaning of the result table

### Module 3. Features and Comparison Structure

#### Chapter 6. How to Design Features and Intermediate Representations `Modeling Perspective`

- **P3-6.1 What Features Should We Keep to Represent a Structure for Comparison**: reviews what should be preserved through numerical features such as mean, slope, and variability
- **P3-6.2 What Intermediate Representations Can We Add When Features Alone Are Not Enough**: reviews how far segment representation and tokenization need to go
- **P3-6.3 How Should We Distinguish Human-Made Features from Representations Learned by the Model**: organizes the connection and boundary between feature design and representation learning
- **P3-6.4 Why Not Every Column in a Summary Table Is a Feature**: organizes how to read columns as feature, comparison, result candidate, identifier, or context
- **P3-6.5 How Should We Read and Keep Features Together When Their Units and Scales Differ**: reviews how numeric values should be interpreted through unit, role, and comparison standard rather than absolute size alone
- **P3-6.6 Same Column Name, Different Feature**: organizes how changes in unit, sensor version, calculation rule, or operational definition alter feature meaning

#### Chapter 7. How to Read Baseline Comparison Structure `Modeling Perspective`

- **P3-7.1 What Should We Compare the Structure We Kept Against So That Change Becomes Visible**: reviews that a baseline is itself part of comparison structure
- **P3-7.2 How Should We Read a Comparison Table as a Human Review Sentence**: reviews the order for turning recent-window vs baseline comparisons into review language
- **P3-7.3 What Is a Baseline the Reference For**: separates a data comparison reference from a model evaluation reference
- **P3-7.4 By What Range and Conditions Should We Set the Baseline**: organizes how to choose a baseline with matched sample unit, operating condition, and sample size
- **P3-7.5 Should a Baseline Stay Fixed, or Should It Be Updated as a Recent-Usual Reference**: organizes which questions fit a fixed baseline and which fit a recent-normal baseline better

### Module 4. Boundaries of Interpretation

#### Chapter 8. How to Read Sample Size and Repeatability `Modeling Perspective`

- **P3-8.1 What Controls Interpretation Strength**: reviews how strongly to speak depending on sample size and repeatability
- **P3-8.2 How Far Should You Describe a Change Signal, and Where Should You Stop on Cause**: reviews the boundary between change signal and confirmed cause
- **P3-8.3 In What Order and With What Wording Should Conservative Interpretation Sentences Be Written**: organizes sentence templates for comparison result, strength condition, and next action
- **P3-8.4 Conservative Interpretation and Operational Columns**: reviews how language turns into structured operational outputs such as `warning_level`, `review_needed`, and `priority_score`
- **P3-8.5 How Are Multiple Comparison Columns Grouped into One Review-Priority Candidate**: organizes how change magnitude, repeatability, interpretation confidence, and operational importance are combined
- **P3-8.6 Confirmed Labels Left Only on Some Cases**: reviews how to record review route and skew so selectively assigned labels are not mistaken for full-population truth
- **P3-8.7 Data Interpretation Changed by Operational Intervention**: organizes the interpretation boundary needed to separate post-intervention data from natural progression

### Module 5. Problem Type and Connection to Later Parts

#### Chapter 9. Which Problems Should Be Turned into Prediction Problems `Modeling Perspective`

- **P3-9.1 How Far Should the Current Problem Be Raised**: distinguishes warning, review-candidate, and target-label-candidate levels
- **P3-9.2 Why Should Some Problems Remain Comparison Reports All the Way Through**: reviews when a comparison report is more appropriate than prediction
- **P3-9.3 Differences Among Three Operational Tables**: reviews how the same data branches into three output forms
- **P3-9.4 How Do Review Results Turn from Review Notes into Target Candidates**: organizes how review notes and operational judgments accumulate into more stable target candidates
- **P3-9.5 By What Is the Same Event Continuously Tracked Across Multiple Outputs**: organizes why consistent sample identifiers and minimal evidence must remain even when outputs differ
- **P3-9.6 Checking Label Consistency**: reviews why label consistency must be checked before target candidates are trusted
- **P3-9.7 Under What Conditions Can Inputs and Results Be Read as a Prediction Problem**: organizes input/output separation, leakage prevention, operational-time reproducibility, cutoff, and horizon
- **P3-9.8 What Does One Prediction Actually Decide, and Why Are Scores and Policy Different**: separates prediction unit, model output, operational policy, and real action
- **P3-9.9 How Should the Actual Target and a Proxy Target Be Distinguished**: reviews whether the current target is a true objective or a substitute field
- **P3-9.10 Delayed Label Confirmation and Incomplete Negatives**: organizes how to record label-confirmation delay separately from incomplete negative observation
- **P3-9.11 Target Candidates and Changing Criteria**: reviews why the representative target and definition version must be fixed first
- **P3-9.12 Target Names and Error Costs**: explains why the operating cost difference between false negatives and false positives should be fixed early
- **P3-9.13 Problem Boundaries to Hand Off to Part 4**: fixes only the names and need of evaluation and problem-type topics that will be recovered later

## Part 4. Machine Learning

This Part rebuilds what it means to learn rules from data. It fixes data splits, evaluation, generalization, and overfitting before moving into algorithm lists.

### Module 1. The Place of Machine Learning

#### Chapter 1. Distinguishing AI, Machine Learning, and Deep Learning `Concept Definition`

- **P4-1.1 The Relationship Among AI, Machine Learning, and Deep Learning**: reconnects the map from Part 1 to machine-learning study
- **P4-1.2 What It Means To Learn Rules From Data**: organizes the difference between writing rules and learning-based approaches in machine-learning terms

#### Chapter 2. Supervised, Unsupervised, and Reinforcement Learning `Learning Principles`

- **P4-2.1 Supervised Learning**: reviews the basic problem of learning the relation between input and label
- **P4-2.2 Unsupervised Learning**: reviews the problem of finding structure without labels
- **P4-2.3 Reinforcement Learning**: reviews the problem of learning a policy from action and reward

#### Chapter 3. Why Heuristics Are Needed `Practical Heuristics`

- **P4-3.1 Why Heuristics Are Needed**: reviews situations where practical criteria matter more than exact optimality
- **P4-3.2 Heuristics And Model Selection**: reviews how experience-based rules can be treated as checkable starting points

### Module 2. Data and Evaluation

#### Chapter 4. Data Splitting and Validation `Learning Principles`

- **P4-4.1 Training Data And Evaluation Data**: explains why data needs to be separated
- **P4-4.2 Validation And Test**: separates model selection from final confirmation

#### Chapter 5. Overfitting and Generalization `Learning Principles`

- **P4-5.1 Overfitting And Underfitting**: reviews models that fit too much or too little
- **P4-5.2 Generalization**: organizes what it means to work well on unseen data

#### Chapter 6. Evaluation Metrics `Learning Principles`

- **P4-6.1 The Role Of Evaluation Metrics**: fixes what accuracy, precision, recall, and related metrics are looking at
- **P4-6.2 Evaluation Criteria By Problem Type**: reviews why evaluation changes across classification, regression, and clustering
- **P4-6.3 Supplementary Learning: How To Read Metrics In Site Reliability Engineering**: supplements how machine-learning metrics differ from operational metrics
- **P4-6.4 Supplementary Learning: A Question Map for Evaluation Metrics**: separates frequently seen but unfamiliar metrics in one large view

### Module 3. Practical Heuristics

#### Chapter 7. Heuristics for Feature Selection and Preprocessing `Practical Heuristics`

- **P4-7.1 Feature Selection**: reviews how to choose which inputs to feed into a model
- **P4-7.2 Preprocessing**: reviews the basic decisions around missing values, scaling, and categorical data
- **P4-7.3 Supplementary Learning: Separating Preprocessing Input Problems**: adds a beginner bridge for splitting preprocessing by the kind of input problem
- **P4-7.4 Supplementary Learning: Distinguishing Feature Selection Methods**: adds criteria for not mixing feature selection with dimensionality reduction

#### Chapter 8. Heuristics for Model Selection `Practical Heuristics`

- **P4-8.1 Model Selection**: reviews how to narrow model candidates according to problem and data
- **P4-8.2 Baseline**: reviews why comparison standards should be set before complex models
- **P4-8.3 Supplementary Learning: How To First Set A Baseline By Problem Type**: reviews the procedure and examples for building representative baselines in classification, regression, and time series

#### Chapter 9. Hyperparameter Tuning `Practical Heuristics`

- **P4-9.1 Hyperparameters**: distinguishes settings that do not change through learning
- **P4-9.2 Tuning And Validation Cost**: reviews the balance between performance improvement and computation cost
- **P4-9.3 Supplementary Learning: Tool Map After Model Selection**: supplements the place of automated tuning and experiment-management tools

### Module 4. Basic Algorithms

#### Chapter 10. Linear Regression `Algorithms`

- **P4-10.1 Intuition For Linear Regression**: reviews the most basic model for predicting continuous values
- **P4-10.2 Evaluation And Limits Of Linear Regression**: reviews residuals, error, and the limits of linear assumptions
- **P4-10.3 Supplementary Learning: How To First Read Regression Diagnostics**: adds the minimum standard for first reading residual patterns and assumption checks

#### Chapter 11. Logistic Regression `Algorithms`

- **P4-11.1 Intuition For Logistic Regression**: reviews outputs that are interpreted like probabilities in classification
- **P4-11.2 Decision Boundary**: reviews the perspective that classification models create boundaries
- **P4-11.3 Supplementary Learning: How To Read Log-Odds And MLE For The First Time**: strengthens why probability interpretation and the learning objective appear together in the same chapter
- **P4-11.4 Supplementary Learning: How To Read Multinomial Logistic Regression**: reviews how binary-class intuition extends into multiclass probability comparison
- **P4-11.5 Supplementary Learning: How To Read Solver And Regularization For The First Time**: reviews why learning computation and regularization settings should be recorded together even within the same logistic-regression family

#### Chapter 12. k-NN `Algorithms`

- **P4-12.1 Intuition For k-NN**: reviews how nearby data influences a judgment
- **P4-12.2 Distance And Scale**: reviews the problems that arise when defining closeness
- **P4-12.3 What Should Be Checked First When Using k-NN?**: organizes whether to revisit the distance rule, `k`, or the data representation first

#### Chapter 13. SVM `Algorithms`

- **P4-13.1 Intuition For SVM**: understands classification through boundaries and margins
- **P4-13.2 Introductory Meaning Of The Kernel**: lightly reviews the idea behind nonlinear boundaries

### Module 5. Trees and Ensembles

#### Chapter 14. Decision Trees `Algorithms`

- **P4-14.1 Decision Tree**: reviews a model that predicts by splitting through questions
- **P4-14.2 Overfitting In Trees**: reviews the problem that emerges when branches grow too deep

#### Chapter 15. Random Forests `Algorithms`

- **P4-15.1 Random Forest**: reviews how combining many trees improves stability
- **P4-15.2 Feature Importance**: reviews an introductory perspective on model interpretation
- **P4-15.3 OOB(Out-Of-Bag) And Checking Random Forest**: reviews the basic habit of reading train, OOB, and test together
- **P4-15.4 Supplementary Learning: Comparing Extra Trees and Random Forest**: compares split randomization, bootstrap defaults, and the conditions under which OOB checks are available within the forest family

#### Chapter 16. Gradient Boosting `Algorithms`

- **P4-16.1 Gradient Boosting**: reviews the flow of strengthening weak models sequentially
- **P4-16.2 Performance And Risk In Boosting**: reviews strong performance alongside tuning sensitivity
- **P4-16.3 Supplementary Learning: Boosting Libraries And Operational Feel**: reviews how XGBoost, LightGBM, CatBoost, GPUs, and automation are first read together from implementation and operational viewpoints

### Module 6. Finding Structure

#### Chapter 17. Clustering `Algorithms`

- **P4-17.1 Intuition For Clustering**: reviews the problem of grouping similar data
- **P4-17.2 Cautions When Interpreting Clustering Results**: organizes why a cluster is not itself a ground-truth label
- **P4-17.3 Supplementary Learning: Hierarchical and Spectral Clustering**: rebinds different clustering intuitions such as center, density, order, and connectivity
- **P4-17.4 Supplementary Learning: How To Connect Clustering And Semi-Supervised Learning For The First Time**: supplements a standard for reading clusters as label hypotheses and review priority rather than automatic labels

#### Chapter 18. Dimensionality Reduction `Algorithms`

- **P4-18.1 Dimensionality Reduction**: reviews why many features are reduced into fewer axes
- **P4-18.2 Visualization And Information Loss**: reviews readable diagrams together with the loss of original information

#### Chapter 19. Reinforcement-Learning Algorithms `Algorithms`

- **P4-19.1 Value-Based Reinforcement Learning**: reviews how Q-learning and SARSA learn the value of states and actions
- **P4-19.2 Policy-Based Reinforcement Learning**: reviews how policy gradients and actor-critic approaches directly adjust the policy
- **P4-19.3 Caution In Applying Reinforcement Learning**: organizes reward design, exploration cost, and the difference between simulation and reality
- **P4-19.4 Supplementary Learning: A Map of Later Reinforcement-Learning Branches**: reorganizes representative RL families in one larger flow
- **P4-19.5 Supplementary Learning: First Reading of Reinforcement-Learning Formula Names**: connects the recursive value equation of value-based reinforcement learning to the background of scaling into large state spaces
- **P4-19.6 Supplementary Learning: First Reading of Policy Gradient**: first connects why policy-based formulas are written in the form of log-probability gradients

## Part 5. Deep Learning

This Part explains how neural networks represent and learn from data. It follows the flow from perceptrons to backpropagation, optimization, representation learning, CNNs, RNNs, Transformers, and generative models.

### Module 1. Starting Point of Neural Networks

#### Chapter 1. The Perceptron `Deep-Learning Structures`

- **P5-1.1 Intuition for the Perceptron**: reviews the simplest flow of input, weight, and output
- **P5-1.2 Linear Combination and Activation**: reviews how a perceptron creates a decision boundary

#### Chapter 2. Multilayer Neural Networks `Deep-Learning Structures`

- **P5-2.1 Multilayer Neural Networks**: reviews why several layers are stacked
- **P5-2.2 Hidden Layers and Representation**: builds the intuition that intermediate representations arise

### Module 2. Output, Loss, and Backpropagation

#### Chapter 3. Activation Functions `Deep-Learning Structures`

- **P5-3.1 Activation Functions**: reviews why nonlinearity is needed
- **P5-3.2 Sigmoid**: reviews the formula and intuition for compressing scores into the 0-to-1 range
- **P5-3.3 Tanh**: reviews zero-centered representations between -1 and 1
- **P5-3.4 ReLU**: reviews negative-value cutoff and positive-value pass-through
- **P5-3.5 Formula Comparison of Representative Activation Functions**: compares sigmoid, tanh, and ReLU formulas and output ranges side by side
- **P5-3.6 Choosing Output Layers and Activation**: reviews why the interpretation of the last output changes by problem type

#### Chapter 4. Loss Functions `Learning Principles`

- **P5-4.1 Loss Functions**: reviews the criteria that express model error numerically
- **P5-4.2 Loss By Problem Type**: reviews why loss differs across regression, classification, and generation

#### Chapter 5. Backpropagation `Deep-Learning Structures`

- **P5-5.1 How Does Loss Become a Gradient Signal**: reviews the flow in which error is passed backward through earlier weights
- **P5-5.2 Computation Graphs**: understands complicated differentiation as a flow of computation

### Module 3. Learning Loops and Stabilization

#### Chapter 6. Separating Learning and Inference `Learning Principles`

- **P5-6.1 The Four Steps of the Training Loop**: separates the stage that changes parameters from the stage that uses them
- **P5-6.2 Training Step, Batch, Epoch**: separates the repetition units that make the training loop run on real data
- **P5-6.3 Learning and Model Execution (Inference)**: separates the stage that changes parameters from the stage that uses them
- **P5-6.4 Training Mode and Evaluation Mode**: prepares the reader to later understand differences such as dropout and batch normalization

#### Chapter 7. Optimizers `Learning Principles`

- **P5-7.1 The Role of the Optimizer**: explains where gradients become actual parameter updates
- **P5-7.2 Learning Rate and Update Step Size**: explains why the same gradient can lead to updates that are too small or too large
- **P5-7.3 Intuition for Adaptive Updates: Adam as an Example**: explains how Adam adds adaptive update behavior on top of a simple update baseline
- **P5-7.4 Supplementary Reading: Distinguishing Adaptive Optimization Claims**: separates convergence guarantees from practical performance claims
- **P5-7.5 Supplementary Reading: Major Optimizer Families**: Compares what momentum, AdaGrad, RMSProp, and Adam remember and adjust.
- **P5-7.6 Supplementary Reading: Learning-Rate Control Strategies**: Explains why warmup and decay adjust the learning rate over time.
- **P5-7.7 Supplementary Reading: Optimizer State and Per-Parameter Updates**: Separates parameters, gradients, updates, and optimizer state.
- **P5-7.8 Supplementary Reading: Gradient Clipping and Unstable Updates**: Distinguishes gradient clipping from learning-rate adjustment.

#### Chapter 8. Regularization and Dropout `Learning Principles`

- **P5-8.1 How to Add Constraints to the Objective Function: Regularization**: reviews constraints used to reduce overfitting
- **P5-8.2 How to Reduce Path Dependence: Dropout**: reviews the intuition of learning while disconnecting some links
- **P5-8.3 Supplementary Learning: Stabilizing Deep Computation**: connects initialization, numerical stability, and batch normalization as conditions that keep deep computation from shaking
- **P5-8.4 Supplementary Reading: How a Large Initialization Scale Shakes the Computation Range**: Examines how large initialization scales affect activations and gradients.

### Module 4. Computation Environment and Representation Learning

#### Chapter 9. GPU and Parallel Processing `History and Paradigm`

- **P5-9.1 GPUs and Parallel Processing**: reviews the role of computation resources in the spread of deep learning
- **P5-9.2 Batch and Tensor Computation**: reviews how many items are computed together

#### Chapter 10. Representation Learning `Deep-Learning Structures`

- **P5-10.1 Representation Learning**: compares human-written features with learned representations
- **P5-10.2 Representations in Deep Layers**: reviews the intuition of moving from low-level features to higher-level representations

### Module 5. Spatial Structure and CNNs

#### Chapter 11. CNNs `Algorithms`

- **P5-11.1 The Intuition of Convolutional Neural Networks (CNNs)**: reviews structures that capture local patterns in images
- **P5-11.2 Convolution and Pooling**: lightly reviews the key operations of CNNs
- **P5-11.3 Supplementary Reading: Comparing CNNs and Vision Transformers**: briefly organizes one useful perspective for comparing post-CNN vision structures

### Module 6. Sequential Structures and the RNN Family

#### Chapter 12. RNN, LSTM, and GRU `Algorithms`

- **P5-12.1 Why RNN, LSTM, and GRU Are Needed**: reviews structures for sequential data
- **P5-12.2 Long-Term Dependency**: reviews the problem in which old information disappears

### Module 7. From Attention to Transformers

#### Chapter 13. Attention `Deep-Learning Structures`

- **P5-13.1 The Intuition of Attention**: reviews the idea of looking more strongly at needed positions
- **P5-13.2 The Flow That Leads to Self-Attention**: fixes the connection before moving into Transformers
- **P5-13.3 Supplementary Reading: QKV and Multi-Head Attention**: adds a first-reading standard for the internal components of attention

#### Chapter 14. Transformers `Deep-Learning Structures`

- **P5-14.1 Why Attention Alone Does Not Settle the Transformer**: reviews the place of attention, feed-forward, and layer normalization
- **P5-14.2 What Does Each of the Four Transformer Block Components Do?**: Distinguishes the roles of self-attention, feed-forward networks, residual connections, and normalization.
- **P5-14.3 Two Devices That Stabilize Deep Repetition**: Explains how residual connections and normalization stabilize repeated blocks.
- **P5-14.4 RNN State Passing and Transformer Parallel Computation**: Compares sequential RNN state transfer with Transformer parallel computation.
- **P5-14.5 How Do Sequential State and Direct Re-Reference Split in Long Context?**: Compares sequential state transfer with direct access to earlier representations in long contexts.
- **P5-14.6 Supplementary Learning: Position-Wise Representation Processing**: Explains how feed-forward networks transform each position after attention.
- **P5-14.7 Supplementary Learning: A Path That Preserves the Original Representation**: Explains the residual path that adds the original representation to a new computation.
- **P5-14.8 Supplementary Learning: Normalization That Aligns the Value Baseline**: Explains how layer normalization adjusts the scale of values within a position.

### Module 8. Generative Models and Sampling

#### Chapter 15. Intuition for Generative Models `Deep-Learning Structures`

- **P5-15.1 What Changes When We Read Generative AI Through Deep Learning**: prepares the output viewpoint needed before Part 6 analyzes generative AI in depth
- **P5-15.2 Candidate Distributions in Generative Models**: reads generation through candidate spaces and relative plausibility
- **P5-15.3 How Sampling Pulls Actual Outputs from Candidate Distributions**: reviews how actual outputs are selected from candidate distributions and why quality can vary
- **P5-15.4 How Does a Diffusion Model Learn and Restore Noise?**: Connects forward noising, noise prediction, and iterative denoising.
- **P5-15.5 What Do Attention and Transformers Do in Diffusion Models?**: Distinguishes self-attention, cross-attention, U-Net, and DiT in diffusion models.
- **P5-15.6 How Does a VAE Turn an Image into a Latent Representation?**: Explains encoding, reconstruction, and distribution constraints in a VAE.

## Part 6. LLMs and Generative AI

Part 6 starts from generative-AI outputs, reads LLMs as the representative case, and connects tokens, embeddings, next-candidate generation, learning and adjustment, prompts and grounding, tools and AI agent execution, evaluation, and operations. The development history and the BERT family are placed after the main current as a background map and comparison axis.

### Module 1. Entering Generative AI Through LLMs

#### Chapter 1. The Position of Generative AI and LLMs `LLM Core`

- **P6-1.1 Viewing Generative-AI Output as an Artifact to Review**: fixes that generated results are artifacts to review, not classification labels or numeric predictions.
- **P6-1.2 LLMs as the Central Case for Reading Generative AI**: reviews why LLMs are used as the representative path rather than as all of generative AI.
- **P6-1.3 Generation Is Repeated Candidate Distributions and Selection**: recovers the candidate-distribution and sampling intuition from Part 5 in the LLM generation flow.

### Module 2. Input Units and Representation for Text Generation

#### Chapter 2. Tokens and Tokenization `LLM Core`

- **P6-2.1 Token Units Limiting Inputs and Outputs**: reviews why inputs and outputs are limited by token units in cost, length, and context preservation.
- **P6-2.2 Model Input: Source Strings, Tokens, and Token IDs**: separates strings, tokens, and token-ID sequences in one flow.
- **P6-2.3 Tokenization Changing Length, Cost, and Chunks**: reviews how tokenization changes length, cost, chunks, and output interpretation.
- **P6-2.4 A Token View That Leads to Prompt Length, RAG Chunks, and Cost**: applies the token view to prompt length, RAG chunks, cost budgets, and output-format design.
- **P6-2.5 Supplement: Tokenizer Family Differences Revealed by Operational Observations**: reads BPE, WordPiece, and SentencePiece differences as operational observations.

#### Chapter 3. Embeddings `LLM Core`

- **P6-3.1 Embeddings That Turn Token IDs into Comparable Coordinates**: reviews why token IDs become vector representations that can be computed with.
- **P6-3.2 Nearby Vectors That Make Candidates, Not Answers**: reviews the intuition and limits of similar expressions becoming close candidates.
- **P6-3.3 Supplement: Embedding Learning That Learns Nearby and Distant Expressions**: asks what should be learned to stay close and what should be pushed apart.
- **P6-3.4 Supplement: Speed and Candidate-Missing Tradeoff in ANN Search**: reviews the tradeoff that appears when nearby candidates are narrowed quickly.

### Module 3. LLM Structures That Create the Next Candidate

#### Chapter 4. Reviewing Transformer Structure `Deep-Learning Structures`

- **P6-4.1 Transformer Computation Flow Inside an LLM**: rereads the Transformer as context reflection, representation update, and next-candidate scoring.
- **P6-4.2 Attention Reference Range**: reviews that the model calculates relations inside a limited range.
- **P6-4.3 Supplement: Attention Heads and Positional Representations**: separates order information from multiple relation axes.
- **P6-4.4 Supplement: KV Cache and Repeated Generation**: reviews the recomputation cost of repeated generation.
- **P6-4.5 Supplement: Long Context and Sparse Attention**: separates connection-count control from long-context retention.

#### Chapter 5. The GPT Family `LLM Core`

- **P6-5.1 GPT Family Through Decoder-Based Cumulative Generation**: reviews the position of decoder-centered autoregressive generation.
- **P6-5.2 Instruction Following and Conversational Interfaces Added on Top of Generation Structures**: reviews how instruction following and product interfaces changed user experience.

#### Chapter 6. The BERT Family `LLM Core`

- **P6-6.1 BERT as a Reading-Centered Transformer Comparison Axis**: compares the GPT generation family with the BERT understanding family.
- **P6-6.2 Understanding-Centered Tasks that Output Judgment Values Before Long Answers**: reviews classification, sentence-pair judgment, search and ranking, and embedding reuse.

#### Chapter 7. Next-Token Prediction and Generation `LLM Core`

- **P6-7.1 Next-Token Prediction as the Starting Point of Long Generation**: reviews why the local objective of a next-token distribution can lead to long generation.
- **P6-7.2 Output Selection Rules That Change Answer Stability and Diversity**: reviews how greedy choice, sampling, and temperature change stability and diversity.

### Module 4. Learning and Adjustment That Shape Response Habits

#### Chapter 8. Pretraining `Learning Principles`

- **P6-8.1 Pretraining That First Builds a Broad Language Base**: reviews how large-scale text builds a general language base.
- **P6-8.2 Scale That Grows Capability and Operational Burden Together**: reviews scale as an axis that increases capability and operational burden together.

#### Chapter 9. Fine-Tuning `Learning Principles`

- **P6-9.1 Fine-Tuning Needed for Purpose-Specific Adjustment**: reviews how a base model is adjusted toward a specific goal or domain.
- **P6-9.2 LoRA That Reduces the Burden of Full Fine-Tuning**: reviews how narrowing the adjustment range changes cost and iteration speed.

#### Chapter 10. Instruction Tuning and Alignment `LLM Core`

- **P6-10.1 Instruction Tuning That Builds Response Habits Matching Request Formats**: reviews the response habit of following user instructions.
- **P6-10.2 Alignment That Separates Well-Followed Answers from Acceptable Answers**: reviews usefulness, safety, factuality, and refusal criteria together.
- **P6-10.3 LLM Failures Divided into Format, Evidence, and Execution Gaps**: chooses support methods by failure cause.
- **P6-10.4 Supplement: LoRA Low-Rank Adjustment Delta**: Explains how LoRA represents weight adjustments with low-rank matrices.
- **P6-10.5 Supplement: Constraints in Efficient Adjustment Methods**: Compares the structural and memory constraints of efficient adaptation methods.

### Module 5. Prompts and Grounding

#### Chapter 11. Prompt Engineering `LLM Core`

- **P6-11.1 Prompt Engineering That Adjusts Input Instructions, Context, and Examples**: reviews how instructions, context, examples, and output formats guide generation.
- **P6-11.2 Limits That Move Freshness, Grounding, and Execution Outside Prompts**: reviews why recency, grounding, computation, execution, and reproducibility cannot be solved by prompts alone.
- **P6-11.3 Supplement: Observing and Comparing Response Paths**: separates prompt-layer strategies from their limits.
- **P6-11.4 Supplement: Iterative Improvement of Prompt Candidates**: reviews the relation among prompt candidates, evaluation criteria, and validation sets.

#### Chapter 12. RAG `Service Structure`

- **P6-12.1 RAG That Attaches External Evidence Instead of Model Memory**: reviews the structure that attaches external evidence as input context rather than internal model memory.
- **P6-12.2 RAG Flow That Separates Retrieval Failure from Generation Failure**: separates retrieval failure from generation failure.

#### Chapter 13. Vector Databases `Service Structure`

- **P6-13.1 Vector Databases That Store Embeddings, Source Text, and Metadata Together**: reviews structures that store and search embeddings with payloads and metadata.
- **P6-13.2 Indexes That Trade Off Retrieval Speed and Candidate Quality**: reviews the trade-off between retrieval quality and latency.

### Module 6. Tool and Agent Execution Structure

#### Chapter 14. Tool Use `Service Structure`

- **P6-14.1 Tool Use That Hands Lookup, Computation, and Execution Outside the Model**: reviews cases that require lookup, calculation, file processing, or state checks.
- **P6-14.2 Function Calling That Splits Natural-Language Requests into Names and Arguments**: reviews how natural-language requests are structured as function names and arguments.

#### Chapter 15. Agents `Service Structure`

- **P6-15.1 Agents That Change the Next Task Based on Intermediate Results**: reviews a structure that connects a goal to planning, tool calls, observations, and state judgment.
- **P6-15.2 Agent Loops That Split into Continue, Stop, and Human Review**: reviews continuation, termination, and human-review branches in the AI agent loop.

#### Chapter 16. MCP and Harnesses `Service Structure`

- **P6-16.1 MCP Connecting Tools and Resources in a Shared Format**: reviews the interface layer that connects tools and resources in a common form.
- **P6-16.2 Harnesses That Wrap Execution Records and Reproducible Environments**: reviews the environment around execution, logs, evaluation inputs, approval, and reproducibility.
- **P6-16.3 Supplement: How Are Agent Workflows and Image-Generation Workflows Different?**: compares control flow, data-transformation flow, and execution-record roles.

### Module 7. Reviewable Service State

#### Chapter 17. LLM Evaluation `LLM Core`

- **P6-17.1 LLM Evaluation That Separates Natural Answers from Quality Criteria**: separates natural answers from quality criteria.
- **P6-17.2 Division of Work Between Automatic Evaluation and Human Evaluation**: reviews the division between repeated checks and contextual judgment.

#### Chapter 18. Service Operation Constraints `Service Structure`

- **P6-18.1 Operational Constraints That Filter Again by Cost, Latency, and Usage**: reviews cost, latency, throughput, and usage limits.
- **P6-18.2 Handling Operational Failures by Splitting Errors into Recovery Routes**: separates hallucination, timeout, permission errors, and format mismatch into recovery paths.

#### Chapter 19. Binding a Small Generative-AI Feature Into One Flow `Project Practice`

- **P6-19.1 A Small Generative AI Feature that Connects Question, Evidence, Answer, and Record**: binds question, evidence, answer, state judgment, and record in one flow.
- **P6-19.2 A Minimal Implementation that Records Evidence, State, and Review Before the Response**: closes why the response, evidence, state, and reflection record must remain together before Part 7.

### Module 8. Background Map and Comparison

#### Chapter 20. History of LLM Development `History and Paradigm`

- **P6-20.1 Reading LLM History as a Flow of Limits and Structural Shifts**: reviews the shift from statistical language models to GPT-style interfaces.
- **P6-20.2 A Criterion for Separating Direct Lineage from Surrounding Evidence**: separates direct LLM lineage from surrounding evidence for deep-learning expansion.

#### Chapter 21. Open-Weight Models `Service Structure`

- **P6-21.1 What Does an Open-Weight Model Make Available?**: distinguishes weight availability, open source, and public APIs, then examines licenses, execution environments, and operational responsibility together.
- **P6-21.2 Local Runtime Environments and Memory Placement**: separates GPU VRAM, CPU RAM, dtype, quantization, and CPU offloading when running open-weight models directly, and keeps execution feasibility separate from quality judgment.

## Part 7. Projects

Part 7 is not a separate Part for new theory. It is the practice space for material introduced earlier. The front half covers questions, input units, baselines, and comparison experiments. The middle covers input structure, learning curves, and error cases. The back half covers RAG, AI agents, and deployment or operational judgment through logs and failure records.

### Module 1. Questions and Baselines

#### Chapter 1. Starting Analysis and Designing Baselines `Project Practice`

- **P7-1.1 Defining the Project Question and Input**: shows that even with the same data, changing the prediction target or sample unit creates a different project and changes data preparation and experiment design.
- **P7-1.2 Baselines and the First Comparison**: uses comparison tables and failure cases to show that model performance must be read through `what it improved over` before `how good it looks`.
- **P7-1.3 Baseline Redesign Practice**: compares how the opening line of a retrospective changes when the baseline cutoff and comparison unit change.

#### Chapter 2. Comparing and Improving Traditional Machine Learning `Project Practice`

- **P7-2.1 Reading Comparison Tables and Error Cases**: reads prediction comparison tables and representative error cases together instead of relying on one score.
- **P7-2.2 Building a Retrospective and Next Question**: organizes one experiment into `facts`, `interpretation`, and `next question`, then carries it into the next iteration.
- **P7-2.3 Comparison-Experiment Practice**: places a baseline, raw 1-NN, partial rescaling, and normalization on the same evaluation set and separates failures fixed by preprocessing from failures that still need more boundary cases or features.

### Module 2. Comparison and Structural Interpretation

#### Chapter 3. Input Structure and Model Structure Selection `Project Practice`

- **P7-3.1 How Input Structure Changes a Project**: compares how tabular data, image inputs, and sequence inputs change preparation code, sample inspection, and model input-output definitions.
- **P7-3.2 Comparing CNN, Sequential, and Attention Families**: explains why different computational structures are chosen when input structure and reference relationships differ.
- **P7-3.3 Recompare Input Representations with a Classifier**: Uses a classifier to compare how representations change accuracy, confidence, and review candidates.

#### Chapter 4. Reviewing Learning Results and Representations `Project Practice`

- **P7-4.1 Reading Loss, Metrics, and Error Cases Together**: judges `what actually improved` by reading learning curves, evaluation metrics, and error samples together.
- **P7-4.2 Decomposing a Failed Result Again**: separates weaker-than-expected results into structural problems, data problems, and baseline-setting problems, then sets the next experiment direction and revision priority.
- **P7-4.3 Representation-Normalization Practice**: compares normalized and unnormalized requests and observes how synonym replacement changes coverage, prediction, and retrospective priority.
- **P7-4.4 Comparing Same Averages with Different Patterns**: Compares patterns that have the same average but different spatial arrangements.

## Sources and References

This document is an original table-of-contents document reorganized to make the current project structure easier for readers to scan. It does not directly quote external sources.
