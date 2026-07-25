# P1-2.3 The Flow Toward Machine Learning, Deep Learning, and Generative AI

> Section ID: `P1-2.3`
> Version: `v2026.07.20`

Section 2.1 covered symbolic AI and rule-based approaches, and Section 2.2 covered search, knowledge representation, and probabilistic reasoning. This section turns to the next flow. Why did the center of AI explanation move more and more toward models that learn from data?

The task here is not to explain machine learning, deep learning, and generative AI in full detail. The task is to place, from a historical point of view, why the center of explanation moved from `a way in which people write all the rules directly` toward `a way in which models are trained from data and experience`. Part 3 first organizes data modeling, and Parts 4, 5, and 6 later handle each structure in depth.

In Part 1, the historical flow in which the center moved from rule-based approaches toward learning-based approaches, and the basic connection among `data`, `feature`, `representation`, and `parameter`, is fixed here. The broad relation among `AI / machine learning / deep learning / generative AI / LLM` was already fixed in 1.3, and is reconnected here only as much as needed to see how those terms join into one flow. If the distinction becomes unstable again later, return to this section and the shared [Concept Glossary](/AiBook/reference/concept-glossary/).

## Why AI Moved from Writing Rules to Learning from Data

This section organizes the following questions.

- Why did problems that were difficult to solve through rule-based approaches alone lead toward data-based learning?
- Through what historical flow are machine learning, deep learning, and generative AI connected?
- Why did data, features, representations, models, and parameters become more and more important?

This section first closes `why the center of explanation moved toward data and learning`. Detailed learning structures continue in Part 3, Part 4, Part 5, and Part 6. Here the focus is on organizing that move as one large historical flow.

## Connecting Data, Features, Representations, and Parameters

- Understand why problems that were difficult to solve through rule-based approaches alone led to data-based learning.
- Distinguish machine learning, deep learning, and generative AI inside one historical flow.
- See why data, features, representations, models, and parameters became important.
- Read generative AI and LLMs not as a sudden break, but as the result of an accumulated flow.

## Concepts to Connect First

This section is the representative place where the shift of the explanatory center toward learning-based approaches and the core learning terms are tied together. The concepts below are fixed first by role, and when fuller definitions are needed later, you should return to the corresponding glossary entries.

| Concept | Meaning to fix first here | Why it is needed now |
| --- | --- | --- |
| [data](/AiBook/en/reference/concept-glossary-alpha/d/#data) | the material for learning and judgment | to see what the model learns criteria from instead of hand-written rules |
| [feature](/AiBook/en/reference/concept-glossary-alpha/f/#feature) | a clue that people organize or select first | to understand what kind of input representation early machine learning depends on |
| [representation](/AiBook/en/reference/concept-glossary-alpha/r/#representation) | the internal form handled inside the model | to see why deep learning is explained as representation learning |
| [parameter](/AiBook/en/reference/concept-glossary-alpha/p/#parameter) | an internal value adjusted through learning | to fix what learning actually changes |
| [machine learning](/AiBook/en/reference/concept-glossary-alpha/m/#machine-learning) | a learning approach that improves performance from data | to understand why the center moved from writing rules to training models |
| [deep learning](/AiBook/en/reference/concept-glossary-alpha/d/#deep-learning) | a neural-network-based approach that strongly uses representation learning | to understand the move from feature design toward representation learning |
| [generative AI](/AiBook/en/reference/concept-glossary-alpha/g/#aigenerative-ai) | a category of models and services that produce new content | to see how far the recent flow extends |

## Main Learning Points

This part organizes the large flow of modern AI. The three guideposts below are the overall map.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| problems that were difficult to solve through rules alone led toward `data-based learning` | This helps explain why machine learning rose to the center. | Distinguish that many problems became too hard for people to write all criteria directly. |
| machine learning, deep learning, and generative AI are `a connected flow`, not disconnected buzzwords | This lets many terms be read inside one map. | Organize the flow as data learning -> representation learning -> generation. |
| LLM is `one strong recent flow`, not all of AI | This separates current product experience from the whole historical picture. | Connect that LLM is a representative case inside generative AI. |

`data`, `feature`, `representation`, `model`, and `parameter` are core terms repeated throughout the section. The baseline that should remain first is this: `data is material`, `features are clues organized by people first`, `representations are the forms handled inside the model`, `a model is the computational structure that maps input to output`, and `parameters are internal values adjusted through learning`. Each term is tied together once more in the body below.

## Detailed Learning

### Problems for Which It Is Too Hard to Write All the Rules

Rule-based approaches are strong when people can write judgment criteria explicitly. They are still useful for business approval, permission checks, policy application, and simple classification where the standard is relatively clear.

But many real problems are hard to write down fully as rules.

| Problem | Why it is hard to write fully as rules |
| --- | --- |
| recognizing objects in photos | people cannot write all useful pixel combinations as rules |
| understanding natural-language sentences | there is too much context, omission, ambiguity, and variation in phrasing |
| deciding whether an email is spam | a few words are not enough, and attackers keep changing their patterns |
| predicting customer churn | behavior patterns are complex and change over time |
| speech recognition | pronunciation, intonation, noise, and recording environments keep changing |

In such problems, the more important question becomes not `what rules should people write directly?` but `what relations can be learned from data?` Machine learning places this question at the center.

Even inside the same workflow, some parts can still be handled with rules while other parts need learning. Seeing that split at once makes it clearer why the explanatory center moved.

| Scene inside the same customer-support workflow | Why a rule-based approach fits well | Why a learning-based approach becomes necessary |
| --- | --- | --- |
| checking refund eligibility period | a policy sentence can be written explicitly by a person | even if there are exceptions, the standard itself is relatively clear |
| classifying customer inquiry intent | some word-based rules can be made | expression is diverse and the meaning changes with context |
| deciding urgency priority of inquiries | some criteria can be written | it requires combining past handling history with multiple signals |

The key point of this table is not that rules became useless. It is that even inside one real problem, the part where `explicit standards can be written` and the part where `relations must be learned from data` begin to split apart. Chapter 3 narrows this split further and then examines the strengths and limits of rule-based systems alongside structures that learn patterns from data.

The Stanford Encyclopedia of Philosophy entry on AI describes machine-learning systems as systems that improve performance on a task when given examples. From that perspective, learning is not the act of a person writing every rule. It is the act of adjusting the model's judgment criteria through data and experience.

### Machine Learning: From Writing Rules to Training Models

Machine learning is an approach that improves a model's performance by using data or experience. Here, a model is the computational structure that takes input and produces outputs such as prediction, classification, recommendation, score, or action.

> data or experience -> learning -> model -> prediction or classification or recommendation or action

The difference between rule-based approaches and machine learning can be read like this.

| Distinction | Rule-based approach | Machine-learning approach |
| --- | --- | --- |
| judgment standard | explicit rules written by people | a model trained from data |
| central developer work | writing rules, handling exceptions, managing rule conflicts | preparing data, designing features, training, and evaluating |
| strength | explanation and control are comparatively easy | complex patterns can be learned from data |
| weakness | may be fragile under exceptions and change | data quality, bias, overfitting, and explainability issues arise |
| error review | review whether the rules are correct | review the training data and evaluation results |

Machine learning is not one single method. Supervised learning learns the relation between input and output from examples with answers attached. Unsupervised learning finds structure or patterns in data without attached answers. Reinforcement learning learns a better way of acting through rewards that come back after actions.

This section only fixes the names of those three learning types. Their detailed treatment returns in Part 1 Chapter 8.

| Learning type | English term | Basic question |
| --- | --- | --- |
| supervised learning | supervised learning | when input is given, what answer or value should be predicted? |
| unsupervised learning | unsupervised learning | how can structure in the data be found without answers? |
| reinforcement learning | reinforcement learning | when the result of an action returns later as reward, what policy should be learned? |

### Data Mining and the Background of Data-Based Judgment

The move toward machine learning is not explained only by internal change inside AI. It also grew together with practical demand: more data accumulated, and people increasingly wanted to find patterns in that data.

The KDD overview paper by Fayyad, Piatetsky-Shapiro, and Smyth describes KDD as the whole process of discovering useful knowledge from data, and distinguishes data mining as the stage that extracts patterns through particular algorithms inside that process. The paper also explains KDD as a multidisciplinary activity that meets databases, statistics, AI, and machine learning.

This flow is also loosely connected to the culture of data-based decision tools such as data warehouses, BI, and DSS. These are not AI models themselves, but they widened the practical environment in which data is stored, analyzed, and connected to judgment.

So it is useful to say that `AI moved from rules toward data-based judgment`. But AI itself did not mean only data-based judgment from the beginning. The safer expression is the following.

> To understand modern AI, it is better to say that on top of the layers of rules, search, knowledge representation, and probabilistic reasoning, a strong layer was added in which machine learning learns judgment criteria from data.

### Tying the Core Learning Terms Together Once

This section repeatedly uses `data`, `feature`, `representation`, `model`, and `parameter`. They are tied together here once as a baseline, and the later historical flow and examples assume this distinction.

| Term | English term | Meaning to fix first in this section |
| --- | --- | --- |
| data | data | observed or stored examples and values. Customer click logs, product photos, and collections of sentences are all data. |
| feature | feature | an input clue organized so that the model can read it more easily. For example, the number of words in an email, the number of links, and the sender domain can be features. |
| representation | representation | the result of transforming data into a form the model can handle internally. This is a broader term than feature, and in deep learning the model may learn this representation together with the task. |
| model | model | the computational structure that receives input and produces output such as prediction, classification, recommendation, or generation. |
| parameter | parameter | the values inside the model that are adjusted through learning. If those values change, the output for the same input can also change. |

At this stage, it is enough if the following distinction remains: `data is material`, `features and representations are ways of turning that material into a usable form`, `the model is the structure that performs judgment or generation`, and `parameters are internal values adjusted through learning`.

If `parameter` still feels especially abstract, it helps to think about why the answer of the model can change even for the same kind of input. Imagine a customer-churn model that looks at `number of logins in the last 30 days`, `whether there was a recent payment`, and `support history`. Before learning, it is not fixed which factor should matter more. During learning, the parameters inside the model are adjusted so that `no recent payment` may be treated more strongly, or `falling login count` may be treated more sensitively. In other words, a parameter is not a rule sentence written directly by a person. It is an adjustment value that reflects relations repeatedly found in data inside the model.

### Deep Learning: From Feature Design to Representation Learning

In machine learning, data does not simply enter the model in raw form. Usually it must be transformed into features or representations the model can handle.

For example, to decide whether an email is spam, one can create features such as word frequency, sender information, number of links, and title patterns. In images, one can think of features such as color, edge, texture, and shape. In traditional machine learning, the work of deciding what features to build was important.

Deep learning changed this point greatly. Deep learning is an approach that uses neural networks with multiple layers in order to learn useful representations from data together with the task. The Stanford Encyclopedia of Philosophy entry on AI also explains deep learning in connection with representation learning.

| Distinction | Typical flow of traditional machine learning | Typical flow of deep learning |
| --- | --- | --- |
| features | largely designed by people | the model learns the representation from data |
| model | relatively shallow models were often used | neural networks with multiple layers are used |
| strength | useful when data is limited or the structure is clear | strong on complex input such as image, speech, and language |
| burden | feature design and domain knowledge matter a lot | large data, computational resources, and careful evaluation matter a lot |

It would be misleading to understand deep learning as literally the same thing as a biological brain. The metaphor of neurons and synapses helps intuition, but artificial neural networks are not copies of the biological brain. Here deep learning is explained like this.

> Deep learning is an optimization process in which multi-layer neural networks with learnable weights find useful data representations and prediction rules.

In cases such as classification, language modeling, or generative models, where outputs can be interpreted through probabilities, deep learning can also be read as an attempt to find a strong probabilistic prediction model. But not every deep-learning model should be called an explicit probabilistic model. So here the book distinguishes among probabilistic models, representation learning, and optimization.

A very small example also makes the difference between `feature` and `representation` clearer.

| Problem | Example of features that people may build first | Example of representations that deep learning tries to learn more directly |
| --- | --- | --- |
| spam-mail classification | count of certain title words, number of links, sender domain | internal representations of word combinations, sentence patterns, and contextually strange phrasing |
| product-photo classification | average brightness, number of edges, proportion of a certain color | internal visual representations of surface texture, crack shapes, and part arrangement |
| speech recognition | strength in a certain frequency band, segment length | internal representations of pronunciation patterns, intonation changes, and contextually connected sound structure |

The key point of this table is this: `traditional machine learning tends to rely more on clues designed first by people`, while `deep learning tends to learn more of those clues themselves from data`.

### Generative AI: A Shift That Looks Visible as a Move from Judgment to Generation

Generative AI refers to AI models and services that create new content such as text, images, audio, video, and code. The NIST Generative AI Profile describes generative AI as a category of AI models that generate derived synthetic content by imitating the structure and characteristics of input data, and gives digital content such as image, video, audio, and text as examples.

The important point in this definition is that generative AI is not `a machine that tells facts`. It generates plausible outputs from the structure and patterns of the training data. So even if a generated result sounds natural, it does not automatically become a fact.

| Distinction | Central output | Example |
| --- | --- | --- |
| classification | a category | normal / defective, spam / normal |
| prediction | a value or score | sales prediction, churn probability |
| recommendation | a candidate list | product recommendation, document recommendation |
| generation | new content | sentence, image, code, speech |

One word of caution matters here: in AI contexts, `inference` can mean the runtime computation in which a trained model produces an output. By contrast, `reasoning` usually means logical thinking that follows grounds or steps. The fact that a generative AI system produces an output during inference does not mean that the output is always a logically reasoned fact.

### Where LLMs Sit in This Flow

LLMs, or large language models, are a representative model family inside generative AI, but they are not the same thing as generative AI as a whole. LLMs are large-scale language models trained mainly on language data. The LLM survey by Zhao and colleagues explains that language models developed from statistical language models to neural language models, then to pretrained language models, and then to large language models.

The important point in this section is not to treat LLMs as a sudden exception. They can be understood on top of the following flow.

```mermaid
--8<-- "assets/part-01/chapter-02/ai-history-bridge-flow-en.mmd"
```

This picture should not be read as if one technology erased the one before it. It should be read as showing that the center of AI explanation has gradually accumulated more layers over time. The key point is the cumulative flow: `rules -> handling uncertainty -> data learning -> representation learning -> generation`.

This is a cumulative relation, not a replacement relation. Modern AI services are not made only of LLMs. Search, databases, knowledge graphs, rule-based filters, permission control, evaluation, UI, and operational systems can all coexist in the same product.

So the safest way to read the flow of this section is the following.

> The center of AI explanation expanded from explicit rules and search toward probabilistic reasoning that handles uncertainty, and toward machine learning that learns patterns from data. Deep learning greatly expanded the ability to learn representations from data, and generative AI with LLMs is a recent strong case in which that representation learning, large-scale data, computational resources, and language modeling are combined.

### Reading It Again from a System View

If a traditional software function processes input through logic written directly by people, a machine-learning model can be viewed as processing input by using parameters learned from data. This analogy is useful for learning, but the model is not the same thing as the whole service.

In an actual service, the following flow can move together.

> user request -> input shaping -> model or tool execution -> result review -> response or business handling

Some stages can be fixed by rules, some can be strengthened by search, and some can be predicted or generated by models. The important point is not to give everything to AI. It is to identify the parts that can be repeated and verified, then compose them into a system.

In this section, that view is summarized in the following sentence.

> A modern AI service can be understood as a workflow that handles requests by combining logic written directly by people, models learned from data, search and tools, and verification procedures.

This sentence is a short summary meant to prevent the misunderstanding that `one model equals the entire service`. The first thing that should remain here is the view that `modern AI services are systems in which rules, search, models, and verification are tied together`.

### A Short Exercise in Separating the Flow

Look at the following cases and first distinguish whether the center of explanation is closer to `writing rules`, `machine learning`, `deep learning`, or `generative AI`.

| Case | First question to bring to mind | Closest center of explanation |
| --- | --- | --- |
| in internal expense handling, approval steps are decided by amount limits and rank rules | can a person write the standard directly in documents? | writing rules |
| customer churn is predicted from subscription length, payment history, and recent login frequency | what pattern repeats in past cases? | machine learning |
| subtle defect traces must be found automatically in product photos | should the model learn visual representations instead of people designing all the features? | deep learning |
| when a user writes one-line instructions, the system generates several draft advertising lines | does the task require creating new text? | generative AI |

The key to this exercise is not choosing a fashionable term. It is first separating whether the problem is one where `people should write the standard directly`, one where `patterns must be learned from data`, one where `representations need to be learned deeply`, or one where `new content must be generated`.

## Cases and Examples

### Case 1. Why Photo Classification Does Not Hold Up Well as a Pure Rule List

Imagine a conveyor belt in a factory where product photos are used to divide items into `normal` and `defective`. If a person writes rules, the system might begin with criteria such as `if a crack is longer than a certain length, mark it defective`, `if the number of stains exceeds a threshold, mark it defective`, or `if the color is darker than the standard, mark it defective`.

Even if those rules work at first, the real environment quickly introduces lighting changes, camera angle shifts, reflections, product position differences, and subtle pattern differences that make the appearance of the same defect keep changing. A person may still grasp the similar visual feel when looking at the photo, but writing all of that out as pixel-level rules rapidly becomes difficult.

So the center of explanation moves from `what additional rules should be written?` to `what patterns should be learned from many normal and defective photos?` Machine learning designs features, deep learning learns richer representations, and generative AI extends further toward producing new content.

This case ties together the historical flow of 2.3 in one sentence. It is not that rule-based approaches became useless. It is that as complex inputs that are hard to write directly became more common, approaches that learn relations from data moved to the center.

## Checklist

- I can explain why problems that are hard to solve through rule-based approaches alone led toward data-based learning.
- I can explain machine learning as an approach that improves model performance from data or experience.
- I can explain that data mining and KDD are connected to a culture of data-based judgment, but are not exactly the same thing as machine learning.
- I can explain deep learning as a neural-network-based approach that reduces feature design and learns representations.
- I can explain that generative AI is a category of models and services that generate new content, and that generated content is not automatically factual.
- I can treat LLMs as a representative case of generative AI without equating them with generative AI as a whole.
- I can view a modern AI service not as one model alone, but as a workflow combining rules, search, data, models, and verification.
- I can explain that machine learning, deep learning, and generative AI are different names, but can be read as one flow of `rules -> data learning -> representation learning -> generation`.
- I can explain that newer approaches did not completely replace earlier ones, and that rules, search, knowledge representation, probabilistic reasoning, data mining, machine learning, deep learning, and generative AI can be mixed inside real systems.

## Sources and Further Reading

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Usama Fayyad, Gregory Piatetsky-Shapiro, Padhraic Smyth, [From Data Mining to Knowledge Discovery in Databases](https://www.kdnuggets.com/gpspubs/aimag-kdd-overview-1996-Fayyad.pdf){: target="_blank" rel="noopener noreferrer" }, AI Magazine, 1996, accessed 2026-06-22.
- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://doi.org/10.6028/NIST.AI.600-1){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, accessed 2026-06-22.
- Wayne Xin Zhao et al., [A Survey of Large Language Models](https://arxiv.org/abs/2303.18223){: target="_blank" rel="noopener noreferrer" }, arXiv:2303.18223, accessed 2026-06-22.
