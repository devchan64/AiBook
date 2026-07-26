# P1-2.2 Search, Knowledge Representation, and Probabilistic Reasoning

> Section ID: `P1-2.2`
> Version: `v2026.07.26`

Section 2.1 covered symbolic AI and rule-based approaches. This section takes the next question. When writing rules alone is not enough, AI had to search through possible candidates, represent the knowledge it needed, and reason about plausible conclusions under incomplete information.

The task here is not to study algorithms in detail. The task is to fix why `search`, `knowledge representation`, and `probabilistic reasoning` keep returning in introductory AI, and how this flow becomes part of the background for later explanations of machine learning and deep learning.

In Part 1, the baseline distinction between `search` and `probabilistic reasoning` is fixed here. `Knowledge representation` was introduced in 2.1, and is reconnected here only as much as needed to compare its role between search and probabilistic reasoning. If the term boundaries become blurry again later, return to this section and to the glossary entries for [search](/AiBook/en/reference/concept-glossary-alpha/s/#search), [probabilistic reasoning](/AiBook/en/reference/concept-glossary-alpha/p/#probabilistic-reasoning), and [knowledge representation](/AiBook/en/reference/concept-glossary-alpha/k/#knowledge-representation).

This section organizes the following questions.

- Why was search a core early AI problem-solving method?
- How does knowledge representation connect to rule-based approaches?
- How did probabilistic reasoning try to handle incomplete information and uncertainty?

The focus here is on organizing the `difference in role` among the three flows. The reason the center of explanation later moves toward learning patterns from data is recovered in the next section, 2.3.

## Different Roles of Search, Knowledge Representation, and Probabilistic Reasoning

- Understand why search was a core early AI problem-solving method.
- See how knowledge representation connects to rule-based approaches.
- Understand that probabilistic reasoning is a way to deal with incomplete information and uncertainty.
- Distinguish search, knowledge representation, and probabilistic reasoning as major axes of pre-machine-learning AI.

## Concepts to Connect First

This section is the representative place in Chapter 2 where the role difference among `search`, `knowledge representation`, and `probabilistic reasoning` is first separated in earnest. The concepts below are introduced first by role; when a fuller definition is needed, return to each glossary entry.

| Concept | Meaning to fix first here | Why it is needed now |
| --- | --- | --- |
| [search](/AiBook/en/reference/concept-glossary-alpha/s/#search) | an approach that follows possible states and actions to find a goal | to see why candidate order becomes a problem when there are too many options |
| [knowledge representation](/AiBook/en/reference/concept-glossary-alpha/k/#knowledge-representation) | a format for writing facts, relations, and constraints | to separate the question of what the system should count as knowledge |
| [probabilistic reasoning](/AiBook/en/reference/concept-glossary-alpha/p/#probabilistic-reasoning) | a way to handle plausibility under incomplete information | to read judgments that do not close into simple true or false form |
| [goal](/AiBook/en/reference/concept-glossary-alpha/g/#goal) | the condition to be reached | to see what tells search where to stop |

## Main Learning Points

At this stage the flow can scatter because the terms seem to split in three directions. The three guideposts below are the larger map.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| search is a problem of `where to look first when there are too many candidates` | This shows why rules alone are not enough. | Distinguish that too many possible choices require order. |
| knowledge representation is a problem of `what should be written down as known` | This connects why rules, facts, and relations are discussed separately. | Organize the idea that the standard for solving the problem must be written in a form a computer can handle. |
| probabilistic reasoning is a way of handling `how plausible something is under incomplete information` | This connects AI to real problems that do not fit into simple true/false form. | Connect probability to judgment under ambiguity. |

`state`, `action`, `goal`, `representation`, and `probability` can feel unfamiliar when they appear together. In this section they are separated as follows.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| state | the current shape of the problem | the reference point that shows where search starts |
| action | a choice that changes the state | the unit that creates the next candidate |
| goal | the condition to be reached | the criterion that decides where search stops |
| representation | the way the system writes the facts and relations it knows | the basis for judging candidates |
| probability | a value that indicates how plausible a conclusion is | the language that helps judgment when information is incomplete |

The first distinction that should remain is this: `search handles state, action, and goal`; `knowledge representation decides what to write down`; and `probabilistic reasoning handles plausibility under ambiguous information`.

## Detailed Learning

### Three Questions After Rules

Rule-based approaches explicitly express what conclusion or action should follow under a condition. But real problems often do not end with a single rule.

Imagine choosing a delivery route. The destination is fixed, but there are many possible roads, road conditions can change, and some information is incomplete. At that point an AI system has to deal with the following questions together.

| Question | Connected approach | Core meaning |
| --- | --- | --- |
| When there are many candidates, what should be examined first? | search | find a goal by following states and paths |
| What must the system know in order to solve the problem? | knowledge representation | express facts, relations, constraints, and rules in a form the computer can handle |
| When information is incomplete or noisy, what is more plausible? | probabilistic reasoning | calculate the probability or confidence of possible conclusions from observed evidence |

These three questions are separate, but in real AI systems they often appear together. Search finds candidates, knowledge representation provides the standards for judging them, and probabilistic reasoning handles which candidate is more plausible under uncertainty.

The same problem becomes clearer when divided into the three viewpoints.

| Example problem | Search question | Knowledge representation question | Probabilistic reasoning question |
| --- | --- | --- | --- |
| map route finding | What route should be chosen from the current position to the destination? | How should roads, intersections, one-way restrictions, and travel modes be represented? | How should expected time, congestion, and accident risk be reflected? |
| delivery robot | In what order should it move, pick up objects, and place them down? | How should robot location, object location, destination, and load state be represented? | How should uncertain sensors or the possibility that a door is closed be handled? |
| game agent | What position should it move to next, or what move should it make? | How should location, remaining resources, acquired items, and goal state be represented? | How should the opponent's action or an unobserved state be estimated? |

The open textbook by Poole and Mackworth also uses path finding, delivery robots, and grid games as examples of search and state spaces. Here, instead of copying the original examples directly, the structure is generalized into a learning-oriented form.

### Search: Finding a Goal Among Possible States

Search is an approach that follows possible states and actions in order to find a way to reach a goal. It appears in route finding, puzzles, games, planning, and scheduling whenever there are many possible choices.

A search problem can be simplified into the following components.

| Component | English term | Example |
| --- | --- | --- |
| initial state | initial state | current location, current board state, current schedule |
| possible action | actions | move, move a piece, change task order |
| next state | transition/result | the changed location or state after an action |
| goal check | goal test | destination reached, puzzle solved, condition satisfied |
| cost or evaluation | cost/evaluation | distance, time, risk, score |

This structure maps directly to real examples.

| Example | State | Action | Goal | Cost or evaluation |
| --- | --- | --- | --- | --- |
| map route finding | current location, travel mode, direction of progress | move along roads and intersections | reach destination | distance, time, cost, energy |
| delivery robot | robot location, carried item, items not yet delivered | move, pick up, put down | designated items reach the destination | travel distance, time, battery, failure risk |
| grid game | agent location, fuel, collected coins | move up/down/left/right, recharge, collect coins | collect all coins and reach the goal location | number of moves, remaining fuel, avoiding danger zones |

If every candidate could be checked all the way to the end, search would look simple. But in real problems the number of candidates grows quickly. Looking several moves ahead in a game, choosing a route through many cities, or making a schedule with many constraints can all produce an explosive number of combinations.

That is why heuristics become important in search. A heuristic is not a formula that guarantees the correct answer. It is an experience-based standard that lets the system examine more promising-looking candidates first. A straight-line distance to the destination, the current score, or the number of remaining constraints can all help decide the search order.

One place beginners often get confused is that `heuristic` and `probability` can both look like numbers. But the two values answer different questions.

| Distinction | First question answered | Role of the value | Short example |
| --- | --- | --- | --- |
| heuristic | `Which candidate should be examined first?` | an experience-based criterion that decides search order or priority | inspect the route with a shorter straight-line distance first |
| probability | `Which conclusion is more plausible?` | a value that expresses confidence for possible conclusions under incomplete information | this symptom combination makes disease A more likely |

So a heuristic is closer to `search order`, and probability is closer to `degree of belief`. A real system can contain both, but they do not mean the same thing.

For example, when choosing a delivery route, a system might use `straight-line distance to the destination` as a heuristic to narrow the candidates it examines first, while also calculating `the probability that a certain road segment will be delayed because of rain` in order to judge which route is more unstable. The first value helps search order, and the second reflects uncertainty. Both can look like numbers, but they do different jobs in the system.

```mermaid
--8<-- "assets/part-01/chapter-02/search-heuristic-flow-en.mmd"
```

This diagram helps you read search as the flow `initial state -> candidates -> evaluation criterion -> goal`. The key point is structural: to solve the problem, the system must generate candidates, and it needs a criterion for which ones to inspect first.

This section does not go deeply into search algorithms themselves. Breadth-first search, depth-first search, A* search, game search, and heuristic functions return in Part 1 Chapter 7. Here it is enough to remember search as `a way to find a path to the goal when there are too many possible candidates`.

### Knowledge Representation: What Should Count as Known

If search is the process of finding candidates, knowledge representation is the process of organizing what the system must know in order to judge those candidates.

The rule-based approach from 2.1 is one form of knowledge representation. But knowledge representation is broader than a simple rule list. Facts, relations, concepts, constraints, changes over time, results of actions, and exception conditions can all become representation targets.

For example, a delivery-planning system may need to handle the following kinds of knowledge.

| Knowledge | Example representation |
| --- | --- |
| place | warehouse, customer address, intermediate hub |
| relation | roads are connected, a certain segment is one-way |
| constraint | refrigerated items must be delivered within a certain time |
| action | when a vehicle moves, its location and remaining time change |
| goal | finish all deliveries while reducing cost |

The core of knowledge representation is the question, `what should be represented in what unit?` The same fact can be handled differently depending on the chosen form.

| Fact to represent | Example representation form | Meaning |
| --- | --- | --- |
| object `a` is red | `red(a)` | uses `red` like an attribute |
| the color of object `a` is red | `color(a, red)` | uses `red` as a value and expresses color as a relation |
| `a` is a parcel | `type(a, parcel)` or `is_a(a, parcel)` | expresses what category an entity belongs to |
| Alex gave Chris a book | `agent(event, alex)`, `recipient(event, chris)`, `patient(event, book)` | creates an event as an entity and expresses participant relations |

When Poole and Mackworth explain a knowledge graph, they discuss triple representation composed of subject, verb, and object. Borrowing only that structure, you can read a fact such as `item A is in warehouse B` as a `subject-relation-object` connection. The important point is that representation is not just a storage format. It is a structure that makes certain questions easier to ask.

The Stanford Encyclopedia of Philosophy entry on logic-based AI explains that early expert systems relied on large procedural rule sets, but later the need for a separate knowledge-representation component to express background knowledge became larger. In other words, AI did not only think about executing rules. It also thought about how to structure rules, facts, relations, and background knowledge.

That perspective remains in modern AI. Even when a machine-learning model learns patterns from data, explicit representation such as service policy, domain knowledge, permission structure, data schema, knowledge graphs, and search indexes is still needed.

### Probabilistic Reasoning: Calculating Plausibility Under Incomplete Information

Rules and logic are strong when the structure is `if the condition is true, then the conclusion follows`. But real information is often incomplete, observations contain noise, and the same evidence can support multiple conclusions.

The following questions are difficult to handle through simple true/false rules alone.

| Situation | What is uncertain |
| --- | --- |
| infer a disease from symptoms | the same symptom can appear in several diseases |
| decide whether an email is spam | a few words alone do not make certainty possible |
| detect an obstacle from sensor data | sensor values may contain noise or missing signals |
| predict customer churn | past behavior does not fully determine future behavior |

In probabilistic reasoning, uncertain targets can be represented as random variables. For example, a variable such as `Has_cough` can take true/false values, and a variable such as `Sensor_distance` can take continuous values. These examples show that AI does not simply collapse the uncertain world into one number. It chooses observable variables and the range of possible values they can take.

| Uncertain target | Example random variable | Possible values |
| --- | --- | --- |
| whether a patient is coughing | `Has_cough` | `true`, `false` |
| obstacle distance read by a sensor | `Sensor_distance` | distance values greater than or equal to 0 |
| the shape of an object | `Shape` | `circle`, `triangle`, `star` |
| whether a shape is filled | `Filled` | `true`, `false` |

Probabilistic reasoning uses probability to handle the plausibility of such conclusions. The Stanford Encyclopedia of Philosophy entry on AI describes probabilistic reasoning as calculating the probability of a hypothesis from observed evidence, and explains that probabilistic methods and Bayesian networks became important in AI after the 1990s.

The important point here is that probabilistic reasoning does not mean `answering at random`. Probability is a language for organizing uncertainty. If the observed evidence changes, the plausibility of the conclusion can also change.

Bayes' rule and Bayesian networks return later, and the difference among probability, uncertainty, and stochastic behavior returns in Part 1 Chapter 6. Here it is enough to remember probabilistic reasoning as `a way to calculate the plausibility of possible conclusions under incomplete information`.

### How the Three Flows Connect

Search, knowledge representation, and probabilistic reasoning begin from different questions, but they can be used together.

```mermaid
--8<-- "assets/part-01/chapter-02/search-knowledge-probability-flow-en.mmd"
```

This picture shows that the three flows are not competing, but are connected by different roles in solving the same problem. The key point is the division of labor: `knowledge representation` writes the foundation, `search` finds candidates, and `probabilistic reasoning` calculates ambiguous information to help the conclusion.

Imagine a robot moving objects in a warehouse.

- Knowledge representation expresses the warehouse layout, corridors, objects, robot state, and constraints.
- Search finds possible movement paths and task orders.
- Probabilistic reasoning calculates which judgment is more plausible when sensors are uncertain or corridor conditions change.

This flow shows that AI did not stop at being just `a program that executes rules`. AI also developed search for handling many candidates, representation for structuring knowledge about the world, and probabilistic reasoning for mathematically handling uncertainty.

### Practice Reading the Same Problem Through Three Viewpoints

When looking at one problem, the three terms can keep blending together. In those cases, it helps to separately write down `what is being searched for`, `what must be written down`, and `what is uncertain`.

For example, imagine a delivery app assigning orders on `a rainy evening`.

| Distinction | First question to write down in this situation | Example answer |
| --- | --- | --- |
| search | Which rider should receive which order in what sequence so that total delivery time becomes shortest? | The system must compare candidates for assignment order and movement route. |
| knowledge representation | What must the system know in order to make the judgment? | It must represent rider location, order address, store location, delivery zone, and priority rules. |
| probabilistic reasoning | What is not certain? | There is a possibility of increased travel time because of rain, congestion in certain areas, and rider arrival delay. |

The important point when reading this table is that the three questions do not compete. Even inside the same delivery system, `choosing among candidates` is closer to search, `structuring the world in written form` is closer to knowledge representation, and `dealing with fluctuating expected time` is closer to probabilistic reasoning.

### A Short Practice in Distinguishing Them

Look at the following cases and first classify which one is closer to search, knowledge representation, or probabilistic reasoning.

| Case | First central question to grab | Closest flow |
| --- | --- | --- |
| a one-day training schedule must be arranged while matching meeting rooms, speakers, and equipment constraints | which order and arrangement should be chosen among the possible combinations? | search |
| in an internal permission system, department, role, approval stage, and exception rules must be structured | what facts and relations should be written in what form? | knowledge representation |
| when factory sensor values fluctuate, the system must judge whether equipment is abnormal | given the currently observed values, which conclusion is more plausible? | probabilistic reasoning |
| a warehouse robot knows the corridor layout but encounters unstable sensors while moving | how should route candidates, warehouse structure, and sensor uncertainty be handled together? | all three flows are needed together |

The key to this exercise is not memorizing the three terms separately. It is first separating whether the problem is about `finding candidates`, `writing the world down`, or `judging ambiguous information`. Real systems often use all three together, but if you separate the central question, the role becomes much clearer.

## Cases and Examples

### Case 1. Why a Warehouse Robot Cannot End with Rules Alone

Imagine a robot in a warehouse that picks up an item and moves it to a delivery area. When a person describes the procedure, it may sound simple: `pick it up from shelf A`, `move along the corridor`, and `put it down in the delivery area`.

But in a real environment, there can be several possible routes, one corridor can become blocked so another path must be chosen, and the sensors can misread an object. In that situation, simple rules alone do not fully explain `which candidate should be examined first`, `how the warehouse structure should be represented`, or `which judgment is more plausible when sensor values are ambiguous`.

Search chooses an order among multiple route candidates that reaches the goal. Knowledge representation structures shelves, corridors, objects, load state, and forbidden zones. Probabilistic reasoning handles uncertain information such as sensor error or corridor occupancy. That means the same robot problem can require all three flows together.

The key point to read from this case is that `finding candidates`, `writing the world down`, and `judging ambiguous information` appear at the same time inside a real system.

## Checklist

- I can explain that search is a way of finding a goal by following possible states and actions.
- I can explain that a heuristic is an experience-based criterion for reducing search candidates or deciding their order.
- I can explain that knowledge representation can include not only rules but also facts, relations, constraints, and the results of actions.
- I can explain that probabilistic reasoning is a way of calculating the plausibility of conclusions under incomplete information.
- I can explain that search, knowledge representation, and probabilistic reasoning begin from different questions but can be used together in real systems.
- I can explain that search is a way to find a path to the goal among possible candidates, knowledge representation is a way to organize the facts and relations needed for solving the problem in a computer-readable form, and probabilistic reasoning is a way to calculate the plausibility of possible conclusions under incomplete information.
- I can explain that these three flows are not only background to pre-machine-learning AI, but also remain in modern AI services in forms such as search, recommendation, planning, policy verification, knowledge graphs, and probabilistic prediction.

## Sources and Further Reading

- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed.](https://artint.info/3e/html/ArtInt3e.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/){: target="_blank" rel="noopener noreferrer" }, substantive revision 2024-02-27, accessed 2026-06-22.
