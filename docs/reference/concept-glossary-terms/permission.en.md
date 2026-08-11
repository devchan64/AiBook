<a id="permission"></a>

## tool execution permission

- Meaning: Tool execution permission is the executable scope allowed for a tool or action. The same capability can have different permission levels, such as read-only access, write access, or the ability to cause real external changes. Permission defines a boundary before execution and is separate from approval, which asks whether a specific action should proceed now.
- Why it matters: The same tool call can carry different risk depending on whether it reads, writes, or deploys. This concept separates `can execute` from `is allowed to execute`, which clarifies operational judgment and responsibility. It also explains why permission boundaries and approval steps are both needed.
- Related concepts: `least privilege`, `tool use`, `security`, `accountability`
- Core Section: `P7-6.2`
- Appears in: `P6-14.1`, `P6-16.2`, `P6-18.2`, `P7-6.1`
