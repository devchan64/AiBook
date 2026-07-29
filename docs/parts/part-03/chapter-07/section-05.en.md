# P3-7.5 Should a Baseline Stay Fixed, or Should It Be Updated as a Recent-Usual Reference

> Section ID: `P3-7.5`
> Version: `v2026.07.25`

After [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) candidates are chosen, another question still remains. `Should this reference stay fixed for a while, or should it move together with the recent-usual range?` Even when ranges under the same conditions were selected, the meaning of the comparison sentence changes according to how the baseline is maintained.

The baseline-maintenance method is not a problem where one correct answer has to be fixed in advance. The more natural choice changes according to what kind of change we want to see.

| Baseline form | The question it fits better | What to watch out for |
| --- | --- | --- |
| Fixed baseline | How much did we change from one particular reference point? | If current operation already changed, it can become an overly old reference |
| Recent-usual baseline | Inside the recent flow, is only the current state different? | If the range is too short, the baseline itself becomes unstable |

For example, if we want to keep the stable range right after equipment calibration as a representative reference for a long time, a fixed baseline is natural. By contrast, in a system where the operating environment changes little by little, using a recent-usual range as the baseline may be more realistic. The important point is that whichever method we use, we should be able to explain in words `what exactly are we comparing the present against right now?`

If we generalize this choice, it becomes the problem of `should the reference be kept, or should it roll forward?` BLS's `base period` shows the general principle of fixing a reference point for comparison, while FPP3's rolling forecasting origin shows that as time moves forward, the past range that serves as the reference can also move forward. Here we do not need to copy those concepts directly. It is enough to connect them at the level that `the question decides how the reference should be maintained`.

## How the Sources Connect to the Main Claim

When we attach external sources, it is safer to connect them not only to the word `baseline` itself, but to the role that the reference is playing.

| Main claim in the text | What kind of general support is needed | What role the current source can play |
| --- | --- | --- |
| A baseline should be a reference range for comparison | An explanation that baseline or base period means a comparison reference point | NCI's definition of baseline and BLS's definition of base period support this point |
| A baseline may stay fixed or be updated according to the question | An explanation that a comparison structure is also possible where the reference moves over time | FPP3's rolling forecasting origin shows the analogous point that the reference is not always fixed |

Rolling origin is a concept from the context of forecast evaluation, so we do not equate it directly here. In this book, it is used only as an analogical support for explaining why `a recent-usual baseline` can also be a natural choice.

## What We Do Not Assert Here

The following statements are not asserted in this section.

- A baseline should always keep being updated to the recent range
- The sample-count criterion is the same number in every domain
- A fixed baseline is always more trustworthy than a recent-usual baseline

If the baseline-maintenance method is chosen poorly, the meaning of both the [comparison report](/AiBook/en/reference/concept-glossary-alpha/o/#glossary-output-structure) and the current comparison sentence shakes together. Even for the same change, if the reference itself changes, the weight of the current judgment such as `needs review`, `caution`, or `normal/abnormal candidate` also changes. If this section is reread not as a matter of taste between fixed baselines and recent-usual baselines, but as the problem of [reference maintenance strategy](/AiBook/en/reference/concept-glossary-alpha/r/#glossary-reference-maintenance-strategy), then it becomes clearer that baseline maintenance is not a contest with one right answer. It is a choice of what reference-maintenance method fits the comparison question.

## A Small Diagram

The key point in this section is not the baseline form by itself, but which maintenance method is made more natural by the `comparison question`. Fixed baselines and recent-usual baselines support different questions better, and the meaning of the comparison sentence changes with that choice.

--8<-- "assets/part-03/chapter-07/p3-7-5-mermaid-01-en.mmd"

## Sources and Further Reading

- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general principle of placing one specific point or period as the comparison reference, it supports the role of a fixed baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute, `baseline`. Because it explains baseline as a reference for comparing change over time after an initial measurement is set, it reinforces this section's premise that a baseline is first a reference measurement for comparison. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains that a control chart compares the current process characteristic with past performance and that control limits should change only with a valid and compelling reason, it directly supports this section's point that whether to keep or update a baseline should follow the comparison question and the grounds for operational change. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Hyndman, Athanasopoulos et al., `Forecasting: Principles and Practice (3rd ed)`, `Time series cross-validation`. Because it explains structures such as rolling forecasting origin, where the reference moves forward over time, it serves as an analogous support for the idea that an operating method is possible where the reference range also moves, as with a recent-usual baseline. But because this source belongs to forecast evaluation, this section uses only the higher-level idea of `a moving reference`, and only by analogy. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
