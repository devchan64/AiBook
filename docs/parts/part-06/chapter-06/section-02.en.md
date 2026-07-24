# P6-6.2 Output Selection Rules That Change Answer Stability and Diversity

> Section ID: `P6-6.2`
> Version: `v2026.07.24`

In P6-6.1, we saw that the basic training objective of an LLM is next-token prediction. But the user experience looks much more complicated than the phrase `predicting the next piece`.

The question naturally continues.

Then what flow does actual generation follow? The answer users see is the result of `candidate distribution calculation` and `candidate selection` continuing many times.

We have already grasped the basic meaning of next-token prediction as `calculating the next-token distribution in the current context`. Here, we focus on how the way we actually pick a token from that distribution changes the answer's stability, diversity, and reproducibility.

## What Output Selection Rules Shake

Output selection rules begin with the following questions.

- How does generation continue one token at a time?
- Why can results differ slightly even with the same input?
- What differences do temperature, sampling, and greedy selection create?

What we need here is not to unpack the decoder's internal attention formula again, but to read `why the result changes depending on how candidates are chosen`. Even with the same candidate distribution, when the selection rule changes, the sentence structure and variation visible to the user change.

Therefore, the core is not `the model knows the answer`, but that `the result changes depending on which candidate is chosen by which rule`. In this section, we deal with the process of deciding which token to actually choose after calculating a probability distribution. Detailed decoding formula comparisons such as beam search and top-p are left for later, and we first look at how greedy, sampling, and temperature change result stability and diversity. Problems that further change the generation path, such as alignment, policy constraints, and external tool connections, are also separated here.

The core intuition is that `generation is a process of repeatedly selecting the next token from a probability distribution`.

We need to distinguish `what the model learned` from `how candidates are chosen during generation` to read the same answer variation more accurately.

## Distinguishing Probability Distributions and Output Selection Rules

- You can explain generation as an iterative selection process.
- You can distinguish greedy selection from sampling.
- You can explain that temperature is not a `model parameter`, but a `setting value that changes selection tendency during generation`.
- You can explain why different answers can appear for the same question.

## Judgment Criteria for Output Selection Rules

Output selection rules are not a problem of changing what the model learned, but a problem of deciding what to actually choose from the calculated candidate distribution. Therefore, we need to read the following criteria separately.

| Judgment Criterion | Question to Check |
| --- | --- |
| Iterative structure | Is generation explained as repeated probability-distribution calculation and candidate selection? |
| Selection method | What do greedy and sampling choose differently from the same distribution? |
| Level of the setting value | Is temperature explained as a value that changes selection tendency during generation, not as a training parameter? |
| Use purpose | Which is needed first in the scene: stability, diversity, or reproducibility? |

## How Does Generation Continue?

In very simple terms, the generation process repeats the following sequence.

1. look at the tokens so far
2. calculate the probability distribution of next-token candidates
3. choose one by some rule
4. append the chosen token
5. repeat until a stopping condition

Looking at this process, generation is closer to `continuing the next choice at each step` than to `pulling out a sentence whose correct answer has already been fully written`.

## Why Can Answers Differ Even to the Same Question?

The model usually does not absolutely decide only one candidate. Several candidates can be plausible.

For example, after a sentence, candidates such as:

- `That is good`
- `That is possible`
- `I will review it`

can all be natural.

If we always choose only the highest candidate here, the result can be more stable, but the expression can become monotonous. Conversely, if we sample from the probability distribution, more diverse results can appear, but instability can also increase.

## How Are Greedy and Sampling Different?

The simplest comparison is as follows.

| Method | Core Idea |
| --- | --- |
| greedy | choose the highest-probability candidate at every step |
| sampling | draw a candidate while reflecting the probability distribution |

Greedy is more predictable, and sampling is more diverse.

You can remember it as follows.

`Greedy chooses the safest single point, while sampling probabilistically chooses among plausible candidates.`

## What Does Temperature Change?

We handled this expression carefully once in Part 1 as well. Many users misunderstand temperature as a `training parameter that changes the inside of the model`. But in a general service-use context, it is safer to explain it as follows.

`Temperature is a setting value that adjusts how sharply or diffusely the candidate probability distribution is read during generation.`

That is:

- low temperature: pushes upper candidates more strongly
- high temperature: lets lower candidates be selected more often

This value usually changes the `selection method during generation`, not the `learned knowledge itself`.

## Which Selection Fits Which Purpose First?

Generation settings are closer to choosing what to prioritize now than to a button that `unconditionally raises or lowers creativity`.

| Scene | What You Want First | Selection Sense to Think of First |
| --- | --- | --- |
| Customer-support draft | consistency, policy compliance | low temperature, conservative selection |
| Code generation | reproducibility, structural stability | low temperature, selection close to greedy |
| Marketing-copy draft | candidate diversity, breadth of expression | sampling, somewhat higher temperature |
| Brainstorming | new combinations, exploration | sampling-centered selection |

In other words, even with the same model, the priority of generation settings changes depending on whether you first need an `accurate and steady answer` or want to `look broadly at several candidates`.

## Stability and Diversity Changed by Selection Rules

If we summarize this so far in the shortest form, it is as follows.

- Training deals with `what to predict as the next token`.
- Generation deals with `what to actually draw from those candidates`.
- Temperature, greedy, and sampling belong to this second problem.

This distinction prevents us from mixing `what the model knows` with `what answer was actually pulled out`.

## If We Draw It Very Simply

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s02-decoding-loop-en.mmd"
```

The core of this diagram is that generation is a combination of `probability distribution calculation` and `selection rule`.

## Cases and Examples

The diagram below groups the three cases in this section around the common question `for what purpose, and how conservatively or diversely, should we choose?`, rather than `choosing randomly`.

```mermaid
--8<-- "assets/part-06/chapter-06/p6-c06-s02-selection-criteria-en.mmd"
```

What we should confirm from this diagram is that generation settings are not one `creativity button`. Even with the same model, when purposes differ, such as customer replies, marketing copy, and code generation, the priorities of `stability`, `diversity`, and `reproducibility` differ, and the criteria for reading greedy, sampling, and temperature also change accordingly.

### Case 1. Customer-Reply Draft

We can think of automatically creating a customer-support draft. In this scene, people usually first use the criterion `does a stable sentence that follows policy come out?`

For example, if one answer first apologizes to a refund inquiry and another immediately states the policy, the content may be correct, but the service tone can feel inconsistent. Also, if one answer states refund conditions first while another explains the submission documents at length first, the customer can become confused about the next action.

If the sampling range is too wide here, tone and guidance order can easily shake even for the same question. Conversely, low temperature and conservative selection rules more often maintain a similar guidance flow such as `policy explanation -> required documents -> next step`.

So the result to check in this case is whether the tone and guidance order do not shake greatly for the same question.

In this scene, `diverse expression` is not necessarily an advantage. What customers want is not answers in several styles, but an experience where, under the same conditions, they receive guidance in a similar structure and the same policy order. In other words, before widening the expression range, the criteria to check first are `is any policy sentence missing?` and `does the next action always appear in the same place?`

| What This Scene Checks First | Problem When It Shakes |
| --- | --- |
| order of apology, policy explanation, and next step | the guidance flow differs by answer and confuses the customer |
| maintaining similar tone under the same conditions | consultation quality looks uneven |
| fixed position for requesting necessary information | next actions such as order number and receipt date become less visible |

### Case 2. Marketing-Copy Draft

Marketing-copy drafts or idea brainstorming are different. In this stage, people usually first check `do several candidates worth comparing appear?` rather than `one safest sentence`. If they keep receiving only the same expression, the candidate range can feel too narrow.

For example, if three drafts are requested and all begin with `easy and fast`, the grammar may be correct, but the team has difficulty comparing directions. Conversely, if emphasis points split into `fast processing`, `reliable shipping`, and `start without complicated procedures`, the team gains material for discussing which message fits better.

In this scene, sampling-style settings that allow a few more plausible candidates can fit better than conservative selection that always chooses only the highest candidate. In other words, the important change is that the criterion moves from finding `one correct sentence` to making `a set of comparable candidates`.

So the result to check in this case is whether several candidates with different emphasis points actually appear.

Here, outputs that are too stable can instead be the problem. If all drafts come out only in the same structure and vocabulary, the team cannot get material for deciding what to compare. Therefore, in this scene, it is better to first ask `do candidates from different angles appear even if they are a little less safe?` and `do the emphasis points actually split?`

| What This Scene Checks First | Problem When It Is Lacking |
| --- | --- |
| number of candidates with different emphasis points | there are no comparable drafts, so one sentence is repeatedly reviewed |
| diversity that does not leave the brand tone | candidates increase, but the quality line can collapse |
| variation in sentence starts and core messages | all phrases begin similarly, narrowing the options |

### Case 3. Code Generation

In code generation, syntax stability and reproducibility are especially important. Here, people first use the criterion `does it answer the same request with a similar structure stably?` rather than `slightly different code every time`.

For example, if the same function-modification request includes `try/except` once and omits it next time, comparison and regression checking become much harder. If the structure changes greatly when generating again after tests have been matched to the first result, more time can be spent tracking generation variation than the actual bug.

If the sampling range is too wide here, exception-handling methods, variable structures, and return order can shake unnecessarily. Conversely, more conservative settings make `same request -> similar structure` happen more often, making it easier to set a debugging baseline.

So the result to check in this case is whether the code structure and exception-handling method do not shake greatly when repeating the same request.

If we group the three cases again by decoding selection criteria, we get the following.

| Situation | What Is Better When Read More Conservatively | What Is Better When More Diverse Candidates Are Allowed |
| --- | --- | --- |
| Customer-reply draft | tone consistency, guidance-order stability | almost nothing; variation is more often a problem |
| Marketing-copy draft | maintaining a minimum quality line | several drafts with different emphasis points |
| Code generation | structural stability, reproducibility | excessive diversity increases debugging cost |

Grouping the three cases shows that generation settings should be read not as a `creativity button`, but as a choice about `how much structural variation to allow`.

## Scenes Where Selection Rules Appear

Even if you do not yet know detailed formulas such as beam search or top-p, you can first distinguish whether the scene you are seeing is a `model does not know` problem or a problem of `what is drawn from already available candidates`. If reply tone and guidance order shake every time for the same inquiry, do not immediately see it only as lack of knowledge; ask whether the candidates are known, but structural variation has grown because of sampling range or temperature. If marketing drafts are too similar to give comparison material, ask whether selection rules that allow more diverse candidates are needed rather than calling it a lack of creativity. If exception-handling methods differ on each run for the same code-modification request, more conservative selection rules may be needed before adding knowledge.

What matters here is not mechanically memorizing `raise or lower temperature`, but first reading `what was learned` and `what is actually being drawn from it` as different problems.

The things often mixed here are as follows.

- It is easy to bundle lack of model knowledge and output-selection variation under the same cause.
- It is easy to judge scenes that need diversity and scenes that need consistency by the same evaluation criteria.
- It is easy to feel temperature as a `value that changes the inside of the model`, while missing that it is actually a setting value that changes output-selection tendency.

Therefore, the phrase `generation is the process of deciding what to actually draw from a candidate distribution` should become a criterion for reading real service scenes.

The purpose of this distinction is not to decide the cause all at once. Instead of flattening it into one sentence, `generation is strange`, it is to briefly distinguish whether the current problem first appears in `selection rule`, `candidate diversity`, or `structural variation` rather than `lack of knowledge`.

## Exercise and Example

The goal of this example is to directly see how `greedy`, `sampling`, `temperature`, and `seed` change next-token selection from probability candidates. We do not bring in the huge vocabulary table inside a real LLM, but place `next-token candidates` and base probabilities at each position and complete a sentence by drawing one token at a time. Therefore, the core is not combining answer templates, but `which candidate piece was actually selected at the current position`.

The input CSV is [p6-6-2-next-token-candidates-en.csv](/AiBook/assets/part-06/chapter-06/p6-6-2-next-token-candidates-en.csv){ .csv-preview }. One row means one candidate token at a specific position. For example, at position 1, `Refund`, `Order`, `Check`, and `Guide` are candidates, and at position 6, time-expression candidates such as ` 7 days`, ` 3 days`, ` 14 days`, and ` 2 business days` appear. The values readers can directly change are `base_probability`, `temperatures`, and `seeds`.

There are three key points to confirm.

- greedy fixes the output by choosing only the highest-probability token at each position.
- sampling creates output diversity because the actually drawn token can differ even with the same candidate distribution.
- fixing the seed makes it possible to recreate the same sampling result, so reproducibility can be checked.

However, seed reproducibility here is reproducibility inside this example, where the local Python random-number generator is fixed. In an actual API service, even with the same seed and the same generation settings, complete determinism may not be guaranteed depending on conditions such as the model serving environment, backend settings, and system fingerprint. This section focuses not on the reproducibility guarantee range of an operational API, but on how observed outputs change when selection rules are fixed or changed.

```python
# This compares which token is actually drawn from the next-token candidate distribution.
import csv
import random
from collections import Counter, defaultdict
from pathlib import Path

candidate_path = Path("docs/assets/part-06/chapter-06/p6-6-2-next-token-candidates-en.csv")
temperatures = [0.3, 1.0, 1.7]
seeds = range(1, 13)

def load_candidates(path):
    candidates_by_step = defaultdict(list)
    with path.open(encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            row["step"] = int(row["step"])
            row["base_probability"] = float(row["base_probability"])
            candidates_by_step[row["step"]].append(row)
    return dict(sorted(candidates_by_step.items()))

def apply_temperature(candidates, temperature):
    adjusted = [
        row["base_probability"] ** (1.0 / temperature)
        for row in candidates
    ]
    total = sum(adjusted)
    return [value / total for value in adjusted]

def pick_top_token(candidates, probabilities):
    top_index = max(range(len(candidates)), key=lambda index: probabilities[index])
    return top_index, candidates[top_index]["candidate_token"]

def greedy_decode(candidates_by_step, temperature):
    tokens = []
    for candidates in candidates_by_step.values():
        probabilities = apply_temperature(candidates, temperature)
        _, token = pick_top_token(candidates, probabilities)
        tokens.append(token)
    return "".join(tokens)

def sample_decode(candidates_by_step, temperature, seed):
    rng = random.Random(seed)
    tokens = []
    top_hits = 0
    trace = []
    for step, candidates in candidates_by_step.items():
        probabilities = apply_temperature(candidates, temperature)
        top_index, top_token = pick_top_token(candidates, probabilities)
        picked_index = rng.choices(
            range(len(candidates)),
            weights=probabilities,
            k=1,
        )[0]
        picked_token = candidates[picked_index]["candidate_token"]
        if picked_index == top_index:
            top_hits += 1
        tokens.append(picked_token)
        trace.append({
            "step": step,
            "picked_token": picked_token,
            "top_token": top_token,
        })
    return "".join(tokens), top_hits, trace

candidates_by_step = load_candidates(candidate_path)
print("candidate_rows =", sum(len(rows) for rows in candidates_by_step.values()))
same_seed_output_1 = sample_decode(candidates_by_step, temperature=1.0, seed=7)[0]
same_seed_output_2 = sample_decode(candidates_by_step, temperature=1.0, seed=7)[0]
different_seed_output = sample_decode(candidates_by_step, temperature=1.0, seed=8)[0]

print("same_seed_reproducible =", same_seed_output_1 == same_seed_output_2)
print("same_seed_output =", same_seed_output_1)
print("different_seed_output =", different_seed_output)

print("\ngreedy outputs by temperature")
for temperature in temperatures:
    print(temperature, greedy_decode(candidates_by_step, temperature))

print("\nsampling summary")
token_positions = len(candidates_by_step)
for temperature in temperatures:
    greedy_output = greedy_decode(candidates_by_step, temperature)
    outputs = []
    top_hits = 0
    first_tokens = []
    for seed in seeds:
        output, hits, trace = sample_decode(candidates_by_step, temperature, seed)
        outputs.append(output)
        top_hits += hits
        first_tokens.append(trace[0]["picked_token"])
    print(
        "temperature =",
        temperature,
        "exact_greedy_matches =",
        f"{sum(output == greedy_output for output in outputs)}/{len(seeds)}",
        "unique_outputs =",
        len(set(outputs)),
        "top_token_rate =",
        round(top_hits / (len(seeds) * token_positions), 2),
    )

print("\nfirst token counts")
for temperature in temperatures:
    first_token_counter = Counter(
        sample_decode(candidates_by_step, temperature, seed)[2][0]["picked_token"]
        for seed in seeds
    )
    print("temperature =", temperature, dict(first_token_counter))

print("\nhigh temperature preview")
for seed in [1, 2, 3]:
    print("seed =", seed, sample_decode(candidates_by_step, temperature=1.7, seed=seed)[0])
```

This example was run with the local `.venv` Python environment and checked against the output in the body.

The execution result example can be read as follows.

```text
candidate_rows = 36
same_seed_reproducible = True
same_seed_output = Refund is order completion based on 7 days within can be submitted.
different_seed_output = Refund requests are shipping receipt after 7 days after is available and the order number is required.

greedy outputs by temperature
0.3 Refund is shipping completion after 7 days within is available.
1.0 Refund is shipping completion after 7 days within is available.
1.7 Refund is shipping completion after 7 days within is available.

sampling summary
temperature = 0.3 exact_greedy_matches = 3/12 unique_outputs = 8 top_token_rate = 0.88
temperature = 1.0 exact_greedy_matches = 0/12 unique_outputs = 12 top_token_rate = 0.48
temperature = 1.7 exact_greedy_matches = 0/12 unique_outputs = 12 top_token_rate = 0.37

first token counts
temperature = 0.3 {'Refund': 11, 'Order': 1}
temperature = 1.0 {'Refund': 8, 'Guide': 1, 'Order': 2, 'Check': 1}
temperature = 1.7 {'Refund': 5, 'Guide': 1, 'Order': 5, 'Check': 1}

high temperature preview
seed = 1 Refund eligibility is customer completion based on 3 days by should be checked.
seed = 2 Guide requests are shipping completion at the time of 14 days by is available and the order number is required.
seed = 3 Refund inquiries are shipping status based on 7 days within should be checked.
```

If we first compress the long execution result, it looks as follows. The first table shows why greedy can stay fixed even when temperature changes.

| temperature | greedy output | Meaning to Read |
| --- | --- | --- |
| 0.3 | `Refund is shipping completion after 7 days within is available.` | output is fixed because only the first-ranked token is selected at every position |
| 1.0 | `Refund is shipping completion after 7 days within is available.` | the first-ranked order does not change even when the base probability distribution is read as is |
| 1.7 | `Refund is shipping completion after 7 days within is available.` | even when the distribution spreads more, greedy still chooses only the first-ranked token |

What matters in this table is why greedy looks `stable`. It is not because the model is smarter, but because the actual selection rule chooses only the first-ranked token at every position.

The second table is the result of repeating sampling 12 times with the predefined seed list. Here, we look not at sentence quality, but at `how often upper tokens are maintained`, `how many different outputs appear`, and `whether the same seed can recreate the result`.

| temperature | Output Exactly Same as Greedy | Number of Different Outputs | Top-Token Selection Rate | Meaning to Read |
| --- | ---: | ---: | ---: | --- |
| 0.3 | 3/12 | 8 | 0.88 | at low temperature, upper tokens are strongly maintained, so output is relatively stable |
| 1.0 | 0/12 | 12 | 0.48 | even with the base distribution, sampling can draw different tokens each run |
| 1.7 | 0/12 | 12 | 0.37 | at high temperature, lower candidates are selected more often, so the selection range widens |

These numbers do not mean that `raising temperature produces a good answer`. In this run, the number of different outputs increases greatly from 0.3 to 1.0, and at 1.7 the drop in top-token selection rate and the expansion of the first-token distribution are clearer than output count. In scenes where stability matters, such as customer support or code generation, this diversity can look like variation; in scenes that need candidate breadth, such as drafting, it can become material for comparison.

The core to read in this example is as follows.

- greedy creates the same token sequence in all three cases.
- sampling changes the token sequence actually drawn even from the same candidate distribution.
- at low temperature, the first-ranked token selection rate is high and stability increases; at high temperature, the distribution widens from the first token and the selection range grows.
- the difference between `same_seed_output` and `different_seed_output` shows that even with sampling, fixing the seed can recreate the same output, while changing the seed can produce a different token sequence under the same settings.
- in other words, temperature is closer to a setting value that changes the balance of stability, diversity, and reproducibility by adjusting `how much the next-token candidate distribution is pressed down or spread out`, rather than a `randomness add button`.

If we view this change as a graph, it looks as follows. The left panel shows how often upper candidates are maintained across all token positions, the middle panel shows where the number of different outputs saturates, and the right panel separately shows how the first-token distribution widens. This graph should be read not as meaning that answer quality improved, but that the actual token-selection range widened from the same candidate distribution.

![Token-selection stability and output diversity by temperature](/AiBook/assets/part-06/chapter-06/temperature-unique-reply-count-en.png)

In the body code, readers can directly change the CSV's `base_probability`, `temperatures`, and `seeds`. For example, if you lower the probability of ` 7 days` at position 6 and raise the probability of ` 14 days`, the greedy output itself can change. If you change `temperature` to 0.2 or 2.0, the degree of upper-token fixation and the first-token distribution also move more extremely. If you increase `seeds`, you can better see how diverse outputs become under the same setting.

## Selection Range Changed by Temperature

The following analogy is useful.

- low temperature: `almost always choose only the most likely candidates`
- high temperature: `consider less likely candidates fairly often too`

But this analogy is not everything. In actual implementations, the shape of the probability distribution itself is adjusted. So it is insufficient to say only that `temperature is a randomness button`.

## Output Differences Made by Selection Rules

What matters in this example is not only that candidate probabilities exist, but that `how to choose from that distribution` changes actual user experience. Even with the same model, response stability, creativity, and reproducibility differ depending on whether we draw conservatively or allow more diverse candidates, so later discussions of settings all sit on top of this selection-rule perspective.

To understand language models as actual user tools, we need the habit of separating `what was learned` from `how actual output is drawn from that learned result`.

- training objective: next-token prediction
- generation procedure: repeated process of selecting actual tokens from a candidate distribution

This distinction lets us separate later topics such as:

- prompting
- decoding settings
- hallucination review
- evaluation

into different problems.

If we reduce this example back into judgment criteria, the following three questions should come first.

| Scene | Question to Answer First |
| --- | --- |
| Why does the answer differ slightly even to the same question? | Is the candidate distribution similar, but the actual selection rule changing? |
| Why are variations a larger problem in customer replies and code generation? | Does this task need consistency and reproducibility before diversity? |
| Why is an answer that is too similar instead a problem in marketing-copy drafts? | Is a selection rule that allows broader candidates needed? |

## Checklist
- Can you explain `what was learned` separately from `what is actually drawn`?
- Can you distinguish greedy, sampling, and temperature from the perspectives of stability, diversity, and reproducibility?
- Are you ready to read the next chapters without mixing model knowledge and output selection rules?

## Sources and References

- Tom B. Brown et al., `Language Models are Few-Shot Learners`, arXiv, 2020, accessed 2026-07-19. [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165){: target="_blank" rel="noopener noreferrer" }
- Ari Holtzman et al., `The Curious Case of Neural Text Degeneration`, ICLR, 2020, accessed 2026-07-19. [https://iclr.cc/virtual_2020/poster_rygGQyrFvH.html](https://iclr.cc/virtual_2020/poster_rygGQyrFvH.html){: target="_blank" rel="noopener noreferrer" }
- OpenAI API Reference, `Create a model response`, generation setting examples, accessed 2026-07-19. [https://developers.openai.com/api/reference/resources/responses/methods/create](https://developers.openai.com/api/reference/resources/responses/methods/create){: target="_blank" rel="noopener noreferrer" }
- Clara Meister et al., `Language Model Behavior: A Comprehensive Survey`, Computational Linguistics, 2024, accessed 2026-07-24. [https://direct.mit.edu/coli/article/50/1/293/118131/Language-Model-Behavior-A-Comprehensive-Survey](https://direct.mit.edu/coli/article/50/1/293/118131/Language-Model-Behavior-A-Comprehensive-Survey){: target="_blank" rel="noopener noreferrer" }. Used to confirm that autoregressive language models calculate a next-token probability distribution and use selection methods such as greedy, temperature sampling, top-k, and nucleus sampling in open-ended generation.
- OpenAI Help Center, `Best practices for prompt engineering with the OpenAI API`, accessed 2026-07-24. [https://help.openai.com/en/articles/6654000-how-to-prompt-the-models](https://help.openai.com/en/articles/6654000-how-to-prompt-the-models){: target="_blank" rel="noopener noreferrer" }. Used to confirm that temperature is connected to lower-probability token selection frequency, randomness, and conservative settings for factual use cases.
- OpenAI Cookbook, `How to make your completions outputs consistent with the seed parameter`, accessed 2026-07-24. [https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter](https://developers.openai.com/cookbook/examples/reproducible_outputs_with_the_seed_parameter){: target="_blank" rel="noopener noreferrer" }. Used to confirm that seed is a device for getting mostly consistent outputs under the same settings, but does not guarantee complete determinism.
