# P6-2.5 Supplement: Tokenizer Family Differences Revealed by Operational Observations

> Section ID: `P6-2.5`
> Version: `v2026.07.24`

BPE, WordPiece, and SentencePiece are not a list of names to memorize. Even the same string can have different piece boundaries, token counts, whitespace handling, and rare-expression handling depending on which tokenizer is used. This difference leads directly to cost prediction, retrieval chunks, long-document input, and the sense of length in mixed-notation documents.

The center of this supplement is not memorizing every detail of the three algorithm families. It is reading each family name as `a standard for cutting strings`, then seeing when that standard difference appears in cost, chunks, and mixed-notation length prediction.

## Family Names Point to Cutting Standards

If tokenization changes cost and chunks, the next question is `why the sense of how a string is cut differs slightly by model`. The names you most often meet when reading this difference are `BPE`, `WordPiece`, and `SentencePiece`.

Rather than memorizing the three names, first hold onto where `the standard used to split a string into pieces` diverges. That lets you read differences in length sense, rare-word handling, and whitespace interpretation on the same axis.

## What Does Tokenizer Family Mean?

A tokenizer is a bundle of rules that turns text into units for model computation. Usually, two things come together here.

- A piece vocabulary that decides which pieces are used often
- Segmentation rules that decide how to divide the source string into those pieces

`BPE`, `WordPiece`, and `SentencePiece` are representative family names for building this kind of tokenizer.

## Standards Where Token Boundaries Diverge

Even the same sentence can differ in:

- which expression is treated as one piece
- how strongly whitespace is trusted
- how many pieces a rare word is split into

When these standards differ, token count, length sense, and chunk boundaries also change together. That is why model cards or lectures often state separately `which tokenizer family this model uses`.

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s05-tokenizer-family-map-en.mmd"
```

This diagram briefly shows only that tokenizer names connect to differences in token boundaries, length sense, and whitespace interpretation.

## What the Three Have in Common

What BPE, WordPiece, and SentencePiece have in common is that all are families that try to turn text into subword pieces that are good for computation. Their differences appear in cutting standards such as `what to try combining more often`, `which piece vocabulary explains the string better`, and `whether whitespace can be fixed as a boundary`.

So when you see the three names, it is better to read them not as `technologies with completely different purposes`, but as different standards for making and choosing pieces while pursuing the same goal.

## Cutting Standards by Family

### BPE(Byte Pair Encoding)

BPE is best read as starting from very small pieces, then repeatedly merging pairs of pieces that often appear together into larger pieces.

At first, it starts from smaller units such as characters or bytes. Then, as combinations that frequently appear together in a training corpus are repeatedly merged, larger pieces such as `th`, `ing`, and `token` are made. Here, a corpus is a bundle of text collected for training or analysis. So when first reading BPE, it is closer to `frequent co-occurring pieces gradually solidify` than `the tokenizer knows words from the beginning`.

When reading it for the first time, hold onto this:

- It starts from smaller pieces.
- It merges pieces that often appear together to make larger pieces.
- It lets rare words be read as several pieces rather than not read at all.

For example, if the string `tokenization` appears often, the tokenizer may first read it in smaller pieces, then gradually solidify commonly used pieces such as `token` and `ization` into larger units. What matters here is not `memorizing dictionary words first`, but `gradually growing pieces that repeat often`.

### WordPiece

WordPiece can be read as a family that more strongly asks `which piece vocabulary can explain sentences more efficiently`. Like BPE, it uses subword pieces, but it is useful to read it as paying more attention to `how well this piece vocabulary explains the whole sentence` than to simply merging pairs that often stick together.

When comparing it for the first time, the following distinctions are especially important.

- BPE also grows pieces, but WordPiece more directly treats `which pieces should be put in the vocabulary` as the problem.
- Even if a full word is not in the vocabulary, it reads it by splitting it into smaller subword pieces.
- It often appears together with expressions such as `subword`, `longest match`, and `[UNK]` in explanations of BERT-family models.

For example, even if an expression such as `unhappiness` is not in the vocabulary as a whole, it can be read by splitting it into existing pieces such as `un`, `happi`, and `ness`. The core to hold here is not `does the model immediately discard unknown words`, but `does it try to explain them as much as possible with pieces it already knows`.

The `longest match` sense often seen with WordPiece can also be understood here. It means reading the string from the left and, if there is a longer piece currently in the vocabulary, preferring to use that piece. So it is better to receive the sentence `BERT uses WordPiece` not as a mere proper noun, but as an explanation that `BERT has rules for cutting words into smaller meaning pieces`.

### SentencePiece

SentencePiece is best read as handling the string itself more directly, including whitespace, without assuming that whitespace is already a perfect word boundary. That is why it is often described as relatively consistent not only for languages where spaces are familiar, such as English, but also in environments where whitespace-based boundaries are less stable or languages are mixed.

When first seeing SentencePiece, look at these points first.

- It does not trust whitespace as an absolute standard just because whitespace exists.
- It makes pieces from the whole string.
- It is closer to directly handling the problem that the sense of word boundaries differs by language.

For example, when handling a sentence that mixes Korean, English, numbers, and symbols, people first see spaces with their eyes. But in SentencePiece-family explanations, `whitespace is also treated as part of the string, and which pieces repeatedly become useful` is decided again. So the line `this model uses SentencePiece` is also a clue that `this model may not use whitespace as an absolute standard`.

## A Very Simple Comparison of the Three

| Name | One-line explanation | First question to recall |
| --- | --- | --- |
| BPE | Gradually merges small pieces that often stick together into larger pieces | What repeatedly appears together |
| WordPiece | Pays more attention to which piece vocabulary explains the sentence better | Which pieces are better to put in the vocabulary |
| SentencePiece | Handles the whole string, including whitespace, more directly | How much to trust whitespace as a word boundary |

This table does not mean you should memorize all strict algorithmic differences. What you should first hold onto is that `all three names are subword families, but each pays attention to a slightly different standard`.

## Misunderstandings When Reading Tokenizer Families

### 1. Thinking the Three Have Completely Different Purposes

The three names are not separate devices with completely different purposes. All are `families that try to stably turn strings, including rare words, into computable pieces`. The difference is less in purpose and more in `the sense used to make and choose pieces`.

### 2. Thinking Unknown Words Cannot Be Read Immediately

One reason these families matter is that even when a word is unknown as a whole, they let it be read again by splitting it into smaller pieces. The feeling that `if a word is not in the vocabulary, is that the end?` connects directly to why subword families appeared.

### 3. Thinking Name Memorization Is the Core

The important thing is not memorizing names. You should be able to ask `what unit does this model use to read strings`, `how much does it trust whitespace`, and `how does it split rare expressions`.

## Why This Distinction Is Used in Actual Judgment

Representative tokenizer families are needed not to memorize detailed comparisons, but to interpret how an LLM reads strings. If you do not know these names, the questions below do not connect to each other.

- Why can sentences with the same meaning have different token counts across models?
- Why are some models cut differently from the whitespace-based word sense?
- Why does the sense of length often miss for rare words, mixed notation, and long terms?

In other words, what is needed here is not memorizing three proper nouns, but having a standard for reading `by what standard the model cuts strings`.

After learning this distinction, you should be able to check yourself with the standards below.

| What you should be able to do after learning the names | What you do not need to do yet |
| --- | --- |
| Say what BPE, WordPiece, and SentencePiece are names of | Implement merge rules directly |
| Understand that all three families are subword families | Trace paper formulas and training details |
| Explain differences in whitespace, rare words, and piece vocabulary perspectives | Train a new tokenizer yourself |

## Cases and Examples of Cutting Standards by Family

### Case 1. Reading BPE by Repeating-Piece Standards

In a corpus where the expression `tokenization` appears often, you do not have to assume the tokenizer knows the whole word from the beginning. It can start from smaller pieces, then pieces that often appear together, such as `token` and `ization`, can gradually solidify.

The standard people often use first in this case is seeing `tokenization` as one English word. The limit of that standard is that the tokenizer does not simply follow a word dictionary. When you see the name BPE, you should first ask `from which repeated pieces did this string grow`.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| First human standard | `tokenization` is one word | Expects it to be handled whole as one word |
| Limit of that standard | Frequently attached pieces can solidify separately | You see piece boundaries such as `token` and `ization` |
| Question changed by the family name | BPE has the sense of repeatedly growing small piece pairs | First asks `what repeatedly appears together` |

So the sentence to close the BPE case is this. BPE is not a name to memorize, but a cutting standard where small pieces that repeatedly attach become larger computation pieces.

### Case 2. Reading WordPiece by Vocabulary-Piece Standards

Even an expression that is unfamiliar as a whole, such as `unhappiness`, can be explained with subword pieces such as `un`, `happi`, and `ness`. This is also why `WordPiece`, `subword`, `longest match`, and `[UNK]` appear together in explanations of BERT-family models.

The standard people often use first in this case is the judgment that `if the word is not in the vocabulary, the model cannot read it`. The limit of that standard is missing that subword families try to explain strings not with whole words, but with an existing piece vocabulary. When you see the name WordPiece, you should first ask `which pieces should be put in the vocabulary to explain the whole string better`.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| First human standard | `unhappiness` is unfamiliar as a whole | Expects it to be treated as an unknown word |
| Limit of that standard | It can be explained with pieces such as `un`, `happi`, and `ness` | The composition of the piece vocabulary matters more than the whole word |
| Question changed by the family name | WordPiece has the sense of explaining strings with vocabulary pieces | First asks `which pieces are better to put in the vocabulary` |

So the sentence to close the WordPiece case is this. WordPiece does not mean giving up immediately on unknown words. It is a cutting standard that tries to explain strings as much as possible with existing subword pieces.

### Case 3. Reading SentencePiece by Whitespace-Boundary Standards

In inputs that mix Korean sentences, English product names, numbers, and symbols, it is difficult to decide word boundaries using whitespace alone. A SentencePiece family can be understood as finding repeated pieces in the whole string, including whitespace markers, rather than trusting whitespace as an absolute boundary.

The standard people often use first in this case is the judgment that whitespace is a word boundary. The limit of that standard is that when Korean, English product names, numbers, and symbols are mixed, whitespace alone cannot reliably decide computation pieces. When you see the name SentencePiece, you should first ask `whether whitespace can be trusted as an absolute boundary`.

| Case step | Value in this scene | Result to check |
| --- | --- | --- |
| First human standard | If there is whitespace, a word boundary is visible | Expects whitespace-based splitting to be enough |
| Limit of that standard | Korean, English, numbers, and symbols are mixed | Whitespace alone cannot reliably decide piece boundaries |
| Question changed by the family name | SentencePiece sees the whole string, including whitespace | First asks `whether whitespace can be fixed as a word boundary` |

So the sentence to close the SentencePiece case is this. SentencePiece is not simply a name often seen in multilingual models. It is a cutting standard that makes us ask again how much to trust whitespace boundaries.

## Tokenization Standards That Diverge in Input Scenes

A point where readers often get stuck again after reading the three names is `so which question should I ask first now`. In that case, it is safer to first choose what problem stands out in the current input, rather than the name itself.

| Scene that first stands out now | First question to ask | More directly connected family |
| --- | --- | --- |
| The same pieces seem to repeatedly appear together often | `Are small pieces that often appear together solidifying into larger pieces?` | BPE |
| A word missing as a whole must be explained as much as possible with existing subword pieces | `Which pieces should be put in the vocabulary to help explain the whole string?` | WordPiece |
| Whitespace, language mixing, numbers, and symbols make it hard to trust whitespace boundaries as-is | `Do we need to look again at the whole string without treating whitespace as an absolute boundary?` | SentencePiece |

The purpose of this table is not to mechanically match the three families. It is to let you quickly choose `whether you first need to check repeated pieces, vocabulary piece selection, or whitespace-boundary handling` when reading a model card or tokenizer explanation.

## What Changes in Tokenizer Family Comparison

Representative tokenizers do not leave much intuition if you only read about them. You need to use them directly to immediately see how `words as humans see them` and `pieces as the model reads them` diverge.

When you use them directly, three things especially stand out.

- Even sentences with the same meaning can have different piece counts if the expression changes a little.
- Whitespace, symbols, numbers, and English mixing can strongly shake the sense of length.
- Even the same string can have different piece boundaries depending on the tokenizer family.

This experience matters because representative family names stop being abstract proper nouns and become an actual sense of piece boundaries. If readers never use them even once, they are likely to read the sentence `the tokenizer family differs` and still return to their sense of words and character counts.

## Differences Visible in a Small Comparison

Before going deeply into representative tokenizers, even a very small comparison like the one below shows piece-boundary differences.

1. Prepare two or three sentences with the same meaning.
2. Make one version that mixes numbers, symbols, English, and abbreviations.
3. See how many pieces each sentence is divided into.
4. Check where the piece boundaries changed.

For example, you can directly compare sentences like these.

| String to compare | First point to observe |
| --- | --- |
| `회의는 내일 열립니다.` | A simple sentence that becomes the comparison baseline |
| `회의는 내일 10:00 AM에 열립니다.` | How much the piece count increases when numbers and English are added |
| `회의는 내일 10:00 AM, Zoom 링크 포함입니다.` | How symbols and English mixing further shake boundaries |

The purpose of this small practice is not choosing `which family is best`. What you need first is to confirm with your own hands that `sentences that look similar to human eyes can be cut differently on the model side`.

## Optional Execution Example: Put the Same Input into Three Families

Representative tokenizers should not end at knowing their names. When an execution environment is ready, it is better to use each one directly at least once. However, this example is not a basic execution example that always closes with package installation alone. Even if `transformers` and `sentencepiece` are installed, the first execution environment may need to download tokenizer files from Hugging Face. If the internet is blocked or the files are not in the local cache, the process can stop at `AutoTokenizer.from_pretrained(...)`.

So this section separates two layers. The code below is an optional execution example for directly checking actual tokenizer output. In an environment where you cannot run it immediately, first read the saved observation CSV [p6-2-5-tokenizer-family-observations.csv](/AiBook/assets/part-06/chapter-02/p6-2-5-tokenizer-family-observations.csv){ .csv-preview } and the result tables that follow. One row in the CSV means `the token count and representative pieces when one input is passed into a specific tokenizer`.

The example has three goals.

- Use BPE, WordPiece, and SentencePiece once each on real input.
- Confirm that even the same string can have different piece boundaries and token counts by family.
- Directly see how numbers, English, symbols, and mixed notation shake the sense of length.

Example models can be set as follows.

| Family | Example model | What to see in this example |
| --- | --- | --- |
| BPE | `gpt2` | How pieces that often appear together are grouped |
| WordPiece | `bert-base-uncased` | How subword pieces and the longest-match sense appear |
| SentencePiece | `google/mt5-small` | How the sense of not treating whitespace as an absolute standard appears |

The value to manipulate directly is the `samples` list. Add Korean, English, numbers, URLs, and code fragments, then see where `TOKEN COUNT` and `TOKENS` differ. Fix the observation order.

| Observation order | Value to check | Interpretation standard |
| --- | --- | --- |
| 1 | `TOKEN COUNT` | Whether the sense of length differs by family even for inputs with the same meaning |
| 2 | `TOKENS` | Whether the word boundaries people see diverge from tokenizer piece boundaries |
| 3 | `TOKEN IDS` | Whether piece strings were changed into vocabulary number sequences |

```python
# Example comparing how BPE, WordPiece, and SentencePiece tokenizers split the same input strings into token pieces and IDs.
from transformers import AutoTokenizer

# Manipulation variable: adding sentences here or changing expressions changes token pieces and token counts.
samples = [
    "회의는 내일 열립니다.",
    "회의는 내일 10:00 AM에 열립니다.",
    "회의는 내일 10:00 AM, Zoom 링크 포함입니다.",
    "tokenization",
    "tokenization helps models read rare words",
]

tokenizers = {
    "BPE / gpt2": AutoTokenizer.from_pretrained("gpt2"),
    "WordPiece / bert-base-uncased": AutoTokenizer.from_pretrained("bert-base-uncased"),
    "SentencePiece / google/mt5-small": AutoTokenizer.from_pretrained("google/mt5-small"),
}

for name, tokenizer in tokenizers.items():
    print(f"\n=== {name} ===")
    for text in samples:
        pieces = tokenizer.tokenize(text)
        ids = tokenizer.convert_tokens_to_ids(pieces)
        print(f"\nTEXT: {text}")
        print("TOKENS:", pieces)
        print("TOKEN COUNT:", len(pieces))
        print("TOKEN IDS:", ids)
```

The code above is an explanatory example that directly checks representative tokenizer use. At the same time, because token pieces and token counts change when the `samples` list changes, it can also be expanded into a small experiment. You do not need to memorize exact token strings. Instead, you should read `which input changes greatly affect token count`, `which family splits boundaries more finely`, and `which pieces whitespace and symbols remain as` together with questions and explanations.

If execution fails, first separate the cause of failure. If the `transformers` import fails, it is a package dependency problem. If it stops at `from_pretrained()`, it is a tokenizer file download or local-cache problem. This distinction is necessary so you do not misunderstand the core of the example as an installation problem. What you learn here is not the download procedure, but how different families split the same input differently.

| Observation question | Explanation |
| --- | --- |
| Which family splits the same sentence more finely? | Because each family has a different piece vocabulary and segmentation rules, even the same string can have different token counts. The central concept to confirm here is that `models differ in the standards they use to cut strings`. |
| How much does token count change when numbers, `:`, `,`, and English abbreviations appear? | Mixed notation can increase the piece count seen by the tokenizer faster than the character count seen by people. This question confirms that BPE, WordPiece, and SentencePiece all solve the same problem but do not make the same boundaries. |
| Can something that looks like one English word actually be split into several subword pieces? | Even familiar words such as `tokenization` can be split into pieces like `token` and `ization`. This explanation connects to the fact that representative families read by subword pieces rather than whole words. |
| How easily does the whitespace-based word sense break when Korean and English are mixed? | Whitespace is a convenient marker for people, but not every tokenizer uses whitespace as an absolute word boundary. This question makes you read SentencePiece by the standard of `string processing that includes whitespace`. |

It is especially worth trying the following two comparisons.

| Input to compare | What to check directly |
| --- | --- |
| `회의는 내일 열립니다.` vs `회의는 내일 10:00 AM에 열립니다.` | How much the piece count increases when numbers and English are added |
| `tokenization` vs `tokenization helps models read rare words` | How piece boundaries differ between one word and the whole sentence |

## Difference Between Output Pieces and Token Counts

If you run the example code above, you can observe differences in the following form. The numbers below are examples organized by the same standard as the saved observation CSV. Because detailed pieces can differ by library and tokenizer file version, read `how to read family differences` in the table below rather than `one exact fixed answer`.

| Input | BPE `gpt2` | WordPiece `bert-base-uncased` | SentencePiece `google/mt5-small` |
| --- | --- | --- | --- |
| `회의는 내일 열립니다.` | 24 | 17 | 8 |
| `회의는 내일 10:00 AM에 열립니다.` | 31 | 23 | 11 |
| `회의는 내일 10:00 AM, Zoom 링크 포함입니다.` | 39 | 30 | 16 |
| `tokenization` | 2 | 2 | 3 |
| `tokenization helps models read rare words` | 7 | 7 | 9 |

Even looking at the numbers first immediately reveals several things.

- The `gpt2` BPE split the same Korean sentence very finely.
- The `bert-base-uncased` WordPiece also split Korean finely, but in some cases handled the front part of the sentence as `[UNK]`.
- The `mt5-small` SentencePiece kept larger pieces such as `회의`, `▁내`, `▁열`, and `립니다`.
- Even though `tokenization` looks like one word, all three families did not leave it only as one single piece.
- After numbers and English were mixed in, token counts increased for all three families, but the amount of increase differed.

The difference becomes clearer if we look only at representative pieces.

| Family | Representative pieces actually seen | Meaning to read here |
| --- | --- | --- |
| BPE `gpt2` | `['Ġ10', ':', '00', 'ĠAM']`, Korean segmented into many broken byte-like pieces | Byte-based BPE can read Korean very finely |
| WordPiece `bert-base-uncased` | `['[UNK]', 'ᄂ', '##ᅢ', ...]`, `['token', '##ization']` | English-centered WordPiece leaves some Korean as `[UNK]` and connects known pieces as subwords |
| SentencePiece `google/mt5-small` | `['▁', '회의', '는', '▁내', '일', '▁열', '립니다', '.']` | It can read while keeping larger pieces based on a string that includes whitespace |

Differences also appeared in the English sentence. `tokenization helps models read rare words` was:

- BPE `gpt2`: `token`, `ization`, `Ġhelps`, `Ġmodels`, `Ġread`, `Ġrare`, `Ġwords`
- WordPiece `bert-base-uncased`: `token`, `##ization`, `helps`, `models`, `read`, `rare`, `words`
- SentencePiece `google/mt5-small`: `▁`, `token`, `ization`, `▁help`, `s`, `▁models`, `▁read`, `▁rare`, `▁words`

In other words, even in a scene where you look at one English word, how to split `tokenization`, how to mark whitespace, and whether to leave `helps` whole or split it into `help` and `s` actually differed.

The judgment readers should close from this result is this. When you see the names `BPE`, `WordPiece`, and `SentencePiece` in a model card or tokenizer explanation, memorize less of the names themselves and check which cutting standard to recall among `repeating pieces`, `vocabulary pieces`, and `string including whitespace`.

The core of this example is to build `the habit of reading family names as actual piece boundaries`. When seeing when tokenization-type differences appear, you should first recall this standard difference.

If you have read family names as actual piece boundaries, you should be able to connect the same observations again to cost, chunks, and length-prediction problems.

## Moments When Differences Appear in Operations

Knowing tokenizer family names is not immediately enough. What matters in practice is `when the difference starts to appear`.

The core of this section is not asking first `which family is better`. What you should see first is the scene where the difference appears.

## When the Sense of Cost Diverges Despite the Same Meaning

People see `환불 정책을 알려줘` and `환불 관련 정책을 간단히 설명해 줘` as similar questions. But if expressions such as `관련`, `간단히`, and `설명해` are split more finely depending on the tokenizer, the actual token count and cost can differ.

In other words, the same meaning does not guarantee the same input cost.

The actual tokenizer results above also confirm this sense.

| Input | BPE `gpt2` | WordPiece `bert-base-uncased` | SentencePiece `google/mt5-small` |
| --- | --- | --- | --- |
| `회의는 내일 열립니다.` | 24 | 17 | 8 |
| `회의는 내일 10:00 AM에 열립니다.` | 31 | 23 | 11 |

Even in the same schedule-notification scene, the moment numbers and English were attached, token counts increased for all three families, and the amount of increase was not the same. This difference is the actual form of the statement that `the sense of cost can differ despite the same meaning`.

## When Retrieval Chunks Are Cut Awkwardly

Dividing paragraphs in a visually pleasing way does not necessarily make chunks good for retrieval. If key conditions and exception clauses are torn into different pieces, the retrieval result can bring only the principle and miss the exception.

In this scene, `token piece boundaries` can become more important than `whitespace-based paragraphs`.

The actual piece examples make the reason clearer.

- BPE `gpt2` tends to split Korean very finely, so phrases people see as one group can scatter into more pieces.
- WordPiece `bert-base-uncased` handles part of Korean as `[UNK]` and connects the rest as subwords, so language-mixed sections can be read differently from the boundaries people expect.
- SentencePiece `google/mt5-small` kept larger pieces such as `회의`, `▁내`, `▁열`, and `립니다`, showing that the same sentence can leave relatively larger meaning units.

The core here is not that `one family is always better`. When cutting chunks, how much `the meaning unit people thought of` and `the actual token piece unit` diverge can shake retrieval quality.

## When Length Sense Shakes in Mixed-Notation Documents

When English product names, version strings, URLs, and code fragments enter Korean explanatory sentences, actual token count can grow faster than the sentence looks to human eyes.

In this scene, `mixed-notation density` becomes a more important judgment standard than `apparent sentence length`.

The third input in the example above shows the same scene well.

| Input | BPE `gpt2` | WordPiece `bert-base-uncased` | SentencePiece `google/mt5-small` |
| --- | --- | --- | --- |
| `회의는 내일 10:00 AM, Zoom 링크 포함입니다.` | 39 | 30 | 16 |

When people see the same sentence, it may feel like `a schedule notice with a little number and product name`. But in reality, sections such as `10:00`, `AM`, `Zoom`, and `링크` are cut differently by family, and token counts diverged greatly. This is why length prediction often misses in mixed-notation documents.

If we compress the same scene again as an operational memo, it becomes the following.

| Phenomenon first seen | Misjudgment if passed over as-is | Safer next judgment |
| --- | --- | --- |
| Requests with similar meanings seem likely to have similar costs | Overtrusting the budget without seeing actual token-count differences | Actually compare token counts for request groups with the same intent |
| Paragraphs are divided naturally, so chunks seem safe | Key conditions can be cut at chunk boundaries | Check where condition sentences are cut, down to token boundaries |
| A sentence looks short, so the input also seems short | Length prediction repeatedly misses in mixed-notation sections | Separately check sections with many numbers, URLs, and code fragments |

## Drawn Very Simply

```mermaid
--8<-- "assets/part-06/chapter-02/p6-c02-s05-tokenizer-difference-cases-en.mmd"
```

What you should check in this diagram is that tokenizer differences do not end as `name differences`. If cutting methods differ even for sentences with the same meaning, token count, chunk boundaries, and later retrieval and cost judgments can change together.

## Tokenization Differences Seen Again in Operational Scenes

| Scene | First question to ask |
| --- | --- |
| Is there a large cost difference between similar requests? | Where do piece boundaries repeatedly diverge? |
| Do retrieval chunks keep cutting out key conditions? | Does the meaning unit remain in the same token group? |
| Does length prediction often miss in mixed-notation documents? | How much does the whitespace-based word sense diverge from actual string processing? |

## Operational Scene Cases and Examples

### Case 1. Running Three Refund Question Templates

`환불 정책을 알려줘`, `환불 관련 정책을 간단히 설명해 줘`, and `환불이 가능한 조건만 짧게 정리해 줘` look like the same intent, but depending on the tokenizer, piece boundaries and token counts can increase differently.

The problem scene in this case is repeatedly sending same-intent requests as templates. The first human standard is the judgment that `if the meaning is similar, the cost will also be similar`. The limit of that standard is missing that when an expression gets a little longer or modifiers are added, the number of pieces can increase differently by tokenizer type.

| Case step | Observation in this scene | Result to check |
| --- | --- | --- |
| First human standard | All three sentences are refund-policy questions | Expects they can be treated as the same cost group |
| Limit of the standard | Expressions such as `관련`, `간단히`, and `가능한 조건만` are added | Each family may split additional expressions differently |
| Moment when the difference appears | A same-intent group repeatedly has a higher token count for a specific expression | Cost difference can first appear as a piece-count difference rather than a meaning difference |
| Changed judgment | Compare actual token counts of frequently used templates | Replace cost-spiking expressions with shorter or more stable expressions |

So the sentence to close this case is this. Tokenization-type differences appear before theory explanations in the scene where `requests with the same meaning have different costs`.

### Case 2. When Policy Chunks Keep Getting Cut Awkwardly

If `annual leave must be requested 3 days in advance` and `urgent sick leave can be reported afterward` must remain in the same evidence group, but token pieces and chunk boundaries diverge, retrieval results can bring only the principle and miss the important exception.

The problem scene in this case is a policy document that looks natural by paragraph standards but often fails in retrieval. The first human standard is the judgment that `because the paragraphs are visually divided well, the chunks should also be fine`. The limit of that standard is missing that chunks are actually cut not on character count or paragraph count, but on token count and token boundaries.

| Case step | Observation in this scene | Result to check |
| --- | --- | --- |
| First human standard | Principle and exception sentences are in nearby paragraphs | Expects retrieval context to capture them together |
| Limit of the standard | The piece count of the same phrase differs by tokenization type | Boundary positions can differ even with the same chunk size |
| Moment when the difference appears | Retrieval results bring only the principle and omit the exception condition | It may be a chunk-boundary problem, not a retrieval-quality problem |
| Changed judgment | Check whether condition and exception remain in the same token group | Recheck chunk size and overlap by token boundaries, not paragraph shape |

So the sentence to close this case is this. Tokenization-type differences appear behind the result that a retriever was wrong as the chunk-boundary question, `did the needed meaning unit remain in the same token group`.

### Case 3. When Cost Jumps in Mixed-Notation Documents

A sentence that mixes `SDK v2.1`, `Authorization`, long URLs, and code fragments can grow in token count faster than it looks. Even in the same document, one tokenizer can read these sections more finely, while another can keep them as larger pieces.

The problem scene in this case is a situation where the document does not look long, but the actual input length often jumps. The first human standard is the judgment that `because it is only a few short lines, the input should also be short`. The limit of that standard is missing that numbers, version strings, URLs, code fragments, and case mixing can split into many pieces for a tokenizer.

| Case step | Observation in this scene | Result to check |
| --- | --- | --- |
| First human standard | `SDK v2.1`, `Authorization`, and URLs are short notations | Expects the input length to also be small |
| Limit of the standard | Numbers, dots, slashes, uppercase letters, and code fragments are mixed | The whitespace-based word sense diverges from actual piece boundaries |
| Moment when the difference appears | Token-count increase is larger in mixed-notation sections than in ordinary sentences | Length-prediction failures concentrate in specific notation sections |
| Changed judgment | Separately inspect sentences with high mixed-notation density | Review separate compression or splitting strategies for URLs, code, and version strings |

So the sentence to close this case is this. Tokenization-type differences appear more clearly in the way length sense collapses in sections mixing numbers, English, symbols, and code than in ordinary sentences.

## Tokenization Differences Visible in Failure Scenes

A common mistake when reading tokenization-type differences is that even after recalling the three family names, readers still cannot immediately choose which scene the current problem should be read as. In that case, it is safer to first choose `which failure is visible now` rather than `which family is better`.

| Failure first visible now | First question to ask | Axis to revisit first |
| --- | --- | --- |
| Requests with similar meanings have a much larger cost difference than expected | `Where does the token count diverge more when the expression changes slightly?` | Cost difference |
| Paragraphs are natural, but retrieval results keep missing key conditions or exceptions | `Was the meaning unit people see as one group split at token boundaries?` | Chunk boundary |
| The sense of length keeps missing in documents that mix numbers, URLs, English, and code fragments | `Does mixed string notation have a larger effect than the whitespace-based word sense?` | Mixed-notation length prediction |

The purpose of this table is not to explain tokenizer families again. It is to make you first branch `whether the visible difference is a cost problem`, `a chunk problem`, or `a mixed-notation length problem` when you see an actual operational scene.

The judgment to close here is clear. Tokenization-type differences are not name differences. They are observations that actually appear in cost differences, chunk boundaries, and mixed-notation length prediction.

## Practice: Branch Observations into Failure Scenes

Do not leave `tokenization-type differences` as an abstract comparison. Check again what differences appear when the same input is put into different families.

Using the results of the example code above, branch the three scenes yourself. For each question, answer by yourself first, then compare with the explanation below.

### Exercise 1. Find the Moment a Cost Difference Appears

Observations:

| Input | BPE `gpt2` | WordPiece `bert-base-uncased` | SentencePiece `google/mt5-small` |
| --- | --- | --- | --- |
| `회의는 내일 열립니다.` | 24 | 17 | 8 |
| `회의는 내일 10:00 AM에 열립니다.` | 31 | 23 | 11 |

Answer by yourself first.

- After numbers and English were added, by how many tokens did each family increase?
- Is this difference a conclusion that `one family is better`, or does it show `when cost differences appear`?

Explanation: BPE increased by `31 - 24 = 7`, WordPiece by `23 - 17 = 6`, and SentencePiece by `11 - 8 = 3`. The answer here is not the superiority of a specific family. Even in the same schedule notice, the moment numbers and English are added, the increase differs by family. So tokenization-type differences can first appear in cost prediction scenes.

### Exercise 2. Find the Moment a Chunk-Boundary Difference Appears

Observations:

| Family | Representative pieces seen in the Korean sentence |
| --- | --- |
| BPE `gpt2` | Korean segmented finely into many byte-like pieces |
| WordPiece `bert-base-uncased` | Some parts are `[UNK]`, and some are subword pieces with `##` |
| SentencePiece `google/mt5-small` | Relatively larger pieces such as `회의`, `▁내`, `▁열`, and `립니다` |

Answer by yourself first.

- Which side has a greater risk that a Korean phrase people see as one group will scatter into finer pieces?
- Why can this difference become a problem in retrieval chunks?

Explanation: In this observation, BPE `gpt2` and WordPiece `bert-base-uncased` show Korean phrases scattering more finely. SentencePiece `google/mt5-small` left relatively larger Korean pieces. This difference shows that even if paragraphs look natural, meaning units can split in actual token groups. Therefore, tokenization-type differences can appear as a chunk-boundary problem where retrieval results miss conditions or exceptions.

### Exercise 3. Find the Moment Mixed-Notation Length Prediction Shakes

Observations:

| Input | BPE `gpt2` | WordPiece `bert-base-uncased` | SentencePiece `google/mt5-small` |
| --- | --- | --- | --- |
| `회의는 내일 10:00 AM에 열립니다.` | 31 | 23 | 11 |
| `회의는 내일 10:00 AM, Zoom 링크 포함입니다.` | 39 | 30 | 16 |

Answer by yourself first.

- After `Zoom 링크 포함` was added, by how many tokens did each family increase?
- In this scene, which axis should be revisited first among cost, chunks, and mixed-notation length prediction?

Explanation: BPE increased by `39 - 31 = 8`, WordPiece by `30 - 23 = 7`, and SentencePiece by `16 - 11 = 5`. All three increased, but the increase was not the same. The core of this scene is not cost calculation alone, but that the sense of length shakes in sections where numbers, English, symbols, and Korean are mixed, such as `10:00`, `AM`, `Zoom`, and `링크`. Therefore, the axis to revisit first is mixed-notation length prediction.

The goal of this exercise is not `choosing one correct family among the three`. What is needed is reading the moment when `tokenization-type differences` actually appear in cost, chunks, and mixed-notation length prediction.

## Checklist

- Can you explain that even sentences with the same meaning can have different token counts?
- Can you say that tokenization-type differences can appear in chunk-boundary and length-prediction problems?
- Do you understand that you should first ask `when does the difference appear`, rather than `which family is superior`?
- Can you explain that using representative tokenizers directly reveals the difference between character-count sense and actual piece boundaries?

## Sources and References

- Rico Sennrich, Barry Haddow, Alexandra Birch, [Neural Machine Translation of Rare Words with Subword Units](https://aclanthology.org/P16-1162/){: target="_blank" rel="noopener noreferrer" }, ACL 2016, accessed 2026-07-19. Used as background evidence for BPE and subword units being used for rare-word and out-of-vocabulary handling.
- Taku Kudo, John Richardson, [SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing](https://aclanthology.org/D18-2012/){: target="_blank" rel="noopener noreferrer" }, EMNLP 2018, accessed 2026-07-19. Used as evidence for SentencePiece's language-independent raw-sentence processing and whitespace handling.
- Hugging Face, [Summary of the tokenizers](https://huggingface.co/docs/transformers/v4.38.1/en/tokenizer_summary){: target="_blank" rel="noopener noreferrer" }, Transformers documentation, accessed 2026-07-19. Used to confirm that BPE, WordPiece, and SentencePiece differences appear as actual tokenizer piece-boundary and token-count differences.
- Hugging Face, [AutoTokenizer](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoTokenizer){: target="_blank" rel="noopener noreferrer" }, Transformers documentation, accessed 2026-07-19. Used to confirm the example-code flow using `AutoTokenizer.from_pretrained`, `tokenize`, and `convert_tokens_to_ids`.
