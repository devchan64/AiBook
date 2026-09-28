# P3-7.5 Should a Baseline Stay Fixed, or Should It Be Updated as a Recent-Usual Reference

> Section ID: `P3-7.5`
> Version: `v2026.09.20`

After [baseline](/AiBook/en/reference/concept-glossary-alpha/b/#glossary-baseline) candidates are chosen, another question still remains. `Should this reference stay fixed for a while, or should it move together with the recent-usual range?` Even when ranges under the same conditions were selected, the meaning of the comparison sentence changes according to how the baseline is maintained.

The baseline-maintenance method is not a problem where one correct answer has to be fixed in advance. The more natural choice changes according to what kind of change we want to see.

| Baseline form | The question it fits better | What to watch out for |
| --- | --- | --- |
| Fixed baseline | How much did we change from one particular reference point? | If current operation already changed, it can become an overly old reference |
| Recent-usual baseline | Inside the recent flow, is only the current state different? | If the range is too short, the baseline itself becomes unstable |

For example, if we want to keep the stable range right after equipment calibration as a representative reference for a long time, a fixed baseline is natural. By contrast, in a system where the operating environment changes little by little, using a recent-usual range as the baseline may be more realistic. The important point is that whichever method we use, we should be able to explain in words `what exactly are we comparing the present against right now?`

## A Moving Baseline Can Hide Long-Term Change

In a fictional example, suppose the mean immediately after calibration is 100, the recent usual mean is 108, and the current value is 110. The difference from the fixed baseline is +10; the difference from recent usual conditions is +2. Both calculations are correct, but one shows accumulated change since calibration and the other shows additional change from the recent state. A continually moving baseline can make gradual change appear small.

When constructing a recent-usual baseline, first define a rule that excludes the current comparison target. Comparing current value 130 with past values 100 and 100 gives a difference of +30. Including the current value in the baseline mean raises it to 110 and reduces the difference to +20. If past windows are defined for each prediction time, also exclude records from after the current time.

NIST's EWMA control chart describes a monitoring statistic that weights recent observations and past information. Updating a statistic is different from redefining control limits, so this does not justify continually accepting signs of an anomaly as the new normal. Baseline updates must retain the included period, excluded states, update time, and previous version.

A fixed baseline can track long-term change; a recent-usual baseline can detect departures from the recent state. Placing both differences side by side in the same report separates their comparison purposes.


## Record Periods, Exclusions, and Versions Alongside Values

The following fictional record makes the preceding 100, 108, and 110 concrete. Values are per-action mean pressures in kPa under matching conditions. Assume equal weighting of actions completed within each reference period, using valid records with matching measurement definitions. The current target is action E110, completed on September 20 at 10:05.

| Record item | Fixed baseline | Recent baseline |
| --- | --- | --- |
| Baseline version | fixed-v1 | recent-0920-1000 |
| Included period | September 1 after calibration, 09:00 inclusive to 10:00 exclusive | September 20, 09:00 inclusive to 10:00 exclusive |
| Reference value | 100 kPa | 108 kPa |
| Calculation complete and effective | September 1 at 10:00, retained thereafter | September 20 at 10:00, used until the next update |
| Current target excluded | E110 excluded | E110 and records completed at or after 10:00 excluded |
| Comparison recorded at 10:05 | E110: 110−100=+10 kPa | E110: 110−108=+2 kPa |

This assumes all required inputs and aggregation are ready at the boundary time. If calculation finishes later, the baseline is unavailable until then; retain completion time as well as the included period. fixed-v1 answers a question about the post-calibration reference; recent-0920-1000 answers one about the immediately preceding hour. Recording only “recent baseline” loses which period was used.

An update at 11:00 creates a new version. Do not overwrite the comparison made at 10:05 with that new baseline. E110 is excluded from its own reference, but may enter a reference for later targets if it meets predefined inclusion and quality rules. Do not change inclusion rules after the fact merely because an anomaly is inconvenient.

Check the separate example with past values 100 and 100 and current value 130. Past-only averaging gives `(100+100)/2=100` and a difference of +30. Including the current value gives `(100+100+130)/3=110` and a difference of +20. Correct arithmetic and units do not make this comply with “compare against past records excluding the current target.” Using a 10:10 record or the 11:00 baseline version in the 10:05 comparison violates the same timing requirement.


## Fixed and Updating References for Different Comparison Goals {#a-small-diagram}

The key point in this section is not the baseline form by itself, but which maintenance method is made more natural by the `comparison question`. Fixed baselines and recent-usual baselines support different questions better, and the meaning of the comparison sentence changes with that choice.

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-5-mermaid-01-en.mmd"
```

## Checklist

- Did you compare current value 110 with fixed reference 100 and moving reference 108 separately?
- Can you explain why including anomalous periods in the baseline reduces the difference?

## Sources and Further Reading

- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general principle of placing one specific point or period as the comparison reference, it supports the role of a fixed baseline. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- National Cancer Institute, `baseline`. Because it explains baseline as a reference for comparing change over time after an initial measurement is set, it reinforces this section's premise that a baseline is first a reference measurement for comparison. [https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline](https://www.cancer.gov/publications/dictionaries/cancer-terms/def/baseline){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains that a control chart compares the current process characteristic with past performance and that control limits should change only with a valid and compelling reason, it directly supports this section's point that whether to keep or update a baseline should follow the comparison question and the grounds for operational change. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- Hyndman, Athanasopoulos et al., `Forecasting: Principles and Practice (3rd ed)`, `Time series cross-validation`. Because it explains structures such as rolling forecasting origin, where the reference moves forward over time, it serves as an analogous support for the idea that an operating method is possible where the reference range also moves, as with a recent-usual baseline. But because this source belongs to forecast evaluation, this section uses only the higher-level idea of `a moving reference`, and only by analogy. [https://otexts.com/fpp3/tscv.html](https://otexts.com/fpp3/tscv.html){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20

- [NIST EWMA Control Charts](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc324.htm){: target="_blank" rel="noopener noreferrer" }. Checked the distinction between an updating reference that weights past observations and a fixed reference. Checked: 2026-09-15.
