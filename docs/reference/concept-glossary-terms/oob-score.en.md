<a id="oob-score"></a>

## oob_score

- Meaning: `oob_score` is a random-forest setting that uses out-of-bag samples, samples not used to train a given tree, to compute an internal evaluation signal.
- Why it matters: OOB can give a partial validation-like signal, but it does not replace every evaluation procedure. It should be read as a helper that naturally follows from bootstrap sampling.
- Related concepts: `bootstrap`, `random forest`, `validation`, `test data`
- Core Section: `P4-15.3`
- Appears in: `P4-15.1`, `P4-15.3`
