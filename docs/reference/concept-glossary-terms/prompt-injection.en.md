<a id="prompt-injection"></a>

## prompt injection

- Meaning: Prompt injection is an attack in which hidden instructions in user input or external documents try to override or bypass the original system instructions and cause unintended model or reinforcement learning AI agent behavior. The key risk is that text that appears to be content can act as an instruction that changes behavior.
- Why it matters: In AI systems connected to search, browsing, file reading, or tool use, external documents can become inputs for action decisions. A hidden instruction can therefore lead to permission abuse or information leakage. This concept explains why least privilege, approvals, execution boundaries, and logs are needed alongside model capability.
- Related concepts: `security`, `least privilege`, `permission`, `retrieval-augmented generation, RAG`, `tool use`
- Core Section: `P1-15.3`
- Appears in: `P1-10.3`, `P1-14.2`, `P1-14.4`, `P1-14.5`
