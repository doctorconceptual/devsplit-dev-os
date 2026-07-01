# DevSplit Laravel Engineering Handbook

**Document:** Actions

---

# Purpose

An Action represents one business use case.

One Action = One responsibility.

---

# Responsibilities

Actions coordinate workflows.

Actions may:

- Call Services
- Dispatch Jobs
- Dispatch Events
- Return results

---

# Avoid

Actions should not:

- Perform SQL directly
- Handle HTTP
- Render views

---

# Naming

```
CreateInvoiceAction

PublishPostAction

ApproveUserAction
```

---

# Best Practices

- One public method.
- Small.
- Focused.
- Easy to test.

---

# AI Notes

When adding features:

Create new Actions rather than expanding existing ones beyond their responsibility.

---

# Checklist

✓ One use case?

✓ Reusable?

✓ Small?