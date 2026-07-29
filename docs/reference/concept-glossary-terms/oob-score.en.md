<a id="oob-score"></a>

### OOB score(out-of-bag score)

- Meaning: An internal validation-like score in random forest that uses samples not drawn into a tree's bootstrap sample.
- Why it matters: Because each tree leaves some samples out of its bootstrap draw, random forest can get a rough self-check signal during training. This score should be read as a quick inspection aid, not as a replacement for final testing.
- Related concepts: `random forest`, `bootstrap`, `validation data`, `metric`
- Core Section: `P4-15.3`
- Appears in: `P4-15.4`
