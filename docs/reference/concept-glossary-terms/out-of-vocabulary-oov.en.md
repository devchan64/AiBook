## out-of-vocabulary, OOV

- Meaning: Out-of-vocabulary, or OOV, refers to a word or token that falls outside the current vocabulary or tokenization rules. A human may see a meaningful expression, but the model may not be able to represent it as familiar units. OOV is therefore a signal that an input expression is outside the current vocabulary system, not simply that the sentence is strange.
- Why it matters: When many OOV items appear in classification or search, the model may effectively read less of the input. This helps interpret poor performance as a possible tokenizer or vocabulary design issue, not only as a model capability issue. Domain terms, new words, and product codes can be clear to people while still being fragmented into unfamiliar pieces for a model.
- Related concepts: `tokenization`, `token coverage`, `embedding`
- Core Section: `P7-4.2`
- Appears in: `P6-2.5`, `P7-4.1`, `P7-4.3`, `P7-summary`
