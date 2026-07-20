# P1-3.1 Strengths and Limits of Rule-Based Systems

> Section ID: `P1-3.1`
> Version: `v2026.07.20`

Section 2.1 located symbolic AI and rule-based approaches historically. Section 2.3 showed that even inside the same workflow, there is a split between `parts that are easy to write as explicit policy conditions` and `parts that need to learn relations from data, such as intent classification`. This section narrows the question one step further and organizes what practical strengths rule-based systems had and where they began to show their limits.

The task here is not to declare rule-based AI a failed method of the past. The task is to separate why rule-based systems were useful, why attention moved toward machine learning, and what kinds of parts still need rules even now.

In Part 1, the baseline for the strengths, limits, and modern operational role of the `rule-based system` is fixed in this section. The basic meanings of `symbolic AI`, `rule-based approach`, and `knowledge representation` were first fixed in 2.1, and are reconnected here only as much as needed to evaluate why real systems are useful in some places and difficult in others.

This section organizes the following questions.

- What components make up a rule-based system?
- Where do the strengths and limits of this approach appear?
- Why are rules still necessary in modern systems?

This section first closes `where rule-based systems are strong and where they become difficult`. The flow of learning patterns from data continues in `P1-3.2`, the difference from representation learning continues in `P1-3.3`, and operational structures where rules and models are used together continue in Parts 6 and 7.

## Standards for Evaluating Rule-Based Systems

- Understand the basic components of a rule-based system.
- See why rule-based systems are strong in explainability and controllability.
- Distinguish the possibility and limit shown by expert-system history.
- Understand why rule writing, knowledge acquisition, and exception management become difficult.
- Fix a simple picture of where rules and models are used together in modern systems.

## Concepts to Connect First

This section is the representative place where a rule-based system is read as an actual operational structure. The concepts below are first fixed by role, and when a fuller definition is needed, you should move directly to each glossary entry.

| Concept | Meaning to fix first here | Why it is needed now |
| --- | --- | --- |
| [rule-based system](/AiBook/reference/concept-glossary/#rule-based-system) | a system that compares current facts against rules to determine a conclusion or action | to make the evaluation target itself explicit |
| [fact](/AiBook/reference/concept-glossary/#fact) | state information treated as true in the current situation | to see what the rules are applied to |
| [knowledge base](/AiBook/reference/concept-glossary/#knowledge-base) | the structure that collects facts, rules, and domain knowledge | to see where the rule set is stored |
| [inference engine](/AiBook/reference/concept-glossary/#inference-engine) | the mechanism that finds and applies rules matching the current facts | to see how a conclusion is actually produced |
| [explanation facility](/AiBook/reference/concept-glossary/#explanation-facility) | the function that shows which rules caused the result | to fix explainability, one of the main strengths of rule-based systems |

## Three Standards

In this section, the rule-based system is being evaluated. The following three standards are the baseline of that evaluation.

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a rule-based system connects `current facts` and `rules` to produce a conclusion | This helps fix the basic structure first. | Distinguish the three positions of input, rules, and result. |
| its strengths are `explainability` and `controllability` | This helps explain why rules still remain in policy and operational procedures. | Connect why it is easy to trace why the system handled something in a certain way. |
| its limit is that `rule management becomes difficult as exceptions and change increase` | This connects to why attention moved toward machine learning. | Organize that rules are strong for narrow problems but struggle to cover all of complex reality. |

## Basic Structure of a Rule-Based System

A rule-based system compares current facts or inputs against rules and then decides a conclusion, classification, action, or processing procedure.

The basic structure can be read as follows.

> current facts + rule set -> inference engine -> conclusion or action

Broken down more explicitly, the following elements are needed.

| Component | English expression | Role |
| --- | --- | --- |
| facts | facts | current input, observed value, user state, or business data |
| rules | rules | knowledge describing what conclusion or action should follow under a condition |
| knowledge base | knowledge base | the structure that stores facts, rules, and domain knowledge |
| inference engine | inference engine | the mechanism that finds and applies rules matching the current facts |
| explanation facility | explanation facility | the function that shows which rules caused the conclusion |

The book by Buchanan and Shortliffe on MYCIN treats MYCIN as a representative experiment in rule-based expert systems. In that material, the knowledge base, rules, inference procedure, explanation facility, and uncertainty handling are discussed as separate elements. In other words, an expert system was not merely a program that collected many `IF-THEN` statements. It was a system that studied how domain knowledge should be represented, applied, and explained.

These terms can sound similar at first. In a short dictionary-like form, they can be fixed again like this.

| Term | Very short meaning | What it corresponds to in the example of this section |
| --- | --- | --- |
| fact | the current state that has been input now | request amount, remaining budget, relation between requester and approver |
| rule | a judgment standard to follow when a condition matches | a sentence like `if it exceeds 1,000,000 won, require department-head approval` |
| knowledge base | the place where facts and rules are collected | approval standards, exception policy, role information |
| inference engine | the part that selects and applies the matching rule | the procedure that calculates which approval step to send it to |
| explanation facility | the part that shows why the result came out | an explanation like `budget sufficient + amount above threshold -> department-head approval` |

The first distinction that should remain in this section is this: `facts are the current state`, `rules are judgment standards`, `the knowledge base is where they are collected`, `the inference engine is the application mechanism`, and `the explanation facility is the mechanism that shows the reason`.

```mermaid
--8<-- "assets/part-01/chapter-03/knowledge-base-engine-flow-en.mmd"
```

This diagram helps you read a rule-based system as the flow `current input -> organize facts -> compare with knowledge base -> conclusion -> explanation`. The key point is that the system can often show not only the result, but also why that result was produced.

## Example: Expressing Approval Work as Rules

One of the easiest ways to understand a rule-based system is through approval work. Approval work has relatively explicit conditions, it requires recording who approved what and why, and under the same condition it should usually produce the same handling again.

For example, if a company's purchase-request handling rules are simplified, they can look like this.

| Current fact | Rule to apply | Result |
| --- | --- | --- |
| request amount is at most 100,000 won and remaining budget is sufficient | automatic approval without team-lead approval | approved |
| request amount is above 100,000 won and at most 1,000,000 won | team-lead approval required | waiting for team lead |
| request amount is above 1,000,000 won | department-head approval required | waiting for department head |
| remaining budget is insufficient | reject regardless of amount | rejected for insufficient budget |
| requester and approver are the same person | self-approval forbidden | approver reassignment |

If read as a procedure, it looks like this.

```mermaid
--8<-- "assets/part-01/chapter-03/purchase-approval-rule-flow-en.mmd"
```

This example is simple, but it shows the character of a rule-based system well. Rules can be read by people, conclusions can be explained, and if policy changes, a particular rule can be revised.

But the same example quickly becomes complex in actual work. Conditions such as urgent purchase, corporate-card exceptions, project-specific budgets, approver vacation, audit-target items, and supplier restrictions start to be added. That growing complexity leads directly to the limits of rule-based systems discussed later in the section.

## Strength 1: People Can Read and Review It

The biggest strength of a rule-based system is that the judgment standard is explicit. Because the rules are visible in documents, code, configuration, or the knowledge base, people can read and review them.

For example, rules like the following are comparatively easy to explain as the judgment standard of the system.

> If the payment amount exceeds the approval limit, send it to the administrator approval step.  
> If the user's privilege is lower than administrator, block the settings change.  
> If the temperature-sensor value exceeds the standard range, send an inspection alert.

These rules may not be perfect, but they are at least easy to trace when someone asks, `Why was it handled this way?` Domain experts, operators, auditors, and developers can also discuss the same rule together.

This advantage is especially important in the following situations.

| Situation | Why a rule-based system is advantageous |
| --- | --- |
| law, policy, permissions | the standard must be explicit and change history matters |
| approval procedure | it must be explainable who should approve under which condition |
| safety filter | people must be able to inspect forbidden and allowed conditions |
| operations automation | repetitive conditions must run in a predictable way |
| education and diagnostic support | not only the conclusion but the reason matters |

For example, when someone asks the purchase-approval system above, `Why is this waiting for department-head approval?`, the answer can be given like this.

> The request amount exceeded 1,000,000 won,  
> the remaining budget was sufficient,  
> and the requester was not the same person as the approver,  
> so the department-head approval rule was applied.

This explanation is not a problem of interpreting hidden model weights. It is a problem of tracing which facts were connected to which rules. That is why rule-based systems fit audit, policy review, and operational logs well.

## Strength 2: It Is Easy to Make the Same Input Produce the Same Output

Rule-based systems usually behave deterministically. If the same facts and the same rules are given, it is comparatively easy to build a structure in which the same conclusion comes out.

This contrasts with modern generative AI. Generative AI can produce different outputs even for the same request depending on settings, context, model state, and sampling method. A rule-based system, by contrast, executes fixed handling when explicit conditions match.

That is why rule-based systems are suitable for procedures that `must be followed`.

- block access when permission is missing
- do not move to the next step if required values are missing
- do not allow forbidden file types to be uploaded
- do not complete signup if terms are not agreed to
- do not run automatically unless operational approval has been given

In such areas, it can matter more that the rule blocks or allows something clearly than that a model judges it `approximately plausibly`.

Alert rules in operations systems are another good example.

| Current state | Rule | Result |
| --- | --- | --- |
| CPU usage stays above 90 percent for 5 minutes | send warning alert | operator review |
| disk usage exceeds 95 percent | send urgent alert | immediate action |
| payment-failure rate rises sharply above normal | mark as an outage candidate | stronger monitoring |
| error rate is above the threshold right after deployment | send rollback-review alert | deployment-owner review |

These rules are useful even when there is no predictive model. What matters is `repeatedly executing fixed handling without missing the stated condition`.

But one more distinction matters here. `The same input gives the same output` means `the judgment is reproducible`. It does not mean `the judgment is always correct`. If the rule itself is wrong or missing an exception condition, the system can repeat the wrong result very consistently.

| Distinction | What it means | Meaning in a rule-based system |
| --- | --- | --- |
| reproducibility | under the same condition, the same result comes out again | useful for audit, tracking, and testing |
| correctness | the result matches the actual policy or real-world judgment | the rule itself must still be reviewed separately |

For example, imagine an approval rule that wrongly says `all purchases by overseas subsidiaries always require headquarters department-head approval`. The system can stably produce the same result every time that condition appears. But if the result does not match the company's actual policy, reproducibility is high while correctness is low. That is why in rule-based systems it is important to inspect separately whether `the same result repeats` and whether `the rule itself is correct`.

## Strength 3: It Can Become Useful Quickly in a Narrow Area

Rule-based systems can become useful quickly when the problem scope is narrow and the standards are clear. If domain experts can explain the judgment criteria, the form of the input data is relatively stable, and there are not many exceptions, rules become a strong tool.

Expert systems showed this possibility well. DENDRAL is known as research that used chemistry knowledge to search molecular-structure candidates, and MYCIN was studied as a medical consultation system that combined rules and uncertainty handling in the domain of infectious disease. These cases showed the possibility that `if domain knowledge is represented well, strong performance can be achieved on a specific problem`.

But those cases should not be generalized directly into modern medical services. MYCIN was a research system, and questions of clinical deployment and responsibility require separate review. In this section, expert systems are treated only as `historical cases that show both the possibility and the limit of rule-based systems`.

For learning purposes, the rules in expert systems can be understood in a simplified form like this.

> If the observed symptoms or test results satisfy certain conditions,  
> raise or lower candidate causes.
>
> If the vibration of a machine exceeds the standard range,  
> and the last maintenance history is old,  
> raise the inspection priority.

These are not completed rules that can be used directly for real medical diagnosis or equipment maintenance. What matters is the structure. Expert systems tried to place the judgment clues held by experts into the knowledge base, then narrow candidate conclusions by comparing them with the current observations.

## Case: Limits of Hand-Designed Features and Procedures

The strengths and limits of rule-based systems did not appear only in expert systems. Similar flows can also be seen in areas where people used to design many features and procedures by hand, such as face recognition, lane tracking, and speech synthesis.

For example, early face-recognition methods often used the location and distance of face components, hand-designed features, and templates, while lane-tracking prototypes often used image-processing procedures such as ROI (region of interest), Canny edge detection, and the Hough transform. These methods can be easy to explain and become useful quickly when the structure is simple and the environment is controlled.

But as input conditions diversify, the limits appear quickly. Lighting, facial expression, pose, background, weather, noise, and exceptional pronunciation create too many variables, and people have to keep adding more features and procedures directly. On the other hand, in areas such as TTS, where spelling and pronunciation rules are comparatively structured, rule-based procedures remained useful for a long time.

The conclusion from this comparison is simple.

> Rules and hand-designed features were a strong way to put human-understood structure into a system. But as the input world becomes too diverse and exceptions increase, the approach in which people directly design every feature and rule hits a limit.

## How the Historical Flow Should Be Expressed

If rule-based systems, symbolic AI, machine learning, and neural networks are understood only as a pure time sequence, confusion appears easily. The history of AI is less like a single-line replacement in which one method completely removed the next, and more like a flow in which the importance of certain approaches became stronger as problems and computational environments changed.

Early on, approaches that explicitly represented knowledge and performed inference through rules were especially important. Later, exceptions and uncertainty in real problems, large-scale data, greater computational resources, and advances in learning algorithms together increased the importance of approaches that learn patterns and representations from data. In that shift, neural networks re-emerged from an older research tradition into the strong central flow now called deep learning.

This flow is better understood as a process in which the center of research and practice moved and the roles of each approach changed. Rule-based systems did not simply disappear and get replaced by neural networks. Rather, the kinds of problems and the engineering conditions changed, and so the approaches that were used more strongly changed. Rule-based systems remain strong in explicit policy, permissions, procedure, and verification, while machine learning and deep learning became more central in many cases because they learn patterns and representations from data that are too difficult for people to write directly.

Physical performance changes also mattered a great deal here. Rule-based systems could create useful systems with relatively small data and computational resources. Deep learning, by contrast, needs a great deal of data, repeated training, and parallel processing ability. As storage became cheaper, more data accumulated, CPUs and GPUs advanced, distributed processing environments and open-source training tools improved, neural-network approaches that once looked closer to research ideas became stronger engineering choices that delivered practical performance. In this section, it is enough to hold the point that `the strengths of rule-based systems remain, but the center of complex pattern recognition gradually moved toward learning-based approaches`.

| Change | Effect on AI approaches |
| --- | --- |
| more stored data and lower storage cost | more material became available for learning patterns that are difficult to write directly as rules |
| progress in parallel processing and computational resources | the conditions for repeatedly training and comparing large learning models improved |
| broader tool and evaluation ecosystems | the speed of reproducing, comparing, and improving research results increased |

This relation can be summarized like this.

> Symbolic AI is the broader flow that tries to represent knowledge and rules explicitly and reason over them. Rule-based systems are one representative way that flow was implemented in real systems. Neural-network-based approaches are not merely a later stage that came after them, but an older parallel research line whose importance was greatly strengthened by the rise of data, computational resources, and learning algorithms.

If expressed as a diagram, the flow looks like this.

```mermaid
--8<-- "assets/part-01/chapter-03/symbolic-to-learning-flow-en.mmd"
```

This diagram does not mean that the earlier stage disappeared and the next stage completely replaced it. Real history overlaps more than that. Rule-based systems, search, probabilistic reasoning, machine learning, and neural networks changed in importance at different times, and they are still used together inside modern systems.

So it is safer to read the diagram not as a history in which `rule-based approaches were switched out for data learning all at once`, but as a history in which `the center of explanation moved as problems and computational conditions changed`. The key point in this section is that this movement came from the strengths and limits of rule-based systems becoming visible.

If reduced into common misunderstandings, the contrast looks like this.

| Easy-to-confuse expression | More accurate expression |
| --- | --- |
| rule-based approaches flowed into symbolic AI | symbolic AI is the broader flow, and rule-based systems are one representative implementation of it |
| symbolic AI then flowed into neural networks | as the limits of symbolic approaches and the need for data-based learning grew, older neural-network research became strong again in deep learning |
| the era changed because the ideas changed | the center of research and practice moved because data scale, physical compute performance, parallel processing, and the tool ecosystem changed together |
| rule-based approaches belong only to the past | rule-based approaches were once the central method, but they are still used in modern AI services for policy, permission, safety, and verification |
| neural networks replaced rules | for some recognition, prediction, and generation problems, neural networks greatly reduced hand-written rules and hand-designed features, but they did not erase every rule |

## Limit 1: It Is Hard to Obtain Good Rules

Rule-based systems require that knowledge be written explicitly. So the first problem they run into is `where do good rules come from?`

Experts make many judgments, but they cannot always explain those judgments as simple sentences. Experience, exceptions, tacit knowledge, and situational judgment are mixed together. Even when an expert explains a rule verbally, real cases can reveal missing conditions, conflicts with another rule, or a scope that was written too narrowly.

This process can be read as knowledge acquisition or knowledge engineering. In MYCIN-related research as well, the problems of moving expert knowledge into the system's knowledge base, entering rules, revising them, explaining them, and debugging them were treated as important.

One point beginners especially miss is that `an expert judges well` and `that judgment can easily be written as a rule` are not the same statement. For example, a skilled support agent may see the same word `refund`, but also notice whether the customer really wants a refund, is angry about shipping delay, or already received a partial refund in an earlier conversation. But such judgment is not adequately transferred by a one-line rule like `if the word refund appears, classify it as a refund request`. That gap is exactly why tacit knowledge is difficult to convert into rules.

The difficulty of a rule-based system is not merely that `a lot of code must be written`. More precisely, it looks like the following.

| Difficulty | Explanation |
| --- | --- |
| knowledge acquisition | expert judgment must be brought out and written as rules |
| representation choice | the system must decide how to express facts, conditions, exceptions, and conclusions |
| verification | the rules must be checked against real cases |
| conflict management | different rules can produce different conclusions |
| maintaining freshness | if work, policy, or the environment changes, the rules must also change |

For example, imagine that you want to create a rule that `blocks risky transactions`. It might first be written like this.

> If a login occurs from a country different from usual,  
> and a large payment is made,  
> require additional authentication.

But real operation immediately increases the number of questions.

| Question | Why rule writing becomes difficult |
| --- | --- |
| how should `different from usual country` be defined? | business travel, VPNs, and overseas residents must be separated |
| how large is a `large amount`? | spending scale differs by user |
| does failing additional authentication mean fraud or a simple mistake? | intent is difficult to decide from behavior alone |
| how should new users be handled when there is no usual pattern? | the comparison baseline itself is missing |
| what if attackers learn the rule and avoid it? | fixed rules invite bypass strategies |

So a good rule is not merely a short sentence. It requires domain knowledge, data distribution, exception handling, and operational policy together.

## Limit 2: It Becomes Complex as Exceptions Increase

Rule-based systems often look simple at the beginning. But as exceptions increase, the rule set becomes complex very quickly.

Imagine a set of rules for classifying customer-support requests.

> If the word `refund` appears, classify it as a refund request.  
> If the word `delivery` appears, classify it as a delivery inquiry.

At first this can look sufficient. But exceptions soon appear.

> "I do not want a refund, I only want to confirm the delivery."  
> "The delivery arrived, but it was damaged and I want an exchange."  
> "This is a delivery inquiry for a new order, separate from the previous refund case."

To handle all such exceptions through rules, conditions keep increasing. As the number of rules grows, someone has to check which rule should be applied first, what should take priority when two rules conflict, and whether a new rule silently breaks an older one.

This is where space opens for machine learning. In problems where people cannot realistically write all the rules, it may be better to learn patterns from many example cases.

The earlier purchase-approval example has the same problem.

| Additional requirement | New rule needed |
| --- | --- |
| urgent outage-response purchases must be approved quickly | if connected to an outage ticket, allow temporary approval |
| audit-target items must be reviewed regardless of amount | send certain item groups to an audit approval step |
| the approver can be on vacation | a replacement-approver rule is needed |
| project budgets and department budgets can differ | a rule for the deduction order by budget type is needed |
| repeated purchases can concentrate on the same supplier | a rule for cumulative amount by period is needed |

At first, three lines of amount thresholds looked enough. But once actual business conditions enter, the rules begin to tangle together. The needed work is no longer simply adding more rules. Priority, conflicts, and test cases also have to be managed together.

## Limit 3: It Is Weak on Ambiguous Input and Complex Patterns

Rule-based systems are strong when the standards are explicit, but they can be weak on ambiguous input and complex patterns.

For example, the following problems are difficult for people to write directly as rules.

- deciding whether an object in a photo is a dog or a cat
- judging a sentence's sentiment or intent while considering context
- separating speech sounds from noise in audio
- predicting churn possibility from many user behaviors
- generating natural new sentences or images

In such problems, the variation of the input is too large, and people cannot write every useful feature as a rule. So the growing strength of data-based learning, statistical models, and deep learning does not mean that rule-based systems were `wrong`. It means the nature of the problem changed.

The customer-inquiry classification example makes the difference clearer.

| Input sentence | Difficulty for a simple rule |
| --- | --- |
| "Refund is fine, I only want to change the delivery address." | the word `refund` appears, but it is not actually a refund request |
| "The product I got yesterday was broken, can I receive it again?" | there is no word `exchange`, but the intent may be exchange or reshipment |
| "Please handle it like last time." | without earlier dialogue context, the meaning is unclear |
| "If delivery is late, I will cancel it." | delivery inquiry and cancellation possibility appear together |

In such input, a word-inclusion rule alone is not enough. Because context, intent, previous history, and expression differences must be examined together, a learned classifier or an LLM may be used as support.

## Limit 4: Rules Do Not Learn

A general rule-based system does not improve its rules by itself from experience. The system changes only when people add, revise, or remove rules.

Of course, there has also been research on automatically generating or revising rules, and on combining rule-based systems with learning-based systems. But the center of an ordinary rule-based system is still explicit knowledge. People create the judgment criteria, and the system applies them.

Machine learning, by contrast, adjusts the model's `parameters` by using data and an evaluation criterion. That difference can be separated like this.

| Distinction | Rule-based system | Machine-learning system |
| --- | --- | --- |
| judgment standard | rules written by people | parameters learned from data |
| improvement mechanism | add, revise, or remove rules | adjust parameters through training data and a loss function |
| review target | rule validity, conflict, and omission | data quality, evaluation performance, overfitting, and bias |
| strong area | explicit procedures and policy | complex pattern recognition and prediction |
| weak area | many exceptions and pattern-rich input | procedures where explainability and control are critical |

### A Short Exercise in Judging Where It Fits

Look at the following cases and first judge whether `a rule-based system fits well first`, `rules alone quickly hit a limit`, or `rules and models should be used together`.

| Case | First question to check | First-pass judgment by the standard of this section |
| --- | --- | --- |
| check approval limits by rank in internal payment workflow | is the standard already organized in explicit sentences? | a rule-based system fits well first |
| automatically classify hidden dissatisfaction in customer inquiry sentences | does the same meaning appear in many very different expressions? | rules alone hit limits quickly |
| prevent an LLM service from retrieving documents that the user has no permission to access | must the allow/block standard be fixed explicitly? | rule-based control is necessary |
| predict breakdown probability from factory sensor values and work history | can people write every pattern directly as rules? | a model is more likely to be needed |
| mask resident-registration numbers before a document assistant creates its answer | is it a safety condition that must always be enforced? | rules and models are easy to use together |

The key to this exercise is not to read rule-based systems as `old methods`, but as tools that are especially strong for `procedures that must be explicitly controlled`. Conversely, when meaning interpretation is ambiguous and patterns are complex, the role of the model grows.

## Rules Do Not Disappear Even in Modern Systems

Modern AI systems are not composed of a model alone. Even in services that use LLMs, explicit rules are needed for permission checks, input validation, forbidden-request handling, personal-information masking, tool-calling conditions, deployment procedures, cost limits, and audit logging.

This section does not explain service architecture in detail. The key point is simply that `even when a learned model exists, there remain areas where explicit rules are necessary`. Concrete structures such as RAG, tool use, and agents return in P1-14 and Part 6.

For example, even when building an LLM-based document assistant, rules like the following are still needed.

> Do not retrieve documents the user has no permission to access.  
> Do not store input containing personal information.  
> Do not state an answer as fact when there is no source.  
> Do not execute automatically unless the operation has been approved.

Looked at in a way closer to an actual service, the roles can be divided like this.

| Processing stage | The part rules are good at handling | The part a model is good at handling |
| --- | --- | --- |
| input reception | checking file size, permission, and forbidden format | classifying the user's intent |
| retrieval | retrieving only accessible documents | finding candidate documents related to the question |
| answer generation | preventing unsupported assertions, masking sensitive data | summarizing document content in natural language |
| tool call | executing only allowed tools and parameters | proposing which tool may be needed |
| deployment or execution | checking approval state, run conditions, and environment conditions | drafting a change summary |

Such rules are difficult to hand over to a model and ask it to `roughly figure it out through learning`, because they are tied to service safety, responsibility, and operational standards.

So to understand modern AI, it is not enough to place rule-based systems and machine learning only in opposition. A more realistic view is the following.

> Rules take explicit procedures and constraints that must be controlled, while machine-learning models take pattern recognition, prediction, and generation problems that are too difficult for people to write fully as rules. Real AI services are built by combining the two.

## Checklist

- I can explain a rule-based system by dividing it into facts, rules, the knowledge base, the inference engine, and the explanation facility.
- I can explain why rule-based systems are strong in explainability and controllability.
- I can explain expert systems as historical cases that tried to represent knowledge in a specific domain through rules and a knowledge base.
- I can explain that knowledge acquisition and knowledge engineering are important difficulties of rule-based systems.
- I can explain that maintenance becomes difficult as exceptions and rule conflicts increase.
- I can distinguish rule-based systems and machine-learning systems not by superiority, but by role difference.
- I can explain the shift of research center and role change together with data scale, computational performance, parallel processing, and tool-ecosystem change.
- I can give examples of areas where explicit rules are still necessary even in modern systems.
- I can explain that a rule-based system is a method where people write knowledge explicitly and the system applies those rules to produce a conclusion or action, and that it is strong in explainability, controllability, and reproducibility.
- I can explain that expert tacit knowledge is hard to extract as rules, rule management becomes complex as exceptions increase, and complex patterns such as image, speech, and language have limits under rule-only handling.

## Sources and Further Reading

- Bruce G. Buchanan, Edward H. Shortliffe (eds.), [Rule-Based Expert Systems: The MYCIN Experiments of the Stanford Heuristic Programming Project](https://people.dbmi.columbia.edu/~ehs7001/Buchanan-Shortliffe-1984/MYCIN%20Book.htm){: target="_blank" rel="noopener noreferrer" }, Addison-Wesley, 1984, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Richmond H. Thomason, [Logic-Based Artificial Intelligence](https://plato.stanford.edu/entries/logic-ai/){: target="_blank" rel="noopener noreferrer" }, substantive revision 2024-02-27, accessed 2026-06-22.
- Stuart Russell, Peter Norvig, [Artificial Intelligence: A Modern Approach, 4th US ed., Full Table of Contents](https://aima.cs.berkeley.edu/contents.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Daniel Saez Trigueros, Li Meng, Margaret Hartnett, [Face Recognition: From Traditional to Deep Learning Methods](https://arxiv.org/abs/1811.00116){: target="_blank" rel="noopener noreferrer" }, arXiv:1811.00116, 2018, accessed 2026-06-22.
- Shervin Minaee, Ping Luo, Zhe Lin, Kevin Bowyer, [Going Deeper Into Face Detection: A Survey](https://arxiv.org/abs/2103.14983){: target="_blank" rel="noopener noreferrer" }, arXiv:2103.14983, 2021, accessed 2026-06-22.
- Sertap Kamci, Dogukan Aksu, Muhammed Ali Aydin, [Lane Detection For Prototype Autonomous Vehicle](https://arxiv.org/abs/1912.05220){: target="_blank" rel="noopener noreferrer" }, arXiv:1912.05220, 2019, accessed 2026-06-22.
- Wojciech Skut, Stefan Ulrich, Kathrine Hammervold, [A Flexible Rule Compiler for Speech Synthesis](https://arxiv.org/abs/cs/0403039){: target="_blank" rel="noopener noreferrer" }, arXiv:cs/0403039, 2004, accessed 2026-06-22.
- Alex Krizhevsky, Ilya Sutskever, Geoffrey E. Hinton, [ImageNet Classification with Deep Convolutional Neural Networks](https://proceedings.neurips.cc/paper/2012/hash/c399862d3b9d6b76c8436e924a68c45b-Abstract.html){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2012, accessed 2026-06-22.
