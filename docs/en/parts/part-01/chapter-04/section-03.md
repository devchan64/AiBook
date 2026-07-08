# P1-4.3 Features, Representations, and Parameters

> Section ID: `P1-4.3`
> Version: `v2026.07.07`

Section 4.2 organized what we want to show the model and what we want back from it: `input`, `output`, and `data`. This section moves one step inward and asks how that input looks inside the model when actual computation begins.

The central question is whether the model sees the input exactly as it is, or whether it turns the input into values that are easier to compute over.

This section introduces `feature`, `representation`, and `parameter` at an introductory level. The goal is to fix the positions of the terms needed to read a model.

## Scope of This Section

This section is not about building a model from scratch. The choice of algorithm, the structure of a model, and the full learning procedure are revisited later in Part 4 and Part 5.

The smaller question here is enough: when we look at a model that is already defined, what values does the input become, and what internal values are used to compute the output?

## Goal of This Section

- Understand a feature as a value the model actually uses for computation.
- Understand a representation as the result of turning original data into a form that is easier to compute over.
- Understand a parameter as an adjusted value inside the model used in output computation.
- Distinguish original input, feature, representation, and parameter from each other.
- Prepare to connect this to problem definition in 4.4.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| a feature is an input value actually used in computation | This shows that the human-readable original sentence and the model’s computational values are not always the same. | Distinguish the original sentence from the clues used for computation. |
| a representation is the result of turning data into a form that is easier to compute over | This becomes the basis for later explanations of deep learning and embeddings. | Understand that the same data may be transformed into different internal forms. |
| a parameter is an adjusted value inside the model | This connects directly to later explanations of training and inference. | Distinguish input values from internal values that get adjusted. |

## Original Input Is Often Hard to Compute Over Directly

Take the customer-support example again.

> If the delivery does not arrive by tomorrow, I will cancel it.

A human reader sees many clues together.

| Clue visible to a human | Possible meaning |
| --- | --- |
| delivery | a delivery-related issue |
| by tomorrow | a time condition |
| if it does not arrive | possible delay |
| I will cancel it | cancellation intent or pressure |

But a model does not understand that sentence in exactly the same way. For computation, the input must be turned into some form of values. This is where `feature` and `representation` appear.

> original input -> feature or representation -> model computation -> output

The key distinction here is between `the original text as written` and `the values the model actually computes with`.

## A Feature Is an Input Value Used by the Model

Google’s Machine Learning Glossary describes a feature as an input variable to a machine-learning model. In the support-message example, very simple features might look like this.

| Original input | Example feature |
| --- | --- |
| `I want a refund.` | whether the word `refund` appears |
| `When will the delivery arrive?` | whether the word `delivery` appears |
| `The item arrived broken.` | whether damage-related expressions appear |
| `I want to change the address.` | whether address-change expressions appear |

These features can be designed by people in advance.

| Message sentence | `refund` clue | `delivery` clue | `damage` clue | label |
| --- | ---: | ---: | ---: | --- |
| `I want a refund.` | 1 | 0 | 0 | refund |
| `When will the delivery arrive?` | 0 | 1 | 0 | delivery |
| `The item arrived broken.` | 0 | 0 | 1 | exchange |

At this stage, it is enough to understand a feature as `an input value the model uses for computation`.

## A Feature Is Not the Same as the Original Input

This distinction matters.

| Distinction | Example |
| --- | --- |
| original input | `The item I received yesterday was damaged, and I want it replaced.` |
| human-designed features | damage clue present, replacement clue present |
| output label | exchange or reshipment |

The original sentence is natural language. Features are values extracted from that sentence so the model can use them for computation.

Without this distinction, it is easy to imagine that `if we feed data to the model, it will simply understand it on its own`. But the actual question is what values are extracted, what clues are kept or dropped, and in what form the input reaches the model.

## A Representation Is the Result of Making Data Easier to Compute Over

Google’s glossary describes `representation` as the process of mapping data to useful features. In this section, we read it more broadly as `the result of transforming original data into a form the model can compute over more easily`.

The same support sentence can be turned into different kinds of representation.

| Representation style | Example | Strength | Limit |
| --- | --- | --- | --- |
| keyword features | `delivery` present, `cancel` present | simple and easy to explain | may miss context |
| numeric features | sentence length, number of exclamation marks | easy to combine with table data | may not capture meaning well |
| categorical features | message channel: app, email, phone | easy to connect with business data | does not carry sentence meaning itself |
| learned representation | convert the sentence into an internal vector | better at handling similarity and context | hard to read directly |

The point is simple: how we represent the input determines what kind of world the model can see.

## Good Representations Reveal Differences That Matter

Bengio, Courville, and Vincent explain in their review of representation learning that the success of machine-learning algorithms depends heavily on data representation.

Consider these two sentences.

> I want to cancel the payment.  
> If delivery does not arrive, I will cancel it.

Both contain the word `cancel`, but the first is closer to payment cancellation or refund, while the second is closer to delivery delay with a conditional cancellation intent.

| Representation | Is it easy to distinguish the two sentences? | Why |
| --- | --- | --- |
| whether `cancel` appears | difficult | both contain the same word |
| check both `delivery` and `cancel` clues | somewhat better | the delivery context becomes visible |
| use a broader sentence-level representation | can become much better | condition, intent, and context can be reflected together |

Good representations help the model see the differences that matter for the task.

## Parameters Are Adjusted Values Inside the Model

If features and representations are closer to `the form of the values entering the model`, parameters are the values adjusted inside the model.

Google’s glossary describes parameters as the weights and biases that a model learns during training. At this level, we can understand a parameter like this:

> parameter = an adjustable internal value the model uses when turning input into output

One common term here is `weight`. A weight is a kind of parameter that controls how strongly some input value or internal value affects the output.

We can simplify the support-message example like this.

| Feature | How strongly connected to the refund output? | How strongly connected to the delivery output? |
| --- | ---: | ---: |
| `refund` clue | strong | weak |
| `delivery` clue | weak | strong |
| `cancel` clue | medium | medium |

This is not a real parameter table. It is only an intuition for what parameters do.

## Parameters, Hyperparameters, and Generation Settings Belong to Different Levels

Beginners often get confused because values like `temperature`, `top-p`, and `max tokens` are also sometimes called parameters.

But these are not the same as model parameters. Google’s glossary describes `temperature` as a hyperparameter that adjusts randomness in model output. In LLM use, it is better read as a generation setting that controls how the learned model chooses output.

| Distinction | Example | Who sets it? | When is it used? | Meaning |
| --- | --- | --- | --- | --- |
| model parameter | weight, bias | learned during training | internal model computation | a value adjusted by learning and stored inside the model |
| hyperparameter | learning rate, batch size | person or tuning process | training setup | a condition that shapes the learning process |
| generation setting | temperature, top-p, max tokens | user or service setting | inference and generation | a setting that changes how the trained model chooses output |

So when this section says `learning changes parameters`, it means model parameters in the first sense.

## What to Remember from This Section

The safest first distinction is this:

> feature = the clue value used in computation  
> representation = the transformed internal form of data  
> parameter = the internal adjusted value used to compute output

Once this is clear, we can move to 4.4 and ask a larger question: how does the way we define the problem determine what kind of model we need?

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, 2012-06-25, accessed 2026-06-22.
