# P1-8.3 Reinforcement Learning: Actions and Rewards

> Section ID: `P1-8.3`
> Version: `v2026.07.20`

Section 8.1 explained supervised learning as learning from examples where inputs and labels are given together. Section 8.2 explained unsupervised learning as learning that looks for structure, clusters, or representations in unlabeled data.

This section introduces the third basic distinction. `Reinforcement learning` is neither the direct fitting of labels nor the search for unlabeled structure alone. It is a learning setting in which an `agent` chooses `actions` in `states`, receives `rewards` after those actions, and tries to improve the `policy` that chooses actions over time.

This is not a suddenly recent distinction. Reinforcement learning was already an important axis in AI and machine-learning education in the 1990s and 2000s. So if older introductory material made reinforcement learning look prominent, that memory is not necessarily mistaken. What should be separated is the older baseline problem setting from much later public examples such as Atari, AlphaGo, or RLHF. This section uses the earlier basic frame: `state`, `action`, `reward`, and `policy`.

The central question is:

> when a correct label is not given directly,  
> what does the model try to change by observing the consequences of its actions?

> reinforcement learning is not the matching of an answer sheet; it is the adjustment of behavior through reward signals that arrive after action

This section organizes `reinforcement learning`, `agent`, `environment`, `state`, `action`, `reward`, `policy`, `exploration`, and `exploitation` through one axis: reward signals from the consequences of action. The intuitive sense of `state` and `action` was already introduced in 7.1, and the distinction among labels, supervised learning, and unsupervised learning was handled in 8.1 and 8.2.

This section does not calculate reinforcement-learning algorithms. Markov decision processes, Bellman equations, Q-learning, policy gradients, actor-critic methods, and deep reinforcement learning appear only as names and positions.

It also does not go deeply into game AI, robot control, recommender systems, or RLHF. Later reinforcement-learning algorithms and the broad picture of RLHF return in Part 4 Chapter 19, and RLHF in the LLM alignment context reconnects in Part 6. Here the focus is narrower: why reinforcement learning is a different problem setting from supervised and unsupervised learning.

The working definition here is:

> reinforcement learning is a method that chooses actions in states  
> and uses the rewards after those actions  
> to find a better long-term policy

## Steering Learning with Actions and Rewards

- Explain reinforcement learning in terms of actions and rewards.
- Distinguish agent, environment, state, action, reward, and policy at an introductory level.
- Avoid confusing reward with the label used in supervised learning.
- Understand the intuition of delayed reward.
- Understand the tension between exploration and exploitation.
- Avoid using reinforcement learning, deep learning, game AI, and RLHF as if they were all the same.

## Three Standards

| Standard | Why it matters | Level of understanding needed here |
| --- | --- | --- |
| reinforcement learning adjusts behavior from state, action, and reward | This makes its difference from supervised learning visible at once. | Read it as a flow of action and consequence rather than input and answer pair. |
| reward is different from a label | This prevents reinforcement learning from being misunderstood as a variant of supervised learning. | Understand that the system does not receive the target answer directly, but receives feedback after action. |
| a good action may not show its value immediately | This is the starting point for delayed reward and the exploration/exploitation issue. | It is enough to keep the intuition that something costly now may lead to better future outcome. |

A short role split is useful:

| Term | Very short meaning | Role in this section |
| --- | --- | --- |
| reinforcement learning | learning that adjusts policy through rewards from action outcomes | the third baseline of Chapter 8 |
| agent | the actor that chooses actions | the main decision-making entity |
| environment | the outside world the agent interacts with | the place where consequences come back |
| state | information about the current situation | the basis for action choice |
| action | what the agent actually chooses to do | the direct cause that changes reward and next state |
| reward | numeric feedback after action | the learning signal that must be kept separate from labels |
| policy | the method of choosing actions from states | the object reinforcement learning tries to improve |
| exploration | trying actions that are not yet well known | information gathering for learning |
| exploitation | choosing the action that currently looks best | using what has already been learned |

## Reinforcement Learning Learns from Consequences of Action

At the center of reinforcement learning is `action`. An `agent` observes a `state` or `observation` inside an `environment`, chooses an `action`, and then the environment changes and returns a `reward`.

OpenAI’s Spinning Up materials describe reinforcement learning as the field where an agent learns by trial and error through interaction with an environment. Google’s glossary likewise explains that an agent uses a policy to choose actions and observes states of the environment.

At the introductory level, the baseline flow is:

> observe a state  
> choose an action  
> the environment changes  
> receive a reward  
> adjust the future way of acting

Consider a warehouse robot:

| Element | Warehouse-robot example |
| --- | --- |
| agent | the robot that moves goods |
| environment | the warehouse, shelves, paths, and obstacles |
| state or observation | robot position, target position, nearby obstacles |
| action | move forward, turn, stop, pick up an item |
| reward | positive reward for moving the right item safely, negative reward for collision |
| policy | the method for choosing actions from states |

In this example, the robot does not receive a direct label at every moment. It acts, experiences consequences, and receives better or worse feedback depending on those consequences.

## Reward Is Not a Label

One of the easiest early misunderstandings is to treat `reward` as if it were the same as a supervised-learning `label`. Both are learning signals, but they are not the same signal.

| Distinction | Label in supervised learning | Reward in reinforcement learning |
| --- | --- | --- |
| when it is given | already attached to the example data | returned after the action |
| central question | what output belongs to this input? | does this way of acting lead to better long-term outcome? |
| form of signal | class, numeric target, expected output | numeric feedback about the consequence of action |
| caution | the label standard is not always absolute truth | reward is not moral truth or the whole objective by itself |

For example, in customer-support classification:

> input: `I want a refund.`  
> label: refund

In a reinforcement-learning-style interaction:

> state: the customer sent a refund-related message  
> action: first send the refund policy guidance  
> result: the customer solved the issue  
> reward: positive reward

Here the reward is not the label `refund`. It is a signal about whether a sequence of actions helped achieve the objective.

## Policy Is the Way of Choosing Actions

`Policy` means the way the agent chooses actions from states or observations. Google’s Machine Learning Glossary defines a policy as a mapping from states to actions. OpenAI Spinning Up also explains policy as the rule that decides what action the agent takes.

So the baseline reading is:

> policy = the method for choosing an action after seeing a state

A simple robot vacuum example:

| State | Action |
| --- | --- |
| no obstacle ahead | move forward |
| obstacle ahead | turn |
| battery low | move to charger |
| high-dust area detected | increase cleaning intensity |

This is not a literal learned RL policy. It is only an intuition for what it means that policy maps states to actions.

The goal of reinforcement learning is not only to match the next action once. It is to find a pattern of action that increases reward over many situations and over time.

## Delayed Reward Makes the Problem Harder

One reason reinforcement learning is difficult is that reward may not come back immediately. This is the intuition of `delayed reward`.

Think of an agent trying to escape a maze:

> it is not told at every single step whether the move was correct  
> it receives a large reward only when it reaches the exit  
> later it must determine which earlier actions contributed to that result

This differs from supervised learning. In supervised learning, each example can have an attached target output. In reinforcement learning, the consequence of an action may only become visible after several more steps.

The same intuition appears in business-like situations:

| Situation | Immediate visible result | Result that appears later |
| --- | --- | --- |
| recommendation system | the user clicks | the user remains satisfied and returns later |
| customer response | the user reacts to the first reply | the issue is actually resolved and dissatisfaction decreases |
| inventory management | today’s cost is reduced | stockouts or overstock shrink weeks later |
| robot control | the robot moves one step without collision | the whole task is completed safely |

So reinforcement learning asks not only `does this action look good right now?`, but also `how does this action affect later outcomes?`

## Exploration and Exploitation

Reinforcement learning contains a tension between `exploration` and `exploitation`.

`Exploration` means trying actions that have not yet been tested enough. `Exploitation` means choosing the action that currently looks best based on what has already been learned.

| Choice | Meaning | Risk |
| --- | --- | --- |
| exploration | try new actions to gather information | may receive low reward in the short term |
| exploitation | choose the action that currently looks best | may fail to discover a better action |

Google’s glossary uses `epsilon-greedy policy` as an example of balancing the two. At the introductory level, the core intuition is:

> if we never try unfamiliar actions, we cannot learn better ones  
> but if we only keep trying, we may fail to produce stable performance

Reinforcement learning is partly about handling that balance.

## Reinforcement Learning Is Not Only About Games

Games are popular examples because they make states, actions, rewards, and win/loss outcomes easier to explain. But understanding reinforcement learning only as game AI makes the scope too narrow.

Its core structure appears whenever the following hold together:

> there are actions to choose  
> actions affect future state  
> there is some reward signal  
> present action influences later outcome

That viewpoint fits examples like these:

| Example | State | Action | Reward |
| --- | --- | --- | --- |
| maze or game | current position, time left, score | move, attack, defend | score increase, win, failure |
| robot control | robot position, joint state, obstacles | move, rotate, grasp | task success, energy saving, collision avoidance |
| recommender system | user context, past response | choose which item to show | click, satisfaction, long-term return |
| inventory management | current stock, demand estimate, cost | adjust order quantity | fewer stockouts, lower storage cost |
| dialogue system | user request, previous conversation state | choose the next reply style | problem resolution, user rating, safety compliance |

These are conceptual examples only. Real deployment raises difficult issues about reward design, safety constraints, exploration cost, data collection, and evaluation.

## The Boundary from Other Learning Types

Chapter 8 separates three basic learning types. Summarized again:

| Learning type | Data and signal | Central question | Place in this chapter |
| --- | --- | --- | --- |
| supervised learning | input and label | what label should be predicted from this input? | 8.1 |
| unsupervised learning | unlabeled data | what structure exists in the data? | 8.2 |
| reinforcement learning | state, action, reward | which actions increase long-term reward? | 8.3 |

`Deep learning` is not on the same classification axis as this table. It can be combined with reinforcement learning, in which case people speak of `deep reinforcement learning`, but reinforcement learning itself is not the same thing as deep learning.

`RLHF` also does not represent all reinforcement learning. It is an important modern setting in LLM alignment, but it is too narrow to serve as the starting definition of reinforcement learning as a whole.

## Checklist

- I can explain reinforcement learning through the flow of state, action, and reward.
- I can distinguish agent, environment, and policy at an introductory level.
- I can explain why reward is not the same thing as a supervised-learning label.
- I can explain why delayed reward makes reinforcement learning harder.
- I can explain the difference between exploration and exploitation.
- I can avoid using reinforcement learning, deep learning, deep reinforcement learning, and RLHF as if they were the same thing.
- I can read a problem through the time flow of action and consequence, not only through the frame of `input and correct answer`.
- I can connect reward, exploration, exploitation, and delayed reward in one reinforcement-learning explanation.

## Sources and Further Reading

- Google for Developers, [Machine Learning Glossary](https://developers.google.com/machine-learning/glossary){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- OpenAI Spinning Up, [Part 1: Key Concepts in RL](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- David L. Poole, Alan K. Mackworth, [Artificial Intelligence: Foundations of Computational Agents, 3rd ed., Chapter 12 Planning with Uncertainty](https://artint.info/3e/html/ArtInt3e.Ch12.html){: target="_blank" rel="noopener noreferrer" }, accessed 2026-06-23.
- Richard S. Sutton and Andrew G. Barto, [Reinforcement Learning: An Introduction, second edition](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }, MIT Press, 2018, accessed 2026-07-19.
