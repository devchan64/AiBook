<a id="actor-critic"></a>

## actor-critic

- Meaning: Actor-critic is a reinforcement-learning structure that uses an actor to produce actions and a critic to evaluate how good those actions were. It adjusts the policy while using value-estimation signals for feedback.
- Why it matters: It makes policy-based and value-based ideas read as cooperating roles rather than only competing families. The critic helps stabilize policy updates by giving an evaluation signal.
- Related concepts: `policy-based reinforcement learning`, `policy gradient`, `value-based reinforcement learning`
- Core Section: `P4-19.2`
- Appears in: `P4-19.4`, `P4-19.6`
