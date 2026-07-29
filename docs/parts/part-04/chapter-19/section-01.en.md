# P4-19.1 Value-Based Reinforcement Learning

> Section ID: `P4-19.1`
> Version: `v2026.07.26`

In P4-2.3, reinforcement learning was framed as `learning that adjusts a policy through actions and rewards`. If we go one step deeper, the following question appears.

When readers first meet reinforcement-learning algorithms, questions immediately follow.

- On what basis does the model learn which action is good in which state?
- Is `good` written like a rule, or like a number?
- If both [Q-learning](/AiBook/en/reference/concept-glossary-alpha/q/#q-learning) and [SARSA](/AiBook/en/reference/concept-glossary-alpha/s/#sarsa) are reinforcement learning, what is different between them?

Value-based reinforcement learning is an approach that learns by attaching values to how good each action is in the long run from each state.

This Section explains the basic meaning of [value-based reinforcement learning](/AiBook/en/reference/concept-glossary-alpha/v/#value-based-reinforcement-learning), [state value](/AiBook/en/reference/concept-glossary-alpha/s/#state-value), [action value](/AiBook/en/reference/concept-glossary-alpha/a/#action-value), and [Q-value](/AiBook/en/reference/concept-glossary-alpha/q/#q-value). Later Sections continue the judgment in the current context from this handle, and the basic sense of reading the long-term goodness of actions as a score reconnects through this Section and the relevant glossary entries.

## Questions Closed By Value-Based Reinforcement Learning

This Section answers the following questions.

- What does it mean to learn value?
- How are state value and action value different?
- Why is the Q-value important in reinforcement learning?
- In what way are Q-learning and SARSA similar, and in what way are they different?
- What kinds of problems fit value-based reinforcement learning well, and where do its limits begin to show?

This Section first closes the question of `what structure reinforcement learning has when it attaches value to actions and learns their long-term goodness`. Policy-based reinforcement learning continues in P4-19.2, reward design and cautions in real-world application continue in P4-19.3, the larger flow of DQN and policy-family methods continues in supplementary learning P4-19.4, and the minimum bridge to the Bellman equation and function approximation continues in supplementary learning P4-19.5.

## Judgments To Keep From Value-Based Reinforcement Learning

- You can explain value-based reinforcement learning as `an approach that learns the long-term goodness of actions as numbers`.
- You can distinguish state value from action value.
- You can say that Q-learning updates by using `the action that looks best in the next state`.
- You can say that SARSA updates by using `the action that was actually chosen next`.
- You can understand that the difference between the two algorithms connects to a difference in learning attitude.

## Why Learn Value?

In reinforcement-learning problems, a correct label is not given every time. Instead, a reinforcement learning agent tries an action, receives a reward, and experiences the next state.

At that point, instead of writing the policy first, there are several advantages in first writing down a number for `how acceptable was this action?`

- It becomes easier to compare actions.
- Even an unfinished policy can be improved gradually.
- Different action candidates in the same state can be read relative to one another.

In other words, value-based reinforcement learning is closer to `scoring what is better first` than to `memorizing directly what to do`.

If we borrow a restaurant recommendation analogy:

- Policy: a way of deciding immediately where to go in this neighborhood
- Value: an expected score for how satisfying that choice will be in the long run

That difference matters. It becomes easier to read value-based reinforcement learning if it is understood as making `an expected scoreboard for actions` before memorizing the action rule itself.

## State Value And Action Value Are Different

In reinforcement-learning books and papers, value is usually split into two types rather than being mentioned only as one word.

| Term | English | Simple meaning |
| --- | --- | --- |
| State value | state value | How good it is overall to be in this state |
| Action value | action value | How good it is to take this action in this state |

Imagine a maze game.

- A cell right in front of the exit may have a high state value.
- But even in that cell, the action of moving toward a wall may have a low action value.

So the action value becomes especially important because `even inside a good state, there can still be bad actions`.

That difference can be read more concretely as follows.

| Scene | State-value view | Action-value view |
| --- | --- | --- |
| Arrived at the cell right before the exit | It is an advantageous location overall | `forward` can be high while `backward` can be low |
| Standing on the edge of a dangerous region | It may be close to the goal | A `shortcut` may look high, but can be low in practice because of falling risk |
| Standing next to a high-reward item | It is potentially a good state | `pick up item` can be high, while `ignore it and go around` can be lower |

So state value reads `where am I`, while action value reads `what should I do from here`. In reinforcement learning, action value is the more direct standard when actual choices are compared.

## What Does The Q-Value Write Down?

Action value is usually written as the Q-value. `Q(s, a)` means the expected long-term return when taking action `a` in state `s`.

What matters here is the interpretation more than the formula.

`The Q-value is an expected score for how acceptable the future path will be if this action is chosen in this state now.`

So a Q-table or Q-function is an attempt to answer questions like these.

- Is going upward from here a good move?
- Is going downward better?
- Even if something looks costly now, does it lead to a bigger reward later?

In a small table, it can be drawn like this.

| State | Action | Current Q-value interpretation |
| --- | --- | --- |
| Start position | Right | Relatively high because it leads toward the exit |
| Start position | Left | Low because it leads to a dead end |
| In front of the exit | Forward | High because it is close to the arrival reward |
| In front of the exit | Backward | Low because it moves farther away |

The key is that the Q-value is not just a number for `one pleasant choice right now`. Even if the immediate reward from moving one step is small, the Q-value can become high if that move leads to the exit later. On the other hand, even if there seems to be a small immediate gain, the Q-value can become low if it leads to a bigger penalty afterward.

| Visible choice | Immediate impression | The question the Q-value asks again |
| --- | --- | --- |
| An action that gives 1 point immediately | It looks good now | Does a larger penalty or dead end remain afterward? |
| An action that goes around briefly | It looks costly now | Does it lead to a larger reward later? |
| A risky shortcut | It looks like it may finish faster | Is it really favorable after adding failure cost too? |

## The Basic Loop Of Value-Based Reinforcement Learning

The core of value-based reinforcement learning is `acting, looking at the result, and slightly revising the value table in repetition`.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-01-en.mmd"
```

This diagram lets value-based reinforcement learning be read as `a loop that gradually corrects the scoreboard after seeing action outcomes`. The key is not finishing the whole policy at once, but gradually adjusting state-action values while the loop runs.

This loop is one step more concrete than the general reinforcement-learning loop seen in P4-2.3. Here, the focus is on repeatedly refining value estimates such as `Q(s, a)` instead of changing the entire policy at once.

## What Does Q-Learning Learn?

Q-learning is the best-known value-based reinforcement-learning algorithm. Its core idea is simple.

`When arriving at the next state, update the value of the current action by using the action that looks best there.`

So Q-learning updates not from `what was actually done next`, but from `what looks like the best choice in the next state`.

Because of this point, Q-learning is usually introduced as an `off-policy` algorithm.

`A way of learning by looking slightly away from the actual behavior flow and using the best-looking choice in the next state`

In a small maze example:

- Even if the reinforcement learning agent moved downward because of exploration
- The update can still revise the current value by using `the truly best action in the next state was right`

So Q-learning reflects a somewhat optimistic path that assumes `how well the reinforcement learning agent could do in the future`.

## What Does SARSA Learn?

SARSA is also a value-based reinforcement-learning algorithm. Its name comes from the initials of state, action, reward, next state, and next action.

The main idea of SARSA is similar to Q-learning, but its standard is different.

`Update the current action value by using the action that was actually chosen in the next state.`

So SARSA reflects not `the best-looking next action`, but `the action that I actually took next`.

Because of that, SARSA is usually explained as an `on-policy` algorithm.

`A way of learning inside the action pattern that I am actually following`

For example, if exploration is still mixing in somewhat risky moves, SARSA learns from the actual path that includes that exploratory tendency.

## The Difference Between Q-Learning And SARSA

Both algorithms update Q-values, but they differ in where the next value is taken from.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-02-en.mmd"
```

This diagram visually separates the difference between Q-learning and SARSA. Both look at the next state, but one corrects the value from `the next action that looks best`, while the other corrects it from `the next action that was actually taken`.

Compressed into a table:

| Item | Q-learning | SARSA |
| --- | --- | --- |
| Basis for next value | The largest Q-value in the next state | The Q-value of the action actually chosen in the next state |
| Learning attitude | Can be more optimistic | Reflects the actual behavior flow more directly |
| Description often attached | off-policy | on-policy |

Here, the feeling matters more than the terminology.

- Q-learning: reflects `the theoretically best-looking next choice`
- SARSA: reflects `the next choice that was actually taken`

If the same scene is compressed once more, the two algorithms read it differently like this.

| Same scene | Q-learning interpretation | SARSA interpretation |
| --- | --- | --- |
| The next state contains one good action and one risky action | It reflects more strongly `if the best action can be taken` | It also reflects `a risky action may actually be taken because of exploration` |
| The exploration rate is still high | It is easier to read the future optimistically | It reflects the instability of the current policy more directly |
| The environment has a high failure cost | It may be pulled faster toward the high optimum | It may reflect the losses of real mistake paths more conservatively |

## Why Does This Difference Matter?

This difference creates a difference in interpretation especially in environments that include risky actions.

Imagine a cliff next to the maze with a large penalty.

- Q-learning tends to increase values in the direction of `it is fine if the reinforcement learning agent always moves optimally`.
- SARSA can reflect more of the fact that `during exploration, the reinforcement learning agent may actually make mistakes`.

So if the current action policy is not careful, SARSA learns that lack of care together with it. For that reason, introductory texts often say that SARSA can look more conservative.

If that difference is rewritten as an operational judgment sentence, it can be read like this.

| Nature of environment | The interpretation question that comes to mind first |
| --- | --- |
| Failure cost is small and searching for the optimal route is important | `Is it right to raise the best-looking path more quickly?` |
| Exploration mistakes happen often and failure cost is large | `Is it better to reflect the instability of the actual policy together with it?` |
| It is a toy maze or a classroom simulation example | `Is it easy to explain the difference between the two algorithms through the scoreboard view?` |
| Real robots or autonomous movement make mistake cost visible | `Could optimistic value estimates hide real risk?` |

## When Should The Value-Based View Come First?

When reinforcement learning is first attached to a problem, the first question should be not the algorithm name, but `should this problem be read as a state-action scoreboard?`

| Problem scene that appears first | Why it is fine to start from the value-based view | What to guard first |
| --- | --- | --- |
| The action candidates are few and clear | The structure fits comparing the long-term score of each action | If the number of states grows, the table-based intuition becomes heavy quickly |
| Several actions are repeatedly compared in the same state | The Q-value can be attached directly to `which action is more favorable?` | Do not miss long-term reward by looking only at immediate reward |
| You want to show the difference between exploration and exploitation in an educational example | The difference between Q-learning and SARSA is easy to explain with a state-action table | A toy example should not be read immediately as the same thing as a real deployment problem |
| It is more intuitive to compare scores than to output the policy directly | Putting a value table before the policy makes the explanatory flow simpler | Continuous actions or huge state spaces quickly reveal the limit |

## Where Is It Used?

Value-based reinforcement learning gives especially clear intuition in problems where the number of states and actions is relatively clear and the result of each action can be tried repeatedly.

- Grid mazes and game movement
- Simple robot path finding
- Toy simulations of resource allocation
- Introductory examples of sequential choice problems

In practice, once the problem scale becomes large, a simple Q-table alone cannot cover the number of states. Then the flow moves toward function approximation, neural networks, and more complex policy-based methods. That bridge becomes important again in Part 4 and Part 5.

Its limits can be written more directly like this.

| Scene where the value-based approach fits well | Scene where the limit appears quickly |
| --- | --- |
| The number of states and actions is small enough to count in a table | The state space is so large that a Q-table is practically impossible to fill |
| Simulation can be repeated many times | Real-world trials are expensive or risky |
| The action candidates are discrete | The action is continuous, so direct scoreboard comparison quickly becomes difficult |
| Long-term reward is easy to explain through a scoreboard | Observation becomes complex, and value estimates alone become too weak to express the policy |

So value-based reinforcement learning is very good for building introductory intuition, but as real problems grow, it quickly runs into the limit of `how should the value table be maintained?`

## Cases And Examples

### Case 1. A Warehouse Robot Learns Through A Scoreboard Which Direction To Take At An Intersection

When a warehouse robot goes to pick up an item, the standard that is easiest for a person to write first is usually a simple rule such as `the closest path now` or `the direction that moves one cell faster right away`. But some routes may look short now while causing later congestion or larger turning cost, making them worse in the long run. Value-based reinforcement learning attaches a score to each location-action pair for `how favorable is it from now on`, so the robot gradually learns a better route. That is why, even at the same intersection, the choice that reflects later traffic flow rather than only immediate distance can gradually receive a higher Q-value.

For example, imagine that right before an intersection the robot accumulates experiences like the following.

| State | Action | Immediate result | Later effect | Why the value changes |
| --- | --- | --- | --- | --- |
| Intersection in front of shelf A | Go straight | Moves one cell faster | The next corridor is often blocked | There is an immediate gain, but long-term delay can be large |
| Intersection in front of shelf A | Turn right | Goes one cell around at first | The later corridor is wide and stable | It looks costly now, but long-term travel may be more stable |
| Intersection in front of shelf A | Turn left | Pays a turning cost | Enters a collision-risk zone | The value can fall after failure cost is included |

The key shown by this table is that `the action that looks shortest now` and `the action that is most favorable in the long run` can be different. Value-based reinforcement learning is precisely an approach that tries to read that difference by accumulating numbers.

```mermaid
--8<-- "assets/part-04/chapter-19/p4-19-1-mermaid-03-en.mmd"
```

If this case is compressed like a review memo, it can be written as follows.

| Current state | Action candidates | Failure costs that should be seen together | Next question |
| --- | --- | --- | --- |
| Right before entering the intersection | Left, right, straight | Blocked corridor, turning delay, collision risk | Is the highest Q-value also the safest path in practice? |
| A crowded region where exploration is mixed in | An action that looks shortest, an action that detours | Exploration can create larger bottlenecks or collisions | Should the actual policy flow be reflected more than an optimistic update? |

The observable result of this case appears when comparing whether `straight looked faster at first` but, after repeated experience, `the detour route gets a higher Q-value`, and whether the delay and collision pattern left by choosing straight keeps repeating. In other words, the value-based interpretation is not about `which direction looked fast`, but about `which direction's long-term score rose more through actual experience`.

### Case 2. When A Fast Path And A Safe Path Split Beside A Cliff

Suppose a reinforcement learning agent has two paths toward the goal. The standard that is easiest for a person to use first is usually `the shortest path to arrival` or `the path where reward rises quickly right now`. So a cliff-side corridor with a fast route and a large nearby penalty can look better at first. But in reinforcement learning, `long-term reward including the chance of mistakes` must be read together. Here, Q-learning can keep the value of the fast path relatively high because it reflects more strongly `if the agent can move optimally in the next state`. By contrast, SARSA reflects more directly the route where cliff-side mistakes are mixed in during exploration, so it may read the safer detour route as better.

| Same route-choice problem | Interpretation that may appear first in Q-learning | Interpretation that may appear first in SARSA |
| --- | --- | --- |
| A fast but risky shortcut | It could be favorable if movement stays optimal | The risk cost is large once exploratory mistakes are included |
| A slow but safe detour | Its immediate efficiency looks lower | It may be more stable under the actual policy |

The observable result of this case appears when comparing how often the cliff penalty is actually accumulated on the fast shortcut, whether the safe detour ends with a higher Q-value after repeated learning, and whether the preference gap between the two algorithms grows larger as the exploration rate stays high. So this case helps the reader interpret the algorithmic difference not through formulas, but through `how directly is the possibility of mistakes reflected in the value estimate?`

### Case 3. When A Customer-Support Bot Learns Different Values Between Fast Closure And Safe Resolution

When a customer-support bot receives an inquiry, the easiest standard for a person to use first is usually an immediate efficiency metric such as `average handling time` or `does it close quickly in one shot`. So among `close the response immediately`, `ask an additional question`, and `handoff to a human agent`, the action that uses the least time right away can look best. But in reality, unresolved inquiries may come back again or customer dissatisfaction may grow. By contrast, handing off to a human agent may look costly immediately, yet help reduce repeat contacts and preserve satisfaction in the long run.

This scene makes clearer why the value-based view is necessary. Instead of writing the policy in sentences ahead of time, the system must learn as values `how acceptable is each state-action pair in the long run`.

| Support state | Action candidates | Immediate impression | What must be reviewed again in the long run |
| --- | --- | --- | --- |
| An early state that looks like a simple inquiry | Close immediately | It is efficient because handling time is short | Whether it was actually resolved and whether repeat contacts occur |
| A state with insufficient information | Ask an additional question | The conversation gets longer right now | Whether wrong answers drop and the resolution rate improves |
| A state where dissatisfaction is rising | Handoff to a human agent | The immediate cost is large | Whether it prevents churn and preserves satisfaction |

This case shows that the Q-value is not just a speed score, but a device for reading `how does the current action change the later state and reward flow?`

The observable result of this case appears when comparing whether follow-up costs such as repeat contacts, dissatisfaction, and repeated human intervention keep growing in states where immediate closure is common, and whether actions such as asking more questions or handing off to a human actually create higher long-term reward. So the value-based view records as a score not `does it close quickly now`, but `how does this action change the next state and later cost?`

## Practice And Example

This example focuses on confirming numerically that `Q-learning` and `SARSA` read the same experience a little differently.

Problem situation:

- Even from the same reward experience, Q-learning and SARSA can produce different update results because their rule for taking the next value is different

Input:

- Current state `S0`
- Current action `right`
- Immediate reward `+1`
- Next state `S1`
- Current values in the Q-table

Expected output:

- The update result computed by Q-learning
- The update result computed by SARSA
- The before-and-after values that make the difference between the two methods visible

Concepts to confirm:

- Q-learning corrects the current value by using the action value that looks best in the next state
- SARSA corrects the current value by using the action value of the action actually taken next
- Even the same experience can lead to different learning attitudes when the update rule is different

```python
# This example compares how Q-learning and SARSA update differently because they read the next value differently.
alpha = 0.5
gamma = 0.9

q_table = {
    ("S0", "right"): 0.40,
    ("S1", "up"): 0.80,
    ("S1", "down"): 0.30,
}

state = "S0"
action = "right"
reward = 1.0
next_state = "S1"
actual_next_action = "down"

old_value = q_table[(state, action)]

# Q-learning: use the largest value in the next state
best_next_value = max(
    q_table[(next_state, "up")],
    q_table[(next_state, "down")],
)
q_learning_target = reward + gamma * best_next_value
q_learning_updated = old_value + alpha * (q_learning_target - old_value)

# SARSA: use the value of the action actually taken next
actual_next_value = q_table[(next_state, actual_next_action)]
sarsa_target = reward + gamma * actual_next_value
sarsa_updated = old_value + alpha * (sarsa_target - old_value)

print("old Q(S0, right) =", round(old_value, 3))
print("Q-learning target =", round(q_learning_target, 3))
print("Q-learning updated =", round(q_learning_updated, 3))
print("SARSA target =", round(sarsa_target, 3))
print("SARSA updated =", round(sarsa_updated, 3))
```

The execution result can be read like this.

```text
old Q(S0, right) = 0.4
Q-learning target = 1.72
Q-learning updated = 1.06
SARSA target = 1.27
SARSA updated = 0.835
```

The important point is that even though both algorithms started from the same current experience, the result changed because the rule for reading the next value was different.

- Q-learning used the value `0.8` of `up`, which looked best in `S1`.
- SARSA used the value `0.3` of `down`, which was the action actually chosen in `S1`.

That is why the Q-learning update rose more.

### Try Changing One Value: If The Actual Next Action Changes, How Much Does The Update Attitude Change?

Now keep the current experience the same, but change only the actual next action in the next state to `up`.

```python
# This example changes the actual next action in SARSA to see how the update gap between Q-learning and SARSA narrows.
alpha = 0.5
gamma = 0.9

q_table = {
    ("S0", "right"): 0.40,
    ("S1", "up"): 0.80,
    ("S1", "down"): 0.30,
}

state = "S0"
action = "right"
reward = 1.0
next_state = "S1"
actual_next_action = "up"

old_value = q_table[(state, action)]
best_next_value = max(
    q_table[(next_state, "up")],
    q_table[(next_state, "down")],
)
q_learning_target = reward + gamma * best_next_value
q_learning_updated = old_value + alpha * (q_learning_target - old_value)

actual_next_value = q_table[(next_state, actual_next_action)]
sarsa_target = reward + gamma * actual_next_value
sarsa_updated = old_value + alpha * (sarsa_target - old_value)

print("Q-learning updated =", round(q_learning_updated, 3))
print("SARSA updated =", round(sarsa_updated, 3))
```

```text
Q-learning updated = 1.06
SARSA updated = 1.06
```

In the first run, the actual next action was `down`, so SARSA updated more conservatively. But once the actual next action is changed to `up`, SARSA produces the same value as Q-learning. In other words, the difference between the two methods is less about memorizing names than about how directly the update reflects `what action the policy actually continues with`.

This comparison exercise shows that even under the same reward, the learning result can change when the actual next action changes. So the evaluation criterion should include not only average reward, but also exploration cost, failure risk, and the policy's real action flow. The key is not the name of the Q-learning formula, but reading the reason the value changed as a difference in the update standard.

### Judge For Yourself

Choose first which interpretation is safer for the observations below.

| Observation | Hasty conclusion | Safer interpretation |
| --- | --- | --- |
| The Q-learning value rose more from the same current experience | Q-learning is always the better algorithm | It updated more optimistically because it used the value that looked best in the next state |
| The SARSA value was updated by a smaller amount | SARSA cannot really learn | It may have reflected the actual next action and exploration flow more directly |
| When the actual next action changed to `up`, the two values became equal | The difference between the two algorithms is not very important | The difference was not the names, but `where the next value was read from` |

The purpose of this table is not to choose which algorithm is superior. It is to build the habit of reading first `what update standard was operating` even when the same numbers are shown.

| Common recording language | What to record immediately from this exercise |
| --- | --- |
| Visible structure | Even from the same reward experience, the Q-learning and SARSA updates split depending on the actual next action |
| Interpretation boundary | A high Q-value or a large update does not immediately mean a safe policy |
| Next question | If reward, exploration rate, or failure cost changes, which update attitude fits better? |

This Section also should not leave value explanation alone. It should record together which state-action candidates and which failure costs were placed side by side. Even if two cases look like the same high Q-value, one state may repeat safely while another state may leave larger exploration cost and failure loss, so the review memo must remain together.

| Item to leave together | What this Section writes | Why it is needed |
| --- | --- | --- |
| State-action candidates | The action candidates being compared in the current state | To make clear what the value table is actually comparing |
| Cumulative reward standard | What is being treated as good in the long run rather than only right now | To show that the Q-value is not a short-term scoreboard |
| Failure cost | The loss created by wrong exploration or a detour route | To ask whether a high value is also safe in real operation |
| Next adjustment question | Whether an optimistic update or a conservative update fits better | To carry the difference between Q-learning and SARSA into the next experiment standard |

The core of this Section is not memorizing two algorithm names, but reading with what attitude the value table is updated.

| What must be read together | The question read first in this Section | Where it connects immediately next |
| --- | --- | --- |
| State value and action value | What kind of goodness is being written as a score? | Value-table interpretation and Q-value comparison |
| Difference between Q-learning and SARSA | Which is used as the standard: the best-looking next action or the actual next action? | P4-19.2 Policy-Based Reinforcement Learning |
| Real-world flow mixed with exploration | How optimistic or conservative is this update rule? | P4-19.3 Deployment risk and exploration cost |
| Failure cost | Can a high-value action also be borne in the real environment? | Risk review before applying reinforcement learning |

## Checklist

- Can you explain value-based reinforcement learning as an approach that learns the long-term goodness of states and actions as values?
- Can you distinguish state value and action value, and explain why action value is more direct for choosing an action?
- Can you explain the Q-value as an expected score for `how acceptable the future will be if this action is taken in this state`?
- Can you explain why Q-learning and SARSA can produce different values even from the same experience?
- Can you explain why the value-based view comes to mind first in problems where action candidates are few and comparable?
- Do you understand that a high Q-value does not immediately mean safety in real-world deployment?

## Sources And References

- Richard S. Sutton and Andrew G. Barto, `Reinforcement Learning: An Introduction`, 2nd ed., The MIT Press, 2018, checked on 2026-06-27. [https://mitpress.mit.edu/9780262039246/reinforcement-learning/](https://mitpress.mit.edu/9780262039246/reinforcement-learning/){: target="_blank" rel="noopener noreferrer" }
- Christopher J. C. H. Watkins, Peter Dayan, `Q-learning`, Machine Learning, 1992, checked on 2026-06-27. [https://link.springer.com/article/10.1007/BF00992698](https://link.springer.com/article/10.1007/BF00992698){: target="_blank" rel="noopener noreferrer" }
- Satinder Singh, Tommi Jaakkola, Michael L. Littman, Csaba Szepesvari, `Convergence Results for Single-Step On-Policy Reinforcement-Learning Algorithms`, Machine Learning, 2000, checked on 2026-06-27. [https://link.springer.com/article/10.1023/A:1022689125041](https://link.springer.com/article/10.1023/A:1022689125041){: target="_blank" rel="noopener noreferrer" }
