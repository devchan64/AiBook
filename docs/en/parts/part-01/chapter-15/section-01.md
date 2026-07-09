# P1-15.1 Bias, Safety, and Accountability

> Section ID: `P1-15.1`
> Version: `v2026.07.09`

P1-14 followed the flow of the AI service through the model, data, tools, agent, harness, and service constraints. The next question moves from technical structure to social impact.

> AI can produce answers.  
> AI can make recommendations.  
> AI can classify and predict.  
> AI can even call tools.
>
> If the result works against someone unfairly, who explains it and who takes responsibility?

`AI ethics` is not only a field of abstract goodwill. It asks what kinds of risks appear when AI systems affect people's opportunities, reputations, safety, rights, costs, and work decisions, and how those risks should be reduced.

This section narrows that broad topic into three words: `bias`, `safety`, and `accountability`.

## Scope of This Section

This section covers the basic reasons AI results can create social problems. Copyright and training-data debates are covered in P1-15.2. Security and privacy are covered separately in P1-15.3.

| Topic | Question in this section |
| --- | --- |
| bias | can AI results work against a particular group or situation? |
| safety | can AI results lead to real harm or dangerous action? |
| accountability | when a problem happens, who can explain it and fix it? |
| transparency | can users understand the role and limits of the AI? |
| human oversight | when should people intervene and make the final judgment? |

The `accountability` discussed here is not a final legal determination. It is a practical question of how people review and use results produced by AI.

## Goal of This Section

- Understand AI ethics as a question about real possible harm rather than as an abstract declaration.
- Understand bias not only as bad intention, but as a problem that can arise from data, metrics, and context of use.
- Treat safety as including mistaken judgment, overconfidence, and dangerous automation, not only physical accidents.
- Understand accountability as something that cannot be passed away with "the AI did it."
- Distinguish factual claims, interpretation, and policy proposals when reading news reports or opinion pieces about AI ethics.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| bias can arise from data and criteria, not only from bad intention | This prevents AI ethics from being reduced to a single moral issue. | It is enough to understand that training data and evaluation methods can distort results. |
| safety includes mistaken automation, not only physical accidents | This reveals the risk that appears when AI output is tied to real action. | It is enough to understand that wrong recommendations and overconfidence are also safety problems. |
| accountability ultimately remains with people and organizations | This prevents responsibility from being handed over to "the AI." | It is enough to understand that designers, operators, and user organizations all carry roles. |

## Why Ethics Is Not Separate from the Technical Problem

AI systems perform computation, but that computation is used inside real institutions and among real people.

> data is collected from the real world  
> the model learns patterns from the data  
> the service is deployed for a specific purpose  
> the result influences human judgment and action

That is why AI ethics is not just a slogan about using technology kindly. It includes what data was used, how evaluation was done, who is affected, and who can correct the result when it goes wrong.

The NIST AI Risk Management Framework is useful here because it describes AI risk as something that can affect individuals, groups, organizations, society, and the environment, and treats AI systems as socio-technical systems shaped by social context and human behavior.

## Where Bias Can Arise

`Bias` can appear when AI repeatedly produces disadvantageous results for a particular person, group, or situation. The important point is that bias does not arise only from a developer's malicious intent.

| Place where bias can arise | Example |
| --- | --- |
| data collection | data for some groups is too sparse or distorted |
| labels | past judgment standards are reflected directly in the labels |
| features | even without directly sensitive attributes, another variable can act as a proxy |
| evaluation metrics | overall accuracy is high, but error is large for one group |
| context of use | a model is used for a high-risk decision outside its original purpose |

The ProPublica reporting on `COMPAS` became a representative example because it raised concrete fairness questions about risk scores used in court decisions. The core lesson is not that one article settles every conclusion. It is that the article forces better questions:

> for whom was accuracy measured?  
> for which group did errors occur more often?  
> how did people use the AI score?  
> could the affected person contest or understand the result?

## Safety Becomes Clearer in High-Risk Areas

`Safety` is not only about whether the model outputs harmless language. The question becomes wider when AI results are connected to real action or institutional judgment.

| Situation | Safety question |
| --- | --- |
| face recognition | if identification is wrong, who is harmed? |
| medical assistance | does a person mistake the output for a diagnosis? |
| legal drafting | does the system present nonexistent cases or rules as if they were real? |
| hiring or screening | does unfair judgment repeat against certain groups? |
| agent tool execution | does the AI call an authorized tool incorrectly? |

Reports about wrongful arrests tied to face-recognition use in Detroit are useful not because they produce a one-line answer of full ban or full approval, but because they leave better questions:

> is the AI result evidence or only a clue?  
> how did a human verify the AI result?  
> how does recovery happen when misidentification harms someone?  
> how much human review is needed in a high-risk field?

Safety cannot be judged from output quality alone. What matters is how the result is tied to real procedure and authority.

## Accountability Cannot Be Handed to the AI

Even when AI produced the result, responsibility does not move to the AI. AI is a tool, and the people and organizations that set its use conditions and adopt its results remain responsible.

| Role | Accountability question |
| --- | --- |
| developer | were the limits of the model and system documented? |
| deployer | were the risks of the intended use reviewed? |
| operator | were logging, evaluation, and error-response standards prepared? |
| user | was the result used as if it were fact without review? |
| organization | is there a procedure for correction, suspension, and explanation if harm appears? |

The OECD AI Principles and the NIST AI RMF are helpful because they organize accountability, transparency, safety, robustness, privacy, and the management of harmful bias as conditions for trustworthy AI.

## Transparency Does Not Mean Publishing Every Internal Detail

`Transparency` is often understood too narrowly as exposing all internal model computation. In a real service, users should at least be able to understand:

| Transparency question | Description |
| --- | --- |
| was AI used? | does the user know AI was involved? |
| what is the purpose? | what is this AI meant to help with? |
| what are the limits? | in what situations can it fail? |
| what is the basis? | what input or material supported the result? |
| can it be challenged? | if the result is unfair, can a human review it again? |

Explainability and interpretability are part of this, but at this stage it is more useful to begin with whether the user can understand the AI's role and limits.

## Human Oversight Must Be Real, Not Formal

In AI services, people often say "a human will review it." That is not enough if review is only formal.

> weak human oversight:  
> a person looks at the AI result but almost always approves it unchanged
>
> better human oversight:  
> a person checks the basis, possible errors, affected people, and alternative judgment

Especially in high-risk situations, human oversight must not become a rubber stamp. People need time, information, and authority to intervene meaningfully.

| Needed condition | Why |
| --- | --- |
| enough information | the reviewer needs at least the basic grounds for the result |
| authority to stop | risky automation must be stoppable |
| a way to object | an affected person must be able to request another review |
| recordkeeping | later review must be able to reconstruct what happened |

The harness, trace, log, and evaluation structures discussed in P1-14.5 matter again here, because technical records can become part of ethical responsibility.

## Caution When Reading News and Opinion Pieces

Ethical issues in AI often become visible first through reporting, commentary, or investigative journalism. These are important because they reveal real harm and real disagreement. But it is risky to treat one article as if it were a complete general law.

| What to separate while reading | Question |
| --- | --- |
| factual claim | what event happened, when, and where? |
| analysis | how did the reporter or expert interpret the cause? |
| counterargument | what did the company or institution dispute? |
| policy proposal | what rule or institutional change was proposed? |
| generalizability | does this case apply directly to other AI systems too? |

In this book, cases help show the real problem, while official documents and research help organize concepts and standards. The text connects both, but avoids overgeneralizing from one case.

## The View to Keep from This Section

AI ethics is not an external decoration around technology. Once AI affects real people and organizations, `bias`, `safety`, and `accountability` become part of service design.

> bias can arise from data, metrics, and context of use  
> safety matters more once AI results connect to real action  
> accountability cannot be handed to the AI  
> transparency means helping users understand the AI's role and limits  
> human oversight must be able to intervene, stop, and judge again

This view leads directly into P1-15.2 on copyright and training data, and P1-15.3 on security and privacy.

## Checklist

- You can explain AI ethics as a question about real possible harm rather than abstract declarations.
- You can explain that bias can arise from data, labels, features, metrics, and context of use.
- You can explain that overall accuracy and group-specific error can differ.
- You can explain safety in connection with real action, authority, and high-risk judgment.
- You can divide accountability across developers, deployers, operators, users, and organizations.
- You can explain transparency through AI use disclosure, purpose, limits, basis, and contestability.
- You can explain why human oversight becomes risky if it ends as formal approval only.
- You can explain why facts, interpretation, counterargument, and policy proposal should be separated when reading news or opinion pieces.

## When to Recall This View First

- When AI ethics is being treated only as an abstract declaration outside technology
- When bias, safety, and accountability are being collapsed into one vague moral issue
- When a real service needs its possible harms and conditions for human oversight checked together

In those situations, separate `bias`, `safety`, `accountability`, `transparency`, and `human oversight` first.

## Sources and Further Reading

- NIST, [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework){: target="_blank" rel="noopener noreferrer" }, National Institute of Standards and Technology, accessed 2026-06-23.
- NIST, [Artificial Intelligence Risk Management Framework (AI RMF 1.0)](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf){: target="_blank" rel="noopener noreferrer" }, NIST AI 100-1, 2023, accessed 2026-06-23.
- OECD.AI, [OECD AI Principles overview](https://oecd.ai/en/ai-principles){: target="_blank" rel="noopener noreferrer" }, OECD AI Policy Observatory, accessed 2026-06-23.
- UNESCO, [Recommendation on the Ethics of Artificial Intelligence](https://www.unesco.org/en/artificial-intelligence/recommendation-ethics){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Julia Angwin, Jeff Larson, Surya Mattu, Lauren Kirchner, [Machine Bias](https://www.propublica.org/article/machine-bias-risk-assessments-in-criminal-sentencing){: target="_blank" rel="noopener noreferrer" }, ProPublica, 2016-05-23, accessed 2026-06-23.
- Ed White, [Judge dismisses lawsuit against Detroit police in wrongful arrest case](https://apnews.com/article/detroit-facial-recognition-arrest-821d260e932a4582a6a912dd61fde157){: target="_blank" rel="noopener noreferrer" }, Associated Press, 2025-09-17, accessed 2026-06-23.
