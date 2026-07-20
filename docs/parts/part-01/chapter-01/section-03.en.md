# P1-1.3 Relationship Among AI, Machine Learning, Deep Learning, and Generative AI

> Section ID: `P1-1.3`
> Version: `v2026.07.20`

Section 1.1 organized the scope of the word AI, and Section 1.2 looked at the kinds of problems AI deals with. This section organizes the relationship among `AI`, `machine learning`, `deep learning`, `generative AI`, and `LLM`, all of which will keep returning later.

What matters here is not memorizing perfect inclusion relations. What matters is fixing a baseline so that terms from different conceptual levels are not mixed as if they meant the same thing.

In Part 1, the baseline relationship among `AI`, `machine learning`, `deep learning`, `generative AI`, and `LLM` is fixed in this section. Even when the terms reappear later, only the minimum connection needed for the current question is carried forward there. When the relationship among the terms themselves needs to be reorganized again, return to this section and to the [Concept Glossary](/AiBook/reference/concept-glossary/).

## Separating the Levels of AI, Machine Learning, and LLMs

This section organizes the following questions.

- What is the safest way to read the relationship among AI, machine learning, deep learning, generative AI, and LLMs?
- What part can be explained through inclusion relation, and what part becomes mixed differently inside real services?
- Why does confusion arise when the terms are narrowed into something like `AI = LLM`?

This section first closes the point that `AI, machine learning, deep learning, generative AI, and LLM are terms from different levels`. The internal structure of each level continues in Part 4, Part 5, and Part 6. Here the focus is first on distinguishing the `place` of each term.

## Distinguishing Inclusion Relations from Service Mixtures

- Distinguish the basic relationship among AI, machine learning, deep learning, generative AI, and LLMs.
- Avoid understanding all of AI too narrowly from recent service experience alone.
- Understand that even if a broad inclusion relation is roughly useful, real services still mix several technologies together.

## Concepts to Connect First

This section is the baseline for the term relationship that Part 1 will keep reusing. The concepts below should be fixed only by position first, and checked again through their glossary entries when fuller definitions are needed.

| Concept | Meaning to fix first here | Why it is needed now |
| --- | --- | --- |
| [AI](/AiBook/reference/concept-glossary/#ai-artificial-intelligence) | the broadest field and system category | to see where all other terms sit |
| [machine learning](/AiBook/reference/concept-glossary/#machine-learning) | a learning approach that improves performance from data | to separate rule-based and learning-based approaches |
| [deep learning](/AiBook/reference/concept-glossary/#deep-learning) | an approach that strongly uses neural networks and representation learning | to fix a major expansion path inside machine learning |
| [generative AI](/AiBook/reference/concept-glossary/#aigenerative-ai) | an output category that produces new content | to keep learning method and output character from collapsing into one |
| [LLM](/AiBook/reference/concept-glossary/#llm) | a family of large language models | to avoid reading generative AI and AI as a whole too narrowly as the same thing |

## Main Learning Points

What should remain first from this section is that the five terms are not all the same kind of name. The three standards below form the overall map.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| AI is the widest category, and machine learning and deep learning are approaches inside it | It reduces the mistake of comparing different kinds of terms as if they were peers. | Distinguish the broad flow `AI > machine learning > deep learning`. |
| Generative AI is a term about `what is produced` | It prevents deep learning, LLMs, and service experience from being collapsed into one block. | Distinguish generative AI as an output category that produces text or images. |
| LLMs are representative examples of generative AI, but not the whole of AI | It prevents recent usage experience from shrinking the whole field too much. | Distinguish clearly that `AI` is not the same thing as `LLM`. |

`AI` is the broadest field and system category. `Machine learning` is a learning approach that improves performance through data. `Deep learning` is a method inside that approach that strongly uses neural networks and representation learning. `Generative AI` is an output category that produces new content. `LLM` is a representative language-model family inside that space. In other words, read them as `AI as outer category`, `machine learning and deep learning as learning approaches`, `generative AI as output category`, and `LLM as a language-model family`.

## Detailed Learning

### Start With the Big Picture

The widest term is AI. AI is the broad field and system category that aims to perform some functions associated with human intelligence through computer systems, machines, and algorithms. Inside it sit different approaches such as rule-based methods, search, planning, probabilistic reasoning, and machine learning.

Machine learning is the approach that improves performance through data or experience. Instead of having people write every rule directly, it lets a model learn decision criteria from input-output examples, rewards, or structure inside data.

Deep learning is an approach inside machine learning that learns representations through neural networks, especially deep networks with multiple layers. Earlier approaches often relied heavily on people designing features directly. Deep learning strongly expands the direction in which useful representations are learned together from raw data.

Generative AI refers to AI models and services that create new content such as text, images, audio, video, or code. Recent generative AI is usually built on deep learning and large-scale models, but `deep learning` and `generative AI` are not the same term. Deep learning is closer to a learning method and model structure. Generative AI is closer to the character of the output.

The reason it is described as an `output character` becomes clearer by comparison. If a system reads a customer inquiry and chooses one among categories such as `refund inquiry`, `delivery inquiry`, and `account inquiry`, that is closer to classification. If the same inquiry is read and the system produces a new answer sentence such as `refunds are usually completed within three business days`, that is closer to generation. So the more direct boundary for generative AI is not that the input is text, but whether the output is a predefined category or a newly created piece of content.

An LLM is a language-model family trained on large-scale text data. It is one of the representative technologies behind today’s generative AI, but it is not the whole of generative AI. Image-generation models, speech-generation models, and video-generation models are also forms of generative AI without being language models in the same sense.

```mermaid
--8<-- "assets/part-01/chapter-01/ai-to-llm-map-en.mmd"
```

This diagram is a learning map. In real research and real services, the boundaries are more complex. For example, when an LLM is attached to a search service, the result may look like generative AI from the outside, but the full system can also include a search engine, a database, permission controls, rule-based filters, and recommendation models.

The key is not memorizing the arrows as a rigid genealogy. The key is reading the place of each term: `AI as the widest outer category`, `machine learning and deep learning on the learning side`, `generative AI on the output side`, and `LLMs as a representative language-model family inside generative AI`.

### Do Not Treat the Terms as Belonging to the Same Level

Confusion happens when terms from different conceptual levels are compared side by side.

| Term | Main conceptual level | Short explanation | Point of caution |
| --- | --- | --- | --- |
| AI | field and system category | the broad field of building machines that perform functions associated with intelligence | should not be narrowed to one recent model |
| machine learning | learning approach | an approach for building models that improve through data or experience | not all AI is machine learning |
| deep learning | machine-learning method | an approach using deep neural networks and representation learning | not all machine learning is deep learning |
| generative AI | output character and service category | models and services that produce new text, images, audio, or code | generation does not mean factual correctness |
| LLM | model family | large language models centered on language data | not all generative AI is LLM-based |

For that reason, a question such as “Which is better, AI or machine learning?” is unstable from the start. Machine learning is one approach inside AI. Likewise, “Which is newer, deep learning or generative AI?” mixes levels. Deep learning belongs more to model-learning method, while generative AI belongs more to the character of the produced output and to service use.

### Inclusion Relation Is Only a Starting Point

At the beginning, one rough guide can be written like this:

> AI > machine learning > deep learning > generative AI > LLM

But that line is a very strong simplification. Generative AI is closer to an output and service category, so it should not be treated only as a simple lower stage beneath deep learning. A more accurate explanation has to keep several exceptions in mind.

- Rule-based AI can still fall inside AI without being machine learning.
- Machine learning includes many methods that are not deep learning.
- Deep learning is used not only for generation, but also for classification, recognition, prediction, and control.
- Generative AI can create text, images, audio, video, and code.
- LLMs are a representative model family inside generative AI, but they do not mean the whole service.

So inclusion relation is useful as a guide, but when an actual system is explained, it is still necessary to separate `what problem is being handled`, `what model or rules are being used`, and `what kind of output is being produced`.

### Separating Again Through Examples

The following table is a practice in distinction.

| Case | Is it AI? | Is it machine learning? | Is it deep learning? | Is it generative AI? | Is it an LLM? |
| --- | --- | --- | --- | --- | --- |
| a system that judges loan eligibility by human-written rules | yes | no | no | no | no |
| a model that predicts fraud risk from past transaction data | yes | yes | depends | usually no | no |
| a neural model that locates defect areas in an image | yes | yes | yes | usually no | no |
| a chatbot that produces a summary from a sentence input | yes | yes | usually yes | yes | usually yes |
| a model that produces an image from a text prompt | yes | yes | usually yes | yes | usually not an LLM in the narrow sense |

Expressions such as `yes`, `usually`, and `depends` are used because the internal implementation still has to be checked. Services that look similar from the outside can still differ internally.

What beginners most often confuse is `one service name` and `the several conceptual layers inside it`. For example, even one chatbot that answers questions over documents can be described in several ways at once.

| Description attached to the same service | Why that description can still be right | What to watch out for |
| --- | --- | --- |
| AI service | because it is a broad system that receives questions, produces answers, and affects human judgment | this only gives the widest category, not the internal method |
| machine-learning or deep-learning-based service | because the core model improving answer quality can rely on data learning and neural representation learning | this does not mean every component is deep learning |
| generative AI service | because the final output is a newly generated answer sentence | this does not mean the output has already been fact-checked |
| service containing an LLM | because the core language model processes questions and answers | retrieval, permissions, logs, and safety filters are not the LLM itself |

The key here is not `which description is wrong` but `which level is being described`. The same system can be an AI service from the outside, deep-learning-based from the model perspective, generative AI from the output perspective, and an LLM-containing system from the language-model perspective.

### Why Generative AI and LLM Must Be Separated

Today, many users first encounter AI through chatbots. Because of that, AI, generative AI, LLM, and product names such as ChatGPT can feel like one block.

But for learning, they still need to be separated. An LLM is a model family centered on language. Generative AI is the broader category that creates new content. The NIST generative-AI profile describes generative AI as a category of AI models that generate synthetic content derived from patterns and properties in the input data, with examples including images, video, audio, and text. It also treats LLMs as one representative common activity within that larger generative-AI space.

From that viewpoint, LLMs are an important case of generative AI, but they cannot explain all of generative AI by themselves. The reverse is also true: building a generative-AI service does not end with one LLM. Real services still need prompt handling, retrieval, permissions, logs, safety filters, user interfaces, and cost control.

### The Standard This Book Will Use

From here on, the book uses the following standards.

- `AI` is used for the widest field and system category.
- `machine learning` is used when a model improves performance from data or experience.
- `deep learning` is used when deep neural networks and representation learning are central.
- `generative AI` is used when models and services that create new content are being explained.
- `LLM` is used for large language models trained on language-centered data.

These standards are refined more closely in later chapters. For now, what matters is fixing the place of the terms. Part 3 first reorganizes data modeling, and the detailed algorithms and learning methods are then recovered again in Part 4, Part 5, and Part 6.

The terms are not finished here all at once. Instead, the section first connects where each one will be read fully again.

| Term fixed now | Where it is revisited more fully later | Why it matters at the current stage |
| --- | --- | --- |
| machine learning | Part 4 | because that is where problem, data, and evaluation are first organized in full structure |
| deep learning | Part 5 | because representation learning, backpropagation, CNNs, attention, and Transformers are recovered there as actual computational structure |
| generative AI | Part 6 | because generation structure, RAG, tool use, and agents are connected there all the way to service perspective |
| LLM | Part 6 | because tokens, next-token prediction, GPT-family models, and instruction tuning are fully explained there as one stream |

### A Short Practice in Separating Levels

The cases below are meant as a practice in dividing whether something is `AI`, `machine learning`, `deep learning`, `generative AI`, or `LLM`.

| Case | Distinction question to ask first | Point most likely to be confused |
| --- | --- | --- |
| a system that helps insurance review with a hand-written rule table | Did it learn from data, or were the rules written directly by people? | It can feel like AI but still not be machine learning. |
| a prediction model that detects abnormal transactions from transaction records | Were patterns learned from data, and is a neural network actually necessary? | Machine learning and deep learning are easily collapsed into one. |
| a service that makes an image from a text prompt | Does it create new content, and is the central output text or image? | It is generative AI but may not be an LLM. |
| a chatbot that answers questions over documents | Is the central model a language model, and are retrieval and rules attached together with it? | It is easy to treat the LLM and the whole service as if they were the same thing. |

The point of this exercise is not memorizing inclusion relations. The point is to separate whether the thing in front of you is being named as a field, a learning approach, a model family, or an output category. The same service can still be described at several levels at once: as a generative-AI service, as a system containing an LLM, and as an application where retrieval and rules are attached together.

## Cases and Examples

### Case 1. Why an Image-Generation Service Is Not Fully Explained as an LLM

Suppose a user sees a service that creates a poster image from a text prompt. Because many recent AI services have looked like chatbots, it can feel tempting to call such a system simply an `LLM`. But even if the service belongs to generative AI, its central model may not be a language model in the narrow sense. So `generative AI` and `LLM` often overlap, but they are not the same term, and the output type still matters. This case shows that generative AI is broader than LLMs.

### Case 2. Why a Rule-Based Judgment System May Not Be Machine Learning

Suppose an internal approval system works only through human-written conditions. The user may feel it is AI because it supports business judgment, but if there is no structure that learns patterns from data, it is hard to call it machine learning. In other words, it may belong to AI in the broad sense while still sitting at a different level from machine learning, deep learning, or generative AI. This case shows why the large map `AI > machine learning > deep learning` still needs to be read together with the actual implementation style.

## Checklist

- You can explain that AI is a broader term than machine learning.
- You can explain the difference between machine learning and deep learning through the viewpoints of data learning and neural representation learning.
- You can explain that deep learning and generative AI are not the same term.
- You can explain the relationship between generative AI and LLMs as `representative case, but not the whole`.
- You can explain that a real AI service can be a combination of several components, not one model alone.
- You can explain that `AI`, `machine learning`, `deep learning`, `generative AI`, and `LLM` are not terms from the same level.
- You can explain that generative AI is a broader category than LLMs, and that LLMs are a representative language-model family inside it.
- You can explain that real services do not end with one model and should be read together with components such as retrieval, permissions, logs, and safety filters.

## Sources and References

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update){: target="_blank" rel="noopener noreferrer" }, 2023-11-29, checked 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, checked 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/){: target="_blank" rel="noopener noreferrer" }, checked 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, checked 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223){: target="_blank" rel="noopener noreferrer" }, arXiv:2303.18223, checked 2026-06-22.
