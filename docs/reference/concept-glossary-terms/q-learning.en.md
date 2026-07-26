<a id="q-learning"></a>

## Q-learning

- Meaning: Q-learning is a value-based reinforcement-learning algorithm that updates a state-action value using the best-looking Q-value in the next state. It learns from the best available next action rather than only from the action actually taken next.
- Why it matters: Q-learning is a representative off-policy example. It makes the contrast with SARSA clear: Q-learning updates from the best-looking next action, while SARSA updates from the next action actually chosen.
- Related concepts: `Q-value`, `SARSA`, `off-policy`, `value-based reinforcement learning`
- Core Section: `P4-19.1`
- Appears in: `P4-19.5`
