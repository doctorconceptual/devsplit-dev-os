# DevSplit Laravel Engineering Handbook

**Document:** Controllers

---

# Purpose

Controllers coordinate incoming requests.

Controllers are orchestration layers.

Nothing more.

---

# Responsibilities

Controllers should:

- Receive requests
- Authorize
- Call an Action
- Return a response

---

# Avoid

Controllers should never contain:

- Business logic
- SQL
- Calculations
- Long methods
- Complex conditionals

---

# Example

```
StoreOrderController

↓

CreateOrderAction
```

---

# Best Practices

- Keep methods short.
- One endpoint = one action.
- Use Form Requests.
- Return Resources for APIs.

---

# Common Mistakes

❌ Business logic

❌ Eloquent queries

❌ Validation

❌ Calculations

---

# AI Notes

When adding functionality:

Do not increase controller complexity.

Move logic into Actions.

---

# Checklist

✓ Thin?

✓ Calls Action?

✓ Returns Response?

✓ No business logic?