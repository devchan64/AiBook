## observation

- Meaning: An observation is new information or a result obtained after taking an action. In reinforcement learning it may be the next screen, number, or signal returned by the environment. In a service-style AI agent, it can be a search result, error message, file content, or test output used for the next decision.
- Why it matters: In multi-step problems, what is learned after an action can immediately change the next action or the decision to stop. Search results, error messages, tool outputs, and test results all update state and reshape the plan. This concept helps frame AI agent execution as a repeated cycle of action, observation, and selection rather than a single answer.
- Related concepts: `AI agent`, `state`, `action`
- Core Section: `P1-14.3`
- Appears in: `P1-14.4`, `P1-14.5`
