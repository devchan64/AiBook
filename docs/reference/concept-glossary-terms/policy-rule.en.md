<a id="policy-rule"></a>
<a id="glossary-policy-rule"></a>

### policy rule

- Meaning: A policy rule is an operational rule that turns a model score or category output into an actual action. Examples include `review if above 0.8`, `inspect only the top 10%`, or `auto-handle low-risk cases`.
- Why it matters: A model output is not automatically the business action. This concept separates the fact that a score was produced from the rule that decides how the score is used. Changing the policy rule can change review load, automation scope, and the balance between false alarms and missed cases without retraining the model.
- Related concepts: `model score`, `threshold`, `action`, `review queue`
- Core Section: `P3-9.8`
- Appears in: `P3-9.8`
