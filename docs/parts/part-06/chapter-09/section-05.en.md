# P6-9.5 Supplement: Constraints in Efficient Adjustment Methods

> Section ID: `P6-9.5`
> Version: `v2026.07.23`

_Subtitle: How adapter, LoRA, and QLoRA split across added structure, small deltas, and memory constraints_

In P6-9.4, we first looked at the name LoRA and the scale intuition of a low-rank adjustment delta. Now we need to distinguish adapter, LoRA, and QLoRA, which often appear together in documents and lectures, without mixing them as the same thing. These names are efficient adjustment choices that split again `after choosing the fine-tuning axis first`.

This Section focuses less on following long formulas and more on reading the names by asking what each tries to reduce among `added structure`, `small delta`, and `memory constraint`.

## Constraints That Split Efficient Adjustment Methods

- At what layer do adapter, LoRA, and QLoRA differ?
- If we know LoRA, can we treat QLoRA as the same thing?
- In which constraint scene should each name come to mind first?

Adjustment methods with similar names should first be separated by constraint scene. If the large difference between fine-tuning and LoRA was `how heavily to adjust the model`, the detailed difference among adapter, LoRA, and QLoRA is closer to `what should be reduced first` among added structure, small delta, and memory constraint. In other words, the question here is not again `will we do fine-tuning?` It is `if we have already chosen the fine-tuning axis, which efficient adjustment name should come to mind in which constraint scene?`

The key point is not `the names are similar`, but `what each method tries to make less heavy`. Data design and operating judgment are separate problems added again on top of this distinction.

## Why This Name Distinction Is Needed After the Selection Map

By P6-8.2, we hold the broad axis that `a way to adapt a large base model more lightly is needed`. By P6-9.3, we have also checked once whether the current problem really should choose the fine-tuning axis first. In P6-9.4, we added the intuition that LoRA's low-rank is attached to small delta representation, not to the whole model size.

But once we start reading real materials, it is easy to become unclear again at `what exactly is that light method?` If adapter, LoRA, and QLoRA appear in the same paragraph, they can easily be received as `a few similar names for new techniques`.

If we read these three as one bundle of names, the later chapters remain confusing. `What to teach` and `how to adjust less heavily` get mixed, scenes that require QLoRA because of memory constraints are passed over with a simple LoRA explanation, and the structural difference between adapter and LoRA can feel like `similar optimization anyway`.

Therefore, this supplementary study is not a list of names that interrupts the main line. It is a cleanup interval that, after the selection map, holds the detailed distinctions needed when we go deeper into the fine-tuning side. Here we distinguish what adapter, LoRA, and QLoRA try to reduce inside the fine-tuning axis. It is the step of separating structural difference, delta learning, and memory constraint into different questions.

In other words, the result to keep here is not `knowing more names`, but `being less confused about which name appears in which constraint scene while reading documents after choosing the fine-tuning side`. Later operating Sections will continue from this distinction when judging which efficient adjustment method is more realistic as operating constraints, cost, memory, and experiment cycles become larger concerns.

## Distinguishing Efficient Adjustment Names and Constraint Scenes

Rather than memorizing three names first, it is safer to first divide whether the current blockage is about `additional module structure`, `small delta learning`, or `memory constraint`.

| Constraint scene seen first | Name to think of first | Why it splits this way |
| --- | --- | --- |
| We want to keep the base model and separately manage task-specific adaptation | Compare adapter or LoRA | Both avoid retraining the whole model heavily, but they place added structure differently. |
| GPU memory is too tight to handle the whole model directly | Check QLoRA first | Not only small delta learning, but also handling the base model in a lighter representation becomes important. |
| We need to compare the balance between cost and expression capacity by changing rank | Detailed LoRA comparison | The bottleneck is likely the balance between delta size and experiment resources, not structural difference. |

If we hold this table first and then read the explanations of adapter, LoRA, and QLoRA below, efficient adjustment methods become easier to understand as `selection standards by constraint scene` rather than `name memorization`.

## How Adapter and LoRA Differ

LoRA and adapter both belong to the flow of `not retraining the whole base model heavily`. But they are not the same method.

| Method | Introductory intuition |
| --- | --- |
| adapter | Adjust by inserting small additional modules between layers |
| LoRA | Learn a small delta added to existing large weights |
| QLoRA | Reduce memory burden further by using quantization together with the LoRA adjustment idea |

What matters in this table is not ranking them, but `the layer where the problem is reduced`.

- adapter is a `structure that inserts additional modules`
- LoRA is a `structure that learns a small delta`
- QLoRA is `LoRA + lighter storage/training conditions`

This is the safer reading.

All three belong to the flow of `not adjusting the whole model from end to end again`, but where they place added structure and what they try to reduce are different. We need to hold this difference first so that experiment cost, memory constraints, and quality comparisons do not get mixed as if they were the same name later.

## Why QLoRA Is Mentioned Together

Readers who learn LoRA soon meet QLoRA. At that point, a question appears: `Are these completely different methods?`

The core point is as follows.

- LoRA is the idea of learning only a small adjustment delta.
- QLoRA is a flow that handles the base model in a lighter representation while adding LoRA adjustment.

So QLoRA is better read not as `a different philosophy that abandons LoRA`, but as `a practical extension that makes LoRA easier to handle under lower-memory conditions`.

It can be summarized in one line as follows.

`LoRA reduces the adjustment target, and QLoRA extends that adjustment so it can be done with less memory.`

## Why This Distinction Matters in Practice

If different choices are mixed under the same word `fine-tuning`, cost judgment becomes blurry.

For example, a team may ask the following.

- Do we have the resources for full fine-tuning?
- Does LoRA balance quality and cost well enough?
- If memory is tighter, do we need a choice such as QLoRA?
- Is structural simplicity more important, or is experiment iteration speed more important?

Understanding LoRA deeply is therefore closer to reading `why these choices appeared` than to memorizing formulas.

## Selection Standards for Efficient Adjustment Methods

The shortest summary so far is as follows.

- adapter is close to `a method that inserts small additional modules`.
- LoRA is close to `a method that learns and attaches a small delta`.
- QLoRA is close to `an extension that makes LoRA adjustment easier under lower-memory conditions`.

We need to distinguish these three so that we do not miss the different cost structures and experiment conditions hidden under the same word `fine-tuning`.

## Cases and Examples

### Case 1. Testing Several Tasks with the Same Base Model

Suppose a team tests customer inquiry classification, document summarization, and internal search assistance with the same base model. In this scene, it is easy to think, `If there are three tasks, don't we need three separate models?` But if we perform full fine-tuning three times with this standard, storage grows and version management becomes complicated. For example, if changing only one classification experiment requires managing a full model copy again, the comparison experiment itself quickly becomes heavy. What blocks the team first here is not theory, but the number of versions and experiment-management cost.

In this situation, the LoRA family keeps the base model as-is and attaches task-specific adjustment deltas separately. This makes it possible to ask `can we manage only the deltas separately?` instead of `do we copy the whole model for each task?` The change here is a move from asking `do we need a full copy for each task?` to asking `is it enough to separate only the task-specific adjustment delta?` The misunderstanding to correct is the feeling that `if tasks increase, whole models must increase proportionally`. The result to check in this case is whether task-specific adjustments can be managed separately on the same base model to actually speed up experiment comparison, and whether the management unit can be reduced from full copies to adjustment copies.

### Case 2. A Memory-Constrained Environment

Handling a whole large base model directly is burdensome on laptop-level equipment or limited GPU environments. In this situation, it is easy to first think, `If we want to adjust it, we have to load and change the whole model anyway.` But with that approach, the experiment may not even start. For example, if the data is ready but GPU memory shortage prevents even the first training step, the experiment is blocked before model selection is discussed. At that point, the team asks, `Can we adapt the model to the purpose without changing everything?`

The reason LoRA and QLoRA are mentioned together is directly connected to this real constraint. The change here is a move from asking `is adjustment possible only if we handle the whole model directly?` to asking `can we start the experiment with only a small adjustment structure?` The misunderstanding to correct is the judgment that `if we cannot load everything, adjustment itself is impossible`. The result to check in this case is whether a small adjustment structure makes real experiment start possible even in an environment where full model modification is blocked, and whether it actually lowers the resource threshold enough for the first step to run.

### Case 3. When Experiment Iteration Matters Before Result Quality

In an early exploration stage, quickly seeing `which data and task definition fits` can matter more than a `perfect final model`. When a performance problem appears, it is easy to first think of training once at large scale to see the best result. But at this stage, it may be more practical to quickly compare which label definition works, whether adjustment is needed more than prompting, and whether data cleaning matters more. For example, if we need to test three task definitions this week but each experiment is too heavy, we cannot run the most important comparison itself.

In this situation, comparing smaller adjustment copies several times can be better than spending a large cost once. The change here is a move from asking `can we obtain the final best score in one shot?` to asking `can we actually compare several hypotheses quickly?` The misunderstanding to correct is the thought that `one best performance result` always means `a good exploration process`. The result to check in this case is whether multiple experiment cycles enable faster task-definition comparison than a final best score, and whether those cycles let the team discard wrong hypotheses earlier.

The three cases can be grouped again as efficient adjustment selection standards.

| Situation | What first grows when touching the whole model | What efficient adjustment first tries to reduce |
| --- | --- | --- |
| Several task experiments with the same base model | Number of model copies and version-management burden | Cost of separately managing only task-specific adjustment copies |
| Memory-constrained environment | Resource burden of entering the first experiment | Whether starting with only a small adjustment structure is possible |
| When experiment iteration matters | Preparation time and storage cost of one experiment | Iteration burden for quickly comparing several hypotheses |

The purpose of this table is not to make us memorize the three technique names again. It leaves the point that even inside the same `fine-tuning` axis, the choice to compare changes depending on whether the first growing burden is copy count, memory, or experiment iteration time.

## Scenes Where Efficient Adjustment Names Split

If we look at practical situations again from the perspective of efficient adjustment, we can practice first dividing whether the current blockage is an `additional module structure problem`, a `small delta problem`, or a `memory constraint problem`, even before knowing low-rank formulas or quantization details. If we want to keep the base model and separately manage task-specific adaptation, we should not treat adapter and LoRA as the same thing. We should compare whether we need a structure that inserts small modules between layers or a structure that attaches small deltas to existing weights. If GPU memory is too tight to handle the whole model directly, we should not assume that LoRA automatically solves the memory problem, but should check whether the base model also needs to be handled in a lighter representation. If the balance between cost and expression capacity becomes confusing while comparing rank candidates, we should ask whether the current bottleneck is resource constraint or insufficient room for expression, rather than assuming smaller rank is always better.

The important point is not to memorize three names. It is to first read `where added structure is placed`, `what scale is being reduced`, and `whether memory constraints must be reduced too` as different questions.

Common confusions here include the following.

- adapter, LoRA, and QLoRA can all feel like different names for the same efficient adjustment.
- If we know LoRA, it is easy to miss why QLoRA is separately needed.
- It is easy not to separate rank comparison into a quality-confirmation problem and an exploration-cost problem.

Therefore, the closing standard to keep is `do not bundle similar names as the same word; choose again by constraint scene`.

## Exercise

For each scene below, choose which of `adapter`, `LoRA`, `QLoRA`, and `full fine-tuning` to check first, and write the reason in one sentence.

1. Customer classification, summarization, and search assistance must be tested in parallel with the same base model, but storage and version management are the first burden.
2. The first experiment must run on one GPU of 24GB or less, and full model modification is burdensome from the start.
3. Before final deployment, comparing three task definitions within this week matters more than reaching the highest performance score.
4. Performance in a specific domain is absolutely important, and there are enough resources and time to accept full model readjustment.

## Checklist

- You should be able to first say which is the current bottleneck among memory, copy count, and experiment iterations.
- You should be able to distinguish adapter, LoRA, and QLoRA by the axes of `additional module`, `small delta`, and `lower-memory condition`.
- You should be able to choose similar-looking efficient adjustment names again by constraint scene, without bundling them as the same thing.

## Sources and References

- Neil Houlsby et al., [Parameter-Efficient Transfer Learning for NLP](https://proceedings.mlr.press/v97/houlsby19a.html){: target="_blank" rel="noopener noreferrer" }, ICML, 2019, accessed 2026-07-19.
- Edward J. Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685){: target="_blank" rel="noopener noreferrer" }, arXiv, 2021, accessed 2026-07-19.
- Tim Dettmers et al., [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314){: target="_blank" rel="noopener noreferrer" }, arXiv, 2023, accessed 2026-07-19.
