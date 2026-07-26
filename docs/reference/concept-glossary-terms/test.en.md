<a id="test"></a>

## test

- Meaning: A test is the final evaluation data or procedure used after training and model-selection choices are finished. It should be read as a final check, not as another place to tune the model.
- Why it matters: Testing separates performance on already-used information from performance on data treated as unseen. Mixing validation and test roles can make reported performance too optimistic.
- Related concepts: `validation`, `data leakage`, `generalization`, `evaluation`
- Core Section: `P2-12.3`
- Appears in: `P2-15.2`, `P4-index`
