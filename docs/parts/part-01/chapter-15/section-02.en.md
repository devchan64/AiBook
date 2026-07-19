# P1-15.2 Copyright and Training Data

> Section ID: `P1-15.2`
> Version: `v2026.07.19`

P1-15.1 examined how to think about `bias`, `safety`, and `accountability` when AI results affect people and society. The next question is more specific.

> AI seems to read and learn from a large amount of material.  
> That material may include books, articles, images, code, and blog posts.  
> Then what place do other people's copyrighted works have when AI is trained or when it generates output?

`Copyright` is not a problem invented by the AI era. But generative AI makes copyright questions harder. A person quoting a short sentence from a book is not the same problem as collecting large-scale data and using it for model `training`.

This section does not force a final legal conclusion. Instead, from the standpoint of making and publishing a Korean-language book, it organizes what concepts need to stay separate, what kinds of material use should be postponed, and what evidence should be preserved.

The focus here is on `copyright`, `quotation`, `training data`, `expression`, `attribution`, and `license`: how to handle other people's expression and source material in public-facing writing. It extends the social-risk discussion from 15.1, while security and privacy move to 15.3.

## Scope of This Section

This section reviews the main checkpoints in copyright and training-data debates. Security, privacy, and leakage of confidential information are covered in P1-15.3.

| Topic | Question in this section |
| --- | --- |
| copyright | what kinds of expression and material can be protected? |
| quotation | how much outside wording can be used in the book text? |
| training data | why does material used for AI model training become controversial? |
| generated output | what problem appears if AI output becomes too similar to an existing work? |
| authoring rule | what material use should this book avoid? |

This section starts from Korean copyright law, but it also treats the legal and case-law landscape of generative AI training as something still developing differently across countries.

The practical stance in this book is cautious rather than permissive. When the source material is paid, closed, copied without authorization, or hard to verify, the safer default is to hold its use back instead of forcing it into the drafting flow.

## Goal of This Section

- Distinguish `copyright`, `license`, `attribution`, and `quotation`.
- Distinguish `idea`, `fact`, and `expression`.
- Explain why quotation in book text and use of `training data` for AI are different issues.
- Understand what rightsholders and AI developers are disputing in the debate over generative AI training data.
- Explain why this book should not use paid publications, closed lecture materials, or unauthorized PDF copies as AI input.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| copyright protects expression rather than ideas | This separates topic reference from sentence copying. | It is enough to understand that concepts themselves and concrete wording or diagrams should be judged differently. |
| quotation in a book and use as AI training data are different issues | This reduces the oversimplified view that source citation alone solves everything. | It is enough to understand that a person quoting in visible text and a model learning from large-scale data raise separate questions. |
| this book should use material conservatively | This connects directly to real authoring rules. | It is enough to understand that paid publications, closed lecture materials, and unauthorized PDFs should not be used as input. |

## Copyright Protects Expression

Copyright does not grant exclusive ownership over every idea. What copyright generally protects is the `expression` of ideas, feelings, information, or arrangement in a concrete form.

> examples that are usually difficult to protect by themselves:  
> the topic of AI ethics  
> the idea that copyright should be handled carefully  
> the idea of making a machine-learning curriculum
>
> examples that may be protected:  
> specific wording from a book  
> the explanation structure and diagrams of specific lecture materials  
> the expression used in a specific article or column  
> a specific image, table, or code example

This matters when building a book. It is different to conclude that "an introduction to AI should cover copyright" and to copy the sentences, sequence, examples, or diagrams of a specific source.

`Attribution` is necessary, but source citation alone does not automatically authorize all use. Attribution may be one condition of lawful use, but it does not replace permission, licensing, or the legal requirements for quotation.

That is why copyright review in this project cannot stop at source formatting. It also has to examine permission, amount, purpose, replacement risk, and whether the original expression is being reproduced too closely.

## Quotation and Training Data Are Not the Same Problem

Using a short outside quote in book text and using large-scale material as AI `training data` raise different issues.

| Distinction | quotation in book text | use as AI training data |
| --- | --- | --- |
| where it appears | inside the visible text read by the audience | inside the model-training process |
| scale | should be limited to what is needed | may involve large-scale collection and copying |
| source visibility | the reader can verify the source | the origin of training data is often opaque |
| purpose | explanation, criticism, research, educational support | improving model performance, providing a service, possible commercial use |
| main risk | excessive quotation, replacing the original, missing attribution | unauthorized copying, market substitution, output similarity, lack of transparency |

Article 28 of the Korean Copyright Act permits quotation of published works for reporting, criticism, education, and research when the use stays within a justified range and follows fair practice. That is not the same as a simple rule saying:

> if the source is written, it is acceptable

The user's own writing still has to remain central, the quoted portion has to remain subordinate, and the amount cannot exceed what is needed.

Article 35-5 of the same law addresses fair use in a more general sense. It asks whether the use conflicts with ordinary exploitation of the work or unfairly harms the legitimate interests of the rightsholder, and it considers factors such as purpose, character, amount, and market effect.

Article 37 separately requires source attribution when a work is used under those provisions. Attribution therefore matters, but attribution alone is not a universal permit. Copyright review is not one checkbox. It is a judgment that combines several conditions.

This is why the review question cannot be reduced to:

> did we write the source?

It also has to ask:

> what was used, for what purpose, in what amount, and in what way?

## The Core of the Training-Data Debate

In generative AI, `training data` is the material from which the model learns patterns. Debate begins when that material includes copyrighted sources such as public webpages, books, articles, images, or code.

Rightsholders commonly raise issues such as:

| Issue from the rightsholder side | Description |
| --- | --- |
| unauthorized reproduction | collecting, storing, and processing works for training may count as copying |
| market substitution | AI output or services may replace demand for the original works |
| transparency | it is often hard to verify what material was used in training |
| output similarity | generated output may become too similar to the expression of an existing work |

AI developers and service providers often respond with arguments such as:

| Argument from the AI developer side | Description |
| --- | --- |
| transformative use | the claim that the goal is statistical pattern learning rather than redistributing the original work |
| fair use | especially important as a legal defense in the U.S. |
| text and data mining | some jurisdictions discuss exceptions for data analysis and research |
| output control | filters, policies, and evaluation are used to reduce overly similar output |

The important point is that this debate is not yet settled into one simple answer. Judgments can differ by country, kind of material, purpose of use, market effect, output behavior, contract, and license.

## What Lawsuits and Reports Show

The New York Times lawsuit against OpenAI and Microsoft became a prominent example because it raised concrete claims about training on news content without permission and about generated output that could substitute for the original reporting. That is useful as a case showing the dispute itself, not as a final legal conclusion.

Materials from the U.S. Copyright Office are also useful because they organize current legal and policy discussion around AI and copyright, including the topic of generative AI training. But those materials do not directly replace legal judgment under Korean copyright law.

Research that treats generative AI as a `supply chain` is also helpful, because it divides the issue into data collection, model training, prompting, output generation, deployment, and use. That prevents oversimplified conclusions such as:

> AI made it, so it must be fine  
> or  
> if it was used for training, it must all be infringement

## Authoring Rules for Handling Korean Publications

This book is a publicly distributed web book, so it needs a stricter standard than a personal memo.

| Type of material | Rule in this book |
| --- | --- |
| paid textbooks or ebooks | do not paste the original into AI tools or ask AI to summarize it |
| unauthorized scans or copied PDFs | do not use them |
| bookstore tables of contents | do not reproduce long tables of contents; only refer at the topic level |
| papers and official documents | verify the original and cite only what is actually connected to the claim |
| news and columns | use them to introduce events and viewpoints, while separating factual claims from interpretation |
| diagrams and images | do not copy without license confirmation; redraw when needed |
| code examples | do not paste external code directly; create original examples |

In particular, this book avoids:

> copying a book's table of contents in long chapter-and-section order  
> paraphrasing lecture-material explanations as if they were newly written  
> feeding paid ebooks to AI and turning them into summaries  
> reusing exercise-book questions and solutions as examples  
> attaching a source while still copying long passages from articles

What the book needs is not a replacement summary of someone else's original work, but a reorganization of topics and concepts so that a beginner can relearn them.

## Generated Output Also Needs Review

The fact that a sentence was produced by AI does not remove copyright risk. If the output becomes too similar to an existing work, or follows the structure of a specific article, book, or lecture material too closely, that can still be a problem.

| Review question | Why it matters |
| --- | --- |
| is the wording too similar to a specific original source? | risk of copying expression |
| does it follow the table-of-contents structure of a specific book too closely? | risk in the similarity of selection and arrangement |
| does it state factual claims without a source? | risk of unsupported claims and false attribution |
| has the quoted part become more important than the book's own writing? | risk of breaking the main-subordinate relationship |
| does it replace the need for the reader to consult the original? | risk of market substitution |

AI drafts are always subject to review. "The AI wrote it" does not reduce responsibility.

## Checklist

- You can explain that copyright mainly protects concrete `expression`, not ideas alone.
- You can distinguish attribution from permission, licensing, and quotation review.
- You can explain that quotation under Article 28 of the Korean Copyright Act requires a justified range and fair practice.
- You can explain that fair use under Article 35-5 is judged by considering purpose, character, amount, and market effect together.
- You can explain that source attribution under Article 37 matters, but does not by itself authorize every use of copyrighted material.
- You can explain that quotation in visible text and use as AI training data are different issues.
- You can distinguish the main arguments of rightsholders and AI developers in the training-data debate.
- You can explain why lawsuits and reports show disputed cases rather than final legal conclusions.
- You can explain why paid ebooks, unauthorized PDFs, and closed lecture materials should not be used as AI input in this project.
- You can explain why AI output also needs review for substantial similarity to existing works.
- You can separate `protection of expression`, `quotation review`, `training-data debate`, and `material-use hold rules` when explaining copyright review.

## Sources and Further Reading

- Korean Law Information Center, [Copyright Act](https://www.law.go.kr/법령/저작권법){: target="_blank" rel="noopener noreferrer" }, effective 2026-05-11, accessed 2026-07-19.
- U.S. Copyright Office, [Copyright and Artificial Intelligence](https://www.copyright.gov/ai/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19.
- U.S. Copyright Office, [Copyright and Artificial Intelligence, Part 3: Generative AI Training](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-3-Generative-AI-Training-Report-Pre-Publication-Version.pdf){: target="_blank" rel="noopener noreferrer" }, pre-publication version, 2025-05-09, accessed 2026-07-19.
- Haleluya Hadero, David Bauder, [The New York Times sues OpenAI and Microsoft for using its stories to train chatbots](https://apnews.com/article/6ea53a8ad3efa06ee4643b697df0ba57){: target="_blank" rel="noopener noreferrer" }, Associated Press, 2023-12-27, accessed 2026-07-19.
- Katherine Lee, A. Feder Cooper, James Grimmelmann, [Talkin' 'Bout AI Generation: Copyright and the Generative-AI Supply Chain](https://arxiv.org/abs/2309.08133){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, accessed 2026-07-19.
- Daniel M. German, [Copyright related risks in the creation and use of ML/AI systems](https://arxiv.org/abs/2405.01560){: target="_blank" rel="noopener noreferrer" }, arXiv, 2024, accessed 2026-07-19.
