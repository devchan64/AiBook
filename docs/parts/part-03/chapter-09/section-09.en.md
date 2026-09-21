# P3-9.9 How Do We Distinguish the Actual Target from a Proxy Target

> Section ID: `P3-9.9`
> Version: `v2026.09.20`

[P3-9.8](section-08.en.md) separated model scores from review-assignment policies. We must also check whether the value a model predicts well is the outcome we actually want to know. Even if a model was intended to reduce failures, training it against review requests directly teaches it to predict requests, not failures themselves. A column used in place of the desired outcome is a [proxy target](/AiBook/en/reference/concept-glossary-alpha/p/#glossary-proxy-target).

## Separate Failure Reduction, Failure Prediction, and Review Requests

| Level | Question in this example | Required records |
| --- | --- | --- |
| Ultimate purpose | We want fewer failures in operation | Actual failures, operating conditions, interventions, and comparison evidence |
| Outcome we want to predict directly | Will a failure occur within seven days of prediction? | Failure and maintenance records with an explicit observation window |
| Currently observable proxy | Did a person request additional review? | Request decision, reviewer, time, and judgment criteria |

“Reduce failures” is an operational objective; `failure_within_7d` is the outcome column to predict. `review_requested` is an intermediate human judgment. A request does not confirm failure, and no request does not confirm absence of failure. Combining these questions under one name obscures what the model does well.

## Revisit the Same Three Subjects When Outcomes Arrive

The following fictional equipment IDs A, B, and C are local to this section. Each sample describes one piece of equipment at `2026-09-01 10:00 KST`, using only inputs available then. We are considering review requests recorded at 10:20 that day as proxy labels. `review_requested=1` means a request was made; 0 means the reviewer completed this decision and explicitly recorded no request. Missing records or unreviewed cases do not become 0.

The desired outcome follows `failure-v1` in [P3-9.7](section-07.en.md): an equipment fault prevented completion of a scheduled operation, with its cause confirmed in maintenance records; planned stops are excluded. The outcome window is **at or after September 1 at 10:00 and before September 8 at 10:00**. Initially, outcomes for this window are unconfirmed for all three subjects.

| Equipment | `review_requested` at September 1, 10:20 | Subsequently confirmed `failure_within_7d` | Confirmed course of events |
| --- | ---: | ---: | --- |
| A | 1 | 0 | Settings adjusted September 1 at 10:30; full-window follow-up confirms no failure |
| B | 0 | 1 | No separate intervention; failure on September 4 confirmed through maintenance |
| C | 1 | 1 | No separate intervention; failure on September 5 confirmed through maintenance |

Assume the outcome column was joined at September 8, 11:00, with no gaps in observation or confirmation for these three pieces of equipment in this teaching example. Following only A and C, which received requests, would have missed B's failure. Assessing the proxy requires follow-up outcomes for subjects with and without requests.

A had a request but no observed failure; B had no request but did fail. A's 0 alone does not prove the request was unnecessary. The table lacks the outcome without the adjustment, so this case alone cannot establish that the adjustment prevented failure either. This is the distinction between observed outcomes and intervention effects discussed in [P3-8.7](../chapter-08/section-07.en.md).

## Predicting Every Proxy Label Does Not Mean Predicting Every Failure

Suppose a hypothetical model correctly predicts all three request labels: 1, 0, 1. Its accuracy against requests is `3 / 3 = 100%`. If we simply rename those outputs failure predictions, only C matches the actual outcomes 0, 1, 1, giving `1 / 3 ≈ 33.3%`.

This is a three-row counterexample, not a model-performance estimate or a general rate. It shows that what an evaluation means depends on the answer used for comparison, even with unchanged outputs. Accurate failure prediction and reducing failures through interventions are also different achievements, so request-prediction scores alone cannot demonstrate failure reduction.

If predicting review workload or assigning reviewers is the direct purpose, `review_requested` can be the proper target for that task. It is a proxy when used in place of failures. Earlier availability alone does not make it an appropriate substitute.

## Connecting Observable Proxies to the Actual Target {#a-small-diagram}

```mermaid
--8<-- "assets/part-03/chapter-09/p3-9-9-mermaid-01-en.mmd"
```

The connections represent questions and their supporting records, not a causal claim that requests produce failures. When follow-up outcomes arrive, preserve original request labels and join a separate failure-outcome column by equipment ID and prediction time. Retain both the request criteria and the failure definition.

## Turn “Proxy Limitations” into Records to Check

| Handoff note | What to record in this example |
| --- | --- |
| `business_goal` | Reduce failures in operation |
| Outcome to predict directly | `failure_within_7d`, `failure-v1`, seven days including the start but excluding the end |
| `proxy_target` and `proxy_reason` | `review_requested`; requests are available earlier while failure outcomes remain unconfirmed |
| `proxy_gap` | A has request 1 and failure 0; B has request 0 and failure 1. Request criteria and interventions may affect the relationship |
| Additional records to check | Failure and maintenance records for both request groups, observation completion, intervention types and times, request-criteria version |
| `review_owner` | Assign someone to compare request criteria and follow-up outcomes; fill in their name and role for an actual handoff |

If a rule creates label 1 when an input's decline rate crosses a threshold, a model learning that label from those inputs primarily reproduces the rule. First consider whether the rule can be applied directly. High rule-reproduction scores do not support failure prediction without independently confirmed failure records.

Exercise: If follow-up failure records for B, whose request label is 0, have not yet arrived, may we fill its failure outcome with 0? May we report “all failures predicted” because the model correctly predicted every request?

Answer: Keep B's failure outcome unconfirmed. Request 0 does not substitute for failure 0. We can currently report how well request labels were predicted; evaluating failure prediction requires independently confirmed follow-up outcomes regardless of request status. [P3-9.10](section-10.en.md) continues with late-arriving outcomes and incomplete observation.

## Checklist

- Can you write the ultimate purpose, the outcome to predict directly, and the proxy column currently being learned separately?
- Can you explain why the same 1, 0, 1 matches requests on 3/3 rows but failures on only 1/3?
- Can you identify follow-up outcome and intervention records for checking the proxy, without turning unconfirmed outcomes into 0?

## Sources and References

- Google, *Machine Learning Glossary*, `label`, `derived label`, `proxy labels`. Used to check the term basis that a supervised-learning label is the answer or result part of an example, and that proxy labels should be chosen carefully when an actual label is absent. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-20
