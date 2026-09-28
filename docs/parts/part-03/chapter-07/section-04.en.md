# P3-7.4 By What Range and Conditions Should We Set the Baseline

> Section ID: `P3-7.4`
> Version: `v2026.09.20`

A baseline is not constructed by choosing past values that resemble the current result. **Define the comparison question first, specify which conditions must match and which may differ, then select candidates.** More records or more recent dates alone do not make a reference appropriate.

## Compare Three Candidates Without Seeing Their Results

Consider a fictional machine M1 maintained on September 18, performing type-A actions in standard mode. Recent data consists of twenty actions completed on September 20. The feature is per-action late mean flow in L/min, averaged with equal weight per action. Candidate means are deliberately omitted.

| Candidate | Period and operating state | Conditions | Measurement definition | Count |
| --- | --- | --- | --- | ---: |
| P | September 19, after maintenance | M1, type-A, standard mode | Same sensor location, calibration, late segment, and missing-data rules as recent data | 3 |
| Q | September 1–17, before maintenance | M1, type-A, standard mode | Confirmed to match the recent measurement definition | 200 |
| R | September 19, after maintenance | M1, type-B, high-load mode | Same units, but a different late-segment duration | 200 |

If maintenance changed measurement location or calibration, Q's matching-definition assumption must be checked again. Identical L/min units are insufficient. All three candidate periods also precede the recent period.

## Separate Post-Maintenance Monitoring from Before–After Comparison

The first question is “Has recent type-A standard-mode operation changed from earlier post-maintenance operation?” P is a provisional candidate matching this question. Q represents the pre-maintenance state, and R differs in process, load, and segment definition. **P's three records are not inherently wrong; they provide limited evidence for what is usual after maintenance.**

If P is used, report “twenty recent actions compared with three post-maintenance actions,” with the limitation. Those three may be coincidentally similar or concentrated in particular conditions; do not call them an established stable norm. Without grounds for broadening conditions, collect more data or defer fixing the baseline rather than silently mixing Q and R. This does not defer responses required by existing operating limits.

The second question is “How do observed values differ before and after maintenance?” Now Q is an intentional candidate. The pre-maintenance difference is central to the question; requiring it to match would remove the comparison of interest. Twenty recent actions can be compared with two hundred earlier ones, while checking other changes in process, load, measurement definitions, and observation scope.

A calculated before–after difference is not automatically a causal maintenance effect. Changes in materials, workload, or environment may contribute. Record an observed before–after difference separately from a claim that maintenance caused it.

| Comparison question | Candidate to consider | Limitation to retain |
| --- | --- | --- |
| Post-maintenance monitoring | P | Whether three records represent usual post-maintenance operation is unresolved |
| Before–after comparison | Q | Check other condition changes; causal effect is unestablished |
| Type-A versus type-B comparison | R may be considered as a separate group | State that the question changed to a between-group comparison |

## Equal Counts or Nearby Dates Are Not Selection Rules

Twenty recent and two hundred reference actions need not have equal counts. Match sample units and averaging rules, and report both counts. Two hundred records concentrated on one date or source process may not represent broader conditions. Three records are not worthless for every purpose either. This table cannot establish one universal sufficient sample count.

If selecting the “closest candidate,” explain the meaning of closeness. R's nearby date does not make it match the original type-A question. Selecting a candidate because its mean resembles the current mean can remove the difference being investigated. Record the question, inclusion criteria, period, aggregation method, and exclusion reasons before examining results.

## Record Selection Reasons and Remaining Uncertainty {#looking-through-a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-07/p3-7-4-mermaid-01-en.mmd"
```

Correct choosing Q for post-maintenance monitoring because “two hundred records make it reliable.” The answer is: “It has more records but represents the pre-maintenance state, which does not match the post-maintenance reference question. Use P provisionally with its three-record limitation, or collect more post-maintenance data.”

Suppose you later learn that P's mean differs from the current mean while R's resembles it. May that alone justify switching to R? No. Using R requires an explicit new question and design that accommodate process and load differences. Selection fixes the meaning of the comparison population; it is not a procedure for producing a preferred difference.

## Checklist

- Did you define the question and inclusion criteria before seeing results?
- Can you explain P/Q/R selection or exclusion through period, conditions, and measurement definitions?
- Can you distinguish monitoring after maintenance from comparing before and after?
- Did you record small-sample uncertainty and representativeness limits of larger samples?

## Sources and Further Reading

- NIST/SEMATECH e-Handbook of Statistical Methods, `What are Variables Control Charts?`. Because it explains that samples obtained under the same essential conditions are needed, it reinforces the standard in this section that only baseline candidates with the same sample unit and operating conditions should remain. [https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc32.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
- U.S. Bureau of Labor Statistics, `Base period`. Because it provides the general definition of a reference period used for comparison, it supports the explanation that baseline candidates should also be chosen not as just any past range, but as a comparable reference period. [https://www.bls.gov/bls/glossary.htm](https://www.bls.gov/bls/glossary.htm){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
