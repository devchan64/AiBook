# P4-7.2 Preprocessing

> Section ID: `P4-7.2`
> Version: `v2026.07.31`

First look at the input table. `age` has missing values, `income` moves on a much larger scale than other numbers, and `city` is a string. Here preprocessing is not about memorizing three technique names; it is about deciding which rule fills blanks, how numeric scales are aligned, and what computable representation a string becomes.

P4-7.1 examined `what inputs should remain`. Now the discussion moves to the stage where those remaining inputs are not thrown to the model as they are, but are organized into a form the model can read more easily. That stage is preprocessing.

The core point of this Section is not complex library syntax. It is understanding preprocessing not as something like `data cleaning` alone, but as `the work of changing input representations into a form the model can handle`.

This Section explains the basic meanings of [preprocessing](/AiBook/en/reference/concept-glossary-alpha/p/#preprocessing), [imputation](/AiBook/en/reference/concept-glossary-alpha/m/#missing-value), scale adjustment, and categorical encoding. Later Sections continue the current judgment through this handle, and the basic meaning of input-representation transformation reconnects through this Section and the [concept glossary](/AiBook/en/reference/concept-glossary/).

There is one more important reason. People often learn algorithms first and think preprocessing is an auxiliary step added later. In practice, it is more similar to the opposite. If input representations are not organized, it is hard to read the character of algorithms such as linear regression, logistic regression, k-NN, and SVM that appear later.

This Section is not an appendix to one specific algorithm. It is a common foundational Section that organizes `what kind of input an algorithm receives`.

Academically as well, preprocessing is not peripheral work. In textbooks and tool documentation on data mining, pattern recognition, and machine learning, preprocessing is usually treated as an independent step that moves `raw data` into `feature space` or `model input`. Preprocessing is not miscellaneous work attached before a model, but `the stage that creates a learnable representation`.

The reason this perspective matters is simple. A model does not learn reality itself. It learns inputs represented through preprocessing. Therefore, how preprocessing is done directly affects boundary, [distance](/AiBook/en/reference/concept-glossary-alpha/d/#distance), [optimization](/AiBook/en/reference/concept-glossary-alpha/o/#optimization), and interpretability.

## Scope Of This Section

This Section answers the following questions.

- What does preprocessing change?
- Why can missing values, scale, and categorical values become problems if left as they are?
- Which models are sensitive to scale, and which are less sensitive?
- How should preprocessing be separated between train data and test data?

This Section first settles `how to change the remaining inputs into calculable and comparable representations`. The detailed settings of individual encoders and scalers reconnect again in the context of hyperparameters and tuning in P4-9.1 and P4-9.2, while the purpose and intuition of dimensionality reduction continue in P4-18.1 and P4-18.2.

## Goals Of This Section

- You can explain preprocessing as `the stage that changes raw input into a more suitable representation`.
- You can explain why missing-value handling, scale adjustment, and categorical encoding are necessary.
- You can distinguish `fit` from `transform` in preprocessing and explain why test data must not be used for `fit`.
- You can understand at an introductory level why pipelines and ColumnTransformer are often used in practice.

## Learning Background

The earlier Sections in Part 4 have continued in the following flow.

- P4-4: how should data be split
- P4-5: why is [generalization](/AiBook/en/reference/concept-glossary-alpha/g/#generalization) difficult
- P4-6: what criterion should be used for evaluation
- P4-7.1: what inputs should remain

Once the discussion reaches this point, the next question appears.

`In what form should the remaining inputs be delivered to the model?`

That question is exactly where the preprocessing Section belongs. In the curriculum, this Section plays the following role.

| Curriculum position | Role of the preprocessing Section |
| --- | --- |
| after feature selection | organize what representation the remaining inputs should take |
| before model selection | prepare for understanding which models prefer which kinds of input representation |
| before the algorithm introduction | connect why distance, boundary, and optimization are sensitive to input representation |

Preprocessing is the Section that connects `input design` and `model understanding`.

From the curriculum point of view, this Section is also a boundary where the character of Module 2 and Module 3 changes. The data splitting, generalization, and evaluation metrics covered in Module 2 dealt with `what must be organized first to compare models fairly`. By contrast, Module 3 deals with `what combination of inputs and models should actually be used to begin experiments`. Preprocessing sits exactly at that turning point.

After passing this Section, the reader moves beyond simply having collected data and into the flow of `building comparable input representations and then setting up model candidates`. For that reason, P4-7.2 becomes the common foundation of P4-8 [model selection](/AiBook/en/reference/concept-glossary-alpha/m/#model-selection), P4-9 [hyperparameter tuning](/AiBook/en/reference/concept-glossary-alpha/h/#hyperparameter), and the algorithm Sections after P4-10.

## Main Learning Content

### A First Grip On Preprocessing

When readers first hear the term preprocessing, it can sound difficult. But stated very briefly, it is `the preparation work that changes inputs the model cannot easily read into inputs it can read`.

People can read the following table without difficulty.

| age | income | city |
| --- | ---: | --- |
| 29 | 3200 | Seoul |
| none | 6100 | Busan |
| 35 | none | Incheon |

But many models have difficulty handling this table as it is.

- If there is `none`, calculations break.
- `3200` and `29` are on very different numeric scales.
- Strings such as `Seoul` and `Busan` are hard to calculate with directly.

So it is usually enough to think of preprocessing in the following way.

1. Handle empty values by some rule.
2. Align numeric values to make comparison fairer.
3. Change strings or categories into a calculable representation.

After this process, the same data turn into inputs roughly like the following.

| age_filled | income_scaled | city_search | city_busan | city_incheon |
| ---: | ---: | ---: | ---: | ---: |
| 29 | ... | 1 | 0 | 0 |
| 35 | ... | 0 | 1 | 0 |
| 35 | ... | 0 | 0 | 1 |

In other words, preprocessing is not the work of creating a new answer. It is `rewriting the original input in a format the model can calculate with`.

This Section examines that idea through three representative scenes.

- missing-value handling: how should empty values be handled
- scale adjustment: how should differences in numeric magnitude be aligned
- encoding: how should strings and categories be changed into a calculable form

### What Does Preprocessing Do?

The scikit-learn preprocessing documentation explains that it provides various functions and transformers that convert `raw feature vectors` into representations more suitable for downstream estimators. Rephrased at an introductory level, that means the following.

`Preprocessing is the stage that changes raw input into an input representation the model can handle better.`

Preprocessing is not the work of changing the label. It is the work of changing the input representation.

Put a little more academically, preprocessing is a set of transformations that changes the representation of the input space so that learning algorithms can operate more stably. This can include missing-value handling, scaling, and encoding, and in some cases broader categories such as normalization, feature construction, and dimensionality reduction. This Section focuses on the three categories that readers meet most often.

This Section looks at preprocessing mainly in three parts.

1. imputation
2. numeric transformation and scaling
3. categorical representation transformation

All three share one thing: they `change the input representation`. But what they change differs.

| Type of preprocessing | What it changes | Why it changes it |
| --- | --- | --- |
| imputation | the rule for filling empty values | to make calculation possible |
| scale adjustment | the size and reference of numbers | to stabilize comparison and optimization |
| encoding | categorical values into numeric representation | to match the form of model input |

However, if readers look a little more broadly at the types of preprocessing used in practice, it helps to keep the following larger map in mind.

| Large preprocessing category | What it does | How deeply this Section treats it |
| --- | --- | --- |
| imputation | corrects or marks empty values according to rules | covered in detail |
| numeric scale adjustment | aligns the magnitude and reference of numeric axes | covered in detail |
| categorical encoding | changes string and categorical values into calculable representations | covered in detail |
| outlier handling | keeps extreme values from shaking learning too much | concept only |
| feature construction | creates more useful input representations from original columns | mentioned only as a broad category, connected mainly to P4-7.1 in this book |
| [dimensionality reduction](/AiBook/en/reference/concept-glossary-alpha/d/#dimensionality-reduction) | compresses many inputs into a smaller representation | revisited in P4-18 |
| special representation transforms for text/images and so on | converts unstructured data into numeric representation | treated in later Parts as separate input representations |

The purpose of this table is not to force every preprocessing technique into one Section. Rather, it is to help readers first grasp that the term `preprocessing` does not refer only to the narrow act of filling missing values with an average.

Still, to keep the boundary clear in this book, `which inputs to keep in the first place and what new feature candidates to create` is placed mainly on the feature-design side of P4-7.1, while this Section focuses on `changing the remaining inputs into a calculable and comparable form`. So in a broad sense feature construction can also belong to the large preprocessing category, but the central responsibility of this Section is missing-value handling, scale adjustment, encoding, and the reuse of the same rules.

At the introductory level, it is enough to remember preprocessing in the following way.

1. preprocessing that fills values
2. preprocessing that aligns numeric axes
3. preprocessing that changes the form of representation
4. preprocessing that softens overly extreme values or reduces the number of inputs

In other words, preprocessing is not one technique but `a bundle of different rules that make input representations calculable and comparable`.

When readers are trying to understand preprocessing for the first time, the fastest route is to picture `what one row of raw input becomes after preprocessing`.

| One row before preprocessing | Example of one row after preprocessing |
| --- | --- |
| `age=none, income=5800, city=Seoul` | `age=filled with median, income=scale-adjusted value, city=[0,0,1]` |
| `age=35, income=none, city=Incheon` | `age=keep 35, income=filled with median and then scaled, city=[0,1,0]` |

The key point shown by this comparison is simple.

1. Preprocessing does not change the label.
2. Preprocessing rewrites one input row into a form the model can calculate with.
3. The same rule must be applied repeatedly to other rows as well.

That is why preprocessing is closer not to `fixing data` but to `translating input rows again`.

For example, the following kinds of problems can appear.

| Original input condition | Why the model becomes troubled | Role of preprocessing |
| --- | --- | --- |
| values are empty | immediate calculation is impossible | imputation |
| differences in numeric magnitude are too large | one feature may gain too much influence | scale adjustment |
| values are strings like city names | many models cannot calculate directly | categorical encoding |
| different rules are used for train and test | evaluation becomes distorted | keep the same transformation rules |

Therefore, preprocessing is both `organization` and `representation design`.

If the kinds of preprocessing are grouped again from the viewpoint of input problems, they can be read as follows.

| Input problem | Type of preprocessing to bring to mind | Example |
| --- | --- | --- |
| value is empty | imputation | mean, median, mode, missing flag |
| value magnitudes differ too much | scale adjustment | standardization, min-max scaling |
| value is a string or category | encoding | one-hot encoding |
| some values jump out too much | outlier handling | review robust scaling or clipping |
| there are too many columns | dimensionality reduction / representation compression | methods such as PCA in later Sections |
| the original columns alone contain weak signal | feature construction | create ratio, difference, or aggregated features |

Seen this way, preprocessing is not a list that ends with `missing-value handling + scale + encoding`, but work whose branches split according to `what kind of representation problem the current input has`.

Theoretically, preprocessing is viewed through the following two perspectives at the same time.

1. representation transformation  
   moving the same fact into a different numeric representation
2. assumption matching  
   bringing the input more similar to the conditions expected by the model or learning procedure

For example, standardization is not merely arranging numbers in order. It is an attempt to align the center and variance of the input so that certain algorithms work better. One-hot encoding is not forcing strings into numbers, but changing them into a calculable feature representation.

Academically, preprocessing can be understood as `the stage that transforms the input representation placed before the model and moves it into a space where learning and inference are possible`.

What matters here is that preprocessing is not `making data look neat`, but `re-coordinatizing the world the model will see`. Even with the same customer data, some values remain empty, some sit on overly large numeric axes, and some are strings that cannot be calculated with at all. Preprocessing is the process of bringing all three back into `comparable and calculable representations`.

That is why preprocessing is not auxiliary work, but the stage that determines `what the model will be able to read as the same kind of information`.

If readers want a shorter grip on this perspective, the following contrast helps.

| Question | The answer feature selection is more similar to | The answer preprocessing is more similar to |
| --- | --- | --- |
| What should remain as input? | which columns should be adopted | how should the columns already kept be changed |
| What should not be given to the model? | IDs, leakage columns, post-outcome information | rules fit on test data, incorrect encoding method |
| What should be made calculable? | organize input candidates | fill values, align axes, change representation |

In short, if feature selection is `deciding the entrance`, preprocessing is `translating the values that entered through that entrance into the model's language`.

To understand preprocessing for real, readers also need to grasp that this translation usually happens in the following order.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-2-mermaid-01-en.mmd"
```

The core points of this flow are four.

1. The raw table is not put directly into the model.
2. Data are split first, and rules are learned only on train.
3. The learned rules are applied repeatedly to other rows.
4. Only then does the result become a model input matrix.

That means preprocessing is not `slightly touching up values`, but `reconstructing a raw table into a matrix the model can read`.

#### What Immediately Breaks Without Preprocessing

The shortest way to understand the need for preprocessing is to look at `what happens without preprocessing`.

| Raw input condition | What happens if it is fed in directly without preprocessing | Why it is a problem |
| --- | --- | --- |
| there are missing values | some models and calculations stop completely or throw errors | the row cannot become a calculable input row |
| numeric scales vary wildly | a large-unit axis dominates distance and optimization too much | feature comparison is not fair |
| string categories are mixed in | many models cannot calculate them directly | the input representation does not move into numeric space |
| train and test use different rules | evaluation scores can look better than reality or fluctuate | comparison and reproducibility both collapse |

That means preprocessing is not an optional extra that raises performance a little. In many cases, it is `the minimum condition that lets the model read the input at all`.

Translated into more practical language, the same point reads as follows.

1. Input that cannot be calculated with cannot be learned from.
2. Input whose comparison is unfair creates incorrect boundaries and distances.
3. Rules that cannot be reproduced make it impossible to create the same input again after deployment.

That is why preprocessing is closer not to makeup added after the model, but to foundational construction that makes the input world possible before the model.

### How Do Feature Selection And Preprocessing Connect?

If feature selection in P4-7.1 was the work of deciding `what should remain`, preprocessing is the work of deciding `how what remains should be represented`.

The key point is that even after `selection`, the input representation still has to be handled further. The features that remain must go through transformations such as missing-value handling, scale adjustment, and encoding before they finally become inputs the model can read well.

If preprocessing is viewed not as one technique but as `a bundle of transformations that adjust input representations`, the following input-inspection questions immediately appear.

- Is this value calculable?
- Does the magnitude difference of this value distort learning?
- What effect does this representation have on distance, boundary, and optimization?
- Can the transformation rules learned during training be reproduced unchanged at inference time?

These questions matter because the algorithms that appear later are sensitive to input representation in different ways.

It becomes less confusing if readers organize the fact that the same input can branch into several preprocessing questions.

| Problem arising from the same input | The first question attached to it | The closer preprocessing judgment |
| --- | --- | --- |
| value is empty | is calculation itself possible | imputation |
| numeric magnitudes differ too much | which column dominates distance or optimization | scale adjustment |
| value is a string | can the model calculate this representation directly | encoding |
| train and test use different rules | is the same rule reproduced in evaluation and operations | separate `fit` and `transform` |

This table helps readers see preprocessing again not as technique names, but as `what kind of input problem is being diagnosed`.

Taking one step further, the order of preprocessing judgment can usually be fixed as follows.

| Order | What to inspect first | Why it comes first |
| --- | --- | --- |
| 1 | whether train and test were split first | to prevent leakage while learning rules |
| 2 | whether the values are calculable | because missing-value and string problems must be solved first |
| 3 | whether values are compared fairly with one another | because scale differences can distort learning |
| 4 | whether the same rules are applied repeatedly | because evaluation and deployment must be reproducible |

If readers hold onto this order, preprocessing becomes easier to understand as `an input-representation design procedure` rather than `a checklist for applying tools`.

### Seeing Before And After Preprocessing In One Scene

To understand preprocessing more concretely, it helps to view at once how the same small table changes.

| customer | age | income | channel | label |
| --- | ---: | ---: | --- | ---: |
| A | 29 | 3200 | search | 0 |
| B | none | 6100 | ad | 1 |
| C | 35 | none | direct | 0 |
| D | 41 | 5800 | search | 1 |

This table is readable to a person, but from the model's point of view it is difficult to use directly.

- `none` interrupts calculation.
- `age` and `income` are on different numeric axes.
- `channel` is a string, so direct calculation is hard.

After preprocessing, the same table changes into inputs roughly like the following.

| customer | age_filled | income_filled | age_scaled | income_scaled | channel_search | channel_ad | channel_direct | label |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A | 29 | 3200 | ... | ... | 1 | 0 | 0 | 0 |
| B | 35 | 6100 | ... | ... | 0 | 1 | 0 | 1 |
| C | 35 | 5800 | ... | ... | 0 | 0 | 1 | 0 |
| D | 41 | 5800 | ... | ... | 1 | 0 | 0 | 1 |

What matters here is not the numeric values themselves but the structural change.

1. Missing values were filled according to a rule.
2. Numeric values were moved onto a shared comparison axis.
3. Categorical values were expanded into a bundle of calculable columns.
4. As a result, each row is arranged into an input vector of the same form.

In other words, the result of preprocessing is not `a cleaner table`, but `an input matrix the model can read in the same structure`.

If readers hold onto this scene, it becomes easier to understand preprocessing not as `three partial techniques`, but as `integrated work that moves different values into the same calculational world`.

### Why Must Missing Values Be Handled First?

Real-world data are often empty.

- a value the user did not answer
- a value a sensor failed to read
- a value recorded only later
- a value missing because collection failed

If these values are left as they are, many models and operations cannot proceed immediately. So in the first stage of preprocessing, readers decide `how empty values should be handled`.

The documentation for scikit-learn's `SimpleImputer` provides examples of filling missing values with strategies such as mean, most frequent, and constant.

| Situation | Introductory strategy often used |
| --- | --- |
| numeric column | mean, median |
| categorical column | most frequent, a constant such as `"unknown"` |
| the missingness itself may carry meaning | keep whether it is missing as a separate signal |

What matters here is not `always fill it`, but `why fill it with that rule`.

For example, an income column can have many extreme values, so the median may be better than the mean. By contrast, a test-score column with a relatively even distribution may make the mean more intuitive.

The idea becomes easier to read when moved into work scenes.

| Scene | What the missing value means | Example of introductory judgment |
| --- | --- | --- |
| hospital reservation data | the booking path was not recorded | can be kept as a separate category such as `"unknown"` |
| shopping-mall customer data | income information was not entered | review median fill or adding a separate missingness signal |
| sensor data | measurement failure | may be better treated as a collection-failure signal than simple filling |

Missing values are not simple blanks. They are input states that should be read together with `why they are empty`.

The types of missing-value handling can also be divided very roughly in the following way.

| Method | What it does | Introductory advantage | What to be careful about |
| --- | --- | --- | --- |
| mean/median fill | fills numeric missing values with a representative value | easy and fast to implement | can flatten the distribution too much |
| mode/constant fill | fills categorical missing values with the most common value or `"unknown"` | easy to use on string columns too | can oversimplify the actual meaning |
| add a missing flag | keeps the fact that the value was empty in a separate column | useful when missingness itself is a signal | increases the number of columns and adds interpretation work |
| remove rows | excludes rows or columns that contain missing values altogether | the rule is simple | data loss can become large |

That is why missing-value handling is not only a question of `what should fill the gap`, but also a choice among `should the trace of missingness remain`, `should it be discarded altogether`, and `should it be approximated by a representative value`.

#### What Happens When Missing Values Are Handled Poorly?

If readers think too quickly that `filling with the average solves it`, they can miss important differences.

| Missing-value situation | Hasty handling | Better beginner judgment |
| --- | --- | --- |
| simple omitted input | fill with mean without any explanation | first inspect why it was empty |
| missingness itself may be a behavioral signal | erase the trace of missingness completely | review a missingness flag together |
| sensor collection failure | fill it so that it looks like a normal value | inspect whether it should be treated as a collection-failure signal |

That means missing-value handling is closer not to hiding blanks, but to interpreting `what kind of event the blank represents`.

One more important point is that once missing values are filled, those filled values start to look like `original observations`. So, if possible, readers should remain aware of `is this an observed value or an imputed value`. Preprocessing is not the work of preserving reality exactly, but the work of creating an approximated representation that can be calculated with.

For this reason, it helps to keep the following questions attached in missing-value handling.

1. Is the missingness in this column an accidental omission or a behavioral/collection event?
2. Does filling with a representative value distort the meaning too much?
3. Should the fact of missingness itself be kept as a separate signal?

Without these three questions, missing-value handling easily becomes mere technique application. With them, it becomes input interpretation.

### Why Can Scale Create Problems?

Not every numeric feature moves in the same unit.

For example, readers can imagine the following two columns.

- age: 20, 35, 41
- monthly_income: 2,000,000 / 4,500,000 / 8,000,000

Both are numeric, but their magnitude ranges are very different. Some algorithms, if they receive this difference as it is, can easily treat the large-number axis as more important.

The scikit-learn preprocessing documentation explains that many learning algorithms, including linear models, benefit from standardization, and that if feature variances differ greatly, certain features can dominate the objective function too much.

`Scale adjustment is not the work of making numbers look neat. It is the work of rebalancing influence among features.`

This explanation also connects directly to later theory.

- In k-NN, the distance calculation changes.
- In SVM, the boundary can change.
- In linear models and logistic regression, optimization can become more stable.

Scale adjustment is not a simple preprocessing trick. It is also preparation for understanding the algorithm Sections that come later.

In practical scenes, it can be read as follows.

| Scene | What can happen if scale adjustment is not done |
| --- | --- |
| loan screening | a large-number axis such as income can overwhelm other features |
| user clustering | distance calculation can be dragged toward a column with a particularly large unit |
| anomaly detection | a column where small changes matter can be buried |

#### Which Models Are More Sensitive To Scale?

Not every model is sensitive to scale to the same degree.

| Model family | Effect of scale |
| --- | --- |
| k-NN, SVM, distance-based methods | generally sensitive |
| linear models, logistic regression, gradient-descent-based methods | often sensitive |
| tree families such as decision trees and random forests | relatively less sensitive |

This difference becomes clearer in later chapters.

- P4-10 linear regression
- P4-11 logistic regression
- P4-12 k-NN
- P4-13 SVM
- P4-14 and P4-15 trees and ensembles

Preprocessing does not operate with exactly the same weight in every model. Depending on the model type, it can become more important.

If readers look at a short contrast, the scale problem becomes clearer.

| Feature combination | Reading before scale adjustment | Reading after scale adjustment |
| --- | --- | --- |
| `income`, `visits_30d` | the large-number `income` axis tends to dominate the judgment | the two features are compared on a more similar basis |
| `sensor_peak`, `sensor_std` | only the large-unit axis may stand out too much | variability and magnitude become easier to read together |

That means scale adjustment is not `a technique that enlarges small numbers`, but `a technique that adjusts which axis is speaking too loudly when several features are compared`.

For that reason, scale adjustment should be read together with `what kind of comparison method the model uses`, rather than as a standalone technique. Models that use distance are more sensitive, while tree families that use splitting rules are relatively less sensitive. Preprocessing is always not only `a data problem`, but also `a data-model interaction problem`.

If readers divide scale adjustment very roughly by type, it can be seen as follows.

| Method | What it aligns | When it often comes to mind | What to be careful about |
| --- | --- | --- | --- |
| Standardization | aligns values near mean 0 and variance 1 | linear models, logistic regression, SVM, k-NN | effects of outliers can remain |
| Min-Max scaling | compresses values into a fixed range | when readers want value ranges within a fixed interval | can be dragged by extreme values |
| Robust scaling | aligns values using median and quantiles | when outliers stand out | interpretation can feel a little less intuitive |

Memorizing this table is not the goal, but readers do need to keep the point that `scaling` is not one technique name, but a choice about `what standard should be used to realign axes`.

Scale adjustment also becomes less confusing when read in the following way.

| Question | What scale adjustment answers | What it cannot answer |
| --- | --- | --- |
| Are value ranges too different for fair comparison? | yes | is this feature actually useful |
| Does a large-number axis dominate distance and optimization? | yes | is leakage mixed into that number |
| Does the model learn more stably? | often yes | does performance necessarily improve |

That means scale adjustment is a tool for aligning `comparison standards`. It is not a tool that replaces feature selection or leakage inspection.

### Why Are Categorical Values Hard To Feed In Directly?

Categorical values such as city names, membership tiers, and product categories feel natural in reality, but many models cannot calculate with the strings themselves directly.

So categorical values usually go through encoding and are changed into numeric representations.

Categorical encoding is the process of changing each category into a calculable numeric representation.

| Original value | Example after encoding |
| --- | --- |
| `city = Seoul` | `[1, 0, 0]` |
| `city = Busan` | `[0, 1, 0]` |
| `city = Incheon` | `[0, 0, 1]` |

This kind of method is usually called one-hot encoding.

What matters is not `the string was translated into a number`, but `the representation was changed into a form the model can calculate with`.

At this point, one thing beginners often confuse is thinking that `if it becomes numbers, it also gains order`. But if readers assign arbitrary numbers such as `Seoul=1`, `Busan=2`, `Incheon=3`, the model can misunderstand them as if a magnitude comparison existed when it really does not. So one-hot encoding is better read as a choice that keeps category differences while avoiding the forced creation of an order that does not exist.

That means encoding is not `changing letters into numbers`, but deciding `through what numeric structure the differences among categories should appear`. If readers miss this point, preprocessing can look like a mere format conversion, and they miss that it is really handling the problem of preserving meaning.

At the introductory level, encoding methods can be divided roughly as follows.

| Method | What it does | When it is relatively natural | What to be careful about |
| --- | --- | --- | --- |
| one-hot encoding | creates a separate column for each category | general categorical values without order | if there are many categories, the number of columns grows |
| ordinal-like encoding | places categories on ordered values | when order truly has meaning | if it creates an order that does not exist, distortion follows |
| frequency/statistics-based transformation | changes categories into other summary values | may be used in more advanced situations | should be checked together with leakage caution |

This Section centers on one-hot encoding, but the key habit is to first distinguish `does this category have a real order or not`.

For example, the following two cases both look like strings on the surface, but the reading can differ.

| Category example | Character | More natural introductory judgment |
| --- | --- | --- |
| `bronze/silver/gold` | may carry real order | judge carefully how order meaning should be reflected |
| `Seoul/Busan/Incheon` | unordered distinction values | an order-free representation such as one-hot encoding is more natural |

That means encoding is not `a technique that removes strings`, but `a technique that preserves category meaning in a calculable structure`.

In work scenes, it reads as follows.

| Original value | Why leaving it unchanged is difficult | What is gained after changing it |
| --- | --- | --- |
| membership tier `gold/silver/bronze` | many models cannot calculate the raw string | it turns into tier-specific feature columns |
| delivery region `Seoul/Busan/Incheon` | the region name itself is hard to use in numeric operations | regional patterns can be read separately |
| device type `ios/android/web` | there are category differences but no concept of magnitude comparison | the category distinction signal is expressed as a calculable vector |

## Detailed Learning Content

### In Practice, What Kind Of Problems Does Preprocessing Appear As?

Preprocessing is easy to memorize as individual technique names such as filling with an average, applying a scaler, or choosing an encoder. But in practice, people start the other way around, from `what input problem has appeared`. The missing-value, scale, and categorical representation problems seen earlier are all just different faces of that field question.

In other words, in the field people usually think in the following order.

1. What is unstable in the values arriving right now?
2. How does that instability distort learning and evaluation?
3. What preprocessing rule can reduce that distortion?

If this flow is drawn as the simplest diagram, it looks like the following.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-2-mermaid-02-en.mmd"
```

The core of this diagram is that preprocessing is not `memorizing the order of technique application`, but the flow of `diagnose input problem -> choose transformation rule -> reconstruct consistent input`.

If typical scenes are grouped in a table, they look as follows.

| Work situation | Problem visible in the input | Preprocessing judgment to bring up first |
| --- | --- | --- |
| e-commerce churn prediction | purchase amount is large, visit count is small, and acquisition channel is a string | review numeric scaling + encode the channel |
| ad-click prediction | there are many categories such as device, region, and campaign, and some values are empty | categorical missing-value handling + encoding |
| hospital appointment no-show prediction | booking path and questionnaire information are partly missing | first judge whether the missingness is a simple blank or a separate signal |
| manufacturing sensor anomaly detection | sensor units vary widely and there are collection-failure intervals | separate scale adjustment + collection-failure handling rules |
| customer clustering | age, sales, and visit frequency differ greatly in units | review scale adjustment first before distance calculation |
| loan-screening support | explanation matters and missing plus categorical inputs appear together | prevent leakage + keep interpretable transformation rules |

The purpose of this table is not to add new techniques. It is to help readers read, in connection with practice, what kinds of problems the earlier topics of missing-value handling, scale adjustment, and encoding reappear as.

Seen a little more concretely, practical examples are usually regrouped into the following three judgments.

| Practical judgment axis | Question asked in the field | Connected preprocessing work |
| --- | --- | --- |
| calculability | can the model calculate this value directly | missing-value handling, encoding |
| comparability | is the magnitude comparison fair when placed with other features | scale adjustment, normalization |
| reproducibility | can the rule used in training be reproduced exactly in operations | separate `fit/transform`, build pipelines |

So preprocessing is not simple preparation work, but `the design stage that turns real-world data into input that is calculable, comparable, and reproducible`.

#### Common Misunderstandings In Preprocessing

At the beginning of practical work, the following misunderstandings appear especially often.

| Common misunderstanding | Why it is a problem | More accurate understanding |
| --- | --- | --- |
| preprocessing ends once cleaning is done well | the interaction between the model and input representation is missed | preprocessing is the stage that sets the coordinates the model will read |
| every numeric value must always be scaled | even model families that are less sensitive, such as tree families, are forced into the same rule | sensitivity differs by model family |
| once missing values are filled, the issue is solved | missingness itself can be a signal | the interpretation of why it is missing comes first |
| encoding ends once strings are turned into numbers | an order that does not exist can be created and cause distortion | calculability and meaning preservation must both be checked |

### Why Must The Same Rules Be Used For Train Data And Test Data?

One of the most common mistakes in preprocessing is mixing train data and test data.

The scikit-learn common pitfalls documentation strongly recommends the following.

- split data into train/test first
- do `fit` and `fit_transform` only on train data
- on test data, do only `transform` with the same rules
- pipelines make it easier to keep this boundary

`Test data are for evaluation, not for learning preprocessing rules.`

Simplified, this means the following.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-2-mermaid-03-en.mmd"
```

The core of this diagram is that `fit` happens only once on the training data.

This difference can actually create performance illusions.

| Incorrect flow | Why it is a problem |
| --- | --- |
| compute the average after looking at the whole dataset and then split train/test | test information is mixed into the training rule |
| organize encoding categories after looking at the whole dataset and then evaluate | the result can become more optimistic than the pre-deployment situation |
| align scaling references using test data too | evaluation can look better than it really is |

That means [data leakage](/AiBook/en/reference/concept-glossary-alpha/d/#data-leakage) in preprocessing can distort evaluation numbers even without changing model structure.

If readers look at this difference more directly, it reads as follows.

| Flow | Surface-level result | Actual interpretation |
| --- | --- | --- |
| learn means, scales, and category rules only on train | validation scores may be conservative, but they are more trustworthy | it is more similar to the pre-deployment situation |
| learn rules from the whole dataset and then evaluate | scores may look better | it may be an illusion caused by mixed test information |

That means where preprocessing rules were learned is an evaluation condition just as important as model choice itself.

### Why Do Pipeline And ColumnTransformer Appear So Often?

In practice, numeric columns and categorical columns often need to be handled differently.

- numeric columns: imputation + scale adjustment
- categorical columns: imputation + one-hot encoding

The scikit-learn `Pipeline` documentation shows how to connect `fit` and `transform` stages, and the `ColumnTransformer` documentation shows examples of applying different transforms to different column groups.

| Tool | Introductory meaning |
| --- | --- |
| Pipeline | ties transformation steps and model-learning steps into one line |
| ColumnTransformer | applies different preprocessing rules separately to different kinds of columns |

That means preprocessing does not end with knowing individual techniques. It must also go together with `a structure that can apply the same rules repeatedly`.

This structure is also important from the curriculum perspective. In later Sections on model selection and tuning, people often compare not merely `the model alone`, but a combined bundle of `preprocessing + model`.

### What Preprocessing Questions Should Be Asked First?

Before memorizing technique names, preprocessing begins with quickly diagnosing what problem the current input is creating.

| Input condition | Question to ask first | Preprocessing to review first |
| --- | --- | --- |
| values are empty | why are they empty, and is the emptiness itself a signal | missing-value handling, review of missing flags |
| numeric magnitude differences are large | is distance or optimization being dragged toward a certain column | review standardization or normalization |
| strings/categories are mixed in | can the model calculate this value directly | categorical transformation such as one-hot encoding |
| train/test may use different rules | where were the rules learned and where are they reused | separate `fit`/`transform`, pipeline |
| operational input quality often fluctuates | can the same transformation be reproduced after deployment | fix rules by column, structure with pipelines |

This table helps readers read preprocessing not as `a list of tools to apply`, but as `a response rule for input problems`.

A good explanation of preprocessing should usually be summarizable in the following sentences.

1. What input problem existed?
2. Why did that problem interfere with model calculation?
3. By what rule was it changed?
4. How was the same rule reused identically for train and test?

If these four sentences are not explained, preprocessing is likely to leave only technique names while the judgment reason remains empty.

If readers add one more sentence, the explanation becomes more complete.

5. In which model families does this rule become especially important?

For example, scale adjustment is more sensitive in k-NN, SVM, and linear models, while encoding is almost essential in many models that cannot read strings directly. In other words, preprocessing explanations begin with input problems, but they need to reach the model connection to gain enough density.

## When Input State Requires Preprocessing Rules

### Case 1. When Comparison Collapses Without Preprocessing Rules Even In The Same Customer Data

An e-commerce team is running a churn-prediction experiment. The criteria that people first looked at were inputs such as `recent purchase amount`, `visit count`, `acquisition channel`, and `membership tier`.

The problem is that these values are all different kinds of things. Purchase amount is a number in the thousands, visit count may be a single digit, acquisition channel is a string, and for some customers income or region information is empty. If such data are fed directly into the model, some columns become impossible to calculate with, while others gain excessive influence in distance calculations or optimization.

At this point, preprocessing becomes `the rule that changes inputs into a representation the model can handle`. Readers decide by what standard missing values will be filled, whether numeric features need scaling, and how categorical features will be encoded, and then apply the same rules to the training data and test data. It is especially important not to `fit` on the test data, but only to reuse the rules learned on the training data.

The confirmable results appear in the comparison before and after preprocessing and in the data-splitting procedure. If readers inspect differences in model performance before and after scale adjustment, whether string columns were encoded, and whether medians computed from the training data were reused unchanged on the test data, they can explain why preprocessing is not mere cleaning but input-representation design.

If this case is drawn as a flow, it becomes easier to see that preprocessing is not one round of data cleaning, but `the process of setting rules by column condition and reusing the same rules`.

```mermaid
--8<-- "assets/part-04/chapter-07/p4-7-2-mermaid-04-en.mmd"
```

## Criteria For Separating Preprocessing Decisions By Column

### Reading A Small Preprocessing Scene Through A Tiny Example

Consider the following data.

| age | income | city | label |
| --- | --- | --- | --- |
| 29 | 3200 | Seoul | 0 |
| 41 | 6100 | Busan | 1 |
| none | 5800 | Seoul | 0 |
| 35 | none | Incheon | 1 |

The questions the reader sees first here are the following.

1. What should be done about the empty values?
2. `age` and `income` differ greatly in magnitude, so is adjustment needed?
3. `city` is a string, so how should it be represented?

Possible introductory judgments are as follows.

| Column | Preprocessing judgment |
| --- | --- |
| `age` | missing values can be filled with the median |
| `income` | review scale adjustment after filling missing values with the median |
| `city` | fill with the mode or leave as is and then one-hot encode |

This example does not force one single correct answer. The important point is that `different questions are asked for different columns`.

If readers imagine feeding the same data into different models, the judgment becomes even clearer.

| Model candidate | What to pay attention to first in preprocessing |
| --- | --- |
| logistic regression | numeric scaling and categorical encoding |
| k-NN | scale balance before distance calculation |
| decision tree | encoding is needed, but scale is relatively less sensitive |

Therefore, preprocessing is not `a Section that ends after looking only at data`, but also `a Section read again together with model candidates`.

The reason this point matters is that, even with the same data, a `preprocessing + model` combination often becomes one unit of experiment. In other words, saying that logistic regression is being compared often really means a bundle such as `missing-value handling + scale adjustment + encoding + logistic regression` is being compared.

## Checking The Preprocessing Flow Directly

### Looking At Missing Values, Scale, And Encoding In Order Through A Python Example

The example below is a simplified preprocessing flow written in pure Python to show the concept.

Problem situation:

- preprocessing is not magic that finishes at once, but a process that passes through missing-value handling, scale adjustment, and encoding in order

Input:

- a list of rows `rows` with missing values mixed in

Expected output:

- the result after filling missing values
- scaled numeric values
- encoded categorical values

Concepts to check:

- preprocessing is sequential work that changes data into a calculable input matrix
- if the result of each stage is printed separately, the nature of the change becomes clearer

```python
# This example preprocesses model inputs by handling missing values, category encoding, and scale adjustment.
rows = [
    {"age": 29, "income": 3200, "city": "Seoul"},
    {"age": 41, "income": 6100, "city": "Busan"},
    {"age": None, "income": 5800, "city": "Seoul"},
    {"age": 35, "income": None, "city": "Incheon"},
]

def median(values):
    sorted_values = sorted(values)
    n = len(sorted_values)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_values[mid - 1] + sorted_values[mid]) / 2
    return sorted_values[mid]

age_fill = median([row["age"] for row in rows if row["age"] is not None])
income_fill = median([row["income"] for row in rows if row["income"] is not None])

filled_rows = []
for row in rows:
    filled_rows.append({
        "age": row["age"] if row["age"] is not None else age_fill,
        "income": row["income"] if row["income"] is not None else income_fill,
        "city": row["city"],
    })

ages = [row["age"] for row in filled_rows]
incomes = [row["income"] for row in filled_rows]

age_mean = sum(ages) / len(ages)
income_mean = sum(incomes) / len(incomes)

age_std = (sum((x - age_mean) ** 2 for x in ages) / len(ages)) ** 0.5
income_std = (sum((x - income_mean) ** 2 for x in incomes) / len(incomes)) ** 0.5

cities = sorted({row["city"] for row in filled_rows})

processed_rows = []
for row in filled_rows:
    city_vector = [1 if row["city"] == city else 0 for city in cities]
    processed_rows.append({
        "age_z": round((row["age"] - age_mean) / age_std, 2),
        "income_z": round((row["income"] - income_mean) / income_std, 2),
        "city_onehot": city_vector,
    })

print("age_fill   :", age_fill)
print("income_fill:", income_fill)
print("cities     :", cities)
print()
print("processed rows:")
for row in processed_rows:
    print(row)
```

The output is as follows.

```text
age_fill   : 35
income_fill: 5800
cities     : ['Busan', 'Incheon', 'Seoul']

processed rows:
{'age_z': -1.43, 'income_z': -1.61, 'city_onehot': [0, 0, 1]}
{'age_z': 1.39, 'income_z': 1.03, 'city_onehot': [1, 0, 0]}
{'age_z': 0.0, 'income_z': 0.76, 'city_onehot': [0, 0, 1]}
{'age_z': 0.0, 'income_z': -0.18, 'city_onehot': [0, 1, 0]}
```

This example shows three things at once.

- missing values were filled
- numeric values were moved onto a comparable scale
- categorical values were changed into calculable vectors

In other words, preprocessing is not the work of making data prettier, but the process of changing them into a [calculable input matrix](/AiBook/en/reference/concept-glossary-alpha/m/#matrix).

### Looking At How Scale Changes Distance Calculation Through A Python Example

Why scale adjustment matters becomes more intuitive if readers calculate distance.

Problem situation:

- in distance-based models, the judgment of closeness can be distorted depending on which axis has the larger value range

Input:

- original points `point_a`, `point_b`, `point_c`
- points after scale adjustment `scaled_a`, `scaled_b`, `scaled_c`

Expected output:

- original distances `raw_ab`, `raw_ac`
- distances after scale adjustment `scaled_ab`, `scaled_ac`

Concepts to check:

- the same samples can have different distance relationships before and after scale adjustment
- preprocessing is not making model input prettier, but aligning calculation standards

```python
# This example preprocesses model inputs by handling missing values, category encoding, and scale adjustment.
point_a = {"age": 20, "income": 2000}
point_b = {"age": 40, "income": 2200}
point_c = {"age": 21, "income": 8000}

def distance(p, q):
    return ((p["age"] - q["age"]) ** 2 + (p["income"] - q["income"]) ** 2) ** 0.5

raw_ab = round(distance(point_a, point_b), 2)
raw_ac = round(distance(point_a, point_c), 2)

scaled_a = {"age": 0.0, "income": 0.0}
scaled_b = {"age": 1.0, "income": 0.03}
scaled_c = {"age": 0.05, "income": 1.0}

scaled_ab = round(distance(scaled_a, scaled_b), 2)
scaled_ac = round(distance(scaled_a, scaled_c), 2)

print("raw distance A-B   :", raw_ab)
print("raw distance A-C   :", raw_ac)
print("scaled distance A-B:", scaled_ab)
print("scaled distance A-C:", scaled_ac)
```

The output is as follows.

```text
raw distance A-B   : 201.0
raw distance A-C   : 6000.0
scaled distance A-B: 1.0
scaled distance A-C: 1.0
```

This example shows that in the original distance calculation, the income axis almost completely dominates, but after scale adjustment, age and income can be read with more similar weight.

For that reason, preprocessing explanations become important again in Sections such as k-NN, SVM, and linear models.

## Supplement To The Detailed Learning Content

### Names Of Preprocessing Tools Commonly Seen In scikit-learn

There is no need to memorize every name, but it becomes easier to read examples in later Sections if readers at least know what categories exist.

| Category | Name often seen |
| --- | --- |
| missing-value handling | `SimpleImputer` |
| standardization | `StandardScaler` |
| range scaling | `MinMaxScaler`, `MaxAbsScaler` |
| scaling less sensitive to outliers | `RobustScaler` |
| categorical encoding | `OneHotEncoder` |
| pipeline | `Pipeline`, `make_pipeline` |
| column-wise transformation | `ColumnTransformer` |

The goal of this Section is not API memorization. It is first to understand `what representation problem each tool appeared to solve`.

## Checklist

- Can the input problem you are facing now be classified as missing values, scale, or categorical representation?
- Are you separating `fit` and `transform` so that test data do not get mixed into learning preprocessing rules?
- Can you explain preprocessing not as cleaning before the model, but as `reproducible input-representation design`?
- Can you explain that preprocessing is the stage that changes input into a more suitable representation, and that missing values, scale, and categorical representation are different problems?
- Can you explain why `fit` should be done only on training data, and why test data should receive only `transform` under the same rules?
- Can you explain that pipelines and column transformers are structures that keep preprocessing rules repeatable?

## Sources And References

- scikit-learn, `8.3. Preprocessing data`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/preprocessing.html](https://scikit-learn.org/stable/modules/preprocessing.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `8.4. Imputation of missing values`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/impute.html](https://scikit-learn.org/stable/modules/impute.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `8.1. Pipelines and composite estimators`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/modules/compose.html](https://scikit-learn.org/stable/modules/compose.html){: target="_blank" rel="noopener noreferrer" }
- scikit-learn, `12. Common pitfalls and recommended practices`, scikit-learn User Guide, accessed 2026-07-26. [https://scikit-learn.org/stable/common_pitfalls.html](https://scikit-learn.org/stable/common_pitfalls.html){: target="_blank" rel="noopener noreferrer" }
