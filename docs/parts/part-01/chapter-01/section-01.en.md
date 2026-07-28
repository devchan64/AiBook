# P1-1.1 Scope of the Word AI

> Section ID: `P1-1.1`
> Version: `v2026.07.26`

When studying AI again, the first difficulty is often not the technology itself but the scope of the term. The same word, `AI`, can refer to a rule-based program in one context, to a machine-learning model in another, and in recent usage can even be treated as if it were nearly the same thing as generative AI or an LLM.

The purpose of this section is not to produce one perfect sentence that defines AI once and for all. The purpose is to organize the range of the term so that later sections on rule-based systems, machine learning, deep learning, generative AI, and LLMs can be read on the same map.

In Part 1, `AI` is the widest outer category. Even when the term appears again in later sections, only the amount needed for the current question is carried forward there. When the range itself needs to be separated again, return to this section and to the glossary entry for [AI](/AiBook/en/reference/concept-glossary-alpha/a/#ai-artificial-intelligence).

## Placing AI as the Widest Outer Category

This section organizes the following questions.

- Why is the word AI used so broadly?
- Inside what larger map do rule-based AI, machine learning, deep learning, and generative AI sit?
- Why does confusion arise when recent LLM experience is treated as if it meant all of AI?

This section first closes the point that `AI is the widest outer category`. The detailed technical flows continue in Part 1 Chapter 2, Part 1 Chapter 3, and from Part 4 onward. Here the focus is on placing terms on that large map.

## Reading AI as a Field, Not as a Product

- Explain why the term AI is used broadly.
- Read AI as a field for handling problems, not as the name of one product or one latest model.
- Organize the relationship among AI, machine learning, deep learning, and generative AI at a level that can be reused in later chapters.

## Main Learning Points

Many terms appear in this section, but the structure becomes much clearer once they are not all treated as if they lived on the same conceptual level. The three points below form the large map of the section.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| `AI` is a broad field, not the name of one product | This prevents machine learning, deep learning, and LLMs from being mixed as if they were the whole of AI. | First separate AI as the widest outer category. |
| Even when all are called `AI`, the implementation style has changed across time | This starts to reveal why rules, search, probability, learning, and deep learning all appear together. | First separate the definition of AI from the way AI is implemented. |
| Recent LLMs are one stream inside AI, not AI as a whole | This reduces the mistake of treating current product experience as if it were the whole field. | Separate generative AI and LLMs as later streams inside a wider map. |

`Field`, `system`, `input`, `output`, and `goal` can sound similar in the beginning. In this section, they are separated like this.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| field | a broad academic or technical range that bundles many problems and approaches | the place from which AI is read at its widest |
| system | an implemented structure that receives input and produces results | concrete cases such as a rule-based system, recommendation system, or chatbot |
| input | the information a system receives | sentences, records, images, sensor values |
| output | the result produced by the system | classification, recommendation, prediction, or generated output |
| goal | the purpose that defines why such an output is desirable | approval support, recommendation, search, answer generation |
| impact | the effect the output has on human judgment or the environment | approval decisions, ranking changes, workflow changes |

The first baseline that should remain from this section is that `AI is a broad field` and that `an AI system is a structure with inputs, goals, and outputs`. `Impact` is included because the same output can play very different roles depending on how it affects real people and real environments. If the terms become unstable again, return to the relevant glossary entries for [system](/AiBook/en/reference/concept-glossary-alpha/s/#system), [model input](/AiBook/en/reference/concept-glossary-alpha/m/#model-input), [model output](/AiBook/en/reference/concept-glossary-alpha/m/#model-output), and impact.

For example, consider an online store product recommendation. AI is the broad field that includes such recommendation problems. A `recommendation system` is the actually implemented system. The inputs are click records and purchase records. The output is a ranked list of products. The goal is to choose what the user is likely to look at next. The `impact` is that some products are shown more often and the user’s decision flow changes. Even when later sections introduce different cases, dividing them first into these six slots is often more helpful than trying to memorize the terms directly.

## Detailed Learning

### AI Is Not the Name of One Technique

AI is closer to a broad research field and system category than to the name of one single technique. Because of that, starting only with the question “Is this real intelligence?” quickly becomes unproductive. In practice, it is more stable to ask first, “What kind of problem is being solved, and in what way?”

A system that looks for the next move in chess or Go, a model that recognizes objects in an image, a model that translates sentences, and a chatbot that answers user questions look very different on the surface. But they all share one broad structure: they receive input, perform some computational process, and produce outputs, decisions, recommendations, predictions, or generated results.

Across major English-language dictionaries, East Asian reference materials, and institutional definitions, AI is generally described as the ability of a computer system, machine, or algorithm to perform or simulate some functions associated with human intelligence. Repeatedly listed functions include language, images, problem-solving, learning, prediction, recommendation, and decision.

Accordingly, this book reads AI in the following way.

> Artificial intelligence (AI) is a broad term that refers both to the field and to the systems developed so that computer systems, machines, and algorithms can perform some functions associated with human intelligence.

The Turing test also remains an important historical starting point when reading AI. Rather than trying to define “Can a machine think?” directly, Turing reformulated the question into whether a human can distinguish a machine from a human through conversation. That move is a representative early attempt to judge intelligence by observable behavior rather than by invisible internal structure.

But the Turing test alone cannot explain all of modern AI. Today, it is not enough to ask only whether a system appears human in conversation. We also have to ask what data was used, what model structure was trained, what evaluation criteria were passed, and what effects the system has in real environments. So this book treats the Turing test not as the entire definition of AI but as an early problem-setting about how intelligence should be judged.

The OECD’s 2023 explanation describes an AI system as a machine-based system that, under explicit or implicit objectives, receives input and generates outputs such as predictions, content, recommendations, or decisions. This definition focuses less on whether the system thinks like a human and more on the relationship among inputs, goals, and outputs.

That viewpoint fits the starting point of this book. Rather than beginning with AI as the complete duplication of human intelligence, it begins with AI as a system that turns problems into computational form and produces outputs that affect an environment.

### Why the Word AI Became So Broad

The word AI feels broad because it does not point to only one algorithm. It carries multiple eras of problem-solving approaches together. In early AI, it was central to explicitly design rules, knowledge, and search procedures by hand. When there were too many possible answers, heuristics were used to reduce the search range.

As data grew and storage and processing infrastructure expanded, the center of AI explanation also shifted toward learning judgment criteria from data. Data mining and data-driven decision-support flows were not identical to AI models themselves, but they became part of the background in which “collect data, analyze it, and connect it to judgment” became normal.

Against that background, machine learning took shape as an approach where the system learns patterns from data instead of requiring people to write every rule directly. Deep learning then extended that direction by combining neural networks, weights, and representation learning to handle more complex inputs and outputs.

For that reason, this book does not read AI only as “machines acting like humans.” It reads together the approach in which people write rules directly, the approach in which systems learn judgment criteria from data, and the approach in which those outputs are connected to services and decisions.

| Level | How judgment is produced | Position in this section |
| --- | --- | --- |
| rule-based AI | people explicitly write rules and knowledge | an older approach that still belongs inside AI |
| search and heuristics | candidates are explored but reduced by experience-based criteria | revisited in Part 1 Chapter 7 |
| DSS/BI/DW/OLAP | data is collected and connected to decision-making | background of data-centered systems around AI |
| data mining and machine learning | patterns and predictive criteria are found from data | revisited from Part 1 Chapter 3 onward and in Part 4 |
| deep learning and generative AI | representations and weights are learned to produce complex outputs | revisited from Part 1 Chapter 9 onward and in Part 5 and Part 6 |

This separation is a safety device that prevents dictionary-style definition from being mixed with historical change. In dictionary terms, AI is a computer system or field that performs functions associated with human intelligence. Historically, the implementation of those functions expanded through rules, search, probability, data learning, and deep learning.

The reason `DSS/BI/DW/OLAP` appears here is to show early that data modeling does not suddenly appear later as a separate technique. It grows on top of an older flow that collected data and connected it to decision-making. Memorizing every abbreviation is not the goal. For the present context, it is enough to read `DSS (decision support system)` as a system that supports decisions, `BI (business intelligence)` as a structure for reading data and using it in business judgment, `DW (data warehouse)` as a storage structure that collects data, and `OLAP (online analytical processing)` as a way to analyze collected data by several criteria.

### AI Scope Changes by Context

The word AI is used differently depending on context.

| Expression | Common use context | Point of caution |
| --- | --- | --- |
| AI | the whole class of systems that exhibit intelligent behavior | it can be so broad that the concrete method disappears |
| machine learning | an approach that learns patterns or relations from data | not every AI system is machine learning |
| deep learning | a method that learns complex representations with neural networks | not every machine-learning method is deep learning |
| generative AI | models and services that generate text, images, audio, or code | generation does not mean the output is factual |
| LLM | a large language model | not every generative-AI system is an LLM, and even an LLM may be only one component inside a service |

So this book keeps AI as the widest category first, then separates lower concepts according to how problems are solved.

```mermaid
--8<-- "assets/part-01/chapter-01/ai-scope-map-en.mmd"
```

This diagram is a learning map. It places `AI` as the outer category and shows where rule-based approaches, search and planning, probabilistic reasoning, machine learning, deep learning, generative AI, and LLMs sit relative to one another. The important thing is not to memorize every arrow as a strict inclusion relation. The important thing is to read that `LLM` does not mean all of AI and that `rule-based approaches` are not outside AI but one stream inside it.

### Questions This Book Uses to Read AI

The key is not to judge once and for all whether something is or is not AI. The key is to check how the system in front of you answers the following questions.

- What is the input?
- What is the output?
- Did a person write the rules directly, or did the system learn relations from data?
- How does it handle uncertainty?
- What effect does the result have on the real environment or on a user’s judgment?

These questions make the broad word AI easier to divide into smaller and more stable pieces. Later chapters on rule-based AI, heuristics, probability, machine learning, deep learning, and LLMs can all be placed back on this same frame.

### A Short Practice in Distinction

Try writing down the `input`, `output`, and `decision style` for the following three scenes. Doing so makes the range of the term AI much more stable.

| Scene | What is the input? | What is the output? | What question should a person ask first? |
| --- | --- | --- | --- |
| first-pass loan review table | requested amount, income, delinquency history | hold, further review, reject | Were the rules written directly by people, or learned from data? |
| product recommendation model | customer click records, purchase records, product information | ranked list of recommended products | Were patterns learned from past data? |
| document-summary chatbot | user question, source document, system instruction | summary sentences, answer sentences | Does it only generate, or does it also use retrieval and rules? |

The point of this exercise is not to decide instantly whether something is or is not AI. The point is to distinguish that even within the AI category, there are different ways of working: people can write rules, systems can learn from data, and generative models can be combined with retrieval and rules.

## Cases and Examples

### Case 1. Treating a Chatbot as If It Were All of AI

If the first AI a user has encountered is only a chatbot, it is easy to feel that `AI is a service that answers questions`. But inside the same organization there may also be a rule-based approval system, a recommendation system, a search-ranking model, and a demand-forecasting model. People naturally define AI too narrowly around the single visible conversational experience. The more stable standard for the book is to ask first what inputs are received and what outputs are produced. This case shows that recent LLM experience may be one representative case of AI, but it is not the whole of AI.

### Case 2. Rule-Based Systems Also Fall Within AI

Suppose a loan-review system uses only a hand-written rule table to make a first pass over applications. A reader may feel that, since there is no training data and no chat interface, this is not really AI. But the system still receives input, follows rules and goals to produce a judgment, and affects human decisions and the environment. In that broad sense, it can still be read inside AI as a system designed to perform a function associated with intelligence. This case shows that if AI is narrowed only to recent learned models, an important layer is lost.

## Checklist

- You can explain that AI is used not only as the name of one technology but as a broad field and system category.
- You can explain why confusion arises when AI, machine learning, deep learning, generative AI, and LLMs are treated as if they belonged to the same conceptual level.
- You can distinguish dictionary-style meaning from historically expanded usage.
- You can view an AI system in terms of input, goal, output, and impact.
- You can distinguish between a generated result sounding natural and a generated result being true.
- You can explain that AI is not one product but a broad category of systems with inputs, goals, and outputs.
- You can explain that if AI is defined only through recent generative-AI experience, it becomes easy to miss other layers such as rule-based systems, search, recommendation, and prediction.

## Sources and Further Reading

- OECD.AI, Stuart Russell, Karine Perset, Marko Grobelnik, [Updates to the OECD’s definition of an AI system explained](https://oecd.ai/en/wonk/ai-system-definition-update){: target="_blank" rel="noopener noreferrer" }, 2023-11-29, accessed 2026-06-22.
- NIST AI Resource Center, [Glossary](https://airc.nist.gov/glossary/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Merriam-Webster, [Artificial intelligence Definition & Meaning](https://www.merriam-webster.com/dictionary/artificial%20intelligence){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Cambridge Dictionary, [Meaning of artificial intelligence in English](https://dictionary.cambridge.org/dictionary/english/artificial-intelligence){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Britannica Dictionary, [Artificial intelligence Definition & Meaning](https://www.britannica.com/dictionary/artificial-intelligence){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- 汉典, [人工智能](https://www.zdic.net/hans/%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- A. M. Turing, [Computing Machinery and Intelligence](https://academic.oup.com/mind/article/LIX/236/433/986238){: target="_blank" rel="noopener noreferrer" }, Mind, Volume LIX, Issue 236, 1950-10-01, accessed 2026-07-19.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, accessed 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223){: target="_blank" rel="noopener noreferrer" }, arXiv:2303.18223, accessed 2026-06-22.
- Usama M. Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }, AI Magazine, 1996, accessed 2026-06-22.
- D. J. Power, [A Brief History of Decision Support Systems](https://dssresources.com/history/dsshistory.html){: target="_blank" rel="noopener noreferrer" }, DSSResources.COM, version 4.0, 2007-03-10, accessed 2026-06-22.
