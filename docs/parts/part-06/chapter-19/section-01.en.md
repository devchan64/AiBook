# P6-19.1 Reading LLM History as a Flow of Limits and Structural Shifts

> Section ID: `P6-19.1`
> Version: `v2026.07.26`

A common misunderstanding when trying to understand today's LLMs(large language models) is to see them only as `huge models that suddenly appeared`. In reality, today's generative experience was made by the overlap of language models, embeddings, sequence models, attention, Transformers, and large-scale pretraining.

This section reconnects that flow not as a list of event names, but through the criterion `which limitation led to the next structure?` Here, more important than explaining the chapter's location is learning first why embeddings followed n-grams and why attention and Transformers followed RNNs.

## Limits-to-Structural-Shifts Flow

The core questions are:

- How was language modeled before LLMs?
- What problems did embeddings and sequence models try to solve?
- Why did attention and Transformer become turning points?
- What did pretrained LLMs change?

LLM history is safer to read as a large flow of `which limitation led to the next structure?` The sequence of structural shifts should appear before event names.

Instead of memorizing every detail, focus first on tying together `which limitation called the next shift`. Since you have already read about tokens, Transformers, GPT, and pretraining, what matters now is whether you can retell how those structures arrived in the order `limitation -> next structure`.

If we compress only the shifts to keep, these seven steps are enough.

| Shift | Limitation it tried to reduce | One line to keep |
| --- | --- | --- |
| n-gram | Poor generalization to long context | Language began to be treated as a probability problem. |
| Embedding | Words were treated only as completely separate symbols | Similar expressions could be seen as closer. |
| RNN/Seq2Seq | Difficulty handling long order | Earlier context was connected further into later interpretation. |
| Attention | Fixed-length compression bottleneck | The model could refer back to needed positions. |
| Transformer | Sequential-computation bottleneck | Relationship computation moved into the center of the structure. |
| Pretraining | Each task had to be adapted from scratch | Large language patterns were learned first and reused. |
| GPT-style interface | Tasks felt separated by model | Many tasks could close through one generative interface. |

## Separating Event Names from Structural Shift Flow

- You can explain LLM history through several large turning points.
- You can distinguish the positions of statistical language models, embeddings, RNNs, attention, Transformers, and pretraining.
- You can explain an LLM as one flow in the language-model family, not as all of AI.
- You can prepare to separate direct lineage from surrounding evidence.

## Step 1. Language Began as a Probability Problem

The core question of early language models was simple.

- Given previous words, which next word is likely?
- Which word sequence seems more plausible?

At this stage, methods such as n-grams were widely used. They approximated next-word probabilities by counting word frequencies in a short context.

The key contribution of this period was:

- language began to be treated not only as a list of rules, but as a probability problem;
- the viewpoint of `next-word prediction` became clear.

But the limits were also clear.

- Long context was hard to handle.
- Rare expressions and new combinations were weak.
- Similar words were hard to generalize across.

## Step 2. Words Began to Be Represented as Vectors

The next shift was embedding.

Instead of leaving words as completely separate symbols like one-hot vectors, representing them as vectors of several numbers allows words used in similar contexts to occupy somewhat closer positions.

The important questions at this stage were:

- How can a model see words with similar uses, such as `cat` and `dog`, as closer?
- How can text be turned into a computable continuous representation?

Research such as word2vec spread this intuition widely. After this period, language modeling moved strongly toward learning not only `next-word probability`, but also a good `representation space`.

## Step 3. Order Began to Be Handled by Neural Structures

Language is sequence data, so obtaining word vectors is not enough. The structure must better handle how earlier context affects later interpretation.

At this stage, RNNs(recurrent neural networks), LSTMs(long short-term memory), and GRUs(gated recurrent units) became important.

These structures tried to solve questions such as:

- Can information seen earlier be carried later?
- Can an ordered sentence be accumulated as state?
- Can less information be lost in long context?

For problems such as machine translation, Seq2Seq(sequence-to-sequence) was also a major shift.

- Read the input sentence.
- Build an internal representation.
- Generate the output sentence.

That flow became possible.

## Step 4. Attention Reduced a Bottleneck

RNN-based Seq2Seq was powerful, but it had a bottleneck problem: the whole input had to be compressed into a fixed-length representation.

Attention tried to reduce this problem.

- When producing an output word,
- it looks back across the whole input,
- and gives larger weights to relevant positions.

It is enough to remember it this way.

`Attention is a structure that lets the model refer back to relevant parts of the input when needed.`

This stage matters because the direct structural shift toward LLMs begins here.

## Step 5. Transformer Changed the Central Structure

Transformer made attention not an auxiliary device, but the central structure.

The meaning of this shift is large.

- It is less bound to long sequential computation.
- It fits parallel processing better.
- It can compute relationships among tokens more directly.

As seen earlier in Part 6, Transformer places self-attention at the center and handles token-to-token relationships through large matrix operations.

This structure fit large-scale GPU-based training well. So Transformer became not merely `one translation model`, but the base structure for later LLM spread.

## Step 6. Pretraining Changed How Models Are Used

The next shift was pretraining.

Instead of immediately fitting a model to a small specific task, the central approach became first learning general language patterns from large-scale text and then connecting the model to many tasks.

The important changes at this stage were:

- Learn language patterns broadly first.
- Then connect them through fine-tuning or prompt-based use.
- Increase the possibility that one large model can handle many tasks.

This shift appeared strongly in different directions in BERT and GPT families.

## Step 7. LLMs Broadened the Generative Interface

As GPT-family models grew, the user experience also changed.

- Users can give instructions in natural language.
- A few examples can change behavior.
- The same model begins to look as if it can summarize, classify, translate, draft, and generate code.

At this point, users often feel that `all AI has become LLMs`. But the safer explanation is:

`An LLM is not all of AI. It is one family that created a very large shift in language and generative interfaces.`

## Drawing the Flow Very Simply

```mermaid
--8<-- "assets/part-06/chapter-19/p6-c19-s01-history-flow-en.mmd"
```

This diagram is for holding the `large shift sequence`, not all complex details. The result to confirm from it is whether you can actually explain how statistical language models, embeddings, sequence models, attention, Transformers, and large-scale pretraining connect in order without mixing them together.

## Cases and Examples

### Case 1. Translation

Translation is easy to first imagine as `replacing words with words in another language`. But as sentences grow longer, subjects, negation, and modifier scope from earlier parts affect later word choices, so simple substitution quickly collapses. This scene quickly shows why history needed `short frequency calculation -> order handling -> referring back to relevant positions`. The result to confirm in this case is whether a structure that handles longer sentence relationships more broadly is actually more stable than word-substitution rules.

| Simple intuition that is easy to hold first | What is actually missing | Structure that became necessary |
| --- | --- | --- |
| Just change word meanings | Long-distance relationships and whole-sentence state | Seq2Seq, attention |
| Replace words sequentially from the front | Later context can change earlier choices | Structure for referring back to relevant positions |
| Many dictionary mappings are enough | Natural whole-sentence construction | Transformer-based wide-context handling |

### Case 2. Search and Embeddings

If a user searches `my refund is late`, but the document says `reimbursement processing delay`, it is easy to think that failing to find it is natural because the same words do not appear. But in real services, user expressions and document expressions keep diverging, so word matching alone misses related documents. This scene compresses why `representation space` became important in history, and how that flow later connected to vector search and RAG. The result to confirm in this case is whether a document with a similar meaning can reappear as a candidate even when the same words are absent.

| Seen through surface matching | Problem in real service | Change brought by representation-space thinking |
| --- | --- | --- |
| If the same word is absent, it looks like a different issue | Similar-meaning documents are often missed | Similar-meaning expressions can be compared as closer |
| Search looks like a word-matching game | Search quality drops when user phrasing changes | Related candidates can be recovered even when expressions differ |
| Matching only title words seems enough | Body phrasing differences and indirect expressions are missed | Directly connects to vector search and RAG |

### Case 3. Chatbot Experience

When a user asks one chat window to summarize, classify, and revise sentences one after another, it is easy to feel that `a huge assistant that can do everything appeared from the beginning`. In reality, `next-word prediction`, `representation learning`, `long-context handling`, `attention`, `Transformer`, and `large-scale pretraining` accumulated step by step until `many tasks could close in one interface`. The result to confirm in this case is whether today's chatbot experience can be explained as an accumulation of structural shifts, rather than as one sudden invention.

The three cases can be tied together through the history flow as follows.

| Situation | What looks simple first | Structural shift that actually accumulated |
| --- | --- | --- |
| Translation | Word substitution problem | Expansion to long sentence relationships, attention, and Transformer |
| Search and embeddings | Finding the same word | Representation learning that places similar-meaning expressions closer |
| Chatbot experience | One chat window handles everything | Structural accumulation that lets several tasks close in one interface |

## Scenes to Reread Through Structural Shift Flow

A common misunderstanding when first reading history is to focus on memorizing event names in order and miss `why the next structure became necessary`. The criterion should not be year memorization, but `which limitation pushed the next shift?` Turned into practical questions, this reads as follows.

| If this suspicion appears | First question to ask |
| --- | --- |
| `Why was another structure needed again?` | What could the previous structure not do? |
| `Is this a search story or a model story?` | Did we separate representation generalization from long-order handling? |
| `It looks as if LLMs suddenly do everything.` | In what order did several shifts accumulate? |

The first criterion to learn is simple. History is safer to read not as a `name list`, but as a sequence of structural shifts that tried to reduce limits: `frequency-calculation limit -> need for representation space -> need for long-order handling -> referring back to relevant positions -> Transformer -> pretraining`.

## Structural Shifts Seen on the History Axis

The needed activity in this section is not running code to check a small result value. It is placing a feature or case in front of you back onto the history axis. When understanding LLM history, the more important ability is not `what computation can be mimicked`, but verbally distinguishing `which limitation made the next structure necessary`.

The table below folds the cases above back onto the history axis. In each row, what you need to confirm is not the technology name itself, but the limitation it tried to reduce and why it led to the next structure.

| Observed scene | Directly corresponding history stage | Judgment the reader should gain now |
| --- | --- | --- |
| Predict the next word from short-context frequency | Starting point of statistical language models | Frequency alone is weak for long context and new combinations. |
| Expressions such as `refund` and `reimbursement`, or `late` and `delay`, should be grouped despite different words | Direction of embeddings and representation generalization | A representation space is needed to compare similar meanings even without the same word. |
| `Approved` and `not approved` change meaning through order and negation | Problem awareness behind sequential processing such as RNN, LSTM, and GRU | Even if words look similar, sentence interpretation collapses when previous and following state is missed. |
| In long-sentence translation, the input position relevant to the word being generated must be revisited | Attention and Transformer shift | Computation that refers back to relevant positions when needed moved into the structural center. |
| One large model handles summary, classification, translation, and drafting through the same interface | Pretraining and GPT-style interface | The intuition should move from separate task-specific models to reusing large language patterns. |

## Exercise: Place Feature Scenes on the History Axis

Look at the following features and first write which historical problem awareness is most directly connected. If it is hard to choose only one, write two among `frequency`, `representation`, `order`, `referring back to relevant positions`, and `pretraining`.

1. A system finds the document `reimbursement processing delay guide` even when the customer says `my refund is late`.
2. A system summarizes the final request in a long email thread.
3. One chat interface appears to handle translation, drafting, and classification.
4. If you slightly change the examples given with the same question, the answer style changes with them.

After classifying the four scenes first, compare with the explanation below.

| Feature scene | History axis to mark first | Explanation |
| --- | --- | --- |
| A system finds the document `reimbursement processing delay guide` even when the customer says `my refund is late` | representation | Because similar meanings must be grouped even without the same words, the problem awareness of embeddings and representation space is most direct. |
| A system summarizes the final request in a long email thread | order, referring back to relevant positions | The system must follow the flow of a long input and also revisit positions needed for the current summary, so sequential processing and attention appear together. |
| One chat interface appears to handle translation, drafting, and classification | pretraining, GPT-style interface | The center is the intuition of reusing a model that first learned large language patterns through many instructions, instead of building separate task-specific models. |
| If you slightly change examples given with the same question, the answer style changes with them | pretraining, context use | The model reads examples in the current input context like conditions and changes generation behavior, which connects to prompt-based use after pretraining. |

In this exercise, the reason matters more than the answer. If you can explain a feature through the reason for a structural shift, such as `search is a representation problem`, `summary is a long-context and relevant-position problem`, and `chat interface is a post-pretraining usage problem`, this section's goal is met.

## Criterion Connecting Limits to the Next Structure

After seeing the whole flow, it also becomes clearer that you do not need to remember every implementation detail of each stage. For now, the following is enough.

| What is enough to keep now | Where to revisit it in the main flow |
| --- | --- |
| Language modeling began from the problem of `predicting the next expression` | P6-6.1 Next token prediction |
| Embedding was the shift from symbols to computable vectors | P6-3.1 Embeddings that turn token IDs into comparable coordinates |
| Attention and Transformer were structural turning points | P6-4.1 How Transformer leads to next-candidate scores in LLMs |
| Pretraining changed how models are used | P6-7.1 Pretraining |

The more important question is not `can you memorize the whole history at length?`, but `can you explain why the main flow was arranged in that order?`

The result to confirm is whether explanations such as GPT, next-token prediction, and pretraining can be reread not as a list of features, but as a flow in which each structure filled a limitation and led to the next stage.

- It places the Transformer from the front of Part 6 back into the LLM lineage of Part 6.
- It reduces structural confusion when later reading BERT, GPT, pretraining, instruction tuning, and RAG.
- It reduces the misunderstanding that LLMs are identical to all of AI.

## Checklist

- You should be able to explain LLM history not as an `event-name list`, but as a shift flow of `frequency -> representation -> order -> referring back to relevant positions -> pretraining`.
- You should be able to say which historical-stage problem sits behind translation, search, and chatbot experiences.
- You should be able to explain that today's LLMs can be read more accurately only by holding both the pre-Transformer problem awareness and the post-pretraining usage shift.

## Sources and References

- Yoshua Bengio et al., [A Neural Probabilistic Language Model](https://www.jmlr.org/papers/v3/bengio03a.html){: target="_blank" rel="noopener noreferrer" }, Journal of Machine Learning Research, 2003, accessed 2026-07-19.
- Tomas Mikolov et al., [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/abs/1301.3781){: target="_blank" rel="noopener noreferrer" }, arXiv, 2013, accessed 2026-07-19.
- Ilya Sutskever, Oriol Vinyals, Quoc V. Le, [Sequence to Sequence Learning with Neural Networks](https://arxiv.org/abs/1409.3215){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-07-19.
- Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio, [Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473){: target="_blank" rel="noopener noreferrer" }, arXiv, 2014, accessed 2026-07-19.
- Ashish Vaswani et al., [Attention Is All You Need](https://papers.nips.cc/paper/7181-attention-is-all-you-need){: target="_blank" rel="noopener noreferrer" }, NeurIPS, 2017, accessed 2026-07-19.
- Jacob Devlin et al., [BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding](https://arxiv.org/abs/1810.04805){: target="_blank" rel="noopener noreferrer" }, arXiv, 2018, accessed 2026-07-19.
- Tom B. Brown et al., [Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }, arXiv, 2020, accessed 2026-07-19.
