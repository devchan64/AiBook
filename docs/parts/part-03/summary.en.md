# Part 3 Summary

> Section ID: `P3-summary`
> Version: `v2026.09.20`

In Part 3, [data modeling](/AiBook/en/reference/concept-glossary-alpha/d/#data-modeling) meant deciding how recorded data should represent inputs and outcomes for a question. Source records are already a dataset, but having columns does not make them suitable for comparison or learning. Check their meaning and coverage, choose a sample unit, and decide what information to retain.

Summarizing sensor records for one automated operation into a row changes what the model can see. A mean shows the overall level but loses order. A difference from a baseline shows change without establishing its cause. If review requests are the answers, the model primarily learns requests, which are not the same as actual failures.

## Choices Connecting Records to Questions

| Choice | Question to revisit | Evidence to retain |
| --- | --- | --- |
| Record meaning | What are the units, measurement conditions, and meaning of one row? | Source IDs, equipment, operations, times, units, and conditions |
| Coverage and quality | Which periods and subjects were observed, and what is missing? | Coverage, treatment of missing, duplicate, or anomalous records, and exclusion reasons |
| Sample boundaries | Is a sample one operation or a window combining operations? | Start and end rules and source-record links |
| Representation | Which features were calculated, and which details or ordering were lost? | Formulas, units, input windows, and preserved source data |
| Comparison and interpretation | What is compared, and what can the observed difference establish? | Baseline period, conditions, version, counts, and unconfirmed causes |
| Target and timing | Do we need a description of change, review selection, or a future outcome prediction? | Outputs, policies, outcome definitions, observation windows, and confirmation states |

These choices are not mandatory steps toward a predictive model. A comparison report or review queue may meet the purpose. When a model is needed, separate inputs available at prediction time from outcomes confirmed later and define evaluation around the intended subjects.

## Choose Ten Reviews with a One-Page Design Note

Exercise: Complete the note below for “choose up to ten recently completed operations to review first.” For two features, state the selection reason, formula, unit, and interpretation limit. Distinguish assigning review from actually completing it.

| Note item | What to write |
| --- | --- |
| Records and coverage | Operation IDs, start and end times, units and operating conditions, candidate period, and complete operation roster |
| Quality and missingness | Missing or duplicate records and treatment evidence; retain IDs and exclusion reasons even for operations that cannot be calculated |
| Samples and representation | One operation per candidate, two features, information lost through summary, and source links |
| Comparison reference | Baseline period and version under matching conditions and feature definitions; check for inclusion of the compared subject or future data |
| Review policy | Sort key, tie rule, scope of the maximum ten selections, and nonselection reasons |
| Output and limits | Rank, features, evidence, and selection status; join actual review results separately. Failure causes and probabilities remain unconfirmed |

For a numerical example, suppose one operation has equally spaced flow readings in time order: `2.5, 2.7, 2.1, 2.3 L/min`. Assume complete measurements under the same conditions for this teaching example. Define the first two readings as the early part and the last two as the late part.

| Chosen feature | Calculation and value | Reason and limitation |
| --- | --- | --- |
| Mean operation flow | `(2.5 + 2.7 + 2.1 + 2.3) / 4 = 2.4 L/min` | Compares overall level; loses ordering and momentary variation |
| Late mean minus early mean | `(2.1 + 2.3) / 2 − (2.5 + 2.7) / 2 = 2.2 − 2.6 = -0.4 L/min` | Compares earlier and later parts; does not give exact change timing, cause, or change per unit time |

If baseline mean flow is 2.8 L/min under matching conditions and calculation definitions, this operation's mean difference is `2.4 − 2.8 = -0.4 L/min`. The late-minus-early value is also -0.4, but the comparison subjects differ: two parts within an operation versus this operation and its baseline. Equal numbers do not make them the same feature.

One possible answer is “assign up to ten by descending absolute difference from baseline mean, breaking ties by ascending operation ID.” This rule retains late-minus-early difference as explanatory evidence without using it to sort. Distinguish uncomputable operations from those waiting because of capacity; neither becomes normal. These values and rules are educational, not actual safety limits.

## Change the Question to Failure Within Seven Days

A review queue can use comparison rules, but learning failure prediction also requires an outcome definition and confirmation evidence. Collecting answers only for selected queue entries may leave outcomes for unselected subjects unknown.

| Additional item | Minimum content |
| --- | --- |
| Prediction subject and time | Equipment ID paired with prediction time; state whether the unit changes from operation candidate to equipment and time |
| Actually available inputs | Source arrival and calculation completion for every feature; exclude later arrivals and future baselines |
| Outcome definition and window | For example, `failure-v1`, failure from 2026-09-01 10:00 KST inclusive to September 8, 10:00 KST exclusive |
| Confirmed and unconfirmed outcomes | 1 for confirmed failure in the window; 0 for no failure after full follow-up and record checks; incomplete or pending outcomes retain separate status |
| Evaluation and open checks | Existing equipment's future or unseen equipment, confirmed-outcome coverage, interventions, error costs, and review capacity |

See [P3-9.7](chapter-09/section-07.en.md) for the concrete `failure-v1` definition and input example, [P3-9.10](chapter-09/section-10.en.md) for pending outcomes and confirmation timing, and [P3-9.13](chapter-09/section-13.en.md) for the handoff memo. Do not substitute review need or rule satisfaction for actual failure, or fill unconfirmed outcomes with 0; these distinctions separate the two questions.

## Apply the Same Questions to Documents

Short exercise: Treat one document paragraph as a sample for “Does this paragraph contain the answer to a question?” If only one sentence is retained, what disappears, and which source records should accompany it?

Answer: A sentence's subject or conditions may depend on the title and surrounding paragraphs. Link document ID, version, paragraph location, and required context, and flag pages missing from collection or portions that could not be read. Unread portions do not mean “no answer.” Just as sensor means remove order, sentence extraction reduces context; check whether the information needed by the question remains.

## What to Bring to Part 4

Part 4 examines what models learn from these inputs and outcomes and how they are evaluated. Bring data files, sample and feature and outcome definitions, source and version links, historical availability, comparison and selection rules, and unresolved checks. Separate verified evidence from open questions so subsequent learning inherits the limitations of the available data.

## Checklist

- Can you trace one sample to source records and explain coverage, missingness, and exclusions?
- Can you explain two features' calculations, units, reasons, and information lost through summary?
- Can you distinguish within-operation and baseline differences even when both equal -0.4?
- Can you state how outcome, timing, and evaluation requirements differ between review selection and future failure prediction?

## Sources and Further Reading

- National Academies of Sciences, Engineering, and Medicine, *Data Science for Undergraduates: Opportunities and Options*, 2018. Because it presents data collection, cleaning, representation, modeling, and interpretation as one connected flow, it supports the perspective of this page that ties the Part 3 wrap-up to a summary of `rebuilding data-science problem structure`. [https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options](https://nap.nationalacademies.org/catalog/25104/data-science-for-undergraduates-opportunities-and-options){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- Google for Developers, `Machine Learning Glossary`. Because it provides term distinctions such as feature, label, label leakage, and example, it supports the minimum premise of Part 3 that features and result candidates must not be mixed and that input/output boundaries must be confirmed. [https://developers.google.com/machine-learning/glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
- W3C, `PROV-Overview`. Because it treats derivation and reproducibility together, it supports the summary judgment that the comparison structures and feature definitions left behind at the end of Part 3 must remain reproducible later under the same rules. [https://www.w3.org/TR/prov-overview/](https://www.w3.org/TR/prov-overview/){: target="_blank" rel="noopener noreferrer" } / Accessed: 2026-07-08
