# P5-15.3 How Sampling Pulls Actual Outputs from Candidate Distributions

> Section ID: `P5-15.3`
> Version: `v2026.08.03`

When recording sampling results, separate `candidate_distribution`, `selection_rule`, `temperature_setting`, `top_k_or_top_p`, `selected_output`, and `variation_count`. This distinction lets you naturally connect what the model considered plausible and what was actually drawn to the generation-setting explanations in Part 6.

In P5-15.2, we saw that a generative model does not memorize and return one correct answer, but keeps the relative plausibility of possible output candidates as a candidate distribution. The next question naturally follows.

If a generative model can produce several plausible answers, how does it actually choose one answer?

Sampling is the process by which the model takes out one actual output at a time from several candidates it judged plausible, and this method directly affects the diversity and stability of the result.

This is the main intuition for text generation, where a model samples from token candidates. Image diffusion models also use the word `sampler`, but it means a numerical procedure that moves to the next denoising latent state, not a choice from a visible list of complete-image candidates. Both cases distinguish a learned distribution from the procedure that produces an actual artifact, but text controls such as temperature, top-k, and top-p are not the same controls as an image diffusion model's seed, sampler, and steps.

## Text Sampling and Diffusion Sampling

| View | Text generation | Image diffusion |
| --- | --- | --- |
| item handled at one step | next-token candidates | noisy latent representation |
| main control examples | temperature, top-k, top-p | seed, sampler, steps, guidance |
| result to compare | wording and structural variation | restoration path and image variation |

Both can change visible results, but the comparison must begin by keeping these different roles separate.

This distinction is the minimum safeguard against applying text-generation settings directly to image-generation behavior.

When the model’s scores and the actual output choice need to be separated again, reread the glossary entry on [sampling](/AiBook/en/reference/concept-glossary-alpha/s/#sampling).

## Candidate Distributions and Actual Output Choice Are Different

The core point to hold first in this section is that `the quality of a generative model depends not only on what it learned, but also very strongly on which candidates it actually samples`. If P5-15.2 looked at how the model keeps the relative plausibility of candidates, P5-15.3 looks at the procedure that pulls actual outputs from those already calculated candidates.

| What is read in this section now | What is read more in later Parts |
| --- | --- |
| after the candidate distribution is calculated, by what feel the actual output is chosen | how top-k, top-p, and temperature are handled in more detail as product-setting language |
| why the choice between diversity and stability changes the result | how generation settings adjust response style, length, and variation width |
| how seed, sampler, and steps connect restoration paths to image variation in diffusion | how to record Stable Diffusion components and conditioning separately |

The detailed differences of top-k, top-p, and temperature are made concrete again in P6-5.2. Here we establish the sense that `the stage of calculating the candidate distribution` and `the stage of selecting the actual output` are different, and that output quality depends on both.

For example, consider the beginning of an operation-notice sentence again.

- `Batch inspection result`

After this, several follow-up phrases can continue naturally, such as `reverification is required`, `resume after supervisor confirmation`, `remeasure in 10 minutes`, or `for now it remains normal by the current standard`.

Calculating this candidate distribution and sampling one phrase as the actual guidance sentence are not the same thing. Sampling is this second stage.

## What Does Sampling Do

The core of sampling is that it is a selection procedure that prioritizes higher candidates while still leaving room for other candidates to become actual outputs too.

`Sampling is the procedure that lets the model choose candidates it judged more plausible more often, while still allowing other candidates to become the actual output in some cases.`

That is, sampling deals with the problem between the following two extremes.

- a method that always chooses only the highest candidate
- a method that mixes possible candidates too randomly

In generative AI, the balance between these two is important.

At the introductory stage, it is enough if we distinguish only the following three methods.

| Method | Intuition to hold first |
| --- | --- |
| argmax | always chooses only the highest candidate |
| sampling | chooses higher candidates more often but allows other candidates too |
| temperature adjustment | makes the candidate distribution be read more conservatively or more diversely |

This difference becomes clearer when we place side by side the candidate distribution and the actual choice frequency. First, if we look at how much weight the model gives to each candidate, one highest candidate clearly exists, but the other candidates are not all zero either.

![Relative weights of candidate phrases](/AiBook/assets/part-05/chapter-15/sampling-candidate-weights-en.svg)

Then, if we look at the choice frequency when actually sampling 20 times, the highest candidate appears most often, but the lower candidates do not disappear completely and can still remain as some of the results.

![Choice counts from 20 rounds of sampling](/AiBook/assets/part-05/chapter-15/sampling-choice-counts-en.svg)

The key point in this graph is that sampling is not `picking anything at random`. It should be read as a selection procedure that samples actual outputs based on the weights the model gave to each candidate, but does not fix only one candidate as argmax does.

## Why Must Diversity and Stability Be Seen Together

If sampling is not used at all and only the highest candidate is repeatedly chosen, the output can look stable. But the result can also feel too monotonous or repetitive.

Conversely, if candidates are allowed too broadly, output diversity can increase, but the sentence can suddenly become unnatural or the meaning can start to drift.

`Generative quality is not only a question of correctness, but also a question of balance between diversity and stability.`

## Situations Where We First Look at Which Balance

When reading sampling, it is safer to first ask not `always more diverse` or `always more conservative`, but `what should be prioritized more right now`.

| Situation | Standard looked at first | Choice feel to recall first |
| --- | --- | --- |
| inspection-result guidance phrase | repeatability, minimizing instability | choosing mainly the highest-probability candidates |
| explanatory field-support response | correctness, structural stability | relatively conservative sampling |
| operation-message drafts, response-message variants | breadth of candidates, expression diversity | allowing more diverse candidates |
| image concept exploration | scene variation, style range | allowing broader sampling |

That is, sampling is safer to read not only as `a device that increases fun`, but as a choice that decides which side to prioritize more between consistency and diversity of the output.

## Why Can Even the Same Model Produce Different Results

Even for the same model, the result can change if the following conditions change.

- up to which candidates are left
- how sharply the probability distribution is read
- whether only the highest candidate is chosen, or several candidates are allowed

Because of this, users often feel that `the model changed`, but sometimes what actually changed was only the output-selection strategy.

This viewpoint becomes very important later when reading token-level generation and prompt experiments.

## If We Draw the Flow Very Simply

```mermaid
--8<-- "assets/part-05/chapter-15/sampling-selection-flow-en.mmd"
```

The result to confirm in this diagram is that the stage that calculates `model scores` and the stage that decides which candidate to sample as the actual output are different from one another.

Even when the same candidate scores are given, the user experience can change immediately depending on the final selection rule.

| The same prefix and candidate scores | Result that appears first when only the highest candidate is chosen | Result that appears first when several candidates are allowed |
| --- | --- | --- |
| after `Batch inspection result`, all of `reverification is required`, `resume after supervisor confirmation`, and `remeasure in 10 minutes` are possible | it becomes easy to repeat only one most conservative sentence | the inspection context can remain while the action phrasing and sentence length vary a little |
| a field-support response explains `restart order after shutdown due to pressure anomaly` | it becomes easy to repeat only the same step sentence every time | the core safety procedure can remain while the position of warning phrases and the explanation length vary |
| an image is generated from the prompt `stainless mixing tank with side valve and warning beacon` | fixing seed, sampler, and steps makes comparable restoration paths possible | changing seed or sampler can preserve core conditions while lighting, viewpoint, and pipe placement vary |

That is, `which candidate the model judged highly` and `which one was actually sampled as the output` are not the same problem.

## Cases and Examples

### Representative Case. Inspection-Result Guidance Phrase

`Batch inspection result`

People usually first think of `one most reasonable response phrase`. So it is easy to think that guidance-phrase generation also only needs to choose the one highest candidate. But in real operation sentences, several candidates such as `reverification is required`, `resume after supervisor confirmation`, and `remeasure in 10 minutes` can all be natural, and which one fits better can change depending on the inspection state. For example, if an alert is repeated, `reverification is required` sounds natural, while if field action has already begun, `resume after supervisor confirmation` may sound more natural. If we always choose only the highest candidate, the guidance phrase becomes fixed in the same tone every time. Conversely, if candidates are allowed too broadly, even action phrases less suited to the field context can jump out. Sampling is the stage that controls which candidate will actually be sampled between those extremes.

So the result to confirm in this case is that, even while the prefix `Batch inspection result` stays the same, the actual guidance phrase can vary slightly depending on the operational situation, and sampling is exactly the stage that controls that width of choice.

The same viewpoint extends directly to field-support responses and image-generation prompts. But the core point to hold in this section is not the domain name, but `whether, given the same candidate distribution, the actual output that is sampled changes the width of variation in the result`.

| Case | Candidates the model can hold | What happens if we choose too narrowly | Result to confirm when broader allowance is used |
| --- | --- | --- | --- |
| inspection-result guidance phrase | response candidates such as `reverification is required`, `resume after supervisor confirmation`, and `remeasure in 10 minutes` | the same action phrase repeats every time | does variation appear in the response phrasing while the operational context is still kept? |
| field-support response | short step-type, warning-first, explanation-expanded answer candidates | the same length and structure repeat every time | does the format of the explanation vary while the core safety procedure is still kept? |
| image generation | tank angle, pipe layout, warning-beacon emphasis, viewpoint candidates | the resulting scene becomes too similar every time | does scene variation appear while the core prompt is still preserved? |

| Standard that is easy for a person to see first | Standard to reread from the sampling viewpoint |
| --- | --- |
| it is easy to feel that the one candidate given the highest score by the model immediately becomes the final output | score calculation and actual selection are different stages, so even with the same distribution the result changes depending on what selection rule is used |
| if the result changes every time, it is easy to feel only that the model is unstable | it may be the result of allowing different choices inside the candidate distribution, so diversity and stability must be seen together |
| it is easy to understand sampling as simply adding randomness | the actual core is that it sets how strongly to prioritize the high candidates while allowing other candidates within some range |

If we place the three cases together, the core of sampling does not lie in re-explaining `what the model learned`, but in adjusting `which candidate among several will actually be sampled as the output` to fit the operation context.

If we pause once here and briefly fix `when the explanation that the model learned a candidate distribution is not enough, and the actual output-selection procedure needs to be pulled out separately`, then the later discussion of temperature, top-k, and top-p feels less sudden.

| Question to recall first | Why the sampling viewpoint is needed first | What continues in later Parts |
| --- | --- | --- |
| why can even the same model produce slightly different results each time? | because, apart from the learned candidate distribution, a separate procedure exists that samples the actual output | temperature, top-k, and top-p adjustment |
| why should we not always choose only the highest-score candidate? | because stability rises, but expression diversity and situational fit can shrink too much | product settings and user-experience control |
| why is output quality not only a model problem? | because what has been learned and what has actually been chosen together create the result | response style, length, and variation-width design |

## Practice and Example

### Example 1. Checking Temperature and Top-k with Fixed Logits

The goal of this example is to check, before running an actual LLM, how temperature and top-k change the actual selection distribution from already calculated candidate scores, or logits. Real LLMs handle many more token candidates internally, but a small candidate set is enough at this level to separate `scores -> probabilities -> actual choices`.

```python
# Compare candidate probabilities, choice counts, and entropy while changing only the sampling setting for fixed logits.
import math
import random

import numpy as np

candidates = [
    "Reverification is required.",
    "Resume after supervisor confirmation.",
    "Remeasure in 10 minutes.",
    "Remain normal by the current standard.",
    "Restart immediately.",
]
logits = np.array([3.2, 2.4, 1.7, 0.6, -0.4])

experiments = [
    ("argmax", 0.0, None),
    ("temperature_0.7", 0.7, None),
    ("temperature_1.4", 1.4, None),
    ("top_k_3_temperature_1.0", 1.0, 3),
]


def softmax(values, temperature):
    scaled = values / temperature
    shifted = scaled - np.max(scaled)
    exp_scores = np.exp(shifted)
    return exp_scores / exp_scores.sum()


def apply_top_k(probabilities, k):
    if k is None:
        return probabilities
    kept_indices = np.argsort(probabilities)[-k:]
    filtered = np.zeros_like(probabilities)
    filtered[kept_indices] = probabilities[kept_indices]
    return filtered / filtered.sum()


def probabilities_for(temperature, top_k):
    if temperature == 0.0:
        probabilities = np.zeros_like(logits, dtype=float)
        probabilities[int(np.argmax(logits))] = 1.0
        return probabilities
    return apply_top_k(softmax(logits, temperature), top_k)


def entropy_bits(probabilities):
    non_zero = probabilities[probabilities > 0]
    if len(non_zero) <= 1:
        return 0.0
    return -sum(p * math.log2(p) for p in non_zero)


for label, temperature, top_k in experiments:
    probabilities = probabilities_for(temperature, top_k)
    random.seed(15)
    choices = random.choices(
        range(len(candidates)),
        weights=probabilities,
        k=40,
    )
    counts = [choices.count(index) for index in range(len(candidates))]

    print(f"[{label}]")
    print("probabilities =", [round(float(value), 3) for value in probabilities])
    print("counts =", counts)
    print("entropy_bits =", round(entropy_bits(probabilities), 3))
    print("top_choice =", candidates[int(np.argmax(probabilities))])
    print()
```

```text
[argmax]
probabilities = [1.0, 0.0, 0.0, 0.0, 0.0]
counts = [40, 0, 0, 0, 0]
entropy_bits = 0.0
top_choice = Reverification is required.

[temperature_0.7]
probabilities = [0.682, 0.217, 0.08, 0.017, 0.004]
counts = [24, 8, 5, 2, 1]
entropy_bits = 1.277
top_choice = Reverification is required.

[temperature_1.4]
probabilities = [0.467, 0.264, 0.16, 0.073, 0.036]
counts = [18, 7, 7, 4, 4]
entropy_bits = 1.89
top_choice = Reverification is required.

[top_k_3_temperature_1.0]
probabilities = [0.598, 0.269, 0.133, 0.0, 0.0]
counts = [22, 8, 10, 0, 0]
entropy_bits = 1.341
top_choice = Reverification is required.
```

The first thing to notice is that `top_choice` stays the same across all four settings. But the actual selection distribution changes substantially. `argmax` chooses one candidate all 40 times, `temperature_1.4` leaves more room for lower candidates, and `top_k_3_temperature_1.0` removes the bottom two candidates from the selectable set.

![Candidate probabilities by sampling setting](/AiBook/assets/part-05/chapter-15/sampling-control-probabilities-en.png)

![Choice counts over 40 draws](/AiBook/assets/part-05/chapter-15/sampling-control-counts-en.png)

So the conclusion is not `higher temperature is always better`. Even with the same logits, the spread of the candidate distribution and actual choice counts change when the selection rule changes. Generation settings should therefore be read as the stage that controls `what is sampled from what the model knows`, not as the model's knowledge itself.

### Optional Example. Observing Actual LLM Output Changes with Ollama

The previous example used fixed logits to make the selection rule reproducible. If Ollama and a local model are available, the next example lets us observe that even with the same prompt, changing generation settings can change the stability and variation width of the actual output. Part 1 did not ask the reader to call an LLM from Python, but by this point we have already covered generative models and sampling, so it is reasonable to confirm the idea through real outputs.

This section is not trying to teach API usage as the main topic. The point is to see that `the model calculates candidates` and `one actual sentence is pulled from those candidates` are separate stages, and that generation settings can change the user experience of the second stage.

To run the example, Ollama must be running locally, and the `MODEL` value in the code must be changed to a model installed in your own environment. Ollama provides its local API at `http://localhost:11434/api` by default, and `/api/generate` is the endpoint that generates a response to a prompt.

Before looking at the code, it is enough to hold the four values below.

| Point to confirm | Value to look at directly in the example | Why it matters |
| --- | --- | --- |
| how many times the same prompt is run | `RUNS_PER_SETTING` | keeps us from judging the model's tendency from just one output |
| how the generation setting is changed | `temperature` | lets us compare expression stability and variation width at low and high values |
| how much the response is limited | `num_predict` | keeps the output from becoming so long that the observation point becomes unclear |
| what to inspect in the actual output | `response` | checks whether sentence order, warning placement, and expression width change even under the same request |

Before looking at the code, it helps to predict where the first differences will appear under the same prompt.

| Comparison point | Result to expect first at low temperature | Result to expect first at high temperature |
| --- | --- | --- |
| sentence structure | similar order and wording are more likely to repeat | the core may remain, but expression order or sentence length can vary |
| warning phrase | safety-check wording may repeat more stably | the position or wording of the warning can change |
| review burden | easier to compare, but possibly monotonous | gives more varied drafts, but also increases the differences to review |

The prompt is deliberately kept as a short operational guidance scene. Change the model name to one installed in your own Ollama environment. `temperature` and `RUNS_PER_SETTING` are the variables the reader should try changing.

```python
# Run the same prompt several times through Ollama's local API and observe how generation settings change the outputs.
import json
import textwrap
import urllib.error
import urllib.request

OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"
MODEL = "gemma3"  # Change this to a model installed in your Ollama environment.
RUNS_PER_SETTING = 2

PROMPT = """
Write an operational guidance message in no more than two sentences for a field worker.

Situation:
The batch inspection result shows that pressure fluctuation has decreased, but interlock and sensor status must be checked again before restart.

Conditions:
- Do not assert unseen causes.
- Include the action to check before restart.
- Avoid exaggerated wording and write sentences that can be reviewed.
""".strip()

experiments = [
    {
        "label": "stable_temperature",
        "options": {
            "temperature": 0.1,
            "num_predict": 80,
        },
    },
    {
        "label": "wider_temperature",
        "options": {
            "temperature": 0.9,
            "num_predict": 80,
        },
    },
]

def generate_with_ollama(label, options, run_index):
    payload = {
        "model": MODEL,
        "prompt": PROMPT,
        "stream": False,
        # This is the variable to manipulate in the example. Changing temperature can change the output-selection width.
        "options": options,
    }
    request = urllib.request.Request(
        OLLAMA_GENERATE_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.URLError as error:
        print("Could not connect to Ollama.")
        print("Check whether Ollama is running and whether MODEL is an installed model name.")
        print("error =", error)
        return

    generated = data.get("response", "").strip()
    one_line = " ".join(generated.split())

    print(f"[{label} / run {run_index}]")
    print("options =", options)
    print(textwrap.shorten(one_line, width=220, placeholder=" ..."))
    print()

for experiment in experiments:
    for run_index in range(1, RUNS_PER_SETTING + 1):
        generate_with_ollama(
            experiment["label"],
            experiment["options"],
            run_index,
        )
```

The result will vary depending on the model, version, local environment, and time of execution. The important point is not to match one specific sentence as the answer, but to observe that generation settings can change the output experience even with the same prompt and the same model.

| Output to look at first | What this output means | What changes if you vary it |
| --- | --- | --- |
| response from `stable_temperature` | shows whether a relatively stable sentence structure appears at low temperature | if `temperature` is lowered further, repeatability may increase but expression width may shrink |
| response from `wider_temperature` | shows whether expression order, sentence length, and word choice move more at high temperature | if `temperature` is raised further, variation may increase but review burden can also grow |
| two runs under the same setting | shows why one output is not enough to judge a generation setting | increasing `RUNS_PER_SETTING` makes it easier to compare repeatability and variation width |

- if the two low-temperature responses come out with almost the same structure, read it as a case where the candidate-selection width has narrowed and stability has increased
- if sentence order or wording changes more at high temperature, read it as a case where the candidate-selection width has widened and draft diversity has increased
- however, a higher temperature does not always mean a better answer; in field guidance, a human must check again whether safety checks, non-assertion of unseen causes, and pre-restart actions are still included
- therefore, the conclusion of this example is not `higher settings are creative`, but `the output-selection procedure changes the actual sentence experience, and the result must be reviewed again`

This result should not stop only at `they are different`. It should lead directly into checking which values shake the balance between diversity and stability.

| Output signal seen first | Change to try right now | Conclusion not to rush to from this example alone |
| --- | --- | --- |
| sentences almost repeat at low temperature | raise `temperature` gradually and see where expression width starts to widen | do not conclude that high repeatability always means high quality |
| sentences become more varied at high temperature | increase `RUNS_PER_SETTING` under the same condition and observe more variation | do not conclude that diversity directly means correctness or safety |
| an output omits an important checking action | make the prompt conditions clearer or lower temperature | do not assume that prompt and settings remove the need for review |

If we go one step further here, it is better to read this section's example as `an actual LLM output-selection sensitivity experiment`.

| Value to change first | What we get to see shaking | Result to confirm first in this section |
| --- | --- | --- |
| raise `temperature` from 0.1 to 0.9 | how much the expression order and word choice change under the same prompt | even if variation widens, are the core safety conditions still kept? |
| lower or raise `num_predict` | whether output length and omitted information change | does a shorter output become easier to review while still not dropping important conditions? |
| remove `Do not assert unseen causes` from the prompt conditions | whether the model more easily asserts a cause | output diversity and risky assertions must be reviewed together |

That is, the example in this section should not remain at the hand-calculation intuition that `argmax and sampling are different`. It should let us see in actual local LLM outputs how generation settings and prompt conditions shake operational messages and follow-up action phrasing.

Language models usually calculate the plausibility of the next token, and image-generation models gradually construct possible visual patterns. At that point, the actual output appears by going through the calculated distribution and the selection strategy.

- token and tokenization
- next-token prediction
- generation settings such as temperature, top-k, and top-p
- why output changes according to the prompt

## Checklist

- Can you explain that sampling is the process that chooses the actual output among learned candidates?
- Can you explain how the choice between diversity and stability affects the result?
- Can you explain that the generative model calculates the plausibility of candidates, and sampling chooses the actual output among them?
- Can you say that a generative problem may not be one that has only one correct answer?
- Can you explain that the balance between diversity and stability is important in generative quality?
- Can you explain sampling not only as `adding randomness`, but as `the procedure that selects the actual output from the candidate distribution`?
- Can you distinguish argmax and sampling as `fix only the highest candidate` versus `choose high candidates more often but still allow other candidates`?
- When reading the generation settings in later Parts, are you ready first to see `model score calculation` and `actual output selection` as different stages?

## Sources and References

- Ian Goodfellow, Yoshua Bengio, Aaron Courville, `Deep Learning`, MIT Press, 2016, checked on 2026-06-29. [https://www.deeplearningbook.org/](https://www.deeplearningbook.org/){: target="_blank" rel="noopener noreferrer" }
- Christopher D. Manning, Hinrich Schutze, `Foundations of Statistical Natural Language Processing`, MIT Press, 1999, checked on 2026-07-19. [https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/](https://mitpress.mit.edu/9780262133609/foundations-of-statistical-natural-language-processing/){: target="_blank" rel="noopener noreferrer" }
- Daniel Jurafsky, James H. Martin, `Speech and Language Processing` draft materials, checked on 2026-07-19. [https://web.stanford.edu/~jurafsky/slp3/](https://web.stanford.edu/~jurafsky/slp3/){: target="_blank" rel="noopener noreferrer" }
- Ollama, [Introduction](https://docs.ollama.com/api/introduction){: target="_blank" rel="noopener noreferrer" }, Ollama API documentation, checked on 2026-07-22.
- Ollama, [Generate a response](https://docs.ollama.com/api/generate){: target="_blank" rel="noopener noreferrer" }, Ollama API documentation, checked on 2026-07-22.
