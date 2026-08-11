# P6-8.1 Pretraining That First Builds a Broad Language Base

> Section ID: `P6-8.1`
> Version: `v2026.07.26`

Up to P6-6, we saw that the Transformer and GPT structures create next-token candidates, and that output selection rules change the stability and diversity of actual answers. But that still leaves one thing. `Why do some models respond plausibly across broader scenes even with the same generation structure, while others quickly reveal limits?`

From this question onward, the computation structure alone is not enough. Now we need to read together `what is learned first`, `at what scale it is learned`, and `what later adjustment is placed on top`. Chapter 7 is the starting point of that learning axis.

In P6-5.2, we saw that a conversational LLM is a user experience where instruction following, safety adjustment, and interface layers are added on top of a simple autocomplete model. Here, we go one level lower and look again at what base the model must first have before such adjustments are added.

Pretraining is the stage where, before entering one specific task, a model first learns general language patterns and expressions from large-scale text. In other words, it is closer to a preparation stage that first learns a broad basic sense of language than to a stage that immediately solves practical work problems.

## Stage Building a Broad Language Base First

The foundation-learning stage begins with the following questions.

- What does pretraining learn?
- Why learn first from large text, and then adjust later for a purpose?
- How are pretraining, fine-tuning, and instruction tuning distinguished?

Pretraining is a `foundation-learning stage that first learns large-scale general patterns`. This criterion is needed so that fine-tuning and instruction tuning are not lumped together under the same name of learning.

Scale and computation constraints are the problem of `why we build such a broad base at such a large scale`, and instruction tuning and alignment are the problem of `how we fit that base to user requests and policy criteria`. If we first separate pretraining, these later questions do not get mixed into one bundle.

If we see pretraining as a `magical process that stores knowledge as a whole`, later explanations shake. A more accurate starting point is that before the generation structure leads to actual task adjustment, the model first learns broad language patterns and expression relationships.

Therefore, the core is not the impression of `an already smart model`, but the structure of `first learning a broad language base and later adding purpose-specific adjustment`.

## Why Read the Learning Axis Again After Generation?

A common misunderstanding right after understanding the generation structure is to feel, `Then if models share the same structure, they will respond similarly.` But in reality, they do not. Even with the same Transformer structure, the basic response range differs greatly depending on what was first learned and how broadly it was learned, and the user experience changes again depending on what adjustment is added on top.

So Chapter 7 is not a separate topic attached after generation principles, but the start of the learning axis that answers `why the basic response range differs even with the same generation structure`. What we first grasp here is pretraining, which learns a broad language base before a specific task. Scale is the problem of why we try to make that base large, and fine-tuning, instruction tuning, and alignment are the problem of how we further fit that base to user purposes and policy criteria.

The impression that `the model is already smart` should be reread as `a structure where large-scale general patterns are learned first and later purpose-specific adjustment is added`.

Therefore, the center of this section is the sense that `a language base is made first`. Once this criterion is in place, later fine-tuning and instruction tuning also begin to look not like adding new functions, but as later adjustments that narrow an already-made base toward purposes and user responses.

## Distinguishing Broad Language Base from Later Adjustment

- You can explain pretraining at an introductory level.
- You can say the difference between pretraining, fine-tuning, and instruction tuning.
- You can explain why pretraining becomes the base for transfer to diverse tasks.
- You can read the `data and scale` problem as a problem of the size of the pretraining base.

This distinction is needed for the following reasons.

- because it lets us read several later models from the common perspective of pretraining
- because it ties later explanations of fine-tuning, instruction tuning, prompts, and alignment into one line

## Distinguishing Foundation Learning and Later Adjustment

To understand pretraining, we need to separate the `stage that creates a broad base` from the `stage that narrows it for a purpose`.

| Stage to Distinguish | Criterion to Check |
| --- | --- |
| Pretraining | Does it first make a broad language base rather than specific task answers? |
| Fine-tuning | Does it further narrow an already-made base to specific task data? |
| Instruction tuning | Does it adjust the model to respond better to users' natural-language request formats? |
| Case judgment | Can we separate whether what is lacking now is language base, task adjustment, or request-format adjustment? |

## What Does Pretraining Learn?

Pretraining is not the stage where the model first learns one internal task of a company or one specific exam problem. It is the stage where it first learns broader text patterns.

| Question | Short Answer |
| --- | --- |
| What does the model learn at this stage? | general patterns of how sentences and expressions continue |
| What does it not yet learn? | specific company policies or specific task rules |
| Why go through this stage first? | to make a base that can later be used commonly across many tasks |

For example, the model can indirectly learn things such as:

- which words and expressions often appear together
- what structures sentences usually continue with
- how formats such as questions, explanations, comparisons, and summaries appear
- which token more naturally follows in a specific context

In other words, it is safer to see pretraining as a process that first learns the `large statistical structure of language use`.

## Why Learn Broadly First and Adjust Later?

We need to grasp this question first to distinguish `making a small task model from the beginning` from `learning broadly and then narrowing for a purpose`.

Why not immediately make only a customer-center classification model, and why first train a large general model?

The reason is simple.

- if general patterns are learned first
- then later, even with small data
- the model can adapt better to several tasks

It is helpful to understand it as follows.

`Pretraining first creates a general-purpose language sense, and later detailed task adjustment is placed on top of it.`

This also connects to the perspectives of transfer and generalization learned in Part 3.

In other words, pretraining is closer to `first making the ground for solving problems` than to `solving the problem immediately`.

This criterion must be visible for the explanation of scale in P6-8.2 to continue naturally. The question `why use such large data and computation?` connects to how broad and heavy the preparation stage of `first making a broad base`, which we are looking at now, actually is.

For example, even when making customer-center classification, if the model has first broadly learned sentence structure and expression differences, it becomes easier to adapt it later to narrower classification rules such as `refund`, `exchange`, and `account issue`.

## How Are Pretraining, Fine-Tuning, and Instruction Tuning Different?

These three expressions often appear together, but they are not the same thing.

| Category | Core Question |
| --- | --- |
| Pretraining | Does it first learn general language patterns? |
| Fine-tuning | Are weights further adjusted to specific task data? |
| Instruction tuning | Is it adjusted to follow users' natural-language instructions better? |

If we do not distinguish this difference, users can easily misunderstand that `the model originally knew everything` or that `writing prompts well has the same effect as learning`.

We can first grasp it with this one-line comparison.

- pretraining: learn broadly
- fine-tuning: narrow for a purpose
- instruction tuning: make it respond better to human request formats

## Pretraining Is Not the Same as Fact Storage

We need to separate this point first so that `broadly learning patterns` is not misunderstood as the same thing as `perfectly storing facts`.

It is risky to explain pretraining as follows.

> The model memorizes all facts in the world.

A safer explanation is the following.

> The model learns patterns and expressions from large-scale text.
> As a result, it can create plausible sentences and structures well,
> but it does not always guarantee knowledge whose facts have been verified.

In other words, pretraining is closer to:

- language pattern learning
- expression learning
- next-token prediction structure learning

and is not the same as a `truth guarantee system`.

## Why Does Pretraining Connect to Several Tasks?

Because a pretrained model already knows general language patterns, it can more easily connect to diverse tasks when small adjustments are added on top.

For example, tasks such as:

- summarization
- classification
- question answering
- information extraction
- translation

can continue on top of one large foundation model instead of each starting as a completely different model.

This is an important shift in the LLM era.

## Pretraining Base and Remaining Adjustment

If we summarize this so far in the shortest form, it is as follows.

- Pretraining first makes a `broad language base`.
- Fine-tuning makes `specific task responses` clearer.
- Instruction tuning creates `a way of responding better to human request formats`.

This distinction helps reduce both the misunderstanding that `the model originally knows everything` and the misunderstanding that `changing only the prompt has the same effect as learning`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-07/p6-c07-s01-pretraining-flow-en.mmd"
```

This diagram organizes that pretraining is not the end, but the starting point for several later usage methods. So the result to check in this diagram is whether, after a broad base is made from large text, later stages are actually read as a flow that adjusts that base by purpose.

The most important way to read this figure is as follows.

- large text is the `material`
- pretraining is `making a broad base`
- later stages are `adjustments that use that base for a purpose`

## Cases and Examples

The diagram below groups the three cases in this section around the common question `do we first make a broad language base and place a purpose on top?`, rather than `do we train only one task from the beginning?`

```mermaid
--8<-- "assets/part-06/chapter-07/p6-c07-s01-pretraining-cases-en.mmd"
```

What we should confirm from this diagram is that all three scenes are closer to `first making a broad base and later adjusting a purpose` than to `learning only one purpose by heart from the beginning`. Even when tasks differ, the sequence of first learning general patterns and then placing detailed purposes on top is common.

### Case 1. Document Summarization

Suppose we try to build a model that summarizes long meeting minutes right away from the beginning. When people see this problem, they may first think, `Wouldn't a few thousand summary examples be enough?` But if the data stops at that level, the model has to learn not only summarization rules but also sentence structure and information arrangement at the same time, making the start heavy. For example, it must keep the order `conclusion -> reason -> next action` inside the summary, but if the language base is weak, sentence connection can often shake before key-sentence compression.

What changes here is a shift from the criterion `just give more summary examples` to the criterion `first have a broad language base and place the summarization purpose on top`. A pretrained model starts in a state where it has already learned sentence patterns and compression forms to some degree from broad text. So even for the same summarization task, it can reduce the stage of `learning language itself from scratch` and enter summarization-purpose adjustment more quickly. So the result to check in this case is whether key-sentence compression and sentence connection stabilize faster even with a small amount of summary data.

This case matters because it is easy to feel that once task examples are collected, a task model can be made immediately. But summarization is not simply reducing length; it becomes stable only when the model already knows to some degree, at the language level, which information is central and in what order it should remain. If summarization alone is learned immediately while the language base is weak, the model must newly learn both `what to summarize` and `how to connect sentences`. So the value of pretraining is not in memorizing summarization rules instead, but in first reducing the language-base burden before the task.

If we reread this difference from the perspective of work preparation, it looks as follows.

| Starting Method | What Is Easy to Expect First | What Is Likely to Be Lacking First in Practice |
| --- | --- | --- |
| start directly with only summary data | because task examples exist, it seems the model will immediately learn summarization | sentence connection, key-information arrangement, compressed expressions |
| summarize after a broad text base | it can look like a detour | it first reduces the language-structure burden before the task |
| small summary data + pretraining base | it can work to some degree with small data | it can focus on task-purpose adjustment more quickly |

The misunderstanding to correct in this table is the thought that `if summary data looks plentiful, the language base is also solved together`. In reality, there must be a base that handles language structure before the summarization task, so that the model can converge more stably even with the same number of summary examples.

### Case 2. Customer-Inquiry Classification

Suppose we classify customer inquiries into `refund`, `delivery`, and `account`. If there is not much labeled data, people easily think, `If we just attach labels, can't we make a classifier right away?` But when training a new model from the beginning, there may also be too little data for learning sentence expressions themselves. For example, `I canceled the payment; when will it be reflected?` and `I want to check the cancellation processing status` can be the same flow even though their surface sentences differ.

When people use a simple criterion, they first look at how many words overlap, but this criterion alone can often miss sentences whose expressions differ greatly. If fine-tuning is done on top of pretrained representations, the model is already in a state where it can read similar sentence structures and word relationships to some degree. So even with little labeled data, it becomes easier to quickly match `which business flow this sentence is close to`. So the result to check in this case is whether similar inquiries gather into the same handling queue more stably even when the exact same words do not appear.

This scene is also directly connected to practical work. In customer-inquiry data, expression variation is usually a bigger problem than the number of labels. Even the same refund inquiry can be phrased differently by each person, using words such as `cancel`, `withdraw`, `return`, and `refund request`. It is easy to feel that if the label definition is clear, the classifier will immediately stabilize, but in reality, before labels, a base that reads `same intent despite different expression` is needed. Pretraining matters because it broadly creates this expression base and then lets small labeled data narrow the business boundaries.

The difficulty of the same classification task changes depending on preparation state.

| Classification Preparation Method | What Is Expected First | Problem Encountered in Practice |
| --- | --- | --- |
| start directly with labeled data | labels alone seem enough to create classification boundaries | same inquiries with different expressions are often missed |
| fine-tune on pretrained expressions | it can look like a detour | similar-intent grouping can begin with fewer labels |
| simple rule based on word overlap | it seems fast | weak on same-flow inquiries with different surface words |

The important criterion in this case is separating `memorizing labels` from `reading the same intent even when expressions differ`. Because pretraining first reduces this second burden, classification can stabilize faster even with small labeled data.

### Case 3. Conversational Response

When a conversational LLM answers naturally, it can feel as if it learned only conversation from the beginning. But what we should first think about is that these responses also sit on top of a base that learned sentence connection and general language patterns. For example, to respond to requests such as `explain briefly`, `organize step by step`, and `add cautions too`, the model must broadly know sentence structure and explanation methods before dialogue format.

If we use a simple criterion, it is easy to feel that conversation quality will appear immediately if the final tone adjustment improves. But if the underlying language patterns are weak, explanation order and sentence connection can easily collapse even if polite tone is added. What changes here is a shift from first looking at `final tone adjustment` to first looking at `whether the language base underneath is sufficient`. Actual conversational adjustment is usually added by placing extra instruction following and response-format adjustment on top of this broad language base. So the result to check in this case is whether explanation sentence connection and basic response structure remain natural to some degree even before tone adjustment.

If we group the three cases again from the foundation-building perspective, we get the following.

| Situation | What Is Likely to Be Lacking First If Starting Only With Task Data | What the Pretraining Base Gives First |
| --- | --- | --- |
| Document summarization | sentence connection and general compression patterns | broad language structure and information-arrangement sense |
| Customer-inquiry classification | grouping same inquiries with different expressions | base for reading similar sentence relationships |
| Conversational response | explanation sentence connection and basic response structure | general language flow of question-answering |

We also need to clearly hold that all three cases point in the same direction. Summarization, classification, and conversation look like different tasks on the surface, but all three return to the question of whether the problem we see now should be read immediately as lack of task rules, or whether a broad language base is weak before that. This common question is needed so the flow of reading P6-8.2, `why try to make that broad base large`, does not break.

## Scenes Where Learning Stages Split

After reading this section, even if you do not yet know the large-scale training procedure in detail, you can first practice separating whether what is needed now is `broad foundation learning`, `task adjustment`, or `instruction adjustment`. If there are some summary examples but sentence connection and key compression themselves often shake, it may not be a problem solved only by adding more summary data; you should check whether the broad language base is weak. If classification into `refund`, `exchange`, and `account` works but same inquiries with different expressions are often missed, you should ask whether fine-tuning on top of a base that reads expression relationships is needed before label definitions. If basic explanation works but request formats such as `in three sentences`, `calmly`, and `step by step` are often violated, the instruction adjustment layer may be appearing first rather than the need to make pretraining bigger.

What matters here is not seeing `large pretraining solves everything`, but first reading `the stage that learns broadly`, `the stage that narrows for a purpose`, and `the stage that fits human request formats` as different levels.

The things often mixed here are as follows.

- It is easy to bundle pretraining, fine-tuning, and instruction tuning all as the same additional learning.
- It is easy to feel that if there are a few task examples, the language-base burden is also solved together.
- It is easy to see conversational format problems as the same cause as lack of foundation learning.

Therefore, the sentence `pretraining first makes a broad base` should become a criterion for classifying real problems.

The purpose of this distinction is not to decide the cause all at once. Instead of flattening it into one sentence, `more learning is needed`, it is to briefly distinguish whether the phenomenon you are seeing first appears in `broad base`, `task adjustment`, or `request-format adjustment`.

## Exercise and Example

The goal of this example is to directly see `how patterns are first collected from general text, and how those patterns are narrowed further with small task data`. It is not an example that implements real LLM pretraining, but a reduced experiment that separately observes how connections change when the training-data bundle changes.

The example data is in [p6-7-pretraining-stage-sentences-en.csv](/AiBook/assets/part-06/chapter-07/p6-7-pretraining-stage-sentences-en.csv){ .csv-preview }. One row is one short training sentence, and `stage` indicates which learning bundle the sentence belongs to. `general_text` is broad general sentences, `customer_support` is customer-center domain sentences, and `instruction_reply` is response sentences that match request formats.

Input:

- `general_text`: sentences containing broad general expressions such as documents, meetings, questions, and explanations
- `customer_support`: sentences containing specific business vocabulary such as refund, delivery, account, and exchange
- `instruction_reply`: sentences showing response formats such as `step_by_step`, `calmly`, and `three_sentences`

Output:

- number of connections when only the general corpus is seen
- connections newly created or strengthened when customer-center domain sentences are added
- request-format connections that appear only when instruction-style response sentences are added

The key point to confirm is that `more learning` is not one kind of change. A general corpus creates broad language connections, domain sentences add specific business vocabulary connections, and instruction-style response sentences separately strengthen connections that fit human request formats.

```python
# This example compares which next-token links are maintained, created, or strengthened as CSV sentences are added stage by stage.
from collections import Counter, defaultdict
from csv import DictReader
from pathlib import Path

DATA_PATH = Path("docs/assets/part-06/chapter-07/p6-7-pretraining-stage-sentences-en.csv")

STAGE_BUNDLES = [
    ("general_only", ("general_text",)),
    ("with_domain", ("general_text", "customer_support")),
    ("with_instruction", ("general_text", "customer_support", "instruction_reply")),
]

FOCUS_LINKS = [
    ("broad_language", "content", ("check", "organize", "summarize", "explain")),
    ("domain_support", "refund", ("inquiry", "request", "status", "process")),
    ("instruction_style", "step_by_step", ("guide", "explain", "summarize")),
]

DOMAIN_START_TOKENS = {"refund", "delivery", "account", "exchange"}


def load_rows(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(DictReader(f))


def build_bigram_counts(sentences):
    counts = defaultdict(Counter)
    for sentence in sentences:
        tokens = sentence.split()
        for left, right in zip(tokens, tokens[1:]):
            counts[left][right] += 1
    return counts


def rows_for_stages(rows, stages):
    return [row for row in rows if row["stage"] in stages]


def link_count(counts, left, rights):
    return sum(counts[left][right] for right in rights)


rows = load_rows(DATA_PATH)

print("[stage_rows]")
for stage in ("general_text", "customer_support", "instruction_reply"):
    print(f"{stage}: {sum(row['stage'] == stage for row in rows)}")

print("\n[focus_link_counts]")
for link_name, left, rights in FOCUS_LINKS:
    values = {}
    for bundle_name, stages in STAGE_BUNDLES:
        bundle_rows = rows_for_stages(rows, stages)
        counts = build_bigram_counts(row["sentence"] for row in bundle_rows)
        values[bundle_name] = link_count(counts, left, rights)
    print(
        f"{link_name}: "
        f"general_only={values['general_only']}, "
        f"with_domain={values['with_domain']}, "
        f"with_instruction={values['with_instruction']}"
    )

print("\n[new_links_after_domain]")
general_counts = build_bigram_counts(
    row["sentence"] for row in rows if row["stage"] == "general_text"
)
domain_counts = build_bigram_counts(
    row["sentence"] for row in rows if row["stage"] == "customer_support"
)
new_links = []
for left, right_counts in domain_counts.items():
    if left not in DOMAIN_START_TOKENS:
        continue
    for right, domain_count in right_counts.items():
        if general_counts[left][right] == 0:
            new_links.append((f"{left} -> {right}", domain_count))

for link_name, count in sorted(new_links, key=lambda item: (-item[1], item[0]))[:6]:
    print(f"{link_name}: {count}")
```

This example was run with the local `.venv` Python environment and checked against the output in the body.

The execution result example can be read as follows.

```text
[stage_rows]
general_text: 40
customer_support: 24
instruction_reply: 12

[focus_link_counts]
broad_language: general_only=35, with_domain=46, with_instruction=48
domain_support: general_only=0, with_domain=8, with_instruction=8
instruction_style: general_only=0, with_domain=0, with_instruction=3

[new_links_after_domain]
refund -> inquiry: 2
refund -> process: 2
refund -> request: 2
refund -> status: 2
account -> inquiry: 1
account -> lock: 1
```

What we should first see in this output is `broad_language`. Broad connections such as `content -> check/organize/summarize/explain` already appear often when only the general corpus is seen. When domain sentences are added, this value grows further, but it is a change added on top of an existing language base rather than a completely new connection.

Conversely, `domain_support` is 0 with only the general corpus. Connections such as `refund -> inquiry/request/status/process` appear only after customer-center sentences are added. This is close to what task adjustment does. It makes specific business vocabulary and procedures clearer on top of an already-made language base.

Finally, `instruction_style` remains 0 even after domain sentences are added, and appears only after instruction-style response sentences are added. This value shows that beyond pretraining and fine-tuning, a separate layer may be needed to adjust responses to the user's request format.

As a graph, the difference that the three connections do not grow in the same way becomes clearer.

![Next-token link counts by learning stage](/AiBook/assets/part-06/chapter-07/pretraining-adaptation-counts-en.png)

The core to read in this example is as follows.

- A general corpus first creates broad language connections.
- Adding customer-center sentences newly creates or strengthens domain connections such as `refund`, `delivery`, `account`, and `exchange`.
- Adding instruction-style response sentences separately creates connections that match request formats, such as `step_by_step guide`.
- In other words, pretraining broadly makes base patterns, and later adjustment is closer to making business vocabulary or response formats stand out on top of that base.

## Distribution Shift Seen in Separating Learning Stages

This example again shows that we should not lump pretraining and later adjustment together under one sentence, `the model learned a lot`. Even with the same next-word structure, the stage made with a general corpus shows `broad language connections`, while the stage with added domain sentences shows `reinforced specific business expressions`. When reading later fine-tuning, instruction tuning, and alignment, we also need the habit of first separating `the stage that broadens foundation ability` from `the stage that fits response behavior to a purpose`.

Pretraining is a key transition for explaining the LLM era. Language models and representation learning existed before, but as the approach of first learning general patterns from large-scale text and later connecting to diverse tasks became central, the way models are used changed.

What we need to hold more importantly is that `the stage that broadens foundation ability` and `the stage that places task-specific adjustment on top` are not the same layer. Even when reading the LLM era, we need to understand it as a structure where a large foundation model is first made and several task adjustments are then placed on top, so fine-tuning, instruction tuning, and alignment become easier to read within one flow.

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why does sentence connection itself shake even with a few summary examples? | Is the broad language base sufficient before task adjustment? |
| Why are same inquiries with different expressions often missed even when label definitions are clear? | Is the base for reading expression relationships weaker than the task rules? |
| Why does the model often violate request formats even though basic explanation works? | Should the instruction adjustment layer be handled more than foundation learning? |

## Checklist
- Can you explain pretraining as `broad foundation formation` separately from fine-tuning?
- Can you explain why prompt use and learning-stage adjustment should not be seen as the same layer?
- Are you ready to read scale as the problem of `why that base is made at such a large scale`?

## Sources and References

- Alec Radford et al., `Improving Language Understanding by Generative Pre-Training`, OpenAI, 2018, accessed 2026-07-19. [https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }
- Jeremy Howard, Sebastian Ruder, `Universal Language Model Fine-tuning for Text Classification`, arXiv, 2018, accessed 2026-07-19. [https://arxiv.org/abs/1801.06146](https://arxiv.org/abs/1801.06146){: target="_blank" rel="noopener noreferrer" }
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
- Daniel Jurafsky, James H. Martin, `Speech and Language Processing` draft materials, accessed 2026-07-19. [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }
