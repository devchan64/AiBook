# P3-7.3 What Is a Baseline the Reference For

> Section ID: `P3-7.3`
> Version: `v2026.09.20`

“Compare against a reference” can describe different questions: comparing a measurement with the past, with an operating limit, or comparing model performance with a simple prediction rule. **Record both the comparison target and the calculation units to keep these references distinct.**

## Three References Answer Different Questions

| Reference | Question | Values compared | Example result |
| --- | --- | --- | --- |
| Data baseline | How much changed from the usual level? | Current and historical reference pressure | +8 kPa |
| Operating limit | Was the specified allowed condition exceeded? | Current pressure and upper limit | +3 kPa above the limit |
| Baseline model | Does prediction outperform a simple rule? | Correct counts or metrics on the same evaluation data | 5/12 versus 9/12 |

A data baseline uses historical measurements or group summaries as references. An operating limit specifies an allowed condition separately. A baseline model is a model or rule used as a starting point for performance comparison. None automatically determines the others.

## Distinguish +8 from +3 at a Current Pressure of 108 kPa

Assume, for illustration, current pressure 108 kPa, historical reference pressure 100 kPa under matching conditions, and a separately specified upper limit of 105 kPa. These numbers are not limits for actual equipment. In this example, the allowed condition is pressure at or below 105 kPa.

| Calculation | Result | Interpretation |
| --- | --- | --- |
| Current−data baseline | 108−100=+8 kPa | Eight above the historical reference |
| Current−upper limit | 108−105=+3 kPa | Three above the specified limit |

Both differences use kPa but answer different questions. The +8 baseline difference cannot replace the amount above the limit. If current pressure were 103, it would be +3 relative to baseline but −2 relative to the limit, satisfying this upper-limit condition. That one condition alone still would not establish safety of all operations.

If the historical reference were also 108, the baseline difference would be zero, yet current pressure would remain three above the 105 limit. “Same as usual” does not mean “within allowed conditions” or “safe.” The historical state may itself have been persistently unsuitable.

## A Baseline Model Compares Predictions Rather Than Measurements

The `dummy` in [P3-4.5](../chapter-04/section-05.en.md) always predicted 0, the more common training label. This is a simple baseline model. On the same twelve test cases, dummy got five correct and the decision tree got nine. The comparison concerns agreement between predictions and labels, not changes in pressure.

| Model | Correct / evaluated | Accuracy |
| --- | ---: | ---: |
| dummy | 5/12 | About 41.7% |
| tree | 9/12 | 75.0% |

The difference is four correct cases, or about **33.3 percentage points** of accuracy. Labels in that example come from a fictional rule applied to input conditions, so it does not validate actual failure prediction. Nor should scores from different test datasets be compared directly. Part 4 develops evaluation metrics and data splitting in detail.

A simple baseline model does not necessarily perform poorly. Evaluation must establish whether a more complex model surpasses it. Accuracy of 75% also cannot determine whether 108 kPa is permitted: the decisions concern different objects.

## State the Comparison Target in the Report {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-3-mermaid-01-en.mmd"
```

Complete “Three above the reference.” For the pressure example, write “Current pressure of 108 kPa is 3 kPa above the upper limit of 105 kPa.” If the statement instead compares with the 100 kPa data baseline, the difference must be 8 kPa.

Also correct “Zero difference from baseline means normal.” The answer is: “Current and historical reference values match, but compliance with operating limits must be checked separately.” Recording change observations, operating-condition decisions, and model performance separately prevents transferring one result into another judgment.

## Checklist

- Can you identify the comparison targets for +8 kPa and +3 kPa?
- Can you explain zero baseline difference while exceeding an upper limit?
- Can you explain what P3-4.5's dummy predicts as a baseline?
- Can you distinguish percentage points of accuracy from units of physical differences?

## Sources and Further Reading

- National Cancer Institute, `baseline`. Because it explains baseline as the standard against which later change is compared after an initial measurement is set, it provides a general basis for reading baseline in this section as `a state-comparison reference`. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the definition of a reference period used to compare other times, it reinforces the explanation in this section that the current range and the usual range should be placed side by side so the direction of change can be read. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
