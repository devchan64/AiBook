# P1-2.1 Symbolic AI and Rule-Based Approaches

> Section ID: `P1-2.1`
> Version: `v2026.07.20`

P1-1 organized the scope of the word AI and the relationship among the major terms. P1-2 turns to the historical paradigms through which AI tried to solve problems. The center of this section is `symbolic AI` and the `rule-based approach`.

Symbolic AI is an approach that tries to represent human knowledge through symbols, rules, logic, and explicit representation, then manipulate that representation to obtain a conclusion or action. In simpler words, it begins from the idea that we can write human knowledge in a form a computer can handle, then make the computer reason over that form.

In Part 1, the baseline meaning of `symbolic AI`, `rule-based approach`, and `knowledge representation` is fixed here. Even when these terms appear again in later sections, only the amount needed for the local question should be reconnected. When the fuller definition needs to be checked again, return to this section and the shared [Concept Glossary](/AiBook/reference/concept-glossary/).

## Writing Knowledge as Symbols and Rules

This section organizes the following questions.

- What was symbolic AI trying to do?
- In what larger flow are rules, knowledge representation, inference, and search connected?
- Why is this approach still valid in some systems today?

This section first closes `how symbolic AI tried to write and handle knowledge and rules`. The detailed flow of search, knowledge representation, and probabilistic inference continues in the next section, `P1-2.2`, and a more concrete evaluation of the strengths and limits of rule-based systems continues in Part 1 Chapter 3.

## Strengths and Limits of Rule-Based Approaches

- Understand what symbolic AI was trying to do.
- See how rules, knowledge representation, inference, and search connect.
- Distinguish the strengths and limits of rule-based approaches.
- Understand why this approach is still useful in some systems today.

## Concepts to Connect First

This section is the representative place where the baseline for the core Chapter 2 terms is fixed. The concepts below are introduced here only to establish their role. When a fuller definition is needed, return to the corresponding glossary entry.

| Concept | Meaning to fix first here | Why it is needed now |
| --- | --- | --- |
| [symbolic AI](/AiBook/reference/concept-glossary-parts/01-giyeok/#aisymbolic-ai) | an AI approach centered on symbols, rules, and explicit knowledge representation | to establish the starting point that later learning-based approaches are contrasted against |
| [rule-based system](/AiBook/reference/concept-glossary-parts/01-giyeok/#rule-based-system) | a system that compares current facts with rules to decide a conclusion or action | to see a concrete implementation shape of symbolic AI |
| [knowledge representation](/AiBook/reference/concept-glossary-parts/09-jieut/#knowledge-representation) | a format for writing facts, relations, and rules | to define what it means for a system to be treated as knowing something |
| [fact](/AiBook/reference/concept-glossary-parts/07-siot/#fact) | information treated as true in the current state | to separate the input material to which rules are applied |
| [inference engine](/AiBook/reference/concept-glossary-parts/11-chieut/#inference-engine) | a mechanism that finds and applies rules matching the current facts | to see the execution structure between rules and conclusions |

## Main Learning Points

This section may look like history, but in practice it introduces one old and important way in which AI tried to solve problems. The three guideposts below are the overall map.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| symbolic AI is a way of `writing knowledge explicitly` | This creates the contrast with later machine learning. | Distinguish that people write the rules and facts first. |
| a rule-based approach is a way of `determining a conclusion or action by condition` | This makes it easier to connect the idea to everyday rules. | See the structure that matches the current situation against rules and produces a result. |
| this approach is `not a vanished past` but something that still remains in parts of modern systems | This prevents it from being misunderstood as a completely disconnected old technology. | Connect it to policy, permission, and safety rules that still remain today. |

`symbol`, `rule`, `fact`, `knowledge representation`, and `inference` can sound similar early on. In this section they are separated like this.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| symbol | a marker that gives something a name and separates it from other things | the unit that lets people and systems refer to the same target |
| rule | a criterion that determines a conclusion or action by condition | an explicit judgment standard |
| fact | information treated as true in the current state | the input material for rule application |
| knowledge representation | a format for writing facts, relations, and rules | the frame that defines what the system is considered to know |
| inference | the process of obtaining a conclusion from given facts and rules | the procedure that produces a result |

The first distinction that should remain is this: what is named explicitly, what is written down as a rule, what counts as fact in the current state, and what conclusion is drawn from the two.

## Detailed Learning

### Why This Approach Appeared First

One of the large questions early AI researchers faced was: how can intelligent behavior be turned into a computer program? One major line of thought was to write down the facts, rules, and reasoning procedures that people know explicitly, then let the computer manipulate them and draw a conclusion.

The Stanford Encyclopedia of Philosophy entry on logic-based AI explains that John McCarthy tried to formalize commonsense reasoning by using ideas from philosophical logic. In that line of thought, intelligence was often treated as a process of manipulating symbolically represented facts and rules in order to obtain a conclusion or action.

Rule-based approaches made this idea easier to turn into real systems. If an expert writes judgment standards as explicit rules involving conditions, situations, patterns, conclusions, and actions, a computer can compare the current facts against those rules and produce a conclusion. Early expert systems depended on large sets of procedural rules, and later work emphasized the need for separate knowledge representation to express background knowledge more systematically.

So symbolic AI and rule-based approaches should not be read as merely old technology. They are better understood as an important early AI strategy: write knowledge explicitly, then reason over that knowledge.

### Why Is It Called “Symbolic”?

The word `symbol` here is different from the symbolic meaning used in literature or art. In AI history, a symbol is closer to an explicit marker or label that a computer can distinguish and manipulate. Examples include `rain`, `wet road`, `patient`, `symptom`, `position of chess pieces`, and `rule A`: markers that stand for an object, state, concept, or relation.

In this book, `symbolic AI` is the default expression. Terms such as “symbolic artificial intelligence” or “symbol-centered AI” can appear elsewhere, but the point is the same: an approach that uses symbols, rules, and explicit representation as the main way to implement intelligence.

Because several related expressions can appear together, it helps to read them with the following distinction in mind.

| Expression | English term | Meaning in this book |
| --- | --- | --- |
| symbolic AI | symbolic AI | the default expression in this book; a broad approach centered on symbols, rules, and explicit knowledge representation |
| logic-based AI | logic-based AI | a symbolic-AI family that uses logical forms and inference rules strongly |
| rule-based approach | rule-based approach | an implementation style that organizes judgment through rules that map condition, situation, or pattern to conclusion or action |
| classical AI | classical AI | a broad label for pre-deep-learning AI; its scope is wide, so the local context still matters |

If this is your first encounter with symbolic AI, the simplest first picture is: give the computer human-readable labels and rules, then let it manipulate them to reach a conclusion.

### The Attempt to Represent the World Through Symbols

The starting point of symbolic AI is the belief that knowledge can be represented explicitly. People can express world knowledge in sentences, rules, symbols, and relations: “If it rains, roads become wet,” “a certain combination of symptoms suggests a disease,” or “this move changes the chess position in this way.”

Symbolic AI tried to turn such expression into structures a computer could handle. The main ingredients are the following.

| Component | English term | Role |
| --- | --- | --- |
| symbol | symbol | marks an object, concept, or state that people or systems can distinguish |
| rule | rule | expresses what conclusion or action should follow under a certain condition |
| knowledge representation | knowledge representation | the format that stores and handles facts, relations, concepts, and rules |
| inference | reasoning, inference | the process of deriving a new conclusion from given knowledge |
| search | search | the process of moving through possible states or candidate solutions to find a goal |

From this perspective, an AI system solves problems not mainly by automatically learning patterns from data, but by using knowledge and rules that people have organized in advance. That is why symbolic AI is deeply connected to directly writing rules, deriving conclusions through logic, and exploring possible states through search.

A common confusion for beginners is that `rule`, `inference`, and `search` can all look like similar processing steps. Their roles are different.

| Element | What is given first | What it actually does | Short example |
| --- | --- | --- | --- |
| rule | a connection between condition and conclusion | writes down what judgment should be used in what situation | `If payment exceeds the limit, require an extra approval.` |
| inference | current facts and rules | applies the matching rule to the current facts and produces a conclusion | `The limit is exceeded, so extra approval is required.` |
| search | possible states or next choices | follows candidates to find a goal state or solution | trying candidate next moves in chess |

So a rule is closer to a `judgment standard`, inference is closer to `applying the current standard`, and search is closer to `finding a path among possibilities`. In real systems the three often appear together. A game AI may express how pieces can move through rules, search through available moves on the current board, and use inference to judge which move is better.

### The Basic Shape of a Rule-Based Approach

A rule-based approach shows symbolic AI in one of its easiest-to-understand forms. The core idea is to compare current facts or situations against explicit rules and then determine a conclusion, classification, action, or processing procedure.

> condition or situation or pattern -> conclusion or classification or action or procedure

`IF condition THEN conclusion` is a simple notation often used to explain such rules. But a rule-based approach as a whole does not have to be written only in that grammar. Rules can appear in several forms.

| Situation | Example rule | Result |
| --- | --- | --- |
| everyday judgment | if it is raining and you are going out, take an umbrella | action decision |
| workflow handling | if the payment amount exceeds the approval limit, send it to the manager approval step | procedure selection |
| classification | if the blood pressure, temperature, and symptom combination enters the criterion range, classify it as requiring further review | classification or warning |
| access control | if the user's role is not `admin`, do not allow a settings change | allow or block |
| recommendation | if customer grade, purchase history, and inventory state match the condition, prioritize a certain product group | recommendation adjustment |
| safety policy | if an input matches a prohibited request type, stop the response or switch to a safer reply | policy application |

The same content can be rewritten in `IF-THEN` form like this.

> IF it is raining THEN take an umbrella  
> IF the payment amount exceeds the approval limit THEN send it to the manager approval step  
> IF temperature is high and there is a cough THEN check the possibility of infection  
> IF the user's role is not admin THEN block the settings change

These examples are too simple to be used directly as medical, business, or security rules. What matters here is the structure. A rule-based system collects facts and rules, then applies the rules matching the current situation to produce a conclusion.

```mermaid
--8<-- "assets/part-01/chapter-02/rule-based-decision-flow-en.mmd"
```

This diagram helps you read a rule-based system as four parts: `current facts`, `explicit rules`, `application procedure`, and `conclusion`. The key point is structural: facts alone are not enough, rules alone are not enough, and a separate procedure is needed to match them and produce a conclusion.

An expert system is a representative case in which this rule-based approach developed into an applied system. It tried to organize expert judgment as rules and knowledge in order to support diagnosis, classification, recommendation, or decision-making in a specific domain. This section first holds onto the basic way of thinking behind symbolic AI and rule-based approaches, and the strengths and limits that appear when they become real applications are revisited in `P1-3.1`.

A tiny example makes the structure clearer. Imagine that an online store return screen receives the following facts.

| Current fact | Value |
| --- | --- |
| seller fault | yes |
| customer remorse | no |
| bundled order | yes |

Suppose the system has the following rules.

- if the seller is at fault, refund the shipping fee
- if the return is customer remorse, the customer pays the shipping fee
- if it is a bundled order, recalculate by item instead of by whole order

Then the system can output both the conclusion `refund shipping fee` and the procedure `recalculate by item`. The key point of this example is that a rule-based approach can produce a judgment from `current facts` and `explicit rules` without requiring complex learning.

At the same time, the same structure shows why rule conflicts arise. Imagine that one team adds the rule `if the seller is at fault, refund the shipping fee`, while another team separately adds an operational rule such as `if it is a bundled order, the customer temporarily prepays shipping and settlement happens later`. If the current facts are both `seller fault` and `bundled order`, both rules match and the system can produce conflicting handling directions at once. Then extra design is needed: which rule has priority, whether to create a separate exception rule, or whether to hand the case to human review. The important beginner-level takeaway is that a rule-based system is not just a structure where you add many rules. It is also a structure where rule priority and conflict resolution must be designed together.

### Logic-Based AI and Knowledge Representation

If a rule-based approach is closer to organizing judgment by applying explicit rules, logic-based AI is a more formal line of work that tries to express knowledge and reason over it through structured languages. The Stanford Encyclopedia of Philosophy entry on logic-based AI explains that John McCarthy tried to formalize commonsense reasoning and apply ideas from philosophical logic to AI.

This line of work raises questions such as the following.

- In what language should facts and relations in the world be expressed?
- From that expression, what conclusions should be treated as following?
- When new information arrives, how should earlier conclusions be revised?
- How should action and change over time be represented?
- How should common-sense knowledge, which is ambiguous and full of exceptions, be handled?

These questions have not disappeared in modern AI. Even when using LLMs or deep-learning models, service policy, permission control, safety filters, workflow rules, and verification logic are still often managed as explicit rules.

### Strength: Easier to Explain and Control

One strength of symbolic AI and rule-based approaches is that people can read the structure.

- The rules are explicit, so it is easier to trace what condition led to what conclusion.
- Domain experts can directly review and revise the knowledge.
- It fits domains in which explicit standards matter, such as law, policy, and business procedure.
- It is easier to control the system so that the same input leads to the same output.
- It is comparatively easy to explain why the system made that judgment.

That is why rule-based approaches are old but not gone. Even inside modern AI services, rules remain useful in explicit and repeatable parts such as permission checks, banned-term filters, parts of policy-violation detection, workflow validation, and routing rules.

### Limit: Not All Knowledge Can Be Written as Rules

The limits are just as clear. Real-world problems contain many exceptions, change often, and can be hard for people to explain precisely in rules.

For example, recognizing an object from an image, understanding natural sentences, or distinguishing subtle differences in speech are things people can do, but it is hard to write all the necessary rules explicitly in language. In such problems, approaches that learn patterns from data can become stronger.

Representative limits of rule-based approaches are the following.

- Writing and maintaining rules directly is costly.
- As exceptions increase, rules become more complex and can conflict.
- The system is weak on situations that were not expressed in rules.
- It can be vulnerable to ambiguous input, noisy data, and incomplete information.
- Its ability to improve representation by learning on its own is limited.

So it is too simple to say that rule-based AI was wrong and machine learning is right. A more accurate reading is that problem characteristics differ. Some problems are sufficiently handled by explicit rules, while others are better solved by learning patterns from data.

### A Short Exercise for Judging Where It Fits

If you look at the cases below and first judge whether they are better to start with a rule-based approach, a learning-based approach, or both together, the boundary of this section becomes clearer.

| Case | First question to ask | First-pass judgment in this section |
| --- | --- | --- |
| In internal expense settlement, should requests over a rank-based approval limit be sent to an extra approval step? | Is the standard written clearly in documents? | Good to start with a rule-based approach. |
| Should a system read customer inquiry sentences and automatically classify complaint type? | Are the expressions highly varied with many exceptional sentences? | A learning-based approach may be more necessary. |
| Should a generative AI answer be blocked when a prohibited topic request appears? | Are policy rules explicit, and is contextual judgment also needed? | Rules and learning-based judgment are often used together. |
| Should factory sensor values be used to predict failure in advance? | Can people write all patterns as rules? | A learning-based approach is often more suitable. |

The key to this exercise is not to read `rule-based` as an outdated method. It is to read it as an approach that especially fits problems with strong explicit standards. Conversely, when input is ambiguous and patterns are complex, the limits of rules alone grow and pattern learning from data becomes more important.

## Cases and Examples

### Case 1. A Customer Center Where People Used to Check Shipping-Fee Refund Rules Manually

Imagine an online shopping customer center where an agent directly decides whether a shipping fee should be refunded. The person checks one criterion at a time: whether there was seller fault, whether it was a wrong shipment, whether it was customer remorse, and whether the free-shipping condition was satisfied.

At first the standard can look clear, but real inquiries soon add exceptions such as `partial refund`, `coupon use`, `bundled order`, and `cases where seller fault and customer fault coexist`. If a human handles everything by experience, the process can feel fast, but different staff members may judge differently and it becomes harder to trace later why a certain decision was made.

A rule-based approach writes those standards explicitly, then compares current order information against the rules and produces a conclusion. For example, a knowledge base can include rules such as `if the seller is at fault, refund the shipping fee`, `if it is customer remorse, the customer pays`, and `if it is a bundled order, recalculate by item instead of by whole order`.

The important point in this case is that a rule-based system does not erase human judgment standards. It converts repeated judgment criteria into a readable form. At the same time, it also reveals the limit that rule management becomes more complex as exceptions increase.

### A Loose Connection to Data Labeling

Data labeling is also loosely connected to this perspective. In supervised learning, a label is close to an answer, name, or category attached to data. If you attach labels such as `cat`, `dog`, `normal`, or `defective` to images, a model learns the relation between input features and labels.

In that sense, a label can be viewed like a symbol because it is an explicit name attached by a person to distinguish the world. But data labeling should not be treated as the same thing as symbolic AI. Data labeling is mainly a process of preparing data for a machine-learning model to learn from, whereas symbolic AI is an approach that tries to reason by directly manipulating symbols and rules themselves.

So in this section, the relation between the two only needs to be remembered like this.

> A label is an explicit name tag inside learning data, so it can be seen as one contact point between symbolic AI and machine learning. But labeling is not a reasoning method. It is a way of constructing learning data.

The more detailed relation among label, data, input, and output is organized again in `P1-4.2`. Here it is enough to keep only the connection that a label can be read as an explicit name tag attached by a person.

## Checklist

- I can explain that symbolic AI centers on symbols, rules, knowledge representation, and inference.
- I can explain that a rule-based approach uses explicit rules that determine a conclusion or action according to condition, situation, or pattern.
- I can explain that rule-based approaches are strong in explainability and controllability.
- I can explain the limit that not all knowledge is easy to write as rules.
- I can explain that data labels can be read like symbols, but that data labeling and symbolic AI should not be treated as the same thing.
- I can read rule-based approaches and learning-based approaches not as a simple ranking of better and worse, but as a difference in problem characteristics.
- I can explain that data labels can be seen like symbols, but data labeling is not the same thing as symbolic AI.
- I can explain that rule-based and learning-based approaches should be compared by problem character, not as a simple better-or-worse ranking.
- I can explain that symbolic AI tried to represent knowledge through human-readable symbols and rules, then perform inference and search over that representation.
- I can explain that this approach is strong in explainability and controllability, but showed limits in handling real-world ambiguity, exceptions, and large-scale pattern recognition.

## Sources and Further Reading

- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/){: target="_blank" rel="noopener noreferrer" }, substantive revision 2024-02-27, accessed 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed.](https://aima.cs.berkeley.edu/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
