# P6-2.3 Tokenization That Changes Length, Cost, And Chunks

> Section ID: `P6-2.3`
> Version: `v2026.07.24`

In P6-2.2, we separated token pieces, token count, token IDs, and the token-ID sequence in tokenizer output. Now we move one step beyond `how to read it` and look at how tokenization results change actual judgments.

The center of this section is not rereading tokenizer output values again. It is to hold onto the fact that the moment a source string changes into certain boundaries and an ID sequence, input length, cost, chunk boundaries, and output-preservation judgments change together.

## What Procedure Is Tokenization?

Once we know that tokens are computational units, we need to see how a string actually becomes those computational units. Tokenization is the procedure that changes source text into a token sequence read by the model.

The characters people see are not computed as-is. We first need to see the flow where a tokenizer sets boundaries, chooses pieces in a vocabulary, and changes those pieces into IDs.

## Why Tokenization Is Needed Separately

People see sentences as characters, words, and sentences. But models do not use these units directly for computation. First, the input must be changed into computable pieces, and those pieces must be numbered and passed into computation.

So tokenization is not an add-on feature. It is the first gate from `source string -> token sequence -> token ID`.

The important point here is that tokenization is not simple whitespace splitting. A tokenizer looks at the source, makes possible piece boundaries, checks whether those pieces are in the vocabulary, and finally creates the ID sequence the model will receive. So when reading tokenization results, it is safer to ask the following three questions in order.

| Reading question | Value to check | Easy misunderstanding |
| --- | --- | --- |
| Where was it split? | Boundaries of token pieces | Thinking they match the word boundaries people see |
| What piece was accepted? | Token piece connected to the vocabulary | Thinking all visible character pieces are handled the same way |
| What number was attached? | Token-ID sequence | Interpreting ID numbers as meaning or importance |

## What Tokenization Actually Does

In tokenization, the following usually happen together.

- It decides boundaries for splitting the source string.
- It connects the split pieces to a token vocabulary.
- It changes each piece into a token ID and passes it to model computation.

Something that looks like one word to a person can be split more finely, and parts people do not strongly notice as meaning units, such as spaces or punctuation, can affect token boundaries.

Written more step by step, the same procedure looks like this.

| Step | What happens here | Common human misunderstanding |
| --- | --- | --- |
| 1. Look at the string | Decide where to split the source | Assuming character or word boundaries will stay the same |
| 2. Choose pieces | Connect pieces to items in the token vocabulary | Assuming a piece matching the human word always exists |
| 3. Change to IDs | Create token IDs corresponding to each piece | Assuming the model understands the sentence directly |

In other words, tokenization does not end at `cutting a string`. It includes `which piece will be treated as a vocabulary item` and `which ID will be passed for that piece`.

The same procedure becomes clearer in a small example. The values below are not actual tokenizer output; they are explanatory examples for showing the reading order.

| Source string | Possible token pieces | Possible token IDs | What to read here |
| --- | --- | --- | --- |
| `환불정책` | `["환불", "정책"]` | `[4012, 8830]` | An expression that looks like a word can connect as two pieces. |
| `10시에` | `["10", "시", "에"]` | `[110, 740, 812]` | Numbers and Korean particles can become different boundaries. |
| `Authorization` | `["Author", "ization"]` | `[6201, 14627]` | A long English expression can connect as subpieces. |

What this table asks us to check is not the numbers themselves. During the change from `source -> token pieces -> token IDs`, the word boundaries a person felt are reset as computational boundaries made by the tokenizer.

## Drawing The Tokenization Procedure In One Line

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s03-tokenization-flow-en.mmd"
```

In this flow, tokenization is the stage that changes `a string into a token sequence and token IDs`. Only after that are IDs looked up as vector representations and connected to computation.

## Tokenization-Procedure Cases And Examples

### Case 1. When We Trust Something That Looks Like A Word As-Is

Suppose the expression `refundpolicy` repeats in a customer-support document. A person quickly reads this as one meaningful word. So it is easy to think the tokenizer will also pass this string as one piece.

The limit of that standard is that it treats the word boundary a person feels as the same as the tokenizer boundary. In tokenization, `refundpolicy` may remain as one vocabulary item, but it may also split into `refund`, `policy`, or smaller pieces.

The result to check in this case is not `Does it look like a word?`, but `At what boundary is the source split, which vocabulary item is that piece connected to, and what ID sequence does it become?` The numbers are explanatory examples.

| Source | Fast human standard | Tokenization procedure | Result to check |
| --- | --- | --- | --- |
| `환불정책` | It looks like one word | boundary: `환불` / `정책` -> vocabulary pieces: `["환불", "정책"]` -> ID: `[4012, 8830]` | One human word can become two token IDs. |
| `Authorization` | It looks like one English word | boundary: `Author` / `ization` -> vocabulary pieces: `["Author", "ization"]` -> ID: `[6201, 14627]` | A long English expression can become an ID sequence of subpieces. |

So the safer judgment is not guessing token count or IDs immediately from the source, but checking the boundary, vocabulary pieces, and ID sequence made by the tokenizer in order.

### Case 2. When We Think Spaces Mean The Units Are The Same

When people see a sentence such as `The meeting starts tomorrow at 10 AM`, they first think of words separated by spaces. So it is easy to feel that the number of whitespace-separated words will be similar to the token count.

The limit of that standard is that a tokenizer does not split only by spaces. Numbers, endings, particles, and time expressions can make different piece boundaries depending on the vocabulary and splitting rules. `10시에` may remain one bundle, or it may split into `10`, `시`, and `에`.

The result to check in this case is that tokenization is not `whitespace splitting`, but a procedure that resets boundaries for numbers, particles, endings, and other elements outside spaces too.

| Part of source | Fast human standard | Tokenization procedure | Result to check |
| --- | --- | --- | --- |
| `tomorrow morning` | Two words separated by a space | boundary: `tomorrow` / ` morning` -> vocabulary pieces: `["tomorrow", " morning"]` -> ID: `[5920, 7710]` | Whether the space attaches to a piece or separates from it is part of tokenizer output. |
| `10시에` | One time expression | boundary: `10` / `시` / `에` -> vocabulary pieces: `["10", "시", "에"]` -> ID: `[110, 740, 812]` | Numbers and Korean particles can split into separate pieces. |

So the safer judgment is not converting whitespace word count into token count, but looking at the piece boundaries actually made by the tokenizer and the ID sequence corresponding to those boundaries.

### Case 3. When It Feels Like The Sentence Is Computed Directly

When a user enters `Summarize the refund policy`, it is easy to imagine that the model reads the whole sentence and immediately grasps the meaning. But from the tokenization view, the string is first split into pieces, each piece connects to a vocabulary item, and then it changes into a token-ID sequence.

The limit of that standard is that it erases the conversion step between `sentence input` and `computational input`. If tokenization is skipped, we cannot distinguish whether what the model actually receives is the source string, token pieces, or token IDs.

The result to check in this case is that tokenization is not an auxiliary task, but the starting stage that passes a string into actual computational input. This starting stage includes not only `the model received one sentence` but also `it chose pieces and changed them into an ID sequence`.

| Stage | What appears in input | Tokenization procedure | Result to check |
| --- | --- | --- | --- |
| Source string | `Summarize the refund policy` | The tokenizer receives the whole string | It is not computational input yet. |
| Boundary selection | It may look like words and phrases | It makes candidate boundaries such as `Summ`, `arize`, `the`, `refund`, `policy` | Human phrase boundaries can be split again. |
| Vocabulary connection | Piece candidates appear | It matches token pieces such as `["Summ", "arize", " the", " refund", " policy"]` | Computational units are made. |
| ID conversion | A piece list appears | It changes them into an ID sequence such as `[4012, 8830, 812, 6200, 930]` | A number sequence to pass as model input appears. |

## How Far The Procedure Explanation Needs To Go

When first reading tokenization, it is enough to separate `the unit people see` and `the unit the model passes into computation` as follows.

| Input expression | Unit people see first | What to recheck on the model side |
| --- | --- | --- |
| `환불정책` | One word | Does it actually split more finely? |
| `The meeting starts tomorrow at 10 AM` | Words separated by spaces | What pieces do numbers and time expressions become? |
| One full sentence line | One sentence | Does it become a token sequence and token IDs? |

If we stop here, tokenization can become only a procedure to memorize. The more important question in this section is the next one: once the pieces and IDs change that way, which of cost budget, chunk boundary, and output-preservation judgment must be checked again?

When looking at actual tokenizer output or logs, read not only the procedure itself but also the later judgment changes.

| What appears in the log | Question to ask first | Judgment that changes next |
| --- | --- | --- |
| `tokens: ["환불", "정책"]` | Where was the source split? | Can we keep using the word-based sense of length as-is? |
| `ids: [4012, 8830]` | What number did each piece become? | How many computational pieces does the input pass as? |
| The number of `tokens` and `ids` is the same | In what order do pieces and numbers correspond? | How should this count be used later for cost, chunks, and output judgments? |

## What Must Be Distinguished From What?

When understanding tokenization, it is safer to separate the following three levels.

| Level | What happens here |
| --- | --- |
| Source string | Characters and notation read by people |
| Tokenization | Process of splitting the string into computational pieces |
| Model computation | Stage that performs actual computation with token IDs and vectors |

Without this distinction, confusions such as `is a token just a word?` or `does the model read the sentence as-is?` repeat.

The important point here is not memorizing tokenizer-family names. It is reading the flow where the source string is not computed directly, but changes into pieces and IDs in the tokenization stage before moving into model input. This flow must be in place before we can understand why cost, chunks, and output length move together later.

## What Tokenization Results Change

Once we know what tokenization is, we need to see what its result actually changes. The core is simple.

`Tokenization is not simple splitting. It is a process that changes length, cost, chunks, and output interpretation together.`

The value to see before tokenization rules themselves is the observed value that appears after tokenization. Even for the same source, token count can change, the position where context splits can change, and the room left for output can change. So after seeing `how it is split`, we should immediately ask `what judgment must change because of that result?`

## Why The Same Sentence Can Differ

Even with the same meaning, token boundaries and token counts can change when notation changes.

- Use of abbreviations
- Number notation
- Whether special characters are included
- Mixing English and Korean

This is where the reason appears for why sentences that look similar to people can be read as different lengths and costs by the model.

If we unpack very small where the difference appears even with the same meaning, it looks like this.

| Requests that look almost the same to people | Explanatory tokenization observation | Judgment that shifts immediately later |
| --- | --- | --- |
| `Meeting tomorrow at 10 AM` | 6 tokens | Input length and cost |
| `10:00 AM meeting tomorrow` | 8 tokens | Input length and cost |
| `The meeting starts tomorrow at 10 AM. The Zoom link was sent to mail@example.com` | 22 tokens | Cost estimate and output room |

The numbers are not actual tokenizer results, but explanatory values for showing the judgment flow. The key is not comparing sentence meaning, but first seeing `which notation elements can increase computational pieces`. If this step is missing, it is easy to move too quickly into the intuition that `the sentences are similar, so the cost should be similar too`.

## When Token Boundaries Lead To Operation Judgments

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s03-tokenization-impact-en.mmd"
```

There is one result to check in this diagram. When token boundaries change, later service judgments change together.

## What Actually Changes 1. Cost

Even a sentence that looks short can make the actual token count grow quickly when numbers, symbols, emails, or URLs are mixed in. So the intuition that `it is a short inquiry, so the cost should also be small` often fails.

## What Actually Changes 2. Context Length And Chunks

When splitting documents, people first look at paragraph count or rough visual length. But by the tokenization standard, `principle` and `exception`, or `question` and `condition`, can split into different pieces. Then retrieval may bring back only the principle and miss an important exception.

## What Actually Changes 3. Output Length

The longer the response format becomes, the more output tokens are used. When tables, lists, code blocks, and additional explanations increase, the risk that the final key sentence is cut off also grows.

## Scenes Where Operation Judgment Shifts Immediately

Tokenization can look like a preprocessing detail, but it directly shifts operation judgments in practice.

- A sentence that looks short can actually be more expensive.
- A visually clean paragraph split can be bad for retrieval.
- A friendly output format can cut off the final key sentence.

In other words, tokenization differences do not end at `how a string is split`. They lead to operation choices about `what to preserve and what to give up`.

## Operation-Judgment Cases And Examples

The diagram below first groups the three scenes we repeatedly see. The reading flow is `why it looks fine on the surface -> what changes from the tokenization view -> where operation judgment changes`.

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s03-tokenization-operation-cases-en.mmd"
```

The diagram alone can still leave `what failure actually appears` somewhat abstract, so the three cases below read the same scenes more slowly.

The same scenes can be grouped very briefly again as follows.

| Scene | What tokenization changes | Value to recheck first |
| --- | --- | --- |
| Short-sentence cost calculation | Actual token count and cost | Input token count |
| RAG chunk splitting | Whether context is preserved | chunk size, overlap |
| Long answer format | Whether the final key sentence remains | max output tokens |

### Case 1. When A Short Inquiry Changes Cost Judgment

A sentence such as `The meeting is tomorrow at 10:00 AM. The Zoom link was sent to mail@example.com` looks short on the screen. But when numbers, a colon, English text, and an email address are mixed in, the actual token count can grow faster than expected.

The problem scene in this case is the moment we judge that `it is a short schedule notice, so the cost should also be small`. The standard people first use is the number of visible lines and characters. The limit of that standard is that it misses elements a tokenizer may split more finely, such as numbers, special characters, English text, and emails. So the judgment changed by tokenization moves from `is the character count short?` to `how many actual computational pieces are there?`

If we turn it into small observed values, the judgment difference becomes clearer. The numbers are explanatory examples.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| Standard people see first | One short schedule notice sentence | They expect the cost to be small. |
| Limit of that standard | Simple notice 6 tokens, mixed English-symbol notice 22 tokens | Screen line count alone cannot judge input cost. |
| Observation after tokenization | 22 input tokens, 60 expected output tokens | The whole request is read as 82 tokens. |
| Changed operation judgment | 18 tokens remain from a 100-token budget | If room is small, reduce response format or input expression. |

The sentence to close in this case is this: without seeing the tokenization result, the first judgment that `it looks short` can incorrectly pull cost judgment along with it.

### Case 2. When Retrieval Results Change Chunk Judgment

If `annual leave must be requested three days in advance` and `emergency sick leave may be reported afterward` split into different chunks in a policy document, retrieval may bring back only the principle and miss the important exception.

The problem scene in this case is the moment we judge that `retrieval succeeded because the search result brought back the principle document`. The standard people first use is whether the related document appears in the search result. The limit of that standard is that it does not check whether the principle and exception needed for the answer remain in the same token bundle. So the judgment changed by tokenization moves from `is the search result relevant?` to `does the context that must remain together stay in the same chunk?`

The same scene can be read as observed values as follows.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| Standard people see first | Search result brought back the principle document | They judge retrieval successful. |
| Limit of that standard | Principle sentence 42 tokens, exception sentence 18 tokens | At least 60 tokens are needed to contain both together. |
| Observation after tokenization | chunk size 50, overlap 0 | The exception after the principle cannot all stay in the same chunk. |
| Changed operation judgment | Exception conditions can disappear from retrieval context | Reset chunk size and overlap. |

The sentence to close in this case is this: without seeing chunk boundaries after tokenization, the judgment that `retrieval worked` can hide missing exception conditions.

### Case 3. When A Friendly Format Changes Output Preservation Judgment

If an answer that could end as one paragraph explaining a shipping delay keeps adding tables and caution lists, the final refund-condition sentence may be cut off by the output limit. So we must separate `friendly format` from `the core that must remain to the end`.

The problem scene in this case is the moment we judge that `adding tables and lists makes the answer friendlier`. The standard people first use is whether the answer looks clean and sufficiently detailed. The limit of that standard is that table headers, separators, and repeated phrases all use output tokens. So the judgment changed by tokenization moves from `is the format friendlier?` to `does the sentence that must remain fit within the output limit?`

On the output side too, tokenization results appear as observed values.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| Standard people see first | Tables and lists make it friendlier | They judge it is safe to expand the format. |
| Limit of that standard | Table headers and separators use 35 tokens first | Format also consumes output budget. |
| Observation after tokenization | General explanation 32 tokens, must-keep condition 18 tokens, max output tokens 80 | Total need is 85 tokens, so it exceeds the limit. |
| Changed operation judgment | The final condition can be cut off | Move core conditions earlier or reduce the format. |

The sentence to close in this case is this: without seeing where output tokens are used after tokenization, a `friendly format` can push out the final key condition.

Now tokenization results can be read as observed values that change the three judgments of cost, chunks, and output preservation.

## Judgments That Change After Tokenization

To hold onto what tokenization actually changes, it is useful to place `surface change` and `operation-judgment change` side by side.

| Surface change | What actually changes from the tokenization view | Judgment to change immediately |
| --- | --- | --- |
| Numbers and English increase in a short sentence | Actual input token count grows beyond expectation | Should input budget and cost be reset? |
| A regulation sentence is split nicely into two parts | Principle and exception may not remain in the same chunk | Should chunk size or overlap be reset? |
| Tables and lists keep being added to the answer format | Output tokens are used first by format, and the final sentence can be cut | Should we reprioritize what must remain to the end? |

The key application in this section is reading `tokenization difference` not as a preprocessing detail, but as something connected immediately to cost, chunk, and output choices.

Written again so readers can apply the same judgment by hand, it looks like this.

| Observed value now seen | Judgment to drop first | Judgment to hold again |
| --- | --- | --- |
| Token count is higher than expected | Only thinking the tokenizer is strange | Check whether numbers, URLs, code, or mixed notation increased input cost |
| The chunk was split into a clean-looking shape | Thinking natural paragraph shape is sufficient | Check whether principle and exception needed for the answer remain in the same token bundle |
| Output is long and friendly | Thinking more detail is always better | Check whether core conditions remain to the end within max output tokens |

Without this middle application table, tokenization explanation easily stops at `how strings are split`. But the goal of this Section is not memorizing cutting rules. It is changing input budget, chunk boundary, and output-preservation judgments after seeing the cutting result.

## Exercises And Examples

The exercise below is not a problem of guessing token count exactly. First, use an actual tokenizer SDK to check how many tokens the input becomes, and then move that value into cost, chunk, and output-preservation judgments. For each question, first answer for yourself, then compare with the explanation immediately below.

### Example. Checking Input Budget And Output Room With `tiktoken`

This example directly counts input tokens with OpenAI's `tiktoken` library under the same encoding. It is not an example for memorizing the latest context length of a particular model, but for seeing how operation judgment changes when input tokens and expected output tokens are added together. Here we use the `o200k_base` encoding.

The value the actual tokenizer calculates here is `input_tokens`. `expected_output_tokens`, `token_budget`, and `chunk_size` are operation assumptions set by the service designer. This distinction prevents the misunderstanding that `the SDK automatically makes every judgment`. The tokenizer tells us how many pieces the input became, and the person connects that value to output room and chunk room judgments.

The values to manipulate directly are `text`, `expected_output_tokens`, `token_budget`, and `chunk_size` inside `samples`. The values to look at first in the result are `input_tokens`, `remaining_tokens`, and `chunk_margin`.

```python
# Count real input tokens with tiktoken and connect them to cost, chunk, and output-room judgments.
import tiktoken

encoding = tiktoken.get_encoding("o200k_base")

samples = [
    {
        "case": "plain_notice",
        "text": "회의는 내일 열립니다.",
        "expected_output_tokens": 40,
        "token_budget": 120,
        "chunk_size": 80,
    },
    {
        "case": "mixed_schedule",
        "text": "회의는 내일 10:00 AM에 열립니다. Zoom 링크는 mail@example.com으로 보냈어요.",
        "expected_output_tokens": 55,
        "token_budget": 120,
        "chunk_size": 80,
    },
    {
        "case": "policy_with_exception",
        "text": "연차는 3일 전 신청합니다. 단, 긴급 병가는 사후 보고가 가능하며 증빙을 첨부해야 합니다.",
        "expected_output_tokens": 70,
        "token_budget": 120,
        "chunk_size": 30,
    },
    {
        "case": "verbose_output_request",
        "text": "배송 지연 사유를 표로 정리하고, 주의사항 목록과 환불 제한 조건을 마지막에 덧붙여 주세요.",
        "expected_output_tokens": 95,
        "token_budget": 120,
        "chunk_size": 80,
    },
]

for sample in samples:
    input_tokens = len(encoding.encode(sample["text"]))
    total_tokens = input_tokens + sample["expected_output_tokens"]
    remaining_tokens = sample["token_budget"] - total_tokens
    chunk_margin = sample["chunk_size"] - input_tokens
    print(
        sample["case"],
        "input_tokens=", input_tokens,
        "expected_output_tokens=", sample["expected_output_tokens"],
        "total_tokens=", total_tokens,
        "remaining_tokens=", remaining_tokens,
        "chunk_margin=", chunk_margin,
    )
```

The sample result can be read as follows. The output below was checked locally with `tiktoken==0.13.0` inside `.venv`.

```text
plain_notice input_tokens= 7 expected_output_tokens= 40 total_tokens= 47 remaining_tokens= 73 chunk_margin= 73
mixed_schedule input_tokens= 24 expected_output_tokens= 55 total_tokens= 79 remaining_tokens= 41 chunk_margin= 56
policy_with_exception input_tokens= 31 expected_output_tokens= 70 total_tokens= 101 remaining_tokens= 19 chunk_margin= -1
verbose_output_request input_tokens= 30 expected_output_tokens= 95 total_tokens= 125 remaining_tokens= -5 chunk_margin= 50
```

The key to read from this result is not one number but the movement of judgment. Input tokens are actual tokenizer results, while output tokens, budget, and chunk size are conditions readers can change.

| Case | Value visible first | Judgment that changes |
| --- | ---: | --- |
| `plain_notice` | 7 input tokens, 47 total tokens | A short notice has enough input and output room. |
| `mixed_schedule` | 24 input tokens, 79 total tokens | When numbers, English, and an email are attached, input tokens grow even if the text looks short on screen. |
| `policy_with_exception` | 31 input tokens, `chunk_margin` -1 token | If chunk size is 30, this input cannot remain inside one bundle. |
| `verbose_output_request` | 125 total tokens, -5 remaining tokens | A friendly output format can exceed the budget and push out core conditions. |

If we see the number movement as a figure, it becomes visible that `expected output format` can eat into the total budget faster than long input.

![Input tokens and output room viewed through tiktoken observations](/AiBook/assets/part-06/chapter-02/tiktoken-budget-en.png)

The purpose of this example is not memorizing the tokenizer's internal rules. It is to check actual token count and then change human standards such as `does it look short`, `are the paragraphs natural`, and `is the output friendly` into input budget, chunk room, and output-preservation standards.

### Exercise 1. Choosing The Judgment Value For A Short Notice

Observed values:

| Item | Value |
| --- | --- |
| Visible length | 1 paragraph |
| Source features | 1 URL, 2 coupon codes, 1 date range |
| Tokenizer log | General notice 12 tokens, URL/code/date notation 31 tokens |
| Expected output | 50 tokens |

First answer for yourself.

- What value should be rechecked first in this scene?
- Is the screen standard of `short notice` enough?
- If input and expected output are added, how many tokens should the judgment use?
- Does this judgment connect first to cost, chunk, or output?

Explanation: The values to recheck first are input token count and the resulting cost. The input is `12 + 31 = 43 tokens`, and with 50 expected output tokens, the total judgment value is 93 tokens. Even if it is one paragraph on screen, URL, coupon codes, and date notation can quickly increase token pieces. So this scene should first check `how many tokens a short-looking input actually became`, before chunks or output.

### Exercise 2. Finding Why Exceptions Disappear From Search Results

Observed values:

| Item | Value |
| --- | --- |
| Principle sentence | 42 tokens |
| Exception sentence | 18 tokens |
| Current chunk size | 50 tokens |
| overlap | 0 tokens |

First answer for yourself.

- What value should be rechecked first in this scene?
- How many tokens are needed at minimum to keep principle and exception in one chunk?
- Why can the answer be wrong even if the retriever found the principle sentence?
- Does this judgment connect first to cost, chunk, or output?

Explanation: The values to recheck first are chunk size and overlap. Principle 42 tokens and exception 18 tokens require at least 60 tokens together. Current chunk size is 50 and overlap is also 0, so they split easily. Even if the retriever found the principle sentence, the answer can miss an important condition if the exception sentence is not in the same token bundle. So this scene should first check `whether context that must stay together remains in the same chunk`, before cost.

### Exercise 3. Finding Why The Final Conclusion Is Cut Off

Observed values:

| Item | Value |
| --- | --- |
| max output tokens | 80 tokens |
| Table and list format | 35 tokens |
| General explanation | 32 tokens |
| Restriction condition that must remain | 18 tokens |

First answer for yourself.

- What value should be rechecked first in this scene?
- Does the current output composition fit within the limit?
- Why can a friendly format become a failure cause?
- Does this judgment connect first to cost, chunk, or output?

Explanation: The values to recheck first are max output tokens and output format. The current composition is `35 + 32 + 18 = 85 tokens`, so it exceeds the 80-token limit. Tables and lists look friendly, but separators and repeated phrases use output tokens first. So this scene should reduce the output format by the standard `will the core restriction condition remain to the end`, not `will the answer look prettier`.

After the three exercises, you should be able to summarize the point in one sentence.

`Tokenization results are not preprocessing details, but observed values that make us recheck input cost, chunk context, and output preservation.`

## Checklist

- Can you say that sentences with the same meaning can have different token counts when notation changes?
- Can you explain that tokenization shakes cost, chunk design, and output length limits together?
- Do you understand that tokenization changes do not stop at `string splitting` but continue into operation judgment?

## Sources And References

- OpenAI Help Center, [What are tokens and how to count them?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm that input and output token counts connect to usage, cost, and request-length judgment.
- OpenAI Help Center, [Controlling the length of OpenAI model responses](https://help.openai.com/en/articles/5072518-controlling-the-length-of-openai-model-responses){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm that response length is controlled with output-token limits such as `max_output_tokens` or `max_completion_tokens`.
- OpenAI, [tiktoken README](https://github.com/openai/tiktoken/blob/main/README.md){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used as background support that tokenizer encoding results become observed values for service judgment even for the same text.
- Rico Sennrich, Barry Haddow, Alexandra Birch, [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/){: target="_blank" rel="noopener noreferrer" }, ACL 2016, accessed 2026-07-19. Used as background support that subword units are used for rare-word and out-of-vocabulary handling.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as general NLP background for tokenization and word-boundary explanation in the `Words and Tokens` chapter.
