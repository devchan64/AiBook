<a id="q-value"></a>

## Q-value

- Meaning: A Q-value is the action value for taking action `a` in state `s`, often written as `Q(s, a)`. It scores how good the future is expected to be if that action is chosen now in that state.
- Why it matters: Q-learning and SARSA both update Q-values, but they read the next value from different places. Q-value is therefore the main handle for comparing value-based reinforcement-learning updates.
- Related concepts: `action value`, `Q-learning`, `SARSA`, `value-based reinforcement learning`
- Core Section: `P4-19.1`
- Appears in: `P4-19.5`
