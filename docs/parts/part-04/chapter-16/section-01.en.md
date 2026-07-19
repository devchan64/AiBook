# P4-16.1 Gradient Boosting

> Section ID: `P4-16.1`
> Version: `v2026.07.19`

The random forest in P4-15 was an ensemble that built many trees `in parallel` and reduced instability by gathering their results.

At this point, a different question appears with gradient boosting: instead of stopping at gathering many trees, can the next tree directly correct the error left by the previous stage?

Gradient boosting is an ensemble method that stacks small trees so that the next stage reduces the error left by the previous stage in sequence.

If random forest is closer to `gathering many opinions in parallel`, gradient boosting is closer to `having the next stage fix the previous stage's error`.

This Section explains the basic meanings of `gradient boosting`, `residual`, `weak learner`, and `additive model`. The later Sections continue the current line of judgment from those handles, and the basic sense of sequentially correcting error reconnects through this Section and the [concept glossary](/AiBook/reference/concept-glossary/).

## Scope Of This Section

This Section answers the following questions.

- Why is gradient boosting called `sequential`?
- What do `weak learner`, `residual`, and `additive model` mean?
- How is the mindset of gradient boosting different from that of random forest?
- Why should `n_estimators` and `learning_rate` be read together?

This Section focuses on understanding `what kind of approach boosting is`. Performance and risk, and the roles of early stopping and shrinkage, continue in P4-16.2. The wider view of hyperparameters and validation cost reconnects in P4-9.1 and P4-9.2. Implementation differences among XGBoost, LightGBM, and CatBoost also continue in P4-16.2 at the level of `what they try to make faster and what they try to make safer to handle`, and if a wider implementation comparison becomes necessary, it can be recovered separately as supplementary learning for this chapter.

## Goals Of This Section

- You can explain gradient boosting as `an ensemble that reduces error sequentially`.
- You can explain why weak learners are usually described through small trees.
- You can explain residual as `the part the previous stage still failed to explain`.
- You can explain why `learning_rate` and `n_estimators` should be read together.

## Why This Section Is Needed

Right after readers understand random forest, they can easily think:

- I understand gathering many trees.
- Then are all ensembles roughly the same?

But a major difference opens here.

| Question | Random Forest | Gradient Boosting |
| --- | --- | --- |
| How are the trees created? | many trees are made differently and read together | the next tree receives the error of the earlier tree |
| Core purpose | variance reduction and stability | bias reduction and error correction |
| Learning flow | parallel | sequential |

So 16.1 is the Section that distinguishes the completely different learning philosophy hidden behind the common point `using many trees`.

## What Large Frame Is Boosting?

The scikit-learn User Guide explains boosting as a representative ensemble method that combines weak learners sequentially to build a stronger predictor. Inside that family, gradient boosting generalizes the idea to differentiable loss functions.

`Instead of building one big perfect model from the beginning, add small models one after another and reduce what is still wrong.`

Gradient boosting is easier to understand as `a model that gets closer by repeated fixes` than as `a model that guesses the full answer at once`.

## Why Is It Called Sequential?

The scikit-learn documentation explains gradient-boosted trees as a way of stacking trees sequentially. The tree at each stage is added based on the prediction result of the earlier stage.

That is the biggest difference from random forest.

- In random forest, tree 1 does not directly know the mistake of tree 2.
- In gradient boosting, stage 2 enters after seeing the error left by stage 1.

Gradient boosting is sequential because `the next stage knows the earlier stage`.

## Read It In One Scene

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-1-mermaid-01-en.mmd"
```

The key point in this diagram is that the new tree does not solve the whole problem again from the beginning. It adds a small correction fitted to the residual left by the current prediction. The dotted arrow shows the repeated structure: after one correction is added, the remaining error is calculated again.

## What Is Residual?

In a regression context, residual can usually be read as:

`actual value - current prediction`

For example, if the actual value is `120` and the current model predicts `100`, the residual is `20`. If the actual value is `80` and the current model predicts `95`, the residual is `-15`.

More important than the formula is the following intuition.

`Residual is the part that the model still failed to explain.`

Gradient boosting keeps trying to reduce exactly that remaining part.

The same idea can be compressed again into a short table.

| Current scene | Meaning of the residual |
| --- | --- |
| the prediction is lower than the actual value | some upward correction is still needed |
| the prediction is higher than the actual value | some downward correction is still needed |
| the residual is small | the current stage already explained a large part |
| the residual keeps remaining in the same direction | some pattern is still being missed by the current rules |

So residual is not only a mark that says `the model was wrong`. It is also a signal that tells the next stage `where to enter to correct`.

## What Does Additive Model Mean?

The scikit-learn documentation explains the gradient boosting regressor as an additive model. That means the final prediction is made by adding the outputs of stage models together.

1. Start from a very simple base prediction.
2. Let the next tree create a small correction.
3. Add that correction to the current prediction.
4. Look again at the remaining error.
5. Repeat the process.

Compressed into one sentence: gradient boosting is `the accumulation of small corrections`.

What matters here is not only the fact that `many trees are used`, but that `each stage adds a small fix on top of the previous answer`. So the final prediction in gradient boosting is not `choose one among many independent opinions`. It is closer to `existing answer + new correction + next correction + ...`.

A tiny number table makes this clearer.

| Stage | Current prediction | Correction added at this stage | Updated prediction |
| --- | --- | --- | --- |
| initial value | 100 | - | 100 |
| stage 1 | 100 | +4 | 104 |
| stage 2 | 104 | -2 | 102 |
| stage 3 | 102 | +1 | 103 |

In this table, stage 2 does not create a brand-new answer from scratch. It corrects the existing 104 by adding `-2`. Stage 3 does the same by moving from 102 to 103 through `+1`.

So additive model can be read like this.

- the first stage 잡s the rough direction
- later stages keep correcting that answer little by little
- the final answer is built not by `one big jump`, but by `the sum of many small moves`

This feel matters especially when we compare it with random forest.

| Model | How the final answer is created after using many trees |
| --- | --- |
| random forest | average or vote across tree predictions at the end |
| gradient boosting | add each stage's correction to the previous answer in sequence |

So if random forest is read as `an aggregation of many opinions`, gradient boosting is read more accurately as `an accumulation of many corrections`.

In a practical scene, additive model is closer to building a churn score not by fixing it in one shot, but by starting from `a base risk score` and then letting signals such as `failed payment`, `recent usage drop`, and `more inquiries` raise or lower the score in later stages. The key question for the reader is `what new signal did each stage reflect?`

## Why Is Weak Learner Explained Through Small Trees?

The scikit-learn documentation explains the weak learner in gradient boosting through fixed-size regression trees. Examples often use very small trees, such as decision stumps.

Readers should not misunderstand weak learner as `a useless model`. A better reading is:

`a model that does not try to solve the whole problem at once, but handles only a small correction at one stage`

Why are small trees used?

- the role of each stage becomes clearer
- it reduces the chance that one stage memorizes too much of the whole problem
- it fits the structure where many stages accumulate corrections

A common beginner misunderstanding is to read `weak learner` as `a poor model`. But in boosting, it is closer to `a small correction tool with a limited role`.

| Easy misunderstanding | More accurate reading in this Section |
| --- | --- |
| because it is weak, it is not very useful | it is a tool that handles only a small correction at one stage |
| if the tree is small, the performance is always weak | many small trees accumulate into a strong model |
| if one stage cannot correct a lot, it is inefficient | not correcting too much at once fits sequential correction better |

If we go one step further, it also becomes clearer why `small trees` appear so often. In boosting, what matters more than `one big rule that solves everything` is `the next rule that reduces the current residual a little more`. Small trees fit that role better.

| Size of the stage model | What that stage tends to do | Advantage / risk in a boosting view |
| --- | --- | --- |
| very small tree | correct one simple residual pattern | the stage role is clear and it invites less memorization |
| medium-size tree | correct a few signal combinations together | expressive power grows, but the influence of one stage also grows |
| large tree | try to memorize many exceptions and complex branches in one stage | less room is left for later correction and overfitting risk rises |

So the reason weak learners are small trees is not `because they are low-performance`, but `because the role of one stage is being kept narrow`.

If we move this difference into a churn scene:

| Stage design | Question asked by one stage | Result that should be read |
| --- | --- | --- |
| small tree | one simple signal such as `did recent usage drop?` | the next stage can still fix another remaining pattern |
| large tree | split many things at once such as `usage drop + failed payment + more inquiries + membership age` | the first stage can explain too many scenes and make later stages follow noise more easily |

So in boosting, a small tree is not `a tool used because there is no better choice`. It is closer to `a basic part matched to the learning philosophy of sequential correction`.

## The Difference Between Random Forest And Gradient Boosting

Both models use many trees, but their operating philosophies differ.

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-1-mermaid-02-en.mmd"
```

This diagram shows at a glance that random forest gathers many tree outputs, whereas gradient boosting keeps having the next stage correct the error of the earlier stage.

Compressed briefly:

- random forest: `gather many independent opinions`
- gradient boosting: `the next answer corrects the previous answer`

This contrast matters a lot later when readers inspect performance, tuning sensitivity, and overfitting risk.

## Why Is `learning_rate` Important?

The scikit-learn documentation explains the learning rate as shrinkage. It scales down the contribution of each weak learner, and a smaller learning rate usually requires more weak learners.

It can be read like this.

- if `learning_rate` is large, one-stage corrections are reflected more strongly
- if `learning_rate` is small, one-stage corrections are reflected more gently

So `learning_rate` should not be read alone. It should be read together with `n_estimators`.

| Setting | Intuition |
| --- | --- |
| large learning rate + few trees | it moves quickly, but can shake too aggressively |
| small learning rate + many trees | it moves slowly, but can fit more finely |

That is why boosting is really about deciding together `how many correction stages to use` and `how much to correct at one stage`.

Rewritten more directly for beginners:

`The central setting of boosting is deciding together whether to move quickly in a few stages, or slowly across many stages.`

So if `learning_rate` is inspected separately, or `n_estimators` separately, the feeling becomes blurry. In practice the two move as one combination.

| First question to ask when reading the combination | Why it matters |
| --- | --- |
| Is one-stage correction too strong? | because a large `learning_rate` makes the influence of one stage large |
| Are there too few stages? | because a small `learning_rate` may need more opportunities for correction |
| Are residuals decreasing, but too slowly? | because readers need to inspect the balance between correction strength and stage count |

## What Does `n_estimators` Mean?

The scikit-learn documentation explains `n_estimators` as the number of boosting iterations, that is, the number of weak learners to fit.

If `n_estimators` in random forest meant `the number of trees in the forest`, then in gradient boosting it is closer to `how many correction stages should be used`.

It can be read like this.

- random forest: adding trees means gathering more opinions
- gradient boosting: adding stages means giving more chances for correction

So even the same name `n_estimators` feels different across the two models.

That difference matters a lot. In random forest, adding trees feels closer to `stabilizing the average`. In gradient boosting, adding stages feels closer to `holding onto the remaining error for longer`.

So in boosting, it is safer to read `n_estimators` not as `use more trees`, but as `continue the correction stages for longer`.

The effect of `continuing for longer` can also be shown more directly.

| When `n_estimators` is small | When `n_estimators` is large |
| --- | --- |
| large residuals can still remain | the model keeps trying to reduce even smaller residuals |
| the model is less complex, so the risk of excessive correction is relatively smaller | later stages can begin to follow noise and borderline cases |
| underfitting signals can appear first | overfitting signals can appear later |

So `n_estimators` is not just a model-size number. It is a handle that decides `through how many rounds the model keeps trying to correct error`.

The same idea looks easier in a tiny scene.

| Stage-count setting | How the prediction tends to look | Interpretation to read |
| --- | --- | --- |
| few stages | large errors shrink, but many borderline cases still remain | there may still be too few opportunities for correction |
| moderate stages | large errors shrink and some borderline cases are also cleaned up | this may be the zone where correction and generalization are more balanced |
| many stages | train can become nearly perfect, but validation can grow unstable | later stages may have started to follow the remaining noise |

So the more important questions in boosting are:

- Are many large residuals still left at the current stage count?
- Does validation actually improve as stages increase?
- Are later stages learning new structure, or beginning to memorize exceptions?

The feel becomes clearer again when we read it together with `learning_rate`.

| Combination | What readers expect first | What should be watched together |
| --- | --- | --- |
| small `learning_rate` + small `n_estimators` | cautious correction | the model may still not have learned enough |
| small `learning_rate` + large `n_estimators` | slow and fine correction through many stages | computation grows, and if it goes too long it can still overfit |
| large `learning_rate` + small `n_estimators` | residuals shrink quickly | one stage can shake the model early because its influence is large |
| large `learning_rate` + large `n_estimators` | strong correction keeps going for a long time | the risk of excessive correction and overfitting becomes the largest |

Under this table, `n_estimators` is not read alone. It is a value that decides the length and speed of correction together with `learning_rate`.

## Why Is Boosting Often Strong On Tabular Data?

The scikit-learn User Guide shows gradient-boosted trees and histogram-based gradient boosting as often-strong performance candidates in practice. They are frequently mentioned as a strong baseline or a high-performance candidate on tabular data.

The intuition is:

- they handle numeric data and transformed categorical data well
- they directly target the error left by the earlier stage
- they can accumulate small nonlinear patterns stage by stage

So in many practical scenes, boosting is often reviewed as `a stronger candidate than a linear model` or `a higher-performance candidate than random forest`.

Restated even more practically: it tends to be considered when `the expressiveness of a linear model feels insufficient on tabular data, and readers want to push the remaining error farther down than a single tree or random forest`.

But that strength can also come together with higher tuning sensitivity and higher overfitting risk. That continues in P4-16.2.

## In What Practical Scene Should We Recall It?

In practice, gradient boosting comes to mind first in scenes where `a single tree or random forest already catches the large flow, but readers still want to reduce the remaining error pattern further`.

### When Is It Good To Raise Gradient Boosting Early?

| Current problem state | Why raise gradient boosting early | What to check first |
| --- | --- | --- |
| a stronger performance candidate is needed on tabular data | because small patterns can be accumulated through sequential correction | whether there is a plan for overfitting control |
| the residual error left by a single tree or random forest is still clear | because the next stage can target residuals directly | what error scenes keep remaining |
| a structure of adding many weak rules feels natural | because the improvement flow is easy to read through the additive-model view | whether stage-wise correction becomes too strong |
| readers can accept more tuning for higher base performance | because `learning_rate`, stage count, and tree size can be tuned finely | whether validation procedure and early stopping are ready |
| readers want to reduce bias more aggressively than in random forest | because the method prioritizes error correction over average stability | the risk of following data noise too far |

The point of this table is to position gradient boosting not as `another ensemble that uses more trees`, but as `a high-performance candidate that sequentially fixes residual error`.

| Work scene | Why boosting comes to mind |
| --- | --- |
| churn prediction | it can capture several weak patterns through sequential correction |
| fraud detection | the next stage can respond more strongly to difficult cases missed earlier |
| score modeling for loan review | it can build a score through accumulated small rules and nonlinear interactions |
| ad-click prediction | in many feature combinations, it can keep reducing what is still wrong |

So it connects better to practical intuition when boosting is recalled as `a model that stacks many small corrections`, not `a model that makes one large split at once`.

## Cases And Examples

### Case 1. When Several Small Corrections Fit Better Than One Large Rule In Churn Prediction

In churn prediction for a subscription service, the easy human-first criteria are usually one or two rules such as `recent login count` or `whether payment failed`. For example: `if logins dropped sharply in the last 7 days, risk is high`, or `if there was a failed payment, risk is high`. Those rules are easy to understand, but in reality churn often grows through small overlaps such as membership age, recent usage drop, payment history, and increased inquiry count. So some customers are missed by only one simple rule.

The scene can be shrunk into this small table.

| Customer | Recent login drop | Failed payment | More inquiries | Membership age | Easy first rule | Actual reading |
| --- | --- | --- | --- | --- | --- | --- |
| A | large | yes | yes | short | high | truly high churn risk |
| B | small | no | yes | short | low | a borderline case that one simple rule can miss |
| C | large | no | no | long | high | a case that can be overstated by recent drop alone |

In this scene, gradient boosting lets the next small tree keep correcting what the first stage missed, so weak signal combinations such as `short membership age + more inquiries` and `failed payment + usage drop` can be reflected step by step. Then a case that looked ordinary under the first rule can move upward in churn score after later corrections, while a case whose risk was exaggerated only by recent login drop can be softened by later stages.

```mermaid
--8<-- "assets/part-04/chapter-16/p4-16-1-mermaid-03-en.mmd"
```

This scene is also read through the structure `current error -> next correction -> remaining review cases`. Even when the final score looks similar, one boosting setting may reduce errors for a certain customer type more strongly, while another setting may leave the same borderline cases. So those remaining patterns should be written down together.

| Stage | What to record | Why it matters |
| --- | --- | --- |
| current error | customer types missed by the first stage and cases given too low a churn score | to show what the next tree enters to correct |
| next correction | the new signal combination to which the next tree responded | to connect how boosting actually reduces residuals |
| remaining review cases | borderline cases that stay confusing even after several stages | to judge whether more stages are needed or overfitting risk is growing |

Compressed into project-note style:

| Current baseline | What this stage corrected | Cases still remaining | Next question |
| --- | --- | --- | --- |
| recent logins alone miss some churn customers | added the combination of failed payment, more inquiries, and usage drop | cases where normal customers were overstated because of temporary usage decline | should the stages continue, or is the model already fitting borderline cases too much? |

The verifiable result in this case appears when readers compare `whether borderline churn customers that one large rule missed are brought back by later corrections` and `whether cases overstated by recent decline alone still remain high after later correction`. So the boosting case is more accurately read through `what customer-type residual was reduced` than through only `the score improved`.

### Case 2. Why Can The Same Residual Look Like A Different Model When Correction Strength Changes?

Suppose a price-prediction team tests two settings on the same residual pattern. One uses a small `learning_rate` and continues for many stages. The other uses a large `learning_rate` and tries to reduce residuals quickly in fewer stages.

At first glance both still look like `models that reduce error`, so the difference can feel small. But in reality, the first is closer to `a model that fixes things little by little many times`, while the second is closer to `a model where one correction stage has much larger influence`.

The same residual can create different scenes like this.

| Setting | What it looks like after the first correction | Easy human-first misunderstanding | More accurate reading |
| --- | --- | --- | --- |
| small `learning_rate` + many stages | residual shrinks slowly and borderline cases remain longer | the model is still weak | it may be correcting gradually without aggressive overreaction |
| large `learning_rate` + few stages | residual shrinks quickly and early scores look good | it is the better model | one-step corrections may be too strong and later instability can grow |

For example, if a few samples have temporary price spikes, a large-`learning_rate` setting may follow those spikes faster and reduce train residual quickly. By contrast, a small-`learning_rate` setting may reflect the same residual more slowly, so early improvement can look less dramatic but the later stages may read more stably.

So in gradient boosting, it is not enough to stop at the sentence `the next tree sees the residual`. Readers should also ask `across how many steps is that residual reflected, and with what strength?` Only then do configuration differences connect to behavior differences.

The verifiable result in this case appears when readers compare, under the same residual pattern, `the speed of early train-residual reduction`, `the kinds of remaining borderline cases`, and `the instability of later stages`. The core is always `at what speed and with what strength was the same error corrected?`

## Practice And Example

This example is a toy exercise used only to build the feel that `corrections accumulate` from a regression viewpoint. It does not stop after one correction. It also checks how differently residuals shrink when correction strength changes.

- problem situation: inspect how the next stage adds a small correction after seeing the gap between the current prediction and the actual value
- input: current predictions and actual values
- expected output: stage-wise residuals and updated predictions
- concepts to check:
- residual is the remaining error - the next stage moves in the direction that reduces the residual - learning rate decides how much to correct at one time

```python
actual = [120, 110, 90, 80]
pred_stage0 = [100, 100, 100, 100]

residual_stage1 = [a - p for a, p in zip(actual, pred_stage0)]
tree1_correction = [15, 10, -10, -15]
learning_rate = 0.1

pred_stage1 = [
    p + learning_rate * c
    for p, c in zip(pred_stage0, tree1_correction)
]

residual_stage2 = [a - p for a, p in zip(actual, pred_stage1)]

print("actual           :", actual)
print("stage0 prediction:", pred_stage0)
print("stage1 residual  :", residual_stage1)
print("tree1 correction :", tree1_correction)
print("stage1 prediction:", [round(x, 1) for x in pred_stage1])
print("stage2 residual  :", [round(x, 1) for x in residual_stage2])
```

The output is as follows.

```text
actual           : [120, 110, 90, 80]
stage0 prediction: [100, 100, 100, 100]
stage1 residual  : [20, 10, -10, -20]
tree1 correction : [15, 10, -10, -15]
stage1 prediction: [101.5, 101.0, 99.0, 98.5]
stage2 residual  : [18.5, 9.0, -9.0, -18.5]
```

What should be read here is:

1. the first prediction is simple, so the error is large
2. the next stage adds a small correction in the direction of the residual
3. because `learning_rate = 0.1`, the correction is not used all at once, but only a little
4. so the residual does not immediately become 0, and room remains for later stages

So gradient boosting is closer to `many small corrections` than to `one large correction`.

### Change One Value: If `learning_rate` Grows, How Is The Same Correction Reflected Differently?

This time, keep the same correction and change only `learning_rate` to `0.5`.

```python
actual = [120, 110, 90, 80]
pred_stage0 = [100, 100, 100, 100]

tree1_correction = [15, 10, -10, -15]
learning_rate = 0.5

pred_stage1 = [
    p + learning_rate * c
    for p, c in zip(pred_stage0, tree1_correction)
]

residual_stage2 = [a - p for a, p in zip(actual, pred_stage1)]

print("stage1 prediction:", [round(x, 1) for x in pred_stage1])
print("stage2 residual  :", [round(x, 1) for x in residual_stage2])
```

```text
stage1 prediction: [107.5, 105.0, 95.0, 92.5]
stage2 residual  : [12.5, 5.0, -5.0, -12.5]
```

Compared with `learning_rate = 0.1`, the residual shrank faster. But the influence of one correction stage also became much larger. This comparison shows that, in gradient boosting, it is not enough to know `the next tree sees residuals`. Readers should also inspect `how strongly that residual is reflected`.

The difference can be fixed once more in the following table.

| Setting | Advantage that appears first | Caution to watch together |
| --- | --- | --- |
| small `learning_rate` | one-stage correction is less rough | more stages may be needed |
| large `learning_rate` | residuals can seem to shrink quickly | one-stage corrections can be reflected too aggressively |

So `learning_rate` is not only a speed control. It is a handle that decides `the strength of one correction`.

### What Should Be Read Together In This Example?

What matters here is not only `how much the value changed`. More important is reading together `with what strength the remaining error was reduced` and `how much room was left for the next stage to keep correcting`. Even with the same correction, if `learning_rate` changes, the speed of residual reduction and the influence of one stage change too. So in boosting, `residual correction` and `tuning handles` should be read in the same scene.

| Common record language | What to leave immediately in this exercise |
| --- | --- |
| structure that appeared | even with the same correction, the speed of residual reduction changed depending on learning rate |
| interpretation boundary | even if residuals shrink quickly, it does not mean that one-stage correction is always safer or more generalizable |
| next question | if the number of stages increases, how do the remaining errors and the overfitting risk change together? |

## Checklist

- Is the current need closer to residual correction than to variance reduction?
- Can you explain the structure that reduces residuals?
- Are you reading the higher performance potential together with the higher tuning sensitivity?
- Can you explain that gradient boosting is an ensemble where the next stage sequentially reduces the error of the earlier stage, and that residual is the remaining part that the earlier stage still failed to explain?
- Can you explain that a weak learner is a small tree that handles a small correction, and that `learning_rate` and `n_estimators` must be read together?
- Can you explain that if random forest is parallel aggregation, gradient boosting is sequential correction?

## Sources And References

- scikit-learn developers, `1.11. Ensembles: Gradient boosting, random forests, bagging, voting, stacking`, scikit-learn User Guide, accessed 2026-06-27. [https://scikit-learn.org/stable/modules/ensemble.html](https://scikit-learn.org/stable/modules/ensemble.html){: target="_blank" rel="noopener noreferrer" }
- Jerome H. Friedman, `Greedy Function Approximation: A Gradient Boosting Machine`, Annals of Statistics, 2001, accessed 2026-07-19. [https://doi.org/10.1214/aos/1013203451](https://doi.org/10.1214/aos/1013203451){: target="_blank" rel="noopener noreferrer" }
- Jerome H. Friedman, `Stochastic Gradient Boosting`, Computational Statistics & Data Analysis, 2002, accessed 2026-07-19. [https://doi.org/10.1016/S0167-9473(01)00065-2](<https://doi.org/10.1016/S0167-9473(01)00065-2>){: target="_blank" rel="noopener noreferrer" }
