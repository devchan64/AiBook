# P1-4.3 Features, Representations, and Parameters

> Section ID: `P1-4.3`
> Version: `v2026.07.20`

Section 4.2 examined the relation among `input`, `output`, and `data`, or what we want to show the model and what we want back from it. This section explains what kind of computational material that input becomes inside the model.

The central question is whether the model sees the input exactly as it is, or whether it changes the input into values that are easier to compute over.

This section organizes `feature`, `representation`, and `parameter` at an introductory level. Building on the customer-support example from 4.2, the focus is on fixing the positions of the terms needed to read a model.

In Part 1, this section sets the basic standard for reading `feature`, `representation`, and `parameter` from the viewpoint of model computation. The contrast between `representation learning` and `rule-based approaches` was fixed earlier in 3.3, and the basic structure of `input`, `output`, `data`, `example`, and `label` was fixed in 4.2. Here the narrower focus is on how `input turns into computational material inside the model`.

The question needed here is smaller. When we look at a model that is already defined, what values does the input turn into, and what internal values are used to compute the output?

The goal here is not the procedure for making a model, but the basic vocabulary needed to read the flow of computation inside a model.

## Turning Input into Computational Material

- Understand a feature as a value the model uses from the input.
- Understand a representation as the result of turning original data into a form that is easier to compute over.
- Understand a parameter as an adjusted value inside the model used in output computation.
- Distinguish original input, feature, representation, and parameter from each other.
- Prepare to move into the relation between problem definition and model choice in 4.4.

## Three Standards

When reading internal model terms, the following three points should be separated first.

| Standard | Why it matters | Level of understanding needed in this section |
| --- | --- | --- |
| a feature is an input value the model actually uses in computation | This shows that the original sentence and the computational value can differ. | Distinguish that the sentence a person reads and the numeric clue the model uses are not always the same. |
| a representation is the result of turning data into a form that is easier to compute over | This becomes a bridge to later explanations of deep learning and embeddings. | Keep the point that the same data can be turned into different representations. |
| a parameter is a value adjusted inside the model | This becomes a key connection for understanding later explanations of learning and inference. | Distinguish that it is not the input itself, but internal model values, that get adjusted. |

`feature`, `representation`, `parameter`, `vector`, and `activation` all appear in computation, but they point to different places.

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| feature | an input value the model actually uses | a computational clue extracted from the original input |
| representation | the result of changing data into an easier form for computation | the internal input form the model sees |
| parameter | an adjusted value inside the model | an internal criterion that affects output computation |
| vector | a bundle of numbers arranged side by side | a common format that carries a representation |
| activation | an intermediate value produced during computation | one moment in the process where a representation changes through layers |

Here they are read with the following position split: `feature is an input clue`, `representation is the changed form`, `parameter is the internal criterion`, `vector is a numeric bundle`, and `activation is an intermediate computed value`.

The part that is especially easy to confuse here is `feature` versus `representation`. In this section, it is safest to read a `feature` as a value on the input side that the model directly uses, and a `representation` as the overall form or result that turns the original data into such values. In other words, one slot such as `delivery clue present` is closer to a feature, while the state where the whole sentence has been changed into a numeric vector is closer to a representation.

## The Original Input Is Hard to Compute Over Directly

Return to the customer-support example from 4.2.

> If the delivery does not arrive by tomorrow, I will cancel it.

A human reader sees several clues together.

| Clue visible to a person | Possible meaning |
| --- | --- |
| delivery | a delivery-related inquiry |
| by tomorrow | a deadline condition |
| if it does not arrive | possible delivery delay |
| I will cancel it | cancellation intent or pressure |

But the model does not understand the sentence exactly as a person does. For the model to compute, the input has to be turned into some form of values. This is where `feature` and `representation` appear.

> original input -> feature or representation -> model computation -> output

This flow replaces the intuition that `the model understands the input as it is` with the perspective that `the model uses the input after turning it into computable values`. The key here is to distinguish clearly between `the original text` and `the values the model actually computes with`.

## A Feature Is an Input Value Used by the Model

Google’s Machine Learning Glossary explains a feature as an input variable to a machine-learning model. One example can have one or more features and a label.

If we simplify the customer-support classification example, features can look like this.

| Original input | Feature |
| --- | --- |
| `I want a refund.` | whether the word `refund` appears |
| `When will the delivery arrive?` | whether the word `delivery` appears |
| `The item arrived broken.` | whether damage-related expressions appear |
| `I want to change the address.` | whether address-change expressions appear |

These features can be defined by people in advance. For example, each message sentence can be assigned the following values.

| Message sentence | `refund` clue | `delivery` clue | `damage` clue | label |
| --- | ---: | ---: | ---: | --- |
| `I want a refund.` | 1 | 0 | 0 | refund |
| `When will the delivery arrive?` | 0 | 1 | 0 | delivery |
| `The item arrived broken.` | 0 | 0 | 1 | exchange |

Here, `1` means the clue is present and `0` means it is absent. Real models can use far more varied values, but in this section it is enough to understand a feature as `an input value used in computation`.

## A Feature Is Not the Same as the Original Input

The important point is that a feature is not the original input itself.

| Distinction | Example |
| --- | --- |
| original input | `The item I received yesterday was damaged, and I want another one.` |
| human-designed features | damage clue present, replacement clue present |
| output label | exchange or reshipment |

The original sentence is natural language. A feature is a value extracted from that sentence so the model can compute with it.

Without this distinction, it is easy to think `if we feed data to the model, it will understand by itself`. In practice, what matters is what values are extracted, what clues are kept or dropped, and in what form the input reaches the model.

Connected back to 4.2, one input bundle can unfold into multiple features. For example, if the input is `message sentence + order state + recent delivery event`, the model may create several computational values from it, such as `delivery clue present`, `already shipped`, and `recent delay event present`. The important point is not to treat `one input case` and `many features` as the same thing. Input is the raw material the model receives, while features are the values extracted from that raw material for computation.

In the same sense, a feature can often be seen as part of a representation. Still, to reduce beginner confusion, Section 4.3 keeps the simpler distinction first: `a feature is a concrete value used in computation`, while `a representation is the broader form in which such values are arranged`.

## A Representation Is the Result of Making Data Easier to Compute Over

Google’s glossary describes a `representation` as the process of mapping data to useful features. In Section 4.3, we read representation a bit more broadly as `the result of turning original data into a form the model can compute over more easily`.

For example, the same message sentence can be turned into several kinds of representation.

| Representation style | Example | Strength | Limit |
| --- | --- | --- | --- |
| keyword features | `delivery` present, `cancel` present | simple and easy to explain | may miss context |
| numeric features | sentence length, number of exclamation marks | easy to combine with table data | may not carry enough meaning |
| categorical features | message channel: app, email, phone | easy to connect with business data | does not carry sentence meaning by itself |
| learned representation | convert the sentence into an internal vector | handles similarity and context better | hard for people to read directly |

Section 3.3 already compared rule-based approaches with representation learning. Here that discussion is not repeated. The main point to keep in the modeling context is that `how the input is represented determines what kind of world the model can see`.

## Good Representations Reveal the Differences That Matter

The review by Bengio, Courville, and Vincent explains that the success of machine-learning algorithms depends heavily on data representation. Even with the same data, one representation can expose important factors while another can hide them.

Take the customer-support example again.

> I want to cancel the payment.  
> If the delivery does not arrive, I will cancel it.

Both sentences contain the word `cancel`. But the first is closer to payment cancellation or refund, while the second is closer to delivery delay with conditional cancellation.

If we use only the presence of a word as a feature, the two sentences may appear too similar.

| Representation | Is it easy to distinguish the two sentences? | Why |
| --- | --- | --- |
| whether the word `cancel` appears | difficult | both sentences contain `cancel` |
| use both the `delivery` clue and the `cancel` clue | somewhat better | the delivery context of the second sentence becomes visible |
| use a broader sentence-level meaning representation | can improve much more | condition, intent, and context can be reflected together |

Good representations reveal the differences the model really needs to distinguish. Poor representations can hide important differences or exaggerate differences that do not matter.

## A Parameter Is an Adjusted Value Inside the Model

If features and representations are closer to `the form of values entering the model`, parameters are the values adjusted inside the model.

Google’s Machine Learning Glossary describes parameters as the weights and biases a model learns during training. Here we can understand a parameter more simply like this.

> parameter = an adjustable internal value the model uses when turning input into output

One common term here is `weight`. A weight is one kind of parameter that indicates how strongly some input value or internal value affects the output computation.

Sometimes people use the analogy of `connection strength` when explaining weights. That analogy can help when explaining structures such as neural networks, where multiple computational units are connected. But explaining neural networks is not the purpose of Section 4.3. Other models such as linear models, probabilistic models, and tree-based models have different structures, and not every parameter looks like a neural-network connection.

So `parameter` remains the basic term here. A `weight` is one representative kind of parameter, and `connection strength` is kept only as a limited analogy that can be used again later when studying neural networks.

We can simplify customer-support classification like this.

| Feature | How strongly should it connect to the refund output? | How strongly should it connect to the delivery output? |
| --- | ---: | ---: |
| `refund` clue | strong | weak |
| `delivery` clue | weak | strong |
| `cancel` clue | medium | medium |

This table does not show real parameter values. It is only a simplification for intuition. During learning, many examples are used to adjust such internal values.

The important point in this section is not `how are parameters learned?` That is handled later. For now, it is enough to understand that when we look at a trained model, there are already adjusted internal values inside it, and those values are used in the computation that turns input representations into outputs.

## Why Learning Is Mentioned Briefly

Section 4.2 explained that data is a collection of input-output examples. To explain parameters, learning has to be mentioned briefly, because parameters are not fixed as meaningful values from the beginning. They are adjusted according to training data and learning goals.

> input example -> feature/representation -> model prediction -> comparison with correct answer -> parameter adjustment

Suppose the training data contains many cases such as the following.

| Input | Label |
| --- | --- |
| `I want a refund.` | refund |
| `Can I cancel the payment?` | refund |
| `When will the delivery arrive?` | delivery |
| `Will it ship today?` | delivery |

At first, the model’s internal criteria may not match the task well. When predictions are wrong, the learning procedure adjusts the internal values in a direction that reduces the difference. By repeating that over many examples, the model gradually fits the relation between input representations and outputs.

But the fact that parameters are adjusted does not mean that the model understands meaning like a person. Parameters are computational values adjusted to match the training data and the learning objective.

## The Word "Parameter" Can Refer to Different Levels

There is a common point of confusion for beginners. When using AI tools, values such as `temperature`, `top-p`, and `max tokens` are also sometimes called parameters. But these are not the same thing as the internal model parameters discussed in Section 4.3.

Google’s glossary describes `temperature` as a hyperparameter that controls the degree of randomness in model output. In LLM use, it is usually better read as a generation setting that controls how sharp or flat the probability distribution is when the next token is chosen.

| Distinction | Example | Who sets it? | When is it used? | Meaning |
| --- | --- | --- | --- | --- |
| model parameter | weight, bias | learned during training | internal model computation | a value adjusted by learning and stored inside the model |
| hyperparameter | learning rate, batch size | person or tuning process | training setup | a value that sets the conditions of learning |
| generation setting | temperature, top-p, max tokens | user or service setting | inference and generation | a value that changes how the trained model chooses output |

So even if we see an expression such as `temperature parameter`, we should not immediately read it as a model-internal learned parameter. In this context, it is more accurate to read it as `a setting that controls LLM generation`.

## Term-Boundary Notes

The core terms of Section 4.3 are feature, representation, and parameter. But in actual documents, similar-looking words appear alongside them, so this note fixes only their positions briefly without pulling the focus away from the section.

| Term | Position in 4.3 | Where it will be treated in more detail |
| --- | --- | --- |
| hyperparameter | a value that controls learning or usage conditions | machine learning |
| temperature | not a model-internal parameter, but a generation setting adjusted during generation | LLMs and generative AI |
| embedding | a kind of vector representation | LLMs and vector search |

The key point to keep here is one thing. `Feature`, `representation`, and `parameter` are basic terms for reading model computation, while values such as `temperature` are not learned internal parameters but later settings that adjust generation behavior.

## Seeing the Three Terms Together

Feature, representation, and parameter are connected, but they are not the same thing.

| Term | Question | Customer-support example |
| --- | --- | --- |
| feature | what values does the model use from the input? | `delivery` clue, `refund` clue, sentence length |
| representation | into what computable form is the original data turned? | a keyword table, numeric vector, learned sentence representation |
| parameter | what adjusted internal values are used in the computation? | internal values corresponding to how much each clue affects the output |

The flow looks like this.

```mermaid
--8<-- "assets/part-01/chapter-04/representation-model-parameter-flow-en.mmd"
```

This figure is a simplification. In real models, the boundary between features and representations can blur, and in deep learning the representation itself may be learned through multiple layers. Here the goal is only to read the flow that `input is changed into values the model can use, and those values are combined with adjusted internal values to compute the output`.

The key point of the diagram is to show that `feature/representation` and `parameter` are both important, but they occupy different positions. Keep the position split clear first: `feature/representation is on the input side`, while `parameter is on the inside of the model`.

## What to Hold in This Section

Before understanding those topics, this section only fixes the basic positions of the necessary terms: feature, representation, and parameter.

## Common Confusions

| Confusion | Safer understanding |
| --- | --- |
| input and feature are the same | input is the original data that came in, while a feature is a value made for the model to use |
| a representation is always something people can read | a learned representation may be hard for people to interpret directly |
| intent is a model parameter | intent is closer to the result of interpreting the user input as a business purpose or label, not to parameters stored inside the model |
| a parameter is a rule | a parameter is not a human-readable IF-THEN rule, but an internal value adjusted by learning |
| every parameter is a neural-network connection strength | connection strength is only a useful analogy for neural networks, not a general definition for every model’s parameters |
| temperature is also a model parameter | in LLMs, temperature is not a value learned and stored inside the model, but a setting that controls output generation |
| more parameters are always better | model size alone does not make a model good; data, problem definition, and evaluation must also match |
| if there is data, the representation automatically becomes good | performance and limitations still depend on what representation is used and what data it is learned from |

These confusions remain important later. They become especially frequent when discussions move toward deep learning and LLMs, where terms such as parameter count, representation, and embedding appear often.

## Checklist

- I can explain that a feature is an input value used by the model.
- I can explain that a representation is the result of changing original data into a form that is easier to compute over.
- I can explain that a parameter is an adjusted value inside the model used in output computation.
- I can distinguish original input, feature, representation, and parameter.
- I can explain that a good representation reveals important differences, while a poor representation can hide them.
- I can distinguish intent analysis from model parameters and read it as a layer that interprets input into a business intention or label.
- I can distinguish model parameters from LLM generation settings.
- I can explain that a model does not simply `understand` the original input as it is; input is turned into features or representations, and the model uses those values together with adjusted internal parameters to compute output.
- I can explain the position distinction that `features/representations are on the input side`, while `parameters are inside the model`.
- I can distinguish that Section 4.3 is not a model-building procedure, but a basic vocabulary guide for reading model computation.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary/){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Google for Developers, [Supervised Learning](https://developers.google.com/machine-learning/intro-to-ml/supervised){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-22.
- Stanford Encyclopedia of Philosophy, Selmer Bringsjord and Naveen Sundar Govindarajulu, [Artificial Intelligence](https://plato.stanford.edu/entries/artificial-intelligence/){: target="_blank" rel="noopener noreferrer" }, 2018-07-12, accessed 2026-06-22.
- Yoshua Bengio, Aaron Courville, Pascal Vincent, [Representation Learning: A Review and New Perspectives](https://arxiv.org/abs/1206.5538){: target="_blank" rel="noopener noreferrer" }, arXiv, 2012-06-24, accessed 2026-06-22.
