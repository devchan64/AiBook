## policy-based reinforcement learning

- Meaning: Policy-based reinforcement learning directly adjusts the policy that chooses actions instead of first building a scoreboard of values for states or actions. It is closer to changing the behavior rule itself than to calculating a value and then choosing from it. Updating policy parameters in a direction that increases expected reward is a representative submethod of this approach.
- Why it matters: This concept lets readers separate value-based methods from policy-based methods inside reinforcement learning. It also explains why directly adjusting the policy is natural for continuous actions, stochastic action choices, and methods that update a policy with help from value estimates.
- Related concepts: `reinforcement learning`, `policy`, `expected reward`
- Core Section: `P4-19.2`
- Appears in: `P4-2.3`, `P4-19.3`, `P4-19.4`
