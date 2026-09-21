# P3-8.5 How Do Multiple Comparison Columns Become a Review Priority?

> Section ID: `P3-8.5`
> Version: `v2026.09.20`

A table with many columns does not require combining every column into one score. When creating a [review queue](/AiBook/en/reference/concept-glossary-alpha/o/#output-structure), distinguish columns that determine order from columns retained to explain evidence. The same data can produce different orders under different sorting policies. Priority is a policy result, not an automatic property of an observation.

## Define one row and every input column

The following fictional data describe three comparison windows already selected for review. Each row represents a **comparison window** containing multiple completed operations, not one operation; its identifier is therefore `window_id`. A, B, and C are local identifiers, not continuations of the same letters in the preceding section. Here we determine order among selected candidates, not admission to review.

| Input column | Meaning in this example |
| --- | --- |
| window_id | Unique identifier of a comparison window |
| diff_mean | Recent average of per-operation late-period means minus the corresponding baseline average, in L/min |
| recent_count | Number of distinct completed operations in the recent window |
| decline_count | Recent operations with late-period mean−early-period mean ≤ −0.30 L/min; equality included, each operation counted once |
| safety_related | yes if the item belongs to a safety-related category in a predefined process-review classification; otherwise no |

The decline condition matches [P3-7.2](../chapter-07/section-02.en.md). `safety_related` comes from process-classification records, not the difference or sample count. `yes` does not mean an incident or limit violation has occurred, and `no` does not guarantee safety. This sorting exercise does not replace separate emergency response procedures when they apply.

Assume required measurements and classification flags are available, each baseline and recent group matches in measurement definitions and operating conditions, and all differences are comparable in the same flow unit. Do not fill a missing safety classification with no or sort differences expressed in incompatible units.

## Read differences alongside rule-satisfaction counts {#looking-at-the-comparison-table-first}

| window_id | diff_mean (L/min) | recent_count | decline_count | safety_related |
| --- | ---: | ---: | ---: | --- |
| A | -0.35 | 20 | 14 | yes |
| B | -0.35 | 3 | 1 | no |
| C | -0.18 | 18 | 12 | yes |

Calculate the decline proportion as `decline_count/recent_count`: A is `14/20=70%`, B is `1/3≈33.3%`, and C is `12/18≈66.7%`. These values replace an undefined repetition score, but they contain no occurrence order and must not be read as consecutive-decline counts.

Difference magnitude is the absolute value, ignoring the sign. For A and B, `|−0.35|=0.35`; for C, `|−0.18|=0.18 L/min`. Retain the original sign because absolute values discard increase versus decrease. This policy treats magnitudes in both directions equally; detecting decreases specifically would require a direction-aware rule.

Neither 20 or 18 observations nor a small spread certifies “high confidence.” Coverage, dependence between operations, and baseline suitability need separate checks. B's small sample does not automatically assign it last place either.

## Policy 1: safety category, difference magnitude, then ID

The fictional policy `queue-v1` uses the following order. Once an earlier criterion decides the order, a later criterion cannot overturn it.

1. Put windows with `safety_related=yes` before those with no.
2. Within the same category, put larger absolute `diff_mean` values first.
3. If both values tie, use ascending alphabetical `window_id` order.

First separate A and C into the yes group and B into the no group. Within yes, `0.35 > 0.18`, so A precedes C. The result is **A → C → B**. C precedes B because of the first classification rule, not because of higher failure probability or a larger sample.

## Policy 2: difference magnitude, then ID

The alternative fictional policy `queue-v2` uses only **absolute difference descending → ID ascending**. Safety category is not a sorting criterion in this policy. A and B tie at 0.35, so ID puts A first; C follows at 0.18. The result is **A → B → C**. These policies illustrate calculations; the example does not establish which is more suitable for actual operations.

| window_id | queue-v1 rank | queue-v2 rank | Decisive reason |
| --- | ---: | ---: | --- |
| A | 1 | 1 | v1: larger difference within yes; v2: ID breaks its tie with B |
| B | 3 | 2 | v1: no group; v2: larger difference than C |
| C | 2 | 3 | v1: yes group; v2: smallest difference |

Neither policy **uses the decline proportion or recent count for sorting**. Retain those columns to explain observations and interpretive limitations. Spread and pattern summaries are also absent from these ranking rules. Saying “A ranks first because repetition is high” would therefore give a reason the rules did not use. To change order using those columns, specify their precedence and tie handling in a new policy.

## Connecting Comparison Evidence to Review Priority {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-08/p3-8-5-mermaid-01-en.mmd"
```

Store `window_id`, `rank`, and `policy_version` in the output and link them to the input row used. Rank 1 means review first within this candidate set, not failure probability 1 or a confirmed diagnosis. The ID tie-breaker ensures consistent ordering; the name A is not itself stronger evidence of importance.

## Change the order yourself

What happens under each policy if only B's `diff_mean` changes to −0.40? Then return to the original table and change only C's `decline_count` from 12 to 18: do the ranks change?

Explanation: In the first change, queue-v1 still gives **A → C → B** because safety category comes first. Queue-v2 gives **B → A → C** because difference magnitude comes first. In the second change, only C's decline proportion becomes `18/18=100%`. Neither policy uses that proportion, so they retain the original orders **A → C → B** and **A → B → C**. Again, 100% is not a failure probability.

## Checklist

- Can you explain the row unit, every input column, and the numerator and denominator of the decline proportion?
- Can you reproduce both policies and their tie-breaks without citing unused columns as ranking reasons?
- Can you distinguish rank from failure probability and retain the policy version and input evidence?

## Sources and references

- [Python documentation, Sorting Techniques](https://docs.python.org/3/howto/sorting.html){: target="_blank" rel="noopener noreferrer" } — Reference for comparing multiple sorting keys in order and using the next key when earlier keys tie. The data and two operational policies are fictional examples constructed for this book. Accessed: 2026-09-20.
