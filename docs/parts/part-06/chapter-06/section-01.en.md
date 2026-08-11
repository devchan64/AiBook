# P6-7.1 Next-Token Prediction as the Starting Point of Long Generation

> Section ID: `P6-7.1`
> Version: `v2026.07.26`

In P6-5.2, we saw how a GPT-based generation structure led to the conversational LLM experience. Now it is time to narrow the question further.

What exactly does such a large model repeat during training? The answer most often heard when first encountering LLMs is this.

An LLM is trained to predict the next token.

This sentence is correct, but if it is too short, it causes misunderstandings. Many readers hear this and think, `Then is it just simple autocomplete?` Here, we organize that very question at a more accurate level.

When understanding generative LLMs, the first criterion is `what the model is repeatedly trained to get right`. Search and tool connections are devices that reinforce generated results, and alignment is a stage that adjusts response habits. Before those, the sense we need to hold is that `calculating the next-token distribution in the current context` is the starting point of long generation.

## Basic Goal Called Next-Token Prediction

The basic training goal begins with the following questions.

- What exactly does next-token prediction predict?
- Why can this seemingly simple goal lead to long sentences, summarization, question answering, and code generation?
- What can next-token prediction explain by itself, and what can it not explain?

What we deal with here is `what is used as the training objective`. Which candidate is actually chosen during generation is a problem of output selection rules, and how response habits are adjusted is a problem of alignment and later adjustment. We need to distinguish these three so we do not stretch the one phrase `next-token prediction` to mean too many things.

Therefore, the core is not the impression that it `looks like autocomplete`, but the training objective of `repeatedly calculating the next-token distribution in the current context`. In this section, we grasp what LLMs repeatedly predict during training, and why that local prediction becomes the starting point for long generation and diverse language tasks. Which candidate is actually selected remains a sampling problem for the next section, and how response habits and safety are adjusted remains a later problem of instruction tuning and alignment.

The goal is to establish criteria to the point where you can explain for yourself what the `basic training objective of LLMs` is.

We need to reread the impression of `a model that pulls out a sentence all at once` as `a structure that calculates the next-token distribution in the current context and accumulates that choice`.

## Distinguishing Next-Token Objective from Long Generation

- You can explain next-token prediction at the token level.
- You can explain that sentence generation is not completed all at once, but continues sequentially.
- You can say why a simple prediction objective can lead to complex language behavior.
- You can distinguish that this criterion alone cannot explain all of LLMs.

This criterion matters for the following reasons.

- because it bundles tokens, embeddings, and Transformers again under one training objective
- because it lets us explain the basic operation of generative AI without exaggeration
- because it lets us place sampling, temperature, prompting, and alignment later on top of this foundation

## Judgment Criteria for Next-Token Prediction

To avoid reading next-token prediction only as simple autocomplete, we need to separate four criteria.

| Judgment Criterion | Question to Check |
| --- | --- |
| Prediction unit | Does it calculate a candidate distribution for the next token rather than the whole sentence? |
| Token unit | Is it explained by token pieces rather than words? |
| Cumulative effect | When the current context changes, does the next candidate distribution change together? |
| Later connection | Does it lead to explanations of sampling, prompting, and alignment? |

## What Does Next-Token Prediction Mean?

During training, an LLM sees long text and is adjusted repeatedly to get right which token is likely to come after the tokens given so far.

For example, we can see it as follows.

- input context: `The weather today is very`
- next candidate tokens: `good`, `cold`, `clear`, ...

At this point, the model calculates a probability distribution for the `immediately next token` based on the `tokens so far`.

The important point is that the model does not pull out the whole sentence from the beginning. `Looking at the context so far, predicting one next piece, and attaching that piece back to the context` is repeated.

## Why Is It Token-Based?

LLMs usually do not handle raw characters directly, but handle text in token units. As we saw earlier in this book, a token can be a whole word, part of a word, or a symbol piece.

So saying `next word prediction` is often not precise. A safer expression is the following.

`An LLM is trained to predict the next token.`

We need to distinguish this difference to understand tokenization, context window, and cost calculation together later.

## Why Does a Simple Goal Lead to Complex Functions?

This is where readers most often stop. If a model only repeats `getting the next piece right`, why can it summarize, translate, and write code?

The core is as follows.

- language has sequential structure
- the next expression changes greatly depending on context
- if the model sees many long documents and diverse genres
- then to predict the next token well, it must reflect grammar, expression, relationships, format, and some world knowledge together

In other words, the training objective itself looks local, but to perform that objective well, the model must internally handle broad patterns.

This is why it is difficult to see LLMs as completely the same as simple autocomplete.

## How Far Is It Like Autocomplete, and Where Does It Differ?

The autocomplete analogy is useful because both share the structure of `choosing what comes after the current context`. Autocomplete and LLM generation resemble each other in that they look at the context entered so far, predict the next output, and create the result by appending one piece at a time.

But if we stop here, the explanation is insufficient. LLM generation can reflect much longer contexts, diverse document formats, task instructions, and conversation history together, and as a result expands into task forms such as summarization, question answering, explanation, transformation, and code generation. Therefore, the key comparison is not `is it the same as autocomplete or not`, but what burden the same next-token prediction structure begins to create in larger contexts and longer outputs.

| Comparison Axis | Short Autocomplete Analogy | What Appears More Strongly in LLM Generation |
| --- | --- | --- |
| Input context | part of a short sentence | can reflect long documents, conversation history, and instructions together |
| Output length | the next word or two | can continue into multiple sentences, code blocks, and summary paragraphs |
| Task scope | continuation-writing assistance | expands into diverse formats such as summarization, question answering, explanation, transformation, and code generation |
| Failure mode | awkward next word | can lead to larger-level failures such as factual errors, structural collapse, and wrong central sentences |

In other words, LLMs also start from something similar to autocomplete, but because the `input range`, `output length`, and `cost of failure` become much larger, we should read them as a broader system than simple sentence assistance. A safer summary is the following.

`LLMs are based on a next-token prediction structure, but through large-scale pretraining and additional adjustment, they come to perform many different forms of language work.`

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s01-next-token-loop-en.mmd"
```

The core of this diagram is that generation is not `a calculation that ends at once`, but `a repeated sequential calculation`.

## Cases and Examples

The diagram below groups the three cases in this section around the common question `how do early choices push the whole later context?`, rather than `choosing one next token`.

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s01-branch-effects-en.mmd"
```

What we should confirm from this diagram is that even when tasks differ, generation is all a cumulative structure. Because one early token choice can affect later sentences, later summaries, and later code structures in a chain, it is more accurate to read next-token prediction not as `picking one piece`, but as `a starting choice that sets the later flow`.

### Case 1. Continuing an Email Sentence

We can think of a customer email draft that starts with `Hello, regarding your inquiry`. When people see this sentence, it is easy to feel that the later sentence is almost fixed as one correct answer, but in reality, many expressions such as explanation, apology, and guidance can become candidates.

For example, even for the same inquiry, different starts such as `after checking`, `we apologize for the inconvenience`, and `we will guide you through the next steps` can all be natural. What changes here is moving from a criterion of `does it pull out one correct sentence?` to a criterion of `which candidate is more natural in the current context?`

What matters here is not that the next sentence is fixed as one thing, but which expression among several candidates is more natural in the current context. During training, the model sees these continuation patterns repeatedly and learns next-token distributions.

If the first sentence is set around apology, compensation or processing-schedule guidance is likely to follow; if it is set around checking results, explanatory sentences are likely to follow. So the result to check in this case is whether the tone of the later sentence and the later guidance flow actually change depending on the first expression choice, even with the same input.

This case matters because the generated result can feel like a process of `pulling out a correct sentence that exists somewhere in the head`. But in reality, it is closer to a cumulative structure where the first few tokens push the character of the later sentence. If an email draft starts with `we apologize`, it is likely to continue toward compensation and action guidance, while if it starts with `after checking`, it is likely to continue toward explanation and factual delivery. So when understanding next-token prediction, it is more accurate to see it as `early choices set the direction of the later flow` than as `the whole sentence is chosen at once`.

If we reread this difference from the perspective of continuation-writing choices, it looks as follows.

| First Expression Choice | Why It Looks Natural to a Human | Flow That Is Likely to Change in the Later Sentence |
| --- | --- | --- |
| `We apologize for the inconvenience` | Looks reasonable as a customer response | apology, compensation, and follow-up handling guidance are likely to continue |
| `After checking` | Looks reasonable as a factual-delivery start | explanatory sentences and cause summaries are likely to follow |
| `We will guide you through the next steps` | Looks like friendly guidance | step-by-step action guidance and links/method explanations are likely to continue |

The misunderstanding this table corrects is the expectation that `the later parts will be almost the same anyway because the sentences are similar`. In reality, the first few token choices keep pulling the later tone and guidance structure.

### Case 2. Summarization

We can think of a scene where meeting minutes are converted into a three-line summary. Looking only at the result, people easily feel that `summarization` is a separate ability and imagine that a compressed correct answer is pulled out all at once.

But in the actual generation process, the structure of continuing whichever expression is natural after the summary sentence made so far is repeated. For example, if the first line chooses `the deployment schedule was postponed`, the next line may more naturally continue with the reason or follow-up action.

What changes here is a shift from the sense that `the summary answer is pulled out all at once` to the sense that `the first sentence choice keeps pushing the later summary flow`. Of course, at this point, the core of the input document must be reflected internally so the model does not choose a strange next expression.

If the first line starts incorrectly, the later sentences follow that flow, so the cost of choosing a wrong central sentence early is large. In other words, summarization can also be read not as special magic, but as a sequence of next-token choices that reflect context. So the result to check in this case is whether the reason, action, and emphasis order of later sentences actually change together depending on how the first summary sentence starts.

This scene also directly touches a misunderstanding often felt in practice. After seeing the complete summary result, people easily imagine, `it must have known this whole summary from the beginning`. But in reality, what is chosen as the center in the first line keeps pushing the direction of the second and third lines. If it starts with `the deployment schedule was postponed`, reasons and follow-up actions are likely to attach later; if it starts with `legal review is needed`, risk and approval procedures are likely to become central. In other words, it is more accurate to read summarization not as an ability to pull out a completed compressed answer all at once, but as a cumulative generation structure where how the central sentence is chosen determines the later flow.

Even with the same meeting minutes, the later summary structure changes depending on the first-line choice.

| First Summary Sentence Choice | Impression That Comes First | What Is Likely to Be Emphasized Later |
| --- | --- | --- |
| `The deployment schedule was postponed` | Looks like a summary that catches the key conclusion first | reason for postponement, next action |
| `Legal review is needed` | Looks like a risk-centered summary | approval procedure, pending items |
| `The owner changed` | Looks like a handoff-centered summary | role transition, follow-up responsibility |

The important criterion in this case is not the impression that `a summary is a compressed result all at once`, but the structure that `the first central sentence pushes the emphasis order of later sentences`. The next-token prediction perspective is needed precisely to explain this cumulative effect.

### Case 3. Code Generation

We can imagine a scene where `def calculate_total` has been written in code generation. When people see this position, they expect structures such as parentheses, a colon, and an indented block to follow.

At the same time, code is much stricter than free-form prose, so even one token that does not fit the current context can easily collapse into a syntax error or flow error. For example, if the function name is about calculating a total but a discount variable is missed on the next line, or if a closing parenthesis is skipped, the whole later part can collapse.

The fact that one wrong conditional indentation can shift even the position of the return statement in a chain shows the same structure. What changes here is moving from the sense of `completing a code block all at once` to the sense that `early token choices keep pulling the whole later structure`.

LLMs handle these code token patterns, like natural language, inside a structure that repeatedly selects `what is most plausible after the current context`. So the result to check in this case is whether one early token choice shakes later variable names, indentation, and return structure in a chain.

If we group the three cases again from the next-token-choice perspective, we get the following.

| Situation | What the Current Context Determines First | Candidate That Immediately Changes in the Next Step |
| --- | --- | --- |
| Email continuation | tone such as apology, explanation, or guidance | tone of the later sentence and guidance flow |
| Summarization | central information in the first summary sentence | reason, action, emphasis order |
| Code generation | function structure and current block context | parentheses, indentation, return patterns |

## Scenes Where Next-Token Prediction Appears

Even if you do not yet know the details of sampling or temperature, you can briefly distinguish how the phenomenon you see connects to the training objective called next-token prediction. If apology, explanation, and guidance candidates are all natural after the same previous sentence, you should first ask `is the current context opening several next-candidate distributions?` rather than `is one correct sentence stored?` If the later sentence is pushed in the same direction after the first summary line is chosen incorrectly, you should ask `is this a sequential structure where the first choice keeps changing the later generation path?` rather than `was the whole summary pulled out at once?` If a whole code block collapses after one parenthesis is wrong, you should ask `does the current token choice change later context conditions in a chain?` rather than `one minor token will probably be recovered later`.

What matters in this distinction is not deciding `is it completely the same as autocomplete?`, but applying to actual cases the fact that long generation also sits on a structure that repeatedly predicts `what comes after the current context`.

The things often mixed here are as follows.

- It is easy to bundle the training objective `next-token prediction` and the whole service response into the same level.
- It is easy to see summarization, explanation, and code generation as different kinds of magic while missing that they all sit on the same sequential prediction structure.
- It is easy to underestimate how strongly one next-token choice pushes the whole later structure.

Therefore, the sentence `an LLM is trained to predict the next token` should not be a definition for memorization, but a criterion for reading actual generation scenes.

The purpose of this distinction is not to decide the cause all at once. Instead of memorizing `next-token prediction` only as a one-sentence definition, it is to briefly distinguish whether the phenomenon you are seeing first appears in `candidate distribution`, `cumulative generation`, or `chain errors`.

## Exercise and Example

The goal of this example is not to implement a whole real LLM, but to visually confirm `how next-token candidates are made from training data` and `whether the selected token becomes the input for the next step again`. Instead of manually entering a fixed score dictionary, we will directly count `previous three tokens -> next token` frequencies from a small group of sentences and then continue generating from several prompts with the result.

The code below uses several short training sentences, several generation-start prompts, and a maximum generation length. In the result, we see the next-token candidate distribution by context, the token selected at each step, what candidate competition existed at the first branch, and the final sequence accumulated through generation. When there are tied candidates, the candidate observed first is chosen to make the execution process look simple. This selection rule is not meant to imitate an actual LLM decoding strategy, but is a device for seeing the flow that `a candidate distribution arises, and when one is chosen, the next context changes`.

The key point to confirm is that the next-token distribution is made as the accumulated result of connection patterns repeated in the training sentences.

First, let's look at the small group of training sentences used as input. This input is not real LLM training data, but a reduced corpus designed to show the sense that `even when the previous context is the same, the next candidates can open into several branches`. Each group consists of two sentences that share the same front part, so candidates split into two at the first branch.

| Input Group | Training Sentence | Candidate Created at the First Branch |
| --- | --- | --- |
| meeting result | `meeting result deployment schedule was postponed to next week`<br>`meeting result priority fixes should be handled first` | `deployment`, `priority` |
| customer inquiry check result | `customer inquiry check result refund procedure will be provided`<br>`customer inquiry check result shipping schedule will be provided again` | `refund`, `shipping` |
| deployment error check result | `deployment error check result config file path was wrong`<br>`deployment error check result log collection range should be checked first` | `config`, `log` |

The code splits these sentences into whitespace-based tokens and counts the frequency of `previous three tokens -> next token`. A real LLM is not a structure that looks up this exact three-token table, but this reduced example aims to confirm the sequential generation sense that `a candidate distribution arises in the current context, and the selected token is attached back to the next context`.

```python
# This example counts next-token frequencies by previous three tokens from a small group of training sentences and continues prompts with that distribution.
from collections import Counter, defaultdict

training_sentences = [
    "meeting result deployment schedule was postponed to next week",
    "meeting result priority fixes should be handled first",
    "customer inquiry check result refund procedure will be provided",
    "customer inquiry check result shipping schedule will be provided again",
    "deployment error check result config file path was wrong",
    "deployment error check result log collection range should be checked first",
]

def tokenize(sentence):
    return sentence.split()

def build_ngram_counts(sentences):
    ngram_counts = defaultdict(Counter)
    for sentence in sentences:
        tokens = ["<BOS1>", "<BOS2>", "<BOS3>"] + tokenize(sentence) + ["<EOS>"]
        for i in range(len(tokens) - 3):
            context = (tokens[i], tokens[i + 1], tokens[i + 2])
            next_token = tokens[i + 3]
            ngram_counts[context][next_token] += 1
    return ngram_counts

def next_token_distribution(ngram_counts, context_tokens):
    context = tuple(context_tokens[-3:])
    counter = ngram_counts.get(context, Counter())
    total = sum(counter.values())
    if total == 0:
        return {}
    return {
        token: round(count / total, 2)
        for token, count in counter.most_common()
    }

def generate_tokens(ngram_counts, prompt, max_steps=5):
    generated = ["<BOS1>", "<BOS2>", "<BOS3>"] + tokenize(prompt)
    trace = []

    for _ in range(max_steps):
        context = generated[-3:]
        distribution = next_token_distribution(ngram_counts, context)
        if not distribution:
            trace.append(
                {
                    "context": tuple(context),
                    "distribution": {},
                    "selected": "<STOP:no-known-next-token>",
                }
            )
            break

        selected = max(distribution, key=distribution.get)
        trace.append(
            {
                "context": tuple(context),
                "distribution": distribution,
                "selected": selected,
            }
        )
        if selected == "<EOS>":
            break
        generated.append(selected)

    visible_tokens = [token for token in generated if not token.startswith("<BOS")]
    return visible_tokens, trace

ngram_counts = build_ngram_counts(training_sentences)
prompts = ["meeting result", "customer inquiry check result", "deployment error check result"]

for prompt in prompts:
    generated, trace = generate_tokens(ngram_counts, prompt, max_steps=5)
    print("=" * 80)
    print("prompt =", prompt)
    if trace:
        first_distribution = trace[0]["distribution"]
        print("first_branch_candidates =", first_distribution)
    for step_index, step in enumerate(trace, start=1):
        print(f"[step {step_index}] context =", step["context"])
        print("distribution =", step["distribution"])
        print("selected =", step["selected"])
    print("generated =", generated)
```

This example was run with the local `.venv` Python environment and checked against the output in the body.

The execution result example can be read as follows.

```text
================================================================================
prompt = meeting result
first_branch_candidates = {'deployment': 0.5, 'priority': 0.5}
[step 1] context = ('<BOS3>', 'meeting', 'result')
distribution = {'deployment': 0.5, 'priority': 0.5}
selected = deployment
[step 2] context = ('meeting', 'result', 'deployment')
distribution = {'schedule': 1.0}
selected = schedule
[step 3] context = ('result', 'deployment', 'schedule')
distribution = {'was': 1.0}
selected = was
[step 4] context = ('deployment', 'schedule', 'was')
distribution = {'postponed': 1.0}
selected = postponed
[step 5] context = ('schedule', 'was', 'postponed')
distribution = {'to': 1.0}
selected = to
generated = ['meeting', 'result', 'deployment', 'schedule', 'was', 'postponed', 'to']
================================================================================
prompt = customer inquiry check result
first_branch_candidates = {'refund': 0.5, 'shipping': 0.5}
[step 1] context = ('inquiry', 'check', 'result')
distribution = {'refund': 0.5, 'shipping': 0.5}
selected = refund
[step 2] context = ('check', 'result', 'refund')
distribution = {'procedure': 1.0}
selected = procedure
[step 3] context = ('result', 'refund', 'procedure')
distribution = {'will': 1.0}
selected = will
[step 4] context = ('refund', 'procedure', 'will')
distribution = {'be': 1.0}
selected = be
[step 5] context = ('procedure', 'will', 'be')
distribution = {'provided': 1.0}
selected = provided
generated = ['customer', 'inquiry', 'check', 'result', 'refund', 'procedure', 'will', 'be', 'provided']
================================================================================
prompt = deployment error check result
first_branch_candidates = {'config': 0.5, 'log': 0.5}
[step 1] context = ('error', 'check', 'result')
distribution = {'config': 0.5, 'log': 0.5}
selected = config
[step 2] context = ('check', 'result', 'config')
distribution = {'file': 1.0}
selected = file
[step 3] context = ('result', 'config', 'file')
distribution = {'path': 1.0}
selected = path
[step 4] context = ('config', 'file', 'path')
distribution = {'was': 1.0}
selected = was
[step 5] context = ('file', 'path', 'was')
distribution = {'wrong': 1.0}
selected = wrong
generated = ['deployment', 'error', 'check', 'result', 'config', 'file', 'path', 'was', 'wrong']
```

If we first compress the long execution result, it looks as follows.

| Prompt | First Candidate Distribution | Selected First Token | Later Generation Path |
| --- | --- | --- | --- |
| `meeting result` | `deployment`: 0.5, `priority`: 0.5 | `deployment` | `schedule -> was -> postponed -> to` |
| `customer inquiry check result` | `refund`: 0.5, `shipping`: 0.5 | `refund` | `procedure -> will -> be -> provided` |
| `deployment error check result` | `config`: 0.5, `log`: 0.5 | `config` | `file -> path -> was -> wrong` |

What we should first see in this summary table is that the first candidate is not fixed as one thing. Even in a small corpus made in the same way, the first candidate distribution changes when the current prompt changes, and when one first token is chosen, that token attaches back to the next-stage context and changes the later generation path.

The result to check in this example is that next-candidate distributions by context are made from training data, the candidate distribution changes when the current context changes, and the selected token becomes a longer context again and continues as the condition for the next choice. In particular, by looking at `first_branch_candidates`, we can immediately read that all three prompts already start differently from the first candidate competition.

- next candidates by context are aggregated from training sentences
- the next candidate distribution changes depending on the current context
- once one token is chosen, that token attaches back to the next-stage context
- early choices push the whole later generation flow

## Candidate Distributions Accumulated in Sequential Generation

This example should be read not as a box that pulls out the generation result all at once, but as a circular structure where `the context made so far` keeps returning as the condition for the next choice. After `meeting result`, candidates such as `deployment` and `priority` appear; after `customer inquiry check result`, candidates change to `refund` and `shipping`; after `deployment error check result`, candidates change to `config` and `log`. And once `refund` is chosen, tokens that fit that flow, such as `procedure`, `will`, `be`, and `provided`, continue; if `config` is chosen, a completely different path such as `file`, `path`, `was`, and `wrong` continues. So even when we later look at sampling, prompting, and alignment, it is important to keep the view that `the whole response is made as next-token choices accumulate`.

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why is the candidate not fixed as one thing after the same previous sentence? | Is the current context creating a distribution over several next-token candidates? |
| Why does the first-line choice shake later summaries and later code structures? | Is this a sequential structure where the selected token enters the next-stage context again? |
| Why can summarization, explanation, and code generation start from one training objective? | Do different tasks also sit on the ability to predict `what is natural after this point now`? |

## Checklist
- Can you explain next-token prediction as repetition of `a distribution over the next piece`, not as `the whole long answer`?
- Can you say both what makes autocomplete and LLMs similar and what makes them different?
- Are you ready to read the following explanation of generation choice as a problem of `which candidate is selected`, not `what was learned`?

## Sources and References

- Yoshua Bengio et al., `A Neural Probabilistic Language Model`, JMLR, 2003, accessed 2026-07-19. [https://jmlr.csail.mit.edu/papers/v3/bengio03a](https://jmlr.csail.mit.edu/papers/v3/bengio03a){: target="_blank" rel="noopener noreferrer" }
- Tomas Mikolov et al., `Recurrent Neural Network Based Language Model`, Interspeech, 2010, accessed 2026-07-19. [https://www.isca-archive.org/interspeech_2010/mikolov10_interspeech.html](https://www.isca-archive.org/interspeech_2010/mikolov10_interspeech.html){: target="_blank" rel="noopener noreferrer" }
- Alec Radford et al., `Improving Language Understanding by Generative Pre-Training`, OpenAI, 2018, accessed 2026-07-19. [https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }
- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
