## permission

- Meaning: Permission is the executable scope allowed for a tool or action. The same capability can have different permission levels, such as read-only access, write access, or the ability to cause real external changes. Permission defines a boundary before execution and is separate from approval, which asks whether a specific action should proceed now.
- Why it matters: The same tool call can carry different risk depending on whether it reads, writes, or deploys. This concept separates `can execute` from `is allowed to execute`, which clarifies operational judgment and responsibility. It also explains why permission boundaries and approval steps are both needed.
- Related concepts: `approval`, `tool use`, `trace`, `accountability`
- Core Section: `P7-6.2`
- Appears in: `P6-13.1`, `P6-15.2`, `P6-17.2`, `P7-6.1`
