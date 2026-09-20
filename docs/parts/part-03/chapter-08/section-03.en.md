# P3-8.3 In What Order and Wording Should Conservative Interpretations Be Written?

> Section ID: `P3-8.3`
> Version: `v2026.09.20`

“An anomaly is suspected; review is needed” does not tell readers what was compared or what to check. Conservative writing does not blur observed numbers. It states the established [comparison result](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure) precisely and separates what remains unknown from the next checking action.

## Extract the information needed from one comparison row

Take type-A from the fictional aggregate in [P3-7.2](../chapter-07/section-02.en.md): 200 past baseline operations and 20 recent completed operations. We retain the assumptions of matching type, operating conditions, and measurement definitions, with all required measurements available. These are summary values for a writing exercise, not results calculated from actual raw logs.

| Information to include | Value and meaning for type-A |
| --- | --- |
| Comparison population | 200 past and 20 recent operations under matching conditions |
| Late-period mean difference | Recent 2.2−baseline 2.8=−0.6 L/min |
| Between-operation spread | Standard deviation of per-operation late-period means: 0.2→0.4 L/min |
| Within-operation decline | Late-period mean−early-period mean ≤ −0.30 L/min in 14/20 operations, or 70% |

The overall mean weights each operation's late-period mean equally. The decline rule includes the boundary and counts each operation once. “The mean is 0.6 lower” and “14 operations met the rule” are different observations; neither should be substituted for the other.

## Write observations, uncertainty, and checking actions separately

There is no need to squeeze all conditions into one sentence. Separating the report into three parts makes each role easier to check.

1. **Observation:** Compared with 200 past operations under matching conditions, the late-period mean for 20 recent type-A operations was 0.6 L/min lower, from 2.8 to 2.2 L/min; the standard deviation of per-operation late-period means rose from 0.2 to 0.4 L/min. Fourteen of the 20 operations met the within-operation decline rule.
2. **Uncertainty:** This aggregate lacks occurrence order and the baseline decline count, so it cannot establish consecutive declines or an increased decline proportion; the cause is also unverified.
3. **Checking action:** The reviewer will compare time-ordered raw records for the 20 recent operations with per-operation setting histories and check the baseline decline count calculated using the same rule.

The first part uses two sentences for readability. What matters is separating the three roles, not the number of sentences. “Will check” describes work to do, not a report that checking is complete. In an actual report, add comparison periods, equipment, baseline version, and raw-record location so another person can find the same evidence. Do not invent dates or versions missing from this fictional table.

## Restore missing evidence instead of merely changing adjectives

| Wording to revise | Revised wording | Reason |
| --- | --- | --- |
| Flow has deteriorated sharply | The late-period mean for 20 recent operations was 0.6 L/min below that of 200 baseline operations | Preserves population, counts, and units without adding a deterioration judgment |
| Seventy percent of recent operations failed | Fourteen of 20 recent operations met the defined within-operation decline rule | Separates meeting a rule from a failure diagnosis |
| Decline may have continued consecutively | Fourteen operations met the rule; their occurrence order is unverified | Adding “may” does not supply evidence of consecutiveness |
| Further checking is needed | Compare time-ordered raw records for the 20 recent operations with setting histories | Specifies what to inspect and what to do |

“Suspected” and “possible” do not replace evidence. In particular, “sensor failure is possible” can focus attention on one cause without explaining why that candidate was selected. When proposing a candidate, include its basis and records that would help distinguish it. The example in [P3-8.2](section-02.en.md) shows how to examine candidates.

## Separate small-sample limitations from necessary action

Type-B in the same P3-7.2 example has three recent operations and 200 baseline operations. Its late-period mean fell from 2.8 to 1.9 L/min, and one recent operation met the decline rule. Instead of “only three operations, so postpone action,” write:

> The late-period mean for three recent type-B operations was 0.9 L/min below that of 200 baseline operations, and 1/3 operations met the decline rule. Three observations provide limited evidence for a persistent state change or its cause. Check the three operations' original measurements and separately established limits and response procedures immediately.

The last sentence neither reports a verified limit violation nor orders an automatic shutdown. It calls for checking whether a violation occurred and applying the existing procedure accordingly. The table supplies no allowable limits, so it does not establish a new warning grade. **Limited evidence of persistence** can coexist with **performing necessary checks**.

## Connecting Observations, Comparisons, and Limits in an Interpretation {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-3-mermaid-01-en.mmd"
```

This sequence is a writing framework for communicating an evidence assessment. It does not automatically choose “observe only” or “strong warning” from the sample count.

## Write your own version

Revise this report about type-A: “Twenty operations are sufficient and 70% failed consecutively, so replace the sensor.” Include the comparison difference, operation counts, and rule count, then separately state what is unverified and which records to inspect next.

Example answer: “Against 200 past operations under matching conditions, the late-period mean for 20 recent type-A operations was 0.6 L/min lower, and 14/20 operations met the decline rule. Twenty operations alone do not guarantee representativeness; occurrence order, whether any failure occurred, and the cause remain unverified. Compare time-ordered raw operation records with setting histories and check additional measurement records needed to assess sensor condition.” This removes the unsupported consecutive-failure claim and sensor-replacement decision while retaining checking work.

## Checklist

- Have you included comparison populations, counts, units, and the rule count?
- Have you expressed uncertainty as specific missing information rather than vague qualifiers?
- Have you named records and checking tasks without postponing necessary action solely because the sample is small?

## Sources and references

- [W3C, PROV-Overview](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } — Reference for recording entities, activities, agents, and the provenance of data. The observation–uncertainty–checking-action framework is this book's educational construction, not a W3C reporting-sentence rule. Accessed: 2026-09-20.
