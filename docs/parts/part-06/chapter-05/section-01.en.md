# P6-5.1 GPT Family Through Decoder-Based Cumulative Generation

> Section ID: `P6-5.1`
> Version: `v2026.07.26`

So far, we have reread the Transformer from an LLM perspective and checked context window and attention constraints. Now, even within the same Transformer family, we need to distinguish `the flow that reads input` from `the flow that keeps generating onward`.

If we read the GPT family only as product names, it is easy to miss why this family became the representative path of generative LLMs.
Here, we read GPT as a `decoder-centered generation flow` and first distinguish how it differs from flows like BERT that read the entire input and make a judgment.

Where do models that keep generating onward sit inside the Transformer family?
The GPT family is a flow that centers on the Transformer's decoder, looks at the previous token context, predicts the next token, and generates long text by repeating that process.

## Decoder-Based Sequential Generation Structure

The sequential generation structure begins with the following questions.

- What position does the GPT family have inside the Transformer?
- Why does GPT look like a `model that keeps generating onward`?
- Compared with the BERT family, what is the biggest difference?

Once we first grasp GPT's generation structure, pretraining, next-token prediction, instruction tuning, and alignment problems can also be read on top of the same flow.
In other words, what we need here is a criterion for seeing GPT as a `decoder-based generation structure` rather than as a product lineage.

We read GPT not as a product name but from the structural position of a `decoder-based generative model`. Therefore, what we must first grasp is not a `famous model name`, but `why GPT is read as a sequential generation structure`.

| What We Are Reading Now | Question That Expands Later |
| --- | --- |
| Why GPT is read inside the Transformer family as a `generation flow that keeps writing onward` | How pretraining scales this structure |
| How to distinguish BERT and GPT from the perspectives of input reading and sequential generation | What instruction tuning, alignment, and commercial model version differences change further |

This section's role in the main request flow of Part 6 is to show how the Transformer computation engine becomes a `generation flow that keeps writing onward`. This structure must be in place before we can read P6-6.1's next-token prediction and P6-7.1's pretraining on top of the computation flow instead of jumping directly to user experience.

## Distinguishing Decoder-Based Cumulative Generation

- You can explain the GPT family as a decoder-centered Transformer flow.
- You can say why GPT connects directly to next-token prediction.
- You can explain the difference between BERT and GPT from the perspective of `reading the whole sentence` versus `sequential generation`.
- You can explain that adjustment layers that change user experience can be added on top of this generation structure.

We need to understand GPT as a generation structure to explain why the experience of writing a request in natural language and receiving a result became possible.
However, GPT's sequential generation structure and the user experience of conversational LLMs are not the same level. GPT is a structure that appends the next token based on previous tokens, while the conversational experience is made when instruction following, roles, safety constraints, and interfaces are added on top of that structure.

## Criteria for Comparing Sequential Generation Structures

To read GPT not as a product name but as a sequential generation structure, we need to distinguish four levels.

| Level to Distinguish | Criterion to Check |
| --- | --- |
| Structural position | Can GPT be read as a decoder-centered Transformer flow rather than an encoder-centered one? |
| Generation method | Can it be explained as repeated next-token prediction rather than outputting a completed sentence? |
| Comparison criterion | Can the difference from BERT be distinguished as reading the whole input versus continuing the output? |
| Concrete scene | Can we check in examples whether early choices keep pushing the later generation path? |

## GPT Name and Meaning

GPT stands for `Generative Pre-Trained Transformer`. The name already contains three key points.

- Generative
- Pre-Trained
- Transformer

That is, it means that the model:

- aims at generation
- is first pretrained on large-scale data
- uses the Transformer structure

## Why Is GPT Read Like a `Generative Model`?

The GPT family is usually explained as an autoregressive language model flow that predicts the next token by looking at previous tokens.

For example, suppose the input is as follows.

> Today's meeting is in the afternoon

The model predicts the next candidates from here.

- `at three`
- `at two`
- `at one`

After choosing one, it includes that new token and predicts the next token again.

In other words, the core sense of the GPT family is this.

`It does not pull out a completed sentence all at once; it creates output by repeatedly predicting the next token onward.`

## Why Is It Called Decoder-Centered?

As we saw earlier in Part 6, the Transformer can be read as encoder, decoder, and encoder-decoder structures.

It is safe to see the GPT family as a decoder-centered flow among these.

The core of this structure is that it:

- looks at the context so far
- can generate the next token at the current position
- places attention constraints that match the generation direction

We can understand it as follows.

`GPT is less a model that reads the whole sentence at once and makes a judgment, and more a model that keeps writing the back part based on what has been written in front.`

## Difference Compared with BERT

To summarize again:

| Category | BERT Family | GPT Family |
| --- | --- | --- |
| Central structure | encoder | decoder |
| Basic sense | read the whole input context and create representations | generate the next token based on previous tokens |
| Representative use flow | classification, search, embedding | generation, conversation, summarization, drafting |
| Output character | label, score, representation | new token, new sentence, new paragraph |

The core of this table is the following.

`BERT is more natural for reading input and judging it, while GPT is more natural for continuously creating output.`

## Why Did the GPT Family Change User Experience So Much?

The GPT family is structurally well suited to generation. As a result, users can write a request to a model in natural language, and the model creates a long response by continuing after it.

For example:

- writing an answer to a question
- drafting an email
- summarizing a document
- code autocomplete
- role-based conversation

All of these experiences can be explained as `repetition of next-token generation`.

In other words, technically the GPT family is a next-token prediction model, but from the user's point of view it feels like an `interface that keeps writing sentences for you`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-05/p6-c05-s01-diagram-01-en.mmd"
```

What we should confirm from this diagram is that the GPT family is not a structure that pulls out a completed sentence all at once,
but a generation structure that repeatedly appends next-token candidates based on the previous tokens.

## Cases and Examples

The diagram below groups the three cases in this section again around the common question `how does the initial token choice push the later path?`, rather than around `what is the generated result?`.

```mermaid
--8<-- "assets/part-06/chapter-05/p6-c05-s01-diagram-02-en.mmd"
```

What we should confirm from this diagram is that even when tasks differ, the generation sense is similar.
They all have the structure that `the token or sentence chosen now becomes part of the next input for later output`, so early choices keep pushing the entire later path.

### Case 1. Autocomplete

When a user has only written `The meeting is tomorrow afternoon`, it is easy to feel that the model thinks of the whole sentence at once.
But in actual autocomplete, the model first places next candidates such as `at two`, `at three`, and `at four`, chooses one of them, and then calculates the next token candidates again. In other words, the model does not pull out the completed sentence as a whole; it looks at the tokens that have appeared so far and appends likely next tokens in order.

What changes here is that we stop expecting `a sentence completed all at once` and instead see `a structure where earlier choices keep pushing the later sentence`. If the time is chosen incorrectly at an earlier step, the entire later sentence continues based on that time expression.

For example, if `at four` is selected first instead of `at three`, the later meeting-room notice or attendance request can also continue on the assumption of that time. The misunderstanding to correct here is the sense that `an early word can easily be overwritten later`.

So the result to check in this case is whether the whole later sentence changes when the first few token choices change, and whether early choices actually lock in the direction of the later sentence.

### Case 2. Summary Drafting

When a user enters long meeting minutes and asks, `Summarize this in three sentences`, it is easy to think that the whole summary is first decided and then printed as is.
But internally, the first sentence is created, and that sentence itself becomes part of the context for the next output, so the second and third sentences continue after it. In other words, summarization is also ultimately built on a generation structure that continues next tokens.

What changes here is that we see the first sentence choice chain into the direction of later sentences, rather than feeling that `the summary result is decided all at once`. If the first sentence catches the wrong key point, later sentences can inherit that wrong focus and bend the direction of the whole summary.

For example, if the first line incorrectly asserts `the deployment schedule was confirmed`, even a meeting whose actual center was a discussion about postponement can continue with later sentences that reinforce that wrong conclusion. The misunderstanding to correct here is the expectation that `even if the first sentence is slightly off, the later sentences will rebalance it`.

So the result to check in this case is whether later summary sentences also lean in the same direction when the focus of the first sentence wavers, and whether an early assertion changes even the emphasis order of later sentences.

### Case 3. Code Generation

A developer can give a function name, input description, and expected behavior and ask for an implementation.
Code generation can feel like pulling out one completed answer block as a whole, but in reality, the function definition, indentation, conditionals, and return statements continue in token order. So a variable name or condition generated incorrectly early on keeps affecting the later code.

What changes here is that, instead of expecting `code completed all at once`, we first see that one early token can pull the whole later structure. For example, if `user_id` is chosen incorrectly early on, later lookups, exception handling, and return statements can follow the same error in a chain.

The fact that even one mismatched parenthesis can collapse the whole later block into a syntax error shows the same structure. The misunderstanding to correct here is the sense that `early variable names or conditions are minor choices`.

So the result to check in this case is whether an error in an early token choice shakes later variable names, branches, and syntax in a chain, and whether one earlier choice actually fixes several later lines.

If we group the three cases again from the perspective of cumulative generation, we get the following.

| Situation | What an Early Choice Pushes Especially Strongly | What Also Shakes Later |
| --- | --- | --- |
| Autocomplete | first expressions such as time and topic | the development of the whole later sentence |
| Summary drafting | the focus of the first sentence | the emphasis order of later summary sentences |
| Code generation | variable names, conditions, parenthesis structure | branches, returns, syntax stability |

## Scenes Where the Cumulative Generation Structure Appears

After reading this section, even if you do not yet know the details of next-token prediction or instruction tuning, you can first practice distinguishing `whether the scene you are seeing is a problem of GPT's cumulative generation structure` as follows.

| Scene You See Now | Misunderstanding That Comes First | Question to Ask Instead |
| --- | --- | --- |
| When the first expression in a sentence changes, the tone and flow of the later explanation also change | It is easy to feel that the model has decided the whole sentence all at once | Is this a structure where earlier token choices keep changing later candidate paths? |
| Autocomplete is natural, but formats such as `answer in three sentences` are often violated | It is easy to feel that if the GPT structure just gets bigger, the chatbot experience will be solved immediately | Is what is blocked now a problem of the conversational adjustment layer rather than the generation structure? |
| In long code generation, one early variable name shakes later branches and return statements | It is easy to feel that errors in the front can be overwritten easily later | Does the early token choice actually fix the later code structure? |

What matters in this table is not memorizing GPT as a product name, but applying the structure that `what was generated earlier becomes part of the later input` to concrete scenes.

Two things are often mixed here.

- It is easy to bundle GPT's cumulative generation structure and the conversational adjustment layer into the same problem.
- It is easy to underestimate how strongly one earlier token choice pushes the whole later path.
- It is easy to see autocomplete, summarization, and code generation as different kinds of magic, while missing that they actually sit on the same sequential generation structure.

So the closing point of this section is to turn the phrase `GPT is a generation structure that keeps writing onward` into a criterion for distinguishing real examples.

The purpose of this distinction is not to decide the cause all at once. Instead of flattening the situation into one sentence, `GPT is strange`, it is to briefly distinguish whether the phenomenon you are seeing comes first from the `sequential generation structure` or from the `conversational adjustment layer`.

## Exercise and Example

The goal of this example is to confirm that GPT-family generation does not `pull out a completed sentence all at once`, but repeatedly chooses next-token candidates by looking at the token sequence so far.
In particular, we directly see that if the first choice changes, the later candidate table and final sentence flow also change.

The code below uses a starting token sequence, next-token candidate tables that change depending on the current last token, and two generation paths with different first choices. In the result, we check each path's step-by-step current context, next-token candidates and scores, cumulative score sum, and how the cumulative generation result splits when the first choice changes.

The key point to confirm is that in autoregressive generation, one early choice can greatly split the later candidate path and final sentence.

```python
# This example shows how the first token choice in GPT-style autoregressive generation splits later candidate tables and the final sentence path.
start_sequence = ["Today", "the", "meeting", "is"]

next_token_scores = {
    "is": [("afternoon", 0.62), ("online", 0.27), ("canceled", 0.11)],
    "afternoon": [("at_three", 0.55), ("at_four", 0.28), ("at_five", 0.17)],
    "online": [("today", 0.64), ("room_link", 0.21), ("announced", 0.15)],
    "at_three": [("confirmed", 0.58), ("scheduled", 0.25), ("starting", 0.17)],
    "today": [("confirmed", 0.67), ("changed", 0.21), ("announced", 0.12)],
}

paths = {
    "path_a_time_flow": ["afternoon", "at_three", "confirmed"],
    "path_b_online_flow": ["online", "today", "confirmed"],
}

def render_english_text(tokens):
    """Token labels are kept visible, but display helpers replace underscores in the final text."""
    return " ".join(token.replace("_", " ") for token in tokens)

print("start =", start_sequence)

for path_name, chosen_tokens in paths.items():
    sequence = start_sequence[:]
    cumulative_score = 0.0
    print("=" * 80)
    print("[path]", path_name)
    for step, token in enumerate(chosen_tokens, start=1):
        current_last_token = sequence[-1]
        candidates = next_token_scores.get(current_last_token, [])
        print(f"step {step} context =", sequence)
        print(f"step {step} candidates after '{current_last_token}' =", candidates)
        chosen_score = dict(candidates)[token]
        cumulative_score += chosen_score
        sequence.append(token)
        print(f"step {step} chosen =", token)
        print(f"step {step} chosen_score =", chosen_score)
        print(f"step {step} cumulative_score =", round(cumulative_score, 2))
    print("final_sequence =", sequence)
    print("final_text =", render_english_text(sequence))
    print("path_score_total =", round(cumulative_score, 2))
```

The output below was checked by running the body code with the local `.venv` Python environment.

You can read the execution result example as follows.

```text
start = ['Today', 'the', 'meeting', 'is']
================================================================================
[path] path_a_time_flow
step 1 context = ['Today', 'the', 'meeting', 'is']
step 1 candidates after 'is' = [('afternoon', 0.62), ('online', 0.27), ('canceled', 0.11)]
step 1 chosen = afternoon
step 1 chosen_score = 0.62
step 1 cumulative_score = 0.62
step 2 context = ['Today', 'the', 'meeting', 'is', 'afternoon']
step 2 candidates after 'afternoon' = [('at_three', 0.55), ('at_four', 0.28), ('at_five', 0.17)]
step 2 chosen = at_three
step 2 chosen_score = 0.55
step 2 cumulative_score = 1.17
step 3 context = ['Today', 'the', 'meeting', 'is', 'afternoon', 'at_three']
step 3 candidates after 'at_three' = [('confirmed', 0.58), ('scheduled', 0.25), ('starting', 0.17)]
step 3 chosen = confirmed
step 3 chosen_score = 0.58
step 3 cumulative_score = 1.75
final_sequence = ['Today', 'the', 'meeting', 'is', 'afternoon', 'at_three', 'confirmed']
final_text = Today the meeting is afternoon at three confirmed
path_score_total = 1.75
================================================================================
[path] path_b_online_flow
step 1 context = ['Today', 'the', 'meeting', 'is']
step 1 candidates after 'is' = [('afternoon', 0.62), ('online', 0.27), ('canceled', 0.11)]
step 1 chosen = online
step 1 chosen_score = 0.27
step 1 cumulative_score = 0.27
step 2 context = ['Today', 'the', 'meeting', 'is', 'online']
step 2 candidates after 'online' = [('today', 0.64), ('room_link', 0.21), ('announced', 0.15)]
step 2 chosen = today
step 2 chosen_score = 0.64
step 2 cumulative_score = 0.91
step 3 context = ['Today', 'the', 'meeting', 'is', 'online', 'today']
step 3 candidates after 'today' = [('confirmed', 0.67), ('changed', 0.21), ('announced', 0.12)]
step 3 chosen = confirmed
step 3 chosen_score = 0.67
step 3 cumulative_score = 1.58
final_sequence = ['Today', 'the', 'meeting', 'is', 'online', 'today', 'confirmed']
final_text = Today the meeting is online today confirmed
path_score_total = 1.58
```

![Cumulative generation paths split after the first token choice](/AiBook/assets/part-06/chapter-05/autoregressive-path-split-en.png)

So the result to check in this example is that generation does not pull out a completed sentence all at once; previous outputs change the next candidate set and accumulate one token at a time. In particular, depending on whether the first choice is `afternoon` or `online`, the second candidate table already changes, and `cumulative_score` also accumulates along different paths. In this sense, it is more accurate to read GPT-family generation as a `structure where earlier choices keep pushing later paths and cumulative score flows`.

## Where Cumulative Generation Paths Split

The previous example is not code that implements GPT, but the shortest scene showing that generation is not `pulling out a completed sentence as a whole`, but `a cumulative process where previous output becomes part of the next input`. The key point to read here is that before sentence quality, generation is a structure that appends one step at a time.

The GPT family matters because Transformer decoder-based generative models led to a flow that changed actual user interfaces.

Historically important points are as follows.

- generative pretraining showed that it could transfer to many tasks
- as model scale grew, zero-shot and few-shot use experiences became stronger
- it created the foundation that later led to instruction tuning and conversational interfaces

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why does the first expression push the whole later sentence? | Is this a cumulative generation structure where previous output becomes part of the next input? |
| Why can autocomplete work while chatbot-like formatting is not followed well? | Are you separating the generation structure from the conversational adjustment layer? |
| Why is it insufficient to group BERT and GPT only as the same Transformer? | Are you seeing the structural difference where sequential generation is central rather than whole-input reading? |

## Checklist
- Can you explain GPT as a `cumulative generation structure where previous output becomes part of the next input`?
- Can you distinguish BERT and GPT again by structure and task?
- Are you ready to read the following explanations by separating the generation structure from the conversational adjustment layer?

## Sources and References

- Alec Radford et al., [Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI 2018, accessed 2026-07-19. Used as the basis for the name Generative Pre-Training, the Transformer decoder-based language model, and the next-token conditional probability explanation.
- OpenAI, [Improving language understanding with unsupervised learning](https://openai.com/index/language-unsupervised/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as background evidence that early GPT research showed transfer to diverse language tasks by combining the Transformer with unsupervised pre-training.
- Alec Radford et al., [Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf){: target="_blank" rel="noopener noreferrer" }, OpenAI 2019, accessed 2026-07-19. Used as the basis for GPT-2 as a scale-up flow of Transformer-based language models and zero-shot task transfer.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv 2020, accessed 2026-07-19. Used as the basis for explaining GPT-3's autoregressive language model and text-interaction-based few-shot use flow.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv 2018, accessed 2026-07-19. Used as the basis for comparing BERT with GPT by noting that BERT aims at bidirectional encoder representations.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as general NLP background evidence for language models and Transformer language models.
