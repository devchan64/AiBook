<a id="action"></a>

## action

- Meaning: An action is something an agent actually chooses and executes in a given state. In search or reinforcement learning it changes the environment; in a service agent it may mean searching, reading a file, calling an API, editing a document, or reporting a result.
- Why it matters: Actions are where reasoning turns into state change. The available action set controls what the agent can accomplish, what risks it can create, and what observations it can gather next. This concept helps separate internal computation from external execution, and it makes clear why tool permissions and action design matter for both capability and safety.
- Related concepts: `state`, `policy`, `reward`, `observation`
- Core Section: `P1-8.3`
- Appears in: `P1-7.1`, `P1-14.3`
