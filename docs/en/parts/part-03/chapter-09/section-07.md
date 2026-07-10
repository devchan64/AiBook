# P3-9.7 Under What Conditions Can Inputs and Results Be Read as a Prediction Problem

> Section ID: `P3-9.7`
> Version: `v2026.07.10`

Once you decide to raise the problem into a prediction problem, you now need to close whether its structure satisfies actual prediction conditions. What matters is not a long theory but four checks: which columns are inputs, which columns are result candidates, whether information from after the prediction time has leaked in, and up to what information you look while predicting a result from what time point.

This section closes four things first: the split between inputs and results, leakage prevention, reproducibility at the operating time point, and the time boundary.

| What should be closed first | If turned into a question |
| --- | --- |
| Split between inputs and results | Which columns are features and which are target candidates? |
| Preventing future-information leakage | Has any value been mixed in that would still be unknown at prediction time? |
| Reproducibility at the operating time point | Can the inputs built during training be rebuilt in operations by the same rule? |
| Cutoff / horizon | Up to what information do you look, and what later result are you trying to predict? |

Even when the same sample boundary is kept, the input representation does not need to stay fixed as only one form. In some cases, a one-row feature vector is more natural. In others, a grouped input that preserves time order is more natural. What matters is that regardless of representation style, the contract `is this an input that can actually be used at prediction time` and `is the result candidate closed together with the time boundary` must be satisfied first. What is being handled here is therefore not `just any table`, but an input structure whose sample boundary and time boundary are closed. The core is not `passing along a table`, but `closing the input/result contract that holds at prediction time`. More broadly, what gets closed here is a prediction contract in which `input definition`, `result definition`, `time-point availability`, and `reproducibility` all match together.

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `label leakage`, accessed 2026-07-08. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }
- Google, *Machine Learning Crash Course: Dividing Datasets*, train/validation/test separation and real-world consistency. [https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets](https://developers.google.com/machine-learning/crash-course/overfitting/dividing-datasets){: target="_blank" rel="noopener noreferrer" }
- W3C, *PROV-Overview: An Overview of the PROV Family of Documents*, reproducibility and versioned derivation overview. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" }

