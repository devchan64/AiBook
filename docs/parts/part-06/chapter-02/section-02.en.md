# P6-2.2 Model Input As Source Strings, Tokens, And Token IDs

> Section ID: `P6-2.2`
> Version: `v2026.07.23`

In P6-2.1, we held onto the token as a computational unit for explaining length, cost, truncation, and context preservation. Now we need to read how that computational unit appears in tokenizer output and model input.

The center of this section is not explaining the word token broadly. It is to distinguish the `token pieces`, `token count`, and `token IDs` visible in tokenizer output, and to hold onto the fact that those IDs become a sequence used as model input.

## Values To Distinguish First In Tokenizer Output

A token is the basic computational unit a model counts when handling inputs and outputs. But in an actual output screen or log, a token does not appear as only one value. The source string, token pieces, token count, and token IDs often appear together, and if these values are mixed together, it becomes unclear how model input is made.

Tokens are not decided as meaning units that are convenient for people to read. They are determined by the vocabulary and splitting rules of a particular model's tokenizer. So even for the same source text, token pieces and token counts can change when the model or tokenizer changes.

The minimum distinction needed here is as follows.

| Distinction | Question to read first | Problem if misunderstood |
| --- | --- | --- |
| Source string | What did the person actually enter? | You may mistake sentences or words for the model's input units. |
| Token pieces | In what sequence did the tokenizer split the source? | You may read visible pieces as if they were word definitions. |
| Token count | How many computational pieces are there? | You may treat character count, word count, and token count as the same value. |
| Token ID | Which vocabulary number does each piece point to? | You may think the size of an ID number contains meaning or importance. |

This table is the standard for this section. First read separately `how the source was split`, `how many pieces there are`, and `which number each piece became`, and then look at how those numbers are placed in sequence as model input.

## Misunderstandings To Drop First

Depending on the case, a token can look like the following.

- One word
- Part of a word
- A short piece including a space
- A piece mixed with numbers and symbols
- A piece attached to punctuation

In other words, a token is not always the same as the intuitive `word` a person feels. Something that looks like one word can be split into several tokens, and a part people do not easily see as a word, such as a piece with a leading space, can be included in a token boundary.

The difference becomes clearer in the following table.

| Unit people see | Question the model asks again |
| --- | --- |
| Is it one word? | How many computational pieces is it? |
| Is it one line of sentence? | How does it become a token sequence? |
| Is it the same expression? | Is it the same piece as computational input? |

This difference often appears especially in the following scenes.

| What appears in the source | What can change in tokenization |
| --- | --- |
| A Korean expression written together, such as `환불정책` | It can split into `환불`, `정책`, or smaller pieces. |
| An expression with numbers and symbols, such as `10:00 AM` | Numbers, colon, space, and English pieces can split separately. |
| An English word such as `tokenization` | It can split into frequent subword pieces such as `token` and `ization`. |
| Spaces and punctuation before or after a sentence | A space or period can appear as a separate piece or as an attached piece. |

The important point is not that the split shown above appears exactly the same in every model. The actual split differs by tokenizer. But whatever result appears, the reading standard is the same. Look at the source first, then the boundaries of token pieces, and finally the token count and IDs.

Another misunderstanding is reading a token like the symbol from symbolic AI seen in Part 1. A symbolic-AI symbol was closer to the name of a meaning or rule chosen by people. By contrast, an LLM token is a computational piece made by a tokenizer splitting the source text, and the model turns that piece into an ID and vector for probabilistic computation.

Therefore, we should not overinterpret tokens as logical symbols. On the other hand, we should not pass over token IDs as meaningless internal numbers either. What is needed now is not reading token pieces as definitions, but reading which vocabulary number each piece becomes and where it is placed in the model input.

## How Tokens Are Used Inside The Model

Tokens are not computed as-is. A model usually handles input in the following flow.

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s02-token-id-input-flow-en.mmd"
```

Two points matter in this flow.

- The model does not compute the source string directly. It first converts it into token pieces and a token-ID sequence.
- Token IDs are then looked up as vector representations and enter the actual computation.

In other words, a token is closer to the entrance where model computation starts than to a finished meaning unit by itself.

This flow matters from an engineering perspective because the values people can actually inspect also change along this flow.

| Value people can inspect | What this value means |
| --- | --- |
| Token pieces | What computational pieces the model split the source into |
| Token count | How many computational pieces there are |
| Token IDs | Which numbers in the model's internal vocabulary represent each piece |

So knowing `what a token is` does not mean memorizing one definition. It means being able to distinguish what you are reading later when you see tokenizer output or logs.

When reading token IDs, one more caution is needed. An ID is closer to an identifier saying `which entry in the vocabulary this piece is`. If `4012` is larger than `812`, that does not mean the token is more important or more complex. What matters in model computation is not the size of the ID itself, but which embedding vector that ID retrieves and how it enters later context computation.

## Output-Value Distinction Cases And Examples

### Case 1. When The Word People See Differs From The Token

Suppose the expression `refundpolicy` keeps appearing in a customer-support document. A person reads this expression as one word with a clear meaning. So it is easy to think the model also receives this one word as one computational unit.

But in model input, `whether a person feels it is one word` is not the standard. In tokenizer output, we must check whether this expression remains as one piece, splits into several pieces, and which ID is attached to each piece. Especially in sentences where endings, particles, or closed-up expressions are mixed, the word boundary people see and the tokenizer boundary can easily diverge.

The result to check in this case is that `a token is not always the same as the word a person feels`. Even when looking at the same expression, source string, token pieces, token count, and token IDs must be read separately.

| What people see first | What to recheck in tokenizer output | Judgment gained here |
| --- | --- | --- |
| The word `refundpolicy` | How many token pieces there are | Check whether the word boundary and token boundary are the same. |
| The sense that it is one word | How many tokens there actually are | Separate human-felt length from computational length. |
| The meaning a person knows | Which token ID is attached to each piece | Confirm that you are seeing vocabulary item numbers, not definitions. |

### Case 2. When One Sentence Becomes A Token Sequence

A person reads `The meeting is tomorrow at 10:00 AM` as one schedule sentence. By human standards, one sentence, one meaning, and one time value appear first.

But the model does not place the whole sentence into computation at once. It first converts the source string into a sequence of token pieces, counts those pieces, attaches IDs to each piece, and then prepares for computation.

At first, separating only the following four levels is enough to reveal the difference between a sentence and computational input.

| Level | Value to read in this case |
| --- | --- |
| Source string | `The meeting is tomorrow at 10:00 AM` |
| Token pieces | A piece sequence such as `The` / ` meeting` / ` is` / ` tomorrow` / ` at` / ` 10` / `:` / `00` / ` AM` |
| Token count | How many computational pieces one sentence became |
| Token IDs | Which vocabulary numbers each piece became |

The result to check in this case is that the model first receives not `the meaning of the whole sentence`, but `a sequence of pieces that can be numbered`. What matters more than the exact token count is distinguishing which level of value you are looking at. With this distinction, when model input is read as `a sequence of token IDs`, the values do not feel like internal implementation details that suddenly appeared.

### Case 3. When Tokens Are Not Computed Directly

Suppose a log prints token pieces and token IDs together. At first, token pieces alone can seem sufficient. Because the pieces are visible, it is easy to feel that the model computes those character pieces themselves.

But token pieces are displays that people can inspect easily, and when the input moves into model computation, each piece needs a corresponding token ID. That ID must again become a vector representation to enter actual computation. In other words, the `token piece` is an easy-to-observe marker, while the `token ID` is closer to a key used to look up an embedding in the model's vocabulary.

The same flow can be shortened as follows.

| Stage | What happens here |
| --- | --- |
| Sentence | Source string read by people |
| Token sequence | Ordered computational pieces read by the model |
| Token ID | The number each piece points to in the vocabulary |
| Embedding vector | Numerical representation that enters actual computation |

The result to check in this case is that token pieces and token IDs should not be treated as the same thing. Token pieces show how the source was split, and token IDs show which numbers the pieces are handled as inside the model.

The same scene can be compressed once more into a comparison table.

| Standard easy to grab first | Standard to recover |
| --- | --- |
| It is one word | Source string and token pieces can differ |
| It is one line of sentence | Token count is counted separately from sentence count |
| Token pieces are visible | Model computation continues through token IDs and vector conversion |
| It looks like a meaningful symbol | A token is not a human-chosen logical symbol, but a computational piece made by a tokenizer |

## Practice Asking At The Right Level

Even if we cannot run an actual tokenizer yet, we can practice changing `what people first say` into `a model-standard checking question` as follows.

| Scene being viewed | What people are likely to say first | Question to ask first from the token standard |
| --- | --- | --- |
| One English word is visible | It is one word, so it should also be one computational piece | How many pieces does the tokenizer actually split this expression into? |
| There is one schedule sentence | It is one sentence, so the computational input should also be one | How do the token pieces and token count appear? |
| A list of numbers appears in tokenizer output | It feels like a complicated internal value, so I want to skip it | Which sequence of token pieces do these numbers point to? |
| A token piece looks like a meaningful name | It seems fine to treat it as a symbol with fixed meaning | Is this a human-defined symbol or a computational piece made by a tokenizer? |

The important point in this table is not guessing the exact values in advance. What is needed first is distinguishing whether what you are seeing now is a word definition, a computational piece, a piece count, or a numbered input.

These are exactly the levels that often get mixed together.

- It is easy to feel that model computation has already started just by seeing the source string.
- It is easy to accept token pieces as word definitions.
- Token IDs can look so internal that it is easy to pass over them as meaningless.
- Because tokens look like markers, it is easy to read them at the same level as symbolic-AI symbols.

To read model input as a sequence of token IDs, these levels must first be distinguishable.

When the same distinction is applied to an actual log or explanation screen, read it as follows.

| Value shown in output | Interpretation not to make immediately | Interpretation to make first |
| --- | --- | --- |
| `tokens: ["refund", "policy"]` | The meaning of `refund policy` has already been explained | The source was split into these computational pieces |
| `count: 2` | It confirmed that there are two words | The number of pieces counted by the model is 2 |
| `ids: [4012, 8830]` | The larger number is the more important piece | These are numbers pointing to each piece in the vocabulary |
| The same ID appears twice | The same role has repeated twice | Check whether the position and surrounding context differ |

This table is a device for pausing again inside the current integrated section to check the distinction among `piece`, `count`, `number`, and `position`. If readers pass through this table, they can read the levels between tokenizer output and model input without seeing a token as an isolated name.

## Example Of Reading Tokenizer Output Values

Before comparing tokenization types, it is better to first check `how to read the token itself`. The example below simplifies three values often seen in real tokenizer output. It is not a table for memorizing the exact result of a particular model, but an example for distinguishing what to read from output.

- Token pieces
- Token count
- Token IDs

For example, suppose a tool outputs the following format. The token pieces and ID numbers below are simple examples for conceptual explanation. In an actual model tokenizer, piece boundaries and IDs can differ.

| Output item | Example value |
| --- | --- |
| Source string | `The meeting is tomorrow at 10:00 AM.` |
| Token pieces | `["The", " meeting", " is", " tomorrow", " at", " 10", ":", "00", " AM", "."]` |
| Token count | `10` |
| Token IDs | `[4012, 812, 5920, 110, 25, 405, 2710, 8831, 13, 9]` |

The result readers should immediately read here is as follows.

| What to look at first in the output | Meaning to understand here |
| --- | --- |
| Token-piece list | Which sequence of computational pieces the model changed the source into |
| Token count `10` | Even if it looks like one sentence, the model side counts several computational units |
| Pieces around numbers and time notation | Expressions such as `10:00 AM` can also split into several pieces |
| Token-ID list | The model prepares for computation with a numbered piece sequence, not the string itself |

When reading this table, judge as follows.

- Token pieces show the boundaries where the source was split.
- Token count shows how many computational pieces the source became.
- Token IDs are not meanings read by people, but vocabulary lookup results.
- Even for the same source, token pieces, token count, and IDs can change when the tokenizer changes.

Read one English word in the same way.

| Output item | Example value |
| --- | --- |
| Source string | `tokenization` |
| Token pieces | `["token", "ization"]` |
| Token count | `2` |
| Token IDs | `[30001, 14627]` |

The point to check here is that the human sense of `one English word` and the model sense of `two computational pieces` can differ.

Conversely, a short symbol or punctuation mark can also become a separate token. For example, a period `.` or colon `:` looks like an additional mark to a person, but it can appear as an independent piece in tokenizer output. So when looking at token count, first ask `how many pieces the tokenizer actually made`, not `how many important words there are`.

The goal of this example is not to memorize the exact numbers from a particular tokenizer. What is needed first is to clearly distinguish that in tokenizer output, `what I am seeing now is not a word definition but a computational piece, count, and number`.

Tokenizer output can be closed with the following three questions.

| Scene | Question to answer first |
| --- | --- |
| Token pieces are visible | What computational pieces did the model split the source into? |
| Token count is visible | How many computational pieces are there? |
| Token IDs are visible | In what numbered sequence are these pieces handled inside the model? |

The judgment to close in this example is not memorizing `what a token is` like a dictionary entry. It is enough to distinguish what `piece`, `count`, and `number` mean in tokenizer output.

## How A Token-ID Sequence Becomes Model Input

Earlier, we read tokens separately as `token pieces`, `token count`, and `token IDs`. Now we need to see how those values are used in model input.

The key is not the definition of one token but the `sequence` of tokens. The model does not receive the source sentence as a whole. It receives input where token IDs are lined up, and it continues the next computation on top of that order.

## The Sequence Matters More Than One Token

Tokens are not used only one at a time. In model input, multiple tokens are placed in order, and that order becomes material for the structure of the sentence.

| What people see first | What to recheck in model input |
| --- | --- |
| One sentence | Token-ID sequence |
| One word | One or several tokens |
| Same word repeated | Tokens placed at different positions |

Without token order, expressions with similar pieces, such as `refund possible` and `refund not possible`, are difficult to distinguish reliably. The model must read not only what each token is, but also which tokens were before and after it.

Here, `sequence` does not simply mean lining up tokens. Each token has its own position in the input, and that position is interpreted together with the tokens before and after it. Even the same token ID can play a different role in the next computation depending on what token came before and what token follows.

Written very small, input can be read as follows.

| Position | Token piece | Token ID | What to look at first in this position |
| --- | --- | --- | --- |
| 1 | `refund` | `4012` | Piece that opens the topic |
| 2 | `not` | `920` | Piece that can turn the following piece negative |
| 3 | `possible` | `7731` | Piece that combines with earlier pieces to make the final expression |

What matters in this table is not memorizing ID numbers. It is that even with the same piece list, we must see where each piece is placed and which pieces are attached before and after it to read model input.

## Token IDs Are Number Sequences That Enter Computation

The token IDs seen above are not simple labels. The model receives the sequence of token IDs rather than the string itself, then turns those IDs into vector representations and computes with them.

Written very simply, the flow is as follows.

| Stage | Role in model input |
| --- | --- |
| Source string | Text entered by a person |
| Token pieces | Computational pieces split from the source |
| Token-ID sequence | Number sequence the model actually receives |
| Vector representation | Internal representation used for computation |

The important point here is not explaining tokenization rules in detail yet. It is first holding onto the structure that `the model does not directly read the whole sentence, but receives a token-ID sequence as input`.

More carefully, when reading model input, we look at three things together.

| What to see | Question | Meaning here |
| --- | --- | --- |
| ID | Which token piece is in this position? | It shows which vocabulary item was brought in. |
| Order | Which token comes after which token? | It can create the structure of expression, negation, modification, and connection. |
| Position | Where is the same token placed in the input? | Even a repeated token can have a different contextual role. |

Therefore, model input is neither just an `ID list` nor just a `word-meaning list`. It is a structure that sees together `which ID is placed in which order and position`.

## ID-Sequence Cases And Examples

### Case 1. When The Input Changes Because The Same Pieces Change Order

Suppose we automatically classify `refund possible` and `refund not possible` in a customer-support document. A person immediately distinguishes the two expressions by meaning, but a reader seeing tokenizer output for the first time may feel they are similar inputs because both contain `refund` and `possible`.

The limit of that standard is that it sees tokens like a `list of included pieces`. In model input, what matters is not only which pieces are included, but where each piece is inserted. If a negating piece such as `not` appears before `possible`, the input sequence changes even though it contains the same `refund` and `possible` pieces.

The result to check in this case is that tokens should be read not as a set collected together, but as `a number sequence continuing from front to back`. The numbers are examples for explanation.

| Expression | Fast human standard | Standard to recheck in model input | Result to check |
| --- | --- | --- | --- |
| `refund possible` | It has `refund` and `possible` | `[4012, 7731]` | `possible` follows directly after `refund`. |
| `refund not possible` | It has `refund` and `possible` | `[4012, 920, 7731]` | A negating piece enters before `possible`. |

So the safer judgment in this case is not stopping at `which tokens are included`, but also checking `in what order those tokens are placed`.

### Case 2. When The Same Token Repeats But Its Position Differs

The input `The meeting is tomorrow. Please send the meeting materials.` contains `meeting` twice. A person may first see the same word repeated, and tokenizer output may also show the same token piece or the same ID twice.

But the fact that `the same ID appeared twice` is not enough to say the two positions play the same role. The first `meeting` appears in a position opening a schedule notice, while the second `meeting` appears before the request `materials`. Even the same token can be read differently in model input when its position and surrounding tokens differ.

The result to check in this case is that model input is not a `list of token types` but a `token sequence with positions`.

| Repeated token | Fast human standard | Standard to recheck in model input | Result to check |
| --- | --- | --- | --- |
| First `meeting` | The same word appeared again | It is at the sentence start and is followed by `is`, `tomorrow` | It opens what the schedule notice is about. |
| Second `meeting` | The same word appeared again | It follows the previous sentence and is followed by `materials`, `send` | It marks the target of the request. |

So the safer judgment in this case is to look first not at `is it the same token`, but at `where the same token is placed in the input and with which surrounding pieces`.

### Case 3. When Output Tokens Continue After Input Tokens

Suppose the user asks, `Tell me in one sentence when refunds are not possible`, and the model begins creating an answer. People usually see the answer sentence first as a completed artifact. That makes it easy to feel that the output is created all at once in sentence units.

The limit of that standard is that it sees input and output as disconnected chunks. When an LLM creates an answer, new output tokens continue after the input tokens already provided, and the output token just attached also becomes part of the previous context when the next output is chosen. What we need to hold here is not the details of the selection method, but the fact that input and output both continue on the same sequence.

The result to check in this case is that tokens are not markers used only when reading input. They are also the basic units by which output continues.

| Stage | Fast human standard | Standard to recheck in model input | Result to check |
| --- | --- | --- | --- |
| Question input | One question sentence enters | The question is placed as a token-ID sequence | The earlier sequence the model will use appears. |
| First output token generated | The answer begins | A new token attaches after the existing question sequence | Output continues after input. |
| Next output token generated | The answer gets longer | The next token attaches after the sequence containing the question and earlier output tokens | The output just made also becomes part of the next context. |

So the safer judgment in this case is not separating `input as input, output as result`, but reading that `output tokens continue after input tokens and the same sequence becomes longer`.

## Reading Tokens As A Sequence

When you see the following scenes, first distinguish whether you are seeing `tokens one by one` or `tokens as a sequence`.

| Scene | Thought to drop first | Thought to hold instead |
| --- | --- | --- |
| You see `refund possible` and `refund not possible` | They are similar inputs because they contain the same words | The order of token pieces differs |
| The same word appears twice | The same token always plays the same role | If position and surrounding tokens differ, the role can differ too |
| An answer is generated | The whole sentence comes out at once | Output is made as tokens continue in order |

The application level needed here is not complicated internal model equations, but reading tokens as `ordered input units` rather than as `individual names`.

If you see the same judgment in an actual log or explanation screen, check in this order.

| Check order | Value to see | Question to ask |
| --- | --- | --- |
| 1 | Token pieces | What pieces was the source split into? |
| 2 | Token IDs | What number did each piece become? |
| 3 | Position | At what position in the input is that number placed? |
| 4 | Surrounding context | How do nearby tokens change the role of this position? |

## Standard To Keep From Token-ID Sequences

The token is not simply a concept word. It is the basic unit through which model input and output continue. The question to close now is not an operation judgment, but the fact that tokens are used inside the model as `ordered input`.

Once this flow is understood, the need for tokenization, the procedure that turns a source string into this token sequence, also follows naturally.

## Exercises And Examples

The goal of this exercise is not guessing tokenization rules. It is practice in looking at given token pieces and IDs and reading model input not as `an individual list` but as `a sequence with positions`. For each item, first choose your own answer, then compare it with the explanation immediately below.

### Exercise 1. Finding Order Differences In The Same Piece List

The two inputs below contain all the same pieces: `refund`, `not`, and `possible`.

| Input | Simplified token-ID sequence |
| --- | --- |
| A | `[4012, 920, 7731]` |
| B | `[4012, 7731, 920]` |

First answer for yourself.

- Can the two inputs be treated as the same input?
- If they differ, which position difference appears first?
- Can this difference be explained only by a `token-type list`?

Explanation: The two inputs are not the same even though they contain the same pieces. In A, `920` is placed before `7731`, and in B, `920` is placed at the end. By the standard of this section, `which ID is placed in what order` comes before `what is included`.

### Exercise 2. Reading The Position Of The Same Token

Below is a simplified input where the same token ID `5100` appears twice.

| Position | Token piece | Token ID | Surrounding pieces |
| --- | --- | --- | --- |
| 1 | `meeting` | `5100` | Followed by `is`, `tomorrow` |
| 5 | `meeting` | `5100` | Followed by `materials`, `send` |

First answer for yourself.

- Since the two `meeting` tokens have the same ID, can we say they play the same role?
- To read the two positions differently, what value must we also see?
- What disappears if this input is reduced to a token-type list such as `{meeting}`?

Explanation: Even if the same ID repeats, we cannot conclude that it plays the same role. The two tokens are in different positions, and the pieces that follow them also differ. If we reduce the input to a token-type list, position and surrounding context disappear, so the key information needed to read model input is lost.

### Exercise 3. Tracking Where Output Tokens Attach

The table below simplifies the process where output tokens continue one by one after a question.

| Stage | Current sequence |
| --- | --- |
| Question input | `[question: refund, not, possible, case]` |
| After first output | `[question: refund, not, possible, case, answer: damaged]` |
| After second output | `[question: refund, not, possible, case, answer: damaged, product]` |

First answer for yourself.

- Is the second output token `product` a new sentence chunk separated from the question?
- What is included in the earlier sequence the model refers to when the second output attaches?
- What is missed if the output process is read only as `one completed sentence appears`?

Explanation: `product` is a new token continuing after the earlier question and first output token. At the moment the second output attaches, not only the question tokens but also the already generated `damaged` are part of the previous context. So output should be read not as a completed sentence appearing at once, but as the existing sequence growing token by token.

After the three exercises, you should be able to summarize the point in one sentence.

`Model input is not a collection of token types, but a number sequence where token IDs continue with order and position.`

## Checklist

- Can you explain that model input is not a whole sentence but a token-ID sequence?
- Can you distinguish token pieces, token count, and token IDs as different values in tokenizer output?
- Can you say that surrounding order and position matter more than the name of one token?
- Can you explain that answers are made as output tokens continue after input tokens?

## Sources And References

- OpenAI Help Center, [What are tokens and how to count them?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm that API request text is split into tokens and that responses are generated as token sequences before being converted into text.
- OpenAI, [tiktoken README](https://github.com/openai/tiktoken/blob/main/README.md){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm the explanation that language models see text as a sequence of token numbers rather than in the way people read it.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as background support for token sequences and language-model input in the `Words and Tokens` and `Large Language Models` chapters.
