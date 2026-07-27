<a id="approval-policy"></a>

## approval policy

- Meaning: An approval policy defines which actions may run automatically, which require human approval, and which should be held or blocked. It is a reusable operating rule rather than a one-time yes-or-no decision.
- Why it matters: The risk of the same tool changes with context. Reading a file, modifying a file, running a test, and changing production state should not be governed by the same default. Approval policies keep automation consistent and make scope, logs, and hold states part of the system design.
- Related concepts: `approval`, `permission`, `scope`, `hold state`, `trace`
- Core Section: `P7-6.3`
- Appears in: `P1-14.5`, `P7-6.1`, `P7-6.2`
