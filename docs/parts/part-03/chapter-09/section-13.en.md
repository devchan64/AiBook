# P3-9.13 Why Must Time Boundaries, Entity Boundaries, Information Boundaries, and Output Format Be Closed Together Right Now

> Section ID: `P3-9.13`
> Version: `v2026.07.20`

If the structure has been organized enough to sort out the current problem type, there is one final set of boundaries that still must be closed together. Is time order important? Should the same entity be prevented from mixing across both sides? Has information from after prediction time leaked into the inputs? Is the real output closer to ranking or a continuous value than to simple 0/1 classification? What matters here is not expanding the list of terms, but checking whether the current problem structure stands without contradiction in front of these boundaries.

| Item to check right here | Minimum sentence to hold now |
| --- | --- |
| time split | A problem where time order matters must be read differently from a random split |
| group split | Exaggerated performance can appear if the same entity is mixed across both sides |
| data leakage | If information from after prediction time is mixed in, the score may look good but cannot be used |
| evaluation design | Which metric and split fit must be connected to the problem structure |
| ranking | Selecting the top few cases can be centered on order rather than class |
| multiclass / regression | The result structure may not be only one 0/1 label |

At the stage of sorting out the current problem type, it is enough if boundaries like the following are closed.

- Does this problem require a time-order split first?
- Should the same entity be prevented from appearing on both sides?
- Has information from after the result leaked into the input?
- Is the actual target closer to ranking or a continuous value than to 0/1 classification?

## A Small Diagram

For this last check, the more important thing is not memorizing the item names, but closing the current problem structure in a sensible order.

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-13-mermaid-01-en.mmd"
```

In this section, what matters more than memorizing all the names is checking whether the current data structure has properly closed the time boundary, entity boundary, information boundary, and output format. At the present stage, what is needed is not to unfold detailed procedures at length, but to make the current structure able to state without contradiction what it predicts and what it still should not predict. This section should therefore be read not as a list of names, but as the final checklist for whether `split design`, `information-boundary inspection`, and `output-format selection` are closed without contradiction inside the current problem structure at the stage of sorting out the current problem type.

## Sources and References

- Google, *Machine Learning Glossary*, `label leakage`. Used to check the information-boundary basis that information from after prediction time can become a label proxy inside the features. Accessed: 2026-07-20. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Classification: ROC and AUC*. Used to check the ranking/evaluation-design view that AUC and ROC relate to ranking positive examples above negative examples and are distinct from the chosen threshold. Accessed: 2026-07-20. [https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc](https://developers.google.com/machine-learning/crash-course/classification/roc-and-auc){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*. Used to check the provenance basis for recording processing steps, reproducibility, versioning, and derivation relationships. Accessed: 2026-07-20. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }
- Hyndman, Athanasopoulos, *Forecasting: Principles and Practice (3rd ed.)*, Section 5.10 Time series cross-validation. Used as time-split evidence that, in time-ordered problems, each training set should contain only observations before the test observation and no future observations should be used to construct the forecast. Accessed: 2026-07-20. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn developers, *Cross-validation: evaluating estimator performance*, cross-validation iterators for grouped data. Used as group-split evidence that samples from the same group should not appear in both the paired training and validation/test sides when group dependence matters. Accessed: 2026-07-20. [https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data](https://scikit-learn.org/stable/modules/cross_validation.html#cross-validation-iterators-for-grouped-data){: target="_blank" rel="noopener noreferrer" }
