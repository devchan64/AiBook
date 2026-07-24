# P6-2.1 Token Units That Limit Inputs And Outputs

> Section ID: `P6-2.1`
> Version: `v2026.07.23`

Once we start using an LLM (large language model) in practice, another question appears immediately. Why are some inputs more expensive than expected, why are long documents cut off in the middle, and why can the sense of length change depending on how the same one-line sentence is written?

The model handles input by token count, not by character count or sentence count.

In other words, the token does not first enter as a `definition`. It enters as the computational unit needed to explain length limits, cost, truncation, and input splitting.

At this point, it is important not to immediately define a token as `one word` or `one meaning`. A token is not a word a person looks up in a dictionary, and it is not a marker that contains the meaning of a sentence all at once. At this stage, it is safer to hold it only as `a computational piece the model uses to count inputs and outputs`. Exactly how text is split returns in P6-2.2 and P6-2.3.

## Why Character Count Or Sentence Count Is Not Enough

People usually read input in ways like these.

- Is the sentence short?
- How many files are there?
- How many paragraphs are there?
- How long does it look on the screen?

But models do not use these units directly for computation. So inputs that look similar by human standards can be read by the model as very different lengths and different costs.

For example:

| Human-standard question | Question to ask again in practice |
| --- | --- |
| Is the sentence short? | Is the actual input token count small? |
| Is it one file? | Does the full input fit within the token limit? |
| Does the paragraph look clean? | Does the needed context remain in the same piece? |

The key here is that `the unit people count first` and `the unit the model actually computes with` can differ.

So the first judgment in this section is closer to `What length of computational pieces does the model see in this input?` than to `What does this token mean?` Meaning interpretation returns later through embeddings and Transformers. Here, first hold onto the fact that before input enters model computation, it can already diverge from a person's sense of length.

## Problems That Appear First From A Token View

Problems that require a token view usually appear first in the following scenes.

### 1. Input Length Limits

When a long document is provided, people can easily think, `It is one file, so the model will read it at once.` But the model reads by total input length in computational units, not by number of files, so the conclusion or exception clauses near the end can be cut off.

### 2. Cost

Even a sentence that looks short can make the actual input cost grow faster when numbers, symbols, English notation, or URLs are mixed in. So the intuition that `it is a short notice, so it should be cheap` often fails.

### 3. Context Preservation

When cutting chunks for RAG or search, people first look at paragraph counts, but what matters in practice is whether the question and condition, or principle and exception, remain in the same input bundle. This problem also connects to what we treat as the computational unit.

The same scenes can be grouped again as practical judgments.

| Situation | What people count first | What the model side sees first | Judgment that changes immediately |
| --- | --- | --- | --- |
| Short one-line question | Sentence count, character count | Actual token count | Expected cost and input length |
| One long document file | File count, page count | Total token length | Whether whole input is possible |
| Paragraph splitting for search | Paragraph count, visually clean length | Context preservation inside the same piece | Chunk design and retrieval quality |

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s01-token-question-split-en.mmd"
```

What this diagram asks us to check is that different tasks still hit similar problems first. A short sentence, a long document, and a cost calculation are different scenes, but they all eventually require us to look again at `what the model actually reads as how many computational pieces`.

## Cases And Examples

### Case 1. When The Cost Sense Of A Short-Looking Sentence Shifts

`The weather is nice today` and `The meeting is tomorrow at 10:00 AM. Please refer to https://example.com/report for the materials` can both look like short one-line inputs. People usually judge first by sentence count or screen length.

But when numbers, time notation, English text, URLs, and symbols are mixed in, the input pieces counted by the model can grow differently from a person's one-line sense. If cost is predicted only by character count or sentence count, the result is the familiar problem: `Why did this short request cost more than expected?`

The result to check is not `Does it look short?` but `How many input and output units does the model actually count?` That is why a common computational unit called the token is needed to explain cost.

| Input scene | First impression by human standard | What to recheck from the token view |
| --- | --- | --- |
| `The weather is nice today` | A short one-line sentence | Baseline number of input pieces |
| `The meeting is tomorrow at 10:00 AM` | A short schedule notice | How numbers and English notation are counted |
| Notice with a URL | Still one sentence | How much symbols and long strings increase input length |

### Case 2. When One File Is Not Read To The End

If we provide a 30-page meeting note as a whole, people can easily think, `It is one file, so it will be read at once.` But the model meets its limit based on how many tokens the whole input contains, not on the number of files.

If there are many tables, number lists, appendices, or code fragments, the input length can grow faster than the page count feels to a person. When the limit is exceeded, the conclusion or exception clauses near the end may be cut off, or the request must be split from the beginning.

The result to check is not `How many files are there?` but `Is there enough token budget to keep everything to the end?` That is why input limits also require a token standard.

| Document scene | First judgment by human standard | Judgment that changes from the token view |
| --- | --- | --- |
| One 30-page meeting-note file | One file, so it seems readable at once | Does the full input fit within the limit? |
| Report with many tables and appendices | Page count looks similar | Do notation elements increase tokens faster? |
| Document with the conclusion at the end | Since it was included, the conclusion seems read | Was the key conclusion near the end cut off? |

### Case 3. When Search Answers Shift Despite Clean Paragraphs

When cutting documents for RAG, people can easily feel that `two paragraphs are appropriate`. But if the principle paragraph and exception paragraph are split into different input bundles, retrieval may bring back only the principle and miss the important exception.

In this scene, what matters more than whether the paragraph shape looks natural is whether the condition, principle, and exception needed for the question remain inside the same input unit. If we bundle too much, the limit and cost grow. If we cut too short, the needed context scatters.

The result to check is not `Are the paragraphs neat?` but `Does the needed context remain inside the same token bundle?` That is why context preservation also needs the token view.

| Search scene | First judgment by human standard | Judgment that changes from the token view |
| --- | --- | --- |
| Two regulation paragraphs | Paragraph units look clean | Do principle and exception remain in the same bundle? |
| Long FAQ item | It is one item, so we want to keep it together | Does it avoid exceeding the limit and cost? |
| Short chunks | More retrieval candidates look helpful | Are the conditions needed for the answer scattered? |

Even after all three cases, reading tokens as `meaning units` makes things confusing again. In the cost problem, the sense of length can differ because of notation even when the meaning is similar. In the long-document problem, even one file can hit the computational limit. In the search problem, a clean-looking paragraph may fail to preserve the conditions needed for the answer. The token sense needed here is closer to `pieces and length that enter computation` than to `names that carry meaning`.

## Turning Human Standards Into Model Standards

Even if we cannot yet count the actual number of tokens, we can practice changing `human-standard units` into `model-standard units` like this.

| Input being viewed | What people are likely to say first | What to ask first from the token view |
| --- | --- | --- |
| One-line notice with numbers and a URL | It is short, so the cost should be small | How many actual input and output tokens are there? |
| One meeting-note file | It is one file, so it should be read whole | Does the whole input fit inside the context window? |
| Two regulation paragraphs | The paragraph shape is natural, so search should be fine | Do principle and exception remain in the same token bundle? |

The important point in this table is not getting the correct number. It is changing `what to count first`.

The same standard can be practiced more briefly as follows.

| Problem that appears now | Token view to recall first |
| --- | --- |
| The answer costs more than expected | Look at actual token count before visible length |
| The end of a long document is missing | Look at total token length before file count |
| Search answer misses an exception | Look at context preservation inside the same token bundle before paragraph shape |

At this stage, it is enough if you can say these three lines immediately. Even if you cannot count exact tokens yet, you have begun to distinguish that `cost problems`, `truncation problems`, and `context preservation problems` cannot all be explained by human-standard length alone.

The three cases can be compressed again like this.

| Standard easy to grab first | Why it is insufficient | Standard needed instead |
| --- | --- | --- |
| One line, character count | Numbers, symbols, and URLs can change actual computational length and cost | Input and output token count |
| File count, page count | The limit applies to length the model can receive, not number of files | Total token length and context window |
| Paragraph shape | If needed conditions split into different bundles, the answer can shift | Context preservation inside the same token bundle |
| Word count, number of meanings | A token is not always the same as one word or one meaning | Computational pieces the model actually counts |

The purpose of this table is not to make readers memorize exact token counts. It is to help them hold onto why the units people first see are difficult to use as-is when handling LLMs, and why a separate model-standard computational unit is needed.

If we regroup the three cases, the standard becomes one. Units people first hold onto, such as one line, file count, page count, paragraph shape, and word count, are not stable enough to explain input cost, context windows, search chunks, or output length. So when handling an LLM, we must ask first not `How long does this look to a person?` but `How many computational pieces does the model actually read and write?`

## So Tokens Appear

The concept needed at this point is the token. A token is the computational unit the model counts when handling input and output.

The three earlier cases are actually saying one thing.

- To predict cost, we must look at the actual number of input and output tokens rather than the visible length.
- To handle long documents, we must look at total token length and the context window rather than file count.
- To split input for search, we must look at whether the needed context remains in the same token bundle rather than paragraph shape.

In other words, the token does not appear just so we can learn one more term. It appears as the model-standard computational unit because the human sense of sentence, word, and character counts is not enough to explain LLM inputs and outputs reliably.

What a token itself is, how it differs from a word, and how it is computed inside the model continue in P6-2.2. Here, when you see scenes such as `the answer costs more than expected`, `the end of a long document is missing`, or `the search answer misses an exception`, first let go of the human-standard sense of length. Then ask one question: by the computational pieces counted by the model, how long are this input and output, and how much remains in the same context?

## Exercises And Examples

Read the three input scenes below and choose the token view to check first. At first, it is useful to cover the `example answer` column and choose directly.

| Input scene | Problem to judge first | Example answer |
| --- | --- | --- |
| A one-line notice contains many times, prices, and URLs | Choose whether it is a cost problem, truncation problem, or context preservation problem | Cost problem: even if it looks short, the actual input and output token counts can grow. |
| A long meeting note was provided, but the answer misses the conclusion near the end | Choose whether it is a cost problem, truncation problem, or context preservation problem | Truncation problem: even one file can exceed the total token-length limit. |
| In regulation search, the principle is correct but the exception is missed | Choose whether it is a cost problem, truncation problem, or context preservation problem | Context preservation problem: principle and exception may have been split into different token bundles. |
| A sentence with the same meaning was rewritten shorter, but the cost sense may not stay the same | Judge whether word count and token count can be treated as the same | Word count is not enough. The actual token count must be checked again based on computational pieces made by the tokenizer. |

The goal of this exercise is not to count exact tokens. It is to build the habit of first asking `What problem appears in the model's counted computational units?` rather than `Does it look short to a person?`, `How many files are there?`, or `Do the paragraphs look clean?`

## Checklist

- Can you explain why character count or sentence count alone is not enough to explain LLM input problems?
- Do you understand that length limits, cost, and context preservation all require a different computational unit?
- Can you explain the token first as a computational piece counted by the model, without defining it as one word or one meaning?
- Can you explain that the token first appears as `a computational unit for solving problems`?

## Sources And References

- OpenAI Help Center, [What are tokens and how to count them?](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm that tokens are pieces of text processed by models and that input and output token counts connect to usage and limit judgments.
- OpenAI, [tiktoken README](https://github.com/openai/tiktoken/blob/main/README.md){: target="_blank" rel="noopener noreferrer" }, accessed 2026-07-19. Used to confirm the flow of OpenAI-model BPE tokenizers and converting text into token-number sequences.
- Daniel Jurafsky, James H. Martin, [Speech and Language Processing, 3rd ed. draft](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }, online manuscript released January 6, 2026, accessed 2026-07-19. Used as general NLP background for the explanation of token and word boundaries in the `Words and Tokens` chapter.
