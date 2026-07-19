# P4-1.1 The Relationship Among AI, Machine Learning, and Deep Learning

> Section ID: `P4-1.1`
> Version: `v2026.07.19`

Part 1 looked at the broad scope of the word AI. Part 2 revisited formulas, Python, arrays, tables, and graphs. Now Part 4 separates out machine learning on top of that foundation.

This Section distinguishes the ranges indicated by AI, machine learning, deep learning, generative AI, and LLM, and explains why Part 4 starts again from classical machine learning.

So the focus here is to distinguish `where machine learning sits inside the large field called AI` and `why Part 4 looks at data, models, learning, and evaluation before jumping directly to deep learning or LLMs`.

## Scope Of This Section

This Section first closes where `machine learning, deep learning, generative AI, and LLM sit inside the broad scope called AI`. Later sections hold the shared learning structure of Part 4, and later parts reconnect the full structure of neural networks and Transformers.

- Are AI and machine learning the same thing?
- How are machine learning and deep learning different?
- Do generative AI and LLM represent all of AI?
- Why does Part 4 look at classical machine learning before deep learning?
- How do the formulas and Python tools from Part 2 reappear here?

## Goals Of This Section

- You can roughly explain the inclusion relationship among AI, machine learning, deep learning, generative AI, and LLM.
- You can understand machine learning as `an approach that learns patterns from data and uses them for prediction or judgment`.
- You can explain that deep learning is an important stream inside machine learning, but not the same thing as all machine learning.
- You can see LLMs as a strong representative case of modern AI experience, while not treating them as identical to all of AI.
- You can understand that the study topic of Part 4 is the flow of data, models, learning, and evaluation.

## Reading Order

The terms become clearer if they are read by inclusion and by role.

1. AI is the broadest term.
2. Machine learning is an approach inside it that learns relations from data.
3. Deep learning is a stream inside machine learning that stacks neural networks deeply.
4. Generative AI and LLM are very important in modern AI experience, but they are not the same as all of AI.
5. Part 4 first looks at the data, models, learning, and evaluation that sit beneath all of those flows.

This order is not for perfectly memorizing an academic taxonomy. It is the minimum map needed later to distinguish whether what you are reading now is a data problem, a model problem, or a service problem.

## Distinguishing Them First In One Sentence

As the number of terms grows, it becomes clearer to first look at what question each term is trying to answer, together with the inclusion relationship.

| Term | One-sentence explanation | Central question |
| --- | --- | --- |
| AI (artificial intelligence) | A broad field that tries to create or imitate intelligent behavior with computers. | Can a machine do work that appears intelligent? |
| Machine learning | An approach that builds models or algorithms whose performance improves from data experience. | Can a system learn from data without people writing every rule? |
| Deep learning | A machine learning stream that learns representations through multi-layer neural networks. | Can the model learn the needed representation more directly from the input? |
| Generative AI | AI models and services that create new outputs such as text, images, audio, or code. | Can a model produce new outputs beyond classification and prediction? |
| LLM (large language model) | A family of models that handles language inputs and outputs through large-scale text learning. | Can a model generate the next expression or response from language context? |

This distinction is a reading map, not an exam definition. The same word can be used with slightly different scope across papers, product documents, news articles, and service marketing. So Part 4 keeps the repeated structure of data, models, learning, and evaluation at the center rather than the terms alone.

## Starting From The Largest Scope

AI is the broadest term. It can include rule-based systems, search, heuristics, knowledge representation, probabilistic inference, machine learning, deep learning, generative AI, and agents.

Machine learning is the approach among them that learns patterns from data. Instead of a person writing every rule directly, it finds relations in data, builds a model, and uses that model on new data.

Deep learning is a powerful stream inside machine learning that learns representations by stacking neural networks deeply. It created major results in images, audio, natural language, and generative models, but not all machine learning is deep learning.

Generative AI refers to models and services that generate new outputs such as text, images, audio, and code. Much of today's generative AI is tightly connected with deep learning, but the usage experience called generative AI does not mean all of AI.

LLM means large language model. Many people now first encounter AI through LLM experience, but an LLM is not all of AI. It is a particular model family developed around language.

```mermaid
--8<-- "assets/part-04/chapter-01/ai-scope-map-en.mmd"
```

This diagram is a learning map rather than a strict classification table. In real research and products, many technologies are mixed. For example, a single service can operate with search systems, rule-based filters, machine learning models, and LLMs together.

The next diagram separates the inclusion relationship from the way real services are assembled. If the diagram above shows `the broad position of the terms`, the diagram below shows that `multiple approaches can work together inside one service`.

```mermaid
--8<-- "assets/part-04/chapter-01/ai-service-composition-map-en.mmd"
```

In this diagram, the LLM is not the whole service but one component among several. Model outputs can be combined with policy judgment, and when risk is high or confidence is low, the flow can move to human review.

## Why Inclusion Relationship Alone Is Not Enough

For an introduction, the picture `AI contains machine learning, and machine learning contains deep learning` is useful. But if you remember only that picture, misunderstandings appear when you look at real services.

For example, a recommendation service can use a machine learning model based on user click history. At the same time, it can use rule-based filters that exclude forbidden products, and it can also use a search index or database lookup. A customer-support service may not be built from LLM alone either. Search, permission checks, policy rules, logging, and human review can all be present together.

So the perspective needed in Part 4 is not `which technology is newer`. It is the perspective that asks the following.

- In this problem, which part is written directly by people as rules?
- Which part has to be learned from data?
- Is the model output a score, a class, a numeric prediction, or a generated result?
- When the service makes the final decision, what policies or constraints are used together with the model output?

These questions connect the broad AI map from Part 1 and the data representations from Part 2 to the machine learning study in Part 4.

## Why Part 4 Looks At Machine Learning Separately

Part 4 does not jump directly to deep learning or LLM. It first looks at the basic flow of machine learning.

The reason is simple. Even when you later study deep learning and LLM, the following questions keep coming back.

- What data are being used?
- What are the input and the label?
- What does the model predict or classify?
- What values are changed during learning?
- What is the basis of evaluation?
- Does it work well on data it has not seen?

Classical machine learning is good for showing these questions through relatively small examples. Models such as linear regression, logistic regression, decision trees, and k-NN are simpler in structure than deep learning. So they are suitable for learning data splitting, overfitting, generalization, and metrics first.

In small machine learning examples, the flow `prepare the data`, `train the model`, `apply it to new data`, and `check whether it was right` stays visible. Once that flow is visible, later deep learning or LLM discussions are read by structure before model names.

## The Minimum Unit In Part 4

When returning to machine learning, it matters more to fix the repeated minimum units than to memorize many algorithm names.

| Minimum unit | Question | Example |
| --- | --- | --- |
| Problem | What are you trying to predict or distinguish? | Spam status, price, churn possibility |
| Data | What cases have been collected? | Past emails, transaction logs, sensor measurements |
| Feature | What input representation will be given to the model? | Word count, amount, time, category |
| Label or target | What is the model trying to match? | Spam/normal, actual price, purchase status |
| Model | What learned computation changes input into output? | Linear model, tree, nearest neighbors |
| Training | What values are adjusted from the data? | Weights, split criteria, distance criteria |
| Evaluation | How useful is it on new data? | Accuracy, error, recall, cost |

These minimum units do not disappear completely in deep learning or LLM later. The structure becomes larger and input representations become more complex, but the habit of asking what the data are, what the model learns, and by what criteria it is evaluated is still needed.

This table shows one bundle of questions. `What are we solving`, `what is given as input`, `what is being matched`, and `how do we check whether it was right` are the first questions to check when reading a machine learning document.

## Looking At The Same Problem Through Three Perspectives

The distinction becomes easier if you take spam-email classification as an example.

| Perspective | Question | Possible approach |
| --- | --- | --- |
| Rule-based approach | Should an email be treated as spam if it contains a certain word? | A person writes the rules. |
| Machine learning approach | Can a spam pattern be learned from past emails and labels? | A model is trained on features and labels. |
| Deep learning approach | Can the model learn the email sentence representation more directly? | A neural network learns both representation and the classification boundary. |
| LLM use | Can the model interpret intent and context in the email through natural language? | Prompts, classification instructions, and tool connections can be used together. |

These four perspectives are not perfect replacements for one another. In real services, rule-based filters, machine learning models, and LLM-based review can all be used together. So the better understanding is not `the newest method removes all older ones`, but `multiple methods are combined according to the problem and its constraints`.

When actually reading documents or in meetings, confusion is reduced if you first judge `which term is most accurate for what is being described now` as below.

| What is being described now | The first term to use | Why |
| --- | --- | --- |
| The full intelligent-function scope of a service | AI | Because it can include search, rules, models, and human review together. |
| The part that learns relations from data for prediction or classification | Machine learning | Because the core is a learned model rather than hand-written rules. |
| Neural-network-based representation learning and large-model structure | Deep learning | Because neural-network structure is central even within machine learning. |
| The experience or service that creates new outputs such as text, images, or code | Generative AI | Because generated output is the center of the user experience rather than classification. |
| A large model that handles language input and output | LLM | Because it points precisely to a language model inside generative AI. |

## Where The Language Of Part 2 Reappears

The expressions learned in Part 2 reappear immediately in Part 4.

| Expression from Part 2 | How it reappears in Part 4 |
| --- | --- |
| row, column | They express samples and features. |
| array, shape | They explain the form of input data `X`. |
| label | It appears as the target value `y` in supervised learning. |
| function | It appears as the computation that changes input into output. |
| loss, error | They become criteria for how wrong a prediction is. |
| mean, variance | They are used to read data distributions and evaluation results. |
| plot | It is used to inspect learning results, error, distributions, and decision boundaries. |

In scikit-learn documents as well, input data `X` is usually described as a matrix with samples in rows and features in columns. In supervised learning, the target value `y` appears together with it, and the model is trained with `fit` and then computes the result for new inputs with `predict`.

## Misunderstandings To Avoid First

At the start of Part 4, the first misunderstandings to avoid are the following.

- Do not treat AI as the same thing as machine learning.
- Do not treat machine learning as the same thing as deep learning.
- Do not treat deep learning as the same thing as LLM.
- Do not use LLM service experience as the standard for all of AI.
- Do not treat knowing many model names as the same thing as understanding machine learning.
- Do not treat fitting the training data well as the same thing as solving the real problem well.

The core of Part 4 is the flow of data, learning, and evaluation, not a model list. Algorithm names must be understood inside that flow.

## Cases And Examples

### Case 1. Why Using Chatbots Does Not Mean You Already Know All Of Machine Learning

Suppose a learner begins studying AI again for the first time, but has already used chatbots and image-generation tools often. That can make the learner think `isn't AI ultimately just LLM or generative AI?`

This thought appears easily because many service experiences now come in through LLM-centered interfaces. But if you look inside the service, search, rule-based filters, recommendation models, policy decisions, and human review can work together, and the LLM can be only one part among them.

That is why this Section separates the inclusion relationship among AI, machine learning, deep learning, generative AI, and LLM. LLM experience is an important starting point for understanding modern AI, but if it is treated as the single name that represents all of AI, the flow of data, models, learning, and evaluation that Part 4 revisits becomes hidden.

The checkable result appears when the service structure is broken into questions. If one part is handled by search, another by a classification model, and another by an LLM-generated response, then the simple equation `AI = LLM` is already not enough as an explanation.

```mermaid
--8<-- "assets/part-04/chapter-01/ai-llm-scope-misconception-flow-en.mmd"
```

## Checklist

- Can you distinguish which term is most accurate among `AI`, `machine learning`, `deep learning`, `generative AI`, and `LLM` in a given context?
- Can you explain why setting `AI = LLM` or `machine learning = deep learning` immediately weakens the explanation of service structure?
- Can you explain why Part 4 looks first at the repeated structure of `data, learning, and evaluation` rather than at model names?
- Can you explain the inclusion relationship among AI, machine learning, deep learning, generative AI, and LLM as different levels?
- Can you explain how the sense of formulas, Python, arrays, tables, and graphs from Part 2 is used again in the data-learning-evaluation flow of Part 4?
- Can you explain with an example that models, rules, search, policy, and human review can work together inside one service?

## Sources And References

- scikit-learn developers, `Getting Started`, scikit-learn documentation, accessed 2026-06-25. [https://scikit-learn.org/stable/getting_started.html](https://scikit-learn.org/stable/getting_started.html){: target="_blank" rel="noopener noreferrer" }
- Google for Developers, `Machine Learning Glossary`, entries for `artificial intelligence`, `machine learning`, `deep model`, `generative AI`, and `large language model`. Used to compare the scope of AI, machine learning, deep learning, generative AI, LLM, and terms for evaluation and learning. Accessed 2026-07-19. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- IBM, `AI vs. machine learning vs. deep learning vs. neural networks: What's the difference?`. Used to check the inclusion relationship that places AI as the broadest scope, with machine learning and deep learning as flows within it. Accessed 2026-07-19. [https://www.ibm.com/think/topics/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks](https://www.ibm.com/think/topics/ai-vs-machine-learning-vs-deep-learning-vs-neural-networks){: target="_blank" rel="noopener noreferrer" }
- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, Chapter 1 Introduction, accessed 2026-06-25. [https://www.deeplearningbook.org/contents/intro.html](https://www.deeplearningbook.org/contents/intro.html){: target="_blank" rel="noopener noreferrer" }
