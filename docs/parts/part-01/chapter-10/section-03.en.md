# P1-10.3 Quality and Risk of Generated Outputs

> Section ID: `P1-10.3`
> Version: `v2026.07.26`

Section 10.1 examined the difference among classification, prediction, and generation. Section 10.2 introduced the intuition that generative AI builds artifacts progressively from conditions.

This section asks how generated results should be read and reviewed.

The central question is:

> if a generative-AI output looks natural and plausible,  
> can we trust it?

The introductory baseline is clear:

> naturalness is only one part of quality; factuality, evidence, safety, copyright, privacy, and the context of use all need separate review

Part 1 introduces the basic distinctions among `quality`, `evidence`, `hallucination`, `confabulation`, `safety`, and `rights and responsibility` here. Section 10.1 asked `what does the model output?` Section 10.2 asked `how is it generated?` This section separates a third question:

> how should we read and verify the result?

Detailed discussion of copyright, security, and privacy returns in P1-15.

This section does not cover every generative-AI risk. Legal interpretation, security architecture, privacy protection, copyright disputes, and AI governance are treated in greater detail in P1-15.

These review terms can sound similar at first. A quick distinction helps:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| quality | how well the output fits the request and whether it is readable | the first visible axis of evaluation |
| evidence | whether factual claims are supported by checkable sources | the axis that separates naturalness from correctness |
| hallucination | a plausible but unsupported error | the representative generative-AI risk |
| safety | the possibility of harm to people or systems | the risk of using the output in context |
| rights and responsibility | copyright, privacy, confidential information, and accountability | the review axis before publication or deployment |

The minimum distinction to keep is:

- naturalness is not the same thing as factuality
- hallucination is a plausible error
- safety and rights need their own review

This section ends Chapter 10 with four review lenses:

| Lens | Core question |
| --- | --- |
| quality | does the result fit the request, read clearly, and help the user? |
| evidence | are factual claims backed by checkable sources? |
| safety | could the output cause harm to people, organizations, or society? |
| rights and responsibility | have copyright, privacy, confidential information, and accountability been reviewed? |

## Reviewing Natural-Looking Generated Outputs

- Distinguish the naturalness of generated output from its factuality.
- Understand hallucination or confabulation as unsupported factual content presented plausibly.
- Understand that AI output does not automatically include valid sources or evidence.
- Review generative-output risks through quality, evidence, safety, and rights.
- Clarify why AI-generated drafts in this book still need human review.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a natural sentence and a correct sentence are not always the same | This corrects one of the most common misunderstandings about generative AI. | It is enough to understand that a smooth sentence can still be wrong. |
| sources and evidence do not arrive automatically with the output | This connects directly to the verification rules of the whole book. | It is enough to know that factual claims need separate checking. |
| risk includes not only quality, but also safety, rights, and responsibility | This prepares a natural bridge into the ethics, copyright, and security topics in P1-15. | It is enough to know that `well written` is not sufficient. |

## A Natural Sentence and a Correct Sentence Are Different

Generated output can look very natural. The sentence may be smooth, the phrasing plausible, and tables or lists neatly organized.

But `naturalness` is not the same as `accuracy`.

> a natural sentence:  
> easy to read and plausible
>
> a correct sentence:  
> factually, contextually, and evidentially sound

For example:

> Transformer was published in 2012 and is a direct follow-up to AlexNet.

This may look natural as a sentence, but it is factually wrong. The Transformer paper was published in 2017, and AlexNet is safer to place as surrounding evidence in the spread of deep learning rather than as direct lineage for LLMs.

This is one of the most dangerous points in using generative AI:

> the sentence sounds natural  
> so it feels true  
> and then it enters the manuscript without evidence review

That flow needs to be blocked.

## Hallucination Is a Plausible Error

The NIST Generative AI Profile describes `confabulation` as the generation of confidently presented but incorrect or false content and notes that this is commonly called `hallucination` or `fabrication`. NIST also links this behavior to the way generative models approximate statistical distributions in training data.

In this book, the Korean term `hallucination` is used, but it helps to keep related expressions in mind as well:

- unsupported generation
- plausible error
- confabulation

Hallucination can appear in forms such as:

| Type | Example |
| --- | --- |
| inventing sources | producing a nonexistent paper, book, or URL |
| wrong dates | giving the wrong publication year or event time |
| concept mixing | explaining AlexNet, YOLO, and LLMs as if they belonged to one direct lineage |
| overgeneralization | treating a feature of some models as if it applied to all generative AI |
| false quotation | presenting words that do not exist in the original source as if they were quoted |

The problem is not only that the output can be wrong. It is that the wrong content is often presented smoothly and confidently, making it easy to accept without review.

## Missing Evidence Is Also a Quality Problem

In this book, AI-generated sentences are treated as drafts. Drafts can be useful, but factual claims still need evidence.

Compare these two examples:

> unsupported sentence:  
> most AI researchers believe generative AI reproduces human thinking
>
> safer sentence:  
> generative AI creates new artifacts from learned patterns in data, but whether that should be interpreted as a reproduction of human thought requires separate analysis

The following kinds of statements especially require source checking:

| Statement type | What to verify |
| --- | --- |
| historical explanation | dates, papers, researchers, context |
| technical definition | official docs, textbooks, papers |
| product features | official docs, release notes |
| law or policy | statutes, agency material, expert review |
| recent trends | dated news, reports, official announcements |
| forecasts | who said it, when, and on what basis |

Even when generative AI provides links, they still need to be checked to confirm that they actually support the claim. `Having a URL` and `having evidence` are not the same thing.

## Safety Risks Often Appear After Output

The risks of generative AI do not exist only inside the model. They depend strongly on where the output is used.

NIST lists risks such as confabulation, data privacy, information integrity, information security, and intellectual property. OWASP’s Top 10 for LLM Applications 2025 also treats prompt injection, sensitive information disclosure, improper output handling, and excessive agency as distinct application-level risks.

At an introductory level, these can be separated like this:

| Risk | Explanation | Example |
| --- | --- | --- |
| factuality risk | wrong content presented as if correct | summarizing a nonexistent case or paper |
| information-integrity risk | spreading false or manipulated content | fake images, fake news drafts |
| privacy risk | sensitive information enters or leaves the system | customer records, medical data, internal documents |
| security risk | model output becomes connected to system action | prompt injection, unsafe code execution |
| copyright risk | the use of others' expression or data becomes problematic | long reproduction of protected text, unauthorized style imitation |
| overtrust risk | people use the result without review | direct use in medical, legal, or financial judgment |

The important point is not the simple conclusion `AI is risky`. The more accurate view is:

> output risk is produced jointly by  
> the model,  
> the input data,  
> the use purpose,  
> the review procedure,  
> and the deployment environment

## News Reports Help Show Real Usage Contexts

News reporting is not the primary standard for technical definition. But it can help show how generative-AI risks appear in actual use contexts.

| Reported context | Connected risk | How to read it in 10.3 |
| --- | --- | --- |
| a campaign website published AI-generated fake-news-style stories | information integrity, hallucination, missing review | a sentence that looks like news still needs source and fact checking |
| court filings cited nonexistent AI-generated legal cases | factuality risk, high-stakes use, accountability | in law, medicine, and finance, human review is mandatory |
| legal responses to deceptive AI-generated media and deepfakes | safety, rights, public trust | generated outputs can affect personal rights, reputation, elections, and public trust |

So in this section, news reports are used only as `real cases`. The main standard stays with more stable official or professional material such as NIST, OWASP, and copyright offices.

## Copyright and Rights Need Review Even at the Draft Stage

The fact that generative AI creates new sentences or images does not erase rights issues.

The U.S. Copyright Office report on AI and copyright keeps the position that `human authorship` remains a core requirement for copyright protection. It also distinguishes between content generated entirely by AI and AI-assisted outputs that include meaningful human creative contribution.

This book is a public Korean-language document and may discuss Korean publications and educational materials, so review under Korean copyright law is also needed. But this section does not try to give legal conclusions. That returns in P1-15.

The main standard to keep in 10.3 is:

> even if AI wrote the sentence,  
> do not present factual claims without sources
>
> even if AI summarized the source,  
> do not reproduce long protected passages
>
> even if AI generated the image or code,  
> review license, originality, similarity, and scope of use

## Basic Review Procedure for Generated Outputs

When generated outputs are reused outside the model, such as in learning documents, work documents, or public writing, it is safer not to trust drafts as-is and to handle them through a procedure like this:

> AI draft generation  
> -> separate claims  
> -> verify evidence  
> -> generalize the wording  
> -> check domain boundaries  
> -> human review  
> -> reflect into the public manuscript

The meaning of each step:

| Step | What to check |
| --- | --- |
| separate claims | divide factual claims, interpretations, and working hypotheses |
| verify evidence | confirm whether real sources support the claim |
| generalize wording | connect personal intuitions to standard concepts |
| check domain boundaries | avoid invading the scope of other sections |
| human review | correct errors, risky phrasing, and missing evidence |

The core point is the same. AI can produce drafts quickly, but the reliability of a document comes from the review process, not from the speed of draft generation.

## Checklist

- I can distinguish a natural sentence from an accurate sentence.
- I can explain hallucination or confabulation as a plausible error.
- I can explain that a source link does not by itself finish evidence review.
- I can separate the risks of generated output into factuality, information integrity, privacy, security, copyright, and overtrust.
- I can explain why human review is required before reflecting AI drafts into a public document.
- I can remember that P1-15 treats copyright, security, and privacy in more detail.
- I can review `naturalness`, `accuracy`, `evidence`, `context of use`, and `rights and responsibility` as separate questions.
- I can explain that even when generative AI is used as a learning tool, the draft still needs stricter human review.

## Sources and Further Reading

- NIST, [Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf){: target="_blank" rel="noopener noreferrer" }, NIST AI 600-1, 2024-07, accessed 2026-06-23.
- OWASP GenAI Security Project, [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/resource/owasp-top-10-for-llm-applications-2025/){: target="_blank" rel="noopener noreferrer" }, 2024-11-17, accessed 2026-06-23.
- U.S. Copyright Office, [Copyright and Artificial Intelligence, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf){: target="_blank" rel="noopener noreferrer" }, 2025-01, accessed 2026-06-23.
- IBM, [What are AI hallucinations?](https://www.ibm.com/think/topics/ai-hallucinations){: target="_blank" rel="noopener noreferrer" }, IBM Think, accessed 2026-06-23.
- Associated Press, [Philly sheriff's campaign takes down bogus 'news' stories posted to site that were generated by AI](https://apnews.com/article/fake-news-philadelphia-sheriff-website-ai-headlines-7bace99ffe0f11d8e8b17862c7b55e4e){: target="_blank" rel="noopener noreferrer" }, 2024-02-05, accessed 2026-06-23.
- Associated Press, [UK judge warns of risk to justice after lawyers cited fake AI-generated cases in court](https://apnews.com/article/uk-courts-fake-ai-cases-46013a78d78dc869bdfd6b42579411cb){: target="_blank" rel="noopener noreferrer" }, 2025-06-07, accessed 2026-06-23.
- Associated Press, [Creating and sharing deceptive AI-generated media is now a crime in New Jersey](https://apnews.com/article/new-jersey-deepfake-videos-criminal-civil-penalties-276ca23b00b10a7ee7e7303ead8b4260){: target="_blank" rel="noopener noreferrer" }, 2025-04-03, accessed 2026-06-23.
