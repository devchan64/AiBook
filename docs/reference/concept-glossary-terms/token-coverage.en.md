## token coverage

- Meaning: Token coverage is the share of tokens in an evaluation sentence or document that are actually readable under the current vocabulary or tokenizer rules. Even if an input looks complete to a person, this value checks how much of it is preserved as usable token units for the model.
- Why it matters: The same accuracy number can mean different things when much of the input falls outside the vocabulary. Token coverage helps readers check whether poor performance comes from model structure alone or from input expressions that were not preserved well enough.
- Related concepts: `tokenization`, `token`, `out-of-vocabulary, OOV`
- Core Section: `P7-4.2`
