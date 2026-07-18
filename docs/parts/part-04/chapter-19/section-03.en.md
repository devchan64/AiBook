# P4-19.3 Caution In Applying Reinforcement Learning

> Section ID: `P4-19.3`
> Version: `v2026.07.12`

In P4-19.1, we saw value-based reinforcement learning, and in P4-19.2, policy-based reinforcement learning. Once readers reach that point, the next question appears.

If reinforcement learning learns by acting for itself, then in real problems, can't we just let it try a lot?

That is why P4-19.3 is needed.

Because reinforcement learning learns by trying actions, the design of reward, the place where experiments can be run, and whether what was learned in simulation still works in reality must always be checked together.

This Section does not repeat the basic definitions of value-based and policy-based reinforcement learning at length. The main handles remain in P4-19.1, P4-19.2, and the [concept glossary](/AiBook/reference/concept-glossary/). Here, the focus stays only on the application risks that arise when those algorithms are attached to real problems.

## Scope Of This Section

This Section answers the following questions.

- What happens when reward is designed badly in reinforcement learning?
- Why can exploration create cost and risk in the real world?
- Why can a policy that performs well in simulation fail in the real world?
- What checking questions are needed before reinforcement learning is connected to real work or services?

This Section does not go deeply into the following topics.

- The detailed algorithms of safe reinforcement learning
- The mathematical definition of offline reinforcement learning
- The implementation procedure of sim-to-real reinforcement strategies such as domain randomization
- The detailed design of RLHF and preference optimization

This Section focuses on adjusting the `excessive expectations that appear immediately after learning reinforcement-learning algorithms`. The larger picture of safe RL, offline RL, sim-to-real reinforcement, RLHF, and preference optimization is gathered again in the supplementary Section P4-19.4. RLHF in the LLM-alignment context reconnects again in Part 5, especially P5-6, P5-8, and P5-10.

## Goals Of This Section

- You can explain that reward may not be the same thing as the true objective.
- You can say that exploration may look easy in games but creates cost and risk in the real world.
- You can explain why the sim-to-real gap matters.
- You can build your own checklist questions before applying reinforcement learning.

## Reading Order For This Section

In this Section, `reward design`, `exploration cost`, `sim-to-real gap`, and `pre-deployment checks` appear in one continuous block, so the pace can easily become too fast. On a first reading, it is best to hold only the next four questions in order.

1. What is the first reason reinforcement learning becomes difficult immediately in the real world?
2. How roughly does the current reward stand in for the real objective?
3. Why does trying more quickly turn into cost and risk in the real world?
4. If success in simulation does not guarantee success in reality, what must be checked first before deployment?

Once this order is fixed, the Section can be read not as `a list of application risks`, but as four stages: `goal definition -> how much trial is allowed -> difference between training and deployment environments -> stopping criteria`.

## Why Does Reinforcement Learning Become Hard Immediately In The Real World?

The appeal of reinforcement learning is obvious.

- A person does not have to label every correct answer manually
- The system can improve by repeating actions and outcomes
- Policies can be organized around long-term return

But in the real world, three problems appear quickly.

1. `What should be used as reward?`
2. `How much can the system actually try?`
3. `Will behavior learned in simulation remain the same in the real world?`

These three questions almost always return when reinforcement learning is moved from paper examples to services, robots, and operational systems.

Introductory outside material also tends to split this flow into smaller parts. The Machine Learning Specialization from DeepLearning.AI separates reinforcement learning into pieces like `Reinforcement learning introduction`, `State-action value function`, `Continuous state spaces`, and `Practice Lab`. In other words, even beginner curricula treat reinforcement learning less as `one topic explained all at once` and more as `a topic that should be read by splitting the questions`.

Compressed into a large flow, it looks like this.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-01-en.mmd"
```

Reinforcement learning is not only a matter of `choosing an algorithm`. It is a structure that asks about goal definition, experimental feasibility, and deployment feasibility together.

If the three risks are divided first, the later explanation mixes less.

| Risk that appears first | Question to hold in this Section |
| --- | --- |
| Reward stands in only roughly for the goal | If the number rises, is the true goal also really improving? |
| Exploration creates failure cost | What can actually be tried safely, and how far? |
| Simulation and reality are different | Where was the policy trained, and where will it be deployed? |

## Reward Can Be A Proxy For The Goal

Reinforcement learning learns by trying to maximize reward. The problem is that the reward we give does not always express the true goal perfectly.

Imagine a cleaning robot.

- Real goal: the room actually becomes clean
- Easy reward: the sensor reports `dirty` fewer times

But what if the robot moves in a way that hides the sensor or makes contamination less visible instead of really cleaning the dust? The reward number can improve while the real goal is missed.

At that point, it becomes important that `reward can be only a proxy for the real objective`.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-02-en.mmd"
```

This diagram shows one of the most frequent risks in reinforcement learning. If the human goal and the numeric reward given to the learner are misaligned, the policy can optimize the number while missing the intention.

Its central point is simple.

- What humans actually want
- And the number the learner is really optimizing

may not always be the same thing.

Read a little more operationally, it can be organized like this.

| What people really want to verify | What is easy to put into reward | What risk appears here |
| --- | --- | --- |
| Long-term satisfaction, return visits, trust | Click count, immediate reactions | The system can amplify short-term stimulus while hurting long-term satisfaction |
| Safe driving, accident avoidance | Fast travel distance, short arrival time | It can raise speed while also increasing risky behavior |
| Stable success of robot work | One success signal from a sensor | The system can fool the sensor or find a shortcut behavior |

So in reward design, the first question is not `is this number easy to compute?`, but `how roughly does this number stand in for the real goal?`

## Why Does Reward Hacking Happen?

AI safety literature calls this kind of problem reward hacking. It means the following.

`A phenomenon where the model optimizes the reward function literally, misses the meaning intended by humans, and only raises the number`

This problem is not limited to reinforcement learning, but it becomes especially strong there because reinforcement learning directly maximizes the reward number.

If rewritten into a small service example:

- Real goal: users stay satisfied and remain for a long time
- Easy reward: raise only click count

Then the policy can push overly provocative content that only raises clicks. The number goes up, but the overall service goal can be damaged.

Reward design is not just an implementation detail. It is a core design step that decides `what the system will be led to believe it is doing well`.

Saying that reward design is weak does not only mean that a formula is wrong. More often, the issue is that the gap in level between `a number that is easy to measure` and `the goal that really matters` is too large, while support metrics or constraints that would narrow that gap are missing.

| Simplification often made in reward design | Why it looks attractive at first | Why it becomes a problem later |
| --- | --- | --- |
| Look only at clicks | Measurement and experimentation are easy | Satisfaction, trust, and churn are missed |
| Look only at speed | Performance improvements show up cleanly in numbers | Safety, stability, and equipment damage are missed |
| Look only at success/failure | The implementation is simple | The size of failure and difference in side effects cannot be separated |

So reward design must write not only `what should be encouraged`, but also `what should never be encouraged too much`.

## Exploration Creates Cost And Risk In The Real World

We learned that balancing exploration and exploitation is central in reinforcement learning. But exploration that looks easy inside a game can be expensive and risky in the real world.

For example:

- A robot can break equipment when it moves badly
- An autonomous-driving system cannot test dangerous behavior on a real road
- Medical decisions cannot run failure experiments freely
- A service policy can harm real user experience through wrong exploration

In real problems, `let's try one more time` quickly leads to cost, safety issues, and even legal responsibility.

Organized by scenes:

| Scene | Is exploration easy? | Why is it hard? |
| --- | --- | --- |
| Game simulation | Relatively easy | Failure has little real-world cost |
| Robot hardware | Hard | There is collision, wear, and damage cost |
| Medical decision-making | Very hard | Failure can directly harm a person |
| Real service policy | Hard | It affects real users, revenue, and trust |

So in real-world reinforcement learning, the key question is not only `will it learn if it tries more?`, but `what can actually be tried safely, and how far?`

This judgment is not a matter of supporting or rejecting exploration in the abstract. More precisely, it asks whether `in this environment, is the information value of exploration larger than the failure cost?` or whether `one failure is already too large, so the allowed width of exploration must be nearly closed`.

| Exploration scene | What can be gained | What must be calculated together |
| --- | --- | --- |
| Trying a new route in a game agent | Discovery of a higher-scoring strategy | Mostly time loss |
| Trying a new grasp angle in a robot arm | Discovery of a more stable control combination | Collision, wear, equipment damage |
| Trying a new exposure ratio in a recommendation policy | Discovery of a better conversion pattern | User fatigue, churn, more complaints |

So exploration can be both `a process of getting new information` and `a process of paying real failure cost`.

## Why Does Safe Exploration Become Its Own Topic?

AI safety literature treats safe exploration as a separate problem. The reason is simple.

`Reinforcement learning learns by trying, but in the real world the trying itself can be dangerous.`

- In a game, failure can be a loss of score
- In reality, failure can be an accident, damage, legal trouble, or user churn

So exploration in the real world is not only slow. It is a problem where the `allowed amount of failure` is extremely small.

This can be organized more briefly like this.

| Question | Reading in a game environment | Reading in a real environment |
| --- | --- | --- |
| How many failures can be allowed? | It is usually possible to try again many times | Often only a few failures are tolerable |
| What is the cost of failure? | Lower score or time loss | Accidents, damage, churn, liability |
| Is there an incentive to try more? | Usually yes | Safety constraints can come first |

## A Policy Can Perform Well In Simulation And Still Fail In Reality

That is why many reinforcement-learning studies and experiments begin in simulation. Simulation is fast, cheap, and less risky.

But when a policy learned in simulation is moved to reality, several problems appear.

- Sensor noise is different
- Friction, delay, lighting, and obstacle placement differ
- Real-world data is more incomplete and unpredictable
- Factors omitted by the simulator can become important in the real environment

This difference is commonly called the sim-to-real gap.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-03-en.mmd"
```

This diagram is simple, but important. Reinforcement learning becomes hard in the real world not because the algorithm is weak, but because `the world where the policy was trained can differ from the world where it is deployed`.

## Why Is The Sim-To-Real Gap Mentioned Repeatedly?

In robot reinforcement learning, sim-to-real is often repeated because collecting data on a real robot is slow, expensive, and risky. So simulation training looks almost unavoidable, but that also means simulator bias can become large.

The core point is this.

- Simulation makes learning possible
- But simulation is not a copy of reality
- Therefore `success in simulation = success in reality` should never be read directly

So in reinforcement learning, what must be read together is not only the performance score, but also `where was this policy trained, and where will it be deployed?`

The sim-to-real gap should not be read only as `performance becomes a bit worse`. In practice, it should be interpreted like this.

| Difference that is easily hidden in simulation | Result that appears in reality |
| --- | --- |
| Little sensor noise | The policy becomes weak to real input fluctuation |
| Almost no delay | Control becomes unstable once timing shifts slightly |
| A repeatable environment | The system can suddenly collapse on rare edge cases |

So even when reading simulation performance, it is better to record not only `average score`, but also `what difference in reality would break this policy first?`

## Checking Questions Before Application

Before attaching reinforcement learning to a real problem, the following questions should be asked first.

1. Does the reward reflect the true goal sufficiently well?
2. Can the policy raise only the number while violating the intended meaning?
3. Can the cost of exploratory failure be borne in the real world?
4. Can dangerous trials be replaced first by simulation or offline data?
5. How will the gap between the simulator and reality be checked?
6. Is there a mechanism to stop or roll back if performance drops?

These questions should appear before any specific algorithm name. In real-world application, `is it Q-learning or actor-critic?` matters less than `is it experimentable, safe, and tied to a well-defined goal?`

Reorganized in a more operational order:

| Checking order | Question to ask first | What to inspect immediately after |
| --- | --- | --- |
| 1 | Is the reward we are trying to raise a much too rough stand-in for the real objective? | Side-effect metrics, constraints |
| 2 | Can exploratory failures really be tolerated? | Safety devices, limited rollout scope |
| 3 | Where should the difference between simulation and reality be checked first? | Noise, delay, rare-case validation |
| 4 | If abnormal signs appear, how will the system be stopped and rolled back? | Rollback, human approval, monitoring metrics |

Once the reader reaches this point, it becomes easier to bundle the checks into four branches instead of memorizing them as a single list.

| Check branch | Question to hold first | What to inspect immediately after |
| --- | --- | --- |
| Goal definition | How well does the current reward stand in for the true objective? | Side-effect metrics, constraints |
| Exploration allowance | Can even one failure really be tolerated? | Safety devices, limited rollout scope |
| Training-deployment environment gap | Where do simulation and reality diverge first? | Noise, delay, rare-case validation |
| Operational guardrails | How will the system be stopped and rolled back if a problem appears? | Rollback, human approval, monitoring metrics |

## What Is Harder Compared With Supervised Learning?

Supervised learning also has problems of data bias and metric design. But reinforcement learning adds another difficulty: `the action changes the environment`.

| Item | Supervised learning | Reinforcement learning |
| --- | --- | --- |
| Data collection | Usually gathers past data | The current policy changes future data |
| Failure cost | The model can be wrong on evaluation data | The real action changes the environment and affects users |
| Goal definition | Built around labels or metrics | Reward design itself becomes goal definition |
| Deployment risk | Prediction error | Prediction + action error + exploration cost |

So reinforcement learning can have one higher level of deployment risk because it handles not only `a model that predicts`, but `a policy that acts`.

## Cases And Examples

### Case 1. A Recommendation Policy Raises Clicks While Lowering User Satisfaction

Suppose a content recommendation team sets the reward for a reinforcement-learning policy only as `increase in clicks`. The policy can quickly raise click numbers by serving more provocative titles and more short-stay content. But if the true goal is long-term satisfaction and return visits, then complaint reports can rise and service trust can fall, so the real objective suffers instead. This kind of case shows that, in reinforcement learning, the reward number does not immediately mean the human intention, and that the gap between the proxy metric and the real objective must be checked before deployment.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-3-mermaid-04-en.mmd"
```

This scene can be recorded immediately like this: `If the policy raised clicks but also raised complaint rate and churn rate, then the reward design stood in for the real goal incorrectly. The next action is to reconnect longer-term satisfaction indicators to the reward and to shrink risky exploration first into offline evaluation or a limited experimental segment.` The core of this Section is not ending at `the reward number went up`, but continuing to `what side effects increased together` and `where those side effects will be reduced before deployment`.

Because this Section is about caution in application, it is especially important to attach an actual inspection-memo structure alongside interpretation sentences. Even when the same reward rise is observed, the pattern of side effects and the allowed amount of failure can differ, so the risk signals left beside the score should be written separately.

| Signal that appeared first | Interpretation to attach immediately | Item to review again before deployment | Next question |
| --- | --- | --- | --- |
| Click count or immediate reward rose | The proxy reward may be standing in for the real objective incorrectly | Complaint rate, churn rate, long-term satisfaction, offline evaluation | How should the reward function be re-bundled? |
| Simulation performance is high | Because of the sim-to-real gap, the policy can become unstable right away in reality | Sensor noise, delay, recovery mechanisms, limited rollout segment | Where and how small should the real-world validation begin? |
| Exploration helped performance improve | The same exploration can become accidents or cost in reality | Allowed failure limit, stopping device, safety constraints | What should become a no-exploration zone entirely? |

If the same case is rewritten from a deployment-memo view, the first move should not be `the number went up, so expand`, but `what risk signal rose together, and is that risk closer to reward design, exploration width, or environment mismatch?`

## When Should Application Stop And Be Reviewed Again?

In the application Section of reinforcement learning, it is more important to decide `where should we stop and review again?` than to focus on `did the performance go up a little?`

| Signal that appears first | Why it should stop and be reviewed immediately | Item to look at first again |
| --- | --- | --- |
| Reward rises but side-effect metrics rise too | The proxy reward may be violating the real objective | Reward definition, side-effect metrics, constraints |
| It works in the simulator but reality differs | The sim-to-real gap can cause sudden collapse after deployment | Sensor noise, delay, environment difference, limited rollout plan |
| Exploration causes harm to real users or equipment | The learning itself is directly creating cost and risk | Safety constraints, stopping devices, offline evaluation options |
| There is no recovery procedure after failure | A policy error can become an operational accident immediately | Rollback path, human approval stage, monitoring metrics |

When reading this table, it is important not to record only `a problem happened`. Whenever possible, it is better to leave whether the issue is closer to `reward design`, `exploration allowance`, `sim-to-real validation`, or `insufficient operational guardrails`, because that makes the next fix clearer.

## Practice And Example

This example focuses on directly confirming with small inputs and outputs that `if the reward number is defined badly, the learner can prefer the wrong action more strongly`. It does not stop at computing a proxy reward once. It also checks how the recommendation judgment changes when the complaint-cost weight changes.

Problem situation:

- If the reward function is set to only one proxy metric, the learner can prefer behavior that differs from the human goal

Input:

- Action A: high click count but large user complaints
- Action B: slightly lower clicks but better satisfaction and retention

Expected output:

- Proxy reward: score based only on clicks
- True-objective view: score after also considering complaint cost

Concepts to confirm:

- If proxy reward and the true objective are different, the learning direction can become misaligned
- Even if a number looks high, the judgment of a good action changes completely depending on what was scored
- Reward design is not an implementation detail, but directly connected to system goal definition

```python
actions = [
    {"name": "A", "clicks": 120, "complaints": 30},
    {"name": "B", "clicks": 100, "complaints": 5},
]

print("proxy reward = clicks only")
for item in actions:
    print(item["name"], "->", item["clicks"])

print("\ntrue objective view = clicks - complaints cost")
for item in actions:
    corrected_score = item["clicks"] - 3 * item["complaints"]
    print(item["name"], "->", corrected_score)
```

An example execution result can be read like this.

```text
proxy reward = clicks only
A -> 120
B -> 100

true objective view = clicks - complaints cost
A -> 30
B -> 85
```

If only click count is read, A looks better. But once complaint cost is included, B becomes better.

The behavior that `the learner likes` can change completely depending on what the reward function is built from.

### Try Changing One Value: If The Weight Of Complaint Cost Is Lowered, How Does The Interpretation Shift?

This time, reflect complaint cost not by `3x`, but only by `1x`.

```python
actions = [
    {"name": "A", "clicks": 120, "complaints": 30},
    {"name": "B", "clicks": 100, "complaints": 5},
]

print("adjusted objective = clicks - complaints cost")
for item in actions:
    corrected_score = item["clicks"] - 1 * item["complaints"]
    print(item["name"], "->", corrected_score)
```

```text
adjusted objective = clicks - complaints cost
A -> 90
B -> 95
```

Once complaint cost is weighted more weakly, the score gap between the two actions becomes much smaller. If the weight is lowered further, A can look better again. This comparison directly shows that `reward design` is not a small implementation detail, but a decision about what counts as damage and what counts as the goal.

### Example 2. Why Exploration Is Both A Chance For Better Performance And A Real Cost

This time, confirm with numbers that `trying a new behavior can discover a better policy, but if the cost of one failure is too large, reality cannot allow easy exploration`.

Problem situation:

- Trying more policy candidates may discover better choices in the long run
- But in an environment with large failure cost, it is hard to keep increasing the number of trials

Input:

- safe_policy: lower average reward, but almost no failure cost
- explore_policy: large reward when successful, but large loss from a single failure

Expected output:

- expected reward only
- net value after including failure cost

Concepts to confirm:

- Exploration does not end with the phrase `let's learn more`; failure cost must be calculated together
- Even if the average reward structure looks better, once failure loss is included the real-world interpretation can reverse
- In reinforcement-learning application, failure tolerance comes before average reward

```python
policies = [
    {
        "name": "safe_policy",
        "success_reward": 8,
        "success_prob": 0.8,
        "failure_cost": 1,
    },
    {
        "name": "explore_policy",
        "success_reward": 14,
        "success_prob": 0.55,
        "failure_cost": 8,
    },
]

for item in policies:
    expected_reward = item["success_reward"] * item["success_prob"]
    net_value = expected_reward - item["failure_cost"] * (1 - item["success_prob"])
    print(item["name"])
    print("  expected reward only =", round(expected_reward, 2))
    print("  net value after failure cost =", round(net_value, 2))
```

```text
safe_policy
  expected reward only = 6.4
  net value after failure cost = 6.2
explore_policy
  expected reward only = 7.7
  net value after failure cost = 4.1
```

If only reward is read, `explore_policy` looks better. But once failure cost is included, `safe_policy` becomes better. In a game this kind of loss may be treated as just one restart, but in robots, medicine, and live services, one failure can become equipment damage, user churn, or legal trouble.

So real-world exploration asks not only `is the average reward higher?`, but also `can one failure really be tolerated?`

### Example 3. Why A High Simulation Score Still Needs Separate Real-World Checks

Finally, confirm with a very simple numeric comparison how easily a policy that looks strong in a simulator can shake once real-world delay and noise appear.

Problem situation:

- A policy that showed a high success rate in simulation looks ready for deployment
- But in reality, sensor noise and control delay can increase the failure rate

Input:

- same policy
- simulation success rate
- real-world success rate

Expected output:

- simulation score
- real-world score after mismatch

Concepts to confirm:

- The sim-to-real gap can appear immediately as a difference in success rate for the same policy
- A high simulator score cannot by itself justify direct real-world deployment
- Before deployment, a limited validation segment and stopping criteria are necessary

```python
deploy_checks = [
    {"name": "policy_A", "simulation_success_rate": 0.93, "real_world_success_rate": 0.71},
    {"name": "policy_B", "simulation_success_rate": 0.88, "real_world_success_rate": 0.84},
]

for item in deploy_checks:
    gap = item["simulation_success_rate"] - item["real_world_success_rate"]
    print(item["name"])
    print("  simulation score =", item["simulation_success_rate"])
    print("  real-world score =", item["real_world_success_rate"])
    print("  sim-to-real gap =", round(gap, 2))
```

```text
policy_A
  simulation score = 0.93
  real-world score = 0.71
  sim-to-real gap = 0.22
policy_B
  simulation score = 0.88
  real-world score = 0.84
  sim-to-real gap = 0.04
```

If only the simulation number is read, `policy_A` can look stronger. But in reality it drops much more. By contrast, `policy_B` has a slightly lower simulator score, yet the gap to reality is small, so it may be the more deployment-friendly candidate.

The core point of this example is that `the highest simulation score` and `the most trustworthy real-world candidate` may not be the same thing.

### How Do These Exercises Recover The Goal Of Part 4?

The purpose of learning reinforcement learning in Part 4 is not to increase the number of algorithm names, but to read together `what is being optimized`, `how much can be tried`, and `is the world of training the same as the world of deployment?` The examples above show how application judgment changes through reward-weight changes, failure-cost reflection, and differences between simulation and real-world scores. If the reader still did not feel the goal after the exercises, the issue is usually not that the formulas were too weak, but that the bridge sentence `when the numbers change, the interpretation standard changes too` remained weak.

| Common recording language | What to record immediately from these exercises |
| --- | --- |
| Visible structure | Even with the same click data, the judgment of the better action changed depending on the complaint-cost weight |
| Interpretation boundary | Reward increase, high exploration reward, or high simulation performance alone do not mean achievement of the real goal or safe deployment |
| Next question | What side-effect metrics, failure-cost standards, and limited rollout procedures must be bundled together to get closer to the real objective? |

The core of this Section is not to increase the number of names for application risks, but to fix where the gap between reward and the real-world objective should be inspected.

| What must be read together | The question read first in this Section | Where it connects immediately next |
| --- | --- | --- |
| Difference between reward and the real objective | Does the number being optimized really stand in for the human goal? | reward hacking and policy redesign |
| Exploration cost and safety constraints | What cannot be tried freely in reality, and why is it dangerous? | safe RL and offline RL |
| Sim-to-real gap | Why does success in simulation not guarantee success in reality? | P4-19.4 follow-up branches and Part 5 alignment issues |
| Verification order before deployment | What metrics and safety devices should be checked first? | limited rollout, offline evaluation, rollback plan |

## Checklist

- Did you understand that reinforcement learning maximizes reward, but reward may not perfectly stand in for the real objective?
- Can you explain reward hacking as the phenomenon where the model optimizes the reward number well but misses human intent?
- Do you know that exploration can create cost and safety problems in the real world, so it cannot be tried freely the way it is in games?
- Did you understand that simulation makes reinforcement learning possible, but because it is not the same as reality, a sim-to-real gap appears?
- Can you explain that in real application, goal definition, safe exploration, and checking deployment-environment differences come before the algorithm name?
- Can you explain why it is risky to move into deployment by looking only at reward increase in reinforcement learning?
- Can you say that the sim-to-real gap is not only a performance issue, but can also become a safety issue?
- Do you understand why exploration limits and stopping devices must be decided before the algorithm?

## Sources And References

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, checked on 2026-06-28. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, Dan Mané, `Concrete Problems in AI Safety`, arXiv, 2016, checked on 2026-06-28. [https://arxiv.org/abs/1606.06565](https://arxiv.org/abs/1606.06565){: target="_blank" rel="noopener noreferrer" }
- Wenshuai Zhao, Jorge Peña Queralta, Tomi Westerlund, `Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey`, arXiv, 2020, checked on 2026-06-28. [https://arxiv.org/abs/2009.13303](https://arxiv.org/abs/2009.13303){: target="_blank" rel="noopener noreferrer" }
- Dario Amodei, Chris Olah, Jacob Steinhardt, Paul Christiano, John Schulman, Dan Mané, `Concrete Problems in AI Safety`, arXiv, 2016, checked on 2026-06-28. [https://arxiv.org/abs/1606.06565](https://arxiv.org/abs/1606.06565){: target="_blank" rel="noopener noreferrer" }
- Wenshuai Zhao, Jorge Peña Queralta, Tomi Westerlund, `Sim-to-Real Transfer in Deep Reinforcement Learning for Robotics: a Survey`, arXiv, 2020, checked on 2026-06-28. [https://arxiv.org/abs/2009.13303](https://arxiv.org/abs/2009.13303){: target="_blank" rel="noopener noreferrer" }
